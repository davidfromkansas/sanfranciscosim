// Tiny modelling kit for the bespoke landmarks. Primitives are baked with
// vertex colours and merged into three meshes per landmark (solid / glass /
// emissive), so a hand-built landmark costs ~3 draw calls, not 200.

import {
  BoxGeometry,
  BufferAttribute,
  CatmullRomCurve3,
  Color,
  ConeGeometry,
  CylinderGeometry,
  Group,
  LatheGeometry,
  Matrix4,
  Mesh,
  MeshBasicMaterial,
  MeshLambertMaterial,
  SphereGeometry,
  TorusGeometry,
  TubeGeometry,
  Vector2,
  Vector3,
} from 'three';
import { mergeGeometries } from 'three/addons/utils/BufferGeometryUtils.js';
import { createBuildingMaterial } from './materials.js';
import { shared } from './env.js';

const tmpColor = new Color();

function paint(geometry, color) {
  tmpColor.set(color);
  const count = geometry.attributes.position.count;
  const colors = new Float32Array(count * 3);
  for (let i = 0; i < count; i++) {
    // Slight per-vertex variation keeps large flat landmark faces from reading
    // as plastic.
    const v = 0.96 + ((i * 37) % 11) / 110;
    colors[i * 3] = tmpColor.r * v;
    colors[i * 3 + 1] = tmpColor.g * v;
    colors[i * 3 + 2] = tmpColor.b * v;
  }
  geometry.setAttribute('color', new BufferAttribute(colors, 3));
  geometry.deleteAttribute('uv');
  return geometry;
}

function transform(geometry, { x = 0, y = 0, z = 0, rotY = 0, rotX = 0, rotZ = 0 }) {
  const m = new Matrix4();
  if (rotX) geometry.applyMatrix4(new Matrix4().makeRotationX(rotX));
  if (rotZ) geometry.applyMatrix4(new Matrix4().makeRotationZ(rotZ));
  if (rotY) geometry.applyMatrix4(new Matrix4().makeRotationY(rotY));
  geometry.applyMatrix4(m.makeTranslation(x, y, z));
  return geometry;
}

export class Kit {
  constructor(seed = 128) {
    this.solid = [];
    this.glass = [];
    this.glow = [];
    this.seed = seed;
  }

  add(geometry, color, placement = {}) {
    this.solid.push(paint(transform(geometry, placement), color));
    return this;
  }

  // Glass volumes get the procedural window grid + dusk ignition.
  addGlass(geometry, color, placement = {}, baseY = 0) {
    const g = paint(transform(geometry, placement), color);
    const count = g.attributes.position.count;
    const meta = new Uint8Array(count * 2);
    const localY = new Uint16Array(count);
    const pos = g.attributes.position;
    const normal = g.attributes.normal;
    for (let i = 0; i < count; i++) {
      const upright = Math.abs(normal.getY(i)) < 0.5;
      meta[i * 2] = this.seed;
      meta[i * 2 + 1] = upright ? 1 : 0;
      localY[i] = Math.max(0, Math.min(65535, Math.round((pos.getY(i) - baseY) * 10)));
    }
    g.setAttribute('aMeta', new BufferAttribute(meta, 2));
    g.setAttribute('aLocalY', new BufferAttribute(localY, 1));
    this.glass.push(g);
    return this;
  }

  addGlow(geometry, color, placement = {}) {
    this.glow.push(paint(transform(geometry, placement), color));
    return this;
  }

  box(w, h, d, color, placement) {
    return this.add(new BoxGeometry(w, h, d), color, placement);
  }

  glassBox(w, h, d, color, placement, baseY) {
    return this.addGlass(new BoxGeometry(w, h, d), color, placement, baseY);
  }

  cylinder(rTop, rBottom, h, color, placement, segments = 12) {
    return this.add(new CylinderGeometry(rTop, rBottom, h, segments), color, placement);
  }

