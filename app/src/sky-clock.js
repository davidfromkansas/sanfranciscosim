// The deck in the top-left corner: San Francisco's real wall time, today's
// date, one line about whichever body is currently in the sky, the weather, and
// a turntable spinning the city's record. Brushed-metal chassis, pale green LCD
// on the left, metallic blue player on the right, dot-matrix logo bar below.
//
// The DOM is built once and only textContent is written afterwards, so a 1 Hz
// tick costs nothing and never thrashes layout.
//
// The deck is kept as narrow as its contents allow: it sits over the city in
// the top-left corner, and every column it does not need is width the city
// gets back. Both modules are sized to their contents, not split evenly.

import { TZ } from '../../api/_lib/astro.mjs';

// 24-hour, and zero-padded so the digits never change width. This is the
// deck's own formatter: astro.mjs still formats sunset/moonset as 12-hour
// because the concierge answers in prose and "8:38 PM" is what a person says.
// hourCycle rather than hour12:false — the latter renders midnight as 24:00
// under some ICU builds.
const TIME_PARTS = new Intl.DateTimeFormat('en-US', {
  timeZone: TZ,
  hour: '2-digit',
  minute: '2-digit',
  hourCycle: 'h23',
});
const WEEKDAY = new Intl.DateTimeFormat('en-US', { timeZone: TZ, weekday: 'short' });
const MONTH_DAY = new Intl.DateTimeFormat('en-US', { timeZone: TZ, month: 'short', day: 'numeric' });

const SVG_NS = 'http://www.w3.org/2000/svg';

// The deck writes the phase short; the almanac spelling from astro.mjs stays
// as it is because the concierge answers in prose and wants the long form.
// The quarters go to fractions, and the glyph beside the text already draws
// the shape, so the words only have to carry waxing vs waning. An unknown
// name falls through to whatever astro sent rather than rendering blank.
const MOON_SHORT = {
  'new moon': 'new',
  'waxing crescent': 'wax cres',
  'first quarter': '1/4',
  'waxing gibbous': 'wax gib',
  'full moon': 'full',
  'waning gibbous': 'wan gib',
  'last quarter': '3/4',
  'waning crescent': 'wan cres',
};

// The record spins for as long as the track plays; the tonearm rides down onto
// it. One CSS animation, paused rather than removed, so nothing re-lays out.
const TRACK_URL = `${import.meta.env.BASE_URL}audio/beats.mp3`;

// The deck has no volume dial: play/pause is the whole of its control surface,
// so the track plays at a fixed level chosen to sit under the city rather than
// over it. This was the knob's default position.
const TRACK_VOLUME = 0.55;

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

// Three drifting strokes: the wind row's own glyph, so the reading never has to
// borrow the cloud that already means "overcast".
function windGlyph() {
  const root = svg('svg', { class: 'sky-glyph', viewBox: '0 0 20 20', 'aria-hidden': 'true' });
  const strokes = [
    'M2.6 7.2h9.2a2.4 2.4 0 1 0-2.4-2.4',
    'M2.6 11h12.6a2.4 2.4 0 1 1-2.4 2.4',
    'M4.4 14.8h6.2',
  ];
  for (const d of strokes) {
    root.appendChild(
      svg('path', { d, fill: 'none', stroke: 'var(--teal)', 'stroke-width': 2, 'stroke-linecap': 'round' })
    );
  }
  return root;
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
  return TIME_PARTS.format(new Date(ms)).trim();
}

const formatWeekday = (ms) => WEEKDAY.format(new Date(ms)).toUpperCase();
const formatMonthDay = (ms) => MONTH_DAY.format(new Date(ms)).toUpperCase();

// The pale-green pip the LCD uses between two readings instead of a middle dot.
function pip() {
  const dot = document.createElement('span');
  dot.className = 'clock-dot';
  dot.setAttribute('aria-hidden', 'true');
  return dot;
}

