// The city is inhabited: ferries and container ships crossing the Bay, traffic
// on the real street centrelines, cable cars on the three surviving lines,
// pedestrians when you are down at street level, gulls over the water and flags
// snapping on the landmarks. All instanced; the whole system is ~12 draw calls.

import {
  BoxGeometry,
  BufferAttribute,
  Color,
  ConeGeometry,
  CylinderGeometry,
  DoubleSide,
  DynamicDrawUsage,
  Group,
  IcosahedronGeometry,
  InstancedMesh,
  Mesh,
  MeshBasicMaterial,
  MeshLambertMaterial,
  Object3D,
  PlaneGeometry,
  ShaderMaterial,
  Vector3,
} from 'three';
import { createGLTFLoader } from './gltf.js';
import { mergeGeometries } from 'three/addons/utils/BufferGeometryUtils.js';
import { shared } from './env.js';
import { DECK_HALF_THICKNESS } from './landmarks.js';

const ASSETS = `${import.meta.env.BASE_URL}sf-assets/`;

const CAR_COUNT = 720;
const PED_COUNT = 420;
const BIRD_COUNT = 90;
// The low tier halves-or-better the live population instead of resizing the
// pools: the instanced meshes keep their allocation and the simulation simply
// stops at the cap, so the governor can move this lever every few seconds
// without a rebuild.
const LOW_CAPS = { cars: 320, peds: 160, birds: 45 };
const CAR_RANGE = 2200;
// Vehicle geometry is base-origin, and the renderer lifts every car this far
// off its path so street cars clear the road ribbon.
const CAR_LIFT = 0.2;
const PED_RANGE = 420;

// Ferry / container-ship routes across the Bay, in lon/lat.
const SHIP_ROUTES = [
  {
    name: 'Sausalito ferry',
    kind: 'ferry',
    points: [
      [-122.3934, 37.7952],
      [-122.4025, 37.8095],
      [-122.4213, 37.8305],
      [-122.4547, 37.8443],
    ],
  },
  {
    name: 'Alcatraz cruise',
    kind: 'ferry',
    points: [
      [-122.4162, 37.8093],
      [-122.4207, 37.8203],
      [-122.4231, 37.8264],
      [-122.4141, 37.8171],
      [-122.4162, 37.8093],
    ],
  },
  {
    name: 'Oakland container run',
    kind: 'container',
    points: [
      [-122.4855, 37.8261],
      [-122.4501, 37.8206],
      [-122.4053, 37.8218],
      [-122.3603, 37.8171],
    ],
  },
  {
    name: 'Golden Gate outbound',
    kind: 'container',
    points: [
      [-122.3854, 37.7808],
      [-122.4204, 37.8085],
      [-122.4767, 37.8206],
      [-122.5265, 37.8281],
    ],
  },
  {
    name: 'Bay sail',
    kind: 'sail',
    points: [
      [-122.4392, 37.8112],
      [-122.4197, 37.8221],
      [-122.3961, 37.8168],
      [-122.4104, 37.8047],
      [-122.4392, 37.8112],
    ],
  },
  {
    name: 'Ocean sail',
    kind: 'sail',
    points: [
      [-122.5121, 37.7503],
      [-122.5093, 37.7724],
      [-122.5162, 37.7921],
      [-122.5138, 37.7681],
      [-122.5121, 37.7503],
    ],
  },
];

// Toy-mode extras: construction sites, balloon launch points and the
// helicopter's downtown orbit. Invented placements, deliberately playful.
const CRANE_SITES = [
  [-122.3971, 37.7842],
  [-122.4032, 37.7885],
  [-122.4113, 37.7776],
  [-122.3925, 37.7745],
  [-122.4192, 37.7659],
  [-122.4271, 37.7845],
  [-122.4478, 37.7833],
  [-122.3888, 37.7688],
];
const BALLOON_SITES = [
  [-122.4712, 37.7694],
  [-122.4451, 37.7712],
  [-122.4232, 37.7601],
  [-122.4098, 37.8062],
  [-122.4835, 37.7521],
  [-122.4552, 37.8018],
];
const HELI_CENTER = [-122.4014, 37.7893];

// The three surviving cable car lines.
const CABLE_LINES = [
  {
    name: 'Powell-Hyde',
    points: [
      [-122.4083, 37.7847],
      [-122.4098, 37.7889],
      [-122.4113, 37.7938],
      [-122.4157, 37.7955],
      [-122.4193, 37.7975],
      [-122.4205, 37.8022],
      [-122.4207, 37.8062],
    ],
  },
  {
    name: 'Powell-Mason',
    points: [
      [-122.4083, 37.7847],
      [-122.4098, 37.7889],
      [-122.4113, 37.7938],
      [-122.4098, 37.7985],
      [-122.4114, 37.8043],
      [-122.4137, 37.8072],
    ],
  },
  {
    name: 'California St',
    points: [
      [-122.3944, 37.7935],
      [-122.4022, 37.7924],
      [-122.4116, 37.7919],
      [-122.4213, 37.7914],
      [-122.4295, 37.7908],
    ],
  },
];

function polylineLengths(points) {
  const cumulative = new Float32Array(points.length / 3);
  let total = 0;
  for (let i = 1; i < cumulative.length; i++) {
    total += Math.hypot(
      points[i * 3] - points[(i - 1) * 3],
      points[i * 3 + 2] - points[(i - 1) * 3 + 2]
    );
    cumulative[i] = total;
  }
  return { cumulative, total };
}

function samplePolyline(points, cumulative, total, distance, out, tangent) {
  const d = Math.max(0, Math.min(total, distance));
  let i = 1;
  while (i < cumulative.length - 1 && cumulative[i] < d) i++;
  const d0 = cumulative[i - 1];
  const d1 = cumulative[i];
  const t = d1 - d0 > 1e-4 ? (d - d0) / (d1 - d0) : 0;
  const ax = points[(i - 1) * 3];
  const ay = points[(i - 1) * 3 + 1];
  const az = points[(i - 1) * 3 + 2];
  const bx = points[i * 3];
  const by = points[i * 3 + 1];
  const bz = points[i * 3 + 2];
  out.set(ax + (bx - ax) * t, ay + (by - ay) * t, az + (bz - az) * t);
  if (tangent) tangent.set(bx - ax, by - ay, bz - az).normalize();
}

