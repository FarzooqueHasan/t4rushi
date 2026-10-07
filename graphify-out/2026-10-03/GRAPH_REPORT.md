# Graph Report - MBD  (2026-10-02)

## Corpus Check
- 25 files · ~732,568 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 12 file(s) not represented in the graph (top: .bin 4, .gltf 4, .css 2)

## Summary
- 305 nodes · 501 edges · 36 communities (23 shown, 13 thin omitted)
- Extraction: 98% EXTRACTED · 2% INFERRED · 0% AMBIGUOUS · INFERRED: 9 edges (avg confidence: 0.84)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `be856eb6`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- GLTFParser
- GLTFLoader
- os
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
- GLTFCubicSplineInterpolant
- Task 6 for Antigravity
- Correction — Tasks 6 and 7 progress windows
- Task 7 for Antigravity
- Task 10 — second correction
- FastQuietHandler
- FastQuietHandler
- The three pieces
- QuietHandler
- QuietHandler
- QuietHandler
- QuietHandler

## God Nodes (most connected - your core abstractions)
1. `GLTFParser` - 31 edges
2. `Tarushi Birthday Site — Antigravity Brief` - 25 edges
3. `GLTFLoader` - 10 edges
4. `Task 8 for Antigravity` - 10 edges
5. `assignExtrasToUserData()` - 8 edges
6. `addPrimitiveAttributes()` - 8 edges
7. `Task 4 for Antigravity` - 8 edges
8. `Task 9 for Antigravity — Beat 6 formation escorts` - 8 edges
9. `Task 10 for Antigravity` - 8 edges
10. `Task 12 for Antigravity — real Black Hole model at Beat 1` - 8 edges

## Surprising Connections (you probably didn't know these)
- None detected - all connections are within the same source files.

## Import Cycles
- None detected.

## Communities (36 total, 13 thin omitted)

### Community 0 - "GLTFParser"
Cohesion: 0.08
Nodes (21): addMorphTargets(), addPrimitiveAttributes(), assignAttributeAccessor(), addUnknownExtensionsToUserData(), assignExtrasToUserData(), buildNodeHierachy(), computeBounds(), createAttributesKey() (+13 more)

### Community 1 - "GLTFLoader"
Cohesion: 0.07
Nodes (8): GLTFLightsExtension, GLTFLoader, GLTFMaterialsClearcoatExtension, GLTFMaterialsTransmissionExtension, GLTFMeshoptCompression, GLTFTextureBasisUExtension, GLTFTextureWebPExtension, resolveURL()

### Community 2 - "os"
Cohesion: 0.23
Nodes (13): http_server, json, os, selenium, selenium_webdriver_chrome_options, selenium_webdriver_common_action_chains, selenium_webdriver_common_by, selenium_webdriver_support_ui (+5 more)

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
Cohesion: 0.43
Nodes (6): animate(), checkCheckpointLog(), damp(), getInterpolatedFOV(), updateAircraftOpacities(), updateBeat1Caption()

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

### Community 27 - "The three pieces"
Cohesion: 0.67
Nodes (3): Part 1 — The Prank, Part 2 — The 3D Motion Sequence (8 beats, one continuous scroll), The three pieces

## Knowledge Gaps
- **93 isolated node(s):** `Overview`, `Tech stack`, `Part 1 — The Prank`, `Part 2 — The 3D Motion Sequence (8 beats, one continuous scroll)`, `Part 3 — The ScrapBook Art Portfolio (persists after the birthday)` (+88 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 150 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **13 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Tarushi Birthday Site — Antigravity Brief` connect `Tarushi Birthday Site — Antigravity Brief` to `Task 8 for Antigravity`, `Task 10 for Antigravity`, `Task 12 for Antigravity — real Black Hole model at Beat 1`, `Task 4 for Antigravity`, `Task 9 for Antigravity — Beat 6 formation escorts`, `Task 3 for Antigravity`, `Task 5 for Antigravity`, `Task 11 for Antigravity — MiG-21 Bison replaces the procedural fighter jet`, `Task 2 for Antigravity`, `Task 5 correction — read before continuing`, `Task 10 correction — read before continuing`, `Task 10 — starfield correction`, `Task 6 for Antigravity`, `Correction — Tasks 6 and 7 progress windows`, `Task 7 for Antigravity`, `Task 10 — second correction`, `The three pieces`?**
  _High betweenness centrality (0.131) - this node is a cross-community bridge._
- **Why does `GLTFParser` connect `GLTFParser` to `GLTFLoader`, `GLTFMaterialsPbrSpecularGlossinessExtension`?**
  _High betweenness centrality (0.036) - this node is a cross-community bridge._
- **Why does `Task 8 for Antigravity` connect `Task 8 for Antigravity` to `Tarushi Birthday Site — Antigravity Brief`?**
  _High betweenness centrality (0.021) - this node is a cross-community bridge._
- **What connects `Overview`, `Tech stack`, `Part 1 — The Prank` to the rest of the system?**
  _93 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `GLTFParser` be split into smaller, more focused modules?**
  _Cohesion score 0.0771478667445938 - nodes in this community are weakly interconnected._
- **Should `GLTFLoader` be split into smaller, more focused modules?**
  _Cohesion score 0.06890756302521009 - nodes in this community are weakly interconnected._