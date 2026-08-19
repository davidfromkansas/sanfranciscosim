// Lints the serverless handlers in api/.
//
// It is a separate config from app/eslint.config.js because ESLint 9 resolves
// files against the directory its config sits in, and api/ is a sibling of
// app/ rather than inside it. No imports, so it needs nothing installed at
// this level — the globals list below is only what a Vercel function touches.
//
// The rule that matters is no-undef. api/ is not bundled and has no tests, so
// `node --check` was the only thing looking at it, and that parses without
// resolving a single name: a handler shipped calling three functions it had
// forgotten to import, and 500'd on every cron fire until the logs were read.
export default [
  {
    files: ["api/**/*.mjs"],
    languageOptions: {
      ecmaVersion: 2023,
      sourceType: "module",
      globals: {
        process: "readonly",
        console: "readonly",
        URL: "readonly",
        URLSearchParams: "readonly",
        fetch: "readonly",
        Response: "readonly",
        Request: "readonly",
        Headers: "readonly",
        AbortController: "readonly",
        AbortSignal: "readonly",
        Buffer: "readonly",
        TextEncoder: "readonly",
        TextDecoder: "readonly",
        setTimeout: "readonly",
        clearTimeout: "readonly",
        setInterval: "readonly",
        clearInterval: "readonly",
        structuredClone: "readonly",
        crypto: "readonly",
        performance: "readonly",
      },
    },
    rules: {
      "no-undef": "error",
      "no-unused-vars": ["error", { argsIgnorePattern: "^_" }],
      "no-dupe-keys": "error",
      "no-unreachable": "error",
    },
  },
];
