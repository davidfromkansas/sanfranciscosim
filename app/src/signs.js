// Rooftop signs for the diorama: chunky extruded letters standing on notable
// roofs, the way a model railway labels its buildings. Config driven, invented
// names only (no real wordmarks), merged into a single draw call, hidden when
// the camera pulls back beyond 5 km.

import { BufferAttribute, Color, Mesh, MeshBasicMaterial, MeshLambertMaterial } from 'three';
import { FontLoader } from 'three/addons/loaders/FontLoader.js';
import { TextGeometry } from 'three/addons/geometries/TextGeometry.js';
import { mergeGeometries } from 'three/addons/utils/BufferGeometryUtils.js';

const FONT_URL = 'fonts/helvetiker_bold.typeface.json';

// Neighbourhood labels: the district's real name in the same chunky extruded
// letters as the rooftop signs, floating over the middle of it.
//
// They replace the 420 m ground ring that used to appear when a click landed on
// open ground — a circle that said "you are somewhere in the Mission" only
// after you clicked, and looked like a warning while it did. A standing label
// says the same thing continuously and reads from the air, which is where this
// city is looked at from.
//
// MAJOR ones only, not all 41: the full set puts a wall of text over the city.
// This is the list a visitor would name, and it is deliberately hand-picked
// rather than "the biggest by area" — Chinatown is small and major, Bayview is
// huge and rarely the thing you are looking for.
const MAJOR_HOODS = [
  'Financial District/South Beach', 'Chinatown', 'North Beach', 'Nob Hill', 'Russian Hill',
  'Mission', 'Castro/Upper Market', 'Haight Ashbury', 'Hayes Valley', 'Marina',
  'Pacific Heights', 'Sunset/Parkside', 'Inner Sunset', 'Inner Richmond', 'Outer Richmond',
  'Potrero Hill', 'Bernal Heights', 'Noe Valley', 'Tenderloin', 'South of Market',
  'Golden Gate Park', 'Presidio', 'Twin Peaks', 'Japantown', 'Western Addition',
];
// Cap height in metres. These are read from kilometres up, so they dwarf a
// rooftop sign on purpose.
const HOOD_SIZE = 78;
// Metres above the ground under the label's anchor: clear of the hills and of
// everything but the towers, which are their own landmarks anyway.
const HOOD_FLOAT = 210;
const HOOD_COLOR = '#f3e7c8';
// Below this the labels stand down: at street level you are inside the district
// and a 78 m word overhead is in the way.
const HOOD_MIN_DISTANCE = 1200;
const MAX_SIGNS = 40;
export const SIGN_RANGE = 5000;

// lon, lat, text, y = roof height in metres, size = cap height.
const SIGNS = [
  { lon: -122.4021, lat: 37.7926, text: 'GOLDEN GATE MUTUAL', y: 196, size: 13, color: '#e8735a' },
  { lon: -122.4009, lat: 37.7912, text: 'BAYSIDE TRUST', y: 176, size: 12, color: '#3fa8a0' },
  { lon: -122.3985, lat: 37.7898, text: 'EMBARCADERO WORKS', y: 152, size: 11, color: '#d9a441' },
  { lon: -122.4041, lat: 37.7885, text: 'MARKET & MAIN', y: 138, size: 11, color: '#6db3d9' },
  { lon: -122.4067, lat: 37.7853, text: 'SOMA PRINTING CO', y: 74, size: 9, color: '#e8735a' },
  { lon: -122.4103, lat: 37.7836, text: 'CIVIC HALL HOTEL', y: 66, size: 9, color: '#8fd0a8' },
  { lon: -122.4076, lat: 37.7955, text: 'JACKSON SQUARE FISH', y: 58, size: 8, color: '#6db3d9' },
  { lon: -122.4143, lat: 37.8035, text: 'WHARF ICE CREAM', y: 34, size: 8, color: '#e2557f' },
  { lon: -122.4183, lat: 37.7614, text: 'MISSION BAKERY', y: 28, size: 7, color: '#d9a441' },
  { lon: -122.4318, lat: 37.7692, text: 'HAIGHT RECORDS', y: 26, size: 7, color: '#3fa8a0' },
  { lon: -122.4489, lat: 37.7714, text: 'INNER SUNSET HARDWARE', y: 24, size: 6.5, color: '#e8735a' },
  { lon: -122.4776, lat: 37.7631, text: 'OCEAN LAUNDRY', y: 22, size: 6.5, color: '#6db3d9' },
  { lon: -122.4213, lat: 37.8005, text: 'NORTH BEACH CAFE', y: 30, size: 7, color: '#e2557f' },
  { lon: -122.4665, lat: 37.7841, text: 'RICHMOND GROCERY', y: 24, size: 6.5, color: '#8fd0a8' },
  { lon: -122.3925, lat: 37.7752, text: 'SOUTH YARD DEPOT', y: 42, size: 8, color: '#d9a441' },
  { lon: -122.4396, lat: 37.7433, text: 'NOE HILL DAIRY', y: 26, size: 7, color: '#3fa8a0' },
];

