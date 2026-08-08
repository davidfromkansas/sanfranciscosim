// Street classes and landcover kinds: shared by the bake steps, the validation
// gate and (via manifest.json) the runtime renderer.

// DataSF classcodes: 1 freeway, 2 major, 3 arterial/secondary, 4 collector,
// 5 residential, 6/7 ramp or private/other.
export const STREET_CLASSES = [
  { id: 'freeway', width: 22, color: [0.34, 0.34, 0.36], lanes: 4, speed: 28 },
  { id: 'major', width: 18, color: [0.36, 0.36, 0.38], lanes: 3, speed: 18 },
  { id: 'arterial', width: 14, color: [0.35, 0.35, 0.37], lanes: 2, speed: 14 },
  { id: 'collector', width: 11, color: [0.33, 0.33, 0.35], lanes: 1, speed: 11 },
  { id: 'residential', width: 9, color: [0.31, 0.31, 0.33], lanes: 1, speed: 9 },
  { id: 'ramp', width: 8, color: [0.33, 0.33, 0.35], lanes: 1, speed: 14 },
  { id: 'other', width: 6, color: [0.3, 0.3, 0.32], lanes: 1, speed: 7 },
];

export const CLASS_BY_CODE = { 1: 0, 2: 1, 3: 2, 4: 3, 5: 4, 6: 6, 7: 6, 0: 6 };

export const LAND_KINDS = [
  { id: 'grass', color: [0.36, 0.47, 0.25] },
  { id: 'trees', color: [0.2, 0.34, 0.18] },
  { id: 'sand', color: [0.78, 0.72, 0.55] },
  { id: 'water', color: [0.12, 0.28, 0.34] },
  { id: 'pitch', color: [0.31, 0.45, 0.28] },
  { id: 'scrub', color: [0.42, 0.45, 0.28] },
  { id: 'paved', color: [0.42, 0.42, 0.42] },
];
