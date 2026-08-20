// The selection overlay: one reused wireframe box plus one reused ground ring.
// Nothing is allocated per click and nothing is ever added to the scene twice —
// selecting a different entity only moves and rescales these two objects.

import {
  AdditiveBlending,
  BoxGeometry,
  BufferAttribute,
  CylinderGeometry,
  EdgesGeometry,
  LineBasicMaterial,
  LineSegments,
  Mesh,
  MeshBasicMaterial,
  RingGeometry,
} from 'three';

const HIGHLIGHT = 0xffcf5a;

// The selection beam: a column of light standing on the thing you picked.
//
// Built as an open cylinder whose vertex colours fade to black upward. Under
// additive blending black IS transparent, so the beam dissolves into the sky
// without a shader or an alpha texture — the same trick the route walls use to
// keep a hard bottom edge and a soft top.
function makeBeam() {
  const geometry = new CylinderGeometry(1, 1, 1, 14, 24, true);
  const pos = geometry.attributes.position;
  const colors = new Float32Array(pos.count * 3);
  for (let i = 0; i < pos.count; i++) {
    // y runs -0.5..0.5 up the unit cylinder.
    const t = pos.getY(i) + 0.5;
    // Hot and white at the base, the highlight colour through the middle, gone
    // by the top. Squared falloff keeps the core tight rather than a smear.
    const fade = Math.pow(1 - t, 2.2);
    colors[i * 3] = 1.0 * fade + 0.25 * Math.pow(1 - t, 6);
    colors[i * 3 + 1] = 0.81 * fade + 0.25 * Math.pow(1 - t, 6);
    colors[i * 3 + 2] = 0.35 * fade + 0.25 * Math.pow(1 - t, 6);
  }
  geometry.setAttribute('color', new BufferAttribute(colors, 3));
  return geometry;
}

export function createFocusOverlay(scene) {
  const box = new LineSegments(
    new EdgesGeometry(new BoxGeometry(1, 1, 1)),
    new LineBasicMaterial({ color: HIGHLIGHT, transparent: true, opacity: 0.95, depthTest: false })
  );
  box.name = 'focus-box';
  box.renderOrder = 900;
  box.visible = false;
  box.frustumCulled = false;

  const glow = new Mesh(
    new BoxGeometry(1, 1, 1),
    new MeshBasicMaterial({
      color: HIGHLIGHT,
      transparent: true,
      opacity: 0.14,
      blending: AdditiveBlending,
      depthWrite: false,
    })
  );
  glow.name = 'focus-glow';
  glow.renderOrder = 899;
  glow.visible = false;
  glow.frustumCulled = false;

  const ring = new Mesh(
    new RingGeometry(0.86, 1, 40),
    new MeshBasicMaterial({ color: HIGHLIGHT, transparent: true, opacity: 0.85, depthTest: false })
  );
  ring.name = 'focus-ring';
  ring.rotation.x = -Math.PI / 2;
  ring.renderOrder = 900;
  ring.visible = false;
  ring.frustumCulled = false;

  scene.add(box, glow, ring);

  const beam = new Mesh(
    makeBeam(),
    new MeshBasicMaterial({
      vertexColors: true,
      transparent: true,
      opacity: 0.9,
      blending: AdditiveBlending,
      depthWrite: false,
      side: 2, // DoubleSide: the far wall of the column reads through the near one
      toneMapped: false,
    })
  );
  beam.name = 'focus-beam';
  beam.renderOrder = 901;
  beam.visible = false;
  beam.frustumCulled = false;
  scene.add(beam);

  let pulse = 0;

  function clear() {
    box.visible = false;
    glow.visible = false;
    ring.visible = false;
    beam.visible = false;
  }

  // `height` comes from the entity's pick box, so the overlay matches whichever
  // tier is on screen (the toy tier clamps building heights).
  function show(entity, { toy = false, groundY = 0 } = {}) {
    clear();
    if (!entity) return;
    // Anything that knows its own extents draws a wire box on them. Landmarks
    // used to get a fixed 90 m ground ring regardless of size, which put a
    // 180 m circle around an 18 m tower.
    if (entity.bounds) {
      const b = entity.bounds;
      const baseY = b.y - b.h / 2;
      // Stands ON the landmark and climbs well clear of it, so the column reads
      // from the hero view as well as from the street.
      const height = Math.max(220, b.h * 3);
      // Keyed to the footprint so a slab does not get a needle and a tower does
      // not get a chimney, but clamped: this is a marker, not a scale model.
      const radius = Math.max(2.5, Math.min(14, Math.min(b.w, b.d) * 0.1));
      beam.position.set(b.x, baseY + height / 2, b.z);
      beam.scale.set(radius, height, radius);
      beam.visible = true;
      return;
    }
    if (entity.kind === 'building') {
      const height = Math.max(4, toy ? entity.toyHeight : entity.height);
      // No padding: the wire sits ON the border. It draws with depthTest off,
      // so a coincident edge still reads clearly.
      const w = Math.max(3, entity.w * 2);
      const d = Math.max(3, entity.d * 2);
      for (const object of [box, glow]) {
        object.position.set(entity.x, entity.baseY + height / 2, entity.z);
        object.rotation.y = -entity.r;
        object.scale.set(w, height, d);
        object.visible = true;
      }
      return;
    }
    const radius =
      entity.kind === 'landmark' ? 90 : entity.kind === 'neighborhood' ? 420 : entity.kind === 'park' ? 160 : 30;
    ring.position.set(entity.x, groundY + 1.5, entity.z);
    ring.scale.setScalar(radius);
    ring.visible = true;
  }

  function update(dt) {
    pulse = (pulse + dt) % 2;
    const wave = 0.5 + 0.5 * Math.sin(pulse * Math.PI);
    glow.material.opacity = 0.08 + wave * 0.08;
    ring.material.opacity = 0.6 + wave * 0.3;
    beam.material.opacity = 0.62 + wave * 0.34;
  }

  return { show, clear, update };
}
