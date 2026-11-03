(function (global) {
  "use strict";

  var P, rows = [], codes = [], armed = "";
  var $ = function (id) { return document.getElementById(id); };

  function esc(s) {
    return String(s == null ? "" : s).replace(/[&<>"]/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c];
    });
  }
  function when(iso) {
    var d = new Date(iso);
    return iso && !isNaN(d) ? d.toLocaleDateString(undefined, { month: "short", day: "numeric" }) : "&ndash;";
  }

  function call(fn, args) {
    return P.neon().then(function (db) {
      if (!db) throw new Error("The course database is not connected yet.");
      return db.rpc(fn, args || {}, { attempts: 1 });
    });
  }

  function load() {
    $("status").textContent = "Loading…";
    return call("api_teacher_students").then(function (d) {
      rows = d.students || [];
      codes = d.codes || [];
      var n = rows.filter(function (r) { return !r.teacher; }).length;
      $("status").textContent = n + " student" + (n === 1 ? "" : "s") + " · updated " +
        new Date(d.generatedAt).toLocaleTimeString();
      draw();
      drawCodes();
    }).catch(function (e) { $("status").textContent = "Could not load: " + e.message; });
  }

  function access(r) {
    if (r.teacher) return "Teacher";
    if (!r.unlocked) return "Locked";
    return "Unlocked" + (r.via ? " (" + esc(r.via) + ")" : "");
  }

  function password(r) {
    if (!r.account) return "No account yet";
    if (r.locked) return "Locked out (too many tries)";
    return r.starter ? "Starter (lock&amp;key)" : "Their own";
  }

  function button(act, email, label) {
    var hot = armed === act + "|" + email;
    return '<button class="btn" data-act="' + act + '" data-email="' + esc(email) + '">' +
      (hot ? "Click again to confirm" : label) + "</button>";
  }

  function draw() {
    var q = $("q").value.trim().toLowerCase();
    var list = rows.filter(function (r) { return !q || r.email.indexOf(q) !== -1; });
    var h = ["<table class='aa-grid-t'><tr><th>Student</th><th>Access</th><th>Password</th><th>Joined</th>" +
      "<th>Last active</th><th></th></tr>"];
    list.forEach(function (r) {
      var acts = r.teacher ? "" :
        (r.account ? button("reset", r.email, "Reset password") + " " : "") +
        (r.unlocked ? button("lock", r.email, "Take away access") : button("unlock", r.email, "Give access")) + " " +
        button("remove", r.email, "Remove");
      h.push('<tr><td class="aa-who">' + esc(r.email) + "</td><td>" + access(r) + "</td><td>" + password(r) +
        "</td><td>" + when(r.joined) + "</td><td>" + when(r.last) + '</td><td style="text-align:left">' + acts + "</td></tr>");
    });
    h.push("</table>");
    if (!list.length) h.push('<p class="aa-sub">No students yet.</p>');
    $("grid").innerHTML = h.join("");
    $("grid").querySelectorAll("button[data-act]").forEach(function (b) {
      b.addEventListener("click", function () { act(b.getAttribute("data-act"), b.getAttribute("data-email")); });
    });
  }

  var ACTIONS = {
    reset: ["api_teacher_reset_password", function (e) { return { p_email: e }; },
      "Password reset. They sign in with lock&key and choose a new one."],
    lock: ["api_teacher_set_unlock", function (e) { return { p_email: e, p_on: false }; }, "Access taken away."],
    unlock: ["api_teacher_set_unlock", function (e) { return { p_email: e, p_on: true }; }, "Full course access given."],
    remove: ["api_teacher_remove_student", function (e) { return { p_email: e }; },
      "Removed, with their progress and grades. Payment records are kept."]
  };

  function act(kind, email) {
    var key = kind + "|" + email;
    if (kind !== "unlock" && armed !== key) { armed = key; draw(); return; }
    armed = "";
    var a = ACTIONS[kind];
    $("status").textContent = "Working…";
    call(a[0], a[1](email)).then(function (r) {
      if (!r || !r.ok) throw new Error((r && r.error) || "That didn't work.");
      return load().then(function () { $("status").textContent = email + ": " + a[2]; });
    }).catch(function (e) { $("status").textContent = e.message; draw(); });
  }

  function add() {
    var email = $("add-email").value.trim().toLowerCase();
    $("add-msg").textContent = "Adding…";
    call("api_teacher_add_student", { p_email: email, p_unlock: $("add-unlock").checked }).then(function (r) {
      if (!r || !r.ok) throw new Error((r && r.error) || "That didn't work.");
      $("add-email").value = "";
      $("add-msg").textContent = "Added " + email + ". Starter password: lock&key";
      return load();
    }).catch(function (e) { $("add-msg").textContent = e.message; });
  }

  function drawCodes() {
    var live = codes.filter(function (c) { return c.usesLeft > 0; });
    if (!live.length) { $("codes").innerHTML = '<p class="aa-sub">No codes with uses left.</p>'; return; }
    $("codes").innerHTML = "<table class='aa-grid-t'><tr><th>Code</th><th>Uses left</th><th>Note</th><th>Made</th><th></th></tr>" +
      live.map(function (c) {
        return '<tr><td class="aa-who"><b>' + esc(c.code) + "</b></td><td>" + c.usesLeft + "</td><td>" + esc(c.note) +
          "</td><td>" + when(c.created) + '</td><td><button class="btn" data-end="' + esc(c.code) + '">' +
          (armed === "end|" + c.code ? "Click again to confirm" : "End code") + "</button></td></tr>";
      }).join("") + "</table>";
    $("codes").querySelectorAll("button[data-end]").forEach(function (b) {
      b.addEventListener("click", function () {
        var code = b.getAttribute("data-end");
        if (armed !== "end|" + code) { armed = "end|" + code; drawCodes(); return; }
        armed = "";
        call("api_teacher_end_code", { p_code: code }).then(load).catch(function (e) { $("code-msg").textContent = e.message; });
      });
    });
  }

  function make() {
    $("code-msg").textContent = "Making…";
    call("api_teacher_make_code", { p_note: $("code-note").value, p_uses: Number($("code-uses").value) || 1 }).then(function (r) {
      if (!r || !r.ok) throw new Error((r && r.error) || "That didn't work.");
      $("code-msg").innerHTML = "New code: <b>" + esc(r.code) + "</b>";
      $("code-note").value = "";
      return load();
    }).catch(function (e) { $("code-msg").textContent = e.message; });
  }

  function start() {
    P = global.AayatProgress;
    $("q").addEventListener("input", draw);
    $("reload").addEventListener("click", load);
    $("add").addEventListener("click", add);
    $("make").addEventListener("click", make);
    load();
  }
  if (document.readyState === "complete") start();
  else document.addEventListener("DOMContentLoaded", start);
})(window);
