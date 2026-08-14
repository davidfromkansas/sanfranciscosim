// Live air traffic over San Francisco.
//
// /api/flights serves every airborne aircraft within 30 NM from community
// ADS-B receivers; this layer flies each one at its real position, on one of
// three procedural toy airframes chosen from the ICAO type the feed reports —
// airliner, light aircraft, helicopter — with a callsign bubble, a fading
// track behind it, and nav/strobe lights that ignite at dusk.
//
// The experience rules the mechanics here serve:
//   - Aircraft MOVE. Fixes arrive every ~20 s and a jet covers 5 km in that
//     time, so everything dead-reckons on its own velocity and eases onto each
//     new fix; nothing ever teleports.
//   - The sky has to be readable from the hero camera. Real cruise altitude is
//     11 km, twice the camera's own ceiling, so display altitude is COMPRESSED
//     (see dispY) while every number on the card stays true.
//   - The city's airports are off-scene. SFO sits at z +16.7 km and OAK at
//     x +19 km, both outside the 15 km water plane, so this is an OVERFLIGHT
//     layer: the arrival stream crosses the Bay and fades out at the scene
//     edge rather than popping.
//   - No feed, no key, no aircraft → the layer is simply empty. Nothing else
//     in the city depended on it, so there is no fallback to hand off (rule 3
//     is satisfied by construction, not by a spare code path).
//
// Draw calls: 3 airframes + 1 spinner (rotors/propellers) + trails + lights +
// badges = 7 worst case, and only for the classes actually in the sky.

import {
  AdditiveBlending,
  BufferAttribute,
  BufferGeometry,
  CanvasTexture,
  Color,
  CylinderGeometry,
  BoxGeometry,
  ConeGeometry,
  DynamicDrawUsage,
  InstancedBufferAttribute,
  InstancedMesh,
  LineSegments,
  LineBasicMaterial,
  MeshBasicMaterial,
  MeshLambertMaterial,
  Object3D,
  PlaneGeometry,
  Points,
  ShaderMaterial,
  SRGBColorSpace,
} from 'three';
import { mergeGeometries } from 'three/addons/utils/BufferGeometryUtils.js';

import { shared } from './env.js';

const ENDPOINT = `${import.meta.env.BASE_URL.replace(/\/$/, '')}/api/flights`;

const CAPACITY = 96;
const POLL_MS = 20 * 1000; // matches the feed's ttl; the CDN answers most of these
const POLL_JITTER_MS = 3 * 1000;
const DEMO_POLL_MS = 5 * 1000;
const STALE_MS = 3 * 60 * 1000; // backstop when polling itself fails
const MISSES_TO_DROP = 3; // consecutive snapshots without it → it has gone
const DEAD_RECKON_MAX_S = 120; // never extrapolate a fix further than this

// The water plane is 30 km across (app/src/water.js), so that is the edge of
// the world for anything airborne. Aircraft shrink away over the last 2 km
// instead of vanishing mid-air.
const SCENE_RADIUS = 15000;
const FADE_BAND = 2000;

// Semantic scale, the same move the road fleet makes (agents.js draws cars at
// 1.6x). A 38 m airliner is 4 px at the hero camera and reads as a speck; at
// 2.2x it reads as an aeroplane, which is the point of a diorama.
const AIR_SCALE = 2.2;
// Beyond this distance the airframe grows with range so it holds a roughly
// constant size on screen — the same reasoning as the muni badges, applied to
// the model itself, because the camera spends most of its life kilometres up.
const SCALE_REF_DIST = 1800;
const SCALE_MAX = 3.4;

// Display altitude. True below 800 m — that band holds the helicopters, the
// light traffic and the SFO approaches, and it is where being able to compare
// an aircraft against Salesforce Tower (326 m) actually matters. Above it the
// curve compresses asymptotically toward 3000 m, so an FL380 cruiser at
// 11.6 km still flies below the camera's 5.3 km ceiling and above the skyline,
// and relative order is preserved throughout. Floor 120 m: barometric
// altimeters read near or below zero on a low-pressure day and an aircraft
// embedded in the ground is worse than one flown slightly high.
const ALT_TRUE_TO = 800;
const ALT_COMPRESS_SPAN = 2200;
const ALT_COMPRESS_RATE = 3000;
const ALT_FLOOR = 120;
function dispY(altM) {
  const a = Math.max(ALT_FLOOR, altM);
  if (a <= ALT_TRUE_TO) return a;
  return ALT_TRUE_TO + ALT_COMPRESS_SPAN * (1 - Math.exp(-(a - ALT_TRUE_TO) / ALT_COMPRESS_RATE));
}

// Tracks: a preallocated ring per slot, one point every TRAIL_STEP_S, drawn as
// segments that fade from transparent (oldest) to bright (newest). This is what
// turns scattered dots into legible TRAFFIC — the arrival stream into SFO draws
// itself as a line across the Bay.
const TRAIL_POINTS = 20;
const TRAIL_SEGMENTS = TRAIL_POINTS - 1;
const TRAIL_STEP_S = 2.5;

// Nav lights: port red, starboard green, tail white, belly anti-collision red.
const LIGHTS_PER_AIRCRAFT = 4;

// Callsign bubbles, the same speech-bubble idiom the Muni badges use, in a 2:1
// cell because "UAL1577" needs the width that "38R" does not.
const BADGE_COLS = 4;
const BADGE_ROWS = 8;
const BADGE_CELL_W = 256;
const BADGE_CELL_H = 128;
const BADGE_W = 15.5; // metres
const BADGE_H = 7.75;
const BADGE_RADIUS_MIN = 400;
const BADGE_RADIUS_MAX = 14000;
const BADGE_RADIUS_PER_M = 2.6;
const BADGE_REF_DIST = 600;
const BADGE_SCALE_MIN = 0.9;
const BADGE_SCALE_MAX = 22;
const MAX_BADGES = 10;

const PICK_RADIUS = 90; // generous: aircraft are small, far away and moving
const MAX_PICK_DISTANCE = 16000;

// Toy palette (docs/styles/miniature-toy.md §7): neutral airframe, saturated
// identity accent, muted blue-gray glass. Airliners are warm white with a
// coloured tail; the accent is picked per aircraft from the hex so a given
// flight keeps its livery for as long as it is on screen.
const SHELL = 0xf2ece0; // warm white
const SHELL_SHADE = 0xdcd4c6; // underside / engine nacelle
const INK = 0x3a3530; // charcoal, the same ink the badges use
const GLASS = 0x4a5766; // muted blue-gray window band
const LIVERY = [0xe2604f, 0x3f7fa6, 0xd9a441, 0x5c8f6a, 0x9a6bb0, 0xd97b3f];
const HELI_SHELL = 0x4e5a63; // utility grey-blue: patrol, medevac, news
const LIGHT_SHELL = 0xf5f1e8;

