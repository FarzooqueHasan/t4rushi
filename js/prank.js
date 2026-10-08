/**
 * Tarushi Birthday Site — Part 1: The Prank
 * 
 * Sequence:
 * 1. Kawaii layer visible, Fredoka heading, original bow mascot, visitor counter, guestbook, sparkle trail, 2A hold button.
 * 2. Hold completes (1200ms) -> desaturates to grayscale over 400ms.
 * 3. Centered text fades in over desaturated layer: "did you really think my skills are this bad?" (holds 1200ms).
 * 4. 2B burn/dissolve shader (800ms, rim-color addendum applied) plays over the whole desaturated layer.
 * 5. On completion, remove #prank-layer from the DOM entirely. Task 1 rig is visible underneath at Beat 1.
 */

(function () {
  'use strict';

  const prankLayer = document.getElementById('prank-layer');
  if (!prankLayer) return;

  const prankContent = document.getElementById('prank-content');
  const holdBtn = document.getElementById('hold-btn');
  const ringProgress = document.getElementById('ring-progress');
  const flashOverlay = document.getElementById('flash-overlay');
  const punchlineText = document.getElementById('punchline-text');
  const guestbookBtn = document.getElementById('guestbook-btn');
  const guestbookTooltip = document.getElementById('guestbook-tooltip');
  const burnCanvas = document.getElementById('burn-canvas');

  const CIRCUMFERENCE = 2 * Math.PI * 50; // 314.159
  const HOLD_DURATION = 1200; // ms
  const RELEASE_DURATION = 300; // ms

  let isHolding = false;
  let holdStartTime = 0;
  let currentProgress = 0;
  let hasCompleted = false;
  let releaseStartTime = 0;
  let releaseStartProgress = 0;
  let rafId = null;
  let sparkleActive = true;

  // --------------------------------------------------------------------------
  // 1. Sparkle Cursor Trail
  // --------------------------------------------------------------------------
  let lastSparkleTime = 0;
  function onPointerMove(e) {
    if (!sparkleActive) return;
    const now = performance.now();
    if (now - lastSparkleTime < 40) return; // throttle
    lastSparkleTime = now;

    const sparkle = document.createElement('div');
    sparkle.className = 'sparkle-particle';
    sparkle.style.left = e.clientX + 'px';
    sparkle.style.top = e.clientY + 'px';

    // SVG 4-point star
    sparkle.innerHTML = `
      <svg width="18" height="18" viewBox="0 0 18 18">
        <path d="M9 0 L11 7 L18 9 L11 11 L9 18 L7 11 L0 9 L7 7 Z" fill="#FF5C8A" />
      </svg>
    `;
    document.body.appendChild(sparkle);

    setTimeout(() => {
      sparkle.remove();
    }, 600);
  }

  const isTouchDevice = ('ontouchstart' in window) || (navigator.maxTouchPoints > 0);
  if (!isTouchDevice) {
    window.addEventListener('pointermove', onPointerMove);
  }

  // --------------------------------------------------------------------------
  // 2. Interactive Guestbook Modal Logic
  // --------------------------------------------------------------------------
  const guestbookModal = document.getElementById('prank-guestbook-modal');
  const guestbookBackdrop = document.getElementById('guestbook-backdrop');
  const guestbookClose = document.getElementById('guestbook-close');
  const guestbookForm = document.getElementById('guestbook-form');
  const guestbookName = document.getElementById('guestbook-name');
  const guestbookMsg = document.getElementById('guestbook-msg');
  const guestbookList = document.getElementById('guestbook-entries-list');
  const stickerChips = document.querySelectorAll('.sticker-chip');

  let activeSticker = '🎂';

  const DEFAULT_WISHES = [
    { name: 'Shreya ✨', msg: 'Happy Birthday Queen!! Keep shining brighter than a supernova! 💖', sticker: '🎂' },
    { name: 'Aryan 🚀', msg: 'To the coolest pilot in AEROSS, have the happiest 20th! Keep soaring high! ✈️', sticker: '🚀' },
    { name: 'Ria 🌸', msg: 'Happy happy birthday Tarushi!! May this year bring endless adventures! ♡', sticker: '✨' },
    { name: 'Kabir 🏀', msg: 'Court MVP and sweetest friend ever! Happy birthday Tarushi! 🏀🎉', sticker: '🧸' }
  ];

  function getSavedWishes() {
    try {
      const data = localStorage.getItem('tarushi_guestbook_wishes');
      return data ? JSON.parse(data) : DEFAULT_WISHES;
    } catch (_) {
      return DEFAULT_WISHES;
    }
  }

  function renderGuestbookEntries() {
    if (!guestbookList) return;
    const wishes = getSavedWishes();
    guestbookList.innerHTML = '';
    wishes.forEach(item => {
      const card = document.createElement('div');
      card.className = 'guestbook-entry';
      card.innerHTML = `
        <div class="guestbook-entry-header">
          <span class="guestbook-entry-name">${escapeHtml(item.name)}</span>
          <span class="guestbook-entry-sticker">${item.sticker || '💖'}</span>
        </div>
        <p class="guestbook-entry-msg">${escapeHtml(item.msg)}</p>
      `;
      guestbookList.appendChild(card);
    });
  }

  function escapeHtml(str) {
    return String(str || '').replace(/[&<>"']/g, m => ({
      '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'
    })[m]);
  }

  function openGuestbook() {
    if (!guestbookModal) return;
    renderGuestbookEntries();
    guestbookModal.classList.add('open');
    guestbookModal.setAttribute('aria-hidden', 'false');
  }

  function closeGuestbook() {
    if (!guestbookModal) return;
    guestbookModal.classList.remove('open');
    guestbookModal.setAttribute('aria-hidden', 'true');
  }

  if (guestbookBtn) {
    guestbookBtn.addEventListener('click', (e) => {
      e.stopPropagation();
      openGuestbook();
    });
  }
  if (guestbookClose) guestbookClose.addEventListener('click', closeGuestbook);
  if (guestbookBackdrop) guestbookBackdrop.addEventListener('click', closeGuestbook);

  stickerChips.forEach(chip => {
    chip.addEventListener('click', () => {
      stickerChips.forEach(c => c.classList.remove('active'));
      chip.classList.add('active');
      activeSticker = chip.getAttribute('data-sticker') || '🎂';
    });
  });

  if (guestbookForm) {
    guestbookForm.addEventListener('submit', (e) => {
      e.preventDefault();
      const name = (guestbookName.value || '').trim();
      const msg = (guestbookMsg.value || '').trim();
      if (!name || !msg) return;

      const wishes = getSavedWishes();
      wishes.unshift({ name, msg, sticker: activeSticker });
      try {
        localStorage.setItem('tarushi_guestbook_wishes', JSON.stringify(wishes));
      } catch (_) {}

      renderGuestbookEntries();
      guestbookMsg.value = '';

      // Cute burst animation
      const submitBtn = guestbookForm.querySelector('.guestbook-submit-btn');
      if (submitBtn) {
        const originalText = submitBtn.textContent;
        submitBtn.textContent = 'Signed with Love! 💖';
        setTimeout(() => { submitBtn.textContent = originalText; }, 1800);
      }
    });
  }

  // --------------------------------------------------------------------------
  // 2B. Retro Pink Turntable / Record Player & Happy Birthday Web Audio Synth
  // --------------------------------------------------------------------------
  const vinylDisc = document.getElementById('vinyl-disc');
  const tonearm = document.getElementById('tonearm-assembly');
  const turntableLed = document.getElementById('turntable-led');
  const turntableStatus = document.getElementById('turntable-status-text');
  const turntablePlayBtn = document.getElementById('turntable-play-btn');
  const playBtnIcon = document.getElementById('play-btn-icon');
  const playBtnLabel = document.getElementById('play-btn-label');

  let audioCtx = null;
  let isMusicPlaying = false;
  let audioTimerIds = [];

  // Melody: Happy Birthday to You in C Major
  // Note frequencies
  const NOTES = {
    G4: 392.00, A4: 440.00, B4: 493.88,
    C5: 523.25, D5: 587.33, E5: 659.25, F5: 698.46, G5: 783.99
  };

  const BDAY_MELODY = [
    // Happy Birthday to you
    { note: 'G4', dur: 0.35, pause: 0.1 },
    { note: 'G4', dur: 0.35, pause: 0.1 },
    { note: 'A4', dur: 0.7, pause: 0.1 },
    { note: 'G4', dur: 0.7, pause: 0.1 },
    { note: 'C5', dur: 0.7, pause: 0.1 },
    { note: 'B4', dur: 1.2, pause: 0.3 },
    // Happy Birthday to you
    { note: 'G4', dur: 0.35, pause: 0.1 },
    { note: 'G4', dur: 0.35, pause: 0.1 },
    { note: 'A4', dur: 0.7, pause: 0.1 },
    { note: 'G4', dur: 0.7, pause: 0.1 },
    { note: 'D5', dur: 0.7, pause: 0.1 },
    { note: 'C5', dur: 1.2, pause: 0.3 },
    // Happy Birthday dear Tarushi
    { note: 'G4', dur: 0.35, pause: 0.1 },
    { note: 'G4', dur: 0.35, pause: 0.1 },
    { note: 'G5', dur: 0.7, pause: 0.1 },
    { note: 'E5', dur: 0.7, pause: 0.1 },
    { note: 'C5', dur: 0.7, pause: 0.1 },
    { note: 'B4', dur: 0.7, pause: 0.1 },
    { note: 'A4', dur: 1.2, pause: 0.3 },
    // Happy Birthday to you
    { note: 'F5', dur: 0.35, pause: 0.1 },
    { note: 'F5', dur: 0.35, pause: 0.1 },
    { note: 'E5', dur: 0.7, pause: 0.1 },
    { note: 'C5', dur: 0.7, pause: 0.1 },
    { note: 'D5', dur: 0.7, pause: 0.1 },
    { note: 'C5', dur: 1.6, pause: 1.0 }
  ];

  function playTone(freq, duration, startTime) {
    if (!audioCtx) return;
    const osc1 = audioCtx.createOscillator();
    const osc2 = audioCtx.createOscillator();
    const gainNode = audioCtx.createGain();

    // Sweet celesta/music-box bell tones
    osc1.type = 'sine';
    osc1.frequency.setValueAtTime(freq, startTime);
    osc2.type = 'triangle';
    osc2.frequency.setValueAtTime(freq * 2, startTime); // octave chime harmonic

    // Warm envelope
    gainNode.gain.setValueAtTime(0.0001, startTime);
    gainNode.gain.linearRampToValueAtTime(0.28, startTime + 0.02);
    gainNode.gain.exponentialRampToValueAtTime(0.0001, startTime + duration);

    osc1.connect(gainNode);
    osc2.connect(gainNode);
    gainNode.connect(audioCtx.destination);

    osc1.start(startTime);
    osc2.start(startTime);
    osc1.stop(startTime + duration);
    osc2.stop(startTime + duration);
  }

  function scheduleBdaySong() {
    if (!isMusicPlaying) return;
    if (!audioCtx) {
      audioCtx = new (window.AudioContext || window.webkitAudioContext)();
    }
    if (audioCtx.state === 'suspended') {
      audioCtx.resume();
    }

    let now = audioCtx.currentTime + 0.1;
    let totalTime = 0;

    BDAY_MELODY.forEach(item => {
      const freq = NOTES[item.note] || 440;
      playTone(freq, item.dur, now + totalTime);
      totalTime += item.dur + item.pause;
    });

    const loopTimer = setTimeout(() => {
      if (isMusicPlaying) scheduleBdaySong();
    }, totalTime * 1000);

    audioTimerIds.push(loopTimer);
  }

  function stopBdaySong() {
    isMusicPlaying = false;
    audioTimerIds.forEach(id => clearTimeout(id));
    audioTimerIds = [];
    if (audioCtx && audioCtx.state === 'running') {
      audioCtx.suspend();
    }
  }

  function toggleMusic() {
    if (isMusicPlaying) {
      stopBdaySong();
      if (vinylDisc) vinylDisc.classList.remove('spinning');
      if (tonearm) tonearm.classList.remove('active');
      if (turntableLed) turntableLed.classList.remove('active');
      if (turntableStatus) turntableStatus.textContent = 'PAUSED · CLICK TO PLAY';
      if (playBtnIcon) playBtnIcon.textContent = '▶';
      if (playBtnLabel) playBtnLabel.textContent = 'PLAY POOKIE SONG';
    } else {
      isMusicPlaying = true;
      scheduleBdaySong();
      if (vinylDisc) vinylDisc.classList.add('spinning');
      if (tonearm) tonearm.classList.add('active');
      if (turntableLed) turntableLed.classList.add('active');
      if (turntableStatus) turntableStatus.textContent = 'NOW PLAYING ♡ POOKIE SONG';
      if (playBtnIcon) playBtnIcon.textContent = '❚❚';
      if (playBtnLabel) playBtnLabel.textContent = 'PAUSE SONG';
    }
  }

  if (turntablePlayBtn) turntablePlayBtn.addEventListener('click', toggleMusic);
  if (vinylDisc) vinylDisc.addEventListener('click', toggleMusic);

  // --------------------------------------------------------------------------
  // 3. 2A Hold-to-Proceed Gesture Logic
  // --------------------------------------------------------------------------
  function setProgress(p) {
    currentProgress = Math.max(0, Math.min(1, p));
    const offset = CIRCUMFERENCE * (1 - currentProgress);
    ringProgress.setAttribute('stroke-dashoffset', offset);
    ringProgress.style.strokeDashoffset = `${offset}px`;
  }

  function triggerCompletionFlash(callback) {
    flashOverlay.style.opacity = '1';
    setTimeout(() => {
      flashOverlay.style.transition = 'opacity 0.2s ease-out';
      flashOverlay.style.opacity = '0';
      if (callback) callback();
    }, 120);
  }

  function updateHold(now) {
    if (isHolding && !hasCompleted) {
      const elapsed = now - holdStartTime;
      const p = elapsed / HOLD_DURATION;

      if (p >= 1.0) {
        setProgress(1.0);
        hasCompleted = true;
        isHolding = false;

        console.log("hold-complete");
        triggerCompletionFlash(() => {
          startPrankTransition();
        });
        return;
      } else {
        setProgress(p);
        rafId = requestAnimationFrame(updateHold);
      }
    } else if (!isHolding && currentProgress > 0 && !hasCompleted) {
      const elapsed = now - releaseStartTime;
      const releaseProgress = Math.min(1.0, elapsed / RELEASE_DURATION);
      const p = releaseStartProgress * (1 - releaseProgress);
      setProgress(p);

      if (releaseProgress < 1.0) {
        rafId = requestAnimationFrame(updateHold);
      } else {
        setProgress(0);
      }
    }
  }

  function onPointerDown(e) {
    if (hasCompleted) return;
    try { holdBtn.setPointerCapture(e.pointerId); } catch (_) {}
    isHolding = true;
    holdStartTime = performance.now() - (currentProgress * HOLD_DURATION);
    cancelAnimationFrame(rafId);
    rafId = requestAnimationFrame(updateHold);
  }

  function onPointerUp(e) {
    if (!isHolding || hasCompleted) return;
    try { holdBtn.releasePointerCapture(e.pointerId); } catch (_) {}
    isHolding = false;
    releaseStartTime = performance.now();
    releaseStartProgress = currentProgress;
    cancelAnimationFrame(rafId);
    rafId = requestAnimationFrame(updateHold);
  }

  if (holdBtn) {
    holdBtn.addEventListener('pointerdown', onPointerDown);
    holdBtn.addEventListener('pointerup', onPointerUp);
    holdBtn.addEventListener('pointercancel', onPointerUp);
    holdBtn.addEventListener('pointerleave', onPointerUp);

    // Explicit touch events to guarantee instantaneous response on mobile touch
    holdBtn.addEventListener('touchstart', (e) => {
      e.preventDefault();
      onPointerDown(e);
    }, { passive: false });
    holdBtn.addEventListener('touchend', (e) => {
      e.preventDefault();
      onPointerUp(e);
    }, { passive: false });
    holdBtn.addEventListener('touchcancel', (e) => {
      e.preventDefault();
      onPointerUp(e);
    }, { passive: false });
  }

  // --------------------------------------------------------------------------
  // 4. 2B Burn/Dissolve Shader Setup (Orthographic WebGL Quad)
  // --------------------------------------------------------------------------
  let burnRenderer = null;
  let burnScene = null;
  let burnCamera = null;
  let burnMaterial = null;

  function initBurnShader() {
    if (burnRenderer) return;

    burnScene = new THREE.Scene();
    burnCamera = new THREE.OrthographicCamera(-1, 1, 1, -1, 0, 1);

    burnRenderer = new THREE.WebGLRenderer({
      canvas: burnCanvas,
      antialias: true,
      alpha: true
    });
    burnRenderer.setSize(window.innerWidth, window.innerHeight);
    burnRenderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));

    const vertexShader = `
      varying vec2 vUv;
      void main() {
        vUv = uv;
        gl_Position = vec4(position, 1.0);
      }
    `;

    const fragmentShader = `
      precision highp float;
      varying vec2 vUv;
      uniform float u_progress;
      uniform vec3 u_color;
      uniform float u_edgeWidth;
      uniform vec2 u_resolution;

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
        vec2 aspectUv = vUv;
        aspectUv.x *= (u_resolution.x / u_resolution.y);

        float n = fbm(aspectUv * 5.5);
        float threshold = u_progress * (1.0 + u_edgeWidth);
        float diff = n - threshold;

        if (diff < 0.0) {
          discard;
        }

        vec3 col = u_color;
        if (diff < u_edgeWidth) {
          float rim = 1.0 - (diff / u_edgeWidth);
          // Addendum: 1.4-1.6x intensity, red-biased over green, blue suppressed
          // Stays visibly hot amber-orange (#FFAE42 / #FF9533), never clips to pale cream
          float boost = rim * 1.5;
          col.r = min(1.0, u_color.r * (1.0 + boost * 0.5));
          col.g = min(0.68, u_color.g * (1.0 + boost * 0.25));
          col.b = u_color.b * (1.0 + boost * 0.05);
        }

        gl_FragColor = vec4(col, 1.0);
      }
    `;

    burnMaterial = new THREE.ShaderMaterial({
      vertexShader: vertexShader,
      fragmentShader: fragmentShader,
      uniforms: {
        u_progress: { value: 0.0 },
        u_color: { value: new THREE.Vector3(1.0, 0.541, 0.239) }, // #FF8A3D
        u_edgeWidth: { value: 0.05 },
        u_resolution: { value: new THREE.Vector2(window.innerWidth, window.innerHeight) }
      },
      transparent: true,
      depthWrite: false
    });

    const quad = new THREE.Mesh(new THREE.PlaneGeometry(2, 2), burnMaterial);
    burnScene.add(quad);
  }

  function setBurnProgress(p) {
    initBurnShader();
    burnMaterial.uniforms.u_progress.value = Math.max(0, Math.min(1, p));
    burnRenderer.render(burnScene, burnCamera);
  }

  function playBurn(callback) {
    initBurnShader();
    burnCanvas.style.display = 'block';

    const BURN_DURATION = 800; // ms
    const burnStartTime = performance.now();

    function step(now) {
      const elapsed = now - burnStartTime;
      const p = Math.min(1.0, elapsed / BURN_DURATION);
      burnMaterial.uniforms.u_progress.value = p;
      burnRenderer.render(burnScene, burnCamera);

      if (p < 1.0) {
        requestAnimationFrame(step);
      } else {
        const totalElapsed = performance.now() - burnStartTime;
        console.log("burn-complete. measured duration: " + totalElapsed.toFixed(1) + "ms");
        if (callback) callback();
      }
    }

    requestAnimationFrame(step);
  }

  // --------------------------------------------------------------------------
  // 5. Sequence Handoff: Steps 2, 3, 4, 5
  // --------------------------------------------------------------------------
  function startPrankTransition() {
    sparkleActive = false;

    // Step 2: Desaturate to grayscale over 400ms
    if (prankContent) prankContent.classList.add('desaturated');

    setTimeout(() => {
      // Step 3: Centered text fades in over desaturated layer; holds 1200ms
      punchlineText.style.opacity = '1';

      setTimeout(() => {
        // Step 4: Burn/dissolve (800ms) plays over whole desaturated layer
        if (prankContent) prankContent.classList.add('hidden');
        
        playBurn(() => {
          // Step 5: On completion, remove the Prank layer from the DOM entirely
          prankLayer.remove();
          document.documentElement.classList.remove('prank-active');
          document.body.classList.remove('prank-active');
          if (window.ScrollTrigger) window.ScrollTrigger.refresh();
          console.log("prank-layer removed from DOM. Beat 1 active.");
        });
      }, 1200); // 1200ms hold of punchline text
    }, 400); // 400ms desaturation transition
  }

  // --------------------------------------------------------------------------
  // 6. Verification Helpers & Query State Support
  // --------------------------------------------------------------------------
  const urlParams = new URLSearchParams(window.location.search);
  const prankState = urlParams.get('prankState');

  if (prankState === 'idle') {
    setProgress(0);
  } else if (prankState === 'photobooth') {
    setTimeout(() => {
      const el = document.getElementById('prank-photobooth');
      if (el) el.scrollIntoView({ behavior: 'instant', block: 'start' });
    }, 50);
  } else if (prankState === 'mixtape') {
    setTimeout(() => {
      const el = document.getElementById('prank-mixtape');
      if (el) el.scrollIntoView({ behavior: 'instant', block: 'start' });
    }, 50);
  } else if (prankState === 'gameday') {
    setTimeout(() => {
      const el = document.getElementById('prank-gameday');
      if (el) el.scrollIntoView({ behavior: 'instant', block: 'start' });
    }, 50);
  } else if (prankState === 'hold') {
    setTimeout(() => {
      const el = document.getElementById('prank-hold-screen');
      if (el) el.scrollIntoView({ behavior: 'instant', block: 'start' });
    }, 50);
  } else if (prankState === 'hold50') {
    setTimeout(() => {
      const el = document.getElementById('prank-hold-screen');
      if (el) el.scrollIntoView({ behavior: 'instant', block: 'start' });
    }, 50);
    setProgress(0.5);
  } else if (prankState === 'punchline') {
    setProgress(1.0);
    sparkleActive = false;
    if (prankContent) prankContent.classList.add('desaturated');
    punchlineText.style.opacity = '1';
  } else if (prankState === 'burn50') {
    sparkleActive = false;
    if (prankContent) prankContent.classList.add('hidden');
    burnCanvas.style.display = 'block';
    setBurnProgress(0.5);
  } else if (prankState === 'done') {
    prankLayer.remove();
    document.documentElement.classList.remove('prank-active');
    document.body.classList.remove('prank-active');
    if (window.ScrollTrigger) window.ScrollTrigger.refresh();
  } else {
    setProgress(0);
  }

  // --------------------------------------------------------------------------
  // 7. Apple Hello Effect — Hello Kitty Pink Gradient Stroke Draw Animation
  // Based on https://framer.com/m/AppleHelloEffect-5Xzz.js@oxtIyxKcumiOBhJd8rdv
  // --------------------------------------------------------------------------
  function initAppleHelloAnimation() {
    const path1 = document.querySelector('.prank-hello-path-1');
    const path2 = document.querySelector('.prank-hello-path-2');
    if (!path1 || !path2) return;

    const len1 = path1.getTotalLength ? path1.getTotalLength() : 450;
    const len2 = path2.getTotalLength ? path2.getTotalLength() : 1800;

    path1.style.strokeDasharray = `${len1} ${len1}`;
    path1.style.strokeDashoffset = len1;
    path2.style.strokeDasharray = `${len2} ${len2}`;
    path2.style.strokeDashoffset = len2;

    function playAnimation() {
      if (typeof gsap !== 'undefined') {
        gsap.killTweensOf([path1, path2]);
        path1.style.strokeDashoffset = len1;
        path2.style.strokeDashoffset = len2;
        path1.style.opacity = '1';
        path2.style.opacity = '1';

        const tl = gsap.timeline({ delay: 0.15 });
        tl.to(path1, {
          strokeDashoffset: 0,
          duration: 0.85,
          ease: 'power2.inOut'
        });
        tl.to(path2, {
          strokeDashoffset: 0,
          duration: 2.3,
          ease: 'power2.inOut'
        }, '-=0.15');
      } else {
        setTimeout(() => {
          path1.style.transition = 'stroke-dashoffset 0.85s ease-in-out';
          path1.style.strokeDashoffset = '0';
          setTimeout(() => {
            path2.style.transition = 'stroke-dashoffset 2.3s ease-in-out';
            path2.style.strokeDashoffset = '0';
          }, 700);
        }, 150);
      }
    }

    playAnimation();

    const wrap = document.getElementById('prank-hello-wrap');
    if (wrap) {
      wrap.addEventListener('click', () => {
        playAnimation();
      });
    }

    window.replayHelloAnimation = playAnimation;
  }

  initAppleHelloAnimation();

  window.prankAPI = {
    setProgress: setProgress,
    triggerTransition: startPrankTransition,
    setBurnProgress: setBurnProgress,
    replayHello: () => {
      if (window.replayHelloAnimation) window.replayHelloAnimation();
    }
  };

  window.addEventListener('resize', () => {
    if (burnRenderer && burnMaterial) {
      burnRenderer.setSize(window.innerWidth, window.innerHeight);
      burnMaterial.uniforms.u_resolution.value.set(window.innerWidth, window.innerHeight);
    }
  });
})();
