# Graph Report - MBD  (2026-10-04)

## Corpus Check
- 34 files · ~797,228 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 12 file(s) not represented in the graph (top: .bin 4, .gltf 4, .css 2)

## Summary
- 349 nodes · 602 edges · 41 communities (25 shown, 16 thin omitted)
- Extraction: 99% EXTRACTED · 1% INFERRED · 0% AMBIGUOUS · INFERRED: 9 edges (avg confidence: 0.84)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `be856eb6`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- GLTFParser
- GLTFLoader
- selenium
- prank.js
- Tarushi Birthday Site — Antigravity Brief
- Task 8 for Antigravity
- GLTFMaterialsPbrSpecularGlossinessExtension
- main.js
- Task 10 for Antigravity
- Task 12 for Antigravity — real Black Hole model at Beat 1
- Task 4 for Antigravity
- Task 9 for Antigravity — Beat 6 formation escorts
- OBJLoader
- Task 3 for Antigravity
- Task 5 for Antigravity
- Task 11 for Antigravity — MiG-21 Bison replaces the procedural fighter jet
- Task 2 for Antigravity
- Task 5 correction — read before continuing
- Task 10 correction — read before continuing
- Task 10 — starfield correction
- Task 13 correction
- Task 6 for Antigravity
- Correction — Tasks 6 and 7 progress windows
- Task 7 for Antigravity
- Task 10 — second correction
- FastQuietHandler
- FastQuietHandler
- Task 13 for Antigravity — Beats 2 and 3
- QuietHandler
- QuietHandler
- QuietHandler
- QuietHandler
- FastQuietHandler
- FastQuietHandler
- The three pieces
- FastQuietHandler
- FastQuietHandler

## God Nodes (most connected - your core abstractions)
1. `GLTFParser` - 31 edges
2. `Tarushi Birthday Site — Antigravity Brief` - 27 edges
3. `GLTFLoader` - 10 edges
4. `animate()` - 10 edges
5. `Task 8 for Antigravity` - 10 edges
6. `assignExtrasToUserData()` - 8 edges
7. `addPrimitiveAttributes()` - 8 edges
8. `Task 4 for Antigravity` - 8 edges
9. `Task 9 for Antigravity — Beat 6 formation escorts` - 8 edges
10. `Task 10 for Antigravity` - 8 edges

## Surprising Connections (you probably didn't know these)
- None detected - all connections are within the same source files.

## Import Cycles
- None detected.

## Communities (41 total, 16 thin omitted)

### Community 0 - "GLTFParser"
Cohesion: 0.06
Nodes (24): addMorphTargets(), addPrimitiveAttributes(), assignAttributeAccessor(), addUnknownExtensionsToUserData(), assignExtrasToUserData(), buildNodeHierachy(), computeBounds(), createAttributesKey() (+16 more)

### Community 1 - "GLTFLoader"
Cohesion: 0.09
Nodes (6): GLTFLoader, GLTFMaterialsClearcoatExtension, GLTFMaterialsTransmissionExtension, GLTFMeshoptCompression, GLTFTextureBasisUExtension, GLTFTextureWebPExtension

### Community 2 - "selenium"
Cohesion: 0.19
Nodes (14): http_server, json, os, selenium, selenium_webdriver_chrome_options, selenium_webdriver_common_action_chains, selenium_webdriver_common_by, selenium_webdriver_support_ui (+6 more)

### Community 3 - "prank.js"
Cohesion: 0.29
Nodes (9): initBurnShader(), onPointerDown(), onPointerUp(), playBurn(), setBurnProgress(), setProgress(), startPrankTransition(), triggerCompletionFlash() (+1 more)

### Community 4 - "Tarushi Birthday Site — Antigravity Brief"
Cohesion: 0.18
Nodes (10): Copy — Beat 1 & Beat 7, Open items — what to add, Overview, Part 3 — The ScrapBook Art Portfolio (persists after the birthday), Tarushi Birthday Site — Antigravity Brief, Task 1 correction — read before continuing, Task 1 for Antigravity, Task 5 — second addendum: yaw for a broadside read (+2 more)

