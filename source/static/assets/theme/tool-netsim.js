(function (global) {
  "use strict";
  var T = global.AayatTools, K = T.kit;
  var CSS = ".nsm-box svg{background:#f7f9fc}.nsm-box .nsm-rt .btn{min-width:84px}.nsm-box .nsm-env{pointer-events:none}" +
    ".nsm-box .nsm-ctrl{display:flex;flex-wrap:wrap;gap:6px;align-items:center;margin:6px 0}.nsm-box .nsm-filt label{display:inline-flex;gap:3px;align-items:center;margin-right:8px;font-size:12px}" +
    ".nsm-box .nsm-ev{max-height:220px;overflow:auto;border:1px solid var(--m-line);background:var(--m-win)}.nsm-box .nsm-ev table{border-collapse:collapse;width:100%;font:11.5px ui-monospace,Consolas,monospace}" +
    ".nsm-box .nsm-ev td,.nsm-box .nsm-ev th{padding:2px 6px;border-bottom:1px solid var(--m-line);text-align:left;white-space:nowrap}.nsm-box .nsm-ev tr.ev{cursor:pointer}.nsm-box .nsm-ev tr.on td{background:var(--m-sel)}.nsm-box .nsm-ev tr.drop td{color:#a12}" +
    ".nsm-box .nsm-sq{display:inline-block;width:11px;height:9px;border:1px solid #0006;margin-right:5px;vertical-align:middle}" +
    ".nsm-box .nsm-pdu{border:1px solid var(--m-line);background:var(--m-win);padding:6px 8px;font:11.5px/1.5 ui-monospace,Consolas,monospace;max-height:220px;overflow:auto}.nsm-box .nsm-pdu b{display:block;margin-top:4px}.nsm-box .nsm-pdu .bad{color:#a12}" +
    ".nsm-box .nsm-split{display:grid;grid-template-columns:minmax(0,1.4fr) minmax(0,1fr);gap:8px}@media (max-width:820px){.nsm-box .nsm-split{grid-template-columns:1fr}}";
  var MODEL = { pc: "PC-PT", laptop: "Laptop-PT", server: "Server-PT", hub: "Hub-PT", "switch": "2960-24TT", router: "1941" };
  var BASE = { pc: "PC", laptop: "Laptop", server: "Server", hub: "Hub", "switch": "Switch", router: "Router" };
  var COLOR = { ARP: "#f2d14b", ICMP: "#b07ce8", DNS: "#5aa9e6", TCP: "#7fcf5a", HTTP: "#3fa34d" };
  var TYPES = ["ARP", "ICMP", "DNS", "TCP", "HTTP"];

  function mount(el, ctx) {
    var NK = global.AayatNetKit, C = NK && NK.core, Nt = global.AayatNet;
    if (!NK) { el.textContent = "The network kit did not load. Reload the page."; return; }
    var simOn = false, events = [], cur = -1, known = {}, filt = { ARP: 1, ICMP: 1, DNS: 1, TCP: 1, HTTP: 1 }, timer = null, ctype = "auto", labels = false, pduFrom = "", anim = null;
    K.css("tool-netsim-css", CSS);

    function shown() { return events.filter(function (e) { return filt[e.proto]; }); }
    function addEvents(api, f) {
      var list = C.simEvents(api.doc(), api.model(), f, known);
      list.forEach(function (e) { e.n = events.length + 1; e.time = (events.length * 0.001).toFixed(3); events.push(e); });
      if (list.length) api.msg("Simulation: " + list.length + " events queued. Press Capture / Forward to move the packet one step.");
      if (api.tab() === "events") renderEvents(api);
    }
    function devName(api, id) { var d = C.dev(api.doc(), id); return d ? d.name : id; }
    function step(api, dir) {
      var list = shown();
      if (!list.length) { api.msg("No events yet. Send a ping or a PDU while in Simulation mode.", true); return false; }
      var ix = list.indexOf(events[cur]), nx = ix + dir;
      if (ix < 0) nx = dir > 0 ? 0 : -1;
      if (nx < 0 || nx >= list.length) { stop(); api.msg(dir > 0 ? "No more events. Reset the simulation to start again." : "This is the first event."); return false; }
      var e = list[nx];
      cur = events.indexOf(e);
      animate(api, e);
      api.msg("Event " + e.n + ": " + e.proto + " at " + devName(api, e.at) + (e.drop ? ", dropped" : ""), !!e.drop);
      if (api.tab() === "events") renderEvents(api);
      return true;
    }
    function stop() { if (timer) { clearInterval(timer); timer = null; } }
    function play(api) {
      if (timer) { stop(); renderEvents(api); return; }
      timer = setInterval(function () { if (!step(api, 1)) { stop(); renderEvents(api); } }, 900);
      renderEvents(api);
    }
    function resetSim(api) { stop(); events = []; cur = -1; known = {}; anim = null; api.draw(); renderEvents(api); api.msg("Simulation reset."); }
    function animate(api, e) {
      var D = api.doc(), a = C.dev(D, e.last), b = C.dev(D, e.at);
      if (!a || !b) { anim = null; api.draw(); return; }
      anim = { from: api.pos(a), to: api.pos(b), t0: performance.now(), e: e };
      api.draw();
      function tick(now) {
        if (!anim || anim.e !== e) return;
        var g = api.svg.querySelector(".nsm-env");
        if (!g) return;
        var k = Math.min(1, (now - anim.t0) / 520), x = anim.from.x + (anim.to.x - anim.from.x) * k, y = anim.from.y + (anim.to.y - anim.from.y) * k;
        g.setAttribute("transform", "translate(" + x.toFixed(1) + " " + y.toFixed(1) + ")");
        if (k < 1) requestAnimationFrame(tick);
      }
      requestAnimationFrame(tick);
    }
    function envelope(api) {
      if (!anim || !simOn) return "";
      var e = anim.e, p = anim.to, col = COLOR[e.proto] || "#ccc";
      return '<g class="nsm-env" transform="translate(' + p.x + " " + p.y + ')"><g transform="translate(-13 -44)"><rect width="26" height="17" rx="2" fill="' + col + '" stroke="#333" stroke-width="1"/><path d="M0 0L13 9L26 0" fill="none" stroke="#333" stroke-width="1"/>' +
        (e.drop ? '<path d="M-2 -3L28 20M28 -3L-2 20" stroke="#c0392b" stroke-width="3"/>' : "") + "</g></g>";
    }
    function renderEvents(api) {
      var pane = api.pane, list = shown(), ev = events[cur];
      pane.innerHTML = '<div class="nsm-ctrl">' + (simOn ? "" : '<span class="sx-empty">You are in Realtime mode. Press <b>Simulation</b> in the bar to queue packets here.</span>') +
        '<button type="button" class="btn" data-r="sback">&#9664; Back</button><button type="button" class="btn dark" data-r="sfwd">Capture / Forward &#9654;</button><button type="button" class="btn" data-r="splay">' + (timer ? "Pause" : "Play") + '</button><button type="button" class="btn" data-r="sreset">Reset simulation</button></div>' +
        '<div class="nsm-ctrl nsm-filt">Event filters: ' + TYPES.map(function (t) { return '<label><input type="checkbox" data-f="' + t + '"' + (filt[t] ? " checked" : "") + '><span class="nsm-sq" style="background:' + COLOR[t] + '"></span>' + t + "</label>"; }).join("") + "</div>" +
        '<div class="nsm-split"><div class="nsm-ev"><table><tr><th>Vis.</th><th>Time (sec)</th><th>Last device</th><th>At device</th><th>Type</th><th>Info</th></tr>' +
        list.map(function (e) { return '<tr class="ev' + (e === ev ? " on" : "") + (e.drop ? " drop" : "") + '" data-n="' + e.n + '"><td>' + (e === ev ? "&#128065;" : "") + "</td><td>" + e.time + "</td><td>" + K.esc(devName(api, e.last)) + "</td><td>" + K.esc(devName(api, e.at)) + '</td><td><span class="nsm-sq" style="background:' + (COLOR[e.proto] || "#ccc") + '"></span>' + e.proto + "</td><td>" + K.esc(e.info || "") + "</td></tr>"; }).join("") +
        '</table></div><div class="nsm-pdu">' + pdu(api, ev) + "</div></div>" + (list.length ? "" : "<p><small>No events yet. In Simulation mode, ping from a console or use Add Simple PDU.</small></p>");
      pane.querySelector('[data-r="sback"]').addEventListener("click", function () { stop(); step(api, -1); });
      pane.querySelector('[data-r="sfwd"]').addEventListener("click", function () { stop(); step(api, 1); });
      pane.querySelector('[data-r="splay"]').addEventListener("click", function () { play(api); });
      pane.querySelector('[data-r="sreset"]').addEventListener("click", function () { resetSim(api); });
      pane.querySelectorAll("[data-f]").forEach(function (b) { b.addEventListener("change", function () { filt[b.getAttribute("data-f")] = b.checked ? 1 : 0; renderEvents(api); }); });
      pane.querySelectorAll("tr.ev").forEach(function (tr) {
        tr.addEventListener("click", function () {
          var e = events[+tr.getAttribute("data-n") - 1];
          if (!e) return;
          stop();
          cur = e.n - 1;
          animate(api, e);
          api.msg("Event " + e.n + ": " + e.proto + " at " + devName(api, e.at) + (e.drop ? ", dropped" : ""), !!e.drop);
          renderEvents(api);
        });
      });
    }
    function pdu(api, e) {
      if (!e) return "<small>Click an event, or press Capture / Forward, to see the PDU at that device.</small>";
      var h = "<b>PDU Information at Device: " + K.esc(devName(api, e.at)) + "</b><div>Came from: " + K.esc(devName(api, e.last)) + "</div>" + (e.vlan ? "<div>802.1Q tag: VLAN " + e.vlan + "</div>" : "");
      if (e.drop) h += '<div class="bad">' + K.esc(e.why || (e.proto === "ARP" ? "This device does not own the address asked for, so it ignores the request." : "The device drops the packet.")) + "</div>";
      return h + (e.layers || []).map(function (l, i) { return "<b>Layer " + [2, 2, 3, 4][Math.min(i, 3)] + ": " + K.esc(l.t) + "</b>" + l.rows.map(function (r) { return "<div>&nbsp;&nbsp;" + K.esc(r) + "</div>"; }).join(""); }).join("");
    }
    function sendPdu(api, from, to) {
      var M = api.model(), fd = C.dev(api.doc(), from), td = C.dev(api.doc(), to), ip = (Nt.ifaces(M, to).filter(function (f) { return f.ip; })[0] || {}).ip;
      if (!(Nt.ifaces(M, from).filter(function (f) { return f.ip; })[0])) { api.msg(fd.name + " has no IP address, so it cannot send.", true); return; }
      if (!ip) { api.msg(td.name + " has no IP address to send to.", true); return; }
      var r = Nt.route(M, from, ip);
      api.logFlow({ kind: "icmp", from: from, to: ip, ok: r.ok, r: r, count: 1, quiet: true });
      api.msg("Simple PDU " + fd.name + " to " + td.name + ": " + (r.ok ? "Successful" : "Failed"), !r.ok);
      api.goals();
    }
    function setSim(api, on) {
      simOn = !!on;
      stop();
      api.F.r("rt").classList.toggle("on", !simOn);
      api.F.r("sm").classList.toggle("on", simOn);
      anim = null;
      api.draw();
      api.setTab(simOn ? "events" : api.tab() === "events" ? "goals" : api.tab());
      api.msg(simOn ? "Simulation mode: ping or send a PDU, then step through the events." : "Realtime mode.");
    }

    var bar = '<span class="sep"></span><label class="nbd-row" title="Connections">Cable <select data-r="ctype"><option value="auto">Automatic</option><option value="straight">Copper Straight-Through</option><option value="cross">Copper Cross-Over</option></select></label>' +
      '<label class="nbd-row"><input type="checkbox" data-r="plab"> Port labels</label><button type="button" class="btn" data-r="mode-pdu" title="Add Simple PDU: a single ping from one device to another">&#9993; Add Simple PDU</button>' +
      '<span class="sep"></span><span class="nbd-row nsm-rt"><button type="button" class="btn on" data-r="rt">&#9201; Realtime</button><button type="button" class="btn" data-r="sm">&#9654; Simulation</button></span>';
    var nk = NK.mount(el, ctx, {
      id: "netsim", title: "Network Simulator", cls: "nsm-box",
      palette: [["pc", "PC"], ["laptop", "Laptop"], ["server", "Server"], ["switch", "Switch 2960"], ["router", "Router 1941"], ["hub", "Hub"]],
      tabs: [["goals", "Goals"], ["console", "CLI and Desktop"], ["events", "Simulation panel"], ["capture", "Capture"]],
      cableLabel: "Connect", bar: bar, lamps: true,
      help: "Add devices from the bar. Choose <b>Connect</b> and click two devices to cable them; link lights turn green when both ends are up. Click a device to set it up, double-click it for its CLI or Command Prompt.",
      hostHelp: "Command Prompt. Type help for the commands. Set the address in IP Configuration on the right.",
      portLabels: function () { return labels; },
      portName: function (d, p) { return d.kind === "router" ? "Gig" + String(p).slice(1) : C.isHost(d) ? "Fa0" : C.portText(d, p); },
      autoPort: function () { return ctype === "auto"; },
      cableType: function () { return ctype === "auto" ? "" : ctype; },
      onCable: function (api, c) {
        var D = api.doc(), a = C.dev(D, C.ep(c[0]).id), b = C.dev(D, C.ep(c[1]).id);
        if (!(a && b && (a.kind === "switch" || b.kind === "switch"))) return;
        D.settle = D.settle || {};
        D.settle[C.ckey(c)] = Date.now() + 3000;
        setTimeout(function () { if (D === api.doc()) { delete D.settle[C.ckey(c)]; api.rebuild(true); } }, 3100);
      },
      added: function (api, d) {
        var n = api.doc().devices.filter(function (x) { return x !== d && x.kind === d.kind; }).length;
        d.name = BASE[d.kind] + n;
        if (d.kind === "switch" || d.kind === "router") d.hostname = BASE[d.kind];
        d.model = MODEL[d.kind];
      },
      kindName: function (d) { return MODEL[d.kind] || d.kind; },
      sub: function (d) { return d.model || MODEL[d.kind] || ""; },
      form: { noOs: true },
      modeText: { pdu: "Add Simple PDU: click the source device, then the destination." },
      onPick: function (api, id, mode) {
        if (mode !== "pdu") return false;
        if (!pduFrom || !C.dev(api.doc(), pduFrom)) { pduFrom = id; api.msg("Source: " + devName(api, id) + ". Now click the destination."); return true; }
        if (pduFrom === id) return true;
        var a = pduFrom;
        pduFrom = "";
        api.setMode("select", true);
        sendPdu(api, a, id);
        return true;
      },
      onFlow: function (api, f) { if (simOn) addEvents(api, f); },
      drawExtra: envelope,
      pane: function (api, tab) { if (tab === "events") { renderEvents(api); return true; } return false; }
    });
    if (!nk) return;
    nk.F.r("mode-pdu").addEventListener("click", function () { pduFrom = ""; nk.setMode("pdu"); });
    nk.F.r("ctype").addEventListener("change", function (e) { ctype = e.target.value; nk.msg(ctype === "auto" ? "Automatic: the right cable and the first free ports." : (ctype === "cross" ? "Cross-over" : "Straight-through") + " cable: click two devices, then pick their ports."); });
    nk.F.r("plab").addEventListener("change", function (e) { labels = e.target.checked; nk.draw(); });
    nk.F.r("rt").addEventListener("click", function () { setSim(nk, false); });
    nk.F.r("sm").addEventListener("click", function () { setSim(nk, true); });
  }

  global.AayatTools.register({ id: "netsim", title: "Network Simulator", console: true, group: "Security engineer", mount: mount });
})(window);
