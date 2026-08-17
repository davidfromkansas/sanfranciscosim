import js from '@eslint/js';
import globals from 'globals';

export default [
  js.configs.recommended,
  {
    files: ['**/*.js'],
    languageOptions: {
      ecmaVersion: 2023,
      sourceType: 'module',
      globals: {
        ...globals.browser,
        ...globals.worker,
        __TILES_VERSION__: 'readonly',
      },
    },
    rules: {
      'no-unused-vars': ['error', { argsIgnorePattern: '^_' }],
      'no-console': 'off',
      // Everything under sf-assets is meshopt-compressed at intake, so a bare
      // GLTFLoader throws on load and the feature silently ceases to exist
      // (this is what took the fog banks out). src/gltf.js is the one place
      // allowed to construct the loader; it wires the decoder.
      'no-restricted-imports': ['error', {
        paths: [{
          name: 'three/addons/loaders/GLTFLoader.js',
          message: 'Use createGLTFLoader() from ./gltf.js — a bare loader cannot read meshopt-compressed GLBs.',
        }],
      }],
    },
  },
  {
    files: ['src/gltf.js'],
    rules: { 'no-restricted-imports': 'off' },
  },
  {
    files: ['test/**/*.mjs'],
    languageOptions: {
      ecmaVersion: 2023,
      sourceType: 'module',
      globals: { ...globals.node },
    },
  },
];