### Community 5 - "Task 8 for Antigravity"
Cohesion: 0.20
Nodes (10): Assets, Components, Cover (first viewport), Explicitly not in scope, Flight Log spread (second section), Motion, Palette and fonts — bounded, nothing else, Task 8 for Antigravity (+2 more)

### Community 7 - "main.js"
Cohesion: 0.24
Nodes (10): animate(), checkCheckpointLog(), damp(), getInterpolatedFOV(), updateAircraftOpacities(), updateBeat1Caption(), updateBeat2Warp(), updateBeat3Environment() (+2 more)

### Community 8 - "Task 10 for Antigravity"
Cohesion: 0.25
Nodes (8): Accretion disk, Caption, Event horizon core, Explicitly not in scope, Lensing warp — applied once, at generation time, to each star's position, Starfield, Task 10 for Antigravity, Verification

### Community 9 - "Task 12 for Antigravity — real Black Hole model at Beat 1"
Cohesion: 0.25
Nodes (8): Attribution, Explicitly not in scope, Keep the original materials and textures — do not override them, Normalize, Step 0 — verify the loader can actually render this, before anything else, Task 12 for Antigravity — real Black Hole model at Beat 1, Verification, What to keep from the file, what to exclude

### Community 10 - "Task 4 for Antigravity"
Cohesion: 0.25
Nodes (8): Determine orientation — verify, don't assume, Explicitly not in scope, Materials and lighting — unchanged from the original spec, Normalize the geometry, Placement, Strip before use, Task 4 for Antigravity, Verification

### Community 11 - "Task 9 for Antigravity — Beat 6 formation escorts"
Cohesion: 0.25
Nodes (8): Explicitly not in scope, License and attribution — required, not optional, Materials — override, discard the originals, Normalize each model independently, Placement — Beat 6 formation, Reveal, same mechanic as Task 6, Task 9 for Antigravity — Beat 6 formation escorts, Verification

### Community 13 - "Task 3 for Antigravity"
Cohesion: 0.29
Nodes (7): Explicitly not in scope, Prank layer — visual spec, Sequence, exact timings, Task 3 for Antigravity, The hold button — do not restyle it, Verification, Where this lives

### Community 14 - "Task 5 for Antigravity"
Cohesion: 0.29
Nodes (7): Explicitly not in scope, Geometry — exact silhouette, don't reinterpret, Materials and lighting — same as the B2, no new colors, Placement, Scale, Task 5 for Antigravity, Verification

### Community 15 - "Task 11 for Antigravity — MiG-21 Bison replaces the procedural fighter jet"
Cohesion: 0.29
Nodes (7): Explicitly not in scope, License and attribution, Materials — override, same treatment as every other aircraft, Normalize, Placement — unchanged from the existing Beat 5 setup, Task 11 for Antigravity — MiG-21 Bison replaces the procedural fighter jet, Verification

### Community 16 - "Task 2 for Antigravity"
Cohesion: 0.33
Nodes (6): 2A — Hold-to-proceed gesture (`hold-test.html`), 2B — Burn/dissolve shader (`burn-test.html`), Combined check, before calling this task done, Explicitly not in scope for this task, Task 2 for Antigravity, Verification

### Community 17 - "Task 5 correction — read before continuing"
Cohesion: 0.40
Nodes (5): Explicitly not in scope, Fuselage — new geometry, added to the same jet group, Material — reuse, don't create a new one, Task 5 correction — read before continuing, Verification

### Community 18 - "Task 10 correction — read before continuing"
Cohesion: 0.40
Nodes (5): Explicitly not in scope, Problem 1: the disk has no turbulence, no radial gradient, and a stray gap cut into one side, Problem 2: the void doesn't read as a void, Task 10 correction — read before continuing, Verification

