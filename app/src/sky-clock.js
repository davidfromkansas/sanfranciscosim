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

// A flat toy cloud, used alone for overcast and tucked behind the sun for
// partly cloudy. Same 2 px ink stroke as the sun and the moon.
function cloudPath(fill) {
  return svg('path', {
    d: 'M5.6 15.4a3.4 3.4 0 0 1 .5-6.8 4.7 4.7 0 0 1 9-1.2 3.9 3.9 0 0 1-.7 8Z',
    fill,
    stroke: 'var(--ink)',
    'stroke-width': 2,
    'stroke-linejoin': 'round',
  });
}

function weatherGlyph(kind) {
  const root = svg('svg', { class: 'sky-glyph', viewBox: '0 0 20 20', 'aria-hidden': 'true' });
  if (kind === 'clear') {
    root.appendChild(svg('circle', { cx: 10, cy: 10, r: 4.6, fill: 'var(--mustard)', stroke: 'var(--ink)', 'stroke-width': 2 }));
    for (let i = 0; i < 8; i++) {
      const a = (i * Math.PI) / 4;
      root.appendChild(
        svg('line', {
          x1: (10 + Math.cos(a) * 7).toFixed(2),
          y1: (10 + Math.sin(a) * 7).toFixed(2),
          x2: (10 + Math.cos(a) * 8.9).toFixed(2),
          y2: (10 + Math.sin(a) * 8.9).toFixed(2),
          stroke: 'var(--ink)',
          'stroke-width': 2,
          'stroke-linecap': 'round',
        })
      );
    }
    return root;
  }
  if (kind === 'partly') {
    root.appendChild(svg('circle', { cx: 13.4, cy: 6.6, r: 3.6, fill: 'var(--mustard)', stroke: 'var(--ink)', 'stroke-width': 2 }));
    root.appendChild(cloudPath('var(--paper-2)'));
    return root;
  }
  if (kind === 'fog') {
    root.appendChild(cloudPath('var(--paper-2)'));
    for (let i = 0; i < 3; i++) {
      root.appendChild(
        svg('line', {
          x1: 3.2 + (i % 2) * 1.6,
          y1: 16.4 + i * 0,
          x2: 16.4 - (i % 2) * 1.8,
          y2: 16.4,
          stroke: 'var(--ink)',
          'stroke-width': 2,
          'stroke-linecap': 'round',
          transform: `translate(0 ${i * 0})`,
          opacity: 1 - i * 0.25,
        })
      );
    }
    return root;
  }
  // cloudy, drizzle, rain, heavy, storm, snow all start from a cloud.
  root.appendChild(cloudPath(kind === 'storm' ? 'var(--navy)' : 'var(--paper-2)'));
  if (kind === 'drizzle' || kind === 'rain' || kind === 'heavy') {
    const drops = kind === 'heavy' ? 3 : 2;
    for (let i = 0; i < drops; i++) {
      root.appendChild(
        svg('line', {
          x1: 6.4 + i * 3.6,
          y1: 16.2,
          x2: 5.2 + i * 3.6,
          y2: 19,
          stroke: 'var(--teal)',
          'stroke-width': 2,
          'stroke-linecap': 'round',
        })
      );
    }
  }
  if (kind === 'storm') {
    root.appendChild(
      svg('path', { d: 'M10.8 14.6 8 18.6h2.6l-1 3 3.4-4.4h-2.4l1.2-2.6Z', fill: 'var(--mustard)', stroke: 'var(--ink)', 'stroke-width': 1.6, 'stroke-linejoin': 'round' })
    );
  }
  return root;
}

const COMPASS = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW'];
// Meteorological direction is where the wind comes FROM, which is what a
// person means by "a westerly".
const compass = (deg) => COMPASS[Math.round(((deg % 360) + 360) % 360 / 45) % 8];

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

export function createSkyClock({ read, readWeather = () => null }) {
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

  // The weather line. Built once like everything else here; when the feed is
  // not live the whole row is simply hidden — a diorama has no error states.
  const weatherRow = document.createElement('div');
  weatherRow.className = 'clock-weather';
  weatherRow.hidden = true;
  let weatherKind = null;
  let weatherIcon = null;
  const weatherText = document.createElement('span');
  // The wind is its own node so the narrow-screen drop is a CSS media query,
  // not a per-second read of window.innerWidth (a layout read, and one that
  // reports 0 in a backgrounded tab).
  const windText = document.createElement('span');
  windText.className = 'clock-wind';
  const aqiChip = document.createElement('span');
  aqiChip.className = 'chip clock-aqi';
  aqiChip.hidden = true;
  weatherRow.append(weatherText, windText, aqiChip);

  panel.append(timeRow, dateNode, skyRow, weatherRow);
  document.body.appendChild(panel);

  function renderWeather() {
    const weather = readWeather();
    const summary = weather?.live ? weather.summary : null;
    if (!summary) {
      weatherRow.hidden = true;
      return;
    }
    weatherRow.hidden = false;

    // Swap the glyph only when the condition class actually changes.
    if (summary.kind !== weatherKind) {
      weatherKind = summary.kind;
      const next = weatherGlyph(weatherKind);
      if (weatherIcon) weatherIcon.replaceWith(next);
      else weatherRow.prepend(next);
      weatherIcon = next;
    }

    const line = `${Math.round(summary.temp)}° · ${summary.label}`;
    if (weatherText.textContent !== line) weatherText.textContent = line;

    // Below 480 px CSS drops this line, not the temperature.
    const gust = summary.windSpeed >= 1 ? ` · ${Math.round(summary.windSpeed)} mph ${compass(summary.windDir)}` : '';
    if (windText.textContent !== gust) windText.textContent = gust;

    // The eased value so a debug override moves the chip; the feed's own
    // reading when nothing has overridden it.
    const aqi = weather.aqi ?? summary.aqi;
    aqiChip.hidden = !(Number.isFinite(aqi) && aqi > 100);
    if (!aqiChip.hidden) {
      const text = `AQI ${Math.round(aqi)}`;
      if (aqiChip.textContent !== text) aqiChip.textContent = text;
      aqiChip.dataset.tone = aqi > 150 ? 'coral' : 'mustard';
    }
  }

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

    renderWeather();

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
