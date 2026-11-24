(function (global) {
  "use strict";
  var PRIV = /^(10\.|192\.168\.|172\.(1[6-9]|2\d|3[01])\.|127\.)/;
  var WAN = "100.64.0.2", ISP = "100.64.0.1";
  var HOSTLIKE = { pc: 1, laptop: 1, server: 1, printer: 1, camera: 1, phone: 1, nas: 1, wifirouter: 1 };
  var ROUTERS = { router: 1, firewall: 1 };
  var SWITCHES = { "switch": 1, ap: 1 };

  function clone(o) { return JSON.parse(JSON.stringify(o)); }
  function ipNum(ip) {
    var p = String(ip || "").trim().split(".");
    if (p.length !== 4 || p.some(function (x) { return !/^\d+$/.test(x) || +x > 255; })) return null;
    return ((+p[0] << 24) >>> 0) + (+p[1] << 16) + (+p[2] << 8) + +p[3];
  }
  function numIp(n) { return [n >>> 24, (n >>> 16) & 255, (n >>> 8) & 255, n & 255].join("."); }
  function maskOf(bits) { return bits === 0 ? 0 : (~0 << (32 - bits)) >>> 0; }
  function maskText(bits) { return numIp(maskOf(bits)); }
  function bitsOf(mask) { var n = ipNum(mask); if (n === null) return null; var b = 0; while (b < 32 && (n & (0x80000000 >>> b))) b++; return maskOf(b) === n ? b : null; }
  function cidr(s) {
    var m = /^\s*([\d.]+)(?:\/(\d+))?\s*$/.exec(String(s || ""));
    if (!m || ipNum(m[1]) === null) return null;
    return { ip: m[1], bits: m[2] == null ? 24 : Math.min(32, +m[2]) };
  }
  function inNet(ip, net, bits) { var a = ipNum(ip), b = ipNum(net); if (a === null || b === null) return false; var k = maskOf(bits); return ((a & k) >>> 0) === ((b & k) >>> 0); }
  function netAddr(ip, bits) { return numIp((ipNum(ip) & maskOf(bits)) >>> 0); }
  function hash(s) { var h = 2166136261; for (var i = 0; i < s.length; i++) { h ^= s.charCodeAt(i); h = Math.imul(h, 16777619) >>> 0; } return h; }
  function mac(id) { var h = hash(id), g = hash(id + "x"); return ["02", (h >>> 24) & 255, (h >>> 16) & 255, (h >>> 8) & 255, h & 255, g & 255].map(function (x, i) { return i ? ("0" + x.toString(16)).slice(-2) : x; }).join(":"); }
  function vlans(spec) {
    spec = String(spec == null ? "all" : spec).trim().toLowerCase();
    if (spec === "all" || spec === "") return null;
    if (spec === "none") return [];
    var out = [];
    spec.split(",").forEach(function (x) {
      var m = /^(\d+)(?:-(\d+))?$/.exec(x.trim());
      if (!m) return;
      for (var v = +m[1]; v <= +(m[2] || m[1]) && v < 4095; v++) out.push(v);
    });
    return out;
  }
  function vlanText(list) {
    if (list == null) return "all";
    if (!list.length) return "none";
    var s = list.slice().sort(function (a, b) { return a - b; }), out = [], a = s[0], b = s[0];
    for (var i = 1; i <= s.length; i++) {
      if (s[i] === b + 1) { b = s[i]; continue; }
      out.push(a === b ? String(a) : a + "-" + b);
      a = b = s[i];
    }
    return out.join(",");
  }
  function allowed(p, v) { var l = vlans(p.allowed); return l == null || l.indexOf(v) >= 0; }

  function kindOf(h) {
    var n = (h.name || "").toLowerCase(), svcs = (h.ports || []).map(function (p) { return p.svc + " " + (p.ver || "") + " " + (p.title || ""); }).join(" ").toLowerCase();
    if (!h.internal) return "internet";
    if (/gateway|router|^gw|edge-fw|firewall|fw\d/.test(n)) return "router";
    if (/switch|^sw\d/.test(n)) return "switch";
    if (/wireless n router|wi-?fi router|tl-wr|access point/.test(svcs + " " + n)) return "wifirouter";
    if (/printer|jetdirect/.test(n + " " + svcs)) return "printer";
    if (/nvr|cam|cctv/.test(n)) return "camera";
    if (/laptop|-lt\d|lt\d\d/.test(n)) return "laptop";
    if (/pc|ws\d|desk|till|-ws/.test(n) || (/ms-wbt-server|netbios|microsoft-ds/.test(svcs) && !/dc|srv|server|file|fs\d|db|nas|backup|mail/.test(n))) return "pc";
    return "server";
  }
  function osOf(h, kind) {
    var t = String(h.os || "").toLowerCase(), svcs = (h.ports || []).map(function (p) { return p.svc; }).join(" ");
    if (/windows/.test(t) || (!t && /microsoft-ds|ms-wbt|netbios/.test(svcs))) return "windows";
    if (kind === "router" || kind === "switch" || kind === "ap") return "netos";
    return "linux";
  }

  function parseHosts(hostsText, dnsText) {
    var hosts = {}, names = {};
    String(dnsText || "").split("\n").forEach(function (l) { var p = l.trim().split(/\s+/); if (p[0] === "A" && p[2]) names[p[2]] = names[p[2]] || p[1]; });
    String(hostsText || "").split("\n").forEach(function (l) {
      var f = l.replace(/\r$/, "").split("|");
      if (f.length < 3) return;
      if (f[0] === "os") { (hosts[f[1]] = hosts[f[1]] || { ip: f[1], name: "", ports: [] }).os = [f[2], f[3]].filter(Boolean).join(" "); return; }
      var h = hosts[f[0]] = hosts[f[0]] || { ip: f[0], name: "", ports: [] };
      if (f[1]) h.name = f[1];
      h.ports.push({ port: +f[2], proto: f[3], svc: f[4], ver: f[5], flag: f[6] === "1", title: f[7] || "" });
    });
    return Object.keys(hosts).map(function (ip) { var h = hosts[ip]; if (!h.name) h.name = names[ip] || ""; h.internal = PRIV.test(ip); return h; });
  }

  function fromHosts(list, title) {
    var inside = (list || []).filter(function (h) { return PRIV.test(h.ip); });
    var outside = (list || []).filter(function (h) { return !PRIV.test(h.ip); });
    var M = { title: title || "", dev: {}, sw: {}, links: [], tasks: [], rooms: {}, outside: {}, auto: true, vlanNames: {} };
    inside.forEach(function (h) { h.kind = h.kind || kindOf(Object.assign({ internal: true }, h)); });
    var gwH = inside.filter(function (h) { return h.kind === "router"; })[0] || inside.filter(function (h) { return /\.1$/.test(h.ip); })[0];
    var first = gwH || inside[0];
    var lan = first ? netAddr(first.ip, 24) : "10.0.0.0";
    var gwIp = gwH ? gwH.ip : numIp(ipNum(lan) + 1);
    var gwId = gwH ? short(gwH) : "gw";
    var swH = inside.filter(function (h) { return h.kind === "switch"; })[0];
    var swId = swH ? short(swH) : "sw1";
    var rest = inside.filter(function (h) { return h !== gwH && h !== swH; }).sort(function (a, b) { return rank(a.kind) - rank(b.kind) || ipNum(a.ip) - ipNum(b.ip); });
    var nets = [lan];
    inside.forEach(function (h) { var nt = netAddr(h.ip, 24); if (nets.indexOf(nt) < 0) nets.push(nt); });
    var used = {};
    inside.forEach(function (h) { used[h.ip] = 1; });
    var ifs = { "g0/1": { ip: WAN, bits: 30, wan: true } }, gwOf = {}, vlanOf = {};
    nets.forEach(function (nt, k) {
      var ip = k === 0 ? gwIp : used[numIp(ipNum(nt) + 1)] ? numIp(ipNum(nt) + 254) : numIp(ipNum(nt) + 1);
      ifs[k === 0 ? "g0/0" : "g0/" + (k + 1)] = { ip: ip, bits: 24 };
      gwOf[nt] = ip;
      vlanOf[nt] = k === 0 ? 1 : k * 10;
      if (k) M.vlanNames[swId + ":" + k * 10] = "net-" + nt.split(".").slice(0, 3).join("-");
    });
    M.dev[gwId] = { id: gwId, name: gwH ? (gwH.name || gwH.ip) : "gateway", kind: "router", os: "netos", room: "comms cupboard", ifs: ifs, routes: [{ net: "0.0.0.0/0", via: ISP }], svc: gwH ? gwH.ports : [] };
    M.dev[swId] = { id: swId, name: swH ? (swH.name || swH.ip) : "sw1", kind: "switch", os: "netos", room: "comms cupboard", ip: swH ? swH.ip : "", bits: 24, mvlan: swH ? vlanOf[netAddr(swH.ip, 24)] : 1, svc: swH ? swH.ports : [] };
    var n = Math.max(8, Math.ceil((rest.length + nets.length + 2) / 8) * 8), ports = {}, desk = 0, at = 1;
    for (var i = 1; i <= n; i++) ports[i] = { n: i, mode: "access", vlan: 1, socket: "", room: "", to: null };
    nets.forEach(function (nt, k) { var p = ports[at++]; p.to = gwId + ":" + (k === 0 ? "g0/0" : "g0/" + (k + 1)); p.room = "comms cupboard"; p.socket = "-"; p.vlan = vlanOf[nt]; });
    rest.forEach(function (h) {
      var id = short(h), kind = h.kind, office = !(kind === "server" || kind === "camera"), nt = netAddr(h.ip, 24);
      M.dev[id] = { id: id, name: h.name || h.ip, kind: kind, os: osOf(h, kind), ip: h.ip, bits: 24, gw: gwOf[nt], room: office ? "office" : "comms cupboard", usb: kind === "pc" || kind === "laptop" ? true : undefined, svc: h.ports || [] };
      var p = ports[at++];
      p.to = id + ":eth0";
      p.room = M.dev[id].room;
      p.vlan = vlanOf[nt];
      p.socket = office ? "D" + (++desk) : "-";
    });
    for (var j = at; j <= n; j++) { ports[j].room = "office"; ports[j].socket = "D" + (++desk); }
    M.sw[swId] = ports;
    M.dev.internet = { id: "internet", name: "Internet", kind: "internet", os: "netos", ifs: { eth0: { ip: ISP, bits: 30 } } };
    M.links.push([gwId + ":g0/1", "internet:eth0"]);
    outside.forEach(function (h) { if (h.ip) M.outside[h.ip] = h.name || h.ip; });
    return M;
  }
  function short(h) { return String(h.name || h.ip).split(".")[0].toLowerCase().replace(/[^a-z0-9-]/g, "") || String(h.ip).replace(/\./g, "-"); }
  var RANK = { server: 0, camera: 1, wifirouter: 2, printer: 3, pc: 4, laptop: 5 };
  function rank(k) { return RANK[k] == null ? 6 : RANK[k]; }

  function normalize(json, hosts) {
    if (!json || !json.devices) {
      var A = fromHosts(hosts, json && json.title);
      if (json) { A.tasks = json.tasks || []; A.intro = json.intro || ""; A.rooms = json.rooms || {}; }
      return A;
    }
    var M = { title: json.title || "", dev: {}, sw: {}, links: [], tasks: json.tasks || [], rooms: json.rooms || {}, outside: {}, intro: json.intro || "", vlanNames: {} };
    (hosts || []).forEach(function (h) { if (!PRIV.test(h.ip)) M.outside[h.ip] = h.name || h.ip; });
    Object.keys(json.outside || {}).forEach(function (ip) { M.outside[ip] = json.outside[ip]; });
    json.devices.forEach(function (d) {
      var o = clone(d), c = o.ip ? cidr(o.ip) : null;
      o.kind = o.kind || "pc";
      o.os = o.os || (ROUTERS[o.kind] || SWITCHES[o.kind] ? "netos" : "linux");
      o.name = o.name || o.id;
      if (c) { o.ip = c.ip; o.bits = c.bits; }
      if (o.ifs) Object.keys(o.ifs).forEach(function (k) {
        var f = o.ifs[k];
        if (typeof f === "string") f = o.ifs[k] = f === "wan" ? { ip: WAN, bits: 30, wan: true } : Object.assign({}, cidr(f));
        if (f.ip && f.ip.indexOf("/") > 0) { var cc = cidr(f.ip); f.ip = cc.ip; f.bits = cc.bits; }
        if (k.indexOf(".") > 0) { f.parent = f.parent || k.split(".")[0]; f.vlan = f.vlan || +k.split(".")[1]; }
      });
      if (ROUTERS[o.kind] && o.ifs && !o.routes && Object.keys(o.ifs).some(function (k) { return o.ifs[k].wan; })) o.routes = [{ net: "0.0.0.0/0", via: ISP }];
      if (SWITCHES[o.kind]) {
        var ports = {};
        for (var i = 1; i <= (o.ports || 8); i++) ports[i] = { n: i, mode: "access", vlan: 1, socket: "", room: "", to: null };
        o.ports = undefined;
        M.sw[o.id] = ports;
        if (o.vlans) Object.keys(o.vlans).forEach(function (v) { M.vlanNames[o.id + ":" + v] = o.vlans[v]; });
      }
      if (o.svc == null) {
        var h = (hosts || []).filter(function (x) { return x.ip === o.ip; })[0];
        o.svc = h ? h.ports : [];
      }
      M.dev[o.id] = o;
    });
    Object.keys(json.ports || {}).forEach(function (s) {
      (json.ports[s] || []).forEach(function (p) {
        var key = String(p.n);
        var base = M.sw[s][key] = Object.assign(M.sw[s][key] || { n: p.n, mode: "access", vlan: 1 }, clone(p));
        if (base.to && base.to.indexOf(":") < 0) base.to = base.to + ":" + defIf(M, base.to);
      });
    });
    Object.keys(M.sw).forEach(function (s) {
      Object.keys(M.sw[s]).forEach(function (n) {
        var to = M.sw[s][n].to;
        if (!to) return;
        var e = split(to);
        if (M.sw[e.id] && M.sw[e.id][e.port] && !M.sw[e.id][e.port].to) M.sw[e.id][e.port].to = s + ":" + n;
      });
    });
    (json.links || []).forEach(function (l) { M.links.push([l[0].indexOf(":") < 0 ? l[0] + ":" + defIf(M, l[0]) : l[0], l[1].indexOf(":") < 0 ? l[1] + ":" + defIf(M, l[1]) : l[1]]); });
    if (Object.keys(M.dev).some(function (k) { var d = M.dev[k]; return d.ifs && Object.keys(d.ifs).some(function (f) { return d.ifs[f].wan; }); }) && !M.dev.internet) {
      M.dev.internet = { id: "internet", name: "Internet", kind: "internet", os: "netos", ifs: { eth0: { ip: ISP, bits: 30 } } };
      Object.keys(M.dev).forEach(function (k) { var d = M.dev[k]; if (d.ifs) Object.keys(d.ifs).forEach(function (f) { if (d.ifs[f].wan && !d.ifs[f].parent) M.links.push([k + ":" + f, "internet:eth0"]); }); });
    }
    return M;
  }
  function defIf(M, id) {
    var d = M.dev[id];
    if (!d) return "eth0";
    if (d.ifs) return Object.keys(d.ifs).filter(function (k) { return k.indexOf(".") < 0; })[0] || "eth0";
    if (M.sw[id]) return "1";
    return "eth0";
  }

  function blank() { return { p: {}, d: {}, i: {}, rules: {}, door: false, vl: {}, routes: {} }; }
  function merge(base, st) {
    var M = clone(base);
    st = st || blank();
    Object.keys(st.p || {}).forEach(function (k) {
      var s = k.split(":")[0], n = k.split(":")[1];
      if (!M.sw[s]) return;
      M.sw[s][n] = Object.assign(M.sw[s][n] || { n: +n, mode: "access", vlan: 1 }, st.p[k]);
    });
    Object.keys(st.d || {}).forEach(function (id) { if (M.dev[id]) Object.assign(M.dev[id], st.d[id]); });
    Object.keys(st.i || {}).forEach(function (k) {
      var id = k.split(":")[0], f = k.slice(id.length + 1), d = M.dev[id];
      if (!d) return;
      d.ifs = d.ifs || {};
      if (st.i[k] === null) { delete d.ifs[f]; return; }
      d.ifs[f] = Object.assign(d.ifs[f] || {}, st.i[k]);
      if (f.indexOf(".") > 0) { d.ifs[f].parent = f.split(".")[0]; d.ifs[f].vlan = d.ifs[f].vlan || +f.split(".")[1]; }
    });
    Object.keys(st.rules || {}).forEach(function (id) { if (M.dev[id]) M.dev[id].rules = st.rules[id]; });
    Object.keys(st.routes || {}).forEach(function (id) { if (M.dev[id]) M.dev[id].routes = st.routes[id]; });
    Object.keys(st.vl || {}).forEach(function (k) { M.vlanNames = M.vlanNames || {}; if (st.vl[k] === null) delete M.vlanNames[k]; else M.vlanNames[k] = st.vl[k]; });
    M.door = !!st.door;
    return M;
  }

  function cables(M) {
    var c = {};
    function link(a, b) { c[a] = c[a] || []; c[b] = c[b] || []; if (c[a].indexOf(b) < 0) c[a].push(b); if (c[b].indexOf(a) < 0) c[b].push(a); }
    Object.keys(M.sw).forEach(function (s) { Object.keys(M.sw[s]).forEach(function (n) { var p = M.sw[s][n]; if (p.to) link(s + ":" + n, p.to); }); });
    M.links.forEach(function (l) { link(l[0], l[1]); });
    return c;
  }
  function split(ep) { var i = ep.indexOf(":"); return { id: ep.slice(0, i), port: ep.slice(i + 1) }; }
  function on(M, id) { var d = M.dev[id]; return !!d && d.power !== false; }

  function ifaces(M, id) {
    var d = M.dev[id], out = [];
    if (!d) return out;
    if (d.ifs) Object.keys(d.ifs).forEach(function (k) { var f = d.ifs[k], par = f.parent || k.split(".")[0], pf = par !== k && d.ifs[par]; out.push({ name: k, ip: f.ip || "", bits: f.bits == null ? 24 : f.bits, vlan: f.vlan || 0, parent: par, shut: !!f.shut || !!(pf && pf.shut), wan: !!f.wan }); });
    else if (M.sw[id]) { if (d.ip) out.push({ name: "vlan" + (d.mvlan || 1), ip: d.ip, bits: d.bits || 24, vlan: d.mvlan || 1, svi: true, parent: "", shut: false }); }
    else out.push({ name: "eth0", ip: d.ip || "", bits: d.bits == null ? 24 : d.bits, vlan: 0, parent: "eth0", shut: false });
    return out;
  }

  function flood(M, C, start) {
    var seen = {}, reached = [];
    function send(ep, tag) { (C[ep] || []).forEach(function (peer) { arrive(peer, tag); }); }
    function inside(sid, v, skip) {
      var sw = M.sw[sid], d = M.dev[sid];
      if (d.ip && (d.mvlan || 1) === v) reached.push({ id: sid, ip: d.ip, bits: d.bits || 24, name: "vlan" + v });
      Object.keys(sw).forEach(function (n) {
        if (n === skip) return;
        var q = sw[n];
        if (q.shut || !q.to) return;
        if (q.mode === "trunk") { if (allowed(q, v)) send(sid + ":" + n, v === (+q.native || 1) ? 0 : v); }
        else if ((+q.vlan || 1) === v) send(sid + ":" + n, 0);
      });
    }
    function arrive(ep, tag) {
      var k = ep + "|" + tag;
      if (seen[k]) return;
      seen[k] = 1;
      var e = split(ep), d = M.dev[e.id];
      if (!d || d.power === false) return;
      var sw = M.sw[e.id];
      if (sw) {
        var p = sw[e.port];
        if (!p || p.shut) return;
        var v;
        if (p.mode === "trunk") { v = tag || +p.native || 1; if (!allowed(p, v)) return; }
        else { if (tag) return; v = +p.vlan || 1; }
        inside(e.id, v, e.port);
        return;
      }
      ifaces(M, e.id).forEach(function (f) {
        if (f.parent !== e.port || f.shut || !f.ip) return;
        if ((f.vlan || 0) === (tag || 0)) reached.push({ id: e.id, ip: f.ip, bits: f.bits, name: f.name });
      });
    }
    if (start.sw) inside(start.sw, start.vlan, null);
    else send(start.ep, start.tag || 0);
    return reached;
  }

  function linked(M, C, ep) {
    var peers = C[ep] || [];
    return peers.some(function (peer) { var e = split(peer); if (!on(M, e.id)) return false; var sw = M.sw[e.id]; return !sw || (sw[e.port] && !sw[e.port].shut); });
  }

  function lookup(M, name) {
    name = String(name || "").trim().toLowerCase().replace(/\.$/, "");
    if (ipNum(name) !== null) return name;
    var ids = Object.keys(M.dev);
    for (var i = 0; i < ids.length; i++) {
      var d = M.dev[ids[i]];
      if (d.kind === "internet") continue;
      var n = String(d.name || "").toLowerCase();
      if (ids[i] === name || n === name || n.split(".")[0] === name) { var f = ifaces(M, ids[i]).filter(function (x) { return x.ip && !x.wan; })[0]; if (f) return f.ip; }
    }
    var out = Object.keys(M.outside || {}).filter(function (ip) { var n = String(M.outside[ip]).toLowerCase(); return n === name || n.split(".")[0] === name; })[0];
    return out || null;
  }
  function nameOf(M, ip) {
    var ids = Object.keys(M.dev);
    for (var i = 0; i < ids.length; i++) if (ifaces(M, ids[i]).some(function (f) { return f.ip === ip; })) return M.dev[ids[i]].kind === "internet" ? "isp-gateway" : M.dev[ids[i]].name;
    return (M.outside || {})[ip] || "";
  }
  function owner(M, ip) {
    var ids = Object.keys(M.dev);
    for (var i = 0; i < ids.length; i++) if (ifaces(M, ids[i]).some(function (f) { return f.ip === ip; })) return ids[i];
    return null;
  }

  function nextHop(M, id, dst) {
    var d = M.dev[id], fs = ifaces(M, id).filter(function (f) { return f.ip && !f.shut; });
    var conn = fs.filter(function (f) { return inNet(dst, f.ip, f.bits); }).sort(function (a, b) { return b.bits - a.bits; })[0];
    if (conn) return { f: conn, via: dst };
    var gw = null;
    if (ROUTERS[d.kind] || d.kind === "internet") {
      var r = (d.routes || []).map(function (x) { var c = cidr(x.net); return { c: c, via: x.via }; }).filter(function (x) { return x.c && inNet(dst, x.c.ip, x.c.bits); }).sort(function (a, b) { return b.c.bits - a.c.bits; })[0];
      gw = r ? r.via : null;
    } else gw = d.gw || null;
    if (!gw) return { err: "nogw" };
    var f = fs.filter(function (x) { return inNet(gw, x.ip, x.bits); })[0];
    if (!f) return { err: "nogw" };
    return { f: f, via: gw };
  }
  function startOf(M, id, f) {
    if (f.svi) return { sw: id, vlan: f.vlan };
    return { ep: id + ":" + f.parent, tag: f.vlan || 0 };
  }

  function entryText(e) { return e.rule + " " + e.proto + " " + e.src + " -> " + e.dst + (e.port ? ":" + e.port : ""); }
  function aclCheck(FW, R, flow, ing, eg) {
    var lists = [], fi = (R.ifs || {})[ing], fe = (R.ifs || {})[eg];
    if (fi && fi.acl && fi.acl["in"]) lists.push(fi.acl["in"]);
    if (fe && fe.acl && fe.acl.out) lists.push(fe.acl.out);
    for (var i = 0; i < lists.length; i++) {
      var entries = (R.acls || {})[lists[i]];
      if (!entries) continue;
      var text = entries.map(function (l) { return aclEntry(l, aclStd(lists[i])); }).filter(Boolean).map(entryText).join("\n") + "\ndefault deny", fw = FW.parse(text);
      if (fw.errors.length) continue;
      var dec = FW.decide(fw, flow);
      if (dec.action === "deny") return dec.rule ? dec.rule.text : "implicit deny";
    }
    return null;
  }
  function firewall(M, R, flow, ing, eg) {
    var FW = global.AayatTools && global.AayatTools.get && global.AayatTools.get("firewall");
    if (R.acls && Object.keys(R.acls).length) return FW ? aclCheck(FW, R, flow, ing, eg) : null;
    if (!R.rules) return null;
    var fw = FW.parse(R.rules);
    if (fw.errors.length) return null;
    var dec = FW.decide(fw, flow);
    return dec.action === "deny" ? (dec.rule ? dec.rule.text : "default deny") : null;
  }

  function inbound(M, src, target, opts) {
    var C = cables(M), res = { ok: false, hops: [{ id: "out", ip: src, name: (M.outside || {})[src] || "" }], src: src, dst: "", why: "", at: "" };
    var dst = lookup(M, target);
    if (!dst) { res.why = "unknown"; return res; }
    res.dst = dst;
    var edge = (C["internet:eth0"] || []).map(split).filter(function (e) { var d = M.dev[e.id]; return d && ROUTERS[d.kind] && on(M, e.id) && !((d.ifs || {})[e.port] || {}).shut; })[0];
    if (!edge) { res.why = "gwdown"; res.at = "internet"; return res; }
    var R = M.dev[edge.id];
    res.hops.push({ id: edge.id, ip: ((R.ifs || {})[edge.port] || {}).ip || "", name: R.name });
    var deny = firewall(M, R, { proto: opts.proto || "icmp", src: src, dst: dst, dport: opts.port || 0 });
    if (deny) { res.why = "filtered"; res.at = edge.id; res.rule = deny; return res; }
    var r = route(M, edge.id, dst, opts);
    r.hops.forEach(function (h) { if (h.id !== edge.id) res.hops.push(h); });
    if (!r.ok) { res.why = r.why; res.at = r.at; if (r.rule) res.rule = r.rule; return res; }
    var last = res.hops[res.hops.length - 1];
    if (last && last.id !== edge.id && HOSTLIKE[(M.dev[last.id] || {}).kind] && !back(M, C, last.id, src)) { res.why = "noreturn"; res.at = last.id; return res; }
    res.ok = true;
    return res;
  }

  function route(M, from, target, opts) {
    opts = opts || {};
    if (!M.dev[from] && ipNum(from) !== null && !PRIV.test(from)) return inbound(M, from, target, opts);
    var C = cables(M), res = { ok: false, hops: [], src: "", dst: "", why: "", at: "" };
    var dst = lookup(M, target);
    if (!dst) { res.why = "unknown"; return res; }
    res.dst = dst;
    if (!on(M, from)) { res.why = "off"; return res; }
    var cur = from, srcIp = null, guard = 0;
    var mine = ifaces(M, from).filter(function (f) { return f.ip === dst; })[0];
    if (mine) { res.ok = true; res.src = dst; res.hops.push({ id: from, ip: dst, name: M.dev[from].name }); return res; }
    while (guard++ < 10) {
      var d = M.dev[cur];
      if (cur !== from && ifaces(M, cur).some(function (f) { return f.ip === dst && !f.shut; })) { res.hops[res.hops.length - 1].ip = dst; res.ok = true; return res; }
      if (d.kind === "internet") {
        if (PRIV.test(dst)) { res.why = "noroute"; res.at = cur; return res; }
        res.ok = true; res.hops.push({ id: "out", ip: dst, name: (M.outside || {})[dst] || "" }); return res;
      }
      var nh = nextHop(M, cur, dst);
      if (nh.err) { res.why = cur === from ? "nogw" : "noroute"; res.at = cur; return res; }
      if (srcIp == null) srcIp = res.src = nh.f.ip;
      if (!nh.f.svi && !linked(M, C, cur + ":" + nh.f.parent)) { res.why = cur === from ? "nolink" : "gwdown"; res.at = cur; return res; }
      var reach = flood(M, C, startOf(M, cur, nh.f)), hit = reach.filter(function (r) { return r.ip === nh.via; })[0];
      if (!hit) { res.why = nh.via === dst ? (cur === from ? "arp" : "lost") : (cur === from ? "gwdown" : "lost"); res.at = cur; return res; }
      var H = M.dev[hit.id];
      if (nh.via === dst) {
        res.hops.push({ id: hit.id, ip: dst, name: H.name });
        if (res.hops.length > 1 && HOSTLIKE[H.kind] && !back(M, C, hit.id, srcIp)) { res.why = "noreturn"; res.at = hit.id; res.hops.pop(); return res; }
        res.ok = true;
        return res;
      }
      if (!(ROUTERS[H.kind] || H.kind === "internet")) { res.why = "notrouter"; res.at = hit.id; return res; }
      var egn = nextHop(M, hit.id, dst), deny = firewall(M, H, { proto: opts.proto || "icmp", src: srcIp, dst: dst, dport: opts.port || 0 }, hit.name, egn.f ? egn.f.name : "");
      res.hops.push({ id: hit.id, ip: nh.via, name: H.kind === "internet" ? "isp-gateway" : H.name });
      if (deny) { res.why = "filtered"; res.at = hit.id; res.rule = deny; return res; }
      cur = hit.id;
    }
    res.why = "loop";
    return res;
  }
  function back(M, C, id, srcIp) {
    var nh = nextHop(M, id, srcIp);
    if (nh.err) return false;
    if (!linked(M, C, id + ":" + nh.f.parent)) return false;
    return flood(M, C, startOf(M, id, nh.f)).some(function (r) { return r.ip === nh.via; });
  }

  var WHY = {
    unknown: "The name doesn't resolve to an address.", off: "This device is switched off.", nogw: "No gateway or route for that address.",
    nolink: "The network cable is unplugged, or the switch port is shut.", arp: "Nothing answers at that address on this network segment.",
    gwdown: "The gateway doesn't answer on this segment.", lost: "The packet was lost after the last hop shown.", notrouter: "That next hop isn't a router.",
    filtered: "A firewall rule dropped it.", noreturn: "It arrived, but the reply has no way back (check the far end's gateway).", noroute: "A router has no route for it.", loop: "The packet went round in a loop."
  };

  function ttlBase(M, id) { var d = M.dev[id] || {}; return d.os === "windows" ? 128 : d.os === "netos" ? 255 : 64; }
  function ms(seed, i, hops) { return (0.3 + ((hash(seed + i) % 900) / 1000) + hops * 2.1); }
  function pingText(M, from, target, count, os) {
    var r = route(M, from, target), n = count || 4, out = [], dst = r.dst || target, hopsIn = Math.max(0, r.hops.length - 1);
    var last = r.hops[r.hops.length - 1], ttl = r.ok ? ttlBase(M, last.id === "out" ? "internet" : last.id) - hopsIn : 0;
    if (r.ok && last.id === "out") ttl = 117;
    var times = [];
    for (var i = 0; i < n; i++) times.push(ms(from + dst, i, hopsIn));
    if (os === "windows") {
      if (r.why === "unknown") return { text: "Ping request could not find host " + target + ". Please check the name and try again.", r: r };
      if (r.why === "off") return { text: "", r: r };
      out.push("", "Pinging " + (dst !== target ? target + " [" + dst + "]" : dst) + " with 32 bytes of data:");
      for (var j = 0; j < n; j++) {
        if (r.ok) out.push("Reply from " + dst + ": bytes=32 time" + (times[j] < 1 ? "<1ms" : "=" + Math.round(times[j]) + "ms") + " TTL=" + ttl);
        else if (r.why === "nolink" || r.why === "nogw") out.push("PING: transmit failed. General failure.");
        else if (r.why === "arp") out.push("Reply from " + r.src + ": Destination host unreachable.");
        else if (r.why === "filtered" || r.why === "noroute") out.push("Reply from " + r.hops[r.hops.length - 1].ip + ": Destination net unreachable.");
        else out.push("Request timed out.");
      }
      var got = r.ok || r.why === "arp" || r.why === "filtered" || r.why === "noroute" ? n : 0;
      out.push("", "Ping statistics for " + dst + ":", "    Packets: Sent = " + n + ", Received = " + got + ", Lost = " + (n - got) + " (" + Math.round((n - got) / n * 100) + "% loss),");
      if (r.ok) {
        var mn = Math.round(Math.min.apply(null, times)), mx = Math.round(Math.max.apply(null, times)), av = Math.round(times.reduce(function (a, b) { return a + b; }, 0) / n);
        out.push("Approximate round trip times in milli-seconds:", "    Minimum = " + mn + "ms, Maximum = " + mx + "ms, Average = " + av + "ms");
      }
      return { text: out.join("\n"), r: r };
    }
    if (os === "netos") {
      out.push("Type escape sequence to abort.", "Sending " + n + ", 100-byte ICMP Echos to " + dst + ", timeout is 2 seconds:");
      var marks = "";
      for (var q = 0; q < n; q++) marks += r.ok ? "!" : r.why === "filtered" || r.why === "noroute" ? "U" : ".";
      out.push(marks, "Success rate is " + (r.ok ? 100 : 0) + " percent (" + (r.ok ? n : 0) + "/" + n + ")" + (r.ok ? ", round-trip min/avg/max = 1/" + Math.round(1 + hopsIn * 2) + "/" + Math.round(3 + hopsIn * 3) + " ms" : ""));
      return { text: out.join("\n"), r: r };
    }
    if (r.why === "unknown") return { text: "ping: " + target + ": Name or service not known", r: r };
    if (r.why === "nogw") return { text: "ping: connect: Network is unreachable", r: r };
    out.push("PING " + (dst !== target ? target + " (" + dst + ")" : dst + " (" + dst + ")") + " 56(84) bytes of data.");
    for (var k = 0; k < n; k++) {
      if (r.ok) out.push("64 bytes from " + (dst !== target ? target + " (" + dst + ")" : dst) + ": icmp_seq=" + (k + 1) + " ttl=" + ttl + " time=" + times[k].toFixed(3).replace(/0+$/, "").replace(/\.$/, ".0") + " ms");
      else if (r.why === "arp" || r.why === "nolink") out.push("From " + (r.src || "0.0.0.0") + " icmp_seq=" + (k + 1) + " Destination Host Unreachable");
      else if (r.why === "filtered" || r.why === "noroute") out.push("From " + r.hops[r.hops.length - 1].ip + " icmp_seq=" + (k + 1) + " Destination Net Unreachable");
    }
    var rec = r.ok ? n : 0, errs = r.ok ? 0 : (r.why === "arp" || r.why === "nolink" || r.why === "filtered" || r.why === "noroute") ? n : 0;
    out.push("", "--- " + (dst !== target ? target : dst) + " ping statistics ---", n + " packets transmitted, " + rec + " received, " + (errs ? "+" + errs + " errors, " : "") + Math.round((n - rec) / n * 100) + "% packet loss, time " + ((n - 1) * 1001 + 3) + "ms");
    if (r.ok) {
      var a = times.reduce(function (x, y) { return x + y; }, 0) / n;
      out.push("rtt min/avg/max/mdev = " + Math.min.apply(null, times).toFixed(3) + "/" + a.toFixed(3) + "/" + Math.max.apply(null, times).toFixed(3) + "/" + (Math.max.apply(null, times) - a).toFixed(3) + " ms");
    }
    return { text: out.join("\n"), r: r };
  }
  function traceText(M, from, target, os) {
    var r = route(M, from, target), dst = r.dst || target, out = [];
    if (r.why === "unknown") return { text: os === "windows" ? "Unable to resolve target system name " + target + "." : target + ": Name or service not known\nCannot handle \"host\" cmdline arg `" + target + "' on position 1 (argc 1)", r: r };
    var lines = r.hops.map(function (h, i) {
      var t = [0, 1, 2].map(function (x) { return ms(h.ip, x, i + 1); });
      var nm = h.name && h.name !== h.ip ? h.name : h.ip;
      if (os === "windows") return ("  " + (i + 1)).slice(-3) + t.map(function (x) { return ("     " + (x < 1 ? "<1" : Math.round(x)) + " ms").slice(-9); }).join("") + "  " + (nm !== h.ip ? nm + " [" + h.ip + "]" : h.ip);
      if (os === "netos") return ("  " + (i + 1)).slice(-2) + " " + h.ip + " " + t.map(function (x) { return Math.max(1, Math.round(x)) + " msec"; }).join(" ");
      return ("  " + (i + 1)).slice(-2) + "  " + nm + " (" + h.ip + ")  " + t.map(function (x) { return x.toFixed(3) + " ms"; }).join("  ");
    });
    var max = r.ok ? lines.length : Math.min(30, lines.length + 3);
    for (var i = lines.length; i < max; i++) lines.push(os === "windows" ? ("  " + (i + 1)).slice(-3) + "     *        *        *     Request timed out." : ("  " + (i + 1)).slice(-2) + "  * * *");
    if (os === "windows") out.push("", "Tracing route to " + (dst !== target ? target + " [" + dst + "]" : dst), "over a maximum of 30 hops:", "");
    else if (os === "netos") out.push("Type escape sequence to abort.", "Tracing the route to " + dst, "");
    else out.push("traceroute to " + (dst !== target ? target : dst) + " (" + dst + "), 30 hops max, 60 byte packets");
    out = out.concat(lines);
    if (os === "windows") out.push("", "Trace complete.");
    return { text: out.join("\n"), r: r };
  }

  function linkState(M, s, n) {
    var p = M.sw[s] && M.sw[s][n];
    if (!p) return "none";
    if (p.shut) return "disabled";
    if (!p.to) return "empty";
    var e = split(p.to);
    if (!on(M, e.id)) return "nolink";
    var peer = M.sw[e.id];
    if (peer && peer[e.port] && peer[e.port].shut) return "nolink";
    return "up";
  }

  function reachMap(M) {
    var hosts = Object.keys(M.dev).filter(function (id) { return HOSTLIKE[M.dev[id].kind]; });
    var servers = hosts.filter(function (id) { var k = M.dev[id].kind; return k === "server" || k === "nas" || k === "printer" || k === "camera"; });
    var out = {};
    hosts.forEach(function (id) {
      var o = out[id] = { up: on(M, id), net: route(M, id, "198.51.100.1").ok, see: {} };
      servers.forEach(function (s) { if (s !== id) o.see[s] = route(M, id, s).ok; });
    });
    return out;
  }
  function impact(base, M) {
    var a = reachMap(base), b = reachMap(M), lines = [], lostNet = [], lostSrv = {};
    Object.keys(a).forEach(function (id) {
      var x = a[id], y = b[id], nm = M.dev[id].name;
      if (!y) return;
      if (x.up && !y.up) { lines.push("Switched off: " + nm); return; }
      var C = cables(M), alone = !linked(M, C, id + ":eth0");
      if (alone && !linked(base, cables(base), id + ":eth0")) return;
      if (alone) { lines.push("No network at all: " + nm + " (cable out or port shut)"); return; }
      if (x.net && !y.net) lostNet.push(nm);
      Object.keys(x.see).forEach(function (s) { if (x.see[s] && !y.see[s] && on(M, s)) (lostSrv[s] = lostSrv[s] || []).push(nm); });
    });
    if (lostNet.length) lines.push("Lost the internet: " + lostNet.join(", "));
    Object.keys(lostSrv).forEach(function (s) { lines.push("Can't reach " + M.dev[s].name + ": " + lostSrv[s].join(", ")); });
    return lines;
  }

  function check(M, c) {
    if (!c) return false;
    if (c.all) return c.all.every(function (x) { return check(M, x); });
    if (c.any) return c.any.some(function (x) { return check(M, x); });
    if (c.not) return !check(M, c.not);
    if (c.cable) { var e = c.cable.split(":"), p = M.sw[e[0]] && M.sw[e[0]][e[1]]; if (!p) return false; return c.to === null ? !p.to : !!p.to && split(p.to).id === c.to; }
    if (c.unplugged) return !Object.keys(M.sw).some(function (s) { return Object.keys(M.sw[s]).some(function (n) { var p = M.sw[s][n]; return p.to && split(p.to).id === c.unplugged && !p.shut; }); });
    if (c.port) {
      var f = c.port.split(":"), q = M.sw[f[0]] && M.sw[f[0]][f[1]];
      if (!q) return false;
      return ["shut", "vlan", "mode", "native"].every(function (k) { return c[k] === undefined || (k === "shut" ? !!q.shut === c.shut : String(q[k] == null ? (k === "mode" ? "access" : 1) : q[k]) === String(c[k])); }) &&
        (c.allowed === undefined || vlanText(vlans(q.allowed)) === vlanText(vlans(c.allowed)));
    }
    if (c.ping) { var r = route(M, c.ping[0], c.ping[1], { proto: c.proto || "icmp", port: c.dport || 0 }); return r.ok === (c.ok !== false); }
    if (c.door !== undefined) return !!M.door === !!c.door;
    if (c.vlanName) return String((M.vlanNames || {})[c.vlanName] || "").toLowerCase() === String(c.is || "").toLowerCase();
    if (c.usb) return !!M.dev[c.usb] && (M.dev[c.usb].usb !== false) === (c.on !== false);
    if (c.power) return !!M.dev[c.power] && (M.dev[c.power].power !== false) === (c.on !== false);
    if (c.dev) { var d = M.dev[c.dev]; if (!d) return false; return Object.keys(c).every(function (k) { return k === "dev" || String(d[k]) === String(c[k]); }); }
    return false;
  }
  function tasks(M) { return (M.tasks || []).map(function (t) { return { id: t.id, text: t.text, hint: t.hint || "", done: check(M, t.check) }; }); }

  function ifName(raw, M, id) {
    var s = String(raw || "").toLowerCase().replace(/\s+/g, "");
    var m = /^(?:fastethernet|fa|f|ethernet|eth|e)(\d+)\/(\d+)$/.exec(s);
    if (m && M.sw[id]) return { port: String(+m[2]) };
    m = /^(?:gigabitethernet|gi|g)(\d+)\/(\d+)(?:\.(\d+))?$/.exec(s);
    if (m) {
      if (M.sw[id] && !m[3]) return { port: M.sw[id][String(24 + +m[2])] ? String(24 + +m[2]) : String(+m[2]) };
      return { ifn: "g" + m[1] + "/" + m[2] + (m[3] ? "." + m[3] : "") };
    }
    m = /^vlan(\d+)$/.exec(s);
    if (m) return { svi: +m[1] };
    return null;
  }
  function range(raw, M, id) {
    var out = [];
    String(raw).split(",").forEach(function (part) {
      var m = /^\s*([a-z]+)\s*(\d+)\/(\d+)\s*(?:-\s*(\d+))?\s*$/i.exec(part);
      if (!m) { var one = ifName(part, M, id); if (one) out.push(one); return; }
      for (var i = +m[3]; i <= +(m[4] || m[3]); i++) { var x = ifName(m[1] + m[2] + "/" + i, M, id); if (x) out.push(x); }
    });
    return out;
  }
  function is(t, word, min) { t = String(t || "").toLowerCase(); return t.length >= (min || 1) && word.indexOf(t) === 0; }
  function portLabel(n) { return +n > 24 ? "Gi0/" + (n - 24) : "Fa0/" + n; }
  function portFull(n) { return +n > 24 ? "GigabitEthernet0/" + (n - 24) : "FastEthernet0/" + n; }
  var WORDPORT = { www: 80, http: 80, https: 443, ssh: 22, telnet: 23, ftp: 21, domain: 53, smtp: 25, pop3: 110, ntp: 123 };
  function wild(w) {
    var n = ipNum(w);
    if (n === null) return null;
    if (n !== 4294967295 && (((n + 1) >>> 0) & n) !== 0) return null;
    var k = 0;
    while (k < 32 && ((n >>> k) & 1)) k++;
    return 32 - k;
  }
  function aclAddr(t, i) {
    if (t[i] === "any") return { v: "0.0.0.0/0", n: 1 };
    if (t[i] === "host" && ipNum(t[i + 1]) !== null) return { v: t[i + 1] + "/32", n: 2 };
    if (ipNum(t[i]) === null) return null;
    if (t[i + 1] !== undefined && wild(t[i + 1]) !== null) return { v: netAddr(t[i], wild(t[i + 1])) + "/" + wild(t[i + 1]), n: 2 };
    return { v: t[i] + "/32", n: 1 };
  }
  function aclEntry(line, standard) {
    var t = String(line).trim().split(/\s+/), act = (t[0] || "").toLowerCase();
    if (act !== "permit" && act !== "deny") return null;
    var i = 1, proto = "ip";
    if (!standard) { proto = (t[i++] || "").toLowerCase(); if (!/^(ip|tcp|udp|icmp)$/.test(proto)) return null; }
    var s1 = aclAddr(t, i);
    if (!s1) return null;
    i += s1.n;
    var d1 = { v: "0.0.0.0/0", n: 0 }, port = "";
    if (!standard) {
      d1 = aclAddr(t, i);
      if (!d1) return null;
      i += d1.n;
      if (t[i] && /^eq$/i.test(t[i])) { var pw = WORDPORT[String(t[i + 1]).toLowerCase()] || (/^\d+$/.test(t[i + 1] || "") ? +t[i + 1] : 0); if (!pw) return null; port = String(pw); i += 2; }
      if (t[i]) return null;
    } else if (t[i]) return null;
    return { act: act, text: t.join(" "), rule: act === "permit" ? "allow" : "deny", proto: proto === "ip" ? "any" : proto, src: s1.v, dst: d1.v, port: port };
  }
  function aclStd(n) { return +n < 100 || (+n >= 1300 && +n < 2000); }
  function aclRules(d) {
    var acls = d.acls || {}, used = {}, order = [];
    Object.keys(d.ifs || {}).sort().forEach(function (k) {
      var a = d.ifs[k].acl || {};
      ["in", "out"].forEach(function (dir) { if (a[dir] && acls[a[dir]] && !used[a[dir]]) { used[a[dir]] = 1; order.push(a[dir]); } });
    });
    if (!order.length) return "";
    var out = [];
    order.forEach(function (n) { acls[n].forEach(function (l) { var e = aclEntry(l, aclStd(n)); if (e) out.push(entryText(e)); }); });
    return out.join("\n") + "\ndefault deny";
  }
  function aclShow(d) {
    var acls = d.acls || {}, out = [];
    Object.keys(acls).sort().forEach(function (n) {
      out.push((aclStd(n) ? "Standard" : "Extended") + " IP access list " + n);
      acls[n].forEach(function (l, i) { out.push("    " + (i + 1) * 10 + " " + l); });
    });
    return out.join("\n");
  }
  function ifLabel(n) { return n.replace(/^g/, "GigabitEthernet"); }

  function cli(api, id, sess, line) {
    var M = api.model(), d = M.dev[id], isSw = !!M.sw[id], out = [];
    sess.mode = sess.mode || "user";
    var hn = d.hostname || String(d.name).split(".")[0];
    var raw = String(line || "").trim(), t = raw.split(/\s+/), a0 = t[0] || "";
    function say(x) { out.push(x); }
    function prompt() { return hn + ({ user: ">", priv: "#", config: "(config)#", "if": "(config-if)#", vlan: "(config-vlan)#", range: "(config-if-range)#", acl: "(config-ext-nacl)#", line: "(config-line)#" })[sess.mode]; }
    function bad() { say("% Invalid input detected at '^' marker."); }
    if (!raw) return { out: "", prompt: prompt() };
    if (raw === "?" || /\s\?$/.test(raw) || raw === "help") { say(help(sess.mode, isSw)); return { out: out.join("\n"), prompt: prompt() }; }
    if (is(a0, "do", 2) && sess.mode !== "user" && sess.mode !== "priv") { var keep = sess.mode; sess.mode = "priv"; var r0 = cli(api, id, sess, t.slice(1).join(" ")); sess.mode = keep; return { out: r0.out, prompt: prompt() }; }
    if (is(a0, "end", 3) || raw === "\u001a") { if (sess.mode !== "user") sess.mode = "priv"; return { out: "", prompt: prompt() }; }
    if (is(a0, "exit", 2)) {
      var was = sess.mode;
      sess.mode = { "if": "config", range: "config", vlan: "config", acl: "config", line: "config", config: "priv", priv: "user", user: "user" }[sess.mode];
      return { out: "", prompt: prompt(), closed: was === "user" || was === "priv" };
    }
    if (sess.mode === "user" || sess.mode === "priv") {
      if (is(a0, "enable", 2)) { sess.mode = "priv"; return { out: "", prompt: prompt() }; }
      if (is(a0, "disable", 4)) { sess.mode = "user"; return { out: "", prompt: prompt() }; }
      if (is(a0, "show", 2)) { say(show(api, M, id, t.slice(1))); return { out: out.join("\n"), prompt: prompt() }; }
      if (is(a0, "ping", 2) && t[1]) { say(pingText(M, id, t[1], 5, "netos").text); api.emit("bench.ping", { from: id, to: t[1], ok: route(M, id, t[1]).ok }); return { out: out.join("\n"), prompt: prompt() }; }
      if (is(a0, "traceroute", 3) && t[1]) { say(traceText(M, id, t[1], "netos").text); return { out: out.join("\n"), prompt: prompt() }; }
      if (sess.mode === "priv" && is(a0, "configure", 4)) { sess.mode = "config"; say("Enter configuration commands, one per line.  End with CNTL/Z."); return { out: out.join("\n"), prompt: prompt() }; }
      if (sess.mode === "priv" && (is(a0, "write", 2) || (is(a0, "copy", 2) && /run/.test(t[1] || "")))) { say("Building configuration...\n[OK]"); return { out: out.join("\n"), prompt: prompt() }; }
      if (sess.mode === "user" && (is(a0, "configure", 4) || is(a0, "write", 2))) { say("% Type enable first: this command needs privileged mode."); return { out: out.join("\n"), prompt: prompt() }; }
      say("% Unknown command or computer name, or unable to find computer address");
      return { out: out.join("\n"), prompt: prompt() };
    }
    if (sess.mode !== "config" && ((is(a0, "vlan", 2) && /^\d+$/.test(t[1] || "") && isSw) || is(a0, "hostname", 4) || (is(a0, "enable", 2) && /^(secret|password)$/i.test(t[1] || "")) ||
        (is(a0, "line", 2) && /^(console|vty)$/i.test(t[1] || "")) || is(a0, "access-list", 3) || (is(a0, "ip", 2) && (is(t[1], "access-list", 3) || is(t[1], "route", 2))))) sess.mode = "config";
    if (is(a0, "interface", 3)) {
      var multi = is(t[1], "range", 1) && t.length > 2, list = multi ? range(t.slice(2).join(" "), M, id) : [ifName(t.slice(1).join(""), M, id)];
      list = list.filter(Boolean);
      if (!list.length) { bad(); return { out: out.join("\n"), prompt: prompt() }; }
      for (var i = 0; i < list.length; i++) {
        var x = list[i];
        if (x.port && !M.sw[id][x.port]) { say("% Interface doesn't exist on this switch."); return { out: out.join("\n"), prompt: prompt() }; }
        if (x.ifn && !isSw) {
          var exists = d.ifs && d.ifs[x.ifn];
          if (!exists && x.ifn.indexOf(".") < 0) { say("% Interface doesn't exist on this router."); return { out: out.join("\n"), prompt: prompt() }; }
          if (!exists) api.setIf(id, x.ifn, {});
        }
        if (x.svi && !isSw) { bad(); return { out: out.join("\n"), prompt: prompt() }; }
      }
      sess.ifs = list;
      sess.mode = multi ? "range" : "if";
      return { out: "", prompt: prompt() };
    }
    if (sess.mode === "config") {
      if (is(a0, "vlan", 2) && /^\d+$/.test(t[1] || "") && isSw) { sess.vlan = +t[1]; sess.mode = "vlan"; if (!api.model().vlanNames || api.model().vlanNames[id + ":" + t[1]] === undefined) api.vlanName(id, +t[1], "VLAN" + ("000" + t[1]).slice(-4)); return { out: "", prompt: prompt() }; }
      if (is(a0, "no", 2) && is(t[1], "vlan", 2) && /^\d+$/.test(t[2] || "") && isSw) { api.vlanName(id, +t[2], null); return { out: "", prompt: prompt() }; }
      if (is(a0, "hostname", 4) && t[1]) { api.setDev(id, { hostname: t[1] }); return { out: "", prompt: prompt() }; }
      if (is(a0, "enable", 2) && /^(secret|password)$/i.test(t[1] || "") && t[2]) { api.setDev(id, { secrets: Object.assign({}, d.secrets, { enable: true }) }); return { out: "", prompt: prompt() }; }
      if (is(a0, "line", 2) && /^(console|vty)$/i.test(t[1] || "")) { sess.line = t[1].toLowerCase(); sess.mode = "line"; return { out: "", prompt: prompt() }; }
      if (/^(service|banner|security|spanning-tree|logging|clock|ntp)$/i.test(a0) || (is(a0, "no", 2) && /^(ip|service|logging)$/i.test(t[1] || "") && !/access-list/i.test(t[2] || ""))) return { out: "", prompt: prompt() };
      if (is(a0, "access-list", 3) && /^\d+$/.test(t[1] || "")) {
        var ent = aclEntry(t.slice(2).join(" "), aclStd(t[1]));
        if (!ent) { bad(); return { out: out.join("\n"), prompt: prompt() }; }
        var al = JSON.parse(JSON.stringify(d.acls || {}));
        al[t[1]] = (al[t[1]] || []).concat([ent.text]);
        api.setDev(id, { acls: al });
        api.setRules(id, aclRules(api.model().dev[id]));
        return { out: "", prompt: prompt() };
      }
      if (is(a0, "no", 2) && is(t[1], "access-list", 3) && t[2]) {
        var al2 = JSON.parse(JSON.stringify(d.acls || {}));
        delete al2[t[2]];
        api.setDev(id, { acls: al2 });
        api.setRules(id, aclRules(api.model().dev[id]));
        return { out: "", prompt: prompt() };
      }
      if (is(a0, "ip", 2) && is(t[1], "access-list", 3) && /^(extended|standard)$/i.test(t[2] || "") && t[3]) {
        var al3 = JSON.parse(JSON.stringify(d.acls || {}));
        al3[t[3]] = al3[t[3]] || [];
        api.setDev(id, { acls: al3 });
        sess.acl = t[3];
        sess.aclStd = /^standard$/i.test(t[2]);
        sess.mode = "acl";
        return { out: "", prompt: prompt() };
      }
      if (is(a0, "ip", 2) && is(t[1], "route", 2) && !isSw) {
        var b = bitsOf(t[3]);
        if (ipNum(t[2]) === null || b === null || ipNum(t[4]) === null) { bad(); return { out: out.join("\n"), prompt: prompt() }; }
        var rs = (d.routes || []).filter(function (x) { return x.net !== netAddr(t[2], b) + "/" + b; }).concat([{ net: netAddr(t[2], b) + "/" + b, via: t[4] }]);
        api.setRoutes(id, rs);
        return { out: "", prompt: prompt() };
      }
      bad();
      return { out: out.join("\n"), prompt: prompt() };
    }
    if (sess.mode === "acl") {
      var seq = /^\d+$/.test(t[0] || "") ? t.slice(1) : t, ent2 = aclEntry(seq.join(" "), sess.aclStd);
      if (!ent2) { bad(); return { out: out.join("\n"), prompt: prompt() }; }
      var al4 = JSON.parse(JSON.stringify(d.acls || {}));
      al4[sess.acl] = (al4[sess.acl] || []).concat([ent2.text]);
      api.setDev(id, { acls: al4 });
      api.setRules(id, aclRules(api.model().dev[id]));
      return { out: "", prompt: prompt() };
    }
    if (sess.mode === "line") {
      if (is(a0, "password", 4) && t[1]) { var sc = Object.assign({}, d.secrets); sc[sess.line] = true; api.setDev(id, { secrets: sc }); return { out: "", prompt: prompt() }; }
      if (/^(login|exec-timeout|logging|transport|privilege|no)$/i.test(a0)) return { out: "", prompt: prompt() };
      bad();
      return { out: out.join("\n"), prompt: prompt() };
    }
    if (sess.mode === "vlan") {
      if (is(a0, "name", 2) && t[1]) { api.vlanName(id, sess.vlan, t.slice(1).join("_")); return { out: "", prompt: prompt() }; }
      bad();
      return { out: out.join("\n"), prompt: prompt() };
    }
    var neg = is(a0, "no", 2), w = neg ? t.slice(1) : t;
    var msgs = [];
    sess.ifs.forEach(function (x) {
      var m = msgs;
      if (is(w[0], "shutdown", 2)) { if (x.port) api.setPort(id, x.port, { shut: !neg }); else if (x.ifn) api.setIf(id, x.ifn, { shut: !neg }); return; }
      if (is(w[0], "description", 4)) { if (x.port) api.setPort(id, x.port, { desc: neg ? "" : w.slice(1).join(" ") }); return; }
      if (is(w[0], "ip", 2) && is(w[1], "access-group", 3) && x.ifn && !isSw) {
        var dirn = (w[3] || "").toLowerCase();
        if (!neg && (!w[2] || (dirn !== "in" && dirn !== "out"))) { m.push("bad"); return; }
        var cur2 = Object.assign({}, (api.model().dev[id].ifs[x.ifn] || {}).acl);
        if (neg) { delete cur2["in"]; delete cur2.out; } else cur2[dirn] = w[2];
        api.setIf(id, x.ifn, { acl: cur2 });
        api.setRules(id, aclRules(api.model().dev[id]));
        return;
      }
      if (is(w[0], "switchport", 2) && x.port && is(w[1], "port-security", 2)) {
        var pcur = Object.assign({ on: false, max: 1, viol: "shutdown", sticky: false }, api.model().sw[id][x.port].sec);
        if (!w[2]) pcur.on = !neg;
        else if (is(w[2], "maximum", 3) && /^\d+$/.test(w[3] || "")) { pcur.max = +w[3]; pcur.on = true; }
        else if (is(w[2], "violation", 3) && /^(shutdown|restrict|protect)$/i.test(w[3] || "")) pcur.viol = w[3].toLowerCase();
        else if (is(w[2], "mac-address", 3) && /^sticky$/i.test(w[3] || "")) pcur.sticky = !neg;
        else if (!is(w[2], "mac-address", 3)) { m.push("bad"); return; }
        api.setPort(id, x.port, { sec: pcur });
        return;
      }
      if (/^(spanning-tree|storm-control|speed|duplex|negotiation)$/i.test(w[0])) return;
      if (is(w[0], "switchport", 2) && (/^nonegotiate$/i.test(w[1] || "") || (is(w[1], "trunk", 2) && is(w[2], "encapsulation", 3)))) return;
      if (is(w[0], "switchport", 2) && x.port) {
        if (is(w[1], "mode", 2)) { if (is(w[2], "access", 2)) api.setPort(id, x.port, { mode: "access" }); else if (is(w[2], "trunk", 2)) api.setPort(id, x.port, { mode: "trunk" }); else m.push("bad"); return; }
        if (is(w[1], "access", 2) && is(w[2], "vlan", 1) && /^\d+$/.test(w[3] || "")) {
          var vn = api.model().vlanNames || {};
          if (vn[id + ":" + w[3]] === undefined && +w[3] !== 1) { api.vlanName(id, +w[3], "VLAN" + ("000" + w[3]).slice(-4)); if (m.indexOf("made") < 0) m.push("made", "% Access VLAN does not exist. Creating vlan " + w[3]); }
          api.setPort(id, x.port, { vlan: +w[3] });
          return;
        }
        if (is(w[1], "trunk", 2) && is(w[2], "native", 2) && is(w[3], "vlan", 1) && /^\d+$/.test(w[4] || "")) { api.setPort(id, x.port, { native: +w[4] }); return; }
        if (is(w[1], "trunk", 2) && is(w[2], "allowed", 2) && is(w[3], "vlan", 1) && w[4]) {
          var cur = vlans(api.model().sw[id][x.port].allowed), op = w[4].toLowerCase(), arg = w[5];
          var nv;
          if (op === "add" && arg) nv = cur == null ? null : cur.concat(vlans(arg) || []);
          else if (op === "remove" && arg) nv = (cur == null ? vlans("1-4094") : cur).filter(function (v) { return (vlans(arg) || []).indexOf(v) < 0; });
          else if (op === "all") nv = null;
          else if (op === "none") nv = [];
          else nv = vlans(op);
          api.setPort(id, x.port, { allowed: vlanText(nv == null ? null : nv.filter(function (v, i, s) { return s.indexOf(v) === i; })) });
          return;
        }
        m.push("bad");
        return;
      }
      if (is(w[0], "ip", 2) && is(w[1], "address", 2)) {
        if (neg) { if (x.ifn) api.setIf(id, x.ifn, { ip: "" }); else if (x.svi) api.setDev(id, { ip: "" }); return; }
        var bb = bitsOf(w[3]);
        if (ipNum(w[2]) === null || bb === null) { m.push("bad"); return; }
        if (x.ifn) api.setIf(id, x.ifn, { ip: w[2], bits: bb });
        else if (x.svi) api.setDev(id, { ip: w[2], bits: bb, mvlan: x.svi });
        else m.push("% IP addresses go on a VLAN interface on a switch: interface vlan 1");
        return;
      }
      if (is(w[0], "encapsulation", 3) && x.ifn && x.ifn.indexOf(".") > 0 && /^dot1q$/i.test(w[1] || "") && /^\d+$/.test(w[2] || "")) { api.setIf(id, x.ifn, { vlan: +w[2] }); return; }
      m.push("bad");
    });
    msgs.forEach(function (x) { if (x === "bad") { if (out.indexOf("% Invalid input detected at '^' marker.") < 0) bad(); } else if (x !== "made") say(x); });
    if (!msgs.length) api.emit("bench.config", { dev: id, line: raw });
    return { out: out.join("\n"), prompt: prompt() };
  }
  function help(mode, isSw) {
    if (mode === "user") return "  enable      Turn on privileged commands\n  ping        Send echo messages\n  show        Show running system information\n  traceroute  Trace route to destination\n  exit        Exit from the EXEC";
    if (mode === "priv") return "  configure terminal   Enter configuration mode\n  show ...             vlan brief, interfaces status, ip interface brief, running-config, mac address-table, ip route, access-lists\n  ping / traceroute    Test a path\n  write memory         Save the configuration\n  disable / exit";
    if (mode === "config") return "  interface fa0/N            Configure one port (interface range fa0/1-4 for several)\n" + (isSw ? "  vlan N                     Create a VLAN, then: name WORD\n  no vlan N                  Delete a VLAN\n  interface vlan 1           The switch's own address\n" : "  interface g0/0.N           A subinterface for VLAN N\n  ip route NET MASK NEXTHOP  A static route\n") + "  hostname WORD\n  do show ...                Run a show command from here\n  end / exit";
    if (mode === "vlan") return "  name WORD   Name this VLAN\n  exit";
    return isSw ? "  shutdown / no shutdown\n  switchport mode access | trunk\n  switchport access vlan N\n  switchport trunk allowed vlan LIST | add N | remove N | all\n  switchport trunk native vlan N\n  description TEXT\n  exit / end" :
      "  ip address A.B.C.D MASK\n  encapsulation dot1Q N      (on a subinterface such as g0/0.10)\n  shutdown / no shutdown\n  exit / end";
  }
  function pad(s, n) { s = String(s); return s.length >= n ? s.slice(0, n - 1) + " " : s + new Array(n - s.length + 1).join(" "); }
  function show(api, M, id, args) {
    var d = M.dev[id], sw = M.sw[id], a = args.map(function (x) { return x.toLowerCase(); }), w = a.join(" ");
    var hn = d.hostname || String(d.name).split(".")[0];
    if (sw && is(a[0], "vlan", 1)) {
      var names = M.vlanNames || {}, ids = { 1: "default" };
      Object.keys(names).forEach(function (k) { if (k.split(":")[0] === id) ids[k.split(":")[1]] = names[k]; });
      Object.keys(sw).forEach(function (n) { if (sw[n].mode !== "trunk" && !ids[sw[n].vlan || 1]) ids[sw[n].vlan || 1] = "VLAN" + ("000" + (sw[n].vlan || 1)).slice(-4); });
      var rows = ["VLAN Name                             Status    Ports", "---- -------------------------------- --------- -------------------------------"];
      Object.keys(ids).map(Number).sort(function (x, y) { return x - y; }).forEach(function (v) {
        var ps = Object.keys(sw).filter(function (n) { return sw[n].mode !== "trunk" && (+sw[n].vlan || 1) === v; }).map(function (n) { return portLabel(n); });
        var chunks = [];
        for (var i = 0; i < ps.length; i += 4) chunks.push(ps.slice(i, i + 4).join(", "));
        rows.push(pad(v, 5) + pad(ids[v], 33) + pad("active", 10) + (chunks[0] || ""));
        chunks.slice(1).forEach(function (c) { rows.push(new Array(49).join(" ") + c); });
      });
      return rows.join("\n");
    }
    if (sw && is(a[0], "interfaces", 2) && /trunk/.test(w)) {
      var tr = Object.keys(sw).filter(function (n) { return sw[n].mode === "trunk"; });
      if (!tr.length) return "";
      return ["Port        Mode         Encapsulation  Status        Native vlan"].concat(tr.map(function (n) { return pad(portLabel(n), 12) + pad("on", 13) + pad("802.1q", 15) + pad(linkState(M, id, n) === "up" ? "trunking" : "not-trunking", 14) + (sw[n].native || 1); }))
        .concat(["", "Port        Vlans allowed on trunk"]).concat(tr.map(function (n) { return pad(portLabel(n), 12) + (vlans(sw[n].allowed) == null ? "1-4094" : vlanText(vlans(sw[n].allowed))); })).join("\n");
    }
    if (sw && is(a[0], "interfaces", 2)) {
      return ["Port      Name               Status       Vlan       Duplex  Speed Type"].concat(Object.keys(sw).map(Number).sort(function (x, y) { return x - y; }).map(function (n) {
        var p = sw[n], ls = linkState(M, id, n), peer = p.to ? M.dev[split(p.to).id] : null;
        return pad(portLabel(n), 10) + pad(p.desc || p.room || (peer ? String(peer.name).split(".")[0] : ""), 19) + pad(ls === "up" ? "connected" : ls === "disabled" ? (p.err ? "err-disabled" : "disabled") : "notconnect", 13) + pad(p.mode === "trunk" ? "trunk" : (p.vlan || 1), 11) + pad(ls === "up" ? "a-full" : "auto", 8) + pad(ls === "up" ? "a-100" : "auto", 6) + "10/100BaseTX";
      })).join("\n");
    }
    if (is(a[0], "ip", 2) && is(a[1], "interface", 2)) {
      var rows2 = ["Interface              IP-Address      OK? Method Status                Protocol"];
      if (sw) {
        Object.keys(sw).map(Number).sort(function (x, y) { return x - y; }).forEach(function (n) { var ls = linkState(M, id, n); rows2.push(pad(portFull(n), 23) + pad("unassigned", 16) + "YES unset  " + pad(ls === "disabled" ? "administratively down" : ls === "up" ? "up" : "down", 22) + (ls === "up" ? "up" : "down")); });
        rows2.push(pad("Vlan" + (d.mvlan || 1), 23) + pad(d.ip || "unassigned", 16) + "YES " + pad(d.ip ? "manual" : "unset", 7) + pad("up", 22) + "up");
      } else {
        var C = cables(M);
        Object.keys(d.ifs || {}).sort().forEach(function (k) {
          var f = d.ifs[k], par = f.parent || k, up = !f.shut && !(d.ifs[par] && d.ifs[par].shut) && linked(M, C, id + ":" + par);
          rows2.push(pad(ifLabel(k), 23) + pad(f.ip || "unassigned", 16) + "YES " + pad(f.ip ? "manual" : "unset", 7) + pad(f.shut ? "administratively down" : up ? "up" : "down", 22) + (up ? "up" : "down"));
        });
      }
      return rows2.join("\n");
    }
    if (is(a[0], "ip", 2) && is(a[1], "route", 2) && !sw) {
      var rows3 = ["Codes: C - connected, S - static, * - candidate default", ""];
      var def = (d.routes || []).filter(function (r) { return r.net === "0.0.0.0/0"; })[0];
      rows3.push("Gateway of last resort is " + (def ? def.via + " to network 0.0.0.0" : "not set"), "");
      Object.keys(d.ifs || {}).sort().forEach(function (k) { var f = d.ifs[k]; if (f.ip && !f.shut) rows3.push("C        " + netAddr(f.ip, f.bits) + "/" + f.bits + " is directly connected, " + ifLabel(k)); });
      (d.routes || []).forEach(function (r) { rows3.push((r.net === "0.0.0.0/0" ? "S*       " : "S        ") + r.net + " [1/0] via " + r.via); });
      return rows3.join("\n");
    }
    if (sw && is(a[0], "port-security", 4)) {
      var pr = ["Secure Port  MaxSecureAddr  CurrentAddr  SecurityViolation  Security Action", "                (Count)       (Count)          (Count)", "--------------------------------------------------------------------"];
      Object.keys(sw).map(Number).sort(function (x, y) { return x - y; }).forEach(function (n) {
        var q = sw[n].sec;
        if (q && q.on) pr.push(pad(portLabel(n), 13) + pad(q.max, 15) + pad(sw[n].to && linkState(M, id, n) === "up" ? 1 : 0, 13) + pad(sw[n].err ? 1 : 0, 19) + (q.viol === "shutdown" ? "Shutdown" : q.viol === "restrict" ? "Restrict" : "Protect"));
      });
      return pr.length > 3 ? pr.join("\n") : "";
    }
    if (is(a[0], "access-lists", 2) && !sw && d.acls && Object.keys(d.acls).length) return aclShow(d);
    if (is(a[0], "access-lists", 2) && !sw) return d.rules ? "Rules on " + hn + " (first match wins):\n" + String(d.rules).split("\n").filter(function (l) { return l.trim(); }).map(function (l, i) { return "    " + (i + 1) * 10 + " " + l.trim(); }).join("\n") : "No rules: everything is allowed through.";
    if (sw && is(a[0], "mac", 2)) {
      var rows4 = ["          Mac Address Table", "-------------------------------------------", "", "Vlan    Mac Address       Type        Ports", "----    -----------       --------    -----"];
      Object.keys(sw).map(Number).sort(function (x, y) { return x - y; }).forEach(function (n) {
        var p = sw[n];
        if (!p.to || linkState(M, id, n) !== "up") return;
        var e = split(p.to);
        rows4.push(pad(p.mode === "trunk" ? (p.native || 1) : (p.vlan || 1), 8) + pad(mac(e.id).replace(/:/g, "").replace(/(.{4})(.{4})(.{4})/, "$1.$2.$3"), 18) + pad("DYNAMIC", 12) + portLabel(n));
      });
      return rows4.join("\n");
    }
    if (is(a[0], "running-config", 3) || (is(a[0], "run", 3))) return running(M, id);
    return "% Invalid input detected at '^' marker.";
  }
  function running(M, id) {
    var d = M.dev[id], sw = M.sw[id], out = ["Building configuration...", "", "Current configuration:", "!", "hostname " + (d.hostname || String(d.name).split(".")[0]), "!"];
    if (d.secrets && d.secrets.enable) out.push("enable secret 5 $1$mERr$hashed", "!");
    if (sw) {
      Object.keys(M.vlanNames || {}).filter(function (k) { return k.split(":")[0] === id; }).forEach(function (k) { out.push("vlan " + k.split(":")[1], " name " + M.vlanNames[k], "!"); });
      Object.keys(sw).map(Number).sort(function (x, y) { return x - y; }).forEach(function (n) {
        var p = sw[n];
        out.push("interface " + portFull(n));
        if (p.desc) out.push(" description " + p.desc);
        if (p.mode === "trunk") { out.push(" switchport mode trunk"); if (p.native && +p.native !== 1) out.push(" switchport trunk native vlan " + p.native); if (vlans(p.allowed) != null) out.push(" switchport trunk allowed vlan " + vlanText(vlans(p.allowed))); }
        else { if ((+p.vlan || 1) !== 1) out.push(" switchport access vlan " + p.vlan); out.push(" switchport mode access"); }
        if (p.sec && p.sec.on) {
          out.push(" switchport port-security");
          if (p.sec.max !== 1) out.push(" switchport port-security maximum " + p.sec.max);
          if (p.sec.viol !== "shutdown") out.push(" switchport port-security violation " + p.sec.viol);
          if (p.sec.sticky) out.push(" switchport port-security mac-address sticky");
        }
        if (p.shut && !p.err) out.push(" shutdown");
        out.push("!");
      });
      out.push("interface Vlan" + (d.mvlan || 1), d.ip ? " ip address " + d.ip + " " + maskText(d.bits || 24) : " no ip address", "!");
    } else {
      Object.keys(d.ifs || {}).sort().forEach(function (k) {
        var f = d.ifs[k];
        out.push("interface " + ifLabel(k));
        if (f.vlan && k.indexOf(".") > 0) out.push(" encapsulation dot1Q " + f.vlan);
        out.push(f.ip ? " ip address " + f.ip + " " + maskText(f.bits) : " no ip address");
        if (f.acl && f.acl["in"]) out.push(" ip access-group " + f.acl["in"] + " in");
        if (f.acl && f.acl.out) out.push(" ip access-group " + f.acl.out + " out");
        if (f.shut) out.push(" shutdown");
        out.push("!");
      });
      (d.routes || []).forEach(function (r) { var c = cidr(r.net); out.push("ip route " + c.ip + " " + maskText(c.bits) + " " + r.via); });
      if (d.acls) Object.keys(d.acls).sort().forEach(function (n) { d.acls[n].forEach(function (l) { out.push("access-list " + n + " " + l); }); });
      else if (d.rules) out.push("!", "! firewall rules (show access-lists)");
    }
    out.push("!", "end");
    return out.join("\n");
  }

  function hostShell(M, id, line, os) {
    var d = M.dev[id], t = String(line || "").trim().split(/\s+/), c = (t[0] || "").toLowerCase(), args = t.slice(1);
    var f = ifaces(M, id)[0] || {}, hn = String(d.name).split(".")[0];
    function arg() { return args.filter(function (x) { return !/^-/.test(x) && !/^\/[a-z]$/i.test(x) && !/^\d+$/.test(x) || ipNum(x) !== null; }).pop(); }
    function count(flag) { var i = args.indexOf(flag); return i >= 0 && /^\d+$/.test(args[i + 1] || "") ? Math.min(20, +args[i + 1]) : 4; }
    function neigh() {
      var C = cables(M);
      if (!f.ip || !linked(M, C, id + ":eth0")) return [];
      return flood(M, C, { ep: id + ":eth0", tag: 0 }).filter(function (r) { return r.id !== id && inNet(r.ip, f.ip, f.bits); });
    }
    if (os === "windows") {
      if (c === "ipconfig") {
        var all = /\/all/i.test(line), C0 = cables(M), up = linked(M, C0, id + ":eth0");
        var o = ["", "Windows IP Configuration", ""];
        if (all) o.push("   Host Name . . . . . . . . . . . . : " + hn, "   Primary Dns Suffix  . . . . . . . : " + String(d.name).split(".").slice(1).join("."), "");
        o.push("Ethernet adapter Ethernet:", "");
        if (!up) o.push("   Media State . . . . . . . . . . . : Media disconnected", "   Connection-specific DNS Suffix  . : ");
        else {
          if (all) o.push("   Description . . . . . . . . . . . : Ethernet adapter", "   Physical Address. . . . . . . . . : " + mac(id).toUpperCase().replace(/:/g, "-"), "   DHCP Enabled. . . . . . . . . . . : No");
          o.push("   IPv4 Address. . . . . . . . . . . : " + (f.ip || "0.0.0.0"), "   Subnet Mask . . . . . . . . . . . : " + maskText(f.bits || 24), "   Default Gateway . . . . . . . . . : " + (d.gw || ""));
          if (all) o.push("   DNS Servers . . . . . . . . . . . : " + (d.dns || d.gw || ""));
        }
        return o.join("\n");
      }
      if (c === "ping") return arg() ? pingText(M, id, arg(), count("-n"), "windows").text : "Usage: ping [-n count] target_name";
      if (c === "tracert") return arg() ? traceText(M, id, arg(), "windows").text : "Usage: tracert target_name";
      if (c === "arp") { var nb = neigh(); return nb.length ? "\nInterface: " + f.ip + " --- 0x6\n  Internet Address      Physical Address      Type\n" + nb.map(function (r) { return "  " + pad(r.ip, 22) + pad(mac(r.id).replace(/:/g, "-"), 22) + "dynamic"; }).join("\n") : "No ARP Entries Found."; }
      if (c === "nslookup") { var ip = arg() ? lookup(M, arg()) : null; return "Server:  " + (nameOf(M, d.dns || d.gw) || "UnKnown") + "\nAddress:  " + (d.dns || d.gw || "") + "\n\n" + (ip ? "Name:    " + (nameOf(M, ip) || arg()) + "\nAddress:  " + ip : "*** " + (nameOf(M, d.dns || d.gw) || "server") + " can't find " + (arg() || "") + ": Non-existent domain"); }
      if (c === "route" && /print/i.test(line)) return "IPv4 Route Table\n===========================================================================\nActive Routes:\nNetwork Destination        Netmask          Gateway       Interface  Metric\n          0.0.0.0          0.0.0.0  " + pad(d.gw || "On-link", 14) + pad(f.ip, 15) + "25\n" + pad("       " + netAddr(f.ip || "0.0.0.0", f.bits || 24), 27) + pad(maskText(f.bits || 24), 17) + pad("On-link", 14) + pad(f.ip, 15) + "281\n===========================================================================";
      return null;
    }
    if (c === "ip" && /^a/.test(args[0] || "") || c === "ifconfig") {
      var C1 = cables(M), up1 = linked(M, C1, id + ":eth0");
      return "1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000\n    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00\n    inet 127.0.0.1/8 scope host lo\n" +
        "2: eth0: <BROADCAST,MULTICAST" + (up1 ? ",UP,LOWER_UP" : ",NO-CARRIER,UP") + "> mtu 1500 qdisc fq_codel state " + (up1 ? "UP" : "DOWN") + " group default qlen 1000\n    link/ether " + mac(id) + " brd ff:ff:ff:ff:ff:ff\n" + (f.ip ? "    inet " + f.ip + "/" + f.bits + " brd " + numIp((ipNum(f.ip) | ~maskOf(f.bits)) >>> 0) + " scope global eth0\n" : "");
    }
    if (c === "ip" && /^r/.test(args[0] || "") || c === "route") return (d.gw ? "default via " + d.gw + " dev eth0 proto static\n" : "") + (f.ip ? netAddr(f.ip, f.bits) + "/" + f.bits + " dev eth0 proto kernel scope link src " + f.ip : "");
    if (c === "ip" && /^n/.test(args[0] || "") || c === "arp") { var nb2 = neigh(); return nb2.map(function (r) { return r.ip + " dev eth0 lladdr " + mac(r.id) + " REACHABLE"; }).join("\n"); }
    if (c === "ping") return arg() ? pingText(M, id, arg(), count("-c"), "linux").text : "ping: usage error: Destination address required";
    if (c === "traceroute" || c === "tracepath") return arg() ? traceText(M, id, arg(), "linux").text : "Usage: traceroute host";
    if (c === "host" || c === "nslookup" || c === "dig") { var ip2 = arg() ? lookup(M, arg()) : null; return ip2 ? (c === "host" ? arg() + " has address " + ip2 : "Server:\t\t" + (d.dns || d.gw) + "\nAddress:\t" + (d.dns || d.gw) + "#53\n\nName:\t" + (nameOf(M, ip2) || arg()) + "\nAddress: " + ip2) : "Host " + (arg() || "") + " not found: 3(NXDOMAIN)"; }
    return null;
  }

  function session(base, state, hooks) {
    hooks = hooks || {};
    var st = state || blank(), cache = null, was = null;
    ["p", "d", "i", "rules", "vl", "routes"].forEach(function (k) { st[k] = st[k] || {}; });
    function model() { if (!cache) cache = merge(base, st); return cache; }
    function changed(what) {
      cache = null;
      var now = tasks(model());
      if (was) now.forEach(function (t) { var old = was.filter(function (x) { return x.id === t.id; })[0]; if (t.done && old && !old.done) api.emit("bench.task", { id: t.id, text: t.text }); });
      was = now;
      if (hooks.change) hooks.change(what);
    }
    function patch(bag, key, v) { bag[key] = Object.assign(bag[key] || {}, v); }
    var api = {
      base: base, state: st, model: model,
      tasks: function () { return tasks(model()); },
      setPort: function (s, n, v) {
        var before = model().sw[s] && model().sw[s][n];
        if (!before) return;
        var e = before.to ? split(before.to) : null, dev = e ? model().dev[e.id] : null;
        patch(st.p, s + ":" + n, v);
        if (v.to !== undefined && e && model().sw[e.id] && model().sw[e.id][e.port]) patch(st.p, e.id + ":" + e.port, { to: null });
        if (v.to) { var f = split(v.to); if (model().sw[f.id] && model().sw[f.id][f.port]) patch(st.p, f.id + ":" + f.port, { to: s + ":" + n }); }
        var act = v.to === null ? "unplug" : v.to ? "plug" : v.shut === true ? "shut" : v.shut === false ? "enable" : v.vlan != null ? "vlan" : v.mode ? "mode" : "config";
        if (act !== "config") api.emit("rack.cable", { sw: s, port: String(n), socket: before.socket || "", room: before.room || "", device: dev ? dev.name : "", id: e ? e.id : "", ip: dev && dev.ip || "", action: act, to: v.to || "", vlan: v.vlan != null ? v.vlan : "", shut: !!(v.shut != null ? v.shut : before.shut) });
        changed("port");
      },
      setIf: function (id, f, v) { if (v === null) st.i[id + ":" + f] = null; else patch(st.i, id + ":" + f, v); changed("if"); },
      setDev: function (id, v) { patch(st.d, id, v); if (v.usb !== undefined) api.emit("bench.usb", { id: id, on: v.usb }); if (v.power !== undefined) api.emit("bench.power", { id: id, on: v.power }); changed("dev"); },
      setRules: function (id, text) { st.rules[id] = text; api.emit("bench.rules", { id: id, rules: text }); changed("rules"); },
      setRoutes: function (id, list) { st.routes[id] = list; changed("routes"); },
      vlanName: function (s, v, name) { st.vl[s + ":" + v] = name; changed("vlan"); },
      setDoor: function (on) { st.door = !!on; api.emit("rack.door", { locked: !!on }); changed("door"); },
      emit: function (type, data) { if (hooks.emit) hooks.emit(type, data); },
      reset: function () { Object.keys(st).forEach(function (k) { delete st[k]; }); Object.assign(st, blank()); changed("reset"); }
    };
    was = tasks(model());
    return api;
  }

  global.AayatNet = {
    PRIV: PRIV, session: session, parseHosts: parseHosts, fromHosts: fromHosts, normalize: normalize, merge: merge, blank: blank, route: route, why: WHY, pingText: pingText, traceText: traceText,
    linkState: linkState, impact: impact, check: check, tasks: tasks, ifaces: ifaces, cables: cables, linked: linked, lookup: lookup, nameOf: nameOf, owner: owner,
    cli: cli, aclRules: aclRules, aclEntry: aclEntry, portLabel: portLabel, hostShell: hostShell, vlans: vlans, vlanText: vlanText, mac: mac, maskText: maskText, bitsOf: bitsOf, cidr: cidr, split: split, kindOf: kindOf,
    HOSTLIKE: HOSTLIKE, ROUTERS: ROUTERS, SWITCHES: SWITCHES
  };
})(typeof window !== "undefined" ? window : globalThis);
