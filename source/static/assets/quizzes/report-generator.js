/* Quiz Report Generator */

const QuizReport = (() => {
  function escapeHtml(s) {
    return (s || "").toString().replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
  }

  function generate({ questions, answers, config }) {
    const total = questions.length;
    const correctCount = Object.values(answers).filter(a => a.correct).length;
    const pct = total ? Math.round((correctCount / total) * 100) : 0;

    const bySkill = {};
    questions.forEach(q => {
      const skill = q.skill_code || "Unclassified";
      if (!bySkill[skill]) bySkill[skill] = { correct: 0, total: 0, name: q.skill_name || "" };
      const ans = answers[q.id];
      if (ans) {
        bySkill[skill].total++;
        if (ans.correct) bySkill[skill].correct++;
      }
    });

    const skillRows = Object.entries(bySkill).map(([skill, s]) => {
      const skillPct = s.total ? Math.round((s.correct / s.total) * 100) : 0;
      return `<tr><td>${escapeHtml(skill)}</td><td>${escapeHtml(s.name)}</td><td>${s.correct}/${s.total}</td><td>${skillPct}%</td></tr>`;
    }).join("");

    const questionRows = questions.map((q, i) => {
      const ans = answers[q.id];
      const verdict = ans ? (ans.correct ? '<span class="ok">CORRECT</span>' : '<span class="bad">INCORRECT</span>') : '<span class="skip">SKIPPED</span>';
      const choicesHtml = (q.choices || []).map(c => {
        const isAnswer = c.key === q.answer_key;
        const wasSelected = ans && ans.selectedKey === c.key;
        let cls = "";
        if (isAnswer) cls = "correct-choice";
        else if (wasSelected) cls = "wrong-choice";
        const rationale = q.distractor_rationale && q.distractor_rationale[c.key]
          ? `<div class="rationale">${escapeHtml(q.distractor_rationale[c.key])}</div>` : "";
        return `<div class="choice ${cls}">${escapeHtml(c.key)}. ${escapeHtml(c.text)}${wasSelected ? ' <em>(selected)</em>' : ''}${rationale}</div>`;
      }).join("");

      return `
        <div class="question-report">
          <div class="qr-head"><strong>Q${i + 1}.</strong> ${verdict} &middot; Skill ${escapeHtml(q.skill_code || '—')} &middot; ${escapeHtml(q.lo_ref || '')}</div>
          <div class="qr-stem">${escapeHtml(q.stem)}</div>
          <div class="qr-choices">${choicesHtml}</div>
          <div class="qr-explanation"><strong>Explanation:</strong> ${escapeHtml(q.explanation || '')}</div>
        </div>`;
    }).join("");

    const html = `<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Quiz Report, ${escapeHtml(config.title)}</title>
<style>
  body { font-family: Georgia, "Times New Roman", serif; max-width: 820px; margin: 40px auto; padding: 0 20px; color: #1a1a1a; line-height: 1.6; }
  h1 { font-family: Arial, sans-serif; font-size: 24px; border-bottom: 2px solid #800000; padding-bottom: 10px; }
  .score-summary { font-family: Arial, sans-serif; font-size: 36px; font-weight: 700; color: #800000; margin: 20px 0; }
  .score-summary span { font-size: 16px; color: #555; font-weight: 400; }
  table { width: 100%; border-collapse: collapse; margin: 20px 0; font-family: Arial, sans-serif; font-size: 13px; }
  th, td { text-align: left; padding: 6px 10px; border-bottom: 1px solid #ddd; }
  th { text-transform: uppercase; font-size: 10.5px; letter-spacing: 0.05em; color: #555; }
  .question-report { border-top: 1px solid #ddd; padding: 16px 0; }
  .qr-head { font-family: Arial, sans-serif; font-size: 12px; color: #555; margin-bottom: 6px; }
  .qr-head .ok { color: #1f6d3a; font-weight: 700; }
  .qr-head .bad { color: #a9141f; font-weight: 700; }
  .qr-head .skip { color: #999; font-weight: 700; }
  .qr-stem { font-size: 15px; margin-bottom: 10px; }
  .choice { font-size: 13px; margin-bottom: 6px; padding: 6px 10px; border-radius: 3px; }
  .choice.correct-choice { background: #eaf7ee; border-left: 3px solid #1f6d3a; }
  .choice.wrong-choice { background: #fdeceb; border-left: 3px solid #a9141f; }
  .rationale { font-size: 11.5px; color: #666; margin-top: 3px; font-style: italic; }
  .qr-explanation { font-size: 13px; color: #444; margin-top: 10px; }
  @media print { body { margin: 10px auto; } }
</style>
</head>
<body>
<h1>Quiz Report, ${escapeHtml(config.title)}</h1>
<p>${escapeHtml(config.subtitle || "")} &middot; Generated ${new Date().toLocaleString()}</p>
<div class="score-summary">${correctCount} / ${total} <span>(${pct}%)</span></div>
<h3>Score by Skill</h3>
<table>
  <tr><th>Skill</th><th>Learning Objective</th><th>Score</th><th>Percent</th></tr>
  ${skillRows}
</table>
<h3>Question-by-Question Analysis</h3>
${questionRows}
</body>
</html>`;

    const blob = new Blob([html], { type: "text/html" });
    const a = document.createElement("a");
    a.href = URL.createObjectURL(blob);
    a.download = `Quiz_Report_${(config.title || "quiz").replace(/\s+/g, "_")}.html`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
  }

  return { generate };
})();
