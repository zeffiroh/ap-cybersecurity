(function (global) {
  "use strict";
  var me = document.currentScript && document.currentScript.src;
  var ROOT = me ? me.replace(/assets\/theme\/workstation-apps\.js.*$/, "") : "";
  var SLA = { critical: 15, high: 60, medium: 240, low: 1440, info: 2880 };
  var DISP = [["tp-handled", "True positive, handled"], ["escalated", "True positive, escalated"], ["false", "False positive"], ["benign", "Benign (expected activity)"], ["dup", "Duplicate"]];

  function D() { return global.AayatDesk; }
  function esc(s) { return D().esc(s); }
  function load(key, def) { try { return JSON.parse(D().store(key) || "null") || def; } catch (e) { return def; } }
  function save(key, v) { D().store(key, JSON.stringify(v)); }
  function hm(ms) {
    var neg = ms < 0, m = Math.floor(Math.abs(ms) / 60000), h = Math.floor(m / 60);
    return (neg ? "-" : "") + (h ? h + "h " + (m % 60) + "m" : m + "m");
  }
  function slaOf(meta) {
    var raw = meta && meta.sla, out = {}, own = false;
    Object.keys(SLA).forEach(function (k) {
      var v = raw && Math.round(+raw[k]);
      if (v >= 1 && v <= 43200) { out[k] = v; own = true; } else out[k] = SLA[k];
    });
    return { mins: out, own: own, note: own && raw.note ? String(raw.note) : "" };
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
      function sla() { return slaOf(d.caseMeta()); }
      function due(a) { return t0 + (sla().mins[a.sev] || 240) * 60000; }
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
        r("stat").textContent = items.length + " tickets · " + open + " open · " + late + " past SLA · " + (sla().own ? "this case's SLA" : "standard SLA") + " · clock started " + new Date(t0).toTimeString().slice(0, 5);
      }
      function note(a, text) { state(a).log.push({ t: Date.now(), text: text }); keep(); }
      function view() {
        var a = items.filter(function (x) { return x.id === pick; })[0];
        if (!a) return;
        var s = state(a), l = left(a), g = sla();
        r("view").innerHTML = '<div class="tk-head"><span class="sev ' + a.sev + '">' + esc(a.sev) + "</span><h3>" + esc(a.id + " " + a.rule) + "</h3></div>" +
          '<dl class="tk-meta"><dt>Status</dt><dd>' + esc(s.status) + (s.disp ? " (" + esc((DISP.filter(function (x) { return x[0] === s.disp; })[0] || [0, s.disp])[1]) + ")" : "") + "</dd><dt>Assignee</dt><dd>" + esc(s.who || "Unassigned") +
          "</dd><dt>Raised</dt><dd>" + esc(a.time) + "</dd><dt>SLA</dt><dd" + (l != null && l < 0 ? ' class="late"' : "") + ">" + (l == null ? "met or closed" : (l < 0 ? "breached by " + hm(-l) : hm(l) + " left")) +
          "</dd><dt>Target</dt><dd>" + esc(hm(g.mins[a.sev] * 60000) + " for " + a.sev + (g.own ? " (this case's SLA" + (g.note ? ": " + g.note : "") + ")" : " (standard SLA)")) +
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
          d.emit("ticket." + ({ mine: "assign", work: "start", esc: "escalate", add: "note" })[k], { id: a.id, rule: a.rule || "", host: a.host || "", status: s.status, text: (txt.value || "").trim() });
          keep(); list(); view();
        });
        r("view").querySelector('[data-a="disp"]').addEventListener("change", function () {
          var v = this.value;
          if (!v) return;
          var why = need();
          if (!why) { this.value = ""; return; }
          s.status = "Closed"; s.disp = v; note(a, "Closed as " + (DISP.filter(function (x) { return x[0] === v; })[0] || [0, v])[1] + ": " + why);
          d.emit("ticket.close", { id: a.id, rule: a.rule || "", host: a.host || "", disp: v, text: why });
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
      function fill() {
        d.files().then(function (fs) {
          var A = global.AayatTools.get("alerts"), Q = A ? A.queues(global.AayatTools.kit.textFiles(fs, function (k) { return d.visible(k); })) : {};
          var had = items.length;
          items = [];
          Object.keys(Q).sort().forEach(function (n) { items = items.concat(Q[n]); });
          if (!items.length) { r("list").innerHTML = '<p class="ws-empty">No alerts yet, so no tickets.</p>'; return; }
          items = A.order(items);
          list();
          if (had && items.length > had) d.toast("New alerts", (items.length - had) + " new ticket" + (items.length - had === 1 ? "" : "s") + " in the queue");
        });
      }
      w.refresh = fill;
      fill();
      timer = setInterval(function () { if (!document.body.contains(w.el)) { clearInterval(timer); return; } if (items.length) list(); }, 30000);
    }, { w: 1000, h: 560 });
  }

  function netOf(cid) {
    var V = global.AayatVM;
    if (!cid || !V) return Promise.resolve(null);
    return V.manifest(cid).then(function (m) {
      var base = ROOT + "assets/linux/cases/" + (m.caseDir || m.base || m.id) + "/";
      if ((m.files || []).indexOf("net/hosts.txt") < 0) return null;
      return Promise.all(["net/hosts.txt", "net/dns.txt"].map(function (f) { return (m.files || []).indexOf(f) < 0 ? "" : fetch(base + f).then(function (x) { return x.ok ? x.text() : ""; }); }));
    }).then(function (t) {
      if (!t) return null;
      return global.AayatNet.parseHosts(t[0], t[1]).map(function (h) { h.kind = kind(h); return h; }).sort(function (a, b) { return order(a) - order(b) || a.ip.localeCompare(b.ip, undefined, { numeric: true }); });
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

  var HELLO = "Click a device to inspect it. Every lit port is a service someone can reach. Patch panel shows the cables.";
  function rack() {
    var d = D(), cid = d.caseId();
    d.win("Server room" + (d.caseTitle() ? ": " + d.caseTitle() : ""), "rack", function (w) {
      w.body.innerHTML = '<div class="rk"><div class="rk-room" data-r="room"><div class="rk-rack" data-r="rack"></div><div class="rk-side"><div data-r="desk" class="rk-desk"></div><div data-r="net" class="rk-net"></div></div></div>' +
        '<aside class="rk-panel" data-r="panel"><p class="ws-empty">' + HELLO + '</p></aside>' +
        '<div class="ws-status" data-r="stat"></div><div class="ws-toolbar rk-bar"><span class="rk-tabs" role="tablist"><button type="button" class="on" data-view="rack" role="tab">Rack</button><button type="button" data-view="patch" role="tab">Patch panel</button></span>' +
        '<label><input type="checkbox" data-r="door"> Rack door locked</label><button type="button" class="btn" data-r="bench">Open on the bench</button><button type="button" class="btn" data-r="csv">Export asset inventory</button></div></div>';
      var r = function (n) { return w.body.querySelector('[data-r="' + n + '"]'); };
      if (!cid) { r("rack").innerHTML = '<p class="ws-empty">No case is open.</p>'; return; }
      var st = load("ws-rack-" + cid, { tag: {}, shut: {}, note: {}, door: false }), hosts = [], net = null, view = "rack", pp = null;
      r("door").checked = !!st.door;
      if (global.AayatBench) global.AayatBench.open("case:" + cid).then(function (a) {
        net = a;
        if (!a) return;
        if (st.door && !a.state.door) a.setDoor(true);
        r("door").checked = !!a.state.door;
        st.door = !!a.state.door;
        if (hosts.length) draw();
      });
      function show(v) {
        view = v;
        w.body.querySelectorAll("[data-view]").forEach(function (b) { b.classList.toggle("on", b.getAttribute("data-view") === v); b.setAttribute("aria-selected", b.getAttribute("data-view") === v ? "true" : "false"); });
        var old = r("room").querySelector(".rk-patch");
        if (old) old.remove();
        r("rack").hidden = v !== "rack";
        r("room").querySelector(".rk-side").hidden = v !== "rack";
        if (v === "rack") { r("panel").innerHTML = '<p class="ws-empty">' + HELLO + "</p>"; if (hosts.length) draw(); return; }
        var box = document.createElement("div");
        box.className = "rk-patch";
        r("room").appendChild(box);
        global.AayatBench.patch(box, r("panel"), r("stat"), cid).then(function (x) { pp = x; });
      }
      w.body.querySelectorAll("[data-view]").forEach(function (b) { b.addEventListener("click", function () { if (b.getAttribute("data-view") === "patch" && !global.AayatBench) return; show(b.getAttribute("data-view")); }); });
      r("bench").addEventListener("click", function () { d.run("bench", { bench: "case:" + cid }); });
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
        if (view !== "rack") return;
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
        r("panel").querySelector("[data-tag]").addEventListener("change", function () { if (this.value) st.tag[h.ip] = this.value; else delete st.tag[h.ip]; d.emit("rack.tag", { ip: h.ip, name: h.name || "", tag: this.value }); keep(); draw(); panel(ip); });
        r("panel").querySelector("[data-note]").addEventListener("input", function () { st.note[h.ip] = this.value; keep(); });
        r("panel").querySelector("[data-term]").addEventListener("click", function () { d.terminal(); });
        r("panel").querySelectorAll("[data-shut]").forEach(function (b) { b.addEventListener("click", function () { var k = b.getAttribute("data-shut"); if (st.shut[k]) delete st.shut[k]; else st.shut[k] = 1; d.emit("rack.port", { ip: h.ip, name: h.name || "", port: k.split(":")[1], shut: !!st.shut[k] }); keep(); draw(); panel(ip); }); });
      }
      w.body.addEventListener("click", function (e) { var b = e.target.closest("[data-ip]"); if (b && !e.target.closest(".rk-panel")) panel(b.getAttribute("data-ip")); });
      r("door").addEventListener("change", function () { st.door = this.checked; keep(); if (net) net.setDoor(this.checked); draw(); if (pp) pp.draw(); });
      r("csv").addEventListener("click", function () {
        d.emit("rack.export", { hosts: hosts.length, tagged: Object.keys(st.tag).length, shut: Object.keys(st.shut).length });
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

  function rdp() {
    var d = D(), cid = d.caseId();
    d.win("Remote desktop", "rdp", function (w) {
      w.body.innerHTML = '<div class="rd-pick"><p class="ws-empty">Loading…</p></div>';
      if (!cid) { w.body.innerHTML = '<p class="ws-empty">No case is open.</p>'; return; }
      d.files().then(function (fs) {
        var H = global.AayatMachine.evidence(fs), L = global.AayatLinux ? global.AayatLinux.evidence(fs) : {}, names = Object.keys(H).sort(), lnames = Object.keys(L).filter(function (h) { return !H[h]; }).sort();
        if (!names.length && !lnames.length) { w.body.innerHTML = '<p class="ws-empty">This case has no machines with saved evidence.</p>'; return; }
        w.body.innerHTML = '<div class="rd-pick"><h3>Connect to a machine</h3><p>Each machine below is rebuilt from the case’s saved evidence: its processes, logs, services, sign-ins and the files they mention, as the incident team captured them.</p>' +
          names.map(function (h) { return '<button type="button" class="rd-host" data-h="' + esc(h) + '">' + d.icon("rdp", 36) + "<span><b>" + esc(h) + "</b><small>Windows · " + H[h].procs.length + " processes · " + H[h].logs.length + " event logs" + (H[h].services.length ? " · " + H[h].services.length + " services" : "") + "</small></span></button>"; }).join("") +
          lnames.map(function (h) { var x = L[h], n = Object.keys(x.logs).reduce(function (a, f) { return a + x.logs[f].length; }, 0); return '<button type="button" class="rd-host" data-l="' + esc(h) + '">' + d.icon("terminal", 36) + "<span><b>" + esc(h) + "</b><small>Linux · " + n + " log lines" + (x.ps ? " · process list" : "") + (x.cron.length ? " · cron" : "") + (x.units.length ? " · " + x.units.length + " unit files" : "") + "</small></span></button>"; }).join("") + "</div>";
        w.body.querySelectorAll("[data-h]").forEach(function (b) { b.addEventListener("click", function () { var h = b.getAttribute("data-h"); global.AayatMachine.mount(w, { host: h, fs: fs, evidence: H[h] }); }); });
        w.body.querySelectorAll("[data-l]").forEach(function (b) { b.addEventListener("click", function () { var h = b.getAttribute("data-l"); global.AayatLinux.mount(w, { host: h, fs: fs, evidence: L[h] }); }); });
      });
    }, { w: 1000, h: 620 });
  }

  function netlab() {
    var d = D();
    var PROGS = [
      ["netstarter", "Network Starter", "Labs 1 to 3", "Made for a first network. Design mode to place computers, switches and routers and cable them; Simulation mode to use each computer's desktop: command line, web browser, web and DNS servers, and its data exchange."],
      ["netsim", "Network Simulator", "Labs 4 to 7", "Switch and router models with real IOS commands: VLANs, trunks, port security and access lists. Link lights, cable types, and a Simulation mode that steps one packet at a time."],
      ["netemu", "Network Emulator", "Lab 8", "Nodes you start and stop, a console tab for each, interface labels, and a capture on any link that lists every packet layer by layer."]
    ];
    function which(id) { var n = +((/^sem-n0*(\d+)/.exec(id) || [])[1] || 0); return n >= 8 ? "netemu" : n >= 4 ? "netsim" : "netstarter"; }
    function name(id) { return PROGS.filter(function (p) { return p[0] === id; })[0][1]; }
    d.win("Network lab", "net", function (w) {
      w.body.classList.add("ws-app-body");
      w.body.innerHTML = '<div class="ws-help"><h3>Network lab</h3><p>Every network lab runs in one of three programs on this desktop, with its starting network and its goals. Open a lab below, or open a program from the Start menu to build anything you like.</p>' +
        '<div class="ws-netprogs">' + PROGS.map(function (p) { return '<div class="ws-netprog"><b>' + d.esc(p[1]) + "</b><small>" + d.esc(p[2]) + "</small><p>" + d.esc(p[3]) + '</p><button type="button" class="btn dark" data-prog="' + p[0] + '">Open ' + d.esc(p[1]) + "</button></div>"; }).join("") + "</div>" +
        '<h4>The labs</h4><ol class="ws-netlabs"><li>Loading…</li></ol></div>';
      w.body.querySelectorAll("[data-prog]").forEach(function (b) { b.addEventListener("click", function () { if (!d.run("tool-" + b.getAttribute("data-prog"), {})) d.toast("That program is not available here."); }); });
      var list = w.body.querySelector(".ws-netlabs");
      fetch(base + "assets/linux/cases/index.json").then(function (r) { return r.json(); }).then(function (all) {
        var labs = all.filter(function (c) { return /^sem-n\d+-[a-z0-9-]+$/.test(c.id) && !/--(guided|solo)$/.test(c.id); });
        list.innerHTML = labs.map(function (c) {
          var p = which(c.id);
          return '<li><a target="_blank" rel="noopener" href="' + base + "workstation.html?case=" + encodeURIComponent(c.id) + "&open=tool-" + p + '">' + d.esc(c.title) + "</a> <small>" + d.esc(name(p) + (c.minutes ? " · about " + c.minutes + " min" : "")) + "</small> " + '<a target="_blank" rel="noopener" href="' + base + "notebook.html?ref=rb-" + encodeURIComponent(c.id.replace(/^sem-/, "")) + "&runbook=" + encodeURIComponent(c.id) + '">Steps</a></li>';
        }).join("") || "<li>No network labs yet.</li>";
      }).catch(function () { list.innerHTML = '<li><a target="_blank" rel="noopener" href="' + base + 'labs.html#lv-network">Open the Network lab on the Labs page</a></li>'; });
    }, { w: 760, h: 520 });
  }
  var base = (document.currentScript && document.currentScript.src || "").replace(/assets\/theme\/workstation-apps\.js.*$/, "");

  global.AayatDeskApps = [
    { id: "netlab", title: "Network lab", icon: "net", open: netlab },
    { id: "tickets", title: "Tickets", icon: "ticket", open: tickets },
    { id: "rack", title: "Server room", icon: "rack", open: rack },
    { id: "rdp", title: "Remote desktop", icon: "rdp", open: rdp }
  ];
})(window);
