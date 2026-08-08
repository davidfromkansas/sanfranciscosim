// All city materials. Lambert bases patched with onBeforeCompile so we keep
// Three's shadow/fog plumbing while adding: procedural window grids that ignite
// at dusk, cheap vertical AO, and hashed-dither LOD cross-fades (dithered, never
// blended, so there is no sorting cost and no visible pop).

import { Color, MeshLambertMaterial, Vector4 } from 'three';
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
        totalEmissiveRadiance += emissive;`
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
  };

  material.onBeforeCompile = function patchFar(shader) {
    Object.assign(shader.uniforms, this.uniformsHolder);
    shader.vertexShader = shader.vertexShader
      .replace(
        '#include <common>',
        `#include <common>
        attribute float aQuad;
        uniform vec4 uQuadFade;
        varying float vFade;`
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
        uniform float uNight;
        varying float vFade;
        ${DITHER}`
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
        totalEmissiveRadiance += vec3(1.0, 0.72, 0.42) * uNight * 0.075;`
      );
  };

  return material;
}

// Streets + landcover share one material: both are draped, vertex-coloured
// ground. Asphalt (kind 64) picks up a faint warm sheen at night.
export function createGroundMaterial() {
  const material = new MeshLambertMaterial({ vertexColors: true, dithering: true });
  material.uniformsHolder = { uNight: shared.uNight };
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
        varying float vKind;`
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
        varying float vKind;`
      )
      .replace(
        '#include <color_fragment>',
        `#include <color_fragment>
        float asphalt = step(63.5, vKind);
        totalEmissiveRadiance += vec3(1.0, 0.72, 0.42) * asphalt * uNight * 0.06;`
      );
  };

  return material;
}

export function createTreeMaterial() {
  return new MeshLambertMaterial({ vertexColors: true, dithering: true });
}

export const PALETTE_TINT = new Color();
