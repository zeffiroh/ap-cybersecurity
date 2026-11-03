(function (global) {
  "use strict";

  var STORAGE_KEY = "apcyber_student_email";
  var SESSION_KEY = "apcyber_session";
  var EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]+$/i;
  var me = document.currentScript;
  var root = me ? me.src.replace(/assets\/shared\/identity\.js.*$/, "") : "";
  var waiting = [];
  var open_ = null;

  function normalize(email) {
    return (email || "").trim().toLowerCase();
  }

  function isValid(email) {
    return EMAIL_RE.test(normalize(email));
  }

  function get(k) {
    try { return localStorage.getItem(k) || ""; } catch (e) { return ""; }
  }

  function set(k, v) {
    try { localStorage.setItem(k, v); } catch (e) {  }
  }

  function del(k) {
    try { localStorage.removeItem(k); } catch (e) {  }
  }

  if (get(STORAGE_KEY) && !get(SESSION_KEY)) del(STORAGE_KEY);

  function getStoredEmail() {
    return get(SESSION_KEY) ? normalize(get(STORAGE_KEY)) || null : null;
  }

  function neon() {
    if (global.Neon) return Promise.resolve(global.Neon);
    if (global.Paywall) return global.Paywall.neon();
    return new Promise(function (ok, fail) {
      var s = document.createElement("script");
      s.src = root + "assets/shared/neon.js";
      s.onload = function () { ok(global.Neon); };
      s.onerror = fail;
      document.head.appendChild(s);
    });
  }

  function rpc(fn, args) {
    return neon().then(function (N) { return N.rpc(fn, args, { attempts: 2 }); });
  }

  function announce(email) {
    if (global.AayatProgress) global.AayatProgress.signIn(email);
    else global.dispatchEvent(new Event("aayat-identity-set"));
  }

  function signedIn(res) {
    set(SESSION_KEY, res.token);
    set(STORAGE_KEY, res.email);
    announce(res.email);
  }

  function clearStoredEmail() {
    del(SESSION_KEY);
    del(STORAGE_KEY);
  }

  function signOut() {
    var had = get(SESSION_KEY);
    var done = function () {
      clearStoredEmail();
      global.dispatchEvent(new Event("aayat-identity-set"));
    };
    if (!had) return Promise.resolve(done());
    return rpc("api_sign_out", {}).catch(function () {  }).then(done);
  }

  function injectStyles() {
    if (document.getElementById("identity-modal-styles")) return;
    var style = document.createElement("style");
    style.id = "identity-modal-styles";
    style.textContent =
      ".identity-overlay{position:fixed;inset:0;background:rgba(0,0,0,.45);z-index:10000;" +
      "display:flex;align-items:center;justify-content:center;font-family:'Times New Roman',Times,serif;" +
      "padding:16px;box-sizing:border-box;overflow:auto}" +
      ".identity-box{position:relative;background:#fff;color:#111;max-width:380px;width:100%;padding:28px 26px;" +
      "border:1px solid #000;box-shadow:6px 6px 0 rgba(0,0,0,.15);box-sizing:border-box;text-align:left}" +
      ".identity-box h3{margin:0 0 8px;font-family:'Times New Roman',Georgia,serif;font-size:22px;color:#000}" +
      ".identity-box p{margin:0 0 14px;font-size:14px;color:#444;line-height:1.5}" +
      ".identity-box label{display:block;font-size:13px;font-weight:700;margin:10px 0 4px}" +
      ".identity-box input{width:100%;padding:9px 10px;font-size:15px;border:1px solid #000;" +
      "box-sizing:border-box;font-family:inherit;background:#fff;color:#111}" +
      ".identity-box input:focus{outline:2px solid #000;outline-offset:1px}" +
      ".identity-error{color:#9b1c1c;font-size:13px;margin-top:8px;min-height:17px}" +
      ".identity-btn{margin-top:12px;width:100%;padding:11px;background:#000;color:#fff;" +
      "border:none;font-size:13px;text-transform:uppercase;letter-spacing:.5px;cursor:pointer;" +
      "font-family:inherit;font-weight:700}" +
      ".identity-btn:hover{background:#333}.identity-btn[disabled]{background:#777;cursor:wait}" +
      ".identity-links{margin-top:14px;font-size:14px;display:flex;justify-content:space-between;gap:10px;flex-wrap:wrap}" +
      ".identity-links a{color:#111;cursor:pointer}" +
      ".identity-x{position:absolute;right:8px;top:6px;background:none;border:0;font-size:22px;cursor:pointer;color:#111;padding:4px 8px}" +
      ".identity-badge{position:fixed;bottom:10px;right:14px;font-family:'Times New Roman',Times,serif;" +
      "font-size:11px;color:#444;background:#fff;padding:4px 10px;border:1px solid #000;z-index:500}" +
      ".identity-badge a{color:#000;text-decoration:none;margin-left:8px;cursor:pointer}" +
      ".identity-badge a:hover{text-decoration:underline}";
    document.head.appendChild(style);
  }

  function field(id, label, type, auto) {
    return '<label for="id-' + id + '">' + label + '</label><input id="id-' + id + '" type="' + type +
      '" autocomplete="' + auto + '"' + (type === "text" ? ' inputmode="numeric" maxlength="6"' : "") + ">";
  }

  var MODES = {
    signin: {
      title: "Sign in",
      text: "Your account keeps your course access, progress and grades. Only you and your instructor see your grades.",
      fields: [["email", "Email", "email", "email"], ["pw", "Password", "password", "current-password"]],
      button: "Sign in",
      links: [["forgot", "Forgot password?"], ["signup", "New here? Create an account"]]
    },
    signup: {
      title: "Create your account",
      text: "Use the email you paid or signed up with. Choose a password of at least 8 characters.",
      fields: [["email", "Email", "email", "email"], ["pw", "Password", "password", "new-password"],
               ["pw2", "Password again", "password", "new-password"]],
      button: "Create account",
      links: [["signin", "Already have an account? Sign in"]]
    },
    forgot: {
      title: "Reset your password",
      text: "Enter your account's email and we'll send you a 6-digit code.",
      fields: [["email", "Email", "email", "email"]],
      button: "Email me a code",
      links: [["signin", "Back to sign in"]]
    },
    reset: {
      title: "Enter your code",
      text: "",
      fields: [["code", "6-digit code", "text", "one-time-code"], ["pw", "New password", "password", "new-password"],
               ["pw2", "New password again", "password", "new-password"]],
      button: "Set new password",
      links: [["forgot", "Send a new code"], ["signin", "Back to sign in"]]
    },
    change: {
      title: "Choose a new password",
      text: "Pick a password only you know, at least 8 characters.",
      fields: [["pw", "New password", "password", "new-password"], ["pw2", "New password again", "password", "new-password"]],
      button: "Save password",
      links: []
    }
  };

  function finish(email) {
    if (open_) { open_.remove(); open_ = null; }
    var cbs = waiting;
    waiting = [];
    cbs.forEach(function (cb) { try { cb(email); } catch (e) { console.error(e); } });
  }

  function dialog(mode, opts) {
    opts = opts || {};
    injectStyles();
    if (open_) open_.remove();
    var M = MODES[mode];
    var forced = mode === "change" && opts.forced;
    var overlay = document.createElement("div");
    overlay.className = "identity-overlay";
    var text = mode === "reset"
      ? "We emailed a code to " + opts.email + ". It can take up to 5 minutes to arrive; check your spam folder too. The code works for 30 minutes."
      : forced ? "You signed in with the starter password. Choose your own now so only you can see your grades." : M.text;
    overlay.innerHTML =
      '<form class="identity-box" role="dialog" aria-labelledby="identity-title" novalidate>' +
      (forced ? "" : '<button type="button" class="identity-x" aria-label="Close">&times;</button>') +
      '<h3 id="identity-title">' + M.title + "</h3><p></p>" +
      M.fields.map(function (f) { return field(f[0], f[1], f[2], f[3]); }).join("") +
      '<div class="identity-error" role="status"></div>' +
      '<button type="submit" class="identity-btn">' + M.button + "</button>" +
      '<div class="identity-links">' + M.links.map(function (l) {
        return '<a data-go="' + l[0] + '" tabindex="0">' + l[1] + "</a>";
      }).join("") + "</div></form>";
    overlay.querySelector("p").textContent = text;
    document.body.appendChild(overlay);
    open_ = overlay;

    var form = overlay.querySelector("form");
    var err = overlay.querySelector(".identity-error");
    var btn = overlay.querySelector(".identity-btn");
    var val = function (id) { var el = overlay.querySelector("#id-" + id); return el ? el.value : ""; };
    var emailEl = overlay.querySelector("#id-email");
    if (emailEl && opts.email) emailEl.value = opts.email;
    var first = overlay.querySelector(emailEl && opts.email ? "#id-pw, #id-code" : "input");
    if (first) first.focus();

    var x = overlay.querySelector(".identity-x");
    if (x) x.addEventListener("click", function () { overlay.remove(); open_ = null; waiting = []; });
    overlay.querySelectorAll("[data-go]").forEach(function (a) {
      var go = function () { dialog(a.getAttribute("data-go"), { email: normalize(val("email")) || opts.email }); };
      a.addEventListener("click", go);
      a.addEventListener("keydown", function (e) { if (e.key === "Enter") go(); });
    });

    function busy(on) { btn.disabled = on; }
    function fail(msg) { busy(false); err.textContent = msg; }
    function oops() { fail("Couldn't reach the course server. Check your connection and try again."); }

    form.addEventListener("submit", function (e) {
      e.preventDefault();
      err.textContent = "";
      var email = normalize(val("email")) || opts.email || "";
      if (emailEl && !isValid(email)) return fail("Please enter a valid email address.");
      if (overlay.querySelector("#id-pw2") && val("pw") !== val("pw2")) return fail("The two passwords don't match.");
      busy(true);
      if (mode === "signin") {
        if (!val("pw")) return fail("Enter your password.");
        rpc("api_sign_in", { p_email: email, p_password: val("pw") }).then(function (res) {
          if (!res || !res.ok) {
            if (res && res.noAccount) return dialog("signup", { email: email });
            return fail((res && res.error) || "Wrong email or password.");
          }
          signedIn(res);
          if (res.mustChange) dialog("change", { forced: true, email: res.email });
          else finish(res.email);
        }, oops);
      } else if (mode === "signup") {
        rpc("api_sign_up", { p_email: email, p_password: val("pw") }).then(function (res) {
          if (!res || !res.ok) return fail((res && res.error) || "That didn't work. Please try again.");
          signedIn(res);
          finish(res.email);
        }, oops);
      } else if (mode === "forgot") {
        rpc("api_forgot_password", { p_email: email }).then(function () {
          dialog("reset", { email: email });
        }, oops);
      } else if (mode === "reset") {
        rpc("api_reset_password", { p_email: opts.email, p_code: val("code").trim(), p_new: val("pw") }).then(function (res) {
          if (!res || !res.ok) return fail((res && res.error) || "That didn't work. Please try again.");
          signedIn(res);
          finish(res.email);
        }, oops);
      } else if (mode === "change") {
        rpc("api_change_password", { p_new: val("pw") }).then(function (res) {
          if (!res || !res.ok) return fail((res && res.error) || "That didn't work. Please try again.");
          finish(getStoredEmail());
        }, oops);
      }
    });
  }

  function open(opts, cb) {
    opts = opts || {};
    if (cb) waiting.push(cb);
    dialog(opts.mode || "signin", opts);
  }

  function showBadge(email) {
    if (document.querySelector(".apnav")) return;
    injectStyles();
    var existing = document.getElementById("identity-badge");
    if (existing) existing.remove();
    var badge = document.createElement("div");
    badge.id = "identity-badge";
    badge.className = "identity-badge";
    badge.textContent = email;
    var a = document.createElement("a");
    a.textContent = "Sign out";
    a.addEventListener("click", function () {
      signOut().then(function () {
        badge.remove();
        open({}, function (e) { showBadge(e); });
      });
    });
    badge.appendChild(a);
    document.body.appendChild(badge);
  }

  global.Identity = {
    getEmail: function () {
      return getStoredEmail();
    },
    ensureEmail: function (callback) {
      var existing = getStoredEmail();
      if (existing) {
        showBadge(existing);
        callback(existing);
        return;
      }
      open({}, function (email) {
        showBadge(email);
        callback(email);
      });
    },
    open: open,
    signOut: signOut,
    changePassword: function () { open({ mode: "change" }); },
    isValid: isValid,
    clear: clearStoredEmail
  };
})(window);
