// The clock in the top-left corner: San Francisco's real wall time, today's
// date, and one line about whichever body is currently in the sky. Cream card
// stock, 2 px ink border, hard offset shadow — the tokens in ui-theme.css and
// nothing else.
//
// The DOM is built once and only textContent is written afterwards, so a 1 Hz
// tick costs nothing and never thrashes layout.

import { TZ } from '../../api/_lib/astro.mjs';

const TIME_PARTS = new Intl.DateTimeFormat('en-US', { timeZone: TZ, hour: 'numeric', minute: '2-digit' });
const WEEKDAY = new Intl.DateTimeFormat('en-US', { timeZone: TZ, weekday: 'short' });
const MONTH_DAY = new Intl.DateTimeFormat('en-US', { timeZone: TZ, month: 'short', day: 'numeric' });

const SVG_NS = 'http://www.w3.org/2000/svg';

function svg(name, attributes) {
  const node = document.createElementNS(SVG_NS, name);
  for (const [key, value] of Object.entries(attributes)) node.setAttribute(key, value);
  return node;
}

// A drawn glyph, not an emoji: 2 px ink strokes over flat toy fills.
function sunGlyph() {
  const root = svg('svg', { class: 'sky-glyph', viewBox: '0 0 20 20', 'aria-hidden': 'true' });
  root.appendChild(svg('circle', { cx: 10, cy: 10, r: 4.4, fill: 'var(--mustard)', stroke: 'var(--ink)', 'stroke-width': 2 }));
  for (let i = 0; i < 8; i++) {
    const a = (i * Math.PI) / 4;
    root.appendChild(
      svg('line', {
        x1: (10 + Math.cos(a) * 7).toFixed(2),
        y1: (10 + Math.sin(a) * 7).toFixed(2),
        x2: (10 + Math.cos(a) * 8.8).toFixed(2),
        y2: (10 + Math.sin(a) * 8.8).toFixed(2),
        stroke: 'var(--ink)',
        'stroke-width': 2,
        'stroke-linecap': 'round',
      })
    );
  }
  return root;
}

function moonGlyph() {
  const root = svg('svg', { class: 'sky-glyph', viewBox: '0 0 20 20', 'aria-hidden': 'true' });
  root.appendChild(
    svg('path', {
      d: 'M13.4 2.9a7.6 7.6 0 1 0 3.6 9.9 6 6 0 0 1-3.6-9.9Z',
      fill: 'var(--paper-2)',
      stroke: 'var(--ink)',
      'stroke-width': 2,
      'stroke-linejoin': 'round',
    })
  );
  return root;
}

function formatTime(ms) {
  const parts = TIME_PARTS.formatToParts(new Date(ms));
  let clock = '';
  let period = '';
  for (const part of parts) {
    if (part.type === 'dayPeriod') period = part.value.toUpperCase();
    else if (part.type !== 'literal' || clock) clock += part.value;
  }
  return { clock: clock.trim(), period };
}

const formatDate = (ms) =>
  `${WEEKDAY.format(new Date(ms))} · ${MONTH_DAY.format(new Date(ms))}`.toUpperCase();

export function createSkyClock({ read }) {
  const panel = document.createElement('div');
  panel.id = 'sky-clock';
  panel.className = 'toy-panel';

  const timeRow = document.createElement('div');
  timeRow.className = 'clock-time';
  const clockNode = document.createElement('span');
  clockNode.className = 'clock-hm';
  const periodNode = document.createElement('span');
  periodNode.className = 'chip clock-period';
  periodNode.dataset.tone = 'mustard';
  timeRow.append(clockNode, periodNode);

  const dateNode = document.createElement('div');
  dateNode.className = 'clock-date';

  const skyRow = document.createElement('div');
  skyRow.className = 'clock-sky';
  const sun = sunGlyph();
  const moon = moonGlyph();
  // SVG elements do not honour the [hidden] attribute the way HTML ones do.
  moon.style.display = 'none';
  const skyText = document.createElement('span');
  skyRow.append(sun, moon, skyText);

  panel.append(timeRow, dateNode, skyRow);
  document.body.appendChild(panel);

  function render() {
    const sky = read();
    // The time itself never depends on the astronomy: if the sky maths is
    // unavailable the panel keeps telling San Francisco's time and simply drops
    // the sun/moon line.
    const ms = sky ? sky.epochMs : Date.now();
    const { clock, period } = formatTime(ms);
    if (clockNode.textContent !== clock) clockNode.textContent = clock;
    if (periodNode.textContent !== period) periodNode.textContent = period;
    periodNode.dataset.tone = !sky || sky.isDay ? 'mustard' : 'navy';

    const date = formatDate(ms);
    if (dateNode.textContent !== date) dateNode.textContent = date;

    if (!sky) {
      sun.style.display = 'none';
      moon.style.display = 'none';
      if (skyText.textContent !== '') skyText.textContent = '';
      return;
    }

    sun.style.display = sky.isDay ? '' : 'none';
    moon.style.display = sky.isDay ? 'none' : '';
    const line = sky.isDay
      ? `sets ${sky.sun.sunset || '—'}`
      : [sky.moon.phaseName, sky.moon.isUp ? `sets ${sky.moon.moonset || '—'}` : `rises ${sky.moon.moonrise || '—'}`]
          .join(' · ');
    if (skyText.textContent !== line) skyText.textContent = line;
  }

  render();
  // Its own 1 Hz timer rather than the render loop: the clock must keep ticking
  // even when the GPU is crawling.
  const timer = setInterval(render, 1000);

  return {
    element: panel,
    update: render,
    dispose() {
      clearInterval(timer);
      panel.remove();
    },
  };
}
