// The route wall: a vertical ribbon of light tracing a transit route's shape.
//
// This is the "Tron light trail" material the Muni route glow settled on over
// PRs #141/#143/#148/#149, lifted out so the ferry routes draw in the same
// idiom instead of a second, subtly different one. A route wall is not a tinted
// pane: it is a blown-out WHITE core with the colour living in the falloff
// around it, bounded by a hard clean edge, so the ribbon spends its alpha at
// the two edges — a crisp lit rim along the top and a contact flare where it
// meets the ground — and stays nearly clear through the middle, which is what
// lets you see the city through it.
//
// Geometry contract, per vertex:
//   aRibbon  0 at the ground, 1 at the top of the wall. NOT derivable from
//            world y — a wall that follows terrain has a different world height
//            at every vertex, and the profile is in wall space.
//   aFade    0..1 multiplier on the whole ribbon's alpha, for tapering a wall
//            out rather than cutting it off. Pass 1 everywhere to ignore it.
//
// NOTE: app/src/muni.js still carries its own copy of this shader. It is the
// older one and should migrate onto this module, but the bus walls only draw
// for routes with a live vehicle on them, and `vite preview` serves no
// /api/muni, so that swap cannot be verified in this environment — doing it
// blind risks a shipped feature for a tidy-up. Migrate it in a change that can
// be checked against the deployed feed.

import { Color, MeshBasicMaterial } from 'three';

// The toy theme's warm ink, used to outline the daylight ribbon. A coloured
// edge only contrasts where the city behind it happens to be a different
// colour; an ink line contrasts everywhere, which is why the UI cards are
// drawn this way.
export const ROUTE_WALL_INK = [0.13, 0.09, 0.07];

// uNight below this counts as day: the palette and blend mode swap here.
export const ROUTE_WALL_NIGHT_AT = 0.5;

//   coreWhite: how far the edges wash out to white (the "hot" core)
//   body:      alpha of the transparent interior
//   bodyFall:  how fast the interior thins with height (1 = linear, 2+ = only
//              a skirt near the ground)
//   topEdge:   width of the top rim, as a fraction of wall height
//   baseEdge:  width of the ground flare
//   ink:       width of the dark outline along the top (0 = none)
export const ROUTE_WALL_PROFILE = {
  // After dark the core goes properly white-hot and the interior nearly
  // vanishes, so the route reads as a drawn line of light. No ink: the wall is
  // emitted light against a dark city, and additive blending cannot draw a
  // dark line anyway.
  night: { coreWhite: 0.92, body: 0.27, bodyFall: 2.2, topEdge: 0.075, baseEdge: 0.16, ink: 0 },
  // By day the same ribbon has to survive sunlight AND be findable from the
  // hero altitude, where a rim alone is a hairline. So daylight fills the
  // interior nearly to the top, whitens the core less — a white edge on a pale
  // surface is an invisible edge — and outlines the whole thing in warm ink.
  day: { coreWhite: 0.3, body: 1.0, bodyFall: 1.0, topEdge: 0.05, baseEdge: 0.13, ink: 0.05 },
};

export const NORMAL_BLENDING = 1;
export const ADDITIVE_BLENDING = 2;

// A ribbon material plus the uniforms that shape it. The caller owns the
// day/night decision and calls applyRouteWallDay when it flips.
export function createRouteWallMaterial({ isDay = true } = {}) {
  const material = new MeshBasicMaterial({
    vertexColors: true,
    transparent: true,
    blending: isDay ? NORMAL_BLENDING : ADDITIVE_BLENDING,
    depthWrite: false,
    side: 2, // DoubleSide — visible from both sides of the wall
    toneMapped: false, // a light trail is emitted light, not a lit surface
  });
  const profile = ROUTE_WALL_PROFILE[isDay ? 'day' : 'night'];
  const uniforms = {
    uCoreWhite: { value: profile.coreWhite },
    uBody: { value: profile.body },
    uBodyFall: { value: profile.bodyFall },
    uTopEdge: { value: profile.topEdge },
    uBaseEdge: { value: profile.baseEdge },
    uInk: { value: profile.ink },
    uInkColor: { value: new Color(...ROUTE_WALL_INK) },
  };
  material.onBeforeCompile = (shader) => {
    Object.assign(shader.uniforms, uniforms);
    shader.vertexShader = shader.vertexShader
      .replace(
        '#include <common>',
        '#include <common>\n        attribute float aRibbon;\n        attribute float aFade;\n        varying float vRibbon;\n        varying float vFade;'
      )
      .replace(
        '#include <begin_vertex>',
        '#include <begin_vertex>\n        vRibbon = aRibbon;\n        vFade = aFade;'
      );
    shader.fragmentShader = shader.fragmentShader
      .replace(
        '#include <common>',
        `#include <common>
        uniform float uCoreWhite;
        uniform float uBody;
        uniform float uBodyFall;
        uniform float uTopEdge;
        uniform float uBaseEdge;
        uniform float uInk;
        uniform vec3 uInkColor;
        varying float vRibbon;
        varying float vFade;`
      )
      .replace(
        '#include <dithering_fragment>',
        `#include <dithering_fragment>
        // Two hot edges and a near-clear interior.
        float top = exp(-pow((1.0 - vRibbon) / uTopEdge, 2.0));
        float base = exp(-pow(vRibbon / uBaseEdge, 2.0));
        // The interior is brightest where the light spills off the ground and
        // thins upward, so the wall has a direction: it is lit FROM the route,
        // not uniformly filled.
        float body = uBody * pow(1.0 - vRibbon, uBodyFall);
        float edge = clamp(top + base * 0.85, 0.0, 1.0);
        gl_FragColor.rgb = mix(gl_FragColor.rgb, vec3(1.0), edge * uCoreWhite);
        float alpha = clamp(body * 0.55 + top + base * 0.8, 0.0, 1.0);
        // Ink outline (day only): a dark line capping the ribbon, so it is
        // legible over a pale surface and a dark one alike.
        float ink = uInk > 0.0 ? smoothstep(1.0 - uInk, 1.0 - uInk * 0.35, vRibbon) : 0.0;
        gl_FragColor.rgb = mix(gl_FragColor.rgb, uInkColor, ink);
        gl_FragColor.a = max(alpha, ink) * opacity * vFade;`
      );
  };
  return { material, uniforms };
}

// Swap palette and blend mode when the scene crosses dusk or dawn. Additive
// keeps the beam glowing after dark; NormalBlending makes the same wall painted
// colour by day, which is the only way it survives sunlight.
export function applyRouteWallDay({ material, uniforms }, isDay) {
  material.blending = isDay ? NORMAL_BLENDING : ADDITIVE_BLENDING;
  material.needsUpdate = true;
  const profile = ROUTE_WALL_PROFILE[isDay ? 'day' : 'night'];
  uniforms.uCoreWhite.value = profile.coreWhite;
  uniforms.uBody.value = profile.body;
  uniforms.uBodyFall.value = profile.bodyFall;
  uniforms.uTopEdge.value = profile.topEdge;
  uniforms.uBaseEdge.value = profile.baseEdge;
  uniforms.uInk.value = profile.ink;
}