// The turntable: a looping record with a play/pause centre and a tonearm that
// rides down while it plays. Autoplay is blocked until the visitor has
// interacted with the page, so the deck arms itself on the first gesture
// anywhere and only gives up if playback is refused outright.
function createPlayer() {
  const module = document.createElement('div');
  module.className = 'deck-module deck-player';

  const label = document.createElement('div');
  label.className = 'player-label';
  const cue = svg('svg', { class: 'player-cue', viewBox: '0 0 10 10', 'aria-hidden': 'true' });
  cue.appendChild(svg('path', { d: 'M2 1.4 8.4 5 2 8.6Z', fill: 'var(--neon)' }));
  const labelText = document.createElement('span');
  labelText.textContent = 'now playing';
  label.append(cue, labelText);

  const platter = document.createElement('div');
  platter.className = 'player-platter';

  const disc = document.createElement('div');
  disc.className = 'player-disc';

  const button = document.createElement('button');
  button.type = 'button';
  button.className = 'player-button';
  const icon = svg('svg', { class: 'player-icon', viewBox: '0 0 12 12', 'aria-hidden': 'true' });
  const barLeft = svg('rect', { x: 3, y: 2.2, width: 2.2, height: 7.6, rx: 0.6, fill: 'currentColor' });
  const barRight = svg('rect', { x: 6.8, y: 2.2, width: 2.2, height: 7.6, rx: 0.6, fill: 'currentColor' });
  const wedge = svg('path', { d: 'M3.6 2.2 9.6 6l-6 3.8Z', fill: 'currentColor' });
  icon.append(barLeft, barRight, wedge);
  button.appendChild(icon);

  const pivot = document.createElement('div');
  pivot.className = 'player-pivot';

  const arm = document.createElement('div');
  arm.className = 'player-arm';
  const armHead = document.createElement('div');
  armHead.className = 'player-arm-head';
  arm.appendChild(armHead);

  platter.append(disc, button);

  const deckFoot = document.createElement('div');
  deckFoot.className = 'player-foot';
  const led = document.createElement('span');
  led.className = 'player-led';
  deckFoot.appendChild(led);

  module.append(label, platter, pivot, arm, deckFoot);

  const audio = new Audio(TRACK_URL);
  audio.loop = true;
  audio.preload = 'auto';
  audio.volume = TRACK_VOLUME;

  // The record is only ever asked to spin or hold: the animation stays attached
  // so the groove keeps its angle across a pause.
  function paint() {
    const playing = !audio.paused;
    module.classList.toggle('is-playing', playing);
    button.setAttribute('aria-label', playing ? 'Pause the record' : 'Play the record');
    button.setAttribute('aria-pressed', String(playing));
  }

  // One shared arming path: an explicit click and the page's first gesture both
  // land here, and a refusal simply leaves the deck stopped.
  let armed = false;
  function tryPlay() {
    const attempt = audio.play();
    if (attempt && typeof attempt.catch === 'function') attempt.catch(() => paint());
  }

  // A pointerdown on the button itself must NOT arm the deck: pointerdown runs
  // before click, so arming here would start the record and the click that
  // follows would read it as playing and stop it again.
  function armOnGesture(event) {
    if (armed) return;
    if (event.target instanceof Node && button.contains(event.target)) return;
    armed = true;
    window.removeEventListener('pointerdown', armOnGesture);
    window.removeEventListener('keydown', armOnGesture);
    tryPlay();
  }

  button.addEventListener('click', () => {
    armed = true;
    window.removeEventListener('pointerdown', armOnGesture);
    window.removeEventListener('keydown', armOnGesture);
    if (audio.paused) tryPlay();
    else audio.pause();
  });

  audio.addEventListener('play', paint);
  audio.addEventListener('pause', paint);

  window.addEventListener('pointerdown', armOnGesture);
  window.addEventListener('keydown', armOnGesture);
  // Some browsers allow a muted-adjacent start; asking once costs nothing and
  // saves the visitor a click when the policy permits it.
  tryPlay();
  paint();

  return {
    element: module,
    dispose() {
      window.removeEventListener('pointerdown', armOnGesture);
      window.removeEventListener('keydown', armOnGesture);
      audio.pause();
      audio.src = '';
    },
  };
}

