// Rain, and the wet streets that sell it better than the drops do.
//
// Streaks live in a box around the point the camera is LOOKING AT, not around
// the camera itself. This is a diorama: the camera sits high and looks down, so
// a box centred on the camera put every drop above and behind the view, drawing
// seventeen hundred streaks that rendered exactly zero pixels. The box follows
// the rig's pivot instead, which is the patch of city on screen.
//
// One InstancedMesh, one draw call. Count scales with the precipitation the
// weather field reports at that same point, so a shower over the Richmond is a
// shower over the Richmond (WEATHER-PLAN §3.2).
//
// Off entirely at Quality=Low: rain is the first thing to go.

import { Color, DynamicDrawUsage, InstancedMesh, Matrix4, MeshBasicMaterial, PlaneGeometry, Quaternion, Vector3 } from 'three';
import { shared } from './env.js';

// Never zero. Setting the low tier to 0 meant the governor -- which demotes
// readily on a loaded machine -- silently deleted the rain, so a storm looked
// like a dry overcast day. Same mistake the fog banks made.
export const RAIN_CAPS = { ultra: 2600, high: 2600, medium: 1400, low: 600 };

// The box the streaks live in, metres, at the CLOSEST zoom. It scales up with
// the camera's distance: a fixed 520 m box is most of the frame at street level
// and an unnoticeable patch in the corner from the hero view, which is why a
// storm read as dry from far out.
const BOX = 520;
const TOP = 420;
const BOX_MAX_SCALE = 7;
// Terminal velocity, toy-scale: real rain at ~9 m/s reads as a static smear at
// this camera distance, so it falls slower and reads as motion instead.
const FALL = 34;

const _matrix = new Matrix4();
const _position = new Vector3();
const _quaternion = new Quaternion();
const _scale = new Vector3();
const _hidden = new Vector3(0, -100000, 0);
const _tilt = new Vector3();
const UP = new Vector3(0, 1, 0);

function hash(i, salt) {
  const x = Math.sin(i * 127.1 + salt * 311.7) * 43758.5453;
  return x - Math.floor(x);
}

export function createRain(scene, { sampleAt }) {
  // A vertical streak, sized for the DIORAMA camera rather than for life. The
  // first cut used a realistic 0.45 m x 9 m drop, which at the 600-3000 m the
  // camera actually sits at is well under a pixel wide -- seventeen hundred of
  // them changed the frame by 0.09 of one brightness level. Rain has to be a
  // graphic mark at this scale, not a raindrop.
  const geometry = new PlaneGeometry(3.2, 34);
  const material = new MeshBasicMaterial({
    color: new Color(0xc8dbe8),
    transparent: true,
    opacity: 0.42,
    depthWrite: false,
    fog: false,
  });

  const cap = RAIN_CAPS.high;
  const mesh = new InstancedMesh(geometry, material, cap);
  mesh.instanceMatrix.setUsage(DynamicDrawUsage);
  mesh.name = 'rain';
  mesh.frustumCulled = false;
  mesh.renderOrder = 900;
  mesh.visible = false;
  scene.add(mesh);

  // Each drop keeps its own offset inside the box and falls on its own phase.
  const drops = [];
  for (let i = 0; i < cap; i++) {
    drops.push({
      x: (hash(i, 1) - 0.5) * 2 * BOX,
      z: (hash(i, 2) - 0.5) * 2 * BOX,
      y: hash(i, 3) * TOP,
      speed: 0.8 + hash(i, 4) * 0.5,
      length: 0.7 + hash(i, 5) * 0.9,
    });
  }

  let activeCap = cap;
  const setQuality = (key) => {
    activeCap = RAIN_CAPS[key] ?? cap;
  };

  // `focus` is the ground point the camera is framing (the rig pivot), NOT the
  // camera position.
  function update(dt, focus, cameraDistance = 900) {
    // Zoomed out, the box grows and the streaks grow with it, so rain reads at
    // every zoom instead of only from the street.
    const spread = Math.max(1, Math.min(BOX_MAX_SCALE, cameraDistance / 700));
    // Local rain, not the citywide mean: stand in the shower, not near it.
    const local = Math.max(0, Math.min(1, sampleAt(focus.x, focus.z, 'precip')));
    const count = Math.round(activeCap * local);
    mesh.visible = count > 0;
    if (!mesh.visible) return 0;

    const wind = shared.uWind.value;
    // Streaks lean downwind. The lean is exaggerated over the true ratio —
    // vertical rain reads as static noise, a slant reads as weather.
    _tilt.set(wind.x * 0.06, -1, wind.y * 0.06).normalize();
    _quaternion.setFromUnitVectors(UP, _tilt);

    for (let i = 0; i < cap; i++) {
      if (i >= count) {
        _matrix.compose(_hidden, _quaternion, _scale.set(0.0001, 0.0001, 0.0001));
        mesh.setMatrixAt(i, _matrix);
        continue;
      }
      const drop = drops[i];
      drop.y -= FALL * drop.speed * dt;
      // Recycle from the top rather than allocating anything.
      if (drop.y < 0) drop.y += TOP;

      // Falls from the top of the box down to the ground being looked at.
      _position.set(focus.x + drop.x * spread, focus.y + drop.y * spread, focus.z + drop.z * spread);
      _scale.set(spread, drop.length * spread, spread);
      _matrix.compose(_position, _quaternion, _scale);
      mesh.setMatrixAt(i, _matrix);
    }
    mesh.instanceMatrix.needsUpdate = true;
    mesh.count = cap;
    material.opacity = 0.3 + 0.45 * local;
    return count;
  }

  return {
    mesh,
    update,
    setQuality,
    dispose() {
      scene.remove(mesh);
      geometry.dispose();
      material.dispose();
    },
  };
}
