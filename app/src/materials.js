// All city materials. Lambert bases patched with onBeforeCompile so we keep
// Three's shadow/fog plumbing while adding: procedural window grids that ignite
// at dusk, cheap vertical AO, and hashed-dither LOD cross-fades (dithered, never
// blended, so there is no sorting cost and no visible pop).

import {
  AdditiveBlending,
  BufferGeometry,
  Color,
  DoubleSide,
  Float32BufferAttribute,
  MeshBasicMaterial,
  MeshLambertMaterial,
  Vector3,
  Vector4,
} from 'three';
import { shared } from './env.js';

const DITHER = /* glsl */ `
  // 4x4 ordered dither: stable in screen space, so a fading tier disappears as
  // an even stipple rather than a pop.
  float ditherThreshold(vec2 c) {
    int x = int(mod(c.x, 4.0));
    int y = int(mod(c.y, 4.0));
    int index = x + y * 4;
    float limit = 0.0;
    if (index == 0) limit = 0.0625; else if (index == 1) limit = 0.5625;
    else if (index == 2) limit = 0.1875; else if (index == 3) limit = 0.6875;
    else if (index == 4) limit = 0.8125; else if (index == 5) limit = 0.3125;
    else if (index == 6) limit = 0.9375; else if (index == 7) limit = 0.4375;
    else if (index == 8) limit = 0.25; else if (index == 9) limit = 0.75;
    else if (index == 10) limit = 0.125; else if (index == 11) limit = 0.625;
    else if (index == 12) limit = 1.0; else if (index == 13) limit = 0.5;
    else if (index == 14) limit = 0.875; else limit = 0.375;
    return limit;
  }
`;

// Cloud shadows: two scrolling value-noise octaves in world XZ, sampled per
// fragment, so soft shadow blankets drift across the city with the real wind.
// How dark a fully overcast cell may go. The toy city has to stay a painted
// object, so this is deliberately well short of 1.0 — it is an art call, not a
// physical one.
export const CLOUD_MAX_SHADE = 0.45;

const CLOUDS = /* glsl */ `
  // uNight is declared by the host shader (every one that injects this block
  // already had it) — declaring it here too is a GLSL redefinition error.
  uniform vec2 uCloudDrift;
  uniform float uToy;
  uniform sampler2D uWeatherField;
  uniform vec2 uWeatherOrigin;
  uniform vec2 uWeatherScale;

  float cloudNoise(vec2 p) {
    vec2 i = floor(p);
    vec2 f = fract(p);
    f = f * f * (3.0 - 2.0 * f);
    float a = fract(sin(dot(i, vec2(127.1, 311.7))) * 43758.5453);
    float b = fract(sin(dot(i + vec2(1.0, 0.0), vec2(127.1, 311.7))) * 43758.5453);
    float c = fract(sin(dot(i + vec2(0.0, 1.0), vec2(127.1, 311.7))) * 43758.5453);
    float d = fract(sin(dot(i + vec2(1.0, 1.0), vec2(127.1, 311.7))) * 43758.5453);
    return mix(mix(a, b, f.x), mix(c, d, f.x), f.y);
  }

  float cloudShadow(vec2 world) {
    // Cover comes from the sky, shape comes from the noise. The field is
    // sampled by world position, so an overcast Sunset darkens while a clear
    // Mission does not — a single citywide number cannot do that.
    // (Weather used to be switched off entirely in diorama mode: "no weather on
    // the tabletop". David reversed that deliberately — see
    // docs/plans/WEATHER-PLAN.md §0. Do not put the uToy kill back.)
    vec2 uv = (world - uWeatherOrigin) * uWeatherScale;
    float cover = texture2D(uWeatherField, clamp(uv, 0.0, 1.0)).g;
    // No cloud, no work: skip the two noise evaluations entirely.
    if (cover < 0.01) return 1.0;

    vec2 p = world * 0.00055 + uCloudDrift;
    float n = cloudNoise(p) * 0.65 + cloudNoise(p * 2.3 + 11.0) * 0.35;
    float shade = smoothstep(0.42, 0.72, n);
    // MAX_SHADE caps how dark it can ever get: a fully shadowed toy city is a
    // grey city, and the model has to keep its painted look. uNight fades the
    // whole term out — cloud shade only means anything while there is sun.
    return 1.0 - shade * cover * ${CLOUD_MAX_SHADE.toFixed(2)} * (1.0 - uNight * 0.85);
  }
`;

