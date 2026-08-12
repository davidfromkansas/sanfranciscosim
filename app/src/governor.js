const DEFAULT_TAU_MS = 1000;
const DOWN_THRESHOLD_MS = 19;
const DOWN_SUSTAIN_MS = 1500;
const UP_THRESHOLD_MS = 12;
const UP_SUSTAIN_MS = 10000;
const DOWN_COOLDOWN_MS = 4000;
const UP_COOLDOWN_MS = 10000;
const UNSTABLE_WINDOW_MS = 30000;
const STREAMING_WINDOW_MS = 1500;

export function createGovernor({
  tiers,
  ladder,
  initialTier,
  mode = 'auto',
  apply,
  isFlying,
  readStreaming,
  tauMs = DEFAULT_TAU_MS,
}) {
  if (!Array.isArray(ladder) || ladder.length !== Object.keys(tiers).length) {
    throw new Error('quality governor requires a complete worst-to-best tier ladder');
  }
  const keys = ladder.slice();
  const indexByKey = Object.create(null);
  for (let i = 0; i < keys.length; i++) {
    const key = keys[i];
    if (!tiers[key] || indexByKey[key] !== undefined) {
      throw new Error(`quality governor ladder has invalid tier: ${key}`);
    }
    indexByKey[key] = i;
  }

  let current = indexByKey[initialTier] === undefined ? keys[0] : indexByKey[initialTier];
  let currentMode = mode === 'auto' || indexByKey[mode] !== undefined ? mode : 'auto';
  if (currentMode !== 'auto') current = indexByKey[currentMode];
  let emaMs = null;
  let clockMs = 0;
  let lastChangeMs = 0;
  let lastStepUpMs = -Infinity;
  let downQualifyingMs = 0;
  let upQualifyingMs = 0;
  let cooldownMs = 0;
  let unstable = 0;
  let lastCells = null;
  let lastNearChunks = null;
  let streamingUntilMs = 0;
  let totalChanges = 0;

  function resetQualification() {
    downQualifyingMs = 0;
    upQualifyingMs = 0;
  }

  function changeTier(next) {
    if (next < 0 || next >= keys.length || next === current || (unstable & (1 << next))) return false;
    const previous = current;
    current = next;
    lastChangeMs = clockMs;
    cooldownMs = next < previous ? DOWN_COOLDOWN_MS : UP_COOLDOWN_MS;
    if (next > previous) lastStepUpMs = clockMs;
    else if (lastStepUpMs > -Infinity && clockMs - lastStepUpMs <= UNSTABLE_WINDOW_MS) {
      unstable |= 1 << previous;
    }
    totalChanges++;
    apply(keys[next]);
    resetQualification();
    return true;
  }

  function update(frameTimeMs) {
    const dtMs = Number.isFinite(frameTimeMs) && frameTimeMs > 0 ? frameTimeMs : 0;
    clockMs += dtMs;
    if (emaMs === null) emaMs = dtMs;
    else emaMs += (dtMs - emaMs) * (1 - Math.exp(-dtMs / tauMs));

    const streaming = readStreaming();
    if (
      streaming &&
      (streaming.cellsLoaded !== lastCells || streaming.nearChunks !== lastNearChunks)
    ) {
      lastCells = streaming.cellsLoaded;
      lastNearChunks = streaming.nearChunks;
      streamingUntilMs = clockMs + STREAMING_WINDOW_MS;
    }
    const flying = isFlying();
    if (cooldownMs > 0) cooldownMs = Math.max(0, cooldownMs - dtMs);

    if (currentMode !== 'auto' || flying || clockMs < streamingUntilMs) {
      resetQualification();
      return;
    }
    if (cooldownMs > 0) {
      resetQualification();
      return;
    }

    if (emaMs > DOWN_THRESHOLD_MS) {
      downQualifyingMs += dtMs;
      upQualifyingMs = 0;
    } else if (emaMs < UP_THRESHOLD_MS) {
      upQualifyingMs += dtMs;
      downQualifyingMs = 0;
    } else {
      resetQualification();
    }

    if (downQualifyingMs >= DOWN_SUSTAIN_MS) {
      if (!changeTier(current - 1)) resetQualification();
    } else if (upQualifyingMs >= UP_SUSTAIN_MS) {
      if (!changeTier(current + 1)) resetQualification();
    }
  }

  function setMode(nextMode) {
    currentMode = nextMode === 'auto' || indexByKey[nextMode] !== undefined ? nextMode : 'auto';
    if (currentMode !== 'auto') current = indexByKey[currentMode];
    resetQualification();
  }

  function state() {
    let heldOff = null;
    if (isFlying()) heldOff = 'flying';
    else if (clockMs < streamingUntilMs) heldOff = 'streaming';
    else if (cooldownMs > 0) heldOff = 'cooldown';
    return {
      mode: currentMode,
      tier: keys[current],
      emaMs,
      fps: emaMs ? 1000 / emaMs : null,
      heldOff,
      timeSinceLastChangeMs: clockMs - lastChangeMs,
      totalChanges,
      unstableTiers: keys.filter((_, i) => unstable & (1 << i)),
    };
  }

  return {
    update,
    setMode,
    get mode() {
      return currentMode;
    },
    get tier() {
      return keys[current];
    },
    state,
  };
}
