(function (global) {
  "use strict";
  var K = global.AayatTools.kit;
  var STRIDE = { S: ["Spoofing", "Pretending to be someone or something else", "authentication"], T: ["Tampering", "Changing data or code", "integrity checks, signing"],
    R: ["Repudiation", "Denying having done something", "logging and audit trails"], I: ["Information disclosure", "Seeing data you shouldn't", "encryption, access control"],
    D: ["Denial of service", "Stopping it from working", "rate limits, redundancy"], E: ["Elevation of privilege", "Gaining rights you shouldn't have", "least privilege, input checks"] };
  var APPLIES = { external: "SR", process: "STRIDE", store: "TRID", flow: "TID" };
  var STARTER = "external Customer\nprocess Shop web app\nstore Orders database\nflow Customer -> Shop web app : login and orders over HTTPS\nflow Shop web app -> Orders database : SQL queries\nboundary Internet | Shop web app\n";
  var TREE = "OR Steal customer orders\n  AND Get into the database directly\n    Find the database open to the internet  cost=2\n    Guess the database password  cost=5\n  SQL injection through the search box  cost=3\n  AND Phish an admin\n    Send a convincing email  cost=1\n    Admin enters password on a fake page  cost=4\n";
  var CSS = ".ttm-box textarea{min-height:120px}.ttm-box .ttm-el{border:1px solid #ccc;background:#fff;margin-top:6px;padding:6px 8px}.ttm-box .ttm-el h5{margin:0 0 4px}" +
    ".ttm-box .ttm-el label{display:flex;gap:6px;align-items:flex-start;font-size:12.5px;margin:3px 0}.ttm-box .ttm-el input[type=text]{flex:1;font-size:12px;padding:2px 4px}.ttm-box pre{white-space:pre-wrap;font:12px/1.5 ui-monospace,Consolas,monospace;background:#fff;border:1px solid #bbb;padding:6px}";

  function model(text) {
    var els = [], bad = [];
    String(text || "").replace(/\r/g, "").split("\n").forEach(function (l, i) {
      l = l.trim();
      var m;
      if (!l) return;
      if ((m = /^(external|process|store)\s+(.+)$/i.exec(l))) els.push({ kind: m[1].toLowerCase(), name: m[2].trim() });
      else if ((m = /^flow\s+(.+?)\s*->\s*(.+?)(?:\s*:\s*(.+))?$/i.exec(l))) els.push({ kind: "flow", name: m[1] + " → " + m[2] + (m[3] ? " (" + m[3] + ")" : ""), from: m[1], to: m[2] });
      else if ((m = /^boundary\s+(.+?)\s*\|\s*(.+)$/i.exec(l))) els.push({ kind: "boundary", name: m[1] + " | " + m[2] });
      else bad.push("Line " + (i + 1) + " should start with external, process, store, flow or boundary.");
    });
    return { els: els, bad: bad };
  }
  function tree(text) {
    var root = null, stack = [], bad = [];
    String(text || "").replace(/\r/g, "").split("\n").forEach(function (raw, i) {
      if (!raw.trim()) return;
      var ind = raw.match(/^ */)[0].length, l = raw.trim(), m = /^(AND|OR)\s+(.+)$/.exec(l), c = /\bcost\s*=\s*(\d+(?:\.\d+)?)/.exec(l);
      var n = { gate: m ? m[1] : "", name: (m ? m[2] : l).replace(/\s*cost\s*=\s*[\d.]+/, "").trim(), cost: c ? +c[1] : null, kids: [], ind: ind };
      while (stack.length && stack[stack.length - 1].ind >= ind) stack.pop();
      if (!stack.length) { if (root) bad.push("Line " + (i + 1) + ": there can be only one goal at the top."); else root = n; }
      else stack[stack.length - 1].kids.push(n);
      if (!n.gate && n.cost == null && !(stack.length === 0)) bad.push("Line " + (i + 1) + ": a step needs a cost=N, or start it with AND or OR.");
      stack.push(n);
    });
    function solve(n) {
      if (!n.kids.length) return { cost: n.cost == null ? Infinity : n.cost, path: [n.name] };
      var ks = n.kids.map(solve);
      if (n.gate === "AND") return { cost: ks.reduce(function (s, k) { return s + k.cost; }, 0), path: [].concat.apply([], ks.map(function (k) { return k.path; })) };
      var best = ks.reduce(function (a, b) { return b.cost < a.cost ? b : a; });
      return { cost: best.cost, path: best.path };
    }
    return { root: root, bad: bad, best: root ? solve(root) : null };
  }

  function mount(el, ctx) {
    K.css("tool-threatmodel-css", CSS);
    var notes = {};
    var F = K.frame(el, ctx, {
      title: "Threat model", cls: "ttm-box",
      body: '<div class="tl-tabs"><button type="button" data-t="stride" class="on">STRIDE</button><button type="button" data-t="tree">Attack tree</button></div>' +
        '<div data-r="stride"><label style="display:block;font-size:12px;margin-top:6px">The system, one element per line<textarea class="tl-area" data-r="sys" spellcheck="false"></textarea></label>' +
        '<button type="button" class="btn" data-r="gen">List the threats</button><div data-r="els"></div></div>' +
        '<div data-r="tree" hidden><label style="display:block;font-size:12px;margin-top:6px">Goal at the top, AND or OR for groups, cost=N for each step<textarea class="tl-area" data-r="tr" spellcheck="false"></textarea></label>' +
        '<button type="button" class="btn" data-r="solve">Find the cheapest attack</button><pre data-r="tout" hidden></pre></div>',
      actions: '<button type="button" class="btn dark" data-r="done">Check the model</button><button type="button" class="btn" data-r="md">Download Markdown</button>',
      showLabel: "Show the recorded model",
      show: function (a) { if (a.sys != null) F.r("sys").value = a.sys; if (a.tr != null) F.r("tr").value = a.tr; if (a.notes) notes = a.notes; gen(); }
    });
    var init = F.saved || F.st;
    F.r("sys").value = init.sys != null && init.sys !== "" ? init.sys : STARTER;
    F.r("tr").value = init.tr != null && init.tr !== "" ? init.tr : TREE;
    if (init.notes) notes = init.notes;
    function keep() { F.remember({ sys: F.r("sys").value, tr: F.r("tr").value, notes: notes }); }
    function gen() {
      var m = model(F.r("sys").value);
      if (m.bad.length) { F.msg(m.bad.join(" "), true); return m; }
      F.r("els").innerHTML = m.els.filter(function (e) { return e.kind !== "boundary"; }).map(function (e, i) {
        return '<div class="ttm-el"><h5>' + K.esc(e.name) + " <small>(" + e.kind + ")</small></h5>" + APPLIES[e.kind].split("").map(function (c) {
          var k = e.name + "|" + c;
          return '<label><span style="width:170px"><b>' + c + "</b> " + K.esc(STRIDE[c][0]) + "<br><small>" + K.esc(STRIDE[c][1]) + '</small></span><input type="text" data-n="' + K.esc(k) + '" value="' + K.esc(notes[k] || "") +
            '" placeholder="How could it happen here, and what stops it? (' + K.esc(STRIDE[c][2]) + ')"></label>';
        }).join("") + "</div>";
      }).join("") + (m.els.some(function (e) { return e.kind === "boundary"; }) ? "" : "<p>Add a boundary line: the most serious threats cross a trust boundary.</p>");
      F.msg(m.els.length + " elements.");
      return m;
    }
    F.r("els").addEventListener("input", function (e) { var k = e.target.getAttribute("data-n"); if (k) { notes[k] = e.target.value; keep(); } });
    F.r("gen").addEventListener("click", function () { gen(); keep(); });
    F.r("sys").addEventListener("input", keep);
    F.r("tr").addEventListener("input", keep);
    F.r("solve").addEventListener("click", function () {
      var t = tree(F.r("tr").value);
      F.r("tout").hidden = false;
      if (!t.root) { F.r("tout").textContent = "Write a goal first."; return; }
      F.r("tout").textContent = (t.bad.length ? t.bad.join("\n") + "\n\n" : "") + "Goal: " + t.root.name + "\nCheapest attack costs " + t.best.cost + ":\n- " + t.best.path.join("\n- ") +
        "\n\nDefend this path first: raising the cost of any step on it makes the attacker pick a dearer one.";
    });
    el.addEventListener("click", function (e) {
      var t = e.target.closest("[data-t]");
      if (!t || !el.contains(t)) return;
      el.querySelectorAll(".tl-tabs button").forEach(function (b) { b.classList.toggle("on", b === t); });
      F.r("stride").hidden = t.getAttribute("data-t") !== "stride";
      F.r("tree").hidden = t.getAttribute("data-t") !== "tree";
    });
    function done() {
      var m = model(F.r("sys").value), slots = 0, filled = 0;
      m.els.forEach(function (e) { if (e.kind === "boundary") return; APPLIES[e.kind].split("").forEach(function (c) { slots++; if ((notes[e.name + "|" + c] || "").trim().length > 8) filled++; }); });
      return { slots: slots, filled: filled, m: m };
    }
    F.r("done").addEventListener("click", function () {
      var d = done(), t = tree(F.r("tr").value);
      F.msg(d.filled + " of " + d.slots + " STRIDE threats answered." + (t.best ? " Cheapest attack in the tree costs " + t.best.cost + "." : ""));
      F.ready({ sys: F.r("sys").value, tr: F.r("tr").value, notes: notes, n: d.filled, blank: [] }, "Threat model: " + d.m.els.length + " elements, " + d.filled + " of " + d.slots + " threats answered");
    });
    F.r("md").addEventListener("click", function () {
      var d = done(), t = tree(F.r("tr").value), out = ["# Threat model", "", "## System", "", "```", F.r("sys").value.trim(), "```", "", "## STRIDE", ""];
      d.m.els.forEach(function (e) {
        if (e.kind === "boundary") return;
        out.push("### " + e.name + " (" + e.kind + ")", "");
        APPLIES[e.kind].split("").forEach(function (c) { out.push("- **" + STRIDE[c][0] + "**: " + (notes[e.name + "|" + c] || "_not yet answered_")); });
        out.push("");
      });
      if (t.best) out.push("## Attack tree", "", "```", F.r("tr").value.trim(), "```", "", "Cheapest path (" + t.best.cost + "): " + t.best.path.join(", then "), "");
      K.download("threat-model.md", out.join("\n"), "text/markdown");
    });
    gen();
    F.note("");
  }

  global.AayatTools.register({ id: "threatmodel", title: "Threat model", console: true, group: "Governance and risk", mount: mount, model: model, tree: tree });
})(window);