// Lightning. Storms only; the flash IS the effect, there is no bolt geometry.
// (There is deliberately no shader fog here. Fog in this city is the fog-cube
// GLB, instanced by fogbanks.js, and nothing else — do not reintroduce a
// screen-space or per-fragment fog term.)
const FLASH = /* glsl */ `
  uniform float uFlash;
  uniform float uWetness;

  vec3 applyFlash(vec3 color) {
    return color + vec3(0.55, 0.6, 0.75) * uFlash;
  }
`;

const CLOUD_UNIFORMS = () => ({
  uCloudDrift: shared.uCloudDrift,
  uToy: shared.uToy,
  uNight: shared.uNight,
  uWeatherField: shared.uWeatherField,
  uWeatherOrigin: shared.uWeatherOrigin,
  uWeatherScale: shared.uWeatherScale,
  uWetness: shared.uWetness,
  uFlash: shared.uFlash,
});

const HASH = /* glsl */ `
  float hash13(vec3 p) {
    p = fract(p * 0.1031);
    p += dot(p, p.yzx + 33.33);
    return fract((p.x + p.y) * p.z);
  }
`;

export function createBuildingMaterial({ windows = 1 } = {}) {
  const material = new MeshLambertMaterial({ vertexColors: true, dithering: true });
  material.uniformsHolder = {
    uFade: { value: 1 },
    uNight: shared.uNight,
    uWindows: { value: windows },
    uSunColor: shared.uSunColor,
    ...CLOUD_UNIFORMS(),
  };

  // Declared as a normal function: `this` is the material instance, so every
  // chunk's material injects its own uniform objects (per-chunk fade).
  material.onBeforeCompile = function patchBuilding(shader) {
    Object.assign(shader.uniforms, this.uniformsHolder);
    shader.vertexShader = shader.vertexShader
      .replace(
        '#include <common>',
        `#include <common>
        attribute vec2 aMeta;
        attribute float aLocalY;
        varying vec3 vCityWorld;
        varying float vSeed;
        varying float vIsWall;
        varying float vLocalY;`
      )
      .replace(
        '#include <worldpos_vertex>',
        `#include <worldpos_vertex>
        vec4 cityWorld = modelMatrix * vec4(transformed, 1.0);
        vCityWorld = cityWorld.xyz;
        vSeed = aMeta.x;
        vIsWall = aMeta.y;
        vLocalY = aLocalY * 0.1;`
      );

    shader.fragmentShader = shader.fragmentShader
      .replace(
        '#include <common>',
        `#include <common>
        uniform float uFade;
        uniform float uNight;
        uniform float uWindows;
        uniform vec3 uSunColor;
        varying vec3 vCityWorld;
        varying float vSeed;
        varying float vIsWall;
        varying float vLocalY;
        ${DITHER}
        ${HASH}
        ${CLOUDS}
        ${FLASH}`
      )
      .replace(
        '#include <clipping_planes_fragment>',
        `#include <clipping_planes_fragment>
        if (uFade < 0.999 && ditherThreshold(gl_FragCoord.xy) > uFade) discard;`
      )
      .replace(
        '#include <color_fragment>',
        `#include <color_fragment>
        float seed = vSeed / 255.0;

        // Per-building tone shift off the baked district seed: no two
        // neighbours read identically inside a palette.
        diffuseColor.rgb *= 0.84 + seed * 0.34;
        diffuseColor.rgb *= vec3(1.0 + (seed - 0.5) * 0.09, 1.0, 1.0 - (seed - 0.5) * 0.07);

        // Vertical ambient occlusion: streets read as canyons.
        float ao = mix(0.55, 1.0, clamp(vLocalY / 12.0, 0.0, 1.0));
        diffuseColor.rgb *= mix(1.0, ao, vIsWall);

        vec3 emissive = vec3(0.0);
        if (vIsWall > 0.5 && uWindows > 0.0) {
          // Wall-local horizontal coordinate: pick the axis the wall faces
          // away from, so the window grid never smears on diagonal facades.
          float u = mix(vCityWorld.x, vCityWorld.z, step(abs(vNormal.z), abs(vNormal.x)));
          float floorH = 3.6 + seed * 0.9;
          float colW = 3.1 + seed * 0.7;
          float row = floor(vLocalY / floorH);
          float col = floor(u / colW);
          vec2 cell = vec2(fract(vLocalY / floorH), fract(u / colW));
          float pane = smoothstep(0.16, 0.3, cell.x) * (1.0 - smoothstep(0.7, 0.84, cell.x))
                     * smoothstep(0.18, 0.32, cell.y) * (1.0 - smoothstep(0.68, 0.82, cell.y));
          float ground = step(2.0, vLocalY);
          pane *= ground * uWindows;

          // Daylight: panes read as darker glass with a cool sky tint.
          diffuseColor.rgb = mix(diffuseColor.rgb, diffuseColor.rgb * vec3(0.5, 0.58, 0.7), pane * (1.0 - uNight * 0.9));

          // Dusk: seeded progressive ignition, roughly one window at a time.
          float lit = hash13(vec3(row, col, seed * 255.0));
          float ignition = clamp(uNight * 1.35 - 0.05, 0.0, 1.0);
          float on = step(lit, ignition * 0.62) * pane;
          float warm = 0.7 + hash13(vec3(col, row, seed * 91.0)) * 0.6;
          emissive += vec3(1.0, 0.78, 0.5) * on * warm * 1.5 * uNight;
        }
        diffuseColor.rgb *= cloudShadow(vCityWorld.xz);
        totalEmissiveRadiance += emissive;`
      )
      .replace(
        '#include <fog_fragment>',
        `#include <fog_fragment>
        // Karl goes on AFTER lighting: fog is atmosphere between the eye and
        // the surface, not pigment on it.
        gl_FragColor.rgb = applyFlash(gl_FragColor.rgb);`
      );
  };

  return material;
}

