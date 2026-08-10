// GET /api/ferries — real San Francisco Bay Ferry (WETA) vessel positions.
//
// Thin normaliser over 511.org's SIRI VehicleMonitoring feed for agency SB.
// Without FERRY_511_KEY it answers 200 with { live: false } and the client keeps
// its procedural ferries: the city never requires a key. 511 allows 60 requests
// an hour, so a warm instance memoises upstream for 55 s, the CDN caches for
// 60 s, and an upstream failure serves the last good fix (marked stale) and
// backs off for five minutes.

const UPSTREAM = 'https://api.511.org/transit/VehicleMonitoring';
const AGENCY = 'SB'; // SB = SF Bay Ferry / WETA (SF is Muni, GF is Golden Gate).
const MEMO_MS = 55 * 1000;
const STALE_MS = 10 * 60 * 1000;
const BACKOFF_MS = 5 * 60 * 1000;
const TIMEOUT_MS = 10 * 1000;

// Module scope survives across invocations on a warm instance.
let memo = null; // { fetchedAt, vessels }
let backoffUntil = 0;

function asArray(value) {
  if (value == null) return [];
  return Array.isArray(value) ? value : [value];
}

function normalise(payload, now) {
  const deliveries = asArray(payload?.Siri?.ServiceDelivery?.VehicleMonitoringDelivery);
  const vessels = [];
  for (const delivery of deliveries) {
    for (const activity of asArray(delivery?.VehicleActivity)) {
      const journey = activity?.MonitoredVehicleJourney;
      const location = journey?.VehicleLocation;
      if (!journey || !location) continue;
      const lat = Number(location.Latitude);
      const lon = Number(location.Longitude);
      if (!Number.isFinite(lat) || !Number.isFinite(lon) || (lat === 0 && lon === 0)) continue;

      const recordedAt = Date.parse(activity.RecordedAtTime);
      if (Number.isFinite(recordedAt) && now - recordedAt > STALE_MS) continue;

      const bearing = Number(journey.Bearing);
      const ref = journey.VehicleRef == null ? null : String(journey.VehicleRef);
      if (!ref) continue;

      vessels.push({
        id: `${AGENCY}:${ref}`,
        label: ref,
        lat,
        lon,
        // A missing bearing must stay missing: 0 would point every docked boat north.
        bearingDeg: Number.isFinite(bearing) ? bearing : null,
        routeName: journey.PublishedLineName || journey.LineRef || null,
        destination: journey.DestinationName || null,
        inService: journey.LineRef != null,
        recordedAt: Number.isFinite(recordedAt) ? recordedAt : null,
      });
    }
  }
  return vessels;
}

function serveMemo(res, now, reason) {
  if (memo && now - memo.fetchedAt <= STALE_MS) {
    return res.status(200).json({
      live: true,
      stale: true,
      reason,
      fetchedAt: memo.fetchedAt,
      vessels: memo.vessels,
    });
  }
  return res.status(200).json({ live: false, reason, vessels: [] });
}

export default async function handler(req, res) {
  if (req.method && req.method !== 'GET') {
    res.status(405).json({ error: 'method not allowed' });
    return;
  }

  res.setHeader('Cache-Control', 's-maxage=60, stale-while-revalidate=300');

  const key = (process.env.FERRY_511_KEY || '').trim();
  if (!key) {
    res.status(200).json({ live: false, reason: 'no-key', vessels: [] });
    return;
  }

  const now = Date.now();
  if (memo && now - memo.fetchedAt < MEMO_MS) {
    res.status(200).json({ live: true, fetchedAt: memo.fetchedAt, vessels: memo.vessels });
    return;
  }
  if (now < backoffUntil) {
    serveMemo(res, now, 'backoff');
    return;
  }

  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), TIMEOUT_MS);
  try {
    const url = `${UPSTREAM}?api_key=${encodeURIComponent(key)}&agency=${AGENCY}&format=json`;
    const upstream = await fetch(url, { signal: controller.signal });
    if (upstream.status === 429 || upstream.status >= 500) {
      backoffUntil = now + BACKOFF_MS;
      serveMemo(res, now, `upstream-${upstream.status}`);
      return;
    }
    if (!upstream.ok) {
      serveMemo(res, now, `upstream-${upstream.status}`);
      return;
    }
    // 511 serves this feed as UTF-8 with a BOM, which JSON.parse rejects.
    const text = await upstream.text();
    const payload = JSON.parse(text.replace(/^\uFEFF/, ''));
    const vessels = normalise(payload, now);
    memo = { fetchedAt: now, vessels };
    res.status(200).json({ live: true, fetchedAt: now, vessels });
  } catch (error) {
    backoffUntil = now + BACKOFF_MS;
    serveMemo(res, now, error.name === 'AbortError' ? 'timeout' : 'upstream');
  } finally {
    clearTimeout(timer);
  }
}
