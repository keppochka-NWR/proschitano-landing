/* Лендинг: появление блоков при скролле и плотный хедер после героя. */
(function () {
  "use strict";
  document.documentElement.classList.add("js");

  var header = document.getElementById("hdr");
  function onScroll() {
    if (!header) return;
    header.classList.toggle("solid", window.scrollY > 80);
  }
  onScroll();
  window.addEventListener("scroll", onScroll, { passive: true });

  var items = [].slice.call(document.querySelectorAll(".rv"));
  function showAll() {
    items.forEach(function (el) { el.classList.add("in"); });
  }

  if (matchMedia("(prefers-reduced-motion: reduce)").matches ||
      !("IntersectionObserver" in window)) {
    showAll();
    return;
  }

  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (e) {
      if (!e.isIntersecting) return;
      var el = e.target;
      var siblings = [].slice.call(el.parentNode.children).filter(function (n) {
        return n.classList.contains("rv");
      });
      el.style.transitionDelay = Math.min(siblings.indexOf(el), 4) * 70 + "ms";
      el.classList.add("in");
      io.unobserve(el);
    });
  }, { rootMargin: "0px 0px -8% 0px", threshold: 0.06 });

  items.forEach(function (el) { io.observe(el); });

  // страховка: в скрытой вкладке IntersectionObserver не срабатывает
  setTimeout(showAll, 2600);
})();