// Toy tier: flat Lambert over the baked toy colours, with horizontal blue-glass
// window bands keyed to absolute world height so every 3.5 m floor lines up
// across the whole city. Rooftop garnish is flagged aMeta.y = 0 so HVAC boxes
// and solar panels never grow window bands.
// The lore flag byte rides along per vertex:
//   flag = profile * 4 + glowProp * 2 + suppressBands
// Profiles are 0 residential, 1 commercial, 2 always-on, 3 dark; `glowProp`
// marks a prop that is itself a light (marquee, gas canopy, neon blade), and
// `suppressBands` turns off the window grid for a wall that should not have one
// (a church, a warehouse, a parking deck) and for every prop.
const FLAG_DECODE = /* glsl */ `
  float f = vFlag + 0.5;
  float suppress = mod(floor(f), 2.0);
  float glowProp  = mod(floor(f / 2.0), 2.0);
  float profile   = floor(f / 4.0);
`;

export function createToyBuildingMaterial() {
  const material = new MeshLambertMaterial({ vertexColors: true, dithering: true });
  material.uniformsHolder = { uFade: { value: 1 }, uFloor: { value: 3.5 }, uNight: shared.uNight, ...CLOUD_UNIFORMS() };

  material.onBeforeCompile = function patchToy(shader) {
    Object.assign(shader.uniforms, this.uniformsHolder);
    shader.vertexShader = shader.vertexShader
      .replace(
        '#include <common>',
        `#include <common>
        attribute vec2 aMeta;
        attribute float aFlag;
        varying vec3 vToyPos;
        varying vec3 vToyNormal;
        varying float vToyWall;
        varying float vFlag;`
      )
      .replace(
        '#include <worldpos_vertex>',
        `#include <worldpos_vertex>
        vToyPos = (modelMatrix * vec4(transformed, 1.0)).xyz;
        vToyNormal = normal;
        vToyWall = aMeta.y;
        vFlag = aFlag;`
      );

    shader.fragmentShader = shader.fragmentShader
      .replace(
        '#include <common>',
        `#include <common>
        uniform float uFade;
        uniform float uFloor;
        uniform float uNight;
        varying vec3 vToyPos;
        varying vec3 vToyNormal;
        varying float vToyWall;
        varying float vFlag;
        ${CLOUDS}
        ${FLASH}
        ${DITHER}
        ${HASH}`
      )
      .replace(
        '#include <clipping_planes_fragment>',
        `#include <clipping_planes_fragment>
        if (uFade < 0.999 && ditherThreshold(gl_FragCoord.xy) > uFade) discard;`
      )
      .replace(
        '#include <color_fragment>',
        `#include <color_fragment>
        {
          ${FLAG_DECODE}
          float band = fract(vToyPos.y / uFloor);
          float isWall = vToyWall * (1.0 - abs(normalize(vToyNormal).y));
          float glass = step(0.35, band) * (1.0 - step(0.75, band)) * step(0.5, isWall) * (1.0 - suppress);
          diffuseColor.rgb = mix(diffuseColor.rgb, vec3(0.16, 0.30, 0.48), glass * 0.9);

          // Night: the same bands become lit windows, at a rate that depends on
          // what the building is. Homes glow warm and mostly-on, shops go bright
          // but thin out, hospitals and stations stay on, offices go dark.
          if (uNight > 0.001) {
            float share = profile < 0.5 ? 0.62
                        : profile < 1.5 ? 0.34
                        : profile < 2.5 ? 0.86
                        : 0.06;
            vec3 tint = profile < 0.5 ? vec3(1.0, 0.76, 0.46)
                      : profile < 1.5 ? vec3(1.0, 0.84, 0.58)
                      : profile < 2.5 ? vec3(0.94, 0.96, 1.0)
                      : vec3(0.86, 0.9, 1.0);
            float cellId = floor(vToyPos.y / uFloor) * 31.0
                         + floor((vToyPos.x + vToyPos.z) / 2.6) * 7.0;
            float lit = step(hash13(vec3(cellId, floor(vToyPos.x), floor(vToyPos.z))), share);
            totalEmissiveRadiance += tint * glass * lit * uNight * 1.5;
            // A glow prop is its own lamp: it does not wait for a window band.
            totalEmissiveRadiance += diffuseColor.rgb * glowProp * uNight * 1.35;
            diffuseColor.rgb *= mix(1.0, 0.72, uNight);
          }
        }
        diffuseColor.rgb *= cloudShadow(vToyPos.xz);`
      )
      .replace(
        '#include <fog_fragment>',
        `#include <fog_fragment>
        gl_FragColor.rgb = applyFlash(gl_FragColor.rgb);`
      );
  };

  return material;
}

