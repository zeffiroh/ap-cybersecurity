// Shared helpers for the hands-on labs: mission checklist, escaping, hex, Pyodide loading.
(function () {
  function store(key, val) {
    try {
      if (val === undefined) return JSON.parse(localStorage.getItem(key) || "null");
      localStorage.setItem(key, JSON.stringify(val));
    } catch (e) { return null; }
  }

  function Missions(labId, listEl, lineEl, onAll) {
    var key = "aayat_lab_" + labId;
    var done = store(key) || {};
    var items = Array.prototype.slice.call(listEl.querySelectorAll("li[data-m]"));
    function render() {
      var n = 0;
      items.forEach(function (li) {
        var on = !!done[li.getAttribute("data-m")];
        li.classList.toggle("done", on);
        if (on) n++;
      });
      if (lineEl) lineEl.textContent = "MISSIONS " + n + " / " + items.length + (n === items.length ? "  ·  COMPLETE" : "");
      if (n === items.length && onAll) onAll();
    }
    this.complete = function (id) {
      if (done[id]) return false;
      done[id] = new Date().toISOString();
      store(key, done);
      render();
      return true;
    };
    this.isDone = function (id) { return !!done[id]; };
    this.reset = function () { done = {}; store(key, done); render(); };
    render();
  }

  function esc(s) {
    return String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");
  }

  function hex(buf) {
    return Array.prototype.map.call(new Uint8Array(buf), function (b) { return ("0" + b.toString(16)).slice(-2); }).join("");
  }

  function bytes(str) { return new TextEncoder().encode(str); }

  var pyodidePromise = null;
  function pyodide(assetsUrl, packages, onStatus) {
    if (!pyodidePromise) {
      pyodidePromise = new Promise(function (resolve, reject) {
        var base = assetsUrl + "vendor/pyodide-0.26.1/";
        onStatus && onStatus("Loading Python (first visit downloads about 14 MB)...");
        var s = document.createElement("script");
        s.src = base + "pyodide.js";
        s.onload = function () {
          window.loadPyodide({ indexURL: base }).then(function (py) {
            onStatus && onStatus("Loading packages...");
            return py.loadPackage(packages || []).then(function () { resolve(py); });
          }).catch(reject);
        };
        s.onerror = function () { reject(new Error("could not load " + s.src)); };
        document.head.appendChild(s);
      });
    }
    return pyodidePromise;
  }

  window.Lab = { Missions: Missions, esc: esc, hex: hex, bytes: bytes, pyodide: pyodide, store: store };
})();
