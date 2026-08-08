// District material palettes. Buildings are assigned the nearest district
// anchor (a coarse Voronoi over the city), and the runtime shader varies tone
// per building from the baked seed so no two neighbours read identically.

export const PALETTE = [
  { id: 'glass', color: [0.42, 0.5, 0.58], windows: 0.95 }, // downtown curtain wall
  { id: 'brick', color: [0.55, 0.36, 0.29], windows: 0.55 }, // SoMa / Mission masonry
  { id: 'pastel', color: [0.78, 0.74, 0.66], windows: 0.4 }, // Sunset / Richmond stucco rows
  { id: 'cream', color: [0.85, 0.82, 0.74], windows: 0.45 }, // Russian / Nob / Marina
  { id: 'victorian', color: [0.72, 0.66, 0.72], windows: 0.45 }, // Haight / Alamo / Castro
  { id: 'industrial', color: [0.5, 0.5, 0.48], windows: 0.3 }, // Bayview / Hunters Point
  { id: 'stone', color: [0.68, 0.66, 0.6], windows: 0.5 }, // civic center
  { id: 'presidio', color: [0.6, 0.44, 0.36], windows: 0.35 }, // Presidio red brick
];

const P = Object.fromEntries(PALETTE.map((p, i) => [p.id, i]));

export const DISTRICTS = [
  { name: 'Financial District', lon: -122.4008, lat: 37.7935, palette: P.glass },
  { name: 'SoMa', lon: -122.4022, lat: 37.7785, palette: P.brick },
  { name: 'Mission Bay', lon: -122.3925, lat: 37.7706, palette: P.glass },
  { name: 'Mission', lon: -122.4194, lat: 37.7599, palette: P.brick },
  { name: 'Potrero Hill', lon: -122.399, lat: 37.7576, palette: P.industrial },
  { name: 'Bayview', lon: -122.39, lat: 37.7299, palette: P.industrial },
  { name: 'Hunters Point', lon: -122.3739, lat: 37.7259, palette: P.industrial },
  { name: 'Excelsior', lon: -122.4266, lat: 37.7241, palette: P.pastel },
  { name: 'Sunset', lon: -122.4949, lat: 37.7522, palette: P.pastel },
  { name: 'Parkside', lon: -122.4863, lat: 37.7367, palette: P.pastel },
  { name: 'Richmond', lon: -122.4826, lat: 37.7802, palette: P.pastel },
  { name: 'Sunset Heights', lon: -122.4675, lat: 37.7539, palette: P.pastel },
  { name: 'Haight-Ashbury', lon: -122.4463, lat: 37.7692, palette: P.victorian },
  { name: 'Castro', lon: -122.435, lat: 37.7609, palette: P.victorian },
  { name: 'Western Addition', lon: -122.4326, lat: 37.7797, palette: P.victorian },
  { name: 'Civic Center', lon: -122.4181, lat: 37.7799, palette: P.stone },
  { name: 'Nob Hill', lon: -122.4149, lat: 37.7931, palette: P.cream },
  { name: 'Russian Hill', lon: -122.4184, lat: 37.8014, palette: P.cream },
  { name: 'North Beach', lon: -122.4098, lat: 37.8003, palette: P.cream },
  { name: 'Marina', lon: -122.4364, lat: 37.8021, palette: P.cream },
  { name: 'Pacific Heights', lon: -122.4356, lat: 37.7925, palette: P.cream },
  { name: 'Presidio', lon: -122.4662, lat: 37.7989, palette: P.presidio },
  { name: 'Treasure Island', lon: -122.3705, lat: 37.8235, palette: P.industrial },
  { name: 'Visitacion Valley', lon: -122.4053, lat: 37.7137, palette: P.pastel },
  { name: 'Twin Peaks', lon: -122.4477, lat: 37.7544, palette: P.cream },
  { name: 'Ingleside', lon: -122.4655, lat: 37.7222, palette: P.pastel },
];

// Nearest-anchor lookup in projected meters.
export function makeDistrictLookup(project) {
  const anchors = DISTRICTS.map((d) => {
    const [x, z] = project(d.lon, d.lat);
    return { x, z, palette: d.palette, name: d.name };
  });
  return function paletteAt(x, z) {
    let best = 0;
    let bestD = Infinity;
    for (let i = 0; i < anchors.length; i++) {
      const dx = anchors[i].x - x;
      const dz = anchors[i].z - z;
      const d = dx * dx + dz * dz;
      if (d < bestD) {
        bestD = d;
        best = anchors[i].palette;
      }
    }
    return best;
  };
}
