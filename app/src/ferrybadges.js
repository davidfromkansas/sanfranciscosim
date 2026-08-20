// Route badges over the live ferries: a cream pill naming the service each
// hull is working, so a boat crossing the Bay reads as "Vallejo" rather than as
// an anonymous white shape.
//
// Same idiom as the Muni route badges (muni.js): one canvas atlas, one
// instanced quad layer, each instance selecting its route's cell through an
// instanced uv-rect attribute patched into the material. Two differences, both
// because ferries are not buses:
//
// 1. The label is a NAME, not a number. "South San Francisco" needs a wide
//    cell and auto-fitted type where "38R" needed neither, so the atlas cells
//    are 2:1 and the font size is measured down to fit.
// 2. The pill carries the route's livery colour as a bar under the type, which
//    is what ties a badge to the wall its boat is running along. With only
//    seven services the colour is a faster read than the words.
//
// Declutter is not needed here the way it was for 2,976 bus stops: WETA runs
// about fifteen boats and they are kilometres apart on open water.
//
// Draw calls: one.

import {
  CanvasTexture,
  DynamicDrawUsage,
  InstancedBufferAttribute,
  InstancedMesh,
  MeshBasicMaterial,
  Object3D,
  PlaneGeometry,
  SRGBColorSpace,
} from 'three';

import { loadFerryNetwork } from './ferrynetwork.js';

const CAPACITY = 24; // matches the ferry fleet cap in ferries.js
const COLS = 4;
const ROWS = 4;
const CELL_W = 256;
const CELL_H = 128;

// Metres. 2:1, matching the atlas cell, so type is never stretched.
const BADGE_W = 15;
const BADGE_H = 7.5;
// Height of the badge tip above the waterline: clear of the deckhouse and the
// funnel at any drawn size.
const BADGE_TIP_Y = 11;
const TAIL_DROP = 0.34 * BADGE_H;

const REF_DIST = 420;
const SCALE_MIN = 0.85;
const SCALE_MAX = 26;

// Where a vessel's route badge floats, given how far the camera is from it.
// Exported because the PICK has to hit the badge a viewer can see, and the two
// must not be separate copies of these numbers — a badge drawn at one height and
// picked at another is a tag that ignores the click that plainly landed on it.
export function badgeHeightAt(camDist) {
  const scale = Math.max(SCALE_MIN, Math.min(SCALE_MAX, camDist / REF_DIST));
  return BADGE_TIP_Y + TAIL_DROP * scale;
}

// Rule 2. Never zero: a badge layer that vanishes on low is indistinguishable
// from one that broke. Low simply labels fewer boats — the nearest ones.
const QUALITY_CAP = { high: CAPACITY, medium: CAPACITY, low: 6 };

const dummy = new Object3D();

class BadgeAtlas {
  constructor() {
    this.canvas = document.createElement('canvas');
    this.canvas.width = COLS * CELL_W;
    this.canvas.height = ROWS * CELL_H;
    this.ctx = this.canvas.getContext('2d');
    this.texture = new CanvasTexture(this.canvas);
    this.texture.colorSpace = SRGBColorSpace;
    this.slots = new Map(); // "name|color" -> [u, v, w, h]
  }

  rect(label, color) {
    const key = `${label}|${color}`;
    let slot = this.slots.get(key);
    if (slot) return slot;
    const index = this.slots.size;
    if (index >= COLS * ROWS) return null;
    const x = (index % COLS) * CELL_W;
    const y = Math.floor(index / COLS) * CELL_H;

    const ctx = this.ctx;
    ctx.clearRect(x, y, CELL_W, CELL_H);
    ctx.save();
    ctx.translate(x, y);

    // Bubble and tail as ONE path, so the outline runs around the joint rather
    // than drawing a seam across the underside.
    const bx = 8;
    const by = 6;
    const bw = CELL_W - 16;
    const bh = 84;
    const r = 18;
    const tailL = CELL_W / 2 - 16;
    const tailR = CELL_W / 2 + 16;
    ctx.beginPath();
    ctx.moveTo(bx + r, by);
    ctx.lineTo(bx + bw - r, by);
    ctx.quadraticCurveTo(bx + bw, by, bx + bw, by + r);
    ctx.lineTo(bx + bw, by + bh - r);
    ctx.quadraticCurveTo(bx + bw, by + bh, bx + bw - r, by + bh);
    ctx.lineTo(tailR, by + bh);
    ctx.lineTo(CELL_W / 2 - 4, by + bh + 30); // the point, aimed at the hull
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

    // Livery bar: the tie back to this route's wall out on the water.
    ctx.save();
    ctx.clip();
    ctx.fillStyle = color;
    ctx.fillRect(bx, by + bh - 16, bw, 16);
    ctx.restore();

    // Measured down to fit rather than guessed from length: "Oakland &
    // Alameda" and "Vallejo" are the same badge with very different widths.
    ctx.fillStyle = '#3a3530';
    let size = 46;
    const maxWidth = bw - 26;
    do {
      ctx.font = `800 ${size}px ui-rounded, "SF Pro Rounded", -apple-system, system-ui, sans-serif`;
      if (ctx.measureText(label).width <= maxWidth) break;
      size -= 2;
    } while (size > 18);
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    ctx.fillText(label, bx + bw / 2, by + (bh - 16) / 2 + 2);
    ctx.restore();

    slot = [
      x / this.canvas.width,
      1 - (y + CELL_H) / this.canvas.height,
      CELL_W / this.canvas.width,
      CELL_H / this.canvas.height,
    ];
    this.slots.set(key, slot);
    this.texture.needsUpdate = true;
    return slot;
  }
}

