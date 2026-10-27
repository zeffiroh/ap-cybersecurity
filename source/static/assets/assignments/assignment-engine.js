/* practice-question runner (mcq/multi/short) */
(function (global) {
  "use strict";

  function normalizeShort(s) {
    return (s || "").trim().toLowerCase().replace(/[^\w\s]/g, "").replace(/\s+/g, " ");
  }

  function gradeItem(item, response) {
    if (item.type === "mcq") {
      var correct = Number(response) === Number(item.answer);
      return { correct: correct, points: correct ? item.points : 0 };
    }
    if (item.type === "multi") {
      var chosen = (response || []).slice().sort();
      var expected = (item.answer || []).slice().sort();
      var correct2 = JSON.stringify(chosen) === JSON.stringify(expected);
      return { correct: correct2, points: correct2 ? item.points : 0 };
    }
    if (item.type === "short") {
      var norm = normalizeShort(response);
      var accept = (item.accept || []).map(normalizeShort);
      var correct3 = accept.some(function (a) { return norm.indexOf(a) !== -1 || a.indexOf(norm) !== -1; }) && norm.length > 0;
      return { correct: correct3, points: correct3 ? item.points : 0 };
    }
    return { correct: false, points: 0 };
  }

  function renderCard(item, container, topicId, email) {
    var card = document.createElement("div");
    card.className = "pq-card";

    var meta = document.createElement("div");
    meta.className = "pq-meta";
    meta.textContent = item.atom_id + " · " + item.points + " pt" + (item.points === 1 ? "" : "s");
    card.appendChild(meta);

    var prompt = document.createElement("p");
    prompt.className = "pq-prompt";
    prompt.textContent = item.prompt;
    card.appendChild(prompt);

    var response = item.type === "multi" ? [] : null;
    var optionsWrap = null;
    var shortInput = null;

    if (item.type === "mcq" || item.type === "multi") {
      optionsWrap = document.createElement("div");
      optionsWrap.className = "pq-options";
      (item.options || []).forEach(function (opt, idx) {
        var optEl = document.createElement("div");
        optEl.className = "pq-option";
        optEl.textContent = opt;
        optEl.addEventListener("click", function () {
          if (card.dataset.locked) return;
          if (item.type === "mcq") {
            response = idx;
            Array.prototype.forEach.call(optionsWrap.children, function (c) { c.classList.remove("selected"); });
            optEl.classList.add("selected");
          } else {
            var pos = response.indexOf(idx);
            if (pos === -1) { response.push(idx); optEl.classList.add("selected"); }
            else { response.splice(pos, 1); optEl.classList.remove("selected"); }
          }
        });
        optionsWrap.appendChild(optEl);
      });
      card.appendChild(optionsWrap);
    } else if (item.type === "short") {
      shortInput = document.createElement("input");
      shortInput.type = "text";
      shortInput.className = "pq-short-input";
      shortInput.placeholder = "Type your answer…";
      card.appendChild(shortInput);
    }

    var btn = document.createElement("button");
    btn.className = "pq-check-btn";
    btn.textContent = "Check Answer";
    card.appendChild(btn);

    var feedback = document.createElement("div");
    feedback.className = "pq-feedback";
    card.appendChild(feedback);

    btn.addEventListener("click", function () {
      var finalResponse = item.type === "short" ? shortInput.value : response;
      if (finalResponse === null || finalResponse === "" || (Array.isArray(finalResponse) && finalResponse.length === 0)) {
        return;
      }
      var result = gradeItem(item, finalResponse);
      card.dataset.locked = "1";
      btn.disabled = true;

      if (optionsWrap) {
        Array.prototype.forEach.call(optionsWrap.children, function (c, idx) {
          var isCorrectOpt = item.type === "mcq" ? idx === item.answer : (item.answer || []).indexOf(idx) !== -1;
          if (isCorrectOpt) c.classList.add("correct");
          else if (c.classList.contains("selected")) c.classList.add("incorrect");
        });
      }
      if (shortInput) shortInput.disabled = true;

      feedback.classList.add("show", result.correct ? "correct" : "incorrect");
      feedback.textContent = (result.correct ? "Correct. " : "Not quite. ") + (item.explain || "");

      Backend.submit({
        email: email,
        topic_id: topicId,
        atom_id: item.atom_id,
        kind: "practice_question",
        item_id: item.id,
        correct: result.correct,
        points: result.points,
        maxPoints: item.points,
        response: Array.isArray(finalResponse) ? JSON.stringify(finalResponse) : String(finalResponse),
        explanation: item.explain || ""
      });
    });

    container.appendChild(card);
  }

  var AssignmentEngine = {
    /** Renders every practice item into `container` (a DOM node), gated
     *  behind Identity.ensureEmail so submissions are attributable. */
    renderPracticeItems: function (items, container, topicId) {
      Identity.ensureEmail(function (email) {
        items.forEach(function (item) { renderCard(item, container, topicId, email); });
      });
    }
  };

  global.AssignmentEngine = AssignmentEngine;
})(window);
