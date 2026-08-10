# Styles — design knowledge for the SF diorama

Versioned reference material for the visual direction of the city. Skills and
prompts should LINK here rather than duplicate this content, so there is one
source of truth and style changes are reviewed commits.

| File | Style | When it applies |
|---|---|---|
| [`miniature-toy.md`](./miniature-toy.md) | Stylized miniature tech-city (toy diorama) | The default and currently ONLY user-facing style. Governs all asset authoring, kit pieces, landmarks, props, and visual judgment. |

Adding a new style or scenario variant: add a file here, add a row to this
table stating exactly when it applies, and update the `sf-miniature-style`
skill stub (`.agents/skills/sf-miniature-style/SKILL.md`) if discovery rules
change. Do not fork the bible into prompts — cite it.

Where the style is IMPLEMENTED in code (as opposed to defined):
`app/src/env.js` (lighting), `app/src/camera.js` (locked diorama camera),
`app/src/toypost.js` (tilt-shift + grade), `app/src/materials.js` (flat
shading), `pipeline/toy.mjs` (baked toy geometry/palette),
`app/src/ui-theme.css` (UI theme tokens).
