/* --------------------------------------------------------------------------
   Tarushi Birthday Site — Beat 7 Name Reveal
   Progress range 0.75 - 0.875, 4 discrete non-overlapping stages:
   1. Φ (0.750 - 0.788) with strikethrough animation at 0.77 - 0.78
   2. taNushi (0.790 - 0.828) with strikethrough animation at 0.81 - 0.82
   3. Tarushi (0.830 - 0.858) with soft #FF8A3D glow pulse, un-struck
   4. Happy Birthday (0.860 - 0.875+) larger scale, holds through 0.875
   -------------------------------------------------------------------------- */

(function () {
  'use strict';

  const stage1 = document.getElementById('reveal-stage-1');
  const strike1 = document.getElementById('reveal-strike-1');

  const stage2 = document.getElementById('reveal-stage-2');
  const strike2 = document.getElementById('reveal-strike-2');

  const stage3 = document.getElementById('reveal-stage-3');
  const wordTarushi = document.getElementById('reveal-word-tarushi');

  const stage4 = document.getElementById('reveal-stage-4');

  let isAllHidden = false;

  function updateNameReveal(p) {
    if (p < 0.90) {
      if (isAllHidden) return;
      if (stage1) { stage1.style.opacity = '0'; stage1.style.visibility = 'hidden'; }
      if (strike1) { strike1.style.transform = 'scaleX(0)'; }
      if (stage2) { stage2.style.opacity = '0'; stage2.style.visibility = 'hidden'; }
      if (strike2) { strike2.style.transform = 'scaleX(0)'; }
      if (stage3) { stage3.style.opacity = '0'; stage3.style.visibility = 'hidden'; }
      if (stage4) { stage4.style.opacity = '0'; stage4.style.visibility = 'hidden'; }
      isAllHidden = true;
      return;
    }
    isAllHidden = false;

    // ------------------------------------------------------------------------
    // Stage 1: Φ (0.9050 - 0.9330)
    // Fade in 0.9050 - 0.9088
    // Hold 0.9088 - 0.9278
    // Strike draws 0.9202 - 0.9278 (scaleX 0 -> 1)
    // Fade out 0.9278 - 0.9330 (fully 0 by 0.9330)
    // ------------------------------------------------------------------------
    let s1Opacity = 0.0;
    let s1ScaleX = 0.0;

    if (p >= 0.9050 && p <= 0.9330) {
      if (p < 0.9088) {
        s1Opacity = (p - 0.9050) / (0.9088 - 0.9050);
      } else if (p <= 0.9278) {
        s1Opacity = 1.0;
      } else {
        s1Opacity = 1.0 - (p - 0.9278) / (0.9330 - 0.9278);
      }

      if (p < 0.9202) {
        s1ScaleX = 0.0;
      } else if (p <= 0.9278) {
        s1ScaleX = (p - 0.9202) / (0.9278 - 0.9202);
      } else {
        s1ScaleX = 1.0;
      }
    }

    if (stage1) {
      stage1.style.opacity = s1Opacity;
      stage1.style.visibility = s1Opacity > 0.001 ? 'visible' : 'hidden';
    }
    if (strike1) {
      strike1.style.transform = `scaleX(${s1ScaleX})`;
    }

    // ------------------------------------------------------------------------
    // Stage 2: taNushi (0.9354 - 0.9635)
    // Fade in 0.9354 - 0.9392
    // Hold 0.9392 - 0.9582
    // Strike draws 0.9506 - 0.9582 (scaleX 0 -> 1)
    // Fade out 0.9582 - 0.9635 (fully 0 by 0.9635)
    // ------------------------------------------------------------------------
    let s2Opacity = 0.0;
    let s2ScaleX = 0.0;

    if (p >= 0.9354 && p <= 0.9635) {
      if (p < 0.9392) {
        s2Opacity = (p - 0.9354) / (0.9392 - 0.9354);
      } else if (p <= 0.9582) {
        s2Opacity = 1.0;
      } else {
        s2Opacity = 1.0 - (p - 0.9582) / (0.9635 - 0.9582);
      }

      if (p < 0.9506) {
        s2ScaleX = 0.0;
      } else if (p <= 0.9582) {
        s2ScaleX = (p - 0.9506) / (0.9582 - 0.9506);
      } else {
        s2ScaleX = 1.0;
      }
    }

    if (stage2) {
      stage2.style.opacity = s2Opacity;
      stage2.style.visibility = s2Opacity > 0.001 ? 'visible' : 'hidden';
    }
    if (strike2) {
      strike2.style.transform = `scaleX(${s2ScaleX})`;
    }

    // ------------------------------------------------------------------------
    // Stage 3: Tarushi (0.9658 - 0.9860)
    // Fade in 0.9658 - 0.9734
    // Soft glow text-shadow pulse around 0.9734 - 0.9800 (peak around 0.9760)
    // Fade out 0.9800 - 0.9860 (fully 0 by 0.9860)
    // ------------------------------------------------------------------------
    let s3Opacity = 0.0;
    let glowFactor = 0.0;

    if (p >= 0.9658 && p <= 0.9860) {
      if (p < 0.9734) {
        s3Opacity = (p - 0.9658) / (0.9734 - 0.9658);
      } else if (p <= 0.9800) {
        s3Opacity = 1.0;
      } else {
        s3Opacity = 1.0 - (p - 0.9800) / (0.9860 - 0.9800);
      }

      // Glow pulse peak around 0.9760
      if (p >= 0.9700 && p <= 0.9820) {
        const distFromCenter = Math.abs(p - 0.9760) / 0.006;
        glowFactor = Math.max(0, 1.0 - distFromCenter);
      }
    }

    if (stage3) {
      stage3.style.opacity = s3Opacity;
      stage3.style.visibility = s3Opacity > 0.001 ? 'visible' : 'hidden';
    }
    if (wordTarushi) {
      const radius1 = (20 + 16 * glowFactor).toFixed(1);
      const radius2 = (40 + 28 * glowFactor).toFixed(1);
      const alpha1 = (0.6 + 0.38 * glowFactor).toFixed(2);
      const alpha2 = (0.3 + 0.35 * glowFactor).toFixed(2);
      wordTarushi.style.textShadow = `0 0 ${radius1}px rgba(255, 138, 61, ${alpha1}), 0 0 ${radius2}px rgba(255, 138, 61, ${alpha2})`;
    }

    // ------------------------------------------------------------------------
    // Stage 4: Happy Birthday (0.9886 - 1.0000)
    // Prior text/caption fade out by 0.9860
    // Fade in 0.9886 - 1.0000
    // Holds full opacity through end of range at 1.0000
    // ------------------------------------------------------------------------
    let s4Opacity = 0.0;

    if (p >= 0.9886) {
      if (p < 1.0000) {
        s4Opacity = (p - 0.9886) / (1.0000 - 0.9886);
      } else {
        s4Opacity = 1.0;
      }
    }

    if (stage4) {
      stage4.style.opacity = s4Opacity;
      stage4.style.visibility = s4Opacity > 0.001 ? 'visible' : 'hidden';
    }
  }

  window.updateNameReveal = updateNameReveal;

  window.getNameRevealState = function () {
    return {
      stage1: stage1 ? parseFloat(stage1.style.opacity || '0') : 0,
      strike1: strike1 ? strike1.style.transform : '',
      stage2: stage2 ? parseFloat(stage2.style.opacity || '0') : 0,
      strike2: strike2 ? strike2.style.transform : '',
      stage3: stage3 ? parseFloat(stage3.style.opacity || '0') : 0,
      stage4: stage4 ? parseFloat(stage4.style.opacity || '0') : 0
    };
  };
})();
