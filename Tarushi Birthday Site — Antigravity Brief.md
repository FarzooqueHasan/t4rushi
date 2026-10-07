# Tarushi Birthday Site — Antigravity Brief

Sep 26, 2026 · @Farzooque Hasan

## Overview

Three pieces, one linear reveal on her birthday, one piece that survives it. The Prank opens as a fake pastel Hello Kitty page; a hold-to-proceed gesture blows it apart into the 3D Motion Sequence — an 8-beat cinematic scroll through a black hole into an aviation flyby built from her own sketches, ending in a Φ → taNushi → Tarushi → Happy Birthday name reveal. That sequence crossfades directly into the ScrapBook Art Portfolio, which is what she keeps using after the birthday is over.

## Tech stack

| Piece | Stack | Why |
| --- | --- | --- |
| Prank | Rive or Lottie, CSS | Cheap 2D animation — it's meant to look simple before the reveal |
| 3D Motion Sequence | Three.js, GSAP + ScrollTrigger, Lenis, hand-written GLSL (burn/dissolve, lensing), Blender-exported models | The only piece that needs a real WebGL engine and a scroll-scrubbed camera |
| ScrapBook Portfolio | HTML/CSS, light scroll JS | No 3D — this keeps the entire WebGL/shader budget on the Motion Sequence |
| Sound (all pieces) | Howler.js or the Web Audio API | Charge-up, burn, kaboom, and "yay" cues |

## The three pieces

### Part 1 — The Prank

1. Kawaii pink landing page: bubble font, sparkle cursor, fake visitor counter, a fake guestbook — sells it as genuinely hers before anything cracks
2. A big glittery button reads "click for surprise" but requires a hold, not a click; a charge ring fills
3. As the ring completes, the page freezes and glitches; centered text fades in: "did you really think my skills are this bad?"
4. **KABOOM** — a thick brutalist-stencil burst (screen-shake, particles) blows the pink layer apart via the burn/dissolve shader, straight into Beat 0 of the Motion Sequence below

### Part 2 — The 3D Motion Sequence (8 beats, one continuous scroll)

| Beat | What happens |
| --- | --- |
| 0 | Prank layer finishes its burn/dissolve from Part 1 |
| 1 | Deep space, stylized black hole, gravitational lensing; one line of type near it |
| 2 | Camera accelerates into the event horizon, whiteout warp |
| 3 | Punches through cloud cover into an atmosphere flyover |
| 4 | Her own B2 pen sketch extrudes/morphs into the rendered 3D model as it banks into frame |
| 5 | Secondary fighter-jet flyby, built off her cockpit sketch |
| 6 | Formation flyby, camera decelerates into the hangar |
| 7 | Name reveal plays as the camera lands: Φ → taNushi → Tarushi → Happy Birthday |
| 8 | WebGL canvas crossfades into the ScrapBook's first page |

Palette stays to deep navy/black plus one glow accent shared by the event horizon and engine trails — two colors through all eight beats.

## Copy — Beat 1 & Beat 7

Final for now — edit inline if you want different wording, otherwise Antigravity builds these exact lines.

**Beat 1 (black hole line):** "some people just pull everything toward them."

**Beat 7 (name-reveal sequence):**

1. Φ fades in, gets struck through — caption: "what my phone thinks your name is."
2. taNushi fades in, gets struck through — caption: "still wrong."
3. Tarushi settles, un-struck, soft glow — caption: "there she is."
4. Scrolls into: Happy Birthday

### Part 3 — The ScrapBook Art Portfolio (persists after the birthday)

Paper-and-tape aesthetic: kraft/handmade-paper texture, polaroid-style photos, washi tape, a handwritten display font, torn edges. Scroll-triggered spreads, not literal page-flip.

| Section | Content |
| --- | --- |
| Flight Log | B2 and cockpit sketches, taped in like logbook pages |
| Studio Pages | Remaining sketches and watercolors, mixed-media layout |
| Mixtape | Spotify embed styled as a ticket stub; dance photos once available |
| Game Day | Basketball/athletics — currently empty, no material yet |
| Photo Booth | General candid photo dump as a polaroid strip |

## Task 1 for Antigravity

Build the empty camera rig before any real content — nothing else. This is deliberately the first task handed to Antigravity, before the Prank or the ScrapBook, since it carries the most that can go wrong and is cheapest to fix while it's still boxes instead of finished models.

- [ ] Set up Three.js + GSAP ScrollTrigger + Lenis in a blank page
- [ ] Define 8 fixed camera positions matching Beats 1–8 of the Motion Sequence above
- [ ] Place placeholder colored boxes at each beat's focal point — no real models, no shaders yet
- [ ] Wire scroll position to scrub the camera smoothly across all 8 positions
- [ ] Verify: scrolling top to bottom moves through all 8 positions with no jump cuts or stutter, confirmed with a screenshot or recording at each beat

Don't start on the burn/dissolve shader, the sketch-to-mesh morph, or any real asset until this scaffold is verified — those get built and tested in isolation next, per the build order, then wired in.

## Task 1 correction — read before continuing

Rejected as submitted. The camera rig itself — the Catmull-Rom spline interpolation, the 8 beat positions/lookAt/FOV values, the ScrollTrigger + Lenis wiring — is correct engineering and stays as-is. Everything visible on screen beyond the canvas is a debug dashboard nobody asked for, and it doesn't ship. Fix exactly as follows. Nothing else gets added.

**Delete entirely** (markup and CSS): `.hud-header`, `.hud-brand`, `.hud-telemetry-pill`, `.beat-card` and its contents, `.beat-nav` and every `.nav-dot`, `.bottom-progress-bar`. Drop the JetBrains Mono font import — it was only used by these elements.

**Palette, final:** background `#05060B`, flat, no gradient. One accent, `#FF8A3D`, used anywhere something needs to read as lit — box wireframes, any glow. Text `#F4F1EA` where text exists at all. No cyan, no purple, no blue, no second accent, ever.

**Placeholder boxes:** plain `BoxGeometry`, wireframe `MeshBasicMaterial`, color `#FF8A3D`, identical for all 8 beats — no per-beat color-coding, no billboard labels, no landing rings, no local lights.

**The 8 `.chapter-section` elements:** keep them, empty, for scroll-anchoring only. No title, tag, body copy, cue text, card background, blur, or border. Real copy (see Copy section above) is wired in on a later content-pass task, not this one.

**Verification, replaces the HUD:** `console.table()` the beat number, camera position, lookAt target, and FOV at each of the 8 checkpoints. Screenshots at each checkpoint, saved to a local `/verification` folder via your own browser automation. None of this — no numbers, no screenshots, no debug text — renders inside the page. What a visitor sees: a black screen and one amber wireframe box moving through camera positions as they scroll. Nothing else.

**Standing rule, this task and every task after:** if it isn't explicitly specified in this brief, it does not get built. No navigation aids, no HUD, no decorative cards, no extra colors, no placeholder copy standing in for real copy. A genuine open decision gets flagged and asked, never invented.

## Task 2 for Antigravity

Task 1 verified — camera rig confirmed clean against every point in the correction above. Task 2 builds the two remaining interaction primitives, each in isolation, on their own throwaway test pages. Neither gets wired into the Task 1 camera-rig page yet. Same standing rule as the Task 1 correction: nothing not listed here gets built, ask instead of inventing.

### 2A — Hold-to-proceed gesture (`hold-test.html`)

- One circle, centered, on the `#05060B` background: idle state is a thin `#FF8A3D` stroked ring with the label "HOLD" in `#F4F1EA` beneath it. No other UI on the page.
- On pointerdown (mouse and touch), a radial progress ring fills clockwise in `#FF8A3D` over exactly 1200ms.
- Released early: ring animates back to empty over 300ms, nothing else happens, no error state, no shake.
- Held to completion: fire a `hold-complete` event, log `"hold-complete"` to console, button flashes full-opacity once as the only completion feedback.

### 2B — Burn/dissolve shader (`burn-test.html`)

- A `ShaderMaterial` full-screen quad, noise-threshold alpha dissolve, applied to a plane filled solid `#FF8A3D` sitting over the `#05060B` background (stand-in for whatever art it wraps later).
- Dissolve runs over exactly 800ms; the leading edge of the dissolving region gets a thin bright rim (still `#FF8A3D`, just higher opacity/intensity — no new color) as it burns away, then the plane is fully gone.
- Trigger for this isolated test only: spacebar or a plain button, both thrown away once this task closes — neither ships.

### Combined check, before calling this task done

On one page, wire 2A's `hold-complete` event straight into 2B's burn trigger — hold completes, burn plays immediately, no gap, no second confirmation step. This is the exact handoff Task 3 (the real Prank page) will reuse.

### Explicitly not in scope for this task

No wiring into the Task 1 camera-rig page. No "did you really think my skills are this bad?" text — that's copy, later. No real Hello Kitty prank visuals. This task is the two mechanics and their combined trigger, nothing further.

