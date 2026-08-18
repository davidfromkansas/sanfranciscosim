// The toy-paper UI: one reusable context card, one search box. Every string
// that comes from the data is written with textContent — nothing baked from
// open data is ever interpreted as markup, and nothing here invents a fact.

import { CATEGORY_LABELS, confidenceLabel, humanize, sourceLabel } from './context.js';

const GLYPHS = {
  building: '<path d="M4 21V6l7-3v18M11 21h9V10l-9-4M7 10h1M7 14h1M15 12h1M15 16h1"/>',
  park: '<path d="M12 21v-5M6 13l6-9 6 9zM8 17h8l-4-5z"/>',
  street: '<path d="M6 21 9 3M18 21 15 3M12 5v3M12 11v3M12 17v3"/>',
  landmark: '<path d="M12 3 5 9v12h14V9zM9 21v-6h6v6"/>',
  neighborhood: '<path d="M3 8l6-3 6 3 6-3v11l-6 3-6-3-6 3z"/>',
  water: '<path d="M3 9c3-3 6 3 9 0s6-3 9 0M3 15c3-3 6 3 9 0s6-3 9 0"/>',
  search: '<circle cx="11" cy="11" r="6"/><path d="m20 20-4.5-4.5"/>',
  close: '<path d="M6 6l12 12M18 6 6 18"/>',
  fly: '<path d="M3 12h13M12 6l6 6-6 6"/>',
  chat: '<path d="M4 5h16v11H9l-5 4z"/>',
  view: '<circle cx="12" cy="12" r="3"/><path d="M2 12s4-6 10-6 10 6 10 6-4 6-10 6S2 12 2 12z"/>',
  vessel: '<path d="M4 14h16l-2 5H6zM12 14V5l6 4-6 2M7 14v-4h5"/>',
  transit: '<rect x="5" y="4" width="14" height="13" rx="2"/><path d="M5 12h14M8 20l1-3M16 20l-1-3"/><circle cx="9" cy="15" r=".5"/><circle cx="15" cy="15" r=".5"/>',
  aircraft: '<path d="M12 3c.9 0 1.4.9 1.4 2v4.2l7.1 4v2l-7.1-2.2V17l2.2 1.6v1.7L12 19.5l-3.6.8v-1.7L10.6 17v-3.9L3.5 15.3v-2l7.1-4V5c0-1.1.5-2 1.4-2z"/>',
};

const KIND_GLYPH = {
  building: 'building',
  park: 'park',
  street: 'street',
  landmark: 'landmark',
  neighborhood: 'neighborhood',
  water: 'water',
  view: 'view',
  vessel: 'vessel',
  transit: 'transit',
  'transit-stop': 'transit',
  'ferry-terminal': 'vessel',
  aircraft: 'aircraft',
};

const CAT_TONE = [
  'mustard', 'mustard', 'mustard', 'navy', 'coral', 'coral', 'plum', 'coral', 'plum', 'teal',
  'teal', 'coral', 'coral', 'coral', 'navy', 'teal', 'plum', 'plum', 'navy', 'navy',
  'navy', 'mustard', 'forest', 'navy', 'teal', 'teal',
];

function glyph(name, className = 'glyph') {
  const svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
  svg.setAttribute('viewBox', '0 0 24 24');
  svg.setAttribute('class', className);
  svg.setAttribute('aria-hidden', 'true');
  svg.innerHTML = GLYPHS[name] || GLYPHS.building;
  return svg;
}

function el(tag, className, text) {
  const node = document.createElement(tag);
  if (className) node.className = className;
  if (text !== undefined) node.textContent = text;
  return node;
}

// Clock time in the Bay's own timezone, so a viewer anywhere reads the schedule
// the way the terminals post it.
const BAY_TIME = new Intl.DateTimeFormat('en-US', {
  timeZone: 'America/Los_Angeles',
  hour: 'numeric',
  minute: '2-digit',
});

function clock(ms) {
  return Number.isFinite(ms) ? BAY_TIME.format(new Date(ms)) : null;
}

// "in 6 min" / "12 min ago": the useful half of a timestamp for a moving boat.
function relative(ms, now = Date.now()) {
  if (!Number.isFinite(ms)) return null;
  const minutes = Math.round((ms - now) / 60000);
  if (minutes === 0) return 'now';
  if (minutes > 0) return `in ${minutes} min`;
  return `${-minutes} min ago`;
}

