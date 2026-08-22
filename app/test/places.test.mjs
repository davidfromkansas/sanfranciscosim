import assert from 'node:assert/strict';
import { afterEach, describe, it } from 'node:test';

import {
  autocomplete,
  findPlace,
  placesStatus,
  resetPlacesForTests,
  resolvePlace,
  SF_RECTANGLE,
} from '../../api/_lib/places.mjs';

const originalFetch = globalThis.fetch;
const originalKey = process.env.GOOGLE_PLACES_KEY;

afterEach(() => {
  globalThis.fetch = originalFetch;
  if (originalKey === undefined) delete process.env.GOOGLE_PLACES_KEY;
  else process.env.GOOGLE_PLACES_KEY = originalKey;
  resetPlacesForTests();
});

function response(body, status = 200) {
  return {
    ok: status >= 200 && status < 300,
    status,
    async json() {
      return body;
    },
  };
}

describe('Google Places access', () => {
  it('degrades cleanly when no key is configured', async () => {
    delete process.env.GOOGLE_PLACES_KEY;
    assert.deepEqual(await autocomplete({ input: 'coffee' }), {
      error: 'place search is not configured',
    });
    assert.deepEqual(await findPlace({ query: 'coffee' }), {
      error: 'place search is not configured',
    });
    assert.deepEqual(await resolvePlace({ query: 'coffee' }), {
      error: 'place search is not configured',
    });
  });

  it('builds an SF-restricted autocomplete request and normalizes predictions', async () => {
    process.env.GOOGLE_PLACES_KEY = 'test-key';
    let request;
    globalThis.fetch = async (url, options) => {
      request = { url, options, body: JSON.parse(options.body) };
      return response({
        suggestions: [
          {
            placePrediction: {
              place: 'places/abc',
              text: { text: 'The Coffee Shop, San Francisco, CA' },
              structuredFormat: {
                mainText: { text: 'The Coffee Shop' },
                secondaryText: { text: 'San Francisco, CA' },
              },
            },
          },
        ],
      });
    };
    assert.deepEqual(await autocomplete({ input: 'coffee' }), {
      predictions: [
        {
          placeId: 'abc',
          text: 'The Coffee Shop, San Francisco, CA',
          mainText: 'The Coffee Shop',
          secondaryText: 'San Francisco, CA',
        },
      ],
    });
    assert.equal(request.url, 'https://places.googleapis.com/v1/places:autocomplete');
    assert.equal(request.options.headers['X-Goog-Api-Key'], 'test-key');
    assert.equal(
      request.options.headers['X-Goog-FieldMask'],
      'suggestions.placePrediction.place,suggestions.placePrediction.text,suggestions.placePrediction.structuredFormat',
    );
    assert.deepEqual(request.body.includedRegionCodes, ['us']);
    assert.deepEqual(request.body.locationRestriction.rectangle, SF_RECTANGLE);
  });

  it('builds a capped text-search request and normalizes its first result', async () => {
    process.env.GOOGLE_PLACES_KEY = 'test-key';
    const requests = [];
    globalThis.fetch = async (url, options) => {
      requests.push({ url, options, body: JSON.parse(options.body) });
      return response({
        places: [
          {
            displayName: { text: 'A Place' },
            formattedAddress: '1 Market St, San Francisco, CA',
            location: { latitude: 37.79, longitude: -122.4 },
            types: ['cafe', 'food'],
            businessStatus: 'OPERATIONAL',
          },
        ],
      });
    };
    assert.deepEqual(await findPlace({ query: 'a place' }), {
      query: 'a place',
      results: [{
        name: 'A Place',
        address: '1 Market St, San Francisco, CA',
        lat: 37.79,
        lon: -122.4,
        types: ['cafe', 'food'],
        status: 'operational',
      }],
    });
    assert.equal(requests[0].url, 'https://places.googleapis.com/v1/places:searchText');
    assert.equal(requests[0].body.maxResultCount, 5);
    assert.deepEqual(requests[0].body.locationRestriction.rectangle, SF_RECTANGLE);
    assert.equal(
      requests[0].options.headers['X-Goog-FieldMask'],
      'places.displayName,places.formattedAddress,places.location,places.types,places.businessStatus',
    );
  });

  it('resolves a selected place by id through Essentials Place Details fields', async () => {
    process.env.GOOGLE_PLACES_KEY = 'test-key';
    let request;
    globalThis.fetch = async (url, options) => {
      request = { url, options };
      return response({
        formattedAddress: '580 19th St, San Francisco, CA',
        location: { latitude: 37.79, longitude: -122.4 },
      });
    };
    assert.deepEqual(await resolvePlace({
      query: 'The Ferry Building, San Francisco, CA',
      placeId: 'places/ferry_123',
    }), {
      query: 'The Ferry Building, San Francisco, CA',
      place: {
        name: 'The Ferry Building, San Francisco, CA',
        address: '580 19th St, San Francisco, CA',
        lat: 37.79,
        lon: -122.4,
        types: [],
        status: null,
      },
    });
    assert.equal(request.url, 'https://places.googleapis.com/v1/places/ferry_123');
    assert.equal(request.options.method, 'GET');
    assert.equal(request.options.headers['X-Goog-FieldMask'], 'location,formattedAddress');
    assert.equal('body' in request.options, false);
  });

  it('falls back to text search when no place id is supplied', async () => {
    process.env.GOOGLE_PLACES_KEY = 'test-key';
    const requests = [];
    globalThis.fetch = async (url, options) => {
      requests.push({ url, options });
      return response({
        places: [{
          displayName: { text: 'A Place' },
          location: { latitude: 37.79, longitude: -122.4 },
        }],
      });
    };
    const result = await resolvePlace({ query: 'a place' });
    assert.equal(result.place.name, 'A Place');
    assert.equal(requests.length, 1);
    assert.equal(requests[0].url, 'https://places.googleapis.com/v1/places:searchText');
  });

  it('caches identical recent queries', async () => {
    process.env.GOOGLE_PLACES_KEY = 'test-key';
    let calls = 0;
    globalThis.fetch = async () => {
      calls += 1;
      return response({ places: [] });
    };
    await findPlace({ query: 'same place' });
    await findPlace({ query: '  same   place ' });
    assert.equal(calls, 1);
  });

  it('splits daily caps by API and latches after a quota response', async () => {
    process.env.GOOGLE_PLACES_KEY = 'test-key';
    let calls = 0;
    globalThis.fetch = async (url) => {
      calls += 1;
      return url.endsWith('autocomplete')
        ? response({ suggestions: [] })
        : response({ places: [] });
    };
    for (let i = 0; i < 250; i++) await autocomplete({ input: `query ${i}` });
    assert.deepEqual(await autocomplete({ input: 'query over cap' }), {
      error: 'place search is over its daily budget — try again tomorrow',
    });
    assert.equal(calls, 250);
    assert.deepEqual(await findPlace({ query: 'still available' }), {
      query: 'still available',
      results: [],
    });
    assert.equal(calls, 251);
    for (let i = 0; i < 6; i++) await findPlace({ query: `search ${i}` });
    assert.deepEqual(await findPlace({ query: 'search over cap' }), {
      error: 'place search is over its daily budget — try again tomorrow',
    });
    assert.equal(calls, 257);

    resetPlacesForTests();
    calls = 0;
    globalThis.fetch = async () => {
      calls += 1;
      return response({}, 429);
    };
    assert.deepEqual(await findPlace({ query: 'quota' }), {
      error: 'place search is over its daily budget — try again tomorrow',
    });
    assert.deepEqual(await findPlace({ query: 'another query' }), {
      error: 'place search is over its daily budget — try again tomorrow',
    });
    assert.equal(calls, 1);
  });

  it('maps module errors to endpoint status codes', () => {
    assert.equal(placesStatus({}), 200);
    assert.equal(placesStatus({ error: 'place input is required' }), 400);
    assert.equal(placesStatus({ error: 'place query is required' }), 400);
    assert.equal(placesStatus({ error: 'place id is invalid' }), 400);
    assert.equal(placesStatus({ error: 'place search is over its daily budget — try again tomorrow' }), 429);
    assert.equal(placesStatus({ error: 'place search is not configured' }), 503);
    assert.equal(placesStatus({ error: 'place search unavailable right now' }), 503);
  });
});
