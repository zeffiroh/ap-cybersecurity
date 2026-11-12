(function (global) {
  "use strict";
  var me = document.currentScript && document.currentScript.src;
  var ROOT = me ? me.replace(/assets\/theme\/tool-proxy\.js.*$/, "") : "";
  var BLANK = "___";
  var REASON = { 0: "Held", 200: "OK", 201: "Created", 302: "Found", 400: "Bad Request", 401: "Unauthorized", 403: "Forbidden", 404: "Not Found", 405: "Method Not Allowed", 409: "Conflict", 500: "Internal Server Error" };
  var CSS = ".tx-box .tx-tabs{display:flex;flex-wrap:wrap;gap:4px;margin:8px 0 6px}.tx-box .tx-tabs button{border:1px solid #000;background:#fff;color:#111;padding:3px 9px;cursor:pointer;font-size:12px}" +
    ".tx-box .tx-tabs button.on{background:#111;color:#fff}.tx-box .tx-tabs em{font-style:normal;background:#c0392b;color:#fff;border-radius:8px;padding:0 6px;margin-left:4px;font-size:11px}" +
    ".tx-box textarea{width:100%;box-sizing:border-box;font:12px/1.45 ui-monospace,Consolas,monospace;border:1px solid #000;padding:6px;background:#fff;color:#111;resize:vertical}" +
    ".tx-box .tx-split{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:8px}@media (max-width:760px){.tx-box .tx-split{grid-template-columns:1fr}}" +
    ".tx-box .tx-pane h4{margin:6px 0 4px;font-size:12px}.tx-box pre.tx-raw{margin:0;border:1px solid #bbb;padding:6px;min-height:120px;max-height:320px;overflow:auto;background:#fafafa;font:12px/1.45 ui-monospace,Consolas,monospace;white-space:pre-wrap;word-break:break-word}" +
    ".tx-box .tx-scroll{max-height:220px;overflow:auto;border:1px solid #bbb;background:#fff;margin-bottom:8px}.tx-box table{border-collapse:collapse;width:100%;font:12px/1.35 ui-monospace,Consolas,monospace}" +
    ".tx-box th{position:sticky;top:0;background:#e8e8e8;text-align:left;padding:3px 6px;border-bottom:1px solid #999}.tx-box td{padding:2px 6px;border-bottom:1px solid #eee;white-space:nowrap;max-width:360px;overflow:hidden;text-overflow:ellipsis}" +
    ".tx-box tr.tx-row{cursor:pointer}.tx-box tr.tx-row:hover td{background:#f3f3f3}.tx-box tr.tx-row.on td{background:#1f4e8c;color:#fff}.tx-box tr.err td:nth-child(4){color:#c0392b;font-weight:bold}" +
    ".tx-box .tx-on{background:#c0392b!important;color:#fff!important;border-color:#c0392b!important}.tx-box .tx-small{font-size:12px;color:#555;margin:6px 0}";

  var lastToken = "";

  function style() {
    if (document.getElementById("tool-proxy-css")) return;
    var s = document.createElement("style");
    s.id = "tool-proxy-css";
    s.textContent = CSS;
    document.head.appendChild(s);
  }
  function esc(s) {
    return String(s == null ? "" : s).replace(/[&<>"']/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]; });
  }
  function script(src) {
    return new Promise(function (ok, bad) {
      var s = document.createElement("script");
      s.src = src;
      s.onload = ok;
      s.onerror = function () { bad(new Error("Couldn't load " + src.split("/").pop())); };
      document.head.appendChild(s);
    });
  }

  var loading = null;
  function shop() {
    if (global.NimbuShop) return global.NimbuShop.boot().then(function () { return global.NimbuShop; });
    if (!loading) {
      loading = (global.initSqlJs ? Promise.resolve() : script(ROOT + "assets/vendor/sqljs-1.13.0/sql-wasm.js"))
        .then(function () { return global.NimbuShop ? null : script(ROOT + "assets/theme/shop-lab.js"); })
        .then(function () { return global.NimbuShop.boot(); })
        .then(function () { return global.NimbuShop; });
      loading.catch(function () { loading = null; });
    }
    return loading;
  }

  function cap(k) { return k.replace(/(^|-)([a-z])/g, function (m, a, b) { return a + b.toUpperCase(); }); }

  function rawRequest(req) {
    var hs = Object.keys(req.headers || {}).map(function (k) { return cap(k) + ": " + req.headers[k]; });
    return req.method + " " + req.path + " HTTP/1.1\nHost: nimbu.shop" + (hs.length ? "\n" + hs.join("\n") : "") + "\n\n" + (req.body || "");
  }

  function parseRaw(text) {
    var s = String(text || "").replace(/\r/g, ""), cut = s.indexOf("\n\n"), head = cut < 0 ? s : s.slice(0, cut), body = cut < 0 ? "" : s.slice(cut + 2);
    var lines = head.split("\n"), m = /^\s*([A-Za-z]+)\s+(\S+)(?:\s+HTTP\/[\d.]+)?\s*$/.exec(lines[0] || "");
    if (!m) throw new Error("The first line should look like  GET /api/products HTTP/1.1");
    var headers = {};
    lines.slice(1).forEach(function (l) {
      var i = l.indexOf(":");
      if (i <= 0) return;
      var k = l.slice(0, i).trim().toLowerCase(), v = l.slice(i + 1).trim();
      if (k === "host" || k === "content-length") return;
      headers[k] = v;
    });
    var path = m[2].replace(/^https?:\/\/nimbu\.shop/i, "") || "/";
    if (path.charAt(0) !== "/") path = "/" + path;
    return { method: m[1].toUpperCase(), path: path, headers: headers, body: body.replace(/\s+$/, "") };
  }

  function withToken(text, sh) {
    var t = (sh && sh.token()) || lastToken;
    return String(text).split("{{token}}").join(t || "");
  }
  function tokenized(text, sh) {
    var out = String(text);
    [sh && sh.token(), lastToken].forEach(function (t) { if (t && t.length > 20) out = out.split(t).join("{{token}}"); });
    return out;
  }

  function rawResponse(res) {
    if (!res) return "";
    var body = res.body || "";
    if (res.type === "application/json") { try { body = JSON.stringify(JSON.parse(body), null, 2); } catch (e) {} }
    var loc = res.status === 302 ? (/Location: (.*)/.exec(res.body || "") || [])[1] : "";
    return "HTTP/1.1 " + res.status + " " + (REASON[res.status] || "") + "\nContent-Type: " + (res.type || "text/plain") + "\nContent-Length: " + (res.body || "").length + (loc ? "\nLocation: " + loc : "") + "\n\n" + body;
  }

  function seeToken(res) {
    if (!res || res.type !== "application/json") return;
    try { var t = JSON.parse(res.body).token; if (t) lastToken = t; } catch (e) {}
  }

  function mount(el, ctx) {
    style();
    var st = ctx.state || {}, saved = ctx.saved || {}, answer = st.a && typeof st.a === "object" ? st.a : null, sh = null, off = null;
    var hasStep = !!st.m, tab = saved.tab || (hasStep ? "repeat" : "intercept"), pick = null, last = null, filter = "";
    var rep = saved.rep != null ? saved.rep : hasStep ? stepRaw(st) : "GET /api/products?q= HTTP/1.1\nHost: nimbu.shop\n\n", repOut = "";
    el.classList.add("tl-box", "tx-box");
    el.innerHTML = '<div class="tl-head"><b>Web proxy</b><small data-r="note">Starting the shop…</small></div>' +
      '<div class="tx-tabs" role="tablist"><button data-pv="intercept">Intercept<em data-r="count" hidden></em></button><button data-pv="history">HTTP history</button><button data-pv="repeat">Repeater</button>' +
      '<button data-pv="reset" title="Start the shop again with fresh data">Reset the shop</button></div>' +
      '<p class="tl-msg" data-r="msg" role="status"></p><div data-r="body"></div>';
    function r(n) { return el.querySelector('[data-r="' + n + '"]'); }

    function stepRaw(s) {
      var head = (s.m || "GET") + " " + (s.p || BLANK) + " HTTP/1.1\nHost: nimbu.shop" + (s.h ? "\n" + s.h : "");
      return head + "\n\n" + (s.b != null && s.b !== "" ? s.b : s.blank && s.blank.indexOf("b") >= 0 && answer && answer.b ? BLANK : "");
    }
    function remember() { if (ctx.remember) ctx.remember({ tab: tab, rep: rep }); }

    function tabs() {
      el.querySelectorAll("[data-pv]").forEach(function (b) { b.classList.toggle("on", b.getAttribute("data-pv") === tab); });
      var n = sh ? sh.held().length : 0;
      r("count").hidden = !n;
      r("count").textContent = n;
    }

    function draw() {
      tabs();
      var b = r("body");
      if (!sh) { b.innerHTML = ""; return; }
      if (tab === "intercept") {
        var held = sh.held(), on = sh.intercept(), first = held[0];
        b.innerHTML = '<div class="tl-row"><button type="button" class="btn' + (on ? " tx-on" : "") + '" data-px="toggle">Intercept is ' + (on ? "on" : "off") + "</button>" +
          (first ? '<button type="button" class="btn dark" data-px="forward">Forward</button><button type="button" class="btn" data-px="drop">Drop</button><button type="button" class="btn" data-px="torep">Send to Repeater</button>' : "") +
          '<span class="tx-small">' + (held.length ? held.length + " waiting" : on ? "Waiting for the next request…" : "Requests pass straight through.") + "</span></div>" +
          (first ? '<p class="tx-small">Request #' + first.n + ". Change anything you like, then Forward it to the shop.</p><textarea data-r=\"held\" rows=\"9\" spellcheck=\"false\"></textarea>" : "") +
          (sh.page() ? '<p class="tx-small">With Intercept on, every request the shop page makes stops here first. The page reloads after the last one is forwarded or dropped.</p>' :
            '<div class="tl-row" style="margin-top:8px"><label>Browser <select data-r="bm"><option>GET</option><option>POST</option></select></label>' +
            '<label class="tl-grow">Address <input data-r="bp" value="/api/products?q=" spellcheck="false" autocomplete="off"></label>' +
            '<label class="tl-grow">Body (JSON, for POST) <input data-r="bb" spellcheck="false" autocomplete="off" placeholder="{&quot;email&quot;:&quot;demo@nimbu.shop&quot;,&quot;password&quot;:&quot;demo123&quot;}"></label>' +
            '<button type="button" class="btn" data-px="browse">Send through the proxy</button></div>' +
            '<p class="tx-small">This browser sends requests to the simulated nimbu.shop the way the shop page would, so Intercept can catch them.</p>');
        if (first) r("held").value = rawRequest(first.req);
      } else if (tab === "history") {
        var list = sh.history().filter(function (x) { return !filter || (x.req.method + " " + x.req.path + " " + x.res.status).toLowerCase().indexOf(filter.toLowerCase()) >= 0; });
        var p = pick != null ? sh.history().filter(function (x) { return x.n === pick; })[0] : null;
        b.innerHTML = '<div class="tl-row"><label class="tl-grow">Filter <input data-r="hf" spellcheck="false" autocomplete="off" placeholder="path, method or status, for example  /api/orders"></label></div>' +
          '<div class="tx-scroll"><table><tr><th>#</th><th>Method</th><th>Path</th><th>Status</th><th>Length</th><th>Type</th><th>From</th></tr>' + list.map(function (x) {
            return '<tr class="tx-row' + (x.n === pick ? " on" : "") + (x.res.status >= 400 ? " err" : "") + '" data-pn="' + x.n + '"><td>' + x.n + "</td><td>" + esc(x.req.method) + '</td><td title="' + esc(x.req.path) + '">' + esc(x.req.path) +
              "</td><td>" + x.res.status + "</td><td>" + (x.res.body || "").length + "</td><td>" + esc(x.res.type) + "</td><td>" + (x.from === "proxy" ? "Repeater" : "Browser") + "</td></tr>";
          }).join("") + "</table></div>" + (list.length ? "" : '<p class="tx-small">Nothing yet. Use the shop, the browser on the Intercept tab, or the Repeater.</p>') +
          (p ? '<div class="tl-row"><button type="button" class="btn" data-px="torep2">Send to Repeater</button></div><div class="tx-split"><div class="tx-pane"><h4>Request</h4><pre class="tx-raw" data-r="hreq"></pre></div>' +
            '<div class="tx-pane"><h4>Response</h4><pre class="tx-raw" data-r="hres"></pre></div></div>' : "");
        r("hf").value = filter;
        if (p) { r("hreq").textContent = rawRequest(p.req); r("hres").textContent = rawResponse(p.res); }
      } else {
        b.innerHTML = '<div class="tl-row"><button type="button" class="btn dark" data-px="send">Send</button>' +
          (answer ? '<button type="button" class="btn" data-px="show">Show the recorded request</button>' : "") +
          (ctx.record ? '<button type="button" class="btn" data-px="save"' + (last ? "" : " disabled") + ">" + esc(ctx.recordLabel) + "</button>" : "") +
          '<span class="tx-small">Write <code>{{token}}</code> to use the token from your last login.</span></div>' +
          '<div class="tx-split"><div class="tx-pane"><h4>Request</h4><textarea data-r="rep" rows="12" spellcheck="false"></textarea></div><div class="tx-pane"><h4>Response</h4><pre class="tx-raw" data-r="rout"></pre></div></div>';
        r("rep").value = rep;
        r("rout").textContent = repOut;
      }
    }

    function send() {
      rep = r("rep").value;
      remember();
      if (rep.indexOf(BLANK) >= 0) { r("msg").textContent = "Fill in the " + BLANK + " blanks first."; return; }
      var req;
      try { req = parseRaw(withToken(rep, sh)); } catch (e) { r("msg").textContent = e.message; return; }
      if (/\{\{token\}\}/.test(rep) && !sh.token() && !lastToken) { r("msg").textContent = "There's no token yet. Log in first (POST /api/login), then send this again."; return; }
      if (req.body && !req.headers["content-type"]) req.headers["content-type"] = "application/json";
      var res = sh.exchange(req);
      seeToken(res);
      repOut = rawResponse(res);
      r("rout").textContent = repOut;
      var text = "Status " + res.status + " " + (REASON[res.status] || "") + ".";
      if (typeof st.s === "number") text += res.status === st.s ? " Same status as the recorded request." : " The recorded request got " + st.s + ".";
      r("msg").textContent = text;
      var hs = Object.keys(req.headers).filter(function (k) { return k !== "content-length"; }).map(function (k) { return cap(k) + ": " + req.headers[k]; }).join("\n");
      last = { m: req.method, p: tokenized(req.path, sh), h: tokenized(hs, sh), b: tokenized(req.body, sh), s: res.status };
      var sv = el.querySelector('[data-px="save"]');
      if (sv) sv.disabled = false;
    }

    el.addEventListener("click", function (e) {
      var t = e.target.closest("[data-pv],[data-px],[data-pn]");
      if (!t || !el.contains(t)) return;
      e.stopPropagation();
      if (!sh) return;
      if (t.hasAttribute("data-pv")) {
        var v = t.getAttribute("data-pv");
        if (v === "reset") { sh.reset(); lastToken = ""; pick = null; r("msg").textContent = "The shop is back to its starting data."; draw(); return; }
        if (tab === "repeat" && r("rep")) rep = r("rep").value;
        tab = v;
        remember();
        return draw();
      }
      if (t.hasAttribute("data-pn")) { pick = +t.getAttribute("data-pn"); return draw(); }
      var a = t.getAttribute("data-px");
      if (a === "toggle") { sh.intercept(!sh.intercept()); return draw(); }
      if (a === "forward" || a === "drop" || a === "torep") {
        if (a === "torep") { rep = r("held").value; tab = "repeat"; remember(); return draw(); }
        var edited = null;
        if (a === "forward") {
          try { edited = parseRaw(r("held").value); } catch (err) { r("msg").textContent = err.message; return; }
        }
        var res = a === "forward" ? sh.forward(0, edited) : sh.drop(0);
        seeToken(res);
        r("msg").textContent = a === "forward" ? "Forwarded. The shop answered " + (res ? res.status : "") + ". See it in HTTP history." : "Dropped. The shop never saw it.";
        return draw();
      }
      if (a === "browse") {
        var body = r("bb").value.trim();
        var out = sh.browse(r("bm").value, r("bp").value.trim() || "/", r("bm").value === "POST" ? body || "{}" : null);
        seeToken(out.raw);
        r("msg").textContent = out.status ? "The shop answered " + out.status + "." : "Held by the proxy.";
        return draw();
      }
      if (a === "torep2") {
        var p = sh.history().filter(function (x) { return x.n === pick; })[0];
        if (p) { rep = tokenized(rawRequest(p.req), sh); tab = "repeat"; remember(); draw(); }
        return;
      }
      if (a === "send") return send();
      if (a === "show") {
        var s = { m: st.m, p: answer.p != null ? answer.p : st.p, h: st.h, b: answer.b != null ? answer.b : st.b };
        rep = (s.m || "GET") + " " + (s.p || "/") + " HTTP/1.1\nHost: nimbu.shop" + (s.h ? "\n" + s.h : "") + "\n\n" + (s.b || "");
        r("rep").value = rep;
        remember();
        return;
      }
      if (a === "save" && last) {
        ctx.record({ m: last.m, p: last.p, h: last.h, b: last.b, s: last.s, blank: ["p", "b"] }, "Web proxy: " + last.m + " " + last.p + " (status " + last.s + ")");
        r("msg").textContent = "Added.";
        t.disabled = true;
      }
    });
    el.addEventListener("input", function (e) {
      if (e.target === r("hf")) {
        filter = e.target.value;
        var pos = e.target.selectionStart;
        draw();
        r("hf").focus();
        r("hf").setSelectionRange(pos, pos);
      }
      if (e.target === r("rep")) { rep = e.target.value; remember(); }
    });
    el.addEventListener("keydown", function (e) {
      if (e.target === r("rep") && e.key === "Enter" && (e.ctrlKey || e.metaKey)) { e.preventDefault(); send(); }
    });

    shop().then(function (s) {
      sh = s;
      r("note").textContent = sh.page() ? "In front of nimbu.shop" : "nimbu.shop (a simulated shop, separate from the Hack the shop page)";
      off = sh.on(function (kind) {
        if (!el.isConnected) { off(); return; }
        if (kind === "held" && tab === "intercept" && r("held")) { tabs(); var sp = el.querySelector(".tx-box .tl-row .tx-small"); if (sp) sp.textContent = sh.held().length + " waiting"; return; }
        if (kind === "held" || kind === "released" || kind === "reset") return draw();
        if (kind === "log" && tab === "history") draw();
        tabs();
      });
      draw();
    }).catch(function (e) { r("note").textContent = ""; r("msg").textContent = "The shop didn't start: " + e.message; });
  }

  global.AayatTools.register({ id: "proxy", title: "Web proxy", console: true, mount: mount, parseRaw: parseRaw, rawRequest: rawRequest });
})(window);
