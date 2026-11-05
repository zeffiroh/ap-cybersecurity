(function () {
  "use strict";
  var $ = function (id) { return document.getElementById(id); };
  var token = new URLSearchParams(location.search).get("t") || "";
  var term = new window.Terminal({ fontSize: 18, fontFamily: "Consolas, 'DejaVu Sans Mono', Menlo, monospace", cursorBlink: true, scrollback: 20000,
    theme: { background: "#000000" } });
  var fit = new window.FitAddon.FitAddon();
  term.loadAddon(fit);
  term.open($("term"));
  var ws, state = { prompt: false, paused: false, video: false, base: 0, at: 0, plan: [], planPos: 0 };
  var lineEmpty = true, toastTimer = 0;

  function send(o) { if (ws && ws.readyState === 1) ws.send(JSON.stringify(o)); }
  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }
  function stamp(t) { t = Math.max(0, Math.floor(t)); var h = Math.floor(t / 3600), m = Math.floor(t % 3600 / 60), s = t % 60; return (h ? h + ":" + String(m).padStart(2, "0") : m) + ":" + String(s).padStart(2, "0"); }
  function toast(text) {
    var el = $("toast");
    el.textContent = text;
    el.hidden = false;
    clearTimeout(toastTimer);
    toastTimer = setTimeout(function () { el.hidden = true; }, 7000);
  }

  function live() {
    $("rec").textContent = state.paused ? "PAUSED" : "REC";
    $("rec").classList.toggle("off", state.paused);
    $("pause").textContent = state.paused ? "Resume recording" : "Pause recording";
    $("video").textContent = state.video ? "Stop screen recording" : "Record screen";
    $("video").classList.toggle("live", state.video);
  }

  function addTimeline(e) {
    var li = document.createElement("li"), text = e.k === "cmd" ? "$ " + e.cmd : e.k === "ask" ? "Question: " + e.q : e.k === "file" ? "File: " + e.name : e.k === "undo" ? "Undid the last item" : e.text;
    if (!text) return;
    li.className = e.k + (e.k === "cmd" && e.code ? " fail" : "");
    li.innerHTML = "<small>" + stamp(e.t) + "</small>" + esc(text);
    $("timeline").prepend(li);
  }

  function drawTools() {
    window.AayatTools.list().forEach(function (def) {
      var b = document.createElement("button");
      b.textContent = def.title;
      b.addEventListener("click", function () {
        var box = document.createElement("div");
        $("toolbody").replaceChildren(box);
        def.mount(box, {
          state: {},
          files: function () { return fetch("/case-files?t=" + encodeURIComponent(token)).then(function (r) { return r.json(); }); },
          recordLabel: "Add to the lesson",
          record: function (st, text) { send({ k: "tool", tool: def.id, state: st, text: text }); }
        });
        $("toolbox").showModal();
      });
      $("toolbtns").appendChild(b);
    });
  }

  function drawPlan() {
    $("planbox").hidden = !state.plan.length;
    $("plan").innerHTML = state.plan.map(function (p, i) {
      return '<li class="' + (i < state.planPos ? "done" : i === state.planPos ? "next" : "") + '"><button data-plan="' + i + '">' + (i + 1) + ". " + esc(p.title) + "</button>" +
        (i === state.planPos ? (p.code || []).map(function (c, k) { return '<pre data-code="' + i + ":" + k + '" title="Click to type this at the prompt">' + esc(c) + "</pre>"; }).join("") : "") + "</li>";
    }).join("");
  }

  function connect() {
    ws = new WebSocket("ws://" + location.host + "/ws?t=" + encodeURIComponent(token));
    ws.binaryType = "arraybuffer";
    ws.onopen = resize;
    ws.onclose = function () { toast("Lost the studio. Reconnecting… Your recording is safe."); setTimeout(connect, 1500); };
    ws.onmessage = function (m) {
      if (typeof m.data !== "string") { term.write(new Uint8Array(m.data)); return; }
      var d = JSON.parse(m.data);
      if (d.k === "state") {
        term.reset();
        $("title").textContent = d.title;
        document.title = "Studio: " + d.title;
        state.prompt = d.prompt; state.paused = d.paused; state.video = d.video; state.plan = d.plan; state.planPos = d.planPos;
        state.base = d.t; state.at = performance.now();
        $("timeline").innerHTML = "";
        d.events.forEach(addTimeline);
        var mic = $("mic"), keep = mic.value;
        mic.innerHTML = '<option value="">No microphone</option>' + d.mics.map(function (n) { return '<option value="' + esc(n) + '">' + esc(n) + "</option>"; }).join("");
        mic.value = keep;
        live(); drawPlan();
      } else if (d.k === "live") {
        state.paused = d.paused; state.video = d.video; state.prompt = d.prompt;
        if (d.prompt) lineEmpty = true;
        if (d.planPos !== undefined) { state.planPos = d.planPos; drawPlan(); }
        live();
      } else if (d.k === "event") addTimeline(d.event);
      else if (d.k === "toast") toast(d.text);
      else if (d.k === "report") showReport(d.report);
    };
  }

  function resize() {
    try { fit.fit(); } catch (e) { return; }
    send({ k: "size", r: term.rows, c: term.cols });
  }

  function showReport(r) {
    var list = r.review.concat(r.problems || []).map(function (x) { return "<li>" + esc(x) + "</li>"; }).join("");
    $("reportBody").innerHTML = "<p>" + r.steps + " steps and " + r.commands + " commands became " + r.notebookCells + " notebook cells in <code>" + esc(r.folder) + "</code>. " +
      r.recordedOnly + " can only be replayed in the browser, because their tools can't run there.</p>" +
      (list ? "<p><b>Check before you publish. The repo is public.</b></p><ul>" + list + "</ul>" : "") +
      "<p>Then set <code>\"published\": true</code> in <code>seminar.json</code> and run <code>" + esc(r.next) + "</code>.</p>";
    $("report").showModal();
  }

  function openBar() {
    $("cmdbar").hidden = false;
    $("cmd").value = "";
    $("cmd").focus();
  }
  function closeBar() { $("cmdbar").hidden = true; term.focus(); }

  function askParts(text) {
    var k = text.indexOf("::");
    return k < 0 ? { q: text.trim(), a: "" } : { q: text.slice(0, k).trim(), a: text.slice(k + 2).trim() };
  }

  function colon(line) {
    var m = /^(\w+)\s*(.*)$/.exec(line.trim());
    if (!m) return;
    var name = m[1], rest = m[2];
    if (name === "step" || name === "note" || name === "hint") send({ k: name, text: rest });
    else if (name === "ask") send(Object.assign({ k: "ask" }, askParts(rest)));
    else if (name === "undo" || name === "pause" || name === "resume") send({ k: name });
    else if (name === "file") send({ k: "grab", path: rest });
    else if (name === "next") send({ k: "plan", i: state.planPos });
    else toast("Studio commands: step, note, hint, ask, file, next, undo, pause, resume");
  }

  term.onData(function (d) {
    if (d === ":" && state.prompt && lineEmpty) { openBar(); return; }
    lineEmpty = d === "\r" || d === "\x03" || d === "\x15";
    send({ k: "in", d: d });
  });

  $("cmd").addEventListener("keydown", function (e) {
    if (e.key === "Enter") { colon(e.target.value); closeBar(); }
    else if (e.key === "Escape") closeBar();
  });
  document.querySelectorAll("[data-add]").forEach(function (b) {
    var kind = b.getAttribute("data-add"), input = b.previousElementSibling;
    function go() {
      var v = input.value;
      if (!v.trim()) return;
      if (kind === "ask") send(Object.assign({ k: "ask" }, askParts(v)));
      else if (kind === "grab") send({ k: "grab", path: v });
      else send({ k: kind, text: v });
      input.value = "";
      term.focus();
    }
    b.addEventListener("click", go);
    input.addEventListener("keydown", function (e) { if (e.key === "Enter") go(); });
  });
  $("plan").addEventListener("click", function (e) {
    var b = e.target.closest("[data-plan]"), c = e.target.closest("[data-code]");
    if (b) send({ k: "plan", i: +b.getAttribute("data-plan") });
    if (c) {
      var p = c.getAttribute("data-code").split(":");
      send({ k: "in", d: state.plan[+p[0]].code[+p[1]] });
      lineEmpty = false;
      term.focus();
    }
  });
  drawTools();
  $("undo").addEventListener("click", function () { send({ k: "undo" }); });
  $("pause").addEventListener("click", function () { send({ k: state.paused ? "resume" : "pause" }); });
  $("video").addEventListener("click", function () { send(state.video ? { k: "video_stop" } : { k: "video_start", mic: $("mic").value }); });
  $("mark").addEventListener("click", function () { send({ k: "video_mark" }); });
  $("finish").addEventListener("click", function () { send({ k: "finish" }); });
  window.addEventListener("resize", resize);
  setInterval(function () { $("clock").textContent = stamp(state.base + (performance.now() - state.at) / 1000); }, 500);
  connect();
  term.focus();
})();