### Verification

Screenshots: 2A idle, 2A at \~50% hold, 2A on completion flash, 2B at \~50% dissolved, 2B fully dissolved. Console confirms `hold-complete` fires exactly once per hold (not once per frame), and the burn's measured duration is 800ms ± 50ms.

**Addendum — 2B rim color:** the 2.8x intensity multiply clips to pale cream instead of a hot amber edge. Lower it to roughly 1.4–1.6x, and bias the boost toward red over green so blue never approaches the red channel's value — the rim has to stay visibly orange, never drift toward white-yellow. Reverify with one updated `2B_dissolved_50pct.png`.

## Task 3 for Antigravity

Build the real Prank (Part 1), wired to 2A and 2B exactly as verified in Task 2 — no new interaction primitives, just real content dropped into the mechanics that already work.

### Where this lives

Extends `index.html` from Task 1. The Prank is a full-viewport layer sitting in front of the existing camera-rig scroll container on page load. When the burn completes, remove the Prank layer from the DOM entirely — don't just hide it — and reveal the rig already at Beat 1 (scroll position 0) underneath. No page navigation, no reload.

### Prank layer — visual spec

A separate, deliberately different palette from the rest of the site, bounded to exactly this set: background `#FFD1E8`, accent `#FF5C8A`, ink `#2B1420`. Don't use the site's real palette anywhere in this layer except the hold button below.

- Heading, centered top third: "tarushi's cute corner ✨" — Google Font `Fredoka`, weight 600.
- One original bow or star mascot shape, built from scratch in CSS/SVG. Do not reference, copy, or approximate any existing trademarked character design, Sanrio's Hello Kitty included — an original rounded bow silhouette in the accent color is enough.
- Fake visitor counter: "you are visitor #000001 \~☆", static text, no real count.
- Fake guestbook button, decorative only — a small "aw thanks!" tooltip on click, nothing more.
- Lightweight sparkle cursor trail: small star-shaped particles spawn at the pointer and fade over \~600ms as it moves. CSS/JS only, no external library.

### The hold button — do not restyle it

Reuse 2A exactly as built in Task 2, unmodified, real `#FF8A3D` / `#F4F1EA` colors included — don't reskin it to match the pink palette. That's deliberate: it's the one thing on the page that reads as subtly wrong, foreshadowing the reveal. Only change is the label, "HOLD" → "HOLD FOR SURPRISE".

### Sequence, exact timings

1. Page loads, kawaii layer fully visible, sparkle trail active, hold button idle.
2. Hold completes (1200ms, per 2A) → the pink layer desaturates to grayscale via CSS filter over 400ms; sparkle trail and guestbook/counter stop animating.
3. Centered text fades in over the desaturated layer, `#F4F1EA` on grey: "did you really think my skills are this bad?" — holds 1200ms.
4. Burn/dissolve (2B, unmodified, 800ms, rim-color addendum applied) plays over the whole desaturated layer.
5. On completion, remove the Prank layer from the DOM. The Task 1 rig is visible underneath, already at Beat 1.

### Explicitly not in scope

No B2 or fighter-jet models — Beats 4 and 5 stay the placeholder wireframe boxes from Task 1. No ScrapBook. No sound. No changes to the rig's camera math.

### Verification