const dummy = new Object3D();
const scratchColor = new Color();

function shortestAngle(from, to) {
  let d = (to - from) % (Math.PI * 2);
  if (d > Math.PI) d -= Math.PI * 2;
  if (d < -Math.PI) d += Math.PI * 2;
  return d;
}

// Compass bearing (deg clockwise from north) to scene yaw. Identical to the
// ferry convention: the scene has -z = north and every airframe here is
// authored nose toward -Z, matching the vehicle manifest's `front: -Z`, so a
// bearing is simply negated.
function bearingToYaw(bearingDeg) {
  return -(bearingDeg * Math.PI) / 180;
}

// ------------------------------------------------------------- airframes
//
// Authored in real metres, nose toward -Z, centred on the origin so the
// instance matrix can place them by their own centre. Chunky and few-parted on
// purpose (style bible §9: rebuild massing from a few clean volumes, then
// simplify again) — these are seen from hundreds of metres away.

// One part: a primitive with a flat colour baked into COLOR_0, so every part of
// every airframe merges into ONE geometry drawn by ONE Lambert material.
function part(geometry, color) {
  const count = geometry.attributes.position.count;
  const colors = new Float32Array(count * 3);
  const r = ((color >> 16) & 255) / 255;
  const g = ((color >> 8) & 255) / 255;
  const b = (color & 255) / 255;
  // Vertex colours multiply the material's white base in linear space; the
  // sRGB→linear conversion matches what the GLB loaders do to material colours.
  const lin = (c) => (c <= 0.04045 ? c / 12.92 : ((c + 0.055) / 1.055) ** 2.4);
  const lr = lin(r);
  const lg = lin(g);
  const lb = lin(b);
  for (let i = 0; i < count; i++) {
    colors[i * 3] = lr;
    colors[i * 3 + 1] = lg;
    colors[i * 3 + 2] = lb;
  }
  geometry.setAttribute('color', new BufferAttribute(colors, 3));
  geometry.deleteAttribute('uv');
  return geometry;
}

// A narrowbody the size of the 737s and A320s that make up most of SFO's
// traffic: 38 m long, 34 m span. Recognition cues kept, everything else cut —
// swept wings, two underslung engines, a tall tail, a dark window band.
function buildAirliner() {
  const parts = [];
  const push = (g, c) => parts.push(part(g, c));

  // Fuselage: an 8-sided tube reads as round at this distance and costs 32 tris.
  push(new CylinderGeometry(1.9, 1.9, 30, 8).rotateX(Math.PI / 2), SHELL);
  push(new ConeGeometry(1.9, 5, 8).rotateX(-Math.PI / 2).translate(0, 0, -17.5), SHELL);
  // Tailcone lifts as it tapers, the way an airliner's does.
  push(new ConeGeometry(1.9, 7, 8).rotateX(Math.PI / 2).translate(0, 0.9, 18), SHELL);

  // Window band: a thin proud strip either side, the one place the airframe
  // gets glass. Reads as "airliner" from far further away than windows would.
  push(new BoxGeometry(0.25, 0.9, 24).translate(1.85, 0.55, -1), GLASS);
  push(new BoxGeometry(0.25, 0.9, 24).translate(-1.85, 0.55, -1), GLASS);

  // Wings: swept by shearing a box in Z along X, so a single box carries the
  // sweep instead of costing extra parts.
  const wing = new BoxGeometry(34, 0.55, 5.4).translate(0, -1.1, 2.5);
  const wingPos = wing.attributes.position;
  for (let i = 0; i < wingPos.count; i++) {
    const x = wingPos.getX(i);
    wingPos.setZ(i, wingPos.getZ(i) + Math.abs(x) * 0.34); // sweepback
    wingPos.setY(i, wingPos.getY(i) + Math.abs(x) * 0.05); // dihedral
  }
  wing.computeVertexNormals();
  push(wing, SHELL);

  // Engines, slung under and ahead of the wing.
  for (const side of [-1, 1]) {
    push(
      new CylinderGeometry(1.15, 1.15, 5.2, 8).rotateX(Math.PI / 2).translate(side * 10.5, -2.4, 1.2),
      SHELL_SHADE
    );
    push(new CylinderGeometry(1.2, 1.2, 0.5, 8).rotateX(Math.PI / 2).translate(side * 10.5, -2.4, -1.5), INK);
  }

  push(new BoxGeometry(13, 0.45, 3.6).translate(0, 1.8, 18.6), SHELL); // horizontal stabiliser

  return mergeGeometries(parts, false);
}

// The tail fin is drawn as its own instanced mesh, NOT as part of the airliner
// geometry, for one reason: InstancedMesh's per-instance colour multiplies the
// whole instance, so a livery baked into the merged airframe would tint the
// entire aeroplane. Split out, `setColorAt` tints exactly the fin — which is
// the identity surface every airline puts its mark on, and the part still
// legible when the aircraft is a few pixels tall. Costs one draw call.
function buildAirlinerFin() {
  const fin = new BoxGeometry(0.5, 7.2, 6).translate(0, 4.6, 17.5);
  const pos = fin.attributes.position;
  for (let i = 0; i < pos.count; i++) {
    pos.setZ(i, pos.getZ(i) + Math.max(0, pos.getY(i)) * 0.42); // swept fin
  }
  fin.computeVertexNormals();
  fin.deleteAttribute('uv');
  return fin;
}

// A high-wing single the shape of the C172s and SR22s out of San Carlos and
// Palo Alto: 8.3 m long, 11 m span, with a spinner the propeller disc rides on.
function buildLight() {
  const parts = [];
  const push = (g, c) => parts.push(part(g, c));
  push(new BoxGeometry(1.5, 1.6, 6.4).translate(0, 0, 0.4), LIGHT_SHELL);
  push(new ConeGeometry(0.85, 2.2, 6).rotateX(-Math.PI / 2).translate(0, 0.1, -4.2), LIGHT_SHELL);
  push(new BoxGeometry(1.35, 0.75, 1.5).translate(0, 0.75, -0.6), GLASS); // cabin glass
  push(new BoxGeometry(11, 0.35, 1.7).translate(0, 1.1, -0.4), LIGHT_SHELL); // high wing
  push(new BoxGeometry(0.35, 2.4, 1.9).translate(0, 1.9, 3.6), 0xe2604f); // fin: the one accent
  push(new BoxGeometry(4.4, 0.3, 1.3).translate(0, 0.9, 3.9), LIGHT_SHELL); // stabiliser
  push(new CylinderGeometry(0.34, 0.2, 0.7, 6).rotateX(Math.PI / 2).translate(0, 0.1, -5.2), INK); // spinner
  return mergeGeometries(parts, false);
}

