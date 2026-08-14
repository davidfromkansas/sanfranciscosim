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
const SAT_ENDPOINT = '/api/satfog';
// How much the satellite reshapes the model's fog. The model (HRRR) is an
// hourly FORECAST with real units -- it knows how foggy, in metres of
// visibility. The satellite is a five-minute OBSERVATION with no units -- it
// knows where, and nothing else. So the blend takes magnitude from the model
// and shape from the observation, and stays a minority partner: a satellite
// sees cloud TOPS, and high cirrus over a clear city reads cold too.
const SAT_WEIGHT = 0.4;
const POLL_MS = 5 * 60 * 1000;
const POLL_JITTER_MS = 15 * 1000;
const RETRY_MS = 60 * 1000;
// A 5-minute poll that teleports the fog in one frame looks broken; the same
// change eased over a minute looks like weather.
const EASE_S = 60;
// Ground wets fast and dries slow. A street that dries the moment the shower
// stops looks wrong; ninety seconds of drying is most of what sells rain.
const WET_UP_S = 12;
const WET_DOWN_S = 90;
// Storms only: a flash every 8-25 s, two frames long.
const FLASH_MIN_S = 8;
const FLASH_MAX_S = 25;

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
  // The last good payload, kept so clearing an override can restore the live
  // field immediately instead of leaving the scene on the override until the
  // next poll lands (up to a minute later).
  let lastPayload = null;
  // Longitude -> observed cloud-top score, from the satellite transect.
  let satCurve = null;
  let nextPollAt = 0;
  let wetness = 0;
  let flashUntil = 0;
  let nextFlashAt = 0;
  let flashSeed = 1;
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
    lastPayload = payload;
    staleSince = 0;
    applySatellite(g);
    return true;
  }

  // The satellite is best-effort in the strictest sense: it refines the fog's
  // shape and nothing depends on it. A failure leaves the model's own field
  // exactly as it was.
  async function pollSatellite() {
    try {
      const res = await fetch(SAT_ENDPOINT, { headers: { accept: 'application/json' } });
      if (!res.ok) throw new Error(String(res.status));
      const payload = await res.json();
      if (!payload?.live || !payload.usable || !payload.cloudTopScore) {
        satCurve = null;
        return;
      }
      // The samples are a west-to-east transect, so collapse them to a curve in
      // longitude: the marine layer boundary runs north-south, and it is the
      // east-west profile that carries the signal.
      const LON = {
        Ocean: -122.52, Sunset: -122.4869, 'Golden Gate': -122.4783, Richmond: -122.4803,
        'Twin Peaks': -122.4477, Downtown: -122.4, Mission: -122.4148, Bayview: -122.39,
      };
      const points = Object.entries(payload.cloudTopScore)
        .filter(([name, v]) => v !== null && LON[name] !== undefined)
        .map(([name, v]) => [LON[name], v])
        .sort((a, b) => a[0] - b[0]);
      satCurve = points.length >= 3 ? points : null;
    } catch {
      satCurve = null;
    }
  }

  // Sample the transect at a longitude, linearly between its two nearest points.
  function satAt(lon) {
    if (!satCurve) return null;
    if (lon <= satCurve[0][0]) return satCurve[0][1];
    if (lon >= satCurve[satCurve.length - 1][0]) return satCurve[satCurve.length - 1][1];
    for (let i = 1; i < satCurve.length; i++) {
      const [x1, y1] = satCurve[i];
      const [x0, y0] = satCurve[i - 1];
      if (lon <= x1) return y0 + ((y1 - y0) * (lon - x0)) / (x1 - x0 || 1);
    }
    return null;
  }

  // Reshape the model's fog towards what the satellite actually sees, keeping
  // the model's overall magnitude: normalise both to their own means, blend the
  // shapes, then restore the model's level.
  function applySatellite(g) {
    if (!satCurve) return;
    let modelSum = 0;
    for (let i = 0; i < CELLS; i++) modelSum += target.fog[i];
    const modelMean = modelSum / CELLS;
    if (modelMean < 0.01) return;

    const sat = new Float32Array(CELLS);
    let satSum = 0;
    for (let row = 0; row < H; row++) {
      for (let col = 0; col < W; col++) {
        const lon = g.lon0 + ((g.lon1 - g.lon0) * col) / (W - 1);
        const v = satAt(lon);
        sat[row * W + col] = v === null ? 1 : v;
        satSum += sat[row * W + col];
      }
    }
    const satMean = satSum / CELLS;
    if (satMean < 0.01) return;

    for (let i = 0; i < CELLS; i++) {
      const shaped = modelMean * (sat[i] / satMean);
      target.fog[i] = clamp01(target.fog[i] * (1 - SAT_WEIGHT) + shaped * SAT_WEIGHT);
    }
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
    // Satellite first, so the shape is available when the model's field lands.
    pollSatellite().then(poll);
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
    const meanRain = rain / CELLS;
    shared.uRain.value = meanRain;
    shared.uSmoke.value = clamp01((s.aqi - 80) / 170);

    // Wetness chases the rain up quickly and falls away slowly.
    const wetTarget = clamp01(meanRain * 1.6);
    const wetK = 1 - Math.exp(-dt / (wetTarget > wetness ? WET_UP_S : WET_DOWN_S));
    wetness += (wetTarget - wetness) * wetK;
    shared.uWetness.value = wetness;

    // Lightning, storms only. Deterministic-ish jitter from a rolling seed so
    // there is no Math.random in the frame path.
    const now2 = shared.uTime.value;
    if (meanRain > 0.55) {
      if (now2 > flashUntil && now2 > nextFlashAt) {
        flashSeed = (flashSeed * 16807) % 2147483647;
        const jitter = flashSeed / 2147483647;
        nextFlashAt = now2 + FLASH_MIN_S + jitter * (FLASH_MAX_S - FLASH_MIN_S);
        flashUntil = now2 + 0.12;
      }
      shared.uFlash.value = now2 < flashUntil ? 0.85 : 0;
    } else {
      shared.uFlash.value = 0;
      flashUntil = 0;
    }

    // 36 texels is free, but not free enough to upload for nothing.
    if (moved) uploadTexture();
  }

  // Jump straight to the target field, skipping the 60 s ease. For screenshots
  // and automated checks: nobody wants to wait out a transition to take a
  // picture, and a headless check has no frame loop to ease with.
  function settle() {
    for (const key of ['cloudLow', 'cloudHigh', 'fog', 'precip']) current[key].set(target[key]);
    scalars.current.windSpeed = scalars.target.windSpeed;
    scalars.current.windDir = scalars.target.windDir;
    scalars.current.aqi = scalars.target.aqi;
    windVector(scalars.current.windDir, scalars.current.windSpeed, wind);
    shared.uWind.value.copy(wind);
    let rain = 0;
    for (let i = 0; i < CELLS; i++) rain += current.precip[i];
    shared.uRain.value = rain / CELLS;
    shared.uSmoke.value = clamp01((scalars.current.aqi - 80) / 170);
    uploadTexture();
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
    settle,
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
        // Put the real weather back at once. Without this the scene keeps the
        // override's field until the next successful poll.
        if (lastPayload) applyPayload(lastPayload);
        override = null;
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
            // Linear, not squared: the Sunset and the Gate sit a column in from
            // the western edge, and squaring the falloff was quietly halving the
            // value they actually got. The floor stays LOW on purpose -- raising
            // it fogs the east side too, and "socked in out west, clear
            // downtown" is the entire point of a field.
            target.fog[r * W + c] = clamp01(merged.fog * (0.12 + 0.88 * west));
            target.cloudLow[r * W + c] = clamp01((merged.cloud ?? merged.fog) * (0.25 + 0.75 * west));
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
    // The names ?weather= will accept. Exposed so the URL parser validates
    // against the real list instead of keeping a second copy of it.
    // Whether the satellite is currently reshaping the fog, for QA.
    get satellite() {
      return satCurve ? { points: satCurve.length, curve: satCurve } : null;
    },
    get presetNames() {
      return Object.keys(PRESETS);
    },
    // Live state, for SF.weather.
    snapshot() {
      return {
        live: this.live,
        stale: staleSince > 0,
        // Whether the satellite observation is currently reshaping the fog.
        satellite: satCurve ? { points: satCurve.length } : null,
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
  karl: { fog: 1, cloud: 1, cloudHigh: 0.25, precip: 0, windSpeed: 7, windDir: 260, gradient: true },
  storm: { fog: 0.35, cloud: 1, cloudHigh: 0.9, precip: 0.85, windSpeed: 18, windDir: 200 },
  // Smoke's fog value is deliberately LOW. The effect is carried by the light
  // -- env.js turns the sun to an ember and the sky brown -- not by thick air.
  // At 0.45 the banks were a pea-souper and the orange sky lit nothing.
  smoke: { fog: 0.1, cloud: 0.1, cloudHigh: 0.25, precip: 0, aqi: 240, windSpeed: 3 },
};