function carArchetype() {
  const parts = [];
  const body = new BoxGeometry(1.85, 1.15, 4.4);
  body.translate(0, 0.75, 0);
  parts.push(body);
  const cabin = new BoxGeometry(1.7, 0.75, 2.2);
  cabin.translate(0, 1.6, -0.2);
  parts.push(cabin);
  const merged = mergeGeometries(parts, false);
  for (const p of parts) p.dispose();
  merged.deleteAttribute('uv');
  return merged;
}

function shipArchetype(kind) {
  const parts = [];
  if (kind === 'sail') {
    const hull = new BoxGeometry(3.4, 1.6, 11);
    hull.translate(0, 0.6, 0);
    parts.push(hull);
    const sail = new ConeGeometry(3.6, 13, 3);
    sail.translate(0, 7.4, -0.6);
    parts.push(sail);
  } else if (kind === 'ferry') {
    const hull = new BoxGeometry(9, 3.4, 34);
    hull.translate(0, 1.6, 0);
    parts.push(hull);
    const deck = new BoxGeometry(8, 3, 20);
    deck.translate(0, 4.6, -1);
    parts.push(deck);
    const bridge = new BoxGeometry(6, 2.4, 7);
    bridge.translate(0, 7.3, -6);
    parts.push(bridge);
    const funnel = new CylinderGeometry(0.8, 0.9, 3.4, 8);
    funnel.translate(0, 9.6, -6);
    parts.push(funnel);
  } else {
    const hull = new BoxGeometry(16, 8, 108);
    hull.translate(0, 3.6, 0);
    parts.push(hull);
    const containers = new BoxGeometry(15, 11, 78);
    containers.translate(0, 12.8, 6);
    parts.push(containers);
    const house = new BoxGeometry(14, 12, 14);
    house.translate(0, 13.6, -42);
    parts.push(house);
  }
  const merged = mergeGeometries(parts, false);
  for (const p of parts) p.dispose();
  merged.deleteAttribute('uv');
  return merged;
}

// Toy archetypes, all merged into single instanced draw calls.
function craneArchetype() {
  const parts = [];
  const mast = new BoxGeometry(2.2, 58, 2.2);
  mast.translate(0, 29, 0);
  parts.push(mast);
  const jib = new BoxGeometry(46, 1.6, 1.6);
  jib.translate(13, 58, 0);
  parts.push(jib);
  const counter = new BoxGeometry(7, 3.4, 3.4);
  counter.translate(-11, 57.5, 0);
  parts.push(counter);
  const cab = new BoxGeometry(3.2, 3.2, 3.2);
  cab.translate(0, 54, 0);
  parts.push(cab);
  const hook = new BoxGeometry(0.4, 14, 0.4);
  hook.translate(26, 50, 0);
  parts.push(hook);
  const merged = mergeGeometries(parts, false);
  for (const p of parts) p.dispose();
  merged.deleteAttribute('uv');
  return merged;
}

function balloonArchetype() {
  // The icosahedron envelope is non-indexed, so the other parts must be too:
  // mergeGeometries returns null when index presence is mixed across the list.
  const parts = [];
  const envelope = new IcosahedronGeometry(9, 2);
  envelope.scale(1, 1.25, 1);
  envelope.translate(0, 11, 0);
  parts.push(envelope);
  const tether = new CylinderGeometry(0.16, 0.16, 5, 4).toNonIndexed();
  tether.translate(0, 1.6, 0);
  parts.push(tether);
  const basket = new BoxGeometry(3, 2.4, 3).toNonIndexed();
  basket.translate(0, -1.2, 0);
  parts.push(basket);
  const merged = mergeGeometries(parts, false);
  for (const p of parts) p.dispose();
  merged.deleteAttribute('uv');
  return merged;
}

function cableCarArchetype() {
  const parts = [];
  const body = new BoxGeometry(2.6, 2.6, 9.2);
  body.translate(0, 1.9, 0);
  parts.push(body);
  const roof = new BoxGeometry(3.0, 0.4, 9.8);
  roof.translate(0, 3.3, 0);
  parts.push(roof);
  const merged = mergeGeometries(parts, false);
  for (const p of parts) p.dispose();
  merged.deleteAttribute('uv');
  return merged;
}

const FLAG_VERT = /* glsl */ `
  uniform float uTime;
  varying vec2 vUv;
  varying float vShade;
  void main() {
    vUv = uv;
    vec3 p = position;
    // Wave amplitude grows toward the free edge of the flag.
    float k = uv.x;
    p.z += sin(uv.x * 9.0 - uTime * 6.0) * 0.42 * k;
    p.y += sin(uv.x * 6.0 - uTime * 4.4) * 0.12 * k;
    vShade = 0.75 + 0.25 * cos(uv.x * 9.0 - uTime * 6.0);
    gl_Position = projectionMatrix * modelViewMatrix * vec4(p, 1.0);
  }
`;

const FLAG_FRAG = /* glsl */ `
  uniform vec3 uColorA;
  uniform vec3 uColorB;
  varying vec2 vUv;
  varying float vShade;
  void main() {
    vec3 col = mix(uColorA, uColorB, step(0.5, fract(vUv.y * 3.0)));
    gl_FragColor = vec4(col * vShade, 1.0);
  }
`;

// The Stars and Stripes, drawn procedurally so it stays a flat-colour toy
// surface: 13 stripes red at top and bottom, a canton over the upper seven,
// and a dot grid standing in for the star field at diorama scale. `uv.x` is
// 0 at the hoist, so the canton sits by the mast from either side.
const FLAG_FRAG_US = /* glsl */ `
  uniform vec3 uColorA;
  uniform vec3 uColorB;
  uniform vec3 uColorC;
  varying vec2 vUv;
  varying float vShade;
  const float CANTON = 0.46153846; // the flag's upper seven stripes
  void main() {
    vec3 col = mix(uColorA, uColorB, step(0.5, fract(vUv.y * 6.5)));
    if (vUv.x < 0.4 && vUv.y > CANTON) {
      col = uColorC;
      vec2 s = vec2(vUv.x / 0.4 * 5.5, (vUv.y - CANTON) / (1.0 - CANTON) * 4.5);
      vec2 f = fract(s) - 0.5;
      float star = 1.0 - smoothstep(0.15, 0.25, length(f));
      col = mix(col, uColorB, star);
    }
    gl_FragColor = vec4(col * vShade, 1.0);
  }
`;

