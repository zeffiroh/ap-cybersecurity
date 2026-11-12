(function (global) {
  "use strict";
  var K = global.AayatTools.kit;
  var CSS = ".tb-box .tb-scene{border:1px solid #bbb;background:#fff;padding:10px 12px;margin-top:8px}.tb-box .tb-clock{float:right;font:600 13px ui-monospace,Consolas,monospace;color:#1f4e8c}" +
    ".tb-box .tb-inject{border-left:4px solid #b7791f;background:#fff8e6;padding:6px 8px;margin:8px 0;font-size:13px}.tb-box .tb-ch{display:block;width:100%;text-align:left;margin:6px 0;border:1px solid #888;background:#fff;padding:8px;cursor:pointer;font:inherit;color:#111}" +
    ".tb-box .tb-ch:hover{border-color:#111;background:#f6f6f6}.tb-box .tb-path li{margin:4px 0}.tb-box .tb-path .good{color:#256b3d}.tb-box .tb-path .bad{color:#a11}.tb-box .tb-role{font-size:12px;color:#555}";

  function scenarios(files) {
    var out = {};
    Object.keys(files).forEach(function (n) {
      if (!/tabletop.*\.json$/i.test(K.base(n))) return;
      var d = K.json(files[n]);
      if (d && d.nodes && d.start && d.nodes[d.start]) out[n] = d;
    });
    return out;
  }
  function check(s) {
    var bad = [];
    Object.keys(s.nodes).forEach(function (k) {
      (s.nodes[k].choices || []).forEach(function (c, i) { if (c.next && !s.nodes[c.next]) bad.push(k + " choice " + (i + 1) + " goes to a missing step \"" + c.next + "\""); });
    });
    return bad;
  }
  function addTime(start, plus) {
    var m = /^\+?(\d+):(\d\d)$/.exec(String(plus || "0:00"));
    return m ? start + (+m[1] * 60 + +m[2]) * 60000 : start;
  }
  function clock(ms) { var m = Math.round(ms / 60000); return "T+" + Math.floor(m / 60) + ":" + ("0" + (m % 60)).slice(-2); }

  function mount(el, ctx) {
    K.css("tool-tabletop-css", CSS);
    var S = {}, cur = "", sc = null, node = "", path = [], t = 0, score = 0;
    var F = K.frame(el, ctx, {
      title: "Tabletop exercise", cls: "tb-box",
      body: '<div class="tl-row"><label class="tl-grow">Scenario <select data-r="file"></select></label><label>Your role <select data-r="role"></select></label>' +
        '<button type="button" class="btn" data-r="restart">Start again</button></div>',
      actions: "",
      showLabel: "Show the recorded decisions",
      show: function (a) { if (Array.isArray(a.path)) F.msg("Recorded path: " + a.path.map(function (p) { return p.label; }).join(" → ")); },
      after: '<div class="tb-scene" data-r="scene"></div><div data-r="log"></div>'
    });
    function start() {
      sc = S[cur];
      node = sc.start;
      path = [];
      t = 0;
      score = 0;
      F.r("role").innerHTML = (sc.roles || ["Incident lead"]).map(function (r) { return "<option>" + K.esc(r) + "</option>"; }).join("");
      draw();
    }
    function draw() {
      var n = sc.nodes[node], end = !(n.choices || []).length;
      F.r("scene").innerHTML = '<span class="tb-clock">' + clock(t) + "</span><h4 style=\"margin:0 0 6px\"></h4><p data-r=\"txt\"></p>" +
        (n.inject ? '<div class="tb-inject"><b>New information:</b> <span data-r="inj"></span></div>' : "") +
        (end ? '<p><b>End of the exercise.</b> Score ' + score + " of " + (sc.max || "?") + ".</p>" + (n.debrief ? '<div class="tb-inject" style="border-color:#256b3d;background:#eef8f1"><b>What good looks like:</b> <span data-r="deb"></span></div>' : "") :
          '<p class="tb-role">What do you do?</p>' + n.choices.map(function (c, i) { return '<button type="button" class="tb-ch" data-c="' + i + '"></button>'; }).join(""));
      F.r("scene").querySelector("h4").textContent = n.title || sc.title;
      F.r("txt").textContent = n.text || "";
      if (n.inject) F.r("inj").textContent = n.inject;
      if (end && n.debrief) F.r("deb").textContent = n.debrief;
      if (!end) n.choices.forEach(function (c, i) { F.r("scene").querySelector('[data-c="' + i + '"]').textContent = c.text; });
      F.r("log").innerHTML = path.length ? '<ol class="tb-path">' + path.map(function (p) {
        return '<li class="' + (p.score > 0 ? "good" : p.score < 0 ? "bad" : "") + '">' + K.esc(clock(p.t)) + " " + K.esc(p.label) + (p.note ? "<br><small>" + K.esc(p.note) + "</small>" : "") + "</li>";
      }).join("") + "</ol>" : "";
      if (end) finish();
    }
    function finish() {
      var msg = "Finished in " + clock(t).slice(2) + " of exercise time with " + score + " points.";
      if (F.answer && Array.isArray(F.answer.path)) {
        var same = path.filter(function (p, i) { return F.answer.path[i] && F.answer.path[i].node === p.node && F.answer.path[i].c === p.c; }).length;
        msg += " " + same + " of your " + path.length + " decisions match the recorded run.";
      }
      F.msg(msg);
      F.ready({ file: cur, path: path, n: score, role: F.r("role").value, blank: ["path"] }, "Tabletop: " + sc.title + ", " + path.length + " decisions, " + score + " points");
      F.remember({ file: cur, path: path });
    }
    F.r("scene").addEventListener("click", function (e) {
      var b = e.target.closest("[data-c]");
      if (!b) return;
      var n = sc.nodes[node], c = n.choices[+b.getAttribute("data-c")];
      t = addTime(t, c.time || n.time || "0:15");
      score += +c.score || 0;
      path.push({ node: node, c: +b.getAttribute("data-c"), label: c.text, note: c.note || "", score: +c.score || 0, t: t });
      node = c.next && sc.nodes[c.next] ? c.next : node;
      if (!c.next) node = "__end";
      if (node === "__end") { sc.nodes.__end = { title: "End", text: "The exercise stops here.", debrief: sc.debrief || "" }; }
      draw();
    });
    F.r("file").addEventListener("change", function () { cur = this.value; start(); });
    F.r("restart").addEventListener("click", start);

    F.note("Loading…");
    F.files().then(function (fs) {
      S = scenarios(K.textFiles(fs));
      var names = Object.keys(S).sort();
      F.note(names.length + " scenario" + (names.length === 1 ? "" : "s"));
      if (!names.length) { F.r("scene").textContent = "There are no tabletop scenarios in this case. They are .json files with \"tabletop\" in the name."; return; }
      var problems = [].concat.apply([], names.map(function (n) { return check(S[n]).map(function (p) { return K.base(n) + ": " + p; }); }));
      if (problems.length) F.msg(problems.join("; "), true);
      F.r("file").innerHTML = names.map(function (n) { return '<option value="' + K.esc(n) + '">' + K.esc(S[n].title || n) + "</option>"; }).join("");
      cur = F.st.file && S[F.st.file] ? F.st.file : names[0];
      F.r("file").value = cur;
      start();
    }).catch(function () { F.note(""); F.msg("The files didn't load.", true); });
  }

  global.AayatTools.register({ id: "tabletop", title: "Tabletop exercise", console: true, group: "Incident responder", mount: mount, scenarios: scenarios, check: check });
})(window);
