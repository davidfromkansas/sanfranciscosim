// The street furniture kit: lamps, signals, hydrants, shelters and the
// commercial-frontage clutter that makes a block look inhabited.
//
// Same contract as the landmark assets (`assets.js`): GLB, real metres, base
// centre on z=0, front −Y, flat `Toy_*` colours, `_Glow` on the surfaces that
// light up. Every piece is merged once at load into one body buffer plus one
// glow buffer, and drawn as an InstancedMesh shared by every streamed cell — so
// the whole kit costs two draw calls per piece type, not two per object.
//
// Placement itself is decided in the tile worker (`streetplan.js`) from the
// baked street polylines; this module supplies the two hint arrays the planner
// cannot derive from geometry (Market Street's centreline and the shopfronts,
// both from the context layer), filters the anchors against the terrain, and
// owns the buffers.
//
// If the index, a GLB or the contract fails, nothing is placed, one warning is
// logged, and the layer 1 streets render exactly as they did before.

import {
  BufferAttribute,
  DynamicDrawUsage,
  InstancedMesh,
  Matrix4,
  MeshBasicMaterial,
  MeshLambertMaterial,
  Object3D,
  Quaternion,
  Vector3,
} from 'three';
import { createGLTFLoader } from './gltf.js';
import { mergeGeometries } from 'three/addons/utils/BufferGeometryUtils.js';
import { alignPoolToGround, createLampPoolGeometry, createLampPoolMaterial } from './materials.js';
import { shared } from './env.js';
import { tileUrl } from './data.js';
import { ANCHOR_STRIDE, PIECES } from './streetplan.js';

const KIT_DIR = `${import.meta.env.BASE_URL}sf-assets/streetkit/`;
const CTX_CELL = 500;
const MAX_SLOPE = 0.4; // m of terrain relief across a piece's footprint
// Shopfront-ish categories from context.js's CATEGORY_LABELS: the doors that
// make a street a shopping street.
const SHOP_CATEGORIES = new Set([4, 5, 6, 7, 15, 16, 17, 22, 24]);
// Worst case per group, so a dense downtown group cannot blow the instance
// budget on its own.
const GROUP_LIMIT = 2400;
// Which pieces light the road, and how wide their pool is. Only the lamps: a
// signal head or a lit shelter is not what the street is lit by. Radii follow
// the fixture — the Path of Gold standards on Market are taller and throw
// wider than a residential pole.
const POOL_RADIUS = {
  sl_standard: 7.5,
  sl_pathofgold: 9,
  sl_residential: 6,
};
const CAPACITY = {
  sl_standard: 3000,
  sl_pathofgold: 400,
  sl_residential: 2000,
  traffic_signal: 900,
  hydrant: 1400,
  mailbox: 500,
  muni_shelter: 250,
  bench: 700,
  trashcan: 900,
  newsboxes: 500,
  planter: 700,
  bikerack: 500,
  cafe_set: 300,
  market_stall: 300,
  parklet: 250,
};

// ------------------------------------------------------------------ loading ---

// One GLB, merged the way assets.js merges a landmark: flat material colours
// baked to vertex colours so many objects and materials collapse into one
// buffer, split by whether the surface glows at night.
function mergePiece(root, id) {
  const body = [];
  const glow = [];
  const materials = new Set();
  root.updateMatrixWorld(true);
  root.traverse((object) => {
    if (!object.isMesh) return;
    const material = object.material;
    if (!material || !material.name || !material.name.startsWith('Toy_')) {
      throw new Error(`${id}: material "${material?.name || 'unnamed'}" is not a Toy_* flat colour`);
    }
    if (material.transparent || material.map) {
      throw new Error(`${id}: material "${material.name}" uses transparency or a texture`);
    }
    materials.add(material.name);

    const geometry = object.geometry.clone();
    geometry.applyMatrix4(object.matrixWorld);
    geometry.deleteAttribute('uv');
    geometry.deleteAttribute('uv1');
    geometry.deleteAttribute('tangent');
    if (!geometry.attributes.normal) geometry.computeVertexNormals();
    const count = geometry.attributes.position.count;
    const colors = new Float32Array(count * 3);
    for (let i = 0; i < count; i++) {
      colors[i * 3] = material.color.r;
      colors[i * 3 + 1] = material.color.g;
      colors[i * 3 + 2] = material.color.b;
    }
    geometry.setAttribute('color', new BufferAttribute(colors, 3));
    (material.name.endsWith('_Glow') ? glow : body).push(geometry);
  });

  const bodyGeometry = mergeGeometries(body, false);
  if (!bodyGeometry) throw new Error(`${id}: nothing to merge`);
  for (const g of body) g.dispose();
  let glowGeometry = null;
  if (glow.length) {
    glowGeometry = mergeGeometries(glow, false);
    for (const g of glow) g.dispose();
  }
  return { bodyGeometry, glowGeometry, materials: [...materials].sort() };
}

