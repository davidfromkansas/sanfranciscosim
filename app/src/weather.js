// The city's weather, as a field the shaders can sample.
//
// Polls /api/weather (see api/_lib/feeds/weather.mjs) and keeps a 6x6 grid of
// conditions over the city in a DataTexture. Materials read it by world
// position, so fog sits over the Sunset while the Mission stays clear — a
// single citywide number cannot do that, and the gradient is the feature
// (docs/plans/WEATHER-PLAN.md §1).
//
// Nothing here throws into the frame loop. No feed, a broken payload, or a
// dead network all degrade to the last good field, or to a neutral fair day if
// there never was one — iron rule 3, applied to weather.

import { ClampToEdgeWrapping, DataTexture, LinearFilter, RGBAFormat, Vector2 } from 'three';
import { shared } from './env.js';

const ENDPOINT = '/api/weather';
const POLL_MS = 5 * 60 * 1000;
const POLL_JITTER_MS = 15 * 1000;
const RETRY_MS = 60 * 1000;
// A 5-minute poll that teleports the fog in one frame looks broken; the same
// change eased over a minute looks like weather.
const EASE_S = 60;

const W = 6;
const H = 6;
const CELLS = W * H;

const DEG = Math.PI / 180;
const clamp01 = (v) => (v < 0 ? 0 : v > 1 ? 1 : v);

// A neutral fair day: what the city looks like when we have never once heard
// from the feed. Deliberately pleasant and unremarkable.
const NEUTRAL = {
  cloudLow: 0.35,
  cloudHigh: 0.2,
  fog: 0.08,
  precip: 0,
  windSpeed: 5.4, // m/s, ~12 mph
  windDir: 270, // from the west, as it almost always is
  aqi: 20,
};

const field = (value) => new Float32Array(CELLS).fill(value);

// Visibility (metres) -> a fog density the shader can use directly. Calibrated
// so 20 km reads as clean air and 1 km is a genuine white-out.
function fogFromVisibility(metres) {
  const v = Math.max(50, metres);
  return clamp01((1 / v - 1 / 20000) * 12000);
}

// Rain intensity from mm in the reporting interval. 0.1 mm is a drizzle you can
// just see; 5 mm is a downpour.
const rainFromPrecip = (mm) => clamp01(Math.sqrt(Math.max(0, mm) / 5));

// Meteorological direction (degrees the wind blows FROM) to a world vector in
// the direction it blows TOWARDS. World frame is +x east, -z north, so a wind
// from 270 (the west) must come out as +x.
function windVector(degFrom, speed, out) {
  const toward = (degFrom + 180) * DEG;
  return out.set(Math.sin(toward) * speed, -Math.cos(toward) * speed);
}

