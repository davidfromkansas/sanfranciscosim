// Ring math: simplification, area, centroid, bbox.

export function ringArea(ring) {
  let a = 0;
  for (let i = 0, j = ring.length - 2; i < ring.length; j = i, i += 2) {
    a += (ring[j] + ring[i]) * (ring[j + 1] - ring[i + 1]);
  }
  return a / 2; // signed; positive = clockwise in (x, z) screen-ish space
}

export function ringCentroid(ring) {
  let cx = 0;
  let cz = 0;
  let a = 0;
  for (let i = 0, j = ring.length - 2; i < ring.length; j = i, i += 2) {
    const f = ring[j] * ring[i + 1] - ring[i] * ring[j + 1];
    a += f;
    cx += (ring[j] + ring[i]) * f;
    cz += (ring[j + 1] + ring[i + 1]) * f;
  }
  if (Math.abs(a) < 1e-9) {
    let sx = 0;
    let sz = 0;
    for (let i = 0; i < ring.length; i += 2) {
      sx += ring[i];
      sz += ring[i + 1];
    }
    return [sx / (ring.length / 2), sz / (ring.length / 2)];
  }
  a *= 3;
  return [cx / a, cz / a];
}

export function ringBBox(ring) {
  let minX = Infinity;
  let maxX = -Infinity;
  let minZ = Infinity;
  let maxZ = -Infinity;
  for (let i = 0; i < ring.length; i += 2) {
    if (ring[i] < minX) minX = ring[i];
    if (ring[i] > maxX) maxX = ring[i];
    if (ring[i + 1] < minZ) minZ = ring[i + 1];
    if (ring[i + 1] > maxZ) maxZ = ring[i + 1];
  }
  return [minX, minZ, maxX, maxZ];
}

function sqSegDist(px, pz, ax, az, bx, bz) {
  let x = ax;
  let z = az;
  let dx = bx - ax;
  let dz = bz - az;
  if (dx !== 0 || dz !== 0) {
    const t = ((px - ax) * dx + (pz - az) * dz) / (dx * dx + dz * dz);
    if (t > 1) {
      x = bx;
      z = bz;
    } else if (t > 0) {
      x += dx * t;
      z += dz * t;
    }
  }
  dx = px - x;
  dz = pz - z;
  return dx * dx + dz * dz;
}

// Douglas-Peucker on a flat [x, z, x, z, ...] array.
export function simplify(points, tolerance) {
  const n = points.length / 2;
  if (n < 4) return points;
  const sqTol = tolerance * tolerance;
  const keep = new Uint8Array(n);
  keep[0] = 1;
  keep[n - 1] = 1;
  const stack = [[0, n - 1]];
  while (stack.length) {
    const [first, last] = stack.pop();
    let maxDist = 0;
    let index = -1;
    for (let i = first + 1; i < last; i++) {
      const d = sqSegDist(
        points[i * 2],
        points[i * 2 + 1],
        points[first * 2],
        points[first * 2 + 1],
        points[last * 2],
        points[last * 2 + 1]
      );
      if (d > maxDist) {
        maxDist = d;
        index = i;
      }
    }
    if (maxDist > sqTol && index > 0) {
      keep[index] = 1;
      stack.push([first, index], [index, last]);
    }
  }
  const out = [];
  for (let i = 0; i < n; i++) {
    if (keep[i]) out.push(points[i * 2], points[i * 2 + 1]);
  }
  return out;
}

// Simplify a closed ring (first point repeated is dropped from the output).
export function simplifyRing(ring, tolerance) {
  let r = ring;
  const n = r.length / 2;
  if (n > 2 && r[0] === r[r.length - 2] && r[1] === r[r.length - 1]) {
    r = r.slice(0, r.length - 2);
  }
  if (r.length / 2 < 5) return r;
  const closed = r.concat([r[0], r[1]]);
  const s = simplify(closed, tolerance);
  const out = s.slice(0, s.length - 2);
  return out.length / 2 >= 3 ? out : r;
}

export function polylineLength(pts) {
  let len = 0;
  for (let i = 2; i < pts.length; i += 2) {
    len += Math.hypot(pts[i] - pts[i - 2], pts[i + 1] - pts[i - 1]);
  }
  return len;
}

// Resample a polyline so consecutive points are at most `step` apart.
export function densify(pts, step) {
  const out = [pts[0], pts[1]];
  for (let i = 2; i < pts.length; i += 2) {
    const ax = pts[i - 2];
    const az = pts[i - 1];
    const bx = pts[i];
    const bz = pts[i + 1];
    const d = Math.hypot(bx - ax, bz - az);
    const steps = Math.max(1, Math.ceil(d / step));
    for (let s = 1; s <= steps; s++) {
      out.push(ax + ((bx - ax) * s) / steps, az + ((bz - az) * s) / steps);
    }
  }
  return out;
}
