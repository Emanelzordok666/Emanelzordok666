(function () {
  "use strict";

  /* ---------- theme ---------- */
  var root = document.documentElement;
  var store = {
    get: function (k) { try { return localStorage.getItem(k); } catch (e) { return null; } },
    set: function (k, v) { try { localStorage.setItem(k, v); } catch (e) {} }
  };
  var saved = store.get("b1theme");
  if (saved === "dark" || saved === "light") root.setAttribute("data-theme", saved);

  var themeBtn = document.getElementById("themeBtn");
  if (themeBtn) {
    themeBtn.addEventListener("click", function () {
      var cur = root.getAttribute("data-theme");
      if (!cur) {
        var prefersDark = window.matchMedia &&
          window.matchMedia("(prefers-color-scheme: dark)").matches;
        cur = prefersDark ? "dark" : "light";
      }
      var next = cur === "dark" ? "light" : "dark";
      root.setAttribute("data-theme", next);
      store.set("b1theme", next);
    });
  }

  /* ---------- search / filter ---------- */
  var search = document.getElementById("search");
  var clearBtn = document.getElementById("searchClear");
  var noResults = document.getElementById("noResults");

  var items = Array.prototype.slice.call(document.querySelectorAll(".s-item"));
  // Pre-compute lowercase search text for each item.
  items.forEach(function (el) {
    el._t = (el.getAttribute("data-text") || el.textContent || "").toLowerCase();
  });

  var COLLAPSE = ".vgroup,.block,.sit,.table-wrap,.pat-box,.both-wrap";
  var collapsers = Array.prototype.slice.call(document.querySelectorAll(COLLAPSE));
  var topics = Array.prototype.slice.call(document.querySelectorAll(".topic"));
  var refBlocks = Array.prototype.slice.call(document.querySelectorAll(".ref-block"));
  var sections = Array.prototype.slice.call(document.querySelectorAll(".sec"));

  function hasVisibleItem(container) {
    var list = container.querySelectorAll(".s-item");
    for (var i = 0; i < list.length; i++) {
      if (!list[i].classList.contains("is-hidden")) return true;
    }
    return false;
  }

  function applyFilter(qRaw) {
    var q = (qRaw || "").trim().toLowerCase();
    var any = false;

    if (!q) {
      items.forEach(function (el) { el.classList.remove("is-hidden"); });
      collapsers.forEach(function (el) { el.classList.remove("is-hidden"); });
      refBlocks.forEach(function (el) { el.classList.remove("is-hidden"); });
      sections.forEach(function (el) { el.classList.remove("is-hidden"); });
      topics.forEach(function (el) { el.classList.remove("is-hidden"); el.open = true; });
      if (noResults) noResults.classList.remove("show");
      if (clearBtn) clearBtn.style.display = "none";
      return;
    }

    if (clearBtn) clearBtn.style.display = "flex";

    items.forEach(function (el) {
      var match = el._t.indexOf(q) !== -1;
      el.classList.toggle("is-hidden", !match);
      if (match) any = true;
    });
    collapsers.forEach(function (el) {
      el.classList.toggle("is-hidden", !hasVisibleItem(el));
    });
    refBlocks.forEach(function (el) {
      el.classList.toggle("is-hidden", !hasVisibleItem(el));
    });
    topics.forEach(function (el) {
      var vis = hasVisibleItem(el);
      el.classList.toggle("is-hidden", !vis);
      el.open = vis;
    });
    sections.forEach(function (el) {
      el.classList.toggle("is-hidden", !hasVisibleItem(el));
    });

    if (noResults) noResults.classList.toggle("show", !any);
  }

  if (search) {
    var t = null;
    search.addEventListener("input", function () {
      var v = search.value;
      if (t) clearTimeout(t);
      t = setTimeout(function () { applyFilter(v); }, 90);
    });
    search.addEventListener("keydown", function (e) {
      if (e.key === "Escape") { search.value = ""; applyFilter(""); search.blur(); }
    });
  }
  if (clearBtn) {
    clearBtn.addEventListener("click", function () {
      if (search) { search.value = ""; search.focus(); }
      applyFilter("");
    });
  }
  // "/" focuses search
  document.addEventListener("keydown", function (e) {
    if (e.key === "/" && document.activeElement !== search &&
        !/^(INPUT|TEXTAREA)$/.test((document.activeElement || {}).tagName || "")) {
      e.preventDefault();
      if (search) search.focus();
    }
  });

  /* ---------- expand / collapse all ---------- */
  var expandBtn = document.getElementById("expandAll");
  var collapseBtn = document.getElementById("collapseAll");
  if (expandBtn) expandBtn.addEventListener("click", function () {
    topics.forEach(function (el) { if (!el.classList.contains("is-hidden")) el.open = true; });
  });
  if (collapseBtn) collapseBtn.addEventListener("click", function () {
    topics.forEach(function (el) { el.open = false; });
  });

  /* ---------- back to top ---------- */
  var toTop = document.getElementById("toTop");
  if (toTop) {
    var onScroll = function () {
      if (window.pageYOffset > 600) toTop.classList.add("show");
      else toTop.classList.remove("show");
    };
    window.addEventListener("scroll", onScroll, { passive: true });
    toTop.addEventListener("click", function () {
      window.scrollTo({ top: 0, behavior: "smooth" });
    });
    onScroll();
  }
})();
