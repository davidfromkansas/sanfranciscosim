// The selection overlay: one reused wireframe box plus one reused ground ring.
// Nothing is allocated per click and nothing is ever added to the scene twice —
// selecting a different entity only moves and rescales these two objects.

import {
  AdditiveBlending,
  BoxGeometry,
  BufferAttribute,
  BufferGeometry,
  CylinderGeometry,
  EdgesGeometry,
  LineBasicMaterial,
  Line,
  LineSegments,
  Mesh,
  MeshBasicMaterial,
  RingGeometry,
} from 'three';

const HIGHLIGHT = 0xffcf5a;

// Column size per kind: slender enough not to swallow what it marks, tall
// enough to spot from the hero view. Radius is roughly the thing's own width,
// height is what makes it findable from the air.
// Kept NARROWER than the thing it marks. The column's base is its hottest part
// (near-white under additive blending), so a radius matching the object washes
// straight over the roof of what you just selected — at 150 m, a follow camera's
// distance, that is most of the vehicle.
const BEAMS = {
  person: { radius: 0.7, height: 90 },
  transit: { radius: 1.6, height: 150 },
  vessel: { radius: 2.8, height: 200 },
  'ferry-scheduled': { radius: 2.8, height: 200 },
  'transit-stop': { radius: 1.2, height: 110 },
  'ferry-terminal': { radius: 3, height: 200 },
  aircraft: { radius: 2.5, height: 260 },
  landmark: { radius: 8, height: 260 },
};
const DEFAULT_BEAM = { radius: 4, height: 140 };

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

  // Park outline: the real boundary, drawn as a closed line on the ground.
  // Rebuilt only when a different park is selected — one buffer, grown in place
  // if a bigger ring turns up.
  const outline = new Line(
    new BufferGeometry(),
    new LineBasicMaterial({ color: HIGHLIGHT, transparent: true, opacity: 0.95, depthTest: false })
  );
  outline.name = 'focus-outline';
  outline.renderOrder = 902;
  outline.visible = false;
  outline.frustumCulled = false;
  scene.add(outline);

  let pulse = 0;

  function clear() {
    box.visible = false;
    glow.visible = false;
    ring.visible = false;
    beam.visible = false;
    outline.visible = false;
  }

  // `height` comes from the entity's pick box, so the overlay matches whichever
  // tier is on screen (the toy tier clamps building heights).
  function show(entity, { toy = false, groundY = 0, groundSample = null } = {}) {
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
    // A park is a shape, not a point: trace it. The rings are lon/lat-projected
    // scene coordinates already, and the first ring is the outer boundary — the
    // rest are holes, which a selection outline has no business drawing.
    if (entity.kind === 'park' && entity.rings?.length) {
      const ring = entity.rings[0];
      if (ring && ring.length >= 6) {
        const points = new Float32Array((ring.length / 2 + 1) * 3);
        for (let i = 0; i < ring.length; i += 2) {
          const x = ring[i];
          const z = ring[i + 1];
          const j = (i / 2) * 3;
          points[j] = x;
          // Ride the terrain rather than cutting through a hill; the line draws
          // with depth testing off, so a metre of lift is enough to read.
          points[j + 1] = (groundSample ? groundSample(x, z) : groundY) + 1.5;
          points[j + 2] = z;
        }
        // Close the loop back to the first point.
        points[points.length - 3] = points[0];
        points[points.length - 2] = points[1];
        points[points.length - 1] = points[2];
        outline.geometry.dispose();
        outline.geometry = new BufferGeometry();
        outline.geometry.setAttribute('position', new BufferAttribute(points, 3));
        outline.visible = true;
        return;
      }
    }
    // An AREA keeps the ground ring — a neighbourhood or a park is a region, and
    // a column of light in the middle of one says nothing about its extent.
    if (entity.kind === 'neighborhood' || entity.kind === 'park') {
      ring.position.set(entity.x, groundY + 1.5, entity.z);
      ring.scale.setScalar(entity.kind === 'neighborhood' ? 420 : 160);
      ring.visible = true;
      return;
    }

    // Everything else is a THING at a point — a person, a bus, a boat, a plane,
    // a stop — and gets the same column of light a landmark gets. A ring drawn
    // round a moving object reads as a target reticle rather than as "this one",
    // and at 30 m radius it dwarfed the 3.5 m person standing in it.
    const beamFor = BEAMS[entity.kind] ?? DEFAULT_BEAM;
    const base = Math.max(0, groundSample ? groundSample(entity.x, entity.z) : groundY);
    // An aircraft is drawn hundreds of metres up, so its column has to REACH it
    // rather than stop short at a height that suits a bus.
    const height =
      entity.kind === 'aircraft'
        ? Math.max(beamFor.height, (entity.displayY ?? entity.y ?? 0) - base + 90)
        : beamFor.height;
    beam.position.set(entity.x, base + height / 2, entity.z);
    beam.scale.set(beamFor.radius, height, beamFor.radius);
    beam.visible = true;
  }

  function update(dt) {
    pulse = (pulse + dt) % 2;
    const wave = 0.5 + 0.5 * Math.sin(pulse * Math.PI);
    glow.material.opacity = 0.08 + wave * 0.08;
    ring.material.opacity = 0.6 + wave * 0.3;
    beam.material.opacity = 0.62 + wave * 0.34;
    outline.material.opacity = 0.7 + wave * 0.28;
  }

  return { show, clear, update };
}
