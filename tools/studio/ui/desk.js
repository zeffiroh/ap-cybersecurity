(function () {
  "use strict";
  var $ = function (id) { return document.getElementById(id); };
  var token = new URLSearchParams(location.search).get("t") || "";
  var state = { lessons: [], sources: [], shells: [], windows: true }, current = null, tab = "edit", steps = [], dirty = false, statusTimer = 0;
  var videos = [], job = { running: false }, jobShown = false, pollTimer = 0, vFilter = "all";
  var RECORDED = [["record", "Record"], ["edit", "Edit steps"], ["check", "Check"], ["preview", "Preview"], ["video", "Video"], ["publish", "Publish"]];
  var PAGES = [["edit", "Edit steps"], ["check", "Check"], ["preview", "Preview"], ["video", "Video"], ["publish", "Publish"]];

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
  function clock(s) {
    s = Math.round(s || 0);
    var h = Math.floor(s / 3600), m = Math.floor(s % 3600 / 60), x = s % 60;
    return (h ? h + ":" + String(m).padStart(2, "0") : m) + ":" + String(x).padStart(2, "0");
  }
  function rows(text, most) { return Math.min(most, Math.max(3, String(text || "").split("\n").length + 1)); }
  function shellName(s) { return s === "bash" ? "This computer's Linux" : s.replace(/^wsl:/, "").replace("kali-linux", "Kali Linux"); }
  function shellOptions() { return state.shells.map(function (s) { return '<option value="' + esc(s) + '">' + esc(shellName(s)) + "</option>"; }).join(""); }
  function tabsFor(c) { return c.kind === "pages" ? PAGES : RECORDED; }

  function refresh() {
    return api("/api/state").then(function (d) { state = d; drawList(); fillNew(); });
  }

  function drawList() {
    $("vidBtn").classList.toggle("on", location.hash === "#videos");
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
      "<p>Two things happen here.</p><ol class=\"path\"><li><b>Videos</b>: make the silent video for any lecture, tutorial, seminar or network lab, record your voice over it, and make the final video for YouTube. No commands to type.</li>" +
      "<li><b>Lessons</b> (on the left): open one to edit its steps, check it, preview it as a student and see how to publish it. <b>New lesson</b> records a new one in a real Linux terminal.</li></ol>" +
      '<div class="row"><button class="go" id="wVid">Open Videos</button><button id="wNew">New lesson</button></div>' +
      (state.shells.length ? "" : '<p class="warn">Recording a new lesson needs Linux. On Windows, install it with <code>wsl --install -d Ubuntu</code>, then reopen the desk. Videos work without it.</p>') + "</div>";
    $("wVid").addEventListener("click", function () { location.hash = "videos"; });
    $("wNew").addEventListener("click", openNew);
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
    var c = current, tabs = tabsFor(c);
    if (!tabs.some(function (t) { return t[0] === tab; })) tab = tabs[0][0];
    $("main").innerHTML = '<header class="head"><h2>' + esc(c.title) + "</h2><p><code>source/seminars/" + esc(c.name) + '</code></p></header><nav class="rail" aria-label="Lesson stages">' +
      tabs.map(function (t, i) {
        return '<button data-tab="' + t[0] + '" class="' + (t[0] === tab ? "on " : "") + (isReady(t[0]) ? "ready" : "") + '"' + (t[0] === tab ? ' aria-current="step"' : "") + "><i>" + (i + 1) + "</i>" + t[1] + "</button>";
      }).join("") + '</nav><section class="pane" id="pane"></section>';
    document.querySelectorAll("[data-tab]").forEach(function (b) {
      b.addEventListener("click", function () {
        var next = b.getAttribute("data-tab");
        if (dirty) { saveCurrent().then(function () { tab = next; draw(); }); return; }
        tab = next;
        draw();
      });
    });
    ({ record: paneRecord, edit: c.kind === "pages" ? panePages : paneEdit, check: paneCheck, preview: panePreview, video: paneVideo, publish: panePublish })[tab]();
  }

  function saveCurrent() { return current && current.kind === "pages" ? savePages() : saveSteps(); }

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
        : state.shells.length ? pick + '<button id="openS" class="go">Open the studio</button>' : '<span>Recording needs Linux: <code>wsl --install -d Ubuntu</code></span>') + "</div>" +
      (c.recorded ? '<div class="facts"><div><b>' + c.steps + "</b><span>steps</span></div><div><b>" + c.commands + "</b><span>commands</span></div><div><b>" + c.minutes + "</b><span>minutes</span></div></div>" : "") + "</div>" +
      (c.recorded ? '<h3>Build the lesson</h3><p>Turns the recording into a codebook, a simulated setup, three support levels, a guide, a replay and video chapters.' + (c.running ? " This closes the studio first." : "") + '</p><p><button id="buildBtn" class="go">Build the lesson</button></p>' +
        '<div id="confirm" class="warn" hidden><p>You edited this lesson\'s steps. Building again replaces those edits with the recording.</p><div class="row"><button id="buildForce">Replace my edits</button><button id="buildKeep">Keep my edits</button></div></div>' : "");
    var openS = $("openS"), stopS = $("stopS"), buildBtn = $("buildBtn"), buildForce = $("buildForce"), buildKeep = $("buildKeep");
    if (openS) openS.addEventListener("click", function () {
      openS.disabled = true;
      var win = window.open("about:blank", "_blank");
      say("Opening the studio…");
      api("/api/open", { name: c.name, shell: $("shell").value }).then(function (d) {
        if (win) win.location = d.link;
        return refresh().then(function () { return load(c.name, "record"); });
      }).catch(function (e) { if (win) win.close(); openS.disabled = false; fail(e); });
    });
    if (stopS) stopS.addEventListener("click", function () {
      api("/api/stop", { name: c.name }).then(function () { say("Closed. Your recording is saved."); return refresh().then(function () { return load(c.name, "record"); }); }).catch(fail);
    });
    if (buildBtn) buildBtn.addEventListener("click", function () { buildNow(false); });
    if (buildForce) buildForce.addEventListener("click", function () { buildNow(true); });
    if (buildKeep) buildKeep.addEventListener("click", function () { tab = "edit"; draw(); });
  }

  function saveSteps() {
    return api("/api/save", { name: current.name, cells: toCells() }).then(function (d) {
      current = d;
      steps = toSteps(d.cells);
      dirty = false;
      say("Saved.");
    }).catch(fail);
  }

  function savePages() {
    return api("/api/pages", { name: current.name, pages: current.pages }).then(function (d) {
      current = d;
      dirty = false;
      say("Saved.");
    });
  }

  function panePages() {
    var c = current;
    $("pane").innerHTML = '<p>Each step is one page in <code>source/seminars/' + esc(c.name) + "</code>. Change the words here, then press <b>Save and build</b> so the site and the next video use them. " +
      "The words you read aloud in the video are separate: they're the \"script\" in <code>seminar.json</code>, and <code>script.md</code> shows them as a page.</p>" +
      c.pages.map(function (p, i) {
        return '<article class="step" data-p="' + i + '"><div class="stephead"><strong>' + (i + 1) + "</strong><code>" + esc(p.file) + "</code></div>" +
          '<label>What students read<textarea data-f="text" rows="' + rows(p.text, 16) + '">' + esc(p.text) + "</textarea></label>" +
          (p.codeFile ? '<div class="cell"><header><span>' + (/\.py$/.test(p.codeFile) ? "Python" : "Linux") + " cell, " + esc(p.codeFile) + '</span></header><textarea data-f="code" spellcheck="false" rows="' + rows(p.code, 14) + '" aria-label="Code for step ' + (i + 1) + '">' + esc(p.code) + "</textarea></div>" : "") +
          "</article>";
      }).join("") +
      '<p class="hint">To add, remove or reorder steps, rename the files in the folder (01-, 02-, …) and reopen this lab.</p>' +
      '<div class="save"><button id="saveP">Save steps</button><button id="buildP" class="go">Save and build</button><span id="saved">' + (dirty ? "Not saved yet" : "All saved") + "</span></div>";
    var pane = $("pane");
    pane.oninput = function (e) {
      var f = e.target.getAttribute("data-f"), art = e.target.closest("[data-p]");
      if (!f || !art) return;
      c.pages[+art.getAttribute("data-p")][f] = e.target.value;
      dirty = true;
      $("saved").textContent = "Not saved yet";
    };
    pane.onclick = null;
    $("saveP").addEventListener("click", function () { savePages().then(function () { $("saved").textContent = "All saved"; }).catch(fail); });
    $("buildP").addEventListener("click", function () {
      savePages().then(function () {
        $("saved").textContent = "Saved. Building…";
        return api("/api/rebuild", { name: c.name });
      }).then(function (d) { showJob(d.job); }).catch(fail);
    });
  }

  function paneEdit() {
    if (!current.built) { $("pane").innerHTML = "<p>Record something and build the lesson first. Its steps appear here.</p>"; return; }
    $("pane").innerHTML = steps.map(function (s, i) {
      return '<article class="step" data-s="' + i + '"><div class="stephead"><strong>' + (i + 1) + '</strong><input data-f="title" aria-label="Step ' + (i + 1) + ' title" value="' + esc(s.title) + '">' +
        '<button data-a="up" aria-label="Move step ' + (i + 1) + ' up"' + (i ? "" : " disabled") + '>Up</button><button data-a="down" aria-label="Move step ' + (i + 1) + ' down"' + (i < steps.length - 1 ? "" : " disabled") + '>Down</button><button data-a="del" aria-label="Delete step ' + (i + 1) + '">Delete</button></div>' +
        '<label>What students read<textarea data-f="note" rows="' + rows(s.note, 10) + '">' + esc(s.note) + "</textarea></label>" +
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
        var list = [["Worked example", d.worked], ["Guided", d.guided], ["On your own", d.solo], ["Printable guide", d.guide]];
        if (d.replay) list.push(["Terminal replay", d.replay]);
        $("pl").innerHTML = list.map(function (r) { return '<a href="' + esc(r[1]) + '" target="_blank" rel="noopener">' + r[0] + "</a>"; }).join("");
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

  function videoStatus(v) {
    if (!v.silent) return "Not made yet";
    if (v.voiced) return "Final video ready: " + v.voiced;
    if (v.takes) return "Silent video " + clock(v.seconds) + ". Voice recorded (" + v.takes + (v.takes === 1 ? " take" : " takes") + "), final video not made yet";
    return "Silent video ready, " + clock(v.seconds) + ". No voice yet";
  }

  function videoRow(v) {
    var busy = job.running, making = busy && job.name === v.key;
    var cls = "vrow" + (v.voiced ? " done" : v.silent ? " half" : "") + (v.stale ? " stale" : "");
    return '<article class="' + cls + '" data-k="' + esc(v.key) + '"><div class="vinfo"><b>' + esc(v.title) + "</b><span>" + (making ? "Being made now…" : esc(videoStatus(v))) + "</span>" +
      (v.stale ? '<span class="stalemsg">The words changed after this video was made. Make it again before you record your voice.</span>' : "") + "</div>" +
      '<div class="vacts"><button data-v="make"' + (busy ? " disabled" : "") + ">" + (v.silent ? "Make it again" : "Make the silent video") + "</button>" +
      '<button data-v="voice" class="' + (v.silent && !v.voiced ? "go" : "") + '"' + (v.silent ? "" : " disabled") + ">" + (v.voicing ? "Back to the voice studio" : "Record my voice") + "</button>" +
      '<button data-v="mix"' + (v.takes && !busy ? "" : " disabled") + ">Make the final video</button>" +
      '<button data-v="folder" class="small"' + (v.silent ? "" : " disabled") + ">Open the folder</button></div></article>";
  }

  function bindVideos(box) {
    box.onclick = function (e) {
      var b = e.target.closest("[data-v]"), row = e.target.closest("[data-k]");
      if (!b || !row || b.disabled) return;
      var a = b.getAttribute("data-v"), key = row.getAttribute("data-k");
      if (a === "voice") {
        var win = window.open("about:blank", "_blank");
        say("Opening the voice studio…");
        return api("/api/video", { action: "voice", name: key }).then(function (d) {
          if (win) win.location = d.link; else location.href = d.link;
          say("The voice studio is open in a new tab. Press R there to record.");
          return loadVideos();
        }).catch(function (err) { if (win) win.close(); fail(err); });
      }
      var v = videos.filter(function (x) { return x.key === key; })[0];
      if (a === "make" && v && v.silent && !b.classList.contains("sure")) {
        b.classList.add("sure", "stop");
        b.textContent = v.takes ? "Click again: this deletes your " + v.takes + (v.takes === 1 ? " voice take" : " voice takes") : "Click again to replace it";
        setTimeout(function () { if (b.isConnected && b.classList.contains("sure")) { b.classList.remove("sure", "stop"); b.textContent = "Make it again"; } }, 6000);
        return;
      }
      b.disabled = true;
      api("/api/video", { action: a, name: key }).then(function (d) {
        if (d.job) showJob(d.job);
        if (a === "folder") say("The folder is open in File Explorer.");
        return loadVideos();
      }).catch(function (err) { b.disabled = false; fail(err); });
    };
  }

  function loadVideos() {
    return api("/api/videos").then(function (d) {
      videos = d.items;
      job = d.job;
      drawVideos();
      if (current && tab === "video" && $("vone")) drawOne();
      if (job.running) showJob(job);
    });
  }

  function drawVideos() {
    var el = $("vlist");
    if (!el) return;
    var keep = { all: function () { return true; }, todo: function (v) { return !v.silent || v.stale; }, voice: function (v) { return v.silent && !v.voiced && !v.stale; }, done: function (v) { return !!v.voiced; } }[vFilter];
    var groups = [];
    videos.forEach(function (v) {
      var g = groups[groups.length - 1];
      if (!g || g.name !== v.group) groups.push(g = { name: v.group, items: [] });
      g.items.push(v);
    });
    el.innerHTML = groups.map(function (g) {
      var shown = g.items.filter(keep), done = g.items.filter(function (v) { return v.voiced; }).length;
      if (!shown.length) return "";
      return '<section class="vgroup"><h3>' + esc(g.name) + " <small>" + done + " of " + g.items.length + " finished</small></h3>" + shown.map(videoRow).join("") + "</section>";
    }).join("") || '<p class="good">Nothing here. Try another filter.</p>';
  }

  function videosPage() {
    current = null;
    dirty = false;
    drawList();
    $("main").innerHTML = '<header class="head"><h2>Videos</h2><p>For each video: <b>1</b> make the silent video, <b>2</b> record your voice over it, <b>3</b> make the final video. ' +
      "Then upload the final video to YouTube as Unlisted, with youtube.txt and the .srt subtitles from its folder.</p></header>" +
      '<div class="vtools" role="group" aria-label="Show">' + [["all", "All"], ["todo", "To make"], ["voice", "Ready for my voice"], ["done", "Finished"]].map(function (f) {
        return '<button data-f="' + f[0] + '" class="small' + (vFilter === f[0] ? " on" : "") + '" aria-pressed="' + (vFilter === f[0]) + '">' + f[1] + "</button>";
      }).join("") + "</div>" +
      '<p class="hint">Only one video is made at a time: two at once runs the computer out of memory. A lab video plays at reading pace, so it takes as long as the narration (5 to 25 minutes); a lecture takes 1 to 2 hours.</p>' +
      '<div id="vlist"><p>Loading…</p></div>';
    document.querySelector(".vtools").addEventListener("click", function (e) {
      var f = e.target.getAttribute("data-f");
      if (!f) return;
      vFilter = f;
      document.querySelectorAll(".vtools button").forEach(function (b) { var on = b.getAttribute("data-f") === f; b.classList.toggle("on", on); b.setAttribute("aria-pressed", on); });
      drawVideos();
    });
    bindVideos($("vlist"));
    loadVideos().catch(fail);
  }

  function drawOne() {
    var v = videos.filter(function (x) { return x.key === current.name; })[0], el = $("vone");
    if (!el) return;
    el.innerHTML = v ? videoRow(v) : '<p class="warn">The Desk makes videos for lectures, free tutorials, seminars and network labs. This one has none yet.</p>';
  }

  function paneVideo() {
    $("pane").innerHTML = "<h3>This lab's video</h3><p>Make the silent video, record your voice over it, then make the final video. Every video is also on the <a href=\"#videos\">Videos</a> page.</p>" +
      '<div id="vone"><p>Loading…</p></div>' +
      (current.kind === "pages" ? '<p class="hint">The words you read are in <code>seminar.json</code> ("script") and <code>script.md</code> in this lab\'s folder. Making the video refreshes script.md and rebuilds the lab first.</p>' : "");
    bindVideos($("vone"));
    loadVideos().catch(fail);
  }

  function showJob(j) {
    job = j || job;
    var box = $("job");
    if (!job.started && !job.label) return;
    jobShown = true;
    box.hidden = false;
    var ok = !job.running && job.code === 0, bad = !job.running && job.code !== 0;
    box.className = "job" + (ok ? " ok" : bad ? " bad" : "");
    box.innerHTML = "<header><b>" + (job.running ? "Making" : ok ? "Done" : job.stopped ? "Stopped" : "It stopped with a problem") + ": " + esc(job.label) + "</b><span>" + clock(job.seconds) + "</span></header>" +
      '<pre aria-live="off">' + esc((job.lines || []).slice(-10).join("\n")) + "</pre>" +
      '<div class="row">' + (job.running ? '<button id="jobStop" class="stop small">Stop</button>' : '<button id="jobClose" class="small">Close</button>') + "</div>";
    var s = $("jobStop"), c = $("jobClose");
    if (s) s.addEventListener("click", function () { s.disabled = true; api("/api/video-stop", {}).then(showJob).catch(fail); });
    if (c) c.addEventListener("click", function () { box.hidden = true; jobShown = false; });
    clearTimeout(pollTimer);
    if (job.running) pollTimer = setTimeout(poll, 2000);
  }

  function poll() {
    api("/api/job").then(function (j) {
      var finished = job.running && !j.running;
      showJob(j);
      if (finished) {
        say(j.code === 0 ? "Finished: " + j.label : "It stopped: " + j.label, j.code !== 0);
        refresh();
        if ($("vlist") || $("vone")) loadVideos();
        if (current && current.kind === "pages" && tab === "edit" && !dirty) load(current.name, "edit");
      }
    }).catch(function () { pollTimer = setTimeout(poll, 5000); });
  }

  function route() {
    var name = decodeURIComponent(location.hash.slice(1));
    if (name === "videos") videosPage();
    else if (name) load(name);
    else welcome();
  }

  $("newBtn").addEventListener("click", openNew);
  $("vidBtn").addEventListener("click", function () { if (location.hash === "#videos") route(); else location.hash = "videos"; });
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
  refresh().then(route).then(function () { return api("/api/job"); }).then(function (j) { if (j.running) showJob(j); }).catch(fail);
})();