// A light twin-engine helicopter, the EC135/A109 shape that covers patrol,
// medevac and news over the city: 12 m including the tail boom.
function buildHeli() {
  const parts = [];
  const push = (g, c) => parts.push(part(g, c));
  push(new BoxGeometry(2.4, 2.3, 5).translate(0, 0, -0.8), HELI_SHELL); // cabin
  push(new ConeGeometry(1.45, 2.4, 6).rotateX(-Math.PI / 2).translate(0, -0.15, -3.6), HELI_SHELL); // nose
  push(new BoxGeometry(2.1, 1.05, 2.2).translate(0, 0.55, -2.5), GLASS); // canopy
  push(new CylinderGeometry(0.5, 0.32, 6.4, 6).rotateX(Math.PI / 2).translate(0, 0.45, 4.6), HELI_SHELL); // boom
  push(new BoxGeometry(0.3, 1.9, 1.5).translate(0, 1.35, 7.3), 0xd9a441); // fin: the one accent
  push(new BoxGeometry(2.6, 0.25, 0.9).translate(0, 0.9, 6.6), HELI_SHELL); // stabiliser
  push(new CylinderGeometry(0.32, 0.32, 0.9, 6).translate(0, 1.7, -0.6), INK); // rotor mast
  push(new CylinderGeometry(0.9, 0.9, 0.12, 8).rotateZ(Math.PI / 2).translate(0.55, 1.2, 7.1), INK); // tail rotor
  for (const side of [-1, 1]) {
    push(new BoxGeometry(0.16, 0.16, 4.2).translate(side * 1.05, -1.5, -0.6), INK); // skid
    push(new BoxGeometry(0.14, 1.0, 0.14).translate(side * 1.05, -0.95, -1.9), INK);
    push(new BoxGeometry(0.14, 1.0, 0.14).translate(side * 1.05, -0.95, 0.7), INK);
  }
  return mergeGeometries(parts, false);
}

// The spinning disc shared by helicopter rotors and propellers: a unit-radius
// blur with two crossed blades. One geometry, oriented and sized per instance —
// horizontal above a helicopter, vertical at the nose of a light aircraft.
function buildSpinner() {
  const parts = [];
  const blade = (rot) => {
    const g = new BoxGeometry(2, 0.02, 0.13);
    g.rotateY(rot);
    return g;
  };
  parts.push(blade(0), blade(Math.PI / 2), blade(Math.PI / 4), blade(-Math.PI / 4));
  return mergeGeometries(parts, false);
}

// Merge helper shared by the three airframes: one Lambert material with vertex
// colours, the same single-material idiom the landmark and ferry loaders use.
function buildAirframeMesh(geometry, name) {
  const material = new MeshLambertMaterial({ vertexColors: true });
  const mesh = new InstancedMesh(geometry, material, CAPACITY);
  mesh.name = name;
  mesh.instanceMatrix.setUsage(DynamicDrawUsage);
  mesh.frustumCulled = false; // instances are placed anywhere in a 30 km box
  mesh.castShadow = false; // aircraft are above the shadow cascade
  mesh.count = 0;
  return mesh;
}

// ---------------------------------------------------------------- badges

class BadgeAtlas {
  constructor() {
    this.canvas = document.createElement('canvas');
    this.canvas.width = BADGE_COLS * BADGE_CELL_W;
    this.canvas.height = BADGE_ROWS * BADGE_CELL_H;
    this.ctx = this.canvas.getContext('2d');
    this.texture = new CanvasTexture(this.canvas);
    this.texture.colorSpace = SRGBColorSpace;
    this.slots = new Map(); // label -> { rect, used }
    this.clock = 0;
  }

  // Callsigns churn as aircraft come and go, so cells are recycled least-
  // recently-used. With BADGE_COLS*BADGE_ROWS = 32 cells and at most
  // MAX_BADGES = 10 drawn per frame, a cell in use this frame can never be the
  // LRU victim — so a badge can never end up showing another flight's callsign.
  slotFor(label) {
    const existing = this.slots.get(label);
    if (existing) {
      existing.used = ++this.clock;
      return existing.rect;
    }
    let index = this.slots.size;
    if (index >= BADGE_COLS * BADGE_ROWS) {
      let victim = null;
      for (const [key, entry] of this.slots) {
        if (!victim || entry.used < victim.entry.used) victim = { key, entry };
      }
      index = victim.entry.index;
      this.slots.delete(victim.key);
    }
    this.draw(index, label);
    const rect = [
      ((index % BADGE_COLS) * BADGE_CELL_W) / this.canvas.width,
      1 - (Math.floor(index / BADGE_COLS) + 1) * (BADGE_CELL_H / this.canvas.height),
      BADGE_CELL_W / this.canvas.width,
      BADGE_CELL_H / this.canvas.height,
    ];
    this.slots.set(label, { rect, index, used: ++this.clock });
    this.texture.needsUpdate = true;
    return rect;
  }

  draw(index, label) {
    const ctx = this.ctx;
    const x = (index % BADGE_COLS) * BADGE_CELL_W;
    const y = Math.floor(index / BADGE_COLS) * BADGE_CELL_H;
    ctx.clearRect(x, y, BADGE_CELL_W, BADGE_CELL_H);
    ctx.save();
    ctx.translate(x, y);

    // Bubble body and its downward tail as one path, so the 2px warm-ink
    // outline runs unbroken around the joint (ui-theme: hard edges, no blur
    // except this one contact shadow that lifts it off the sky).
    const bx = 8;
    const by = 6;
    const bw = BADGE_CELL_W - 16;
    const bh = 78;
    const r = 20;
    const tailL = 104;
    const tailR = 140;
    const tipX = 118;
    const tipY = 116;
    ctx.beginPath();
    ctx.moveTo(bx + r, by);
    ctx.lineTo(bx + bw - r, by);
    ctx.quadraticCurveTo(bx + bw, by, bx + bw, by + r);
    ctx.lineTo(bx + bw, by + bh - r);
    ctx.quadraticCurveTo(bx + bw, by + bh, bx + bw - r, by + bh);
    ctx.lineTo(tailR, by + bh);
    ctx.lineTo(tipX, tipY);
    ctx.lineTo(tailL, by + bh);
    ctx.lineTo(bx + r, by + bh);
    ctx.quadraticCurveTo(bx, by + bh, bx, by + bh - r);
    ctx.lineTo(bx, by + r);
    ctx.quadraticCurveTo(bx, by, bx + r, by);
    ctx.closePath();

    ctx.shadowColor = 'rgba(28, 24, 20, 0.34)';
    ctx.shadowBlur = 7;
    ctx.shadowOffsetY = 4;
    ctx.fillStyle = '#fbf7ee';
    ctx.fill();
    ctx.shadowColor = 'transparent';
    ctx.lineWidth = 5;
    ctx.lineJoin = 'round';
    ctx.strokeStyle = '#3a3530';
    ctx.stroke();

    ctx.fillStyle = '#3a3530';
    const size = label.length > 7 ? 40 : label.length > 5 ? 46 : 52;
    ctx.font = `800 ${size}px ui-rounded, "SF Pro Rounded", -apple-system, system-ui, sans-serif`;
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    ctx.fillText(label, bx + bw / 2, by + bh / 2 + 1);
    ctx.restore();
    this.texture.needsUpdate = true;
  }
}

