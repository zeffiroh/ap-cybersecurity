(function (global) {
  "use strict";
  var K = global.AayatTools.kit;
  var RISKY = /\.(exe|scr|js|jse|vbs|vbe|wsf|hta|bat|cmd|ps1|lnk|iso|img|docm|xlsm|pptm|one|jar|msi|html?|zip|rar|7z)$/i;
  var URGENT = /\b(urgent|immediately|today|final notice|suspend|suspended|expires?|within \d+ hours?|confidential|act now|verify|locked|overdue|before \d)/gi;
  var VERDICTS = [["", "Not decided"], ["phish", "Phishing: block and warn"], ["bec", "Fraud request (BEC): stop the payment"], ["spam", "Spam or marketing: no threat"], ["legit", "Genuine: tell the reporter"]];
  var CSS = ".tm-box .tm-wrap{display:grid;grid-template-columns:220px minmax(0,1fr);gap:10px;margin-top:8px}@media (max-width:820px){.tm-box .tm-wrap{grid-template-columns:1fr}}" +
    ".tm-box .tm-q{border:1px solid #bbb;background:#fff;font-size:12.5px;max-height:460px;overflow:auto}.tm-box .tm-q button{display:block;width:100%;text-align:left;border:0;border-bottom:1px solid #eee;background:none;padding:6px 8px;cursor:pointer;color:#111;font:inherit}" +
    ".tm-box .tm-q button.on{background:#1f4e8c;color:#fff}.tm-box .tm-q small{display:block;opacity:.75}.tm-box .tm-card{border:1px solid #bbb;background:#fff;padding:8px 10px;font-size:13px;min-width:0}" +
    ".tm-box .tm-hops{font-size:12px}.tm-box .tm-why li{margin:2px 0}.tm-box .tm-why li.bad{color:#a11}.tm-box .tm-why li.ok{color:#256b3d}" +
    ".tm-box pre{white-space:pre-wrap;word-break:break-word;background:#f4f4f4;padding:6px;font:12px/1.4 ui-monospace,Consolas,monospace;max-height:220px;overflow:auto}";

  function headers(raw) {
    var text = String(raw).replace(/\r/g, ""), cut = text.indexOf("\n\n"), head = cut < 0 ? text : text.slice(0, cut), body = cut < 0 ? "" : text.slice(cut + 2);
    var list = [];
    head.split("\n").forEach(function (l) {
      if (/^[ \t]/.test(l) && list.length) list[list.length - 1][1] += " " + l.trim();
      else { var i = l.indexOf(":"); if (i > 0) list.push([l.slice(0, i).trim(), l.slice(i + 1).trim()]); }
    });
    return { list: list, body: body };
  }
  function get(h, name) { var n = name.toLowerCase(); for (var i = 0; i < h.list.length; i++) if (h.list[i][0].toLowerCase() === n) return h.list[i][1]; return ""; }
  function all(h, name) { var n = name.toLowerCase(); return h.list.filter(function (x) { return x[0].toLowerCase() === n; }).map(function (x) { return x[1]; }); }
  function addr(v) { var m = /<([^>]+)>/.exec(v || ""); return (m ? m[1] : String(v || "").split(",")[0]).trim().toLowerCase(); }
  function display(v) { var m = /^\s*"?([^"<]*?)"?\s*</.exec(v || ""); return m ? m[1].trim() : ""; }
  function domainOf(a) { return String(a).split("@").pop().toLowerCase(); }
  function org(d) { var p = String(d).split("."); return p.slice(-2).join("."); }
  function lev(a, b) {
    var m = [], i, j;
    for (i = 0; i <= a.length; i++) { m[i] = [i]; }
    for (j = 0; j <= b.length; j++) m[0][j] = j;
    for (i = 1; i <= a.length; i++) for (j = 1; j <= b.length; j++) m[i][j] = Math.min(m[i - 1][j] + 1, m[i][j - 1] + 1, m[i - 1][j - 1] + (a.charAt(i - 1) === b.charAt(j - 1) ? 0 : 1));
    return m[a.length][b.length];
  }
  function skeleton(s) { return String(s).toLowerCase().replace(/rn/g, "m").replace(/vv/g, "w").replace(/[1il|]/g, "l").replace(/0/g, "o").replace(/[^a-z0-9]/g, ""); }

  function parts(h) {
    var ct = get(h, "Content-Type"), m = /boundary="?([^";]+)"?/i.exec(ct), out = [];
    if (!m) return [{ type: ct || "text/plain", name: "", body: h.body }];
    h.body.split("--" + m[1]).forEach(function (chunk) {
      if (/^--\s*$/.test(chunk) || !chunk.trim()) return;
      var p = headers(chunk.replace(/^\n/, "")), pct = get(p, "Content-Type"), disp = get(p, "Content-Disposition");
      var name = (/name="?([^";]+)"?/i.exec(disp) || /name="?([^";]+)"?/i.exec(pct) || [])[1] || "";
      out.push({ type: pct || "text/plain", name: name, body: p.body });
    });
    return out;
  }
  function links(ps) {
    var out = [];
    ps.forEach(function (p) {
      if (/html/i.test(p.type)) {
        var re = /<a\b[^>]*href\s*=\s*["']([^"']+)["'][^>]*>([\s\S]*?)<\/a>/gi, m;
        while ((m = re.exec(p.body))) out.push({ href: m[1], text: m[2].replace(/<[^>]+>/g, "").trim() });
      } else if (/text|^$/i.test(p.type) && !p.name) {
        var r2 = /https?:\/\/[^\s<>"']+/g, x;
        while ((x = r2.exec(p.body))) out.push({ href: x[0], text: "" });
      }
    });
    return out;
  }
  function hostOf(u) { return String(u).replace(/^[a-z]+:\/\//i, "").split(/[/:?#]/)[0].toLowerCase(); }

  function analyse(raw, ours) {
    var h = headers(raw), from = get(h, "From"), fromA = addr(from), fromD = domainOf(fromA), disp = display(from);
    var reply = addr(get(h, "Reply-To")), ret = addr(get(h, "Return-Path")), auth = all(h, "Authentication-Results").join(" ");
    var res = { spf: (/spf=(\w+)/i.exec(auth) || [])[1] || "none", dkim: (/dkim=(\w+)/i.exec(auth) || [])[1] || "none", dmarc: (/dmarc=(\w+)/i.exec(auth) || [])[1] || "none" };
    var hops = all(h, "Received").map(function (r) {
      var f = /from\s+(\S+)(?:\s+\(([^)]*)\))?/i.exec(r) || [], by = /\bby\s+(\S+)/i.exec(r) || [], ip = /\[(\d{1,3}(?:\.\d{1,3}){3})\]/.exec(r) || [], t = /;\s*(.+)$/.exec(r) || [];
      return { from: f[1] || "", by: by[1] || "", ip: ip[1] || "", time: t[1] || "", when: t[1] ? Date.parse(t[1].replace(/\s*\([^)]*\)\s*$/, "")) : NaN };
    });
    var ps = parts(h), ls = links(ps), why = [], score = 0;
    function flag(bad, text, w) { why.push({ bad: bad, text: text }); if (bad) score += w || 1; }
    ["spf", "dkim", "dmarc"].forEach(function (k) { if (res[k] === "pass") flag(false, k.toUpperCase() + " passed"); else flag(true, k.toUpperCase() + " is " + res[k], k === "dmarc" ? 2 : 1); });
    if (reply && domainOf(reply) !== fromD) flag(true, "Replies go to " + domainOf(reply) + ", not the sender's domain " + fromD, 2);
    if (ret && org(domainOf(ret)) !== org(fromD)) flag(res.dmarc !== "pass", "The envelope sender (Return-Path) is " + domainOf(ret) + ", different from " + fromD, 1);
    var lookFor = (ours || []).concat(disp ? [disp] : []), fromLabel = fromD.split(".").slice(0, -1).join(""), fromSk = skeleton(fromLabel), told = false;
    lookFor.forEach(function (o) {
      o = String(o).toLowerCase();
      if (told || o === fromD) return;
      var label = o.split(".").length > 1 ? o.split(".").slice(0, -1).join("") : o, sk = skeleton(label);
      if (!sk || sk.length < 4 || label.replace(/[^a-z0-9]/g, "") === fromLabel.replace(/[^a-z0-9]/g, "")) return;
      if (fromSk === sk || lev(fromSk, sk) <= 2) { told = true; flag(true, "The sender's domain " + fromD + " looks like \"" + o + "\" but isn't it", 3); }
    });
    if (/\((cfo|ceo|md|director|finance)\)|\b(cfo|ceo)\b/i.test(disp) && /freemail|gmail|outlook|yahoo|proton/i.test(fromD)) flag(true, "A senior title (" + disp + ") writing from a free mail address", 3);
    ls.forEach(function (l) {
      var hh = hostOf(l.href);
      if (l.text && /^https?:\/\//i.test(l.text) && hostOf(l.text) !== hh) flag(true, "A link shows " + hostOf(l.text) + " but really goes to " + hh, 3);
      if (/^http:\/\//i.test(l.href)) flag(true, "A link uses plain http: " + hh, 1);
      if (/\.(docm|xlsm|exe|scr|js|hta|iso|zip|lnk)(\?|$)/i.test(l.href)) flag(true, "A link downloads a risky file type: " + l.href.split("/").pop(), 2);
    });
    ps.filter(function (p) { return p.name; }).forEach(function (p) { if (RISKY.test(p.name)) flag(true, "Attachment with a risky type: " + p.name, 2); });
    var words = (get(h, "Subject") + " " + ps.map(function (p) { return p.body; }).join(" ")).match(URGENT) || [];
    if (words.length >= 2) flag(true, "Pressure words: " + words.slice(0, 5).map(function (w) { return w.toLowerCase(); }).filter(function (w, i, a) { return a.indexOf(w) === i; }).join(", "), 1);
    if (/bank|ifsc|account no|wire|transfer|payment/i.test(h.body) && /keep this between us|confidential|can't take calls|reply here/i.test(h.body)) flag(true, "Asks for a payment change and for secrecy", 3);
    if (get(h, "List-Unsubscribe")) flag(false, "Has an unsubscribe header, like normal bulk mail");
    for (var i = 1; i < hops.length; i++) if (!isNaN(hops[i].when) && !isNaN(hops[i - 1].when) && hops[i - 1].when < hops[i].when) flag(true, "The Received times run backwards, which is a sign of forged headers", 2);
    return { subject: get(h, "Subject"), from: from, fromA: fromA, fromD: fromD, display: disp, reply: reply, ret: ret, to: get(h, "To"), date: get(h, "Date"), id: get(h, "Message-ID"),
      auth: res, hops: hops, links: ls, parts: ps, why: why, score: score, risk: score >= 6 ? "high" : score >= 3 ? "medium" : "low", headers: h.list };
  }

  function mount(el, ctx) {
    K.css("tool-email-css", CSS);
    var mails = {}, names = [], cur = "", d = {}, ours = [];
    var F = K.frame(el, ctx, {
      title: "Email triage", cls: "tm-box",
      body: '<div class="tl-row"><label class="tl-grow">Your organisation\'s domains <input data-r="ours" placeholder="kestrel.lan, kestrel-logistics.com"></label></div>',
      actions: '<button type="button" class="btn dark" data-r="done">Finish the queue</button>',
      showLabel: "Show the recorded verdicts",
      show: function (a) { if (a.d) { d = JSON.parse(JSON.stringify(a.d)); queue(); card(); } },
      after: '<div class="tm-wrap"><div class="tm-q" data-r="q"></div><div class="tm-card" data-r="card">Pick a reported email.</div></div>'
    });
    var init = F.saved || F.st;
    function keep() { F.remember({ d: d, ours: F.r("ours").value, file: cur }); }
    function queue() {
      F.r("q").innerHTML = names.map(function (n) {
        var a = analyse(mails[n], ours), v = (VERDICTS.filter(function (x) { return x[0] === (d[n] || ""); })[0] || VERDICTS[0])[1];
        return '<button type="button" data-m="' + K.esc(n) + '"' + (n === cur ? ' class="on"' : "") + "><b>" + K.esc(a.subject || K.base(n)) + "</b><small>" + K.esc(a.display || a.fromA) + "</small><small>" + K.esc(v) + "</small></button>";
      }).join("");
    }
    function card() {
      if (!cur) return;
      var a = analyse(mails[cur], ours);
      F.r("card").innerHTML = "<h4 style=\"margin:0 0 6px\"></h4>" +
        '<div class="te-grid" style="display:grid;grid-template-columns:max-content 1fr;gap:2px 12px;font-size:12.5px">' +
        [["From", a.from], ["Reply-To", a.reply], ["Return-Path", a.ret], ["To", a.to], ["Date", a.date], ["Message-ID", a.id], ["SPF / DKIM / DMARC", a.auth.spf + " / " + a.auth.dkim + " / " + a.auth.dmarc]]
          .filter(function (p) { return p[1]; }).map(function (p) { return "<span style=\"color:#555\">" + K.esc(p[0]) + "</span><span>" + K.esc(p[1]) + "</span>"; }).join("") + "</div>" +
        '<p><b>Risk: <span class="tl-pill ' + (a.risk === "high" ? "hi" : a.risk === "medium" ? "mid" : "ok") + '">' + a.risk + "</span></b> score " + a.score + "</p>" +
        '<ul class="tm-why">' + a.why.map(function (w) { return '<li class="' + (w.bad ? "bad" : "ok") + '">' + (w.bad ? "&#9888; " : "&#10003; ") + K.esc(w.text) + "</li>"; }).join("") + "</ul>" +
        "<details><summary>Path the email took (" + a.hops.length + " hop" + (a.hops.length === 1 ? "" : "s") + ", newest first)</summary><table class=\"tl-table tm-hops\"><tr><th>From</th><th>IP</th><th>By</th><th>Time</th></tr>" +
        a.hops.map(function (x) { return "<tr><td>" + K.esc(x.from) + "</td><td>" + K.esc(x.ip) + "</td><td>" + K.esc(x.by) + "</td><td>" + K.esc(x.time) + "</td></tr>"; }).join("") + "</table></details>" +
        (a.links.length ? "<details><summary>Links (" + a.links.length + ")</summary><ul>" + a.links.map(function (l) { return "<li>" + K.esc(l.href) + (l.text ? " <small>shown as " + K.esc(l.text) + "</small>" : "") + "</li>"; }).join("") + "</ul></details>" : "") +
        "<details><summary>All headers</summary><pre data-r=\"raw\"></pre></details>" +
        '<label style="font-size:12px;display:block;margin-top:8px">Your verdict <select data-r="v">' + VERDICTS.map(function (v) { return '<option value="' + v[0] + '"' + ((d[cur] || "") === v[0] ? " selected" : "") + ">" + K.esc(v[1]) + "</option>"; }).join("") + "</select></label>";
      F.r("card").querySelector("h4").textContent = a.subject;
      F.r("raw").textContent = a.headers.map(function (x) { return x[0] + ": " + x[1]; }).join("\n");
      F.r("v").addEventListener("change", function () { if (this.value) d[cur] = this.value; else delete d[cur]; keep(); queue(); });
    }
    F.r("q").addEventListener("click", function (e) { var b = e.target.closest("[data-m]"); if (!b) return; cur = b.getAttribute("data-m"); keep(); queue(); card(); });
    F.r("ours").addEventListener("change", function () { ours = this.value.split(/[\s,]+/).filter(Boolean); keep(); queue(); card(); });
    F.r("done").addEventListener("click", function () {
      var left = names.filter(function (n) { return !d[n]; }).length, bad = names.filter(function (n) { return d[n] === "phish" || d[n] === "bec"; }).length;
      var msg = (left ? left + " email" + (left === 1 ? "" : "s") + " still need a verdict. " : "Every report has a verdict. ") + bad + " to block or stop.";
      if (F.answer && F.answer.d) { var w = F.answer.d, same = Object.keys(w).filter(function (k) { return d[k] === w[k]; }).length; msg += " " + same + " of " + Object.keys(w).length + " match the recorded verdicts."; }
      F.msg(msg);
      F.ready({ d: d, n: bad, files: names, blank: ["d"] }, "Email triage: " + names.length + " reported emails, " + bad + " malicious");
    });

    F.note("Loading the emails…");
    F.files().then(function (fs) {
      mails = K.textFiles(fs, function (n) { return /\.eml$/i.test(n); });
      names = Object.keys(mails).sort();
      F.note(names.length + " emails");
      if (!names.length) { F.msg("There are no .eml files here."); F.r("done").disabled = true; return; }
      var tos = {};
      names.forEach(function (n) { String(analyse(mails[n], []).to).split(",").forEach(function (t) { var a = addr(t); if (a.indexOf("@") > 0) tos[domainOf(a)] = 1; }); });
      F.r("ours").value = init.ours || Object.keys(tos).join(", ");
      ours = F.r("ours").value.split(/[\s,]+/).filter(Boolean);
      if (init.d && typeof init.d === "object") d = JSON.parse(JSON.stringify(init.d));
      cur = init.file && mails[init.file] ? init.file : names[0];
      queue();
      card();
    }).catch(function () { F.note(""); F.msg("The files didn't load.", true); });
  }

  global.AayatTools.register({ id: "email", title: "Email triage", console: true, group: "SOC analyst", mount: mount, analyse: analyse, headers: headers });
})(window);
