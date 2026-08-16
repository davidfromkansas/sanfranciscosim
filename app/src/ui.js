// HUD: view presets, quality tiers and the debug overlay. Deliberately
// unobtrusive — the city is the interface. Time is not a control: the scene
// runs on San Francisco's real clock (see sky-clock.js).

// The single table of what each tier means. Beyond these numbers, every tier
// key fans out to the subsystems' setQuality(tier) levers (PERF-PLAN #6):
// water (1 noise octave + soft specular on low), agents (live-population caps
// on low), street furniture (clutter classes hide on medium, lamps + signals
// only on low), terrain (30 m grid on medium/low), and the post target's MSAA
// samples below.
export const QUALITY = {
  // poolScale/poolStrength: how far the streetlights' pools of light reach and
  // how hard they hit. Pure overdraw at ground level, so the tier scales them
  // back — but `low` no longer drops them entirely. Losing every pool of light
  // costs the night its single strongest cue (an unlit street reads as a dead
  // one), and the cost is quadratic in the radius, so half the reach is a
  // quarter of the fill. Combined with `low`'s smaller nearScale (fewer lamps
  // exist at all) and its 0.85 pixelRatio, a half-size pool at half strength
  // lands near a fifth of what `high` pays for them.
  ultra: { label: 'Ultra', pixelRatio: 2, shadow: 4096, nearScale: 1.35, treeScale: 1.3, windows: 1, samples: 4, poolScale: 1.35, poolStrength: 1 },
  high: { label: 'High', pixelRatio: 1.5, shadow: 3072, nearScale: 1, treeScale: 1, windows: 1, samples: 4, poolScale: 1, poolStrength: 1 },
  medium: { label: 'Medium', pixelRatio: 1, shadow: 2048, nearScale: 0.75, treeScale: 0.7, windows: 1, samples: 2, poolScale: 0.7, poolStrength: 0.9 },
  low: { label: 'Low', pixelRatio: 0.85, shadow: 0, nearScale: 0.5, treeScale: 0.45, windows: 0, samples: 0, poolScale: 0.5, poolStrength: 0.5 },
};
export const QUALITY_LADDER = ['low', 'medium', 'high', 'ultra'];

// There is no HUD any more. It held four panels — the view presets, the quality
// tier, a keyboard crib sheet and a "Diorama mode" badge — and all four have
// gone, in that order of reluctance.
//
// What they offered is still reachable, by better routes than a select in the
// corner of the sky: every preset is in the search box by name, the numbered
// ones are on the number keys, H is home, and quality is the governor's job —
// it watches the real frame time and moves the tier itself, which is a better
// answer than asking a viewer to guess what their GPU can do. A saved manual
// preference is still honoured if one was ever set (main.js), so nobody who had
// pinned a tier is moved off it.
//
// What is left of this module is the performance overlay, which is not UI: it
// is hidden until F3, and no first-time viewer will ever see it.
export function createUI() {
  const debug = document.getElementById('debug');

  window.addEventListener('keydown', (event) => {
    if (event.code === 'F3' || event.key === '`') {
      debug.hidden = !debug.hidden;
      event.preventDefault();
    }
  });

  return {
    setDebug(text) {
      if (!debug.hidden) debug.textContent = text;
    },
    get debugVisible() {
      return !debug.hidden;
    },
  };
}

// The boot progress indicator now lives in boot.js — a full-screen fog curtain
// with its own reveal gate, mounted from index.html so it paints before any
// module parses. The old bottom hairline bar was removed with it.
