// ALMAVIVA — minimal nav behavior
(function () {
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
})();
