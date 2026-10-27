/* interactive behavior for student activity posters */
(function () {
  "use strict";

  function esc(s) {
    return String(s == null ? "" : s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
  }

  function lsGet(key) {
    try { return localStorage.getItem(key); } catch (e) { return null; }
  }
  function lsSet(key, val) {
    try { localStorage.setItem(key, val); } catch (e) { /* no-op */ }
  }

  function setupChecklist(poster) {
    var section = poster.querySelector(".sec-steps");
    var checks = poster.querySelectorAll(".material-check");
    if (!section || checks.length === 0) {
      if (section) section.classList.remove("locked");
      return;
    }
    var storeKey = "apcyber_materials_" + poster.dataset.topicId + "_" + poster.dataset.atomId;
    var saved = {};
    try { saved = JSON.parse(lsGet(storeKey) || "{}"); } catch (e) { saved = {}; }

    function refresh() {
      var state = {};
      var allChecked = true;
      checks.forEach(function (c, i) {
        state[i] = c.checked;
        if (!c.checked) allChecked = false;
      });
      lsSet(storeKey, JSON.stringify(state));
      section.classList.toggle("locked", !allChecked);
      var notice = section.querySelector(".steps-lock-notice");
      if (notice) {
        var n = Array.prototype.filter.call(checks, function (c) { return c.checked; }).length;
        notice.textContent = allChecked
          ? "All materials ready, steps unlocked."
          : "Check off all materials above to unlock the steps (" + n + "/" + checks.length + ").";
      }
    }

    checks.forEach(function (c, i) {
      if (saved[i]) c.checked = true;
      c.addEventListener("change", refresh);
    });
    refresh();
  }

  function setupCollaborate(poster) {
    var widget = poster.querySelector(".collab-widget");
    if (!widget) return;
    var btn = widget.querySelector(".collab-submit");
    var status = widget.querySelector(".collab-status");
    btn.addEventListener("click", function () {
      var name = widget.querySelector(".collab-name").value.trim();
      var partner = widget.querySelector(".collab-partner").value.trim();
      var notes = widget.querySelector(".collab-notes").value.trim();
      if (!notes) {
        status.textContent = "Write a sentence or two before logging.";
        return;
      }
      btn.disabled = true;
      status.textContent = "Logging…";
      Identity.ensureEmail(function (email) {
        Backend.submit({
          email: email,
          topic_id: poster.dataset.topicId,
          atom_id: poster.dataset.atomId,
          kind: "collaborate_note",
          item_id: poster.dataset.atomId + ".collab",
          correct: true,
          points: 0,
          maxPoints: 0,
          status: "graded",
          response: "Partner: " + (partner || "n/a") + " — " + notes,
          explanation: name ? ("Logged by " + name) : ""
        }).then(function (ok) {
          btn.disabled = false;
          status.textContent = ok
            ? "Logged ✓"
            : "Saved on this device.";
        });
      });
    });
  }

  function renderExitState(poster, ticket) {
    var wrap = poster.querySelector(".certificate");
    var form = wrap.querySelector(".exit-form");
    var result = wrap.querySelector(".exit-result");
    if (!ticket) return;
    form.style.display = "none";
    result.style.display = "block";
    if (ticket.status === "pending") {
      result.innerHTML =
        '<div class="exit-pending">Submitted, awaiting your instructor\'s grade.</div>' +
        '<blockquote>' + esc(ticket.response) + '</blockquote>';
    } else {
      result.innerHTML =
        '<div class="exit-graded">Graded: ' + ticket.points + ' / ' + ticket.maxPoints + '</div>' +
        (ticket.feedback ? '<div class="exit-feedback">"' + esc(ticket.feedback) + '"</div>' : '') +
        '<blockquote>' + esc(ticket.response) + '</blockquote>';
    }
  }

  function setupExitTicket(poster) {
    var wrap = poster.querySelector(".certificate");
    if (!wrap) return;
    var form = wrap.querySelector(".exit-form");
    var btn = form.querySelector(".exit-submit");
    var status = form.querySelector(".exit-status");
    var itemId = poster.dataset.atomId + ".exit";
    var localKey = "apcyber_exit_" + poster.dataset.topicId + "_" + poster.dataset.atomId;

    // Best-effort local memory of a pending submission, so the certificate
    // still shows "submitted" on reload even before the backend is deployed.
    var cachedRaw = lsGet(localKey);
    if (cachedRaw) {
      try { renderExitState(poster, JSON.parse(cachedRaw)); } catch (e) { /* ignore */ }
    }

    var email = Identity.getEmail();
    if (email && Backend.isConfigured()) {
      Backend.getStudentReport(email).then(function (report) {
        if (!report || !report.exitTickets) return;
        var mine = report.exitTickets.filter(function (t) {
          return t.topic_id === poster.dataset.topicId && t.item_id === itemId;
        });
        if (mine.length) {
          var latest = mine[mine.length - 1];
          lsSet(localKey, JSON.stringify(latest));
          renderExitState(poster, latest);
        }
      });
    }

    btn.addEventListener("click", function () {
      var nameInput = form.querySelector(".exit-name");
      var response = form.querySelector(".exit-response").value.trim();
      if (!response) {
        status.textContent = "Write your response before submitting.";
        return;
      }
      btn.disabled = true;
      status.textContent = "Submitting…";
      Identity.ensureEmail(function (studentEmail) {
        if (nameInput && !nameInput.value) nameInput.value = studentEmail;
        Backend.submit({
          email: studentEmail,
          topic_id: poster.dataset.topicId,
          atom_id: poster.dataset.atomId,
          kind: "exit_ticket",
          item_id: itemId,
          correct: false,
          points: 0,
          maxPoints: 10,
          status: "pending",
          response: response,
          explanation: ""
        }).then(function () {
          var ticket = { status: "pending", response: response, points: 0, maxPoints: 10 };
          lsSet(localKey, JSON.stringify(ticket));
          renderExitState(poster, ticket);
        });
      });
    });
  }

  document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll(".poster[data-atom-id]").forEach(function (poster) {
      setupChecklist(poster);
      setupCollaborate(poster);
      setupExitTicket(poster);
    });
  });
})();
