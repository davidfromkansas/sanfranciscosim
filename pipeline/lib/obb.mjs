// Oriented bounding box helpers shared by the toy bake (garnish placement) and
// the context bake (the client's pick boxes). Dominant-edge method: the longest
// edge of the footprint sets the frame, which is what reads as "square on" for
// city blocks and is far cheaper than rotating calipers.

export function obbFrame(ring) {
  const n = ring.length / 2;
  let best = 0;
  let ang = 0;
  for (let i = 0; i < n; i++) {
    const ax = ring[i * 2];
    const az = ring[i * 2 + 1];
    const bx = ring[((i + 1) % n) * 2];
    const bz = ring[((i + 1) % n) * 2 + 1];
    const len = Math.hypot(bx - ax, bz - az);
    if (len > best) {
      best = len;
      ang = Math.atan2(bz - az, bx - ax);
    }
  }
  const cos = Math.cos(-ang);
  const sin = Math.sin(-ang);
  let minU = Infinity;
  let maxU = -Infinity;
  let minV = Infinity;
  let maxV = -Infinity;
  for (let i = 0; i < n; i++) {
    const x = ring[i * 2];
    const z = ring[i * 2 + 1];
    const u = x * cos - z * sin;
    const v = x * sin + z * cos;
    if (u < minU) minU = u;
    if (u > maxU) maxU = u;
    if (v < minV) minV = v;
    if (v > maxV) maxV = v;
  }
  return { ang, minU, maxU, minV, maxV };
}

// Rotate a point from the OBB's local (u, v) frame back into world (x, z).
export function fromFrame(frame, u, v) {
  const cos = Math.cos(frame.ang);
  const sin = Math.sin(frame.ang);
  return [u * cos - v * sin, u * sin + v * cos];
}

export function frameRect(frame, u0, u1, v0, v1) {
  const ring = [];
  for (const [u, v] of [
    [u0, v0],
    [u1, v0],
    [u1, v1],
    [u0, v1],
  ]) {
    const [x, z] = fromFrame(frame, u, v);
    ring.push(x, z);
  }
  return ring;
}

export function obbRing(ring) {
  const f = obbFrame(ring);
  return frameRect(f, f.minU, f.maxU, f.minV, f.maxV);
}

// Centre, half extents and yaw of the footprint's oriented box.
export function obbBox(ring) {
  const f = obbFrame(ring);
  const [cx, cz] = fromFrame(f, (f.minU + f.maxU) / 2, (f.minV + f.maxV) / 2);
  return {
    x: cx,
    z: cz,
    w: (f.maxU - f.minU) / 2,
    d: (f.maxV - f.minV) / 2,
    r: f.ang,
  };
}
