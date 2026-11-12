(function (global) {
  "use strict";
  var K = global.AayatTools.kit;
  var FW = {
    iso: { title: "ISO/IEC 27001:2022 (selected Annex A controls, paraphrased)", note: "Paraphrased for teaching. Use the licensed standard for real audits.", items: [
      ["5.1", "Security policies are written, approved and shared"], ["5.2", "Security roles and responsibilities are assigned"], ["5.9", "There is an inventory of information and assets, with owners"],
      ["5.15", "Access to information follows the business need"], ["5.19", "Supplier security is agreed and checked"], ["5.24", "There is a plan for handling security incidents"],
      ["5.29", "Security continues during a disruption"], ["5.30", "IT is ready for business continuity"], ["6.3", "Staff get security awareness training"],
      ["7.2", "Physical entry to secure areas is controlled"], ["8.2", "Privileged access is limited and managed"], ["8.5", "Logins are secure (for example MFA)"],
      ["8.7", "Protection against malware is in place"], ["8.8", "Technical vulnerabilities are found and fixed in time"], ["8.13", "Backups are made and tested"],
      ["8.15", "Activity is logged"], ["8.16", "Systems and networks are monitored for unusual activity"], ["8.20", "Networks are secured"], ["8.24", "Cryptography is used correctly"],
      ["8.28", "Code is written securely"]] },
    soc2: { title: "SOC 2 Trust Services Criteria (summary, paraphrased)", note: "SOC 2 is a report on your controls, not a certificate. Paraphrased categories only.", items: [
      ["CC1", "Control environment: leadership sets the tone, roles are clear"], ["CC2", "Communication: security information reaches the right people"], ["CC3", "Risk assessment is done and used"],
      ["CC4", "Controls are monitored and problems fixed"], ["CC5", "Control activities: policies turned into procedures"], ["CC6", "Logical and physical access is controlled"],
      ["CC7", "System operations: incidents are detected and handled"], ["CC8", "Changes are authorised, tested and approved"], ["CC9", "Risks from vendors and disruptions are managed"],
      ["A1", "Availability commitments are met (capacity, backups, recovery)"], ["C1", "Confidential information is protected and disposed of"]] },
    pci: { title: "PCI DSS v4.0 (the 12 requirements, paraphrased)", note: "Applies if you store, process or send card data. Paraphrased.", items: [
      ["1", "Network security controls are installed and kept up"], ["2", "Secure settings on every system, no defaults"], ["3", "Stored account data is protected"],
      ["4", "Card data is encrypted over public networks"], ["5", "Systems are protected from malware"], ["6", "Systems and software are developed and kept secure"],
      ["7", "Access is limited to business need to know"], ["8", "Users are identified and authenticated"], ["9", "Physical access to card data is restricted"],
      ["10", "All access to systems and card data is logged and monitored"], ["11", "Security is tested regularly"], ["12", "Policies and programmes support security"]] },
    dpdp: { title: "India: Digital Personal Data Protection Act, 2023", note: "From the Act. The Rules phase in duties over time: check the current Gazette before relying on a date.", items: [
      ["s.5", "A clear notice tells people what personal data is collected and why"], ["s.6", "Consent is free, specific, informed and can be withdrawn as easily as given"],
      ["s.7", "Any processing without consent fits one of the Act's legitimate uses"], ["s.8(5)", "Reasonable security safeguards protect the personal data"],
      ["s.8(6)", "Breaches are reported to the Data Protection Board and to affected people"], ["s.8(7)", "Data is erased when its purpose is over, unless the law needs it kept"],
      ["s.8(9)", "Someone is named to answer people's questions about their data"], ["s.8(10)", "There is a way to handle complaints (grievance redressal)"],
      ["s.9", "Children's data: verifiable parental consent, no tracking or targeted ads"], ["s.11-14", "People can access, correct and erase their data, complain, and nominate someone"]] },
    certin: { title: "CERT-In Directions, 28 April 2022", note: "From the Directions under s.70B of the IT Act. Check CERT-In's site for updates and FAQs.", items: [
      ["Report", "Listed cyber incidents are reported to CERT-In within 6 hours of noticing them"], ["Clocks", "System clocks sync to NIC or NPL time servers (or ones traceable to them)"],
      ["Logs", "Logs of ICT systems are kept for 180 days, in India"], ["Contact", "A point of contact is named to CERT-In"],
      ["Respond", "CERT-In's requests for information are answered in the time it sets"], ["Providers", "Data centres, cloud, VPN and VPS providers keep the subscriber records the Directions require"]] }
  };
  var STATUS = [["", "-"], ["met", "Met"], ["partial", "Partly"], ["gap", "Gap"], ["na", "Not applicable"]];
  var CSS = ".tco-box select{font-size:12px}.tco-box input{width:100%;box-sizing:border-box;font-size:12px;padding:2px 4px}.tco-box tr.gap td{background:#fde2e1}.tco-box tr.partial td{background:#fff3cd}.tco-box tr.met td{background:#eef8f1}";

  function score(fw, ans) {
    var it = FW[fw].items, c = { met: 0, partial: 0, gap: 0, na: 0, open: 0 };
    it.forEach(function (x) { var s = (ans[fw + ":" + x[0]] || {}).s || ""; if (s) c[s]++; else c.open++; });
    var scoped = it.length - c.na;
    return { c: c, pct: scoped ? Math.round((c.met + c.partial / 2) / scoped * 100) : 0 };
  }

  function mount(el, ctx) {
    K.css("tool-compliance-css", CSS);
    var ans = {}, fw = "iso";
    var F = K.frame(el, ctx, {
      title: "Compliance gap check", cls: "tco-box",
      body: '<div class="tl-row"><label class="tl-grow">Framework <select data-r="fw">' + Object.keys(FW).map(function (k) { return '<option value="' + k + '">' + K.esc(FW[k].title) + "</option>"; }).join("") +
        '</select></label></div><p class="tl-msg" data-r="fnote" style="font-size:12px"></p><div class="tl-scroll" data-r="list" style="max-height:440px"></div>',
      actions: '<button type="button" class="btn dark" data-r="done">Score it</button><button type="button" class="btn" data-r="csv">Download CSV</button>',
      showLabel: "Show the recorded assessment",
      show: function (a) { if (a.ans) { ans = JSON.parse(JSON.stringify(a.ans)); draw(); } }
    });
    var init = F.saved || F.st;
    if (init.ans) ans = JSON.parse(JSON.stringify(init.ans));
    if (init.fw && FW[init.fw]) fw = init.fw;
    F.r("fw").value = fw;
    function keep() { F.remember({ ans: ans, fw: fw }); }
    function draw() {
      F.r("fnote").textContent = FW[fw].note;
      F.r("list").innerHTML = '<table class="tl-table"><tr><th>Ref</th><th>Requirement</th><th>Status</th><th>Evidence</th><th>Owner</th></tr>' + FW[fw].items.map(function (x) {
        var k = fw + ":" + x[0], a = ans[k] || {};
        return '<tr class="' + (a.s || "") + '"><td>' + K.esc(x[0]) + "</td><td>" + K.esc(x[1]) + '</td><td><select data-k="' + K.esc(k) + '" data-f="s">' + STATUS.map(function (s) {
          return '<option value="' + s[0] + '"' + ((a.s || "") === s[0] ? " selected" : "") + ">" + s[1] + "</option>"; }).join("") + "</select></td>" +
          '<td><input data-k="' + K.esc(k) + '" data-f="e" value="' + K.esc(a.e || "") + '" placeholder="what proves it"></td><td><input data-k="' + K.esc(k) + '" data-f="o" value="' + K.esc(a.o || "") + '"></td></tr>';
      }).join("") + "</table>";
    }
    F.r("list").addEventListener("input", function (e) {
      var k = e.target.getAttribute("data-k"), f = e.target.getAttribute("data-f");
      if (!k) return;
      (ans[k] = ans[k] || {})[f] = e.target.value;
      if (f === "s") e.target.closest("tr").className = e.target.value;
      keep();
    });
    F.r("fw").addEventListener("change", function () { fw = this.value; draw(); keep(); });
    F.r("done").addEventListener("click", function () {
      var s = score(fw, ans), noEv = FW[fw].items.filter(function (x) { var a = ans[fw + ":" + x[0]] || {}; return a.s === "met" && !(a.e || "").trim(); }).length;
      F.msg(s.pct + "% of the requirements in scope are met (partly met counts half): " + s.c.met + " met, " + s.c.partial + " partly, " + s.c.gap + " gaps, " + s.c.open + " not assessed." +
        (noEv ? " " + noEv + " marked met with no evidence: an auditor will ask for it." : ""));
      F.ready({ fw: fw, ans: ans, n: s.c.gap, blank: [] }, "Compliance: " + FW[fw].title.split(" (")[0] + ", " + s.pct + "% met, " + s.c.gap + " gaps");
    });
    F.r("csv").addEventListener("click", function () {
      K.download("compliance-" + fw + ".csv", "framework,ref,requirement,status,evidence,owner\n" + FW[fw].items.map(function (x) {
        var a = ans[fw + ":" + x[0]] || {};
        return [fw, x[0], x[1], a.s || "", a.e || "", a.o || ""].map(function (v) { v = String(v); return /[",\n]/.test(v) ? '"' + v.replace(/"/g, '""') + '"' : v; }).join(",");
      }).join("\n") + "\n", "text/csv");
    });
    draw();
    F.note("");
  }

  global.AayatTools.register({ id: "compliance", title: "Compliance gap check", console: true, group: "Governance and risk", mount: mount, frameworks: FW, score: score });
})(window);
