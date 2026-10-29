/* Paywall: every page outside APCYBER_PAYWALL.free shows an unlock block until the signed-in account
   has unlocked the course. Unlocked accounts get an occasional donate banner instead.
   The build loads this first thing in <head> of every page, so locked content never flashes. */
(function (global) {
  "use strict";

  var KEY = "apcyber_unlocks";                // { email: { via, ref, ts } }, every account unlocked here
  var EMAIL_KEY = "apcyber_student_email";    // the gradebook sign-in (progress.js, identity.js)
  var DONATE_KEY = "apcyber_donate_next";
  var EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]+$/i;
  var P = global.APCYBER_PAYWALL || {};
  var me = document.currentScript;
  var root = me ? me.src.replace(/assets\/shared\/paywall\.js.*$/, "") : "";

  function get(k) {
    try { return localStorage.getItem(k); } catch (e) { return null; }
  }

  function set(k, v) {
    try { localStorage.setItem(k, v); } catch (e) { /* storage blocked: lasts until the page closes */ }
  }

  function unlocks() {
    try { return JSON.parse(get(KEY) || "{}") || {}; } catch (e) { return {}; }
  }

  function email() {
    return (get(EMAIL_KEY) || "").trim().toLowerCase();
  }

  function isUnlocked(addr) {
    addr = addr === undefined ? email() : addr;
    return !P.enabled || !!(addr && unlocks()[addr]);
  }

  function signIn(addr) {
    if (global.AayatProgress) return global.AayatProgress.signIn(addr);
    set(EMAIL_KEY, addr);
    global.dispatchEvent(new Event("aayat-identity-set"));
  }

  /* Unlock `addr` for good on this browser and sign it in. */
  function unlock(addr, via, ref) {
    var all = unlocks();
    all[addr] = { via: via || "", ref: ref || "", ts: new Date().toISOString() };
    set(KEY, JSON.stringify(all));
    if (!get(DONATE_KEY)) set(DONATE_KEY, String(Date.now() + days(P.donateEveryDays)));
    if (email() !== addr) signIn(addr);
    else apply();
  }

  function days(n) {
    return (Number(n) || 0) * 864e5;
  }

  function neon() {
    var n = (global.APCYBER_CONFIG || {}).neon || {};
    if (!n.authUrl || !n.dataApiUrl) return Promise.reject(new Error("no database"));
    if (global.Neon) return Promise.resolve(global.Neon);
    return new Promise(function (ok, fail) {
      var s = document.createElement("script");
      s.src = root + "assets/shared/neon.js";
      s.onload = function () { ok(global.Neon); };
      s.onerror = fail;
      document.head.appendChild(s);
    });
  }

  /* Whether `addr` has unlocked on any device; unlocks this browser too when it has. */
  function lookup(addr) {
    if (isUnlocked(addr)) return Promise.resolve(true);
    return neon().then(function (N) {
      return N.rpc("api_unlock_status", { p_email: addr }, { attempts: 1 });
    }).then(function (res) {
      if (res && res.unlocked) unlock(addr, "restore", "");
      return !!(res && res.unlocked);
    });
  }

  function glob(p) {
    return new RegExp("^" + p.replace(/[.+?^${}()|[\]\\]/g, "\\$&")
      .replace(/\*\*/g, "\u0000").replace(/\*/g, "[^/]*").replace(/\u0000/g, ".*") + "$");
  }

  /* This page's path from the site root, e.g. "unit-2/2.1/notes.html"; null when outside the site. */
  function pagePath() {
    var here = location.href.split(/[?#]/)[0];
    if (!root || here.indexOf(root) !== 0) return null;
    var p = decodeURIComponent(here.slice(root.length));
    return !p || /\/$/.test(p) ? p + "index.html" : p;
  }

  function hereRel() {
    return (pagePath() || "") + location.search + location.hash;
  }

  function unlockUrl(extra) {
    return root + "unlock/?" + (extra ? extra + "&" : "") + "next=" + encodeURIComponent(hereRel());
  }

  /* The payment page, told where to send the payer when done. */
  function payUrl(ret, extra) {
    var u = new URL(P.payUrl || "pay/", root);
    if (extra) u.search += (u.search ? "&" : "") + extra;
    u.searchParams.set("return", ret);
    return u.href;
  }

  global.Paywall = {
    root: root, email: email, isUnlocked: isUnlocked, unlock: unlock, lookup: lookup, signIn: signIn,
    neon: neon, payUrl: payUrl, EMAIL_RE: EMAIL_RE
  };
  if (!P.enabled || !root) return;

  var path = pagePath();
  var free = path === null || (P.free || []).some(function (f) { return glob(f).test(path); });
  var quiet = /^(unlock|pay|buy|ledger)\//.test(path || "");
  var framed = global.self !== global.top;           // teacher previews: the outer page shows the bars

  var css = document.createElement("style");
  css.textContent =
    "html.pw-locked body>*:not(.apnav):not(.pw-gate){display:none!important}" +
    ".pw-gate{position:fixed;inset:0;z-index:999;overflow:auto;background:#fff;color:#111;" +
    "font-family:'Times New Roman',Times,Georgia,serif;display:flex;align-items:flex-start;justify-content:center;" +
    "padding:96px 16px 48px;box-sizing:border-box}" +
    ".pw-card{max-width:440px;width:100%;border:1px solid #000;box-shadow:6px 6px 0 rgba(0,0,0,.15);padding:30px 26px;" +
    "text-align:center;box-sizing:border-box;background:#fff}" +
    ".pw-card img{width:56px;height:56px;display:block;margin:0 auto 14px}" +
    ".pw-card h2{font-size:24px;margin:0 0 8px;font-weight:700}" +
    ".pw-card p{font-size:15px;line-height:1.5;color:#444;margin:0 0 18px}" +
    ".pw-btn{display:block;background:#000;color:#fff!important;text-decoration:none;padding:12px;font-weight:700;" +
    "font-size:14px;letter-spacing:.5px;text-transform:uppercase}" +
    ".pw-btn:hover{background:#333}" +
    ".pw-links{margin-top:16px;font-size:14px;display:flex;justify-content:center;gap:18px;flex-wrap:wrap}" +
    ".pw-links a{color:#111}" +
    ".pw-who{margin-top:20px;padding-top:16px;border-top:1px solid #d4d4d4;font-size:14px;color:#444}" +
    ".pw-who form{display:flex;gap:6px;margin-top:8px}" +
    ".pw-who input{flex:1;min-width:0;padding:8px;font:inherit;border:1px solid #000}" +
    ".pw-who button{padding:8px 12px;font:inherit;font-weight:700;background:#fff;border:1px solid #000;cursor:pointer}" +
    ".pw-who .pw-msg{min-height:18px;margin-top:6px}" +
    ".pw-bar{position:fixed;left:0;right:0;bottom:0;z-index:998;background:#000;color:#fff;font:15px/1.4 'Times New Roman',Times,serif;" +
    "display:flex;align-items:center;justify-content:center;gap:10px 16px;padding:10px 44px 10px 16px;flex-wrap:wrap;text-align:center}" +
    ".pw-bar a{color:#fff;font-weight:700}" +
    ".pw-bar .pw-x{position:absolute;right:10px;top:50%;transform:translateY(-50%);background:none;border:0;color:#fff;" +
    "font-size:20px;cursor:pointer;padding:4px 8px}" +
    ".pw-bar .pw-later{background:none;border:0;color:#ccc;font:inherit;text-decoration:underline;cursor:pointer}" +
    ".pw-btn:focus-visible,.pw-links a:focus-visible,.pw-bar a:focus-visible,.pw-bar button:focus-visible{outline:3px solid #888;outline-offset:2px}";
  document.head.appendChild(css);

  function remove(sel) {
    var el = document.querySelector(sel);
    if (el) el.remove();
  }

  function gate() {
    var g = document.createElement("div"), who = email();
    g.className = "pw-gate";
    g.innerHTML =
      '<div class="pw-card" role="dialog" aria-labelledby="pw-title">' +
      '<img src="' + root + 'assets/theme/icon.svg" alt="">' +
      '<h2 id="pw-title">Part of the full course</h2>' +
      "<p>Unlock once and your account keeps every topic, lecture, quiz, lab, unit test, the book and the capstone " +
      "for good. Pay what you want, or use a code.</p>" +
      '<a class="pw-btn" href="' + unlockUrl() + '">Unlock the course</a>' +
      '<div class="pw-links"><a href="' + unlockUrl("code=1") + '">I have a code</a>' +
      '<a href="' + root + 'unit-1/1.1/index.html">Try Topic 1.1 free</a></div>' +
      '<div class="pw-who"></div></div>';
    var box = g.querySelector(".pw-who");
    if (who) {
      box.textContent = "Signed in as " + who + ". This account hasn't unlocked the course yet.";
    } else {
      box.innerHTML = "Unlocked before? Sign in with that email." +
        '<form><input type="email" placeholder="you@example.com" autocomplete="email" aria-label="Email" required>' +
        '<button type="submit">Sign in</button></form><div class="pw-msg" role="status"></div>';
      box.querySelector("form").addEventListener("submit", function (e) {
        e.preventDefault();
        var v = box.querySelector("input").value.trim().toLowerCase();
        if (!EMAIL_RE.test(v)) return;
        box.querySelector(".pw-msg").textContent = "Checking…";
        signIn(v);
      });
    }
    return g;
  }

  function bar(html, cls) {
    var b = document.createElement("div");
    b.className = "pw-bar " + cls;
    b.innerHTML = html + '<button type="button" class="pw-x" aria-label="Hide">&times;</button>';
    document.body.appendChild(b);
    return b;
  }

  function ribbon() {
    try { if (sessionStorage.getItem("pw-ribbon-off")) return; } catch (e) {}
    var b = bar('<span>This part is free. The rest of the course is pay what you want.</span>' +
      '<a href="' + unlockUrl() + '">Unlock the full course &rarr;</a>', "pw-ribbon");
    b.querySelector(".pw-x").addEventListener("click", function () {
      b.remove();
      try { sessionStorage.setItem("pw-ribbon-off", "1"); } catch (e) {}
    });
  }

  /* Wikipedia-style: now and then, ask an unlocked account to give (again). */
  function donate() {
    var every = days(P.donateEveryDays);
    var canPay = (P.payUrl && P.payUrl !== "pay/") ||
      ((P.pay || {}).methods || []).some(function (m) { return m.url || m.qr; });
    if (!every || !canPay || Date.now() < Number(get(DONATE_KEY) || 0)) return;
    var b = bar("<span>This course is kept going by learners who chip in. If it has helped you, " +
      "please consider giving what you can.</span>" +
      '<a href="' + payUrl(location.href, "donate=1") + '">Donate</a>' +
      '<button type="button" class="pw-later">Maybe later</button>', "pw-donate");
    function snooze() {
      set(DONATE_KEY, String(Date.now() + every));
      b.remove();
    }
    b.querySelector("a").addEventListener("click", snooze);
    b.querySelector(".pw-later").addEventListener("click", snooze);
    b.querySelector(".pw-x").addEventListener("click", snooze);
  }

  /* Lock or open the page for whoever is signed in now. */
  function apply() {
    var open = isUnlocked(), html = document.documentElement;
    html.classList.toggle("pw-locked", !free && !open);
    if (!document.body) return;
    remove(".pw-gate");
    remove(".pw-bar");
    if (quiet) return;
    if (!free && !open) document.body.appendChild(gate());
    else if (framed) return;
    else if (open) donate();
    else ribbon();
  }

  function check() {
    var who = email();
    if (who && !isUnlocked(who)) lookup(who).catch(function () { /* offline or no database: stay locked */ });
  }

  document.documentElement.classList.toggle("pw-locked", !free && !isUnlocked());
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", apply);
  else apply();
  check();
  function changed() { apply(); check(); }
  global.addEventListener("aayat-identity", changed);
  global.addEventListener("aayat-identity-set", changed);
  global.addEventListener("storage", function (e) { if (e.key === EMAIL_KEY || e.key === KEY) changed(); });
})(window);
