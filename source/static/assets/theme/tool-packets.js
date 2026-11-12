(function (global) {
  "use strict";
  var SHOW = 1000;
  var UDP = { DNS: 1, UDP: 1, NTP: 1, DHCP: 1, SNMP: 1, QUIC: 1, SYSLOG: 1, MDNS: 1, LLMNR: 1, NBNS: 1 };
  var PROTOS = {};
  "http dns ssh smtp pgsql icmp ftp ntp dhcp arp quic snmp telnet rdp ldap kerberos imap pop sip mysql syslog mdns llmnr nbns irc".split(" ").forEach(function (p) { PROTOS[p] = 1; });
  var NUM = { "tcp.port": 1, "udp.port": 1, "tcp.srcport": 1, "tcp.dstport": 1, "udp.srcport": 1, "udp.dstport": 1, "frame.len": 1, "frame.number": 1, "frame.time_relative": 1, "tcp.stream": 1 };
  var STR = { "ip.src": "src", "ip.dst": "dst", "http.request.method": "method", "http.request.uri": "uri", "http.host": "host", "http.user_agent": "ua", "dns.qry.name": "qname", "_ws.col.info": "info", "_ws.col.protocol": "proto", "frame.protocols": "proto" };
  var CSS = ".tp-box .tp-tabs{display:flex;flex-wrap:wrap;gap:4px;margin:8px 0 6px}.tp-box .tp-tabs button{border:1px solid #000;background:#fff;color:#111;padding:3px 9px;cursor:pointer;font-size:12px}" +
    ".tp-box .tp-tabs button.on{background:#111;color:#fff}.tp-box .tp-bad{outline:2px solid #c0392b}.tp-box .tp-good{outline:2px solid #2e7d32}" +
    ".tp-box .tp-scroll{max-height:260px;overflow:auto;border:1px solid #bbb;background:#fff}" +
    ".tp-box table{border-collapse:collapse;width:100%;font:12px/1.35 ui-monospace,Consolas,monospace}.tp-box th{position:sticky;top:0;background:#e8e8e8;text-align:left;padding:3px 6px;border-bottom:1px solid #999;white-space:nowrap}" +
    ".tp-box td{padding:2px 6px;border-bottom:1px solid #eee;white-space:nowrap;max-width:420px;overflow:hidden;text-overflow:ellipsis}.tp-box tr.tp-row{cursor:pointer}.tp-box tr.tp-row:hover td{background:#f3f3f3}" +
    ".tp-box tr.tp-row.on td{background:#1f4e8c;color:#fff}.tp-box tr.p-http td{background:#e4ffc7}.tp-box tr.p-dns td{background:#daeeff}.tp-box tr.p-tls td{background:#efe3ff}.tp-box tr.p-syn td{background:#d8d8d8}.tp-box tr.p-smb td{background:#fdf2c4}" +
    ".tp-box tr.tp-row.on.p-http td,.tp-box tr.tp-row.on.p-dns td,.tp-box tr.tp-row.on.p-tls td,.tp-box tr.tp-row.on.p-syn td,.tp-box tr.tp-row.on.p-smb td{background:#1f4e8c}" +
    ".tp-box .tp-split{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:8px;margin-top:8px}@media (max-width:760px){.tp-box .tp-split{grid-template-columns:1fr}}" +
    ".tp-box .tp-tree{border:1px solid #bbb;padding:6px;max-height:240px;overflow:auto;font:12px/1.45 ui-monospace,Consolas,monospace;background:#fff}.tp-box .tp-tree details{margin-left:4px}.tp-box .tp-tree div{margin-left:18px;white-space:pre-wrap;word-break:break-word}" +
    ".tp-box .tp-hex{margin:0;border:1px solid #bbb;padding:6px;max-height:240px;overflow:auto;font:12px/1.45 ui-monospace,Consolas,monospace;background:#fafafa;white-space:pre}" +
    ".tp-box .tp-stream{margin:8px 0 0;border:1px solid #bbb;padding:8px;max-height:300px;overflow:auto;font:12px/1.5 ui-monospace,Consolas,monospace;background:#fff;white-space:pre-wrap;word-break:break-word}" +
    ".tp-box .tp-c{color:#a3001b;background:#fbeaea;display:block}.tp-box .tp-s{color:#0b3d91;background:#e9eefb;display:block}.tp-box .tp-small{font-size:12px;color:#555;margin:6px 0 0}";

  function style() {
    if (document.getElementById("tool-packets-css")) return;
    var s = document.createElement("style");
    s.id = "tool-packets-css";
    s.textContent = CSS;
    document.head.appendChild(s);
  }
  function own(o, k) { return Object.prototype.hasOwnProperty.call(o, k); }
  function esc(s) {
    return String(s == null ? "" : s).replace(/[&<>"']/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]; });
  }

  function isCapture(text) { return /^#aayat-capture/.test(String(text || "")); }

  function parse(text) {
    var lines = String(text).replace(/\r/g, "").split("\n"), title = "", rows = [], t0 = null;
    lines.forEach(function (l) {
      if (!l) return;
      if (l.charAt(0) === "#") { if (!title) title = l.replace(/^#aayat-capture\s*v\d+\s*/, ""); return; }
      var f = l.split("|"), t = parseFloat(f[0]);
      if (f.length < 8 || isNaN(t)) return;
      if (t0 === null) t0 = t;
      var proto = f[5] || "IP";
      var r = { no: rows.length + 1, t: t - t0, src: f[1] || "", sp: f[2] === "" ? null : +f[2], dst: f[3] || "", dp: f[4] === "" ? null : +f[4],
        proto: proto, len: +f[6] || 0, info: f[7] || "", method: f[8] || "", uri: f[9] || "", host: f[10] || "", ua: f[11] || "", qname: f[12] || "" };
      r.l4 = proto === "ICMP" ? "icmp" : r.sp == null ? "" : own(UDP, proto.toUpperCase()) ? "udp" : "tcp";
      rows.push(r);
    });
    var streams = {}, n = 0;
    rows.forEach(function (r) {
      var k = streamKey(r);
      if (!k) { r.stream = null; return; }
      if (!own(streams, k)) streams[k] = n++;
      r.stream = streams[k];
      r.key = k;
    });
    return { title: title, rows: rows };
  }

  function streamKey(r) {
    if (!r.l4 || r.l4 === "icmp" || r.sp == null) return "";
    var a = r.src + ":" + r.sp, b = r.dst + ":" + r.dp;
    return r.l4 + " " + (a < b ? a + " " + b : b + " " + a);
  }

  function tokens(src) {
    var out = [], i = 0, s = String(src);
    while (i < s.length) {
      var c = s.charAt(i);
      if (/\s/.test(c)) { i++; continue; }
      var two = s.substr(i, 2);
      if (two === "==" || two === "!=" || two === ">=" || two === "<=" || two === "&&" || two === "||") { out.push({ k: "op", v: two }); i += 2; continue; }
      if (c === ">" || c === "<" || c === "!" || c === "(" || c === ")") { out.push({ k: "op", v: c }); i++; continue; }
      if (c === '"') {
        var j = i + 1, v = "";
        while (j < s.length && s.charAt(j) !== '"') { if (s.charAt(j) === "\\" && j + 1 < s.length) j++; v += s.charAt(j); j++; }
        if (j >= s.length) throw new Error("A quote isn't closed.");
        out.push({ k: "str", v: v });
        i = j + 1;
        continue;
      }
      var m = /^[^\s()!=<>&|"]+/.exec(s.slice(i));
      if (!m) throw new Error("\"" + c + "\" isn't allowed here.");
      out.push({ k: "word", v: m[0] });
      i += m[0].length;
    }
    return out;
  }

  var WORDOPS = { eq: "==", ne: "!=", gt: ">", lt: "<", ge: ">=", le: "<=", and: "&&", or: "||", not: "!" };

  function compile(src) {
    if (!String(src || "").trim()) return function () { return true; };
    var tk = tokens(src).map(function (t) { return t.k === "word" && own(WORDOPS, t.v.toLowerCase()) ? { k: "op", v: WORDOPS[t.v.toLowerCase()] } : t; }), p = 0;
    function peek(v) { return tk[p] && tk[p].k === "op" && tk[p].v === v; }
    function orE() { var a = andE(); while (peek("||")) { p++; a = (function (x, y) { return function (r) { return x(r) || y(r); }; })(a, andE()); } return a; }
    function andE() { var a = notE(); while (peek("&&")) { p++; a = (function (x, y) { return function (r) { return x(r) && y(r); }; })(a, notE()); } return a; }
    function notE() { if (peek("!")) { p++; var x = notE(); return function (r) { return !x(r); }; } return prim(); }
    function prim() {
      if (peek("(")) { p++; var e = orE(); if (!peek(")")) throw new Error("A bracket isn't closed."); p++; return e; }
      var t = tk[p++];
      if (!t || t.k !== "word") throw new Error("Expected a field or protocol name.");
      var name = t.v.toLowerCase(), op = tk[p], value;
      if (op && (op.k === "op" && /^(==|!=|>|<|>=|<=)$/.test(op.v) || op.k === "word" && /^(contains|matches)$/i.test(op.v))) {
        p++;
        var vt = tk[p++];
        if (!vt || vt.k === "op") throw new Error("\"" + t.v + "\" needs a value to compare with.");
        value = vt.v;
        return compare(name, op.k === "word" ? op.v.toLowerCase() : op.v, value);
      }
      return bare(name);
    }
    var f = orE();
    if (p < tk.length) throw new Error("\"" + tk[p].v + "\" doesn't fit there.");
    return f;
  }

  function getter(name) {
    if (own(STR, name)) { var k = STR[name]; return function (r) { return [r[k]]; }; }
    if (name === "ip.addr" || name === "ip.host") return function (r) { return [r.src, r.dst]; };
    if (name === "tcp.port" || name === "udp.port") { var l4 = name.slice(0, 3); return function (r) { return r.l4 === l4 ? [r.sp, r.dp] : []; }; }
    if (/^(tcp|udp)\.srcport$/.test(name)) { var a = name.slice(0, 3); return function (r) { return r.l4 === a ? [r.sp] : []; }; }
    if (/^(tcp|udp)\.dstport$/.test(name)) { var b = name.slice(0, 3); return function (r) { return r.l4 === b ? [r.dp] : []; }; }
    if (name === "frame.len") return function (r) { return [r.len]; };
    if (name === "frame.number") return function (r) { return [r.no]; };
    if (name === "frame.time_relative") return function (r) { return [r.t]; };
    if (name === "tcp.stream" || name === "udp.stream") { var c = name.slice(0, 3); return function (r) { return r.l4 === c ? [r.stream] : []; }; }
    if (name === "http.response.code") return function (r) { var m = /^HTTP\/[\d.]+ (\d{3})/.exec(r.info); return m ? [+m[1]] : []; };
    if (name === "tls.handshake.extensions_server_name") return function (r) { var m = /SNI=([^)\s]+)/.exec(r.info); return m ? [m[1]] : []; };
    if (name === "tcp.flags.syn") return function (r) { return r.l4 === "tcp" ? [/\[SYN/.test(r.info) ? 1 : 0] : []; };
    return null;
  }

  function compare(name, op, value) {
    var g = getter(name);
    if (!g) throw new Error("\"" + name + "\" is neither a field nor a protocol name.");
    var numeric = own(NUM, name) || name === "tcp.flags.syn" || name === "http.response.code" || /\.stream$/.test(name);
    if (numeric && op !== "contains" && op !== "matches" && isNaN(+value)) throw new Error("\"" + value + "\" isn't a number, and " + name + " needs one.");
    var re = null;
    if (op === "matches") { try { re = new RegExp(value, "i"); } catch (e) { throw new Error("\"" + value + "\" isn't a valid regular expression."); } }
    var v = numeric ? +value : String(value).toLowerCase();
    function one(x) {
      if (x == null || x === "") return false;
      if (op === "contains") return String(x).toLowerCase().indexOf(String(value).toLowerCase()) >= 0;
      if (op === "matches") return re.test(String(x));
      var y = numeric ? +x : String(x).toLowerCase();
      if (op === "==") return y === v;
      if (op === ">") return y > v;
      if (op === "<") return y < v;
      if (op === ">=") return y >= v;
      if (op === "<=") return y <= v;
      return false;
    }
    if (op === "!=") return function (r) { var xs = g(r); return xs.length > 0 && xs.every(function (x) { return x != null && String(numeric ? +x : String(x).toLowerCase()) !== String(v); }); };
    return function (r) { return g(r).some(one); };
  }

  function bare(name) {
    if (name === "ip") return function (r) { return !!r.src; };
    if (name === "tcp" || name === "udp") return function (r) { return r.l4 === name; };
    if (name === "http.request") return function (r) { return !!r.method; };
    if (name === "http.response") return function (r) { return r.proto === "HTTP" && !r.method; };
    if (name === "tcp.flags.syn") return function (r) { return r.l4 === "tcp" && /\[SYN/.test(r.info); };
    if (name === "tls" || name === "ssl") return function (r) { return /^TLS/i.test(r.proto); };
    if (name === "smb" || name === "smb2") return function (r) { return /^SMB/i.test(r.proto); };
    if (own(PROTOS, name)) return function (r) { return r.proto.toLowerCase().replace(/v[\d.]+$/, "") === name; };
    var g = getter(name);
    if (g) return function (r) { return g(r).some(function (x) { return x != null && x !== ""; }); };
    throw new Error("\"" + name + "\" is neither a field nor a protocol name.");
  }

  function cls(r) {
    if (r.proto === "HTTP") return "p-http";
    if (r.proto === "DNS") return "p-dns";
    if (/^TLS/.test(r.proto)) return "p-tls";
    if (/^SMB/.test(r.proto)) return "p-smb";
    if (/\[SYN|\[RST|\[FIN/.test(r.info)) return "p-syn";
    return "";
  }

  function ipBytes(ip) { var p = String(ip).split(".").map(function (x) { return (+x) & 255; }); return p.length === 4 ? p : [0, 0, 0, 0]; }
  function mac(ip) { var b = ipBytes(ip); return [2, 0].concat(b).map(function (x) { return ("0" + x.toString(16)).slice(-2); }).join(":"); }

  function bytesOf(r) {
    var out = [], s = ipBytes(r.src), d = ipBytes(r.dst), payload = unescape(encodeURIComponent(r.info)), i;
    out.push.apply(out, [2, 0].concat(d));
    out.push.apply(out, [2, 0].concat(s));
    out.push(8, 0);
    var l4len = r.l4 === "tcp" ? 20 : r.l4 === "udp" ? 8 : r.l4 === "icmp" ? 8 : 0, tot = 20 + l4len + payload.length;
    out.push(0x45, 0, (tot >> 8) & 255, tot & 255, (r.no >> 8) & 255, r.no & 255, 0x40, 0, 64, r.l4 === "tcp" ? 6 : r.l4 === "udp" ? 17 : 1, 0, 0);
    out.push.apply(out, s);
    out.push.apply(out, d);
    if (r.l4 === "tcp" || r.l4 === "udp") out.push((r.sp >> 8) & 255, r.sp & 255, (r.dp >> 8) & 255, r.dp & 255);
    if (r.l4 === "tcp") {
      var fl = /\[SYN, ACK/.test(r.info) ? 0x12 : /\[SYN/.test(r.info) ? 0x02 : /\[RST/.test(r.info) ? 0x14 : /\[FIN/.test(r.info) ? 0x11 : 0x18;
      out.push(0, 0, 0, 1, 0, 0, 0, 1, 0x50, fl, 0xfa, 0xf0, 0, 0, 0, 0);
    } else if (r.l4 === "udp") { var ul = 8 + payload.length; out.push((ul >> 8) & 255, ul & 255, 0, 0); }
    else if (r.l4 === "icmp") out.push(8, 0, 0, 0, 0, 1, 0, r.no & 255);
    for (i = 0; i < payload.length; i++) out.push(payload.charCodeAt(i) & 255);
    return out;
  }

  function hexdump(bytes) {
    var lines = [];
    for (var i = 0; i < bytes.length; i += 16) {
      var chunk = bytes.slice(i, i + 16), hex = chunk.map(function (b) { return ("0" + b.toString(16)).slice(-2); });
      while (hex.length < 16) hex.push("  ");
      lines.push(("000" + i.toString(16)).slice(-4) + "  " + hex.slice(0, 8).join(" ") + "  " + hex.slice(8).join(" ") + "  " +
        chunk.map(function (b) { return b >= 32 && b < 127 ? String.fromCharCode(b) : "."; }).join(""));
    }
    return lines.join("\n");
  }

  function dnsParts(r) {
    var m = /Standard query (response )?(0x[0-9a-f]+) (\w+) (\S+)(.*)$/i.exec(r.info);
    if (!m) return null;
    var ans = [], re = /\b(A|AAAA|CNAME|TXT|MX|NS|PTR) (\S+)/g, x, rest = m[5] || "";
    while ((x = re.exec(rest))) ans.push(x[1] + " " + x[2]);
    if (/No such name|NXDOMAIN/i.test(rest)) ans.push("No such name");
    return { response: !!m[1], id: m[2], type: m[3], name: m[4], answers: ans };
  }

  function tree(r) {
    var parts = [];
    function node(title, lines, open) {
      parts.push("<details" + (open ? " open" : "") + "><summary>" + esc(title) + "</summary>" + lines.map(function (l) { return "<div>" + esc(l) + "</div>"; }).join("") + "</details>");
    }
    node("Frame " + r.no + ": " + r.len + " bytes on wire", ["Time since the first frame: " + r.t.toFixed(6) + " seconds", "Frame length: " + r.len + " bytes", "Protocols in frame: eth:ip" + (r.l4 ? ":" + r.l4 : "") + ":" + r.proto.toLowerCase()]);
    node("Ethernet II, Src: " + mac(r.src) + ", Dst: " + mac(r.dst), ["Destination: " + mac(r.dst), "Source: " + mac(r.src), "Type: IPv4 (0x0800)"]);
    node("Internet Protocol Version 4, Src: " + r.src + ", Dst: " + r.dst, ["Version: 4", "Time to live: 64", "Protocol: " + (r.l4 === "tcp" ? "TCP (6)" : r.l4 === "udp" ? "UDP (17)" : "ICMP (1)"), "Source address: " + r.src, "Destination address: " + r.dst]);
    if (r.l4 === "tcp") node("Transmission Control Protocol, Src Port: " + r.sp + ", Dst Port: " + r.dp, ["Source port: " + r.sp, "Destination port: " + r.dp, "Stream index: " + r.stream, "Flags: " + ((/\[([^\]]+)\]/.exec(r.info) || [])[1] || "PSH, ACK")]);
    if (r.l4 === "udp") node("User Datagram Protocol, Src Port: " + r.sp + ", Dst Port: " + r.dp, ["Source port: " + r.sp, "Destination port: " + r.dp, "Stream index: " + r.stream]);
    if (r.proto === "HTTP") {
      var h = [r.info];
      if (r.host) h.push("Host: " + r.host);
      if (r.ua) h.push("User-Agent: " + r.ua);
      if (r.method) h.push("[Full request URI: http://" + (r.host || r.dst) + r.uri + "]");
      node("Hypertext Transfer Protocol", h, true);
    } else if (r.proto === "DNS") {
      var d = dnsParts(r);
      node("Domain Name System (" + (d && d.response ? "response" : "query") + ")", d ? ["Transaction ID: " + d.id, "Flags: " + (d.response ? "Standard query response" : "Standard query"), "Queries: " + d.name + ": type " + d.type].concat(d.answers.map(function (a) { return "Answer: " + d.name + ": type " + a; })) : [r.info], true);
    } else if (/^TLS/.test(r.proto)) {
      var sni = /SNI=([^)\s]+)/.exec(r.info);
      node("Transport Layer Security", [r.proto + " Record Layer: " + r.info].concat(sni ? ["Server Name Indication: " + sni[1]] : []), true);
    } else if (r.proto !== "TCP" && r.proto !== "UDP" && r.proto !== "IP") node(r.proto, [r.info], true);
    return parts.join("");
  }

  function convs(rows, byPort) {
    var map = {}, list = [];
    rows.forEach(function (r) {
      if (!r.src) return;
      if (byPort && r.stream == null) return;
      var a = byPort ? r.src + ":" + r.sp : r.src, b = byPort ? r.dst + ":" + r.dp : r.dst, fwd = a <= b, k = (byPort ? r.l4 + " " : "") + (fwd ? a + " " + b : b + " " + a);
      var c = map[k];
      if (!c) { c = map[k] = { a: fwd ? a : b, b: fwd ? b : a, l4: r.l4, ab: 0, ba: 0, bytes: 0, start: r.t, end: r.t, stream: r.stream, key: r.key }; list.push(c); }
      if ((byPort ? r.src + ":" + r.sp : r.src) === c.a) c.ab++; else c.ba++;
      c.bytes += r.len;
      c.end = r.t;
    });
    return list.sort(function (x, y) { return y.bytes - x.bytes; });
  }

  function internal(ip) {
    var p = String(ip).split(".").map(Number);
    return p[0] === 10 || (p[0] === 172 && p[1] >= 16 && p[1] <= 31) || (p[0] === 192 && p[1] === 168) || p[0] === 127;
  }

  function graph(list) {
    if (!list.length) return '<p class="tp-small">No IPv4 traffic in these packets.</p>';
    var nodes = {}, W = 640, H = 420;
    list.forEach(function (c) {
      [c.a, c.b].forEach(function (ip) { nodes[ip] = nodes[ip] || { ip: ip, bytes: 0, peers: 0 }; });
      nodes[c.a].bytes += c.bytes; nodes[c.b].bytes += c.bytes; nodes[c.a].peers++; nodes[c.b].peers++;
    });
    var ins = Object.keys(nodes).filter(internal).sort(), outs = Object.keys(nodes).filter(function (ip) { return !internal(ip); }).sort();
    function place(arr, cx, rx) {
      arr.forEach(function (ip, i) {
        var a = arr.length === 1 ? 0 : -Math.PI / 2.4 + (i / (arr.length - 1)) * (Math.PI / 1.2);
        nodes[ip].x = cx + Math.cos(a) * rx * (cx < W / 2 ? -1 : 1);
        nodes[ip].y = H / 2 + Math.sin(a) * (H / 2 - 40);
      });
    }
    place(ins, W * 0.36, 150);
    place(outs, W * 0.64, 150);
    var max = Math.max.apply(null, list.map(function (c) { return c.bytes; }).concat([1]));
    var edges = list.map(function (c) {
      var A = nodes[c.a], B = nodes[c.b], w = 1 + 7 * Math.sqrt(c.bytes / max);
      return '<line x1="' + A.x.toFixed(1) + '" y1="' + A.y.toFixed(1) + '" x2="' + B.x.toFixed(1) + '" y2="' + B.y.toFixed(1) + '" stroke="#5b6b7b" stroke-opacity=".55" stroke-width="' + w.toFixed(1) +
        '"><title>' + esc(c.a + " and " + c.b + ": " + (c.ab + c.ba) + " packets, " + c.bytes + " bytes") + "</title></line>";
    }).join("");
    var dots = Object.keys(nodes).map(function (ip) {
      var n = nodes[ip], r = 5 + Math.min(14, n.peers * 2), inn = internal(ip), right = n.x > W / 2;
      return '<g class="tp-node" data-ipn="' + esc(ip) + '" style="cursor:pointer"><circle cx="' + n.x.toFixed(1) + '" cy="' + n.y.toFixed(1) + '" r="' + r + '" fill="' + (inn ? "#1f4e8c" : "#c0392b") +
        '"><title>' + esc(ip + ": " + n.peers + " peer" + (n.peers === 1 ? "" : "s") + ", " + n.bytes + " bytes. Click to filter.") + '</title></circle><text x="' + (n.x + (right ? r + 4 : -r - 4)).toFixed(1) +
        '" y="' + (n.y + 4).toFixed(1) + '" font-size="11" text-anchor="' + (right ? "start" : "end") + '">' + esc(ip) + "</text></g>";
    }).join("");
    return '<svg viewBox="0 0 ' + W + " " + H + '" style="width:100%;max-height:440px;background:#fff;border:1px solid #bbb" role="img" aria-label="Who talked to whom">' +
      '<text x="' + (W * 0.18) + '" y="18" font-size="12" fill="#1f4e8c">Inside the network</text><text x="' + (W * 0.7) + '" y="18" font-size="12" fill="#c0392b">Outside</text>' +
      edges + dots + "</svg>" + '<p class="tp-small">Thicker lines carried more bytes; bigger dots talked to more hosts. Click a dot to filter on that address.</p>';
  }

  function mount(el, ctx) {
    style();
    var st = ctx.state || {}, saved = ctx.saved || {}, answer = st.a && typeof st.a === "object" ? st.a : null;
    var caps = {}, cap = null, rows = [], view = saved.v || st.v || "list", pick = null, stream = saved.s || st.s || "", last = null;
    el.classList.add("tl-box", "tp-box");
    el.innerHTML = '<div class="tl-head"><b>Packet viewer</b><small data-r="note"></small></div>' +
      '<div class="tl-row"><label>Capture <select data-r="file"></select></label>' +
      '<label class="tl-grow">Display filter <input data-r="f" spellcheck="false" autocomplete="off" placeholder="for example  http.request and ip.addr == 10.20.0.14"></label>' +
      '<button type="button" class="btn dark" data-r="go">Apply</button><button type="button" class="btn" data-r="clear">Clear</button>' +
      (answer ? '<button type="button" class="btn" data-r="show">Show the recorded ' + (answer.s ? "stream" : "filter") + "</button>" : "") +
      (ctx.record ? '<button type="button" class="btn" data-r="save" disabled>' + ctx.recordLabel + "</button>" : "") + "</div>" +
      '<div class="tp-tabs" role="tablist"><button data-v="list">Packets</button><button data-v="conv">Conversations</button><button data-v="graph">Who talked to whom</button><button data-v="dns">DNS</button><button data-v="http">HTTP</button><button data-v="stream">Follow stream</button></div>' +
      '<p class="tl-msg" data-r="msg" role="status"></p><div data-r="body"></div>';
    function r(n) { return el.querySelector('[data-r="' + n + '"]'); }
    r("f").value = saved.f != null ? saved.f : st.f || "";

    function remember() { if (ctx.remember) ctx.remember({ file: r("file").value, f: r("f").value, v: view, s: stream }); }

    function apply(quiet) {
      if (!cap) return;
      var fn;
      try { fn = compile(r("f").value); } catch (e) {
        r("f").className = "tp-bad";
        r("msg").textContent = "That filter doesn't work: " + e.message;
        return;
      }
      r("f").className = r("f").value.trim() ? "tp-good" : "";
      rows = cap.rows.filter(fn);
      var text = rows.length + " of " + cap.rows.length + " packets shown" + (rows.length > SHOW && view === "list" ? ", listing the first " + SHOW : "") + ".";
      if (!quiet && typeof st.n === "number" && !st.s) text += rows.length === st.n ? " Same count as the recorded filter." : " The recorded filter showed " + st.n + ".";
      r("msg").textContent = text;
      if (!quiet) {
        last = { file: r("file").value, f: r("f").value, n: rows.length, v: view };
        if (r("save")) r("save").disabled = view === "stream" && !stream;
      }
      remember();
      draw();
    }

    function setView(v) {
      view = v;
      el.querySelectorAll(".tp-tabs button").forEach(function (b) { b.classList.toggle("on", b.getAttribute("data-v") === v); });
      if (last) { last.v = v; if (r("save")) r("save").disabled = v === "stream" && !stream; }
      remember();
      draw();
    }

    function table(head, body) { return '<div class="tp-scroll"><table><tr>' + head.map(function (h) { return "<th>" + esc(h) + "</th>"; }).join("") + "</tr>" + body + "</table></div>"; }

    function draw() {
      var b = r("body");
      if (!cap) { b.innerHTML = ""; return; }
      if (view === "list") {
        b.innerHTML = table(["No.", "Time", "Source", "Destination", "Protocol", "Length", "Info"], rows.slice(0, SHOW).map(function (x) {
          return '<tr class="tp-row ' + cls(x) + (pick === x.no ? " on" : "") + '" data-no="' + x.no + '"><td>' + x.no + "</td><td>" + x.t.toFixed(6) + "</td><td>" + esc(x.src) + "</td><td>" + esc(x.dst) +
            "</td><td>" + esc(x.proto) + "</td><td>" + x.len + '</td><td title="' + esc(x.info) + '">' + esc(x.info) + "</td></tr>";
        }).join("")) + '<div class="tp-split"><div class="tp-tree" data-r="tree">Pick a packet to see its layers.</div><pre class="tp-hex" data-r="hex"></pre></div>' +
          '<p class="tp-small">The bytes are rebuilt from the saved capture: real addresses, ports and text, with the other header fields filled in.</p>';
        if (pick) detail(pick);
      } else if (view === "conv") {
        var ip = convs(rows, false), tp = convs(rows, true);
        b.innerHTML = "<h4>IPv4</h4>" + table(["Address A", "Address B", "Packets", "A → B", "B → A", "Bytes", "Start", "Duration"], ip.map(function (c) {
          return '<tr class="tp-row" data-ipa="' + esc(c.a) + '" data-ipb="' + esc(c.b) + '" title="Filter on this conversation"><td>' + esc(c.a) + "</td><td>" + esc(c.b) + "</td><td>" + (c.ab + c.ba) + "</td><td>" + c.ab + "</td><td>" + c.ba +
            "</td><td>" + c.bytes + "</td><td>" + c.start.toFixed(3) + "</td><td>" + (c.end - c.start).toFixed(3) + "</td></tr>";
        }).join("")) + "<h4>TCP and UDP</h4>" + table(["Type", "Address A", "Address B", "Packets", "Bytes", "Start", "Duration"], tp.map(function (c) {
          return '<tr class="tp-row" data-key="' + esc(c.key) + '" title="Follow this stream"><td>' + c.l4.toUpperCase() + "</td><td>" + esc(c.a) + "</td><td>" + esc(c.b) + "</td><td>" + (c.ab + c.ba) + "</td><td>" + c.bytes +
            "</td><td>" + c.start.toFixed(3) + "</td><td>" + (c.end - c.start).toFixed(3) + "</td></tr>";
        }).join("")) + '<p class="tp-small">Click an IPv4 row to filter on it, or a TCP/UDP row to follow that stream.</p>';
      } else if (view === "graph") {
        b.innerHTML = graph(convs(rows, false));
      } else if (view === "dns") {
        var qs = [], byId = {}, names = {}, order = [];
        rows.forEach(function (x) {
          if (x.proto !== "DNS") return;
          var d = dnsParts(x);
          if (!d) return;
          if (!d.response) { var q = { t: x.t, client: x.src, server: x.dst, name: d.name, type: d.type, answer: "", no: x.no }; qs.push(q); byId[d.id + d.name] = q; }
          else if (byId[d.id + d.name]) byId[d.id + d.name].answer = d.answers.join(", ") || "(empty)";
          if (!d.response) {
            if (!own(names, d.name)) { names[d.name] = { n: 0, clients: {} }; order.push(d.name); }
            names[d.name].n++;
            names[d.name].clients[x.src] = 1;
          }
        });
        order.sort(function (a, c) { return names[c].n - names[a].n; });
        b.innerHTML = "<h4>Names asked for</h4>" + table(["Name", "Queries", "Clients", "Length"], order.map(function (n) {
          return '<tr class="tp-row" data-qname="' + esc(n) + '" title="Filter on this name"><td>' + esc(n) + "</td><td>" + names[n].n + "</td><td>" + esc(Object.keys(names[n].clients).join(", ")) + "</td><td>" + n.length + "</td></tr>";
        }).join("")) + "<h4>Queries</h4>" + table(["Time", "Client", "Server", "Type", "Name", "Answer"], qs.map(function (q) {
          return '<tr class="tp-row" data-pkt="' + q.no + '"><td>' + q.t.toFixed(3) + "</td><td>" + esc(q.client) + "</td><td>" + esc(q.server) + "</td><td>" + esc(q.type) + "</td><td>" + esc(q.name) + "</td><td>" + esc(q.answer) + "</td></tr>";
        }).join("")) + '<p class="tp-small">Long, random-looking names asked many times can mean data is being smuggled out over DNS.</p>';
      } else if (view === "http") {
        var reqs = [], hosts = {}, horder = [];
        rows.forEach(function (x, i) {
          if (x.proto !== "HTTP" || !x.method) return;
          var resp = "";
          for (var j = 0; j < cap.rows.length; j++) {
            var y = cap.rows[j];
            if (y.no > x.no && y.key === x.key && y.src === x.dst && /^HTTP\//.test(y.info)) { resp = y.info.replace(/^HTTP\/[\d.]+\s*/, ""); break; }
          }
          reqs.push({ x: x, resp: resp });
          var hn = x.host || x.dst;
          if (!own(hosts, hn)) { hosts[hn] = 0; horder.push(hn); }
          hosts[hn]++;
        });
        b.innerHTML = "<h4>Hosts</h4>" + table(["Host", "Requests"], horder.map(function (h) { return '<tr class="tp-row" data-host="' + esc(h) + '"><td>' + esc(h) + "</td><td>" + hosts[h] + "</td></tr>"; }).join("")) +
          "<h4>Requests</h4>" + table(["Time", "Client", "Method", "Host", "URI", "Response", "User agent"], reqs.map(function (q) {
            return '<tr class="tp-row" data-key="' + esc(q.x.key) + '" title="Follow this stream"><td>' + q.x.t.toFixed(3) + "</td><td>" + esc(q.x.src) + "</td><td>" + esc(q.x.method) + "</td><td>" + esc(q.x.host || q.x.dst) +
              "</td><td>" + esc(q.x.uri) + "</td><td>" + esc(q.resp) + "</td><td>" + esc(q.x.ua) + "</td></tr>";
          }).join(""));
      } else {
        var keys = [], seen = {};
        cap.rows.forEach(function (x) { if (x.key && !own(seen, x.key)) { seen[x.key] = 1; keys.push(x); } });
        b.innerHTML = '<div class="tl-row"><label class="tl-grow">Stream <select data-r="pickstream"><option value="">Pick a conversation…</option>' + keys.map(function (x) {
          return '<option value="' + esc(x.key) + '">' + x.stream + ": " + esc(x.l4.toUpperCase() + " " + x.src + ":" + x.sp + " ↔ " + x.dst + ":" + x.dp + " (" + x.proto + ")") + "</option>";
        }).join("") + '</select></label></div><div class="tp-stream" data-r="stream"></div>';
        r("pickstream").value = stream && own(seen, stream) ? stream : "";
        follow();
      }
    }

    function follow() {
      var box = r("stream");
      if (!box) return;
      if (!stream) { box.textContent = "Pick a conversation to read it from start to end."; return; }
      var list = cap.rows.filter(function (x) { return x.key === stream; });
      if (!list.length) { box.textContent = "That stream isn't in this capture."; return; }
      var client = list[0].src + ":" + list[0].sp, bytes = 0;
      box.innerHTML = list.map(function (x) {
        bytes += x.len;
        var mine = x.src + ":" + x.sp === client, text = x.info;
        if (x.method && x.host) text += "\nHost: " + x.host + (x.ua ? "\nUser-Agent: " + x.ua : "");
        return '<span class="' + (mine ? "tp-c" : "tp-s") + '">' + esc(text) + "</span>";
      }).join("") + '<p class="tp-small">' + list.length + " packets, " + bytes + " bytes. Red is " + esc(client) + " (it spoke first); blue is the other side." +
        (answer && answer.s ? (stream === answer.s ? " This is the stream the recording followed." : " The recording followed a different stream.") : "") + "</p>";
      if (r("save") && last) r("save").disabled = false;
    }

    function detail(no) {
      var x = cap.rows[no - 1];
      if (!x || !r("tree")) return;
      r("tree").innerHTML = tree(x) + (x.key ? '<p><button type="button" class="btn" data-follow="' + esc(x.key) + '">Follow this stream</button></p>' : "");
      r("hex").textContent = hexdump(bytesOf(x));
    }

    function loadCap() {
      var name = r("file").value;
      cap = own(caps, name) ? parse(caps[name]) : null;
      pick = null;
      r("note").textContent = cap ? (cap.title ? cap.title + " · " : "") + cap.rows.length + " packets" : "";
      apply(true);
    }

    el.addEventListener("click", function (e) {
      var t = e.target.closest("[data-v],[data-no],[data-ipa],[data-ipn],[data-key],[data-qname],[data-host],[data-pkt],[data-follow]");
      if (!t || !el.contains(t)) return;
      if (t.hasAttribute("data-v")) return setView(t.getAttribute("data-v"));
      if (t.hasAttribute("data-follow") || t.hasAttribute("data-key")) {
        stream = t.getAttribute("data-follow") || t.getAttribute("data-key");
        if (!last) last = { file: r("file").value, f: r("f").value, n: rows.length, v: "stream" };
        return setView("stream");
      }
      if (t.hasAttribute("data-no")) {
        pick = +t.getAttribute("data-no");
        el.querySelectorAll("tr.on").forEach(function (x) { x.classList.remove("on"); });
        t.classList.add("on");
        return detail(pick);
      }
      if (t.hasAttribute("data-pkt")) { pick = +t.getAttribute("data-pkt"); r("f").value = "frame.number == " + pick; setView("list"); return apply(); }
      if (t.hasAttribute("data-ipa")) r("f").value = "ip.addr == " + t.getAttribute("data-ipa") + " and ip.addr == " + t.getAttribute("data-ipb");
      if (t.hasAttribute("data-ipn")) r("f").value = "ip.addr == " + t.getAttribute("data-ipn");
      if (t.hasAttribute("data-qname")) r("f").value = 'dns.qry.name == "' + t.getAttribute("data-qname") + '"';
      if (t.hasAttribute("data-host")) r("f").value = 'http.host == "' + t.getAttribute("data-host") + '"';
      setView("list");
      apply();
    });
    el.addEventListener("change", function (e) {
      if (e.target === r("file")) { stream = ""; loadCap(); remember(); }
      if (e.target === r("pickstream")) { stream = e.target.value; if (!last) last = { file: r("file").value, f: r("f").value, n: rows.length, v: "stream" }; remember(); follow(); }
    });
    r("go").addEventListener("click", function () { apply(); });
    r("clear").addEventListener("click", function () { r("f").value = ""; apply(); });
    r("f").addEventListener("keydown", function (e) { if (e.key === "Enter") { e.preventDefault(); apply(); } });
    r("f").addEventListener("input", function () { r("f").className = ""; remember(); });
    if (r("show")) r("show").addEventListener("click", function () {
      if (answer.f != null) r("f").value = answer.f;
      if (answer.s) { stream = answer.s; setView("stream"); }
      r("f").focus();
    });
    if (r("save")) r("save").addEventListener("click", function () {
      if (!last) return;
      var state = { file: last.file, f: last.f, n: last.n, v: view, blank: ["f"] }, text;
      if (view === "stream" && stream) {
        state.s = stream;
        state.blank = ["f", "s"];
        text = "Packet viewer: follow " + stream.replace(/^\w+ /, "").replace(" ", " ↔ ") + " in " + last.file;
      } else text = "Packet viewer: " + (last.f ? last.f : "all packets") + " in " + last.file + " (" + last.n + " packets)";
      ctx.record(state, text);
      r("msg").textContent = "Added.";
      r("save").disabled = true;
    });

    el.querySelectorAll(".tp-tabs button").forEach(function (b) { b.classList.toggle("on", b.getAttribute("data-v") === view); });
    r("note").textContent = "Loading the files…";
    Promise.resolve(ctx.files()).then(function (fs) {
      fs = fs || {};
      Object.keys(fs).forEach(function (k) { if (isCapture(fs[k])) caps[k] = fs[k]; });
      var names = Object.keys(caps).sort();
      if (!names.length) {
        r("note").textContent = "";
        r("msg").textContent = "There's no saved capture here yet. Captures are files like capture.pcap.";
        r("go").disabled = true;
        return;
      }
      names.forEach(function (n) {
        var o = document.createElement("option");
        o.value = n;
        o.textContent = n;
        r("file").appendChild(o);
      });
      var want = saved.file || st.file;
      r("file").value = want && own(caps, want) ? want : names[0];
      loadCap();
      if (r("f").value.trim() && (saved.f != null || st.f)) apply(true);
    }).catch(function () { r("note").textContent = ""; r("msg").textContent = "The files didn't load."; });
  }

  global.AayatTools.register({ id: "packets", title: "Packet viewer", console: true, mount: mount, parse: parse, compile: compile });
})(window);