// The hand-made building kit, drawn as one batch.
//
// Every kit vertex carries `aKit`: 0 = fixed palette, 1 = `Toy_body`, 2 = glass.
// The batch's per-instance colour is a straight multiply on everything, so the
// vertex stage puts the fixed palette back exactly as authored — trim, roofs,
// doors and awnings never take the lot tint, only the body does. The instance
// colour's alpha doubles as the chunk's dither fade, matching the procedural
// tiers' cross-fade instead of popping in.
export function createKitMaterial() {
  const material = new MeshLambertMaterial({ vertexColors: true, dithering: true });
  material.uniformsHolder = { uNight: shared.uNight, ...CLOUD_UNIFORMS() };

  material.onBeforeCompile = function patchKit(shader) {
    Object.assign(shader.uniforms, this.uniformsHolder);
    shader.vertexShader = shader.vertexShader
      .replace(
        '#include <common>',
        `#include <common>
        attribute float aKit;
        varying float vKit;
        varying vec3 vKitPos;`
      )
      .replace(
        '#include <color_vertex>',
        `#include <color_vertex>
        #ifdef USE_BATCHING_COLOR
          vColor.rgb = mix(color.rgb, vColor.rgb, step(0.5, aKit) * step(aKit, 1.5));
        #endif
        vKit = aKit;`
      )
      .replace(
        '#include <worldpos_vertex>',
        `#include <worldpos_vertex>
        vKitPos = (modelMatrix * vec4(transformed, 1.0)).xyz;`
      );

    shader.fragmentShader = shader.fragmentShader
      .replace(
        '#include <common>',
        `#include <common>
        uniform float uNight;
        varying float vKit;
        varying vec3 vKitPos;
        ${CLOUDS}
        ${FLASH}
        ${DITHER}
        ${HASH}`
      )
      .replace(
        '#include <clipping_planes_fragment>',
        `#include <clipping_planes_fragment>
        if (vColor.a < 0.999 && ditherThreshold(gl_FragCoord.xy) > vColor.a) discard;`
      )
      .replace(
        '#include <color_fragment>',
        `#include <color_fragment>
        if (uNight > 0.001) {
          // Only the glass ignites; doors, awnings and roofs stay dark.
          float glass = step(1.5, vKit);
          float lit = step(hash13(floor(vKitPos * vec3(1.4, 0.45, 1.4))), 0.58);
          totalEmissiveRadiance += vec3(1.0, 0.78, 0.48) * glass * lit * uNight * 1.5;
          diffuseColor.rgb *= mix(1.0, 0.72, uNight);
        }
        diffuseColor.rgb *= cloudShadow(vKitPos.xz);`
      )
      .replace(
        '#include <fog_fragment>',
        `#include <fog_fragment>
        gl_FragColor.rgb = applyFlash(gl_FragColor.rgb);`
      );
  };

  return material;
}