/** Loads and merges the whole kit. Rejects if any piece breaks the contract. */
export async function loadStreetKit() {
  const res = await fetch(`${KIT_DIR}streetkit_index.json`);
  if (!res.ok) throw new Error(`index ${res.status}`);
  const index = await res.json();
  if (!index || !Array.isArray(index.pieces)) throw new Error('index has no pieces');

  const byId = new Map(index.pieces.map((p) => [p.id, p]));
  const missing = PIECES.filter((id) => !byId.has(id));
  if (missing.length) throw new Error(`index is missing ${missing.join(', ')}`);

  const loader = createGLTFLoader();
  const pieces = [];
  for (const id of PIECES) {
    const entry = byId.get(id);
    const gltf = await loader.loadAsync(`${KIT_DIR}${entry.file}`);
    pieces.push({ id, entry, ...mergePiece(gltf.scene, id) });
  }
  return { pieces };
}

// ------------------------------------------------------------------- hints ---

// The context-layer facts the worker cannot see: where Market Street runs and
// where the shops are. Cells are fetched once and cached; these are the same
// sidecars the picking layer already streams for the cells under the camera.
export function createStreetHints(manifest, contextCells) {
  const grid = manifest.grid;
  // LRU: hints for cells the camera left long ago are cheap to refetch (the
  // sidecars are immutable-cached JSON) and needless to keep for a whole
  // session. Recency-refreshed on read, oldest evicted past the cap.
  const cells = new Map();
  const CELLS_MAX = 150;
  const EMPTY = { market: [], commercial: [] };

  function remember(key, value) {
    cells.set(key, value);
    while (cells.size > CELLS_MAX) {
      cells.delete(cells.keys().next().value);
    }
    return value;
  }

  function load(key) {
    const cached = cells.get(key);
    if (cached) {
      cells.delete(key);
      cells.set(key, cached);
      return cached;
    }
    // Cells the bake never wrote carry no hints, and requesting one is a 404.
    if (contextCells && !contextCells.has(key)) {
      return remember(key, EMPTY);
    }
    const promise = fetch(tileUrl(`ctx/${key}.json`))
      .then((r) => (r.ok ? r.json() : null))
      .catch(() => null)
      .then((cell) => {
        const market = [];
        const commercial = [];
        for (const run of cell?.s || []) {
          if (run.n !== 'MARKET ST') continue;
          for (let i = 2; i < run.p.length; i += 2) {
            market.push(run.p[i - 2], run.p[i - 1], run.p[i], run.p[i + 1]);
          }
        }
        const pick = cell?.pick;
        for (let i = 0; pick && i < pick.id.length; i++) {
          const info = cell.b[pick.id[i]];
          if (info && SHOP_CATEGORIES.has(info.c)) commercial.push(pick.x[i], pick.z[i]);
        }
        const value = { market, commercial };
        // The promise entry may already have been evicted under pressure;
        // remember() re-inserts the resolved value either way.
        return remember(key, value);
      });
    return remember(key, promise);
  }

  /** Hint arrays covering a box, with a margin for the pieces on its edge. */
  return async function hintsFor(minX, minZ, maxX, maxZ, margin = 60) {
    const x0 = Math.floor((minX - margin - grid.originX) / CTX_CELL);
    const x1 = Math.floor((maxX + margin - grid.originX) / CTX_CELL);
    const z0 = Math.floor((minZ - margin - grid.originZ) / CTX_CELL);
    const z1 = Math.floor((maxZ + margin - grid.originZ) / CTX_CELL);
    const wanted = [];
    for (let cz = z0; cz <= z1; cz++) {
      for (let cx = x0; cx <= x1; cx++) {
        if (cx < 0 || cz < 0 || cx >= grid.cols || cz >= grid.rows) continue;
        wanted.push(load(`${cx}_${cz}`));
      }
    }
    const loaded = await Promise.all(wanted);
    const market = [];
    const commercial = [];
    for (const cell of loaded) {
      market.push(...cell.market);
      commercial.push(...cell.commercial);
    }
    return { market: new Float32Array(market), commercial: new Float32Array(commercial) };
  };
}

// ----------------------------------------------------------------- instances ---

/**
 * Owns one InstancedMesh pair per piece type, shared by every group in the near
 * tier. Groups hand in their anchors and get them back out on eviction; the
 * matrices are re-packed so the pool never fragments.
 */
