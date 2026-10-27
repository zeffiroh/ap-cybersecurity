/* audience mode (student / instructor) */

(function (global) {
  "use strict";

  var STORAGE_KEY = "apcyber_audience";

  /* Path back to the site root, resolved from this script's own src. */
  var thisScript = document.currentScript;
  var BASE = thisScript
    ? (thisScript.getAttribute("src") || "").replace(/assets\/site-shared\/audience\.js.*$/, "")
    : "";

  function onInstructorPage() {
    return /\/instructor\//.test(location.pathname);
  }

  function read() {
    try {
      return localStorage.getItem(STORAGE_KEY) || "student";
    } catch (e) {
      return "student";
    }
  }

  function write(mode) {
    try {
      localStorage.setItem(STORAGE_KEY, mode === "instructor" ? "instructor" : "student");
    } catch (e) { /* storage unavailable, mode just won't persist */ }
  }

  /* Landing on any /instructor/ page is the signal that this browser belongs
     to a teacher; it latches so their topic pages keep showing teacher cards. */
  function detect() {
    if (onInstructorPage()) {
      write("instructor");
      return "instructor";
    }
    return read();
  }

  /* From an /instructor/ page a reload would re-latch the flag, so leave the page. */
  function leaveInstructorMode() {
    write("student");
    if (onInstructorPage()) {
      location.href = BASE + "index.html";
    } else {
      location.reload();
    }
  }

  function injectToggle() {
    var nav = document.querySelector(".site-nav");
    if (!nav || nav.querySelector(".nav-audience-toggle")) return;
    var btn = document.createElement("button");
    btn.type = "button";
    btn.className = "nav-audience-toggle";
    btn.textContent = "Instructor view";
    btn.title = "This browser is showing teacher-only cards. Click to switch back to the student view.";
    btn.addEventListener("click", leaveInstructorMode);
    nav.appendChild(btn);
  }

  function apply() {
    var mode = detect();
    if (mode !== "instructor") return;

    document.documentElement.setAttribute("data-audience-mode", "instructor");
    injectToggle();

    var revealed = 0;
    var hidden = document.querySelectorAll('[data-audience="instructor"][hidden]');
    Array.prototype.forEach.call(hidden, function (el) {
      el.hidden = false;
      revealed += 1;
    });

    // The topic hero counts only student-visible assets; correct it once the
    // teacher-only cards are on screen.
    if (revealed) {
      var counter = document.querySelector("[data-asset-count] strong");
      var all = document.querySelector("[data-asset-count]");
      if (counter && all && all.getAttribute("data-count-all")) {
        counter.textContent = all.getAttribute("data-count-all");
      }
    }
  }

  global.Audience = {
    get: read,
    set: write,
    isInstructor: function () { return read() === "instructor"; },
    leave: leaveInstructorMode
  };

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", apply);
  } else {
    apply();
  }
})(window);
