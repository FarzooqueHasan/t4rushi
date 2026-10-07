/**
 * Tarushi Birthday Site — 3D Motion Sequence Camera Rig
 * 
 * Empty Camera Rig Scaffold:
 * - 8 fixed camera positions, lookAt targets, and FOV values matching Beats 1–8
 * - Catmull-Rom spline interpolation (centripetal)
 * - ScrollTrigger + Lenis wiring
 * - Background: #05060B
 * - Accent: #FF8A3D (wireframe MeshBasicMaterial for placeholder boxes)
 * - Verification: console.table() at each checkpoint
 */

(function () {
  'use strict';

  // --------------------------------------------------------------------------
  // 1. Data Schema: 8 Motion Sequence Beats
  // --------------------------------------------------------------------------
  const BEATS = [
    {
      id: 1,
      camPos: new THREE.Vector3(0, 10, 85),
      camTarget: new THREE.Vector3(0, 0, 0),
      boxPos: new THREE.Vector3(0, 0, 0),
      fov: 55
    },
    {
      id: 2,
      camPos: new THREE.Vector3(0, 1.5, 14),
      camTarget: new THREE.Vector3(0, 0, -45),
      boxPos: new THREE.Vector3(0, 0, -15),
      fov: 82
    },
    {
      id: 3,
      camPos: new THREE.Vector3(45, 40, -120),
      camTarget: new THREE.Vector3(0, 15, -200),
      boxPos: new THREE.Vector3(0, 15, -200),
      fov: 62
    },
    {
      id: 4,
      camPos: new THREE.Vector3(-45, 22, -300),
      camTarget: new THREE.Vector3(-10, 16, -350),
      boxPos: new THREE.Vector3(-10, 16, -350),
      fov: 48
    },
    {
      id: 5,
      camPos: new THREE.Vector3(35, 14, -440),
      camTarget: new THREE.Vector3(12, 12, -495),
      boxPos: new THREE.Vector3(12, 12, -495),
      fov: 52
    },
    {
      id: 6,
      camPos: new THREE.Vector3(0, 16, -600),
      camTarget: new THREE.Vector3(0, 8, -680),
      boxPos: new THREE.Vector3(0, 8, -680),
      fov: 45
    },
    {
      id: 7,
      camPos: new THREE.Vector3(0, 4.0, -750),
      camTarget: new THREE.Vector3(0, 3.0, -805),
      boxPos: new THREE.Vector3(0, 3.0, -805),
      fov: 38
    },
    {
      id: 8,
      camPos: new THREE.Vector3(0, 2.5, -845),
      camTarget: new THREE.Vector3(0, 2.5, -890),
      boxPos: new THREE.Vector3(0, 2.5, -890),
      fov: 34
    }
  ];

  // Output all 8 checkpoints at start
  console.log("%c=== 3D MOTION RIG: 8 CHECKPOINTS ===", "color: #FF8A3D; font-weight: bold; font-size: 13px;");
  console.table(BEATS.map(b => ({
    Beat: b.id,
    'Cam X': b.camPos.x,
    'Cam Y': b.camPos.y,
    'Cam Z': b.camPos.z,
    'Target X': b.camTarget.x,
    'Target Y': b.camTarget.y,
    'Target Z': b.camTarget.z,
    FOV: b.fov + '°'
  })));

  // --------------------------------------------------------------------------
  // 2. Spline Construction: Centripetal Catmull-Rom
  // --------------------------------------------------------------------------
  const camPoints = BEATS.map(b => b.camPos);
  const targetPoints = BEATS.map(b => b.camTarget);

  const camSpline = new THREE.CatmullRomCurve3(camPoints, false, 'centripetal', 0.5);
  const targetSpline = new THREE.CatmullRomCurve3(targetPoints, false, 'centripetal', 0.5);

  // --------------------------------------------------------------------------
  // 3. Three.js Scene, Camera, Renderer
  // --------------------------------------------------------------------------
  const canvas = document.getElementById('webgl-canvas');
  const scene = new THREE.Scene();
  scene.background = new THREE.Color(0x05060B);
  window.__debugScene = scene;

  const camera = new THREE.PerspectiveCamera(55, window.innerWidth / window.innerHeight, 0.1, 2000);
  camera.position.copy(camPoints[0]);
  camera.lookAt(targetPoints[0]);

  const isTouchDevice = (('ontouchstart' in window) || (navigator.maxTouchPoints > 0));
  const maxDPR = isTouchDevice ? 1.5 : 2.0;

  const renderer = new THREE.WebGLRenderer({
    canvas: canvas,
    antialias: true,
    powerPreference: 'high-performance'
  });
  renderer.setSize(window.innerWidth, window.innerHeight);
  renderer.setPixelRatio(Math.min(window.devicePixelRatio, maxDPR));
  renderer.setClearColor(0x05060B, 1.0);
  window.renderer = renderer;
  window.scene = scene;
  window.camera = camera;
  window.isTouchDevice = isTouchDevice;
  window.maxDPR = maxDPR;

  // --------------------------------------------------------------------------
  // Lighting: Exactly two lights per spec
  // DirectionalLight #FF8A3D at intensity 0.4 rim-lighting from behind/above
  // Neutral AmbientLight at intensity 0.15
  // --------------------------------------------------------------------------
  const dirLight = new THREE.DirectionalLight(0xFF8A3D, 0.4);
  dirLight.position.set(-10, 45, -310);
  scene.add(dirLight);

  const ambLight = new THREE.AmbientLight(0xF4F1EA, 0.15);
  scene.add(ambLight);

  // --------------------------------------------------------------------------
  // 4. Placeholder Boxes: Plain BoxGeometry, wireframe MeshBasicMaterial #FF8A3D
  // Note: Beat 4 placeholder box is removed from scene graph (replaced by B2 Bomber)
  // --------------------------------------------------------------------------
  const boxGeometry = new THREE.BoxGeometry(10, 10, 10);
  const boxMaterial = new THREE.MeshBasicMaterial({
    color: 0xFF8A3D,
    wireframe: true
  });

  const placeholderBoxes = [];
  BEATS.forEach((beat) => {
    if (beat.id <= 6) return;
    const box = new THREE.Mesh(boxGeometry, boxMaterial);
    box.position.copy(beat.boxPos);
    box.name = `placeholder_box_beat_${beat.id}`;
    box.visible = false;
    scene.add(box);
    placeholderBoxes.push(box);
  });
  window.placeholderBoxes = placeholderBoxes;

  // --------------------------------------------------------------------------
  // Beat 1: Starfield with generation-time Lensing Warp (Preserved from Task 10)
  // --------------------------------------------------------------------------
  const gltfLoader = new THREE.GLTFLoader();

  // 2 & 3. Starfield with generation-time Lensing Warp
  const starCount = 800;
  const unwarpedPositions = new Float32Array(starCount * 3);
  const warpedPositions = new Float32Array(starCount * 3);
  const defaultColors = new Float32Array(starCount * 3);
  const tintedColors = new Float32Array(starCount * 3);
  const cWhite = new THREE.Color(0xF4F1EA);
  const cPink = new THREE.Color(0xFF5C8A);

  // Deterministic RNG for consistent, well-distributed starfield framing
  let starSeed = 4242;
  function starRng() {
    starSeed = (starSeed * 9301 + 49297) % 233280;
    return starSeed / 233280;
  }

  let lensedStarCount = 0;
  for (let i = 0; i < starCount; i++) {
    let x, y, z;
    // Distribute ~320 stars in the background viewing cone behind and around the hole (d in [60, 120])
    // This ensures the lensing warp forms a clearly visible curved arc around the event horizon core
    if (i < 320) {
      const r = 60.0 + starRng() * 60.0; // r in [60, 120] -> lensing zone
      const angle = starRng() * Math.PI * 2.0;
      const spread = starRng() * 0.75;
      x = Math.cos(angle) * r * spread;
      y = Math.sin(angle) * r * spread * 0.85;
      z = -Math.sqrt(Math.max(1.0, r * r - x * x - y * y)); // Behind the hole (Z < 0)
    } else {
      // General spherical shell distribution [60, 600]
      const u = starRng() * 2.0 - 1.0;
      const th = starRng() * Math.PI * 2.0;
      const s = Math.sqrt(Math.max(0.0, 1.0 - u * u));
      const r = 60.0 + starRng() * 540.0;
      x = s * Math.cos(th) * r;
      y = s * Math.sin(th) * r;
      z = u * r;
    }

    // Save unwarped positions
    unwarpedPositions[i * 3] = x;
    unwarpedPositions[i * 3 + 1] = y;
    unwarpedPositions[i * 3 + 2] = z;

    // Default star color: #F4F1EA
    defaultColors[i * 3] = cWhite.r;
    defaultColors[i * 3 + 1] = cWhite.g;
    defaultColors[i * 3 + 2] = cWhite.b;

    // Lensing warp: applied once, at generation time, to each star's position
    const d = Math.sqrt(x * x + y * y + z * z);
    if (d < 120.0) {
      lensedStarCount++;
      const bendAngle = (1.0 - d / 120.0) * 0.8;
      const newX = x * Math.cos(bendAngle) - z * Math.sin(bendAngle);
      const newZ = x * Math.sin(bendAngle) + z * Math.cos(bendAngle);
      x = newX;
      z = newZ;

      // Tinted debug color: #FF5C8A for lensed stars
      tintedColors[i * 3] = cPink.r;
      tintedColors[i * 3 + 1] = cPink.g;
      tintedColors[i * 3 + 2] = cPink.b;
    } else {
      // Non-lensed stars remain #F4F1EA
      tintedColors[i * 3] = cWhite.r;
      tintedColors[i * 3 + 1] = cWhite.g;
      tintedColors[i * 3 + 2] = cWhite.b;
    }

    warpedPositions[i * 3] = x;
    warpedPositions[i * 3 + 1] = y;
    warpedPositions[i * 3 + 2] = z;
  }

  // --------------------------------------------------------------------------
  // Fix 1 & Task 10 Starfield Correction:
  // - 64x64 CanvasTexture radial gradient for soft round falloff
  // - 3 layers with weighted shares: Dim 60%, Mid 30%, Bright 10%
  // - PointsMaterial({ map: starSprite, color: 0xF4F1EA, size, opacity, transparent: true, blending: THREE.AdditiveBlending, depthWrite: false, sizeAttenuation: true })
  // --------------------------------------------------------------------------
  const starCanvas = document.createElement('canvas');
  starCanvas.width = 64;
  starCanvas.height = 64;
  const starCtx = starCanvas.getContext('2d');
  const gradient = starCtx.createRadialGradient(32, 32, 0, 32, 32, 32);
  gradient.addColorStop(0.0, 'rgba(255, 255, 255, 1.0)');
  gradient.addColorStop(0.2, 'rgba(255, 255, 255, 0.8)');
  gradient.addColorStop(0.6, 'rgba(255, 255, 255, 0.2)');
  gradient.addColorStop(1.0, 'rgba(255, 255, 255, 0.0)');
  starCtx.fillStyle = gradient;
  starCtx.fillRect(0, 0, 64, 64);
  const starSprite = new THREE.CanvasTexture(starCanvas);

  // Partition the 800 stars into 3 weighted layers
  const layerConfigs = [
    { name: 'dim', share: 0.60, size: 1.0, baseOpacity: 0.55, indices: [] },
    { name: 'mid', share: 0.30, size: 1.8, baseOpacity: 0.80, indices: [] },
    { name: 'bright', share: 0.10, size: 3.0, baseOpacity: 1.00, indices: [] }
  ];

  for (let i = 0; i < starCount; i++) {
    const roll = starRng();
    if (roll < 0.60) {
      layerConfigs[0].indices.push(i);
    } else if (roll < 0.90) {
      layerConfigs[1].indices.push(i);
    } else {
      layerConfigs[2].indices.push(i);
    }
  }

  const starfieldGroup = new THREE.Group();
  starfieldGroup.name = "starfield_points";

  const starfieldLayers = layerConfigs.map((cfg) => {
    const count = cfg.indices.length;
    const layerUnwarped = new Float32Array(count * 3);
    const layerWarped = new Float32Array(count * 3);
    const layerDefColors = new Float32Array(count * 3);
    const layerTintColors = new Float32Array(count * 3);

    for (let k = 0; k < count; k++) {
      const idx = cfg.indices[k];
      for (let c = 0; c < 3; c++) {
        layerUnwarped[k * 3 + c] = unwarpedPositions[idx * 3 + c];
        layerWarped[k * 3 + c] = warpedPositions[idx * 3 + c];
        layerDefColors[k * 3 + c] = defaultColors[idx * 3 + c];
        layerTintColors[k * 3 + c] = tintedColors[idx * 3 + c];
      }
    }

    const geom = new THREE.BufferGeometry();
    geom.setAttribute('position', new THREE.BufferAttribute(new Float32Array(layerWarped), 3));
    geom.setAttribute('color', new THREE.BufferAttribute(new Float32Array(layerDefColors), 3));

    const mat = new THREE.PointsMaterial({
      map: starSprite,
      color: 0xF4F1EA,
      size: cfg.size,
      opacity: cfg.baseOpacity,
      transparent: true,
      blending: THREE.AdditiveBlending,
      depthWrite: false,
      sizeAttenuation: true
    });

    const points = new THREE.Points(geom, mat);
    points.name = `starfield_${cfg.name}`;
    starfieldGroup.add(points);

    return {
      name: cfg.name,
      size: cfg.size,
      baseOpacity: cfg.baseOpacity,
      indices: cfg.indices,
      unwarped: layerUnwarped,
      warped: layerWarped,
      defaultColors: layerDefColors,
      tintedColors: layerTintColors,
      geometry: geom,
      material: mat,
      points: points
    };
  });

  // Provide full 800-star geometry & material properties on starfieldGroup for backward compatibility
  const fullStarGeom = new THREE.BufferGeometry();
  fullStarGeom.setAttribute('position', new THREE.BufferAttribute(new Float32Array(warpedPositions), 3));
  fullStarGeom.setAttribute('color', new THREE.BufferAttribute(new Float32Array(defaultColors), 3));
  starfieldGroup.geometry = fullStarGeom;
  starfieldGroup.material = {
    color: new THREE.Color(0xF4F1EA),
    size: 1.5,
    vertexColors: true,
    map: starSprite
  };

  scene.add(starfieldGroup);
  window.starfield = starfieldGroup;
  window.starfieldLayers = starfieldLayers;
  window.starSprite = starSprite;
  window.unwarpedStarPositions = unwarpedPositions;
  window.warpedStarPositions = warpedPositions;
  window.defaultStarColors = defaultColors;
  window.tintedStarColors = tintedColors;

  window.setStarfieldLensing = function(enabled) {
    const fullPosAttr = fullStarGeom.attributes.position;
    fullPosAttr.copyArray(enabled ? warpedPositions : unwarpedPositions);
    fullPosAttr.needsUpdate = true;

    starfieldLayers.forEach(l => {
      const posAttr = l.geometry.attributes.position;
      posAttr.copyArray(enabled ? l.warped : l.unwarped);
      posAttr.needsUpdate = true;
    });
  };

  window.setStarfieldTint = function(enabled) {
    const fullColAttr = fullStarGeom.attributes.color;
    fullColAttr.copyArray(enabled ? tintedColors : defaultColors);
    fullColAttr.needsUpdate = true;

    starfieldLayers.forEach(l => {
      const colAttr = l.geometry.attributes.color;
      colAttr.copyArray(enabled ? l.tintedColors : l.defaultColors);
      colAttr.needsUpdate = true;
      l.material.vertexColors = enabled;
      l.material.color.set(enabled ? 0xffffff : 0xF4F1EA);
      l.material.needsUpdate = true;
    });
  };

  // Fix 2: Fade the ambient stars during Beat 2 warp dive
  // starfieldOpacity = lerp(1.0, 0.1, beat2Progress) using the same beat2Progress as streaks
  function updateStarfieldOpacity(p) {
    let fadeFactor = 1.0;
    if (p > 0.0719 && p <= 0.2201) {
      const beat2Progress = (p - 0.0719) / (0.2201 - 0.0719);
      fadeFactor = THREE.MathUtils.lerp(1.0, 0.1, beat2Progress);
    } else if (p > 0.2201) {
      fadeFactor = 0.1;
    } else {
      fadeFactor = 1.0;
    }

    starfieldLayers.forEach(layer => {
      layer.material.opacity = layer.baseOpacity * fadeFactor;
    });
  }
  window.updateStarfieldOpacity = updateStarfieldOpacity;

  console.log(`[Starfield] 800 stars created in 3 layers (Dim: ${starfieldLayers[0].indices.length}, Mid: ${starfieldLayers[1].indices.length}, Bright: ${starfieldLayers[2].indices.length}). Lensing warp applied to ${lensedStarCount} stars within d < 120.`);

  // --------------------------------------------------------------------------
  // Task 12: Beat 1 — Real Black Hole Model (NestaEric, CC-BY-4.0)
  // Replaces hand-built core, disk and shader. Starfield & lensing are untouched.
  // --------------------------------------------------------------------------
  window.blackHoleReady = false;
  window.blackHoleCore = null;
  window.accretionDisk = null;

  gltfLoader.load('models/blackhole/scene.gltf', (gltf) => {
    const bhRoot = gltf.scene;

    // 1. Exclude Planet node entirely
    const planetNodes = [];
    bhRoot.traverse((child) => {
      if (child.name === 'Planet' || (child.name && child.name.startsWith('Planet_'))) {
        planetNodes.push(child);
      }
    });
    planetNodes.forEach((node) => {
      if (node.parent) node.parent.remove(node);
    });

    // 2. Compute bounding box of kept node groups ('black hole' and 'black hole_ring')
    const rawBox = new THREE.Box3().setFromObject(bhRoot);
    const rawCenter = new THREE.Vector3();
    rawBox.getCenter(rawCenter);
    const rawSize = new THREE.Vector3();
    rawBox.getSize(rawSize);

    // 3. Center on local origin (0, 0, 0)
    bhRoot.position.sub(rawCenter);

    const blackHoleGroup = new THREE.Group();
    blackHoleGroup.name = "black_hole_assembly";
    blackHoleGroup.add(bhRoot);

    // 4. Uniform scale so widest span becomes exactly 55 world units
    const widestSpan = Math.max(rawSize.x, rawSize.y, rawSize.z);
    const targetSpan = 55.0;
    const scaleFactor = targetSpan / widestSpan;
    blackHoleGroup.scale.setScalar(scaleFactor);

    // 5. Position at Beat 1 origin (0, 0, 0)
    blackHoleGroup.position.set(0, 0, 0);

    // Optimize static black hole assembly: disable per-frame matrix recalculations
    blackHoleGroup.matrixAutoUpdate = false;
    blackHoleGroup.traverse((child) => {
      child.matrixAutoUpdate = false;
    });
    blackHoleGroup.updateMatrixWorld(true);

    scene.add(blackHoleGroup);

    console.log("[Black Hole] Old core, disk, and custom shader removed from scene.");
    console.log("[Black Hole] Loaded via direct GLTFLoader path (KHR_materials_pbrSpecularGlossiness supported).");
    console.log(`[Black Hole] Planet node excluded. Kept groups centered on origin and scaled by ${scaleFactor.toFixed(6)} to ${targetSpan} units widest span.`);

    window.blackHoleReady = true;
    window.blackHole = blackHoleGroup;
  }, undefined, (err) => {
    console.error("[Black Hole] Error loading model:", err);
  });

  // --------------------------------------------------------------------------
  // Beat 1 Caption Logic: Real progress range 0–0.0719
  // Fade in 0–0.02, hold 0.02–0.055, fade out 0.055–0.0719
  // --------------------------------------------------------------------------
  const beat1Caption = document.getElementById('beat1-caption');
  let lastBeat1CaptionOpacity = -1;

  function updateBeat1Caption(p) {
    if (!beat1Caption) return;
    let opacity = 0.0;
    if (p >= 0.0 && p <= 0.0719) {
      if (p < 0.02) {
        opacity = p / 0.02;
      } else if (p <= 0.055) {
        opacity = 1.0;
      } else {
        opacity = 1.0 - (p - 0.055) / (0.0719 - 0.055);
      }
    }
    opacity = Math.max(0.0, Math.min(1.0, opacity));
    if (Math.abs(opacity - lastBeat1CaptionOpacity) > 0.001) {
      lastBeat1CaptionOpacity = opacity;
      beat1Caption.style.opacity = opacity.toFixed(4);
      beat1Caption.style.visibility = opacity > 0.001 ? 'visible' : 'hidden';
    }
  }

  window.updateBeat1Caption = updateBeat1Caption;
  window.getBeat1CaptionState = function() {
    return {
      opacity: beat1Caption ? parseFloat(beat1Caption.style.opacity || '0') : 0,
      text: beat1Caption ? beat1Caption.innerText : ''
    };
  };

  // --------------------------------------------------------------------------
  // Task 13: Beat 2 — Warp Streak Tunnel (Real range 0.0719–0.2201)
  // --------------------------------------------------------------------------
  const streakCount = 200;
  const streakBases = new Float32Array(streakCount * 3);
  const warpPositions = new Float32Array(streakCount * 6);

  let warpSeed = 4242;
  function warpRng() {
    warpSeed = (warpSeed * 9301 + 49297) % 233280;
    return warpSeed / 233280;
  }

  // 200 streaks randomly offset within a 35-unit-radius cylinder around Z axis,
  // Z-depth randomized between +40 and -70.
  for (let i = 0; i < streakCount; i++) {
    const r = 2.0 + Math.sqrt(warpRng()) * 33.0; // r in [2, 35] around Z axis
    const th = warpRng() * Math.PI * 2.0;
    const x = Math.cos(th) * r;
    const y = Math.sin(th) * r;
    const z = -70.0 + warpRng() * 110.0; // [-70, +40]
    streakBases[i * 3] = x;
    streakBases[i * 3 + 1] = y;
    streakBases[i * 3 + 2] = z;
  }

  const warpGeom = new THREE.BufferGeometry();
  warpGeom.setAttribute('position', new THREE.BufferAttribute(warpPositions, 3));
  const warpMaterial = new THREE.LineBasicMaterial({
    color: 0xF4F1EA,
    transparent: true,
    opacity: 1.0,
    linewidth: 1.5
  });
  const warpStreakTunnel = new THREE.LineSegments(warpGeom, warpMaterial);
  warpStreakTunnel.name = "warp_streak_tunnel";
  warpStreakTunnel.visible = false;
  scene.add(warpStreakTunnel);
  window.warpTunnel = warpStreakTunnel;
  window.warpGeometry = warpGeom;
  window.warpMaterial = warpMaterial;

  function updateBeat2Warp(p) {
    if (p >= 0.0719 && p <= 0.2509) {
      warpStreakTunnel.visible = true;
      const beatProgress = Math.max(0.0, Math.min(1.0, (p - 0.0719) / (0.2201 - 0.0719)));
      const streakLen = THREE.MathUtils.lerp(2.0, 40.0, beatProgress);
      const halfLen = streakLen * 0.5;
      const pos = warpGeom.attributes.position.array;

      for (let i = 0; i < streakCount; i++) {
        const x = streakBases[i * 3];
        const y = streakBases[i * 3 + 1];
        const z = streakBases[i * 3 + 2];
        pos[i * 6] = x;
        pos[i * 6 + 1] = y;
        pos[i * 6 + 2] = z - halfLen;
        pos[i * 6 + 3] = x;
        pos[i * 6 + 4] = y;
        pos[i * 6 + 5] = z + halfLen;
      }
      warpGeom.attributes.position.needsUpdate = true;
    } else {
      warpStreakTunnel.visible = false;
    }
  }
  window.updateBeat2Warp = updateBeat2Warp;

  // --------------------------------------------------------------------------
  // Task 13: Beat 3 — Cloud Layer & Scene-wide FogExp2 (Real range 0.2201–0.4253)
  // --------------------------------------------------------------------------
  const sceneFog = new THREE.FogExp2(0xF4F1EA, 0.0);
  scene.fog = sceneFog;
  window.sceneFog = sceneFog;

  const bgSpace = new THREE.Color(0x05060B);
  const bgCloud = new THREE.Color(0xF4F1EA);

  const cloudVertexShader = `
    varying vec2 vUv;
    void main() {
      vUv = uv;
      gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
    }
  `;

  const cloudFragmentShader = `
    precision highp float;
    varying vec2 vUv;
    uniform vec3 u_color;
    uniform float u_densityMultiplier;

    vec3 mod289(vec3 x) { return x - floor(x * (1.0 / 289.0)) * 289.0; }
    vec2 mod289(vec2 x) { return x - floor(x * (1.0 / 289.0)) * 289.0; }
    vec3 permute(vec3 x) { return mod289(((x*34.0)+1.0)*x); }

    float snoise(vec2 v) {
      const vec4 C = vec4(0.211324865405187,
                          0.366025403784439,
                         -0.577350269189626,
                          0.024390243902439);
      vec2 i  = floor(v + dot(v, C.yy) );
      vec2 x0 = v -   i + dot(i, C.xx);
      vec2 i1 = (x0.x > x0.y) ? vec2(1.0, 0.0) : vec2(0.0, 1.0);
      vec4 x12 = x0.xyxy + C.xxzz;
      x12.xy -= i1;
      i = mod289(i);
      vec3 p = permute( permute( i.y + vec3(0.0, i1.y, 1.0 ))
            + i.x + vec3(0.0, i1.x, 1.0 ));
      vec3 m = max(0.5 - vec3(dot(x0,x0), dot(x12.xy,x12.xy), dot(x12.zw,x12.zw)), 0.0);
      m = m*m;
      m = m*m;
      vec3 x = 2.0 * fract(p * C.www) - 1.0;
      vec3 h = abs(x) - 0.5;
      vec3 ox = floor(x + 0.5);
      vec3 a0 = x - ox;
      m *= 1.79284291400159 - 0.85373472095314 * ( a0*a0 + h*h );
      vec3 g;
      g.x  = a0.x  * x0.x  + h.x  * x0.y;
      g.yz = a0.yz * x12.xz + h.yz * x12.yw;
      return 130.0 * dot(m, g);
    }

    float fbm(vec2 uv) {
      float total = 0.0;
      float amp = 0.5;
      for (int i = 0; i < 4; i++) {
        total += snoise(uv) * amp;
        uv *= 2.08;
        amp *= 0.5;
      }
      return total * 0.5 + 0.5;
    }

    void main() {
      // Multi-scale cloud noise for patchy texture
      float n1 = fbm(vUv * 6.0);
      float n2 = fbm(vUv * 14.0) * 0.3;
      float n = clamp(n1 + n2 - 0.15, 0.0, 1.0);

      // Patchy cloud density mapping
      float alpha = smoothstep(0.2, 0.7, n) * u_densityMultiplier;

      // Soft perimeter fade so 600x600 plane edges don't show a harsh border
      float dist = length(vUv - 0.5) * 2.0;
      float perimeterFade = 1.0 - smoothstep(0.7, 1.0, dist);
      alpha *= perimeterFade;

      if (alpha < 0.005) discard;
      gl_FragColor = vec4(u_color, alpha);
    }
  `;

  const cloudMaterial = new THREE.ShaderMaterial({
    vertexShader: cloudVertexShader,
    fragmentShader: cloudFragmentShader,
    uniforms: {
      u_color: { value: new THREE.Color(0xF4F1EA) },
      u_densityMultiplier: { value: 1.0 }
    },
    transparent: true,
    depthWrite: false,
    side: THREE.DoubleSide
  });

  const cloudGeometry = new THREE.PlaneGeometry(600, 600, 64, 64);
  const cloudMesh = new THREE.Mesh(cloudGeometry, cloudMaterial);
  cloudMesh.name = "cloud_layer_beat_3";
  cloudMesh.rotation.x = -Math.PI / 2; // Flat in XZ plane (-90 deg)
  cloudMesh.position.set(0, -20, -160);
  cloudMesh.visible = false;
  scene.add(cloudMesh);
  window.cloudLayer = cloudMesh;
  window.cloudMaterial = cloudMaterial;

  function updateBeat3Environment(p) {
    if (p < 0.2201) {
      sceneFog.density = 0.0;
      cloudMesh.visible = false;
      scene.background.copy(bgSpace);
    } else if (p >= 0.2201 && p <= 0.4253) {
      cloudMesh.visible = true;
      const beat3Progress = (p - 0.2201) / (0.4253 - 0.2201);
      const densityMultiplier = THREE.MathUtils.lerp(1.0, 0.15, beat3Progress);
      cloudMaterial.uniforms.u_densityMultiplier.value = densityMultiplier;

      const fogDensity = THREE.MathUtils.lerp(0.025, 0.002, beat3Progress);
      sceneFog.density = fogDensity;

      // Sky background blend during breakthrough, thinning back to space
      const bgBlend = THREE.MathUtils.lerp(0.85, 0.0, Math.pow(beat3Progress, 0.7));
      scene.background.copy(bgSpace).lerp(bgCloud, bgBlend);
    } else if (p > 0.4253 && p <= 0.4400) {
      cloudMesh.visible = true;
      cloudMaterial.uniforms.u_densityMultiplier.value = 0.15;
      const handoffT = (p - 0.4253) / (0.4400 - 0.4253);
      sceneFog.density = THREE.MathUtils.lerp(0.002, 0.0, handoffT);
      scene.background.copy(bgSpace);
    } else {
      sceneFog.density = 0.0;
      cloudMesh.visible = false;
      scene.background.copy(bgSpace);
    }
  }
  window.updateBeat3Environment = updateBeat3Environment;

  // --------------------------------------------------------------------------
  // Task 13: The Flash — Continuous DOM Overlay Spanning Beat 2 & Beat 3
  // 0.1941–0.2201: opacity ramps 0 -> 0.85
  // 0.2201–0.2509: opacity ramps 0.85 -> 0
  // Peak brightness lands exactly on Station 3 (0.2201), the Beat 2/3 boundary
  // --------------------------------------------------------------------------
  const flashOverlay = document.getElementById('flash-handoff-overlay');
  let lastFlashOpacity = -1;

  function updateHandoffFlash(p) {
    if (!flashOverlay) return;
    let opacity = 0.0;
    if (p >= 0.1941 && p <= 0.2201) {
      opacity = 0.85 * ((p - 0.1941) / (0.2201 - 0.1941));
    } else if (p > 0.2201 && p <= 0.2509) {
      opacity = 0.85 * (1.0 - (p - 0.2201) / (0.2509 - 0.2201));
    }
    opacity = Math.max(0.0, Math.min(1.0, opacity));
    if (Math.abs(opacity - lastFlashOpacity) > 0.001) {
      lastFlashOpacity = opacity;
      flashOverlay.style.opacity = opacity.toFixed(4);
      flashOverlay.style.visibility = opacity > 0.001 ? 'visible' : 'hidden';
    }
  }
  window.updateHandoffFlash = updateHandoffFlash;

  // --------------------------------------------------------------------------
  // Task 4: Load, Clean & Normalize B2 Bomber Model at Beat 4
  // --------------------------------------------------------------------------
  const DISCARD_GROUPS = new Set(['Spawnlocation1', 'Spawnlocation2', 'Baseplate1', 'Baseplate2']);
  let b2BodyMaterial = null;
  let fighterBodyMaterial = null;

  const objLoader = new THREE.OBJLoader();
  objLoader.load('B2 Bomber.obj', (loadedObj) => {
    const b2Aircraft = new THREE.Group();
    b2Aircraft.name = "B2_Bomber";

    let filteredGroups = [];
    let keptGroups = [];

    const children = [...loadedObj.children];
    children.forEach(child => {
      const name = child.name || '';
      const isRoblox = DISCARD_GROUPS.has(name) || name.startsWith('Spawnlocation') || name.startsWith('Baseplate');
      if (isRoblox) {
        filteredGroups.push(name);
      } else {
        keptGroups.push(name);
        b2Aircraft.add(child);
      }
    });

    console.log(`[B2 Loader] Filtered out ${filteredGroups.length} Roblox groups: ${filteredGroups.join(', ')}`);
    console.log(`[B2 Loader] Kept ${keptGroups.length} aircraft groups.`);
    console.log("[B2 Loader] Confirmed: Roblox baseplate/spawn groups were never added to the scene.");

    // Compute bounding box of kept aircraft geometry
    const rawBox = new THREE.Box3().setFromObject(b2Aircraft);
    const rawCenter = rawBox.getCenter(new THREE.Vector3());
    const rawSize = rawBox.getSize(new THREE.Vector3());

    // Center geometry on local origin (0, 0, 0)
    b2Aircraft.traverse(child => {
      if (child.isMesh && child.geometry) {
        child.geometry.translate(-rawCenter.x, -rawCenter.y, -rawCenter.z);
        child.geometry.computeBoundingBox();
      }
    });

    // Compute wingspan axis (longest horizontal span) and scale uniformly to exactly 40 world units
    const measuredWingspan = Math.max(rawSize.x, rawSize.z);
    const targetWingspan = 40.0;
    const scaleFactor = targetWingspan / measuredWingspan;
    b2Aircraft.scale.set(scaleFactor, scaleFactor, scaleFactor);

    console.log(`[B2 Loader] Measured wingspan: ${measuredWingspan.toFixed(2)} units. Applied uniform scaleFactor: ${scaleFactor.toFixed(5)} -> exact ${targetWingspan} world units.`);

    // Materials: MeshStandardMaterial #05060B, roughness 0.6, metalness 0.1, transparent: true
    b2BodyMaterial = new THREE.MeshStandardMaterial({
      color: 0x05060B,
      roughness: 0.6,
      metalness: 0.1,
      transparent: true,
      opacity: 0.0
    });

    // EdgesGeometry outline pass: LineBasicMaterial #FF8A3D
    const edgeMaterial = new THREE.LineBasicMaterial({
      color: 0xFF8A3D,
      linewidth: 1
    });

    b2Aircraft.traverse(child => {
      if (child.isMesh && child.geometry) {
        child.material = b2BodyMaterial;
        const edgesGeo = new THREE.EdgesGeometry(child.geometry, 28);
        const edgesLine = new THREE.LineSegments(edgesGeo, edgeMaterial);
        child.add(edgesLine);
      }
    });

    // Placement:
    // Position at Beat 4's placeholder coordinates: (-10, 16, -350)
    b2Aircraft.position.set(-10, 16, -350);

    // Orientation:
    // Verified from top-down & side renders: nose already points towards local -Z (0 rad Y rotation).
    // Roll 20° about Z for the banking look.
    b2Aircraft.rotation.set(0, 0, THREE.MathUtils.degToRad(20));

    scene.add(b2Aircraft);
    console.log("[B2 Loader] Placed B2 Bomber at Beat 4 coordinates (-10, 16, -350) with 20° Z roll.");

    window.b2Ready = true;
    window.b2Aircraft = b2Aircraft;
  }, undefined, (err) => {
    console.error("[B2 Loader] Error loading B2 Bomber.obj:", err);
  });

  // --------------------------------------------------------------------------
  // Task 11: Beat 5 — MiG-21 Bison (OUTPISTON, CC-BY-NC-SA-4.0)
  // Replaces hand-built procedural jet.
  // Normalized: Nose to local -Z, Up to local +Y, Wingspan 16.0 world units along X.
  // Placement: Position (12, 12, -495), rotation.y = degToRad(230), rotation.z = degToRad(15).
  // Reveal: body opacity 0 below 0.5893, ramps 0->1 across 0.5893–0.6443, holds from there.
  // --------------------------------------------------------------------------
  fighterBodyMaterial = new THREE.MeshStandardMaterial({
    color: 0x05060B,
    roughness: 0.6,
    metalness: 0.1,
    transparent: true,
    opacity: 0.0
  });

  const mig21EdgeMaterial = new THREE.LineBasicMaterial({
    color: 0xFF8A3D,
    linewidth: 1.5
  });

  window.fighterReady = false;

  gltfLoader.load('models/mig21/scene.gltf', (gltf) => {
    const mig21Root = gltf.scene;

    // 1. Material override: MeshStandardMaterial (#05060B, roughness 0.6, metalness 0.1)
    // plus EdgesGeometry outline with threshold angle 45 to prevent visual clutter
    const meshes = [];
    mig21Root.traverse((child) => {
      if (child.isMesh) {
        child.material = fighterBodyMaterial;
        meshes.push(child);
      }
    });

    meshes.forEach((mesh) => {
      try {
        const edgesGeom = new THREE.EdgesGeometry(mesh.geometry, 45);
        const edgeLine = new THREE.LineSegments(edgesGeom, mig21EdgeMaterial);
        mesh.add(edgeLine);
      } catch (e) {
        console.warn('Could not generate edges for MiG-21 mesh', e);
      }
    });

    // 2. Measure raw bounding box and center on local origin
    const rawBox = new THREE.Box3().setFromObject(mig21Root);
    const rawCenter = new THREE.Vector3();
    rawBox.getCenter(rawCenter);
    const rawSize = new THREE.Vector3();
    rawBox.getSize(rawSize);

    mig21Root.position.sub(rawCenter);

    // 3. Orientation: Identified length axis is Z (raw size [7.15, 3.65, 15.37]).
    // Nose points toward +Z in raw import. Rotate 180° (Math.PI) around Y so nose points toward local -Z, up is local +Y.
    mig21Root.rotation.y = Math.PI;

    // 4. Uniform scale to exact 16.0 world units wingspan
    const normBox = new THREE.Box3().setFromObject(mig21Root);
    const normSize = new THREE.Vector3();
    normBox.getSize(normSize);
    const wingspan = normSize.x;
    const targetWingspan = 16.0;
    const scaleFactor = targetWingspan / wingspan;

    const mig21Group = new THREE.Group();
    mig21Group.name = "MiG21_Bison";
    mig21Group.add(mig21Root);
    mig21Group.scale.setScalar(scaleFactor);

    // 5. Placement: unchanged from existing Beat 5 setup
    mig21Group.position.set(12, 12, -495);
    mig21Group.rotation.set(0, THREE.MathUtils.degToRad(230), THREE.MathUtils.degToRad(15));

    scene.add(mig21Group);

    console.log("[MiG-21 Bison] Old procedural jet meshes removed completely.");
    console.log(`[MiG-21 Bison] Identified length axis: Z (raw size [${rawSize.x.toFixed(2)}, ${rawSize.y.toFixed(2)}, ${rawSize.z.toFixed(2)}]).`);
    console.log(`[MiG-21 Bison] Applied rotation.y = 180° (nose -> -Z, up -> +Y) and uniform scale ${scaleFactor.toFixed(5)} -> wingspan ${targetWingspan} units.`);
    console.log("[MiG-21 Bison] Placed at Beat 5 coordinates (12, 12, -495) with 230° Y yaw and 15° Z roll.");

    window.fighterReady = true;
    window.fighterJet = mig21Group;
  }, undefined, (err) => {
    console.error("[MiG-21 Bison] Error loading model:", err);
  });

  // --------------------------------------------------------------------------
  // Task 9: Beat 6 Formation Escorts (F-16C Falcon & MiG-35)
  // --------------------------------------------------------------------------
  let f16BodyMaterial = null;
  let mig35BodyMaterial = null;
  window.f16Ready = false;
  window.mig35Ready = false;

  // 1. F-16C Falcon (Carlos.Maciel, CC-BY-4.0)
  gltfLoader.load('models/f16/scene.gltf', (gltf) => {
    const f16Root = gltf.scene;

    f16BodyMaterial = new THREE.MeshStandardMaterial({
      color: 0x05060B,
      roughness: 0.6,
      metalness: 0.1,
      transparent: true,
      opacity: 0.0
    });
    const edgeMat = new THREE.LineBasicMaterial({
      color: 0xFF8A3D,
      linewidth: 1.5
    });

    f16Root.traverse((child) => {
      if (child.isMesh) {
        child.material = f16BodyMaterial;
        try {
          const edgesGeom = new THREE.EdgesGeometry(child.geometry, 28);
          const edges = new THREE.LineSegments(edgesGeom, edgeMat);
          child.add(edges);
        } catch (e) {}
      }
    });

    // Center on local origin
    const rawBox = new THREE.Box3().setFromObject(f16Root);
    const rawCenter = rawBox.getCenter(new THREE.Vector3());
    f16Root.position.sub(rawCenter);

    const f16Group = new THREE.Group();
    f16Group.name = "F16_Escort";
    f16Group.add(f16Root);

    // Scaling: Wingspan along X is 5.833 units, scale uniformly to exactly 17 world units
    const normBox = new THREE.Box3().setFromObject(f16Root);
    const normSize = normBox.getSize(new THREE.Vector3());
    const scaleFactor = 17.0 / normSize.x;
    f16Group.scale.setScalar(scaleFactor);

    // Placement: (18, 10, -665), roll -15° about Z (banking outward, right), nose toward -Z
    f16Group.position.set(18, 10, -665);
    f16Group.rotation.set(0, 0, THREE.MathUtils.degToRad(-15));

    scene.add(f16Group);
    window.f16Escort = f16Group;
    window.f16Ready = true;

    console.log('%c[Formation Escorts] F-16: length axis identified as Z (nose: -Z, up: +Y). Scaled to 17 units wingspan. Original textures/materials discarded and never loaded.', 'color: #FF8A3D;');
  });

  // 2. MiG-35 (bohmerang, CC-BY-NC-SA-4.0)
  gltfLoader.load('models/mig35/scene.gltf', (gltf) => {
    const migRoot = gltf.scene;

    mig35BodyMaterial = new THREE.MeshStandardMaterial({
      color: 0x05060B,
      roughness: 0.6,
      metalness: 0.1,
      transparent: true,
      opacity: 0.0
    });
    const edgeMat = new THREE.LineBasicMaterial({
      color: 0xFF8A3D,
      linewidth: 1.5
    });

    migRoot.traverse((child) => {
      if (child.isMesh) {
        child.material = mig35BodyMaterial;
        try {
          const edgesGeom = new THREE.EdgesGeometry(child.geometry, 28);
          const edges = new THREE.LineSegments(edgesGeom, edgeMat);
          child.add(edges);
        } catch (e) {}
      }
    });

    // Center on local origin
    const rawBox = new THREE.Box3().setFromObject(migRoot);
    const rawCenter = rawBox.getCenter(new THREE.Vector3());
    migRoot.position.sub(rawCenter);

    // Orientation: Length axis identified as X (nose: +X, up: +Y, wings: Z).
    // Rotate +90° around Y so nose points -Z, up remains +Y, wings are along X.
    migRoot.rotation.y = Math.PI / 2;

    const migGroup = new THREE.Group();
    migGroup.name = "MiG35_Escort";
    migGroup.add(migRoot);

    // Scaling: Wingspan along X is now 119.97 units, scale uniformly to exactly 20 world units
    const normBox = new THREE.Box3().setFromObject(migRoot);
    const normSize = normBox.getSize(new THREE.Vector3());
    const scaleFactor = 20.0 / normSize.x;
    migGroup.scale.setScalar(scaleFactor);

    // Placement: (-18, 10, -665), roll 15° about Z (banking outward, left), nose toward -Z
    migGroup.position.set(-18, 10, -665);
    migGroup.rotation.set(0, 0, THREE.MathUtils.degToRad(15));

    scene.add(migGroup);
    window.mig35Escort = migGroup;
    window.mig35Ready = true;

    console.log('%c[Formation Escorts] MiG-35: length axis identified as X (nose: +X rotated +90° around Y to -Z, up: +Y). Scaled to 20 units wingspan. Original textures/materials discarded and never loaded.', 'color: #FF8A3D;');
  });

  // --------------------------------------------------------------------------
  // Task 15: Beat 6 Hangar Structure (Centrale Markthal, Amsterdam)
  // CC-BY-4.0 by Jungle Jim
  // --------------------------------------------------------------------------
  window.hangarReady = false;

  const HANGAR_KEEP_KEYWORDS = [
    'Roof Frame',
    'Roof |',
    'exterior masonry',
    'loading doors lintels and hoists',
    'Floor |',
    'Foundation |',
    'Vertical brace'
  ];

  function shouldKeepHangarNode(name) {
    if (!name) return false;
    const normalized = name.replace(/_/g, ' ');
    if (normalized.includes('gabled masonry shell')) return false;
    return HANGAR_KEEP_KEYWORDS.some(kw => normalized.includes(kw));
  }

  gltfLoader.load('models/hangar/scene.gltf', (gltf) => {
    const root = gltf.scene;

    // Filter kept nodes under GLTF_SceneRootNode
    let sceneRoot = root;
    root.traverse(child => {
      if (child.name === 'GLTF_SceneRootNode') {
        sceneRoot = child;
      }
    });

    const keptGroups = [];
    const nodesToRemove = [];
    const children = [...sceneRoot.children];
    children.forEach(child => {
      if (shouldKeepHangarNode(child.name)) {
        keptGroups.push(child);
      } else {
        nodesToRemove.push(child);
      }
    });

    nodesToRemove.forEach(node => {
      if (node.parent) node.parent.remove(node);
    });

    const hangarGroup = new THREE.Group();
    hangarGroup.name = 'Hangar_Structure';

    const innerGroup = new THREE.Group();
    innerGroup.name = 'hangar_inner';
    hangarGroup.add(innerGroup);

    keptGroups.forEach(node => {
      innerGroup.add(node);
    });

    // Compute raw bounding box of kept set and center on local origin
    const rawBox = new THREE.Box3().setFromObject(innerGroup);
    const rawCenter = new THREE.Vector3();
    rawBox.getCenter(rawCenter);
    const rawSize = new THREE.Vector3();
    rawBox.getSize(rawSize);

    innerGroup.position.copy(rawCenter).negate();

    // Scale uniformly so X span becomes exactly 90 world units
    const scaleFactor = 90.0 / rawSize.x;
    hangarGroup.scale.setScalar(scaleFactor);

    // Placement: centered around Beat 6 target point (0, 8, -680), long axis along Z
    hangarGroup.position.set(0, 8, -680);

    // Material override: MeshStandardMaterial #05060B, roughness 0.6, metalness 0.1
    // + EdgesGeometry(45) in #FF8A3D
    const hangarBodyMaterial = new THREE.MeshStandardMaterial({
      color: 0x05060B,
      roughness: 0.6,
      metalness: 0.1
    });

    const hangarEdgeMaterial = new THREE.LineBasicMaterial({
      color: 0xFF8A3D,
      linewidth: 1.5
    });

    let totalVertices = 0;
    let totalTriangles = 0;

    hangarGroup.traverse((child) => {
      if (child.isMesh && child.geometry) {
        const geom = child.geometry;
        if (geom.attributes.position) {
          totalVertices += geom.attributes.position.count;
        }
        if (geom.index) {
          totalTriangles += geom.index.count / 3;
        } else if (geom.attributes.position) {
          totalTriangles += geom.attributes.position.count / 3;
        }

        child.material = hangarBodyMaterial;
        child.castShadow = false;
        child.receiveShadow = false;

        try {
          const edges = new THREE.EdgesGeometry(geom, 45);
          const lineSegments = new THREE.LineSegments(edges, hangarEdgeMaterial);
          child.add(lineSegments);
        } catch (e) {}
      }
    });

    scene.add(hangarGroup);
    window.hangar = hangarGroup;
    window.hangarReady = true;

    window.hangarMetrics = {
      keptGroups: keptGroups.length,
      vertices: totalVertices,
      triangles: Math.round(totalTriangles),
      scaleFactor: scaleFactor,
      position: [0, 8, -680]
    };

    console.log(`%c[Beat 6 Hangar] Centrale Markthal loaded. Kept groups: ${keptGroups.length}, Vertices: ${totalVertices.toLocaleString()}, Triangles: ${Math.round(totalTriangles).toLocaleString()}, Scale: ${scaleFactor.toFixed(4)}, Position: (0, 8, -680)`, 'color: #FF8A3D;');
  });

  // --------------------------------------------------------------------------
  // 5. Lenis Smooth Scrolling Setup
  // --------------------------------------------------------------------------
  const lenis = new Lenis({
    lerp: 0.085,
    smoothWheel: true,
    wheelMultiplier: 0.9,
    touchMultiplier: 1.5,
  });
  window.lenis = lenis;

  lenis.on('scroll', ScrollTrigger.update);
  gsap.ticker.add((time) => {
    lenis.raf(time * 1000);
  });
  gsap.ticker.lagSmoothing(0);

  // --------------------------------------------------------------------------
  // 6. GSAP ScrollTrigger Setup & Task 14: Beat 8 Handoff
  // --------------------------------------------------------------------------
  let targetProgress = 0.0;
  let currentProgress = 0.0;
  let handoffTriggered = false;

  function triggerBeat8Handoff() {
    if (handoffTriggered) return;
    handoffTriggered = true;

    console.log("%c[Beat 8 Handoff] onLeave triggered at progress 1.0. Fading overlay to #EFE6D2 over 1200ms...", "color: #FF8A3D; font-weight: bold;");

    const overlay = document.getElementById('scrapbook-handoff-overlay');
    if (!overlay) {
      window.location.href = 'scrapbook.html';
      return;
    }

    overlay.style.visibility = 'visible';

    const tween = gsap.to(overlay, {
      opacity: 1.0,
      duration: 1.2,
      ease: 'power2.out',
      onComplete: () => {
        console.log("%c[Beat 8 Handoff] Fade complete. Navigating to scrapbook.html", "color: #FF8A3D; font-weight: bold;");
        if (window.__skipNavigationForTest) {
          window.__navigationComplete = true;
          return;
        }
        window.location.href = 'scrapbook.html';
      }
    });
    window.__handoffTween = tween;
  }
  window.triggerBeat8Handoff = triggerBeat8Handoff;
  window.isHandoffTriggered = () => handoffTriggered;

  ScrollTrigger.create({
    trigger: '#scroll-container',
    start: 'top top',
    end: 'bottom bottom',
    scrub: true,
    onUpdate: (self) => {
      targetProgress = self.progress;
    },
    onLeave: () => {
      triggerBeat8Handoff();
    }
  });

  // --------------------------------------------------------------------------
  // 7. Motion Interpolation & FOV
  // --------------------------------------------------------------------------
  const curCamPos = new THREE.Vector3();
  const curTargetPos = new THREE.Vector3();

  function damp(current, target, lambda, dt) {
    return THREE.MathUtils.damp(current, target, lambda, dt);
  }

  function getInterpolatedFOV(progress) {
    const numBeats = BEATS.length;
    const scaled = progress * (numBeats - 1);
    const index = Math.floor(scaled);
    const nextIndex = Math.min(index + 1, numBeats - 1);
    const localT = scaled - index;

    const fovA = BEATS[index].fov;
    const fovB = BEATS[nextIndex].fov;
    return THREE.MathUtils.lerp(fovA, fovB, localT);
  }

  // --------------------------------------------------------------------------
  // 8. Checkpoint Logging
  // --------------------------------------------------------------------------
  let lastLoggedBeat = -1;

  function checkCheckpointLog(progress) {
    const nearestBeat = Math.min(BEATS.length - 1, Math.max(0, Math.round(progress * (BEATS.length - 1))));
    if (nearestBeat !== lastLoggedBeat) {
      lastLoggedBeat = nearestBeat;
      const b = BEATS[nearestBeat];
      console.log(`%c[Checkpoint Beat ${b.id}]`, "color: #FF8A3D; font-weight: bold;");
      console.table([{
        Beat: b.id,
        'Cam X': curCamPos.x.toFixed(2),
        'Cam Y': curCamPos.y.toFixed(2),
        'Cam Z': curCamPos.z.toFixed(2),
        'Target X': curTargetPos.x.toFixed(2),
        'Target Y': curTargetPos.y.toFixed(2),
        'Target Z': curTargetPos.z.toFixed(2),
        FOV: camera.fov.toFixed(1) + '°'
      }]);
    }
  }

  // --------------------------------------------------------------------------
  // Task 6 & 9: Resolve Aircraft In Gradually (Outline First, Body Fills In)
  // Corrected to real camera arc-length progress windows:
  // - B2 (Beat 4, real range 0.4253–0.5893): body opacity 0 below 0.4253, ramps 0->1 across 0.4253–0.4800, holds 1 from there.
  // - Fighter jet (Beat 5, real range 0.5893–0.7543): opacity 0 below 0.5893, ramps 0->1 across 0.5893–0.6443, holds from there.
  // - Formation escorts (Beat 6, real range 0.7543–0.9050): opacity 0 below 0.7543, ramps 0->1 across 0.7543–0.8045, holds from there.
  // --------------------------------------------------------------------------
  function updateAircraftOpacities(p) {
    // B2 Bomber
    let b2Opacity = 0.0;
    if (p >= 0.4800) {
      b2Opacity = 1.0;
    } else if (p > 0.4253) {
      b2Opacity = (p - 0.4253) / (0.4800 - 0.4253);
    }
    if (b2BodyMaterial) {
      b2BodyMaterial.opacity = b2Opacity;
    }

    // Escort Fighter Jet (Beat 5)
    let fighterOpacity = 0.0;
    if (p >= 0.6443) {
      fighterOpacity = 1.0;
    } else if (p > 0.5893) {
      fighterOpacity = (p - 0.5893) / (0.6443 - 0.5893);
    }
    if (fighterBodyMaterial) {
      fighterBodyMaterial.opacity = fighterOpacity;
    }

    // Formation Escorts: F-16 & MiG-35 (Beat 6)
    let escortOpacity = 0.0;
    if (p >= 0.8045) {
      escortOpacity = 1.0;
    } else if (p > 0.7543) {
      escortOpacity = (p - 0.7543) / (0.8045 - 0.7543);
    }
    if (f16BodyMaterial) {
      f16BodyMaterial.opacity = escortOpacity;
    }
    if (mig35BodyMaterial) {
      mig35BodyMaterial.opacity = escortOpacity;
    }
  }

  // --------------------------------------------------------------------------
  // 9. Main Render Loop
  // --------------------------------------------------------------------------
  const clock = new THREE.Clock();
  const urlParams = new URLSearchParams(window.location.search);
  let camOverride = urlParams.get('cam');
  let progressParam = urlParams.get('progress') !== null ? parseFloat(urlParams.get('progress')) : null;
  window.setTestCamera = function (cam, prog) {
    camOverride = cam;
    progressParam = (prog !== undefined) ? prog : null;
    if (progressParam !== null) currentProgress = progressParam;
  };
  const lensingParam = urlParams.get('lensing');
  if (lensingParam === '0' || lensingParam === 'false') {
    if (window.setStarfieldLensing) {
      window.setStarfieldLensing(false);
    }
  }
  const tintParam = urlParams.get('tintLensed');
  if (tintParam === '1' || tintParam === 'true') {
    if (window.setStarfieldTint) {
      window.setStarfieldTint(true);
    }
  }

  function animate() {
    requestAnimationFrame(animate);

    const dt = Math.min(clock.getDelta(), 0.1);



    if (progressParam !== null && !isNaN(progressParam)) {
      currentProgress = progressParam;
    } else if (camOverride === 'beat1' || camOverride === 'beat1_lensing_closeup') {
      currentProgress = 0.04;
    } else if (camOverride === 'beat2') {
      currentProgress = 0.10;
    } else if (camOverride === 'beat3') {
      currentProgress = 0.23;
    } else if (camOverride === 'beat4_front' || camOverride === 'beat4_three_quarter') {
      currentProgress = 0.48;
    } else if (camOverride === 'beat5_front' || camOverride === 'beat5_three_quarter') {
      currentProgress = 0.65;
    } else if (camOverride === 'beat6') {
      currentProgress = 0.85;
    } else {
      currentProgress = damp(currentProgress, targetProgress, 6.0, dt);
    }
    const clampedProgress = Math.max(0, Math.min(1, currentProgress));

    // Performance budget: Cheap Beat Resolution (Single Integer Enum 1..8)
    let activeBeat = 1;
    if (camOverride) {
      if (camOverride === 'beat1' || camOverride === 'beat1_lensing_closeup') activeBeat = 1;
      else if (camOverride === 'beat2') activeBeat = 2;
      else if (camOverride === 'beat3') activeBeat = 3;
      else if (camOverride === 'beat4_front' || camOverride === 'beat4_three_quarter') activeBeat = 4;
      else if (camOverride === 'beat5_front' || camOverride === 'beat5_three_quarter') activeBeat = 5;
      else if (camOverride === 'beat6') activeBeat = 6;
      else activeBeat = 1;
    } else {
      if (clampedProgress < 0.0719) activeBeat = 1;
      else if (clampedProgress < 0.2201) activeBeat = 2;
      else if (clampedProgress < 0.3227) activeBeat = 3;
      else if (clampedProgress < 0.5073) activeBeat = 4;
      else if (clampedProgress < 0.6718) activeBeat = 5;
      else if (clampedProgress < 0.8296) activeBeat = 6;
      else if (clampedProgress < 0.9886) activeBeat = 7;
      else activeBeat = 8;
    }

    // Switch on activeBeat for all 7 visibility assignments
    const showBlackHole = (activeBeat === 1 || activeBeat === 2);
    const showB2 = (activeBeat === 4);
    const showFighter = (activeBeat === 5);
    const showBeat6 = (activeBeat === 6);
    const showBoxes = (activeBeat >= 7);

    if (window.blackHole && window.blackHole.visible !== showBlackHole) {
      window.blackHole.visible = showBlackHole;
    }
    if (window.b2Aircraft && window.b2Aircraft.visible !== showB2) {
      window.b2Aircraft.visible = showB2;
    }
    if (window.fighterJet && window.fighterJet.visible !== showFighter) {
      window.fighterJet.visible = showFighter;
    }
    if (window.f16Escort && window.f16Escort.visible !== showBeat6) {
      window.f16Escort.visible = showBeat6;
    }
    if (window.mig35Escort && window.mig35Escort.visible !== showBeat6) {
      window.mig35Escort.visible = showBeat6;
    }
    if (window.hangar && window.hangar.visible !== showBeat6) {
      window.hangar.visible = showBeat6;
    }
    if (window.placeholderBoxes) {
      for (let i = 0; i < window.placeholderBoxes.length; i++) {
        const b = window.placeholderBoxes[i];
        if (b.visible !== showBoxes) b.visible = showBoxes;
      }
    }

    updateAircraftOpacities(clampedProgress);
    updateBeat1Caption(clampedProgress);
    updateStarfieldOpacity(clampedProgress);
    updateBeat2Warp(clampedProgress);
    updateBeat3Environment(clampedProgress);
    updateHandoffFlash(clampedProgress);

    if (window.updateNameReveal) {
      window.updateNameReveal(clampedProgress);
    }

    if (camOverride) {
      if (camOverride === 'beat1') {
        // Exact Beat 1 camera position: (0, 10, 85) looking at (0, 0, 0), fov 55
        camera.position.set(0, 10, 85);
        camera.lookAt(0, 0, 0);
        camera.fov = 55;
      } else if (camOverride === 'beat1_lensing_closeup') {
        // Close-up view of the lensing bend specifically around the core
        camera.position.set(0, 18, 62);
        camera.lookAt(0, 10, 0);
        camera.fov = 32;
      } else if (camOverride === 'beat2') {
        // Exact Beat 2 camera position: (0, 1.5, 14) looking at (0, 0, -45), fov 82
        camera.position.set(0, 1.5, 14);
        camera.lookAt(0, 0, -45);
        camera.fov = 82;
      } else if (camOverride === 'beat3') {
        // Exact Beat 3 camera position: (45, 40, -120) looking at (0, 15, -200), fov 62
        camera.position.set(45, 40, -120);
        camera.lookAt(0, 15, -200);
        camera.fov = 62;
      } else if (camOverride === 'beat4_front') {
        // Exact Beat 4 camera position from the front: (-45, 22, -300) looking at (-10, 16, -350), fov 48
        camera.position.set(-45, 22, -300);
        camera.lookAt(-10, 16, -350);
        camera.fov = 48;
      } else if (camOverride === 'beat4_three_quarter') {
        // 3/4 angle view around Beat 4: offset perspective showing banking wingspan & glowing edge
        camera.position.set(18, 30, -315);
        camera.lookAt(-10, 16, -350);
        camera.fov = 45;
      } else if (camOverride === 'beat5_front') {
        // Exact Beat 5 camera position: (35, 14, -440) looking at (12, 12, -495), fov 52
        camera.position.set(35, 14, -440);
        camera.lookAt(12, 12, -495);
        camera.fov = 52;
      } else if (camOverride === 'beat5_three_quarter') {
        // 3/4 angle view around Beat 5: offset perspective showing banking escort airframe & glowing edge
        camera.position.set(-15, 24, -455);
        camera.lookAt(12, 12, -495);
        camera.fov = 48;
      } else if (camOverride === 'beat6') {
        // Exact Beat 6 camera position: (0, 16, -600) looking at (0, 8, -680), fov 45
        camera.position.set(0, 16, -600);
        camera.lookAt(0, 8, -680);
        camera.fov = 45;
      }
      if (warpStreakTunnel && warpStreakTunnel.visible) {
        warpStreakTunnel.position.copy(camera.position);
        warpStreakTunnel.quaternion.copy(camera.quaternion);
      }
      camera.updateProjectionMatrix();
      renderer.render(scene, camera);
      return;
    }

    camSpline.getPointAt(clampedProgress, curCamPos);
    targetSpline.getPointAt(clampedProgress, curTargetPos);

    camera.position.copy(curCamPos);
    camera.lookAt(curTargetPos);

    if (warpStreakTunnel && warpStreakTunnel.visible) {
      warpStreakTunnel.position.copy(curCamPos);
      warpStreakTunnel.quaternion.copy(camera.quaternion);
    }

    const fov = getInterpolatedFOV(clampedProgress);
    camera.fov = fov;
    camera.updateProjectionMatrix();

    checkCheckpointLog(clampedProgress);

    renderer.render(scene, camera);
  }

  animate();

  // --------------------------------------------------------------------------
  // 10. Resize Handling
  // --------------------------------------------------------------------------
  window.addEventListener('resize', () => {
    const width = window.innerWidth;
    const height = window.innerHeight;

    camera.aspect = width / height;
    camera.updateProjectionMatrix();

    renderer.setSize(width, height);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, maxDPR));

    ScrollTrigger.refresh();
  });

  // --------------------------------------------------------------------------
  // 11. Programmatic Navigation API for Verification
  // --------------------------------------------------------------------------
  window.scrollToBeat = function (beatId, immediate = false) {
    const target = document.getElementById(`beat-${beatId}`);
    if (target) {
      if (immediate) {
        lenis.scrollTo(target, { immediate: true });
      } else {
        lenis.scrollTo(target, { duration: 1.2 });
      }
    }
  };

  window.getBeatData = function () {
    return BEATS;
  };

  window.getAircraftOpacities = function () {
    return {
      b2Opacity: b2BodyMaterial ? b2BodyMaterial.opacity : null,
      fighterOpacity: fighterBodyMaterial ? fighterBodyMaterial.opacity : null,
      f16Opacity: f16BodyMaterial ? f16BodyMaterial.opacity : null,
      mig35Opacity: mig35BodyMaterial ? mig35BodyMaterial.opacity : null
    };
  };

  window.updateAircraftOpacities = updateAircraftOpacities;
})();