export function createFerryBadges(scene, ferries) {
  const atlas = new BadgeAtlas();
  let mesh = null;
  let uvRect = null;
  let cap = QUALITY_CAP.high;
  // routeName -> livery colour, from the same bake the walls use.
  let colors = new Map();

  loadFerryNetwork().then((n) => {
    if (n) for (const route of n.routes.values()) colors.set(route.name, route.color);
  });

  const geometry = new PlaneGeometry(BADGE_W, BADGE_H);
  uvRect = new InstancedBufferAttribute(new Float32Array(CAPACITY * 4), 4);
  uvRect.setUsage(DynamicDrawUsage);
  geometry.setAttribute('uvRect', uvRect);
  const material = new MeshBasicMaterial({
    map: atlas.texture,
    transparent: true,
    depthWrite: false,
    alphaTest: 0.02,
    // A badge behind a hull is a label you cannot read; it is UI, not city.
    depthTest: false,
  });
  material.onBeforeCompile = (shader) => {
    shader.vertexShader = shader.vertexShader
      .replace('#include <common>', '#include <common>\nattribute vec4 uvRect;')
      .replace('#include <uv_vertex>', '#include <uv_vertex>\n  vMapUv = uvRect.xy + vMapUv * uvRect.zw;');
  };
  mesh = new InstancedMesh(geometry, material, CAPACITY);
  mesh.name = 'live-ferry-badges';
  mesh.instanceMatrix.setUsage(DynamicDrawUsage);
  mesh.frustumCulled = false;
  mesh.renderOrder = 5;
  mesh.count = 0;
  scene.add(mesh);

  function setQuality(tier) {
    cap = QUALITY_CAP[tier] ?? QUALITY_CAP.high;
  }

  function update(dt, camera) {
    if (!mesh) return;
    const vessels = (ferries?.liveEntities?.() || []).filter((v) => v.drawn && v.routeName);
    // Nearest the camera first, so the low tier drops the far side of the Bay.
    vessels.sort(
      (a, b) =>
        (a.x - camera.position.x) ** 2 + (a.z - camera.position.z) ** 2 -
        ((b.x - camera.position.x) ** 2 + (b.z - camera.position.z) ** 2)
    );

    let count = 0;
    for (const vessel of vessels) {
      if (count >= cap) break;
      const slot = atlas.rect(vessel.routeName, colors.get(vessel.routeName) || '#7f8c94');
      if (!slot) continue;
      const camDist = Math.hypot(
        vessel.x - camera.position.x,
        vessel.z - camera.position.z,
        camera.position.y
      );
      const scale = Math.max(SCALE_MIN, Math.min(SCALE_MAX, camDist / REF_DIST));
      // The tip stays a fixed height over the water while the card above it
      // grows, so a badge never drifts off its own hull as you zoom out.
      dummy.position.set(vessel.x, badgeHeightAt(camDist), vessel.z);
      dummy.quaternion.copy(camera.quaternion);
      dummy.scale.setScalar(scale);
      dummy.updateMatrix();
      mesh.setMatrixAt(count, dummy.matrix);
      uvRect.setXYZW(count, slot[0], slot[1], slot[2], slot[3]);
      count++;
    }
    mesh.count = count;
    mesh.instanceMatrix.needsUpdate = true;
    uvRect.needsUpdate = true;
  }

  return {
    update,
    setQuality,
    get count() {
      return mesh ? mesh.count : 0;
    },
  };
}