const OCCUPANCY_LABEL = {
  empty: 'Empty',
  manySeatsAvailable: 'Many seats available',
  fewSeatsAvailable: 'Few seats available',
  standingRoomOnly: 'Standing room only',
  crushedStandingRoomOnly: 'Crowded',
  full: 'Full',
  notAcceptingPassengers: 'Not accepting passengers',
};

function when(ms) {
  const time = clock(ms);
  return time ? `${time} (${relative(ms)})` : null;
}

function chip(text, tone, glyphName) {
  const node = el('span', 'chip', text);
  if (tone) node.dataset.tone = tone;
  if (glyphName) node.prepend(glyph(glyphName));
  return node;
}

export function createContextCard({ onFly, onAsk, onSelectHistory, onClose }) {
  const card = el('div', 'toy-card');
  card.id = 'context-card';
  card.hidden = true;

  const head = el('div', 'card-head');
  const titleWrap = el('div');
  const title = el('h2', 'card-title');
  const subtitle = el('p', 'card-sub');
  titleWrap.append(title, subtitle);
  const close = el('button', 'icon-button');
  close.type = 'button';
  close.title = 'Close';
  close.setAttribute('aria-label', 'Close');
  close.append(glyph('close'));
  head.append(titleWrap, close);

  const chips = el('div', 'chip-row');
  const facts = el('dl', 'card-facts');
  const source = el('p', 'card-source');
  const actions = el('div', 'card-actions');
  const flyButton = el('button', 'toy-button', 'Fly here');
  flyButton.type = 'button';
  const askButton = el('button', 'toy-button', 'Ask about this');
  askButton.type = 'button';
  askButton.dataset.tone = 'teal';
  actions.append(flyButton, askButton);
  const history = el('div', 'card-history');

  card.append(head, chips, facts, source, actions, history);
  document.body.appendChild(card);

  let current = null;
  close.addEventListener('click', () => {
    // Dismissing the card is also how you let go of whatever it was about —
    // for a followed aircraft that means handing the camera back.
    const dismissed = current;
    hide();
    onClose?.(dismissed);
  });
  flyButton.addEventListener('click', () => current && onFly(current));
  askButton.addEventListener('click', () => current && onAsk(current));

  function fact(term, value) {
    if (value === null || value === undefined || value === '') return;
    facts.append(el('dt', null, term), el('dd', null, String(value)));
  }

  function hide() {
    card.hidden = true;
    current = null;
  }

  function show(entity, { neighborhood = null, recent = [] } = {}) {
    current = entity;
    card.hidden = false;
    title.textContent = entity.title;
    chips.replaceChildren();
    facts.replaceChildren();

    if (entity.kind === 'building') {
      subtitle.textContent = entity.address || neighborhood?.name || '';
      chips.append(chip(CATEGORY_LABELS[entity.cat] || 'Building', CAT_TONE[entity.cat] || 'mustard', 'building'));
      if (entity.sub && entity.sub !== CATEGORY_LABELS[entity.cat]?.toLowerCase()) {
        chips.append(chip(humanize(entity.sub)));
      }
      if (entity.tier === 'A') chips.append(chip('Notable', 'coral'));
      fact('Floors', entity.floors);
      fact('Height', `${Math.round(entity.height)} m`);
      fact('Footprint', `${Math.round(entity.w * entity.d * 4)} m²`);
      if (neighborhood) fact('Neighbourhood', neighborhood.name);
    } else if (entity.kind === 'street') {
      subtitle.textContent = 'Street';
      chips.append(chip('Street', 'navy', 'street'));
      if (entity.nhood) fact('Neighbourhood', entity.nhood);
      if (entity.length) fact('Length in the city', `${(entity.length / 1000).toFixed(1)} km`);
    } else if (entity.kind === 'park') {
      subtitle.textContent = entity.type || 'Park';
      chips.append(chip('Park', 'forest', 'park'));
      if (entity.acres) fact('Area', `${entity.acres} acres`);
      if (neighborhood) fact('Neighbourhood', neighborhood.name);
    } else if (entity.kind === 'landmark') {
      subtitle.textContent = 'Landmark';
      chips.append(chip('Landmark', 'coral', 'landmark'));
      if (entity.height) fact('Height', `${Math.round(entity.height)} m`);
      if (neighborhood) fact('Neighbourhood', neighborhood.name);
    } else if (entity.kind === 'vessel') {
      subtitle.textContent = entity.routeName
        ? `San Francisco Bay Ferry · ${entity.routeName} route`
        : 'San Francisco Bay Ferry';
      chips.append(chip(entity.demo ? 'Demo vessel' : 'Live vessel', 'teal', 'vessel'));
      if (entity.routeName) chips.append(chip(entity.routeName, 'navy'));
      if (!entity.inService) chips.append(chip('Not in service', 'mustard'));
      fact('Vessel', entity.title);
      // A boat still boarding at its origin has a departure time in the future,
      // so the label follows the clock rather than assuming it has left.
      const left = entity.origin?.departedAt;
      const sailed = Number.isFinite(left) && left <= Date.now();
      fact(sailed ? 'Departed from' : 'Sailing from', entity.origin?.name || 'Not reported');
      fact(sailed ? 'Departed at' : 'Scheduled departure', when(left) || 'Scheduled time unavailable');
      const nextStop = entity.next?.name || entity.destination;
      fact('Next stop', nextStop || 'Not reported');
      fact('Arriving', when(entity.next?.arrivalAt) || 'Predicted time unavailable');
      if (entity.next?.scheduledArrivalAt && entity.next.scheduledArrivalAt !== entity.next.arrivalAt) {
        fact('Scheduled arrival', clock(entity.next.scheduledArrivalAt));
      }
      if (entity.destination && entity.destination !== nextStop) {
        fact('Final destination', entity.destination);
      }
      fact('Speed', `${entity.speedKn.toFixed(1)} kn`);
      fact('Position reported', relative(entity.recordedAt));
    } else if (entity.kind === 'transit') {
      subtitle.textContent = entity.routeName ? `Muni · ${entity.routeName}` : 'Muni';
      chips.append(chip(entity.demo ? 'Demo bus' : 'Live bus', 'teal', 'transit'));
      chips.append(chip(entity.route, 'coral'));
      if (entity.occupancy && OCCUPANCY_LABEL[entity.occupancy]) {
        chips.append(chip(OCCUPANCY_LABEL[entity.occupancy], 'mustard'));
      }
      fact('Bus', `${entity.fleetNumber} · New Flyer XDE40 hybrid`);
      fact('Headed to', entity.destination || 'Not reported');
      if (entity.stops?.length) {
        // The next stops with live ETAs, the way the rider-facing signs put it.
        for (const [i, stop] of entity.stops.entries()) {
          fact(i === 0 ? 'Next stop' : 'Then', `${stop.name} · ${when(stop.arrivalAt) || 'no prediction'}`);
        }
      } else {
        fact('Next stop', entity.degraded ? 'No predictions (degraded feed)' : 'No prediction');
      }
      fact('Speed', `${Math.round(entity.speedKmh)} km/h`);
      fact('Position reported', relative(entity.recordedAt));
    } else if (entity.kind === 'transit-stop') {
      subtitle.textContent = 'Muni bus stop';
      chips.append(chip('Bus stop', 'navy', 'transit'));
      for (const route of entity.routes.slice(0, 6)) chips.append(chip(route, 'coral'));
      if (entity.routes.length > 6) chips.append(chip(`+${entity.routes.length - 6}`, 'navy'));
      fact('Routes stopping here', entity.routes.join(' \u00b7 '));
      // Grouped by route, because "when is the next 38R" is the question a
      // rider is asking — a flat list of vehicles makes them do the grouping.
      if (entity.arrivals.length) {
        for (const group of entity.arrivals) {
          fact(group.route, group.minutes.map((m) => (m <= 0 ? 'now' : `${m} min`)).join(', '));
        }
      } else {
        fact('Coming soon', 'Nothing predicted in the next few minutes');
      }
    } else if (entity.kind === 'ferry-terminal') {
      subtitle.textContent = entity.operatorNames?.length
        ? entity.operatorNames.join(' \u00b7 ')
        : 'Ferry terminal';
      chips.append(chip('Ferry terminal', 'teal', 'vessel'));
      for (const route of entity.routes.slice(0, 6)) chips.append(chip(route.name, 'coral'));
      if (entity.routes.length > 6) chips.append(chip(`+${entity.routes.length - 6}`, 'navy'));
      if (entity.routes.length) {
        fact('Routes calling here', entity.routes.map((r) => r.name).join(' \u00b7 '));
      } else {
        // Pier 48 is the Chase Center / Oracle Park event dock and Pier 41 is
        // Blue & Gold's berth — a private operator 511 does not publish at all.
        // Both are real terminals with zero trips in the timetable, so the card
        // says so rather than leaving a pin that seems to have lost its routes.
        fact('Scheduled service', 'None in the published timetable');
        fact('Why', 'A real berth used for charters or event sailings, or served by an operator that does not publish a schedule to 511.');
      }
      if (entity.stops > 1) fact('Berths', `${entity.stops} gates or docks grouped here`);
      // Only WETA publishes live positions, so only its terminals can ever show
      // an inbound boat. Saying nothing would read as "no boats due".
      if (entity.vessels?.length) {
        for (const vessel of entity.vessels.slice(0, 4)) {
          const eta = vessel.arrivingAt
            ? `${Math.max(0, Math.round((vessel.arrivingAt - Date.now()) / 60000))} min`
            : 'departed from here';
          fact(vessel.routeName || vessel.label, eta);
        }
      } else if (entity.routes.length) {
        fact('Live vessels', 'None reporting on these routes right now');
      }
    } else if (entity.kind === 'aircraft') {
      // Every number here is the TRUE reading from the transponder. Only the
      // height the aircraft is DRAWN at is compressed (see aircraft.js dispY),
      // so the card is never the place that lies.
      // The route is the most glanceable fact there is, so it headlines when
      // known: "Airliner \u00b7 B739 \u00b7 SFO \u2192 PVR".
      const leg =
        entity.route && (entity.route.from?.iata || entity.route.to?.iata)
          ? `${entity.route.from?.iata || '?'} \u2192 ${entity.route.to?.iata || '?'}`
          : null;
      subtitle.textContent = [entity.name, entity.aircraftType, leg].filter(Boolean).join(' \u00b7 ');
      chips.append(chip(entity.demo ? 'Demo aircraft' : 'Live aircraft', 'teal', 'aircraft'));
      if (entity.phase) chips.append(chip(entity.phase, 'navy'));
      if (entity.emergency) chips.append(chip(entity.emergency, 'coral'));
      if (entity.military) chips.append(chip('Military', 'mustard'));
      if (entity.callsign) fact('Callsign', entity.callsign);
      if (entity.registration && entity.registration !== entity.callsign) {
        fact('Tail number', entity.registration);
      }
      if (entity.aircraftType) fact('Type', entity.aircraftType);
      // Origin and destination. ADS-B does not broadcast these — they are
      // looked up from the callsign, so a private flight legitimately has none
      // and says so rather than showing a blank row.
      if (entity.route) {
        const place = (node) =>
          node
            ? [node.city, node.iata ? `(${node.iata})` : null].filter(Boolean).join(' ') ||
              node.name ||
              'Not reported'
            : 'Not reported';
        fact('From', place(entity.route.from));
        fact('To', place(entity.route.to));
      } else if (entity.callsign && entity.callsign !== entity.registration) {
        fact('Route', 'Not published');
      }
      fact('Altitude', `${entity.altitudeFt.toLocaleString('en-US')} ft \u00b7 ${entity.altitudeM.toLocaleString('en-US')} m`);
      fact('Ground speed', `${entity.speedKt} kn \u00b7 ${Math.round(entity.speedKmh)} km/h`);
      // A vertical rate under ~500 fpm is noise on a barometric encoder, so it
      // is reported as level rather than as a spurious 40 fpm climb.
      const fpm = entity.verticalRateFpm;
      fact(
        'Vertical rate',
        Math.abs(fpm) < 500
          ? 'Level'
          : `${fpm > 0 ? 'Climbing' : 'Descending'} ${Math.abs(fpm).toLocaleString('en-US')} ft/min`
      );
      fact('Heading', `${entity.heading}\u00b0`);
      // Say plainly that the aircraft is drawn nearer than it is. The distance
      // is the real one; only the position on screen is compressed.
      if (entity.scaledPlacement) {
        fact(
          'Actually',
          `${entity.trueDistanceKm.toFixed(1)} km from the city \u00b7 drawn overhead to keep it in view`
        );
      }
      if (entity.squawk) fact('Squawk', entity.squawk);
      fact('Position reported', relative(entity.recordedAt));
    } else if (entity.kind === 'neighborhood') {
      subtitle.textContent = 'Analysis neighbourhood';
      chips.append(chip('Neighbourhood', 'plum', 'neighborhood'));
    } else {
      subtitle.textContent = 'Open water';
      chips.append(chip('Water', 'teal', 'water'));
    }

    // The concierge only knows the baked city, so it has nothing to say about a
    // boat that showed up in a live feed thirty seconds ago.
    // Aircraft DO get the ask button: unlike a ferry or a bus, the concierge
    // has the whole flights feed through live_data, and the clicked aircraft's
    // full state rides along in the focus context — so it can actually answer.
    askButton.hidden =
      entity.kind === 'vessel' || entity.kind === 'transit' || entity.kind === 'transit-stop';

    const bits = [`Source: ${sourceLabel(entity.source)}`];
    if (entity.kind === 'building') bits.push(confidenceLabel(entity.confidence));
    source.replaceChildren(document.createTextNode(bits.join(' · ')));
    if (entity.wikidata) {
      const link = el('a', null, ' Wikidata');
      link.href = `https://www.wikidata.org/wiki/${encodeURIComponent(entity.wikidata)}`;
      link.target = '_blank';
      link.rel = 'noopener noreferrer';
      source.append(document.createTextNode(' ·'), link);
    }

    history.replaceChildren();
    for (const item of recent) {
      if (item.id === entity.id) continue;
      const button = el('button', 'history-chip', item.title);
      button.type = 'button';
      button.addEventListener('click', () => onSelectHistory(item));
      history.append(button);
    }
  }

  return { show, hide, get entity() { return current; } };
}

