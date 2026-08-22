import assert from 'node:assert/strict';
import { describe, it } from 'node:test';

import { lookupAddress, normalizeStreetName, parseAddressQuery } from '../../api/_lib/addresses.mjs';

const shard = {
  streets: {
    'anza st': { name: 'ANZA ST', n: [1700, 1726, 1740], x: [1, 2, 3], z: [4, 5, 6] },
    'anza ave': { name: 'ANZA AVE', n: [100], x: [7], z: [8] },
    'anzavista ave': { name: 'ANZAVISTA AVE', n: [100], x: [9], z: [10] },
    'n point ave': { name: 'N POINT AVE', n: [100, 102, 121], x: [10, 11, 12], z: [20, 21, 22] },
  },
};

describe('address normalization and parsing', () => {
  it('parses a normal street address', () => {
    assert.deepEqual(parseAddressQuery('1726 Anza Street'), {
      number: 1726,
      streetKey: 'anza st',
      label: '1726 ANZA ST',
    });
  });

  it('strips unit suffixes and normalizes punctuation/location', () => {
    assert.deepEqual(parseAddressQuery('1726 anza st #3'), parseAddressQuery('1726 Anza St, San Francisco, CA 94118'));
  });

  it('rejects street-only queries', () => {
    assert.equal(parseAddressQuery('Anza Street'), null);
  });

  it('normalizes ordinals and directional prefixes', () => {
    assert.equal(normalizeStreetName('Third Street'), '3rd st');
    assert.equal(parseAddressQuery('2200 Third Street').streetKey, parseAddressQuery('2200 3rd St').streetKey);
    assert.equal(normalizeStreetName('03rd Street'), '3rd st');
    assert.equal(normalizeStreetName('North Point Avenue'), 'n point ave');
  });
});

describe('address lookup', () => {
  it('returns an exact hit by binary search', () => {
    const hit = lookupAddress(shard, parseAddressQuery('1726 Anza Street'));
    assert.deepEqual(hit, { x: 2, z: 5, exact: true, matchedNumber: 1726, street: 'ANZA ST' });
  });

  it('falls back within twenty house numbers and prefers matching parity', () => {
    const hit = lookupAddress(shard, { number: 111, streetKey: 'n point ave' });
    assert.deepEqual(hit, { x: 12, z: 22, exact: false, matchedNumber: 121, street: 'N POINT AVE' });
    assert.equal(lookupAddress(shard, { number: 150, streetKey: 'n point ave' }), null);
  });

  it('accepts a unique street prefix but rejects an ambiguous one', () => {
    assert.equal(lookupAddress(shard, parseAddressQuery('1726 Anza')).street, 'ANZA ST');
    const ambiguous = {
      streets: {
        'n point ave': { name: 'N POINT AVE', n: [100], x: [1], z: [2] },
        'n point park': { name: 'N POINT PARK', n: [100], x: [3], z: [4] },
      },
    };
    assert.equal(lookupAddress(ambiguous, { number: 100, streetKey: 'n point' }), null);
    assert.equal(lookupAddress(shard, parseAddressQuery('1726 Anza Str')).street, 'ANZA ST');
  });

  it('accepts a nearest number exactly twenty away but not twenty-one', () => {
    assert.equal(lookupAddress(shard, { number: 141, streetKey: 'n point ave' }).matchedNumber, 121);
    assert.equal(lookupAddress(shard, { number: 142, streetKey: 'n point ave' }), null);
  });

  it('uses same-parity numbers even when the opposite side is closer', () => {
    const parityShard = {
      streets: {
        '3rd st': {
          name: '3RD ST',
          n: [2191, 2202],
          x: [1, 2],
          z: [3, 4],
        },
      },
    };
    assert.equal(lookupAddress(parityShard, parseAddressQuery('2200 3rd St')).matchedNumber, 2202);
  });
});
