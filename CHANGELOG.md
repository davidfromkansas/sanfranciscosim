## 🗺️ Optional Google Places fallback
**Shipped:** August 22, 2026
**TL;DR:**
Search and the City Concierge can now find San Francisco businesses, venues,
and misspelled place names through the optional
[Google Places API](https://developers.google.com/maps/documentation/places/web-service/overview).

**What you'll see:**
DataSF remains the free, exact primary path for street addresses. When a local
address or city index result is not found, and `GOOGLE_PLACES_KEY` is
configured, Google-backed place suggestions can appear in the search box and
the Concierge can fly to a selected result. Without the key, the existing
keyless behavior is unchanged.

**How it works:**
Google requests stay server-side and are restricted to San Francisco. Results
come from Google's index, carry Google attribution, and are protected by
per-IP rate limits, recent-query caching, and a per-warm-instance daily budget
with a daily circuit-breaker latch.
