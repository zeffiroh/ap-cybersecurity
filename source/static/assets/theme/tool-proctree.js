(function (global) {
  "use strict";
  var K = global.AayatTools.kit;
  var CSS = ".tr-box .tr-tree{font:12.5px/1.5 ui-monospace,Consolas,monospace;background:#fff;border:1px solid #bbb;padding:6px;max-height:420px;overflow:auto;margin-top:8px}" +
    ".tr-box ul{list-style:none;margin:0;padding-left:18px;border-left:1px dotted #aaa}.tr-box .tr-root>ul{border-left:0;padding-left:0}.tr-box li{margin:1px 0}" +
    ".tr-box .tr-n{cursor:pointer}.tr-box .tr-n:hover{background:#f0f0f0}.tr-box .tr-n.on{background:#1f4e8c;color:#fff}.tr-box .tr-flag{color:#b42318;font-weight:600}" +
    ".tr-box .tr-detail{margin-top:8px;border:1px solid #bbb;background:#fafafa;padding:6px 8px;font-size:12.5px}.tr-box .tr-detail code{word-break:break-all}";
  var RULES = [
    [/\\(users\\public|appdata\\|temp\\|downloads\\|programdata\\)|^\/tmp\/|^\/dev\/shm\//i, "runs from a folder any user can write to", "image"],
    [/(winword|excel|powerpnt|outlook|acrord32)\.exe$/i, "an Office or PDF program started a shell", "parentShell"],
    [/\s-(e|en|enc|encodedcommand)\s/i, "PowerShell with an encoded command", "cmd"],
    [/-w(indowstyle)?\s+hidden|-nop\b/i, "PowerShell hiding its window or skipping the profile", "cmd"],
    [/schtasks(\.exe)?\s+\/create|crontab\s|at\s+\d/i, "creates a scheduled task", "cmd"],
    [/(vssadmin|wbadmin).*(delete|shadow)|bcdedit.*recoveryenabled/i, "deletes backups or recovery options", "cmd"],
    [/(certutil.*-urlcache|bitsadmin.*\/transfer|curl|wget|invoke-webrequest|downloadstring|net\.webclient)/i, "downloads a file", "cmd"],
    [/\bnet(1)?\s+(user|localgroup)\b.*\/add/i, "adds a user or group member", "cmd"],
    [/svchost|lsass|csrss|winlogon|explorer/i, "has a system process name in an unusual place", "masq"]
  ];
  var SHELLS = /\\(cmd|powershell|pwsh|wscript|cscript|mshta|rundll32|regsvr32)\.exe$/i;
  var REAL = /^c:\\windows\\(system32|syswow64)\\|^c:\\windows\\explorer\.exe$/i;

  function hexOrDec(v) { v = String(v == null ? "" : v).trim(); return /^0x/i.test(v) ? parseInt(v, 16) : /^\d+$/.test(v) ? +v : null; }
  function procs(files) {
    var out = [];
    Object.keys(files).sort().forEach(function (n) {
      var b = K.base(n);
      if (/\.csv$/i.test(b)) {
        var rows = K.csv(files[n]);
        if (!rows.length || !("pid" in rows[0]) || !("ppid" in rows[0])) return;
        rows.forEach(function (r) { out.push({ src: n, time: r.time || "", host: r.host || "", pid: hexOrDec(r.pid), ppid: hexOrDec(r.ppid), user: r.user || "", image: r.image || "", cmd: r.command_line || r.cmd || r.commandline || "" }); });
      } else if (/\.jsonl$/i.test(b)) {
        String(files[n]).split("\n").forEach(function (l) {
          var o = l.trim() && K.json(l);
          if (!o || !o.Data) return;
          var d = o.Data, host = String(o.Computer || "").split(".")[0];
          if (o.EventID === 4688 && !/sysmon/i.test(String(o.Provider))) out.push({ src: n, time: o.TimeCreated, host: host, pid: hexOrDec(d.NewProcessId), ppid: hexOrDec(d.ProcessId), user: (d.SubjectDomainName ? d.SubjectDomainName + "\\" : "") + (d.SubjectUserName || ""), image: d.NewProcessName || "", cmd: d.CommandLine || "", parentImage: d.ParentProcessName || "" });
          if (o.EventID === 1 && /sysmon/i.test(String(o.Provider))) out.push({ src: n, time: o.TimeCreated, host: host, pid: hexOrDec(d.ProcessId), ppid: hexOrDec(d.ParentProcessId), user: d.User || "", image: d.Image || "", cmd: d.CommandLine || "", parentImage: d.ParentImage || "" });
        });
      }
    });
    return out.filter(function (p) { return p.pid != null; });
  }
  function flags(p, parent) {
    var f = [], img = String(p.image), par = parent ? parent.image : p.parentImage || "";
    RULES.forEach(function (r) {
      if (r[2] === "image" && r[0].test(img)) f.push(r[1]);
      else if (r[2] === "cmd" && r[0].test(" " + p.cmd + " ")) f.push(r[1]);
      else if (r[2] === "parentShell" && r[0].test(par) && SHELLS.test(img)) f.push(r[1]);
      else if (r[2] === "masq" && r[0].test(img.split("\\").pop()) && /\.exe$/i.test(img) && !REAL.test(img) && /^[a-z]:\\/i.test(img)) f.push(r[1]);
    });
    return f.filter(function (x, i, a) { return a.indexOf(x) === i; });
  }
  function trees(list) {
    var pick = {}, order = [];
    list.forEach(function (p) {
      var k = p.host + "|" + p.pid;
      if (!pick[k] || (pick[k].src !== p.src && /sysmon/i.test(p.src))) { if (!pick[k]) order.push(k); pick[k] = p; }
    });
    var nodes = order.map(function (k) { var p = pick[k]; return { p: p, key: k, kids: [] }; }), by = {};
    nodes.forEach(function (n) { by[n.key] = n; });
    var roots = [];
    nodes.forEach(function (n) {
      var par = by[n.p.host + "|" + n.p.ppid];
      n.flags = flags(n.p, par && par.p);
      if (par && par !== n) par.kids.push(n); else roots.push(n);
    });
    function sort(a) { a.sort(function (x, y) { return String(x.p.time) < String(y.p.time) ? -1 : 1; }); a.forEach(function (n) { sort(n.kids); }); }
    sort(roots);
    return { roots: roots, all: nodes };
  }

  function mount(el, ctx) {
    K.css("tool-proctree-css", CSS);
    var T = { roots: [], all: [] }, mark = {}, cur = null;
    var F = K.frame(el, ctx, {
      title: "Process tree", cls: "tr-box",
      body: '<div class="tl-row"><label>Host <select data-r="host"></select></label><label style="flex-direction:row;align-items:center;gap:4px"><input type="checkbox" data-r="sus"> Only branches with warnings</label></div>',
      actions: '<button type="button" class="btn dark" data-r="done">Save the processes I marked</button>',
      showLabel: "Show the recorded marks",
      show: function (a) { (a.marks || []).forEach(function (k) { mark[k] = 1; }); draw(); },
      after: '<div class="tr-tree tr-root" data-r="tree"></div><div class="tr-detail" data-r="detail" hidden></div>'
    });
    var init = F.saved || F.st;
    (Array.isArray(init.marks) ? init.marks : []).forEach(function (k) { mark[k] = 1; });
    function keep() { F.remember({ marks: Object.keys(mark) }); }
    function bad(n) { return n.flags.length || n.kids.some(bad); }
    function li(n) {
      var name = String(n.p.image).split(/[\\/]/).pop() || "?";
      return '<li><span class="tr-n' + (cur === n.key ? " on" : "") + '" data-k="' + K.esc(n.key) + '">' + (mark[n.key] ? "&#9873; " : "") + K.esc(name) + " <small>(" + n.p.pid + ")</small>" +
        (n.flags.length ? ' <span class="tr-flag">&#9888; ' + n.flags.length + "</span>" : "") + "</span>" +
        (n.kids.length ? "<ul>" + n.kids.filter(function (k) { return !F.r("sus").checked || bad(k); }).map(li).join("") + "</ul>" : "") + "</li>";
    }
    function draw() {
      var host = F.r("host").value, rs = T.roots.filter(function (n) { return !host || n.p.host === host; }).filter(function (n) { return !F.r("sus").checked || bad(n); });
      F.r("tree").innerHTML = rs.length ? "<ul>" + rs.map(li).join("") + "</ul>" : "No processes.";
      var w = T.all.filter(function (n) { return n.flags.length && (!host || n.p.host === host); }).length;
      F.msg(T.all.length + " processes, " + w + " with warnings. Click one to read it, then mark it if it's part of the attack.");
    }
    function detail(n) {
      var d = F.r("detail");
      d.hidden = false;
      d.innerHTML = "<b></b><div>Process " + n.p.pid + ", parent " + n.p.ppid + ", " + K.esc(n.p.user) + ", " + K.esc(n.p.time) + "</div><div>Command line: <code></code></div>" +
        (n.flags.length ? '<ul class="tr-flag">' + n.flags.map(function (f) { return "<li>" + K.esc(f) + "</li>"; }).join("") + "</ul>" : "<p>No warnings. That doesn't mean it's safe.</p>") +
        '<label style="display:flex;gap:6px;align-items:center"><input type="checkbox" data-r="mk"' + (mark[n.key] ? " checked" : "") + "> Part of the attack</label><small>From " + K.esc(n.p.src) + "</small>";
      d.querySelector("b").textContent = n.p.image;
      d.querySelector("code").textContent = n.p.cmd;
      F.r("mk").addEventListener("change", function () { if (this.checked) mark[n.key] = 1; else delete mark[n.key]; keep(); draw(); });
    }
    F.r("tree").addEventListener("click", function (e) {
      var s = e.target.closest("[data-k]");
      if (!s) return;
      cur = s.getAttribute("data-k");
      draw();
      detail(T.all.filter(function (n) { return n.key === cur; })[0]);
    });
    F.r("host").addEventListener("change", draw);
    F.r("sus").addEventListener("change", draw);
    F.r("done").addEventListener("click", function () {
      var ks = Object.keys(mark).filter(function (k) { return T.all.some(function (n) { return n.key === k; }); });
      if (!ks.length) { F.msg("Mark at least one process first.", true); return; }
      var msg = ks.length + " processes marked.";
      if (F.answer && Array.isArray(F.answer.marks)) {
        var hit = ks.filter(function (k) { return F.answer.marks.indexOf(k) >= 0; }).length;
        msg += " " + hit + " of the " + F.answer.marks.length + " recorded ones, plus " + (ks.length - hit) + " others.";
      }
      F.msg(msg);
      var files = T.all.filter(function (n) { return mark[n.key]; }).map(function (n) { return n.p.src; }).filter(function (s, i, a) { return a.indexOf(s) === i; });
      F.ready({ marks: ks, n: ks.length, files: files, blank: ["marks"] }, "Process tree: " + ks.length + " processes marked as part of the attack");
    });

    F.note("Loading…");
    F.files().then(function (fs) {
      T = trees(procs(K.textFiles(fs)));
      var hosts = T.all.map(function (n) { return n.p.host; }).filter(function (h, i, a) { return h && a.indexOf(h) === i; }).sort();
      F.r("host").innerHTML = '<option value="">All</option>' + hosts.map(function (h) { return '<option value="' + K.esc(h) + '">' + K.esc(h) + "</option>"; }).join("");
      F.note(T.all.length + " processes");
      if (!T.all.length) { F.msg("No process data here. Process lists are CSV files with pid and ppid columns, or event logs with process events."); return; }
      draw();
    }).catch(function () { F.note(""); F.msg("The files didn't load.", true); });
  }

  global.AayatTools.register({ id: "proctree", title: "Process tree", console: true, group: "Incident responder", mount: mount, procs: procs, trees: trees, flags: flags });
})(window);
