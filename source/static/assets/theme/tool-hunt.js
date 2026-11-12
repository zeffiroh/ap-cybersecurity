(function (global) {
  "use strict";
  var K = global.AayatTools.kit;
  var VERDICTS = [["", "Still hunting"], ["confirmed", "Confirmed: found the activity"], ["refuted", "Refuted: looked properly, it isn't there"], ["inconclusive", "Inconclusive: the data can't answer it"]];
  var CSS = ".th-box .th-step{border:1px solid #ccc;background:#fafafa;padding:6px 8px;margin-top:6px;font-size:12.5px}.th-box .th-step code{font:12px ui-monospace,Consolas,monospace;background:#fff;padding:1px 4px;border:1px solid #ddd}" +
    ".th-box .th-step button{float:right;border:0;background:none;cursor:pointer;color:#a00}.th-box .th-lines{margin:6px 0 0;padding:6px;background:#fff;border:1px solid #ddd;font:11.5px/1.4 ui-monospace,Consolas,monospace;white-space:pre-wrap;max-height:140px;overflow:auto}" +
    ".th-box textarea{min-height:46px}.th-box .th-hyp textarea{min-height:56px}";

  function search(files, file, q) {
    var re;
    try { re = new RegExp(q, "i"); } catch (e) { re = new RegExp(q.replace(/[.*+?^${}()|[\]\\]/g, "\\$&"), "i"); }
    var names = file ? [file] : Object.keys(files).sort(), hits = [];
    names.forEach(function (n) {
      String(files[n] || "").replace(/\r/g, "").split("\n").forEach(function (l, i) { if (l && re.test(l)) hits.push({ file: n, line: i + 1, text: l }); });
    });
    return hits;
  }
  function report(h) {
    var v = (VERDICTS.filter(function (x) { return x[0] === h.verdict; })[0] || VERDICTS[0])[1];
    return ["# Threat hunt", "", "## Hypothesis", "", h.hyp || "(none)", "", h.attack ? "ATT&CK: " + h.attack + "\n" : "", "## What was searched", ""]
      .concat(h.steps.map(function (s, i) { return (i + 1) + ". `" + s.q + "` in " + (s.file || "all files") + ": " + s.n + " hit" + (s.n === 1 ? "" : "s") + (s.note ? ". " + s.note : ""); }))
      .concat(["", "## Result", "", v, "", h.end || ""]).join("\n");
  }

  function mount(el, ctx) {
    K.css("tool-hunt-css", CSS);
    var files = {}, h = { hyp: "", attack: "", steps: [], verdict: "", end: "" }, lastHits = [];
    var F = K.frame(el, ctx, {
      title: "Threat hunt", cls: "th-box",
      body: '<div class="th-hyp"><label style="font-size:12px;display:block">Hypothesis: what do you think happened, and what would prove it?' +
        '<textarea class="tl-area" data-r="hyp" placeholder="If an attacker kept access to web01, a scheduled job or new account would start a process from an odd folder."></textarea></label></div>' +
        '<div class="tl-row"><label>ATT&amp;CK technique <input data-r="attack" placeholder="T1053.003" size="12"></label></div>' +
        '<div class="tl-row" style="margin-top:6px"><label>File <select data-r="file"><option value="">All files</option></select></label>' +
        '<label class="tl-grow">Search (text or regex) <input data-r="q" spellcheck="false" placeholder="cron|/tmp/"></label>' +
        '<button type="button" class="btn" data-r="run">Search</button><label class="tl-grow">Note <input data-r="snote" placeholder="what this tells you"></label>' +
        '<button type="button" class="btn" data-r="add" disabled>Log this search</button></div><pre class="th-lines" data-r="lines" hidden></pre><div data-r="steps"></div>' +
        '<div class="tl-row" style="margin-top:8px"><label>Result <select data-r="verdict">' + VERDICTS.map(function (v) { return '<option value="' + v[0] + '">' + K.esc(v[1]) + "</option>"; }).join("") +
        '</select></label><label class="tl-grow">What you concluded <textarea class="tl-area" data-r="end"></textarea></label></div>',
      actions: '<button type="button" class="btn dark" data-r="done">Finish the hunt</button><button type="button" class="btn" data-r="dl">Download the write-up</button>',
      showLabel: "Show the recorded result",
      show: function (a) { if (a.verdict != null) F.r("verdict").value = a.verdict; if (a.end != null) F.r("end").value = a.end; sync(); }
    });
    var st = F.st, init = F.saved || st;
    ["hyp", "attack", "verdict", "end"].forEach(function (k) { if (typeof init[k] === "string") h[k] = init[k]; });
    if (Array.isArray(init.steps)) h.steps = init.steps.slice();
    F.r("hyp").value = h.hyp; F.r("attack").value = h.attack; F.r("verdict").value = h.verdict; F.r("end").value = h.end;
    function sync() { h.hyp = F.r("hyp").value; h.attack = F.r("attack").value.trim(); h.verdict = F.r("verdict").value; h.end = F.r("end").value; F.remember(h); }
    function steps() {
      F.r("steps").innerHTML = h.steps.map(function (s, i) {
        return '<div class="th-step"><button type="button" data-del="' + i + '" aria-label="Remove">&times;</button><b>' + (i + 1) + ".</b> <code></code> in " + K.esc(s.file || "all files") +
          ": <b>" + s.n + "</b> hit" + (s.n === 1 ? "" : "s") + (s.note ? " &middot; " + K.esc(s.note) : "") + "</div>";
      }).join("");
      F.r("steps").querySelectorAll("code").forEach(function (c, i) { c.textContent = h.steps[i].q; });
    }
    ["hyp", "attack", "end"].forEach(function (k) { F.r(k).addEventListener("input", sync); });
    F.r("verdict").addEventListener("change", sync);
    F.r("run").addEventListener("click", function () {
      var q = F.r("q").value.trim();
      if (!q) { F.msg("Type what to search for.", true); return; }
      lastHits = search(files, F.r("file").value, q);
      F.r("lines").hidden = false;
      F.r("lines").textContent = lastHits.slice(0, 60).map(function (x) { return K.base(x.file) + ":" + x.line + ": " + x.text; }).join("\n") || "(no lines matched)";
      F.msg(lastHits.length + " matching line" + (lastHits.length === 1 ? "" : "s") + ".");
      F.r("add").disabled = false;
    });
    F.r("q").addEventListener("keydown", function (e) { if (e.key === "Enter") { e.preventDefault(); F.r("run").click(); } });
    F.r("add").addEventListener("click", function () {
      h.steps.push({ q: F.r("q").value.trim(), file: F.r("file").value, n: lastHits.length, note: F.r("snote").value.trim() });
      F.r("snote").value = "";
      F.r("add").disabled = true;
      steps();
      sync();
    });
    F.r("steps").addEventListener("click", function (e) { var b = e.target.closest("[data-del]"); if (b) { h.steps.splice(+b.getAttribute("data-del"), 1); steps(); sync(); } });
    F.r("dl").addEventListener("click", function () { sync(); K.download("threat-hunt.md", report(h), "text/markdown"); });
    F.r("done").addEventListener("click", function () {
      sync();
      if (!h.hyp.trim()) { F.msg("Write the hypothesis first: a hunt starts from a question.", true); return; }
      if (!h.steps.length) { F.msg("Log at least one search, so someone else can repeat the hunt.", true); return; }
      if (!h.verdict) { F.msg("Choose a result. \"Refuted\" and \"Inconclusive\" are real results too.", true); return; }
      var msg = "Hunt finished with " + h.steps.length + " logged search" + (h.steps.length === 1 ? "" : "es") + ".";
      if (F.answer && F.answer.verdict) msg += F.answer.verdict === h.verdict ? " Same result as the recorded hunt." : " The recorded hunt reached a different result.";
      F.msg(msg);
      F.ready({ hyp: h.hyp, attack: h.attack, steps: h.steps, verdict: h.verdict, end: h.end, files: h.steps.map(function (s) { return s.file; }).filter(Boolean), blank: ["verdict", "end"] },
        "Threat hunt: " + h.hyp.split("\n")[0].slice(0, 90));
    });
    steps();
    F.note("Loading the files…");
    F.files().then(function (fs) {
      files = K.textFiles(fs);
      var names = Object.keys(files).sort();
      F.r("file").innerHTML = '<option value="">All files</option>' + names.map(function (n) { return '<option value="' + K.esc(n) + '">' + K.esc(n) + "</option>"; }).join("");
      F.note(names.length + " files");
    }).catch(function () { F.note(""); F.msg("The files didn't load.", true); });
  }

  global.AayatTools.register({ id: "hunt", title: "Threat hunt", console: true, group: "SOC analyst", mount: mount, search: search, report: report });
})(window);
