(function (global) {
  "use strict";

  var me = document.currentScript && document.currentScript.src;
  var ROOT = me ? me.replace(/assets\/theme\/notebook\.js.*$/, "") : "";
  var PYODIDE = "https://cdn.jsdelivr.net/pyodide/v0.26.4/full/";
  var $ = function (id) { return document.getElementById(id); };
  var q = new URLSearchParams(location.search);
  var ref = (q.get("ref") || "").replace(/[^A-Za-z0-9._-]/g, "").slice(0, 60);
  var space = (q.get("space") || "").replace(/[^a-z0-9]/g, "").slice(0, 20);
  var premium = (q.get("premium") || "").replace(/[^0-9]/g, "").slice(0, 12);
  var version = 0, theirs = null;
  var nb = { title: "", cells: [] }, timer = null, py = null, dirty = false;

  function esc(s) {
    return String(s == null ? "" : s).replace(/[&<>"]/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c];
    });
  }
  function rpc(fn, args) {
    var P = global.AayatProgress;
    return (P ? P.neon() : Promise.resolve(null)).then(function (db) {
      if (!db) throw new Error("The course database is not connected yet.");
      return db.rpc(fn, args || {}, { attempts: 1 });
    });
  }
  function email() { return global.Identity ? global.Identity.getEmail() : ""; }
  function local(k, v) {
    try {
      if (v === undefined) return JSON.parse(localStorage.getItem("aayat_nb_" + k) || "null");
      localStorage.setItem("aayat_nb_" + k, JSON.stringify(v));
    } catch (e) { return null; }
  }
  function map() { return global.AAYAT_MAP || { units: [], topics: {}, atoms: {} }; }

  function labUrl(atom) {
    var M = map(), t = atom.split(".").slice(0, 2).join("."), tp = M.topics[t], a = M.atoms[atom];
    if (!tp || !a) return ROOT + "lab/lab/index.html";
    var u = M.units.filter(function (x) { return x.n === tp.u; })[0] || { n: tp.u, title: "" };
    var safe = function (s) { return s.replace(/[<>:"\/\\|?*]/g, "").trim().slice(0, 60); };
    var path = [safe("Unit " + u.n + " " + u.title), safe(t + " " + tp.title), safe(atom + " " + a.title) + ".ipynb"].join("/");
    return ROOT + "lab/lab/index.html?path=" + encodeURIComponent(path);
  }

  function mdHtml(src) {
    var out = [], list = false;
    String(src || "").split("\n").forEach(function (line) {
      var l = esc(line).replace(/`([^`]+)`/g, "<code>$1</code>").replace(/\*\*([^*]+)\*\*/g, "<b>$1</b>")
        .replace(/\*([^*]+)\*/g, "<i>$1</i>").replace(/\[([^\]]+)\]\((https?:[^)\s]+)\)/g, '<a href="$2" target="_blank" rel="noopener">$1</a>');
      var h = /^(#{1,4})\s+(.*)$/.exec(l), li = /^\s*[-*]\s+(.*)$/.exec(l);
      if (li) { if (!list) { out.push("<ul>"); list = true; } out.push("<li>" + li[1] + "</li>"); return; }
      if (list) { out.push("</ul>"); list = false; }
      if (h) out.push("<h" + (h[1].length + 1) + ">" + h[2] + "</h" + (h[1].length + 1) + ">");
      else if (l.trim()) out.push("<p>" + l + "</p>");
    });
    if (list) out.push("</ul>");
    return out.join("");
  }

  function status(t) { $("nb-status").textContent = t; }

  function save(now) {
    dirty = true;
    clearTimeout(timer);
    timer = setTimeout(function () {
      nb.title = $("nb-title").value;
      if (space) return shareSave();
      local(ref, nb);
      if (!email()) { status("Saved in this browser. Sign in to keep it in your account."); dirty = false; return; }
      status("Saving…");
      rpc("api_notebook_save", { p_ref: ref, p_data: nb }).then(function (r) {
        if (!r.ok) throw new Error(r.error);
        dirty = false;
        status("Saved to your account · " + new Date().toLocaleTimeString());
      }).catch(function (e) { status("Saved in this browser only: " + e.message); });
    }, now ? 0 : 1500);
  }

  function shareSave(force) {
    status("Saving for everyone…");
    rpc("api_shared_save", { p_space: space, p_data: nb, p_version: force ? theirs.version : version }).then(function (r) {
      if (r.conflict) {
        return rpc("api_shared_get", { p_space: space }).then(function (d) {
          theirs = d;
          $("nb-clash").hidden = false;
          status("");
        });
      }
      if (!r.ok) throw new Error(r.error);
      version = r.version;
      dirty = false;
      $("nb-clash").hidden = true;
      status("Saved for everyone · " + new Date().toLocaleTimeString());
    }).catch(function (e) { status(e.message); });
  }

  var YJS = "https://cdn.jsdelivr.net/npm/yjs@13.6.20/+esm";
  function b64(u8) {
    var out = "";
    for (var i = 0; i < u8.length; i += 0x8000) out += String.fromCharCode.apply(null, u8.subarray(i, i + 0x8000));
    return btoa(out);
  }
  function unb64(t) {
    var raw = atob(t), u8 = new Uint8Array(raw.length);
    for (var i = 0; i < raw.length; i++) u8[i] = raw.charCodeAt(i);
    return u8;
  }

  function liveEditor() {
    import(YJS).then(live, function () { sharedEditor(); });
  }

  function live(Y) {
    var doc = new Y.Doc(), cells = doc.getArray("cells"), title = doc.getText("title");
    var lastId = 0, queue = [], pushing = false, outputs = {}, edits = {}, caret = null, pullTimer = null, active = Date.now();
    $("nb-index").hidden = true;
    $("nb-editor").hidden = false;
    $("nb-book").hidden = true;
    $("nb-crumb").innerHTML = '<a href="community.html#' + space + '">Back to the forum</a> &middot; Shared notebook &middot; <span id="nb-here"></span>';
    var uid = function () { return Math.random().toString(36).slice(2, 10); };

    function model() {
      nb.title = title.toString();
      nb.cells = cells.toArray().map(function (m) {
        var id = m.get("id");
        return { id: id, t: m.get("t"), s: m.get("s").toString(), o: outputs[id] || "", edit: !!edits[id] };
      });
    }
    function render() {
      var f = document.activeElement, cell = f && f.closest && f.closest(".nb-cell"), fid = cell && cell.getAttribute("data-id");
      model();
      if (document.activeElement !== $("nb-title")) $("nb-title").value = nb.title;
      draw();
      if (fid) {
        var t = document.querySelector('.nb-cell[data-id="' + fid + '"] textarea');
        if (t) { t.focus(); restore(t, fid); }
      }
    }
    function ytext(i) { return cells.get(i).get("s"); }
    function remember(t) {
      var cell = t.closest(".nb-cell"), i = +cell.getAttribute("data-i");
      if (!cells.get(i)) return;
      caret = { id: cell.getAttribute("data-id"), a: Y.createRelativePositionFromTypeIndex(ytext(i), t.selectionStart),
        b: Y.createRelativePositionFromTypeIndex(ytext(i), t.selectionEnd) };
    }
    function restore(t, id) {
      if (!caret || caret.id !== id) return;
      var a = Y.createAbsolutePositionFromRelativePosition(caret.a, doc), b = Y.createAbsolutePositionFromRelativePosition(caret.b, doc);
      if (a && b) t.setSelectionRange(a.index, b.index);
    }

    ops.text = function (i, v, t) {
      var yt = ytext(i), old = yt.toString();
      if (old === v) return;
      var s0 = 0, e0 = old.length, e1 = v.length;
      while (s0 < e0 && s0 < e1 && old[s0] === v[s0]) s0++;
      while (e0 > s0 && e1 > s0 && old[e0 - 1] === v[e1 - 1]) { e0--; e1--; }
      doc.transact(function () {
        if (e0 > s0) yt.delete(s0, e0 - s0);
        if (e1 > s0) yt.insert(s0, v.slice(s0, e1));
      }, "local");
      if (t) remember(t);
      active = Date.now();
    };
    ops.remove = function (i) { cells.delete(i, 1); };
    ops.move = function (i, d) {
      var m = cells.get(i), copy = new Y.Map();
      doc.transact(function () {
        copy.set("id", m.get("id")); copy.set("t", m.get("t")); copy.set("s", new Y.Text(m.get("s").toString()));
        cells.delete(i, 1);
        cells.insert(i + d, [copy]);
      }, "local");
    };
    ops.add = function (t) {
      var m = new Y.Map(), id = uid();
      m.set("id", id); m.set("t", t); m.set("s", new Y.Text(""));
      edits[id] = true;
      cells.push([m]);
    };
    var oldDraw = draw;
    draw = function () {
      oldDraw();
      document.querySelectorAll("#nb-cells textarea").forEach(function (t) {
        ["keyup", "click", "select"].forEach(function (ev) { t.addEventListener(ev, function () { remember(t); }); });
      });
      document.querySelectorAll("#nb-cells [data-view]").forEach(function (b) {
        b.addEventListener("click", function () {
          var id = b.closest(".nb-cell").getAttribute("data-id");
          edits[id] = !edits[id];
          render();
        }, true);
      });
    };
    save = function () {
      document.querySelectorAll(".nb-cell").forEach(function (el) {
        var c = nb.cells[+el.getAttribute("data-i")];
        if (c && c.id && c.o) outputs[c.id] = c.o;
      });
    };

    doc.on("update", function (u, origin) {
      if (origin !== "remote") { queue.push(u); push(); }
    });
    cells.observeDeep(function (ev, tr) {
      if (tr.origin === "remote" || !ev.every(function (e) { return e.target === cells ? false : true; })) render();
    });
    title.observe(function (ev, tr) { if (tr.origin === "remote") render(); });
    $("nb-title").addEventListener("input", function () {
      var v = $("nb-title").value, old = title.toString();
      doc.transact(function () { title.delete(0, old.length); title.insert(0, v); }, "local");
    });

    function push() {
      if (pushing || !queue.length) return;
      pushing = true;
      setTimeout(function () {
        var u = Y.mergeUpdates(queue);
        queue = [];
        rpc("api_shared_push", { p_space: space, p_update: b64(u) }).then(function (r) {
          if (!r.ok) throw new Error(r.error);
          status("Saved for everyone · " + new Date().toLocaleTimeString());
        }).catch(function (e) { queue.unshift(u); status("Not saved yet: " + e.message); })
          .then(function () { pushing = false; if (queue.length) push(); });
      }, 300);
    }

    function snapshot() {
      model();
      return { title: nb.title, cells: nb.cells.map(function (c) { return { t: c.t, s: c.s }; }) };
    }

    function pull() {
      clearTimeout(pullTimer);
      return rpc("api_shared_pull", { p_space: space, p_after: lastId }).then(function (r) {
        if (!r.ok) throw new Error(r.error);
        var gap = r.upto > lastId && (!r.updates.length || r.updates[0][0] > lastId + 1);
        return (gap ? rpc("api_shared_get", { p_space: space }).then(function (g) {
          if (g.ystate) Y.applyUpdate(doc, unb64(g.ystate), "remote");
          lastId = Math.max(lastId, g.upto || 0);
        }) : Promise.resolve()).then(function () {
          r.updates.forEach(function (u) {
            if (u[0] > lastId) { Y.applyUpdate(doc, unb64(u[1]), "remote"); lastId = u[0]; }
          });
          $("nb-here").textContent = r.here.length ? "Here now: " + r.here.join(", ") : "";
          if (r.count > 150 && Math.random() < 0.34) {
            rpc("api_shared_compact", { p_space: space, p_state: b64(Y.encodeStateAsUpdate(doc)), p_upto: lastId, p_data: snapshot() });
          }
        });
      }).catch(function (e) { status(e.message); }).then(function () {
        var quick = !document.hidden && Date.now() - active < 600000;
        pullTimer = setTimeout(pull, quick ? 1500 : 10000);
      });
    }

    document.addEventListener("visibilitychange", function () { if (!document.hidden) { active = Date.now(); pull(); } });
    document.addEventListener("keydown", function () { active = Date.now(); });
    $("nb-addmd").addEventListener("click", function () { add("md"); });
    $("nb-addpy").addEventListener("click", function () { add("py"); });
    $("nb-runall").addEventListener("click", function () {
      var p = Promise.resolve();
      nb.cells.forEach(function (c, i) { if (c.t === "py") p = p.then(function () { return run(i); }); });
    });
    $("nb-dl").addEventListener("click", function () { model(); download(); });
    $("nb-lab").href = ROOT + "lab/lab/index.html";
    $("nb-import").addEventListener("click", function () { $("nb-file").click(); });
    $("nb-file").addEventListener("change", function () {
      var f = $("nb-file").files[0], r = new FileReader();
      if (!f) return;
      r.onload = function () {
        try {
          var j = JSON.parse(r.result);
          doc.transact(function () {
            (j.cells || []).forEach(function (c) {
              var src = Array.isArray(c.source) ? c.source.join("") : String(c.source || "");
              if (!src.trim()) return;
              var m = new Y.Map();
              m.set("id", uid()); m.set("t", c.cell_type === "code" ? "py" : "md"); m.set("s", new Y.Text(src));
              cells.push([m]);
            });
          }, "local");
          status("Imported " + f.name + " for everyone.");
        } catch (e) { status("That file isn't a notebook (.ipynb)."); }
        $("nb-file").value = "";
      };
      r.readAsText(f);
    });

    rpc("api_shared_get", { p_space: space }).then(function (g) {
      if (!g.ok) throw new Error(g.error);
      if (g.ystate) Y.applyUpdate(doc, unb64(g.ystate), "remote");
      lastId = g.upto || 0;
      return pull().then(function () {
        if (!cells.length && !title.length) {
          var d = g.data || {};
          doc.transact(function () {
            title.insert(0, d.title || "Shared notebook");
            (d.cells || []).forEach(function (c) {
              var m = new Y.Map();
              m.set("id", uid()); m.set("t", c.t === "py" ? "py" : "md"); m.set("s", new Y.Text(c.s || ""));
              cells.push([m]);
            });
          }, "local");
        }
        render();
        status("Live: everyone in this space edits together. Changes save as you type.");
      });
    }).catch(function (e) { status(e.message); });
  }

  function sharedEditor() {
    $("nb-index").hidden = true;
    $("nb-editor").hidden = false;
    $("nb-book").hidden = true;
    var clash = document.createElement("div");
    clash.id = "nb-clash";
    clash.className = "nb-clash";
    clash.hidden = true;
    clash.innerHTML = "Someone else saved this notebook while you were editing. " +
      '<button class="btn" id="nb-theirs">Load their version</button> <button class="btn dark" id="nb-mine">Keep mine (replace theirs)</button>';
    $("nb-cells").parentNode.insertBefore(clash, $("nb-cells"));
    $("nb-theirs").addEventListener("click", function () { apply(theirs); dirty = false; clash.hidden = true; });
    $("nb-mine").addEventListener("click", function () { shareSave(true); });
    $("nb-title").addEventListener("input", function () { save(); });
    $("nb-addmd").addEventListener("click", function () { add("md"); });
    $("nb-addpy").addEventListener("click", function () { add("py"); });
    $("nb-runall").addEventListener("click", function () {
      var p = Promise.resolve();
      nb.cells.forEach(function (c, i) { if (c.t === "py") p = p.then(function () { return run(i); }); });
    });
    $("nb-dl").addEventListener("click", download);
    $("nb-lab").href = ROOT + "lab/lab/index.html";
    $("nb-import").addEventListener("click", function () { $("nb-file").click(); });
    $("nb-file").addEventListener("change", importNb);
    function apply(d) {
      version = d.version || 0;
      nb = d.data && d.data.cells ? { title: d.data.title || "", cells: d.data.cells } : { title: "Shared notebook", cells: [] };
      $("nb-title").value = nb.title;
      draw();
      status(d.by ? "Shared · last saved by " + d.by + " " + new Date(d.updated).toLocaleString() : "Shared with everyone in this space. Edits save for everyone.");
    }
    rpc("api_shared_get", { p_space: space }).then(function (d) {
      if (!d.ok) throw new Error(d.error);
      $("nb-crumb").innerHTML = '<a href="community.html#' + space + '">Back to the forum</a> &middot; Shared notebook';
      apply(d);
      setInterval(function () {
        if (dirty || document.hidden) return;
        var focus = document.activeElement && /TEXTAREA|INPUT/.test(document.activeElement.tagName);
        rpc("api_shared_get", { p_space: space }).then(function (n) { if (n.ok && n.version > version && !focus) apply(n); });
      }, 20000);
    }).catch(function (e) { status(e.message); });
  }

  function grow(t) { t.style.height = "auto"; t.style.height = Math.max(60, t.scrollHeight + 4) + "px"; }

  function draw() {
    var box = $("nb-cells");
    box.innerHTML = nb.cells.map(function (c, i) {
      var code = c.t === "py";
      return '<section class="nb-cell ' + (code ? "nb-code" : "nb-md") + '" data-i="' + i + '" data-id="' + esc(c.id || "") + '">' +
        '<div class="nb-bar"><span>' + (code ? "Python" : "Notes") + "</span>" +
        (code ? '<button class="btn dark" data-run>Run</button>' : '<button class="btn" data-view>' + (c.edit ? "Done" : "Edit") + "</button>") +
        '<button class="btn" data-up title="Move up">&uarr;</button><button class="btn" data-down title="Move down">&darr;</button>' +
        '<button class="btn" data-del title="Delete cell">&times;</button></div>' +
        (code || c.edit || !c.s ? '<textarea spellcheck="' + (code ? "false" : "true") + '">' + esc(c.s) + "</textarea>"
          : '<div class="nb-view">' + mdHtml(c.s) + "</div>") +
        (code ? '<pre class="nb-out"' + (c.o ? "" : " hidden") + ">" + esc(c.o || "") + "</pre>" : "") + "</section>";
    }).join("") || '<p class="nb-empty">Empty notebook. Add notes or code below.</p>';
    box.querySelectorAll(".nb-cell").forEach(function (el) {
      var i = +el.getAttribute("data-i"), c = nb.cells[i], t = el.querySelector("textarea");
      if (t) {
        grow(t);
        t.addEventListener("input", function () { ops.text(i, t.value, t); grow(t); });
        t.addEventListener("keydown", function (e) {
          if (e.key === "Tab") { e.preventDefault(); var p = t.selectionStart; t.setRangeText("    ", p, t.selectionEnd, "end"); ops.text(i, t.value, t); }
          if (e.key === "Enter" && e.shiftKey && c.t === "py") { e.preventDefault(); run(i); }
        });
      }
      var v = el.querySelector(".nb-view");
      if (v) v.addEventListener("dblclick", function () { c.edit = true; draw(); });
      el.querySelector("[data-del]").addEventListener("click", function () { ops.remove(i); });
      el.querySelector("[data-up]").addEventListener("click", function () { if (i) ops.move(i, -1); });
      el.querySelector("[data-down]").addEventListener("click", function () { if (i < nb.cells.length - 1) ops.move(i, 1); });
      var r = el.querySelector("[data-run]");
      if (r) r.addEventListener("click", function () { run(i); });
      var vw = el.querySelector("[data-view]");
      if (vw) vw.addEventListener("click", function () { c.edit = !c.edit; draw(); });
    });
  }

  function loadPy() {
    if (py) return py;
    status("Starting Python (first run takes a few seconds)…");
    py = new Promise(function (ok, bad) {
      var s = document.createElement("script");
      s.src = PYODIDE + "pyodide.js";
      s.onload = function () { global.loadPyodide({ indexURL: PYODIDE }).then(ok, bad); };
      s.onerror = function () { bad(new Error("Couldn't load Python. Check your connection.")); };
      document.head.appendChild(s);
    });
    py.catch(function () { py = null; });
    return py;
  }

  function run(i) {
    var c = nb.cells[i];
    var el = document.querySelector('.nb-cell[data-i="' + i + '"] .nb-out');
    el.hidden = false; el.textContent = "Running…";
    return loadPy().then(function (P) {
      var out = [];
      P.setStdout({ batched: function (s) { out.push(s); } });
      P.setStderr({ batched: function (s) { out.push(s); } });
      return P.loadPackagesFromImports(c.s).then(function () { return P.runPythonAsync(c.s); }).then(function (r) {
        if (r !== undefined && r !== null) out.push(String(r));
      }, function (e) { out.push(String(e.message || e).split("\n").slice(-6).join("\n")); }).then(function () {
        c.o = out.join("\n");
        el.textContent = c.o || "(no output)";
        status("Ran cell " + (i + 1) + ".");
        save();
      });
    }).catch(function (e) { el.textContent = e.message; });
  }

  var ops = {
    text: function (i, v) { nb.cells[i].s = v; save(); },
    remove: function (i) { nb.cells.splice(i, 1); draw(); save(); },
    move: function (i, d) { nb.cells.splice(i + d, 0, nb.cells.splice(i, 1)[0]); draw(); save(); },
    add: function (t) { nb.cells.push({ t: t, s: "", edit: true }); draw(); save(); }
  };
  function add(t) { ops.add(t); }

  function codeBookUrl() {
    var a = map().atoms[ref];
    return a ? ROOT + "teacher/" + a.href.replace(/index\.html$/, "") + ref + "-student.ipynb" : "";
  }

  function loadBook() {
    var u = codeBookUrl();
    if (!u) return Promise.resolve();
    status("Loading the code book…");
    return fetch(u).then(function (r) { if (!r.ok) throw new Error("No code book for this lesson yet."); return r.json(); }).then(function (j) {
      var cells = (j.cells || []).map(function (c) {
        var s = Array.isArray(c.source) ? c.source.join("") : String(c.source || "");
        return { t: c.cell_type === "code" ? "py" : "md", s: s };
      }).filter(function (c) { return c.s.trim(); });
      nb.cells = nb.cells.concat(cells);
      if (!nb.title) nb.title = ref + " code book";
      $("nb-title").value = nb.title;
      draw(); save(true);
      status("Code book loaded. Your edits save as you go.");
    }).catch(function (e) { status(e.message); });
  }

  function importNb() {
    var f = $("nb-file").files[0];
    if (!f) return;
    var r = new FileReader();
    r.onload = function () {
      try {
        var j = JSON.parse(r.result);
        var cells = (j.cells || []).map(function (c) {
          var s = Array.isArray(c.source) ? c.source.join("") : String(c.source || "");
          return { t: c.cell_type === "code" ? "py" : "md", s: s };
        }).filter(function (c) { return c.s.trim(); });
        nb.cells = nb.cells.concat(cells);
        draw(); save(true);
        status("Imported " + cells.length + " cells from " + f.name + ".");
      } catch (e) { status("That file isn't a notebook (.ipynb)."); }
      $("nb-file").value = "";
    };
    r.readAsText(f);
  }

  function download() {
    var j = { nbformat: 4, nbformat_minor: 5, metadata: { kernelspec: { name: "python3", display_name: "Python 3", language: "python" } },
      cells: nb.cells.map(function (c) {
        return c.t === "py" ? { cell_type: "code", metadata: {}, execution_count: null, outputs: [], source: c.s }
          : { cell_type: "markdown", metadata: {}, source: c.s };
      }) };
    var a = document.createElement("a");
    a.href = URL.createObjectURL(new Blob([JSON.stringify(j, null, 1)], { type: "application/x-ipynb+json" }));
    a.download = (ref || "notebook") + ".ipynb";
    a.click();
  }

  function listPage() {
    $("nb-editor").hidden = true;
    $("nb-index").hidden = false;
    var M = map();
    $("nb-lesson").innerHTML = M.units.map(function (u) {
      return '<optgroup label="Unit ' + u.n + '">' + u.topics.map(function (t) {
        return M.topics[t].atoms.map(function (a) { return '<option value="' + a + '">' + esc(a + " " + M.atoms[a].title) + "</option>"; }).join("");
      }).join("") + "</optgroup>";
    }).join("");
    $("nb-open").addEventListener("click", function () { location.search = "?ref=" + encodeURIComponent($("nb-lesson").value); });
    $("nb-openbook").addEventListener("click", function () { location.search = "?ref=" + encodeURIComponent($("nb-lesson").value) + "&book=1"; });
    $("nb-new").addEventListener("click", function () { location.search = "?ref=my-" + Date.now().toString(36); });
    if (!email()) { $("nb-mine").innerHTML = '<p class="nb-empty">Sign in to see the notebooks saved to your account.</p>'; return; }
    rpc("api_notebook_list").then(function (list) {
      $("nb-mine").innerHTML = list.length ? '<ul class="nb-list">' + list.map(function (n) {
        var a = M.atoms[n.ref];
        return '<li><a href="?ref=' + encodeURIComponent(n.ref) + '">' + esc(n.title || (a ? n.ref + " " + a.title : n.ref)) + "</a> <small>" +
          new Date(n.updated).toLocaleDateString() + "</small></li>";
      }).join("") + "</ul>" : '<p class="nb-empty">No notebooks yet. Open one for a lesson below.</p>';
    }).catch(function (e) { $("nb-mine").textContent = e.message; });
  }

  function editor(initial, crumb) {
    $("nb-index").hidden = true;
    $("nb-editor").hidden = false;
    var a = map().atoms[ref];
    $("nb-crumb").innerHTML = crumb || '<a href="notebook.html">My notebooks</a>' + (a ? ' &middot; <a href="' + ROOT + a.href + '">Lesson ' + esc(ref) + "</a>" : "");
    $("nb-book").hidden = !a;
    $("nb-title").addEventListener("input", function () { save(); });
    $("nb-addmd").addEventListener("click", function () { add("md"); });
    $("nb-addpy").addEventListener("click", function () { add("py"); });
    $("nb-runall").addEventListener("click", function () {
      var p = Promise.resolve();
      nb.cells.forEach(function (c, i) { if (c.t === "py") p = p.then(function () { return run(i); }); });
    });
    $("nb-book").addEventListener("click", loadBook);
    $("nb-lab").href = a ? labUrl(ref) : ROOT + "lab/lab/index.html";
    $("nb-import").addEventListener("click", function () { $("nb-file").click(); });
    $("nb-file").addEventListener("change", importNb);
    $("nb-dl").addEventListener("click", download);
    global.addEventListener("beforeunload", function (e) { if (dirty) { save(true); e.preventDefault(); } });
    var start = function (d) {
      nb = d && d.cells ? { title: d.title || "", cells: d.cells } : { title: a ? ref + " " + a.title : "My notebook", cells: [] };
      $("nb-title").value = nb.title;
      draw();
      if (q.get("book") && !nb.cells.some(function (c) { return c.t === "py"; })) loadBook();
      else status(email() ? "Saved to your account as you type." : "Sign in to keep this notebook in your account.");
    };
    if (initial && initial.teacher) start(initial);
    else if (email()) rpc("api_notebook_get", { p_ref: ref }).then(function (d) { start(d && d.cells ? d : local(ref) || initial); }, function () { start(local(ref) || initial); });
    else start(local(ref) || initial);
  }

  function premiumBoot() {
    var crumb = '<a href="' + ROOT + 'labs.html">Labs</a> &middot; <a href="' + ROOT + "labs.html?id=" + premium + '">Back to the lab page</a>';
    Promise.all([rpc("api_whoami").catch(function () { return {}; }), rpc("api_premium_get", { p_id: +premium })]).then(function (r) {
      var who = r[0] || {}, d = r[1];
      if (!d || !d.ok) {
        $("nb-index").hidden = false;
        $("nb-index").innerHTML = "<h1>" + esc((d && d.title) || "Notebook") + "</h1><p>" + esc((d && d.error) || "Not found.") + "</p>" +
          (d && d.locked ? '<p><a class="btn dark" href="' + ROOT + 'store.html#labs">Get Labs</a> <a class="btn" href="' + ROOT + 'store.html#redeem">I have a code</a></p>' : "") +
          (email() ? "" : '<p><button class="btn" id="nb-pw-signin">Sign in</button></p>');
        var b = $("nb-pw-signin");
        if (b) b.addEventListener("click", function () { if (global.Identity) global.Identity.open({}, function () { location.reload(); }); });
        return;
      }
      var item = d.item, data = item.data && item.data.cells ? item.data : { title: item.title, cells: [] };
      data = { title: data.title || item.title, cells: data.cells.map(function (c) { return { t: c.t, s: c.s }; }), teacher: !!who.teacher };
      if (who.teacher) {
        ref = "";
        save = function (now) {
          dirty = true;
          clearTimeout(timer);
          timer = setTimeout(function () {
            nb.title = $("nb-title").value;
            status("Saving to the database…");
            rpc("api_teacher_premium_save", { p: { id: +premium, kind: "notebook", title: nb.title || item.title,
              data: { title: nb.title, cells: nb.cells.map(function (c) { return { t: c.t, s: c.s }; }) } } }).then(function (r) {
              if (!r.ok) throw new Error(r.error);
              dirty = false;
              status("Saved for Labs students · " + new Date().toLocaleTimeString());
            }).catch(function (e) { status("Not saved: " + e.message); });
          }, now ? 0 : 1500);
        };
        editor(data, crumb + " &middot; <b>Teacher: editing the Labs copy</b>");
      } else {
        ref = "premium-" + premium;
        editor(data, crumb + " &middot; Your own copy, saved to your account");
      }
    }).catch(function (e) { status(e.message); });
  }

  function boot() {
    if (!$("nb-app")) return;
    if (premium) premiumBoot(); else if (space) liveEditor(); else if (ref) editor(); else listPage();
  }
  if (document.readyState === "complete") boot();
  else global.addEventListener("load", boot);
})(window);
