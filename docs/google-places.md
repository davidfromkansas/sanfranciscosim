# Google Places search

The search box and City Concierge can optionally use the
[Google Places API](https://developers.google.com/maps/documentation/places/web-service/overview)
to find businesses, venues, and misspelled place names that are not in the
local indexes.

Google Places is an optional fallback, not a requirement. The free DataSF
Enterprise Addressing System index remains the primary exact path for San
Francisco street addresses, and the app, tests, and build work without a
Google key. When no `GOOGLE_PLACES_KEY` is configured, place suggestions are
omitted and address search behaves normally.

Place requests run server-side, are restricted to San Francisco, cached for
recent identical queries, rate-limited per IP, and capped per warm instance
each UTC day. The app allows at most 250 autocomplete requests, 7 Text Search
requests, and 7 Place Details requests per warm instance per UTC day. That
autocomplete allowance is 7,500 requests over 30 days, comfortably below
Google's 10,000-request monthly free usage cap, so its expected exposure is
about $0. The 7 Text Search and 7 Place Details daily caps have a combined
30-day gross exposure of about $7.77 at Google's currently listed first-tier
rates ($32/1,000 Text Search Pro and $5/1,000 Place Details Essentials),
before their monthly free usage caps (5,000 and 10,000 requests,
respectively). Google aggregates usage across projects on the billing account,
so configure a hard per-API quota cap in the
[Google Cloud console](https://console.cloud.google.com/apis/api/places.googleapis.com/quotas)
as the authoritative backstop. The Autocomplete Requests rate is currently
$2.83/1,000 after its free cap. Place Details requests ask only for
`location,formattedAddress`, both Essentials-tier fields; `displayName` is a
Pro-tier field and is deliberately omitted.

The results come from Google's index and include Google attribution; they are
not a live business-status feed. Pricing source:
[Google Maps Platform pricing](https://developers.google.com/maps/billing-and-pricing/pricing).
