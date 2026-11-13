(function (global) {
  "use strict";
  var TOOLS = {};
  var GROUPS = ["SOC analyst", "Incident responder", "Security engineer", "Cloud and DevSecOps", "Penetration tester", "Governance and risk"];

  function register(def) {
    if (!def || !/^[a-z0-9][a-z0-9-]*$/.test(def.id || "") || typeof def.mount !== "function") throw new Error("A tool needs an id and a mount function.");
    TOOLS[def.id] = def;
  }
  function get(id) { return Object.prototype.hasOwnProperty.call(TOOLS, id) ? TOOLS[id] : null; }
  function list() { return Object.keys(TOOLS).map(function (k) { return TOOLS[k]; }); }
  function fence(id, state) { return "```tool " + id + "\n" + JSON.stringify(state) + "\n```"; }
  function parse(text) {
    try {
      var v = JSON.parse(text);
      return v && typeof v === "object" && !Array.isArray(v) ? v : null;
    } catch (e) { return null; }
  }

  function esc(s) {
    return String(s == null ? "" : s).replace(/[&<>"']/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]; });
  }
  function css(id, text) {
    if (typeof document === "undefined" || document.getElementById(id)) return;
    var s = document.createElement("style");
    s.id = id;
    s.textContent = text;
    document.head.appendChild(s);
  }
  function base(name) { return String(name || "").replace(/^.*\//, ""); }
  function textFiles(fs, test) {
    var out = {};
    Object.keys(fs || {}).forEach(function (k) {
      if (typeof fs[k] === "string" && (!test || test(k, fs[k]))) out[k] = fs[k];
    });
    return out;
  }
  function jsonOf(text) { try { return JSON.parse(text); } catch (e) { return null; } }
  function csv(text) {
    var rows = [], row = [], cell = "", q = false, s = String(text || "").replace(/\r/g, "");
    for (var i = 0; i < s.length; i++) {
      var c = s.charAt(i);
      if (q) {
        if (c === '"' && s.charAt(i + 1) === '"') { cell += '"'; i++; } else if (c === '"') q = false; else cell += c;
      } else if (c === '"') q = true;
      else if (c === ",") { row.push(cell); cell = ""; }
      else if (c === "\n") { row.push(cell); rows.push(row); row = []; cell = ""; }
      else cell += c;
    }
    if (cell || row.length) { row.push(cell); rows.push(row); }
    rows = rows.filter(function (r) { return r.length > 1 || r[0]; });
    if (!rows.length) return [];
    var head = rows[0].map(function (h) { return h.trim(); });
    return rows.slice(1).map(function (r) { var o = {}; head.forEach(function (h, i) { o[h] = r[i] == null ? "" : r[i]; }); return o; });
  }
  function download(name, text, type) {
    var a = document.createElement("a");
    a.href = URL.createObjectURL(new Blob([text], { type: type || "text/plain" }));
    a.download = name;
    document.body.appendChild(a);
    a.click();
    setTimeout(function () { URL.revokeObjectURL(a.href); a.remove(); }, 500);
  }

  function md5(bytes) {
    var K = [], S = [7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22, 5, 9, 14, 20, 5, 9, 14, 20, 5, 9, 14, 20, 5, 9, 14, 20,
      4, 11, 16, 23, 4, 11, 16, 23, 4, 11, 16, 23, 4, 11, 16, 23, 6, 10, 15, 21, 6, 10, 15, 21, 6, 10, 15, 21, 6, 10, 15, 21], i;
    for (i = 0; i < 64; i++) K[i] = Math.floor(Math.abs(Math.sin(i + 1)) * 4294967296) | 0;
    var n = bytes.length, len = ((n + 8) >>> 6) + 1, w = new Int32Array(len * 16);
    for (i = 0; i < n; i++) w[i >> 2] |= bytes[i] << ((i % 4) * 8);
    w[n >> 2] |= 0x80 << ((n % 4) * 8);
    w[len * 16 - 2] = (n * 8) | 0;
    w[len * 16 - 1] = Math.floor(n / 536870912);
    var a0 = 0x67452301, b0 = 0xefcdab89 | 0, c0 = 0x98badcfe | 0, d0 = 0x10325476;
    for (var blk = 0; blk < len * 16; blk += 16) {
      var a = a0, b = b0, c = c0, d = d0;
      for (i = 0; i < 64; i++) {
        var f, g;
        if (i < 16) { f = (b & c) | (~b & d); g = i; } else if (i < 32) { f = (d & b) | (~d & c); g = (5 * i + 1) % 16; }
        else if (i < 48) { f = b ^ c ^ d; g = (3 * i + 5) % 16; } else { f = c ^ (b | ~d); g = (7 * i) % 16; }
        var t = d; d = c; c = b;
        var x = (a + f + K[i] + w[blk + g]) | 0;
        b = (b + ((x << S[i]) | (x >>> (32 - S[i])))) | 0;
        a = t;
      }
      a0 = (a0 + a) | 0; b0 = (b0 + b) | 0; c0 = (c0 + c) | 0; d0 = (d0 + d) | 0;
    }
    return [a0, b0, c0, d0].map(function (v) { var s = ""; for (var j = 0; j < 4; j++) s += ("0" + ((v >>> (j * 8)) & 255).toString(16)).slice(-2); return s; }).join("");
  }
  function bytesOf(v) { return typeof v === "string" ? new TextEncoder().encode(v) : v; }
  function digest(algo, v) {
    var b = bytesOf(v);
    if (algo === "md5") return Promise.resolve(md5(b));
    var name = { sha1: "SHA-1", sha256: "SHA-256", sha512: "SHA-512" }[algo];
    if (!name) return Promise.reject(new Error("unknown hash " + algo));
    return global.crypto.subtle.digest(name, b).then(function (h) {
      return Array.prototype.map.call(new Uint8Array(h), function (x) { return ("0" + x.toString(16)).slice(-2); }).join("");
    });
  }

  function frame(el, ctx, o) {
    var st = ctx.state || {}, answer = st.a && typeof st.a === "object" ? st.a : null, last = null;
    el.classList.add("tl-box");
    if (o.cls) el.classList.add(o.cls);
    el.innerHTML = '<div class="tl-head"><b>' + esc(o.title) + '</b><small data-r="note"></small></div>' + o.body +
      '<div class="tl-row tl-acts">' + (o.actions || "") +
      (answer ? '<button type="button" class="btn" data-r="show">' + esc(o.showLabel || "Show the recorded answer") + "</button>" : "") +
      (ctx.record ? '<button type="button" class="btn" data-r="save" disabled>' + esc(ctx.recordLabel || "Add") + "</button>" : "") + "</div>" +
      '<p class="tl-msg" data-r="msg" role="status"></p>' + (o.after || "");
    function r(n) { return el.querySelector('[data-r="' + n + '"]'); }
    var api = {
      st: st, answer: answer, r: r,
      msg: function (t, bad) { var m = r("msg"); m.textContent = t || ""; m.classList.toggle("tl-bad", !!bad); },
      note: function (t) { r("note").textContent = t || ""; },
      ready: function (state, text) {
        last = { state: state, text: text };
        if (r("save")) r("save").disabled = false;
      },
      compare: function (n, what) {
        if (typeof st.n !== "number" || typeof n !== "number") return "";
        return n === st.n ? " Same as the recorded " + (what || "answer") + "." : " The recorded " + (what || "answer") + " found " + st.n + ".";
      },
      remember: function (v) { if (ctx.remember) ctx.remember(v); },
      saved: ctx.saved || null,
      files: function () { return Promise.resolve(ctx.files ? ctx.files() : {}).then(function (f) { return f || {}; }); }
    };
    if (r("save")) r("save").addEventListener("click", function () {
      if (!last) return;
      ctx.record(last.state, last.text);
      api.msg("Added.");
      r("save").disabled = true;
    });
    if (r("show")) r("show").addEventListener("click", function () { if (o.show) o.show(answer); });
    return api;
  }

  var desk = null;
  function access() {
    if (desk) return desk;
    if (global.Paywall && global.Paywall.has("labs")) return Promise.resolve(true);
    var P = global.AayatProgress, who = global.Identity ? global.Identity.getEmail() : "";
    if (!P || !who) return Promise.resolve(false);
    desk = P.neon().then(function (db) {
      if (!db) return false;
      return db.rpc("api_my_access", {}, { attempts: 1 }).then(function (a) { return !!(a && (a.workstation || a.teacher || a.labs)); });
    }).catch(function () { desk = null; return false; });
    return desk;
  }
  function resetAccess() { desk = null; }
  function lockHtml(root) {
    return '<div class="tl-lock"><b>The Hacker Room&rsquo;s programs and simulators come with Seminars or Labs.</b>' +
      "<p>Each seminar teaches its programs step by step, with a hands-on lab and a certificate. Labs gives you incident cases to work in them.</p>" +
      '<p><a class="btn dark" href="' + esc(root || "") + 'workstation.html?trial=1">Try the Hacker Room free</a> <a class="btn" href="' + esc(root || "") + 'seminars.html">See the seminars</a> ' +
      '<a class="btn" href="' + esc(root || "") + 'store.html">Store</a></p></div>';
  }
  if (typeof global.addEventListener === "function") {
    global.addEventListener("aayat-identity", resetAccess);
    global.addEventListener("aayat-identity-set", resetAccess);
  }

  global.AayatTools = {
    register: register, get: get, list: list, fence: fence, parse: parse, groups: GROUPS, access: access, lockHtml: lockHtml,
    kit: { esc: esc, css: css, base: base, textFiles: textFiles, json: jsonOf, csv: csv, download: download, frame: frame, md5: md5, digest: digest, bytes: bytesOf }
  };
})(window);
