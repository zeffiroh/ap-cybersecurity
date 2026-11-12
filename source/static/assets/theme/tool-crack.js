(function (global) {
  "use strict";
  var K = global.AayatTools.kit;
  var WORDS = ("123456 password 12345678 qwerty 123456789 12345 1234 111111 1234567 dragon 123123 baseball abc123 football monkey letmein shadow master 696969 mustang " +
    "michael 666666 qwertyuiop 123321 1234567890 pussycat superman summer winter spring autumn welcome admin root toor changeme secret login princess sunshine " +
    "iloveyou trustno1 starwars hello freedom whatever nimbumart deploy backup shop india mumbai delhi cricket kestrel paperplane password1 test guest").split(" ");
  var CSS = ".tk-box td.tk-h{font:12px ui-monospace,Consolas,monospace;word-break:break-all}.tk-box tr.ok td{background:#fde2e1}";

  function kind(h) {
    h = String(h).trim();
    if (/^\$2[aby]\$/.test(h)) return "bcrypt";
    if (/^\$6\$/.test(h)) return "sha512crypt";
    if (/^\$argon2/.test(h)) return "argon2";
    if (/^[a-f0-9]+\$[a-f0-9]{64}$/i.test(h)) return "sha256(salt+password)";
    if (/^[a-f0-9]{32}$/i.test(h)) return "md5";
    if (/^[a-f0-9]{40}$/i.test(h)) return "sha1";
    if (/^[a-f0-9]{64}$/i.test(h)) return "sha256";
    if (/^[a-f0-9]{128}$/i.test(h)) return "sha512";
    return "";
  }
  function variants(w, rules) {
    var out = [w];
    if (rules) {
      var cap = w.charAt(0).toUpperCase() + w.slice(1), leet = w.replace(/a/g, "@").replace(/o/g, "0").replace(/e/g, "3").replace(/s/g, "$").replace(/i/g, "1");
      [w, cap].forEach(function (b) { ["1", "12", "123", "!", "1!", "2024", "2025", "2026", "2026!", "@123"].forEach(function (s) { out.push(b + s); }); });
      out.push(cap, w.toUpperCase(), leet, w.split("").reverse().join(""));
    }
    return out;
  }
  function hashOf(algo, word, salt) {
    if (algo === "sha256(salt+password)") return K.digest("sha256", salt + word);
    return K.digest(algo, word);
  }
  function hashes(files) {
    var out = [];
    Object.keys(files).sort().forEach(function (n) {
      var t = files[n];
      if (/\.csv$/i.test(n)) {
        var rows = K.csv(t);
        rows.forEach(function (r) {
          var col = Object.keys(r).filter(function (k) { return /hash|password|pass_?md5|pw/i.test(k) && kind(r[k]); })[0];
          if (col) out.push({ who: r.username || r.user || r.email || r.id || "", hash: r[col].trim(), file: n });
        });
      } else if (/hash/i.test(K.base(n))) {
        t.split(/\r?\n/).forEach(function (l) { var m = /^(?:([^:\s]+)[:\s]+)?(\S+)\s*$/.exec(l.trim()); if (m && kind(m[2])) out.push({ who: m[1] || "", hash: m[2], file: n }); });
      }
    });
    return out;
  }

  function mount(el, ctx) {
    K.css("tool-crack-css", CSS);
    var files = {}, list = [], words = WORDS.slice(), found = {};
    var F = K.frame(el, ctx, {
      title: "Password cracking lab", cls: "tk-box",
      body: '<p style="font-size:12.5px;margin:0 0 6px">Only on the lab\'s own data. Cracking hashes you aren\'t authorised to test is a crime.</p>' +
        '<div class="tl-row"><label style="flex-direction:row;align-items:center;gap:4px"><input type="checkbox" data-r="rules" checked> Also try rules (Capital, 123, !, 2026, leetspeak)</label>' +
        '<label class="tl-grow">Extra words <input data-r="extra" placeholder="company, team or pet names"></label></div>',
      actions: '<button type="button" class="btn dark" data-r="go">Crack</button>',
      showLabel: "Show the recorded result",
      show: function (a) { if (typeof a.n === "number") F.msg("The recorded run cracked " + a.n + " of " + list.length + "."); },
      after: '<div class="tl-scroll" data-r="out"></div>'
    });
    function draw() {
      F.r("out").innerHTML = list.length ? '<table class="tl-table"><tr><th>Account</th><th>Hash</th><th>Type</th><th>Password</th><th>File</th></tr>' + list.map(function (h) {
        var k = kind(h.hash), p = found[h.hash];
        return '<tr class="' + (p != null ? "ok" : "") + '"><td>' + K.esc(h.who) + '</td><td class="tk-h">' + K.esc(h.hash) + "</td><td>" + K.esc(k) + (/bcrypt|argon|crypt/.test(k) ? " <small>(slow by design: not tried here)</small>" : "") +
          "</td><td>" + (p != null ? "<b>" + K.esc(p) + "</b>" : "") + "</td><td>" + K.esc(K.base(h.file)) + "</td></tr>";
      }).join("") + "</table>" : "<p>No password hashes in this case. They are CSV columns named password_md5 or hash, or a file with hash in its name.</p>";
    }
    F.r("go").addEventListener("click", function () {
      var extra = F.r("extra").value.split(/[\s,]+/).filter(Boolean), pool = words.concat(extra), rules = F.r("rules").checked, tries = 0, t0 = Date.now();
      var todo = list.filter(function (h) { return found[h.hash] == null && /^(md5|sha1|sha256|sha512|sha256\(salt\+password\))$/.test(kind(h.hash)); });
      if (!todo.length) { F.msg("Nothing left that this lab can try."); return; }
      F.msg("Cracking…");
      var cands = [];
      pool.forEach(function (w) { variants(w, rules).forEach(function (v) { cands.push(v); }); });
      cands = cands.filter(function (w, i, a) { return a.indexOf(w) === i; });
      var i = 0;
      (function batch() {
        var jobs = [];
        for (var n = 0; n < 200 && i < cands.length; n++, i++) {
          (function (w) {
            todo.forEach(function (h) {
              if (found[h.hash] != null) return;
              var k = kind(h.hash), salt = k === "sha256(salt+password)" ? h.hash.split("$")[0] : "", target = (k === "sha256(salt+password)" ? h.hash.split("$")[1] : h.hash).toLowerCase();
              tries++;
              jobs.push(hashOf(k, w, salt).then(function (x) { if (x === target) found[h.hash] = w; }));
            });
          })(cands[i]);
        }
        Promise.all(jobs).then(function () {
          if (i < cands.length && todo.some(function (h) { return found[h.hash] == null; })) return batch();
          var n = list.filter(function (h) { return found[h.hash] != null; }).length;
          draw();
          F.msg("Cracked " + n + " of " + list.length + " with " + tries + " guesses in " + ((Date.now() - t0) / 1000).toFixed(1) + " s." + (n ? " Unsalted fast hashes fall to a wordlist in seconds: store passwords with bcrypt or Argon2." : "") + F.compare(n, "run"));
          F.ready({ n: n, files: list.map(function (h) { return h.file; }).filter(function (f, j, a) { return a.indexOf(f) === j; }), blank: [] }, "Password cracking: " + n + " of " + list.length + " hashes cracked with a wordlist");
        });
      })();
    });
    F.note("Loading…");
    F.files().then(function (fs) {
      files = K.textFiles(fs);
      list = hashes(files);
      Object.keys(files).forEach(function (n) { if (/wordlist|passwords\.txt|rockyou/i.test(K.base(n))) words = words.concat(files[n].split(/\r?\n/).map(function (x) { return x.trim(); }).filter(Boolean)); });
      F.note(list.length + " hashes, " + words.length + " words");
      draw();
    }).catch(function () { F.note(""); F.msg("The files didn't load.", true); });
  }

  global.AayatTools.register({ id: "crack", title: "Password cracking lab", console: true, group: "Penetration tester", mount: mount, kind: kind, variants: variants, hashes: hashes });
})(window);
