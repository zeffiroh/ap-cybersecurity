(function (global) {
  "use strict";
  var q = new URLSearchParams(location.search);
  if (!q.get("demo") || !q.get("sim")) return;
  var rec = q.get("demo") === "rec";
  var speed = Math.max(0.25, Math.min(40, +q.get("speed") || 1));
  var log = [], t0 = 0, paused = false, skip = false, wake = null, label = "Opening";
  var CSS = "#dm-bar{position:fixed;left:0;right:0;bottom:0;z-index:99999;background:rgba(16,16,24,.94);color:#fff;font:18px/1.45 system-ui,sans-serif;padding:12px 18px;display:flex;gap:14px;align-items:center}" +
    "#dm-cap{flex:1;min-height:52px}#dm-cap small{display:block;font-size:12px;letter-spacing:.08em;text-transform:uppercase;opacity:.7;margin-bottom:2px}" +
    "#dm-bar button,#dm-bar select{font:13px system-ui;padding:5px 10px;border:1px solid #fff;background:transparent;color:#fff;cursor:pointer}" +
    ".dm-rec #dm-ctl,.dm-rec #dm-cap span{display:none}#dm-bar.dm-rec{left:auto;right:22px;bottom:64px;padding:7px 14px;border-radius:6px;background:rgba(16,16,24,.82)}" +
    ".dm-rec #dm-cap{min-height:0}.dm-rec #dm-cap small{margin:0;font-size:13px;opacity:.95}.dm-on{outline:4px solid #e0a100!important;outline-offset:2px;transition:outline-color .3s}";

  function D() { return global.AayatDesk; }
  function now() { return (Date.now() - t0) / 1000; }
  function sleep(ms) {
    return new Promise(function (ok) {
      var left = ms, last = Date.now();
      (function tick() {
        if (skip) { ok(); return; }
        if (!paused) left -= (Date.now() - last) * speed;
        last = Date.now();
        if (left <= 0) { wake = null; ok(); return; }
        wake = tick;
        setTimeout(tick, 60);
      })();
    });
  }
  function bar() {
    var s = document.createElement("style");
    s.textContent = CSS;
    document.head.appendChild(s);
    var b = document.createElement("div");
    b.id = "dm-bar";
    if (rec) b.className = "dm-rec";
    b.innerHTML = '<div id="dm-cap"><small>Demo</small><span>Loading the simulation…</span></div><div id="dm-ctl"><button type="button" id="dm-pause">Pause</button> <button type="button" id="dm-next">Skip this line</button> ' +
      '<select id="dm-speed" aria-label="Speed"><option value="0.5">0.5×</option><option value="1">1×</option><option value="1.5">1.5×</option><option value="2">2×</option></select></div>';
    document.body.appendChild(b);
    document.getElementById("dm-speed").value = String(speed);
    document.getElementById("dm-speed").addEventListener("change", function () { speed = +this.value; });
    document.getElementById("dm-pause").addEventListener("click", function () { paused = !paused; this.textContent = paused ? "Play" : "Pause"; if (!paused && wake) wake(); });
    document.getElementById("dm-next").addEventListener("click", function () { skip = true; if (wake) wake(); });
  }
  function sentences(text) {
    var out = [], cur = "";
    String(text || "").replace(/\s+/g, " ").trim().split(/(?<=[.!?:])\s+/).forEach(function (s) {
      if ((cur + " " + s).trim().split(" ").length > 26 && cur) { out.push(cur.trim()); cur = s; } else cur = (cur + " " + s).trim();
    });
    if (cur) out.push(cur);
    return out;
  }
  function say(text) {
    var go = Promise.resolve();
    sentences(text).forEach(function (p) {
      go = go.then(function () {
        skip = false;
        var cap = document.getElementById("dm-cap");
        cap.innerHTML = "<small></small><span></span>";
        cap.querySelector("small").textContent = label;
        cap.querySelector("span").textContent = p;
        var start = now();
        return sleep(Math.max(2600, p.split(" ").length / 2.5 * 1000)).then(function () { log.push({ start: start, end: now(), text: p, label: label }); });
      });
    });
    return go.then(function () { skip = false; });
  }

  function title(w) { var b = w.querySelector(":scope > header b, :scope > .ws-title b, .ws-title b"); return b ? b.textContent : ""; }
  function scope(where) {
    if (!where) return document;
    var all = Array.prototype.slice.call(document.querySelectorAll(".wm-win, .ws-win")).filter(function (w) { return !w.hidden && title(w).toLowerCase().indexOf(String(where).toLowerCase()) >= 0; });
    var inner = all.filter(function (w) { return w.classList.contains("wm-win"); });
    return (inner.length ? inner : all).pop() || null;
  }
  function find(m) {
    var root = scope(m["in"]);
    if (!root) return null;
    var list = Array.prototype.slice.call(root.querySelectorAll(m.sel || "*"));
    if (m.text) list = list.filter(function (el) { return ((el.closest("tr") || el).textContent || "").toLowerCase().indexOf(String(m.text).toLowerCase()) >= 0; });
    list = list.filter(function (el) { return el.offsetParent !== null || el.getClientRects().length; });
    return list[m.nth || 0] || null;
  }
  function waitEl(m, ms) {
    return new Promise(function (ok, bad) {
      var end = Date.now() + (ms || 20000);
      (function poll() {
        var el = find(m);
        if (el) { ok(el); return; }
        if (Date.now() > end) { bad(new Error("Couldn't find " + (m.sel || "") + (m.text ? " with \"" + m.text + "\"" : "") + (m["in"] ? " in the " + m["in"] + " window" : ""))); return; }
        setTimeout(poll, 200);
      })();
    });
  }
  function until(test, ms, what) {
    return new Promise(function (ok, bad) {
      var end = Date.now() + ms;
      (function poll() { if (test()) ok(); else if (Date.now() > end) bad(new Error(what)); else setTimeout(poll, 250); })();
    });
  }
  function mark(el) {
    document.querySelectorAll(".dm-on").forEach(function (x) { x.classList.remove("dm-on"); });
    if (!el) return;
    el.classList.add("dm-on");
    if (el.scrollIntoView) el.scrollIntoView({ block: "nearest" });
  }
  function typeInto(el, text) {
    el.focus();
    el.value = "";
    var chars = String(text), i = 0, step = Math.max(1, Math.ceil(chars.length / 40));
    return new Promise(function (ok) {
      (function next() {
        if (i >= chars.length) { el.dispatchEvent(new Event("input", { bubbles: true })); ok(); return; }
        el.value += chars.slice(i, i + step);
        i += step;
        el.dispatchEvent(new Event("input", { bubbles: true }));
        setTimeout(next, Math.max(5, 35 / speed));
      })();
    });
  }
  function submit(el) {
    var f = el.form || el.closest("form");
    if (f) { if (f.requestSubmit) f.requestSubmit(); else f.dispatchEvent(new Event("submit", { cancelable: true, bubbles: true })); return; }
    el.dispatchEvent(new KeyboardEvent("keydown", { key: "Enter", bubbles: true }));
  }

  function move(m) {
    if (m.say) return say(m.say);
    if (m.wait) return sleep(m.wait);
    if (m.expect) return until(function () { var r = global.AayatSim && global.AayatSim.state(); return r && r.done[m.expect]; }, m.timeout || 15000, "Objective " + m.expect + " didn't complete").then(function () { return sleep(900); });
    if (m.open) { D().run(m.open, m.args || undefined); return sleep(m.pause || 1600); }
    if (m.file) { D().open(m.file); return sleep(m.pause || 2600); }
    if (m.close) { var w = scope(m.close); if (w) { var x = w.querySelector('[data-w="x"], [data-w="close"]'); if (x) x.click(); } return sleep(500); }
    if (m.answer) {
      var spec = { sel: '[data-ask="' + m.answer + '"] input', "in": "Mission" };
      return waitEl(spec, 30000).then(function (el) { mark(el.closest("form")); return typeInto(el, m.value); }).then(function () { return sleep(500); }).then(function () {
        submit(find(spec));
        return until(function () { var r = global.AayatSim && global.AayatSim.state(); return r && r.done[m.answer]; }, 8000, "The answer \"" + m.value + "\" didn't complete objective " + m.answer);
      }).then(function () { return sleep(1200); });
    }
    if (m.type) {
      var t = { sel: "form input", "in": m["in"] || "Terminal" };
      return waitEl(t, 30000).then(function (el) { mark(el.closest("form")); return typeInto(el, m.type).then(function () { return sleep(400); }).then(function () { submit(el); return sleep(300); }).then(function () {
        return until(function () { return !el.disabled; }, m.timeout || 300000, "The command " + m.type + " didn't finish");
      }); }).then(function () { return sleep(m.pause || 2400); });
    }
    if (m.click || m.dbl || m.fill != null || m.pick || m.tick != null) {
      var sel = m.click || m.dbl || m.pick || m.sel;
      return waitEl({ sel: sel, "in": m["in"], text: m.text, nth: m.nth }, m.timeout || 20000).then(function (el) {
        mark(el);
        return sleep(700).then(function () {
          if (m.click && m.then) {
            var end = Date.now() + (m.timeout || 60000);
            return new Promise(function (ok, bad) {
              (function again() {
                if (find({ sel: m.then, "in": m["in"] })) { ok(); return; }
                if (Date.now() > end) { bad(new Error("Clicking " + m.click + " never showed " + m.then)); return; }
                (find({ sel: m.click, "in": m["in"], text: m.text, nth: m.nth }) || el).click();
                setTimeout(again, 1500);
              })();
            });
          }
          if (m.click) { el.click(); return; }
          if (m.dbl) { el.dispatchEvent(new MouseEvent("dblclick", { bubbles: true })); return; }
          if (m.pick) { el.value = m.value; el.dispatchEvent(new Event("change", { bubbles: true })); return; }
          if (m.tick != null) { if (el.checked !== !!m.tick) { el.checked = !!m.tick; el.dispatchEvent(new Event("change", { bubbles: true })); } return; }
          return typeInto(el, m.fill).then(function () { if (m.enter) submit(el); });
        });
      }).then(function () { return sleep(m.pause || 1300); });
    }
    return Promise.reject(new Error("Unknown demo move: " + JSON.stringify(m)));
  }
  function moves(list) {
    var go = Promise.resolve();
    (list || []).forEach(function (m) { go = go.then(function () { return move(m); }); });
    return go;
  }

  function play(meta) {
    var S = meta.script || (meta.sim && meta.sim.script) || {}, steps = S.steps || [];
    t0 = Date.now();
    global.__demo.t0 = t0;
    label = "Opening";
    log.push({ start: 0, end: 0, text: "", chapter: "Opening" });
    var go = say(S.intro || meta.summary || meta.title);
    steps.forEach(function (st, i) {
      go = go.then(function () {
        st = typeof st === "string" ? { say: st } : st;
        label = st.title || "Part " + (i + 1);
        log.push({ start: now(), end: now(), text: "", chapter: label });
        return say(st.say || st.before || "").then(function () { return moves(st["do"]); }).then(function () { return say(st.after || ""); });
      });
    });
    return go.then(function () {
      label = "Debrief";
      log.push({ start: now(), end: now(), text: "", chapter: "Debrief" });
      return waitEl({ sel: "[data-finish]", "in": "Mission" }, 10000);
    }).then(function (b) {
      mark(b);
      return sleep(800).then(function () { b.click(); return sleep(600); });
    }).then(function () {
      var yes = document.querySelector(".sm-over [data-yes]");
      if (yes) yes.click();
      return sleep(1500);
    }).then(function () { return say(S.outro || ""); }).then(function () {
      mark(null);
      var st = global.AayatSim ? global.AayatSim.state() : null;
      document.getElementById("dm-cap").innerHTML = "<small>Demo</small><span>The end.</span>";
      global.__demo = { done: true, log: log, length: now(), t0: t0, score: st ? st.score : null, done_ids: st ? Object.keys(st.done) : [], open: st ? st.open : [] };
    });
  }

  function start() {
    bar();
    global.__demo = { done: false, log: log };
    (function wait() {
      if (!D()) { setTimeout(wait, 200); return; }
      var cid = q.get("case");
      until(function () { var sign = document.querySelector(".ws-signbtn"); if (sign && sign.offsetParent !== null) sign.click(); return D().caseId() === cid && D().caseMeta() && global.AayatSim && global.AayatSim.state(); }, 60000, "The simulation didn't start").then(function () {
        return sleep(1500);
      }).then(function () { return play(D().caseMeta()); }).catch(function (e) {
        document.getElementById("dm-cap").innerHTML = "<small>Demo</small><span></span>";
        document.querySelector("#dm-cap span").textContent = "The demo stopped: " + e.message;
        global.__demo = { done: true, log: log, error: e.message, t0: t0, length: now() };
      });
    })();
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", start); else start();
})(window);