export function createWeather({ project }) {
  // Two copies of every field: what is on screen, and what the feed last said.
  // Every frame eases current towards target.
  const current = {
    cloudLow: field(NEUTRAL.cloudLow),
    cloudHigh: field(NEUTRAL.cloudHigh),
    fog: field(NEUTRAL.fog),
    precip: field(NEUTRAL.precip),
  };
  const target = {
    cloudLow: field(NEUTRAL.cloudLow),
    cloudHigh: field(NEUTRAL.cloudHigh),
    fog: field(NEUTRAL.fog),
    precip: field(NEUTRAL.precip),
  };
  const scalars = {
    current: { windSpeed: NEUTRAL.windSpeed, windDir: NEUTRAL.windDir, aqi: NEUTRAL.aqi },
    target: { windSpeed: NEUTRAL.windSpeed, windDir: NEUTRAL.windDir, aqi: NEUTRAL.aqi },
  };

  // RGBA per cell: R fog, G low cloud, B rain, A high cloud. LinearFilter means
  // the GPU does the spatial interpolation between cells for free.
  const data = new Uint8Array(CELLS * 4);
  const texture = new DataTexture(data, W, H, RGBAFormat);
  texture.minFilter = LinearFilter;
  texture.magFilter = LinearFilter;
  texture.wrapS = ClampToEdgeWrapping;
  texture.wrapT = ClampToEdgeWrapping;
  texture.needsUpdate = true;

  // Live summary for the clock card and the debug hook; null until a feed lands.
  // `live` means "we have usable data", NOT "the last fetch succeeded" — a
  // blip must never blank a reading we are still perfectly able to show.
  let summary = null;
  let staleSince = 0;
  let override = null;
  let nextPollAt = 0;
  let warned = false;
  let grid = null;

  // World-space bbox of the grid, so a shader can turn a world position into a
  // UV. Uses the app's one projection function — never re-derived here.
  const origin = new Vector2();
  const scale = new Vector2(1, 1);
  const wind = new Vector2();

  function setGrid(g) {
    grid = g;
    // Row 0 of the field is the NORTH row, and north is -z, so the texture's
    // v axis runs from the north-west corner southwards.
    const [x0, z0] = project(g.lon0, g.lat1);
    const [x1, z1] = project(g.lon1, g.lat0);
    origin.set(x0, z0);
    // Guard against a degenerate bbox producing a divide by zero in the shader.
    scale.set(1 / (x1 - x0 || 1), 1 / (z1 - z0 || 1));
    shared.uWeatherOrigin.value.copy(origin);
    shared.uWeatherScale.value.copy(scale);
  }

  function uploadTexture() {
    for (let i = 0; i < CELLS; i++) {
      data[i * 4] = current.fog[i] * 255;
      data[i * 4 + 1] = current.cloudLow[i] * 255;
      data[i * 4 + 2] = current.precip[i] * 255;
      data[i * 4 + 3] = current.cloudHigh[i] * 255;
    }
    texture.needsUpdate = true;
  }

  function applyPayload(payload) {
    if (!payload?.live || !payload.grid || !Array.isArray(payload.cloudLow)) return false;
    const g = payload.grid;
    if (g.w !== W || g.h !== H || payload.cloudLow.length !== CELLS) return false;
    if (!grid) setGrid(g);

    for (let i = 0; i < CELLS; i++) {
      target.cloudLow[i] = clamp01(payload.cloudLow[i] / 100);
      target.cloudHigh[i] = clamp01((payload.cloudMid[i] + payload.cloudHigh[i]) / 200);
      target.fog[i] = fogFromVisibility(payload.visibility[i]);
      target.precip[i] = rainFromPrecip(payload.precip[i]);
    }
    // mph to m/s: the scene works in metres.
    scalars.target.windSpeed = (payload.summary?.windSpeed ?? 12) * 0.44704;
    scalars.target.windDir = payload.summary?.windDir ?? 270;
    scalars.target.aqi = payload.summary?.aqi ?? 0;
    summary = payload.summary || null;
    staleSince = 0;
    return true;
  }

  async function poll() {
    try {
      const res = await fetch(ENDPOINT, { headers: { accept: 'application/json' } });
      if (!res.ok) throw new Error(String(res.status));
      const payload = await res.json();
      if (!applyPayload(payload)) {
        // A live-but-empty feed is not an error: the endpoint answers
        // { live: false } without upstream data, and the city carries on with
        // whatever it last knew.
        if (!staleSince) staleSince = Date.now();
        nextPollAt = Date.now() + RETRY_MS;
        return;
      }
      nextPollAt = Date.now() + POLL_MS + Math.random() * POLL_JITTER_MS;
    } catch (error) {
      if (!warned) {
        warned = true;
        console.warn('weather: feed unavailable, holding the last known sky', error);
      }
      if (!staleSince) staleSince = Date.now();
      nextPollAt = Date.now() + RETRY_MS;
    }
  }

  // Fetching is wall-clock work, not frame work, so it runs on its own timer —
  // the same reason the clock does. Driving it from the render loop would mean
  // a backgrounded tab (where rAF stops entirely) never refreshes, then snapped
  // on return; it would also stall whenever the GPU does.
  function tick() {
    if (Date.now() < nextPollAt) return;
    nextPollAt = Date.now() + RETRY_MS; // claim the slot so we never stack requests
    poll();
  }

  // Ease every field towards the target. Frame-rate independent, no allocation.
  function update(dt) {
    const k = 1 - Math.exp(-dt / EASE_S);
    let moved = false;
    for (const key of ['cloudLow', 'cloudHigh', 'fog', 'precip']) {
      const from = current[key];
      const to = target[key];
      for (let i = 0; i < CELLS; i++) {
        const delta = to[i] - from[i];
        if (delta > 0.0005 || delta < -0.0005) {
          from[i] += delta * k;
          moved = true;
        }
      }
    }
    const s = scalars.current;
    const t = scalars.target;
    s.windSpeed += (t.windSpeed - s.windSpeed) * k;
    s.aqi += (t.aqi - s.aqi) * k;
    // Directions wrap: always turn the short way round the compass.
    let turn = ((t.windDir - s.windDir + 540) % 360) - 180;
    s.windDir = (s.windDir + turn * k + 360) % 360;

    windVector(s.windDir, s.windSpeed, wind);
    shared.uWind.value.copy(wind);
    // Mean rain and smoke, for the systems that do not need the field.
    let rain = 0;
    for (let i = 0; i < CELLS; i++) rain += current.precip[i];
    shared.uRain.value = rain / CELLS;
    shared.uSmoke.value = clamp01((s.aqi - 80) / 170);

    // 36 texels is free, but not free enough to upload for nothing.
    if (moved) uploadTexture();
  }

  // Sample the eased field at a world position — for the UI and the concierge,
  // which cannot read a texture. Bilinear, matching what the GPU does.
  function sampleAt(x, z, key = 'fog') {
    const u = clamp01((x - origin.x) * scale.x) * (W - 1);
    const v = clamp01((z - origin.y) * scale.y) * (H - 1);
    const c0 = Math.floor(u);
    const r0 = Math.floor(v);
    const c1 = Math.min(W - 1, c0 + 1);
    const r1 = Math.min(H - 1, r0 + 1);
    const fu = u - c0;
    const fv = v - r0;
    const f = current[key];
    const top = f[r0 * W + c0] * (1 - fu) + f[r0 * W + c1] * fu;
    const bottom = f[r1 * W + c0] * (1 - fu) + f[r1 * W + c1] * fu;
    return top * (1 - fv) + bottom * fv;
  }

  shared.uWeatherField.value = texture;
  uploadTexture();
  // The city boots first; the weather lands a moment later and eases in.
  nextPollAt = 0;
  const timer = setInterval(tick, 5000);
  tick();

  return {
    update,
    dispose() {
      clearInterval(timer);
    },
    sampleAt,
    texture,
    // We have something worth showing. A reading an hour old still beats no
    // reading; past that horizon the card drops rather than lie.
    get live() {
      return summary !== null && (!staleSince || Date.now() - staleSince < 60 * 60 * 1000);
    },
    get summary() {
      return summary;
    },
    get wind() {
      return wind;
    },
    // A debug override must move the readout too, or the smoke preset can never
    // be checked against the card — so while one is active the card reports the
    // commanded value rather than waiting out the 60 s ease.
    get aqi() {
      return override ? scalars.target.aqi : scalars.current.aqi;
    },
    // Debug only (no UI, no URL parameter) — the same contract as SF.setClock.
    // A partial patch merges onto the live field; null returns to live.
    setOverride(patch) {
      override = patch;
      if (patch === null || patch === undefined) {
        nextPollAt = 0;
        return null;
      }
      const preset = PRESETS[patch.preset] || {};
      const merged = { ...preset, ...patch };
      if (merged.fog !== undefined) target.fog.fill(clamp01(merged.fog));
      if (merged.cloud !== undefined) target.cloudLow.fill(clamp01(merged.cloud));
      if (merged.cloudHigh !== undefined) target.cloudHigh.fill(clamp01(merged.cloudHigh));
      if (merged.precip !== undefined) target.precip.fill(clamp01(merged.precip));
      if (merged.windSpeed !== undefined) scalars.target.windSpeed = merged.windSpeed;
      if (merged.windDir !== undefined) scalars.target.windDir = merged.windDir;
      if (merged.aqi !== undefined) scalars.target.aqi = merged.aqi;
      // A west-heavy gradient, so 'karl' looks like Karl and not like a bathtub.
      if (merged.gradient) {
        for (let r = 0; r < H; r++) {
          for (let c = 0; c < W; c++) {
            const west = 1 - c / (W - 1);
            target.fog[r * W + c] = clamp01(merged.fog * (0.15 + 0.85 * west * west));
            target.cloudLow[r * W + c] = clamp01((merged.cloud ?? merged.fog) * (0.2 + 0.8 * west));
          }
        }
      }
      // Never wait for the poll to undo a deliberate override.
      nextPollAt = Date.now() + POLL_MS;
      return merged;
    },
    get override() {
      return override;
    },
    // Live state, for SF.weather.
    snapshot() {
      return {
        live: this.live,
        stale: staleSince > 0,
        summary,
        override,
        wind: { speed: scalars.current.windSpeed, dir: Math.round(scalars.current.windDir) },
        aqi: Math.round(scalars.current.aqi),
        mean: {
          fog: mean(current.fog),
          cloudLow: mean(current.cloudLow),
          cloudHigh: mean(current.cloudHigh),
          precip: mean(current.precip),
        },
      };
    },
  };
}

const mean = (a) => {
  let sum = 0;
  for (let i = 0; i < a.length; i++) sum += a[i];
  return Number((sum / a.length).toFixed(3));
};

// The canonical demo states. Storms and pea-soupers are rare, so they must be
// producible on a clear August afternoon or they can never be QA'd.
const PRESETS = {
  clear: { fog: 0.02, cloud: 0.05, cloudHigh: 0.1, precip: 0, aqi: 15 },
  karl: { fog: 0.85, cloud: 0.95, cloudHigh: 0.2, precip: 0, windSpeed: 7, windDir: 260, gradient: true },
  storm: { fog: 0.35, cloud: 1, cloudHigh: 0.9, precip: 0.85, windSpeed: 18, windDir: 200 },
  smoke: { fog: 0.45, cloud: 0.15, cloudHigh: 0.3, precip: 0, aqi: 240, windSpeed: 3 },
};