### Community 19 - "Task 10 — starfield correction"
Cohesion: 0.40
Nodes (5): Explicitly not in scope, Sprite texture, Task 10 — starfield correction, Three layers, not one, Verification

### Community 20 - "Task 13 correction"
Cohesion: 0.40
Nodes (5): Explicitly not in scope, Fix 1 — the sprite texture, Fix 2 — fade the ambient stars during the dive, Task 13 correction, Verification

### Community 21 - "Task 6 for Antigravity"
Cohesion: 0.50
Nodes (4): Behavior, Explicitly not in scope, Task 6 for Antigravity, Verification

### Community 22 - "Correction — Tasks 6 and 7 progress windows"
Cohesion: 0.50
Nodes (4): Correction — Tasks 6 and 7 progress windows, Task 6 — corrected windows, Task 7 — corrected windows, Verification

### Community 23 - "Task 7 for Antigravity"
Cohesion: 0.50
Nodes (4): Explicitly not in scope, Progress range and four stages, Task 7 for Antigravity, Verification

### Community 24 - "Task 10 — second correction"
Cohesion: 0.50
Nodes (4): Fix, Lensing check, still unresolved, Task 10 — second correction, Verification

### Community 27 - "Task 13 for Antigravity — Beats 2 and 3"
Cohesion: 0.33
Nodes (6): Beat 2 — warp streak tunnel (real range `0.0719`–`0.2201`), Beat 3 — cloud layer (real range `0.2201`–`0.4253`), Explicitly not in scope, Task 13 for Antigravity — Beats 2 and 3, The flash — one function spanning both beats, not two, Verification

### Community 38 - "The three pieces"
Cohesion: 0.67
Nodes (3): Part 1 — The Prank, Part 2 — The 3D Motion Sequence (8 beats, one continuous scroll), The three pieces

## Knowledge Gaps
- **102 isolated node(s):** `Overview`, `Tech stack`, `Part 1 — The Prank`, `Part 2 — The 3D Motion Sequence (8 beats, one continuous scroll)`, `Part 3 — The ScrapBook Art Portfolio (persists after the birthday)` (+97 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 175 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **16 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Tarushi Birthday Site — Antigravity Brief` connect `Tarushi Birthday Site — Antigravity Brief` to `Task 8 for Antigravity`, `Task 10 for Antigravity`, `Task 12 for Antigravity — real Black Hole model at Beat 1`, `Task 4 for Antigravity`, `Task 9 for Antigravity — Beat 6 formation escorts`, `Task 3 for Antigravity`, `Task 5 for Antigravity`, `Task 11 for Antigravity — MiG-21 Bison replaces the procedural fighter jet`, `Task 2 for Antigravity`, `Task 5 correction — read before continuing`, `Task 10 correction — read before continuing`, `Task 10 — starfield correction`, `Task 13 correction`, `Task 6 for Antigravity`, `Correction — Tasks 6 and 7 progress windows`, `Task 7 for Antigravity`, `Task 10 — second correction`, `Task 13 for Antigravity — Beats 2 and 3`, `The three pieces`?**
  _High betweenness centrality (0.121) - this node is a cross-community bridge._
- **Why does `Task 8 for Antigravity` connect `Task 8 for Antigravity` to `Tarushi Birthday Site — Antigravity Brief`?**
  _High betweenness centrality (0.018) - this node is a cross-community bridge._
- **What connects `Overview`, `Tech stack`, `Part 1 — The Prank` to the rest of the system?**
  _102 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `GLTFParser` be split into smaller, more focused modules?**
  _Cohesion score 0.05997778600518327 - nodes in this community are weakly interconnected._
- **Should `GLTFLoader` be split into smaller, more focused modules?**
  _Cohesion score 0.08666666666666667 - nodes in this community are weakly interconnected._