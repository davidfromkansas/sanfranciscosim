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
  // how hard they hit. Pure overdraw at ground level, so `low` drops them.
  ultra: { label: 'Ultra', pixelRatio: 2, shadow: 4096, nearScale: 1.35, treeScale: 1.3, windows: 1, samples: 4, poolScale: 1.35, poolStrength: 1 },
  high: { label: 'High', pixelRatio: 1.5, shadow: 3072, nearScale: 1, treeScale: 1, windows: 1, samples: 4, poolScale: 1, poolStrength: 1 },
  medium: { label: 'Medium', pixelRatio: 1, shadow: 2048, nearScale: 0.75, treeScale: 0.7, windows: 1, samples: 2, poolScale: 0.7, poolStrength: 0.9 },
  low: { label: 'Low', pixelRatio: 0.85, shadow: 0, nearScale: 0.5, treeScale: 0.45, windows: 0, samples: 0, poolScale: 0, poolStrength: 0 },
};
export const QUALITY_LADDER = ['low', 'medium', 'high', 'ultra'];

export function createUI({ presets, onPreset, onQuality }) {
  const hud = document.getElementById('hud');
  const debug = document.getElementById('debug');

  const viewPanel = document.createElement('div');
  viewPanel.className = 'panel';
  const viewLabel = document.createElement('label');
  viewLabel.textContent = 'View';
  const select = document.createElement('select');
  presets.forEach((preset, i) => {
    const option = document.createElement('option');
    option.value = String(i);
    option.textContent = preset.key ? `${preset.key} · ${preset.name}` : preset.name;
    select.appendChild(option);
  });
  select.addEventListener('change', () => onPreset(Number(select.value)));
  viewPanel.append(viewLabel, select);

  const qualityPanel = document.createElement('div');
  qualityPanel.className = 'panel';
  const qualityLabel = document.createElement('label');
  qualityLabel.textContent = 'Quality';
  const qualitySelect = document.createElement('select');
  const autoOption = document.createElement('option');
  autoOption.value = 'auto';
  autoOption.textContent = 'Auto';
  qualitySelect.appendChild(autoOption);
  for (const [key, value] of Object.entries(QUALITY)) {
    const option = document.createElement('option');
    option.value = key;
    option.textContent = value.label;
    qualitySelect.appendChild(option);
  }
  qualitySelect.addEventListener('change', () => onQuality(qualitySelect.value));
  const debugToggle = document.createElement('button');
  debugToggle.textContent = 'stats';
  debugToggle.title = 'Toggle the performance overlay (F3)';
  debugToggle.addEventListener('click', () => {
    debug.hidden = !debug.hidden;
  });
  qualityPanel.append(qualityLabel, qualitySelect, debugToggle);

  const help = document.createElement('div');
  help.className = 'panel';
  help.style.maxWidth = '260px';
  help.style.display = 'block';
  help.innerHTML =
    '<label>Controls</label><div style="margin-top:4px;line-height:1.5;color:rgba(255,255,255,.78)">' +
    'WASD / arrows pan · Q E rotate · wheel zooms to cursor · right-drag orbits · left-drag grabs the ground · ' +
    'screen edges scroll · Shift boosts · 0–9 fly to landmarks · H home · / search · ' +
    'the sky follows San Francisco time' +
    '</div>';

  const styleBadge = document.createElement('div');
  styleBadge.className = 'panel';
  styleBadge.hidden = true;
  styleBadge.innerHTML =
    '<label>Diorama mode</label><div style="margin-top:4px;color:rgba(255,255,255,.78)">' +
    'Locked 42° view · Q E step 45° · click anything for its story</div>';

  hud.append(viewPanel, qualityPanel, help, styleBadge);

  window.addEventListener('keydown', (event) => {
    if (event.code === 'F3' || event.key === '`') {
      debug.hidden = !debug.hidden;
      event.preventDefault();
    }
  });

  return {
    setPresetIndex(i) {
      select.value = String(i);
    },
    setQuality(key) {
      qualitySelect.value = key;
    },
    setStyle(toy) {
      styleBadge.hidden = !toy;
    },
    setDebug(text) {
      if (!debug.hidden) debug.textContent = text;
    },
    get debugVisible() {
      return !debug.hidden;
    },
  };
}

export function createLoader() {
  const loader = document.getElementById('loader');
  const bar = loader.querySelector('i');
  let done = false;
  return {
    set(fraction) {
      if (done) return;
      bar.style.width = `${Math.round(Math.min(1, fraction) * 100)}%`;
    },
    finish() {
      if (done) return;
      done = true;
      bar.style.width = '100%';
      loader.classList.add('done');
      setTimeout(() => loader.remove(), 900);
    },
  };
}
