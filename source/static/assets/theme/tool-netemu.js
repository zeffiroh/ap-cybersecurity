(function (global) {
  "use strict";
  var T = global.AayatTools, K = T.kit;
  var CSS = ".nem-box svg{background:#fff}.nem-box .nem-run .btn{min-width:30px}.nem-box .nem-go{color:#1d7a3a}.nem-box .nem-stop{color:#b02a2a}" +
    ".nem-box .nem-sum{list-style:none;margin:0 0 8px;padding:0}.nem-box .nem-sum li{display:flex;align-items:center;gap:6px;padding:3px 0;border-bottom:1px solid var(--m-line);cursor:pointer}.nem-box .nem-sum i{width:9px;height:9px;border-radius:50%;display:inline-block}" +
    ".nem-box .nem-sum small{margin-left:auto;color:var(--m-mute)}.nem-box .nem-cap{pointer-events:none}";
  var NAMES = { vpcs: "PC", linux: "Linux", ethsw: "Switch", hub: "Hub", iosvl2: "vIOS-L2-", iosv: "R" };
  var TYPE = { vpcs: "VPCS", linux: "Linux container", ethsw: "Ethernet switch", hub: "Ethernet hub", iosvl2: "IOSvL2 switch", iosv: "IOSv router" };

  function typeOf(d) {
    if (d.kind === "router") return "iosv";
    if (d.kind === "hub") return "hub";
    if (d.kind === "switch") return d.builtin ? "ethsw" : "iosvl2";
    return d.os === "vpcs" ? "vpcs" : "linux";
  }
  function mount(el, ctx) {
    var NK = global.AayatNetKit, C = NK && NK.core;
    if (!NK) { el.textContent = "The network kit did not load. Reload the page."; return; }
    var labels = true;
    K.css("tool-netemu-css", CSS);

    function up(d) { return d.power !== false; }
    function power(api, ids, on) {
      var D = api.doc(), n = 0;
      ids.forEach(function (id) { var d = C.dev(D, id); if (d && up(d) !== on) { d.power = on; n++; } });
      api.rebuild();
      if (ids.length === 1) api.msg((on ? "Started " : "Stopped ") + C.dev(D, ids[0]).name + ".");
      else api.msg(n ? (on ? "Started " : "Stopped ") + n + " node" + (n > 1 ? "s" : "") + "." : "All nodes were already " + (on ? "started." : "stopped."));
    }
    function all(api) { return api.doc().devices.map(function (d) { return d.id; }); }
    function suspend(api, i, on) {
      var D = api.doc(), c = D.cables[i];
      if (!c) return;
      D.suspended = D.suspended || {};
      if (on) D.suspended[C.ckey(c)] = 1; else delete D.suspended[C.ckey(c)];
      api.rebuild();
      api.msg((on ? "Suspended" : "Resumed") + " the link " + c[0] + " to " + c[1] + ".");
    }
    function menu(api, what) {
      var D = api.doc();
      if (what.dev) {
        var d = C.dev(D, what.dev);
        if (!d) return [];
        var items = [[up(d) ? "Stop" : "Start", function () { power(api, [d.id], !up(d)); }]];
        if (C.consoleKey(D, d.id)) items.push(["Console", function () { api.openConsole(d.id); }]);
        items.push(["Configure", function () { api.select(d.id); }], ["Delete", function () { C.removeDevice(D, d.id); api.select(""); api.rebuild(); api.msg("Deleted " + d.name + "."); }]);
        return items;
      }
      var c = D.cables[what.cable];
      if (!c) return [];
      var k = C.ckey(c), capturing = api.capLink() === k, susp = !!(D.suspended || {})[k];
      return [[capturing ? "Stop capture" : "Start capture", function () { if (capturing) api.stopCapture(); else api.capture(what.cable); }], [susp ? "Resume" : "Suspend", function () { suspend(api, what.cable, !susp); }], ["Delete", function () { D.cables.splice(what.cable, 1); api.rebuild(); api.msg("Deleted the link."); }]];
    }
    function summary(api) {
      var D = api.doc();
      api.side.innerHTML = "<h4>Topology summary</h4>" + (D.intro ? "<p><small>" + K.esc(D.intro) + "</small></p>" : "") +
        (D.devices.length ? '<ul class="nem-sum">' + D.devices.map(function (d) { return '<li data-id="' + K.esc(d.id) + '"><i style="background:' + (up(d) ? "#2ecc71" : "#c0392b") + '"></i>' + K.esc(d.name) + "<small>" + K.esc(TYPE[typeOf(d)]) + (up(d) ? "" : ", stopped") + "</small></li>"; }).join("") + "</ul>" : "<p>Add nodes from the bar. New nodes start stopped: press <b>&#9654; Start all</b>.</p>") +
        "<p><small>Right-click a node to start, stop or open its console. Right-click a link to capture on it or suspend it. A red dot on a link end means that node is stopped.</small></p>";
      api.side.querySelectorAll("[data-id]").forEach(function (li) { li.addEventListener("click", function () { api.select(li.getAttribute("data-id")); }); });
      return true;
    }
    function capMark(api) {
      var k = api.capLink(), D = api.doc();
      if (!k) return "";
      var c = D.cables.filter(function (x) { return C.ckey(x) === k; })[0];
      if (!c) return "";
      var a = api.pos(C.dev(D, C.ep(c[0]).id)), b = api.pos(C.dev(D, C.ep(c[1]).id)), x = (a.x + b.x) / 2, y = (a.y + b.y) / 2;
      return '<g class="nem-cap" transform="translate(' + x + " " + y + ')"><circle r="10" fill="#fff" stroke="#1f5f9e" stroke-width="2.4"/><circle r="5" fill="none" stroke="#1f5f9e" stroke-width="2"/><path d="M6 6L13 13" stroke="#1f5f9e" stroke-width="3"/></g>';
    }
    function banner(d) {
      if (d.os === "vpcs") return "Welcome to Virtual PC Simulator, version 0.8.3\nPress '?' to get help.\n\nExecuting the startup file\n\n";
      if (d.kind === "router" || d.kind === "switch") return "Connected to " + d.name + ".\nPress RETURN to get started.\n\n";
      return "Linux " + d.name + " 6.1 x86_64\n\n";
    }

    var bar = '<span class="sep"></span><span class="nbd-row nem-run"><button type="button" class="btn nem-go" data-r="startall" title="Start all nodes">&#9654; Start all</button><button type="button" class="btn nem-stop" data-r="stopall" title="Stop all nodes">&#9632; Stop all</button><button type="button" class="btn" data-r="reloadall" title="Reload all nodes">&#10227; Reload</button><button type="button" class="btn" data-r="conall" title="Open a console on every started node">Console to all</button></span>' +
      '<span class="sep"></span><label class="nbd-row"><input type="checkbox" data-r="plab" checked> Interface labels</label><button type="button" class="btn" data-r="zin" title="Zoom in">+</button><button type="button" class="btn" data-r="zout" title="Zoom out">&minus;</button>';
    var nk = NK.mount(el, ctx, {
      id: "netemu", title: "Network Emulator", cls: "nem-box",
      palette: [["vpcs", "VPCS", "pc", { os: "vpcs" }], ["linux", "Linux", "pc", { os: "linux" }], ["ethsw", "Ethernet switch", "switch", { builtin: true, ports: 8 }], ["hub", "Ethernet hub", "hub"], ["iosvl2", "IOSvL2", "switch"], ["iosv", "IOSv router", "router"]],
      tabs: [["goals", "Goals"], ["console", "Consoles"], ["capture", "Capture"]],
      cableLabel: "Add a link", bar: bar, lamps: true, consoleTabs: true, autoPort: false,
      noConsole: "No console is open. Double-click a started node, or right-click it and pick Console.",
      hostHelp: "Type help for the commands.",
      portLabels: function () { return labels; },
      portName: function (d, p) {
        var t = typeOf(d);
        if (t === "vpcs") return "e0";
        if (t === "linux") return "eth0";
        if (t === "ethsw" || t === "hub") return "e" + (+p - 1);
        if (t === "iosv") return "Gi" + String(p).slice(1);
        return C.portText(d, p);
      },
      added: function (api, d, key) {
        var n = 1, D = api.doc(), stem = NAMES[key] || "N";
        while (D.devices.some(function (x) { return x !== d && x.name === stem + n; })) n++;
        d.name = stem + n;
        if (d.kind === "router" || d.kind === "switch") d.hostname = d.name;
        d.power = false;
      },
      kindName: function (d) { return TYPE[typeOf(d)]; },
      sub: function (d) { return up(d) ? TYPE[typeOf(d)] : "stopped"; },
      form: { noOs: true, noAddr: function (d) { return d.os === "vpcs"; }, extra: function (d) { return d.os === "vpcs" ? "<p><small>" + (d.ip ? "Address " + K.esc(d.ip + "/" + (d.bits || 24)) + (d.gw ? ", gateway " + K.esc(d.gw) : "") + ". " : "No address yet. ") + "A VPCS node is set up in its console, for example: ip 10.0.0.1/24 10.0.0.254</small></p>" : ""; } },
      gate: function (api, id) { var d = C.dev(api.doc(), id); return d && !up(d) ? d.name + " is stopped. Start it first: right-click it and pick Start, or press Start all." : ""; },
      onConsole: function (api, id, c) { if (!c.out) c.out = banner(C.dev(api.doc(), id)); },
      menu: menu,
      overview: summary,
      drawExtra: capMark
    });
    if (!nk) return;
    nk.F.r("startall").addEventListener("click", function () { power(nk, all(nk), true); });
    nk.F.r("stopall").addEventListener("click", function () { power(nk, all(nk), false); });
    nk.F.r("reloadall").addEventListener("click", function () { var D = nk.doc(); D.devices.forEach(function (d) { if (up(d)) d.power = true; }); nk.rebuild(); nk.msg("Reloaded the started nodes."); });
    nk.F.r("conall").addEventListener("click", function () {
      var ids = nk.doc().devices.filter(function (d) { return up(d) && C.consoleKey(nk.doc(), d.id); }).map(function (d) { return d.id; });
      if (!ids.length) { nk.msg("No started node has a console. Press Start all first.", true); return; }
      ids.forEach(function (id) { nk.openConsole(id); });
    });
    nk.F.r("plab").addEventListener("change", function (e) { labels = e.target.checked; nk.draw(); });
    nk.F.r("zin").addEventListener("click", function () { nk.zoom(nk.zoom() / 1.2); });
    nk.F.r("zout").addEventListener("click", function () { nk.zoom(nk.zoom() * 1.2); });
  }

  global.AayatTools.register({ id: "netemu", title: "Network Emulator", console: true, group: "Security engineer", mount: mount });
})(window);
