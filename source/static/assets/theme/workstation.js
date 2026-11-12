(function (global) {
  "use strict";
  var $ = function (id) { return document.getElementById(id); };
  var me = document.currentScript && document.currentScript.src;
  var ROOT = me ? me.replace(/assets\/theme\/workstation\.js.*$/, "") : "";
  var q = new URLSearchParams(location.search);
  var T = global.AayatTools;
  var wins = [], z = 10, seq = 0, caseId = "", caseTitle = "", files = null, access = null, notes = "";
  var SYS = [
    { id: "terminal", title: "Terminal", icon: ">_", group: "System", open: terminal },
    { id: "files", title: "Files", icon: "▤", group: "System", open: browser },
    { id: "notes", title: "Notes", icon: "✎", group: "System", open: notepad },
    { id: "help", title: "How to use this desktop", icon: "?", group: "System", open: help }
  ];

  function esc(s) { return String(s == null ? "" : s).replace(/[&<>"']/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]; }); }
  function store(k, v) { try { if (v === undefined) return localStorage.getItem(k); localStorage.setItem(k, v); } catch (e) { return null; } }
  function rpc(fn, args) {
    var P = global.AayatProgress;
    return (P ? P.neon() : Promise.resolve(null)).then(function (db) {
      if (!db) throw new Error("not connected");
      return db.rpc(fn, args || {}, { attempts: 1 });
    });
  }
  function email() { return global.Identity ? global.Identity.getEmail() : ""; }

  function programs() {
    var list = SYS.slice();
    if (T) T.list().filter(function (d) { return d.console; }).forEach(function (d) {
      list.push({ id: "tool-" + d.id, title: d.title, icon: (d.title || "?").charAt(0), group: d.group || "Viewers", open: function () { tool(d); } });
    });
    return list;
  }

  function focus(w) {
    w.el.style.zIndex = ++z;
    wins.forEach(function (x) { x.el.classList.toggle("on", x === w); if (x.btn) x.btn.classList.toggle("on", x === w && !x.min); });
  }
  function win(title, icon, build, size) {
    var n = ++seq, el = document.createElement("section"), desk = $("ws-desk"), dw = desk.clientWidth, dh = desk.clientHeight;
    var w = { el: el, title: title, min: false };
    var width = Math.min((size && size.w) || 720, dw - 20), height = Math.min((size && size.h) || 460, dh - 20);
    el.className = "ws-win";
    el.setAttribute("role", "dialog");
    el.setAttribute("aria-label", title);
    el.style.width = width + "px";
    el.style.height = height + "px";
    el.style.left = Math.max(6, Math.min(dw - width - 6, 40 + (n % 8) * 28)) + "px";
    el.style.top = Math.max(6, Math.min(dh - height - 6, 24 + (n % 8) * 24)) + "px";
    el.innerHTML = '<header class="ws-title"><span class="ws-ico"></span><b></b><span class="ws-btns"><button type="button" data-w="min" aria-label="Minimise">_</button>' +
      '<button type="button" data-w="max" aria-label="Maximise">□</button><button type="button" data-w="close" aria-label="Close">×</button></span></header><div class="ws-body"></div>';
    el.querySelector(".ws-ico").textContent = icon;
    el.querySelector("b").textContent = title;
    desk.appendChild(el);
    var b = document.createElement("button");
    b.type = "button";
    b.className = "ws-task";
    b.textContent = title;
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
    el.querySelector('[data-w="max"]').addEventListener("click", function () { el.classList.toggle("max"); });
    drag(el, el.querySelector(".ws-title"));
    focus(w);
    w.body = el.querySelector(".ws-body");
    if (w.onclose === undefined) w.onclose = null;
    build(w);
    return w;
  }
  function close(w) {
    if (w.onclose) w.onclose();
    w.el.remove();
    if (w.btn) w.btn.remove();
    wins = wins.filter(function (x) { return x !== w; });
  }
  function drag(el, handle) {
    var sx, sy, ox, oy, on = false;
    handle.addEventListener("pointerdown", function (e) {
      if (e.target.closest("button") || el.classList.contains("max")) return;
      on = true; sx = e.clientX; sy = e.clientY; ox = el.offsetLeft; oy = el.offsetTop;
      handle.setPointerCapture(e.pointerId);
    });
    handle.addEventListener("pointermove", function (e) {
      if (!on) return;
      var d = $("ws-desk");
      el.style.left = Math.max(-el.offsetWidth + 80, Math.min(d.clientWidth - 80, ox + e.clientX - sx)) + "px";
      el.style.top = Math.max(0, Math.min(d.clientHeight - 30, oy + e.clientY - sy)) + "px";
    });
    handle.addEventListener("pointerup", function () { on = false; });
    handle.addEventListener("dblclick", function () { el.classList.toggle("max"); });
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
    if (!caseId) return Promise.resolve(true);
    if (access) return access;
    var P = global.Paywall;
    if (P && P.has("labs")) return (access = Promise.resolve(true));
    var tutor = rpc("api_whoami").then(function (w) { return !!(w && w.teacher); }, function () { return false; });
    var labs = tutor.then(function (t) {
      if (t) { $("ws-casename").textContent = caseTitle + " (tutor)"; return true; }
      return email() ? rpc("api_my_access").then(function (a) { return !!(a && a.labs); }, function () { return false; }) : false;
    });
    access = labs.then(function (yes) {
      if (yes || !global.AayatVM) return yes;
      return global.AayatVM.manifest(caseId).then(function (m) {
        return m.seminarId ? rpc("api_seminar_lab", { p_id: +m.seminarId }).then(function (r) { return !!(r && r.access); }) : false;
      }).catch(function () { return false; });
    });
    return access;
  }

  function terminal() {
    var host = caseId ? (caseId.replace(/^sem-/, "").split("-")[0] + "-ws") : "analyst-ws";
    win("Terminal: root@" + host, ">_", function (w) {
      var cwd = "/root" + (caseId ? "/case" : ""), hist = [], hi = 0, busy = false;
      w.body.classList.add("ws-term");
      w.body.innerHTML = '<pre class="ws-out" aria-live="polite"></pre><form class="ws-line"><span class="ws-ps"></span><input aria-label="Command" autocomplete="off" spellcheck="false"></form>';
      var out = w.body.querySelector(".ws-out"), input = w.body.querySelector("input"), ps = w.body.querySelector(".ws-ps");
      function prompt() { ps.textContent = "root@" + host + ":" + cwd.replace(/^\/root/, "~") + "# "; }
      function print(t) { out.textContent += t; if (out.textContent.length > 200000) out.textContent = out.textContent.slice(-150000); w.body.scrollTop = w.body.scrollHeight; }
      prompt();
      print(caseId ? "Case: " + caseTitle + ". The evidence is in ~/case.\n" : "Plain Linux. Open a case from the taskbar to get its evidence and network.\n");
      print("Every terminal shares one Linux computer but keeps its own folder. Type help for ideas.\n\n");
      w.body.addEventListener("click", function () { input.focus(); });
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
        print(ps.textContent + cmd + "\n");
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
    }, { w: 700, h: 420 });
  }
  var readying = null;
  function ready(status) {
    if (!readying) readying = (caseId ? allowed().then(function (ok) {
      if (!ok) {
        status("This case comes with Labs or its seminar, so this desktop runs plain Linux instead. " + "Get Labs at " + ROOT + "store.html#labs");
        return global.AayatVM.boot(status);
      }
      return global.AayatVM.installCase(caseId, status);
    }) : global.AayatVM.boot(status)).then(function () { status(""); }).catch(function (e) { readying = null; throw e; });
    return readying;
  }

  function browser() {
    win("Files" + (caseTitle ? ": " + caseTitle : ""), "▤", function (w) {
      w.body.innerHTML = '<div class="ws-files"><ul class="ws-list" aria-label="Files"></ul><pre class="ws-view">Pick a file.</pre></div>';
      var ul = w.body.querySelector("ul"), view = w.body.querySelector(".ws-view");
      if (!caseId) { ul.innerHTML = "<li>No case is open. Pick one on the taskbar.</li>"; return; }
      ul.innerHTML = "<li>Loading…</li>";
      loadFiles().then(function (fs) {
        var names = Object.keys(fs).sort();
        if (!names.length) { ul.innerHTML = "<li>These files come with Labs or this case's seminar.</li>"; return; }
        ul.innerHTML = names.map(function (n) { return '<li><button type="button" data-f="' + esc(n) + '">' + esc(n) + "</button></li>"; }).join("");
        ul.addEventListener("click", function (e) {
          var b = e.target.closest("[data-f]");
          if (!b) return;
          ul.querySelectorAll("button").forEach(function (x) { x.classList.toggle("on", x === b); });
          var t = fs[b.getAttribute("data-f")];
          view.textContent = t.length > 300000 ? t.slice(0, 300000) + "\n… (cut)" : t;
        });
      });
    }, { w: 760, h: 460 });
  }

  function notepad() {
    win("Notes", "✎", function (w) {
      var key = "ws-notes-" + (caseId || "plain");
      w.body.innerHTML = '<textarea class="ws-notes" spellcheck="true" placeholder="Your notes for this case. They stay in this browser."></textarea><div class="ws-row"><button type="button" class="btn" data-n="dl">Download</button></div>';
      var t = w.body.querySelector("textarea");
      t.value = store(key) || "";
      t.addEventListener("input", function () { store(key, t.value); });
      w.body.querySelector('[data-n="dl"]').addEventListener("click", function () {
        var a = document.createElement("a");
        a.href = URL.createObjectURL(new Blob([t.value], { type: "text/plain" }));
        a.download = (caseId || "notes") + "-notes.txt";
        a.click();
      });
    }, { w: 460, h: 380 });
  }

  function help() {
    win("How to use this desktop", "?", function (w) {
      w.body.innerHTML = '<div class="ws-help"><h3>Your analyst workstation</h3><p>Everything here runs in your browser. Nothing you do can reach the internet or harm your computer.</p>' +
        "<ul><li><b>Start</b> opens every program, grouped by job: SOC analyst, incident responder, security engineer, cloud, penetration tester, governance.</li>" +
        "<li><b>Case</b> on the taskbar loads a case: its evidence goes into <code>~/case</code>, its network into the network tools, and every program can open its files.</li>" +
        "<li><b>Terminal</b> is a real Linux computer. Open as many terminals as you like; they share one computer but each keeps its own folder.</li>" +
        "<li>Drag a window by its title bar, double-click the title to fill the screen, and resize from the bottom-right corner.</li>" +
        "<li><b>Notes</b> are saved in this browser for each case.</li></ul></div>";
    }, { w: 520, h: 360 });
  }

  function tool(d) {
    win(d.title, (d.title || "?").charAt(0), function (w) {
      var host = document.createElement("div");
      host.className = "ws-tool";
      w.body.appendChild(host);
      var key = "ws-tool-" + (caseId || "plain") + "-" + d.id, saved = null;
      try { saved = JSON.parse(store(key) || "null"); } catch (e) { saved = null; }
      d.mount(host, { state: {}, saved: saved, files: loadFiles, remember: function (v) { try { store(key, JSON.stringify(v)); } catch (e) { return; } } });
    }, { w: 860, h: 540 });
  }

  function startMenu() {
    var m = $("ws-start-menu"), list = programs(), groups = {};
    list.forEach(function (p) { (groups[p.group] = groups[p.group] || []).push(p); });
    var order = ["System"].concat(T ? T.groups : []).concat(Object.keys(groups));
    var seen = {};
    m.innerHTML = '<input id="ws-find" placeholder="Search programs" aria-label="Search programs">' + order.filter(function (g) { if (seen[g] || !groups[g]) return false; seen[g] = 1; return true; }).map(function (g) {
      return '<div class="ws-grp"><h4>' + esc(g) + "</h4>" + groups[g].map(function (p) { return '<button type="button" data-p="' + esc(p.id) + '"><span>' + esc(p.icon) + "</span>" + esc(p.title) + "</button>"; }).join("") + "</div>";
    }).join("");
    m.querySelectorAll("[data-p]").forEach(function (b) {
      b.addEventListener("click", function () { m.hidden = true; list.filter(function (p) { return p.id === b.getAttribute("data-p"); })[0].open(); });
    });
    $("ws-find").addEventListener("input", function () {
      var v = this.value.toLowerCase();
      m.querySelectorAll("[data-p]").forEach(function (b) { b.hidden = v && b.textContent.toLowerCase().indexOf(v) < 0; });
    });
  }
  function icons() {
    var pick = ["terminal", "files", "notes", "tool-siem", "tool-packets", "tool-events", "tool-alerts", "tool-proxy", "help"], list = programs();
    $("ws-icons").innerHTML = pick.map(function (id) { return list.filter(function (p) { return p.id === id; })[0]; }).filter(Boolean).map(function (p) {
      return '<button type="button" class="ws-icon" data-p="' + esc(p.id) + '"><span>' + esc(p.icon) + "</span>" + esc(p.title) + "</button>";
    }).join("");
    $("ws-icons").querySelectorAll("[data-p]").forEach(function (b) {
      b.addEventListener("dblclick", function () { list.filter(function (p) { return p.id === b.getAttribute("data-p"); })[0].open(); });
      b.addEventListener("keydown", function (e) { if (e.key === "Enter") list.filter(function (p) { return p.id === b.getAttribute("data-p"); })[0].open(); });
    });
  }
  function caseMenu() {
    var sel = $("ws-case");
    sel.innerHTML = '<option value="">Plain Linux, no case</option>';
    if (!global.AayatVM) return;
    fetch(ROOT + "assets/linux/cases/index.json").then(function (r) { return r.json(); }).then(function (list) {
      sel.innerHTML += list.filter(function (c) { return !/--/.test(c.id); }).map(function (c) {
        return '<option value="' + esc(c.id) + '">' + esc((c.seminarId ? "Seminar lab: " : "") + c.title) + "</option>";
      }).join("");
      var want = (q.get("case") || "").replace(/[^a-z0-9-]/g, "");
      if (want && list.some(function (c) { return c.id === want; })) { sel.value = want; useCase(want, list); }
      sel.addEventListener("change", function () { useCase(sel.value, list); });
    }).catch(function () {});
  }
  function useCase(id, list) {
    if (id === caseId) return;
    wins.slice().forEach(close);
    caseId = id;
    caseTitle = id ? ((list.filter(function (c) { return c.id === id; })[0] || {}).title || id) : "";
    files = null; access = null; readying = null;
    $("ws-casename").textContent = caseTitle || "No case";
    var u = new URL(location.href);
    if (id) u.searchParams.set("case", id); else u.searchParams.delete("case");
    history.replaceState(null, "", u.toString());
    terminal();
  }
  function clock() {
    var d = new Date();
    $("ws-clock").textContent = d.toISOString().slice(11, 16) + " UTC";
  }

  function start() {
    if (!$("ws-app")) return;
    $("ws-start").addEventListener("click", function (e) { e.stopPropagation(); var m = $("ws-start-menu"); m.hidden = !m.hidden; if (!m.hidden) $("ws-find").focus(); });
    document.addEventListener("click", function (e) { var m = $("ws-start-menu"); if (!m.hidden && !m.contains(e.target)) m.hidden = true; });
    document.addEventListener("keydown", function (e) { if (e.key === "Escape") $("ws-start-menu").hidden = true; });
    startMenu();
    icons();
    caseMenu();
    clock();
    setInterval(clock, 30000);
    if (!q.get("case")) help();
  }
  if (document.readyState === "complete") start();
  else global.addEventListener("load", start);
})(window);
