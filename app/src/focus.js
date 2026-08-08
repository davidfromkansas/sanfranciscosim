// The selection overlay: one reused wireframe box plus one reused ground ring.
// Nothing is allocated per click and nothing is ever added to the scene twice —
// selecting a different entity only moves and rescales these two objects.

import {
  AdditiveBlending,
  BoxGeometry,
  EdgesGeometry,
  LineBasicMaterial,
  LineSegments,
  Mesh,
  MeshBasicMaterial,
  RingGeometry,
} from 'three';

const HIGHLIGHT = 0xffcf5a;

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

  let pulse = 0;

  function clear() {
    box.visible = false;
    glow.visible = false;
    ring.visible = false;
  }

  // `height` comes from the entity's pick box, so the overlay matches whichever
  // tier is on screen (the toy tier clamps building heights).
  function show(entity, { toy = false, groundY = 0 } = {}) {
    clear();
    if (!entity) return;
    if (entity.kind === 'building') {
      const height = Math.max(4, toy ? entity.toyHeight : entity.height);
      const w = Math.max(3, entity.w * 2) + 1.2;
      const d = Math.max(3, entity.d * 2) + 1.2;
      for (const object of [box, glow]) {
        object.position.set(entity.x, entity.baseY + height / 2, entity.z);
        object.rotation.y = -entity.r;
        object.scale.set(w, height + 1.2, d);
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
  }

  return { show, clear, update };
}
