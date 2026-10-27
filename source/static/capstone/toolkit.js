/* "mhsec" toolkit, browser port */
(function (global) {
  "use strict";

  var RISKY_SERVICES = ["telnet", "dicom", "ftp", "ssh"];
  var URGENCY = ["urgent", "immediately", "24 hours", "act now", "locked", "verify"];
  var AUTHORITY = ["it department", "it-support", "administrator", "help desk", "official"];

  function uniqueSorted(arr) {
    return Array.from(new Set(arr)).sort();
  }

  var Toolkit = {
    /** recon(network) -> [{ip, name, subnet, risky_services}] sorted by ip */
    recon: function (network) {
      var out = [];
      network.hosts.forEach(function (h) {
        var risky = uniqueSorted(
          (h.services || []).filter(function (s) { return RISKY_SERVICES.indexOf(s.name) !== -1; })
            .map(function (s) { return s.name; })
        );
        if (h.subnet === "DMZ" || risky.length > 0) {
          out.push({ ip: h.ip, name: h.name, subnet: h.subnet, risky_services: risky });
        }
      });
      return out.sort(function (a, b) { return a.ip.localeCompare(b.ip); });
    },

    /** detect_spray(auth_logs, minUsers=5, minFails=20) -> [{src_ip, users, fails}] */
    detect_spray: function (authLogs, minUsers, minFails) {
      minUsers = minUsers == null ? 5 : minUsers;
      minFails = minFails == null ? 20 : minFails;
      var fails = {}, users = {};
      authLogs.forEach(function (e) {
        var ok = e.ok === undefined ? true : e.ok;
        if (!ok) {
          fails[e.src_ip] = (fails[e.src_ip] || 0) + 1;
          users[e.src_ip] = users[e.src_ip] || new Set();
          users[e.src_ip].add(e.user);
        }
      });
      var out = [];
      Object.keys(fails).forEach(function (ip) {
        if (users[ip].size >= minUsers && fails[ip] >= minFails) {
          out.push({ src_ip: ip, users: users[ip].size, fails: fails[ip] });
        }
      });
      return out.sort(function (a, b) {
        if (b.fails !== a.fails) return b.fails - a.fails;
        return a.src_ip.localeCompare(b.src_ip);
      });
    },

    /** find_phish(emails, legitDomain="meridian-health.org") -> [{id, from, to, indicators}] */
    find_phish: function (emails, legitDomain) {
      legitDomain = legitDomain || "meridian-health.org";
      var out = [];
      emails.forEach(function (m) {
        var ind = [];
        var dom = m.from.split("@").pop().toLowerCase();
        if (dom !== legitDomain && dom.indexOf("meridian") !== -1) ind.push("lookalike-domain");
        var text = ((m.subject || "") + " " + (m.body || "")).toLowerCase();
        if (URGENCY.some(function (w) { return text.indexOf(w) !== -1; })) ind.push("urgency");
        var fromPlusText = m.from.toLowerCase() + " " + text;
        if (AUTHORITY.some(function (w) { return fromPlusText.indexOf(w) !== -1; })) ind.push("authority");
        var link = m.link || "";
        if (link.indexOf("http") === 0 && (link.indexOf("verify") !== -1 || link.indexOf("owa") !== -1)) {
          ind.push("credential-link");
        }
        if (ind.length > 0) {
          out.push({ id: m.id, from: m.from, to: m.to, indicators: uniqueSorted(ind) });
        }
      });
      return out.sort(function (a, b) { return String(a.id).localeCompare(String(b.id)); });
    },

    /** ir_timeline(emails, authLogs, meta) -> {victim, entry_email, lookalike_domain,
     *  compromised_login_src, recommendation} */
    ir_timeline: function (emails, authLogs, meta) {
      var phish = Toolkit.find_phish(emails).filter(function (m) {
        return m.indicators.indexOf("lookalike-domain") !== -1;
      });
      var victimUser = meta.victim.split("@")[0];
      var suspicious = authLogs.filter(function (e) {
        return e.user === victimUser && e.geo === "unusual";
      });
      return {
        victim: meta.victim,
        entry_email: phish.length ? phish[0].id : null,
        lookalike_domain: meta.lookalike_domain,
        compromised_login_src: suspicious.length ? suspicious[0].src_ip : null,
        recommendation: ["reset victim credentials", "enable MFA", "block lookalike domain", "user awareness training"],
      };
    },

    /** find_lateral_movement(networkLogs, meta) -> [{ts, src_ip, dst_ip, service}] in time order */
    find_lateral_movement: function (networkLogs, meta) {
      var hostIp = meta.compromised_host === "ws-nguyen" ? "10.20.5.40" : meta.compromised_host;
      var hops = networkLogs.filter(function (e) { return e.src_ip === hostIp; });
      return hops
        .slice().sort(function (a, b) { return a.ts - b.ts; })
        .map(function (e) { return { ts: e.ts, src_ip: e.src_ip, dst_ip: e.dst_ip, service: e.service }; });
    },

    /** detect_ioc(deviceLogs, meta) -> [{host, process, hash}] sorted by host */
    detect_ioc: function (deviceLogs, meta) {
      var out = deviceLogs
        .filter(function (e) { return e.hash === meta.ioc_hash || e.process === meta.ioc_process; })
        .map(function (e) { return { host: e.host, process: e.process, hash: e.hash }; });
      return out.sort(function (a, b) { return a.host.localeCompare(b.host); });
    },

    /** detect_exfil(appLogs, meta) -> [{host, dst_ip, bytes_out}] sorted desc by bytes_out */
    detect_exfil: function (appLogs, meta) {
      var out = appLogs
        .filter(function (e) { return e.dst_ip === meta.exfil_dst_ip && e.bytes_out >= meta.exfil_bytes_threshold; })
        .map(function (e) { return { host: e.host, dst_ip: e.dst_ip, bytes_out: e.bytes_out }; });
      return out.sort(function (a, b) { return b.bytes_out - a.bytes_out; });
    },

    /** full_incident_report(world, meta) -> aggregate after-action report */
    full_incident_report: function (world, meta) {
      return {
        ir_timeline: Toolkit.ir_timeline(world.emails, world.auth_logs, meta),
        lateral_movement: Toolkit.find_lateral_movement(world.network_logs, meta),
        ioc_matches: Toolkit.detect_ioc(world.device_logs, meta),
        exfiltration: Toolkit.detect_exfil(world.app_logs, meta),
        recommendation: [
          "isolate ws-nguyen", "rotate DC/fileserver credentials",
          "block exfil destination IP", "restore from clean backup",
          "patch/remove legacy telnet+dicom exposure on pacs",
        ],
      };
    },
  };

  global.Toolkit = Toolkit;
})(window);