function buildBadgeMesh(atlas) {
  const geometry = new PlaneGeometry(BADGE_W, BADGE_H);
  const uvRect = new InstancedBufferAttribute(new Float32Array(CAPACITY * 4), 4);
  uvRect.setUsage(DynamicDrawUsage);
  geometry.setAttribute('uvRect', uvRect);
  const material = new MeshBasicMaterial({
    map: atlas.texture,
    transparent: true,
    depthWrite: false,
    depthTest: false, // a bubble is a label: never occluded by the city below it
    alphaTest: 0.02,
  });
  material.onBeforeCompile = (shader) => {
    shader.vertexShader = shader.vertexShader
      .replace('#include <common>', '#include <common>\nattribute vec4 uvRect;')
      .replace('#include <uv_vertex>', '#include <uv_vertex>\n  vMapUv = uvRect.xy + vMapUv * uvRect.zw;');
  };
  const mesh = new InstancedMesh(geometry, material, CAPACITY);
  mesh.name = 'live-aircraft-badges';
  mesh.instanceMatrix.setUsage(DynamicDrawUsage);
  mesh.frustumCulled = false;
  mesh.renderOrder = 5;
  mesh.count = 0;
  return { mesh, uvRect };
}

// ---------------------------------------------------------------- lights

// One additive Points layer for the whole fleet. Steady nav lights (red port,
// green starboard, white tail) plus a flashing belly beacon; the flash lives in
// the shader on a per-light phase so nothing pulses in unison and the CPU never
// touches it. Overall intensity follows uNight the way the landmark glow does —
// barely there at noon, the main event after dusk.
function buildLightsMesh() {
  const total = CAPACITY * LIGHTS_PER_AIRCRAFT;
  const geometry = new BufferGeometry();
  const position = new Float32Array(total * 3).fill(-1e5);
  const color = new Float32Array(total * 3);
  const phase = new Float32Array(total);
  const flash = new Float32Array(total); // 0 = steady nav light, 1 = strobe
  const scale = new Float32Array(total).fill(1);
  geometry.setAttribute('position', new BufferAttribute(position, 3));
  geometry.setAttribute('aColor', new BufferAttribute(color, 3));
  geometry.setAttribute('aPhase', new BufferAttribute(phase, 1));
  geometry.setAttribute('aFlash', new BufferAttribute(flash, 1));
  geometry.setAttribute('aScale', new BufferAttribute(scale, 1));

  const material = new ShaderMaterial({
    uniforms: { uTime: { value: 0 }, uIntensity: { value: 0.2 }, uPixelRatio: { value: 1 } },
    transparent: true,
    depthWrite: false,
    blending: AdditiveBlending,
    vertexShader: `
      attribute vec3 aColor;
      attribute float aPhase;
      attribute float aFlash;
      attribute float aScale;
      uniform float uTime;
      uniform float uIntensity;
      uniform float uPixelRatio;
      varying vec3 vColor;
      varying float vAlpha;
      void main() {
        vColor = aColor;
        // Strobes: a short bright pulse once a second. Steady lights hold.
        float t = fract(uTime * 0.9 + aPhase);
        float pulse = smoothstep(0.10, 0.0, t) + smoothstep(0.20, 0.13, t) * 0.7;
        vAlpha = uIntensity * mix(0.85, clamp(pulse, 0.0, 1.0), aFlash);
        vec4 mv = modelViewMatrix * vec4(position, 1.0);
        gl_Position = projectionMatrix * mv;
        // Size in pixels, gently attenuated by range so a light never becomes a
        // dinner plate up close nor disappears from the hero view.
        gl_PointSize = clamp(180.0 * aScale / -mv.z, 1.5, 9.0) * uPixelRatio;
      }
    `,
    fragmentShader: `
      varying vec3 vColor;
      varying float vAlpha;
      void main() {
        vec2 d = gl_PointCoord - vec2(0.5);
        float r = dot(d, d);
        if (r > 0.25) discard;
        float core = smoothstep(0.25, 0.0, r);
        gl_FragColor = vec4(vColor, vAlpha * core);
      }
    `,
  });
  const points = new Points(geometry, material);
  points.name = 'live-aircraft-lights';
  points.frustumCulled = false;
  points.renderOrder = 4;
  return points;
}

// Light colours, and the body-relative mounting points for each airframe kind.
const LIGHT_COLORS = [
  [1.0, 0.25, 0.2], // port, red
  [0.3, 1.0, 0.42], // starboard, green
  [1.0, 0.96, 0.88], // tail, white
  [1.0, 0.3, 0.25], // belly beacon, red (strobes)
];
const LIGHT_FLASH = [0, 0, 0, 1];
// Per-kind wingtip / tail / belly positions in metres.
const LIGHT_OFFSETS = {
  airliner: [
    [-17, -0.8, 3],
    [17, -0.8, 3],
    [0, 2.2, 20],
    [0, -2.4, 0],
  ],
  light: [
    [-5.5, 1.1, -0.4],
    [5.5, 1.1, -0.4],
    [0, 1.9, 4.4],
    [0, -0.9, 0],
  ],
  heli: [
    [-1.3, -0.2, -2.6],
    [1.3, -0.2, -2.6],
    [0, 1.4, 7.6],
    [0, -1.7, -0.6],
  ],
};

// ----------------------------------------------------------------- trails

function buildTrailMesh() {
  const geometry = new BufferGeometry();
  const position = new Float32Array(CAPACITY * TRAIL_SEGMENTS * 2 * 3);
  const color = new Float32Array(CAPACITY * TRAIL_SEGMENTS * 2 * 3);
  geometry.setAttribute('position', new BufferAttribute(position, 3));
  geometry.setAttribute('color', new BufferAttribute(color, 3));
  const material = new LineBasicMaterial({
    vertexColors: true,
    transparent: true,
    opacity: 0.42, // a hint of a path, not a stripe across the sky
    depthWrite: false,
  });
  const lines = new LineSegments(geometry, material);
  lines.name = 'live-aircraft-trails';
  lines.frustumCulled = false;
  return lines;
}