  glassCylinder(rTop, rBottom, h, color, placement, baseY, segments = 16) {
    return this.addGlass(new CylinderGeometry(rTop, rBottom, h, segments), color, placement, baseY);
  }

  cone(r, h, color, placement, segments = 10) {
    return this.add(new ConeGeometry(r, h, segments), color, placement);
  }

  sphere(r, color, placement, segments = 10) {
    return this.add(new SphereGeometry(r, segments, Math.max(4, segments / 2)), color, placement);
  }

  glowSphere(r, color, placement, segments = 6) {
    return this.addGlow(new SphereGeometry(r, segments, 4), color, placement);
  }

  torus(r, tube, color, placement, segments = 12, tubular = 20) {
    return this.add(new TorusGeometry(r, tube, segments, tubular), color, placement);
  }

  // Dome / rotunda profiles.
  dome(radius, height, color, placement, segments = 16) {
    const points = [];
    for (let i = 0; i <= 10; i++) {
      const a = (i / 10) * (Math.PI / 2);
      points.push(new Vector2(Math.cos(a) * radius, Math.sin(a) * height));
    }
    return this.add(new LatheGeometry(points, segments), color, placement);
  }

  tube(points, radius, color, radialSegments = 4, closed = false) {
    const curve = new CatmullRomCurve3(points.map((p) => new Vector3(p[0], p[1], p[2])), closed);
    const divisions = Math.max(8, Math.min(220, Math.round(curve.getLength() / 12)));
    return this.add(new TubeGeometry(curve, divisions, radius, radialSegments, closed), color, {});
  }

  strut(from, to, radius, color) {
    const dx = to[0] - from[0];
    const dy = to[1] - from[1];
    const dz = to[2] - from[2];
    const len = Math.hypot(dx, dy, dz);
    if (len < 0.01) return this;
    const geometry = new CylinderGeometry(radius, radius, len, 5);
    geometry.translate(0, len / 2, 0);
    const m = new Matrix4();
    const quaternion = new Vector3(dx / len, dy / len, dz / len);
    const up = new Vector3(0, 1, 0);
    const axis = new Vector3().crossVectors(up, quaternion);
    const angle = Math.acos(Math.min(1, Math.max(-1, up.dot(quaternion))));
    if (axis.lengthSq() > 1e-8) {
      axis.normalize();
      geometry.applyMatrix4(m.makeRotationAxis(axis, angle));
    } else if (quaternion.y < 0) {
      geometry.applyMatrix4(m.makeRotationX(Math.PI));
    }
    geometry.translate(from[0], from[1], from[2]);
    this.solid.push(paint(geometry, color));
    return this;
  }

  finish(name) {
    const group = new Group();
    group.name = name;
    if (this.solid.length) {
      const geometry = mergeGeometries(this.solid, false);
      for (const g of this.solid) g.dispose();
      const mesh = new Mesh(geometry, new MeshLambertMaterial({ vertexColors: true }));
      mesh.castShadow = true;
      mesh.receiveShadow = true;
      group.add(mesh);
    }
    if (this.glass.length) {
      const geometry = mergeGeometries(this.glass, false);
      for (const g of this.glass) g.dispose();
      const mesh = new Mesh(geometry, createBuildingMaterial({ windows: 1 }));
      mesh.castShadow = true;
      mesh.receiveShadow = true;
      group.add(mesh);
    }
    if (this.glow.length) {
      const geometry = mergeGeometries(this.glow, false);
      for (const g of this.glow) g.dispose();
      const material = new MeshBasicMaterial({ vertexColors: true, transparent: true, opacity: 1 });
      const mesh = new Mesh(geometry, material);
      mesh.userData.nightOnly = true;
      group.add(mesh);
      group.userData.glow = material;
    }
    return group;
  }
}

// Landmark glows (bridge necklaces, beacons, stadium lights) come up with dusk.
export function updateLandmarkGlow(group) {
  const material = group.userData.glow;
  if (material) material.opacity = Math.min(1, 0.12 + shared.uNight.value * 0.95);
}
