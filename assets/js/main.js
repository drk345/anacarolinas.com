// ALMAVIVA — minimal nav behavior
(function () {
  // Signal JS is active so progressively-enhanced components (e.g. the
  // Intensivo FAQ accordion) can hide/collapse content only when JS runs.
  document.documentElement.classList.add('js');

  var nav = document.querySelector('.site-nav');
  var toggle = document.getElementById('navToggle');
  var links = document.getElementById('navLinks');

  // Floating nav after a little scroll
  if (nav) {
    var onScroll = function () {
      nav.classList.toggle('is-floating', window.scrollY > 60);
    };
    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll();
  }

  // Hamburger menu
  if (toggle && links) {
    toggle.addEventListener('click', function (e) {
      e.stopPropagation();
      var open = links.classList.toggle('open');
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
    // Close when a link is tapped
    links.addEventListener('click', function (e) {
      if (e.target.closest('a')) {
        links.classList.remove('open');
        toggle.setAttribute('aria-expanded', 'false');
      }
    });
  }

  // FAQ accordion (Intensivo) — progressive enhancement.
  // Answers are readable without JS; when JS runs they collapse into an
  // accordion (one open at a time; clicking the open item closes it).
  // Triggers are made keyboard-accessible here so no inline script is needed.
  var faqItems = Array.prototype.slice.call(document.querySelectorAll('.fitem'));
  if (faqItems.length) {
    var faqOpen = 0;
    var faqRender = function () {
      faqItems.forEach(function (item, i) {
        var on = i === faqOpen;
        var chev = item.querySelector('.fchev');
        var fa = item.querySelector('.fa');
        var fq = item.querySelector('.fq');
        if (chev) chev.classList.toggle('on', on);
        if (fa) fa.classList.toggle('on', on);
        if (fq) fq.setAttribute('aria-expanded', on ? 'true' : 'false');
      });
    };
    faqItems.forEach(function (item, i) {
      var fq = item.querySelector('.fq');
      var fa = item.querySelector('.fa');
      if (!fq) return;
      fq.setAttribute('role', 'button');
      fq.setAttribute('tabindex', '0');
      if (fa) {
        if (!fa.id) fa.id = 'faq-answer-' + i;
        fq.setAttribute('aria-controls', fa.id);
      }
      var toggle = function () {
        faqOpen = (faqOpen === i) ? -1 : i;
        faqRender();
      };
      fq.addEventListener('click', toggle);
      fq.addEventListener('keydown', function (e) {
        if (e.key === 'Enter' || e.key === ' ' || e.key === 'Spacebar') {
          e.preventDefault();
          toggle();
        }
      });
    });
    faqRender();
  }
})();