// A plain vertex-coloured Lambert whose per-batch-instance colour alpha drives
// the same ordered-dither fade the kit uses: landmark bodies stream in and out
// of one BatchedMesh as a stipple, never a pop. The rgb multiplier stays 1 —
// landmark colours are authored, only the alpha channel is used.
export function createBatchFadeLambert() {
  const material = new MeshLambertMaterial({ vertexColors: true, dithering: true });
  material.uniformsHolder = CLOUD_UNIFORMS();
  material.onBeforeCompile = function patchBatchFade(shader) {
    Object.assign(shader.uniforms, this.uniformsHolder);
    shader.vertexShader = shader.vertexShader
      .replace('#include <common>', `#include <common>\n        varying vec3 vBatchPos;`)
      .replace(
        '#include <worldpos_vertex>',
        `#include <worldpos_vertex>
        vBatchPos = (modelMatrix * vec4(transformed, 1.0)).xyz;`
      );
    shader.fragmentShader = shader.fragmentShader
      .replace(
        '#include <common>',
        `#include <common>
        uniform float uNight;
        varying vec3 vBatchPos;
        ${DITHER}
        ${CLOUDS}
        ${FLASH}`
      )
      .replace(
        '#include <clipping_planes_fragment>',
        `#include <clipping_planes_fragment>
        if (vColor.a < 0.999 && ditherThreshold(gl_FragCoord.xy) > vColor.a) discard;`
      )      .replace(
        '#include <fog_fragment>',
        `#include <fog_fragment>
        gl_FragColor.rgb = applyFlash(gl_FragColor.rgb);`
      );
  };
  return material;
}

// Far tier: one merged prism mesh per 2 km super-cell, with a per-quadrant fade
// so a 1 km near chunk can take over exactly its own quarter.
export function createFarBuildingMaterial() {
  const material = new MeshLambertMaterial({ vertexColors: true, dithering: true });
  material.uniformsHolder = {
    uQuadFade: { value: new Vector4(1, 1, 1, 1) },
    uNight: shared.uNight,
    uToy: shared.uToy,
    ...CLOUD_UNIFORMS(),
  };

  material.onBeforeCompile = function patchFar(shader) {
    Object.assign(shader.uniforms, this.uniformsHolder);
    shader.vertexShader = shader.vertexShader
      .replace(
        '#include <common>',
        `#include <common>
        attribute float aQuad;
        uniform vec4 uQuadFade;
        varying float vFade;
        varying vec3 vFarPos;`
      )
      .replace(
        '#include <worldpos_vertex>',
        `#include <worldpos_vertex>
        vFarPos = (modelMatrix * vec4(transformed, 1.0)).xyz;`
      )
      .replace(
        '#include <begin_vertex>',
        `#include <begin_vertex>
        int q = int(aQuad + 0.5);
        vFade = q == 0 ? uQuadFade.x : (q == 1 ? uQuadFade.y : (q == 2 ? uQuadFade.z : uQuadFade.w));`
      );

    shader.fragmentShader = shader.fragmentShader
      .replace(
        '#include <common>',
        `#include <common>
        // uToy is declared by the CLOUDS chunk below — declaring it here too
        // is a GLSL redefinition error.
        uniform float uNight;
        varying float vFade;
        varying vec3 vFarPos;
        ${DITHER}
        ${CLOUDS}
        ${FLASH}`
      )
      .replace(
        '#include <clipping_planes_fragment>',
        `#include <clipping_planes_fragment>
        if (vFade < 0.999 && ditherThreshold(gl_FragCoord.xy) > vFade) discard;`
      )
      .replace(
        '#include <color_fragment>',
        `#include <color_fragment>
        // Distant blocks pick up a warm glow at dusk instead of resolving windows.
        totalEmissiveRadiance += vec3(1.0, 0.72, 0.42) * uNight * 0.075 * (1.0 - uToy);
        // In toy mode the far tier is not re-baked: it just goes bright and flat
        // so it reads as more of the same model, out of focus.
        diffuseColor.rgb = mix(diffuseColor.rgb, pow(diffuseColor.rgb, vec3(0.72)) * 1.1 + 0.06, uToy);
        diffuseColor.rgb *= cloudShadow(vFarPos.xz);`
      )      .replace(
        '#include <fog_fragment>',
        `#include <fog_fragment>
        gl_FragColor.rgb = applyFlash(gl_FragColor.rgb);`
      );
  };

  return material;
}

