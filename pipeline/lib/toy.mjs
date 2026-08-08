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

// Toy streets: the base widths and lane data, restyled charcoal, plus the white
// edge ribbon class the bake emits alongside every road.
export function toyStreetClasses(base) {
  const road = base.map((c) => ({ ...c, color: hex('#3c3c40') }));
  road.push({ id: 'edge', width: 0.4, color: hex('#e8e8e4'), lanes: 0, speed: 0 });
  return road;
}

export const TOY_EDGE_CLASS = (base) => base.length; // index of the pushed edge class
export const TOY_EDGE_WIDTH = 0.4;
export const TOY_EDGE_INSET = 0.3; // from the kerb, toward the centerline
export const TOY_EDGE_LIFT = 0.02;
