(function (global) {
  "use strict";

  var LOCAL = "aayat_ctf_local";

  function esc(s) {
    return String(s == null ? "" : s).replace(/[&<>"']/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c];
    });
  }

  function local() {
    try { return JSON.parse(localStorage.getItem(LOCAL) || "{}") || {}; } catch (e) { return {}; }
  }

  function remember(id, flag) {
    var l = local();
    l[id] = flag;
    try { localStorage.setItem(LOCAL, JSON.stringify(l)); } catch (e) {}
  }

  function reveal(id) {
    var d = global.AAYAT_LABFLAGS;
    if (!d || !d.flags || !d.flags[id]) return "";
    var b = atob(d.flags[id]), out = "";
    for (var i = 0; i < b.length; i++) out += String.fromCharCode(b.charCodeAt(i) ^ d.key.charCodeAt(i % d.key.length));
    return out;
  }

  function rpc(fn, args) {
    var P = global.AayatProgress;
    return (P ? P.neon() : Promise.resolve(null)).then(function (db) {
      if (!db) throw new Error("The course database is not connected yet.");
      return db.rpc(fn, args || {}, { attempts: 1 });
    });
  }

  function sha256(text) {
    var bytes = new TextEncoder().encode(String(text).trim().toLowerCase());
    return crypto.subtle.digest("SHA-256", bytes).then(function (buf) {
      return Array.prototype.map.call(new Uint8Array(buf), function (b) { return ("0" + b.toString(16)).slice(-2); }).join("");
    });
  }

  function submit(id, flag) {
    return rpc("api_ctf_submit", { p_id: id, p_flag: flag });
  }

  function box() {
    var b = document.getElementById("lk-toast");
    if (b) return b;
    b = document.createElement("div");
    b.id = "lk-toast";
    b.className = "lk-toast";
    b.setAttribute("role", "status");
    document.body.appendChild(b);
    return b;
  }

  var shown = {};

  function award(id, title) {
    var flag = reveal(id);
    if (!flag || shown[id]) return flag;
    shown[id] = true;
    var first = !local()[id];
    remember(id, flag);
    var b = box();
    b.innerHTML = '<button class="lk-x" aria-label="Close">&times;</button><div class="lk-k">' + (first ? "Flag captured" : "Flag again") +
      "</div><b>" + esc(title || id) + '</b><code class="lk-flag">' + esc(flag) + '</code><div class="lk-s">Saving to the CTF board…</div>';
    b.hidden = false;
    b.querySelector(".lk-x").addEventListener("click", function () { b.hidden = true; });
    var s = b.querySelector(".lk-s");
    submit(id, flag).then(function (r) {
      if (r && r.ok && r.correct) s.textContent = r.already ? "Already on your CTF score." : "+" + r.points + " points on the CTF board.";
      else s.textContent = (r && r.error) || "Saved in this browser. Sign in to score it.";
    }, function () { s.textContent = "Saved in this browser. Open the CTF board after signing in to score it."; });
    global.dispatchEvent(new CustomEvent("labkit-award", { detail: { id: id } }));
    return flag;
  }

  function missions(el, list) {
    if (!el) return;
    var done = local();
    el.innerHTML = list.map(function (m) {
      var ok = !!done[m.id];
      return '<div class="lk-m' + (ok ? " ok" : "") + '"><div class="lk-mt"><span class="lk-dot">' + (ok ? "&#10003;" : "") + "</span>" +
        esc(m.title) + ' <small>' + m.points + " pts</small></div><p>" + esc(m.text) + "</p>" +
        (m.hint ? "<details><summary>Hint</summary><p>" + esc(m.hint) + "</p></details>" : "") +
        (ok ? '<code class="lk-flag">' + esc(done[m.id]) + "</code>" : "") + "</div>";
    }).join("");
  }

  function norm(s) { return String(s == null ? "" : s).toLowerCase().trim().replace(/\s+/g, " "); }

  function hex(buf) {
    return Array.prototype.map.call(new Uint8Array(buf), function (b) { return ("0" + b.toString(16)).slice(-2); }).join("");
  }

  function answerHash(text) {
    return crypto.subtle.digest("SHA-256", new TextEncoder().encode(norm(text))).then(hex);
  }

  function key(s) {
    var h = 5381, t = String(s || "");
    for (var i = 0; i < t.length; i++) h = ((h << 5) + h + t.charCodeAt(i)) >>> 0;
    return h.toString(36);
  }

  function inline(t) {
    return esc(t).replace(/`([^`]+)`/g, "<code>$1</code>").replace(/\*\*([^*]+)\*\*/g, "<b>$1</b>")
      .replace(/(^|[^*\w])\*([^*\s][^*]*)\*/g, "$1<i>$2</i>")
      .replace(/\[([^\]]+)\]\((https?:[^)\s]+)\)/g, '<a href="$2" target="_blank" rel="noopener nofollow">$1</a>');
  }

  function guideLine(line) {
    var h = /^\s*>\s*Hint:\s*(.*)$/i.exec(line);
    if (h) return { hint: h[1].trim() };
    var a = /^\s*\?>\s*(.+?)\s*::\s*sha256:([0-9a-fA-F]{64})\s*$/.exec(line);
    if (a) return { ask: a[1], hash: a[2].toLowerCase() };
    return null;
  }

  function hintHtml(text, st) {
    var k = "h" + key(text), open = !!(st && st.hints && st.hints[k]);
    return '<div class="rb-hint' + (open ? " open" : "") + '" data-hint="' + k + '"><button type="button" class="rb-hbtn" aria-expanded="' + open + '">' +
      (open ? "Hint" : "Show hint") + '</button><div class="rb-htext"' + (open ? "" : " hidden") + ">" + inline(text) + "</div></div>";
  }

  function askHtml(q, hash, st) {
    var k = "q" + key(q + hash), a = st && st.answers && st.answers[k], ok = !!(a && a.ok);
    return '<form class="rb-ask' + (ok ? " ok" : "") + '" data-ask="' + k + '" data-hash="' + hash + '" autocomplete="off"><div class="rb-aq">' +
      '<span class="rb-qmark">' + (ok ? "&#10003;" : "?") + "</span>" + inline(q) + '</div><div class="rb-arow"><input class="rb-ain" aria-label="Your answer" spellcheck="false" placeholder="Your answer" value="' +
      esc(a ? a.a : "") + '"><button class="btn dark" type="submit">Check</button></div><div class="rb-amsg" role="status">' +
      (ok ? "Correct." : a && a.a ? "Not quite. Try again." : "") + "</div></form>";
  }

  function bindGuide(root, st, changed) {
    if (!root) return;
    st.hints = st.hints || {}; st.answers = st.answers || {};
    root.querySelectorAll("[data-hint]").forEach(function (h) {
      var b = h.querySelector(".rb-hbtn");
      b.addEventListener("click", function () {
        var t = h.querySelector(".rb-htext"), open = t.hidden;
        t.hidden = !open;
        h.classList.toggle("open", open);
        b.textContent = open ? "Hide hint" : "Show hint";
        b.setAttribute("aria-expanded", String(open));
        if (open && !st.hints[h.getAttribute("data-hint")]) { st.hints[h.getAttribute("data-hint")] = true; if (changed) changed("hint"); }
      });
    });
    root.querySelectorAll("[data-ask]").forEach(function (f) {
      f.addEventListener("submit", function (e) {
        e.preventDefault();
        var k = f.getAttribute("data-ask"), v = f.querySelector(".rb-ain").value, m = f.querySelector(".rb-amsg");
        if (!norm(v)) { m.textContent = "Type an answer first."; return; }
        answerHash(v).then(function (h) {
          var ok = h === f.getAttribute("data-hash");
          st.answers[k] = { a: v, ok: ok, at: new Date().toISOString() };
          f.classList.toggle("ok", ok);
          f.classList.remove("no");
          if (!ok) { void f.offsetWidth; f.classList.add("no"); }
          f.querySelector(".rb-qmark").innerHTML = ok ? "&#10003;" : "?";
          m.textContent = ok ? "Correct." : "Not quite. Check the evidence again, or open the hint.";
          if (changed) changed("answer", ok);
        }, function () { m.textContent = "This browser can't check answers here (it needs a secure https page)."; });
      });
    });
  }

  function copyText(t) {
    if (navigator.clipboard && global.isSecureContext !== false) return navigator.clipboard.writeText(t);
    return new Promise(function (ok, bad) {
      var a = document.createElement("textarea");
      a.value = t; a.style.position = "fixed"; a.style.opacity = "0";
      document.body.appendChild(a); a.select();
      try { document.execCommand("copy") ? ok() : bad(); } catch (e) { bad(e); }
      document.body.removeChild(a);
    });
  }

  function bindCopy(root) {
    root.querySelectorAll("[data-copy]").forEach(function (b) {
      b.addEventListener("click", function () {
        var src = b.getAttribute("data-copy") || (b.parentNode.querySelector("pre,code") || {}).textContent || "";
        copyText(src).then(function () { b.textContent = "Copied"; setTimeout(function () { b.textContent = "Copy"; }, 1500); },
          function () { b.textContent = "Select and copy"; });
      });
    });
  }

  function md(src, st, o) {
    o = o || {};
    var out = [], list = false, fence = null, table = null, para = [], quote = [];
    function flushPara() { if (para.length) { out.push("<p>" + para.join(" ") + "</p>"); para = []; } }
    function flushList() { if (list) { out.push("</ul>"); list = false; } }
    function flushQuote() { if (quote.length) { out.push("<blockquote>" + quote.join("<br>") + "</blockquote>"); quote = []; } }
    function flushTable() {
      if (!table) return;
      var rows = table.filter(function (r) { return !/^\s*\|?\s*:?-{2,}/.test(r); }).map(function (r) {
        return r.trim().replace(/^\||\|$/g, "").split("|").map(function (c) { return inline(c.trim()); });
      });
      out.push('<div class="rb-tablewrap"><table>' + rows.map(function (r, i) {
        var tag = i ? "td" : "th";
        return "<tr>" + r.map(function (c) { return "<" + tag + ">" + c + "</" + tag + ">"; }).join("") + "</tr>";
      }).join("") + "</table></div>");
      table = null;
    }
    function flushAll() { flushPara(); flushList(); flushTable(); flushQuote(); }
    String(src || "").replace(/\r/g, "").split("\n").forEach(function (line) {
      if (fence) {
        if (/^\s*```/.test(line)) {
          var body = fence.join("\n");
          out.push('<div class="rb-code"><pre>' + esc(body) + '</pre><button type="button" class="btn rb-copy" data-copy>Copy</button>' +
            (o.explain && /^(sh|bash|shell|console)?$/.test(fence.lang) ? '<button type="button" class="btn rb-exbtn" data-explain>Explain</button><div class="rb-explain" hidden>' + explain(body) + "</div>" : "") + "</div>");
          fence = null;
        } else fence.push(line);
        return;
      }
      var f = /^\s*```\s*([A-Za-z]*)/.exec(line);
      if (f) { flushAll(); fence = []; fence.lang = f[1].toLowerCase(); return; }
      var g = guideLine(line);
      if (g) { flushAll(); out.push(g.hint !== undefined ? hintHtml(g.hint, st) : askHtml(g.ask, g.hash, st)); return; }
      if (/^\s*\|/.test(line)) { flushPara(); flushList(); flushQuote(); (table = table || []).push(line); return; }
      flushTable();
      var bq = /^\s*>\s?(.*)$/.exec(line);
      if (bq) { flushPara(); flushList(); quote.push(inline(bq[1])); return; }
      flushQuote();
      var h = /^(#{1,4})\s+(.*)$/.exec(line), li = /^\s*(?:[-*]|\d+\.)\s+(.*)$/.exec(line);
      if (li) {
        flushPara();
        if (!list) { out.push("<ul>"); list = true; }
        var box = /^\[( |x|X)\]\s*(.*)$/.exec(li[1]);
        out.push(box ? '<li class="rb-li-check"><span class="rb-box">' + (box[1] === " " ? "" : "&#10003;") + "</span>" + inline(box[2]) + "</li>" : "<li>" + inline(li[1]) + "</li>");
        return;
      }
      flushList();
      if (h) { flushPara(); var n = Math.min(6, h[1].length + (o.shift || 1)); out.push("<h" + n + ">" + inline(h[2]) + "</h" + n + ">"); }
      else if (line.trim()) para.push(inline(line));
      else flushPara();
    });
    if (fence) out.push('<div class="rb-code"><pre>' + esc(fence.join("\n")) + '</pre><button type="button" class="btn rb-copy" data-copy>Copy</button></div>');
    flushAll();
    return out.join("");
  }

  var ARG = "a value the command works on";
  var CMD = {
    grep: ["finds the lines that match a pattern", { "-i": "ignore upper and lower case", "-v": "show the lines that do NOT match", "-c": "count the matching lines instead of printing them",
      "-E": "extended patterns, so a|b means a or b", "-q": "quiet: print nothing, just succeed or fail", "-o": "print only the part that matched", "-n": "show line numbers",
      "-r": "search every file in the folders", "-h": "don't print file names", "-l": "list only the names of files that match", "-A": "also show N lines after each match",
      "-B": "also show N lines before each match", "-F": "treat the pattern as plain text, not a pattern", "-w": "match whole words only" }],
    egrep: ["grep with extended patterns (same as grep -E)", {}],
    awk: ["splits each line into fields ($1, $2 … and $NF for the last) and prints or counts them", { "-F": "use this character between fields instead of spaces", "-v": "set a variable" }],
    sort: ["puts lines in order", { "-n": "sort as numbers", "-r": "reverse: biggest first", "-u": "drop repeated lines", "-k": "sort by this column", "-t": "columns are separated by this character", "-h": "sort sizes like 2K and 1M" }],
    uniq: ["merges repeated neighbouring lines (sort first so repeats sit together)", { "-c": "count how many times each line appears", "-d": "show only lines that repeat", "-u": "show only lines that appear once" }],
    cut: ["keeps only some columns of each line", { "-d": "the character between columns", "-f": "which columns (fields) to keep", "-c": "which characters to keep" }],
    head: ["shows the first lines (10 unless you say)", { "-n": "how many lines", "-c": "how many bytes" }],
    tail: ["shows the last lines (10 unless you say)", { "-n": "how many lines (+N means from line N on)", "-f": "keep watching for new lines" }],
    wc: ["counts lines, words and bytes", { "-l": "count lines only", "-w": "count words only", "-c": "count bytes only" }],
    sha256sum: ["prints the SHA-256 fingerprint (hash) of each file; one changed byte changes the whole hash", { "-c": "check files against a saved list of hashes" }],
    md5sum: ["prints the MD5 hash of each file (old and weak, but still used to match known files)", {}],
    sha1sum: ["prints the SHA-1 hash of each file", {}],
    base64: ["encodes data as base64 text, or decodes it", { "-d": "decode: turn base64 back into the original", "--decode": "decode: turn base64 back into the original", "-w": "wrap lines at this width (0 = never)" }],
    nmap: ["scans machines to see which are up and which ports (services) are open", { "-sn": "ping scan only: which machines are up, no port scan", "-sV": "ask each open port which program and version it runs",
      "-p-": "scan all 65,535 ports", "-p": "only these ports (e.g. -p 22,80 or -p 1-1000)", "-Pn": "don't ping first; treat every host as up", "-A": "aggressive: versions, OS guess and scripts",
      "-O": "guess the operating system", "-sS": "SYN scan (half-open)", "-sT": "full TCP connect scan", "-sU": "scan UDP ports", "-T4": "go faster", "-v": "say more while scanning", "--top-ports": "scan the N most common ports", "-oN": "save the results to a file" }],
    curl: ["sends a web request and prints what the server sends back", { "-I": "ask for the headers only (a HEAD request)", "-i": "include the response headers before the page", "-s": "silent: no progress bar",
      "-v": "verbose: show the whole conversation", "-L": "follow redirects", "-o": "save the page to this file", "-O": "save the page under its own name", "-X": "use this method (GET, POST, PUT …)",
      "-d": "send this data in the body (makes it a POST)", "-H": "add this header", "-A": "pretend to be this browser (User-Agent)", "-k": "don't check the certificate", "-u": "send a username and password", "-b": "send this cookie" }],
    wget: ["downloads a file from a web address", { "-q": "quiet", "-O": "save under this name (- means print it)", "-S": "show the server's headers" }],
    tshark: ["reads network traffic (a packet capture) from the command line, like Wireshark without windows", { "-r": "read packets from this capture file", "-Y": "display filter: only show packets that match (e.g. dns, http.request, ip.src==10.0.0.5)",
      "-T": "output format; -T fields prints only the fields you pick with -e", "-e": "a field to print, e.g. ip.src or dns.qry.name", "-q": "quiet: don't list packets (use with -z)",
      "-z": "statistics, e.g. conv,ip lists who talked to whom", "-c": "stop after this many packets", "-V": "show every detail of each packet", "-x": "show the raw bytes", "-n": "don't turn addresses into names" }],
    dig: ["asks DNS: which address belongs to a name (and more)", { "+short": "just the answer, nothing else", "-x": "reverse lookup: which name belongs to this address", "MX": "ask for mail servers", "TXT": "ask for text records (SPF, DMARC …)", "NS": "ask for the name servers", "A": "ask for the IPv4 address", "ANY": "ask for every record" }],
    nslookup: ["asks DNS for a name's address (older tool than dig)", {}],
    host: ["a short DNS lookup: name to address or address to name", {}],
    whois: ["shows who registered a domain or owns an address block, and when", {}],
    nc: ["netcat: opens a raw connection to a port, to see what answers", { "-z": "just check whether the port is open, send nothing", "-v": "say what happened", "-l": "listen instead of connecting", "-w": "give up after N seconds", "-u": "use UDP" }],
    openssl: ["the Swiss army knife of encryption and certificates", { "s_client": "connect to a TLS (https) server and show its certificate", "-connect": "the host:port to connect to", "-servername": "the site name to ask for (SNI)",
      "x509": "read a certificate", "-noout": "don't print the encoded certificate", "-text": "print it in readable form", "dgst": "hash a file", "enc": "encrypt or decrypt", "-showcerts": "show the whole certificate chain" }],
    tar: ["packs many files into one archive (or unpacks one)", { "-c": "create an archive", "c": "create an archive", "-x": "extract", "x": "extract", "-t": "list what's inside", "t": "list what's inside", "-f": "the archive file name", "f": "the archive file name",
      "-z": "gzip it too", "z": "gzip it too", "-v": "list files as it goes", "v": "list files as it goes", "-C": "change to this folder first", "cf": "create an archive file", "xf": "extract an archive file", "tf": "list an archive file", "czf": "create a gzipped archive file", "xzf": "extract a gzipped archive file" }],
    gzip: ["compresses a file (adds .gz)", { "-f": "overwrite without asking", "-d": "decompress", "-k": "keep the original" }],
    find: ["searches folders for files by name, type, size or time", { "-name": "the file name matches this pattern", "-iname": "same, ignoring case", "-type": "f for files, d for folders", "-newer": "changed more recently than this file",
      "-mtime": "changed N days ago", "-size": "bigger or smaller than this", "-exec": "run a command on each file found ({} is the file)", "!": "NOT: the next test must be false", "-perm": "has these permissions", "-user": "owned by this user" }],
    ls: ["lists the files in a folder", { "-l": "long list: permissions, owner, size and date", "-a": "include hidden files (names starting with .)", "-la": "long list including hidden files", "-h": "sizes like 4K and 2M",
      "-t": "newest first", "-R": "go into every sub-folder", "-S": "biggest first", "-r": "reverse the order" }],
    cat: ["prints a whole file", { "-n": "number the lines", "-A": "show hidden characters" }],
    less: ["shows a long file one screen at a time (q to quit, / to search)", {}],
    more: ["shows a file one screen at a time", {}],
    strings: ["pulls readable text out of a binary file (good for spotting addresses and commands in malware)", { "-n": "only strings at least N characters long" }],
    file: ["says what kind of file something really is, whatever its name says", {}],
    xxd: ["shows a file's raw bytes in hex next to the text", { "-l": "only the first N bytes", "-r": "turn hex back into bytes", "-p": "plain hex, no layout" }],
    hexdump: ["shows a file's raw bytes in hex", { "-C": "hex and text side by side" }],
    echo: ["prints text", { "-n": "no newline at the end (matters when you hash it)", "-e": "understand escapes like \\n" }],
    printf: ["prints text with formatting", {}],
    cd: ["changes folder (~ is your home folder, .. is the folder above)", {}],
    pwd: ["prints which folder you are in", {}],
    date: ["prints the date and time", { "-u": "in UTC, the time zone logs usually use" }],
    mkdir: ["makes a folder", { "-p": "make parent folders too, and don't complain if it exists" }],
    cp: ["copies files", { "-r": "copy folders and everything in them", "-p": "keep dates and permissions" }],
    mv: ["moves or renames files", {}],
    rm: ["deletes files (there is no bin to restore them from)", { "-f": "don't ask, don't complain", "-r": "delete folders and everything in them" }],
    sed: ["edits text as it streams past: find and replace, delete lines", { "-i": "change the file itself", "-n": "print only what you ask for", "-E": "extended patterns", "s/old/new/": "replace old with new", "/x/d": "delete lines containing x" }],
    tr: ["swaps or deletes characters", { "-d": "delete these characters", "-s": "squeeze repeats into one" }],
    chmod: ["changes who may read, write or run a file", { "+x": "allow running it", "600": "only the owner can read and write", "644": "owner writes, everyone reads", "755": "owner writes, everyone reads and runs" }],
    chown: ["changes who owns a file", {}],
    ping: ["checks whether a machine answers, and how fast", { "-c": "send only this many pings" }],
    traceroute: ["lists every router between you and a machine", {}],
    ssh: ["logs in to another machine securely", { "-p": "use this port", "-i": "use this key file" }],
    nikto: ["scans a web server for common mistakes and old software", { "-h": "the site to scan" }],
    gobuster: ["guesses hidden pages and folders on a website from a word list", { "dir": "guess folders and files", "-u": "the site address", "-w": "the word list to try" }],
    ps: ["lists running programs (processes)", { "aux": "every process from every user, with details", "-ef": "every process, full details" }],
    id: ["shows your user and groups", {}], whoami: ["prints your user name", {}], uname: ["shows the system name and kernel", { "-a": "everything" }],
    sudo: ["runs the next command as the administrator (root)", {}],
    python3: ["runs Python", { "-c": "run this Python code" }], python: ["runs Python", { "-c": "run this Python code" }],
    jq: ["picks fields out of JSON", { "-r": "print plain text, not quoted strings" }],
    diff: ["shows the lines that differ between two files", {}], comm: ["compares two sorted files line by line", {}],
    tee: ["prints and also saves to a file", { "-a": "add to the file instead of replacing it" }],
    xargs: ["runs a command on every line it is given", {}], column: ["lines text up in columns", { "-t": "make a table" }],
    for: ["a loop: repeat the commands between do and done for each item", {}], while: ["a loop: repeat while the test is true (while read … reads line by line)", {}],
    do: ["start of the loop body", {}], done: ["end of the loop", {}], if: ["run the next part only if the test succeeds", {}], then: ["the part to run if the test succeeded", {}], else: ["the part to run otherwise", {}], fi: ["end of the if", {}],
    read: ["reads one line into variables", {}], export: ["sets a variable for later commands", {}], true: ["does nothing, successfully", {}], test: ["checks a condition", {}]
  };
  var OPS = { "|": "the pipe: sends the output of the command on the left into the command on the right",
    "&&": "and then: run the next command only if this one worked", "||": "or else: run the next command only if this one failed",
    ";": "then: run the next command whatever happened", "\n": "" };
  var REDIR = { ">": "save the output in this file (replacing it)", ">>": "add the output to the end of this file", "<": "read the input from this file",
    "2>": "send error messages to this file", "2>/dev/null": "throw error messages away", "2>&1": "send errors to the same place as normal output", "&>": "send all output to this file" };

  function tokens(line) {
    var out = [], cur = "", q = "", has = false, depth = 0;
    function push() { if (has) out.push(cur); cur = ""; has = false; }
    for (var i = 0; i < line.length; i++) {
      var c = line[i], n2 = line.substr(i, 2);
      if (q) { cur += c; if (c === q) q = ""; continue; }
      if (c === "'" || c === '"') { q = c; cur += c; has = true; continue; }
      if (c === "$" && line[i + 1] === "(") { depth++; cur += "$("; i++; has = true; continue; }
      if (depth) { cur += c; if (c === "(") depth++; if (c === ")") depth--; continue; }
      if (c === "#" && !has && (!out.length || /^[|;&\n]+$/.test(out[out.length - 1]))) { while (i < line.length && line[i] !== "\n") i++; i--; continue; }
      if (c === "\\" && line[i + 1] === "\n") { i++; continue; }
      if (n2 === "&&" || n2 === "||" || n2 === ">>" || n2 === "&>") { push(); out.push(n2); i++; continue; }
      if (/^2>/.test(line.substr(i, 2)) && !has) {
        var m = /^2>(&1|\/dev\/null)?/.exec(line.slice(i));
        push(); out.push(m[0]); i += m[0].length - 1; continue;
      }
      if (c === "|" || c === ";" || c === ">" || c === "<" || c === "\n") { push(); out.push(c); continue; }
      if (c === " " || c === "\t") { push(); continue; }
      cur += c; has = true;
    }
    push();
    return out;
  }

  function argNote(t) {
    if (/^\d{1,3}(\.\d{1,3}){3}(\/\d+)?$/.test(t)) return /\//.test(t) ? "a whole network (every address in this range)" : "an IP address";
    if (/^https?:\/\//.test(t)) return "a web address";
    if (/^["']/.test(t)) return "text or a pattern for the command";
    if (/^\$\(/.test(t)) return "the output of the command inside $( )";
    if (/^\$/.test(t)) return "a variable's value";
    if (/[*?]/.test(t)) return "every file whose name matches";
    if (/\/|\.[A-Za-z0-9]{1,5}$|^~/.test(t)) return "a file or folder";
    if (/^\d+$/.test(t)) return "a number";
    if (/^[\w.-]+\.(net|com|org|lan|test|io|in|local|corp)$/.test(t)) return "a domain name";
    return ARG;
  }

  function flagNote(fl, t) {
    if (fl[t]) return fl[t];
    var eq = t.split("=")[0];
    if (fl[eq]) return fl[eq];
    if (/^-[A-Za-z]{2,}$/.test(t) && t.slice(1).split("").every(function (c) { return fl["-" + c]; }))
      return t.slice(1).split("").map(function (c) { return fl["-" + c]; }).join("; ");
    var best = "";
    Object.keys(fl).forEach(function (k) { if (k.length > 1 && t.indexOf(k) === 0 && k.length > best.length) best = k; });
    return best ? fl[best] + " (" + esc(t.slice(best.length)) + ")" : "";
  }

  function explain(script) {
    var tk = tokens(String(script || "").replace(/\r/g, "")), segs = [[]], joins = [];
    tk.forEach(function (t) {
      if (OPS[t] !== undefined) { if (segs[segs.length - 1].length) { segs.push([]); joins.push(t); } }
      else segs[segs.length - 1].push(t);
    });
    if (!segs[segs.length - 1].length) segs.pop();
    if (!segs.length) return '<p class="rb-exnone">Nothing to explain yet.</p>';
    return segs.map(function (s, si) {
      var j = 0;
      while (j < s.length && /^[A-Za-z_]\w*=/.test(s[j])) j++;
      var name = (s[j] || "").replace(/^\(+/, ""), base = name.split("/").pop(), info = CMD[base], rows = [];
      if (j > 0) rows.push("<li><code>" + esc(s.slice(0, j).join(" ")) + "</code> sets a variable for later</li>");
      for (var k = j + 1; k < s.length; k++) {
        var t = s[k];
        if (REDIR[t] !== undefined) { rows.push("<li><code>" + esc(t + (s[k + 1] && !/^2>/.test(t) ? " " + s[k + 1] : "")) + "</code> " + REDIR[t] + "</li>"); if (!/^2>/.test(t)) k++; continue; }
        var note = info ? flagNote(info[1], t) : "";
        if (!note && /^-/.test(t)) note = "an option for " + esc(base);
        if (!note) note = argNote(t);
        rows.push("<li><code>" + esc(t) + "</code> " + note + "</li>");
      }
      var head = info ? "<b>" + esc(base) + "</b> " + info[0] : base ? "<b>" + esc(base) + "</b> isn't in the lab's dictionary yet; try <code>" + esc(base) + " --help</code>" : "";
      return (si && joins[si - 1] !== "\n" ? '<div class="rb-exj"><code>' + esc(joins[si - 1]) + "</code> " + OPS[joins[si - 1]] + "</div>" : "") +
        '<div class="rb-exs"><div class="rb-exc"><code>' + esc(s.join(" ")) + '</code></div><div class="rb-exd">' + head + "</div>" +
        (rows.length ? "<ul>" + rows.join("") + "</ul>" : "") + "</div>";
    }).join("");
  }

  var TOOLS = {
    grep: ["Finds lines that contain a word or pattern.", "grep 'Failed password' auth.log"], awk: ["Picks columns out of each line.", "awk '{print $1}' access.log"],
    sort: ["Puts lines in order; -rn puts the biggest number first.", "sort -rn counts.txt"], uniq: ["Counts repeated lines (sort first).", "sort ips.txt | uniq -c"],
    cut: ["Keeps only some columns.", "cut -d, -f2 badge.csv"], head: ["Shows the first lines of a file.", "head -n 5 access.log"], tail: ["Shows the last lines of a file.", "tail -n 20 auth.log"],
    wc: ["Counts lines (-l), words and bytes.", "wc -l access.log"], sha256sum: ["Fingerprints a file so you can prove it never changed.", "sha256sum capture.pcap"],
    base64: ["Encodes or decodes (-d) base64 text.", "echo aGVsbG8= | base64 -d"], nmap: ["Finds machines that are up and their open ports.", "nmap -sV 10.0.0.5"],
    curl: ["Fetches a web page; -I shows only the headers.", "curl -I http://10.0.0.5/"], wget: ["Downloads a file from a web address.", "wget http://10.0.0.5/robots.txt"],
    tshark: ["Reads a packet capture; -Y filters, -T fields picks columns.", "tshark -r capture.pcap -Y dns"], dig: ["Looks up the address behind a name.", "dig +short example.net"],
    nslookup: ["Looks up a name's address (older than dig).", "nslookup example.net"], host: ["Quick name-to-address lookup.", "host web01.corp.lan"],
    whois: ["Shows who registered a domain and when.", "whois example.net"], nc: ["Checks whether a port is open (-z) or talks to it.", "nc -zv 10.0.0.5 20-25"],
    openssl: ["Shows a website's certificate.", "openssl s_client -connect site:443"], tar: ["Packs files into one archive.", "tar cf evidence.tar ."],
    find: ["Searches folders for files.", "find . -name '*.log'"], ls: ["Lists files; -l shows owners, sizes and dates.", "ls -l"], cat: ["Prints a whole file.", "cat notes.txt"],
    less: ["Reads a long file a screen at a time.", "less access.log"], strings: ["Pulls readable text out of a program file.", "strings suspect/kworkerd"],
    file: ["Says what kind of file it really is.", "file suspect/*"], xxd: ["Shows a file's raw bytes in hex.", "xxd -l 64 docm.bin"], sed: ["Finds and replaces text.", "sed 's/%20/ /g'"],
    traceroute: ["Lists the routers on the way to a machine.", "traceroute 198.51.100.66"], ping: ["Checks whether a machine answers.", "ping -c 3 web01"],
    nikto: ["Scans a website for common mistakes.", "nikto -h http://10.0.0.5"], gobuster: ["Guesses hidden pages on a website.", "gobuster dir -u http://10.0.0.5"],
    ssh: ["Logs in to another machine.", "ssh admin@10.0.0.5"], python: ["Runs Python in the notebook's Python cells.", "print(open('case/conn.csv').read())"],
    cyberchef: ["Decodes, decrypts and analyses data in the browser.", "Recipe: From Base64"], wireshark: ["Reads packet captures in a window (tshark is the command-line version).", "Filter: http.request"],
    jq: ["Picks fields out of JSON.", "jq '.[] | .user' audit.json"]
  };

  function tool(name) {
    var k = String(name || "").toLowerCase().replace(/\s.*$/, "");
    return TOOLS[k] || (CMD[k] ? [CMD[k][0].charAt(0).toUpperCase() + CMD[k][0].slice(1) + ".", ""] : null);
  }

  function bindExplain(root) {
    root.querySelectorAll("[data-explain]").forEach(function (b) {
      b.addEventListener("click", function () {
        var p = b.parentNode.querySelector(".rb-explain");
        p.hidden = !p.hidden;
        b.textContent = p.hidden ? "Explain" : "Hide explanation";
      });
    });
  }

  function store(k, v) {
    try {
      if (v === undefined) return JSON.parse(localStorage.getItem(k) || "null");
      localStorage.setItem(k, JSON.stringify(v));
    } catch (e) { return null; }
    return v;
  }

  global.LabKit = { esc: esc, local: local, remember: remember, reveal: reveal, rpc: rpc, sha256: sha256, submit: submit,
    award: award, missions: missions, norm: norm, answerHash: answerHash, key: key, inline: inline, guideLine: guideLine,
    hintHtml: hintHtml, askHtml: askHtml, bindGuide: bindGuide, bindCopy: bindCopy, copyText: copyText, md: md, explain: explain,
    tokens: tokens, tool: tool, bindExplain: bindExplain, store: store };
})(window);
