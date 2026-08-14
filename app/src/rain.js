// Rain, and the wet streets that sell it better than the drops do.
//
// Streaks live in a box that follows the camera — you only ever see rain near
// you, so there is no reason to simulate it over the whole city. One
// InstancedMesh, one draw call. Count scales with the precipitation the weather
// field reports at the camera's own position, so a shower over the Richmond is
// a shower over the Richmond (WEATHER-PLAN §3.2).
//
// Off entirely at Quality=Low: rain is the first thing to go.

import { Color, DynamicDrawUsage, InstancedMesh, Matrix4, MeshBasicMaterial, PlaneGeometry, Quaternion, Vector3 } from 'three';
import { shared } from './env.js';

export const RAIN_CAPS = { ultra: 2000, high: 2000, medium: 900, low: 0 };

// The box that rides with the camera, metres.
const BOX = 300;
const TOP = 220;
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
  // A thin vertical quad. Streaks, not spheres: a droplet at city scale is
  // invisible, and the toy look wants a graphic mark anyway.
  const geometry = new PlaneGeometry(0.45, 9);
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

  function update(dt, cameraPosition) {
    // Local rain, not the citywide mean: stand in the shower, not near it.
    const local = Math.max(0, Math.min(1, sampleAt(cameraPosition.x, cameraPosition.z, 'precip')));
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

      _position.set(cameraPosition.x + drop.x, cameraPosition.y - TOP * 0.5 + drop.y, cameraPosition.z + drop.z);
      _scale.set(1, drop.length, 1);
      _matrix.compose(_position, _quaternion, _scale);
      mesh.setMatrixAt(i, _matrix);
    }
    mesh.instanceMatrix.needsUpdate = true;
    mesh.count = cap;
    material.opacity = 0.24 + 0.3 * local;
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
