/* Audience measurement for sponsorship */

(function (global) {
  "use strict";

  var STORAGE_KEY = "apcyber_view_pings_v1";

  function neonReady() {
    return !!(global.Neon && global.Neon.isConfigured());
  }

  function unitIdFor(pathname) {
    var m = /\/Unit_(\d+)_/.exec(pathname);
    if (m) return "unit-" + m[1];
    if (/book\.html$/i.test(pathname)) return "book";
    return "site";
  }

  function today() {
    return new Date().toISOString().slice(0, 10);
  }

  function alreadyCountedToday(unitId) {
    var day = today();
    var seen;
    try {
      seen = JSON.parse(localStorage.getItem(STORAGE_KEY) || "{}");
    } catch (e) {
      return false;
    }
    if (!seen || typeof seen !== "object") seen = {};
    if (seen[unitId] === day) return true;
    /* Drop yesterday's entries so this never grows without bound. */
    Object.keys(seen).forEach(function (k) {
      if (seen[k] !== day) delete seen[k];
    });
    seen[unitId] = day;
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(seen));
    } catch (e) {
      /* Nothing to do; the ping below still goes out. */
    }
    return false;
  }

  function record() {
    if (!neonReady()) return;

    var unitId = unitIdFor(location.pathname);
    if (alreadyCountedToday(unitId)) return;

    Neon.rpc("api_page_view", { p_unit: unitId }, { keepalive: true, attempts: 1 }).catch(function () {
      /* Measurement is never worth interrupting a reader over. */
    });
  }

  /* Reads the tallies back for the support page's rate card. */
  function fetchMetrics() {
    if (!neonReady()) return Promise.resolve(null);
    return Neon.rpc("api_ad_metrics", {})
      .then(function (data) {
        return data && data.ok ? data : null;
      })
      .catch(function () { return null; });
  }

  global.APCYBER_METRICS = {
    unitIdFor: unitIdFor,
    fetchMetrics: fetchMetrics
  };

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", record);
  } else {
    record();
  }
})(window);
