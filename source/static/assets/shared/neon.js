/* Neon transport (the site's only backend) */
(function (global) {
  "use strict";

  var TOKEN_KEY = "apcyber_neon_token_v1";
  var tokenPromise = null;

  function cfg() {
    var n = (global.APCYBER_CONFIG && global.APCYBER_CONFIG.neon) || {};
    return {
      authUrl: String(n.authUrl || "").replace(/\/+$/, ""),
      dataApiUrl: String(n.dataApiUrl || "").replace(/\/+$/, "")
    };
  }

  function isConfigured() {
    var c = cfg();
    return !!(c.authUrl && c.dataApiUrl);
  }

  /* expires_at may arrive in seconds or milliseconds. */
  function expiryMs(v) {
    var n = Number(v) || 0;
    return n < 1e12 ? n * 1000 : n;
  }

  function readCached() {
    try {
      var t = JSON.parse(sessionStorage.getItem(TOKEN_KEY) || "null");
      if (t && t.token && expiryMs(t.expires_at) - Date.now() > 30000) return t.token;
    } catch (e) { /* storage unavailable: just fetch a fresh token */ }
    return null;
  }

  function getToken(force) {
    if (!force) {
      var cached = readCached();
      if (cached) return Promise.resolve(cached);
      if (tokenPromise) return tokenPromise;
    }
    tokenPromise = fetch(cfg().authUrl + "/token/anonymous", { credentials: "omit" })
      .then(function (res) {
        if (!res.ok) throw new Error("Neon Auth token request failed: HTTP " + res.status);
        return res.json();
      })
      .then(function (t) {
        if (!t || !t.token) throw new Error("Neon Auth returned no token");
        try { sessionStorage.setItem(TOKEN_KEY, JSON.stringify(t)); } catch (e) {}
        tokenPromise = null;
        return t.token;
      }, function (err) {
        tokenPromise = null;
        throw err;
      });
    return tokenPromise;
  }

  function rpc(fn, args, opts) {
    if (!isConfigured()) return Promise.reject(new Error("Neon is not configured"));
    opts = opts || {};
    var attempts = opts.attempts || 3;
    function attempt(n, forceToken) {
      return getToken(forceToken).then(function (token) {
        return fetch(cfg().dataApiUrl + "/rpc/" + fn, {
          method: "POST",
          headers: { "Content-Type": "application/json", "Authorization": "Bearer " + token },
          body: JSON.stringify(args || {}),
          keepalive: !!opts.keepalive,
          credentials: "omit"
        });
      }).then(function (res) {
        if (res.status === 401 && !forceToken) return attempt(n, true);
        if (!res.ok) {
          return res.text().then(function (t) {
            var err = new Error("Neon " + fn + " failed: HTTP " + res.status + " " + t.slice(0, 200));
            err.retryable = res.status >= 500 || res.status === 429;
            throw err;
          });
        }
        return res.json();
      }).catch(function (err) {
        var retryable = err.retryable !== false && !(err instanceof SyntaxError);
        if (n >= attempts || !retryable) throw err;
        return new Promise(function (r) { setTimeout(r, n * 1500); })
          .then(function () { return attempt(n + 1, false); });
      });
    }
    return attempt(1, false);
  }

  global.Neon = { isConfigured: isConfigured, rpc: rpc };
})(window);