export function createAgents(scene, data, city) {
  const { project, sampleElevation, manifest } = data;
  const group = new Group();
  group.name = 'agents';
  scene.add(group);

  const dummy = new Object3D();
  const position = new Vector3();
  const tangent = new Vector3();

  // ------------------------------------------------------------------ ships ---
  const ships = [];
  for (const route of SHIP_ROUTES) {
    const points = new Float32Array(route.points.length * 3);
    route.points.forEach(([lon, lat], i) => {
      const [x, z] = project(lon, lat);
      points[i * 3] = x;
      points[i * 3 + 1] = 0;
      points[i * 3 + 2] = z;
    });
    const { cumulative, total } = polylineLengths(points);
    const count = route.kind === 'sail' ? 5 : route.kind === 'ferry' ? 2 : 2;
    const mesh = new InstancedMesh(
      shipArchetype(route.kind),
      new MeshLambertMaterial({
        color: route.kind === 'container' ? '#7d5f52' : route.kind === 'ferry' ? '#e8e3d6' : '#f2f0e8',
      }),
      count
    );
    mesh.instanceMatrix.setUsage(DynamicDrawUsage);
    mesh.castShadow = false;
    mesh.frustumCulled = false;
    group.add(mesh);
    const speed = route.kind === 'container' ? 7.5 : route.kind === 'ferry' ? 11 : 5;
    const instances = [];
    for (let i = 0; i < count; i++) {
      instances.push({ d: (total / count) * i, dir: 1, bob: Math.random() * 6.28 });
    }
    // Wake: a stretched translucent quad trailing each hull.
    const wake = new InstancedMesh(
      new PlaneGeometry(1, 1),
      new MeshBasicMaterial({ color: '#dfeaf0', transparent: true, opacity: 0.28, depthWrite: false }),
      count
    );
    wake.instanceMatrix.setUsage(DynamicDrawUsage);
    wake.frustumCulled = false;
    wake.renderOrder = 3;
    group.add(wake);
    ships.push({ route, points, cumulative, total, mesh, wake, instances, speed });
  }

  // ---------------------------------------------------------------- traffic ---
  const carMesh = new InstancedMesh(
    carArchetype(),
    new MeshLambertMaterial({ vertexColors: false }),
    CAR_COUNT
  );
  carMesh.instanceMatrix.setUsage(DynamicDrawUsage);
  carMesh.castShadow = false;
  carMesh.frustumCulled = false;
  carMesh.count = 0;
  const carColors = new Float32Array(CAR_COUNT * 3);
  const paint = new Color();
  const carPalette = ['#d8d5cf', '#2f3338', '#8c9096', '#7d2f2a', '#26415c', '#c9a227', '#3d5a45'];
  for (let i = 0; i < CAR_COUNT; i++) {
    paint.set(carPalette[i % carPalette.length]);
    carColors[i * 3] = paint.r;
    carColors[i * 3 + 1] = paint.g;
    carColors[i * 3 + 2] = paint.b;
  }
  carMesh.instanceColor = new BufferAttribute(carColors, 3);
  carMesh.instanceColor.setUsage(DynamicDrawUsage);
  group.add(carMesh);

  // Headlight/taillight glow, only alive after dusk.
  const lightMesh = new InstancedMesh(
    new PlaneGeometry(2.6, 1.4),
    new MeshBasicMaterial({ color: '#fff2cf', transparent: true, opacity: 0, depthWrite: false }),
    CAR_COUNT
  );
  lightMesh.instanceMatrix.setUsage(DynamicDrawUsage);
  lightMesh.frustumCulled = false;
  lightMesh.count = 0;
  group.add(lightMesh);

  // The hand-made vehicle fleet: one merged instanced mesh per type, all
  // sharing one material. Until it loads (or if it never does) the procedural
  // carMesh above keeps traffic on the streets.
  const fleet = [];
  const fleetMaterial = new MeshLambertMaterial({ vertexColors: true });
  let fleetCursors = new Int32Array(0);

  // Signed volume of a closed part; negative means the shell is inside-out, so
  // backface culling would eat the surfaces the camera should see.
  function signedVolume(geometry) {
    const position = geometry.attributes.position;
    const index = geometry.index;
    const count = index ? index.count : position.count;
    let volume = 0;
    for (let t = 0; t < count; t += 3) {
      const a = index ? index.getX(t) : t;
      const b = index ? index.getX(t + 1) : t + 1;
      const c = index ? index.getX(t + 2) : t + 2;
      const ax = position.getX(a);
      const ay = position.getY(a);
      const az = position.getZ(a);
      const bx = position.getX(b);
      const by = position.getY(b);
      const bz = position.getZ(b);
      const cx = position.getX(c);
      const cy = position.getY(c);
      const cz = position.getZ(c);
      volume += (ax * (by * cz - bz * cy) - ay * (bx * cz - bz * cx) + az * (bx * cy - by * cx)) / 6;
    }
    return volume;
  }

  function reverseGeometry(geometry) {
    const index = geometry.index;
    if (index) {
      for (let t = 0; t < index.count; t += 3) {
        const a = index.getX(t);
        index.setX(t, index.getX(t + 2));
        index.setX(t + 2, a);
      }
      index.needsUpdate = true;
    } else {
      const position = geometry.attributes.position;
      for (let t = 0; t < position.count; t += 3) {
        for (const attribute of Object.values(geometry.attributes)) {
          for (let k = 0; k < attribute.itemSize; k++) {
            const a = attribute.array[t * attribute.itemSize + k];
            attribute.array[t * attribute.itemSize + k] = attribute.array[(t + 2) * attribute.itemSize + k];
            attribute.array[(t + 2) * attribute.itemSize + k] = a;
          }
          attribute.needsUpdate = true;
        }
      }
    }
    const normal = geometry.attributes.normal;
    for (let i = 0; i < normal.count; i++) {
      normal.setXYZ(i, -normal.getX(i), -normal.getY(i), -normal.getZ(i));
    }
    normal.needsUpdate = true;
  }

  function mergeVehicle(root) {
    root.updateMatrixWorld(true);
    const parts = [];
    root.traverse((object) => {
      if (!object.isMesh) return;
      const geometry = object.geometry.clone();
      geometry.applyMatrix4(object.matrixWorld);
      geometry.deleteAttribute('uv');
      geometry.deleteAttribute('uv1');
      if (!geometry.attributes.normal) geometry.computeVertexNormals();
      if (signedVolume(geometry) < 0) reverseGeometry(geometry);
      const count = geometry.attributes.position.count;
      const colors = new Float32Array(count * 3);
      const color = object.material?.color;
      for (let i = 0; i < count; i++) {
        colors[i * 3] = color ? color.r : 1;
        colors[i * 3 + 1] = color ? color.g : 1;
        colors[i * 3 + 2] = color ? color.b : 1;
      }
      geometry.setAttribute('color', new BufferAttribute(colors, 3));
      parts.push(geometry);
    });
    const merged = parts.length ? mergeGeometries(parts, false) : null;
    for (const p of parts) p.dispose();
    if (!merged) return null;
    // Models face -Z; the yaw math points +Z down the direction of travel.
    merged.rotateY(Math.PI);
    return merged;
  }

  async function loadVehicles() {
    let entries;
    try {
      const res = await fetch(`${ASSETS}vehicles_manifest.json`);
      if (!res.ok) throw new Error(`manifest ${res.status}`);
      entries = (await res.json()).vehicles;
      if (!Array.isArray(entries)) throw new Error('manifest has no vehicles');
      // weight 0 means "not road traffic" — the live ferry is spawned by ferries.js.
      entries = entries.filter((entry) => (entry.weight ?? 1) > 0);
      if (!entries.length) throw new Error('manifest has no road vehicles');
    } catch (error) {
      console.warn(`sf-assets: no vehicle fleet (${error.message}) — keeping procedural cars`);
      return;
    }

    const loader = createGLTFLoader();
    let loaded;
    try {
      loaded = await Promise.all(
        entries.map(async (entry) => ({
          entry,
          geometry: mergeVehicle((await loader.loadAsync(`${ASSETS}${entry.file}`)).scene),
        }))
      );
    } catch (error) {
      console.warn(`sf-assets: vehicle fleet failed to load (${error.message}) — keeping procedural cars`);
      return;
    }
    if (loaded.some((item) => !item.geometry)) {
      console.warn('sf-assets: a vehicle model had no geometry — keeping procedural cars');
      return;
    }

    const capacity = Math.ceil(CAR_COUNT / loaded.length);
    for (const { entry, geometry } of loaded) {
      const mesh = new InstancedMesh(geometry, fleetMaterial, capacity);
      mesh.name = `vehicle-${entry.id}`;
      mesh.instanceMatrix.setUsage(DynamicDrawUsage);
      mesh.castShadow = false;
      mesh.frustumCulled = false;
      mesh.count = 0;
      group.add(mesh);
      fleet.push(mesh);
    }
    fleetCursors = new Int32Array(fleet.length);
    carMesh.count = 0;
    carMesh.visible = false;
  }

  const cars = [];
  let cityPaths = [];
  city.onPaths((paths) => {
    cityPaths = paths;
  });

  // DataSF's street grid stops at the county line in the middle of the strait,
  // so the baked street ribbons only cover the first fifth of the Golden Gate.
  // A bespoke bridge therefore carries its own traffic path: one unbroken run
  // of the baked deck centreline, so a car seeded anywhere on it drives the
  // full span shore to shore instead of looping inside an approach stub.
  // A baked node's y is the deck centre, so the roadway a car stands on is
  // DECK_HALF_THICKNESS above it — the same surface `deckRibbon` builds.
  // Deck paths carry the surface directly, so the renderer's lift is taken
  // back out: wheels touch the roadway instead of hovering over it.
  const deckSpeed = manifest.streetClasses?.[0]?.speed ?? 28;
  const CAR_CLEARANCE = 0.05 - CAR_LIFT;
  const deckPaths = [];
  for (const [id, spec] of Object.entries(manifest.bridges || {})) {
    for (const deck of [spec, spec.east]) {
      if (!deck?.nodes || deck.nodes.length < 2) continue;
      const flat = new Float32Array(deck.nodes.length * 3);
      deck.nodes.forEach(([lon, lat, y], i) => {
        const [x, z] = project(lon, lat);
        flat[i * 3] = x;
        flat[i * 3 + 1] = y + DECK_HALF_THICKNESS + CAR_CLEARANCE;
        flat[i * 3 + 2] = z;
      });
      deckPaths.push({
        id,
        points: flat,
        baked: Float32Array.from(deck.nodes, ([, , y]) => y + DECK_HALF_THICKNESS + CAR_CLEARANCE),
        klass: 0,
        width: deck.deckWidth ?? 24,
        speed: deckSpeed,
        deck: true,
      });
    }
  }

  // An asset deck is a measured surface of its own, so once a GLB takes a
  // bridge over, its cars ride that surface: flat across the span the asset
  // covers, then down each approach ramp on the same grade `useBridgeAsset`
  // builds — from the asset deck to the abutment the streets already meet.
  function useBridgeDeckTop(id, ends) {
    const path = deckPaths.find((p) => p.id === id);
    const usable = (ends || []).filter((end) => Number.isFinite(end?.y));
    if (!path || !usable.length) return;
    const n = path.points.length / 3;
    const nodeAt = (i) => [path.points[i * 3], path.points[i * 3 + 2]];

    // The span itself is the asset's own flat deck.
    const surface = usable[0].y + CAR_CLEARANCE;
    for (let i = 0; i < n; i++) path.points[i * 3 + 1] = surface;

    // Each ramp grades from the abutment the streets meet up to that deck.
    for (const end of usable) {
      const anchor = end.toward === 'south' ? 0 : n - 1;
      const step = anchor === 0 ? 1 : -1;
      const [ax, az] = nodeAt(anchor);
      const abutment = path.baked[anchor];
      const ramp = [];
      for (let i = anchor; i >= 0 && i < n; i += step) {
        const [x, z] = nodeAt(i);
        if (Math.hypot(x - ax, z - az) >= Math.hypot(x - end.x, z - end.z)) break;
        ramp.push({ i, run: Math.hypot(x - ax, z - az) });
      }
      const run = ramp.length ? ramp[ramp.length - 1].run : 0;
      if (!run) continue;
      for (const node of ramp) {
        path.points[node.i * 3 + 1] = abutment + (surface - abutment) * Math.min(1, node.run / run);
      }
    }
  }

  // Street paths are short enough to test by their first vertex; a deck spans
  // kilometres, so it counts as nearby whenever any of its nodes is in range.
  function pathNear(path, pivot, range) {
    const stride = path.deck ? 3 : path.points.length;
    for (let i = 0; i < path.points.length; i += stride) {
      const dx = path.points[i] - pivot.x;
      const dz = path.points[i + 2] - pivot.z;
      if (dx * dx + dz * dz < range * range) return true;
    }
    return false;
  }

  function nearbyPaths(pivot) {
    const list = [];
    for (const source of [cityPaths, deckPaths]) {
      for (const path of source) {
        if (!path.meta) path.meta = polylineLengths(path.points);
        if (pathNear(path, pivot, CAR_RANGE)) list.push(path);
      }
    }
    return list;
  }

  let carRefresh = 0;

  // ------------------------------------------------------------- cable cars ---
  const cableCars = [];
  const cableMesh = new InstancedMesh(
    cableCarArchetype(),
    new MeshLambertMaterial({ color: '#8f2f24' }),
    CABLE_LINES.length * 3
  );
  cableMesh.instanceMatrix.setUsage(DynamicDrawUsage);
  cableMesh.frustumCulled = false;
  group.add(cableMesh);
  for (const line of CABLE_LINES) {
    const points = new Float32Array(line.points.length * 3);
    line.points.forEach(([lon, lat], i) => {
      const [x, z] = project(lon, lat);
      points[i * 3] = x;
      points[i * 3 + 1] = Math.max(0, sampleElevation(x, z)) + 1.4;
      points[i * 3 + 2] = z;
    });
    const { cumulative, total } = polylineLengths(points);
    for (let i = 0; i < 3; i++) {
      cableCars.push({ points, cumulative, total, d: (total / 3) * i, dir: i % 2 ? -1 : 1 });
    }
  }

  // ------------------------------------------------------------ pedestrians ---
  const pedGeometry = mergeGeometries(
    [
      (() => {
        const g = new CylinderGeometry(0.22, 0.22, 1.2, 5);
        g.translate(0, 0.6, 0);
        return g;
      })(),
      (() => {
        const g = new BoxGeometry(0.34, 0.42, 0.28);
        g.translate(0, 1.42, 0);
        return g;
      })(),
    ],
    false
  );
  pedGeometry.deleteAttribute('uv');
  const pedMesh = new InstancedMesh(pedGeometry, new MeshLambertMaterial({ color: '#3c4550' }), PED_COUNT);
  pedMesh.instanceMatrix.setUsage(DynamicDrawUsage);
  pedMesh.frustumCulled = false;
  pedMesh.count = 0;
  group.add(pedMesh);
  const peds = [];

  // ------------------------------------------------------------------ birds ---
  const birdGeometry = new ConeGeometry(0.5, 2.2, 3);
  birdGeometry.rotateX(Math.PI / 2);
  const birdMesh = new InstancedMesh(
    birdGeometry,
    new MeshBasicMaterial({ color: '#f4f2ea' }),
    BIRD_COUNT
  );
  birdMesh.instanceMatrix.setUsage(DynamicDrawUsage);
  birdMesh.frustumCulled = false;
  group.add(birdMesh);
  const flocks = [];
  const flockAnchors = [
    [-122.4098, 37.8087],
    [-122.4783, 37.8199],
    [-122.5107, 37.7621],
    [-122.3893, 37.7786],
    [-122.4405, 37.8066],
  ];
  for (let f = 0; f < flockAnchors.length; f++) {
    const [x, z] = project(flockAnchors[f][0], flockAnchors[f][1]);
    flocks.push({ x, z, radius: 90 + f * 40, height: 55 + f * 18, phase: f * 1.7 });
  }

  // ------------------------------------------------------------------ flags ---
  const flags = [];
  const flagSpots = [
    // Anchor and mast foot come from the Ferry Building GLB, not the landmark
    // registry: the asset stands on its surveyed centre ~20 m east of the
    // registry point, and its pole steps out of the crown dome at 73.5 m.
    {
      id: 'ferryBuilding',
      anchor: [-122.3933697, 37.7955227],
      height: 73.2,
      pole: 10,
      us: true,
    },
    { id: 'oraclePark', height: 52, colors: ['#e07a1f', '#2b2b2b'] },
    { id: 'fishermansWharf', height: 20, colors: ['#c8332c', '#f0ece2'] },
  ];
  const US_COLORS = ['#b22234', '#f0ece2', '#25406b'];
  for (const spot of flagSpots) {
    const landmark = manifest.landmarks.find((l) => l.id === spot.id);
    if (!landmark) continue;
    const anchor = spot.anchor || [landmark.lon, landmark.lat];
    const [x, z] = project(anchor[0], anchor[1]);
    const base = Math.max(0, sampleElevation(x, z));
    const poleHeight = spot.pole || 12;
    const colors = spot.us ? US_COLORS : spot.colors;
    const pole = new Mesh(
      new CylinderGeometry(0.22, 0.26, poleHeight, 6),
      new MeshLambertMaterial({ color: '#c9c3b6' })
    );
    pole.position.set(x, base + spot.height + poleHeight / 2, z);
    group.add(pole);
    const material = new ShaderMaterial({
      uniforms: {
        uTime: shared.uTime,
        uColorA: { value: new Color(colors[0]) },
        uColorB: { value: new Color(colors[1]) },
        uColorC: { value: new Color(colors[2] || colors[0]) },
      },
      vertexShader: FLAG_VERT,
      fragmentShader: spot.us ? FLAG_FRAG_US : FLAG_FRAG,
      side: DoubleSide,
    });
    const flag = new Mesh(new PlaneGeometry(4.4, 2.8, 12, 3), material);
    // Hoist edge inside the mast, head just under the truck.
    flag.position.set(x + 2.3, base + spot.height + poleHeight - 1.6, z);
    group.add(flag);
    flags.push(flag);
  }

  // ------------------------------------------------------------- toy extras ---
  // Created once and parked invisible: the diorama toggle must not allocate.
  const toyGroup = new Group();
  toyGroup.name = 'toy-life';
  toyGroup.visible = false;
  group.add(toyGroup);

  const craneCount = 8;
  const craneMesh = new InstancedMesh(
    craneArchetype(),
    new MeshLambertMaterial({ color: '#e2b23c' }),
    craneCount
  );
  craneMesh.frustumCulled = false;
  toyGroup.add(craneMesh);
  CRANE_SITES.slice(0, craneCount).forEach(([lon, lat], i) => {
    const [x, z] = project(lon, lat);
    dummy.position.set(x, Math.max(0, sampleElevation(x, z)), z);
    dummy.rotation.set(0, (i * 2.399) % (Math.PI * 2), 0);
    dummy.scale.setScalar(0.8 + (i % 3) * 0.15);
    dummy.updateMatrix();
    craneMesh.setMatrixAt(i, dummy.matrix);
  });
  craneMesh.instanceMatrix.needsUpdate = true;

  const balloonCount = BALLOON_SITES.length;
  const balloonMesh = new InstancedMesh(
    balloonArchetype(),
    new MeshLambertMaterial({ vertexColors: true }),
    balloonCount
  );
  balloonMesh.instanceMatrix.setUsage(DynamicDrawUsage);
  balloonMesh.frustumCulled = false;
  const balloonColors = new Float32Array(balloonCount * 3);
  const balloonPalette = ['#e8735a', '#d9a441', '#3fa8a0', '#6db3d9', '#e2557f', '#8fd0a8'];
  for (let i = 0; i < balloonCount; i++) {
    paint.set(balloonPalette[i % balloonPalette.length]);
    balloonColors[i * 3] = paint.r;
    balloonColors[i * 3 + 1] = paint.g;
    balloonColors[i * 3 + 2] = paint.b;
  }
  balloonMesh.instanceColor = new BufferAttribute(balloonColors, 3);
  toyGroup.add(balloonMesh);
  const balloons = BALLOON_SITES.map(([lon, lat], i) => {
    const [x, z] = project(lon, lat);
    return {
      x,
      z,
      ground: Math.max(0, sampleElevation(x, z)),
      height: 150 + i * 45,
      radius: 90 + i * 30,
      phase: i * 1.31,
    };
  });

  const heliBody = mergeGeometries(
    [
      (() => {
        const g = new IcosahedronGeometry(3.2, 1);
        g.scale(1, 0.85, 1.5);
        return g;
      })(),
      (() => {
        const g = new BoxGeometry(0.7, 0.7, 7).toNonIndexed();
        g.translate(0, 1.2, -6);
        return g;
      })(),
      (() => {
        const g = new BoxGeometry(0.5, 2.6, 0.5).toNonIndexed();
        g.translate(0, 2.2, -9);
        return g;
      })(),
    ],
    false
  );
  heliBody.deleteAttribute('uv');
  const helicopter = new Group();
  const heliHull = new Mesh(heliBody, new MeshLambertMaterial({ color: '#e2554f' }));
  helicopter.add(heliHull);
  const heliRotor = new Mesh(
    new BoxGeometry(18, 0.2, 0.9),
    new MeshLambertMaterial({ color: '#4a4a52' })
  );
  heliRotor.position.y = 3.4;
  helicopter.add(heliRotor);
  toyGroup.add(helicopter);
  const [heliX, heliZ] = project(HELI_CENTER[0], HELI_CENTER[1]);

  // Cars and pedestrians are restyled in place: same pools, toy scale and paint.
  const CAR_PALETTES = {
    base: carPalette,
    toy: ['#e8735a', '#f2c14e', '#3fa8a0', '#6db3d9', '#e2557f', '#8fd0a8', '#f4f0e6'],
  };
  let carScale = 1;
  let pedScale = 1;
  let toy = false;
  let carCap = CAR_COUNT;
  let pedCap = PED_COUNT;
  let birdCap = BIRD_COUNT;

  function paintCars(list) {
    // Fleet colours are baked into the models; only the fallback pool is tinted.
    if (fleet.length) return;
    for (let i = 0; i < CAR_COUNT; i++) {
      paint.set(list[i % list.length]);
      carColors[i * 3] = paint.r;
      carColors[i * 3 + 1] = paint.g;
      carColors[i * 3 + 2] = paint.b;
    }
  }

  const shipStyle = {
    base: ships.map((s) => ({ color: s.mesh.material.color.getHex(), scale: [1, 1, 1] })),
  };

  function setToy(on) {
    toy = on;
    toyGroup.visible = on;
    carScale = on ? 1.6 : 1;
    pedScale = on ? 1.3 : 1;
    paintCars(on ? CAR_PALETTES.toy : CAR_PALETTES.base);
    lightMesh.material.color.set(on ? '#ffffff' : '#fff2cf');
    cableMesh.material.color.set(on ? '#d63b2c' : '#8f2f24');
    pedMesh.material.color.set(on ? '#4a5a72' : '#3c4550');
    // Fat toy tugboats: the same hulls, stubbier and brightly painted.
    ships.forEach((ship, i) => {
      ship.toyScale = on ? [1.6, 1.35, 0.62] : null;
      ship.mesh.material.color.set(
        on
          ? ship.route.kind === 'container'
            ? '#e8735a'
            : ship.route.kind === 'ferry'
              ? '#f4f0e6'
              : '#ffffff'
          : shipStyle.base[i].color
      );
    });
  }

  function update(dt, pivot, cameraPos) {
    const night = shared.uNight.value;

    // Ships.
    for (const ship of ships) {
      const closed =
        Math.abs(ship.points[0] - ship.points[ship.points.length - 3]) < 1 &&
        Math.abs(ship.points[2] - ship.points[ship.points.length - 1]) < 1;
      for (let i = 0; i < ship.instances.length; i++) {
        const inst = ship.instances[i];
        inst.d += ship.speed * dt * inst.dir;
        if (closed) {
          if (inst.d > ship.total) inst.d -= ship.total;
          if (inst.d < 0) inst.d += ship.total;
        } else if (inst.d > ship.total || inst.d < 0) {
          inst.dir *= -1;
          inst.d = Math.min(ship.total, Math.max(0, inst.d));
        }
        samplePolyline(ship.points, ship.cumulative, ship.total, inst.d, position, tangent);
        inst.bob += dt * 1.6;
        dummy.position.set(position.x, 0.3 + Math.sin(inst.bob) * 0.35, position.z);
        dummy.rotation.set(Math.sin(inst.bob * 0.7) * 0.02, Math.atan2(tangent.x, tangent.z), Math.cos(inst.bob) * 0.02);
        if (ship.toyScale) dummy.scale.set(...ship.toyScale);
        else dummy.scale.setScalar(1);
        dummy.updateMatrix();
        ship.mesh.setMatrixAt(i, dummy.matrix);

        const wakeLength = ship.route.kind === 'container' ? 220 : ship.route.kind === 'ferry' ? 90 : 34;
        dummy.position.set(
          position.x - tangent.x * wakeLength * 0.5 * inst.dir,
          0.25,
          position.z - tangent.z * wakeLength * 0.5 * inst.dir
        );
        dummy.rotation.set(-Math.PI / 2, 0, -Math.atan2(tangent.x, tangent.z));
        dummy.scale.set(ship.route.kind === 'container' ? 22 : 10, wakeLength, 1);
        dummy.updateMatrix();
        ship.wake.setMatrixAt(i, dummy.matrix);
      }
      ship.mesh.instanceMatrix.needsUpdate = true;
      ship.wake.instanceMatrix.needsUpdate = true;
    }

    // Traffic: re-seed the pool onto nearby real centrelines as you move.
    carRefresh -= dt;
    if (carRefresh <= 0 && (cityPaths.length || deckPaths.length)) {
      carRefresh = 1.5;
      const candidates = nearbyPaths(pivot);
      // A bridge is one path among hundreds of city blocks, so a plain random
      // draw would leave the deck nearly empty; every sixth slot is reserved
      // for it, which keeps the whole span carrying traffic.
      const decks = candidates.filter((path) => path.deck);
      if (candidates.length) {
        for (let i = 0; i < CAR_COUNT; i++) {
          const existing = cars[i];
          const wantsDeck = decks.length > 0 && i % 6 === 0;
          const stillClose =
            existing && pathNear(existing.path, pivot, CAR_RANGE * 1.3) && (!wantsDeck || existing.path.deck);
          if (stillClose) continue;
          const pool = wantsDeck ? decks : candidates;
          const path = pool[Math.floor(Math.random() * pool.length)];
          cars[i] = {
            path,
            d: Math.random() * path.meta.total,
            dir: Math.random() < 0.5 ? -1 : 1,
            lane: Math.random() < 0.5 ? -1 : 1,
            speed: path.speed * (0.75 + Math.random() * 0.5),
          };
        }
      }
    }

    let visibleCars = 0;
    fleetCursors.fill(0);
    for (let i = 0; i < Math.min(cars.length, carCap); i++) {
      const car = cars[i];
      if (!car) continue;
      const { cumulative, total } = car.path.meta;
      if (total < 30) continue;
      car.d += car.speed * dt * car.dir;
      if (car.d > total) car.d -= total;
      if (car.d < 0) car.d += total;
      samplePolyline(car.path.points, cumulative, total, car.d, position, tangent);
      if (position.distanceTo(cameraPos) > CAR_RANGE * 1.6) continue;
      const offset = (car.path.width / 4) * car.lane * car.dir;
      dummy.position.set(position.x + tangent.z * offset, position.y + CAR_LIFT, position.z - tangent.x * offset);
      dummy.rotation.set(0, Math.atan2(tangent.x * car.dir, tangent.z * car.dir), 0);
      dummy.scale.setScalar(carScale);
      dummy.updateMatrix();
      if (fleet.length) {
        // Slot i always drives the same vehicle type, so every type is on the
        // road with the same frequency.
        const type = i % fleet.length;
        const mesh = fleet[type];
        if (fleetCursors[type] >= mesh.instanceMatrix.count) continue;
        mesh.setMatrixAt(fleetCursors[type]++, dummy.matrix);
      } else {
        carMesh.setMatrixAt(visibleCars, dummy.matrix);
        carMesh.instanceColor.array[visibleCars * 3] = carColors[i * 3];
        carMesh.instanceColor.array[visibleCars * 3 + 1] = carColors[i * 3 + 1];
        carMesh.instanceColor.array[visibleCars * 3 + 2] = carColors[i * 3 + 2];
      }
      if (night > 0.15 || toy) {
        dummy.position.y += 0.55;
        dummy.position.x += tangent.x * 2.4 * car.dir;
        dummy.position.z += tangent.z * 2.4 * car.dir;
        dummy.rotation.x = -Math.PI / 2;
        dummy.updateMatrix();
        lightMesh.setMatrixAt(visibleCars, dummy.matrix);
      }
      visibleCars++;
    }
    if (fleet.length) {
      for (let t = 0; t < fleet.length; t++) {
        fleet[t].count = fleetCursors[t];
        fleet[t].instanceMatrix.needsUpdate = true;
      }
    } else {
      carMesh.count = visibleCars;
      carMesh.instanceMatrix.needsUpdate = true;
      carMesh.instanceColor.needsUpdate = true;
    }
    lightMesh.count = night > 0.15 || toy ? visibleCars : 0;
    lightMesh.instanceMatrix.needsUpdate = true;
    lightMesh.material.opacity = toy ? Math.max(0.5, Math.min(0.85, night)) : Math.min(0.8, night);

    // Cable cars.
    for (let i = 0; i < cableCars.length; i++) {
      const car = cableCars[i];
      car.d += 4.2 * dt * car.dir;
      if (car.d > car.total || car.d < 0) {
        car.dir *= -1;
        car.d = Math.min(car.total, Math.max(0, car.d));
      }
      samplePolyline(car.points, car.cumulative, car.total, car.d, position, tangent);
      dummy.position.copy(position);
      dummy.rotation.set(0, Math.atan2(tangent.x, tangent.z), 0);
      dummy.scale.setScalar(1);
      dummy.updateMatrix();
      cableMesh.setMatrixAt(i, dummy.matrix);
    }
    cableMesh.instanceMatrix.needsUpdate = true;

    // Pedestrians: only worth spawning when the camera is down in the streets.
    if (cameraPos.y - pivot.y < 900 && cityPaths.length) {
      if (peds.length === 0) {
        for (let i = 0; i < PED_COUNT; i++) peds.push(null);
      }
      const candidates = [];
      for (const path of cityPaths) {
        if (!path.meta) path.meta = polylineLengths(path.points);
        if (Math.hypot(path.points[0] - pivot.x, path.points[2] - pivot.z) < PED_RANGE * 2) candidates.push(path);
      }
      let visible = 0;
      for (let i = 0; i < pedCap && candidates.length; i++) {
        let ped = peds[i];
        if (!ped || Math.hypot(ped.x - pivot.x, ped.z - pivot.z) > PED_RANGE * 2.2) {
          const path = candidates[Math.floor(Math.random() * candidates.length)];
          const d = Math.random() * path.meta.total;
          samplePolyline(path.points, path.meta.cumulative, path.meta.total, d, position, tangent);
          const side = Math.random() < 0.5 ? -1 : 1;
          // Down the middle of the sidewalk, standing on the plinth top where
          // the street has one. Path points carry the car lift, which the
          // kerb height replaces rather than stacks on.
          const walk = path.sidewalk;
          const out = path.width / 2 + (walk ? walk.width / 2 : 1.9);
          ped = {
            x: position.x + tangent.z * out * side,
            y: position.y - (path.lift || 0) + (walk ? walk.curb : 0),
            z: position.z - tangent.x * out * side,
            vx: tangent.x * (Math.random() < 0.5 ? -1 : 1) * 1.3,
            vz: tangent.z * (Math.random() < 0.5 ? -1 : 1) * 1.3,
            t: Math.random() * 6.28,
          };
          peds[i] = ped;
        }
        ped.x += ped.vx * dt;
        ped.z += ped.vz * dt;
        ped.t += dt * 6;
        if (Math.hypot(ped.x - cameraPos.x, ped.z - cameraPos.z) > PED_RANGE * 1.6) continue;
        dummy.position.set(ped.x, ped.y + Math.abs(Math.sin(ped.t)) * 0.06, ped.z);
        dummy.rotation.set(0, Math.atan2(ped.vx, ped.vz), 0);
        dummy.scale.set(pedScale, pedScale * (0.94 + Math.abs(Math.sin(ped.t)) * 0.08), pedScale);
        dummy.updateMatrix();
        pedMesh.setMatrixAt(visible, dummy.matrix);
        visible++;
      }
      pedMesh.count = visible;
      pedMesh.instanceMatrix.needsUpdate = true;
    } else {
      pedMesh.count = 0;
    }

    // Gulls.
    const time = shared.uTime.value;
    birdMesh.count = birdCap;
    for (let i = 0; i < birdCap; i++) {
      const flock = flocks[i % flocks.length];
      const k = Math.floor(i / flocks.length);
      const a = time * 0.35 + flock.phase + k * 0.7;
      const r = flock.radius * (0.65 + ((k * 37) % 10) / 22);
      const x = flock.x + Math.cos(a) * r;
      const z = flock.z + Math.sin(a * 1.1) * r;
      const y = flock.height + Math.sin(a * 2.3 + k) * 12;
      dummy.position.set(x, y, z);
      dummy.rotation.set(Math.sin(a * 3) * 0.2, -a + Math.PI / 2, Math.sin(a * 4 + k) * 0.35);
      dummy.scale.setScalar(1);
      dummy.updateMatrix();
      birdMesh.setMatrixAt(i, dummy.matrix);
    }
    birdMesh.instanceMatrix.needsUpdate = true;
    birdMesh.visible = night < 0.7;

    for (const flag of flags) flag.visible = true;

    // Toy extras: balloons drift on lazy circles, the helicopter orbits downtown.
    if (toy) {
      for (let i = 0; i < balloons.length; i++) {
        const b = balloons[i];
        const a = time * 0.05 + b.phase;
        dummy.position.set(
          b.x + Math.cos(a) * b.radius,
          b.ground + b.height + Math.sin(time * 0.3 + b.phase) * 6,
          b.z + Math.sin(a * 1.2) * b.radius
        );
        dummy.rotation.set(0, a, Math.sin(time * 0.4 + b.phase) * 0.05);
        dummy.scale.setScalar(1);
        dummy.updateMatrix();
        balloonMesh.setMatrixAt(i, dummy.matrix);
      }
      balloonMesh.instanceMatrix.needsUpdate = true;

      const a = time * 0.12;
      helicopter.position.set(heliX + Math.cos(a) * 620, 250, heliZ + Math.sin(a) * 620);
      helicopter.rotation.y = -a;
      heliRotor.rotation.y += dt * 34;
    }
  }

  loadVehicles();

  return {
    group,
    update,
    setToy,
    setQuality(tier) {
      const low = tier === 'low';
      carCap = low ? LOW_CAPS.cars : CAR_COUNT;
      pedCap = low ? LOW_CAPS.peds : PED_COUNT;
      birdCap = low ? LOW_CAPS.birds : BIRD_COUNT;
    },
    useBridgeDeckTop,
    // The live-ferry system hides the two looping procedural ferries when real
    // vessel positions are flowing, and shows them again on any fallback.
    // Container and sail traffic are untouched.
    setProceduralFerriesVisible(visible) {
      for (const ship of ships) {
        if (ship.route.kind !== 'ferry') continue;
        ship.mesh.visible = visible;
        ship.wake.visible = visible;
      }
    },
    get carCount() {
      if (!fleet.length) return carMesh.count;
      let total = 0;
      for (const mesh of fleet) total += mesh.count;
      return total;
    },
  };
}
