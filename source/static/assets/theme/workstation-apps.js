(function (global) {
  "use strict";
  var me = document.currentScript && document.currentScript.src;
  var ROOT = me ? me.replace(/assets\/theme\/workstation-apps\.js.*$/, "") : "";
  var SLA = { critical: 15, high: 60, medium: 240, low: 1440, info: 2880 };
  var DISP = [["tp-handled", "True positive, handled"], ["escalated", "True positive, escalated"], ["false", "False positive"], ["benign", "Benign (expected activity)"], ["dup", "Duplicate"]];
  var PRIV = /^(10\.|192\.168\.|172\.(1[6-9]|2\d|3[01])\.|127\.)/;

  function D() { return global.AayatDesk; }
  function esc(s) { return D().esc(s); }
  function load(key, def) { try { return JSON.parse(D().store(key) || "null") || def; } catch (e) { return def; } }
  function save(key, v) { D().store(key, JSON.stringify(v)); }
  function hm(ms) {
    var neg = ms < 0, m = Math.floor(Math.abs(ms) / 60000), h = Math.floor(m / 60);
    return (neg ? "-" : "") + (h ? h + "h " + (m % 60) + "m" : m + "m");
  }
  function csvCell(v) { v = String(v == null ? "" : v); return /[",\n]/.test(v) ? '"' + v.replace(/"/g, '""') + '"' : v; }
  function download(name, rows) { global.AayatTools.kit.download(name, rows.map(function (r) { return r.map(csvCell).join(","); }).join("\n") + "\n", "text/csv"); }

  function tickets() {
    var d = D(), cid = d.caseId();
    d.win("Tickets" + (d.caseTitle() ? ": " + d.caseTitle() : ""), "ticket", function (w) {
      w.body.innerHTML = '<div class="tk"><div class="ws-toolbar"><select data-r="f" aria-label="Show"><option value="open">Open tickets</option><option value="mine">Assigned to me</option>' +
        '<option value="breach">SLA breached</option><option value="all">All tickets</option></select><input data-r="q" type="search" placeholder="Search tickets" aria-label="Search">' +
        '<span class="ws-tb-sp"></span><button type="button" class="btn" data-r="csv">Export CSV</button></div>' +
        '<div class="tk-grid"><div class="tk-list" data-r="list"></div><div class="tk-view" data-r="view"><p class="ws-empty">Pick a ticket.</p></div></div><div class="ws-status" data-r="stat"></div></div>';
      var r = function (n) { return w.body.querySelector('[data-r="' + n + '"]'); };
      if (!cid) { r("list").innerHTML = '<p class="ws-empty">No case is open.</p>'; return; }
      var startKey = "ws-tk-start-" + cid, t0 = +(d.store(startKey) || 0);
      if (!t0) { t0 = Date.now(); d.store(startKey, String(t0)); }
      var st = load("ws-tk-" + cid, {}), items = [], pick = null, timer = null;
      function state(a) { return st[a.id] = st[a.id] || { status: "New", who: "", log: [], disp: "" }; }
      function due(a) { return t0 + (SLA[a.sev] || 240) * 60000; }
      function left(a) { var s = state(a); return s.status === "Closed" ? null : due(a) - Date.now(); }
      function keep() { save("ws-tk-" + cid, st); }
      function shown() {
        var f = r("f").value, q = r("q").value.toLowerCase();
        return items.filter(function (a) {
          var s = state(a), l = left(a);
          if (f === "open" && s.status === "Closed") return false;
          if (f === "mine" && s.who !== "me") return false;
          if (f === "breach" && !(l != null && l < 0)) return false;
          return !q || (a.id + " " + a.rule + " " + a.host + " " + a.user + " " + a.detail).toLowerCase().indexOf(q) >= 0;
        });
      }
      function list() {
        var rows = shown();
        r("list").innerHTML = '<table class="ws-grid"><tr><th>Sev</th><th>ID</th><th>Title</th><th>Host</th><th>Status</th><th>SLA</th></tr>' + rows.map(function (a) {
          var s = state(a), l = left(a);
          return '<tr data-id="' + esc(a.id) + '" class="' + (pick === a.id ? "on" : "") + '"><td><span class="sev ' + a.sev + '">' + esc(a.sev) + "</span></td><td>" + esc(a.id) + "</td><td>" + esc(a.rule) +
            "</td><td>" + esc(a.host) + "</td><td>" + esc(s.status) + (s.who ? " · " + esc(s.who) : "") + '</td><td class="' + (l != null && l < 0 ? "late" : "") + '">' + (l == null ? "done" : hm(l)) + "</td></tr>";
        }).join("") + "</table>" + (rows.length ? "" : '<p class="ws-empty">Nothing here.</p>');
        var open = items.filter(function (a) { return state(a).status !== "Closed"; }).length, late = items.filter(function (a) { var l = left(a); return l != null && l < 0; }).length;
        r("stat").textContent = items.length + " tickets · " + open + " open · " + late + " past SLA · SLA clock started " + new Date(t0).toTimeString().slice(0, 5);
      }
      function note(a, text) { state(a).log.push({ t: Date.now(), text: text }); keep(); }
      function view() {
        var a = items.filter(function (x) { return x.id === pick; })[0];
        if (!a) return;
        var s = state(a), l = left(a);
        r("view").innerHTML = '<div class="tk-head"><span class="sev ' + a.sev + '">' + esc(a.sev) + "</span><h3>" + esc(a.id + " " + a.rule) + "</h3></div>" +
          '<dl class="tk-meta"><dt>Status</dt><dd>' + esc(s.status) + (s.disp ? " (" + esc((DISP.filter(function (x) { return x[0] === s.disp; })[0] || [0, s.disp])[1]) + ")" : "") + "</dd><dt>Assignee</dt><dd>" + esc(s.who || "Unassigned") +
          "</dd><dt>Raised</dt><dd>" + esc(a.time) + "</dd><dt>SLA</dt><dd" + (l != null && l < 0 ? ' class="late"' : "") + ">" + (l == null ? "met or closed" : (l < 0 ? "breached by " + hm(-l) : hm(l) + " left")) +
          "</dd><dt>Host</dt><dd>" + esc(a.host || "-") + "</dd><dt>User</dt><dd>" + esc(a.user || "-") + "</dd>" + (a.src ? "<dt>Source</dt><dd>" + esc(a.src) + "</dd>" : "") + (a.dest ? "<dt>Destination</dt><dd>" + esc(a.dest) + "</dd>" : "") + "</dl>" +
          '<p class="tk-desc"></p>' + (a.evidence.length ? '<p class="tk-ev"><b>Evidence:</b> ' + a.evidence.map(function (f) { return '<button type="button" class="ws-linkbtn" data-ev="' + esc(f) + '">' + esc(f) + "</button>"; }).join(" ") + "</p>" : "") +
          '<div class="ws-toolbar tk-acts"><button type="button" class="btn" data-a="mine">Assign to me</button><button type="button" class="btn" data-a="work">Start work</button><button type="button" class="btn" data-a="esc">Escalate</button>' +
          '<select data-a="disp" aria-label="Disposition"><option value="">Close as…</option>' + DISP.map(function (x) { return '<option value="' + x[0] + '">' + esc(x[1]) + "</option>"; }).join("") + "</select></div>" +
          '<textarea data-a="txt" placeholder="Work note: what you checked, what you found. A reason is needed to close or escalate." rows="3"></textarea><button type="button" class="btn dark" data-a="add">Add note</button>' +
          '<ol class="tk-log">' + s.log.slice().reverse().map(function (x) { return "<li><small>" + new Date(x.t).toTimeString().slice(0, 5) + "</small> " + esc(x.text) + "</li>"; }).join("") + "</ol>";
        r("view").querySelector(".tk-desc").textContent = a.detail;
        var txt = r("view").querySelector('[data-a="txt"]');
        function need() { var v = txt.value.trim(); if (v.length < 8) { txt.focus(); txt.classList.add("bad"); return ""; } return v; }
        r("view").addEventListener("click", function (e) {
          var b = e.target.closest("[data-a],[data-ev]");
          if (!b) return;
          if (b.hasAttribute("data-ev")) { d.open(b.getAttribute("data-ev")); return; }
          var k = b.getAttribute("data-a");
          if (k === "mine") { s.who = "me"; note(a, "Assigned to me"); }
          else if (k === "work") { s.status = "In progress"; if (!s.who) s.who = "me"; note(a, "Started work"); }
          else if (k === "esc") { var v = need(); if (!v) return; s.status = "Escalated"; note(a, "Escalated: " + v); d.post({ name: "Priya Shah", role: "SOC lead" }, "Got your escalation on " + a.id + ". Is the ask first, and does it say what you haven't done?"); }
          else if (k === "add") { var n = txt.value.trim(); if (!n) return; note(a, n); }
          else return;
          keep(); list(); view();
        });
        r("view").querySelector('[data-a="disp"]').addEventListener("change", function () {
          var v = this.value;
          if (!v) return;
          var why = need();
          if (!why) { this.value = ""; return; }
          s.status = "Closed"; s.disp = v; note(a, "Closed as " + (DISP.filter(function (x) { return x[0] === v; })[0] || [0, v])[1] + ": " + why);
          keep(); list(); view();
          d.toast("Ticket closed", a.id + " closed as " + (DISP.filter(function (x) { return x[0] === v; })[0] || [0, v])[1]);
        });
      }
      r("list").addEventListener("click", function (e) { var tr = e.target.closest("tr[data-id]"); if (tr) { pick = tr.getAttribute("data-id"); list(); view(); } });
      r("f").addEventListener("change", list);
      r("q").addEventListener("input", list);
      r("csv").addEventListener("click", function () {
        download((cid || "case") + "-tickets.csv", [["id", "severity", "title", "host", "status", "assignee", "disposition", "sla_due", "notes"]].concat(items.map(function (a) {
          var s = state(a); return [a.id, a.sev, a.rule, a.host, s.status, s.who, s.disp, new Date(due(a)).toISOString(), s.log.map(function (x) { return x.text; }).join(" | ")];
        })));
      });
      d.files().then(function (fs) {
        var A = global.AayatTools.get("alerts"), Q = A ? A.queues(global.AayatTools.kit.textFiles(fs)) : {};
        Object.keys(Q).sort().forEach(function (n) { items = items.concat(Q[n]); });
        if (!items.length) { r("list").innerHTML = '<p class="ws-empty">This case has no alerts, so no tickets.</p>'; return; }
        items = A.order(items);
        list();
        timer = setInterval(function () { if (!document.body.contains(w.el)) { clearInterval(timer); return; } list(); }, 30000);
      });
    }, { w: 1000, h: 560 });
  }

  function netOf(cid) {
    var V = global.AayatVM;
    if (!cid || !V) return Promise.resolve(null);
    return V.manifest(cid).then(function (m) {
      var base = ROOT + "assets/linux/cases/" + (m.base || m.id) + "/";
      if ((m.files || []).indexOf("net/hosts.txt") < 0) return null;
      return Promise.all(["net/hosts.txt", "net/dns.txt"].map(function (f) { return (m.files || []).indexOf(f) < 0 ? "" : fetch(base + f).then(function (x) { return x.ok ? x.text() : ""; }); }));
    }).then(function (t) {
      if (!t) return null;
      var hosts = {}, names = {};
      t[1].split("\n").forEach(function (l) { var p = l.trim().split(/\s+/); if (p[0] === "A" && p[2]) names[p[2]] = names[p[2]] || p[1]; });
      t[0].split("\n").forEach(function (l) {
        var f = l.split("|");
        if (f.length < 3) return;
        if (f[0] === "os") { (hosts[f[1]] = hosts[f[1]] || { ip: f[1], name: "", ports: [] }).os = f[3] || f[2]; return; }
        var h = hosts[f[0]] = hosts[f[0]] || { ip: f[0], name: "", ports: [] };
        if (f[1]) h.name = f[1];
        h.ports.push({ port: +f[2], proto: f[3], svc: f[4], ver: f[5], flag: f[6] === "1", title: f[7] || "" });
      });
      Object.keys(hosts).forEach(function (ip) { var h = hosts[ip]; if (!h.name) h.name = names[ip] || ""; h.internal = PRIV.test(ip); h.kind = kind(h); });
      return Object.keys(hosts).map(function (k) { return hosts[k]; }).sort(function (a, b) { return order(a) - order(b) || a.ip.localeCompare(b.ip, undefined, { numeric: true }); });
    }).catch(function () { return null; });
  }
  function kind(h) {
    var n = (h.name || "").toLowerCase(), svcs = h.ports.map(function (p) { return p.svc; }).join(" ");
    if (!h.internal) return "internet";
    if (/gateway|router|fw|firewall|^gw/.test(n)) return "router";
    if (/switch|sw\d/.test(n)) return "switch";
    if (/laptop|pc|ws\d|desk|till|-ws/.test(n) || /ms-wbt-server|netbios/.test(svcs) && !/dc|srv|server|file|db/.test(n)) return "pc";
    return "server";
  }
  function order(h) { return { router: 0, switch: 1, server: 2, pc: 3, internet: 4 }[h.kind]; }

  function rack() {
    var d = D(), cid = d.caseId();
    d.win("Server room" + (d.caseTitle() ? ": " + d.caseTitle() : ""), "rack", function (w) {
      w.body.innerHTML = '<div class="rk"><div class="rk-room"><div class="rk-rack" data-r="rack"></div><div class="rk-side"><div data-r="desk" class="rk-desk"></div><div data-r="net" class="rk-net"></div></div></div>' +
        '<aside class="rk-panel" data-r="panel"><p class="ws-empty">Click a device to inspect it. Every lit port is a service someone can reach.</p></aside>' +
        '<div class="ws-status" data-r="stat"></div><div class="ws-toolbar rk-bar"><label><input type="checkbox" data-r="door"> Rack door locked</label><button type="button" class="btn" data-r="csv">Export asset inventory</button></div></div>';
      var r = function (n) { return w.body.querySelector('[data-r="' + n + '"]'); };
      if (!cid) { r("rack").innerHTML = '<p class="ws-empty">No case is open.</p>'; return; }
      var st = load("ws-rack-" + cid, { tag: {}, shut: {}, note: {}, door: false }), hosts = [];
      r("door").checked = !!st.door;
      function keep() { save("ws-rack-" + cid, st); }
      function ports(h) {
        return '<span class="rk-ports">' + h.ports.slice(0, 12).map(function (p) {
          var k = h.ip + ":" + p.port, off = st.shut[k];
          return '<i class="rk-jack' + (off ? " off" : p.flag ? " bad" : " on") + '" title="' + esc(p.port + "/" + p.proto + " " + p.svc + (p.ver ? " · " + p.ver : "") + (off ? " (shut)" : "")) + '"></i>';
        }).join("") + "</span>";
      }
      function unit(h) {
        var tag = st.tag[h.ip] || "";
        return '<button type="button" class="rk-unit k-' + h.kind + (h.ports.length > 4 ? " u2" : "") + (tag ? " t-" + tag : "") + '" data-ip="' + esc(h.ip) + '"><span class="rk-ears"></span><span class="rk-leds"><i class="pwr"></i><i class="act"></i></span>' +
          '<span class="rk-label"><b>' + esc(h.name || h.ip) + "</b><small>" + esc(h.ip) + "</small></span>" + ports(h) + '<span class="rk-ears"></span></button>';
      }
      function draw() {
        var inside = hosts.filter(function (h) { return h.kind === "router" || h.kind === "switch" || h.kind === "server"; });
        var empty = Math.max(0, 9 - inside.reduce(function (s, h) { return s + (h.ports.length > 4 ? 2 : 1); }, 0));
        r("rack").innerHTML = '<div class="rk-top">RACK A · ' + esc(d.caseTitle()) + "</div>" + inside.map(unit).join("") + new Array(empty + 1).join('<div class="rk-blank"></div>') + '<div class="rk-foot"></div>';
        r("rack").classList.toggle("locked", !!st.door);
        r("desk").innerHTML = '<h5>Office floor</h5>' + (hosts.filter(function (h) { return h.kind === "pc"; }).map(function (h) {
          return '<button type="button" class="rk-pc' + (st.tag[h.ip] ? " t-" + st.tag[h.ip] : "") + '" data-ip="' + esc(h.ip) + '"><span class="rk-screen"></span><b>' + esc(h.name || h.ip) + "</b><small>" + esc(h.ip) + "</small>" + ports(h) + "</button>";
        }).join("") || '<p class="ws-empty">No desktops in the scan.</p>');
        r("net").innerHTML = '<h5>Internet</h5>' + (hosts.filter(function (h) { return h.kind === "internet"; }).map(function (h) {
          return '<button type="button" class="rk-cloud' + (st.tag[h.ip] ? " t-" + st.tag[h.ip] : "") + '" data-ip="' + esc(h.ip) + '"><b>' + esc(h.name || h.ip) + "</b><small>" + esc(h.ip) + "</small>" + ports(h) + "</button>";
        }).join("") || '<p class="ws-empty">Nothing outside.</p>');
        var exposed = 0, shut = 0;
        hosts.forEach(function (h) { if (!h.internal) return; h.ports.forEach(function (p) { if (st.shut[h.ip + ":" + p.port]) shut++; else exposed++; }); });
        var tagged = Object.keys(st.tag).length;
        r("stat").textContent = hosts.length + " devices · " + exposed + " open services inside · " + shut + " shut · " + tagged + " of " + hosts.length + " devices reviewed" + (st.door ? " · rack locked" : " · rack door open");
      }
      function panel(ip) {
        var h = hosts.filter(function (x) { return x.ip === ip; })[0];
        if (!h) return;
        w.body.querySelectorAll("[data-ip]").forEach(function (b) { b.classList.toggle("sel", b.getAttribute("data-ip") === ip); });
        r("panel").innerHTML = "<h4>" + esc(h.name || h.ip) + "</h4><dl><dt>Address</dt><dd>" + esc(h.ip) + "</dd><dt>Type</dt><dd>" + esc({ router: "Router or gateway", switch: "Switch", server: "Server", pc: "Desktop or laptop", internet: "Outside the network" }[h.kind]) +
          "</dd><dt>System</dt><dd>" + esc(h.os || "unknown") + "</dd></dl>" +
          '<table class="ws-grid"><tr><th>Port</th><th>Service</th><th>Version</th><th></th></tr>' + h.ports.map(function (p) {
            var k = h.ip + ":" + p.port;
            return "<tr" + (p.flag ? ' class="bad"' : "") + "><td>" + p.port + "/" + esc(p.proto) + "</td><td>" + esc(p.svc) + (p.title ? "<br><small>" + esc(p.title) + "</small>" : "") + "</td><td>" + esc(p.ver) + "</td><td>" +
              (h.internal ? '<button type="button" class="btn" data-shut="' + esc(k) + '">' + (st.shut[k] ? "Open" : "Shut") + "</button>" : "") + "</td></tr>";
          }).join("") + "</table>" +
          '<label class="rk-tag">Review <select data-tag><option value="">Not reviewed</option><option value="ok">Known and needed</option><option value="patch">Needs patching or hardening</option>' +
          '<option value="unknown">Unknown device: find the owner</option><option value="bad">Suspicious: investigate</option></select></label>' +
          '<textarea data-note rows="2" placeholder="Note: owner, why it is there, what to change"></textarea>' +
          '<div class="ws-toolbar"><button type="button" class="btn" data-term>Open a terminal</button><small>Try: nmap -sV ' + esc(h.ip) + "</small></div>";
        r("panel").querySelector("[data-tag]").value = st.tag[h.ip] || "";
        r("panel").querySelector("[data-note]").value = st.note[h.ip] || "";
        r("panel").querySelector("[data-tag]").addEventListener("change", function () { if (this.value) st.tag[h.ip] = this.value; else delete st.tag[h.ip]; keep(); draw(); panel(ip); });
        r("panel").querySelector("[data-note]").addEventListener("input", function () { st.note[h.ip] = this.value; keep(); });
        r("panel").querySelector("[data-term]").addEventListener("click", function () { d.terminal(); });
        r("panel").querySelectorAll("[data-shut]").forEach(function (b) { b.addEventListener("click", function () { var k = b.getAttribute("data-shut"); if (st.shut[k]) delete st.shut[k]; else st.shut[k] = 1; keep(); draw(); panel(ip); }); });
      }
      w.body.addEventListener("click", function (e) { var b = e.target.closest("[data-ip]"); if (b && !e.target.closest(".rk-panel")) panel(b.getAttribute("data-ip")); });
      r("door").addEventListener("change", function () { st.door = this.checked; keep(); draw(); });
      r("csv").addEventListener("click", function () {
        download((cid || "case") + "-asset-inventory.csv", [["ip", "name", "type", "system", "open_ports", "shut_ports", "review", "note"]].concat(hosts.map(function (h) {
          return [h.ip, h.name, h.kind, h.os || "", h.ports.filter(function (p) { return !st.shut[h.ip + ":" + p.port]; }).map(function (p) { return p.port + "/" + p.svc; }).join(" "),
            h.ports.filter(function (p) { return st.shut[h.ip + ":" + p.port]; }).map(function (p) { return p.port; }).join(" "), st.tag[h.ip] || "", st.note[h.ip] || ""];
        })));
      });
      netOf(cid).then(function (list) {
        if (!list || !list.length) { r("rack").innerHTML = '<p class="ws-empty">This case has no network map. Cases with a recorded network show their devices here.</p>'; return; }
        hosts = list;
        draw();
      });
    }, { w: 1080, h: 600 });
  }

  function hostsOf(fs) {
    var out = {};
    Object.keys(fs).forEach(function (n) {
      if (/\.csv$/i.test(n) && /(^|\n)time,host,pid,ppid/.test(fs[n].slice(0, 200))) global.AayatTools.kit.csv(fs[n]).forEach(function (row) { if (row.host) (out[row.host.toLowerCase()] = out[row.host.toLowerCase()] || { procs: [], logs: [], services: [] }).procs.push(row); });
      if (/\.jsonl$/i.test(n)) (fs[n].match(/"Computer":\s*"([^"]+)"/g) || []).forEach(function (m) {
        var h = /"Computer":\s*"([^".]+)/.exec(m)[1].toLowerCase(), o = out[h] = out[h] || { procs: [], logs: [], services: [] };
        if (o.logs.indexOf(n) < 0) o.logs.push(n);
      });
      if (/services.*\.csv$/i.test(n)) { var host = (/-([a-z0-9-]+)-services/i.exec(n) || [])[1] || ""; var rows = global.AayatTools.kit.csv(fs[n]); Object.keys(out).forEach(function (k) { if (host && host.toLowerCase() === k) out[k].services = rows; }); if (host && !out[host.toLowerCase()]) out[host.toLowerCase()] = { procs: [], logs: [], services: rows }; }
    });
    return out;
  }
  function rdp() {
    var d = D(), cid = d.caseId();
    d.win("Remote desktop", "rdp", function (w) {
      w.body.innerHTML = '<div class="rd-pick"><p class="ws-empty">Loading…</p></div>';
      if (!cid) { w.body.innerHTML = '<p class="ws-empty">No case is open.</p>'; return; }
      d.files().then(function (fs) {
        var H = hostsOf(fs), names = Object.keys(H).filter(function (h) { return H[h].procs.length || H[h].logs.length || H[h].services.length; }).sort();
        if (!names.length) { w.body.innerHTML = '<p class="ws-empty">This case has no Windows machines with saved evidence.</p>'; return; }
        w.body.innerHTML = '<div class="rd-pick"><h3>Connect to a machine</h3><p>Each machine below is rebuilt from the case\'s saved evidence: its process list, event logs and services, as the incident team captured them.</p>' +
          names.map(function (h) { return '<button type="button" class="rd-host" data-h="' + esc(h) + '">' + d.icon("rdp", 36) + "<span><b>" + esc(h) + "</b><small>" + H[h].procs.length + " processes · " + H[h].logs.length + " event logs" + (H[h].services.length ? " · " + H[h].services.length + " services" : "") + "</small></span></button>"; }).join("") + "</div>";
        w.body.querySelectorAll("[data-h]").forEach(function (b) { b.addEventListener("click", function () { session(w, b.getAttribute("data-h"), H[b.getAttribute("data-h")], fs); }); });
      });
    }, { w: 960, h: 600 });
  }
  function session(w, host, H, fs) {
    var d = D();
    w.el.querySelector(".ws-title b").textContent = "Remote desktop: " + host;
    w.body.innerHTML = '<div class="rd"><div class="rd-desk" data-r="desk"><div class="rd-icons">' +
      [["tasks", "Task Manager", "events"], ["cmd", "Command Prompt", "terminal"], ["evt", "Event Viewer", "events"], ["svc", "Services", "gear"]].map(function (x) {
        return '<button type="button" data-app="' + x[0] + '">' + d.icon(x[2], 38) + "<span>" + x[1] + "</span></button>";
      }).join("") + '</div><div class="rd-win" data-r="app" hidden><div class="rd-wt"><b data-r="apptitle"></b><button type="button" data-r="appx" aria-label="Close">×</button></div><div class="rd-wb" data-r="appbody"></div></div>' +
      '<div class="rd-note">Read-only copy of ' + esc(host) + ' from the evidence. Nothing you do here changes the case.</div></div>' +
      '<div class="rd-bar"><span class="rd-start">' + esc(host.toUpperCase()) + "</span><span data-r=\"rtasks\"></span><span class=\"rd-clock\">" + new Date().toTimeString().slice(0, 5) + "</span></div></div>";
    var r = function (n) { return w.body.querySelector('[data-r="' + n + '"]'); };
    function open(app) {
      r("app").hidden = false;
      r("apptitle").textContent = { tasks: "Task Manager", cmd: "Command Prompt", evt: "Event Viewer", svc: "Services" }[app] + " · " + host;
      r("rtasks").textContent = r("apptitle").textContent;
      var b = r("appbody");
      b.className = "rd-wb" + (app === "cmd" ? " rd-cmd" : "");
      if (app === "tasks") {
        var rows = H.procs.slice().sort(function (a, c) { return a.time < c.time ? -1 : 1; });
        b.innerHTML = rows.length ? '<div class="ws-toolbar"><input type="search" placeholder="Filter processes" data-f><small>' + rows.length + ' processes captured. Look at parents, users, folders and command lines.</small></div><table class="ws-grid"><tr><th>Name</th><th>PID</th><th>Parent</th><th>User</th><th>Started</th><th>Command line</th></tr>' +
          rows.map(function (p) { return "<tr><td>" + esc((p.image || "").split("\\").pop()) + "</td><td>" + esc(p.pid) + "</td><td>" + esc(p.ppid) + "</td><td>" + esc(p.user) + "</td><td>" + esc(p.time) + '</td><td class="mono">' + esc(p.command_line) + "</td></tr>"; }).join("") + "</table>" : '<p class="ws-empty">No process list was captured for this machine.</p>';
        var f = b.querySelector("[data-f]");
        if (f) f.addEventListener("input", function () { var v = f.value.toLowerCase(); b.querySelectorAll("tr").forEach(function (tr, i) { if (i) tr.hidden = v && tr.textContent.toLowerCase().indexOf(v) < 0; }); });
      } else if (app === "svc") {
        b.innerHTML = H.services.length ? '<table class="ws-grid"><tr><th>Name</th><th>State</th><th>Start</th><th>Path</th><th>Account</th></tr>' + H.services.map(function (s) {
          return "<tr><td>" + esc(s.Name || s.name) + "</td><td>" + esc(s.State || s.state) + "</td><td>" + esc(s.StartMode || s.start) + '</td><td class="mono">' + esc(s.PathName || s.path) + "</td><td>" + esc(s.UserAccount || s.account) + "</td></tr>";
        }).join("") + "</table>" : '<p class="ws-empty">No service list was captured for this machine.</p>';
      } else if (app === "evt") {
        b.innerHTML = H.logs.length ? "<p>Event logs saved from " + esc(host) + ":</p><ul>" + H.logs.map(function (n) { return '<li><button type="button" class="ws-linkbtn" data-log="' + esc(n) + '">' + esc(n) + "</button></li>"; }).join("") + "</ul><p><small>They open in the Event viewer on your own desktop.</small></p>" : '<p class="ws-empty">No event logs were captured for this machine.</p>';
        b.querySelectorAll("[data-log]").forEach(function (x) { x.addEventListener("click", function () { d.open(x.getAttribute("data-log")); }); });
      } else {
        b.innerHTML = '<pre class="rd-out"></pre><form><span>C:\\Users\\analyst&gt; </span><input aria-label="Command" autocomplete="off" spellcheck="false"></form>';
        var out = b.querySelector("pre"), inp = b.querySelector("input");
        function say(t) { out.textContent += t + "\n"; b.scrollTop = b.scrollHeight; }
        say("Remote command line on " + host.toUpperCase() + " (read-only, rebuilt from evidence). Type help.");
        b.querySelector("form").addEventListener("submit", function (e) {
          e.preventDefault();
          var c = inp.value.trim(), lc = c.toLowerCase();
          inp.value = "";
          say("C:\\Users\\analyst> " + c);
          if (!c) return;
          if (lc === "help") say("hostname, whoami, tasklist, tasklist /v, wmic process get name,processid,parentprocessid,commandline, sc query, cls");
          else if (lc === "hostname") say(host.toUpperCase());
          else if (lc === "whoami") say(host.toUpperCase() + "\\analyst (incident responder, read-only)");
          else if (lc === "cls") out.textContent = "";
          else if (/^tasklist/.test(lc)) {
            say("Image Name                     PID  Session  User");
            say("========================= ======== ======== ==================");
            H.procs.forEach(function (p) { var n = (p.image || "").split("\\").pop(); say((n + "                         ").slice(0, 25) + " " + ("        " + p.pid).slice(-8) + " " + "Console " + " " + (/v/.test(lc) ? p.user : "")); });
            if (!H.procs.length) say("INFO: no process list was captured for this machine.");
          } else if (/^wmic process/.test(lc)) H.procs.forEach(function (p) { say((p.image || "").split("\\").pop() + "  " + p.pid + "  " + p.ppid + "  " + p.command_line); });
          else if (/^sc query/.test(lc)) { if (!H.services.length) say("No service list was captured."); H.services.forEach(function (s) { say("SERVICE_NAME: " + (s.Name || s.name) + "\n        STATE              : " + (s.State || s.state) + "\n"); }); }
          else say("'" + c.split(" ")[0] + "' isn't available in this read-only copy. Type help.");
        });
        inp.focus();
      }
    }
    w.body.querySelectorAll("[data-app]").forEach(function (b) { b.addEventListener("dblclick", function () { open(b.getAttribute("data-app")); }); b.addEventListener("keydown", function (e) { if (e.key === "Enter") open(b.getAttribute("data-app")); }); });
    r("appx").addEventListener("click", function () { r("app").hidden = true; r("rtasks").textContent = ""; });
    open(H.procs.length ? "tasks" : H.logs.length ? "evt" : "svc");
  }

  global.AayatDeskApps = [
    { id: "tickets", title: "Tickets", icon: "ticket", open: tickets },
    { id: "rack", title: "Server room", icon: "rack", open: rack },
    { id: "rdp", title: "Remote desktop", icon: "rdp", open: rdp }
  ];
})(window);
