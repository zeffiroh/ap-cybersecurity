/* The student's Progress page: course, unit and topic mastery, skill squares, recent activity. */
(function (global) {
  "use strict";

  var KIND = { topic: "Overview", notes: "Notes", slides: "Slides", practice: "Practice", simlab: "SimLab",
               sim: "Sim", flashcards: "Flashcards", quiz: "Quiz", assignments: "Assignments",
               activities: "Activities", unit: "Unit", lecture: "Lecture", book: "Book",
               capstone: "Capstone", test: "Test" };

  function esc(s) {
    return String(s == null ? "" : s).replace(/[&<>"]/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c];
    });
  }
  function bar(pct) { return '<span class="aa-bar"><i style="width:' + pct + '%"></i></span>'; }
  function when(iso) {
    var d = new Date(iso);
    return isNaN(d) ? "" : d.toLocaleDateString(undefined, { month: "short", day: "numeric" }) + " " +
      d.toLocaleTimeString(undefined, { hour: "2-digit", minute: "2-digit" });
  }

  function legend(P) {
    return '<p class="aa-legend">' + P.LEVELS.map(function (l, i) {
      return '<span><i class="aa-lvl aa-lvl-' + i + '"></i>' + l + "</span>";
    }).join("") + "</p>";
  }

  function render(box, rec, ms) {
    var P = global.AayatProgress, M = global.AAYAT_MAP, R = P.ROOT, who = P.email();
    var seen = P.seenSet(rec), h = [];
    h.push('<p class="aa-sub">' + (who ? esc(who) :
      'Not signed in: progress is saved on this device only. Use <b>Sign in</b> in the bar to keep it online.') + "</p>");
    h.push('<div class="aa-course"><span class="aa-big">' + ms.course + '%</span>' + bar(ms.course) +
      '<span class="aa-counts">' + [4, 3, 2, 1].map(function (l) {
        return ms.count[l] + " " + P.LEVELS[l].toLowerCase();
      }).join(" &middot; ") + "</span></div>");
    h.push(legend(P));

    M.units.forEach(function (u) {
      var um = ms.units[u.n];
      var test = um.theta == null ? '<a href="' + R + 'tests/index.html?unit=U' + u.n + '">Unit test: not taken</a>' :
        '<a href="' + R + 'tests/index.html?unit=U' + u.n + '">Unit test: θ ' + um.theta.toFixed(2) +
        (um.passed ? ", passed" : ", below the gate") + "</a>";
      h.push('<h2><a href="' + R + u.href + '">Unit ' + u.n + " " + esc(u.title) + "</a> &middot; " + um.pct + "%</h2>");
      var hw = um.hw == null ? "CW/HW: none taken" : "CW/HW: " + um.hw + "% average over " + um.hwTaken + " quiz" +
        (um.hwTaken === 1 ? "" : "zes");
      h.push('<p class="aa-sub">' + test + " &middot; " + '<a href="' + R + 'tests/hw/index.html">' + hw + "</a></p>");
      h.push('<table class="aa-prog"><tr><th>Topic</th><th>Skills</th><th>Mastery</th><th>Topic quiz</th><th>Opened</th></tr>');
      u.topics.forEach(function (tid) {
        var t = M.topics[tid], tm = ms.topics[tid];
        var squares = t.atoms.map(function (aid) {
          var a = M.atoms[aid], l = ms.atoms[aid];
          return '<a class="aa-lvl aa-lvl-' + l + '" href="' + R + a.href + '" title="' + aid + " " + esc(a.title) +
            ": " + P.LEVELS[l] + '"></a>';
        }).join("");
        var kinds = Object.keys(t.mats), opened = kinds.filter(function (k) { return seen[k + "|" + tid]; }).length;
        h.push('<tr><td><span class="aa-id">' + tid + '</span><a href="' + R + t.href + '">' + esc(t.title) + "</a></td>" +
          '<td class="aa-squares">' + squares + "</td><td>" + bar(tm.pct) + " " + tm.pct + "%</td>" +
          "<td>" + (tm.quiz == null ? "&ndash;" : tm.quiz + "%") + "</td>" +
          "<td>" + opened + " / " + kinds.length + "</td></tr>");
      });
      h.push("</table>");
    });

    h.push("<h2>Recent</h2>");
    if (!rec.recent || !rec.recent.length) h.push('<p class="aa-sub">Nothing yet.</p>');
    else {
      h.push('<table class="aa-prog">');
      rec.recent.slice(0, 25).forEach(function (r) {
        var label = KIND[r[0]] || r[0], name = r[1];
        if (M.topics[r[1]]) name = r[1] + " " + M.topics[r[1]].title;
        else if (M.atoms[r[1]]) name = r[1] + " " + M.atoms[r[1]].title;
        h.push("<tr><td>" + when(r[3]) + "</td><td>" + esc(label) + "</td><td>" + esc(name) + "</td></tr>");
      });
      h.push("</table>");
    }
    h.push('<p class="aa-links" style="margin-top:24px"><a href="' + R + 'report.html">Report card</a>' +
      '<a href="' + R + 'results.html">Skill quiz results on this device</a></p>');
    box.innerHTML = h.join("");
  }

  global.AayatProgressPage = render;
})(window);
