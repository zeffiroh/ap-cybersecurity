(function (global) {
  "use strict";

  var H, $, esc, rpc, url;

  function q(sel, root) { return (root || document).querySelector(sel); }
  function qa(sel, root) { return Array.prototype.slice.call((root || document).querySelectorAll(sel)); }
  function utf8b64(s) { return btoa(unescape(encodeURIComponent(s))); }
  function slug(s) { return String(s || "").toLowerCase().trim().replace(/[^a-z0-9]+/g, "_").replace(/^_+|_+$/g, ""); }
  function ago(iso) { return H.ago ? H.ago(iso) : new Date(iso).toLocaleString(); }

  function inline(t) {
    return esc(t).replace(/`([^`]+)`/g, "<code>$1</code>").replace(/\*\*([^*]+)\*\*/g, "<b>$1</b>");
  }
  function paras(text) {
    return String(text || "").split(/\n{2,}/).filter(function (x) { return x.trim(); }).map(function (p) {
      p = p.trim();
      var m = p.match(/^(#{1,3})\s+(.*)$/);
      if (m) return "<h" + (m[1].length + 2) + ">" + inline(m[2]) + "</h" + (m[1].length + 2) + ">";
      if (/^[-*] /.test(p)) return "<ul>" + p.split(/\n/).map(function (l) { return "<li>" + inline(l.replace(/^[-*] /, "")) + "</li>"; }).join("") + "</ul>";
      return "<p>" + inline(p).replace(/\n/g, "<br>") + "</p>";
    }).join("");
  }
  function fenced(text) {
    return String(text || "").split(/```[^\n]*\n?/).map(function (part, i) {
      return i % 2 ? "<pre>" + esc(part.replace(/\n$/, "")) + "</pre>" : paras(part);
    }).join("");
  }

  function step(n, title, inner, note) {
    return '<section class="sd-step"><header><span class="sd-n">' + n + "</span><div><h3>" + esc(title) + "</h3>" +
      (note ? '<p class="sd-note">' + note + "</p>" : "") + "</div></header>" + inner + "</section>";
  }
  function field(label, html, hint) {
    return '<label class="sd-f"><span>' + esc(label) + (hint ? " <small>" + hint + "</small>" : "") + "</span>" + html + "</label>";
  }
  function chips(name, opts, value) {
    return '<div class="sd-chips" data-chips="' + name + '">' + opts.map(function (o) {
      return '<button type="button" class="sd-chip' + (String(o[0]) === String(value) ? " on" : "") + '" data-v="' + esc(o[0]) + '">' + o[1] + "</button>";
    }).join("") + "</div>";
  }
  function bindChips(root, onPick) {
    qa("[data-chips]", root).forEach(function (g) {
      qa(".sd-chip", g).forEach(function (b) {
        b.addEventListener("click", function () {
          qa(".sd-chip", g).forEach(function (x) { x.classList.toggle("on", x === b); });
          onPick(g.getAttribute("data-chips"), b.getAttribute("data-v"));
        });
      });
    });
  }
  function shell(listTitle) {
    $("studio").innerHTML = '<div class="sd-bar"><input type="search" id="sd-q" placeholder="Search" aria-label="Search">' +
      '<div id="sd-filters" class="sd-chips"></div><span class="tc-note" id="sd-count"></span></div>' +
      '<div id="sd-editor" class="sd-editor" hidden></div><div id="sd-list" class="sd-list"></div>' +
      '<section class="tc-card" id="sd-extra" hidden></section>';
  }
  function openEditor(html) {
    var e = $("sd-editor");
    e.innerHTML = html;
    e.hidden = false;
    e.scrollIntoView({ behavior: "smooth", block: "start" });
    return e;
  }
  function closeEditor() { $("sd-editor").hidden = true; $("sd-editor").innerHTML = ""; }
  function editorFrame(title, form, preview, saveLabel) {
    return '<div class="sd-head"><h2>' + esc(title) + '</h2><div class="tc-btns"><span class="tc-note" id="sd-msg"></span>' +
      '<button class="btn" id="sd-cancel">Cancel</button><button class="btn dark" id="sd-save">' + esc(saveLabel || "Save") + "</button></div></div>" +
      '<div class="sd-cols"><div class="sd-form">' + form + '</div><aside class="sd-prev"><div class="sd-plabel">What students see</div>' +
      '<div id="sd-preview">' + preview + "</div></aside></div>";
  }
  function rows(list, render, addLabel, kind) {
    return '<div class="sd-rows" data-rows="' + kind + '">' + list.map(render).join("") + '</div><button type="button" class="btn sd-add" data-addrow="' + kind + '">' + esc(addLabel) + "</button>";
  }
  function rowTools() {
    return '<span class="sd-rt"><button type="button" class="btn" data-up title="Move up">&uarr;</button>' +
      '<button type="button" class="btn" data-down title="Move down">&darr;</button><button type="button" class="btn" data-x title="Remove">&times;</button></span>';
  }

  var CHEF = {
    base64: ["Base64", function (s) { return utf8b64(s); }, "It ends in = and uses only letters, digits, + and /. Try From Base64."],
    hex: ["Hex", function (s) { return Array.prototype.map.call(unescape(encodeURIComponent(s)), function (c) { return ("0" + c.charCodeAt(0).toString(16)).slice(-2); }).join(" "); },
      "Pairs of 0-9 and a-f. Try From Hex."],
    rot13: ["ROT13", function (s) { return s.replace(/[a-z]/gi, function (c) { var b = c <= "Z" ? 65 : 97; return String.fromCharCode((c.charCodeAt(0) - b + 13) % 26 + b); }); },
      "The letters look scrambled but the punctuation hasn't moved. Try ROT13."],
    caesar: ["Caesar +3", function (s) { return s.replace(/[a-z]/gi, function (c) { var b = c <= "Z" ? 65 : 97; return String.fromCharCode((c.charCodeAt(0) - b + 3) % 26 + b); }); },
      "Every letter has moved the same number of places. Try ROT13 with a different amount."],
    reverse: ["Reversed", function (s) { return s.split("").reverse().join(""); }, "Read it backwards. CyberChef has Reverse."],
    url: ["URL-encoded", function (s) { return Array.prototype.map.call(unescape(encodeURIComponent(s)), function (c) { return "%" + ("0" + c.charCodeAt(0).toString(16).toUpperCase()).slice(-2); }).join(""); },
      "Lots of % signs. Try URL Decode."],
    binary: ["Binary", function (s) { return Array.prototype.map.call(unescape(encodeURIComponent(s)), function (c) { return ("0000000" + c.charCodeAt(0).toString(2)).slice(-8); }).join(" "); },
      "Groups of eight 0s and 1s. Try From Binary."],
    base64x2: ["Base64 twice", function (s) { return utf8b64(utf8b64(s)); }, "Decoding once gives you more Base64. Keep going."]
  };
  var PLACES = [["linux.html", "Linux lab"], ["sqli.html", "SQL injection lab"], ["shop.html", "Hack the shop"], ["notebook.html#nb-cases-h", "An incident runbook"],
    ["cyberchef/index.html", "CyberChef"], ["lab/lab/index.html", "JupyterLab"]];
  var TYPES = [["decode", "&#128273; Decode it"], ["place", "&#128269; Find it in a lab"], ["question", "&#10067; Answer a question"], ["custom", "&#9881; Custom"]];
  var LEVELS = [[50, "Easy · 50"], [100, "Medium · 100"], [200, "Hard · 200"], [300, "Expert · 300"]];

  function ctfTile(c, solvedNote) {
    var kind = /^cyberchef\//.test(c.link || "") ? "Decode" : c.link ? "Lab" : "Question";
    var level = c.points <= 50 ? "Easy" : c.points <= 100 ? "Medium" : c.points <= 200 ? "Hard" : "Expert";
    return '<span class="ct-kind">' + kind + '</span><span class="ct-level l-' + level.toLowerCase() + '">' + level + "</span>" +
      "<b>" + esc(c.title || "Untitled challenge") + '</b><span class="ct-pts">' + (c.points || 0) + " pts" + (solvedNote || "") + "</span>";
  }
  function ctfDetail(c) {
    var link = c.link ? '<a class="btn" href="' + esc(url(c.link)) + '" target="_blank" rel="noopener">' +
      (/^cyberchef\//.test(c.link) ? "Open in CyberChef" : /^notebook/.test(c.link) ? "Open the runbooks" : "Open the lab") + "</a>" : "";
    return '<div class="ct-detail"><div class="ct-dhead">' + ctfTile(c) + "</div>" + fenced(c.body) +
      (c.hint ? "<details><summary>Hint</summary>" + fenced(c.hint) + "</details>" : "") +
      '<div class="ct-try">' + link + '<input placeholder="aayat{...}" disabled><button class="btn dark" disabled>Submit</button></div></div>';
  }

  function ctf() {
    var data = { challenges: [], solves: [] }, filter = { unit: "", q: "", hidden: false };
    shell();
    $("sd-filters").innerHTML = chips("unit", [["", "All units"], [1, "Unit 1"], [2, "Unit 2"], [3, "Unit 3"], [4, "Unit 4"], [5, "Unit 5"], ["h", "Hidden"]], "");
    bindChips($("studio"), function (k, v) { if (v === "h") { filter.hidden = true; filter.unit = ""; } else { filter.hidden = false; filter.unit = v; } draw(); });
    $("sd-q").addEventListener("input", function () { filter.q = this.value.toLowerCase(); draw(); });

    function guess(c) {
      var body = c.body || "", m = body.match(/```[^\n]*\n([\s\S]*?)\n?```/);
      var story = m ? body.replace(m[0], "").trim() : body.trim(), dataBlock = m ? m[1] : "";
      var type = /^cyberchef\//.test(c.link || "") ? "decode" : c.link && PLACES.some(function (p) { return p[0] === c.link; }) ? "place" : c.link ? "custom" : "question";
      var enc = "";
      if (type === "decode") Object.keys(CHEF).forEach(function (k) { if (!enc && c.flag && CHEF[k][1](c.flag) === dataBlock.trim()) enc = k; });
      return { id: c.id, title: c.title || "", unit: c.unit || 0, points: c.points || 100, story: story, data: dataBlock, hint: c.hint || "", link: c.link || "",
        flag: c.flag || "", answer: (c.flag || "").replace(/^aayat\{|\}$/g, ""), solve: c.solve || "", type: type, enc: enc || (type === "decode" ? "keep" : ""),
        builtin: c.builtin };
    }
    function assemble(s) {
      var data = s.type === "decode" && s.enc && s.enc !== "keep" ? CHEF[s.enc][1](s.flag) : s.data;
      var link = s.type === "decode" ? "cyberchef/index.html" + (data ? "#input=" + utf8b64(data).replace(/=+$/, "") : "") :
        s.type === "place" ? (s.link || PLACES[0][0]) : s.type === "custom" ? s.link : "";
      var body = (s.story || "").trim() + (data && s.type !== "place" && s.type !== "question" ? "\n```\n" + data + "\n```\n" : (s.type === "place" || s.type === "question") && data ? "\n```\n" + data + "\n```\n" : "\n");
      return { title: s.title, unit: +s.unit, points: +s.points, body: body, hint: s.hint, link: link, flag: s.flag, solve: s.solve };
    }
    function edit(c) {
      var s = c ? guess(c) : { title: "", unit: 0, points: 100, story: "", data: "", hint: CHEF.base64[2], link: "", flag: "", answer: "", solve: "", type: "decode", enc: "base64" };
      function form() {
        var typeInner = chips("type", TYPES, s.type);
        var puzzle = field("What students read", '<textarea id="cf-story" rows="4" placeholder="Set the scene: where was this found, what should they do?">' + esc(s.story) + "</textarea>");
        if (s.type === "decode") {
          puzzle += field("Hide the flag with", chips("enc", Object.keys(CHEF).map(function (k) { return [k, CHEF[k][0]]; }).concat(s.enc === "keep" ? [["keep", "Keep my data"]] : []), s.enc),
            "the encoded flag and the CyberChef link are made for you") +
            (s.enc === "keep" ? field("Data block", '<textarea id="cf-data" rows="3">' + esc(s.data) + "</textarea>") : "");
        } else if (s.type === "place") {
          puzzle += field("Where do they look?", '<select id="cf-link">' + PLACES.map(function (p) { return '<option value="' + p[0] + '"' + (p[0] === s.link ? " selected" : "") + ">" + p[1] + "</option>"; }).join("") + "</select>") +
            field("Data block", '<textarea id="cf-data" rows="2" placeholder="Optional: a log line, a hash, a command">' + esc(s.data) + "</textarea>", "optional");
        } else if (s.type === "custom") {
          puzzle += field("Link", '<input id="cf-link" value="' + esc(s.link) + '" placeholder="a site page, e.g. linux.html">') +
            field("Data block", '<textarea id="cf-data" rows="3">' + esc(s.data) + "</textarea>", "optional");
        } else {
          puzzle += field("Data block", '<textarea id="cf-data" rows="2" placeholder="Optional: something to read or calculate">' + esc(s.data) + "</textarea>", "optional");
        }
        return step(1, "Name it", field("Title", '<input id="cf-title" maxlength="200" value="' + esc(s.title) + '" placeholder="e.g. Not a secret code">')) +
          step(2, "What kind of challenge?", typeInner) +
          step(3, "The answer", field("Answer", '<input id="cf-answer" value="' + esc(s.answer) + '" placeholder="e.g. base64 is not encryption" autocomplete="off">',
            "words or a value; we turn it into a flag") +
            '<p class="sd-flag">Students type: <code id="cf-flag">' + esc(s.flag || "aayat{...}") + "</code></p>" +
            '<details class="sd-adv"><summary>Type the exact flag yourself</summary>' + field("Flag", '<input id="cf-flagraw" value="' + esc(s.flag) + '" autocomplete="off">', "not case-sensitive") + "</details>",
            "The flag is checked without caring about capitals or spaces at the ends.") +
          step(4, "The puzzle", puzzle) +
          step(5, "Help", field("Hint", '<textarea id="cf-hint" rows="2">' + esc(s.hint) + "</textarea>", "students choose to open it") +
            field("Walkthrough", '<textarea id="cf-solve" rows="2" placeholder="How to solve it. Only teachers see this.">' + esc(s.solve) + "</textarea>", "teachers only")) +
          step(6, "Unit and points", field("Unit", chips("unit", [[0, "Any"], [1, "1"], [2, "2"], [3, "3"], [4, "4"], [5, "5"]], s.unit)) +
            field("Difficulty", chips("points", LEVELS, s.points)) + field("Exact points", '<input id="cf-points" type="number" min="10" max="1000" step="10" value="' + s.points + '">'));
      }
      function preview() {
        var a = assemble(s);
        return ctfDetail(a) + '<div class="sd-test"><b>Test your flag</b><div class="ct-try"><input id="cf-test" placeholder="type what a student would"><span id="cf-testres"></span></div></div>';
      }
      function sync() {
        var v = function (id) { var e = $(id); return e ? e.value : null; };
        if (v("cf-title") !== null) s.title = v("cf-title");
        if (v("cf-story") !== null) s.story = v("cf-story");
        if (v("cf-data") !== null) s.data = v("cf-data");
        if (v("cf-link") !== null) s.link = v("cf-link");
        if (v("cf-hint") !== null) s.hint = v("cf-hint");
        if (v("cf-solve") !== null) s.solve = v("cf-solve");
        if (v("cf-points") !== null) s.points = +v("cf-points") || 100;
        var raw = v("cf-flagraw"), ans = v("cf-answer");
        if (document.activeElement && document.activeElement.id === "cf-flagraw") s.flag = raw.trim();
        else if (ans !== null) { s.answer = ans; s.flag = /^aayat\{.*\}$/i.test(ans.trim()) ? ans.trim() : ans.trim() ? "aayat{" + slug(ans) + "}" : ""; if ($("cf-flagraw")) $("cf-flagraw").value = s.flag; }
        if ($("cf-flag")) $("cf-flag").textContent = s.flag || "aayat{...}";
        $("sd-preview").innerHTML = preview();
        bindTest();
      }
      function bindTest() {
        var t = $("cf-test");
        if (!t) return;
        t.addEventListener("input", function () {
          var ok = t.value.trim().toLowerCase() === (s.flag || "").trim().toLowerCase() && s.flag;
          $("cf-testres").innerHTML = t.value ? (ok ? '<span class="sd-ok">&#10003; Accepted</span>' : '<span class="sd-bad">Not accepted</span>') : "";
        });
      }
      function render() {
        var ed = openEditor(editorFrame(c ? "Edit challenge" : "New challenge", form(), preview(), c ? "Save changes" : "Add to the board"));
        bindChips(ed, function (k, val) {
          sync();
          if (k === "type") { s.type = val; if (val === "decode" && !s.enc) s.enc = "base64"; render(); return; }
          if (k === "enc") { s.enc = val; if (CHEF[val]) s.hint = CHEF[val][2]; render(); return; }
          if (k === "unit") s.unit = +val;
          if (k === "points") { s.points = +val; $("cf-points").value = val; }
          sync();
        });
        qa("input,textarea,select", q(".sd-form", ed)).forEach(function (el) { el.addEventListener("input", sync); el.addEventListener("change", sync); });
        bindTest();
        $("sd-cancel").addEventListener("click", closeEditor);
        $("sd-save").addEventListener("click", function () {
          sync();
          if (!s.title.trim()) { $("sd-msg").textContent = "Give it a title."; return; }
          if (!s.flag.trim()) { $("sd-msg").textContent = "Type the answer, so there is a flag."; return; }
          var p = assemble(s);
          if (s.id) p.id = s.id;
          $("sd-msg").textContent = "Saving…";
          rpc("api_teacher_ctf_save", { p: p }).then(function (r) {
            if (!r || !r.ok) throw new Error((r && r.error) || "Could not save.");
            closeEditor();
            load();
          }).catch(function (e) { $("sd-msg").textContent = e.message; });
        });
      }
      render();
    }
    function draw() {
      var list = data.challenges.filter(function (c) {
        if (filter.hidden ? c.active : !c.active) return false;
        if (filter.unit && String(c.unit) !== String(filter.unit)) return false;
        return !filter.q || (c.title + " " + c.flag + " " + c.body).toLowerCase().indexOf(filter.q) !== -1;
      });
      var solved = data.challenges.reduce(function (t, c) { return t + c.solves; }, 0);
      $("status").textContent = data.challenges.filter(function (c) { return c.active; }).length + " challenges on the board · " + solved + " solves";
      $("sd-count").textContent = list.length + " shown";
      $("sd-list").innerHTML = list.length ? '<div class="ct-grid">' + list.map(function (c) {
        return '<article class="ct-tile sd-tile">' + ctfTile(c, " · " + c.solves + " solved / " + c.tries + " tries") +
          '<code class="sd-flagc">' + esc(c.flag) + '</code><div class="sd-tbtns"><button class="btn" data-e="' + esc(c.id) + '">Edit</button>' +
          '<button class="btn" data-d="' + esc(c.id) + '">Duplicate</button>' + (c.active ? '<button class="btn" data-off="' + esc(c.id) + '">' + (c.builtin ? "Hide" : "Delete") + "</button>" :
            '<button class="btn" data-on="' + esc(c.id) + '">Show</button>') + "</div></article>";
      }).join("") + "</div>" : '<p class="tc-empty">' + (data.challenges.length ? "Nothing matches." : "No challenges yet. Press New challenge.") + "</p>";
      var byId = {};
      data.challenges.forEach(function (c) { byId[c.id] = c; });
      qa("[data-e]").forEach(function (b) { b.addEventListener("click", function () { edit(byId[b.getAttribute("data-e")]); }); });
      qa("[data-d]").forEach(function (b) {
        b.addEventListener("click", function () { var c = JSON.parse(JSON.stringify(byId[b.getAttribute("data-d")])); delete c.id; c.title += " (copy)"; c.builtin = false; edit(c); });
      });
      qa("[data-off]").forEach(function (b) {
        b.addEventListener("click", function () {
          if (!confirm("Take this challenge off the student board?")) return;
          rpc("api_teacher_ctf_delete", { p_id: b.getAttribute("data-off") }).then(load);
        });
      });
      qa("[data-on]").forEach(function (b) {
        b.addEventListener("click", function () { var c = byId[b.getAttribute("data-on")]; rpc("api_teacher_ctf_save", { p: { id: c.id, title: c.title, active: true } }).then(load); });
      });
      var ex = $("sd-extra");
      ex.hidden = false;
      ex.innerHTML = "<h3>Latest solves</h3>" + (data.solves.length ? '<table class="tc-table"><tr><th>When</th><th>Student</th><th>Challenge</th></tr>' +
        data.solves.slice(0, 40).map(function (s) { return "<tr><td>" + ago(s.at) + "</td><td>" + esc(s.email) + "</td><td>" + esc((byId[s.id] || {}).title || s.id) + "</td></tr>"; }).join("") +
        "</table>" : '<p class="tc-note">No flags captured yet.</p>');
    }
    function load() {
      return rpc("api_teacher_ctf").then(function (d) { if (d && d.ok) { data = d; draw(); } }, function (e) { $("status").textContent = "Could not load: " + e.message; });
    }
    $("sd-new").addEventListener("click", function () { edit(null); });
    load();
  }

  function ytId(u) {
    var m = /(?:youtu\.be\/|v=|embed\/|shorts\/|live\/)([A-Za-z0-9_-]{11})/.exec(u || "");
    return m ? m[1] : "";
  }
  function parseChapters(text) {
    var out = [];
    String(text || "").split("\n").forEach(function (l) {
      var m = l.match(/((?:\d{1,2}:)?\d{1,2}:\d{2})/);
      if (!m) return;
      var title = l.replace(m[0], "").replace(/^[\s\-–—:|.)\]]+|[\s\-–—:|(\[]+$/g, "").trim();
      if (title) out.push({ t: m[1], title: title });
    });
    return out;
  }
  function secs(t) { return String(t).split(":").reduce(function (a, x) { return a * 60 + (+x || 0); }, 0); }

  function seminars() {
    var data = [], filter = { q: "", pub: "" };
    shell();
    $("sd-filters").innerHTML = chips("pub", [["", "All"], ["1", "Published"], ["0", "Drafts"]], "");
    bindChips($("studio"), function (k, v) { filter.pub = v; draw(); });
    $("sd-q").addEventListener("input", function () { filter.q = this.value.toLowerCase(); draw(); });
    function poster(s, big) {
      var id = ytId(s.youtube), c = s.cover || (id ? "https://i.ytimg.com/vi/" + id + "/hqdefault.jpg" : "");
      return '<div class="sm-cover' + (big ? " big" : "") + (c ? " img" : "") + '"' + (c ? ' style="background-image:url(&quot;' + esc(c) + '&quot;)"' : "") + ">" +
        (c ? "" : '<span class="sm-ck">Seminar</span><span class="sm-ct">' + esc(s.title || "Untitled seminar") + '</span><span class="sm-cm">' +
          esc([s.level, s.minutes ? s.minutes + " min" : ""].filter(Boolean).join(" · ")) + "</span>") +
        '<span class="sm-badge">' + (+s.tickets ? s.tickets + " ticket" + (+s.tickets === 1 ? "" : "s") : "Free") + "</span></div>";
    }
    function edit(src) {
      var s = src ? JSON.parse(JSON.stringify(src)) : { title: "", youtube: "", summary: "", description: "", level: "", minutes: 0, tickets: 1, sort: 0, topics: "", cover: "",
        chapters: [], resources: [], published: false };
      s.chapters = s.chapters || []; s.resources = s.resources || [];
      function chRow(c) { return '<div class="sd-row"><input class="sd-time" data-k="t" value="' + esc(c.t) + '" placeholder="0:00"><input data-k="title" value="' + esc(c.title) + '" placeholder="Chapter title">' + rowTools() + "</div>"; }
      function reRow(r) { return '<div class="sd-row"><input data-k="title" value="' + esc(r.title) + '" placeholder="Label, e.g. Slides"><input data-k="url" value="' + esc(r.url) + '" placeholder="https://…">' + rowTools() + "</div>"; }
      function form() {
        var id = ytId(s.youtube), list = /[?&]list=/.test(s.youtube || "");
        return step(1, "The video", field("YouTube link", '<input id="sf-youtube" value="' + esc(s.youtube) + '" placeholder="https://youtu.be/… or a playlist link">', "upload it as Unlisted") +
            '<p class="sd-note" id="sf-ytnote">' + (id ? "&#10003; Video found." : list ? "&#10003; Playlist found." : s.youtube ? "That doesn't look like a YouTube link." : "") + "</p>") +
          step(2, "Describe it", field("Title", '<input id="sf-title" maxlength="200" value="' + esc(s.title) + '">') +
            field("One-line summary", '<input id="sf-summary" maxlength="200" value="' + esc(s.summary) + '">', "shown on the card") +
            field("Level", chips("level", [["", "Any"], ["Beginner", "Beginner"], ["Intermediate", "Intermediate"], ["Advanced", "Advanced"]], s.level)) +
            '<div class="sd-two">' + field("Length (minutes)", '<input id="sf-minutes" type="number" min="0" value="' + (s.minutes || "") + '">') +
            field("Topics", '<input id="sf-topics" value="' + esc(s.topics) + '" placeholder="malware, incident response">', "comma separated") + "</div>" +
            field("Full description", '<textarea id="sf-description" rows="5" placeholder="What it covers and who it is for. Start a line with - for a list.">' + esc(s.description) + "</textarea>")) +
          step(3, "Chapters", rows(s.chapters, chRow, "+ Add chapter", "ch") +
            '<details class="sd-adv"><summary>Paste the YouTube description instead</summary><textarea id="sf-paste" rows="4" placeholder="0:00 Introduction&#10;4:30 The phishing email"></textarea>' +
            '<button type="button" class="btn" id="sf-parse">Find the timestamps</button></details>', "Students can jump to each chapter.") +
          step(4, "Resources", rows(s.resources, reRow, "+ Add resource", "re"), "Slides, worksheets or links. Only students who unlocked the seminar see them.") +
          step(5, "Price and publish", field("Tickets to unlock", chips("tickets", [[0, "Free"], [1, "1"], [2, "2"], [3, "3"], [5, "5"]], s.tickets)) +
            '<div class="sd-two">' + field("Order", '<input id="sf-sort" type="number" value="' + (s.sort || 0) + '">', "lower comes first") +
            field("Cover image link", '<input id="sf-cover" value="' + esc(s.cover) + '" placeholder="optional">', "the video thumbnail is used otherwise") + "</div>" +
            '<label class="sd-switch"><input type="checkbox" id="sf-published"' + (s.published ? " checked" : "") + "> <span>Published: students can see it</span></label>");
      }
      function preview() {
        return '<div class="sm-card">' + poster(s) + '<div class="sm-cbody"><b>' + esc(s.title || "Untitled seminar") + "</b><span>" + esc(s.summary) + "</span><small>" +
          esc([s.level, s.minutes ? s.minutes + " min" : "", s.chapters.length ? s.chapters.length + " chapters" : ""].filter(Boolean).join(" · ")) + "</small></div></div>" +
          (s.chapters.length ? '<h4>Chapters</h4><ol class="sm-chapters">' + s.chapters.map(function (c) { return "<li><span>" + esc(c.t) + "</span> " + esc(c.title) + "</li>"; }).join("") + "</ol>" : "") +
          (s.published ? "" : '<p class="sd-note">Draft: only teachers can see it.</p>');
      }
      function readRows() {
        s.chapters = qa('[data-rows="ch"] .sd-row').map(function (r) { return { t: q('[data-k="t"]', r).value.trim(), title: q('[data-k="title"]', r).value.trim() }; });
        s.resources = qa('[data-rows="re"] .sd-row').map(function (r) { return { title: q('[data-k="title"]', r).value.trim(), url: q('[data-k="url"]', r).value.trim() }; });
      }
      function sync() {
        ["youtube", "title", "summary", "minutes", "topics", "description", "sort", "cover"].forEach(function (k) { var e = $("sf-" + k); if (e) s[k] = e.value; });
        s.minutes = +s.minutes || 0;
        s.published = $("sf-published").checked;
        readRows();
        var id = ytId(s.youtube), list = /[?&]list=/.test(s.youtube || "");
        $("sf-ytnote").innerHTML = id ? "&#10003; Video found." : list ? "&#10003; Playlist found." : s.youtube ? "That doesn't look like a YouTube link." : "";
        $("sd-preview").innerHTML = preview();
      }
      function render() {
        var ed = openEditor(editorFrame(src ? "Edit seminar" : "New seminar", form(), preview(), src ? "Save changes" : "Save seminar"));
        bindChips(ed, function (k, v) { sync(); if (k === "tickets") s.tickets = +v; else s[k] = v; sync(); });
        bindRows(ed, function () { sync(); render(); }, function (kind) { sync(); (kind === "ch" ? s.chapters : s.resources).push(kind === "ch" ? { t: "", title: "" } : { title: "", url: "" }); render(); },
          function (kind) { return kind === "ch" ? s.chapters : s.resources; }, readRows);
        qa("input,textarea,select", q(".sd-form", ed)).forEach(function (el) { if (el.id !== "sf-paste") el.addEventListener("input", sync); });
        $("sf-published").addEventListener("change", sync);
        $("sf-parse").addEventListener("click", function () {
          var found = parseChapters($("sf-paste").value);
          if (!found.length) { $("sd-msg").textContent = "No timestamps like 4:30 found."; return; }
          sync(); s.chapters = found.sort(function (a, b) { return secs(a.t) - secs(b.t); }); render();
          $("sd-msg").textContent = found.length + " chapters added.";
        });
        $("sd-cancel").addEventListener("click", closeEditor);
        $("sd-save").addEventListener("click", function () {
          sync();
          if (!s.title.trim()) { $("sd-msg").textContent = "Give it a title."; return; }
          var bad = s.resources.filter(function (r) { return r.url && !/^https:\/\//.test(r.url); });
          if (bad.length) { $("sd-msg").textContent = "Resource links must start with https://"; return; }
          var p = { title: s.title, youtube: s.youtube, summary: s.summary, description: s.description, level: s.level, minutes: s.minutes, tickets: +s.tickets,
            sort: +s.sort || 0, topics: s.topics, cover: s.cover, published: s.published,
            chapters: s.chapters.filter(function (c) { return /^(\d+:)?\d{1,2}:\d{2}$/.test(c.t) && c.title; }).sort(function (a, b) { return secs(a.t) - secs(b.t); }),
            resources: s.resources.filter(function (r) { return r.title && /^https:\/\//.test(r.url); }) };
          if (src && src.id) p.id = src.id;
          $("sd-msg").textContent = "Saving…";
          rpc("api_teacher_save_seminar", { p: p }).then(function (r) {
            if (!r || !r.ok) throw new Error((r && r.error) || "Could not save.");
            closeEditor(); load();
          }).catch(function (e) { $("sd-msg").textContent = e.message; });
        });
      }
      render();
    }
    function draw(d) {
      if (d) $("status").textContent = data.length + " seminar" + (data.length === 1 ? "" : "s") + " · " + d.subscribers + " active subscriber" + (d.subscribers === 1 ? "" : "s");
      var list = data.filter(function (s) {
        return (filter.pub === "" || String(+s.published) === filter.pub) && (!filter.q || (s.title + " " + s.summary).toLowerCase().indexOf(filter.q) !== -1);
      });
      $("sd-count").textContent = list.length + " shown";
      $("sd-list").innerHTML = list.length ? '<div class="sm-grid">' + list.map(function (s) {
        return '<article class="sm-card sd-tile">' + poster(s) + '<div class="sm-cbody"><b>' + esc(s.title) + "</b><small>" + (s.published ? "Published" : "Draft") +
          (s.minutes ? " · " + s.minutes + " min" : "") + " · " + (s.chapters || []).length + " chapters · " + s.owners + " owner" + (s.owners === 1 ? "" : "s") +
          (s.youtube ? "" : " · no video yet") + '</small><div class="sd-tbtns"><button class="btn" data-e="' + s.id + '">Edit</button><a class="btn" href="' +
          url("seminars.html?id=" + s.id) + '" target="_blank" rel="noopener">View</a><button class="btn" data-x="' + s.id + '">' + (s.owners ? "Hide" : "Delete") + "</button></div></div></article>";
      }).join("") + "</div>" : '<p class="tc-empty">' + (data.length ? "Nothing matches." : "No seminars yet. Press New seminar.") + "</p>";
      qa("[data-e]").forEach(function (b) { b.addEventListener("click", function () { edit(data.filter(function (s) { return s.id === +b.getAttribute("data-e"); })[0]); }); });
      qa("[data-x]").forEach(function (b) {
        b.addEventListener("click", function () {
          if (!confirm("Remove this seminar? If anyone has unlocked it, it is hidden instead, so they keep it.")) return;
          rpc("api_teacher_delete_seminar", { p_id: +b.getAttribute("data-x") }).then(function () { load(); });
        });
      });
    }
    function load() { return rpc("api_teacher_seminars").then(function (d) { data = d.seminars || []; draw(d); }, function (e) { $("status").textContent = "Could not load: " + e.message; }); }
    $("sd-new").addEventListener("click", function () { edit(null); });
    load();
  }

  function bindRows(root, rerender, add, listOf, readRows) {
    qa("[data-addrow]", root).forEach(function (b) { b.addEventListener("click", function () { add(b.getAttribute("data-addrow")); }); });
    qa(".sd-rows", root).forEach(function (box) {
      var kind = box.getAttribute("data-rows");
      qa(".sd-row", box).forEach(function (row, i) {
        var move = function (d) {
          readRows();
          var list = listOf(kind), j = i + d;
          if (j < 0 || j >= list.length) return;
          list.splice(j, 0, list.splice(i, 1)[0]);
          rerender();
        };
        var up = q("[data-up]", row), down = q("[data-down]", row), x = q("[data-x]", row);
        if (up) up.addEventListener("click", function () { move(-1); });
        if (down) down.addEventListener("click", function () { move(1); });
        if (x) x.addEventListener("click", function () { readRows(); listOf(kind).splice(i, 1); rerender(); });
      });
    });
  }

  var TOOLS = [["", "No tool"], ["linux", "Linux lab"], ["jupyter", "JupyterLab"], ["sqli", "SQL lab"], ["shop", "Hack the shop"], ["cyberchef", "CyberChef"], ["ctf", "CTF board"]];

  function bodyToSteps(body) {
    var parts = String(body || "").split(/^##\s+(?:\d+\.\s*)?(.+)$/m);
    var intro = parts[0].trim(), steps = [];
    for (var i = 1; i < parts.length; i += 2) {
      var text = parts[i + 1] || "", m = text.match(/```[^\n]*\n([\s\S]*?)\n?```/);
      steps.push({ title: parts[i].trim(), text: (m ? text.replace(m[0], "") : text).trim(), cmds: m ? m[1] : "" });
    }
    return { intro: intro, steps: steps };
  }
  function stepsToBody(intro, steps) {
    return [intro.trim()].concat(steps.filter(function (s) { return s.title || s.text || s.cmds; }).map(function (s, i) {
      return "## " + (i + 1) + ". " + (s.title || "Step") + (s.text ? "\n\n" + s.text.trim() : "") + (s.cmds.trim() ? "\n\n```\n" + s.cmds.trim() + "\n```" : "");
    })).filter(Boolean).join("\n\n");
  }
  function labPreviewHtml(item) {
    var parsed = bodyToSteps(item.body), tool = TOOLS.filter(function (t) { return t[0] === item.tool; })[0];
    return '<div class="lb-kicker">' + (item.kind === "notebook" ? "Notebook" : "Lab") + (item.unit ? " · Unit " + item.unit : "") + (item.topic ? " · " + esc(item.topic) : "") + "</div>" +
      "<h3>" + esc(item.title || "Untitled") + "</h3>" + (item.summary ? '<p class="sd-note">' + esc(item.summary) + "</p>" : "") +
      (item.kind === "notebook" ? notebookPreview(item.data) :
        (tool && tool[0] ? '<p><span class="btn dark">Open the ' + esc(tool[1]) + "</span></p>" : "") + paras(parsed.intro) +
        parsed.steps.map(function (s, i) {
          return '<div class="lb-step"><div class="lb-stephead"><span class="sd-n">' + (i + 1) + "</span><b>" + esc(s.title) + '</b><span class="lb-done">&#9744; Done</span></div>' +
            paras(s.text) + (s.cmds ? '<div class="lb-code"><pre>' + esc(s.cmds) + '</pre><span class="btn">Copy</span></div>' : "") + "</div>";
        }).join(""));
  }
  function notebookPreview(d) {
    var cells = (d && d.cells) || [];
    if (!cells.length) return '<p class="sd-note">No cells yet. Start from a template, import a file, or open the notebook editor after saving.</p>';
    var n = { md: 0, py: 0, sh: 0 };
    cells.forEach(function (c) { n[c.t] = (n[c.t] || 0) + 1; });
    return '<p class="sd-note">' + cells.length + " cells: " + n.md + " notes, " + (n.sh || 0) + " Linux, " + (n.py || 0) + " Python</p>" +
      '<ol class="sd-cells">' + cells.slice(0, 14).map(function (c) {
        var first = String(c.s || "").split("\n").filter(function (l) { return l.trim(); })[0] || "";
        return '<li class="k-' + c.t + '"><span>' + (c.t === "md" ? "Notes" : c.t === "sh" ? "Linux" : "Python") + "</span>" + esc(first.replace(/^#+\s*/, "").slice(0, 80)) + "</li>";
      }).join("") + (cells.length > 14 ? "<li>… " + (cells.length - 14) + " more</li>" : "") + "</ol>";
  }

  function labs() {
    var data = [], filter = { q: "", kind: "" };
    shell();
    $("sd-filters").innerHTML = chips("kind", [["", "All"], ["lab", "Labs"], ["notebook", "Notebooks"], ["draft", "Drafts"]], "");
    bindChips($("studio"), function (k, v) { filter.kind = v; draw(); });
    $("sd-q").addEventListener("input", function () { filter.q = this.value.toLowerCase(); draw(); });

    function chooser() {
      var cases = '<select id="lc-case"><option value="">Loading cases…</option></select>';
      var lessons = '<select id="lc-lesson">' + (H.T.order || []).map(function (a) { return '<option value="' + a + '">' + esc(a + " " + ((H.T.atoms[a] || {}).title || "")) + "</option>"; }).join("") + "</select>";
      var ed = openEditor('<div class="sd-head"><h2>What do you want to make?</h2><div class="tc-btns"><span class="tc-note" id="sd-msg"></span><button class="btn" id="sd-cancel">Cancel</button></div></div>' +
        '<div class="sd-choose">' +
        '<button class="sd-pick" data-pick="lab"><b>Step-by-step lab</b><span>Numbered steps with instructions and commands to copy, plus a button that opens the right tool.</span></button>' +
        '<button class="sd-pick" data-pick="blank"><b>Notebook from scratch</b><span>Notes, Linux and Python cells, written in the notebook editor.</span></button>' +
        '<div class="sd-pick"><b>Notebook from an incident runbook</b><span>Copy one of the five cases, then change it.</span>' + cases + '<button class="btn dark" data-pick="case">Use this case</button></div>' +
        '<div class="sd-pick"><b>Notebook from a lesson code book</b><span>Start from a lesson\'s runbook-style code book.</span>' + lessons + '<button class="btn dark" data-pick="book">Use this code book</button></div>' +
        '<button class="sd-pick" data-pick="import"><b>Import a .ipynb file</b><span>From JupyterLab, Google Colab or anywhere else.</span></button>' +
        '<input type="file" id="lc-file" accept=".ipynb,application/json" hidden></div>');
      fetch(url("assets/linux/cases/index.json")).then(function (r) { return r.json(); }).then(function (list) {
        $("lc-case").innerHTML = list.map(function (c) { return '<option value="' + esc(c.id) + '">' + esc(c.title + " (" + c.kicker + ")") + "</option>"; }).join("");
      }, function () { $("lc-case").innerHTML = '<option value="web01">The hacked web shop</option>'; });
      $("sd-cancel").addEventListener("click", closeEditor);
      qa("[data-pick]", ed).forEach(function (b) {
        b.addEventListener("click", function () {
          var k = b.getAttribute("data-pick");
          if (k === "lab") return edit({ kind: "lab", title: "", summary: "", unit: 0, topic: "", tool: "linux", body: "", published: false });
          if (k === "blank") return edit({ kind: "notebook", title: "", summary: "", unit: 0, topic: "", tool: "", data: { cells: [] }, published: false });
          if (k === "import") return $("lc-file").click();
          $("sd-msg").textContent = "Loading…";
          if (k === "case") {
            fetch(url("assets/linux/cases/" + $("lc-case").value + "/manifest.json")).then(function (r) { return r.json(); }).then(function (m) {
              edit({ kind: "notebook", title: m.title, summary: m.summary, unit: (m.units || [0])[0], topic: "", tool: "", published: false,
                data: { title: m.title, case: m.id, cells: m.template.map(function (c) { return { t: c.t, s: c.s }; }) } });
            }).catch(function (e) { $("sd-msg").textContent = e.message; });
          } else {
            var aid = $("lc-lesson").value, a = H.T.atoms[aid] || {};
            var path = String(a.solution || "").replace(/solution\.html$/, aid + "-student.ipynb");
            fetch(url(path)).then(function (r) { if (!r.ok) throw new Error("This lesson has no code book yet."); return r.json(); }).then(function (j) {
              edit({ kind: "notebook", title: aid + " " + (a.title || ""), summary: "Runbook-style code book for lesson " + aid + ".", unit: +aid.charAt(0), topic: aid.split(".").slice(0, 2).join("."),
                tool: "jupyter", published: false, data: { title: aid + " " + (a.title || ""), cells: cellsFromIpynb(j) } });
            }).catch(function (e) { $("sd-msg").textContent = e.message; });
          }
        });
      });
      $("lc-file").addEventListener("change", function () {
        var f = $("lc-file").files[0];
        if (!f) return;
        var r = new FileReader();
        r.onload = function () {
          try {
            var j = JSON.parse(r.result), t = f.name.replace(/\.ipynb$/, "");
            edit({ kind: "notebook", title: t, summary: "", unit: 0, topic: "", tool: "", published: false, data: { title: t, cells: cellsFromIpynb(j) } });
          } catch (e) { $("sd-msg").textContent = "That file isn't a notebook (.ipynb)."; }
        };
        r.readAsText(f);
      });
    }

    function cellsFromIpynb(j) {
      return (j.cells || []).map(function (c) {
        var s = Array.isArray(c.source) ? c.source.join("") : String(c.source || ""), m = /^%%(bash|sh)[^\n]*\n?/.exec(s);
        if (c.cell_type !== "code") return { t: "md", s: s };
        return m || (c.metadata && c.metadata.aayat === "sh") ? { t: "sh", s: m ? s.slice(m[0].length) : s } : { t: "py", s: s };
      }).filter(function (c) { return c.s.trim(); });
    }

    function edit(src) {
      var s = JSON.parse(JSON.stringify(src)), raw = false, parsed = bodyToSteps(s.body || "");
      var intro = parsed.intro, steps = parsed.steps.length ? parsed.steps : (s.kind === "lab" ? [{ title: "", text: "", cmds: "" }] : []);
      if (s.kind === "lab" && s.body && !parsed.steps.length) raw = true;
      function stepRow(st, i) {
        return '<div class="sd-row sd-lstep"><div class="sd-lhead"><span class="sd-n">' + (i + 1) + '</span><input data-k="title" value="' + esc(st.title) + '" placeholder="Step title, e.g. Look around">' + rowTools() + "</div>" +
          '<textarea data-k="text" rows="2" placeholder="What to do and why">' + esc(st.text) + "</textarea>" +
          '<textarea data-k="cmds" class="sd-mono" rows="2" placeholder="Commands to copy, one per line (optional)">' + esc(st.cmds) + "</textarea></div>";
      }
      function form() {
        var basics = field("Title", '<input id="lf-title" maxlength="200" value="' + esc(s.title) + '">') +
          field("Summary", '<input id="lf-summary" maxlength="300" value="' + esc(s.summary) + '">', "shown on the Labs page") +
          '<div class="sd-two">' + field("Unit", chips("unit", [[0, "Any"], [1, "1"], [2, "2"], [3, "3"], [4, "4"], [5, "5"]], s.unit)) +
          field("Topic", '<input id="lf-topic" maxlength="20" value="' + esc(s.topic) + '" placeholder="e.g. 3.2">', "optional") + "</div>";
        var out = step(1, "Basics", basics);
        if (s.kind === "lab") {
          out += step(2, "Tool", chips("tool", TOOLS, s.tool), "A big button on the lab opens this for the student.");
          out += step(3, "Steps", raw ? '<textarea id="lf-raw" class="sd-mono" rows="14">' + esc(stepsToBody(intro, steps)) + "</textarea>" +
              '<p class="sd-note">Text format: ## for each step, ``` lines around commands. <button type="button" class="btn" id="lf-mode">Back to step blocks</button></p>' :
            field("Before you start", '<textarea id="lf-intro" rows="2" placeholder="Optional: what this lab is about and what students need">' + esc(intro) + "</textarea>") +
              rows(steps, stepRow, "+ Add step", "st") + '<p class="sd-note"><button type="button" class="btn" id="lf-mode">Edit as text instead</button></p>',
            "Students tick each step off as they go.");
        } else {
          out += step(2, "Cells", notebookPreview(s.data) + '<p class="tc-btns">' + (s.id ? '<a class="btn dark" href="' + url("notebook.html?premium=" + s.id) + '" target="_blank" rel="noopener">Open in the notebook editor</a>' :
            '<span class="sd-note">Save first, then open it in the notebook editor to change cells.</span>') + '<button type="button" class="btn" id="lf-import">Replace with a .ipynb file</button>' +
            '<input type="file" id="lf-file" accept=".ipynb,application/json" hidden></p>');
        }
        out += step(s.kind === "lab" ? 4 : 3, "Publish", '<label class="sd-switch"><input type="checkbox" id="lf-published"' + (s.published ? " checked" : "") +
          "> <span>Published: Labs students can open it</span></label>");
        return out;
      }
      function readSteps() {
        if (raw) { var p = bodyToSteps($("lf-raw").value); intro = p.intro; steps = p.steps; return; }
        if ($("lf-intro")) intro = $("lf-intro").value;
        steps = qa('[data-rows="st"] .sd-row').map(function (r) { return { title: q('[data-k="title"]', r).value, text: q('[data-k="text"]', r).value, cmds: q('[data-k="cmds"]', r).value }; });
      }
      function sync() {
        s.title = $("lf-title").value; s.summary = $("lf-summary").value; s.topic = $("lf-topic").value; s.published = $("lf-published").checked;
        if (s.kind === "lab") { readSteps(); s.body = stepsToBody(intro, steps); }
        $("sd-preview").innerHTML = labPreviewHtml(s);
      }
      function render() {
        var ed = openEditor(editorFrame(s.id ? "Edit " + (s.kind === "lab" ? "lab" : "notebook") : "New " + (s.kind === "lab" ? "lab" : "notebook"), form(), labPreviewHtml(s),
          s.id ? "Save changes" : "Save"));
        bindChips(ed, function (k, v) { sync(); s[k] = k === "unit" ? +v : v; sync(); });
        if (s.kind === "lab" && !raw) bindRows(ed, function () { render(); }, function () { readSteps(); steps.push({ title: "", text: "", cmds: "" }); render(); },
          function () { return steps; }, readSteps);
        qa("input,textarea", q(".sd-form", ed)).forEach(function (el) { el.addEventListener("input", sync); });
        $("lf-published").addEventListener("change", sync);
        var mode = $("lf-mode");
        if (mode) mode.addEventListener("click", function () { sync(); raw = !raw; render(); });
        var imp = $("lf-import");
        if (imp) {
          imp.addEventListener("click", function () { $("lf-file").click(); });
          $("lf-file").addEventListener("change", function () {
            var f = $("lf-file").files[0], r = new FileReader();
            if (!f) return;
            r.onload = function () {
              try { s.data = { title: s.title || f.name, cells: cellsFromIpynb(JSON.parse(r.result)) }; sync(); render(); $("sd-msg").textContent = s.data.cells.length + " cells ready. Press Save."; }
              catch (e) { $("sd-msg").textContent = "That file isn't a notebook (.ipynb)."; }
            };
            r.readAsText(f);
          });
        }
        $("sd-cancel").addEventListener("click", closeEditor);
        $("sd-save").addEventListener("click", function () {
          sync();
          if (!s.title.trim()) { $("sd-msg").textContent = "Give it a title."; return; }
          var p = { kind: s.kind, title: s.title, unit: +s.unit || 0, topic: s.topic, tool: s.tool || "", summary: s.summary, published: s.published };
          if (s.kind === "lab") p.body = s.body;
          if (s.kind === "notebook" && s.data && (!s.id || s.dataChanged !== false)) p.data = s.data;
          if (s.id) p.id = s.id;
          $("sd-msg").textContent = "Saving…";
          rpc("api_teacher_premium_save", { p: p }).then(function (r) {
            if (!r || !r.ok) throw new Error((r && r.error) || "Could not save.");
            if (!s.id && s.kind === "notebook") { s.id = r.id; render(); $("sd-msg").textContent = "Saved. Open it in the notebook editor to change cells."; load(); return; }
            closeEditor(); load();
          }).catch(function (e) { $("sd-msg").textContent = e.message; });
        });
      }
      render();
    }
    function draw() {
      var list = data.filter(function (i) {
        if (filter.kind === "draft" ? i.published : filter.kind && i.kind !== filter.kind) return false;
        return !filter.q || (i.title + " " + i.summary).toLowerCase().indexOf(filter.q) !== -1;
      });
      $("status").textContent = data.length + " item" + (data.length === 1 ? "" : "s") + " stored in the database · only Labs owners can open them";
      $("sd-count").textContent = list.length + " shown";
      $("sd-list").innerHTML = list.length ? '<div class="lb-grid">' + list.map(function (i) {
        return '<article class="lb-card sd-tile"><small>' + (i.kind === "notebook" ? "Notebook" : "Lab") + (i.unit ? " · Unit " + i.unit : "") + (i.topic ? " · " + esc(i.topic) : "") +
          (i.published ? "" : ' · <b class="sd-draft">Draft</b>') + "</small><b>" + esc(i.title) + "</b><span>" + esc(i.summary) + '</span><div class="sd-tbtns">' +
          '<button class="btn" data-e="' + i.id + '">Edit</button>' + (i.kind === "notebook" ? '<a class="btn" href="' + url("notebook.html?premium=" + i.id) + '" target="_blank" rel="noopener">Cells</a>' : "") +
          '<a class="btn" href="' + url("labs.html?id=" + i.id) + '" target="_blank" rel="noopener">View</a><button class="btn" data-dup="' + i.id + '">Duplicate</button>' +
          '<button class="btn" data-x="' + i.id + '">Delete</button></div></article>';
      }).join("") + "</div>" : '<p class="tc-empty">' + (data.length ? "Nothing matches." : "Nothing here yet. Press New lab or notebook.") + "</p>";
      qa("[data-e]").forEach(function (b) {
        b.addEventListener("click", function () { rpc("api_premium_get", { p_id: +b.getAttribute("data-e") }).then(function (d) { if (d.ok) { d.item.dataChanged = false; edit(d.item); } }); });
      });
      qa("[data-dup]").forEach(function (b) {
        b.addEventListener("click", function () {
          rpc("api_premium_get", { p_id: +b.getAttribute("data-dup") }).then(function (d) {
            if (!d.ok) return;
            var c = d.item; delete c.id; c.title += " (copy)"; c.published = false; edit(c);
          });
        });
      });
      qa("[data-x]").forEach(function (b) {
        b.addEventListener("click", function () {
          if (!confirm("Delete this from the database? Students lose access to it.")) return;
          rpc("api_teacher_premium_delete", { p_id: +b.getAttribute("data-x") }).then(load);
        });
      });
    }
    function load() { return rpc("api_premium_list").then(function (d) { data = d.items || []; draw(); }, function (e) { $("status").textContent = "Could not load: " + e.message; }); }
    $("sd-new").addEventListener("click", chooser);
    load();
  }

  global.AayatStudio = {
    init: function (h) { H = h; $ = h.$; esc = h.esc; rpc = h.rpc; url = h.url; },
    ctf: ctf, seminars: seminars, labs: labs, bodyToSteps: bodyToSteps
  };
})(window);
