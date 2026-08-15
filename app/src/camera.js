// Custom city-builder camera rig — deliberately not OrbitControls.
//
// The rig is a pivot on the ground plus yaw / pitch / distance. Movement is
// always relative to the pivot, the pivot follows the terrain, pitch is coupled
// to zoom (top-down when high, near-horizon when low), and zoom pulls toward the
// point under the cursor so you can dive into a specific intersection.

import { Raycaster, Vector2, Vector3 } from 'three';

const DEG = Math.PI / 180;

export function createCameraRig(camera, domElement, sampleElevation, extent) {
  const state = {
    pivot: new Vector3(0, 0, 0),
    yaw: 200 * DEG,
    pitch: 62 * DEG,
    distance: 9000,
    minDistance: 28,
    maxDistance: 16000,
    boost: 1,
    edgeScroll: true,
    // Set while the rig is aimed at a focused entity's mid-height instead of the
    // ground under the pivot; any manual movement releases it.
    holdY: false,
    velocity: new Vector3(),
    yawVelocity: 0,
  };

  const keys = new Set();
  const pointer = new Vector2(0, 0); // normalised device coords
  const pointerPx = new Vector2(-1000, -1000);
  const raycaster = new Raycaster();
  let dragMode = null; // 'rotate' | 'pan'
  // Touch: active touch pointers by id; two of them make a pinch/twist gesture.
  const touches = new Map();
  let gesture = null; // { span, angle, midX, midY, twist }
  let lastX = 0;
  let lastY = 0;
  const panPlanePoint = new Vector3();
  let animation = null;
  let pitchLocked = false;

  // Diorama mode: the money shot is locked. Pitch never moves, the yaw only
  // visits eight 45-degree headings, and zoom rides in and out along that fixed
  // angle. Pan, wheel zoom, edge scroll and WASD all keep working.
  // `max` is the zoom-out ceiling. It has to clear the cloud deck: the whole
  // point of the deck's altitude is that you START below it and can climb
  // ABOVE it, so 16000 m of orbit (x sin 42 = ~10.7 km of height) sits well
  // over DECK_ALTITUDE in clouds.js. Raise one and check the other.
  const DIORAMA = { pitch: 42 * DEG, step: 45 * DEG, min: 150, max: 16000, dragPx: 60 };
  let diorama = false;
  let dioramaSaved = null;
  let yawStep = null;
  let dragYaw = 0;

  function stepYaw(direction) {
    const from = state.yaw;
    const target = yawStep ? yawStep.to : Math.round(from / DIORAMA.step) * DIORAMA.step;
    yawStep = { from, to: target + direction * DIORAMA.step, start: performance.now(), duration: 0.5 };
  }

  function setDiorama(on) {
    if (on === diorama) return;
    if (on) {
      dioramaSaved = {
        yaw: state.yaw,
        pitch: state.pitch,
        distance: state.distance,
        minDistance: state.minDistance,
        maxDistance: state.maxDistance,
        pitchLocked,
      };
      diorama = true;
      yawStep = null;
      dragYaw = 0;
      state.yaw = Math.round(state.yaw / DIORAMA.step) * DIORAMA.step;
      state.pitch = DIORAMA.pitch;
      state.minDistance = DIORAMA.min;
      state.maxDistance = DIORAMA.max;
      state.distance = Math.min(DIORAMA.max, Math.max(DIORAMA.min, state.distance));
      pitchLocked = true;
    } else {
      diorama = false;
      yawStep = null;
      state.yaw = dioramaSaved.yaw;
      state.pitch = dioramaSaved.pitch;
      state.distance = dioramaSaved.distance;
      state.minDistance = dioramaSaved.minDistance;
      state.maxDistance = dioramaSaved.maxDistance;
      pitchLocked = dioramaSaved.pitchLocked;
    }
    apply();
  }

  // Pitch is a function of zoom: sky-high views look almost straight down,
  // street-level views sit just above the horizon.
  function pitchForDistance(d) {
    const t = Math.min(
      1,
      Math.max(
        0,
        (Math.log(d) - Math.log(state.minDistance)) /
          (Math.log(state.maxDistance) - Math.log(state.minDistance))
      )
    );
    return (12 + t * 62) * DEG;
  }

  function clampPivot() {
    const margin = 3000;
    state.pivot.x = Math.min(extent.maxX + margin, Math.max(extent.minX - margin, state.pivot.x));
    state.pivot.z = Math.min(extent.maxZ + margin, Math.max(extent.minZ - margin, state.pivot.z));
  }

  function groundHeight(x, z) {
    return Math.max(0, sampleElevation(x, z));
  }

  function apply() {
    const cosPitch = Math.cos(state.pitch);
    const sinPitch = Math.sin(state.pitch);
    const offset = new Vector3(
      Math.sin(state.yaw) * cosPitch,
      sinPitch,
      Math.cos(state.yaw) * cosPitch
    ).multiplyScalar(state.distance);
    camera.position.copy(state.pivot).add(offset);
    // Never let the camera sink into a hill.
    const floor = groundHeight(camera.position.x, camera.position.z) + 12;
    if (camera.position.y < floor) camera.position.y = floor;
    camera.lookAt(state.pivot);
  }

  const rayPoint = new Vector2();

  function screenToGround(nx, ny, out) {
    rayPoint.set(nx, ny);
    raycaster.setFromCamera(rayPoint, camera);
    const dir = raycaster.ray.direction;
    const origin = raycaster.ray.origin;
    // March the ray against the heightfield, then bisect the crossing.
    let t = 0;
    let prev = origin.y - groundHeight(origin.x, origin.z);
    const maxT = state.distance * 6 + 4000;
    for (let i = 1; i <= 48; i++) {
      const tt = (i / 48) * maxT;
      const x = origin.x + dir.x * tt;
      const y = origin.y + dir.y * tt;
      const z = origin.z + dir.z * tt;
      const d = y - groundHeight(x, z);
      if (d <= 0 && prev > 0) {
        let lo = t;
        let hi = tt;
        for (let k = 0; k < 12; k++) {
          const mid = (lo + hi) / 2;
          const mx = origin.x + dir.x * mid;
          const my = origin.y + dir.y * mid;
          const mz = origin.z + dir.z * mid;
          if (my - groundHeight(mx, mz) > 0) lo = mid;
          else hi = mid;
        }
        const ft = (lo + hi) / 2;
        out.set(origin.x + dir.x * ft, origin.y + dir.y * ft, origin.z + dir.z * ft);
        return true;
      }
      prev = d;
      t = tt;
    }
    // Fall back to the y=0 plane (over water).
    if (dir.y < -1e-5) {
      const ft = -origin.y / dir.y;
      out.set(origin.x + dir.x * ft, 0, origin.z + dir.z * ft);
      return true;
    }
    return false;
  }

  function onKeyDown(event) {
    if (event.metaKey || event.ctrlKey) return;
    keys.add(event.code);
    if (event.code === 'ShiftLeft' || event.code === 'ShiftRight') state.boost = 3.4;
    // Diorama yaw is discrete: one heading per keypress, not a continuous spin.
    if (diorama && !event.repeat) {
      if (event.code === 'KeyQ') stepYaw(1);
      if (event.code === 'KeyE') stepYaw(-1);
    }
  }

  function onKeyUp(event) {
    keys.delete(event.code);
    if (event.code === 'ShiftLeft' || event.code === 'ShiftRight') state.boost = 1;
  }

  // The first two touches (Map preserves insertion order) define the gesture;
  // extra fingers are tracked but ignored.
  function gesturePoints() {
    const [a, b] = [...touches.values()];
    return {
      span: Math.hypot(b.x - a.x, b.y - a.y),
      angle: Math.atan2(b.y - a.y, b.x - a.x),
      midX: (a.x + b.x) / 2,
      midY: (a.y + b.y) / 2,
    };
  }

  function anchorPan(clientX, clientY) {
    const rect = domElement.getBoundingClientRect();
    lastX = clientX;
    lastY = clientY;
    pointer.x = ((clientX - rect.left) / rect.width) * 2 - 1;
    pointer.y = -((clientY - rect.top) / rect.height) * 2 + 1;
    dragMode = 'pan';
    screenToGround(pointer.x, pointer.y, panPlanePoint);
  }

  function onPointerDown(event) {
    domElement.setPointerCapture(event.pointerId);
    animation = null;
    if (event.pointerType === 'touch') {
      touches.set(event.pointerId, { x: event.clientX, y: event.clientY });
      if (touches.size === 2) {
        dragMode = null;
        gesture = { ...gesturePoints(), twist: 0 };
        return;
      }
      if (touches.size > 2) return;
    }
    lastX = event.clientX;
    lastY = event.clientY;
    // Anchor from THIS event's position: a touch has no hover, so the shared
    // pointer NDC can be stale from a previous contact and the first pan would
    // grab the wrong ground point.
    const rect = domElement.getBoundingClientRect();
    pointer.x = ((event.clientX - rect.left) / rect.width) * 2 - 1;
    pointer.y = -((event.clientY - rect.top) / rect.height) * 2 + 1;
    if (event.button === 2 || event.button === 1) {
      dragMode = 'rotate';
      domElement.style.cursor = 'grabbing';
    } else if (event.button === 0) {
      dragMode = 'pan';
      screenToGround(pointer.x, pointer.y, panPlanePoint);
      domElement.style.cursor = 'grabbing';
    }
  }

  function onPointerUp(event) {
    if (domElement.hasPointerCapture(event.pointerId)) {
      domElement.releasePointerCapture(event.pointerId);
    }
    if (event.pointerType === 'touch') {
      touches.delete(event.pointerId);
      if (gesture) {
        if (touches.size >= 2) {
          // A spare finger lifted: re-baseline so span/angle don't jump.
          gesture = { ...gesturePoints(), twist: gesture.twist };
          return;
        }
        gesture = null;
        if (touches.size === 1) {
          // Hand the remaining finger a fresh pan anchor instead of ending the drag.
          const [rest] = [...touches.values()];
          anchorPan(rest.x, rest.y);
          return;
        }
      }
    }
    dragMode = null;
    domElement.style.cursor = 'default';
  }

  const dragTarget = new Vector3();

  // Two fingers: pinch zooms toward the midpoint's ground point (same pull as
  // wheel zoom), twist turns — stepped headings in diorama, free yaw otherwise —
  // and outside diorama the midpoint's vertical travel tilts. Pitch stays locked
  // in diorama, exactly like every other input path.
  function onGestureMove() {
    const g = gesturePoints();
    const rect = domElement.getBoundingClientRect();

    if (gesture.span > 0 && g.span > 0 && g.span !== gesture.span) {
      state.holdY = false;
      pointer.x = ((g.midX - rect.left) / rect.width) * 2 - 1;
      pointer.y = -((g.midY - rect.top) / rect.height) * 2 + 1;
      const scale = gesture.span / g.span; // fingers apart -> scale < 1 -> zoom in
      const hasTarget = screenToGround(pointer.x, pointer.y, zoomTarget);
      const next = Math.min(state.maxDistance, Math.max(state.minDistance, state.distance * scale));
      if (hasTarget && scale < 1) {
        const k = 1 - next / state.distance;
        state.pivot.x += (zoomTarget.x - state.pivot.x) * k * 0.9;
        state.pivot.z += (zoomTarget.z - state.pivot.z) * k * 0.9;
        clampPivot();
      }
      state.distance = next;
      if (!pitchLocked) state.pitch = pitchForDistance(state.distance);
    }

    let dAngle = g.angle - gesture.angle;
    while (dAngle > Math.PI) dAngle -= Math.PI * 2;
    while (dAngle < -Math.PI) dAngle += Math.PI * 2;
    if (diorama) {
      // Discrete like every other diorama yaw input: one heading per 30 degrees
      // of twist.
      const TWIST_STEP = 30 * DEG;
      gesture.twist += dAngle;
      while (Math.abs(gesture.twist) >= TWIST_STEP) {
        stepYaw(gesture.twist > 0 ? 1 : -1);
        gesture.twist -= Math.sign(gesture.twist) * TWIST_STEP;
      }
    } else {
      state.yaw += dAngle;
      state.pitch = Math.min(
        86 * DEG,
        Math.max(6 * DEG, state.pitch + (g.midY - gesture.midY) * 0.004)
      );
      pitchLocked = true;
    }

    gesture.span = g.span;
    gesture.angle = g.angle;
    gesture.midX = g.midX;
    gesture.midY = g.midY;
    apply();
  }

  function onPointerMove(event) {
    if (event.pointerType === 'touch' && touches.has(event.pointerId)) {
      touches.set(event.pointerId, { x: event.clientX, y: event.clientY });
      if (gesture && touches.size >= 2) {
        onGestureMove();
        return;
      }
    }
    const rect = domElement.getBoundingClientRect();
    pointerPx.set(event.clientX - rect.left, event.clientY - rect.top);
    pointer.x = (pointerPx.x / rect.width) * 2 - 1;
    pointer.y = -(pointerPx.y / rect.height) * 2 + 1;

    if (!dragMode) return;
    const dx = event.clientX - lastX;
    const dy = event.clientY - lastY;
    lastX = event.clientX;
    lastY = event.clientY;

    if (dragMode === 'rotate') {
      if (diorama) {
        // Right-drag advances one heading per 60 px of travel.
        dragYaw += dx;
        while (Math.abs(dragYaw) >= DIORAMA.dragPx) {
          stepYaw(dragYaw > 0 ? -1 : 1);
          dragYaw -= Math.sign(dragYaw) * DIORAMA.dragPx;
        }
        return;
      }
      state.yaw -= dx * 0.005;
      state.pitch = Math.min(86 * DEG, Math.max(6 * DEG, state.pitch + dy * 0.004));
      pitchLocked = true;
    } else if (dragMode === 'pan') {
      state.holdY = false;
      // Grab-pan: keep the ground point that was under the cursor under it. The
      // camera has to be moved with the pivot immediately, otherwise the next
      // move event raycasts through a stale camera and the grabbed point walks
      // away across a drag.
      if (screenToGround(pointer.x, pointer.y, dragTarget)) {
        state.pivot.x -= dragTarget.x - panPlanePoint.x;
        state.pivot.z -= dragTarget.z - panPlanePoint.z;
        clampPivot();
        apply();
      }
    }
  }

  const zoomTarget = new Vector3();

  function onWheel(event) {
    event.preventDefault();
    animation = null;
    state.holdY = false;
    // Wheel events carry their own cursor position: zooming must aim there even
    // if no pointermove arrived first.
    const rect = domElement.getBoundingClientRect();
    pointer.x = ((event.clientX - rect.left) / rect.width) * 2 - 1;
    pointer.y = -((event.clientY - rect.top) / rect.height) * 2 + 1;
    const scale = Math.exp(
      (event.deltaY > 0 ? 1 : -1) * Math.min(0.35, Math.abs(event.deltaY) * 0.0022)
    );
    const hasTarget = screenToGround(pointer.x, pointer.y, zoomTarget);
    const next = Math.min(state.maxDistance, Math.max(state.minDistance, state.distance * scale));
    // Zoom toward the cursor: pull the pivot proportionally toward the ground
    // point under the mouse as we descend.
    if (hasTarget && scale < 1) {
      const k = 1 - next / state.distance;
      state.pivot.x += (zoomTarget.x - state.pivot.x) * k * 0.9;
      state.pivot.z += (zoomTarget.z - state.pivot.z) * k * 0.9;
      clampPivot();
    }
    state.distance = next;
    if (!pitchLocked) state.pitch = pitchForDistance(state.distance);
    apply();
  }

  function onContextMenu(event) {
    event.preventDefault();
  }

  function onPointerLeave() {
    pointerPx.set(-1000, -1000);
  }

  domElement.addEventListener('pointerdown', onPointerDown);
  domElement.addEventListener('pointerup', onPointerUp);
  domElement.addEventListener('pointercancel', onPointerUp);
  domElement.addEventListener('pointermove', onPointerMove);
  domElement.addEventListener('pointerleave', onPointerLeave);
  domElement.addEventListener('wheel', onWheel, { passive: false });
  domElement.addEventListener('contextmenu', onContextMenu);
  window.addEventListener('keydown', onKeyDown);
  window.addEventListener('keyup', onKeyUp);
  window.addEventListener('blur', () => keys.clear());

  const forward = new Vector3();
  const right = new Vector3();
  const moveTarget = new Vector3();

  function normaliseYaw(from, to) {
    let t = to;
    while (t - from > Math.PI) t -= Math.PI * 2;
    while (from - t > Math.PI) t += Math.PI * 2;
    return t;
  }

  function update(dt) {
    if (animation) {
      // Wall clock, not frame delta: a preset flight takes the same time to
      // land whether we are running at 144 fps or crawling through a tile burst.
      animation.t = Math.min(1, (performance.now() - animation.start) / (animation.duration * 1000));
      // Smootherstep, so presets glide instead of snapping.
      const a = animation.t;
      const e = a * a * a * (a * (a * 6 - 15) + 10);
      state.pivot.lerpVectors(animation.fromPivot, animation.toPivot, e);
      state.yaw = animation.fromYaw + (animation.toYaw - animation.fromYaw) * e;
      state.pitch = animation.fromPitch + (animation.toPitch - animation.fromPitch) * e;
      state.distance =
        animation.fromDistance * (animation.toDistance / animation.fromDistance) ** e;
      // Aim: the camera re-targets every frame of the tween, so a flight to a
      // tower keeps looking at its mid-height rather than swinging up at the end.
      if (animation.toY === null) {
        state.pivot.y += (groundHeight(state.pivot.x, state.pivot.z) - state.pivot.y) * Math.min(1, dt * 6);
      } else {
        state.pivot.y = animation.fromY + (animation.toY - animation.fromY) * e;
      }
      if (animation.t >= 1) {
        state.holdY = animation.toY !== null;
        animation = null;
      }
      apply();
      return;
    }

    // Pan speed scales with altitude: a keystroke crosses a similar fraction of
    // the screen whether you are on Market St or 9 km up.
    const speed = Math.max(60, state.distance * 0.85) * state.boost;
    forward.set(-Math.sin(state.yaw), 0, -Math.cos(state.yaw));
    right.set(forward.z, 0, -forward.x);

    let mx = 0;
    let mz = 0;
    if (keys.has('KeyW') || keys.has('ArrowUp')) mz += 1;
    if (keys.has('KeyS') || keys.has('ArrowDown')) mz -= 1;
    if (keys.has('KeyD') || keys.has('ArrowRight')) mx += 1;
    if (keys.has('KeyA') || keys.has('ArrowLeft')) mx -= 1;

    // Edge scrolling.
    if (state.edgeScroll && pointerPx.x > -500 && !dragMode && !gesture) {
      const w = domElement.clientWidth;
      const h = domElement.clientHeight;
      const band = 22;
      if (pointerPx.x < band) mx -= (band - pointerPx.x) / band;
      if (pointerPx.x > w - band) mx += (pointerPx.x - (w - band)) / band;
      if (pointerPx.y < band) mz += (band - pointerPx.y) / band;
      if (pointerPx.y > h - band) mz -= (pointerPx.y - (h - band)) / band;
    }

    if (mx !== 0 || mz !== 0) state.holdY = false;
    moveTarget.set(0, 0, 0).addScaledVector(forward, mz * speed).addScaledVector(right, mx * speed);
    // Smoothed velocity: no jerk on key press or release.
    state.velocity.lerp(moveTarget, Math.min(1, dt * 7));
    state.pivot.addScaledVector(state.velocity, dt);
    clampPivot();

    if (diorama) {
      state.pitch = DIORAMA.pitch;
      if (yawStep) {
        const t = Math.min(1, (performance.now() - yawStep.start) / (yawStep.duration * 1000));
        const e = t * t * (3 - 2 * t);
        // Shortest path: the target is normalised against the current heading, so
        // a step across 0/360 never unwinds the long way round.
        const to = normaliseYaw(yawStep.from, yawStep.to);
        state.yaw = yawStep.from + (to - yawStep.from) * e;
        if (t >= 1) {
          state.yaw = to;
          yawStep = null;
        }
      }
    } else {
      let yawInput = 0;
      if (keys.has('KeyQ')) yawInput += 1;
      if (keys.has('KeyE')) yawInput -= 1;
      state.yawVelocity += (yawInput * 1.5 - state.yawVelocity) * Math.min(1, dt * 8);
      state.yaw += state.yawVelocity * dt;
    }

    let zoomInput = 0;
    if (keys.has('KeyR') || keys.has('PageUp')) zoomInput -= 1;
    if (keys.has('KeyF') || keys.has('PageDown')) zoomInput += 1;
    if (zoomInput !== 0) {
      state.distance = Math.min(
        state.maxDistance,
        Math.max(state.minDistance, state.distance * Math.exp(zoomInput * dt * 1.6))
      );
      if (!pitchLocked) state.pitch = pitchForDistance(state.distance);
    }

    // The pivot rides the terrain, so pushing uphill tilts the whole view up —
    // unless it is held at a focused entity's mid-height.
    if (!state.holdY) {
      const ground = groundHeight(state.pivot.x, state.pivot.z);
      state.pivot.y += (ground - state.pivot.y) * Math.min(1, dt * 5);
    }
    apply();
  }

  // `preset.y` aims at a point above the ground (an entity's mid-height) and
  // holds that aim after the flight; without it the rig lands on the terrain.
  function flyTo(preset, duration = 2.4) {
    const toY = Number.isFinite(preset.y) ? preset.y : null;
    animation = {
      t: 0,
      duration,
      start: performance.now(),
      fromPivot: state.pivot.clone(),
      fromY: state.pivot.y,
      toY,
      toPivot: new Vector3(preset.x, toY ?? groundHeight(preset.x, preset.z), preset.z),
      fromYaw: state.yaw,
      toYaw: normaliseYaw(state.yaw, preset.yaw * DEG),
      fromPitch: state.pitch,
      toPitch: preset.pitch * DEG,
      fromDistance: state.distance,
      toDistance: preset.distance,
    };
    pitchLocked = true;
  }

  // Hand a view that is aimed at ALTITUDE back to the ground without moving the
  // camera a pixel.
  //
  // A follow camera orbits a point in the sky — a plane at 1600 m. Simply
  // clearing holdY drops the pivot to the terrain (the !holdY branch in
  // update), and since the camera is a fixed offset from the pivot it falls the
  // aircraft's whole altitude with it: a violent lurch downward the instant any
  // movement input arrives, which edge-scroll supplies just from where the
  // cursor happens to rest.
  //
  // So instead of moving the camera to suit the pivot, move the PIVOT to suit
  // the camera: drop it to the ground directly below, then solve the distance
  // and pitch that describe the very same camera position orbiting that new
  // point. Yaw is untouched because the horizontal direction does not change.
  // The result is that releasing a follow is invisible — the view is identical
  // before and after, it is simply anchored to the ground again.
  function releaseHold() {
    if (!state.holdY) return;
    // Solve for DISTANCE and the pivot's ground position, holding yaw and pitch
    // fixed. Pitch is not ours to choose: diorama mode pins it at 42 degrees
    // and rewrites it every frame, so a solution that changes pitch is undone
    // immediately and the camera slides away over the following second.
    // Distance and where the pivot sits on the ground are the free variables.
    const sinPitch = Math.sin(state.pitch);
    const cosPitch = Math.cos(state.pitch);
    const dirX = Math.sin(state.yaw) * cosPitch;
    const dirZ = Math.cos(state.yaw) * cosPitch;
    const cx = camera.position.x;
    const cy = camera.position.y;
    const cz = camera.position.z;
    // The pivot's ground height depends on where the pivot lands, which depends
    // on the distance, which depends on the ground height — so settle it with a
    // few iterations rather than pretending it is closed-form.
    let ground = groundHeight(state.pivot.x, state.pivot.z);
    let distance = state.distance;
    for (let i = 0; i < 4; i++) {
      distance = Math.min(
        state.maxDistance,
        Math.max(state.minDistance, (cy - ground) / Math.max(sinPitch, 0.05))
      );
      ground = groundHeight(cx - dirX * distance, cz - dirZ * distance);
    }
    state.distance = distance;
    state.pivot.set(cx - dirX * distance, ground, cz - dirZ * distance);
    state.holdY = false;
    clampPivot();
    apply();
  }

  function set(preset) {
    state.holdY = Number.isFinite(preset.y);
    state.pivot.set(preset.x, state.holdY ? preset.y : groundHeight(preset.x, preset.z), preset.z);
    state.yaw = preset.yaw * DEG;
    state.pitch = preset.pitch * DEG;
    state.distance = preset.distance;
    pitchLocked = true;
    apply();
  }

  function dispose() {
    domElement.removeEventListener('pointerdown', onPointerDown);
    domElement.removeEventListener('pointerup', onPointerUp);
    domElement.removeEventListener('pointercancel', onPointerUp);
    domElement.removeEventListener('pointermove', onPointerMove);
    domElement.removeEventListener('pointerleave', onPointerLeave);
    domElement.removeEventListener('wheel', onWheel);
    domElement.removeEventListener('contextmenu', onContextMenu);
    window.removeEventListener('keydown', onKeyDown);
    window.removeEventListener('keyup', onKeyUp);
  }

  return {
    state,
    update,
    flyTo,
    set,
    releaseHold,
    setDiorama,
    get diorama() {
      return diorama;
    },
    get flying() {
      return animation !== null;
    },
    dispose,
    screenToGround,
    pointer,
    keys,
  };
}
