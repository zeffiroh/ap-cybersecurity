(function (global) {
  "use strict";

  var $ = function (id) { return document.getElementById(id); };
  var term = null, started = false;

  var SETUP = [
    "mkdir -p ~/lab && cd ~/lab",
    "printf 'Nov  3 09:01:12 web sshd[811]: Failed password for root from 203.0.113.7 port 50122 ssh2\\n" +
      "Nov  3 09:01:15 web sshd[811]: Failed password for root from 203.0.113.7 port 50124 ssh2\\n" +
      "Nov  3 09:02:40 web sshd[822]: Accepted password for maya from 198.51.100.20 port 61200 ssh2\\n" +
      "Nov  3 09:03:02 web sshd[830]: Failed password for admin from 203.0.113.7 port 50190 ssh2\\n" +
      "Nov  3 09:05:51 web sshd[841]: Failed password for invalid user test from 192.0.2.44 port 40001 ssh2\\n" +
      "Nov  3 09:06:10 web sshd[845]: Accepted publickey for deploy from 198.51.100.21 port 61311 ssh2\\n' > auth.log",
    "printf 'password\\n123456\\nletmein\\nqwerty\\ncorrect horse battery staple\\n' > wordlist.txt",
    "echo 'top secret plan' > secret.txt && chmod 644 secret.txt",
    "echo -n letmein | sha256sum | cut -d' ' -f1 > leaked_hash.txt"
  ].join(" && ");

  var LABS = [
    { title: "1. Look around", text: "Who are you, where are you, and what's here?", cmds: ["whoami", "pwd", "ls -la ~/lab", "uname -a"] },
    { title: "2. File permissions", text: "secret.txt is readable by everyone. Lock it so only its owner can read and write it, then check.",
      cmds: ["ls -l secret.txt", "chmod 600 secret.txt", "ls -l secret.txt"] },
    { title: "3. Hashing", text: "A hash is a fingerprint. Change one letter and the hash changes completely.",
      cmds: ["echo -n hello | sha256sum", "echo -n Hello | sha256sum", "md5sum secret.txt"] },
    { title: "4. Crack a leaked hash", text: "leaked_hash.txt holds a SHA-256 of a password. Hash every word in the wordlist and find the match.",
      cmds: ["cat leaked_hash.txt", "for w in $(cat wordlist.txt); do echo -n \"$w\" | sha256sum | grep -q $(cat leaked_hash.txt) && echo \"FOUND: $w\"; done"] },
    { title: "5. Hunt through a log", text: "Count failed logins, then find which address tried the most.",
      cmds: ["grep -c 'Failed password' auth.log", "grep 'Failed password' auth.log | awk '{print $(NF-3)}' | sort | uniq -c | sort -rn"] },
    { title: "6. Users and processes", text: "Which accounts exist, and what's running?", cmds: ["cat /etc/passwd", "id", "ps"] },
    { title: "7. Map the network", text: "Which machines are up on 10.0.0.0/24, and what is web01 running? Then scan every port: one of them shouldn't be there.",
      cmds: ["nmap -sn 10.0.0.0/24", "nmap -sV 10.0.0.5", "nmap -p- 10.0.0.5"] },
    { title: "8. Talk to a web server", text: "Ask the web server for pages the way a browser does, and read the headers it sends back.",
      cmds: ["curl -i http://10.0.0.5/robots.txt", "curl -s http://10.0.0.5/", "curl -I http://203.0.113.7:8080/"] },
    { title: "9. Read a packet capture", text: "capture.pcap was recorded on web01's network. Who talked to whom, which names were looked up, and what went to port 4444?",
      cmds: ["tshark -r ~/case/capture.pcap -c 8", "tshark -r ~/case/capture.pcap -q -z conv,ip", "tshark -r ~/case/capture.pcap -Y dns -T fields -e ip.src -e dns.qry.name",
        "tshark -r ~/case/capture.pcap -Y 'tcp.dstport==4444' -c 5"] },
    { title: "10. Look up names", text: "Turn names into addresses and addresses back into names.",
      cmds: ["dig web01.corp.lan", "dig +short update.kworker-cdn.net", "dig -x 198.51.100.66 +short", "nslookup update.kworker-cdn.net", "host web01.corp.lan"] },
    { title: "11. Who owns that address?", text: "Is it up, how far away is it, and who registered it? A brand-new domain is a warning sign.",
      cmds: ["ping -c 3 web01", "traceroute 198.51.100.66", "whois kworker-cdn.net", "whois 203.0.113.7"] },
    { title: "12. Knock on doors", text: "Check single ports by hand, read what each service says about itself, and look at a website's certificate.",
      cmds: ["nc -zv 10.0.0.5 20-25", "nc 10.0.0.5 22", "ssh admin@10.0.0.5", "openssl s_client -connect shop.nimbumart.test:443"] },
    { title: "13. Scan a website", text: "nikto looks for common mistakes; gobuster guesses hidden paths. Both only give you clues to check by hand.",
      cmds: ["nikto -h http://10.0.0.5", "gobuster dir -u http://10.0.0.5", "wget http://10.0.0.5/robots.txt && cat robots.txt"] }
  ];

  function status(t) { if (t !== undefined) $("lx-status").textContent = t; }

  function boot() {
    if (started) return global.AayatVM.boot(status);
    if (!global.AayatVM || !global.Terminal) { status("Couldn't load the Linux emulator. Check your connection and reload."); return Promise.reject(new Error("no vm")); }
    started = true;
    $("lx-start").hidden = true;
    $("lx-screen").innerHTML = "";
    term = new global.Terminal({ convertEol: false, cursorBlink: true, fontSize: 14, rows: 26,
      fontFamily: 'Consolas, "Courier New", monospace', theme: { background: "#000000" } });
    term.open($("lx-screen"));
    term.write("Booting Linux in your browser...\r\n");
    var buf = [], flush = null;
    global.AayatVM.onOutput(function (b) {
      buf.push(b);
      if (!flush) flush = setTimeout(function () { term.write(new Uint8Array(buf)); buf = []; flush = null; }, 16);
    });
    term.onData(function (d) { global.AayatVM.send(d); });
    return global.AayatVM.boot(status).then(function () {
      status("Linux is running. Press \"Create the lab files\" for the practice files and the network tools.");
      $("lx-setup").disabled = false;
      term.focus();
    }, function (e) { status(e.message); throw e; });
  }

  var DONE = "aayat_lx_done", PICK = "aayat_lx_case", ready = "", cases = [];
  function store(k, v) {
    try {
      if (v === undefined) return JSON.parse(localStorage.getItem(k) || "null");
      localStorage.setItem(k, JSON.stringify(v));
    } catch (e) { return null; }
    return v;
  }
  function esc(s) { return String(s == null ? "" : s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }
  function picked() { return (store(PICK) || "web01").replace(/[^a-z0-9-]/g, "") || "web01"; }

  function setup() {
    $("lx-setup").disabled = true;
    var id = picked();
    return boot().then(function () {
      return global.AayatVM.installCase(id, status);
    }).then(function () {
      return global.AayatVM.shell(SETUP, { hide: true });
    }).then(function () {
      ready = id;
      term.write("\r\n\x1b[1mLab files ready:\x1b[0m ~/lab (practice files) and ~/case (" + id + " case evidence).\r\n" +
        "nmap, curl, tshark and dig now reach the recorded case network.\r\n");
      global.AayatVM.send("\n");
      status("Lab files created in ~/lab and ~/case (" + id + "). Network tools ready.");
      $("lx-setup").disabled = false;
      pickNote();
      term.focus();
    }, function (e) { status(e.message); $("lx-setup").disabled = false; });
  }

  function type(text) {
    boot().then(function () {
      if (global.AayatVM.busy()) { status("Wait a moment: the lab files are still loading."); return; }
      if (!ready) status("Tip: press \"Create the lab files\" first, or the files in ~/lab and ~/case won't exist yet.");
      global.AayatVM.send(text + "\n");
      if (term) term.focus();
    });
  }

  function done() { var d = store(DONE); return d && typeof d === "object" ? d : {}; }

  function progress() {
    var d = done(), n = LABS.filter(function (l, i) { return d[i]; }).length, pct = Math.round(100 * n / LABS.length), el = $("lx-prog");
    if (!el) return;
    var next = -1;
    LABS.some(function (l, i) { if (!d[i]) { next = i; return true; } return false; });
    el.innerHTML = '<div class="rb-prog" role="progressbar" aria-valuemin="0" aria-valuemax="100" aria-valuenow="' + pct + '"><i style="width:' + pct + '%"></i></div>' +
      '<div class="rb-ptxt">' + n + " of " + LABS.length + " steps done" + (next >= 0 ? ' &middot; <a href="#lx-step-' + (next + 1) + '">next: step ' + (next + 1) + "</a>" : " &middot; all done. Try an incident runbook next.") + "</div>";
  }

  function pickNote() {
    var n = $("lx-picknote"), id = picked(), c = cases.filter(function (x) { return x.id === id; })[0];
    if (!n) return;
    n.innerHTML = (c ? esc(c.summary || "") + " " : "") + (id !== "web01" ? "Steps 7 to 13 use web01's addresses, so some answers will differ; the evidence for this case is in <code>~/case</code>. " : "") +
      (ready && ready !== id ? "<b>Press \"Create the lab files\" again to load this case.</b> " : "") +
      '<a href="notebook.html?ref=rb-' + Date.now().toString(36) + "&runbook=" + encodeURIComponent(id) + '">Work this case as a guided runbook &rarr;</a>';
  }

  function picker() {
    var box = $("lx-pickbox");
    if (!box || !global.AayatVM) return;
    global.AayatVM.cases().then(function (list) {
      cases = list;
      var id = picked();
      if (!list.some(function (c) { return c.id === id; })) { id = "web01"; store(PICK, id); }
      box.innerHTML = '<label>Case files in <code>~/case</code>: <select id="lx-case">' + list.map(function (c) {
        return '<option value="' + esc(c.id) + '"' + (c.id === id ? " selected" : "") + ">" + esc(c.title) + (c.teacher ? " (made by your teacher)" : "") + "</option>";
      }).join("") + '</select></label><span id="lx-teach"></span><p class="sx-note" id="lx-picknote"></p>';
      var sel = $("lx-case");
      function badge() {
        var c = list.filter(function (x) { return x.id === sel.value; })[0];
        $("lx-teach").innerHTML = c && c.teacher ? '<span class="rb-teacher">Made by your teacher</span>' : "";
      }
      sel.addEventListener("change", function () { store(PICK, sel.value); badge(); pickNote(); });
      badge(); pickNote();
    }, function () { box.innerHTML = '<p class="sx-note">Case files: web01 (the hacked web shop).</p>'; });
  }

  function labs() {
    var d = done(), K = global.LabKit;
    $("lx-labs").innerHTML = '<div class="lx-steps-head"><h2>Step-by-step</h2><button class="btn" id="lx-clear" type="button">Reset ticks</button></div>' +
      '<div id="lx-pickbox" class="lx-pick"></div><div id="lx-prog"></div>' +
      '<p class="sx-note">Press <b>Start Linux</b>, then <b>Create the lab files</b>. <b>Type it</b> runs a command in the terminal; <b>Explain</b> shows what each part does.</p>' +
      LABS.map(function (l, i) {
        var t = l.title.replace(/^\d+\.\s*/, "");
        return '<section class="lx-lab lv-step' + (d[i] ? " done" : "") + '" id="lx-step-' + (i + 1) + '"><header class="lv-sh"><span class="lv-num" aria-hidden="true">' + (d[i] ? "&#10003;" : i + 1) + "</span>" +
          "<h2><small>Step " + (i + 1) + " of " + LABS.length + "</small>" + esc(t) + '</h2><button type="button" class="lv-done" data-done="' + i + '" aria-pressed="' + !!d[i] + '">' +
          (d[i] ? "&#10003; Done" : "Mark done") + '</button></header><div class="lv-body"><p>' + esc(l.text) + "</p>" + l.cmds.map(function (c, j) {
            return '<div class="lx-cmd"><code>' + esc(c) + '</code><button class="btn dark" data-l="' + i + '" data-c="' + j + '">Type it</button>' +
              '<button class="btn" type="button" data-copy="' + esc(c) + '">Copy</button>' +
              (K ? '<button class="btn" type="button" data-explain>Explain</button><div class="rb-explain" hidden>' + K.explain(c) + "</div>" : "") + "</div>";
          }).join("") + "</div></section>";
      }).join("");
    $("lx-labs").querySelectorAll("[data-l]").forEach(function (b) {
      b.addEventListener("click", function () { type(LABS[+b.getAttribute("data-l")].cmds[+b.getAttribute("data-c")]); });
    });
    $("lx-labs").querySelectorAll("[data-done]").forEach(function (b) {
      b.addEventListener("click", function () {
        var i = +b.getAttribute("data-done"), all = done(), on = !all[i], sec = b.closest(".lv-step");
        if (on) all[i] = true; else delete all[i];
        store(DONE, all);
        sec.classList.toggle("done", on);
        sec.querySelector(".lv-num").innerHTML = on ? "&#10003;" : i + 1;
        b.innerHTML = on ? "&#10003; Done" : "Mark done";
        b.setAttribute("aria-pressed", String(on));
        progress();
        var next = on && $("lx-step-" + (i + 2));
        if (next && !all[i + 1]) next.scrollIntoView({ behavior: "smooth", block: "nearest" });
      });
    });
    $("lx-clear").addEventListener("click", function () { store(DONE, {}); labs(); });
    if (K) { K.bindCopy($("lx-labs")); K.bindExplain($("lx-labs")); }
    progress();
    picker();
  }

  function start() {
    if (!$("lx-app")) return;
    labs();
    $("lx-start").addEventListener("click", function () { boot().catch(function () {}); });
    $("lx-setup").addEventListener("click", setup);
    $("lx-reset").addEventListener("click", function () {
      if (!started) return;
      global.AayatVM.restart();
      ready = "";
      status("Restarting…");
      global.AayatVM.boot().then(function () { status("Linux restarted. Press \"Create the lab files\" again."); });
    });
  }
  if (document.readyState === "complete") start();
  else global.addEventListener("load", start);
})(window);