Screenshots: Prank idle, mid-hold (\~50%), punchline text on the desaturated layer, mid-burn (\~50% dissolved), and the handoff frame showing Beat 1 of the rig fully revealed with the Prank layer confirmed removed from the DOM (inspect the element tree, don't just eyeball it).

## Task 4 for Antigravity

Supersedes the earlier procedural-geometry version of this task. Farzooque supplied a real `B2_Bomber.obj` — use that instead. It's a Roblox Studio scene export, not a clean model on its own, so this task is import-and-clean-up, not just import.

### Strip before use

The file contains two groups that are not the aircraft and must be deleted entirely: `Spawnlocation1`, `Spawnlocation2` (a Roblox spawn marker) and `Baseplate1`, `Baseplate2` (a flat ground platform, roughly 2048×2048 units — verify by bounding box: these four groups sit wildly outside the bounding box of every other group, which is how to tell them apart if group names ever differ from this list). No `.mtl` file was provided and none is needed — ignore the `mtllib`/`usemtl` directives in the file, materials are fully overridden in the next step regardless.

### Normalize the geometry

1. Load the `.obj`, discard the four groups above, keep the remaining \~39 groups (cockpit, canopy glass, radar domes, landing-gear brake pads, left/right intake covers, and the main body/wing shell).
2. Compute the combined bounding box of what's left, translate all geometry so it's centered on local origin.
3. Compute the model's wingspan axis (the longest horizontal span) and scale uniformly so that span becomes exactly `40` world units. Compute the scale factor from the actual loaded geometry's measured span — don't hardcode a multiplier.

### Determine orientation — verify, don't assume

Render the normalized model alone (no placement yet, on the site's background) from directly above and directly from the side. Screenshot both. Identify which end is the nose (tapered, pointed) versus the tail end (wider, where the intake covers and brake pads/landing-gear detail cluster). Rotate about the vertical axis so the nose points toward local -Z — that's the direction the whole 8-beat sequence flies. Do not place the model into Beat 4 until this is confirmed from the renders.

### Materials and lighting — unchanged from the original spec

Override every original material with one `MeshStandardMaterial`, color `#05060B`, roughness `0.6`, metalness `0.1`, applied to the whole model. Add an `EdgesGeometry` outline pass, `LineBasicMaterial` color `#FF8A3D`, so it reads as a dark body with a glowing accent edge — same language as the wireframe boxes it's replacing. Lighting stays the two lights already used elsewhere: one `DirectionalLight` `#FF8A3D` at intensity `0.4` rim-lighting from behind/above, one neutral `AmbientLight` at intensity `0.15`.

### Placement

Position at Beat 4's existing placeholder coordinates, `(-10, 16, -350)`. Roll `20°` about Z for the banking look, on top of whatever Y-rotation the orientation check above required. Remove the old Beat 4 placeholder box from the scene graph — don't leave it underneath the new model.

### Explicitly not in scope

No morph-from-sketch animation. No fighter jet — Beat 5 stays a placeholder box. No changes to any other beat, the camera rig, or the Prank layer.

### Verification

The two orientation-check renders (top-down, side) from above. Then, post-placement: a screenshot at Beat 4's camera position from the front and from a 3/4 angle. Console confirmation that the Roblox baseplate/spawn groups were never added to the scene, and that the old placeholder box is gone, not hidden underneath.

## Task 5 for Antigravity

No source file exists for the fighter jet, so this one goes back to hand-specified geometry — same technique as the original B2 draft, now applied here. Static model only, no morph animation (that's Task 6). Replaces the Beat 5 placeholder box.

### Geometry — exact silhouette, don't reinterpret

A `THREE.Shape` in the local X-Z plane, nose toward +Z, centered on the origin. Trace these points in order, then close back to point 1:

1. (0, 11) — nose tip
2. (1.3, 7.5) — right canopy edge
3. (0.9, 2.5) — right fuselage narrow point / wing root
4. (7, -2) — right wingtip
5. (2.2, -5) — right wing trailing edge
6. (1, -9.5) — right tail edge
7. (0, -11) — engine nozzle center
8. (-1, -9.5) — left tail edge
9. (-2.2, -5) — left wing trailing edge
10. (-7, -2) — left wingtip
11. (-0.9, 2.5) — left fuselage narrow point
12. (-1.3, 7.5) — left canopy edge

Extrude with `THREE.ExtrudeGeometry`: depth `0.6`, `bevelEnabled: true`, `bevelThickness: 0.1`, `bevelSize: 0.1`, `bevelSegments: 2`. One shape, one extrude, same as the B2 draft's approach.

### Scale

Target wingspan `16` world units. The raw shape above measures `14` units across, so the scale factor is `16 / 14`, but compute it from the actual constructed geometry rather than hardcoding — same discipline as Task 4. Deliberately smaller than the B2's 40-unit wingspan: keeps the hero aircraft and the escort readable as different sizes.

### Materials and lighting — same as the B2, no new colors

Body: `MeshStandardMaterial`, color `#05060B`, roughness `0.6`, metalness `0.1`. Edge outline: `EdgesGeometry` + `LineBasicMaterial`, color `#FF8A3D`. Reuse the two lights already in the scene from Task 4 — don't add a third light or a new color anywhere.

### Placement

Position at Beat 5's existing placeholder coordinates, `(12, 12, -495)`. Nose toward -Z, same convention as the B2. Roll `15°` about Z — deliberately different from the B2's 20°, so the two aircraft don't read as identical banking; Beat 5 is an escort pass, not the hero moment. Remove the old Beat 5 placeholder box from the scene graph, don't leave it underneath.

### Explicitly not in scope

No morph animation — Task 6. No changes to Beat 4, the B2 model, the camera rig, or the Prank layer.

### Verification

Screenshot at Beat 5's camera position, front and 3/4 angle. Console confirms the old Beat 5 placeholder box is gone, not hidden underneath the new model.

## Task 5 correction — read before continuing

Verified against the real files: every number matches spec exactly, so this isn't an execution problem, it's a design flaw in the spec itself. A flat `0.6`-deep extrusion was right for the B2 — a flying wing genuinely is that flat — but a fighter jet needs a rounded fuselage with real volume, and from the Beat 5 escort angle the model currently reads as a thin blade, not a jet. Don't touch the existing wing/canopy shape or its code — it's correct and stays. Add a fuselage body alongside it.

### Fuselage — new geometry, added to the same jet group

A `THREE.LatheGeometry`, `segments: 16`, revolved from this radius-vs-axial-position profile (`Vector2(radius, axialPosition)`), in the same local units and the same -11-to-11 axial range as the existing wing shape so it lines up without any extra scale math:

1. (0.05, -11) — engine nozzle, nearly closed
2. (0.65, -9)
3. (1.05, -5)
4. (1.25, -1)
5. (1.25, 3)
6. (1.0, 6)
7. (0.6, 8.5)
8. (0.05, 11) — nose tip, nearly closed

Same `rotateX(Math.PI / 2)` treatment already used elsewhere in this file to map the lathe's revolve axis onto world Z. Add this mesh as a sibling of the existing wing mesh inside the same fighter-jet group — it inherits the group's existing position, rotation, and scale automatically, no new transform math.

### Material — reuse, don't create a new one

Same `fighterBodyMaterial` already defined for the wing shape. Add its own `EdgesGeometry` + the same `#FF8A3D` `LineBasicMaterial` outline, consistent with every other part of the scene.

### Explicitly not in scope

No change to the wing/canopy shape, its material, or its transform. No change to Beat 4, the B2, the camera rig, or the Prank layer.

### Verification

Re-capture both Beat 5 screenshots (front and 3/4 angle). The 3/4 angle is the one that matters most here — confirm the fuselage now reads as a tapered body with visible thickness from that angle, not a flat sliver.

## Task 5 — second addendum: yaw for a broadside read

The fuselage fix is correct and stays — it does have real volume now. The remaining problem is Beat 5's fixed camera looks almost straight down the jet's own length axis, so it foreshortens to a sliver regardless of fuselage roundness. Fix the jet's orientation, not the camera — the rig stays untouched.

Change `rotation.y` from `Math.PI` (180°) to `THREE.MathUtils.degToRad(230)`. This angles the jet across the frame instead of heading straight at/away from the camera — which reads better anyway, a fighter crossing the shot at an angle is a more dynamic escort pass than one coming in dead-on. Roll stays `15°` about Z, position stays `(12, 12, -495)`, nothing else about the model changes.

### Verification

Re-capture both Beat 5 screenshots. Looking for the fuselage's tapered profile and both wings clearly visible in silhouette, not foreshortened into a line.

## Task 6 for Antigravity

Both aircraft currently appear fully solid the instant their beat starts. This makes each one resolve in gradually instead: outline first, body filling in after — the accent-colored edges are already sitting there like a sketch, and the dark body fills in like it's becoming real.

### Behavior

Use the same normalized scroll-progress signal already driving the camera rig (0–1 across the whole 8-beat sequence). For each aircraft's own body material only — not its `EdgesGeometry` outline, which stays fully opaque throughout:

- **B2 (Beat 4, progress range ≈ 0.375–0.5):** body `opacity = 0` for any progress below `0.375`. Ramp linearly from `0` to `1` across progress `0.375` to `0.4167` (the first third of the beat's range). Hold at full opacity `1` from `0.4167` onward.
- **Fighter jet (Beat 5, progress range ≈ 0.5–0.625):** same pattern, shifted to that beat's range — `opacity = 0` below `0.5`, ramps `0→1` across `0.5` to `0.5417`, holds at `1` from there on.

Both materials need `transparent: true` for this to work; set it on both body materials now if it isn't already there.

### Explicitly not in scope

No change to either model's geometry, color, placement, or rotation. No change to the edge outlines — they don't fade, only the body fill does. No changes to the camera rig, the Prank layer, or any other beat.

### Verification

Four screenshots per aircraft, at progress values 0.37 (edges only, body invisible), 0.40 (partway through the fade), 0.42 (fully solid) for the B2, and the equivalent three points (0.49, 0.52, 0.55) for the jet. Confirm the edge outline is present and unchanged across all of them — only the body's opacity should be moving.

## Task 7 for Antigravity

Beat 7's name reveal, using the copy already finalized above (Copy — Beat 1 & Beat 7). DOM text overlay on top of the WebGL canvas, not 3D text — reuse whatever font/color is already set up for the chapter captions from Task 1/3, don't introduce a new typeface.

### Progress range and four stages

Beat 7 spans progress `0.75`–`0.875`. Four states in sequence; each one's text and caption must fully reach opacity `0` before the next stage's fade-in begins, no overlap.

1. **Φ** — text fades in (opacity 0→1) over `0.75`–`0.755`, centered, large, color `#F4F1EA`. At `0.77`–`0.78`, an accent `#FF8A3D` strikethrough line animates left to right across it (`scaleX` 0→1, 3–4px thick). Caption beneath, smaller: "what my phone thinks your name is.", fades in with the main text.
2. **taNushi** — same pattern, shifted: text fades in `0.79`–`0.795`, strike draws `0.81`–`0.82`. Caption: "still wrong."
3. **Tarushi** — text fades in `0.83`–`0.84`, settles with a soft glow (a brief `text-shadow` pulse in `#FF8A3D`) instead of a strike — this one stays intact. Caption: "there she is."
4. **Happy Birthday** — prior text/caption fade out, "Happy Birthday" fades in centered, larger scale than the name states, holds through the end of the range at `0.875`.

### Explicitly not in scope

No change to either aircraft, the camera rig, the Prank layer, or any other beat. No sound.

### Verification

Four screenshots, one at each stage's settled point: `0.78`, `0.82`, `0.845`, `0.87`.

## Correction — Tasks 6 and 7 progress windows

Found this while scoping the formation jets below, not something either task's own verification could have caught on its own. Task 1's camera path is scrubbed with `camSpline.getPointAt()`, and in Three.js `getPointAt` maps progress to arc length along the curve, not to the spline's raw parameter. That means the 8 camera stations do not sit at even eighths of progress — they sit wherever cumulative distance along the curve puts them, and the curve moves at very different speeds through different stretches.

Real station positions, computed from the same 8 camera coordinates already in this brief:

| Station | Progress |
| --- | --- |
| 1 | 0.0000 |
| 2 | 0.0719 |
| 3 | 0.2201 |
| 4 | 0.4253 |
| 5 | 0.5893 |
| 6 | 0.7543 |
| 7 | 0.9050 |
| 8 | 1.0000 |

Every screenshot already delivered for Tasks 6 and 7 is internally correct — the fade and reveal formulas matched the progress values I specified at the time. The problem is those progress values didn't correspond to where the camera actually is at Beat 4, 5, or 7 during real scrolling. Both tasks need their windows corrected to the real numbers above; nothing else about either task changes.

### Task 6 — corrected windows

- **B2 (Beat 4, real range 0.4253–0.5893):** body opacity `0` below `0.4253`, ramps `0→1` across `0.4253`–`0.4800` (first third of the real range), holds `1` from there.
- **Fighter jet (Beat 5, real range 0.5893–0.7543):** opacity `0` below `0.5893`, ramps `0→1` across `0.5893`–`0.6443`, holds from there.

### Task 7 — corrected windows

Beat 7's real range is `0.9050`–`1.0000` (width `0.0950`, not `0.125`) — the whole reveal happens later and faster than originally specified. Same four stages, same relative proportions within the beat, rescaled to the real window:

1. **Φ** — fades in `0.9050`–`0.9088`, strike `0.9202`–`0.9278`.
2. **taNushi** — fades in `0.9354`–`0.9392`, strike `0.9506`–`0.9582`.
3. **Tarushi** — fades in `0.9658`–`0.9734`, glow, no strike.
4. **Happy Birthday** — fades in `0.9886`–`1.0000`, holds.

Captions, fonts, and colors are unchanged from the original Task 7 spec — only these six numbers move.

### Verification

Re-run both tasks' verification screenshots at these corrected progress values in place of the originals.

## Task 8 for Antigravity

Start the ScrapBook as a standalone page and build only its foundation plus one spread, the Flight Log, so the look can be checked before the other spreads get built on top of it. Independent of Task 7 — the two can run in parallel.

### Where this lives

New files only: `scrapbook.html`, `css/scrapbook.css`, `js/scrapbook.js`, and `assets/scrapbook/`. Do not touch `index.html`, `js/main.js`, or `js/prank.js`. It's a separate page on purpose: it keeps the verified camera rig untouched, and after the birthday this is the page that becomes her site's home. The handoff from the 3D sequence into this page is a later task.

### Palette and fonts — bounded, nothing else

| Use | Value |
| --- | --- |
| Page background (paper) | `#EFE6D2` |
| All text and borders (ink) | `#1F1A17` |
| Tape strips only | `#FF8A3D` — same amber as the 3D sequence, so the two pieces feel related |
| Sheet and polaroid frames | `#FFFFFF` |
| Ticket stub | `#F7F0DF` |

Fonts, both from Google Fonts: `Caveat` 600 for titles and notes, `Special Elite` 400 for stamps, the ticket, and the subtitle. Paper texture with no image file: the `#EFE6D2` background plus an inline-SVG `feTurbulence` noise (`baseFrequency` 0.8, `numOctaves` 2) as a data-URI overlay at 8% opacity. No other colors anywhere on this page.

### Assets

| Source file (from the artworks zip) | Save as | Processing |
| --- | --- | --- |
| `WhatsApp Image 2026-09-17 at 4.29.08 PM.jpeg` | `assets/scrapbook/flight-b2-top.jpg` | Rotate 90° clockwise — the raw file has the nose pointing left, it must point up |
| `WhatsApp Image 2026-09-17 at 4.29.09 PM (2).jpeg` | `assets/scrapbook/flight-fighter-top.jpg` | None, already nose-up |
| `WhatsApp Image 2026-09-17 at 4.29.09 PM.jpeg` | `assets/scrapbook/flight-fighter-side.jpg` | None |

For all three: longest edge max 1600px, JPEG quality 82, strip metadata. View each output and confirm the orientation matches the table before using it.

**Asset rule for every ScrapBook task:** use only files named in this brief. Never use any `Screenshot_*` file, or any photo showing other people — the video-call screenshots show other students' names and faces, and this page becomes a public site.

### Components

| Class | Look |
| --- | --- |
| `.sheet` | White rectangle, 10px padding, image shown whole (`object-fit: contain`), `box-shadow: 0 10px 24px rgba(31,26,23,0.22), 0 2px 4px rgba(31,26,23,0.18)`, rotation set through a `--rot` custom property |
| `.tape` | 96×28px, `#FF8A3D` at 85% opacity, `clip-path: polygon(3% 0, 97% 0, 100% 50%, 97% 100%, 3% 100%, 0 50%)`, `0 1px 2px rgba(0,0,0,0.2)` shadow, absolutely positioned across a sheet corner, rotated 30–40° |
| `.note` | `Caveat` 600, 28px, ink color, no background, rotated 1° either way |
| `.stamp` | `Special Elite`, uppercase, `letter-spacing: 0.2em`, 2px solid ink border, `6px 14px` padding, rotated -2° |
| `.ticket` | 320px wide, `#F7F0DF`, left border `2px dashed` ink at 40% opacity (the perforation), `Special Elite` 14px uppercase, three lines of text, rotated 4° |

### Cover (first viewport)

Full viewport, paper background. Centered: "tarushi's scrapbook" in `Caveat` 600, `clamp(56px, 10vw, 128px)`. Under it, `Special Elite` 16px: "vol. 1 · 09.10.2026". One `.tape` strip across the top of the title, rotated -4°. Bottom center: a small "↓" in `Caveat` 40px that bobs `translateY` 0→8px on a 1.6s ease-in-out loop. Nothing else.

### Flight Log spread (second section)

**Desktop, 900px and wider:** section `min-height: 100vh`, `padding: 10vh 5vw`, inner container `max-width: 1200px` centered, 12-column grid, `gap: 24px`.

- `.stamp` reading "FLIGHT LOG": `grid-column: 1 / -1`, aligned left, `margin-bottom: 5vh`.
- B2 sheet (`flight-b2-top.jpg`): `grid-column: 1 / span 5`, `--rot: -3deg`, two tapes on the top-left and top-right corners.
- Fighter top sheet (`flight-fighter-top.jpg`): `grid-column: 6 / span 4`, `margin-top: 6vh`, `--rot: 2deg`, one tape top-center.
- Fighter side sheet (`flight-fighter-side.jpg`): `grid-column: 10 / span 3`, `margin-top: 14vh`, `--rot: -2deg`, two tapes.
- A `.note` directly under each sheet, in order: "B-2 Spirit, top view. pen on paper." / "fighter, top view." / "fighter study, pen."
- `.ticket` at the bottom left, `grid-column: 1 / span 4`, `margin-top: 8vh`, three lines: "FLIGHT LOG · 09.10.2026" / "PASSENGER: TARUSHI" / "FROM: DEL → TO: NDA".

**Phone, under 900px:** single column, each item `88vw` wide, `margin-bottom: 48px`, every rotation halved.

### Motion

Reveal on scroll with `IntersectionObserver` only: each element starts at `opacity: 0` and `translateY(24px)`, and moves to `opacity: 1` and `translateY(0)` over 600ms ease-out once 20% of it is visible, staggered 120ms between siblings within a spread. Disabled under `prefers-reduced-motion`. No GSAP, no Lenis, no other library on this page.

### Explicitly not in scope

No other spreads, no photos, no videos, no Spotify, no page-flip effect, no sound, no handoff from the 3D page. No changes to any existing file.

### Verification

Screenshots at 1440×900 and at 390×844 (phone) of the cover and of the Flight Log fully revealed. A directory listing of `assets/scrapbook/` showing only the three files above. Console shows zero errors. Combined size of the three images under 1.5 MB.

## Task 9 for Antigravity — Beat 6 formation escorts

Two real Sketchfab models for this beat — Farzooque supplied `f16-c_falcon` and `mig-35_-_fighter_jet_-_free`, both glTF. Same import-and-normalize discipline as Task 4's B2, but each model needs its own orientation check: their raw bounding boxes don't share a consistent axis convention with each other or with the B2, so nothing about axis or scale can be assumed here — it has to be checked per model.

### License and attribution — required, not optional

- **F-16C Falcon** by Carlos.Maciel: CC-BY-4.0, commercial use allowed, credit required.
- **MiG-35** by bohmerang: CC-BY-NC-SA-4.0, non-commercial only, credit required, share-alike if the model itself is redistributed. Non-commercial is already true of this project and of the Vercel Hobby plan, so this is compatible as-is — it would only become a problem if the site were ever monetized later.

Add a small, muted footer to the ScrapBook page (the page that persists after the birthday) with both credit lines verbatim:

> This work is based on "F16-C Falcon" (https://sketchfab.com/3d-models/f16-c-falcon-4bc2ff75dc584af2afd0aa6bd8b79015) by Carlos.Maciel (https://sketchfab.com/Carlos.Maciel) licensed under CC-BY-4.0 (http://creativecommons.org/licenses/by/4.0/)
>
> This work is based on "MiG-35 - Fighter Jet - Free" (https://sketchfab.com/3d-models/mig-35-fighter-jet-free-1dcea306e8a14ed4ab4d11a819cb6676) by bohmerang (https://sketchfab.com/bohmerang) licensed under CC-BY-NC-SA-4.0 (http://creativecommons.org/licenses/by-nc-sa/4.0/)

### Normalize each model independently

For each of the two models, separately:

1. Compute the bounding box, translate so it's centered on local origin.
2. Render top-down and side orthographic views of the recentered, unscaled model. From these, determine which axis is actually the nose-tail length axis — do not assume X or Z, or inherit Task 4's convention — and which end is the nose.
3. Rotate so the nose points local -Z, up is local +Y.
4. Scale uniformly: F-16 to `17` world units wingspan, MiG-35 to `20` world units wingspan. Both stay smaller than the B2's `40`; MiG-35 slightly larger than the F-16, roughly matching their real relative sizes.

### Materials — override, discard the originals

Both models carry their own PBR textures. Ignore them completely, for the same reason as everywhere else on this site: override every material on both with the established treatment — `MeshStandardMaterial`, color `#05060B`, roughness `0.6`, metalness `0.1`, plus an `EdgesGeometry` outline in `#FF8A3D`. No embedded texture or image file from either package gets used. This keeps both new aircraft visually identical in treatment to the B2 and the existing fighter jet, rather than introducing full-color photoreal aircraft into an otherwise two-color scene.

### Placement — Beat 6 formation

Beat 6's camera is `(0, 16, -600)` looking at `(0, 8, -680)`, FOV `45°` — already in this brief, untouched. Position the two escorts flanking that target point, nose toward -Z:

- F-16: `(18, 10, -665)`, roll `-15°` about Z (banking outward, right).
- MiG-35: `(-18, 10, -665)`, roll `15°` about Z (banking outward, left).

The B2 from Beat 4 stays where it is and is not relocated here — this is a fresh formation of the two escorts arriving at the hangar, not a reunion shot with the B2.

### Reveal, same mechanic as Task 6

Same edges-first-then-fill treatment, using Beat 6's real progress range from the correction above (`0.7543`–`0.9050`). Both aircraft: body opacity `0` below `0.7543`, ramp `0→1` across `0.7543`–`0.8045`, hold from there. Same timing for both, no stagger.

### Explicitly not in scope

No hangar structure yet — that's its own task. No change to the B2, the existing fighter jet, the camera rig, the Prank layer, or any other beat.

### Verification

Orientation-check renders (top-down, side) for each model, before placement. A Beat 6 screenshot showing both escorts in formation. Console confirms both models' original materials/textures were never loaded, and states which local axis was identified as the length axis for each model, since it isn't assumed.

## Task 10 for Antigravity

Beat 1 — the opening shot, currently still the placeholder wireframe box. Four pieces: the event horizon core, a starfield, a lensing warp on the stars near the hole (position-based, not a post-process shader — keeps this out of the render pipeline that's already working), and the accretion disk. Replace Beat 1's placeholder box with this assembly.

### Event horizon core

`SphereGeometry(14, 32, 32)`, `MeshBasicMaterial({ color: 0x05060B })`, positioned at `(0, 0, 0)` — Beat 1's existing lookAt target. Deliberately the same color as the page background: it should read as an absence, not an object — the silhouette comes from blocking the stars behind it and from the disk around it, not from its own material.

### Starfield

`THREE.Points`, 800 vertices, positions randomly distributed in a spherical shell between radius `60` and `600` from the origin. `PointsMaterial({ color: 0xF4F1EA, size: 1.5, sizeAttenuation: true })`. Generated once, not animated.

### Lensing warp — applied once, at generation time, to each star's position

For every star position `p = (x, y, z)` with distance `d` from the origin:

```
if (d < 120) {
  bendAngle = (1 - d / 120) * 0.8; // radians, up to ~0.8 rad for stars nearest the hole, 0 at d=120
  newX = x * cos(bendAngle) - z * sin(bendAngle);
  newZ = x * sin(bendAngle) + z * cos(bendAngle);
  p = (newX, y, newZ);
}
```

This is the entire lensing effect — a one-time position bend, not a runtime distortion shader. Stars farther than 120 units are untouched.

### Accretion disk

`THREE.TorusGeometry(20, 5, 16, 64)`, centered at `(0, 0, 0)`, tilted `rotation.x = degToRad(75)` for a dramatic near-edge-on angle. `ShaderMaterial` reusing the exact FBM noise function already written for the 2B burn/dissolve shader — same noise code, new use: drive a color mix instead of a dissolve threshold. Mix from full-intensity `#FF8A3D` at the torus's inner edge to that same color at 35% intensity (multiply RGB by `0.35`) at the outer edge, modulated by the noise for a turbulent, non-uniform glow. Rotate the mesh continuously, `rotation.z += 0.15 * deltaTime` per frame.

### Caption

The Beat 1 line from the Copy section above ("some people just pull everything toward them."), same DOM-overlay treatment as every other caption — `#F4F1EA`, centered. Beat 1's real progress range is `0`–`0.0719` (from the correction above). Fade in `0`–`0.02`, hold `0.02`–`0.055`, fade out `0.055`–`0.0719`.

### Explicitly not in scope

No changes to any other beat, the camera rig, the Prank layer, or the ScrapBook. Whether the starfield and black hole should be hidden once the camera moves into Beat 3's atmosphere is a later concern, not this task — leave them rendering for now.

### Verification

A screenshot at Beat 1's camera position showing the full assembly — core, disk, and warped stars. A close-up screenshot of the lensing bend specifically (stars visibly curving around the core, not just scattered randomly). The caption at its held state (`~0.04`). Console confirms the old Beat 1 placeholder box is gone.

## Task 10 correction — read before continuing

Every number in the verification table passed, but the screenshots don't show a black hole — they show a solid, lit orange donut. The numeric checks confirmed radii and rotation speed; they couldn't have caught that the visual goal wasn't met, which is why I'm looking at the renders directly and not just the pass/fail table. Two specific problems, both fixable without touching the geometry or placement already verified.

### Problem 1: the disk has no turbulence, no radial gradient, and a stray gap cut into one side

The brief said to reuse the burn/dissolve shader's noise **function** — not its discard/threshold logic. The current result looks like ordinary lit `MeshStandardMaterial` shading (a highlight on top, shadow underneath) with a chunk missing on one side, which is what happens if the burn shader's alpha-cutout got carried over along with its noise function. Fix:

- The fragment shader uses the `fbm()` noise function only — nothing else from the burn shader's logic comes along with it.
- **No `discard` anywhere in this shader.** Every fragment across the full ring renders; the gap in the current render should disappear entirely once discard is removed. Confirm `TorusGeometry`'s `arc` parameter is left at its default (`Math.PI * 2`) — a full ring, not a partial one.
- Color formula, computed per-fragment: `radialT` = normalized distance from the torus's inner edge (`0`) to outer edge (`1`). `finalColor = mix(vec3(0.35) * accentColor, accentColor, radialT) * (0.6 + 0.4 * fbmNoise)`, where `accentColor` is `#FF8A3D` as a 0–1 vec3. This is the entire color logic — no discard, no threshold, no separate "dissolve" step.
- **Additive glow, not lit shading:** `ShaderMaterial({ transparent: true, blending: THREE.AdditiveBlending, depthWrite: false })`. This is what makes it read as light being emitted rather than a solid surface being lit by the scene's directional light — the flat, shaded-donut look in the current render is the tell that this wasn't additive.

### Problem 2: the void doesn't read as a void

With the torus's inner edge (`20 - 5 = 15`) barely larger than the core's radius (`14`), the core sits almost flush against the disk with no visible gap — so there's nothing distinguishing "the dark core" from "the disk just isn't there yet." Widen the gap: change the torus to `TorusGeometry(22, 4, 16, 64)` (inner edge `18`, outer edge `26`), keeping the core at radius `14`. That leaves a clear 4-unit band of open space between the core's edge and the disk's inner edge, where background and stars show through — that visible dark gap against the bright ring is what actually sells the silhouette, not the core's own invisibility.

### Explicitly not in scope

No change to the core's position, the starfield, the lensing warp, the disk's tilt or rotation speed, or the caption — all of those are correct and stay as built.

### Verification

Re-capture `beat1_full_assembly.png` and `beat1_lensing_closeup.png`. Looking for: visible turbulent variation across the ring (not a flat gradient), no gap anywhere in the ring's circumference, a clearly visible dark band between the core and the disk's inner edge, and the overall disk reading as glowing rather than shaded. If the lensing bend still isn't visually obvious in the closeup at this larger disk size, add one temporary debug frame — render the starfield once with the bend disabled and once with it enabled, same camera position, so the difference is actually checkable by eye instead of inferred from the vertex count.

## Task 10 — second correction

The shader fix worked — the re-captured renders show real turbulence and the gap band is there, confirmed in code too (`discard` is genuinely gone, the color formula matches exactly). But the disk still doesn't read as a black hole: at `75°` tilt it's nearly edge-on to Beat 1's camera, which compresses the torus's hole into a thin bright seam down the middle of what now looks like a glowing tube, not a ring with a dark center. This is a mistake in my original tilt choice, not anything to do with the shader work just done.

### Fix

Change `rotation.x` from `degToRad(75)` to `degToRad(20)`. Beat 1's camera at `(0, 10, 85)` looks almost straight down -Z at the origin with only a slight downward angle — a shallow tilt presents the disk close to face-on to that camera, which is what actually makes the hole (and the core sitting inside it) read clearly, rather than fighting the camera's own angle. Nothing else about the disk — geometry, shader, colors, rotation speed — changes.

### Lensing check, still unresolved

Looking at both the warped and unwarped comparison frames myself, I can't confidently tell them apart — whatever bend exists isn't visually obvious at this crop, so I'm not calling this verified yet, but I'm also not assuming it's broken. Rather than another loose "compare two screenshots" request: render a third debug frame, same camera position, with every lensed star (the 371 within `d < 120`) tinted a distinct color (e.g. the prank's `#FF5C8A`) so the bent ones are identifiable on sight against the unwarped white stars, instead of relying on spotting a subtle position shift.

### Verification

Re-capture `beat1_full_assembly.png` at the new tilt — looking for a clearly visible dark circular gap between the core and the glowing ring. The new tinted-star debug frame for the lensing check.

## Task 10 — starfield correction

Uniform-size square dots read as particles, not stars. Fix is a round glow sprite plus size/brightness variation — same 800 positions and the same lensing warp logic, unchanged, just how they're drawn.

### Sprite texture

Generate once at startup: a 64×64 `Canvas`, radial gradient from `rgba(255,255,255,1)` at center to `rgba(255,255,255,0)` at the edge, converted to a `THREE.CanvasTexture`. Used as `map` on every star material below — the material's own `color: 0xF4F1EA` tints it, so stars stay the established off-white, the texture just gives them a soft round falloff instead of a hard square edge.

### Three layers, not one

Split the existing 800 star positions into three separate `THREE.Points` objects at generation time, by a weighted random roll per star — don't change the position generation or the lensing warp, only how each star is grouped afterward:

| Layer | Share | Size | Opacity |
| --- | --- | --- | --- |
| Dim | 60% (\~480 stars) | `1.0` | `0.55` |
| Mid | 30% (\~240 stars) | `1.8` | `0.8` |
| Bright | 10% (\~80 stars) | `3.0` | `1.0` |

Each layer: `PointsMaterial({ map: starSprite, color: 0xF4F1EA, size, opacity, transparent: true, blending: THREE.AdditiveBlending, depthWrite: false, sizeAttenuation: true })`.

### Explicitly not in scope

No change to star count, distribution, the lensing warp math, or anything else in Task 10.

### Verification

Re-capture `beat1_full_assembly.png`. Looking for visibly soft round points in a mix of sizes, not uniform hard-edged squares.

## Task 11 for Antigravity — MiG-21 Bison replaces the procedural fighter jet

Farzooque supplied a real `MiG-21 Bison` glTF for Beat 5. Remove the hand-built jet entirely — the 12-point extruded wing/canopy shape and the lathe-revolved fuselage from Task 5 and its corrections — and replace with this import. Everything already tuned around that jet (its position, the 230° yaw, the 15° roll, and Task 6's edges-first opacity reveal) carries over unchanged onto the new model; only the geometry source changes.

### License and attribution

**MiG-21 Bison** by OUTPISTON: CC-BY-NC-SA-4.0 — non-commercial only, credit required, share-alike if the model itself is redistributed. Same terms as the MiG-35, already compatible with this project. Add a third credit line, verbatim, to the same ScrapBook footer as the other two:

> This work is based on "MiG-21 Bison" (https://sketchfab.com/3d-models/mig-21-bison-f60f84227a954e3293e5ccb016c2de3f) by OUTPISTON (https://sketchfab.com/outpiston) licensed under CC-BY-NC-SA-4.0 (http://creativecommons.org/licenses/by-nc-sa/4.0/)

### Normalize

Same discipline as Tasks 4 and 9 — verify, don't assume:

1. Compute the bounding box, center it on local origin.
2. Render top-down and side orthographic views of the recentered, unscaled model. The raw bounding box span is largest on one axis and that's a reasonable first guess for the nose-tail length axis, but confirm it from the renders rather than trusting the number alone — the F-16 and MiG-35 didn't agree with each other on this, so don't assume this model matches either.
3. Rotate so the nose points local -Z, up is local +Y.
4. Scale uniformly to `16` world units wingspan — matching the procedural jet it's replacing, so Beat 5's existing framing doesn't need to be re-tuned.

### Materials — override, same treatment as every other aircraft

`MeshStandardMaterial`, color `#05060B`, roughness `0.6`, metalness `0.1`, plus an `EdgesGeometry` outline in `#FF8A3D`. No embedded texture or image from the package gets used.

One addition specific to this model: it's far denser than anything imported so far (hundreds of thousands of vertices, dozens of parts, versus the B2's tens of thousands). A default `EdgesGeometry` threshold on a mesh this dense will likely trace every small panel line instead of just the silhouette, reading as visual noise rather than a clean outline. Use a wider threshold angle — `EdgesGeometry(geometry, 45)` instead of the lower default used on the simpler models — and check the result against a render before calling it done; raise the angle further if it's still cluttered.

### Placement — unchanged from the existing Beat 5 setup

Position `(12, 12, -495)`, `rotation.y = THREE.MathUtils.degToRad(230)`, `rotation.z = THREE.MathUtils.degToRad(15)`. Reveal: body opacity `0` below `0.5893`, ramps `0→1` across `0.5893`–`0.6443`, holds from there — the corrected Beat 5 window already in this brief.

### Explicitly not in scope

No change to the B2, Beat 6's escorts, the camera rig, the Prank layer, or the ScrapBook beyond the new credit line.

### Verification

Orientation-check renders (top-down, side) before placement. A Beat 5 screenshot at the existing camera position, front and 3/4 angle, for direct comparison against the procedural jet it replaces. Console confirms the old procedural jet's meshes are gone, and states which local axis was identified as the length axis.

## Task 12 for Antigravity — real Black Hole model at Beat 1

Farzooque supplied `black_hole.zip`, matching the model recommended earlier. This replaces the entire hand-built assembly from Task 10 and its three correction rounds — the event horizon sphere, the torus, and the custom shader all get deleted. The starfield (and its Task 10 correction — round sprites, three size layers, the lensing warp) is untouched and stays exactly as built; it isn't part of this swap.

### Step 0 — verify the loader can actually render this, before anything else

The file declares `extensionsRequired: ['KHR_materials_pbrSpecularGlossiness']`. Per the glTF spec, a loader that doesn't support a *required* extension can't correctly render the asset at all — this isn't a graceful-degradation case. Load the model with the project's existing GLTFLoader and render one unstyled screenshot before doing anything else:

- If materials and textures appear (the ring shows its swirl texture, the glow elements are visibly colored, not flat grey or white) — the loader supports it, proceed normally.
- If it renders as blank/grey/untextured geometry, or the console logs an unsupported-extension warning — don't debug the loader itself. Instead, convert the file offline, once, using the standard tool for exactly this: `npx gltf-pipeline -i scene.gltf -o scene-converted.gltf --specularGlossinessToMetallicRoughness`, then load the converted output instead. This is a well-established, widely-used conversion specifically for this situation, not something to hand-roll.

Report which path was needed.

### What to keep from the file, what to exclude

Keep the full `black hole` node group (8 parts: three "blackoutside" layers, three "light" glow/flare layers, the distortion mesh, and the center mesh) and the full `black hole_ring` node group (5 parts). Exclude the `Planet` node entirely — it's a small decorative object from the original Sketchfab scene, unrelated to this beat, sitting well off-center from the black hole itself.

### Keep the original materials and textures — do not override them

This is the one deliberate exception to the palette rule used everywhere else on this site. The entire reason to use this model instead of continuing to hand-build the effect is the authored texture and material work — stripping it to the flat `#05060B`/`#FF8A3D` treatment would throw away the thing being imported for. Load it with its own diffuse, emissive, and specular-glossiness textures intact.

### Normalize

1. Combine the kept node groups, compute their bounding box, center on local origin (the `Planet` node is excluded from this calculation too).
2. Scale uniformly so the combined group's widest span becomes `55` world units — compute the factor from the actual measured span, don't hardcode it.
3. Render an orientation check at Beat 1's exact camera position, `(0, 10, 85)` looking at `(0, 0, 0)`, before finalizing rotation. This asset weirdly outputs very large source coordinates (thousands of units pre-scale) — place it at `(0, 0, 0)` after scaling and confirm from the render whether any rotation is actually needed, rather than assuming it's already camera-ready.

### Explicitly not in scope

No change to the starfield or its lensing warp. No change to the caption, its timing, or any other beat, the camera rig, or the Prank layer.

### Attribution

Add a fourth credit line, verbatim, to the same ScrapBook footer as the other three:

> This work is based on "Black Hole" (https://sketchfab.com/3d-models/black-hole-e410da98b1e5445eae2acafaaa53587d) by NestaEric (https://sketchfab.com/Nestaeric) licensed under CC-BY-4.0 (http://creativecommons.org/licenses/by/4.0/)

### Verification

The step 0 loader-check screenshot. The orientation-check render. A full Beat 1 screenshot at the camera position, with the starfield visible behind/around it and the caption in its held state. Console confirms the old core/disk/shader objects are gone and states which loading path (direct vs. converted) was used.

## Task 13 for Antigravity — Beats 2 and 3

Still placeholder boxes, right between two beats that now look good — the warp dive (Beat 2) and the cloud punch-through (Beat 3). Both cameras are already in the rig, untouched. One continuous flash connects the two beats, specified once here so it isn't built twice inconsistently.

### Beat 2 — warp streak tunnel (real range `0.0719`–`0.2201`)

`THREE.LineSegments`, \~200 streaks, `LineBasicMaterial` color `#F4F1EA`. Each streak: two vertices along local Z, randomly offset within a 35-unit-radius cylinder around the Z axis, Z-depth randomized between `+40` and `-70`. Streak length is driven by this beat's own progress, `beatProgress = (globalProgress - 0.0719) / (0.2201 - 0.0719)`, clamped 0–1: `length = lerp(2, 40, beatProgress)` — streaks start short and stretch longer as the beat advances, reading as acceleration into warp.

### Beat 3 — cloud layer (real range `0.2201`–`0.4253`)

`THREE.PlaneGeometry(600, 600)`, rotated flat (`rotation.x = -90°`), positioned around `(0, -20, -160)` to sit under the camera's path through this beat. `ShaderMaterial` reusing the same `fbm()` noise function already written for the burn/dissolve shader and the accretion disk — third reuse of that function, not a new one. Noise drives alpha across the plane's UV space for a patchy cloud look, color `#F4F1EA`. Density is driven by this beat's own progress, `beat3Progress = (globalProgress - 0.2201) / (0.4253 - 0.2201)`, clamped 0–1: `densityMultiplier = lerp(1.0, 0.15, beat3Progress)` — dense and opaque at the start, thinning toward the end.

Also add scene-wide `THREE.FogExp2`, color `#F4F1EA`, density driven by the same `beat3Progress`: `lerp(0.025, 0.002, beat3Progress)`. This is what sells "breaking through" rather than just a cloud plane sitting there — it touches everything in the scene, including the B2 that appears right after in Beat 4, so by the end of Beat 3 it should have faded low enough not to visibly affect Beat 4's reveal.

### The flash — one function spanning both beats, not two

A full-viewport DOM overlay, background `#F4F1EA`, opacity driven directly by global progress (not either beat's local progress) so it reads as one continuous flash at the handoff:

- `0.1941`–`0.2201` (the last 15% of Beat 2): opacity ramps `0 → 0.85`.
- `0.2201`–`0.2509` (the first \~15% of Beat 3): opacity ramps `0.85 → 0`.

Peak brightness lands exactly on station 3, the Beat 2/3 boundary — the moment of breaking through.

### Explicitly not in scope

No change to the camera rig, any other beat, the Prank layer, or the ScrapBook.

### Verification

Screenshots at four points: `0.10` (short streaks, warp just starting), `0.21` (streaks near full length, approaching the flash peak), `0.23` (inside the flash, near-white), `0.38` (clouds thinned, fog mostly cleared, approaching Beat 4). Console confirms both old placeholder boxes are gone.

## Task 13 correction

The math and the cloud/fog/flash handoff are all correct and stay as built — this is one isolated problem. At `p = 0.10`, the ambient starfield renders as hard-edged squares of varying size, not the round, soft-falloff sprites from the Task 10 starfield correction, and there are enough of them to visually clutter what should read as a clean warp tunnel.

### Fix 1 — the sprite texture

Confirm the `starSprite` canvas texture from the Task 10 correction is still being passed as `map` on all three starfield layers' `PointsMaterial` at this camera position. If the squares are back, something in Task 13's changes is either constructing a new material without it or losing the reference — find which, don't just reapply the texture over whatever the current bug is.

### Fix 2 — fade the ambient stars during the dive

Separately from the texture bug: even fixed, this many ambient stars at full brightness competing with 200 dedicated streaks is cluttered. The ambient starfield (all three layers) should fade out as Beat 2 progresses — `starfieldOpacity = lerp(1.0, 0.1, beat2Progress)`, using the same `beat2Progress` already driving the streak length. Full brightness entering the dive, mostly gone by the time the streaks are at full length.

### Explicitly not in scope

No change to the streak tunnel's own geometry or timing, the cloud layer, the fog, or the flash — all of those are correct.

### Verification

Re-capture `beat2_warp_start_0.10.png`. Looking for round, soft stars at reduced density/brightness, not hard squares cluttering the frame.

## Task 14 for Antigravity — Beat 8 handoff

`index.html` (Prank + 3D sequence) and `scrapbook.html` are separate files, so this can't be a true same-page crossfade — it's a fade-to-cover, then a navigation. Reuses the overlay-fade technique already used twice (the Prank's burn, the Beat 2/3 flash), not a new mechanism.

### Trigger

There's no station 9 — Beat 8 is what happens once the pinned ScrollTrigger section has nowhere further to scroll. Use the trigger's own `onLeave` callback (the standard GSAP signal that the user scrolled past a pinned section's end) rather than hand-rolling scroll-delta detection. "Happy Birthday" is already holding at progress `1.0` per Task 7 — this fires on the scroll *after* that point, not before it.

### Sequence

1. On `onLeave`: fade a full-viewport overlay from transparent to solid `#EFE6D2` — the ScrapBook's own paper color, not the 3D scene's dark palette — over `1200ms`, ease-out.
2. Once the fade reaches full opacity: `window.location.href = 'scrapbook.html'`.
3. No change needed on the ScrapBook side — its cover section is already `#EFE6D2` by default from Task 8, so the two pages meet on the same color and the seam across the navigation should be invisible rather than a visible cut.

### Optional, not required

If `document.startViewTransition` is trivially available for this same-origin navigation, it could make the handoff a true native crossfade instead of fade-to-color-then-cut. Don't spend real effort chasing this or build a fallback path around it — cross-document view transition support is inconsistent, especially on mobile, which is this project's stated priority platform. The fade-and-navigate sequence above has to work regardless; treat the view-transition as a free upgrade only if it costs nothing to try.

### Explicitly not in scope

No change to any beat's content, the camera rig, the Prank layer, or the ScrapBook's existing sections.

### Verification

Screen recording or sequential screenshots of: progress at `1.0` holding, the overlay fading in, and the ScrapBook's cover visible immediately after navigation. Confirm it triggers only after `1.0`, not before — scrolling back up from `1.0` should not fire it.

## Task 15 for Antigravity — Beat 6 hangar structure

Farzooque supplied `Centrale Markthal, Amsterdam (Interior+Exterior)` — a real 227-node, 373,760-vertex architectural reconstruction, not a hangar. It's being used as a structural donor, not imported whole. Groups are unusually well-labeled (e.g. `"Roof Frame 03 | 70m solid-web steel"`, not generic `Object_N`), which is what makes a precise cut possible.

### Keep only these groups, by name match

A node is kept if its name contains any of: `"Roof Frame"`, `"Roof |"`, `"exterior masonry"`, `"loading doors lintels and hoists"`, `"Floor |"`, `"Foundation |"`, `"Vertical brace"`. Everything else is excluded — office floors and canopies, all three galleries front and rear, every stair volume and its glazing, both clock faces, the entrance canopies and glazing, the yellow brick office walls, service pipes and luminaires, the upper walkway rail, the air heater louvres, the gutters, and the ceremonial split stair. This cuts the kept set to roughly 156,000 vertices — still substantial, but less than half the source file, and none of what's cut is visible in a flythrough anyway.

**Do not keep `"gabled masonry shell"`** (Front or Rear) even though it matches no exclusion rule above — it isn't in the keep list for a reason: those are the solid end walls, and keeping them would seal the hall shut on both ends. Beat 6 needs an open-ended structure the camera flies through, not into a dead end.

### Normalize

1. Load only the kept nodes, compute their combined bounding box, center on local origin. Measured from the source file: span `(37.07, 14.61, 52.0)`, so centering should land close to that already — confirm rather than assume.
2. Scale uniformly so the X span (the kept set's width) becomes `90` world units — compute the factor from the actual measured span, don't hardcode `90 / 37.07`. This is deliberately wider than the escort jets' \~36-unit formation spread from Task 9, so the hall reads as spacious around them rather than a tight fit.
3. The long axis (Z in the source) becomes the hall's depth — after scaling, roughly `126` units long. This is what the camera flies through.

### Orientation check — before placement, same discipline as every other import

Render the normalized structure alone, from outside at a 3/4 angle, and from directly down the long axis through one open end. Confirm both ends are genuinely open (sky/void visible straight through, not capped) before proceeding. If a rotation is needed to align the long axis with world Z, determine it from this render — don't assume the source file's Z already matches.

### Placement

Center the hall around Beat 6's existing target point, `(0, 8, -680)`, with its long axis along Z so the camera flies down its length. The escort jets from Task 9 keep their existing positions — this task doesn't move them, just builds the space around them.

### Materials — override, same as the aircraft, not the black hole's exception

This shares a beat with the two escort jets, which are already dark-body/accent-edge. A fully textured brick-and-steel building here would clash with that, unlike the black hole, which had no other geometry in its beat to stay consistent with. Same treatment as every aircraft: `MeshStandardMaterial`, color `#05060B`, roughness `0.6`, metalness `0.1`, plus `EdgesGeometry` outlines in `#FF8A3D`. Given the vertex count, use a wide edge threshold (`45°`, same as the MiG-21) and check the result before calling it done — a structure this detailed will trace brick coursing and rivet lines as noise at a narrow threshold.

### License and attribution

**Centrale Markthal, Amsterdam (Interior+Exterior)** by Jungle Jim: CC-BY-4.0, commercial use allowed, credit required. Add a fifth credit line, verbatim, to the same ScrapBook footer as the other four:

> This work is based on "Centrale Markthal, Amsterdam (Interior+Exterior)" (https://sketchfab.com/3d-models/centrale-markthal-amsterdam-interiorexterior-a11dee950272459b935ecb469730e6bc) by Jungle Jim (https://sketchfab.com/jungle\_jim) licensed under CC-BY-4.0 (http://creativecommons.org/licenses/by/4.0/)

### Explicitly not in scope

No change to the escort jets' positions, materials, or reveal timing. No change to any other beat, the camera rig, the Prank layer, or the ScrapBook beyond the new credit line.

### Verification

The two orientation-check renders (3/4 exterior, down the open long axis) before placement. A Beat 6 screenshot at the existing camera position showing the hall, both jets, and open space visible through the far end. A performance note — frame time or triangle count actually rendered — given this is the heaviest single import so far and this project has a stated phone-first priority.

## Task 16 for Antigravity — complete the ScrapBook

All four remaining spreads in one task — Studio Pages, Mixtape, Game Day, Photo Booth — since they're the same mechanics as Flight Log (Task 8) with new content, not new technique. Reuse `.sheet` / `.tape` / `.note` / `.stamp` / `.ticket` exactly as they already exist; don't rebuild them.

### Studio Pages — the 7 artworks not used in Flight Log

From the artworks folder, everything except the B2 sketch and the two fighter sketches (those are Flight Log's): the jellyfish watercolor, the courtyard/café painting, the green dragon-head sketch, the full-color dragon piece, both still-life studies (apple and orange, each with the cylinder), and the sunset sailboat watercolor. Denser than Flight Log's 3 large pieces, so lay these out as a masonry/grid wall of smaller `.sheet` cards rather than a few large showcases — 2 size tiers is enough: the sunset and the dragon piece as slightly larger "featured" sheets, the remaining 5 at a smaller uniform size. One `.note` per piece, same handwritten-caption pattern as Flight Log.

### Mixtape — honest about what's actually available

There's no specific playlist or track, only her Spotify profile link, and no dance photos. Don't pad this with placeholder music-player UI that implies more than exists. One `.ticket`, styled like a backstage pass: "HER SPOTIFY" / a tap-through link to `https://open.spotify.com/user/314ipmyt62uzmajordk4fg3pwrmi` / a handwritten `.note` underneath: "tap in ♡". That's the whole spread — small and honest beats padded and fake.

### Game Day — placeholder only, marked as such

No basketball or athletics material exists at all. Build a single small `.ticket`: "GAME DAY · stats incoming", same visual treatment as everywhere else so the scroll rhythm doesn't have a dead gap, but this is explicitly a placeholder to swap out the moment real material shows up — not a finished spread. Flag it as such in the completion report so it doesn't get mistaken for done.

### Photo Booth — the 4 cleared solo photos

The hills/travel photo, the stairs photo, the green field photo, and the blue door photo — the only four photos confirmed to have no one else in them. Polaroid strip layout, `.sheet` + `.tape`, consistent with the rest.

### Explicitly not in scope

No new components — if a spread seems to need something `.sheet`/`.tape`/`.note`/`.stamp`/`.ticket` can't do, use the closest existing one rather than inventing a new class. No change to Flight Log, the cover, the footer, or any page outside the ScrapBook.

### Verification

Screenshots of all four new spreads at 1440×900. Confirm the existing Task 8 mobile breakpoint rule (single column, 88vw, halved rotation under 900px) actually applies to these new spreads too, not just Flight Log — check, don't assume it inherited automatically.

## Task 17 for Antigravity — mobile/responsive pass

Both pages in one task, bundled since most of this is the same handful of root causes showing up twice (`index.html`'s 3D sequence and `scrapbook.html`), not two separate problems. Every screenshot delivered across all 17 tasks so far has been desktop-sized — this is the first time any of it gets checked at phone width, which is the stated priority platform.

### Viewport fundamentals, both pages

- `100vh` on any full-bleed section becomes `100svh` (small viewport height) — plain `vh` includes the space mobile browser chrome collapses into/out of, causing visible jumps as the address bar shows and hides mid-scroll.
- Confirm the viewport meta tag includes `viewport-fit=cover`, and add `env(safe-area-inset-*)` padding to anything pinned to a screen edge (the Prank's hold button, the 3D sequence's captions, the ScrapBook's footer) so none of it sits under a notch or home-indicator area.

### The 3D sequence — performance budget

Beat 6 is now the heaviest single beat (129K triangles rendered with the hangar in frame) and this project has no tested floor for what a mid-range phone GPU can sustain. Before any further optimization: profile actual frame time on a mid-tier Android profile (not just desktop Chrome's mobile emulation, which doesn't reflect real GPU limits), across at least Beat 1 (black hole), Beat 6 (hangar + both jets), and Beat 3 (fog + cloud shader). If any beat drops meaningfully below 60fps: cap `devicePixelRatio` at `1.5` on touch devices first — cheapest fix, try it before anything structural. If that's not enough, frustum-cull or hide the hangar's geometry outside Beat 6's progress range (`p < 0.70` or `p > 0.95`, per Task 15's own performance note) rather than leaving it in the scene graph for the whole sequence.

### The 3D sequence — touch interactions

- The sparkle cursor trail (Prank, Task 3) is pointer-move-based and doesn't mean anything on a touch screen with no hover state. Disable it on touch devices rather than leaving dead code firing on touchmove.
- Confirm the hold-to-proceed button (Task 2's `pointerdown`/`pointerup`) genuinely fires on touch, not just mouse — Pointer Events should cover both, but this has never actually been checked on a real or emulated touch device.
- Confirm Lenis' smooth scroll doesn't fight native touch-scroll momentum — test actual touch-drag scrolling through the full sequence, not just verifying it loads.

### The ScrapBook — extend the existing breakpoint, verify it actually reaches everything

Task 8 already defined the mobile rule (single column, 88vw, halved rotation, under 900px) and Task 16 was told to confirm it reaches the new spreads — if Task 16 already handled this, this task doesn't redo it, just confirms. If any spread doesn't actually comply once checked, this is where it gets fixed, not somewhere else.

### Explicitly not in scope

No new visual content on either page. No change to any beat's camera, geometry, or timing beyond the device-pixel-ratio and culling changes above, and only if profiling actually shows they're needed.

### Verification

Screenshots of both pages at 390×844 (a standard phone size): the Prank, at least Beats 1/4/6/7 of the 3D sequence, and all five ScrapBook spreads including the four from Task 16. The actual measured frame-time numbers from the mid-tier profiling, not just a pass/fail — numbers, so a future task can tell if a later change regresses them.

## Task 18 for Antigravity — fix Beat 1's performance

Task 17's own telemetry: Beat 1 averages `780ms` per frame under mid-tier throttling — `1.3fps`, measured across 37 samples, not a single spike. Beat 3 (`8.8fps`) and Beat 6 (`4fps`) aren't good either, but Beat 1 is the opening beat on the stated priority platform, so it's the one that can't ship like this. The DPR cap and hangar culling from Task 17 didn't touch this number — whatever's costing that much per frame is something else, and this task starts with finding out what, not with another guess.

### Profile first, fix second

Use the browser's own performance profiler (Chrome DevTools Performance panel, or `performance.now()` bracketing around each render-loop stage) to get a breakdown of where Beat 1's frame time actually goes — script execution vs. GPU paint vs. layout, and within script, which function. Report the actual breakdown before changing anything. Don't apply a fix aimed at a guessed cause without that number in hand first.

### One concrete hypothesis worth checking, not assuming

The black hole model (Task 12) has three separate semi-transparent "light" flare layers doing overlapping `AdditiveBlending`, on top of the starfield's own three additive layers. Overlapping transparent fill is a fill-rate cost that has nothing to do with triangle count or draw calls — the exact kind of problem the vertex/triangle framing used for Beat 6 would never surface. Worth checking specifically whether disabling the light-flare layers one at a time changes the frame time, before looking anywhere else.

### Also verify this, separately

Confirm the starfield's lensing warp is still a one-time position computation at generation time, as originally specified in Task 10, not something that regressed into running every frame — a per-frame loop over 800 star positions plus trig would be a real CPU cost that throttling would expose exactly like this.

### Explicitly not in scope

No change to Beat 1's visual design, the black hole's materials or scale, the starfield's appearance, or any other beat — this is a performance investigation and fix, not a redesign.

### Verification

The profiler breakdown itself, not just a before/after number. Re-measure Beat 1 under the same mid-tier throttle profile Task 17 used, so the comparison is apples to apples. State plainly what the fix actually was and why the breakdown pointed there.

## Open items — what to add

| Item | Needed for | Status |
| --- | --- | --- |
| Her actual birthday date | Scheduling every task against a real deadline | 09 October 2026 |
| Real Spotify playlist/track link (not just her profile) | Mixtape section | <https://open.spotify.com/user/314ipmyt62uzmajordk4fg3pwrmi> |
| Dance photos or video | Mixtape section | Not Available |
| Basketball/athletics photos or stats | Game Day section | Not Available |
| Copy for the black-hole line (Beat 1) and each name-reveal strike (Beat 7) | Motion Sequence | Drafted — see Copy section under Part 2; edit inline if you want different wording |
| Exact palette hex values | Applies to all three pieces | Resolved — bg #05060B, accent #FF8A3D, text #F4F1EA (see Task 1 Correction) |
| Hosting/domain for after the birthday | Antigravity's final deploy task | We'll check |
| Device priority | Build and QA order | phone-first, but laptop also |
| Purpose of the 3 video clips in the first zip | Unclear which section they belong to | Those are clips of her |