// Streets + landcover share one material: both are draped, vertex-coloured
// ground. Asphalt (kind 64) picks up a faint warm sheen at night.
export function createGroundMaterial() {
  const material = new MeshLambertMaterial({ vertexColors: true, dithering: true });
  material.uniformsHolder = { uNight: shared.uNight, ...CLOUD_UNIFORMS() };
  material.polygonOffset = true;
  material.polygonOffsetFactor = -2;
  material.polygonOffsetUnits = -2;

  material.onBeforeCompile = function patchGround(shader) {
    Object.assign(shader.uniforms, this.uniformsHolder);
    shader.vertexShader = shader.vertexShader
      .replace(
        '#include <common>',
        `#include <common>
        attribute float aKind;
        varying float vKind;
        varying vec3 vGroundWorld;`
      )
      .replace(
        '#include <worldpos_vertex>',
        `#include <worldpos_vertex>
        vGroundWorld = (modelMatrix * vec4(transformed, 1.0)).xyz;`
      )
      .replace(
        '#include <begin_vertex>',
        `#include <begin_vertex>
        vKind = aKind;`
      );
    shader.fragmentShader = shader.fragmentShader
      .replace(
        '#include <common>',
        `#include <common>
        uniform float uNight;
        varying float vKind;
        varying vec3 vGroundWorld;
        ${CLOUDS}
        ${FLASH}`
      )
      .replace(
        '#include <color_fragment>',
        `#include <color_fragment>
        // 64 asphalt, 65 sidewalk, 66 paint: only the roadway picks up the
        // warm sodium sheen at night, and the paint stays crisp on top of it.
        float asphalt = step(63.5, vKind) * step(vKind, 64.5);
        float marking = step(65.5, vKind);
        diffuseColor.rgb *= cloudShadow(vGroundWorld.xz);
        // Wet ground: darker and slightly cooler, the way tarmac actually goes.
        diffuseColor.rgb *= mix(1.0, 0.62, uWetness * asphalt);
        diffuseColor.rgb = mix(diffuseColor.rgb, diffuseColor.rgb * vec3(0.86, 0.92, 1.06), uWetness * asphalt);
        totalEmissiveRadiance += vec3(1.0, 0.72, 0.42) * asphalt * uNight * 0.06;
        totalEmissiveRadiance += vec3(0.85, 0.86, 0.82) * marking * uNight * 0.1;`
      )
      .replace(
        '#include <fog_fragment>',
        `#include <fog_fragment>
        // Karl goes on AFTER lighting: fog is atmosphere between the eye and
        // the surface, not pigment on it.
        gl_FragColor.rgb = applyFlash(gl_FragColor.rgb);`
      );
  };

  return material;
}

// Terrain and trees: the same drifting cloud shade, so a shadow blanket crosses
// hillside, park and rooftop as one.
export function createCloudShadedMaterial() {
  const material = new MeshLambertMaterial({ vertexColors: true, dithering: true });
  material.uniformsHolder = CLOUD_UNIFORMS();
  material.onBeforeCompile = function patchCloudShaded(shader) {
    Object.assign(shader.uniforms, this.uniformsHolder);
    shader.vertexShader = shader.vertexShader
      .replace('#include <common>', `#include <common>\n        varying vec3 vCloudWorld;`)
      .replace(
        '#include <worldpos_vertex>',
        `#include <worldpos_vertex>
        vCloudWorld = (modelMatrix * vec4(transformed, 1.0)).xyz;`
      );
    shader.fragmentShader = shader.fragmentShader
      .replace('#include <common>', `#include <common>\n        uniform float uNight;\n        varying vec3 vCloudWorld;\n        ${CLOUDS}
        ${FLASH}`)
      .replace(
        '#include <color_fragment>',
        `#include <color_fragment>
        diffuseColor.rgb *= cloudShadow(vCloudWorld.xz);`
      .replace(
        '#include <fog_fragment>',
        `#include <fog_fragment>
        // Karl goes on AFTER lighting: fog is atmosphere between the eye and
        // the surface, not pigment on it.
        gl_FragColor.rgb = applyFlash(gl_FragColor.rgb);`
      )
      );
  };
  return material;
}