export function createSkyClock({ read, readWeather = () => null }) {
  const panel = document.createElement('div');
  panel.id = 'sky-clock';
  panel.className = 'sfsim-deck';
  panel.setAttribute('aria-label', 'SFSIM status widget');

  const row = document.createElement('div');
  row.className = 'deck-row';

  const info = document.createElement('div');
  info.className = 'deck-module deck-info';
  const body = document.createElement('div');
  body.className = 'info-body';
  info.appendChild(body);

  const timeRow = document.createElement('div');
  timeRow.className = 'clock-time';
  const clockNode = document.createElement('span');
  clockNode.className = 'clock-hm';
  timeRow.appendChild(clockNode);

  const dateNode = document.createElement('div');
  dateNode.className = 'clock-date';
  const weekdayNode = document.createElement('span');
  const monthDayNode = document.createElement('span');
  dateNode.append(weekdayNode, pip(), monthDayNode);

  const skyRow = document.createElement('div');
  skyRow.className = 'clock-row clock-sky';
  const sun = sunGlyph();
  const moon = moonGlyph();
  // SVG elements do not honour the [hidden] attribute the way HTML ones do.
  moon.style.display = 'none';
  const skyText = document.createElement('span');
  skyRow.append(sun, moon, skyText);

  // The weather rows. Built once like everything else here; when the feed is
  // not live they are simply hidden — a diorama has no error states.
  const weatherRow = document.createElement('div');
  weatherRow.className = 'clock-row clock-weather';
  weatherRow.hidden = true;
  let weatherKind = null;
  let weatherIcon = null;
  const tempNode = document.createElement('span');
  const conditionNode = document.createElement('span');
  weatherRow.append(tempNode, pip(), conditionNode);

  // The wind is its own row so the narrow-screen drop is a CSS media query,
  // not a per-second read of window.innerWidth (a layout read, and one that
  // reports 0 in a backgrounded tab).
  const windRow = document.createElement('div');
  windRow.className = 'clock-row clock-wind';
  windRow.hidden = true;
  const windText = document.createElement('span');
  windRow.append(windGlyph(), windText);

  const aqiChip = document.createElement('span');
  aqiChip.className = 'clock-aqi';
  aqiChip.hidden = true;

  body.append(timeRow, dateNode, skyRow, weatherRow, windRow, aqiChip);

  const player = createPlayer();
  row.append(info, player.element);

  const logo = document.createElement('div');
  logo.className = 'deck-logo';
  const grillLeft = document.createElement('span');
  grillLeft.className = 'logo-grill';
  const logoText = document.createElement('span');
  logoText.className = 'logo-text';
  logoText.textContent = 'WWW.SFSIM.NET';
  const grillRight = document.createElement('span');
  grillRight.className = 'logo-grill';
  // No chevrons: the >>> <<< pair cost ~46px that the wordmark now spends on
  // type size instead. The grills still carry the hi-fi faceplate read.
  logo.append(grillLeft, logoText, grillRight);

  const credit = document.createElement('a');
  credit.className = 'deck-credit';
  credit.href = 'https://www.linkedin.com/in/davidfromkansas';
  credit.target = '_blank';
  credit.rel = 'noopener noreferrer';
  credit.textContent = 'Made by David Lietjauw';

  panel.append(row, logo, credit);
  document.body.appendChild(panel);

  function renderWeather() {
    const weather = readWeather();
    const summary = weather?.live ? weather.summary : null;
    if (!summary) {
      weatherRow.hidden = true;
      windRow.hidden = true;
      aqiChip.hidden = true;
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

    const temp = `${Math.round(summary.temp)}°`;
    if (tempNode.textContent !== temp) tempNode.textContent = temp;
    if (conditionNode.textContent !== summary.label) conditionNode.textContent = summary.label;

    // Below 480 px CSS drops this row, not the temperature.
    const gust = summary.windSpeed >= 1 ? `${Math.round(summary.windSpeed)} mph ${compass(summary.windDir)}` : '';
    windRow.hidden = gust === '';
    if (windText.textContent !== gust) windText.textContent = gust;

    // Always shown whenever there is a reading, not only when the air is bad:
    // a chip that appears once a year is a chip nobody knows exists, and clean
    // air on a clear day is worth stating. Colour carries the severity.
    const aqi = weather.aqi ?? summary.aqi;
    aqiChip.hidden = !Number.isFinite(aqi);
    if (!aqiChip.hidden) {
      const text = `AQI ${Math.round(aqi)}`;
      if (aqiChip.textContent !== text) aqiChip.textContent = text;
      // EPA bands: good / moderate / unhealthy for sensitive groups / worse.
      aqiChip.dataset.tone = aqi <= 50 ? 'forest' : aqi <= 100 ? 'mustard' : aqi <= 150 ? 'coral' : 'plum';
      aqiChip.title = aqi <= 50 ? 'Air quality: good' : aqi <= 100 ? 'Air quality: moderate' : aqi <= 150 ? 'Air quality: unhealthy for sensitive groups' : 'Air quality: unhealthy';
    }
  }

  function render() {
    const sky = read();
    // The time itself never depends on the astronomy: if the sky maths is
    // unavailable the panel keeps telling San Francisco's time and simply drops
    // the sun/moon line.
    const ms = sky ? sky.epochMs : Date.now();
    const clock = formatTime(ms);
    if (clockNode.textContent !== clock) clockNode.textContent = clock;

    const weekday = formatWeekday(ms);
    if (weekdayNode.textContent !== weekday) weekdayNode.textContent = weekday;
    const monthDay = formatMonthDay(ms);
    if (monthDayNode.textContent !== monthDay) monthDayNode.textContent = monthDay;

    renderWeather();

    if (!sky) {
      sun.style.display = 'none';
      moon.style.display = 'none';
      if (skyText.textContent !== '') skyText.textContent = '';
      return;
    }

    sun.style.display = sky.isDay ? '' : 'none';
    moon.style.display = sky.isDay ? 'none' : '';
    // The moon line is the phase and nothing else: its rise/set time was the
    // longest string on the LCD and had been silently truncated at every width
    // this deck has ever shipped at. The sun keeps its set time — that one
    // fits, and it is the reading people actually look for by day.
    const line = sky.isDay
      ? `sets ${sky.sunsetMs ? formatTime(sky.sunsetMs) : '—'}`
      : MOON_SHORT[sky.moon.phaseName] || sky.moon.phaseName;
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
      player.dispose();
      panel.remove();
    },
  };
}
