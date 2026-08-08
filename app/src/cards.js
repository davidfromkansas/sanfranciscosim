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
};

const KIND_GLYPH = {
  building: 'building',
  park: 'park',
  street: 'street',
  landmark: 'landmark',
  neighborhood: 'neighborhood',
  water: 'water',
  view: 'view',
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

function chip(text, tone, glyphName) {
  const node = el('span', 'chip', text);
  if (tone) node.dataset.tone = tone;
  if (glyphName) node.prepend(glyph(glyphName));
  return node;
}

export function createContextCard({ onFly, onAsk, onSelectHistory }) {
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
  close.addEventListener('click', () => hide());
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
    } else if (entity.kind === 'neighborhood') {
      subtitle.textContent = 'Analysis neighbourhood';
      chips.append(chip('Neighbourhood', 'plum', 'neighborhood'));
    } else {
      subtitle.textContent = 'Open water';
      chips.append(chip('Water', 'teal', 'water'));
    }

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
