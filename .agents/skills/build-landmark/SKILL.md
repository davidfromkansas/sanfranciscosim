---
name: build-landmark
description: End-to-end pipeline that turns an SF address or building name ("Fairmont Hotel", "950 Mason St") into a planned, built, approved, optimized, and integrated 3D landmark in the sanfranciscosim scene. Use when the user asks to add, create, or build a building/landmark for the SF city from a name or address.
---

# Build a landmark from an address

This skill is a pointer: the full procedure lives at
[`docs/asset-pipeline/ADDRESS-TO-ASSET.md`](../../../docs/asset-pipeline/ADDRESS-TO-ASSET.md).
Read it and execute it with `BUILDING: <the user's address or name>`.

Summary of what it does (do not execute from this summary — read the doc):
resolve the building via OSM → write the research plan doc → build the GLB
per the plan and asset contract → STOP for the owner's explicit approval of
the renders → run the shrink pass (`docs/asset-pipeline/GLB-OPTIMIZE-PROMPT.md`)
→ integrate locally per `docs/asset-plans/INTEGRATION-PROMPT.md`, then ask
before any push or deploy.
