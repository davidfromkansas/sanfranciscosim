// Shared address parsing and lookup. The bake and browser use the same
// normalization rules so human street names resolve to DataSF street keys.

const STREET_TYPES = {
  street: 'st',
  avenue: 'ave',
  boulevard: 'blvd',
  drive: 'dr',
  court: 'ct',
  terrace: 'ter',
  place: 'pl',
  lane: 'ln',
  road: 'rd',
  highway: 'hwy',
  circle: 'cir',
  alley: 'aly',
  plaza: 'plz',
  stairway: 'stwy',
  hill: 'hl',
  crossing: 'xing',
  tunnel: 'tunl',
  passage: 'psge',
};

const DIRECTIONS = { north: 'n', south: 's', east: 'e', west: 'w' };
const ONES = ['zero', 'first', 'second', 'third', 'fourth', 'fifth', 'sixth', 'seventh', 'eighth', 'ninth'];
const TEENS = ['tenth', 'eleventh', 'twelfth', 'thirteenth', 'fourteenth', 'fifteenth', 'sixteenth', 'seventeenth', 'eighteenth', 'nineteenth'];
const TENS = { 20: 'twentieth', 30: 'thirtieth', 40: 'fortieth' };
const TENS_CARDINAL = { 20: 'twenty', 30: 'thirty', 40: 'forty' };
const ORDINAL_SUFFIX = (n) => (n % 100 >= 11 && n % 100 <= 13 ? 'th' : ({ 1: 'st', 2: 'nd', 3: 'rd' }[n % 10] || 'th'));

const ORDINALS = new Map();
for (let n = 1; n <= 48; n++) {
  if (n < 10) ORDINALS.set(ONES[n], `${n}${ORDINAL_SUFFIX(n)}`);
  else if (n < 20) ORDINALS.set(TEENS[n - 10], `${n}${ORDINAL_SUFFIX(n)}`);
  else if (n % 10 === 0) ORDINALS.set(TENS[n], `${n}${ORDINAL_SUFFIX(n)}`);
  else ORDINALS.set(`${TENS_CARDINAL[Math.floor(n / 10) * 10]}-${ONES[n % 10]}`, `${n}${ORDINAL_SUFFIX(n)}`);
}

function ordinalize(words) {
  for (let i = 0; i < words.length; i++) {
    const pair = `${words[i]}-${words[i + 1]}`;
    if (ORDINALS.has(pair)) {
      words.splice(i, 2, ORDINALS.get(pair));
      i--;
    } else if (ORDINALS.has(words[i])) {
      words[i] = ORDINALS.get(words[i]);
    } else {
      const numeric = words[i].match(/^0*(\d{1,2})(?:st|nd|rd|th)$/);
      const number = numeric && Number(numeric[1]);
      if (number >= 1 && number <= 48) words[i] = `${number}${ORDINAL_SUFFIX(number)}`;
    }
  }
  return words;
}

export function normalizeStreetName(value) {
  let text = String(value ?? '').toLowerCase().trim();
  if (!text) return '';
  text = text
    .replace(/\b(?:apt|apartment|unit|ste|suite)\s*[a-z0-9-]+\b/gi, ' ')
    .replace(/#[a-z0-9-]+/gi, ' ')
    .replace(/\b\d{5}(?:-\d{4})?\s*$/, ' ')
    .replace(/,\s*(?:san\s+francisco|sf)(?:\s*,\s*ca)?\s*$/i, ' ')
    .replace(/,\s*ca(?:lifornia)?\s*$/i, ' ')
    .replace(/[^\p{L}\p{N}]+/gu, ' ')
    .replace(/\s+/g, ' ')
    .trim();
  if (!text) return '';
  const words = ordinalize(text.split(' '));
  if (words.length && STREET_TYPES[words.at(-1)]) words[words.length - 1] = STREET_TYPES[words.at(-1)];
  if (words.length && DIRECTIONS[words[0]]) words[0] = DIRECTIONS[words[0]];
  return words.join(' ');
}

export function parseAddressQuery(query) {
  const match = String(query ?? '').trim().match(/^(\d{1,6})\s*[a-z]?\s+(.+)$/i);
  if (!match) return null;
  const number = Number(match[1]);
  const streetKey = normalizeStreetName(match[2]);
  if (!streetKey || !Number.isSafeInteger(number)) return null;
  return { number, streetKey, label: `${number} ${streetKey.toUpperCase()}` };
}

function compareNumber(a, b) {
  return a - b;
}

export function lookupAddress(shard, { number, streetKey } = {}) {
  const street = shard?.streets?.[streetKey];
  if (!street || !Number.isFinite(number)) return null;
  const numbers = street.n || [];
  if (!numbers.length) return null;
  let lo = 0;
  let hi = numbers.length - 1;
  while (lo <= hi) {
    const mid = (lo + hi) >> 1;
    if (numbers[mid] === number) {
      return { x: street.x[mid], z: street.z[mid], exact: true, matchedNumber: numbers[mid], street: street.name };
    }
    if (numbers[mid] < number) lo = mid + 1;
    else hi = mid - 1;
  }
  const candidates = [];
  for (const index of [hi, lo]) {
    if (index < 0 || index >= numbers.length) continue;
    const delta = Math.abs(numbers[index] - number);
    if (delta <= 20) candidates.push(index);
  }
  if (!candidates.length) return null;
  candidates.sort((a, b) => {
    const parity = (numbers[a] & 1) === (number & 1) ? 0 : 1;
    const otherParity = (numbers[b] & 1) === (number & 1) ? 0 : 1;
    return parity - otherParity || Math.abs(numbers[a] - number) - Math.abs(numbers[b] - number) || compareNumber(numbers[a], numbers[b]);
  });
  const index = candidates[0];
  return { x: street.x[index], z: street.z[index], exact: false, matchedNumber: numbers[index], street: street.name };
}
