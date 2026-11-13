(function (global) {
  "use strict";
  var $ = function (id) { return document.getElementById(id); };
  var me = document.currentScript && document.currentScript.src;
  var ROOT = me ? me.replace(/assets\/theme\/workstation\.js.*$/, "") : "";
  var q = new URLSearchParams(location.search);
  var T = global.AayatTools;
  var wins = [], z = 10, seq = 0, caseId = "", caseTitle = "", caseMeta = null, files = null, access = null, trial = false, opened = false;
  var notes = [], unread = 0, chatLog = [];

  var SVG = {
    terminal: '<rect x="3" y="4" width="18" height="16" rx="2"/><path d="M7 9l3 3-3 3M12 15h5"/>',
    files: '<path d="M3 7a2 2 0 0 1 2-2h4l2 2h8a2 2 0 0 1 2 2v8a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/>',
    mail: '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3 7l9 6 9-6"/>',
    chat: '<path d="M4 5h16v11H9l-4 4v-4H4z"/><path d="M8 9h8M8 12h5"/>',
    notes: '<path d="M6 3h9l4 4v14H6z"/><path d="M15 3v4h4M9 12h7M9 15h7M9 18h4"/>',
    help: '<circle cx="12" cy="12" r="9"/><path d="M9.5 9.5a2.5 2.5 0 1 1 3.5 2.3c-.7.3-1 .8-1 1.7M12 17h.01"/>',
    text: '<path d="M6 3h9l4 4v14H6z"/><path d="M9 10h7M9 13h7M9 16h7"/>',
    packets: '<path d="M3 12h3l2-6 3 12 3-9 2 3h5"/>',
    events: '<rect x="4" y="3" width="16" height="18" rx="2"/><path d="M8 8h8M8 12h8M8 16h5"/>',
    siem: '<circle cx="10.5" cy="10.5" r="6"/><path d="M15 15l5 5"/>',
    alerts: '<path d="M6 16V11a6 6 0 0 1 12 0v5l2 2H4z"/><path d="M10 20h4"/>',
    shield: '<path d="M12 3l8 3v6c0 4.5-3.4 8.3-8 9-4.6-.7-8-4.5-8-9V6z"/>',
    flame: '<path d="M12 3c1 4 5 5 5 10a5 5 0 0 1-10 0c0-3 2-4 2-7 2 1 3 3 3 5"/>',
    gear: '<circle cx="12" cy="12" r="3"/><path d="M12 2v3M12 19v3M2 12h3M19 12h3M4.9 4.9l2.1 2.1M17 17l2.1 2.1M4.9 19.1L7 17M17 7l2.1-2.1"/>',
    cloud: '<path d="M7 18a4 4 0 0 1-.5-8 6 6 0 0 1 11.4 1.5A3.5 3.5 0 0 1 17.5 18z"/>',
    target: '<circle cx="12" cy="12" r="8"/><circle cx="12" cy="12" r="3"/><path d="M12 2v4M12 18v4M2 12h4M18 12h4"/>',
    scales: '<path d="M12 4v16M7 20h10M5 7h14M5 7l-3 7a3 3 0 0 0 6 0zM19 7l-3 7a3 3 0 0 0 6 0z"/>',
    folder: '<path d="M3 7a2 2 0 0 1 2-2h4l2 2h8a2 2 0 0 1 2 2v8a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/>',
    bell: '<path d="M6 16V11a6 6 0 0 1 12 0v5l2 2H4z"/><path d="M10 20h4"/>',
    net: '<path d="M2 9a15 15 0 0 1 20 0M5 12.5a10 10 0 0 1 14 0M8.5 16a5 5 0 0 1 7 0M12 19.5h.01"/>',
    power: '<path d="M12 3v9M6.3 6.3a8 8 0 1 0 11.4 0"/>',
    lock: '<rect x="5" y="11" width="14" height="10" rx="2"/><path d="M8 11V8a4 4 0 0 1 8 0v3"/>',
    user: '<circle cx="12" cy="8" r="4"/><path d="M4 21a8 8 0 0 1 16 0"/>',
    ticket: '<path d="M4 7a2 2 0 0 0 2-2h12a2 2 0 0 0 2 2v3a2 2 0 0 0 0 4v3a2 2 0 0 0-2 2H6a2 2 0 0 0-2-2v-3a2 2 0 0 0 0-4z"/><path d="M9 9h6M9 12h6M9 15h4"/>',
    rack: '<rect x="5" y="3" width="14" height="18" rx="1.5"/><path d="M5 8h14M5 13h14M5 18h14"/><path d="M8 5.5h.01M8 10.5h.01M8 15.5h.01"/>',
    rdp: '<rect x="3" y="4" width="18" height="12" rx="1.5"/><path d="M8 20h8M12 16v4M9 9l2 2 4-4"/>'
  };
  var TINT = { terminal: "#2b2f36", files: "#d89a2b", mail: "#2d74c4", chat: "#3a9d6a", notes: "#c9a227", help: "#5d6b7a", text: "#7a8796",
    packets: "#1f7a8c", events: "#6a4c93", siem: "#c0392b", alerts: "#d35400", shield: "#2c5f8a", flame: "#b03a2e", gear: "#4a5a6a", cloud: "#2980b9", target: "#7d3c98", scales: "#5b6c3a", folder: "#d89a2b", ticket: "#16a085", rack: "#34495e", rdp: "#1e5aa8" };
  var GROUP_ICON = { "SOC analyst": "shield", "Incident responder": "flame", "Security engineer": "gear", "Cloud and DevSecOps": "cloud", "Penetration tester": "target", "Governance and risk": "scales" };
  var TOOL_ICON = { packets: "packets", events: "events", siem: "siem", alerts: "alerts", email: "mail", logsearch: "siem", timeline: "events", proctree: "events" };

  function esc(s) { return String(s == null ? "" : s).replace(/[&<>"']/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]; }); }
  function icon(name, size) {
    var n = SVG[name] ? name : "text", t = TINT[n] || "#4a5a6a";
    return '<span class="ws-gl" style="--g:' + t + ';' + (size ? "--s:" + size + "px" : "") + '"><svg viewBox="0 0 24 24" aria-hidden="true">' + SVG[n] + "</svg></span>";
  }
  function glyph(name) { return '<svg class="ws-sv" viewBox="0 0 24 24" aria-hidden="true">' + (SVG[name] || "") + "</svg>"; }
  function store(k, v) { try { if (v === undefined) return localStorage.getItem(k); localStorage.setItem(k, v); } catch (e) { return null; } }
  function rpc(fn, args) {
    var P = global.AayatProgress;
    return (P ? P.neon() : Promise.resolve(null)).then(function (db) {
      if (!db) throw new Error("not connected");
      return db.rpc(fn, args || {}, { attempts: 1 });
    });
  }
  function email() { return global.Identity ? global.Identity.getEmail() : ""; }
  function base(n) { return String(n || "").replace(/^.*\//, ""); }
  function hostName() { return caseId ? (caseId.replace(/^sem-/, "").replace(/^[a-z]\d*-|^t-/, "").split("-")[0] + "-ws") : "analyst-ws"; }

  function programs() {
    var list = [
      { id: "terminal", title: "Terminal", icon: "terminal", group: "System", open: function () { terminal(); } },
      { id: "files", title: "Files", icon: "files", group: "System", open: function () { browser(); } },
      { id: "mail", title: "Mail", icon: "mail", group: "System", open: function () { mail(); } },
      { id: "chat", title: "Team chat", icon: "chat", group: "System", open: function () { chat(); } },
      { id: "notes", title: "Notes", icon: "notes", group: "System", open: function () { notepad(); } },
      { id: "help", title: "How to use this desktop", icon: "help", group: "System", open: function () { help(); } }
    ];
    (global.AayatDeskApps || []).forEach(function (a) { list.push({ id: a.id, title: a.title, icon: a.icon, group: "Workplace", open: function (st) { a.open(st); } }); });
    if (T) T.list().filter(function (d) { return d.console; }).forEach(function (d) {
      list.push({ id: "tool-" + d.id, title: d.title, icon: TOOL_ICON[d.id] || GROUP_ICON[d.group] || "gear", group: d.group || "Viewers", open: function (st) { tool(d, st); } });
    });
    return list;
  }
  function prog(id) { return programs().filter(function (p) { return p.id === id; })[0]; }

  function focus(w) {
    w.el.style.zIndex = ++z;
    wins.forEach(function (x) { x.el.classList.toggle("on", x === w); if (x.btn) x.btn.classList.toggle("on", x === w && !x.min); });
  }
  function win(title, ico, build, size) {
    var n = ++seq, el = document.createElement("section"), desk = $("ws-desk"), dw = desk.clientWidth, dh = desk.clientHeight;
    var w = { el: el, title: title, min: false, onclose: null };
    var width = Math.min((size && size.w) || 720, dw - 20), height = Math.min((size && size.h) || 460, dh - 20);
    el.className = "ws-win ws-open";
    el.setAttribute("role", "dialog");
    el.setAttribute("aria-label", title);
    el.style.width = width + "px";
    el.style.height = height + "px";
    el.style.left = Math.max(6, Math.min(dw - width - 6, 120 + (n % 7) * 30)) + "px";
    el.style.top = Math.max(6, Math.min(dh - height - 6, 18 + (n % 7) * 26)) + "px";
    el.innerHTML = '<header class="ws-title">' + icon(ico, 18) + '<b></b><span class="ws-btns"><button type="button" data-w="min" aria-label="Minimise" title="Minimise">' +
      '<i class="m"></i></button><button type="button" data-w="max" aria-label="Maximise" title="Maximise"><i class="x"></i></button>' +
      '<button type="button" data-w="close" aria-label="Close" title="Close"><i class="c"></i></button></span></header><div class="ws-body"></div>';
    el.querySelector(".ws-title b").textContent = title;
    desk.appendChild(el);
    setTimeout(function () { el.classList.remove("ws-open"); }, 180);
    var b = document.createElement("button");
    b.type = "button";
    b.className = "ws-task";
    b.innerHTML = icon(ico, 18) + "<span></span>";
    b.lastChild.textContent = title;
    b.title = title;
    b.addEventListener("click", function () {
      if (w.min) { w.min = false; el.hidden = false; focus(w); }
      else if (el.classList.contains("on")) { w.min = true; el.hidden = true; b.classList.remove("on"); }
      else focus(w);
    });
    $("ws-tasks").appendChild(b);
    w.btn = b;
    wins.push(w);
    el.addEventListener("mousedown", function () { focus(w); });
    el.querySelector('[data-w="close"]').addEventListener("click", function () { close(w); });
    el.querySelector('[data-w="min"]').addEventListener("click", function (e) { e.stopPropagation(); w.min = true; el.hidden = true; b.classList.remove("on"); });
    el.querySelector('[data-w="max"]').addEventListener("click", function () { snap(el, el.classList.contains("max") ? "" : "max"); });
    drag(el, el.querySelector(".ws-title"));
    focus(w);
    w.body = el.querySelector(".ws-body");
    build(w);
    return w;
  }
  function snap(el, how) {
    el.classList.remove("max", "left", "right");
    if (how) el.classList.add(how);
  }
  function close(w) {
    if (w.onclose) w.onclose();
    w.el.remove();
    if (w.btn) w.btn.remove();
    wins = wins.filter(function (x) { return x !== w; });
  }
  function drag(el, handle) {
    var sx, sy, ox, oy, on = false, zone = "";
    var hint = $("ws-snap");
    handle.addEventListener("pointerdown", function (e) {
      if (e.target.closest("button")) return;
      if (el.classList.contains("max") || el.classList.contains("left") || el.classList.contains("right")) {
        var r = el.getBoundingClientRect();
        snap(el, "");
        el.style.left = Math.max(0, e.clientX - $("ws-desk").getBoundingClientRect().left - r.width / 4) + "px";
      }
      on = true; sx = e.clientX; sy = e.clientY; ox = el.offsetLeft; oy = el.offsetTop;
      handle.setPointerCapture(e.pointerId);
    });
    handle.addEventListener("pointermove", function (e) {
      if (!on) return;
      var d = $("ws-desk"), r = d.getBoundingClientRect();
      el.style.left = Math.max(-el.offsetWidth + 80, Math.min(d.clientWidth - 80, ox + e.clientX - sx)) + "px";
      el.style.top = Math.max(0, Math.min(d.clientHeight - 30, oy + e.clientY - sy)) + "px";
      zone = e.clientX - r.left < 12 ? "left" : r.right - e.clientX < 12 ? "right" : e.clientY - r.top < 8 ? "max" : "";
      hint.className = "ws-snap" + (zone ? " " + zone : "");
    });
    handle.addEventListener("pointerup", function () { if (on && zone) snap(el, zone); on = false; zone = ""; hint.className = "ws-snap"; });
    handle.addEventListener("dblclick", function (e) { if (!e.target.closest("button")) snap(el, el.classList.contains("max") ? "" : "max"); });
  }

  function loadFiles() {
    if (!caseId || !global.AayatVM) return Promise.resolve({});
    if (!files) files = allowed().then(function (ok) {
      if (!ok) return {};
      return global.AayatVM.caseFiles(caseId).then(function (all) {
        var out = {};
        Object.keys(all).forEach(function (k) { if (typeof all[k] === "string" && all[k].indexOf("\u0000") < 0) out[k] = all[k]; });
        return out;
      });
    }).catch(function () { files = null; return {}; });
    return files;
  }
  function allowed() {
    if (!caseId || caseId === "trial") return Promise.resolve(true);
    if (access) return access;
    var P = global.Paywall, sem = /^sem-/.test(caseId);
    if ((global.APCYBER_PAYWALL || {}).enabled === false) return (access = Promise.resolve(true));
    if (!sem && P && P.has("labs")) return (access = Promise.resolve(true));
    var tutor = rpc("api_whoami").then(function (w) { return !!(w && w.teacher); }, function () { return false; });
    var labs = tutor.then(function (t) {
      if (t) return true;
      if (sem) return false;
      return email() ? rpc("api_my_access").then(function (a) { return !!(a && a.labs); }, function () { return false; }) : false;
    });
    access = labs.then(function (yes) {
      if (yes || !global.AayatVM) return yes;
      return global.AayatVM.manifest(caseId).then(function (m) {
        if (m.free) return true;
        return m.seminarId ? rpc("api_seminar_lab", { p_id: +m.seminarId }).then(function (r) { return !!(r && r.access); }) : false;
      }).catch(function () { return false; });
    });
    return access;
  }

  function terminal(dir) {
    var host = hostName();
    win("Terminal: analyst@" + host, "terminal", function (w) {
      var cwd = dir || ("/root" + (caseId ? "/case" : "")), hist = [], hi = 0, busy = false;
      w.body.classList.add("ws-term");
      w.body.innerHTML = '<pre class="ws-out" aria-live="polite"></pre><form class="ws-line"><span class="ws-ps"></span><input aria-label="Command" autocomplete="off" spellcheck="false"></form>';
      var out = w.body.querySelector(".ws-out"), input = w.body.querySelector("input"), ps = w.body.querySelector(".ws-ps");
      function promptText() { return "analyst@" + host + ":" + cwd.replace(/^\/root/, "~") + "$ "; }
      function prompt() { ps.innerHTML = '<span class="u">analyst@' + esc(host) + '</span>:<span class="p">' + esc(cwd.replace(/^\/root/, "~")) + "</span>$ "; }
      function print(t) { out.textContent += t; if (out.textContent.length > 200000) out.textContent = out.textContent.slice(-150000); w.body.scrollTop = w.body.scrollHeight; }
      prompt();
      print(caseId ? "Case: " + caseTitle + ". The evidence is in ~/case.\n" : "Plain Linux. Open a case from the taskbar to get its evidence and network.\n");
      print("Every terminal shares one Linux computer but keeps its own folder. Type help for ideas.\n\n");
      w.body.addEventListener("click", function () { if (!getSelection().toString()) input.focus(); });
      input.focus();
      input.addEventListener("keydown", function (e) {
        if (e.key === "ArrowUp") { if (hi > 0) input.value = hist[--hi] || ""; e.preventDefault(); }
        else if (e.key === "ArrowDown") { input.value = hist[++hi] || ""; if (hi > hist.length) hi = hist.length; e.preventDefault(); }
        else if (e.key === "c" && e.ctrlKey && busy) { global.AayatVM.stop(); e.preventDefault(); }
        else if (e.key === "l" && e.ctrlKey) { out.textContent = ""; e.preventDefault(); }
      });
      w.body.querySelector("form").addEventListener("submit", function (e) {
        e.preventDefault();
        var cmd = input.value;
        input.value = "";
        if (cmd.trim()) { hist.push(cmd); hi = hist.length; }
        print(promptText() + cmd + "\n");
        if (!cmd.trim()) return;
        if (/^\s*clear\s*$/.test(cmd)) { out.textContent = ""; return; }
        if (/^\s*exit\s*$/.test(cmd)) { close(w); return; }
        if (/^\s*help\s*$/.test(cmd)) { print("Try: ls -l, cat FILE, grep -i WORD FILE, sha256sum *, ps, ss, nmap -sn 10.20.0.0/24, curl http://HOST/, dig NAME, tshark -r capture.pcap\nCtrl+C stops a command, Ctrl+L clears, arrows recall history, exit closes the window.\n"); return; }
        if (!global.AayatVM) { print("Linux didn't load. Reload the page.\n"); return; }
        busy = true;
        input.disabled = true;
        var waiting = global.AayatVM.busy() ? setTimeout(function () { print("(waiting for another terminal's command to finish)\n"); }, 600) : null;
        ready(function (t) { print(t + "\n"); }).then(function () {
          return global.AayatVM.shell('cd "' + cwd.replace(/"/g, "") + '" 2>/dev/null || cd /root\n' + cmd + "\nprintf '\\n__WS_PWD__%s' \"$(pwd)\"");
        }).then(function (r) {
          clearTimeout(waiting);
          var m = /\n?__WS_PWD__(.*)$/.exec(r.out), text = m ? r.out.slice(0, m.index) : r.out;
          if (m) cwd = m[1] || cwd;
          if (text) print(text + (/\n$/.test(text) ? "" : "\n"));
        }).catch(function (err) { clearTimeout(waiting); print(String(err && err.message || err) + "\n"); }).then(function () {
          busy = false; input.disabled = false; prompt(); input.focus();
        });
      });
    }, { w: 720, h: 430 });
  }
  var readying = null;
  function ready(status) {
    if (!readying) readying = (caseId ? allowed().then(function (ok) {
      if (!ok) {
        status(/^sem-/.test(caseId) ? "This lab comes with its seminar, so this desktop runs plain Linux instead. Unlock it at " + ROOT + "seminars.html" : "This case comes with Labs, so this desktop runs plain Linux instead. Get Labs at " + ROOT + "store.html#labs");
        return global.AayatVM.boot(status);
      }
      return global.AayatVM.installCase(caseId, status);
    }) : global.AayatVM.boot(status)).then(function () { status(""); }).catch(function (e) { readying = null; throw e; });
    return readying;
  }

  function kindOf(name, text) {
    var b = base(name).toLowerCase();
    if (/^#aayat-capture/.test(text)) return { app: "tool-packets", label: "Packet capture", ico: "packets" };
    if (/\.jsonl$/.test(b) && /"EventID"/.test(text.slice(0, 2000))) return { app: "tool-events", label: "Event log", ico: "events" };
    if (/\.eml$/.test(b)) return { app: "mail", label: "Email message", ico: "mail" };
    if (/alert.*\.json$/.test(b)) return { app: "tool-alerts", label: "Alert queue", ico: "alerts" };
    if (/tabletop.*\.json$/.test(b)) return { app: "tool-tabletop", label: "Tabletop exercise", ico: "flame" };
    if (/certin.*\.json$/.test(b)) return { app: "tool-certin", label: "CERT-In case", ico: "scales" };
    if (/^ai.*\.json$/.test(b)) return { app: "tool-aisec", label: "AI assistant setup", ico: "scales" };
    if (/audit.*\.json$|polic.*\.json$/.test(b)) return { app: "tool-cloudiam", label: "Cloud audit or policy", ico: "cloud" };
    if (/\.(log|txt|csv|json|md|conf|ya?ml|tf|sh|py|patch)$|^dockerfile/.test(b)) return { app: "text", label: ({ log: "Log file", csv: "Spreadsheet (CSV)", json: "JSON data" })[(b.match(/\.([a-z]+)$/) || [])[1]] || "Text file", ico: "text" };
    return { app: "text", label: "File", ico: "text" };
  }
  function openFile(name, how) {
    loadFiles().then(function (fs) {
      var text = fs[name];
      if (text == null) return;
      var k = how || kindOf(name, text).app;
      if (k === "text") return viewer(name, text);
      if (k === "mail") return mail(name);
      if (k === "hex") return tool(T.get("hex"), { file: name });
      var p = prog(k);
      if (p) p.open({ file: name });
    });
  }
  function viewer(name, text) {
    win(base(name) + " - Text viewer", "text", function (w) {
      var lines = text.split("\n");
      w.body.innerHTML = '<div class="ws-vbar"><input type="search" placeholder="Find (Enter)" aria-label="Find"><small></small></div><div class="ws-viewer"><pre class="ws-ln"></pre><pre class="ws-tx"></pre></div>';
      var ln = w.body.querySelector(".ws-ln"), tx = w.body.querySelector(".ws-tx"), find = w.body.querySelector("input"), info = w.body.querySelector("small");
      var shown = lines.slice(0, 5000);
      ln.textContent = shown.map(function (_, i) { return i + 1; }).join("\n");
      tx.textContent = shown.join("\n");
      info.textContent = lines.length + " lines" + (lines.length > 5000 ? ", first 5000 shown" : "") + " · " + name;
      find.addEventListener("keydown", function (e) {
        if (e.key !== "Enter") return;
        var v = find.value.toLowerCase();
        if (!v) { tx.textContent = shown.join("\n"); return; }
        var hits = 0;
        tx.innerHTML = shown.map(function (l) { var i = l.toLowerCase().indexOf(v); if (i < 0) return esc(l); hits++; return esc(l.slice(0, i)) + "<mark>" + esc(l.slice(i, i + v.length)) + "</mark>" + esc(l.slice(i + v.length)); }).join("\n");
        info.textContent = hits + " matching lines";
        var m = tx.querySelector("mark");
        if (m) m.scrollIntoView({ block: "center" });
      });
    }, { w: 780, h: 480 });
  }

  function browser(start) {
    win("Files" + (caseTitle ? ": " + caseTitle : ""), "files", function (w) {
      w.body.innerHTML = '<div class="ws-fm"><div class="ws-crumbs"></div><div class="ws-fgrid"><nav class="ws-tree" aria-label="Folders"></nav><div class="ws-flist" role="list"></div></div><div class="ws-fstat"></div></div>';
      var tree = w.body.querySelector(".ws-tree"), list = w.body.querySelector(".ws-flist"), crumbs = w.body.querySelector(".ws-crumbs"), stat = w.body.querySelector(".ws-fstat");
      if (!caseId) { list.innerHTML = '<p class="ws-empty">No case is open. Pick one from Case on the taskbar.</p>'; return; }
      list.innerHTML = '<p class="ws-empty">Loading…</p>';
      loadFiles().then(function (fs) {
        var names = Object.keys(fs).sort();
        if (!names.length) { list.innerHTML = '<p class="ws-empty">' + (/^sem-/.test(caseId) ? "These files come with this seminar." : "These files come with Labs.") + "</p>"; return; }
        var dirs = {};
        names.forEach(function (n) { var parts = n.split("/"); for (var i = 1; i < parts.length; i++) dirs[parts.slice(0, i).join("/")] = 1; });
        var cur = start && dirs[start] ? start : "";
        function draw() {
          tree.innerHTML = ['""'].concat(Object.keys(dirs).sort().map(function (d) { return JSON.stringify(d); })).map(function (j) {
            var d = JSON.parse(j), depth = d ? d.split("/").length : 0;
            return '<button type="button" data-d="' + esc(d) + '" class="' + (d === cur ? "on" : "") + '" style="padding-left:' + (6 + depth * 12) + 'px">' + glyph("folder") + esc(d ? base(d) : "~/case") + "</button>";
          }).join("");
          crumbs.innerHTML = '<button type="button" data-d="">~/case</button>' + (cur ? cur.split("/").map(function (p, i, a) { return ' / <button type="button" data-d="' + esc(a.slice(0, i + 1).join("/")) + '">' + esc(p) + "</button>"; }).join("") : "");
          var pre = cur ? cur + "/" : "", sub = Object.keys(dirs).filter(function (d) { return d.indexOf(pre) === 0 && d.slice(pre.length).indexOf("/") < 0 && d !== cur; }).sort();
          var here = names.filter(function (n) { return n.indexOf(pre) === 0 && n.slice(pre.length).indexOf("/") < 0; });
          list.innerHTML = '<div class="ws-frow ws-fhead"><span>Name</span><span>Type</span><span>Size</span></div>' +
            sub.map(function (d) { return '<button type="button" class="ws-frow" data-d="' + esc(d) + '" role="listitem"><span>' + icon("folder", 18) + esc(base(d)) + "</span><span>Folder</span><span></span></button>"; }).join("") +
            here.map(function (n) { var k = kindOf(n, fs[n]); return '<button type="button" class="ws-frow" data-f="' + esc(n) + '" role="listitem"><span>' + icon(k.ico, 18) + esc(base(n)) + "</span><span>" + esc(k.label) + "</span><span>" + size(fs[n].length) + "</span></button>"; }).join("");
          stat.textContent = sub.length + " folders, " + here.length + " files · double-click to open, right-click for more";
        }
        w.body.addEventListener("click", function (e) {
          var d = e.target.closest("[data-d]");
          if (d && w.body.contains(d) && (d.closest(".ws-tree") || d.closest(".ws-crumbs"))) { cur = d.getAttribute("data-d"); draw(); return; }
          var r = e.target.closest(".ws-frow");
          list.querySelectorAll(".ws-frow").forEach(function (x) { x.classList.toggle("on", x === r); });
        });
        list.addEventListener("dblclick", function (e) {
          var r = e.target.closest(".ws-frow");
          if (!r) return;
          if (r.hasAttribute("data-d")) { cur = r.getAttribute("data-d"); draw(); } else if (r.hasAttribute("data-f")) openFile(r.getAttribute("data-f"));
        });
        list.addEventListener("keydown", function (e) {
          var r = e.target.closest(".ws-frow");
          if (e.key !== "Enter" || !r) return;
          if (r.hasAttribute("data-d")) { cur = r.getAttribute("data-d"); draw(); } else if (r.hasAttribute("data-f")) openFile(r.getAttribute("data-f"));
        });
        list.addEventListener("contextmenu", function (e) {
          var r = e.target.closest(".ws-frow[data-f]");
          if (!r) return;
          e.preventDefault();
          var n = r.getAttribute("data-f"), k = kindOf(n, fs[n]);
          menu(e, [["Open in " + (k.app === "text" ? "Text viewer" : (prog(k.app) || { title: "Mail" }).title), function () { openFile(n); }],
            ["Open with Text viewer", function () { openFile(n, "text"); }],
            ["Hashes and strings", function () { openFile(n, "hex"); }],
            ["Open a terminal here", function () { terminal("/root/case" + (n.indexOf("/") > 0 ? "/" + n.slice(0, n.lastIndexOf("/")) : "")); }],
            ["Copy path", function () { try { navigator.clipboard.writeText("~/case/" + n); } catch (err) {} toast("Copied", "~/case/" + n); }]]);
        });
        draw();
      });
    }, { w: 820, h: 480 });
  }
  function size(n) { return n < 1024 ? n + " B" : n < 1048576 ? (n / 1024).toFixed(1) + " KB" : (n / 1048576).toFixed(1) + " MB"; }

  function parseMail(text) {
    var cut = text.replace(/\r/g, "").indexOf("\n\n"), head = cut < 0 ? text : text.slice(0, cut), body = cut < 0 ? "" : text.slice(cut + 2), h = {};
    head.replace(/\n[ \t]+/g, " ").split("\n").forEach(function (l) { var m = /^([A-Za-z-]+):\s*(.*)$/.exec(l); if (m && !h[m[1].toLowerCase()]) h[m[1].toLowerCase()] = m[2]; });
    var links = [], plain = "", html = "";
    var bnd = /boundary="?([^";\s]+)"?/i.exec(h["content-type"] || "");
    var parts = bnd ? body.split("--" + bnd[1]).map(function (p) {
      p = p.replace(/^\r?\n/, "");
      var c = p.indexOf("\n\n");
      return c < 0 ? null : { type: (/content-type:\s*([^;\n]+)/i.exec(p.slice(0, c)) || [])[1] || "text/plain", body: p.slice(c + 2) };
    }).filter(function (p) { return p && !/^--\s*$/.test(p.body.trim()); }) : [{ type: h["content-type"] || "text/plain", body: body }];
    parts.forEach(function (p) {
      if (/html/i.test(p.type) || /<[a-z][\s\S]*>/i.test(p.body)) html = html || p.body;
      else if (/text\/plain/i.test(p.type)) plain = plain || p.body;
    });
    if (html) {
      html.replace(/<a\s[^>]*href="([^"]+)"[^>]*>([\s\S]*?)<\/a>/gi, function (_, href, label) { links.push({ href: href, label: label.replace(/<[^>]+>/g, "").trim() }); });
      if (!plain) plain = html.replace(/<br\s*\/?>/gi, "\n").replace(/<\/p>/gi, "\n\n").replace(/<[^>]+>/g, "").replace(/&nbsp;/g, " ").replace(/&amp;/g, "&");
    }
    return { h: h, body: (plain || body).trim(), links: links, raw: text };
  }
  function mail(pick) {
    win("Mail" + (caseTitle ? ": " + caseTitle : ""), "mail", function (w) {
      w.body.innerHTML = '<div class="ws-mail"><div class="ws-mlist" role="list"></div><article class="ws-mread"><p class="ws-empty">Pick a message.</p></article></div>';
      var listEl = w.body.querySelector(".ws-mlist"), read = w.body.querySelector(".ws-mread");
      loadFiles().then(function (fs) {
        var msgs = Object.keys(fs).filter(function (n) { return /\.eml$/i.test(n); }).map(function (n) { var m = parseMail(fs[n]); m.file = n; m.t = Date.parse(m.h.date || "") || 0; return m; })
          .sort(function (a, b) { return b.t - a.t; });
        if (!msgs.length) { listEl.innerHTML = '<p class="ws-empty">No email in this case.</p>'; return; }
        var seen = JSON.parse(store("ws-mail-seen-" + caseId) || "{}");
        function show(m) {
          seen[m.file] = 1;
          store("ws-mail-seen-" + caseId, JSON.stringify(seen));
          listEl.querySelectorAll(".ws-mrow").forEach(function (r) { r.classList.toggle("on", r.getAttribute("data-f") === m.file); if (seen[r.getAttribute("data-f")]) r.classList.remove("new"); });
          read.innerHTML = '<h3></h3><dl><dt>From</dt><dd data-k="from"></dd><dt>To</dt><dd data-k="to"></dd><dt>Date</dt><dd data-k="date"></dd>' + (m.h["reply-to"] ? '<dt>Reply-To</dt><dd data-k="reply-to"></dd>' : "") + "</dl>" +
            '<div class="ws-mact"><button type="button" class="btn" data-a="orig">Show original</button><button type="button" class="btn" data-a="triage">Report as phishing</button><button type="button" class="btn" data-a="auth">Check SPF, DKIM, DMARC</button></div>' +
            '<div class="ws-mbody"></div>' + (m.links.length ? '<div class="ws-mlinks"><b>Links in this message</b><ul>' + m.links.map(function (l) { return "<li><span>" + esc(l.label) + "</span> &rarr; <code>" + esc(l.href) + "</code></li>"; }).join("") + "</ul><small>Hover a link to see where it really goes. Here they never open.</small></div>" : "") +
            '<pre class="ws-morig" hidden></pre>';
          read.querySelector("h3").textContent = m.h.subject || "(no subject)";
          ["from", "to", "date", "reply-to"].forEach(function (k) { var e = read.querySelector('[data-k="' + k + '"]'); if (e) e.textContent = m.h[k] || ""; });
          read.querySelector(".ws-mbody").textContent = m.body;
          read.querySelector(".ws-morig").textContent = m.raw;
          read.querySelector('[data-a="orig"]').addEventListener("click", function () { var o = read.querySelector(".ws-morig"); o.hidden = !o.hidden; this.textContent = o.hidden ? "Show original" : "Hide original"; });
          read.querySelector('[data-a="triage"]').addEventListener("click", function () { var p = prog("tool-email"); if (p) p.open({ files: [m.file] }); });
          read.querySelector('[data-a="auth"]').addEventListener("click", function () { var p = prog("tool-mailauth"); if (p) p.open({ file: m.file }); });
        }
        listEl.innerHTML = msgs.map(function (m) {
          return '<button type="button" class="ws-mrow' + (seen[m.file] ? "" : " new") + '" data-f="' + esc(m.file) + '" role="listitem"><b>' + esc((m.h.from || "").replace(/<[^>]*>/, "").replace(/"/g, "").trim() || m.h.from || "") + "</b><span>" + esc(m.h.subject || "") + "</span><small>" + esc(m.t ? new Date(m.t).toISOString().slice(0, 16).replace("T", " ") : "") + "</small></button>";
        }).join("");
        listEl.addEventListener("click", function (e) { var r = e.target.closest(".ws-mrow"); if (r) show(msgs.filter(function (m) { return m.file === r.getAttribute("data-f"); })[0]); });
        show(msgs.filter(function (m) { return m.file === pick; })[0] || msgs[0]);
      });
    }, { w: 900, h: 520 });
  }

  function briefing() {
    var lead = { name: "Priya Shah", role: "SOC lead" }, out = [];
    if (!caseId) { out.push([lead, "Morning. No case is open yet: pick one from Case on the taskbar and I'll brief you."]); return out; }
    var m = caseMeta || {};
    out.push([lead, "New case for you: " + (caseTitle || caseId) + "."]);
    if (m.summary) out.push([lead, m.summary]);
    out.push([lead, "Evidence is in ~/case (open Files on the desktop). Hash it before you touch it, write down what you check, and keep facts apart from guesses."]);
    out.push([{ name: "On-call bot", role: "automation" }, "Case loaded on " + hostName() + ". Terminal, Files and every program on the Start menu can read it."]);
    if (trial) out.push([lead, "You're on the trial desk: this sample case only. The full Hacker Room has every case and the seminars that teach each program."]);
    return out;
  }
  function chat() {
    var open = wins.filter(function (x) { return x.chat; })[0];
    if (open) { if (open.min) { open.min = false; open.el.hidden = false; } focus(open); unread = 0; badge(); return; }
    var w = win("Team chat: #soc", "chat", function (w) {
      w.body.innerHTML = '<div class="ws-chat"><aside><b>Channels</b><button type="button" class="on"># soc</button><button type="button" disabled># ir-war-room</button><button type="button" disabled># it-helpdesk</button><b>People</b>' +
        '<span><i class="ok"></i>Priya Shah</span><span><i class="ok"></i>Arjun (IT)</span><span><i></i>Legal</span></aside><div class="ws-cmain"><div class="ws-clog" aria-live="polite"></div>' +
        '<form class="ws-csend"><input placeholder="Message #soc" aria-label="Message"><button class="btn dark">Send</button></form></div></div>';
      var log = w.body.querySelector(".ws-clog");
      function add(who, text, mine) {
        var d = document.createElement("div");
        d.className = "ws-msg" + (mine ? " me" : "");
        d.innerHTML = '<span class="ws-av">' + esc((who.name || "?").charAt(0)) + '</span><div><b></b> <small></small><p></p></div>';
        d.querySelector("b").textContent = who.name;
        d.querySelector("small").textContent = (who.role ? who.role + " · " : "") + new Date().toTimeString().slice(0, 5);
        d.querySelector("p").textContent = text;
        log.appendChild(d);
        log.scrollTop = log.scrollHeight;
      }
      chatLog.forEach(function (x) { add(x[0], x[1], x[2]); });
      w.addMsg = add;
      w.body.querySelector("form").addEventListener("submit", function (e) {
        e.preventDefault();
        var inp = w.body.querySelector("input"), v = inp.value.trim();
        if (!v) return;
        inp.value = "";
        chatLog.push([{ name: "You" }, v, true]);
        add({ name: "You" }, v, true);
        var r = /escalat|urgent|now|stop/i.test(v) ? "Understood. Put the ask first and say what you haven't done. I'll read it as soon as it's in the report builder."
          : /done|finished|report/i.test(v) ? "Thanks. Send me the note when it's in the report builder; I'll review it."
          : /help|stuck|hint/i.test(v) ? "Start from the README and the hashes, then follow the times. What's the first thing that looks out of place?"
          : "Noted. Keep going, and write down each command you run.";
        setTimeout(function () { var lead = { name: "Priya Shah", role: "SOC lead" }; chatLog.push([lead, r]); add(lead, r); }, 1400);
      });
    }, { w: 760, h: 460 });
    w.chat = true;
    unread = 0;
    badge();
  }
  function post(who, text) {
    chatLog.push([who, text]);
    var w = wins.filter(function (x) { return x.chat; })[0];
    if (w && w.addMsg) w.addMsg(who, text);
    if (!w || w.min || !w.el.classList.contains("on")) { unread++; badge(); }
  }
  function badge() { var b = $("ws-bell-n"); if (b) { b.textContent = unread || ""; b.hidden = !unread; } }
  function toast(title, text, onclick) {
    notes.unshift({ title: title, text: text, t: new Date() });
    var t = document.createElement("div");
    t.className = "ws-toast";
    t.innerHTML = "<b></b><p></p>";
    t.querySelector("b").textContent = title;
    t.querySelector("p").textContent = text;
    t.addEventListener("click", function () { t.remove(); if (onclick) onclick(); });
    $("ws-app").appendChild(t);
    setTimeout(function () { t.classList.add("out"); setTimeout(function () { t.remove(); }, 400); }, 5200);
    var c = $("ws-center");
    if (c && !c.hidden) center();
  }
  function center() {
    var c = $("ws-center");
    c.innerHTML = "<h4>Notifications</h4>" + (notes.length ? notes.map(function (n) { return '<div class="ws-note"><b>' + esc(n.title) + "</b><p>" + esc(n.text) + "</p><small>" + n.t.toTimeString().slice(0, 5) + "</small></div>"; }).join("") : '<p class="ws-empty">Nothing new.</p>') +
      '<button type="button" class="btn" id="ws-clear">Clear all</button>';
    $("ws-clear").addEventListener("click", function () { notes = []; center(); });
  }

  function notepad() {
    win("Notes", "notes", function (w) {
      var key = "ws-notes-" + (caseId || "plain");
      w.body.innerHTML = '<textarea class="ws-notes" spellcheck="true" placeholder="Your notes for this case: what you checked, what you found, what you don\'t know yet. They stay in this browser."></textarea><div class="ws-row"><button type="button" class="btn" data-n="dl">Download</button> <small>Saved as you type</small></div>';
      var t = w.body.querySelector("textarea");
      t.value = store(key) || "";
      t.addEventListener("input", function () { store(key, t.value); });
      w.body.querySelector('[data-n="dl"]').addEventListener("click", function () {
        var a = document.createElement("a");
        a.href = URL.createObjectURL(new Blob([t.value], { type: "text/plain" }));
        a.download = (caseId || "notes") + "-notes.txt";
        a.click();
      });
    }, { w: 480, h: 400 });
  }
  function help() {
    win("How to use this desktop", "help", function (w) {
      w.body.innerHTML = '<div class="ws-help"><h3>The Hacker Room</h3><p>This is an analyst\'s computer, in your browser. Nothing you do can reach the internet or harm your own computer.</p>' +
        "<ul><li><b>Team chat</b>: your SOC lead hands you the case. Read the briefing first.</li>" +
        "<li><b>Files</b>: the evidence. Double-click a file to open it in the right program: captures in the Packet viewer, event logs in the Event viewer, emails in Mail. Right-click for hashes, a terminal in that folder, and more.</li>" +
        "<li><b>Terminal</b>: a real Linux computer. Open as many as you like.</li>" +
        "<li><b>Start</b>: every program, grouped by job. <b>Case</b> on the taskbar switches case.</li>" +
        "<li>Drag a window to the left or right edge to fill half the screen, or to the top to fill it. Right-click the desktop for more.</li>" +
        "<li><b>Notes</b> are saved in this browser for each case.</li></ul></div>";
    }, { w: 560, h: 380 });
  }
  function tool(d, state) {
    if (!d) return;
    win(d.title + (state && state.file ? ": " + base(state.file) : ""), TOOL_ICON[d.id] || GROUP_ICON[d.group] || "gear", function (w) {
      w.body.classList.add("ws-app-body");
      w.body.innerHTML = '<nav class="ws-menubar"><span data-m="file">File</span><span data-m="view">View</span><span data-m="help">Help</span></nav>';
      var host = document.createElement("div");
      host.className = "ws-tool";
      w.body.appendChild(host);
      var bar = document.createElement("div");
      bar.className = "ws-status";
      bar.textContent = d.title + " · " + (caseTitle || "no case open") + (state && state.file ? " · " + state.file : "") + (d.group ? " · " + d.group : "");
      w.body.appendChild(bar);
      var zoom = 1;
      w.body.querySelector(".ws-menubar").addEventListener("click", function (e) {
        var m = e.target.getAttribute("data-m");
        if (m === "file") menu(e, [["Open evidence in Files", function () { browser(); }], ["Open a terminal", function () { terminal(); }], null, ["Close", function () { close(w); }]]);
        else if (m === "view") menu(e, [["Bigger text", function () { zoom = Math.min(1.4, zoom + 0.1); host.style.fontSize = zoom * 100 + "%"; }], ["Smaller text", function () { zoom = Math.max(0.8, zoom - 0.1); host.style.fontSize = zoom * 100 + "%"; }],
          ["Fill the screen", function () { snap(w.el, "max"); }], ["Left half", function () { snap(w.el, "left"); }], ["Right half", function () { snap(w.el, "right"); }]]);
        else if (m === "help") menu(e, [["How to use this desktop", help], ["Ask the SOC lead", chat]]);
      });
      var key = "ws-tool-" + (caseId || "plain") + "-" + d.id + (state && state.file ? "-" + state.file : ""), saved = null;
      try { saved = JSON.parse(store(key) || "null"); } catch (e) { saved = null; }
      d.mount(host, { state: state || {}, saved: saved, files: loadFiles, remember: function (v) { try { store(key, JSON.stringify(v)); } catch (e) { return; } } });
    }, { w: 880, h: 540 });
  }

  function menu(e, items) {
    var m = $("ws-ctx");
    m.innerHTML = items.map(function (it, i) { return it ? '<button type="button" data-i="' + i + '">' + esc(it[0]) + "</button>" : "<hr>"; }).join("");
    var r = $("ws-app").getBoundingClientRect();
    m.hidden = false;
    m.style.left = Math.min(e.clientX - r.left, r.width - m.offsetWidth - 4) + "px";
    m.style.top = Math.min(e.clientY - r.top, r.height - m.offsetHeight - 4) + "px";
    m.querySelectorAll("[data-i]").forEach(function (b) { b.addEventListener("click", function () { m.hidden = true; items[+b.getAttribute("data-i")][1](); }); });
  }

  function startMenu() {
    var m = $("ws-start-menu"), list = programs(), groups = {};
    list.forEach(function (p) { (groups[p.group] = groups[p.group] || []).push(p); });
    var order = ["System", "Workplace"].concat(T ? T.groups : []).concat(Object.keys(groups)), seen = {};
    m.innerHTML = '<div class="ws-who">' + icon("user", 32) + "<div><b>analyst</b><small>" + esc(email() || (trial ? "Trial desk" : "Hacker Room")) + '</small></div><button type="button" id="ws-lockbtn" title="Lock">' + glyph("lock") + "</button></div>" +
      '<input id="ws-find" placeholder="Search programs" aria-label="Search programs">' + order.filter(function (g) { if (seen[g] || !groups[g]) return false; seen[g] = 1; return true; }).map(function (g) {
        return '<div class="ws-grp"><h4>' + esc(g) + "</h4>" + groups[g].map(function (p) { return '<button type="button" data-p="' + esc(p.id) + '">' + icon(p.icon, 20) + "<span>" + esc(p.title) + "</span></button>"; }).join("") + "</div>";
      }).join("");
    m.querySelectorAll("[data-p]").forEach(function (b) {
      b.addEventListener("click", function () { m.hidden = true; prog(b.getAttribute("data-p")).open(); });
    });
    $("ws-find").addEventListener("input", function () {
      var v = this.value.toLowerCase();
      m.querySelectorAll("[data-p]").forEach(function (b) { b.hidden = v && b.textContent.toLowerCase().indexOf(v) < 0; });
    });
    $("ws-find").addEventListener("keydown", function (e) {
      if (e.key !== "Enter") return;
      var b = Array.prototype.filter.call(m.querySelectorAll("[data-p]"), function (x) { return !x.hidden; })[0];
      if (b) b.click();
    });
    $("ws-lockbtn").addEventListener("click", function () { m.hidden = true; lockScreen(); });
  }
  function icons() {
    var pick = ["files", "terminal", "mail", "chat", "tickets", "rack", "rdp", "tool-packets", "tool-events", "tool-siem", "notes", "help"], list = programs();
    $("ws-icons").innerHTML = pick.map(function (id) { return list.filter(function (p) { return p.id === id; })[0]; }).filter(Boolean).map(function (p) {
      return '<button type="button" class="ws-icon" data-p="' + esc(p.id) + '">' + icon(p.icon, 44) + "<span>" + esc(p.title) + "</span></button>";
    }).join("");
    $("ws-icons").querySelectorAll("[data-p]").forEach(function (b) {
      b.addEventListener("dblclick", function () { prog(b.getAttribute("data-p")).open(); });
      b.addEventListener("keydown", function (e) { if (e.key === "Enter") prog(b.getAttribute("data-p")).open(); });
      b.addEventListener("click", function () { $("ws-icons").querySelectorAll(".ws-icon").forEach(function (x) { x.classList.toggle("sel", x === b); }); });
    });
  }
  function pins() {
    var p = document.createElement("div");
    p.className = "ws-pins";
    p.innerHTML = ["files", "terminal", "mail", "chat", "tickets", "tool-packets", "tool-siem"].map(function (id) {
      var x = prog(id);
      return x ? '<button type="button" data-p="' + id + '" title="' + esc(x.title) + '" aria-label="' + esc(x.title) + '">' + icon(x.icon, 22) + "</button>" : "";
    }).join("");
    p.addEventListener("click", function (e) { var b = e.target.closest("[data-p]"); if (b) prog(b.getAttribute("data-p")).open(); });
    $("ws-start").after(p);
  }
  function tray() {
    var t = document.createElement("div");
    t.className = "ws-tray";
    t.innerHTML = '<span class="ws-net" id="ws-net" title="Not connected to a case network">' + glyph("net") + '</span><button type="button" class="ws-bellb" id="ws-bell" title="Notifications" aria-label="Notifications">' + glyph("bell") +
      '<i id="ws-bell-n" hidden></i></button>';
    $("ws-clock").before(t);
    var c = document.createElement("div");
    c.id = "ws-center";
    c.className = "ws-center";
    c.hidden = true;
    $("ws-app").appendChild(c);
    $("ws-bell").addEventListener("click", function (e) { e.stopPropagation(); c.hidden = !c.hidden; if (!c.hidden) center(); });
  }

  function caseMenu() {
    var sel = $("ws-case");
    sel.innerHTML = '<option value="">Plain Linux, no case</option>';
    if (!global.AayatVM) return;
    fetch(ROOT + "assets/linux/cases/index.json").then(function (r) { return r.json(); }).then(function (list) {
      list = [{ id: "trial", title: "Trial case: Lantern Cafe" }].concat(list.filter(function (c) { return !/--/.test(c.id); }));
      sel.innerHTML += list.map(function (c) {
        var off = trial && c.id !== "trial" && !c.free;
        return '<option value="' + esc(c.id) + '"' + (off ? " disabled" : "") + ">" + esc((c.seminarId ? "Seminar lab: " : "") + c.title + (off ? " (with Seminars or Labs)" : "")) + "</option>";
      }).join("");
      var want = (q.get("case") || (trial ? "trial" : "")).replace(/[^a-z0-9-]/g, "");
      if (trial && want !== "trial" && !list.some(function (c) { return c.id === want && c.free; })) want = "trial";
      if (want && list.some(function (c) { return c.id === want; })) { sel.value = want; useCase(want, list); }
      else { chatLog = briefing().map(function (x) { return [x[0], x[1]]; }); }
      sel.addEventListener("change", function () { useCase(sel.value, list); });
    }).catch(function () {});
  }
  function useCase(id, list) {
    if (id === caseId && opened) return;
    opened = true;
    wins.slice().forEach(close);
    caseId = id;
    caseTitle = id ? ((list.filter(function (c) { return c.id === id; })[0] || {}).title || id) : "";
    caseMeta = null;
    files = null; access = null; readying = null;
    $("ws-casename").textContent = caseTitle || "No case";
    var net = $("ws-net");
    if (net) { net.classList.toggle("on", !!id); net.title = id ? "Connected to the case network: " + caseTitle : "Not connected to a case network"; }
    var u = new URL(location.href);
    if (id) u.searchParams.set("case", id); else u.searchParams.delete("case");
    history.replaceState(null, "", u.toString());
    chatLog = [];
    var go = id && global.AayatVM ? global.AayatVM.manifest(id).then(function (m) { caseMeta = m; }, function () {}) : Promise.resolve();
    go.then(function () {
      var lines = briefing();
      lines.forEach(function (x, i) { setTimeout(function () { post(x[0], x[1]); }, 500 + i * 900); });
      if (id) setTimeout(function () { toast("Priya Shah in #soc", "New case for you: " + caseTitle, chat); }, 700);
    });
    if (id) browser();
  }

  function clock() {
    var d = new Date();
    $("ws-clock").innerHTML = "<b>" + d.toISOString().slice(11, 16) + " UTC</b><small>" + d.toISOString().slice(0, 10) + "</small>";
    var l = $("ws-lock-time");
    if (l) { l.textContent = d.toTimeString().slice(0, 5); $("ws-lock-date").textContent = d.toLocaleDateString(undefined, { weekday: "long", day: "numeric", month: "long" }); }
  }
  function lockScreen(first) {
    var l = document.createElement("div");
    l.className = "ws-lockscr";
    l.innerHTML = '<div class="ws-lock-clock"><b id="ws-lock-time"></b><span id="ws-lock-date"></span></div><div class="ws-lock-card">' + icon("user", 72) + "<b>analyst</b><small>" +
      esc(trial ? "Trial desk" : email() || "Hacker Room") + '</small><button type="button" class="ws-signbtn">Sign in</button><small class="ws-lock-hint">Press Enter</small></div>';
    $("ws-app").appendChild(l);
    clock();
    var b = l.querySelector(".ws-signbtn");
    function enter() {
      l.classList.add("out");
      document.removeEventListener("keydown", key);
      setTimeout(function () { l.remove(); if (first) first(); }, 350);
    }
    function key(e) { if (e.key === "Enter" && document.activeElement && !/INPUT|TEXTAREA/.test(document.activeElement.tagName)) { e.preventDefault(); enter(); } }
    b.addEventListener("click", enter);
    document.addEventListener("keydown", key);
    b.focus({ preventScroll: true });
  }

  function deskAllowed() {
    var want = (q.get("case") || "").replace(/[^a-z0-9-]/g, "");
    return (T ? T.access() : Promise.resolve(false)).then(function (ok) {
      if (ok || !want || !global.AayatVM) return ok;
      return global.AayatVM.manifest(want).then(function (m) {
        if (m.free) return true;
        return m.seminarId ? rpc("api_seminar_lab", { p_id: +m.seminarId }).then(function (r) { return !!(r && r.access); }) : false;
      }).catch(function () { return false; });
    });
  }
  function lock() {
    var app = $("ws-app"), g = document.createElement("div");
    app.classList.add("ws-locked");
    g.className = "ws-gate";
    g.setAttribute("role", "dialog");
    g.setAttribute("aria-label", "Welcome to the Hacker Room");
    g.innerHTML = '<div class="tl-lock ws-offer"><b>Welcome to the Hacker Room</b>' +
      "<p>An analyst's computer in your browser: a team chat with your SOC lead, mail, files, Linux terminals, and the programs security teams use every day, each as a window.</p>" +
      "<p><b>Try it free</b> on a small sample case. The real cases, the seminars that teach every program and the certificates come with Seminars or Labs.</p>" +
      '<p><button type="button" class="btn dark" id="ws-trial">Try it free</button> <a class="btn" href="' + ROOT + 'careers.html">Career training</a> ' +
      '<a class="btn" href="' + ROOT + 'store.html">Store</a></p>' +
      (email() ? "<p><small>Signed in as " + esc(email()) + ".</small></p>" : '<p><small>Bought it already? <button type="button" class="ws-link" id="ws-signin">Sign in</button></small></p>') + "</div>";
    app.appendChild(g);
    $("ws-trial").addEventListener("click", startTrial);
    var b = $("ws-signin");
    if (b) b.addEventListener("click", function () { if (global.Identity) global.Identity.open({}, function () { location.reload(); }); });
  }
  function startTrial() {
    var app = $("ws-app"), g = app.querySelector(".ws-gate");
    if (g) g.remove();
    app.classList.remove("ws-locked");
    trial = true;
    var r = document.createElement("a");
    r.className = "ws-trial";
    r.href = ROOT + "store.html";
    r.textContent = "Trial · get the full Hacker Room";
    $("ws-tasks").parentNode.insertBefore(r, $("ws-tasks").nextSibling);
    openDesk();
  }

  function start() {
    if (!$("ws-app")) return;
    deskAllowed().then(function (ok) { if (ok) openDesk(); else if (q.get("trial")) startTrial(); else lock(); });
  }
  function openDesk() {
    var app = $("ws-app");
    ["ws-ctx", "ws-snap"].forEach(function (id, i) { var d = document.createElement("div"); d.id = id; d.className = i ? "ws-snap" : "ws-ctx"; if (!i) d.hidden = true; app.appendChild(d); });
    pins();
    tray();
    $("ws-start").innerHTML = glyph("shield") + "<span>Start</span>";
    $("ws-start").addEventListener("click", function (e) { e.stopPropagation(); var m = $("ws-start-menu"); m.hidden = !m.hidden; if (!m.hidden) $("ws-find").focus(); });
    document.addEventListener("click", function (e) {
      var m = $("ws-start-menu"); if (!m.hidden && !m.contains(e.target)) m.hidden = true;
      var c = $("ws-ctx"); if (c && !c.hidden && !c.contains(e.target)) c.hidden = true;
      var n = $("ws-center"); if (n && !n.hidden && !n.contains(e.target)) n.hidden = true;
    });
    document.addEventListener("keydown", function (e) { if (e.key === "Escape") { $("ws-start-menu").hidden = true; $("ws-ctx").hidden = true; $("ws-center").hidden = true; } });
    $("ws-desk").addEventListener("contextmenu", function (e) {
      if (e.target.closest(".ws-win")) return;
      e.preventDefault();
      menu(e, [["Open a terminal", function () { terminal(); }], ["Open Files", function () { browser(); }], ["Open Mail", function () { mail(); }], ["Team chat", chat], null,
        ["Change wallpaper", function () { var n = (+(store("ws-wall") || 0) + 1) % 4; store("ws-wall", String(n)); $("ws-desk").setAttribute("data-wall", n); }],
        ["Close all windows", function () { wins.slice().forEach(close); }], null, ["How to use this desktop", help]]);
    });
    $("ws-desk").setAttribute("data-wall", store("ws-wall") || "0");
    startMenu();
    icons();
    clock();
    setInterval(clock, 30000);
    lockScreen(function () {
      caseMenu();
      if (!q.get("case") && !trial) setTimeout(help, 400);
    });
  }
  global.AayatDesk = {
    win: win, files: loadFiles, open: function (n, how) { openFile(n, how); }, toast: toast, post: post, icon: icon, glyph: glyph, esc: esc, base: base, store: store,
    terminal: function (dir) { terminal(dir); }, caseId: function () { return caseId; }, caseTitle: function () { return caseTitle; }
  };
  if (document.readyState === "complete") start();
  else global.addEventListener("load", start);
})(window);