// `hoods` is the context module's neighbourhood list — it does NOT live on the
// core data bundle, which is what this module used to reach for and why the
// labels silently built nothing.
export function createSigns(scene, data, hoods = []) {
  let mesh = null;
  let hoodMesh = null;
  let loading = null;
  let wanted = false;

  // The diorama only ever looks from eight headings, so each sign turns about
  // its own anchor in the vertex shader to face the current one. That keeps the
  // lettering readable from every heading while staying a single draw call.
  const uSignYaw = { value: 0 };
  // The labels are UNLIT on purpose: a Lambert sign goes dark with the city, and
  // a district name has to be readable at 3 a.m. as well as at noon.
  const hoodMaterial = new MeshBasicMaterial({ vertexColors: true, toneMapped: false });
  const material = new MeshLambertMaterial({ vertexColors: true });
  const billboard = (shader) => {
    shader.uniforms.uSignYaw = uSignYaw;
    shader.vertexShader = shader.vertexShader
      .replace(
        '#include <common>',
        `#include <common>
        attribute vec3 aAnchor;
        uniform float uSignYaw;`
      )
      .replace(
        '#include <begin_vertex>',
        `vec3 local = position - aAnchor;
        float s = sin(uSignYaw);
        float c = cos(uSignYaw);
        vec3 transformed = aAnchor + vec3(
          local.x * c + local.z * s,
          local.y,
          -local.x * s + local.z * c
        );`
      )
      .replace(
        '#include <beginnormal_vertex>',
        `vec3 objectNormal = vec3(
          normal.x * cos(uSignYaw) + normal.z * sin(uSignYaw),
          normal.y,
          -normal.x * sin(uSignYaw) + normal.z * cos(uSignYaw)
        );`
      );
  };
  material.onBeforeCompile = billboard;
  hoodMaterial.onBeforeCompile = billboard;

  // One label per major neighbourhood, standing over its centre.
  function buildHoods(font) {
    const parts = [];
    const color = new Color(HOOD_COLOR);
    for (const hood of hoods || []) {
      if (!MAJOR_HOODS.includes(hood.name)) continue;
      const geometry = new TextGeometry(hood.name.replace(/\/.*$/, '').toUpperCase(), {
        font,
        size: HOOD_SIZE,
        depth: HOOD_SIZE * 0.18,
        curveSegments: 2,
        bevelEnabled: false,
      });
      geometry.computeBoundingBox();
      const b = geometry.boundingBox;
      const x = hood.x;
      const z = hood.z;
      const ground = data.sampleElevation ? data.sampleElevation(x, z) : 0;
      const base = Math.max(0, ground) + HOOD_FLOAT;
      // Centre the word on the district rather than starting it there.
      geometry.translate(x - (b.max.x - b.min.x) / 2, base, z);
      const count = geometry.attributes.position.count;
      const colors = new Float32Array(count * 3);
      const anchors = new Float32Array(count * 3);
      for (let i = 0; i < count; i++) {
        colors[i * 3] = color.r;
        colors[i * 3 + 1] = color.g;
        colors[i * 3 + 2] = color.b;
        anchors[i * 3] = x;
        anchors[i * 3 + 1] = base;
        anchors[i * 3 + 2] = z;
      }
      geometry.setAttribute('color', new BufferAttribute(colors, 3));
      geometry.setAttribute('aAnchor', new BufferAttribute(anchors, 3));
      geometry.deleteAttribute('uv');
      parts.push(geometry);
    }
    if (!parts.length) return;
    const merged = mergeGeometries(parts, false);
    for (const part of parts) part.dispose();
    merged.computeBoundingSphere();
    merged.boundingSphere.radius += 400;
    hoodMesh = new Mesh(merged, hoodMaterial);
    hoodMesh.name = 'hood-labels';
    hoodMesh.renderOrder = 5;
    hoodMesh.visible = wanted;
    scene.add(hoodMesh);
  }

  async function build() {
    const font = await new FontLoader().loadAsync(FONT_URL);
    const parts = [];
    const color = new Color();
    for (const sign of SIGNS.slice(0, MAX_SIGNS)) {
      const geometry = new TextGeometry(sign.text, {
        font,
        size: sign.size,
        depth: sign.size * 0.25,
        curveSegments: 2,
        bevelEnabled: false,
      });
      geometry.computeBoundingBox();
      const box = geometry.boundingBox;
      // Stand the letters up on the roof, centred on the anchor point.
      geometry.translate(-(box.max.x - box.min.x) / 2, 0, 0);
      const [x, z] = data.project(sign.lon, sign.lat);
      const base = Math.max(0, data.sampleElevation(x, z)) + sign.y;
      geometry.translate(x, base, z);

      color.set(sign.color);
      const count = geometry.attributes.position.count;
      const colors = new Float32Array(count * 3);
      const anchors = new Float32Array(count * 3);
      for (let i = 0; i < count; i++) {
        colors[i * 3] = color.r;
        colors[i * 3 + 1] = color.g;
        colors[i * 3 + 2] = color.b;
        anchors[i * 3] = x;
        anchors[i * 3 + 1] = base;
        anchors[i * 3 + 2] = z;
      }
      geometry.setAttribute('color', new BufferAttribute(colors, 3));
      geometry.setAttribute('aAnchor', new BufferAttribute(anchors, 3));
      geometry.deleteAttribute('uv');
      parts.push(geometry);
    }

    const merged = mergeGeometries(parts, false);
    for (const part of parts) part.dispose();
    merged.computeBoundingSphere();
    mesh = new Mesh(merged, material);
    // The letters swing about their anchors, so the merged bounds are only a
    // starting point; the widest sign is well under the padding here.
    merged.boundingSphere.radius += 60;
    mesh.name = 'toy-signs';
    mesh.castShadow = true;
    mesh.visible = wanted;
    scene.add(mesh);
    buildHoods(font);
  }

  return {
    setVisible(value) {
      wanted = value;
      if (mesh) {
        mesh.visible = value;
        if (hoodMesh) hoodMesh.visible = value;
        return;
      }
      // First reveal pays for the font fetch and the merge, once per session.
      if (value && !loading) {
        loading = build().catch((err) => console.warn('rooftop signs failed', err));
      }
    },
    update(distance, cameraYaw) {
      // Snap to the diorama's eight headings: the signs turn with the view in
      // 45-degree steps instead of following the camera continuously.
      uSignYaw.value = Math.round(cameraYaw / (Math.PI / 4)) * (Math.PI / 4);
      if (mesh) mesh.visible = wanted && distance < SIGN_RANGE;
      // The opposite rule from the rooftop signs: a district name is FOR the
      // wide view, so it appears as you pull back and gets out of the way once
      // you are down among the buildings it labels.
      if (hoodMesh) hoodMesh.visible = wanted && distance > HOOD_MIN_DISTANCE;
    },
    get count() {
      return mesh ? SIGNS.length : 0;
    },
  };
}
