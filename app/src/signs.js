// Rooftop signs for the diorama: chunky extruded letters standing on notable
// roofs, the way a model railway labels its buildings. Config driven, invented
// names only (no real wordmarks), merged into a single draw call, hidden when
// the camera pulls back beyond 5 km.

import { BufferAttribute, Color, Mesh, MeshLambertMaterial } from 'three';
import { FontLoader } from 'three/addons/loaders/FontLoader.js';
import { TextGeometry } from 'three/addons/geometries/TextGeometry.js';
import { mergeGeometries } from 'three/addons/utils/BufferGeometryUtils.js';

const FONT_URL = 'fonts/helvetiker_bold.typeface.json';
const MAX_SIGNS = 40;
export const SIGN_RANGE = 5000;

// lon, lat, text, y = roof height in metres, size = cap height, yaw in degrees.
const SIGNS = [
  { lon: -122.4021, lat: 37.7926, text: 'GOLDEN GATE MUTUAL', y: 196, size: 13, yaw: 30, color: '#e8735a' },
  { lon: -122.4009, lat: 37.7912, text: 'BAYSIDE TRUST', y: 176, size: 12, yaw: 30, color: '#3fa8a0' },
  { lon: -122.3985, lat: 37.7898, text: 'EMBARCADERO WORKS', y: 152, size: 11, yaw: 32, color: '#d9a441' },
  { lon: -122.4041, lat: 37.7885, text: 'MARKET & MAIN', y: 138, size: 11, yaw: 30, color: '#6db3d9' },
  { lon: -122.4067, lat: 37.7853, text: 'SOMA PRINTING CO', y: 74, size: 9, yaw: 30, color: '#e8735a' },
  { lon: -122.4103, lat: 37.7836, text: 'CIVIC HALL HOTEL', y: 66, size: 9, yaw: 28, color: '#8fd0a8' },
  { lon: -122.4076, lat: 37.7955, text: 'JACKSON SQUARE FISH', y: 58, size: 8, yaw: 34, color: '#6db3d9' },
  { lon: -122.4143, lat: 37.8035, text: 'WHARF ICE CREAM', y: 34, size: 8, yaw: 20, color: '#e2557f' },
  { lon: -122.4183, lat: 37.7614, text: 'MISSION BAKERY', y: 28, size: 7, yaw: 0, color: '#d9a441' },
  { lon: -122.4318, lat: 37.7692, text: 'HAIGHT RECORDS', y: 26, size: 7, yaw: 0, color: '#3fa8a0' },
  { lon: -122.4489, lat: 37.7714, text: 'INNER SUNSET HARDWARE', y: 24, size: 6.5, yaw: 0, color: '#e8735a' },
  { lon: -122.4776, lat: 37.7631, text: 'OCEAN LAUNDRY', y: 22, size: 6.5, yaw: 0, color: '#6db3d9' },
  { lon: -122.4213, lat: 37.8005, text: 'NORTH BEACH CAFE', y: 30, size: 7, yaw: 12, color: '#e2557f' },
  { lon: -122.4665, lat: 37.7841, text: 'RICHMOND GROCERY', y: 24, size: 6.5, yaw: 0, color: '#8fd0a8' },
  { lon: -122.3925, lat: 37.7752, text: 'SOUTH YARD DEPOT', y: 42, size: 8, yaw: 30, color: '#d9a441' },
  { lon: -122.4396, lat: 37.7433, text: 'NOE HILL DAIRY', y: 26, size: 7, yaw: 0, color: '#3fa8a0' },
];

export function createSigns(scene, data) {
  let mesh = null;
  let loading = null;
  let wanted = false;

  const material = new MeshLambertMaterial({ vertexColors: true });

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
      geometry.rotateY((sign.yaw * Math.PI) / 180);
      const [x, z] = data.project(sign.lon, sign.lat);
      const base = Math.max(0, data.sampleElevation(x, z)) + sign.y;
      geometry.translate(x, base, z);

      color.set(sign.color);
      const count = geometry.attributes.position.count;
      const colors = new Float32Array(count * 3);
      for (let i = 0; i < count; i++) {
        colors[i * 3] = color.r;
        colors[i * 3 + 1] = color.g;
        colors[i * 3 + 2] = color.b;
      }
      geometry.setAttribute('color', new BufferAttribute(colors, 3));
      geometry.deleteAttribute('uv');
      parts.push(geometry);
    }

    const merged = mergeGeometries(parts, false);
    for (const part of parts) part.dispose();
    merged.computeBoundingSphere();
    mesh = new Mesh(merged, material);
    mesh.name = 'toy-signs';
    mesh.castShadow = true;
    mesh.visible = wanted;
    scene.add(mesh);
  }

  return {
    setVisible(value) {
      wanted = value;
      if (mesh) {
        mesh.visible = value;
        return;
      }
      // First reveal pays for the font fetch and the merge, once per session.
      if (value && !loading) {
        loading = build().catch((err) => console.warn('rooftop signs failed', err));
      }
    },
    update(distance) {
      if (mesh) mesh.visible = wanted && distance < SIGN_RANGE;
    },
    get count() {
      return mesh ? SIGNS.length : 0;
    },
  };
}