export function createSearch({ onPick, onEmpty }) {
  const wrap = el('div');
  wrap.id = 'search';
  const box = el('div', 'toy-card');
  box.id = 'search-box';
  box.append(glyph('search'));
  const input = el('input');
  input.id = 'search-input';
  input.type = 'search';
  input.placeholder = 'Search buildings, streets, parks, neighbourhoods…';
  input.setAttribute('aria-label', 'Search the city');
  const hint = el('span', null, '/');
  hint.id = 'search-hint';
  box.append(input, hint);
  const results = el('div', 'toy-card');
  results.id = 'search-results';
  results.hidden = true;
  wrap.append(box, results);
  document.body.appendChild(wrap);

  let items = [];
  let active = -1;

  function render(list, query) {
    items = list;
    active = list.length ? 0 : -1;
    results.replaceChildren();
    results.hidden = false;
    if (!list.length) {
      const empty = el('button', 'result');
      empty.type = 'button';
      empty.append(glyph('chat'), el('strong', null, `Ask the concierge about “${query}”`));
      empty.addEventListener('click', () => {
        results.hidden = true;
        onEmpty(query);
      });
      results.append(empty);
      return;
    }
    list.forEach((entry, i) => {
      const button = el('button', 'result');
      button.type = 'button';
      button.setAttribute('aria-selected', String(i === 0));
      button.append(glyph(KIND_GLYPH[entry.t] || 'building'), el('strong', null, entry.n), el('span', null, entry.t));
      button.addEventListener('click', () => choose(i));
      results.append(button);
    });
  }

  function choose(index) {
    const entry = items[index];
    if (!entry) return;
    results.hidden = true;
    input.blur();
    onPick(entry);
  }

  function highlight(delta) {
    if (!items.length) return;
    active = (active + delta + items.length) % items.length;
    [...results.children].forEach((child, i) => child.setAttribute('aria-selected', String(i === active)));
    results.children[active]?.scrollIntoView({ block: 'nearest' });
  }

  input.addEventListener('keydown', (event) => {
    event.stopPropagation();
    if (event.key === 'ArrowDown') {
      highlight(1);
      event.preventDefault();
    } else if (event.key === 'ArrowUp') {
      highlight(-1);
      event.preventDefault();
    } else if (event.key === 'Enter') {
      if (items.length) choose(active < 0 ? 0 : active);
      else if (input.value.trim()) onEmpty(input.value.trim());
      event.preventDefault();
    } else if (event.key === 'Escape') {
      input.value = '';
      results.hidden = true;
      input.blur();
    }
  });
  input.addEventListener('keyup', (event) => event.stopPropagation());
  input.addEventListener('blur', () => setTimeout(() => (results.hidden = true), 160));

  return {
    input,
    render,
    focus() {
      input.focus();
      input.select();
    },
    close() {
      results.hidden = true;
    },
  };
}