export function createTreeMaterial() {
  return createCloudShadedMaterial();
}

// --------------------------------------------------- streetlight pools ---
// The disc of light a streetlight throws on the road at night. Shared by both
// lamp systems: the procedural glow spheres in `city.js` and the kit's modelled
// `sl_*` poles in `streetkit.js`, so a pool looks the same whichever kind of
// lamp is standing there.
//
// Unit radius, lying in the XZ plane. The falloff lives in RGBA vertex colours
// rather than a texture or a patched shader: three's AdditiveBlending is
// (SRC_ALPHA, ONE), so that alpha ramp becomes a soft round wash straight out
// of MeshBasicMaterial. Two rings, not one — a lone fan puts the whole
// highlight on a single centre vertex and the pool reads as a cone.
// 16 segments, not 24: the disc is soft-edged and small on screen, so the extra
// tessellation is invisible while costing a third of the pool triangle budget —
// and hero-view night triangles are already the tightest number in PERF-PLAN.
export function createLampPoolGeometry(segments = 16) {
  const RINGS = [
    { r: 0, a: 1 },
    { r: 0.34, a: 0.72 },
    { r: 1, a: 0 },
  ];
  const positions = [0, 0, 0];
  const colors = [1, 1, 1, 1];
  const indices = [];
  for (let ring = 1; ring < RINGS.length; ring++) {
    const { r, a } = RINGS[ring];
    for (let i = 0; i <= segments; i++) {
      const t = (i / segments) * Math.PI * 2;
      positions.push(Math.cos(t) * r, 0, Math.sin(t) * r);
      colors.push(1, 1, 1, a);
    }
  }
  const ringStart = (ring) => 1 + (ring - 1) * (segments + 1);
  for (let i = 0; i < segments; i++) indices.push(0, ringStart(1) + i, ringStart(1) + i + 1);
  for (let ring = 1; ring < RINGS.length - 1; ring++) {
    const inner = ringStart(ring);
    const outer = ringStart(ring + 1);
    for (let i = 0; i < segments; i++) {
      indices.push(inner + i, outer + i, outer + i + 1);
      indices.push(inner + i, outer + i + 1, inner + i + 1);
    }
  }
  const geometry = new BufferGeometry();
  geometry.setAttribute('position', new Float32BufferAttribute(positions, 3));
  geometry.setAttribute('color', new Float32BufferAttribute(colors, 4));
  geometry.setIndex(indices);
  return geometry;
}

// Lays a pool flat on the ground it is standing on rather than on a global
// horizontal plane. San Francisco's grades are the whole reason this exists: a
// flat disc on a 20% street floats over a metre clear of the tarmac at its
// downhill rim and buries itself at the uphill one, which reads as a hovering
// ellipse rather than light on a road. The normal comes from finite
// differences on the terrain either side of the lamp.
//
// Writes into `out` and returns it. Called at build time, never per frame.
const GROUND_UP = new Vector3(0, 1, 0);
const groundNormal = new Vector3();
export function alignPoolToGround(out, x, z, sampleElevation, probe = 3) {
  const ex = sampleElevation(x + probe, z) - sampleElevation(x - probe, z);
  const ez = sampleElevation(x, z + probe) - sampleElevation(x, z - probe);
  // Gradient (ex, ez) over 2*probe; the surface normal is (-dx, 1, -dz).
  groundNormal.set(-ex / (2 * probe), 1, -ez / (2 * probe)).normalize();
  return out.setFromUnitVectors(GROUND_UP, groundNormal);
}

// Additive so the pool brightens the road rather than painting over it, and
// depthWrite off so overlapping pools from neighbouring lamps blend instead of
// fighting each other. Opacity is driven from the night ramp by the owner.
export function createLampPoolMaterial() {
  return new MeshBasicMaterial({
    color: new Color(1.0, 0.76, 0.42),
    vertexColors: true,
    transparent: true,
    opacity: 0,
    blending: AdditiveBlending,
    depthWrite: false,
    side: DoubleSide,
  });
}

export const PALETTE_TINT = new Color();