// ------------------------------------------------------------------ demo
//
// ?flights=demo — four synthetic aircraft that exercise the whole layer with no
// network: an SFO arrival crossing the Bay on descent, a departure climbing out
// northwest, a helicopter orbiting downtown, and a light aircraft that stops
// reporting so stale removal can be watched.
const DEMO_AIRCRAFT = [
  {
    id: 'AC:demo1',
    callsign: 'UAL1903',
    registration: 'N77302',
    type: 'B739',
    kind: 'airliner',
    from: [-122.28, 37.92],
    to: [-122.39, 37.63],
    altFrom: 2400,
    altTo: 300,
    speed: 95,
    periodS: 210,
    stopsAfterS: Infinity,
  },
  {
    id: 'AC:demo2',
    callsign: 'ASA318',
    registration: 'N625AS',
    type: 'A20N',
    kind: 'airliner',
    from: [-122.4, 37.66],
    to: [-122.62, 38.02],
    altFrom: 600,
    altTo: 6200,
    speed: 130,
    periodS: 240,
    stopsAfterS: Infinity,
  },
  {
    id: 'AC:demo3',
    callsign: 'N911SF',
    registration: 'N911SF',
    type: 'EC35',
    kind: 'heli',
    from: [-122.42, 37.79],
    to: [-122.39, 37.75],
    altFrom: 420,
    altTo: 380,
    speed: 38,
    periodS: 90,
    stopsAfterS: Infinity,
  },
  {
    id: 'AC:demo4',
    callsign: 'N2444H',
    registration: 'N2444H',
    type: 'C172',
    kind: 'light',
    from: [-122.51, 37.72],
    to: [-122.36, 37.86],
    altFrom: 900,
    altTo: 900,
    speed: 45,
    periodS: 150,
    stopsAfterS: 75, // goes quiet: proves the stale path fades it out
  },
];

function demoFixes(startedAt, now) {
  const elapsedS = (now - startedAt) / 1000;
  const out = [];
  for (const spec of DEMO_AIRCRAFT) {
    if (elapsedS > spec.stopsAfterS) continue;
    // Ping-pong along the leg so the demo never runs out of sky.
    const cycle = (elapsedS % (spec.periodS * 2)) / spec.periodS;
    const t = cycle <= 1 ? cycle : 2 - cycle;
    const dir = cycle <= 1 ? 1 : -1;
    const lon = spec.from[0] + (spec.to[0] - spec.from[0]) * t;
    const lat = spec.from[1] + (spec.to[1] - spec.from[1]) * t;
    const altM = spec.altFrom + (spec.altTo - spec.altFrom) * t;
    const dLon = (spec.to[0] - spec.from[0]) * dir;
    const dLat = (spec.to[1] - spec.from[1]) * dir;
    const bearingDeg =
      (Math.atan2(dLon * Math.cos((lat * Math.PI) / 180), dLat) * 180) / Math.PI;
    const vertical = ((spec.altTo - spec.altFrom) * dir) / spec.periodS;
    out.push({
      id: spec.id,
      hex: spec.id.slice(3),
      callsign: spec.callsign,
      registration: spec.registration,
      type: spec.type,
      kind: spec.kind,
      lat,
      lon,
      altM,
      bearingDeg: (bearingDeg + 360) % 360,
      groundSpeedMs: spec.speed,
      verticalRateMs: vertical,
      phase: vertical > 2.5 ? 'climbing' : vertical < -2.5 ? 'on approach' : 'level',
      squawk: '1200',
      emergency: null,
      recordedAt: now,
    });
  }
  return out;
}

// ------------------------------------------------------------------ layer

