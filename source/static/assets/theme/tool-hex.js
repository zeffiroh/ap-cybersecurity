(function (global) {
  "use strict";
  var K = global.AayatTools.kit;
  var MAX = 64 * 1024;
  var CSS = ".tx-box pre{margin:8px 0 0;padding:8px;background:#fff;border:1px solid #bbb;font:12px/1.45 ui-monospace,Consolas,monospace;max-height:340px;overflow:auto;white-space:pre}" +
    ".tx-box .tx-hash{font:12px ui-monospace,Consolas,monospace;word-break:break-all}.tx-box .tx-ent{display:block;width:100%;height:70px;background:#fafafa;border:1px solid #ddd;margin-top:6px}" +
    ".tx-box .tx-ent rect{fill:#1f4e8c}.tx-box .tx-ent rect.hi{fill:#c0392b}";

  function entropy(b, from, to) {
    var c = new Array(256).fill(0), n = to - from;
    if (n <= 0) return 0;
    for (var i = from; i < to; i++) c[b[i]]++;
    var e = 0;
    for (var j = 0; j < 256; j++) if (c[j]) { var p = c[j] / n; e -= p * Math.log2(p); }
    return e;
  }
  function dump(b, start) {
    var out = [];
    for (var o = start; o < Math.min(b.length, start + MAX); o += 16) {
      var hex = [], asc = "";
      for (var i = 0; i < 16; i++) {
        var v = b[o + i];
        hex.push(v == null ? "  " : ("0" + v.toString(16)).slice(-2));
        asc += v == null ? "" : v >= 32 && v < 127 ? String.fromCharCode(v) : ".";
      }
      out.push(("0000000" + o.toString(16)).slice(-8) + "  " + hex.slice(0, 8).join(" ") + "  " + hex.slice(8).join(" ") + "  |" + asc + "|");
    }
    return out.join("\n");
  }
  function strings(b, min) {
    var out = [], cur = "", at = 0;
    for (var i = 0; i <= b.length; i++) {
      var v = b[i];
      if (v != null && v >= 32 && v < 127) { if (!cur) at = i; cur += String.fromCharCode(v); }
      else { if (cur.length >= min) out.push([at, cur]); cur = ""; }
    }
    return out;
  }

  function mount(el, ctx) {
    K.css("tool-hex-css", CSS);
    var files = {}, bytes = null, cur = "", custody = [], hashes = {};
    var F = K.frame(el, ctx, {
      title: "Hex, strings and hashes", cls: "tx-box",
      body: '<div class="tl-row"><label class="tl-grow">File <select data-r="file"></select></label><label>View <select data-r="v"><option value="hex">Hex</option>' +
        '<option value="str">Strings</option></select></label><label>Min length <input data-r="min" type="number" value="6" min="3" max="40" style="width:60px"></label>' +
        '<label class="tl-grow">Find <input data-r="q" placeholder="text to look for"></label></div>',
      actions: '<button type="button" class="btn dark" data-r="hash">Hash it</button><button type="button" class="btn" data-r="log">Add to the custody log</button>' +
        '<button type="button" class="btn" data-r="dl">Download custody log</button>',
      showLabel: "Show the recorded hash",
      show: function (a) { if (a.sha256) F.msg("The recorded SHA-256 of " + (F.st.file || "the file") + " is " + a.sha256); },
      after: '<div class="tx-hash" data-r="hashes"></div><svg class="tx-ent" data-r="ent" viewBox="0 0 400 70" preserveAspectRatio="none"></svg><pre data-r="out"></pre>' +
        '<details style="margin-top:8px"><summary>Chain of custody (' + '<span data-r="cn">0</span> entries)</summary><div class="tl-row" style="margin-top:6px">' +
        '<label>Action <select data-r="act"><option>Collected</option><option>Copied for analysis</option><option>Analysed</option><option>Handed over</option><option>Stored</option></select></label>' +
        '<label>By <input data-r="by" placeholder="your name" size="14"></label><label class="tl-grow">Note <input data-r="cnote" placeholder="where it is kept, who has it"></label></div><div data-r="clist"></div></details>'
    });
    var init = F.saved || F.st;
    if (Array.isArray(init.custody)) custody = init.custody.slice();
    function keep() { F.remember({ file: cur, custody: custody }); }
    function show() {
      if (!bytes) return;
      var v = F.r("v").value, q = F.r("q").value;
      if (v === "hex") {
        var start = 0;
        if (q) { var at = new TextDecoder("latin1").decode(bytes).indexOf(q); if (at >= 0) start = at - (at % 16); F.msg(at >= 0 ? "Found at offset 0x" + at.toString(16) + "." : "Not found."); }
        F.r("out").textContent = dump(bytes, start) + (bytes.length - start > MAX ? "\n… showing 64 KB of " + bytes.length + " bytes" : "");
      } else {
        var ss = strings(bytes, Math.max(3, +F.r("min").value || 6)).filter(function (s) { return !q || s[1].toLowerCase().indexOf(q.toLowerCase()) >= 0; });
        F.r("out").textContent = ss.slice(0, 3000).map(function (s) { return ("0000000" + s[0].toString(16)).slice(-8) + "  " + s[1]; }).join("\n");
        F.msg(ss.length + " strings.");
      }
      var blocks = Math.min(100, Math.max(1, Math.ceil(bytes.length / 256))), size = Math.ceil(bytes.length / blocks), w = 400 / blocks, svg = "";
      for (var i = 0; i < blocks; i++) {
        var e = entropy(bytes, i * size, Math.min(bytes.length, (i + 1) * size)), h = e / 8 * 66;
        svg += '<rect x="' + (i * w).toFixed(2) + '" y="' + (68 - h).toFixed(1) + '" width="' + Math.max(0.5, w - 0.5).toFixed(2) + '" height="' + h.toFixed(1) + '"' + (e > 7.2 ? ' class="hi"' : "") + "><title>bytes " + i * size + "+: " + e.toFixed(2) + " bits per byte</title></rect>";
      }
      F.r("ent").innerHTML = svg;
    }
    function open(name) {
      cur = name;
      bytes = K.bytes(files[name] || "");
      hashes = {};
      var e = entropy(bytes, 0, bytes.length);
      F.r("hashes").innerHTML = "<b>" + bytes.length + " bytes</b>, entropy " + e.toFixed(2) + " bits per byte" + (e > 7.2 ? " (looks encrypted or packed)" : e < 5 ? " (plain text or code)" : "") + ".";
      show();
      keep();
    }
    function clist() {
      F.r("cn").textContent = custody.length;
      F.r("clist").innerHTML = custody.length ? '<table class="tl-table"><tr><th>When (UTC)</th><th>Action</th><th>File</th><th>SHA-256</th><th>By</th><th>Note</th></tr>' + custody.map(function (c) {
        return "<tr><td>" + K.esc(c.t) + "</td><td>" + K.esc(c.act) + "</td><td>" + K.esc(c.file) + '</td><td class="tx-hash">' + K.esc(c.sha256) + "</td><td>" + K.esc(c.by) + "</td><td>" + K.esc(c.note) + "</td></tr>";
      }).join("") + "</table>" : "<p>No entries yet. Hash a file, then add each time it is collected, copied or handed over.</p>";
    }
    F.r("file").addEventListener("change", function () { open(this.value); });
    F.r("v").addEventListener("change", show);
    F.r("min").addEventListener("change", show);
    F.r("q").addEventListener("keydown", function (e) { if (e.key === "Enter") { e.preventDefault(); show(); } });
    F.r("hash").addEventListener("click", function () {
      if (!bytes) return;
      Promise.all([K.digest("md5", bytes), K.digest("sha1", bytes), K.digest("sha256", bytes)]).then(function (h) {
        hashes = { md5: h[0], sha1: h[1], sha256: h[2] };
        el.querySelector("details").open = true;
        F.r("hashes").innerHTML += '<div>MD5 ' + h[0] + "</div><div>SHA-1 " + h[1] + "</div><div><b>SHA-256 " + h[2] + "</b></div>";
        var msg = "Hashed " + cur + ".";
        if (F.answer && F.answer.sha256) msg += F.answer.sha256 === h[2] ? " Same SHA-256 as the recorded hash: the file hasn't changed." : " Different from the recorded SHA-256: this isn't the same file, or it changed.";
        F.msg(msg);
        F.ready({ file: cur, sha256: h[2], n: custody.length, custody: custody, blank: ["sha256"] }, "Hashes: SHA-256 of " + cur + " is " + h[2]);
      });
    });
    F.r("log").addEventListener("click", function () {
      if (!hashes.sha256) { F.msg("Hash the file first, so the log proves what you had.", true); return; }
      if (!F.r("by").value.trim()) { F.msg("Write who is doing this. A custody log names a person every time.", true); return; }
      custody.push({ t: new Date().toISOString().replace(/\.\d+Z$/, "Z"), act: F.r("act").value, file: cur, sha256: hashes.sha256, by: F.r("by").value.trim(), note: F.r("cnote").value.trim() });
      F.r("cnote").value = "";
      clist();
      keep();
      F.ready({ file: cur, sha256: hashes.sha256, n: custody.length, custody: custody, blank: ["sha256"] }, "Chain of custody: " + custody.length + " entries for " + cur);
    });
    F.r("dl").addEventListener("click", function () {
      K.download("chain-of-custody.csv", "time_utc,action,file,sha256,by,note\n" + custody.map(function (c) {
        return [c.t, c.act, c.file, c.sha256, c.by, c.note].map(function (v) { v = String(v); return /[",\n]/.test(v) ? '"' + v.replace(/"/g, '""') + '"' : v; }).join(",");
      }).join("\n") + "\n", "text/csv");
    });

    F.note("Loading the files…");
    F.files().then(function (fs) {
      files = K.textFiles(fs);
      var names = Object.keys(files).sort();
      F.r("file").innerHTML = names.map(function (n) { return '<option value="' + K.esc(n) + '">' + K.esc(n) + "</option>"; }).join("");
      F.note(names.length + " files");
      clist();
      if (!names.length) { F.msg("There are no files here."); return; }
      var want = init.file && files[init.file] ? init.file : F.st.file && files[F.st.file] ? F.st.file : names[0];
      F.r("file").value = want;
      open(want);
    }).catch(function () { F.note(""); F.msg("The files didn't load.", true); });
  }

  global.AayatTools.register({ id: "hex", title: "Hex, strings and hashes", console: true, group: "Incident responder", mount: mount, entropy: entropy, strings: strings, dump: dump });
})(window);
