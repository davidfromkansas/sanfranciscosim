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
each UTC day. The results come from Google's index and include Google
attribution; they are not a live business-status feed.
