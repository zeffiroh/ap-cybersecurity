(function () {
  "use strict";
  var $ = function (id) { return document.getElementById(id); };
  var token = new URLSearchParams(location.search).get("t") || "";
  var state = { lessons: [], sources: [], shells: [], windows: true }, current = null, tab = "record", steps = [], dirty = false, statusTimer = 0;
  var TABS = [["record", "Record"], ["edit", "Edit steps"], ["check", "Check"], ["preview", "Preview"], ["publish", "Publish"]];

  function esc(s) { return String(s == null ? "" : s).replace(/[&<>"']/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]; }); }
  function say(text, bad) {
    var el = $("status");
    el.textContent = text;
    el.hidden = false;
    el.classList.toggle("bad", !!bad);
    clearTimeout(statusTimer);
    statusTimer = setTimeout(function () { el.hidden = true; }, bad ? 9000 : 4500);
  }
  function api(path, body) {
    var opts = { headers: { "X-Desk": token } };
    if (body) { opts.method = "POST"; opts.headers["Content-Type"] = "application/json"; opts.body = JSON.stringify(body); }
    return fetch(path, opts).then(function (r) {
      return r.json().then(function (d) {
        if (!r.ok || d.error) throw new Error(d.error || "That didn't work.");
        return d;
      });
    });
  }
  function fail(e) { say(e.message, true); }
  function shellName(s) { return s === "bash" ? "This computer's Linux" : s.replace(/^wsl:/, "").replace("kali-linux", "Kali Linux"); }
  function shellOptions() { return state.shells.map(function (s) { return '<option value="' + esc(s) + '">' + esc(shellName(s)) + "</option>"; }).join(""); }

  function refresh() {
    return api("/api/state").then(function (d) { state = d; drawList(); fillNew(); });
  }

  function drawList() {
    $("list").innerHTML = state.lessons.length ? state.lessons.map(function (l) {
      var where = l.running ? '<span class="live">Studio open</span>' : l.published ? "Ready to publish" : l.built ? "Draft" : l.recorded ? "Recorded, not built" : "Not recorded";
      return '<a href="#' + esc(l.name) + '" class="' + (current && current.name === l.name ? "on" : "") + '"><b>' + esc(l.title) + "</b><small>" + where + "</small></a>";
    }).join("") : '<p class="empty">Your lessons appear here.</p>';
  }

  function fillNew() {
    var groups = {};
    state.sources.forEach(function (s) { (groups[s.kind] = groups[s.kind] || []).push(s); });
    $("nSource").innerHTML = '<option value="">An empty folder</option>' + Object.keys(groups).map(function (k) {
      return '<optgroup label="' + esc(k) + 's">' + groups[k].map(function (s) { return '<option value="' + esc(s.id) + '">' + esc(s.title) + "</option>"; }).join("") + "</optgroup>";
    }).join("");
    $("nShell").innerHTML = shellOptions();
  }

  function welcome() {
    current = null;
    drawList();
    $("main").innerHTML = '<div class="welcome"><h2>Teach it once. Students get a lab they can run.</h2>' +
      "<p>Each lesson moves through five stages:</p><ol class=\"path\"><li><b>Record</b> real work in a real Linux terminal, with screen video if you want it.</li>" +
      "<li><b>Edit steps</b> to tidy titles, notes, hints and questions.</li><li><b>Check</b> what was removed or left out. The repo is public.</li>" +
      "<li><b>Preview</b> the three support levels, the guide and the replay.</li><li><b>Publish</b> when it reads right.</li></ol>" +
      (state.shells.length ? '<p><button class="go" id="wNew">Start your first lesson</button></p>' : '<p class="warn">Recording needs Linux. On Windows, install it with <code>wsl --install -d Ubuntu</code>, then reopen the desk.</p>') + "</div>";
    var b = $("wNew");
    if (b) b.addEventListener("click", openNew);
  }

  function openNew() {
    if (!state.shells.length) return say("Recording needs Linux. Install it with: wsl --install -d Ubuntu", true);
    $("newDlg").showModal();
    $("nTitle").focus();
  }

  function load(name, nextTab) {
    return api("/api/lesson?name=" + encodeURIComponent(name)).then(function (d) {
      current = d;
      steps = toSteps(d.cells);
      dirty = false;
      if (nextTab) tab = nextTab;
      else if (!d.built) tab = "record";
      drawList();
      draw();
    }).catch(fail);
  }

  function toSteps(cells) {
    var out = [];
    cells.forEach(function (c) {
      if (c.t === "md") {
        var m = /^##\s*(?:\d+[.)]\s*)?(.*)(?:\n+([\s\S]*))?$/.exec(c.s);
        out.push({ title: m ? m[1].trim() : "", note: m ? (m[2] || "").trim() : c.s, cells: [] });
      } else {
        if (!out.length) out.push({ title: "Getting started", note: "", cells: [] });
        out[out.length - 1].cells.push(Object.assign({}, c));
      }
    });
    return out;
  }
  function toCells() {
    var cells = [];
    steps.forEach(function (s, i) {
      cells.push({ t: "md", s: "## " + (i + 1) + ". " + (s.title.trim() || "Untitled step") + (s.note.trim() ? "\n\n" + s.note.trim() : "") });
      s.cells.forEach(function (c) { cells.push(c); });
    });
    return cells;
  }

  function isReady(key) {
    var c = current;
    if (key === "record") return c.recorded;
    if (key === "edit") return c.built;
    if (key === "check") return c.built && !c.problems.length && !!(c.about.summary || "").trim();
    if (key === "publish") return c.published;
    return false;
  }

  function draw() {
    if (!current) return welcome();
    var c = current;
    $("main").innerHTML = '<header class="head"><h2>' + esc(c.title) + "</h2><p><code>source/seminars/" + esc(c.name) + '</code></p></header><nav class="rail" aria-label="Lesson stages">' +
      TABS.map(function (t, i) {
        return '<button data-tab="' + t[0] + '" class="' + (t[0] === tab ? "on " : "") + (isReady(t[0]) ? "ready" : "") + '"' + (t[0] === tab ? ' aria-current="step"' : "") + "><i>" + (i + 1) + "</i>" + t[1] + "</button>";
      }).join("") + '</nav><section class="pane" id="pane"></section>';
    document.querySelectorAll("[data-tab]").forEach(function (b) {
      b.addEventListener("click", function () {
        if (dirty) { saveSteps().then(function () { tab = b.getAttribute("data-tab"); draw(); }); return; }
        tab = b.getAttribute("data-tab");
        draw();
      });
    });
    ({ record: paneRecord, edit: paneEdit, check: paneCheck, preview: panePreview, publish: panePublish })[tab]();
  }

  function buildNow(force) {
    say("Building the lesson…");
    var name = current.name;
    return api("/api/build", { name: name, force: !!force }).then(function (d) {
      if (d.needsConfirm) {
        $("pane").querySelector("#confirm").hidden = false;
        say("Your edits would be replaced. Choose below.");
        return;
      }
      say("Built. Check what changed.");
      return refresh().then(function () { return load(name, "check"); });
    }).catch(fail);
  }

  function paneRecord() {
    var c = current, pick = '<select id="shell" aria-label="Linux to teach on">' + shellOptions() + "</select>";
    $("pane").innerHTML = '<div class="studio"><h3>' + (c.running ? '<span class="dot"></span>The studio is open' : c.recorded ? "Carry on recording" : "Start recording") + "</h3>" +
      "<p>Teach in a real terminal. Everything you type and every file you change is saved as you go. A screen recording button is inside.</p>" +
      '<div class="row">' + (c.running ? '<a class="go-link" href="' + esc(c.link) + '" target="_blank" rel="noopener"><button class="go" tabindex="-1">Go to the studio</button></a><button id="stopS" class="stop">Close the studio</button>'
        : pick + '<button id="openS" class="go">Open the studio</button>') + "</div>" +
      (c.recorded ? '<div class="facts"><div><b>' + c.steps + "</b><span>steps</span></div><div><b>" + c.commands + "</b><span>commands</span></div><div><b>" + c.minutes + "</b><span>minutes</span></div></div>" : "") + "</div>" +
      (c.recorded ? '<h3>Build the lesson</h3><p>Turns the recording into a codebook, a simulated setup, three support levels, a guide, a replay and video chapters.' + (c.running ? " This closes the studio first." : "") + '</p><p><button id="buildBtn" class="go">Build the lesson</button></p>' +
        '<div id="confirm" class="warn" hidden><p>You edited this lesson\'s steps. Building again replaces those edits with the recording.</p><div class="row"><button id="buildForce">Replace my edits</button><button id="buildKeep">Keep my edits</button></div></div>' : "");
    var el;
    if ((el = $("openS"))) el.addEventListener("click", function () {
      el.disabled = true;
      var win = window.open("about:blank", "_blank");
      say("Opening the studio…");
      api("/api/open", { name: c.name, shell: $("shell").value }).then(function (d) {
        if (win) win.location = d.link;
        return refresh().then(function () { return load(c.name, "record"); });
      }).catch(function (e) { if (win) win.close(); el.disabled = false; fail(e); });
    });
    if ((el = $("stopS"))) el.addEventListener("click", function () {
      api("/api/stop", { name: c.name }).then(function () { say("Closed. Your recording is saved."); return refresh().then(function () { return load(c.name, "record"); }); }).catch(fail);
    });
    if ((el = $("buildBtn"))) el.addEventListener("click", function () { buildNow(false); });
    if ((el = $("buildForce"))) el.addEventListener("click", function () { buildNow(true); });
    if ((el = $("buildKeep"))) el.addEventListener("click", function () { tab = "edit"; draw(); });
  }

  function saveSteps() {
    return api("/api/save", { name: current.name, cells: toCells() }).then(function (d) {
      current = d;
      steps = toSteps(d.cells);
      dirty = false;
      say("Saved.");
    }).catch(fail);
  }

  function paneEdit() {
    if (!current.built) { $("pane").innerHTML = "<p>Record something and build the lesson first. Its steps appear here.</p>"; return; }
    $("pane").innerHTML = steps.map(function (s, i) {
      return '<article class="step" data-s="' + i + '"><div class="stephead"><strong>' + (i + 1) + '</strong><input data-f="title" aria-label="Step ' + (i + 1) + ' title" value="' + esc(s.title) + '">' +
        '<button data-a="up" aria-label="Move step ' + (i + 1) + ' up"' + (i ? "" : " disabled") + '>Up</button><button data-a="down" aria-label="Move step ' + (i + 1) + ' down"' + (i < steps.length - 1 ? "" : " disabled") + '>Down</button><button data-a="del" aria-label="Delete step ' + (i + 1) + '">Delete</button></div>' +
        '<label>What students read<textarea data-f="note" rows="' + Math.min(10, Math.max(3, s.note.split("\n").length + 1)) + '">' + esc(s.note) + "</textarea></label>" +
        '<div class="row"><button class="small" data-a="hint">Add a hint</button><button class="small" data-a="ask">Add a question</button><button class="small" data-a="check">Add a checklist item</button></div>' +
        s.cells.map(function (c, k) {
          var rec = !!c.r;
          return '<div class="cell" data-c="' + k + '"><header><span>' + (c.t === "py" ? "Python" : "Linux") + (rec ? ", recorded on a real system. Students replay this, so it can't be edited" : "") + '</span><button class="small" data-a="delc">Remove</button></header>' +
            (rec ? "<pre>" + esc(c.s) + "</pre>" : '<textarea data-f="code" spellcheck="false" rows="' + Math.min(14, c.s.split("\n").length + 1) + '" aria-label="Code">' + esc(c.s) + "</textarea>") +
            (c.e ? "<details><summary>Recorded output</summary><pre>" + esc(c.e) + "</pre></details>" : "") + "</div>";
        }).join("") + "</article>";
    }).join("") + '<p><button id="addStep">Add a step</button></p><div class="save"><button id="saveBtn" class="go">Save steps</button><span id="saved">' + (dirty ? "Not saved yet" : "All saved") + "</span></div>";
    var pane = $("pane");
    function touch() { dirty = true; $("saved").textContent = "Not saved yet"; }
    pane.oninput = function (e) {
      var f = e.target.getAttribute("data-f"), art = e.target.closest("[data-s]");
      if (!f || !art) return;
      var s = steps[+art.getAttribute("data-s")];
      if (f === "code") s.cells[+e.target.closest("[data-c]").getAttribute("data-c")].s = e.target.value;
      else s[f] = e.target.value;
      touch();
    };
    pane.onclick = function (e) {
      var a = e.target.getAttribute("data-a"), art = e.target.closest("[data-s]");
      if (!a || !art) return;
      var i = +art.getAttribute("data-s"), s = steps[i], note = art.querySelector('[data-f="note"]');
      function add(text) { s.note = (s.note.trim() ? s.note.trim() + "\n\n" : "") + text; note.value = s.note; note.focus(); touch(); }
      if (a === "hint") return add("> Hint: ");
      if (a === "ask") return add("?> Your question :: the answer");
      if (a === "check") return add("- [ ] Something to do");
      if (a === "up" || a === "down") { var j = i + (a === "up" ? -1 : 1); steps[i] = steps[j]; steps[j] = s; }
      else if (a === "del") steps.splice(i, 1);
      else if (a === "delc") s.cells.splice(+e.target.closest("[data-c]").getAttribute("data-c"), 1);
      dirty = true;
      paneEdit();
    };
    $("addStep").addEventListener("click", function () { steps.push({ title: "New step", note: "", cells: [] }); dirty = true; paneEdit(); });
    $("saveBtn").addEventListener("click", function () { saveSteps().then(paneEdit); });
  }

  function paneCheck() {
    var c = current;
    if (!c.built) { $("pane").innerHTML = "<p>Build the lesson first. What needs checking appears here.</p>"; return; }
    var a = c.about, items = c.problems.concat(c.review);
    $("pane").innerHTML = "<h3>Before it goes public</h3>" + (items.length ? '<div class="warn"><ul class="checks">' + items.map(function (x) { return "<li>" + esc(x) + "</li>"; }).join("") + "</ul></div>"
      : '<p class="good">Nothing was removed or left out. Still read the lab: automatic cleaning can miss things.</p>') +
      '<h3>Lesson details</h3><form id="aboutForm"><div class="fields"><label class="all">Title<input name="title" required value="' + esc(a.title) + '"></label>' +
      '<label class="all">Summary students see<textarea name="summary" rows="3">' + esc(a.summary) + "</textarea></label>" +
      '<label>Level<select name="level">' + ["Beginner", "Intermediate", "Advanced"].map(function (l) { return "<option" + (a.level === l ? " selected" : "") + ">" + l + "</option>"; }).join("") + "</select></label>" +
      '<label>Minutes<input name="minutes" type="number" min="1" value="' + esc(a.minutes) + '"></label><label>Units<input name="units" placeholder="1, 4" value="' + esc((a.units || []).join(", ")) + '"></label></div>' +
      '<label class="toggle"><input type="checkbox" name="published"' + (a.published ? " checked" : "") + ">I have read this lab, and it can go public next time I publish</label>" +
      '<p><button class="go">Save details</button></p></form>';
    $("aboutForm").addEventListener("submit", function (e) {
      e.preventDefault();
      var f = e.target;
      api("/api/save", { name: c.name, about: { title: f.title.value, summary: f.summary.value, level: f.level.value, minutes: f.minutes.value, units: f.units.value, published: f.published.checked } }).then(function (d) {
        current = d;
        say("Saved.");
        return refresh().then(draw);
      }).catch(fail);
    });
  }

  function panePreview() {
    if (!current.built) { $("pane").innerHTML = "<p>Build the lesson first, then preview it here.</p>"; return; }
    $("pane").innerHTML = "<h3>See it as a student</h3><p>This preview stays on your computer, even for a draft.</p><p><button id=\"makeP\" class=\"go\">Make a preview</button></p><div id=\"pl\" class=\"links\"></div>";
    $("makeP").addEventListener("click", function () {
      say("Making the preview…");
      api("/api/preview", { name: current.name }).then(function (d) {
        var rows = [["Worked example", d.worked], ["Guided", d.guided], ["On your own", d.solo], ["Printable guide", d.guide]];
        if (d.replay) rows.push(["Terminal replay", d.replay]);
        $("pl").innerHTML = rows.map(function (r) { return '<a href="' + esc(r[1]) + '" target="_blank" rel="noopener">' + r[0] + "</a>"; }).join("");
        say("Preview ready.");
      }).catch(fail);
    });
  }

  function panePublish() {
    var c = current, cmd = (state.windows ? ".\\publish.cmd" : "./publish") + ' "' + c.title.replace(/"/g, "") + '"';
    $("pane").innerHTML = (c.published ? '<p class="good">This lesson goes live the next time you publish.</p>' : '<p class="warn">This lesson stays private until you tick the box in Check.</p>') +
      "<h3>See what would go up</h3><p>This builds the site and lists the changes. Nothing is pushed.</p><p><button id=\"dry\">Run a publish check</button></p><pre id=\"dryOut\" class=\"out\" hidden></pre>" +
      "<h3>Publish</h3><p>Run this yourself in the project folder. It checks again and asks before pushing:</p><pre class=\"out\" id=\"cmd\">" + esc(cmd) + '</pre><p><button id="copyCmd">Copy the command</button></p>' +
      (c.chapters ? '<h3>YouTube chapters</h3><p>Paste these into your video description:</p><pre class="out">' + esc(c.chapters) + '</pre><p><button id="copyCh">Copy the chapters</button></p>' : "");
    function copy(id, text) { var b = $(id); if (b) b.addEventListener("click", function () { navigator.clipboard.writeText(text).then(function () { say("Copied."); }, function () { say("Your browser blocked copying. Select the text instead.", true); }); }); }
    copy("copyCmd", cmd);
    copy("copyCh", c.chapters);
    $("dry").addEventListener("click", function () {
      var b = $("dry"), out = $("dryOut");
      b.disabled = true;
      out.hidden = false;
      out.textContent = "Building the site. This can take a minute…";
      api("/api/dryrun", {}).then(function (d) { out.textContent = d.output || "(no output)"; }).catch(function (e) { out.textContent = e.message; }).then(function () { b.disabled = false; });
    });
  }

  function route() {
    var name = decodeURIComponent(location.hash.slice(1));
    if (name) load(name);
    else welcome();
  }

  $("newBtn").addEventListener("click", openNew);
  $("nCancel").addEventListener("click", function () { $("newDlg").close(); });
  $("newForm").addEventListener("submit", function (e) {
    e.preventDefault();
    var title = $("nTitle").value.trim(), go = $("nGo");
    var name = title.toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-+|-+$/g, "").slice(0, 48);
    if (!name) return say("Use some letters or numbers in the title.", true);
    go.disabled = true;
    var win = window.open("about:blank", "_blank");
    say("Opening the studio…");
    api("/api/new", { name: name, title: title, source: $("nSource").value, shell: $("nShell").value }).then(function (d) {
      if (win) win.location = d.link;
      $("newDlg").close();
      $("newForm").reset();
      tab = "record";
      return refresh().then(function () { location.hash = d.name; });
    }).catch(function (err) { if (win) win.close(); fail(err); }).then(function () { go.disabled = false; });
  });
  window.addEventListener("hashchange", route);
  window.addEventListener("beforeunload", function (e) { if (dirty) { e.preventDefault(); e.returnValue = ""; } });
  refresh().then(route).catch(fail);
})();
