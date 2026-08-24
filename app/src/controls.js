// The keyboard legend in the bottom-left corner: drawn keycaps, not prose, so a
// first-time viewer can see what the city answers to without being told.
//
// The number row is built from the presets main.js already has (which come from
// the tiles manifest), so a new numbered landmark shows up here with no edit —
// the legend cannot drift from the bindings.
//
// Desktop only, and the corner is shared: #context-card owns the same spot when
// something is selected, and the stylesheet hides the legend behind it (sibling
// selector), so this module is mounted AFTER the card.

const MOVE_KEYS = [
  { cap: '↑', label: 'Forward' },
  { cap: '←', label: 'Left' },
  { cap: '↓', label: 'Back' },
  { cap: '→', label: 'Right' },
];

const TURN_KEYS = [
  { cap: 'Q', label: 'Turn counter-clockwise' },
  { cap: 'E', label: 'Turn clockwise' },
];

function el(tag, className, text) {
  const node = document.createElement(tag);
  if (className) node.className = className;
  if (text !== undefined) node.textContent = text;
  return node;
}

function keycap(cap, className = 'keycap') {
  return el('kbd', className, cap);
}

function row(cap, label) {
  const line = el('li', 'legend-row');
  line.append(keycap(cap), el('span', 'legend-label', label));
  return line;
}

export function createControlsLegend(presets) {
  const panel = el('section', 'toy-panel');
  panel.id = 'controls-legend';
  panel.setAttribute('aria-label', 'Keyboard controls');

  const toggle = el('button', 'legend-toggle');
  toggle.type = 'button';
  const toggleText = el('span', 'legend-title', 'Controls');
  toggle.append(keycap('⌨', 'keycap is-glyph'), toggleText, el('span', 'legend-chevron', '▾'));

  const body = el('div', 'legend-body');

  // Arrow cluster: the real key shape, so it reads as the keyboard rather than
  // as a list of glyphs. Up sits over Down, Left and Right flank it.
  const move = el('div', 'legend-group');
  const cluster = el('div', 'legend-cluster');
  for (const key of MOVE_KEYS) {
    const cap = keycap(key.cap);
    cap.dataset.dir = key.label.toLowerCase();
    cap.title = key.label;
    cluster.append(cap);
  }
  const moveLabels = el('ul', 'legend-list');
  moveLabels.append(
    el('li', 'legend-label', '↑ / ↓  move forward and back'),
    el('li', 'legend-label', '← / →  move left and right')
  );
  move.append(cluster, moveLabels);

  const turn = el('ul', 'legend-list legend-turn');
  for (const key of TURN_KEYS) turn.append(row(key.cap, key.label));

  body.append(move, turn);

  // Numbered flights, straight off the manifest: 1-9 in order, whatever they
  // point at today.
  const numbered = presets
    .filter((preset) => /^[1-9]$/.test(preset.key ?? ''))
    .sort((a, b) => a.key.localeCompare(b.key));
  if (numbered.length) {
    const heading = el('p', 'legend-heading', 'Fly to');
    const grid = el('ul', 'legend-list legend-numbers');
    for (const preset of numbered) grid.append(row(preset.key, preset.name));
    body.append(heading, grid);
  }

  panel.append(toggle, body);

  // Collapsed state persists: someone who wants the city uncluttered should not
  // have to fold the legend away on every visit.
  let open = true;
  try {
    open = window.localStorage.getItem('sf.controls') !== 'closed';
  } catch {
    // Safari private windows can reject a read.
  }

  function render() {
    panel.classList.toggle('is-open', open);
    toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    body.hidden = !open;
  }

  toggle.addEventListener('click', () => {
    open = !open;
    render();
    try {
      window.localStorage.setItem('sf.controls', open ? 'open' : 'closed');
    } catch {
      // Ignore: the panel still works, it just forgets.
    }
  });

  render();
  document.body.appendChild(panel);

  return {
    get open() {
      return open;
    },
    setVisible(visible) {
      panel.hidden = !visible;
    },
  };
}