export function createStreetKitFleet(scene, kit, sampleElevation) {
  const root = new Object3D();
  root.name = 'streetkit';
  scene.add(root);

  const bodyMaterial = new MeshLambertMaterial({ vertexColors: true });
  const glowMaterial = new MeshBasicMaterial({ vertexColors: true, transparent: true, opacity: 0.2 });
  const poolMaterial = createLampPoolMaterial();
  const poolGeometry = createLampPoolGeometry();
  const matrix = new Matrix4();
  const poolMatrix = new Matrix4();
  const position = new Vector3();
  const quaternion = new Quaternion();
  const scale = new Vector3(1, 1, 1);
  const poolScale = new Vector3(1, 1, 1);
  const poolTilt = new Quaternion();
  const axis = new Vector3(0, 1, 0);
  // The pool sits on the pavement the pole stands on: the kit contract puts a
  // piece's origin at its base centre, so the anchor's own y is ground level.
  const POOL_LIFT = 0.08;

  const types = kit.pieces.map((piece) => {
    const capacity = CAPACITY[piece.id] || 400;
    const body = new InstancedMesh(piece.bodyGeometry, bodyMaterial, capacity);
    body.instanceMatrix.setUsage(DynamicDrawUsage);
    body.name = `streetkit-${piece.id}`;
    body.count = 0;
    body.visible = false;
    body.frustumCulled = false; // instances are spread across the whole near tier
    root.add(body);
    let glow = null;
    if (piece.glowGeometry) {
      glow = new InstancedMesh(piece.glowGeometry, glowMaterial, capacity);
      glow.instanceMatrix.setUsage(DynamicDrawUsage);
      glow.name = `streetkit-${piece.id}-glow`;
      glow.count = 0;
      glow.visible = false;
      glow.frustumCulled = false;
      root.add(glow);
    }
    let pool = null;
    const poolRadius = POOL_RADIUS[piece.id] || 0;
    if (poolRadius) {
      pool = new InstancedMesh(poolGeometry, poolMaterial, capacity);
      pool.instanceMatrix.setUsage(DynamicDrawUsage);
      pool.name = `streetkit-${piece.id}-pool`;
      pool.count = 0;
      pool.visible = false;
      pool.frustumCulled = false;
      pool.renderOrder = 3; // after the road ribbon, so the wash lands on it
      root.add(pool);
    }
    return { id: piece.id, capacity, body, glow, pool, poolRadius, groups: new Map(), dirty: false, overflow: 0 };
  });

  let instances = 0;
  let overflowWarned = false;

  // Terrain relief across the piece's own footprint. A kerb that steps a metre
  // inside two metres would leave the piece floating or buried, so it is simply
  // not placed there.
  function tooSteep(x, z) {
    const r = 1.2;
    let min = Infinity;
    let max = -Infinity;
    for (const [dx, dz] of [
      [-r, -r],
      [r, -r],
      [-r, r],
      [r, r],
    ]) {
      const y = sampleElevation(x + dx, z + dz);
      if (y < min) min = y;
      if (y > max) max = y;
    }
    return max - min > MAX_SLOPE;
  }

  // Quality mask: the placement data always stays planned and packed, only
  // the meshes hide, so the governor can pull this lever without a replan.
  // low keeps the pieces that carry the street's function (lamps, signals);
  // medium sheds the clutter that reads only up close.
  const LOW_KEEPS = new Set(['sl_standard', 'sl_pathofgold', 'sl_residential', 'traffic_signal']);
  const MEDIUM_DROPS = new Set(['newsboxes', 'planter', 'bikerack', 'trashcan']);
  let allowedId = () => true;
  // The pools are ground-level overdraw, so the tier scales them down and
  // `low` switches them off. `poolsLit` is the night gate, updated per frame.
  let poolStrength = 1;
  // Multiplier on each lamp's pool radius; fill cost goes as its square.
  let poolRadiusScale = 1;
  let poolsLit = false;

  function applyVisibility(type) {
    const on = type.body.count > 0 && allowedId(type.id);
    type.body.visible = on;
    if (type.glow) type.glow.visible = on;
    // The pool follows its pole, but only while the night ramp has it lit and
    // the tier is paying for pools at all.
    if (type.pool) type.pool.visible = on && poolsLit;
  }

  function repack(type) {
    let n = 0;
    for (const list of type.groups.values()) {
      for (let i = 0; i < list.length; i += 16) {
        if (n >= type.capacity) break;
        matrix.fromArray(list, i);
        type.body.setMatrixAt(n, matrix);
        if (type.glow) type.glow.setMatrixAt(n, matrix);
        if (type.pool) {
          // On the ground under the pole: the pole's translation, tilted to the
          // grade rather than the pole's own yaw (a disc has no yaw to inherit),
          // scaled to the pool radius.
          position.setFromMatrixPosition(matrix);
          alignPoolToGround(poolTilt, position.x, position.z, sampleElevation);
          position.y += POOL_LIFT;
          const radius = type.poolRadius * poolRadiusScale;
          poolScale.set(radius, 1, radius);
          poolMatrix.compose(position, poolTilt, poolScale);
          type.pool.setMatrixAt(n, poolMatrix);
        }
        n++;
      }
    }
    type.body.count = n;
    type.body.instanceMatrix.needsUpdate = true;
    if (type.glow) {
      type.glow.count = n;
      type.glow.instanceMatrix.needsUpdate = true;
    }
    if (type.pool) {
      type.pool.count = n;
      type.pool.instanceMatrix.needsUpdate = true;
    }
    applyVisibility(type);
    return n;
  }

  function recount() {
    instances = types.reduce((sum, type) => sum + type.body.count, 0);
  }

  return {
    root,
    setQuality(tier, quality = null) {
      allowedId =
        tier === 'low'
          ? (id) => LOW_KEEPS.has(id)
          : tier === 'medium'
            ? (id) => !MEDIUM_DROPS.has(id)
            : () => true;
      // From the QUALITY table when it is given. This used to re-derive the
      // numbers from the tier NAME, which quietly made the table's poolScale
      // and poolStrength dead settings — editing them changed nothing.
      poolStrength = quality?.poolStrength ?? (tier === 'low' ? 0 : tier === 'medium' ? 0.9 : 1);
      const nextScale = quality?.poolScale ?? (tier === 'medium' ? 0.7 : 1);
      if (nextScale !== poolRadiusScale) {
        poolRadiusScale = nextScale;
        // The radius is baked into each pool's matrix, so a change to it has to
        // be repacked rather than just re-uniformed.
        for (const type of types) if (type.pool) repack(type);
      }
      if (poolStrength === 0) poolsLit = false;
      for (const type of types) applyVisibility(type);
    },
    /** Adds one group's planned anchors. Returns how many pieces were placed. */
    add(key, anchors) {
      if (!anchors || anchors.length === 0) return 0;
      const buckets = new Map();
      let placed = 0;
      for (let i = 0; i < anchors.length; i += ANCHOR_STRIDE) {
        const type = types[anchors[i]];
        if (!type) continue;
        const x = anchors[i + 1];
        const y = anchors[i + 2];
        const z = anchors[i + 3];
        if (tooSteep(x, z)) continue;
        let list = buckets.get(type);
        if (!list) buckets.set(type, (list = []));
        if (list.length / 16 + (type.groups.get(key)?.length || 0) / 16 >= type.capacity) {
          type.overflow++;
          continue;
        }
        position.set(x, y, z);
        quaternion.setFromAxisAngle(axis, anchors[i + 4]);
        matrix.compose(position, quaternion, scale);
        for (let m = 0; m < 16; m++) list.push(matrix.elements[m]);
        placed++;
      }
      for (const [type, list] of buckets) {
        type.groups.set(key, list);
        repack(type);
      }
      recount();
      const overflowed = types.filter((t) => t.overflow > 0);
      if (overflowed.length && !overflowWarned) {
        overflowWarned = true;
        console.warn(`[streetkit] instance capacity reached for ${overflowed.map((t) => t.id).join(', ')}`);
      }
      return placed;
    },
    remove(key) {
      let removed = false;
      for (const type of types) {
        if (!type.groups.delete(key)) continue;
        repack(type);
        removed = true;
      }
      if (removed) recount();
      return removed;
    },
    clear() {
      for (const type of types) {
        if (type.groups.size === 0) continue;
        type.groups.clear();
        repack(type);
      }
      recount();
    },
    update() {
      // Lamp heads, signal lenses and the shelter strip are the only lit
      // surfaces; they ignite on the same dusk curve as the landmark glows.
      glowMaterial.opacity = Math.min(1, 0.1 + shared.uNight.value * 0.95);
      // The pools ignite on the same curve, but from nothing: an unlit lamp
      // throws no light, so there is no daytime floor here.
      poolMaterial.opacity = Math.min(1, shared.uNight.value * 1.1) * poolStrength;
      const lit = shared.uNight.value > 0.08 && poolStrength > 0;
      if (lit !== poolsLit) {
        poolsLit = lit;
        for (const type of types) applyVisibility(type);
      }
    },
    get instances() {
      return instances;
    },
    get drawCalls() {
      let calls = 0;
      for (const type of types) {
        if (type.body.visible) calls++;
        if (type.glow?.visible) calls++;
        if (type.pool?.visible) calls++;
      }
      return calls;
    },
    dispose() {
      for (const type of types) {
        type.body.dispose();
        type.glow?.dispose();
      }
      root.clear();
      scene.remove(root);
      bodyMaterial.dispose();
      glowMaterial.dispose();
    },
  };
}

export { GROUP_LIMIT };
