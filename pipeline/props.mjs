// Bake-time view of the runtime prop vocabulary.
//
// The recipes themselves live in app/src/props.js, because that is where they
// run: the tile worker grows them straight into its merged buffers so a lit
// marquee costs no draw call and no texture. But the plan's budget (average
// <=150 added triangles per building, hard cap 500, vehicles rationed) has to be
// proven before anything ships, so the bake imports the very same module and
// runs it with an emitter that counts triangles instead of writing vertices.
//
// One source of truth, two consumers: if a recipe grows, the audit notices.

import { emitProps, makeCtx } from '../app/src/props.js';

// A face of n points is a fan of n - 2 triangles, which is exactly how the
// worker's `face()` indexes it.
export function countProps(building) {
  let triangles = 0;
  const ctx = makeCtx(
    { cx: 0, cz: 0, ux: 1, uz: 0, vx: 0, vz: 1 },
    (points) => {
      triangles += Math.max(0, points.length - 2);
    }
  );
  emitProps(ctx, {
    ...building,
    wall: [200, 200, 200],
    roof: [180, 180, 180],
  });
  return triangles;
}

export { CAT, PROP } from '../app/src/props.js';
