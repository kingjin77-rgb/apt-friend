/* 아파트친구 — 공통 스크립트 (모바일 메뉴) */
(function () {
  'use strict';
  var toggle = document.querySelector('[data-af-toggle]');
  if (!toggle) return;
  toggle.addEventListener('click', function () {
    var open = document.body.classList.toggle('af-open');
    toggle.setAttribute('aria-expanded', String(open));
  });
  document.querySelectorAll('.afh__nav a').forEach(function (a) {
    a.addEventListener('click', function () {
      document.body.classList.remove('af-open');
      toggle.setAttribute('aria-expanded', 'false');
    });
  });
})();
