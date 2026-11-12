(function (global) {
  "use strict";
  var K = global.AayatTools.kit;
  var W = { AV: { N: 0.85, A: 0.62, L: 0.55, P: 0.2 }, AC: { L: 0.77, H: 0.44 }, UI: { N: 0.85, R: 0.62 }, CIA: { H: 0.56, L: 0.22, N: 0 } };
  var NAMES = { AV: ["Attack vector", { N: "Network", A: "Adjacent", L: "Local", P: "Physical" }], AC: ["Attack complexity", { L: "Low", H: "High" }],
    PR: ["Privileges required", { N: "None", L: "Low", H: "High" }], UI: ["User interaction", { N: "None", R: "Required" }], S: ["Scope", { U: "Unchanged", C: "Changed" }],
    C: ["Confidentiality", { N: "None", L: "Low", H: "High" }], I: ["Integrity", { N: "None", L: "Low", H: "High" }], A: ["Availability", { N: "None", L: "Low", H: "High" }] };
  var ORDER = ["AV", "AC", "PR", "UI", "S", "C", "I", "A"];
  var CSS = ".tc-box .tc-calc{display:grid;grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:6px 10px;margin-top:6px}.tc-box .tc-calc label{font-size:12px}" +
    ".tc-box .tc-score{font:700 22px system-ui;margin:6px 0}.tc-box .tc-vec{font:12px ui-monospace,Consolas,monospace}";

  function roundup(x) { var i = Math.round(x * 100000); return i % 10000 === 0 ? i / 100000 : (Math.floor(i / 10000) + 1) / 10; }
  function parseVector(v) {
    var m = String(v || "").trim().replace(/^CVSS:3\.[01]\//i, ""), out = {};
    m.split("/").forEach(function (p) { var kv = p.split(":"); if (kv.length === 2) out[kv[0].toUpperCase()] = kv[1].toUpperCase(); });
    ORDER.forEach(function (k) { if (!out[k] || !NAMES[k][1][out[k]]) throw new Error("The vector needs " + k + " (" + NAMES[k][0] + ") with one of " + Object.keys(NAMES[k][1]).join("/") + "."); });
    return out;
  }
  function score(v) {
    var m = typeof v === "string" ? parseVector(v) : v, changed = m.S === "C";
    var pr = m.PR === "N" ? 0.85 : m.PR === "L" ? (changed ? 0.68 : 0.62) : (changed ? 0.5 : 0.27);
    var iss = 1 - (1 - W.CIA[m.C]) * (1 - W.CIA[m.I]) * (1 - W.CIA[m.A]);
    var impact = changed ? 7.52 * (iss - 0.029) - 3.25 * Math.pow(iss - 0.02, 15) : 6.42 * iss;
    var expl = 8.22 * W.AV[m.AV] * W.AC[m.AC] * pr * W.UI[m.UI];
    var base = impact <= 0 ? 0 : changed ? roundup(Math.min(1.08 * (impact + expl), 10)) : roundup(Math.min(impact + expl, 10));
    return { base: base, impact: Math.round(impact * 10) / 10, exploitability: Math.round(expl * 10) / 10, severity: rating(base) };
  }
  function rating(s) { return s === 0 ? "None" : s < 4 ? "Low" : s < 7 ? "Medium" : s < 9 ? "High" : "Critical"; }
  function vector(m) { return "CVSS:3.1/" + ORDER.map(function (k) { return k + ":" + m[k]; }).join("/"); }
  function yes(v) { return /^(y|yes|true|1)$/i.test(String(v || "").trim()); }
  function priority(r) {
    var s = r.cvss, kev = yes(r.known_exploited), net = yes(r.internet_facing), epss = parseFloat(r.epss) || 0;
    if (kev && net) return [1, "Patch now: known to be exploited and reachable from the internet"];
    if (kev || (net && s >= 9)) return [2, kev ? "Patch this week: known to be exploited" : "Patch this week: critical and internet-facing"];
    if (s >= 7 || epss >= 0.5 || net) return [3, "Patch this month"];
    return [4, "Next routine cycle"];
  }
  function list(files) {
    var out = [];
    Object.keys(files).sort().forEach(function (n) {
      if (!/\.csv$/i.test(n)) return;
      var rows = K.csv(files[n]);
      if (!rows.length || !("vector" in rows[0])) return;
      rows.forEach(function (r) {
        try { var s = score(r.vector); r.cvss = s.base; r.severity = s.severity; } catch (e) { r.cvss = null; r.severity = "bad vector"; }
        r.file = n;
        var p = r.cvss == null ? [9, "Fix the vector first"] : priority(r);
        r.prio = p[0];
        r.why = p[1];
        out.push(r);
      });
    });
    return out.sort(function (a, b) { return a.prio - b.prio || (b.cvss || 0) - (a.cvss || 0); });
  }

  function mount(el, ctx) {
    K.css("tool-patch-css", CSS);
    var m = { AV: "N", AC: "L", PR: "N", UI: "N", S: "U", C: "H", I: "H", A: "H" }, rows = [];
    var F = K.frame(el, ctx, {
      title: "CVSS and patch priority", cls: "tc-box",
      body: '<div class="tl-row"><label class="tl-grow">Vector <input class="tc-vec" data-r="vec" spellcheck="false"></label><button type="button" class="btn" data-r="read">Read the vector</button></div>' +
        '<div class="tc-calc" data-r="calc"></div><div class="tc-score" data-r="score"></div>',
      actions: '<button type="button" class="btn dark" data-r="rank">Rank the vulnerability list</button>',
      showLabel: "Show the recorded vector",
      show: function (a) { if (a.vec) { F.r("vec").value = a.vec; read(); } },
      after: '<div class="tl-scroll" data-r="list" hidden></div>'
    });
    function calc() {
      F.r("calc").innerHTML = ORDER.map(function (k) {
        return "<label>" + K.esc(NAMES[k][0]) + ' <select data-k="' + k + '">' + Object.keys(NAMES[k][1]).map(function (v) { return '<option value="' + v + '"' + (m[k] === v ? " selected" : "") + ">" + v + " " + K.esc(NAMES[k][1][v]) + "</option>"; }).join("") + "</select></label>";
      }).join("");
    }
    function show() {
      var s = score(m), vec = vector(m);
      F.r("vec").value = vec;
      F.r("score").innerHTML = s.base.toFixed(1) + ' <span class="tl-pill ' + (s.base >= 7 ? "hi" : s.base >= 4 ? "mid" : "ok") + '">' + s.severity + '</span> <small style="font-weight:400;font-size:12px">impact ' + s.impact + ", exploitability " + s.exploitability + "</small>";
      var msg = "";
      if (F.answer && F.answer.vec) msg = F.answer.vec === vec ? "Same vector as the recorded answer." : "Not the recorded vector yet: compare each metric.";
      F.msg(msg);
      F.ready({ vec: vec, n: s.base, blank: ["vec"] }, "CVSS 3.1: " + vec + " scores " + s.base.toFixed(1) + " (" + s.severity + ")");
      F.remember({ vec: vec });
    }
    function read() {
      try { m = parseVector(F.r("vec").value); calc(); show(); } catch (e) { F.msg(e.message, true); }
    }
    F.r("calc").addEventListener("change", function (e) { var k = e.target.getAttribute("data-k"); if (k) { m[k] = e.target.value; show(); } });
    F.r("read").addEventListener("click", read);
    F.r("vec").addEventListener("keydown", function (e) { if (e.key === "Enter") { e.preventDefault(); read(); } });
    F.r("list").addEventListener("click", function (e) { var t = e.target.closest("[data-vec]"); if (t) { F.r("vec").value = t.getAttribute("data-vec"); read(); } });
    F.r("rank").addEventListener("click", function () {
      if (!rows.length) { F.msg("There's no vulnerability list in this case. It's a CSV with a vector column."); return; }
      F.r("list").hidden = false;
      F.r("list").innerHTML = '<table class="tl-table"><tr><th>Priority</th><th>Asset</th><th>ID</th><th>Title</th><th>CVSS</th><th>Exploited</th><th>Internet</th><th>EPSS</th><th>Fix</th></tr>' + rows.map(function (r) {
        return '<tr><td><span class="tl-pill ' + (r.prio === 1 ? "hi" : r.prio === 2 ? "mid" : "") + '">' + r.prio + "</span> <small>" + K.esc(r.why) + "</small></td><td>" + K.esc(r.asset) + "</td><td>" + K.esc(r.id) + "</td><td>" + K.esc(r.title) +
          '</td><td><a href="#" data-vec="' + K.esc(r.vector) + '">' + (r.cvss == null ? "?" : r.cvss.toFixed(1)) + "</a> " + K.esc(r.severity) + "</td><td>" + (yes(r.known_exploited) ? "yes" : "") + "</td><td>" + (yes(r.internet_facing) ? "yes" : "") + "</td><td>" +
          K.esc(r.epss) + "</td><td>" + K.esc(r.fix) + "</td></tr>";
      }).join("") + "</table><small>Priority puts known exploitation and exposure ahead of the CVSS number alone. Click a score to open its vector.</small>";
      var now = rows.filter(function (r) { return r.prio === 1; }).length;
      F.msg(rows.length + " vulnerabilities ranked; " + now + " to patch now.");
    });
    var init = F.saved || F.st;
    if (init.vec) { try { m = parseVector(init.vec); } catch (e) { m = m; } }
    calc();
    if (F.st.a) { F.r("vec").value = ""; F.r("score").textContent = ""; } else show();
    F.note("Loading…");
    F.files().then(function (fs) { rows = list(K.textFiles(fs)); F.note(rows.length ? rows.length + " vulnerabilities in the case" : "calculator"); }).catch(function () { F.note(""); });
  }

  global.AayatTools.register({ id: "patch", title: "CVSS and patch priority", console: true, group: "Security engineer", mount: mount, score: score, parseVector: parseVector, vector: vector, list: list });
})(window);
