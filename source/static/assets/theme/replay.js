(function () {
  "use strict";
  var $ = function (id) { return document.getElementById(id); };
  var id = (new URLSearchParams(location.search).get("case") || "").replace(/[^a-z0-9-]/g, "");
  var base = "assets/linux/cases/" + id + "/";
  var data = null, term = null, pos = 0, clock = 0, playing = false, last = 0;

  function stamp(t) { t = Math.floor(t); return Math.floor(t / 60) + ":" + String(t % 60).padStart(2, "0"); }

  function show() {
    $("seek").value = data.duration ? Math.round(1000 * clock / data.duration) : 0;
    $("when").textContent = stamp(clock) + " / " + stamp(data.duration);
    var cur = -1;
    data.steps.forEach(function (s, i) { if (s.t <= clock) cur = i; });
    $("steps").querySelectorAll("button").forEach(function (b, i) { b.classList.toggle("on", i === cur); });
  }

  function jump(t) {
    term.reset();
    pos = 0;
    clock = t;
    var buf = "";
    while (pos < data.chunks.length && data.chunks[pos][0] <= t) buf += data.chunks[pos++][1];
    term.write(buf);
    show();
  }

  function frame(now) {
    if (!playing) return;
    clock += (now - last) / 1000 * +$("speed").value;
    last = now;
    var buf = "";
    while (pos < data.chunks.length && data.chunks[pos][0] <= clock) buf += data.chunks[pos++][1];
    if (buf) term.write(buf);
    if (clock >= data.duration) { clock = data.duration; toggle(false); }
    show();
    if (playing) requestAnimationFrame(frame);
  }

  function toggle(on) {
    playing = on;
    $("play").textContent = on ? "Pause" : "Play";
    if (on) {
      if (clock >= data.duration) jump(0);
      last = performance.now();
      requestAnimationFrame(frame);
    }
  }

  fetch(base + "replay.json").then(function (r) {
    if (!r.ok) throw new Error("missing");
    return r.json();
  }).then(function (d) {
    data = d;
    term = new window.Terminal({ fontSize: 15, disableStdin: true, cursorBlink: false, scrollback: 20000, cols: d.width, rows: d.height, fontFamily: "Consolas, 'DejaVu Sans Mono', Menlo, monospace" });
    term.open($("term"));
    $("steps").innerHTML = "";
    d.steps.forEach(function (s) {
      var b = document.createElement("button");
      b.textContent = stamp(s.t) + "  " + s.title;
      b.addEventListener("click", function () { jump(s.t); });
      $("steps").appendChild(b);
    });
    $("play").addEventListener("click", function () { toggle(!playing); });
    $("seek").addEventListener("input", function (e) { jump(+e.target.value / 1000 * data.duration); });
    show();
    return fetch(base + "manifest.json").then(function (r) { return r.json(); });
  }).then(function (m) {
    $("title").textContent = m.title;
    document.title = m.title + " · Watch the recording";
    $("open").href = "notebook.html?ref=rb-" + Date.now().toString(36) + "&runbook=" + encodeURIComponent(m.id);
  }).catch(function () {
    $("title").textContent = "This recording isn't available.";
  });
})();
