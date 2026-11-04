(function (global) {
  "use strict";

  var me = document.currentScript && document.currentScript.src;
  var ROOT = me ? me.replace(/assets\/theme\/labs\.js.*$/, "") : "";
  var $ = function (id) { return document.getElementById(id); };
  var TOOLS = { linux: ["Open the Linux lab", "linux.html"], jupyter: ["Open JupyterLab", "lab/lab/index.html"],
    sqli: ["Open the SQL injection lab", "sqli.html"], shop: ["Open Hack the shop", "shop.html"],
    cyberchef: ["Open CyberChef", "cyberchef/index.html"], ctf: ["Open the CTF board", "ctf.html"] };
  var access = null;

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
  function signIn() { if (global.Identity) global.Identity.open({}, function () { location.reload(); }); }

  function inline(t) {
    return esc(t).replace(/`([^`]+)`/g, "<code>$1</code>").replace(/\*\*([^*]+)\*\*/g, "<b>$1</b>")
      .replace(/\[([^\]]+)\]\((https:\/\/[^\s)]+)\)/g, '<a href="$2" target="_blank" rel="noopener nofollow">$1</a>');
  }

  function markup(text) {
    return String(text || "").split(/```[^\n]*\n?/).map(function (part, i) {
      if (i % 2) return '<div class="lb-code"><pre>' + esc(part.replace(/\n$/, "")) + '</pre><button class="btn" data-copy>Copy</button></div>';
      return part.split(/\n{2,}/).filter(function (x) { return x.trim(); }).map(function (para) {
        var p = para.trim(), m = p.match(/^(#{1,3})\s+(.*)$/);
        if (m) return "<h" + (m[1].length + 1) + ">" + inline(m[2]) + "</h" + (m[1].length + 1) + ">";
        if (/^[-*] /.test(p)) return "<ul>" + p.split(/\n/).map(function (l) { return "<li>" + inline(l.replace(/^[-*] /, "")) + "</li>"; }).join("") + "</ul>";
        return "<p>" + inline(p).replace(/\n/g, "<br>") + "</p>";
      }).join("");
    }).join("");
  }

  function buy(title) {
    return '<div class="sx-buy"><b>' + esc(title) + '</b><p>Labs is sold separately from the course. ' +
      '<a class="btn dark" href="' + ROOT + 'store.html#labs">Get Labs</a> <a class="btn" href="' + ROOT + 'store.html#redeem">I have a code</a>' +
      (access && access.me ? "" : ' <button class="btn" data-signin>Already bought it? Sign in</button>') + "</p></div>";
  }

  function bind(root) {
    root.querySelectorAll("[data-signin]").forEach(function (b) { b.addEventListener("click", signIn); });
    root.querySelectorAll("[data-copy]").forEach(function (b) {
      b.addEventListener("click", function () {
        var t = b.previousElementSibling.textContent;
        (navigator.clipboard ? navigator.clipboard.writeText(t) : Promise.reject()).then(function () {
          b.textContent = "Copied"; setTimeout(function () { b.textContent = "Copy"; }, 1500);
        }, function () {});
      });
    });
  }

  function index() {
    $("lb-index").hidden = false;
    $("lb-view").hidden = true;
    $("lb-access").innerHTML = access && access.labs ? '<p class="sx-ok">You have Labs. Everything on this page is open to you.</p>' : buy("Get Labs to open these");
    bind($("lb-access"));
    rpc("api_premium_list").then(function (d) {
      var items = d.items || [];
      $("lb-premium").innerHTML = items.length ? '<div class="lb-grid">' + items.map(function (i) {
        return '<a class="lb-card" href="?id=' + i.id + '"><small>' + (i.kind === "notebook" ? "Notebook" : "Lab") +
          (i.unit ? " · Unit " + i.unit : "") + (i.topic ? " · " + esc(i.topic) : "") + (i.published ? "" : " · draft") + "</small><b>" + esc(i.title) +
          "</b><span>" + esc(i.summary) + "</span></a>";
      }).join("") + "</div>" : '<p class="sx-empty">None yet.</p>';
    }).catch(function () { $("lb-premium").innerHTML = '<p class="sx-empty">Couldn\'t reach the course database.</p>'; });
  }

  function view(id) {
    $("lb-index").hidden = true;
    var box = $("lb-view");
    box.hidden = false;
    box.innerHTML = '<p class="sx-empty">Loading…</p>';
    rpc("api_premium_get", { p_id: +id }).then(function (d) {
      var back = '<p><a href="labs.html">&larr; All labs</a></p>';
      if (!d.ok) {
        box.innerHTML = back + "<h1>" + esc(d.title || "Lab") + "</h1>" + (d.summary ? '<p class="aa-sub">' + esc(d.summary) + "</p>" : "") +
          (d.locked ? buy("This " + (d.kind === "notebook" ? "notebook" : "lab") + " is part of Labs") : "<p>" + esc(d.error) + "</p>");
        bind(box);
        return;
      }
      var i = d.item, tool = TOOLS[i.tool];
      document.title = i.title + " · Labs";
      box.innerHTML = back + '<div class="cm-kicker">' + (i.kind === "notebook" ? "Notebook" : "Lab") + (i.unit ? " · Unit " + i.unit : "") +
        (i.topic ? " · " + esc(i.topic) : "") + "</div><h1>" + esc(i.title) + "</h1>" +
        (i.summary ? '<p class="aa-sub">' + esc(i.summary) + "</p>" : "") + '<p class="sx-act">' +
        (i.kind === "notebook" ? '<a class="btn dark" href="' + ROOT + "notebook.html?premium=" + i.id + '">Open the notebook</a> ' : "") +
        (tool ? '<a class="btn' + (i.kind === "notebook" ? "" : " dark") + '" href="' + ROOT + tool[1] + '" target="_blank" rel="noopener">' + tool[0] + "</a>" : "") +
        "</p>" + '<div class="lb-body">' + markup(i.body) + "</div>";
      bind(box);
    }).catch(function (e) { box.innerHTML = '<p class="sx-empty">' + esc(e.message) + "</p>"; });
  }

  function route() {
    var id = new URLSearchParams(location.search).get("id");
    if (id && /^\d+$/.test(id)) view(id); else index();
  }

  function start() {
    if (!$("lb-app")) return;
    rpc("api_my_access").then(function (a) { access = a; }, function () { access = null; }).then(route);
  }
  if (document.readyState === "complete") start();
  else global.addEventListener("load", start);
})(window);
