// Toy-diorama palettes and street classes. Shared by the toy bake and, through
// manifest.json, by the runtime: the toy tier's palette indices mean nothing
// without this table.

const hex = (h) => [
  parseInt(h.slice(1, 3), 16) / 255,
  parseInt(h.slice(3, 5), 16) / 255,
  parseInt(h.slice(5, 7), 16) / 255,
];

// Index layout is part of the binary contract: the bake writes these indices
// into every toy building record.
export const TOY_PALETTE = [
  { id: 'warm-white', color: hex('#f2ede3') }, // 0
  { id: 'cream', color: hex('#ece4d4') }, // 1
  { id: 'light-grey', color: hex('#e6e6e2') }, // 2
  { id: 'pale-sand', color: hex('#f5f0e8') }, // 3
  { id: 'teal', color: hex('#3fa8a0') }, // 4
  { id: 'coral', color: hex('#e8735a') }, // 5
  { id: 'mustard', color: hex('#d9a441') }, // 6
  { id: 'mint', color: hex('#8fd0a8') }, // 7
  { id: 'sky-blue', color: hex('#6db3d9') }, // 8
  { id: 'tower-glass', color: hex('#c3cdd6') }, // 9
  { id: 'roof-brick', color: hex('#b5533c') }, // 10
  { id: 'roof-slate', color: hex('#5a6672') }, // 11
  { id: 'roof-forest', color: hex('#4a6b50') }, // 12
  { id: 'roof-charcoal', color: hex('#45454a') }, // 13
  { id: 'hvac-grey', color: hex('#9a9a9e') }, // 14
  { id: 'garden-green', color: hex('#4e8f4a') }, // 15
  { id: 'solar-blue', color: hex('#2a3f66') }, // 16
  { id: 'helipad-grey', color: hex('#d0d0cc') }, // 17
];

export const TOY_BASE = [0, 1, 2, 3];
export const TOY_ACCENT = [4, 5, 6, 7, 8];
export const TOY_TOWER_GLASS = 9;
export const TOY_ROOFS = [10, 11, 12, 13];
export const TOY_HVAC = 14;
export const TOY_GARDEN = 15;
export const TOY_SOLAR = 16;
export const TOY_HELIPAD = 17;

// Record flags in the version 2 building blob.
export const TOY_FLAG_PITCHED = 1;
export const TOY_FLAG_GARNISH = 2;

export const TOY_FLOOR = 3.5;
export const TOY_ROOF_RISE = 2.5;

// Toy streets: the base widths and lane data, restyled charcoal, plus the
// streetscape ribbon classes the bake emits alongside every road — raised
// sidewalk plinths, centre dashes and crosswalk zebras.
//
// Geometry the classes imply, and which the runtime reads back out of
// manifest.json rather than hardcoding:
//   `sidewalk` on a road class — that class carries kerbed sidewalks: which
//     ribbon class they are baked as, how wide, and how high the kerb is (the
//     runtime also uses `curb` to stand pedestrians on the plinth top).
//   `dash` on a road class — the ribbon class its centre dashes are baked as.
//   `dash` on a ribbon class — the dash/gap rhythm in metres. The bake emits
//     one trimmed centreline per road and the ribbon builder chops it, which
//     costs one polyline instead of one per dash.
//   `lift` on a ribbon class — how far above the road surface it sits. Too
//     small to survive the blob's decimetre y quantisation, so it is applied at
//     ribbon-build time.
//   `profile: 'curb'` — build an L-section (top strip plus kerb faces), not a
//     flat strip.
//   `detail: true` — near tier only; the far tier keeps plain charcoal.
export const TOY_CURB_H = 0.35;
export const TOY_SIDEWALK_W = 3;
export const TOY_SIDEWALK_W_WIDE = 4; // major/arterial
export const TOY_MARK_LIFT = 0.03; // must stay under agents.js CAR_LIFT (0.2)
export const TOY_DASH_W = 0.5;
export const TOY_ZEBRA_W = 0.8;

const SIDEWALK_IDS = new Set(['major', 'arterial', 'collector', 'residential']);
const WIDE_SIDEWALK_IDS = new Set(['major', 'arterial']);
const DASH_IDS = new Set(['freeway', 'major', 'arterial', 'collector', 'residential']);
const BIG_DASH_IDS = new Set(['freeway', 'major']);

export function toyStreetClasses(base) {
  const road = base.map((c) => ({
    ...c,
    color: hex('#3c3c40'),
    ...(SIDEWALK_IDS.has(c.id)
      ? {
          sidewalk: {
            ribbon: WIDE_SIDEWALK_IDS.has(c.id) ? 'sidewalk_wide' : 'sidewalk',
            width: WIDE_SIDEWALK_IDS.has(c.id) ? TOY_SIDEWALK_W_WIDE : TOY_SIDEWALK_W,
            curb: TOY_CURB_H,
          },
        }
      : null),
    ...(DASH_IDS.has(c.id) ? { dash: BIG_DASH_IDS.has(c.id) ? 'dash_major' : 'dash' } : null),
  }));
  const stone = hex('#d9d2c2');
  const paint = hex('#f0ece0');
  road.push({
    id: 'sidewalk',
    width: TOY_SIDEWALK_W,
    color: stone,
    lanes: 0,
    speed: 0,
    profile: 'curb',
    lift: TOY_CURB_H,
  });
  road.push({
    id: 'sidewalk_wide',
    width: TOY_SIDEWALK_W_WIDE,
    color: stone,
    lanes: 0,
    speed: 0,
    profile: 'curb',
    lift: TOY_CURB_H,
  });
  road.push({
    id: 'dash',
    width: TOY_DASH_W,
    color: paint,
    lanes: 0,
    speed: 0,
    lift: TOY_MARK_LIFT,
    detail: true,
    dash: { length: 3, gap: 6 },
  });
  road.push({
    id: 'dash_major',
    width: TOY_DASH_W * 1.5,
    color: paint,
    lanes: 0,
    speed: 0,
    lift: TOY_MARK_LIFT,
    detail: true,
    dash: { length: 4.5, gap: 9 },
  });
  road.push({
    id: 'zebra',
    width: TOY_ZEBRA_W,
    color: paint,
    lanes: 0,
    speed: 0,
    lift: TOY_MARK_LIFT,
    detail: true,
  });
  return road;
}
