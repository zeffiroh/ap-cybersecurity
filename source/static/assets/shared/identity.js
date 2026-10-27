/* student self-identification (email address, no real auth) */
(function (global) {
  "use strict";

  var STORAGE_KEY = "apcyber_student_email";
  var EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]+$/i;

  function normalize(email) {
    return (email || "").trim().toLowerCase();
  }

  function isValid(email) {
    return EMAIL_RE.test(normalize(email));
  }

  function getStoredEmail() {
    try {
      return localStorage.getItem(STORAGE_KEY) || null;
    } catch (e) {
      return null;
    }
  }

  function setStoredEmail(email) {
    try {
      localStorage.setItem(STORAGE_KEY, normalize(email));
    } catch (e) { /* localStorage unavailable, identity just won't persist */ }
    global.dispatchEvent(new Event("aayat-identity-set"));
  }

  function clearStoredEmail() {
    try {
      localStorage.removeItem(STORAGE_KEY);
    } catch (e) { /* no-op */ }
  }

  function injectStyles() {
    if (document.getElementById("identity-modal-styles")) return;
    var style = document.createElement("style");
    style.id = "identity-modal-styles";
    style.textContent =
      ".identity-overlay{position:fixed;inset:0;background:rgba(0,0,0,.45);z-index:9999;" +
      "display:flex;align-items:center;justify-content:center;font-family:'Times New Roman',Times,serif;}" +
      ".identity-box{background:#fff;max-width:380px;width:90%;padding:28px 26px;" +
      "border:1px solid #000;box-shadow:6px 6px 0 rgba(0,0,0,.15);}" +
      ".identity-box h3{margin:0 0 8px;font-family:'Times New Roman',Georgia,serif;font-size:22px;color:#000;}" +
      ".identity-box p{margin:0 0 16px;font-size:13.5px;color:#444;line-height:1.5;}" +
      ".identity-box input{width:100%;padding:9px 10px;font-size:14px;border:1px solid #000;" +
      "box-sizing:border-box;font-family:inherit;}" +
      ".identity-box input:focus{outline:2px solid #000;outline-offset:1px;}" +
      ".identity-error{color:#000;font-size:12.5px;margin-top:6px;min-height:16px;}" +
      ".identity-btn{margin-top:14px;width:100%;padding:10px;background:#000;color:#fff;" +
      "border:none;font-size:13px;text-transform:uppercase;letter-spacing:.5px;cursor:pointer;" +
      "font-family:inherit;font-weight:700;}" +
      ".identity-btn:hover{background:#333;}" +
      ".identity-badge{position:fixed;bottom:10px;right:14px;font-family:'Times New Roman',Times,serif;" +
      "font-size:11px;color:#444;background:#fff;padding:4px 10px;border:1px solid #000;z-index:500;}" +
      ".identity-badge a{color:#000;text-decoration:none;margin-left:8px;cursor:pointer;}" +
      ".identity-badge a:hover{text-decoration:underline;}";
    document.head.appendChild(style);
  }

  function showBadge(email) {
    if (document.querySelector(".apnav")) return;   // the bar shows who is signed in
    injectStyles();
    var existing = document.getElementById("identity-badge");
    if (existing) existing.remove();
    var badge = document.createElement("div");
    badge.id = "identity-badge";
    badge.className = "identity-badge";
    badge.innerHTML = email + '<a id="identity-switch">Switch student</a>';
    document.body.appendChild(badge);
    document.getElementById("identity-switch").addEventListener("click", function () {
      clearStoredEmail();
      badge.remove();
      prompt_(function () { showBadge(getStoredEmail()); });
    });
  }

  function prompt_(onDone) {
    injectStyles();
    var overlay = document.createElement("div");
    overlay.className = "identity-overlay";
    overlay.innerHTML =
      '<div class="identity-box">' +
      "<h3>Sign in</h3>" +
      "<p>Your email keeps your progress and scores, on this device and online.</p>" +
      '<input type="email" placeholder="you@example.com" id="identity-input" autocomplete="email">' +
      '<div class="identity-error" id="identity-error"></div>' +
      '<button class="identity-btn" id="identity-submit">Sign in</button>' +
      "</div>";
    document.body.appendChild(overlay);
    var input = overlay.querySelector("#identity-input");
    var err = overlay.querySelector("#identity-error");
    input.focus();

    function submit() {
      var val = normalize(input.value);
      if (!isValid(val)) {
        err.textContent = "Please enter a valid email address.";
        return;
      }
      setStoredEmail(val);
      overlay.remove();
      if (onDone) onDone(val);
    }

    overlay.querySelector("#identity-submit").addEventListener("click", submit);
    input.addEventListener("keydown", function (e) {
      if (e.key === "Enter") submit();
    });
  }

  var Identity = {
    /** Returns the stored email synchronously, or null if never set. */
    getEmail: function () {
      return getStoredEmail();
    },
    /** Ensures an email is present, prompting the student if not, then calls back with it.
     *  Also renders the small "logged in as" badge once resolved. */
    ensureEmail: function (callback) {
      var existing = getStoredEmail();
      if (existing) {
        showBadge(existing);
        callback(existing);
        return;
      }
      prompt_(function (email) {
        showBadge(email);
        callback(email);
      });
    },
    isValid: isValid,
    clear: clearStoredEmail
  };

  global.Identity = Identity;
})(window);
