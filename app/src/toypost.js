// Diorama post-processing: a tilt-shift blur that keeps a horizontal focus band
// sharp and softens top and bottom, plus a gentle saturation/contrast grade.
// Hand-rolled rather than EffectComposer: one render target, one fullscreen
// triangle-pair, created once and reused across every toggle.

import {
  LinearFilter,
  Mesh,
  OrthographicCamera,
  PlaneGeometry,
  RGBAFormat,
  Scene,
  ShaderMaterial,
  Vector2,
  WebGLRenderTarget,
} from 'three';

const VERT = /* glsl */ `
  varying vec2 vUv;
  void main() {
    vUv = uv;
    gl_Position = vec4(position.xy, 0.0, 1.0);
  }
`;

const FRAG = /* glsl */ `
  uniform sampler2D tDiffuse;
  uniform vec2 uTexel;
  uniform float uMaxBlur;
  uniform float uFocus;   // screen-space y of the sharp band
  uniform float uRange;   // half-height of the sharp band
  uniform float uSaturation;
  uniform float uContrast;
  varying vec2 vUv;

  void main() {
    // Blur grows with distance from the focus band, like a shifted lens plane.
    float d = abs(vUv.y - uFocus);
    float blur = clamp((d - uRange) / max(0.0001, 1.0 - uRange), 0.0, 1.0) * uMaxBlur;
    vec3 col = vec3(0.0);
    float total = 0.0;
    for (int y = -1; y <= 1; y++) {
      for (int x = -1; x <= 1; x++) {
        vec2 offset = vec2(float(x), float(y)) * uTexel * blur;
        float w = (x == 0 && y == 0) ? 2.0 : 1.0;
        col += texture2D(tDiffuse, vUv + offset).rgb * w;
        total += w;
      }
    }
    col /= total;

    // Toy grade: saturate, then a soft S-curve around mid grey.
    float luma = dot(col, vec3(0.2126, 0.7152, 0.0722));
    col = mix(vec3(luma), col, uSaturation);
    col = clamp((col - 0.5) * uContrast + 0.5, 0.0, 1.0);
    gl_FragColor = vec4(col, 1.0);
  }
`;

export function createToyPost(renderer) {
  const size = renderer.getSize(new Vector2());
  const pixelRatio = renderer.getPixelRatio();
  const target = new WebGLRenderTarget(size.x * pixelRatio, size.y * pixelRatio, {
    minFilter: LinearFilter,
    magFilter: LinearFilter,
    format: RGBAFormat,
    depthBuffer: true,
    stencilBuffer: false,
  });

  const material = new ShaderMaterial({
    uniforms: {
      tDiffuse: { value: target.texture },
      uTexel: { value: new Vector2(1 / target.width, 1 / target.height) },
      uMaxBlur: { value: 4 },
      uFocus: { value: 0.46 },
      uRange: { value: 0.16 },
      uSaturation: { value: 1.25 },
      uContrast: { value: 1.08 },
    },
    vertexShader: VERT,
    fragmentShader: FRAG,
    depthTest: false,
    depthWrite: false,
  });

  const quadScene = new Scene();
  const quadCamera = new OrthographicCamera(-1, 1, 1, -1, 0, 1);
  const quad = new Mesh(new PlaneGeometry(2, 2), material);
  quad.frustumCulled = false;
  quadScene.add(quad);

  let enabled = false;

  function setSize() {
    const s = renderer.getSize(new Vector2());
    const ratio = renderer.getPixelRatio();
    target.setSize(Math.max(1, s.x * ratio), Math.max(1, s.y * ratio));
    material.uniforms.uTexel.value.set(1 / target.width, 1 / target.height);
  }

  return {
    get enabled() {
      return enabled;
    },
    setEnabled(value) {
      enabled = value;
      if (enabled) setSize();
    },
    setSize,
    // Drop-in for renderer.render: off, it renders straight to the canvas.
    render(scene, camera) {
      if (!enabled) {
        renderer.setRenderTarget(null);
        renderer.render(scene, camera);
        return;
      }
      renderer.setRenderTarget(target);
      renderer.render(scene, camera);
      renderer.setRenderTarget(null);
      renderer.render(quadScene, quadCamera);
    },
    dispose() {
      target.dispose();
      material.dispose();
      quad.geometry.dispose();
    },
  };
}
