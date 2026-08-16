// Every live feed registers itself on import — one line per feed, in the order
// they joined the city. The dispatcher (api/[...path].mjs) imports this file
// once; adding a feed here is step 3 of the recipe in feedcore.mjs.

import './ferries.mjs';
import './muni.mjs';
import './weather.mjs';
import './satfog.mjs';
import './flights.mjs';
