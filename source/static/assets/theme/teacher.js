(function (global) {
  "use strict";

  var me = document.currentScript && document.currentScript.src;
  var ROOT = me ? me.replace(/assets\/theme\/teacher\.js.*$/, "") : "../";
  var T = global.AAYAT_TEACH || { order: [], atoms: {}, topics: {}, decks: [] };
  var DOW = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"];
  var $ = function (id) { return document.getElementById(id); };

  function esc(s) {
    return String(s == null ? "" : s).replace(/[&<>"]/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c];
    });
  }
  function url(p) { return p ? ROOT + p : ""; }
  function abs(p) { return new URL(url(p), location.href).href; }
  function rpc(fn, args) {
    var P = global.AayatProgress;
    return (P ? P.neon() : Promise.resolve(null)).then(function (db) {
      if (!db) throw new Error("The course database is not connected yet.");
      return db.rpc(fn, args || {}, { attempts: 1 });
    });
  }
  function ago(iso) {
    if (!iso) return "&ndash;";
    var m = Math.round((Date.now() - new Date(iso)) / 60000);
    if (m < 1) return "just now";
    if (m < 60) return m + " min ago";
    if (m < 1440) return Math.round(m / 60) + " h ago";
    return new Date(iso).toLocaleDateString(undefined, { month: "short", day: "numeric" });
  }
  function copy(text, note) {
    var done = function () { if (note) { note.textContent = "Copied."; setTimeout(function () { note.textContent = ""; }, 1800); } };
    if (navigator.clipboard) return navigator.clipboard.writeText(text).then(done, function () { fallback(text); done(); });
    fallback(text); done();
  }
  function fallback(text) {
    var t = document.createElement("textarea");
    t.value = text; document.body.appendChild(t); t.select();
    try { document.execCommand("copy"); } catch (e) {  }
    t.remove();
  }
  function body(html) {
    return String(html || "").replace(/^\s*<h2[^>]*>[\s\S]*?<\/h2>/, "");
  }
  function plain(html) {
    var d = document.createElement("div");
    d.innerHTML = html.replace(/<\/(p|li|h\d)>/g, "\n").replace(/<li>/g, "- ");
    return d.textContent.replace(/\n{3,}/g, "\n\n").trim();
  }

  function spark(values, cls) {
    var vs = values.map(function (v) { return v == null ? null : Number(v); });
    var real = vs.filter(function (v) { return v != null; });
    var w = 100, h = 30, max = Math.max.apply(null, real.concat([1])), n = vs.length;
    var pts = [];
    vs.forEach(function (v, i) {
      if (v == null) return;
      pts.push([n > 1 ? (i / (n - 1)) * w : w / 2, h - (v / max) * (h - 3) - 1.5]);
    });
    if (!pts.length) return '<svg class="tc-spark ' + (cls || "") + '" viewBox="0 0 100 30" preserveAspectRatio="none"></svg>';
    var line = pts.map(function (p, i) { return (i ? "L" : "M") + p[0].toFixed(2) + " " + p[1].toFixed(2); }).join("");
    var area = line + "L" + pts[pts.length - 1][0].toFixed(2) + " " + h + "L" + pts[0][0].toFixed(2) + " " + h + "Z";
    return '<svg class="tc-spark ' + (cls || "") + '" viewBox="0 0 100 30" preserveAspectRatio="none" aria-hidden="true">' +
      '<path class="a" d="' + area + '"/><path class="l" d="' + line + '"/></svg>';
  }

  function ymd(d) { return global.AayatCal.ymd(d); }
  function nice(d) {
    return d ? d.toLocaleDateString(undefined, { weekday: "short", day: "numeric", month: "short" }) : "";
  }
  function hm(d) { return d.toLocaleTimeString(undefined, { hour: "numeric", minute: "2-digit" }); }
  function local(iso) {
    if (!iso) return "";
    var d = new Date(iso);
    return new Date(d.getTime() - d.getTimezoneOffset() * 60000).toISOString().slice(0, 16);
  }

  var plans = null;
  function loadPlans() {
    if (plans) return Promise.resolve(plans);
    return rpc("api_teacher_groups").then(function (r) {
      plans = [{ id: "", name: "Everyone", schedule: r["default"] || {}, members: [] }].concat((r.groups || []).map(function (g) {
        return { id: String(g.id), name: g.name, schedule: g.schedule || {}, members: g.members || [] };
      }));
      return plans;
    }, function () { plans = [{ id: "", name: "Everyone", schedule: {}, members: [] }]; return plans; });
  }
  function groupOptions(withAll) {
    return (withAll ? '<option value="*">All groups</option>' : "") + (plans || []).map(function (g) {
      return '<option value="' + esc(g.id) + '">' + esc(g.name) + (g.id ? " (" + g.members.length + ")" : "") + "</option>";
    }).join("");
  }
  function sessions(p) { return global.AayatCal.sessions(p, T.order); }
  function upcoming(list) {
    var now = Date.now() - 2 * 3600000;
    for (var i = 0; i < list.length; i++) if (list[i].date && list[i].date.getTime() >= now) return list[i];
    return list[0];
  }
  function label(s, name) {
    return (name ? name + " · " : "") + "Class " + s.n + (s.date ? " · " + nice(s.date) + (s.timed ? " " + hm(s.date) : "") : "");
  }
  function topicOptions(blank) {
    var units = {};
    Object.keys(T.topics).forEach(function (t) { (units[T.topics[t].unit] = units[T.topics[t].unit] || []).push(t); });
    return (blank ? '<option value="">' + blank + "</option>" : "") + Object.keys(units).sort().map(function (u) {
      return '<optgroup label="Unit ' + u + '">' + units[u].map(function (t) {
        return '<option value="' + t + '">' + esc(t + " " + T.topics[t].title) + "</option>";
      }).join("") + "</optgroup>";
    }).join("");
  }
  function atomOptions(blank) {
    return (blank ? '<option value="">' + blank + "</option>" : "") + Object.keys(T.topics).map(function (t) {
      return '<optgroup label="' + esc(t + " " + T.topics[t].title) + '">' + T.order.filter(function (a) { return T.atoms[a].topic === t; })
        .map(function (a) { return '<option value="' + a + '">' + esc(a + " " + T.atoms[a].title) + "</option>"; }).join("") + "</optgroup>";
    }).join("");
  }

  function atomName(id) {
    var a = T.atoms[id];
    return a ? id + " " + a.title : id;
  }
  function whatOpen(o) {
    var a = T.atoms[o.ref], t = T.topics[o.ref] || T.topics[o.topic];
    return esc(o.kind) + " &middot; " + esc(a ? o.ref + " " + a.title : t ? (o.topic || o.ref) + " " + t.title : o.ref);
  }

  function dashboard() {
    var P = global.AayatProgress, POSTS = global.AAYAT_POSTS || [];
    function load() {
      $("status").textContent = "Loading…";
      Promise.all([rpc("api_teacher_dashboard"), rpc("api_class_progress").catch(function () { return null; }), loadPlans(),
        rpc("api_teacher_classes").catch(function () { return null; }), rpc("api_teacher_assignments").catch(function () { return []; })])
        .then(function (r) {
          var d = r[0], prog = r[1], cls = r[3], asg = r[4], days = d.days || [], me = global.Identity && global.Identity.getEmail();
          var last = days[days.length - 1] || {}, scored = days.filter(function (x) { return x.pct != null; });
          var avg = scored.length ? Math.round(scored.reduce(function (s, x) { return s + Number(x.pct); }, 0) / scored.length) : null;
          var sum = function (k, n) { return days.slice(-n).reduce(function (s, x) { return s + Number(x[k] || 0); }, 0); };
          var kpi = function (k, v, s, vals) {
            return '<div class="tc-kpi"><div class="k">' + k + '</div><div class="v">' + v + '</div><div class="s">' + s + "</div>" +
              spark(vals) + "</div>";
          };
          $("kpis").innerHTML =
            kpi("Students", d.students, d.activeWeek + " active in the last 7 days", days.map(function (x) { return x.active; })) +
            kpi("Active today", last.active || 0, "students who opened something", days.map(function (x) { return x.active; })) +
            kpi("Opens", sum("opens", 7), "lessons, sims and quizzes this week", days.map(function (x) { return x.opens; })) +
            kpi("Quiz answers", sum("submissions", 7), "this week · " + d.pendingTickets + " exit tickets to grade",
              days.map(function (x) { return x.submissions; })) +
            kpi("Average score", avg == null ? "&ndash;" : avg + "%", "last 30 days", days.map(function (x) { return x.pct; }));

          var best = null;
          plans.forEach(function (g) {
            var n = upcoming(sessions(g.schedule));
            if (n && n.date && (!best || n.date < best.s.date)) best = { s: n, g: g };
          });
          if (!best) best = { s: sessions(plans[0].schedule)[0], g: plans[0] };
          var next = best.s, today = next.date && ymd(next.date) === ymd(new Date());
          $("next").innerHTML = "<h3>" + (today ? "Today's class" : "Next class") + ' <a class="tc-more" href="schedule.html">Calendar</a></h3>' +
            '<div class="tc-kicker">' + esc(label(next, best.g.id ? best.g.name : "")) + "</div>" +
            '<div class="big">' + esc(T.topics[T.atoms[next.atoms[0]].topic].title) + "</div><ol>" +
            next.atoms.map(function (a) { return "<li>" + esc(atomName(a)) + "</li>"; }).join("") + "</ol>" +
            '<div class="tc-btns"><a class="btn dark" href="teach.html?s=' + next.n + (best.g.id ? "&g=" + best.g.id : "") + '">Start class</a>' +
            '<a class="btn" href="blog.html?q=' + encodeURIComponent(next.atoms[0]) + '">Class posts</a></div>' +
            (next.date ? "" : '<p class="tc-note">No dates yet. <a href="schedule.html">Set a timetable</a> to plan the term.</p>');

          $("online").innerHTML = d.online.length ? '<ul class="tc-people">' + d.online.map(function (o) {
            return "<li><span>" + esc(o.email) + "<br><small>" + whatOpen(o) + "</small></span><small>" + ago(o.at) + "</small></li>";
          }).join("") + "</ul>" : '<p class="tc-empty">Nobody in the last 15 minutes.</p>';

          var soon = cls ? cls.classes.filter(function (c) { return c.starts && new Date(c.starts).getTime() > Date.now() - c.minutes * 60000; })
            .sort(function (a, b) { return a.starts < b.starts ? -1 : 1; }).slice(0, 4) : [];
          var open = cls ? cls.requests.filter(function (q) { return q.status === "open"; }).length : 0;
          $("liveclasses").innerHTML = (soon.length ? '<ul class="tc-people">' + soon.map(function (c) {
            return "<li><span>" + esc(c.title) + "<br><small>" + esc(new Date(c.starts).toLocaleString(undefined, { weekday: "short", day: "numeric", month: "short", hour: "numeric", minute: "2-digit" })) +
              " · " + c.seats.length + " booked</small></span>" + (c.meet ? '<a class="btn" href="' + esc(c.meet) + '" target="_blank" rel="noopener">Open</a>' : "") + "</li>";
          }).join("") + "</ul>" : '<p class="tc-empty">No live classes booked.</p>') +
            (open ? '<p><a class="btn dark" href="classes.html">' + open + " class request" + (open === 1 ? "" : "s") + " waiting</a></p>" : "");

          var due = (asg || []).filter(function (a) { return a.due && new Date(a.due).getTime() > Date.now() - 3 * 864e5; })
            .sort(function (a, b) { return a.due < b.due ? -1 : 1; }).slice(0, 5);
          $("due").innerHTML = due.length ? due.map(function (a) {
            var pct = a.students ? Math.round(a.done.length / a.students * 100) : 0;
            return '<div class="tc-bar"><span>' + esc(a.title) + "<br><small class='tc-note'>due " + nice(new Date(a.due)) + "</small></span>" +
              '<span class="t"><i style="width:' + pct + '%"></i></span><span class="n">' + a.done.length + "/" + a.students + "</span></div>";
          }).join("") : '<p class="tc-empty">Nothing due. <a href="assignments.html">Assign something</a>.</p>';

          var recs = prog ? Object.keys(prog.students).filter(function (e) { return e !== me; })
            .map(function (e) { return P.mastery(prog.students[e]); }) : [];
          var M = global.AAYAT_MAP || { units: [] };
          $("units").innerHTML = recs.length ? M.units.map(function (u) {
            var pct = Math.round(recs.reduce(function (s, m) { return s + m.units[u.n].pct; }, 0) / recs.length);
            return '<div class="tc-bar"><span>Unit ' + u.n + " " + esc(u.title) + '</span><span class="t"><i style="width:' + pct +
              '%"></i></span><span class="n">' + pct + "%</span></div>";
          }).join("") + '<p class="tc-note">Average across ' + recs.length + " student" + (recs.length === 1 ? "" : "s") + ".</p>"
            : '<p class="tc-empty">No progress yet.</p>';

          var posts = POSTS.filter(function (p) { return next.atoms.indexOf(p.id) !== -1; });
          $("posts").innerHTML = posts.length ? '<ul class="tc-people">' + posts.map(function (p) {
            return '<li><span><a href="' + esc(p.href) + '">' + (p.kind === "pre" ? "Pre" : "Post") + "-lecture: " + esc(p.id) +
              "</a><br><small>" + esc(p.title) + "</small></span></li>";
          }).join("") + "</ul>" : '<p class="tc-empty">No posts.</p>';

          var rows = Object.keys(d.sparks).map(function (e) {
            var rec = prog && prog.students[e];
            return { email: e, spark: d.sparks[e], ms: rec ? P.mastery(rec).course : 0, last: rec ? rec.last : "" };
          }).sort(function (a, b) { return (b.last || "") < (a.last || "") ? -1 : 1; });
          $("roster").innerHTML = rows.length ? '<table class="tc-table"><tr><th>Student</th><th>Last 14 days</th><th>Course</th><th>Last active</th></tr>' +
            rows.map(function (r) {
              return "<tr><td>" + esc(r.email) + "</td><td>" + spark(r.spark, "tc-mini") + "</td><td>" + r.ms + "%</td><td>" + ago(r.last) + "</td></tr>";
            }).join("") + "</table>" : '<p class="tc-empty">No student activity yet.</p>';
          $("status").textContent = "Updated " + new Date(d.generatedAt).toLocaleTimeString();
        }).catch(function (e) { $("status").textContent = "Could not load: " + e.message; });
    }
    $("reload").addEventListener("click", function () { plans = null; load(); });
    load();
    setInterval(function () { if (!document.hidden) load(); }, 60000);
  }

  function teach() {
    var q = new URLSearchParams(location.search), list = [], cur = null, tab = "", poll = null, group = { id: "" };
    var timer = { left: 0, end: 0, run: false, h: null };

    function pickInitial() {
      var s = Number(q.get("s")), topic = q.get("topic");
      if (s && list[s - 1]) return list[s - 1];
      if (topic) for (var i = 0; i < list.length; i++)
        if (list[i].atoms.some(function (a) { return T.atoms[a].topic === topic; })) return list[i];
      return upcoming(list);
    }

    function tabs() {
      var out = [], seen = {};
      cur.atoms.forEach(function (aid) {
        var a = T.atoms[aid], t = T.topics[a.topic];
        if (!seen[a.topic] && t.slides) { seen[a.topic] = 1; out.push(["Topic " + a.topic + " slides", t.slides]); }
      });
      cur.atoms.forEach(function (aid) {
        var a = T.atoms[aid];
        [["lesson", "Lesson"], ["sim", "Sim"], ["code", "Code"], ["quiz", "Quiz"]].forEach(function (k) {
          if (a[k[0]]) out.push([aid + " " + k[1], a[k[0]]]);
        });
      });
      return out;
    }

    function show(path) {
      tab = path;
      $("frame").src = url(path);
      $("open").href = url(path);
      $("tabs").querySelectorAll("button").forEach(function (b) { b.classList.toggle("on", b.getAttribute("data-p") === path); });
    }

    function render() {
      var a0 = T.atoms[cur.atoms[0]], t0 = T.topics[a0.topic];
      $("when").textContent = label(cur, group.id ? group.name : "") + " of " + list.length;
      $("title").textContent = a0.topic + " " + t0.title;
      $("skills").textContent = cur.atoms.map(atomName).join("  ·  ");
      $("pick").value = String(cur.n);
      $("prev").disabled = cur.n <= 1;
      $("next").disabled = cur.n >= list.length;
      var ts = tabs();
      $("tabs").innerHTML = ts.map(function (t) { return '<button data-p="' + esc(t[1]) + '">' + esc(t[0]) + "</button>"; }).join("");
      $("tabs").querySelectorAll("button").forEach(function (b) { b.addEventListener("click", function () { show(b.getAttribute("data-p")); }); });
      if (ts.length) show(ts[0][1]);

      var POSTS = global.AAYAT_POSTS || [];
      var share = [];
      cur.atoms.forEach(function (aid) {
        var a = T.atoms[aid];
        [["lesson", "Lesson"], ["sim", "Sim"], ["quiz", "Quiz"], ["code", "Code"]].forEach(function (k) {
          if (a[k[0]]) share.push([aid + " " + k[1], abs(a[k[0]])]);
        });
        POSTS.filter(function (p) { return p.id === aid; }).forEach(function (p) {
          share.push([aid + (p.kind === "pre" ? " pre-lecture post" : " recap post"),
            atomName(aid) + "\n\n" + plain(body(p.html)) + (a.lesson ? "\n\nLesson: " + abs(a.lesson) : "")]);
        });
      });
      $("share").innerHTML = share.map(function (s, i) {
        return '<div class="tc-share"><span>' + esc(s[0]) + '</span><button class="btn" data-i="' + i + '">Copy</button></div>';
      }).join("");
      $("share").querySelectorAll("button").forEach(function (b) {
        b.addEventListener("click", function () { copy(share[+b.getAttribute("data-i")][1], $("copied")); });
      });

      var priv = [];
      var seenT = {};
      cur.atoms.forEach(function (aid) {
        var a = T.atoms[aid], t = T.topics[a.topic];
        if (!seenT[a.topic]) {
          seenT[a.topic] = 1;
          [["Topic " + a.topic + " teacher page", t.page], ["Quiz key", t.quizKey], ["Assignment key", t.assignKey],
           ["Activity keys", t.activityKeys], ["PowerPoint", t.ppt]].forEach(function (x) { if (x[1]) priv.push(x); });
        }
        [[aid + " solution", a.solution], [aid + " assignment page", a.assign], [aid + " pre handout", a.preDoc],
         [aid + " recap handout", a.postDoc]].forEach(function (x) { if (x[1]) priv.push(x); });
      });
      $("private").innerHTML = '<ul class="tc-people">' + priv.map(function (x) {
        return '<li><a href="' + esc(url(x[1])) + '" target="_blank" rel="noopener">' + esc(x[0]) + "</a></li>";
      }).join("") + "</ul>";
      live();
    }

    function live() {
      clearTimeout(poll);
      var topic = T.atoms[cur.atoms[0]].topic;
      rpc("api_teacher_live", { p_topic: topic }).then(function (d) {
        var h = "<p class='tc-note'>Online now (" + d.online.length + ")</p>";
        h += d.online.length ? '<ul class="tc-people">' + d.online.map(function (o) {
          return "<li><span>" + esc(o.email) + "<br><small>" + whatOpen(o) + "</small></span><small>" + ago(o.at) + "</small></li>";
        }).join("") + "</ul>" : '<p class="tc-empty">Nobody yet.</p>';
        h += "<p class='tc-note'>Topic " + esc(topic) + " answers today</p>";
        h += d.results.length ? '<ul class="tc-people">' + d.results.map(function (r) {
          var pct = r.max ? Math.round(r.points / r.max * 100) : 0;
          return "<li><span>" + esc(r.email) + "<br><small>" + r.n + " answered</small></span><b>" + pct + "%</b></li>";
        }).join("") + "</ul>" : '<p class="tc-empty">No answers yet.</p>';
        $("live").innerHTML = h;
      }).catch(function (e) { $("live").textContent = "Could not load: " + e.message; })
        .then(function () { poll = setTimeout(function () { if (!document.hidden) live(); else poll = setTimeout(live, 5000); }, 20000); });
    }

    function go(n) {
      if (!list[n - 1]) return;
      cur = list[n - 1];
      history.replaceState(null, "", "?s=" + n + (group.id ? "&g=" + group.id : ""));
      render();
    }

    function tick() {
      var left = timer.run ? Math.max(0, Math.round((timer.end - Date.now()) / 1000)) : timer.left;
      $("timer").textContent = String(Math.floor(left / 60)).padStart(2, "0") + ":" + String(left % 60).padStart(2, "0");
      $("timer").classList.toggle("done", timer.run && left === 0);
      if (timer.run && left === 0) { timer.run = false; timer.left = 0; }
    }
    function timerUi() {
      var b = [[1, "1 min"], [3, "3"], [5, "5"], [10, "10"], [15, "15"]].map(function (x) {
        return '<button class="btn" data-m="' + x[0] + '">' + x[1] + "</button>";
      }).join("") + '<button class="btn dark" id="tgo">Start</button><button class="btn" id="treset">Reset</button>';
      $("timer-btns").innerHTML = b;
      $("timer-btns").querySelectorAll("[data-m]").forEach(function (el) {
        el.addEventListener("click", function () {
          timer.left = +el.getAttribute("data-m") * 60; timer.end = Date.now() + timer.left * 1000; timer.run = true;
          $("tgo").textContent = "Pause"; tick();
        });
      });
      $("tgo").addEventListener("click", function () {
        if (timer.run) { timer.left = Math.max(0, Math.round((timer.end - Date.now()) / 1000)); timer.run = false; $("tgo").textContent = "Start"; }
        else if (timer.left > 0) { timer.end = Date.now() + timer.left * 1000; timer.run = true; $("tgo").textContent = "Pause"; }
        tick();
      });
      $("treset").addEventListener("click", function () { timer.run = false; timer.left = 0; $("tgo").textContent = "Start"; tick(); });
      timer.h = setInterval(tick, 250);
    }

    function useGroup(id) {
      group = plans.filter(function (g) { return g.id === id; })[0] || plans[0];
      list = sessions(group.schedule);
      $("pick").innerHTML = list.map(function (s) {
        return '<option value="' + s.n + '">' + esc(label(s) + " · " + s.atoms.join(", ")) + "</option>";
      }).join("");
    }

    loadPlans().then(function () {
      $("grp").innerHTML = groupOptions(false);
      $("grp").value = q.get("g") || "";
      useGroup($("grp").value);
      $("grp").addEventListener("change", function () { useGroup($("grp").value); cur = upcoming(list); go(cur.n); });
      $("pick").addEventListener("change", function () { go(+$("pick").value); });
      $("prev").addEventListener("click", function () { go(cur.n - 1); });
      $("next").addEventListener("click", function () { go(cur.n + 1); });
      cur = pickInitial();
      timerUi();
      render();
    });
  }

  function schedule() {
    var cal = null, classes = [], asg = [], q = new URLSearchParams(location.search);
    function plan() { return plans.filter(function (g) { return g.id === $("plan-for").value; })[0] || plans[0]; }
    function form() {
      var p = plan().schedule || {};
      $("start").value = p.start || "";
      $("time").value = p.time || "";
      $("minutes").value = p.minutes || 60;
      $("per").value = p.per || 2;
      $("off").value = p.off || "";
      var days = p.days && p.days.length ? p.days : [1, 2, 3, 4, 5];
      $("days").innerHTML = "<legend>Class days</legend>" + [1, 2, 3, 4, 5, 6, 0].map(function (d) {
        return '<label><input type="checkbox" value="' + d + '"' + (days.indexOf(d) !== -1 ? " checked" : "") + "> " + DOW[d] + "</label>";
      }).join("");
    }
    function read() {
      return {
        start: $("start").value, time: $("time").value, minutes: Math.max(15, Math.min(480, Number($("minutes").value) || 60)),
        per: Math.max(1, Math.min(6, Number($("per").value) || 2)), off: $("off").value.trim(),
        days: Array.prototype.map.call($("days").querySelectorAll("input:checked"), function (i) { return +i.value; })
      };
    }
    function events() {
      var show = $("show").value, ev = [];
      plans.forEach(function (g) {
        if (show !== "*" && show !== g.id) return;
        ev = ev.concat(global.AayatCal.classEvents(g.id ? g.name : "Everyone", g.schedule, function (s) {
          return "teach.html?s=" + s.n + (g.id ? "&g=" + g.id : "");
        }));
      });
      classes.forEach(function (c) {
        if (c.starts && c.status !== "cancelled") ev.push({ start: new Date(c.starts), minutes: c.minutes, kind: "class",
          title: "Live: " + c.title, sub: c.seats.length + " booked", href: "classes.html#c" + c.id });
      });
      asg.forEach(function (a) {
        if (!a.due || (show !== "*" && String(a.group || "") !== show && a.group)) return;
        ev.push({ start: new Date(a.due), minutes: 0, kind: "due", title: "Due: " + a.title, sub: a.done.length + "/" + a.students + " done",
          href: "assignments.html" });
      });
      return ev;
    }
    function draw() {
      var ev = events();
      if (!cal) cal = global.AayatCal.view($("tcal"), ev, { id: "teacher", mode: "week" });
      else cal.set(ev);
      var n = sessions(plan().schedule).filter(function (s) { return s.date; });
      $("status").textContent = n.length ? plan().name + ": " + n.length + " classes, " + nice(n[0].date) + " to " + nice(n[n.length - 1].date)
        : plan().name + ": pick a first class date to put the classes on the calendar.";
    }
    Promise.all([loadPlans(), rpc("api_teacher_classes").catch(function () { return { classes: [] }; }),
      rpc("api_teacher_assignments").catch(function () { return []; })]).then(function (r) {
      classes = r[1].classes || [];
      asg = r[2] || [];
      $("show").innerHTML = groupOptions(true);
      $("plan-for").innerHTML = groupOptions(false);
      if (q.get("g")) { $("plan-for").value = q.get("g"); $("show").value = q.get("g"); }
      else $("show").value = "*";
      form(); draw();
      $("show").addEventListener("change", draw);
      $("plan-for").addEventListener("change", function () { form(); draw(); });
      $("save").addEventListener("click", function () {
        var g = plan(), p = read();
        $("saved").textContent = "Saving…";
        (g.id ? rpc("api_teacher_save_group", { p: { id: +g.id, schedule: p } }) : rpc("api_teacher_set_schedule", { p: p })).then(function (r) {
          if (!r || !r.ok) throw new Error((r && r.error) || "That didn't work.");
          g.schedule = p;
          $("saved").textContent = "Saved. Students in " + g.name + " see it on their calendar.";
          draw();
        }).catch(function (e) { $("saved").textContent = e.message; });
      });
    });
  }

  function blog() {
    var POSTS = global.AAYAT_POSTS || [], shown = 15, q = new URLSearchParams(location.search);
    var units = {};
    Object.keys(T.topics).forEach(function (t) { units[T.topics[t].unit] = 1; });
    $("unit").innerHTML = '<option value="">All units</option>' + Object.keys(units).sort().map(function (u) {
      return '<option value="' + u + '">Unit ' + u + "</option>";
    }).join("");
    if (q.get("q")) $("q").value = q.get("q");
    function match() {
      var u = $("unit").value, k = $("kind").value, s = $("q").value.trim().toLowerCase();
      return POSTS.filter(function (p) {
        var t = T.topics[p.topic];
        return (!u || (t && String(t.unit) === u)) && (!k || p.kind === k) &&
          (!s || (p.id + " " + p.title + " " + p.html).toLowerCase().indexOf(s) !== -1);
      });
    }
    function draw() {
      var list = match(), groups = [], at = {};
      list.forEach(function (p) {
        if (!at[p.id]) { at[p.id] = { id: p.id, title: p.title, topic: p.topic, posts: {} }; groups.push(at[p.id]); }
        at[p.id].posts[p.kind] = p;
      });
      var lastUnit = null, total = POSTS.length / 2;
      function half(p, kind) {
        if (!p) return '<section class="bl-post bl-missing"><div class="bl-kind">' + (kind === "pre" ? "Before class" : "After class") + "</div><p class=\"tc-note\">Hidden by the filter.</p></section>";
        var i = list.indexOf(p);
        return '<section class="bl-post"><div class="bl-kind ' + kind + '">' + (kind === "pre" ? "Before class" : "After class") + "</div>" +
          '<div class="bl-body clip">' + body(p.html) + "</div>" +
          '<div class="bl-acts"><a class="btn" href="' + esc(p.href) + '">Open</a><button class="btn" data-more>Read here</button>' +
          '<button class="btn" data-copy="' + i + '">Copy text</button><button class="btn" data-link="' + i + '">Copy link</button><span class="tc-note"></span></div></section>';
      }
      $("bl-count").textContent = groups.length === total ? total + " lessons, 2 posts each" : groups.length + " of " + total + " lessons";
      $("blog").innerHTML = groups.slice(0, shown).map(function (g) {
        var t = T.topics[g.topic], head = "";
        if (t && t.unit !== lastUnit) { lastUnit = t.unit; head = '<h2 class="bl-unit"><span>Unit ' + t.unit + "</span></h2>"; }
        var k = $("kind").value;
        return head + '<article class="bl-card"><header class="bl-head"><div class="bl-id">' + esc(g.id) + "</div>" +
          '<div class="bl-titles"><div class="bl-topic">' + (t ? esc(g.topic + " " + t.title) : esc(g.topic)) + "</div><h3>" + esc(g.title) + "</h3></div>" +
          '<a class="btn" href="teach.html?topic=' + esc(g.topic) + '">Teach this</a></header>' +
          '<div class="bl-cols' + (k ? " one" : "") + '">' + (k === "post" ? "" : half(g.posts.pre, "pre")) + (k === "pre" ? "" : half(g.posts.post, "post")) + "</div></article>";
      }).join("") + (groups.length > shown ? '<p class="bl-moreRow"><button class="btn" id="more">Show more lessons (' + (groups.length - shown) + ")</button></p>" : "") +
        (groups.length ? "" : '<p class="tc-empty">No posts match.</p>');
      $("blog").querySelectorAll("[data-more]").forEach(function (b) {
        b.addEventListener("click", function () {
          var el = b.closest(".bl-post").querySelector(".bl-body");
          el.classList.toggle("clip");
          b.textContent = el.classList.contains("clip") ? "Read here" : "Show less";
        });
      });
      $("blog").querySelectorAll("[data-copy]").forEach(function (b) {
        b.addEventListener("click", function () {
          var p = list[+b.getAttribute("data-copy")], a = T.atoms[p.id];
          copy(atomName(p.id) + "\n\n" + plain(body(p.html)) + (a && a.lesson ? "\n\nLesson: " + abs(a.lesson) : ""), b.parentNode.querySelector(".tc-note"));
        });
      });
      $("blog").querySelectorAll("[data-link]").forEach(function (b) {
        b.addEventListener("click", function () {
          copy(new URL(list[+b.getAttribute("data-link")].href, location.href).href, b.parentNode.querySelector(".tc-note"));
        });
      });
      var more = $("more");
      if (more) more.addEventListener("click", function () { shown += 15; draw(); });
    }
    ["unit", "kind"].forEach(function (id) { $(id).addEventListener("change", function () { shown = 15; draw(); }); });
    $("q").addEventListener("input", function () { shown = 15; draw(); });
    draw();
  }

  function resources() {
    var box = $("q");
    if (!box) return;
    box.addEventListener("input", function () {
      var s = box.value.trim().toLowerCase();
      document.querySelectorAll(".tc-topic").forEach(function (c) {
        var hit = !s || c.textContent.toLowerCase().indexOf(s) !== -1;
        c.style.display = hit ? "" : "none";
        if (hit && s) c.querySelector("details").open = true;
      });
      document.querySelectorAll(".tc-unit").forEach(function (u) { if (s) u.open = true; });
    });
  }

  function gate(el) {
    return rpc("api_whoami").then(function (r) {
      if (r && r.teacher) return true;
      var box = document.createElement("div");
      box.className = "tc-card";
      box.innerHTML = "<h3>Teachers only</h3><p>Sign in with a teacher account to see your class here.</p>" +
        '<div class="tc-btns"><button class="btn dark" id="tc-signin">Sign in</button></div>' +
        '<p class="tc-note">Or use a teacher key: <input id="tc-keyin" type="password" autocomplete="off"> <button class="btn" id="tc-key">Use key</button></p>';
      Array.prototype.forEach.call(el.children, function (c) { if (!c.classList.contains("tc-head")) c.style.display = "none"; });
      el.insertBefore(box, el.firstChild);
      $("tc-signin").addEventListener("click", function () {
        if (global.Identity) global.Identity.open({}, function () { location.reload(); });
      });
      $("tc-key").addEventListener("click", function () {
        var k = $("tc-keyin").value.trim();
        if (!k) return;
        try { localStorage.setItem("apcyber_teacher_key", k); } catch (e) {  }
        location.reload();
      });
      return false;
    }, function () { return true; });
  }

  function teamUrl(u, t) { return /^https:\/\/meet\.jit\.si\//.test(u) ? u.replace(/[?#].*$/, "") + "-team" + t : u; }

  function live() {
    var data = { classes: [], requests: [] }, editing = null, armed = "";
    $("c-topic").innerHTML = topicOptions("No topic");
    function fill(c, req) {
      editing = c ? c.id : null;
      $("form").hidden = false;
      $("form-title").textContent = c ? "Edit class " + c.code : req ? "Schedule the request from " + req.email : "New class";
      $("form").setAttribute("data-request", req ? req.id : "");
      $("c-title").value = c ? c.title : req ? "1:1 class" + (req.topic && T.topics[req.topic] ? ": " + T.topics[req.topic].title : "") : "";
      $("c-topic").value = c ? c.topic : req ? req.topic : "";
      $("c-starts").value = c ? local(c.starts) : req && req.slot ? local(req.slot) : "";
      if (req && req.slot && data.availability && data.availability.minutes) $("c-minutes").value = data.availability.minutes;
      $("c-minutes").value = c ? c.minutes : 60;
      $("c-mode").value = c ? c.mode : req ? "request" : "open";
      $("c-tickets").value = c ? c.cost : req ? 3 : 1;
      $("c-cap").value = c ? c.capacity : 0;
      $("c-meet").value = c ? c.meet || "" : "";
      $("c-rec").value = c && c.recording ? "https://youtu.be/" + c.recording : "";
      $("c-note").value = c ? c.note : req ? req.note : "";
      $("c-msg").textContent = "";
      $("form").scrollIntoView({ behavior: "smooth" });
    }
    function load() {
      return rpc("api_teacher_classes").then(function (d) {
        data = d;
        availability();
        var openReq = d.requests.filter(function (r) { return r.status === "open"; });
        $("status").textContent = d.classes.length + " classes · " + openReq.length + " open request" + (openReq.length === 1 ? "" : "s");
        $("requests").innerHTML = d.requests.length ? '<table class="tc-table"><tr><th>Student</th><th>Topic</th><th>Times</th><th>Note</th><th>Status</th><th></th></tr>' +
          d.requests.map(function (r) {
            return "<tr><td>" + esc(r.email) + "</td><td>" + esc(r.topic && T.topics[r.topic] ? r.topic + " " + T.topics[r.topic].title : "Any") +
              "</td><td>" + (r.slot ? "<b>" + esc(new Date(r.slot).toLocaleString(undefined, { weekday: "short", day: "numeric", month: "short", hour: "numeric", minute: "2-digit" })) + "</b><br>" : "") +
              esc(r.times) + "</td><td>" + esc(r.note) + "</td><td>" + esc(r.status) + "</td><td>" +
              (r.status === "open" ? '<button class="btn dark" data-sched="' + r.id + '">Schedule</button> <button class="btn" data-decline="' + r.id + '">Decline</button>' : "") +
              "</td></tr>";
          }).join("") + "</table>" : '<p class="tc-empty">No requests yet. Students ask for classes from the Live classes page.</p>';
        var now = Date.now();
        var card = function (c) {
          var past = c.starts && new Date(c.starts).getTime() + c.minutes * 60000 < now;
          var money = c.mode === "open" ? "Open, free" : (c.mode === "request" ? "1:1 · " : "Batch · ") + c.tickets + " ticket" + (c.tickets === 1 ? "" : "s");
          return '<article class="tc-card" id="c' + c.id + '"><h3><span>' + esc(c.title) + " · " + esc(c.code) + '</span><span class="tc-btns">' +
            '<button class="btn" data-edit="' + c.id + '">Edit</button><button class="btn" data-del="' + c.id + '">' +
            (armed === "del" + c.id ? "Click again to delete" : "Delete") + "</button></span></h3>" +
            '<p class="tc-note">' + (c.starts ? esc(new Date(c.starts).toLocaleString(undefined, { weekday: "long", day: "numeric", month: "long", hour: "numeric", minute: "2-digit" })) : "No time set") +
            " · " + c.minutes + " min · " + esc(money) + (c.capacity ? " · " + c.capacity + " seats" : "") +
            (c.recording ? " · recording added" : past ? " · <b>add the recording</b>" : "") + "</p>" +
            (past ? "" : '<div class="tc-btns tc-live">' +
              (c.meet ? '<a class="btn dark" href="' + esc(c.meet) + '" target="_blank" rel="noopener">Start the class</a>' : "") +
              (c.checkinCode ? '<span class="tc-code">Check-in code <b>' + esc(c.checkinCode) + "</b> until " +
                esc(new Date(c.checkinUntil).toLocaleTimeString(undefined, { hour: "numeric", minute: "2-digit" })) + "</span>" +
                '<button class="btn" data-checkoff="' + c.id + '">Close check-in</button>'
                : '<button class="btn" data-checkon="' + c.id + '">Open check-in (10 min)</button>') +
              '<span class="tc-teams"><input type="number" min="2" max="12" value="' + (c.teams || 3) + '" data-teamsin="' + c.id + '" aria-label="Number of teams">' +
              '<button class="btn" data-split="' + c.id + '">Split into breakout teams</button>' +
              (c.teams ? '<button class="btn" data-unsplit="' + c.id + '">End breakouts</button>' : "") + "</span></div>") +
            (c.teams && c.meet ? '<p class="tc-note">Team rooms: ' + Array.apply(null, Array(c.teams)).map(function (_, i) {
              return '<a href="' + esc(teamUrl(c.meet, i + 1)) + '" target="_blank" rel="noopener">Team ' + (i + 1) + "</a>";
            }).join(" · ") + "</p>" : "") +
            (past ? '<p class="aa-tools"><input class="tc-recin" placeholder="Unlisted YouTube link for the recording" value="' +
              (c.recording ? "https://youtu.be/" + esc(c.recording) : "") + '" data-recin="' + c.id + '"> <button class="btn dark" data-rec="' + c.id + '">' +
              (c.recording ? "Update recording" : "Add recording") + "</button></p>" : "") +
            '<table class="tc-table"><tr><th>Student</th><th>Seat</th><th>Attendance</th><th>Team</th><th>Joined</th><th></th></tr>' + c.seats.map(function (s) {
              return "<tr><td>" + esc(s.email) + "</td><td>" + (s.ok ? "Confirmed" : "Waiting for payment") + (s.paid ? " · paid" : "") + "</td>" +
                '<td><select data-mark="' + c.id + '" data-email="' + esc(s.email) + '">' +
                [["", "Auto: " + (s.mark ? "" : s.attendance || "not yet")], ["present", "Present"], ["late", "Late"], ["absent", "Absent"], ["excused", "Excused"]]
                  .map(function (o) { return '<option value="' + o[0] + '"' + (s.mark === o[0] ? " selected" : "") + ">" + esc(o[1]) + "</option>"; }).join("") +
                "</select>" + (s.checkedIn ? " ✓" : "") + "</td><td>" + (s.team || "&ndash;") + "</td><td>" +
                (s.joined ? esc(new Date(s.joined).toLocaleTimeString(undefined, { hour: "numeric", minute: "2-digit" })) : "&ndash;") + "</td><td>" +
                (!s.ok ? '<button class="btn" data-paid="' + c.id + '" data-email="' + esc(s.email) + '">Let in without tickets</button> ' : "") +
                '<button class="btn" data-rm="' + c.id + '" data-email="' + esc(s.email) + '">Remove</button></td></tr>';
            }).join("") + "</table>" +
            '<p class="aa-tools"><input placeholder="student@email" data-addin="' + c.id + '"> <button class="btn" data-add="' + c.id + '">Add student</button>' +
            (c.seats.length ? ' <button class="btn" data-csv="' + c.id + '">Attendance CSV</button>' : "") + "</p></article>";
        };
        var up = d.classes.filter(function (c) { return !c.starts || new Date(c.starts).getTime() + c.minutes * 60000 >= now; });
        var past = d.classes.filter(function (c) { return c.starts && new Date(c.starts).getTime() + c.minutes * 60000 < now; });
        $("list").innerHTML = "<h2>Upcoming</h2>" + (up.length ? up.map(card).join("") : '<p class="tc-empty">None.</p>') +
          "<h2>Past</h2>" + (past.length ? past.map(card).join("") : '<p class="tc-empty">None.</p>');
        bind();
      }).catch(function (e) { $("status").textContent = "Could not load: " + e.message; });
    }
    function find(id) { return data.classes.filter(function (c) { return c.id === +id; })[0]; }
    function bind() {
      var on = function (sel, fn) { document.querySelectorAll(sel).forEach(function (b) { b.addEventListener("click", function () { fn(b); }); }); };
      on("[data-sched]", function (b) { fill(null, data.requests.filter(function (r) { return r.id === +b.getAttribute("data-sched"); })[0]); });
      on("[data-decline]", function (b) { rpc("api_teacher_answer_request", { p_id: +b.getAttribute("data-decline"), p_status: "declined" }).then(load); });
      on("[data-edit]", function (b) { fill(find(b.getAttribute("data-edit"))); });
      on("[data-del]", function (b) {
        var id = b.getAttribute("data-del");
        if (armed !== "del" + id) { armed = "del" + id; load(); return; }
        armed = "";
        rpc("api_teacher_delete_class", { p_id: +id }).then(load);
      });
      on("[data-paid]", function (b) { rpc("api_teacher_set_seat", { p_id: +b.getAttribute("data-paid"), p_email: b.getAttribute("data-email"), p_state: "paid" }).then(load); });
      on("[data-rm]", function (b) { rpc("api_teacher_set_seat", { p_id: +b.getAttribute("data-rm"), p_email: b.getAttribute("data-email"), p_state: "remove" }).then(load); });
      var err = function (e) { $("status").textContent = e.message; };
      on("[data-checkon]", function (b) { rpc("api_teacher_open_checkin", { p_id: +b.getAttribute("data-checkon"), p_minutes: 10 }).then(load, err); });
      on("[data-checkoff]", function (b) { rpc("api_teacher_open_checkin", { p_id: +b.getAttribute("data-checkoff"), p_minutes: 0 }).then(load, err); });
      on("[data-split]", function (b) {
        var c = find(b.getAttribute("data-split")), n = Math.max(2, Math.min(12, +document.querySelector('[data-teamsin="' + c.id + '"]').value || 3));
        var people = c.seats.filter(function (s) { return s.ok; }).map(function (s) { return s.email; }).sort(function () { return Math.random() - 0.5; });
        var teams = Array.apply(null, Array(Math.min(n, people.length || 1))).map(function () { return []; });
        people.forEach(function (e, i) { teams[i % teams.length].push(e); });
        rpc("api_teacher_breakouts", { p_id: c.id, p_teams: teams }).then(load, err);
      });
      on("[data-unsplit]", function (b) { rpc("api_teacher_breakouts", { p_id: +b.getAttribute("data-unsplit"), p_teams: [] }).then(load, err); });
      on("[data-rec]", function (b) {
        var c = find(b.getAttribute("data-rec"));
        rpc("api_teacher_save_class", { p: { id: c.id, title: c.title, topic: c.topic, starts: c.starts || "", minutes: c.minutes, mode: c.mode,
          tickets: c.cost, capacity: c.capacity, meet: c.meet || "", note: c.note,
          recording: document.querySelector('[data-recin="' + c.id + '"]').value } }).then(function (r) {
          if (!r.ok) throw new Error(r.error);
          load();
        }).catch(err);
      });
      on("[data-csv]", function (b) {
        var c = find(b.getAttribute("data-csv"));
        var rows = [["email", "seat", "attendance", "checked_in", "joined", "team"].join(",")].concat(c.seats.map(function (s) {
          return [s.email, s.ok ? "confirmed" : "pending", s.mark || s.attendance, s.checkedIn || "", s.joined || "", s.team || ""].join(",");
        }));
        var a = document.createElement("a");
        a.href = URL.createObjectURL(new Blob([rows.join("\n")], { type: "text/csv" }));
        a.download = "attendance-" + c.code + ".csv";
        a.click();
      });
      document.querySelectorAll("[data-mark]").forEach(function (sel) {
        sel.addEventListener("change", function () {
          rpc("api_teacher_set_attendance", { p_id: +sel.getAttribute("data-mark"), p_email: sel.getAttribute("data-email"), p_status: sel.value }).then(load, err);
        });
      });
      on("[data-add]", function (b) {
        var id = b.getAttribute("data-add"), inp = document.querySelector('[data-addin="' + id + '"]');
        rpc("api_teacher_set_seat", { p_id: +id, p_email: inp.value, p_state: find(id).mode === "paid" ? "paid" : "add" }).then(function (r) {
          if (!r.ok) throw new Error(r.error);
          load();
        }).catch(function (e) { $("status").textContent = e.message; });
      });
    }
    var av = null;
    function grid() {
      var hours = [], days = [1, 2, 3, 4, 5, 6, 0];
      for (var h = 6; h < 23; h++) hours.push(String(h).padStart(2, "0") + ":00");
      var on = function (d, t) { return (av.slots[d] || []).indexOf(t) !== -1; };
      $("av-grid").innerHTML = "<table class='tc-avt'><tr><th></th>" + days.map(function (d) { return "<th>" + DOW[d] + "</th>"; }).join("") + "</tr>" +
        hours.map(function (t) {
          return "<tr><th>" + t + "</th>" + days.map(function (d) {
            return '<td><button class="' + (on(d, t) ? "on" : "") + '" data-d="' + d + '" data-t="' + t + '" aria-label="' + DOW[d] + " " + t + '"></button></td>';
          }).join("") + "</tr>";
        }).join("") + "</table>";
      $("av-grid").querySelectorAll("button").forEach(function (b) {
        b.addEventListener("click", function () {
          var d = b.getAttribute("data-d"), t = b.getAttribute("data-t"), list = av.slots[d] = av.slots[d] || [];
          var i = list.indexOf(t);
          if (i === -1) list.push(t); else list.splice(i, 1);
          list.sort();
          b.classList.toggle("on");
          $("av-msg").textContent = "Not saved yet.";
        });
      });
    }
    function availability() {
      if (av) return;
      av = JSON.parse(JSON.stringify(data.availability || {}));
      av.slots = av.slots || {};
      $("av-tz").value = av.tz || Intl.DateTimeFormat().resolvedOptions().timeZone || "Asia/Kolkata";
      $("av-min").value = av.minutes || 60;
      $("av-weeks").value = av.weeks || 2;
      grid();
    }
    $("av-save").addEventListener("click", function () {
      av.tz = $("av-tz").value.trim() || "Asia/Kolkata";
      av.minutes = +$("av-min").value || 60;
      av.weeks = +$("av-weeks").value || 2;
      $("av-msg").textContent = "Saving…";
      rpc("api_teacher_set_availability", { p: av }).then(function (r) {
        if (!r.ok) throw new Error(r.error);
        $("av-msg").textContent = "Saved. Students can book these hours now.";
      }).catch(function (e) { $("av-msg").textContent = e.message; });
    });
    $("new").addEventListener("click", function () { fill(null); });
    $("c-cancel").addEventListener("click", function () { $("form").hidden = true; });
    $("c-save").addEventListener("click", function () {
      var starts = $("c-starts").value ? new Date($("c-starts").value).toISOString() : "";
      var p = { id: editing || "", title: $("c-title").value, topic: $("c-topic").value, starts: starts, minutes: $("c-minutes").value,
        mode: $("c-mode").value, tickets: $("c-tickets").value, capacity: $("c-cap").value, meet: $("c-meet").value,
        recording: $("c-rec").value, note: $("c-note").value, request: $("form").getAttribute("data-request") || "" };
      $("c-msg").textContent = "Saving…";
      rpc("api_teacher_save_class", { p: p }).then(function (r) {
        if (!r.ok) throw new Error(r.error);
        $("form").hidden = true;
        return load();
      }).catch(function (e) { $("c-msg").textContent = e.message; });
    });
    load().then(function () { if (location.hash) { var el = document.querySelector(location.hash); if (el) el.scrollIntoView(); } });
    setInterval(function () {
      var busy = document.activeElement && /INPUT|TEXTAREA|SELECT/.test(document.activeElement.tagName);
      if (!document.hidden && !busy && $("form").hidden) load();
    }, 20000);
  }

  function assign() {
    var videos = [], list = [], armed = "";
    function items() {
      var k = $("a-kind").value;
      $("a-link").hidden = k !== "link";
      $("a-item").hidden = k === "link";
      if (k === "skill") $("a-item").innerHTML = atomOptions();
      else if (k === "topic" || k === "quiz") $("a-item").innerHTML = topicOptions();
      else if (k === "adaptive") $("a-item").innerHTML = (T.units || []).map(function (u) { return '<option value="U' + u.n + '">Unit ' + u.n + " " + esc(u.title) + "</option>"; }).join("");
      else if (k === "video") $("a-item").innerHTML = videos.length ? videos.map(function (v) { return '<option value="v' + v.id + '">' + esc(v.title) + "</option>"; }).join("") : '<option value="">Post a video first</option>';
      else if (k === "lecture") $("a-item").innerHTML = (T.decks || []).map(function (d) { return '<option value="' + esc(d.stem) + '">' + String(d.n).padStart(2, "0") + " " + esc(d.title) + "</option>"; }).join("");
    }
    function chosen() {
      var k = $("a-kind").value, v = $("a-item").value;
      if (k === "link") return { ref: "", title: $("a-note").value || $("a-link").value, href: $("a-link").value };
      if (k === "skill") return { ref: v, title: atomName(v), href: T.atoms[v].lesson };
      if (k === "topic") return { ref: v, title: v + " " + T.topics[v].title, href: T.topics[v].student };
      if (k === "quiz") return { ref: v, title: v + " quiz", href: T.topics[v].student };
      if (k === "adaptive") { var u = T.units.filter(function (x) { return "U" + x.n === v; })[0]; return { ref: v, title: "Unit " + u.n + " adaptive test", href: u.test }; }
      if (k === "video") { var vid = videos.filter(function (x) { return "v" + x.id === v; })[0]; return vid ? { ref: v, title: "Watch: " + vid.title, href: "videos.html#" + v } : null; }
      var d = T.decks.filter(function (x) { return x.stem === v; })[0];
      return { ref: v, title: "Lecture " + String(d.n).padStart(2, "0") + ": " + d.title, href: d.page };
    }
    function load() {
      return Promise.all([rpc("api_teacher_assignments"), loadPlans()]).then(function (r) {
        list = r[0];
        draw();
      }).catch(function (e) { $("status").textContent = "Could not load: " + e.message; });
    }
    function draw() {
      var f = $("a-filter").value;
      var shown = list.filter(function (a) { return f === "*" || String(a.group || "") === f; });
      $("status").textContent = list.length + " assignment" + (list.length === 1 ? "" : "s");
      $("list").innerHTML = shown.length ? shown.map(function (a) {
        var g = plans.filter(function (x) { return x.id === String(a.group || ""); })[0];
        var pct = a.students ? Math.round(a.done.length / a.students * 100) : 0;
        return '<article class="tc-card"><h3><span>' + esc(a.title) + '</span><button class="btn" data-del="' + a.id + '">' +
          (armed === "d" + a.id ? "Click again to delete" : "Delete") + "</button></h3>" +
          '<p class="tc-note">' + esc(g ? g.name : "Everyone") + (a.due ? " · due " + esc(new Date(a.due).toLocaleString(undefined, { weekday: "short", day: "numeric", month: "short", hour: "numeric", minute: "2-digit" })) : " · no due date") +
          (a.note ? " · " + esc(a.note) : "") + (a.href ? ' · <a href="' + esc(/^https?:/.test(a.href) ? a.href : url(a.href)) + '" target="_blank" rel="noopener">open</a>' : "") + "</p>" +
          (a.kind === "link" ? "" : '<div class="tc-bar"><span>Done</span><span class="t"><i style="width:' + pct + '%"></i></span><span class="n">' + a.done.length + "/" + a.students + "</span></div>" +
            "<details><summary>Who's done</summary><p>" + (a.done.map(esc).join(", ") || "Nobody yet.") + "</p></details>") + "</article>";
      }).join("") : '<p class="tc-empty">Nothing assigned yet.</p>';
      document.querySelectorAll("[data-del]").forEach(function (b) {
        b.addEventListener("click", function () {
          var id = b.getAttribute("data-del");
          if (armed !== "d" + id) { armed = "d" + id; draw(); return; }
          armed = "";
          rpc("api_teacher_unassign", { p_id: +id }).then(load);
        });
      });
    }
    Promise.all([loadPlans(), rpc("api_teacher_videos").catch(function () { return { videos: [] }; })]).then(function (r) {
      videos = r[1].videos || [];
      $("a-group").innerHTML = groupOptions(false);
      $("a-filter").innerHTML = groupOptions(true);
      $("a-filter").value = "*";
      $("a-filter").addEventListener("change", draw);
      $("a-kind").addEventListener("change", items);
      items();
      load();
    });
    $("a-save").addEventListener("click", function () {
      var c = chosen();
      if (!c || (!c.ref && !c.href)) { $("a-msg").textContent = "Pick what to assign."; return; }
      $("a-msg").textContent = "Saving…";
      rpc("api_teacher_assign", { p: { group: $("a-group").value, kind: $("a-kind").value, ref: c.ref, title: c.title, href: c.href,
        due: $("a-due").value ? new Date($("a-due").value).toISOString() : "", note: $("a-note").value } }).then(function (r) {
        if (!r.ok) throw new Error(r.error);
        $("a-msg").textContent = "Assigned. Students see it on their calendar and in their menu.";
        $("a-note").value = "";
        return load();
      }).catch(function (e) { $("a-msg").textContent = e.message; });
    });
  }

  function videos() {
    var list = [], editing = null, armed = "";
    function reset() {
      editing = null;
      ["v-yt", "v-title", "v-note"].forEach(function (id) { $(id).value = ""; });
      $("v-atom").value = ""; $("v-group").value = ""; $("v-free").checked = false; $("v-email").checked = false;
      $("v-head").textContent = "Post a video"; $("v-save").textContent = "Post video";
      preview();
    }
    function ytId(u) {
      var m = /(?:youtu\.be\/|v=|embed\/|shorts\/|live\/)([A-Za-z0-9_-]{11})/.exec(u || "") || /^([A-Za-z0-9_-]{11})$/.exec((u || "").trim());
      return m ? m[1] : "";
    }
    function preview() {
      var id = ytId($("v-yt").value), g = $("v-group"), a = $("v-atom");
      $("v-pthumb").innerHTML = id ? '<img src="https://i.ytimg.com/vi/' + id + '/mqdefault.jpg" alt="">'
        : "<span>" + ($("v-yt").value.trim() ? "That doesn't look like a YouTube link" : "Paste a YouTube link to see it here") + "</span>";
      $("v-ptitle").textContent = $("v-title").value.trim() || "Untitled video";
      $("v-pmeta").textContent = (a.value ? a.options[a.selectedIndex].text : "Not tied to a lesson") + " · " +
        (g.selectedIndex >= 0 ? g.options[g.selectedIndex].text : "Everyone") + " · " + ($("v-free").checked ? "Free" : "Labs");
    }
    function load() {
      return rpc("api_teacher_videos").then(function (d) {
        list = d.videos || [];
        var views = list.reduce(function (n, v) { return n + (v.views || 0); }, 0);
        $("status").textContent = list.length + " video" + (list.length === 1 ? "" : "s") + " · " + views + " view" + (views === 1 ? "" : "s") +
          (typeof d.buyers === "number" ? " · " + d.buyers + " student" + (d.buyers === 1 ? "" : "s") + " with Labs" : "");
        $("v-count").textContent = list.length ? list.length + " in all, newest first" : "";
        $("list").innerHTML = list.length ? list.map(function (v) {
          var g = plans.filter(function (x) { return x.id === String(v.group || ""); })[0];
          return '<article class="tv-item"><a class="tv-thumb" href="https://youtu.be/' + esc(v.youtube) + '" target="_blank" rel="noopener">' +
            '<img src="https://i.ytimg.com/vi/' + esc(v.youtube) + '/mqdefault.jpg" alt="" loading="lazy"></a>' +
            '<div class="tv-info"><h4>' + esc(v.title) + "</h4>" +
            '<div class="tv-tags">' + (v.atom ? '<span class="tv-tag">' + esc(atomName(v.atom)) + "</span>" : '<span class="tv-tag dim">No lesson</span>') +
            '<span class="tv-tag">' + esc(g ? g.name : "Everyone") + "</span>" +
            '<span class="tv-tag ' + (v.free ? "on" : "") + '">' + (v.free ? "Free" : "Labs") + "</span>" +
            (v.email ? '<span class="tv-tag dim">' + (v.emailed ? "Emailed" : "Email queued") + "</span>" : "") + "</div>" +
            (v.note ? '<p class="tc-note">' + esc(v.note) + "</p>" : "") + "</div>" +
            '<div class="tv-views"><b>' + (v.views || 0) + "</b>watched</div>" +
            '<div class="tv-acts"><button class="btn" data-edit="' + v.id + '">Edit</button><a class="btn" href="assignments.html">Assign</a>' +
            '<button class="btn' + (armed === "d" + v.id ? " dark" : "") + '" data-del="' + v.id + '">' + (armed === "d" + v.id ? "Click again to delete" : "Delete") + "</button></div></article>";
        }).join("") : '<p class="tc-empty">No videos yet. Upload to YouTube as Unlisted, then paste the link above.</p>';
        document.querySelectorAll("[data-edit]").forEach(function (b) {
          b.addEventListener("click", function () {
            var v = list.filter(function (x) { return x.id === +b.getAttribute("data-edit"); })[0];
            editing = v.id;
            $("v-yt").value = "https://youtu.be/" + v.youtube; $("v-title").value = v.title; $("v-note").value = v.note;
            $("v-atom").value = v.atom || ""; $("v-group").value = v.group ? String(v.group) : ""; $("v-free").checked = v.free;
            $("v-head").textContent = "Edit video"; $("v-save").textContent = "Save changes";
            preview();
            scrollTo(0, 0);
          });
        });
        document.querySelectorAll("[data-del]").forEach(function (b) {
          b.addEventListener("click", function () {
            var id = b.getAttribute("data-del");
            if (armed !== "d" + id) { armed = "d" + id; load(); return; }
            armed = "";
            rpc("api_teacher_delete_video", { p_id: +id }).then(load);
          });
        });
      }).catch(function (e) { $("status").textContent = "Could not load: " + e.message; });
    }
    $("v-atom").innerHTML = atomOptions("Not tied to a lesson");
    loadPlans().then(function () { $("v-group").innerHTML = groupOptions(false); preview(); load(); });
    ["v-yt", "v-title"].forEach(function (id) { $(id).addEventListener("input", preview); });
    ["v-atom", "v-group", "v-free"].forEach(function (id) { $(id).addEventListener("change", preview); });
    $("v-reset").addEventListener("click", reset);
    $("v-save").addEventListener("click", function () {
      var atom = $("v-atom").value;
      $("v-msg").textContent = "Saving…";
      rpc("api_teacher_save_video", { p: { id: editing || "", youtube: $("v-yt").value, title: $("v-title").value, note: $("v-note").value,
        atom: atom, topic: atom ? T.atoms[atom].topic : "", group: $("v-group").value, free: $("v-free").checked, email: $("v-email").checked } })
        .then(function (r) {
          if (!r.ok) throw new Error(r.error);
          $("v-msg").textContent = editing ? "Saved." : "Posted. Students see it on the Video lessons page" + (atom ? " and on lesson " + atom : "") + ".";
          reset();
          return load();
        }).catch(function (e) { $("v-msg").textContent = e.message; });
    });
  }

  function present() {
    var stem = (new URLSearchParams(location.search).get("deck") || "").replace(/[^A-Za-z0-9_-]/g, "");
    var deck = (T.decks || []).filter(function (d) { return d.stem === stem; })[0];
    if (!deck) { $("p-notes").textContent = "Pick a deck on the Lectures page."; return; }
    $("p-title").textContent = String(deck.n).padStart(2, "0") + " " + deck.title;
    $("p-frame").src = url(deck.page);
    $("p-pop").href = url(deck.page);
    var t0 = Date.now();
    setInterval(function () {
      var s = Math.floor((Date.now() - t0) / 1000);
      $("p-clock").textContent = String(Math.floor(s / 60)).padStart(2, "0") + ":" + String(s % 60).padStart(2, "0");
    }, 1000);
    $("p-reset").addEventListener("click", function () { t0 = Date.now(); });
    try {
      var bc = new BroadcastChannel("deck-sync-" + stem);
      bc.onmessage = function (e) {
        var d = e.data || {};
        if (d.type !== "nav") return;
        $("p-count").textContent = "Slide " + (d.index + 1) + " of " + d.total;
        $("p-unit").textContent = d.unit || "";
        $("p-slide").textContent = d.title || "";
        $("p-notes").innerHTML = d.notesBody || "<p><i>No speaker notes for this slide.</i></p>";
      };
    } catch (e) { $("p-notes").textContent = "This browser can't sync notes. Use the deck's own Speaker Notes button (N)."; }
    $("p-frame").addEventListener("load", function () { try { $("p-frame").contentWindow.focus(); } catch (e) {  } });
  }

  function ctf() {
    var data = { challenges: [], solves: [] }, editing = null;
    var F = ["title", "unit", "points", "body", "hint", "link", "flag", "solve"];
    function fill(c) {
      editing = c ? c.id : null;
      F.forEach(function (k) { $("f-" + k).value = c ? (c[k] == null ? "" : c[k]) : k === "points" ? 100 : k === "unit" ? "0" : ""; });
      $("f-head").textContent = c ? "Edit: " + c.title : "New challenge";
      $("f-new").hidden = !c;
      $("f-msg").textContent = c && c.builtin ? "Built-in challenge: edits last until the next database seed." : "";
      if (c) $("f-card").scrollIntoView({ behavior: "smooth" });
    }
    function draw() {
      var solved = data.challenges.reduce(function (t, c) { return t + c.solves; }, 0);
      $("status").textContent = data.challenges.length ? data.challenges.length + " challenges · " + solved + " solves" :
        "No challenges in the database yet. Load the built-in set with: python db/sql.py db/ctf_challenges.sql";
      $("c-list").innerHTML = data.challenges.length ? '<table class="tc-table"><tr><th>Unit</th><th>Challenge</th><th>Flag</th><th>Walkthrough</th>' +
        "<th>Solves</th><th></th></tr>" + data.challenges.map(function (c) {
          return "<tr" + (c.active ? "" : ' style="opacity:.5"') + "><td>" + (c.unit || "&ndash;") + "</td><td><b>" + esc(c.title) + "</b><br><small>" +
            c.points + " pts" + (c.link ? " · " + esc(c.link.split("#")[0]) : "") + (c.active ? "" : " · hidden") + "</small></td>" +
            "<td><code>" + esc(c.flag) + "</code></td><td><small>" + esc(c.solve) + "</small></td><td>" + c.solves + " <small>/ " + c.tries + " tries</small></td>" +
            '<td class="tc-btns"><button class="btn" data-edit="' + esc(c.id) + '">Edit</button>' +
            (c.active ? '<button class="btn" data-off="' + esc(c.id) + '">' + (c.builtin ? "Hide" : "Delete") + "</button>" :
              '<button class="btn" data-on="' + esc(c.id) + '">Show</button>') + "</td></tr>";
        }).join("") + "</table>" : "";
      var titles = {};
      data.challenges.forEach(function (c) { titles[c.id] = c.title; });
      $("c-solves").innerHTML = data.solves.length ? '<table class="tc-table"><tr><th>When</th><th>Student</th><th>Challenge</th></tr>' +
        data.solves.slice(0, 60).map(function (s) {
          return "<tr><td>" + ago(s.at) + "</td><td>" + esc(s.email) + "</td><td>" + esc(titles[s.id] || s.id) + "</td></tr>";
        }).join("") + "</table>" : '<p class="tc-note">No flags captured yet.</p>';
      document.querySelectorAll("[data-edit]").forEach(function (b) {
        b.addEventListener("click", function () { fill(data.challenges.filter(function (c) { return c.id === b.getAttribute("data-edit"); })[0]); });
      });
      document.querySelectorAll("[data-off]").forEach(function (b) {
        b.addEventListener("click", function () {
          if (!confirm("Remove this challenge from the student board?")) return;
          rpc("api_teacher_ctf_delete", { p_id: b.getAttribute("data-off") }).then(load);
        });
      });
      document.querySelectorAll("[data-on]").forEach(function (b) {
        b.addEventListener("click", function () {
          var c = data.challenges.filter(function (x) { return x.id === b.getAttribute("data-on"); })[0];
          rpc("api_teacher_ctf_save", { p: { id: c.id, title: c.title, active: true } }).then(load);
        });
      });
    }
    function load() {
      return rpc("api_teacher_ctf").then(function (d) { if (d && d.ok) { data = d; draw(); } },
        function (e) { $("status").textContent = "Could not load: " + e.message; });
    }
    $("f-new").addEventListener("click", function () { fill(null); });
    $("f-save").addEventListener("click", function () {
      var p = {};
      F.forEach(function (k) { p[k] = $("f-" + k).value; });
      p.unit = +p.unit; p.points = +p.points;
      if (editing) p.id = editing;
      if (editing && !p.flag.trim()) delete p.flag;
      rpc("api_teacher_ctf_save", { p: p }).then(function (r) {
        if (!r || !r.ok) { $("f-msg").textContent = (r && r.error) || "Could not save."; return; }
        fill(null);
        $("f-msg").textContent = "Saved.";
        load();
      }, function (e) { $("f-msg").textContent = e.message; });
    });
    load();
  }

  function seminarsPage() {
    var data = [], editing = null;
    var F = ["title", "youtube", "summary", "description", "level", "minutes", "tickets", "sort", "topics", "cover"];
    function lines(list, fmt) { return (list || []).map(fmt).join("\n"); }
    function fill(s) {
      editing = s ? s.id : null;
      F.forEach(function (k) { $("s-" + k).value = s ? (s[k] == null ? "" : s[k]) : k === "tickets" ? 1 : k === "sort" ? 0 : ""; });
      $("s-chapters").value = s ? lines(s.chapters, function (c) { return c.t + " " + c.title; }) : "";
      $("s-resources").value = s ? lines(s.resources, function (r) { return r.title + " | " + r.url; }) : "";
      $("s-published").checked = !!(s && s.published);
      $("s-head").textContent = s ? "Edit: " + s.title : "New seminar";
      $("s-new").hidden = !s;
      if (s) $("s-card").scrollIntoView({ behavior: "smooth" });
    }
    function draw(d) {
      $("status").textContent = data.length + " seminar" + (data.length === 1 ? "" : "s") + " · " + d.subscribers + " active subscriber" + (d.subscribers === 1 ? "" : "s");
      $("s-list").innerHTML = data.length ? '<table class="tc-table"><tr><th>Seminar</th><th>Tickets</th><th>Owners</th><th></th></tr>' +
        data.map(function (s) {
          return "<tr><td><b>" + esc(s.title) + "</b><br><small>" + (s.published ? "Published" : "Draft") + (s.minutes ? " · " + s.minutes + " min" : "") +
            " · " + (s.chapters || []).length + " chapters" + (s.youtube ? "" : " · no video yet") + "</small></td><td>" + s.tickets + "</td><td>" + s.owners + "</td>" +
            '<td class="tc-btns"><button class="btn" data-sedit="' + s.id + '">Edit</button><a class="btn" href="' + url("seminars.html?id=" + s.id) +
            '" target="_blank" rel="noopener">View</a><button class="btn" data-sdel="' + s.id + '">' + (s.owners ? "Hide" : "Delete") + "</button></td></tr>";
        }).join("") + "</table>" : '<p class="tc-note">No seminars yet. Add your first one above.</p>';
      document.querySelectorAll("[data-sedit]").forEach(function (b) {
        b.addEventListener("click", function () { fill(data.filter(function (s) { return s.id === +b.getAttribute("data-sedit"); })[0]); });
      });
      document.querySelectorAll("[data-sdel]").forEach(function (b) {
        b.addEventListener("click", function () {
          if (!confirm("Remove this seminar? If anyone has unlocked it, it is hidden instead, so they keep it.")) return;
          rpc("api_teacher_delete_seminar", { p_id: +b.getAttribute("data-sdel") }).then(load);
        });
      });
    }
    function load() {
      return rpc("api_teacher_seminars").then(function (d) { data = d.seminars; draw(d); }, function (e) { $("status").textContent = "Could not load: " + e.message; });
    }
    $("s-new").addEventListener("click", function () { fill(null); });
    $("s-save").addEventListener("click", function () {
      var p = {};
      F.forEach(function (k) { p[k] = $("s-" + k).value; });
      p.minutes = +p.minutes || 0; p.tickets = +p.tickets; p.sort = +p.sort || 0;
      p.published = $("s-published").checked;
      p.chapters = $("s-chapters").value.split("\n").map(function (l) {
        var m = l.trim().match(/^((?:\d+:)?\d{1,2}:\d{2})\s+(.+)$/);
        return m ? { t: m[1], title: m[2] } : null;
      }).filter(Boolean);
      p.resources = $("s-resources").value.split("\n").map(function (l) {
        var i = l.lastIndexOf("|");
        return i > 0 && /^https:\/\//.test(l.slice(i + 1).trim()) ? { title: l.slice(0, i).trim(), url: l.slice(i + 1).trim() } : null;
      }).filter(Boolean);
      if (editing) p.id = editing;
      rpc("api_teacher_save_seminar", { p: p }).then(function (r) {
        if (!r || !r.ok) { $("s-msg").textContent = (r && r.error) || "Could not save."; return; }
        fill(null);
        $("s-msg").textContent = "Saved.";
        load();
      }, function (e) { $("s-msg").textContent = e.message; });
    });
    load();
  }

  function labsPage() {
    var data = [], editing = null, nbData = null;
    function kind() { return $("l-kind").value; }
    function show() {
      $("l-body-wrap").hidden = kind() !== "lab";
      $("l-nb-wrap").hidden = kind() !== "notebook";
      $("l-edit-nb").hidden = !editing;
      $("l-cells").textContent = kind() === "notebook" ? (editing ? "Save first, then open the editor to write cells." : "Save it first to open the editor, or import a file.") : "";
      if (editing) $("l-edit-nb").href = url("notebook.html?premium=" + editing);
    }
    function fill(i) {
      editing = i ? i.id : null;
      nbData = null;
      ["kind", "title", "unit", "topic", "tool", "summary", "body"].forEach(function (k) { $("l-" + k).value = i ? (i[k] == null ? "" : i[k]) : k === "kind" ? "lab" : k === "unit" ? "0" : ""; });
      $("l-published").checked = !!(i && i.published);
      $("l-head").textContent = i ? "Edit: " + i.title : "New lab";
      $("l-new").hidden = !i;
      show();
      if (i) $("l-card").scrollIntoView({ behavior: "smooth" });
    }
    function draw() {
      $("status").textContent = data.length + " item" + (data.length === 1 ? "" : "s") + " stored in the database";
      $("l-list").innerHTML = data.length ? '<table class="tc-table"><tr><th>Item</th><th>Unit</th><th></th></tr>' + data.map(function (i) {
        return "<tr><td><b>" + esc(i.title) + "</b><br><small>" + (i.kind === "notebook" ? "Notebook" : "Lab") + " · " + (i.published ? "Published" : "Draft") +
          "</small></td><td>" + (i.unit || "&ndash;") + (i.topic ? " · " + esc(i.topic) : "") + '</td><td class="tc-btns"><button class="btn" data-ledit="' + i.id + '">Edit</button>' +
          (i.kind === "notebook" ? '<a class="btn" href="' + url("notebook.html?premium=" + i.id) + '" target="_blank" rel="noopener">Notebook editor</a>' : "") +
          '<a class="btn" href="' + url("labs.html?id=" + i.id) + '" target="_blank" rel="noopener">View</a><button class="btn" data-ldel="' + i.id + '">Delete</button></td></tr>';
      }).join("") + "</table>" : '<p class="tc-note">Nothing here yet. Write your first lab above.</p>';
      document.querySelectorAll("[data-ledit]").forEach(function (b) {
        b.addEventListener("click", function () {
          rpc("api_premium_get", { p_id: +b.getAttribute("data-ledit") }).then(function (d) { if (d.ok) fill(d.item); });
        });
      });
      document.querySelectorAll("[data-ldel]").forEach(function (b) {
        b.addEventListener("click", function () {
          if (!confirm("Delete this from the database? Students lose access to it.")) return;
          rpc("api_teacher_premium_delete", { p_id: +b.getAttribute("data-ldel") }).then(load);
        });
      });
    }
    function load() {
      return rpc("api_premium_list").then(function (d) { data = d.items; draw(); }, function (e) { $("status").textContent = "Could not load: " + e.message; });
    }
    $("l-kind").addEventListener("change", show);
    $("l-new").addEventListener("click", function () { fill(null); });
    $("l-import").addEventListener("click", function () { $("l-file").click(); });
    $("l-file").addEventListener("change", function () {
      var f = $("l-file").files[0];
      if (!f) return;
      var r = new FileReader();
      r.onload = function () {
        try {
          var j = JSON.parse(r.result);
          nbData = { title: $("l-title").value || f.name.replace(/\.ipynb$/, ""), cells: (j.cells || []).map(function (c) {
            var s = Array.isArray(c.source) ? c.source.join("") : String(c.source || ""), m = /^%%(bash|sh)[^\n]*\n?/.exec(s);
            if (c.cell_type !== "code") return { t: "md", s: s };
            return m || (c.metadata && c.metadata.aayat === "sh") ? { t: "sh", s: m ? s.slice(m[0].length) : s } : { t: "py", s: s };
          }).filter(function (c) { return c.s.trim(); }) };
          if (!$("l-title").value) $("l-title").value = nbData.title;
          $("l-cells").textContent = nbData.cells.length + " cells ready. Press Save.";
        } catch (e) { $("l-cells").textContent = "That file isn't a notebook (.ipynb)."; }
        $("l-file").value = "";
      };
      r.readAsText(f);
    });
    $("l-save").addEventListener("click", function () {
      var p = { kind: kind(), title: $("l-title").value, unit: +$("l-unit").value, topic: $("l-topic").value, tool: $("l-tool").value,
        summary: $("l-summary").value, published: $("l-published").checked };
      if (kind() === "lab") p.body = $("l-body").value;
      if (nbData) p.data = nbData;
      if (editing) p.id = editing;
      rpc("api_teacher_premium_save", { p: p }).then(function (r) {
        if (!r || !r.ok) { $("l-msg").textContent = (r && r.error) || "Could not save."; return; }
        $("l-msg").textContent = "Saved.";
        editing = r.id;
        nbData = null;
        $("l-new").hidden = false;
        show();
        load();
      }, function (e) { $("l-msg").textContent = e.message; });
    });
    show();
    load();
  }

  var PAGES = { dash: dashboard, teach: teach, schedule: schedule, blog: blog, resources: resources, live: live, assign: assign,
    videos: videos, lectures: present, ctf: ctf, seminars: seminarsPage, labs: labsPage };
  var OPEN = { blog: 1, resources: 1, accounts: 1 };

  function foot() {
    var f = document.querySelector(".tc-foot"), who = global.Identity && global.Identity.getEmail();
    if (!f || !who) return;
    var d = document.createElement("div");
    d.className = "tc-who";
    d.textContent = who;
    var a = document.createElement("a");
    a.href = "#"; a.textContent = "Sign out";
    a.addEventListener("click", function (e) {
      e.preventDefault();
      global.Identity.signOut().then(function () { location.reload(); });
    });
    f.insertBefore(d, f.firstChild);
    f.appendChild(a);
  }

  function start() {
    foot();
    var el = document.querySelector("[data-tc]"), key = el && el.getAttribute("data-tc"), fn = PAGES[key];
    if (key === "lectures" && !$("p-frame")) fn = null;
    if (!el) return;
    if (OPEN[key]) { if (fn) fn(); return; }
    gate(el).then(function (ok) { if (ok && fn) fn(); });
  }
  if (document.readyState === "complete") start();
  else global.addEventListener("load", start);
})(window);
