import assert from 'node:assert/strict';
import { describe, it } from 'node:test';

import { lookupAddress, normalizeStreetName, parseAddressQuery } from '../../api/_lib/addresses.mjs';

const shard = {
  streets: {
    'anza st': { name: 'ANZA ST', n: [1700, 1726, 1740], x: [1, 2, 3], z: [4, 5, 6] },
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
});