export function createLiveAircraft(scene, data) {
  const params = new URLSearchParams(window.location.search);
  const demo = params.get('flights') === 'demo';

  const aircraft = new Map(); // id -> state
  const meshes = {};
  let finMesh = null;
  let spinnerMesh = null;
  let trails = null;
  let lights = null;
  let badge = null;
  let atlas = null;
  let ready = false;
  let live = false;
  let source = null;
  let polling = false;
  let nextPollAt = 0;
  let warnedFetch = false;
  let spinAngle = 0;
  const demoStart = Date.now();

  // Trail ring buffers, indexed by slot.
  const ring = new Float32Array(CAPACITY * TRAIL_POINTS * 3);
  const freeSlots = [];
  for (let i = CAPACITY - 1; i >= 0; i--) freeSlots.push(i);

  function build() {
    meshes.airliner = buildAirframeMesh(buildAirliner(), 'live-aircraft-airliner');
    meshes.light = buildAirframeMesh(buildLight(), 'live-aircraft-light');
    meshes.heli = buildAirframeMesh(buildHeli(), 'live-aircraft-heli');
    for (const key of Object.keys(meshes)) scene.add(meshes[key]);

    // Airliner tails, tinted per instance (see buildAirlinerFin). Shares the
    // airframe's transform exactly, so it is the same matrix written twice.
    finMesh = new InstancedMesh(
      buildAirlinerFin(),
      new MeshLambertMaterial(),
      CAPACITY
    );
    finMesh.name = 'live-aircraft-fins';
    finMesh.instanceMatrix.setUsage(DynamicDrawUsage);
    finMesh.frustumCulled = false;
    finMesh.count = 0;
    scene.add(finMesh);

    spinnerMesh = new InstancedMesh(
      buildSpinner(),
      new MeshBasicMaterial({ color: 0x2e2a26, transparent: true, opacity: 0.34, depthWrite: false }),
      CAPACITY
    );
    spinnerMesh.name = 'live-aircraft-spinners';
    spinnerMesh.instanceMatrix.setUsage(DynamicDrawUsage);
    spinnerMesh.frustumCulled = false;
    spinnerMesh.count = 0;
    scene.add(spinnerMesh);

    trails = buildTrailMesh();
    scene.add(trails);
    lights = buildLightsMesh();
    scene.add(lights);
    atlas = new BadgeAtlas();
    badge = buildBadgeMesh(atlas);
    scene.add(badge.mesh);
    ready = true;
  }

  // ------------------------------------------------------------- ingest

  function releaseSlot(state) {
    freeSlots.push(state.slot);
    const base = state.slot * TRAIL_SEGMENTS * 2 * 3;
    trails.geometry.attributes.position.array.fill(0, base, base + TRAIL_SEGMENTS * 6);
    trails.geometry.attributes.color.array.fill(0, base, base + TRAIL_SEGMENTS * 6);
    trails.geometry.attributes.position.needsUpdate = true;
    trails.geometry.attributes.color.needsUpdate = true;
    const lightBase = state.slot * LIGHTS_PER_AIRCRAFT * 3;
    lights.geometry.attributes.position.array.fill(-1e5, lightBase, lightBase + LIGHTS_PER_AIRCRAFT * 3);
    lights.geometry.attributes.position.needsUpdate = true;
  }

  function apply(list, now, fetchedAt) {
    // Every fix is advanced by its own velocity across the gap between when it
    // was recorded and now, so re-ingesting a cached snapshot can never pull an
    // aircraft backwards through the sky.
    const seen = new Set();
    for (const a of list) {
      if (!Number.isFinite(a.lat) || !Number.isFinite(a.lon) || !Number.isFinite(a.altM)) continue;
      const [x, z] = data.project(a.lon, a.lat);
      const radius = Math.hypot(x, z);
      if (radius > SCENE_RADIUS + 6000) continue; // far outside the world; not worth a slot

      seen.add(a.id);
      const ageS = Math.min(DEAD_RECKON_MAX_S, Math.max(0, (now - (a.recordedAt || fetchedAt || now)) / 1000));
      const speed = Math.max(0, a.groundSpeedMs || 0);
      let state = aircraft.get(a.id);

      // A missing bearing must stay missing (the ferry lesson): rather than
      // pointing the aircraft north, derive the heading from where it has
      // actually moved since the previous fix. Almost every ADS-B transponder
      // reports track, so this is the rare path — but "rare" is exactly how a
      // fleet of north-facing aircraft ships unnoticed.
      let yaw = Number.isFinite(a.bearingDeg) ? bearingToYaw(a.bearingDeg) : null;
      if (yaw === null && state) {
        const dx = x - state.fixX;
        const dz = z - state.fixZ;
        if (Math.hypot(dx, dz) > 30) yaw = Math.atan2(-dx, -dz);
        else yaw = state.targetYaw ?? state.yaw; // hasn't moved enough to tell
      }
      // Velocity along the heading. Front is -Z, so world forward for a yaw is
      // (-sin, -cos) — the same derivation the ferry layer documents.
      const vx = yaw === null ? 0 : -Math.sin(yaw) * speed;
      const vz = yaw === null ? 0 : -Math.cos(yaw) * speed;
      const vy = a.verticalRateMs || 0;

      if (!state) {
        if (!freeSlots.length) continue;
        const slot = freeSlots.pop();
        state = {
          id: a.id,
          slot,
          x: x + vx * ageS,
          y: Math.max(0, a.altM + vy * ageS),
          z: z + vz * ageS,
          yaw: yaw ?? 0,
          bank: 0,
          trailHead: -1,
          trailCount: 0,
          trailT: 0,
          index: -1,
        };
        aircraft.set(a.id, state);
      }
      state.misses = 0;
      // Raw projected fix, kept so the next one can derive a heading from the
      // distance actually travelled.
      state.fixX = x;
      state.fixZ = z;
      state.targetX = x + vx * ageS;
      state.targetY = Math.max(0, a.altM + vy * ageS);
      state.targetZ = z + vz * ageS;
      state.vx = vx;
      state.vy = vy;
      state.vz = vz;
      state.speed = speed;
      state.targetYaw = yaw;
      // Card/label data, refreshed on every fix.
      state.kind = a.kind === 'heli' || a.kind === 'light' ? a.kind : 'airliner';
      state.callsign = a.callsign || null;
      state.registration = a.registration || null;
      state.label = a.callsign || a.registration || a.hex?.toUpperCase() || 'AIRCRAFT';
      state.type = a.type || null;
      state.altM = a.altM;
      state.verticalRateMs = a.verticalRateMs || 0;
      state.phaseLabel = a.phase || null;
      state.squawk = a.squawk || null;
      state.emergency = a.emergency || null;
      state.military = a.military || false;
      state.recordedAt = a.recordedAt || fetchedAt || now;
      state.lastFixAt = now;
      // Livery accent is deterministic per airframe, so a flight keeps the same
      // tail colour for as long as it is on screen — and two aircraft in the
      // same patch of sky are told apart at a glance.
      if (state.livery === undefined) {
        let hash = 0;
        for (let i = 0; i < state.id.length; i++) hash = (hash * 31 + state.id.charCodeAt(i)) >>> 0;
        state.livery = LIVERY[hash % LIVERY.length];
      }
    }

    // Each poll is a full snapshot, so anything absent from it has landed, left
    // the radius, or lost coverage. Retiring on the third consecutive miss
    // (~60 s) tolerates one truncated response without leaving a ghost
    // dead-reckoning across the Bay for the full stale horizon.
    for (const state of aircraft.values()) {
      if (seen.has(state.id)) continue;
      state.misses = (state.misses || 0) + 1;
      if (state.misses >= MISSES_TO_DROP) state.lastFixAt = 0; // update() reclaims the slot
    }
  }

  async function poll(now) {
    if (demo) {
      apply(demoFixes(demoStart, now), now, now);
      live = true;
      source = 'demo';
      return;
    }
    try {
      const res = await fetch(ENDPOINT, { headers: { accept: 'application/json' } });
      if (!res.ok) throw new Error(`flights ${res.status}`);
      const body = await res.json();
      live = body.live === true;
      source = body.source || null;
      if (Array.isArray(body.aircraft)) apply(body.aircraft, Date.now(), body.fetchedAt);
    } catch (error) {
      // Keep dead-reckoning what we have; the stale horizon retires it if the
      // feed never comes back. One warning, not one per poll.
      if (!warnedFetch) {
        warnedFetch = true;
        console.warn('[aircraft] live feed unavailable, sky will empty:', error?.message || error);
      }
      live = false;
    }
  }

  function tick(now) {
    if (polling || document.hidden || now < nextPollAt) return;
    polling = true;
    poll(now).finally(() => {
      polling = false;
      nextPollAt = Date.now() + (demo ? DEMO_POLL_MS : POLL_MS + Math.random() * POLL_JITTER_MS);
    });
  }

  document.addEventListener('visibilitychange', () => {
    if (!document.hidden) nextPollAt = 0;
  });

  // ------------------------------------------------------------- trails

  function appendTrailPoint(state, x, y, z) {
    state.trailHead = (state.trailHead + 1) % TRAIL_POINTS;
    const w = state.slot * TRAIL_POINTS * 3 + state.trailHead * 3;
    ring[w] = x;
    ring[w + 1] = y;
    ring[w + 2] = z;
    if (state.trailCount < TRAIL_POINTS) state.trailCount++;

    const position = trails.geometry.attributes.position.array;
    const color = trails.geometry.attributes.color.array;
    const base = state.slot * TRAIL_SEGMENTS * 2 * 3;
    const readBase = state.slot * TRAIL_POINTS * 3;
    for (let s = 0; s < TRAIL_SEGMENTS; s++) {
      const o = base + s * 6;
      if (s < state.trailCount - 1) {
        const k0 = (((state.trailHead - (state.trailCount - 1) + s) % TRAIL_POINTS) + TRAIL_POINTS) % TRAIL_POINTS;
        const k1 = (k0 + 1) % TRAIL_POINTS;
        const f0 = s / (state.trailCount - 1);
        const f1 = (s + 1) / (state.trailCount - 1);
        position[o] = ring[readBase + k0 * 3];
        position[o + 1] = ring[readBase + k0 * 3 + 1];
        position[o + 2] = ring[readBase + k0 * 3 + 2];
        position[o + 3] = ring[readBase + k1 * 3];
        position[o + 4] = ring[readBase + k1 * 3 + 1];
        position[o + 5] = ring[readBase + k1 * 3 + 2];
        // Fade from nothing at the oldest point to a soft cream at the newest.
        for (const [offset, f] of [
          [o, f0],
          [o + 3, f1],
        ]) {
          color[offset] = 0.86 * f;
          color[offset + 1] = 0.88 * f;
          color[offset + 2] = 0.94 * f;
        }
      } else {
        // Unused segment: collapse to a degenerate point far below the world.
        position[o] = position[o + 3] = 0;
        position[o + 1] = position[o + 4] = -1e5;
        position[o + 2] = position[o + 5] = 0;
        color[o] = color[o + 1] = color[o + 2] = 0;
        color[o + 3] = color[o + 4] = color[o + 5] = 0;
      }
    }
    trails.geometry.attributes.position.needsUpdate = true;
    trails.geometry.attributes.color.needsUpdate = true;
  }

  // -------------------------------------------------------------- frame

  const badgeCandidates = [];

  function update(dt, camera) {
    const now = Date.now();
    tick(now);
    if (!ready) return;

    const step = Math.min(dt, 0.25); // a backgrounded tab must not teleport the fleet
    spinAngle = (spinAngle + step * 22) % (Math.PI * 2);
    const nightLift = Math.min(1, 0.14 + (shared.uNight.value ?? 0) * 0.95);
    lights.material.uniforms.uIntensity.value = nightLift;
    lights.material.uniforms.uTime.value = (now % 100000) / 1000;

    const counts = { airliner: 0, light: 0, heli: 0 };
    let spinnerCount = 0;
    const lightPos = lights.geometry.attributes.position.array;
    const lightColor = lights.geometry.attributes.aColor.array;
    const lightPhase = lights.geometry.attributes.aPhase.array;
    const lightFlash = lights.geometry.attributes.aFlash.array;
    const lightScale = lights.geometry.attributes.aScale.array;

    const camY = camera.position.y;
    const badgeRadius = Math.max(BADGE_RADIUS_MIN, Math.min(BADGE_RADIUS_MAX, camY * BADGE_RADIUS_PER_M));
    badgeCandidates.length = 0;

    for (const state of aircraft.values()) {
      if (now - state.lastFixAt > STALE_MS) {
        releaseSlot(state);
        aircraft.delete(state.id);
        continue;
      }

      // Dead-reckon, then ease onto the advancing target. Both move, so the
      // correction is absorbed smoothly instead of snapping on each poll.
      state.targetX += state.vx * step;
      state.targetY += state.vy * step;
      state.targetZ += state.vz * step;
      state.x += state.vx * step;
      state.y += state.vy * step;
      state.z += state.vz * step;
      const ease = 1 - Math.exp(-step * 0.7);
      state.x += (state.targetX - state.x) * ease;
      state.y += (state.targetY - state.y) * ease;
      state.z += (state.targetZ - state.z) * ease;
      state.y = Math.max(0, state.y);

      // Heading: the reported track when there is one, otherwise derived from
      // motion. Banking is proportional to the turn rate, which is what sells
      // an aircraft turning rather than sliding sideways.
      const wantYaw =
        state.targetYaw !== null && state.targetYaw !== undefined
          ? state.targetYaw
          : Math.atan2(-state.vx, -state.vz);
      const turn = shortestAngle(state.yaw, wantYaw);
      const applied = Math.max(-1.6 * step, Math.min(1.6 * step, turn));
      state.yaw += applied;
      const wantBank = Math.max(-0.42, Math.min(0.42, (applied / Math.max(step, 1e-3)) * 0.55));
      state.bank += (wantBank - state.bank) * Math.min(1, step * 2.5);

      const y = dispY(state.y);
      const distance = Math.hypot(camera.position.x - state.x, camera.position.y - y, camera.position.z - state.z);

      // Edge fade: shrink to nothing across the last band of the water plane
      // instead of popping out of existence at the boundary.
      const radius = Math.hypot(state.x, state.z);
      const edge =
        radius <= SCENE_RADIUS - FADE_BAND
          ? 1
          : Math.max(0, (SCENE_RADIUS - radius) / FADE_BAND);
      if (edge <= 0) {
        // Off the edge of the world: stop drawing it, and park its lights so
        // they do not hang in the void where the airframe used to be.
        if (state.index >= 0) {
          const parked = state.slot * LIGHTS_PER_AIRCRAFT * 3;
          lightPos.fill(-1e5, parked, parked + LIGHTS_PER_AIRCRAFT * 3);
        }
        state.index = -1;
        continue;
      }

      const scale =
        AIR_SCALE * edge * Math.min(SCALE_MAX, Math.max(1, distance / SCALE_REF_DIST));

      // Pitch from the climb/descent angle, clamped: a 2000 fpm climb is only
      // a few degrees in reality and reads as nothing, so it is exaggerated.
      const pitch = Math.max(-0.3, Math.min(0.3, Math.atan2(state.vy, Math.max(state.speed, 1)) * 2.2));
      dummy.position.set(state.x, y, state.z);
      dummy.rotation.set(0, 0, 0);
      dummy.rotateY(state.yaw);
      dummy.rotateX(pitch);
      dummy.rotateZ(state.bank);
      dummy.scale.setScalar(scale);
      dummy.updateMatrix();

      const mesh = meshes[state.kind];
      const index = counts[state.kind]++;
      mesh.setMatrixAt(index, dummy.matrix);
      if (state.kind === 'airliner') {
        // Same transform as the airframe; only the colour differs per instance.
        finMesh.setMatrixAt(index, dummy.matrix);
        finMesh.setColorAt(index, scratchColor.setHex(state.livery));
      }
      state.index = index;
      state.drawScale = scale;
      state.displayY = y;

      // Rotors and propellers: same disc geometry, placed and sized by kind.
      if (state.kind === 'heli' || state.kind === 'light') {
        const heli = state.kind === 'heli';
        dummy.rotation.set(0, 0, 0);
        dummy.rotateY(state.yaw);
        dummy.rotateX(pitch);
        dummy.rotateZ(state.bank);
        if (heli) {
          dummy.translateY(2.2);
          dummy.rotateY(spinAngle);
          dummy.scale.setScalar(scale * 5.4); // ~11 m rotor disc
        } else {
          dummy.translateZ(-5.5);
          dummy.rotateX(Math.PI / 2); // propeller stands upright at the nose
          dummy.rotateY(spinAngle * 2.4);
          dummy.scale.setScalar(scale * 0.95);
        }
        dummy.updateMatrix();
        spinnerMesh.setMatrixAt(spinnerCount++, dummy.matrix);
      }

      // Nav lights ride the airframe. The offsets are rotated into world space
      // by hand — yaw only, since pitch and bank are small enough that their
      // effect on a wingtip position is well under a light's own size, and this
      // runs LIGHTS_PER_AIRCRAFT times for every aircraft every frame.
      const offsets = LIGHT_OFFSETS[state.kind];
      const cosY = Math.cos(state.yaw);
      const sinY = Math.sin(state.yaw);
      for (let k = 0; k < LIGHTS_PER_AIRCRAFT; k++) {
        const o = offsets[k];
        const lx = o[0] * scale;
        const ly = o[1] * scale;
        const lz = o[2] * scale;
        const wx = lx * cosY + lz * sinY;
        const wz = -lx * sinY + lz * cosY;
        const li = (state.slot * LIGHTS_PER_AIRCRAFT + k) * 3;
        lightPos[li] = state.x + wx;
        lightPos[li + 1] = y + ly;
        lightPos[li + 2] = state.z + wz;
        lightColor[li] = LIGHT_COLORS[k][0];
        lightColor[li + 1] = LIGHT_COLORS[k][1];
        lightColor[li + 2] = LIGHT_COLORS[k][2];
        lightPhase[state.slot * LIGHTS_PER_AIRCRAFT + k] = (state.slot * 0.137 + k * 0.07) % 1;
        lightFlash[state.slot * LIGHTS_PER_AIRCRAFT + k] = LIGHT_FLASH[k];
        lightScale[state.slot * LIGHTS_PER_AIRCRAFT + k] = scale / AIR_SCALE;
      }

      // Trail sampling is on wall time, so the path is the same shape whatever
      // the frame rate.
      state.trailT += step;
      if (state.trailT >= TRAIL_STEP_S) {
        state.trailT = 0;
        appendTrailPoint(state, state.x, y, state.z);
      }

      if (distance < badgeRadius) {
        state.badgeDistance = distance;
        badgeCandidates.push(state);
      }
    }

    for (const key of Object.keys(meshes)) {
      meshes[key].count = counts[key];
      meshes[key].instanceMatrix.needsUpdate = true;
    }
    finMesh.count = counts.airliner;
    finMesh.instanceMatrix.needsUpdate = true;
    if (finMesh.instanceColor) finMesh.instanceColor.needsUpdate = true;
    spinnerMesh.count = spinnerCount;
    spinnerMesh.instanceMatrix.needsUpdate = true;
    lights.geometry.attributes.position.needsUpdate = true;
    lights.geometry.attributes.aColor.needsUpdate = true;
    lights.geometry.attributes.aPhase.needsUpdate = true;
    lights.geometry.attributes.aFlash.needsUpdate = true;
    lights.geometry.attributes.aScale.needsUpdate = true;

    // Badges: nearest first, hard-capped, each drawn at a size that holds
    // roughly constant on screen so the hero view is labelled too.
    badgeCandidates.sort((a, b) => a.badgeDistance - b.badgeDistance);
    const shown = Math.min(MAX_BADGES, badgeCandidates.length);
    const uvRect = badge.uvRect;
    for (let i = 0; i < shown; i++) {
      const state = badgeCandidates[i];
      const rect = atlas.slotFor(state.label);
      uvRect.setXYZW(i, rect[0], rect[1], rect[2], rect[3]);
      const badgeScale = Math.max(
        BADGE_SCALE_MIN,
        Math.min(BADGE_SCALE_MAX, state.badgeDistance / BADGE_REF_DIST)
      );
      // The bubble's tail tip must sit just above the airframe at EVERY zoom.
      // Both the aircraft and the bubble grow with range, so the lift has to
      // track both: half a bubble height (its tip is at the bottom edge) plus
      // the airframe's own drawn half-height.
      dummy.position.set(
        state.x,
        state.displayY + BADGE_H * badgeScale * 0.42 + state.drawScale * 4,
        state.z
      );
      dummy.quaternion.copy(camera.quaternion); // billboard
      dummy.scale.setScalar(badgeScale);
      dummy.updateMatrix();
      badge.mesh.setMatrixAt(i, dummy.matrix);
    }
    badge.mesh.count = shown;
    badge.mesh.instanceMatrix.needsUpdate = true;
    uvRect.needsUpdate = true;
  }

  // ----------------------------------------------------------- entities

  function entityFor(state) {
    const ft = Math.round(state.altM / 0.3048);
    const kt = Math.round(state.speed / 0.514444);
    const fpm = Math.round(state.verticalRateMs / 0.00508);
    return {
      kind: 'aircraft',
      id: state.id,
      title: state.label,
      name:
        state.kind === 'heli' ? 'Helicopter' : state.kind === 'light' ? 'Light aircraft' : 'Airliner',
      x: state.x,
      z: state.z,
      // The card shows TRUE numbers; only the rendered height is compressed.
      altitudeFt: ft,
      altitudeM: Math.round(state.altM),
      speedKt: kt,
      speedKmh: state.speed * 3.6,
      verticalRateFpm: fpm,
      phase: state.phaseLabel,
      aircraftType: state.type,
      callsign: state.callsign,
      registration: state.registration,
      squawk: state.squawk,
      emergency: state.emergency,
      military: state.military || undefined,
      heading: Math.round(((-state.yaw * 180) / Math.PI + 360) % 360),
      recordedAt: state.recordedAt,
      demo,
      source: demo ? 'demo' : `ADS-B (${source || 'community'})`,
      confidence: 3,
    };
  }

  function pickAircraft(origin, direction) {
    if (!ready) return null;
    let best = null;
    const now = Date.now();
    for (const state of aircraft.values()) {
      if (state.index < 0 || now - state.lastFixAt > STALE_MS) continue;
      const px = state.x - origin.x;
      const py = state.displayY - origin.y;
      const pz = state.z - origin.z;
      const t = px * direction.x + py * direction.y + pz * direction.z;
      if (t <= 0 || t > MAX_PICK_DISTANCE) continue;
      const away = Math.hypot(px - direction.x * t, py - direction.y * t, pz - direction.z * t);
      // The pick radius grows with the airframe's drawn scale, so an aircraft
      // that looks big from the hero camera is as easy to hit as it looks.
      const radius = PICK_RADIUS * Math.max(1, state.drawScale / AIR_SCALE);
      if (away > radius || (best && t >= best.distance)) continue;
      best = { ...entityFor(state), distance: t };
    }
    return best;
  }

  function aircraftEntity(id) {
    const state = aircraft.get(id);
    return state && state.index >= 0 ? entityFor(state) : null;
  }

  build();

  return {
    update,
    pickAircraft,
    aircraftEntity,
    get live() {
      return live;
    },
    get demo() {
      return demo;
    },
    get source() {
      return source;
    },
    get count() {
      return aircraft.size;
    },
    // Aircraft table for debugging / automated checks.
    get aircraft() {
      return [...aircraft.values()].map((state) => ({
        id: state.id,
        label: state.label,
        kind: state.kind,
        type: state.type,
        x: Math.round(state.x),
        z: Math.round(state.z),
        altM: Math.round(state.altM),
        displayY: Math.round(dispY(state.y)),
        speedKt: Math.round(state.speed / 0.514444),
        drawn: state.index >= 0,
      }));
    },
  };
}
