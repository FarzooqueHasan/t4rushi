/**
 * Tarushi's ScrapBook — Scroll Reveal Controller
 *
 * Rules:
 * - Reveal on scroll with IntersectionObserver only
 * - Each element starts at opacity: 0 and translateY(24px)
 * - Moves to opacity: 1 and translateY(0) over 600ms ease-out once 20% of it is visible
 * - Staggered 120ms between siblings within a spread
 * - Disabled under prefers-reduced-motion
 * - Zero external libraries (no GSAP, no Lenis)
 */

(function () {
  'use strict';

  function initScrollReveal() {
    // Check prefers-reduced-motion: if enabled, immediately reveal everything
    var prefersReduced = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    if (prefersReduced) {
      document.querySelectorAll('.spread-item').forEach(function (el) {
        el.classList.add('is-revealed');
      });
      return;
    }

    // Process each spread independently to stagger siblings within that spread
    var spreads = document.querySelectorAll('.spread-flight-log, .spread');

    spreads.forEach(function (spread) {
      var items = Array.prototype.slice.call(spread.querySelectorAll('.spread-item'));
      if (items.length === 0) return;

      var observer = new IntersectionObserver(
        function (entries, obs) {
          entries.forEach(function (entry) {
            if (entry.isIntersecting) {
              var target = entry.target;
              var index = items.indexOf(target);
              var delay = index >= 0 ? index * 120 : 0;

              target.style.transitionDelay = delay + 'ms';
              target.classList.add('is-revealed');
              obs.unobserve(target);
            }
          });
        },
        {
          threshold: 0.2 // Trigger once 20% is visible
        }
      );

      items.forEach(function (item) {
        observer.observe(item);
      });
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initScrollReveal);
  } else {
    initScrollReveal();
  }
})();
