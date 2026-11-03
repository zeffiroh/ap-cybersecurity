(function (global) {
  "use strict";

  var DOW = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"];
  var me = document.currentScript && document.currentScript.src;
  var ROOT = me ? me.replace(/assets\/theme\/calendar\.js.*$/, "") : "";

  function esc(s) {
    return String(s == null ? "" : s).replace(/[&<>"]/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c];
    });
  }
  function ymd(d) {
    return d.getFullYear() + "-" + String(d.getMonth() + 1).padStart(2, "0") + "-" + String(d.getDate()).padStart(2, "0");
  }
  function parse(s) {
    var m = /^(\d{4})-(\d{2})-(\d{2})$/.exec(String(s || "").trim());
    return m ? new Date(+m[1], +m[2] - 1, +m[3]) : null;
  }
  function hm(d) { return d.toLocaleTimeString(undefined, { hour: "numeric", minute: "2-digit" }); }
  function addDays(d, n) { var x = new Date(d); x.setDate(x.getDate() + n); return x; }
  function monday(d) { var x = new Date(d.getFullYear(), d.getMonth(), d.getDate()); return addDays(x, -((x.getDay() + 6) % 7)); }

  function order() {
    var M = global.AAYAT_MAP;
    if (global.AAYAT_TEACH && global.AAYAT_TEACH.order) return global.AAYAT_TEACH.order;
    if (!M) return [];
    var out = [];
    M.units.forEach(function (u) { u.topics.forEach(function (t) { out = out.concat(M.topics[t].atoms); }); });
    return out;
  }

  function sessions(p, ord) {
    p = p || {};
    ord = ord || order();
    var per = Math.max(1, Math.min(6, Number(p.per) || 2)), out = [];
    for (var i = 0; i < ord.length; i += per) out.push({ n: out.length + 1, atoms: ord.slice(i, i + per), date: null });
    var start = parse(p.start), days = p.days && p.days.length ? p.days : [1, 2, 3, 4, 5], off = {};
    String(p.off || "").split(/[\s,]+/).forEach(function (s) { if (parse(s)) off[s] = 1; });
    if (start) {
      var d = new Date(start), k = 0, guard = 0;
      while (k < out.length && guard++ < 3000) {
        if (days.indexOf(d.getDay()) !== -1 && !off[ymd(d)]) out[k++].date = new Date(d);
        d.setDate(d.getDate() + 1);
      }
    }
    var t = /^(\d{1,2}):(\d{2})$/.exec(String(p.time || ""));
    out.forEach(function (s) {
      if (s.date && t) s.date.setHours(+t[1], +t[2], 0, 0);
      s.timed = !!(s.date && t);
      s.minutes = Math.max(15, Math.min(480, Number(p.minutes) || 60));
    });
    return out;
  }

  function classEvents(name, p, href) {
    var M = global.AAYAT_MAP || { atoms: {} };
    return sessions(p).filter(function (s) { return s.date; }).map(function (s) {
      return {
        start: s.date, minutes: s.timed ? s.minutes : 0, kind: "class", group: name,
        title: (name ? name + " · " : "") + "Class " + s.n,
        sub: s.atoms.map(function (a) { return a + (M.atoms[a] ? " " + M.atoms[a].title : ""); }).join(" · "),
        href: href ? href(s) : ""
      };
    });
  }

  function view(el, events, opts) {
    opts = opts || {};
    var key = "aayat_cal_view_" + (opts.id || "x");
    var state = { mode: opts.force || read(key) || opts.mode || "month", at: opts.at || new Date() };
    function read(k) { try { return localStorage.getItem(k); } catch (e) { return ""; } }
    function save(k, v) { try { localStorage.setItem(k, v); } catch (e) {  } }

    function byDay() {
      var m = {};
      events.forEach(function (e) { var k = ymd(e.start); (m[k] = m[k] || []).push(e); });
      Object.keys(m).forEach(function (k) { m[k].sort(function (a, b) { return a.start - b.start; }); });
      return m;
    }
    function chip(e, compact) {
      var t = e.minutes || e.kind === "due" ? hm(e.start) + " " : "";
      var inner = '<b>' + esc(t) + esc(e.title) + "</b>" + (compact ? "" : e.sub ? "<small>" + esc(e.sub) + "</small>" : "");
      return e.href ? '<a class="cal-ev cal-' + e.kind + '" href="' + esc(e.href) + '" title="' + esc(e.title + (e.sub ? "\n" + e.sub : "")) + '">' + inner + "</a>"
        : '<span class="cal-ev cal-' + e.kind + '" title="' + esc(e.title + (e.sub ? "\n" + e.sub : "")) + '">' + inner + "</span>";
    }

    function month(map) {
      var a = state.at, first = new Date(a.getFullYear(), a.getMonth(), 1), today = ymd(new Date()), h = [];
      var d = monday(first);
      h.push('<div class="cal-month">');
      [1, 2, 3, 4, 5, 6, 0].forEach(function (x) { h.push('<div class="cal-dow">' + DOW[x] + "</div>"); });
      for (var i = 0; i < 42; i++, d = addDays(d, 1)) {
        if (i === 35 && d.getMonth() !== a.getMonth()) break;
        var k = ymd(d), evs = map[k] || [];
        h.push('<div class="cal-day' + (d.getMonth() !== a.getMonth() ? " cal-out" : "") + (k === today ? " cal-today" : "") + '">' +
          '<span class="cal-d">' + d.getDate() + "</span>" + evs.slice(0, 4).map(function (e) { return chip(e, true); }).join("") +
          (evs.length > 4 ? '<span class="cal-more">+' + (evs.length - 4) + " more</span>" : "") + "</div>");
      }
      h.push("</div>");
      return { title: a.toLocaleDateString(undefined, { month: "long", year: "numeric" }), html: h.join("") };
    }

    function week(map) {
      var start = monday(state.at), days = [], today = ymd(new Date());
      for (var i = 0; i < 7; i++) days.push(addDays(start, i));
      var lo = 8, hi = 18;
      days.forEach(function (d) {
        (map[ymd(d)] || []).forEach(function (e) {
          if (!e.minutes && e.kind !== "due") return;
          lo = Math.min(lo, e.start.getHours());
          hi = Math.max(hi, e.start.getHours() + Math.ceil(((e.start.getMinutes() + (e.minutes || 30)) / 60)));
        });
      });
      hi = Math.min(24, hi);
      var hours = hi - lo, PX = 52, h = ['<div class="cal-week" style="--rows:' + hours + ';--px:' + PX + 'px">'];
      h.push('<div class="cal-corner"></div>');
      days.forEach(function (d) {
        h.push('<div class="cal-wh' + (ymd(d) === today ? " cal-today" : "") + '">' + DOW[d.getDay()] + " <b>" + d.getDate() + "</b></div>");
      });
      h.push('<div class="cal-allday-l">All day</div>');
      days.forEach(function (d) {
        h.push('<div class="cal-allday">' + (map[ymd(d)] || []).filter(function (e) { return !e.minutes && e.kind !== "due"; })
          .map(function (e) { return chip(e, true); }).join("") + "</div>");
      });
      h.push('<div class="cal-hours">');
      for (var t = lo; t < hi; t++) h.push('<div class="cal-hour">' + hm(new Date(2000, 0, 1, t)) + "</div>");
      h.push("</div>");
      days.forEach(function (d) {
        var k = ymd(d);
        h.push('<div class="cal-col' + (k === today ? " cal-today" : "") + '">');
        for (var r = 0; r < hours; r++) h.push('<div class="cal-slot"></div>');
        (map[k] || []).filter(function (e) { return e.minutes || e.kind === "due"; }).forEach(function (e) {
          var top = (e.start.getHours() - lo + e.start.getMinutes() / 60) * PX, len = Math.max(22, ((e.minutes || 30) / 60) * PX);
          h.push('<div class="cal-block" style="top:' + top + "px;height:" + len + 'px">' + chip(e) + "</div>");
        });
        if (k === today) {
          var now = new Date(), y = (now.getHours() - lo + now.getMinutes() / 60) * PX;
          if (y >= 0 && y <= hours * PX) h.push('<div class="cal-now" style="top:' + y + 'px"></div>');
        }
        h.push("</div>");
      });
      h.push("</div>");
      var end = days[6];
      return { title: days[0].toLocaleDateString(undefined, { day: "numeric", month: "short" }) + " – " +
        end.toLocaleDateString(undefined, { day: "numeric", month: "short", year: "numeric" }), html: h.join("") };
    }

    function agenda() {
      var from = new Date(); from.setHours(0, 0, 0, 0);
      var list = events.filter(function (e) { return e.start >= from; }).sort(function (a, b) { return a.start - b.start; }).slice(0, 60);
      var h = ['<div class="cal-agenda">'], last = "";
      list.forEach(function (e) {
        var k = ymd(e.start);
        if (k !== last) {
          h.push('<div class="cal-ag-day">' + e.start.toLocaleDateString(undefined, { weekday: "long", day: "numeric", month: "long" }) + "</div>");
          last = k;
        }
        h.push('<div class="cal-ag-row"><span class="cal-ag-t">' + (e.minutes || e.kind === "due" ? hm(e.start) : "All day") + "</span>" + chip(e) + "</div>");
      });
      if (!list.length) h.push('<p class="cal-empty">Nothing coming up.</p>');
      h.push("</div>");
      return { title: "Coming up", html: h.join("") };
    }

    function draw() {
      var map = byDay(), out = state.mode === "week" ? week(map) : state.mode === "agenda" ? agenda() : month(map);
      el.innerHTML = '<div class="cal-bar"><div class="cal-nav"><button class="btn" data-go="-1" aria-label="Previous">&lsaquo;</button>' +
        '<button class="btn" data-go="0">Today</button><button class="btn" data-go="1" aria-label="Next">&rsaquo;</button>' +
        '<span class="cal-title">' + esc(out.title) + '</span></div><div class="cal-modes">' +
        ["month", "week", "agenda"].map(function (m) {
          return '<button class="btn' + (state.mode === m ? " on" : "") + '" data-mode="' + m + '">' + m[0].toUpperCase() + m.slice(1) + "</button>";
        }).join("") + "</div></div>" + out.html +
        '<div class="cal-key"><span class="cal-ev cal-class"><b>Class</b></span><span class="cal-ev cal-due"><b>Due</b></span>' +
        '<span class="cal-ev cal-video"><b>Video</b></span></div>';
      el.querySelectorAll("[data-go]").forEach(function (b) {
        b.addEventListener("click", function () {
          var g = +b.getAttribute("data-go"), a = state.at;
          if (!g) state.at = new Date();
          else if (state.mode === "week") state.at = addDays(a, 7 * g);
          else state.at = new Date(a.getFullYear(), a.getMonth() + g, 1);
          draw();
        });
      });
      el.querySelectorAll("[data-mode]").forEach(function (b) {
        b.addEventListener("click", function () { state.mode = b.getAttribute("data-mode"); save(key, state.mode); draw(); });
      });
    }
    draw();
    return { set: function (evs) { events = evs; draw(); }, goTo: function (d) { state.at = d; draw(); } };
  }

  function feedEvents(feed, root) {
    var ev = [], url = function (p) { return p ? (/^https?:/.test(p) ? p : root + p) : ""; };
    (feed.groups || []).forEach(function (g) { ev = ev.concat(classEvents(g.name, g.schedule)); });
    if (!(feed.groups || []).length) ev = ev.concat(classEvents("", feed["default"]));
    (feed.classes || []).forEach(function (c) {
      if (!c.starts) return;
      ev.push({ start: new Date(c.starts), minutes: c.minutes, kind: "class", title: c.title + (c.seat === "pending" ? " (unpaid)" : ""),
                sub: c.seat === "confirmed" && c.meet ? "Meeting link on the Live classes page" : "Live class " + c.code,
                href: root + "classes.html" });
    });
    (feed.assignments || []).forEach(function (a) {
      if (!a.due) return;
      ev.push({ start: new Date(a.due), minutes: 0, kind: "due", title: "Due: " + a.title + (a.done ? " ✓" : ""), sub: a.note, href: url(a.href) });
    });
    (feed.videos || []).forEach(function (v) {
      ev.push({ start: new Date(v.created), minutes: 0, kind: "video", title: "Video: " + v.title, sub: v.note, href: root + "videos.html#v" + v.id });
    });
    return ev;
  }

  function studentPage() {
    var el = document.getElementById("cal");
    if (!el) return;
    var root = ROOT;
    var at = parse(new URLSearchParams(location.search).get("at"));
    var cal = view(el, [], { id: "student", force: at ? "week" : "", at: at });
    var P = global.AayatProgress;
    (P ? P.neon() : Promise.resolve(null)).then(function (db) {
      return db ? db.rpc("api_my_feed", {}, { attempts: 1 }) : null;
    }).then(function (f) {
      if (!f) return;
      cal.set(feedEvents(f, root));
      var who = document.getElementById("cal-who");
      if (who) who.textContent = f.me ? (f.groups.length ? "Your class: " + f.groups.map(function (g) { return g.name; }).join(", ")
        : "The whole-course timetable") : "Sign in to see your own class and what's due.";
      var box = document.getElementById("cal-due");
      if (box) {
        var open = (f.assignments || []).filter(function (a) { return !a.done; });
        box.innerHTML = open.length ? '<ul class="cal-list">' + open.map(function (a) {
          return "<li>" + (a.href ? '<a href="' + esc(/^https?:/.test(a.href) ? a.href : root + a.href) + '">' + esc(a.title) + "</a>" : esc(a.title)) +
            (a.due ? " <small>due " + new Date(a.due).toLocaleString(undefined, { weekday: "short", day: "numeric", month: "short", hour: "numeric", minute: "2-digit" }) + "</small>" : "") +
            (a.note ? "<br><small>" + esc(a.note) + "</small>" : "") + "</li>";
        }).join("") + "</ul>" : '<p class="cal-empty">' + (f.me ? "Nothing assigned right now." : "Sign in to see your assignments.") + "</p>";
      }
    }).catch(function () {  });
  }

  global.AayatCal = { root: ROOT, sessions: sessions, classEvents: classEvents, feedEvents: feedEvents, view: view, ymd: ymd, parse: parse };
  if (document.readyState === "complete") studentPage();
  else global.addEventListener("load", studentPage);
})(window);
