// San Francisco news, as the raw material for the subreddit's event posts.
//
// Fetch and parse only. What becomes a post, when, and who argues about it is
// residents.mjs's business — this module knows nothing about the subreddit.
//
// The outlet list and the parser are ported from the personas project's
// fetch-events.mjs, which had already done the work of finding fourteen SF
// newsrooms that publish usable RSS. No parser dependency: RSS is regular
// enough that a few regexes beat adding a package to a serverless bundle.

const SOURCES = [
  { url: "https://missionlocal.org/feed/", name: "Mission Local" },
  { url: "https://sfstandard.com/feed/", name: "The San Francisco Standard" },
  { url: "https://sfist.com/feed/", name: "SFist" },
  { url: "https://48hills.org/feed/", name: "48 Hills" },
  { url: "https://www.sfpublicpress.org/feed/", name: "SF Public Press" },
  { url: "https://eltecolote.org/content/en/feed/", name: "El Tecolote" },
  { url: "https://sfbayview.com/feed/", name: "SF Bay View" },
  { url: "https://sf.eater.com/rss/index.xml", name: "Eater SF" },
  { url: "https://www.richmondsunsetnews.com/feed/", name: "Richmond Review" },
  { url: "https://thefrisc.com/feed/", name: "The Frisc" },
  { url: "https://localnewsmatters.org/feed/", name: "Local News Matters" },
  { url: "https://www.sfgate.com/rss/feed/Bay-Area-News-429.php", name: "SFGate" },
  { url: "https://abc7news.com/feed/", name: "ABC7" },
  { url: "https://patch.com/feeds/california/san-francisco", name: "Patch SF" },
  // Neighbourhood press, added after probing two dozen candidates — most of
  // the city's small papers are dead, RSS-less, or behind bot walls. These
  // four are alive and parse. NOT added: sfrichmondreview.com, which is the
  // same paper as the Richmond Review above under a second domain (identical
  // items, different links — link-dedupe would post every story twice), and
  // Bernalwood / Richmond District Blog, which last published years ago.
  // The city-scoped path, NOT /rss/ — Hoodline went national and its main
  // feed is Denver and Orlando; every item was (correctly) rejected by the
  // relevance filter before this was caught.
  { url: "https://hoodline.com/news/san-francisco/rss", name: "Hoodline SF" },
  { url: "https://glenparkassociation.org/feed/", name: "Glen Park Association" },
  { url: "https://potreroview.net/feed/", name: "Potrero View" },
  // Monthly, so it clears the 48-hour freshness gate only just after an issue
  // lands — a story or two a month, from a neighbourhood nothing else covers.
  { url: "https://www.marinatimes.com/feed", name: "Marina Times" },
];

// Nothing older than this is worth posting as news.
const MAX_AGE_MS = 48 * 60 * 60 * 1000;
const PER_SOURCE = 6;

// Several of these outlets are regional or national — ABC7, SFGate and Patch
// carry Pasadena, Vallejo and the US Army alongside real San Francisco stories.
// The subreddit's own fifth rule forbids posts that are not about the city, so
// an item has to name something in it to get through.
//
// This is a RELEVANCE test, not a topic one: it does not care what the story is
// about, only where it happened. Dropping the offending outlets entirely would
// be simpler and would also throw away the SF reporting they do.
const SF_TERMS = [
  "san francisco", "sf ", " sf", "s.f.", "bay area",
  // agencies and institutions
  "muni", "sfmta", "bart", "caltrain", "sfpd", "sffd", "sfusd", "sfo",
  "board of supervisors", "city hall", "golden gate", "presidio", "alcatraz",
  "embarcadero", "market street", "van ness", "castro", "tenderloin",
  "chinatown", "north beach", "haight", "soma", "mission district",
  "fisherman's wharf", "union square", "nob hill", "russian hill",
  "pacific heights", "bayview", "hunters point", "excelsior", "ingleside",
  "potrero", "dogpatch", "sunset district", "richmond district", "noe valley",
  "bernal heights", "glen park", "twin peaks", "visitacion valley",
  "treasure island", "japantown", "hayes valley", "western addition",
  "outer sunset", "inner sunset", "outer richmond", "inner richmond",
  "oceanview", "portola", "lake merced", "west portal", "mission bay",
];

function aboutSF(item) {
  const hay = `${item.title} ${item.description}`.toLowerCase();
  return SF_TERMS.some((term) => hay.includes(term));
}

const clean = (s) =>
  s
    .replace(/<!\[CDATA\[|\]\]>/g, "")
    .replace(/<[^>]+>/g, " ")
    .replace(/&amp;/g, "&")
    .replace(/&#8217;|&rsquo;|&#039;|&apos;/g, "'")
    .replace(/&#8216;|&lsquo;/g, "'")
    .replace(/&#8220;|&ldquo;|&#8221;|&rdquo;|&quot;/g, '"')
    .replace(/&#8211;|&ndash;/g, "–")
    .replace(/&#8212;|&mdash;/g, "—")
    .replace(/&#\d+;/g, "")
    .replace(/\s+/g, " ")
    .trim();

// RSS and Atom in one pass — the outlets are split between them and the only
// real differences are the item element and where the link hides.
function parse(xml) {
  const atom = !/<item[\s>]/.test(xml) && /<entry[\s>]/.test(xml);
  const out = [];
  for (const block of xml.split(atom ? /<entry[\s>]/ : /<item[\s>]/).slice(1)) {
    const pick = (tag) => {
      const m = block.match(new RegExp(`<${tag}[^>]*>([\\s\\S]*?)</${tag}>`, "i"));
      return m ? clean(m[1]) : "";
    };
    let link = pick("link");
    if (!link) link = block.match(/<link[^>]*href="([^"]+)"/i)?.[1] ?? "";
    const title = pick("title");
    if (!title || !link) continue;
    out.push({
      title,
      link: link.split("?")[0], // strip tracking params so the same story is the same link
      description: pick("description") || pick("summary"),
      published: Date.parse(pick("pubDate") || pick("published") || "") || 0,
    });
  }
  return out;
}

// Everything the outlets are carrying right now, newest first. One slow or
// broken newsroom must not take the others down with it, so each is fetched
// independently and a failure just contributes nothing.
export async function fetchNews({ signal } = {}) {
  const now = Date.now();
  const results = await Promise.all(
    SOURCES.map(async (source) => {
      try {
        const res = await fetch(source.url, {
          headers: { "User-Agent": "sanfranciscosim/1.0 (+https://www.sfsim.net)" },
          redirect: "follow",
          signal,
        });
        if (!res.ok) return [];
        return parse(await res.text())
          .slice(0, PER_SOURCE)
          .map((item) => ({ ...item, source: source.name }));
      } catch {
        return [];
      }
    }),
  );
  return results
    .flat()
    .filter((i) => i.published && now - i.published < MAX_AGE_MS)
    .filter(aboutSF)
    .sort((a, b) => b.published - a.published);
}

export const newsSources = () => SOURCES.length;
