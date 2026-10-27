/* adaptive assessment engine (runs in the browser) */
(function (global) {
  "use strict";

  var MAX_ITEMS = 24;       // hard cap per session
  var MIN_ITEMS = 8;        // fewest items before the test may stop early
  var SE_STOP = 0.40;       // stop once the overall estimate is this precise
  var GATE_THETA = 0.5;     // Proficient and above passes the unit gate
  var MASTERY_LOGIT = 0.55; // a skill counts as mastered above this
  var STEP = 0.35;          // per-skill update step
  var STORE_KEY = "apcyber_engine_sessions_v1";
  var LOCAL_KEEP = 50;      // sessions kept in one browser's storage

  var SKILL_META = {
    "1.A": { name: "Identify Concepts", color: "#3b82f6" },
    "1.B": { name: "Identify Adversary Types", color: "#6366f1" },
    "1.C": { name: "Explain Mechanisms", color: "#8b5cf6" },
    "1.D": { name: "Determine / Document Risks", color: "#a855f7" },
    "2.A": { name: "Apply Security Controls", color: "#06b6d4" },
    "2.B": { name: "Implement Controls", color: "#0891b2" },
    "3.A": { name: "Evaluate Security Posture", color: "#10b981" },
    "3.B": { name: "Analyze Incidents", color: "#14b8a6" }
  };

  /* engine/ folder, resolved from this script's own src. */
  var BASE = (function () {
    var s = document.currentScript && document.currentScript.getAttribute("src");
    return s ? s.replace(/engine\.js.*$/, "") : "";
  })();

  // ------------------------------------------------------------ IRT maths --

  function prob(theta, a, b, c) {
    return c + (1 - c) / (1 + Math.exp(-a * (theta - b)));
  }

  function info(theta, a, b, c) {
    var p = prob(theta, a, b, c);
    var d = p * (1 - p);
    if (d < 1e-9) return 0;
    return (a * a) * (p - c) * (p - c) / ((1 - c) * (1 - c) * d);
  }

  /* One gradient step on the log-likelihood (per-skill diagnostic θ). */
  function stepTheta(theta, correct, a, b, c) {
    var p = prob(theta, a, b, c);
    var g = correct
      ? a * (1 - p) * (p - c) / (Math.max(p, 1e-9) * (1 - c))
      : -a * (p - c) / Math.max(1 - c, 1e-9);
    return Math.max(-4, Math.min(4, theta + STEP * g));
  }

  /* EAP estimate of overall θ and its posterior SD from all responses. */
  function eap(responses, byId) {
    var num = 0, den = 0, sq = 0;
    for (var t = -4; t <= 4.0001; t += 0.05) {
      var w = Math.exp(-t * t / 2);
      for (var i = 0; i < responses.length; i++) {
        var it = byId[responses[i].question_id];
        if (!it) continue;
        var p = prob(t, it.a, it.b, it.c);
        w *= responses[i].correct ? p : 1 - p;
      }
      num += t * w; sq += t * t * w; den += w;
    }
    var mean = num / den;
    return { theta: mean, se: Math.sqrt(Math.max(sq / den - mean * mean, 0)) };
  }

  function thetaToLevel(theta) {
    if (theta >= 1.5) return ["Advanced", "#22c55e"];
    if (theta >= 0.5) return ["Proficient", "#3b82f6"];
    if (theta >= -0.5) return ["Developing", "#f59e0b"];
    return ["Beginning", "#ef4444"];
  }

  function thetaToPct(theta) {
    return Math.max(0, Math.min(100, Math.floor((theta + 4) / 8 * 100)));
  }

  function round(x, d) {
    var f = Math.pow(10, d);
    return Math.round(x * f) / f;
  }

  // ------------------------------------------------------------------ data --

  var cache = {};

  function getJson(path) {
    if (!cache[path]) {
      cache[path] = fetch(BASE + "data/" + path).then(function (r) {
        if (!r.ok) throw new Error("Could not load " + path + " (HTTP " + r.status + ")");
        return r.json();
      });
    }
    return cache[path];
  }

  function bank(unit) {
    return getJson(unit + ".json").then(function (d) {
      if (!d.byId) {
        d.byId = {};
        d.items.forEach(function (it) { d.byId[it.id] = it; });
      }
      return d;
    });
  }

  // -------------------------------------------------------------- storage --

  function loadStore() {
    try { return JSON.parse(localStorage.getItem(STORE_KEY) || "{}"); } catch (e) { return {}; }
  }

  function save(session) {
    var store = loadStore();
    store[session.id] = session;
    // A shared lab computer collects everyone's sessions; keep the newest.
    var ids = Object.keys(store);
    if (ids.length > LOCAL_KEEP) {
      ids.sort(function (a, b) { return (store[b].timestamp || "") < (store[a].timestamp || "") ? -1 : 1; });
      ids.slice(LOCAL_KEEP).forEach(function (id) { delete store[id]; });
    }
    try { localStorage.setItem(STORE_KEY, JSON.stringify(store)); } catch (e) { /* full or blocked */ }
    if (global.Neon && global.Neon.isConfigured()) {
      global.Neon.rpc("api_save_engine_session", { p: session }, { keepalive: true }).catch(function (err) {
        console.warn("[Engine] session not saved to Neon, kept on this device:", err);
      });
    }
  }

  function newId(prefix) {
    var b = new Uint8Array(4);
    crypto.getRandomValues(b);
    return (prefix || "") + Array.prototype.map.call(b, function (x) {
      return ("0" + x.toString(16)).slice(-2);
    }).join("").toUpperCase();
  }

  function now() { return Date.now() / 1000; }

  // ----------------------------------------------------------- selection --

  function finished(session) {
    var n = session.administered.length;
    return n >= MAX_ITEMS || (n >= MIN_ITEMS && session.overall.se < SE_STOP);
  }

  function selectNext(items, session) {
    if (finished(session)) return null;
    var given = {}, skipped = {};
    session.administered.forEach(function (id) { given[id] = true; });
    (session.skipped || []).forEach(function (id) { skipped[id] = true; });
    var pool = items.filter(function (it) { return !given[it.id] && !skipped[it.id]; });
    if (!pool.length) pool = items.filter(function (it) { return !given[it.id]; });
    if (!pool.length) return null;
    var th = session.overall.theta, best = null, bestScore = -1;
    pool.forEach(function (it) {
      // Small jitter so equally informative items rotate between students.
      var s = info(th, it.a, it.b, it.c) + Math.random() * 0.03;
      if (s > bestScore) { bestScore = s; best = it; }
    });
    return best;
  }

  // ----------------------------------------------------------- lifecycle --

  /* Begin a session. student: {student_name, student_id, student_email, unit}. */
  function start(student) {
    var session = {
      id: newId(),
      session_type: "adaptive",
      student_name: student.student_name || "Anonymous",
      student_id: student.student_id || "",
      student_email: student.student_email || "",
      unit: student.unit || "U1",
      theta_estimates: {},
      overall: { theta: 0, se: 1 },
      administered: [],
      skipped: [],
      responses: [],
      current_qid: null,
      start_time: now(),
      end_time: null,
      timestamp: new Date().toISOString(),
      done: false
    };
    save(session);
    return session;
  }

  /* The next question, or {done:true}. skip=true sets the current one aside. */
  function next(session, skip) {
    if (session.done) return Promise.resolve({ done: true });
    return bank(session.unit).then(function (d) {
      var cur = session.current_qid;
      if (skip && cur && session.administered.indexOf(cur) === -1) {
        session.skipped = (session.skipped || []).filter(function (q) { return q !== cur; }).concat([cur]);
      } else if (cur && session.administered.indexOf(cur) === -1) {
        // A reload or repeat call keeps the question already on screen.
        return question(d, d.byId[cur], session);
      }
      var it = selectNext(d.items, session);
      if (!it) {
        finish(session);
        return { done: true };
      }
      session.current_qid = it.id;
      save(session);
      return question(d, it, session);
    });
  }

  function question(d, it, session) {
    var stim = d.stimuli[it.stim] || {};
    return {
      done: false,
      question_id: it.id,
      stimulus_label: stim.label || "",
      stimulus_context: stim.context || "",
      stimulus_html: stim.html || "",
      stem: it.stem,
      choices: it.choices,
      primary_skill: it.skill,
      topic_refs: it.topic_refs,
      est_time: it.est_time,
      item_number: session.administered.length + 1,
      theta_estimates: session.theta_estimates,
      overall: session.overall
    };
  }

  function finish(session) {
    session.done = true;
    session.current_qid = null;
    session.end_time = now();
    save(session);
  }

  /* Score one answer to the question currently on screen. */
  function respond(session, qid, answer, timeTaken) {
    return bank(session.unit).then(function (d) {
      var it = d.byId[qid];
      if (!it || session.done || qid !== session.current_qid || session.administered.indexOf(qid) !== -1) {
        throw new Error("That is not the current question.");
      }
      var correct = answer === it.answer;
      var th = session.theta_estimates;

      var before = th[it.skill] || 0;
      th[it.skill] = before * (1 - it.weight) + stepTheta(before, correct, it.a, it.b, it.c) * it.weight;
      if (it.sec_skill && it.sec_weight > 0) {
        var old = th[it.sec_skill] || 0;
        th[it.sec_skill] = old * (1 - it.sec_weight) +
          stepTheta(old, correct, it.a * 0.7, it.b, it.c) * it.sec_weight;
      }

      session.administered.push(qid);
      session.skipped = (session.skipped || []).filter(function (q) { return q !== qid; });
      session.responses.push({
        question_id: qid,
        answer: answer,
        correct: correct,
        correct_answer: it.answer,
        primary_skill: it.skill,
        b_param: it.b,
        theta_before: before,
        theta_after: th[it.skill],
        time_taken: Math.round(timeTaken || 0),
        stem: it.stem,
        topic_refs: it.topic_refs
      });
      session.overall = eap(session.responses, d.byId);
      session.current_qid = null;

      var done = finished(session);
      if (done) finish(session); else save(session);
      return {
        correct: correct,
        correct_answer: it.answer,
        explanation: it.explanation,
        distractor_rationale: it.rationale,
        choices: it.choices,
        done: done,
        theta_estimates: th,
        overall: session.overall,
        n_answered: session.administered.length
      };
    });
  }

  // -------------------------------------------------------------- reports --

  function overallSummary(session) {
    var o = session.overall || { theta: 0, se: 1 };
    var lv = thetaToLevel(o.theta);
    return {
      theta: round(o.theta, 3), se: round(o.se, 3), pct: thetaToPct(o.theta),
      level: lv[0], level_color: lv[1], meets_gate: o.theta >= GATE_THETA
    };
  }

  function fmtTime(sec) {
    sec = Math.floor(sec);
    return Math.floor(sec / 60) + "m " + ("0" + (sec % 60)).slice(-2) + "s";
  }

  /* Student / tutor report for a session (same fields the old server sent,
     plus `overall`). */
  function report(session) {
    return bank(session.unit).then(function (d) {
      var resp = session.responses || [];
      var n = resp.length;
      var correct = resp.filter(function (r) { return r.correct; }).length;
      var elapsed = (session.end_time || now()) - session.start_time;

      var skills = {};
      Object.keys(session.theta_estimates || {}).forEach(function (sk) {
        var theta = session.theta_estimates[sk];
        var meta = SKILL_META[sk] || { name: sk, color: "#94a3b8" };
        var mine = resp.filter(function (r) { return r.primary_skill === sk; });
        var lv = thetaToLevel(theta);
        skills[sk] = {
          skill: sk, name: meta.name, color: meta.color,
          theta: round(theta, 3), pct: thetaToPct(theta),
          level: lv[0], level_color: lv[1],
          mastered: theta >= MASTERY_LOGIT && mine.length >= 2,
          n_items: mine.length,
          n_correct: mine.filter(function (r) { return r.correct; }).length
        };
      });
      var list = Object.keys(skills).map(function (k) { return skills[k]; });
      var strengths = list.filter(function (s) { return s.theta >= 0.5; })
        .sort(function (a, b) { return b.theta - a.theta; });
      var gaps = list.filter(function (s) { return s.theta < 0; })
        .sort(function (a, b) { return a.theta - b.theta; });

      var items = [];
      resp.forEach(function (r, i) {
        var it = d.byId[r.question_id];
        if (!it) return;
        var b = it.b;
        var diff = b >= 1 ? ["Hard", "#ef4444"] : b >= 0.3 ? ["Medium", "#f59e0b"] : ["Easy", "#22c55e"];
        var stem = it.stem || "";
        items.push({
          seq: i + 1,
          question_id: r.question_id,
          stem: stem.length > 120 ? stem.slice(0, 120) + "…" : stem,
          full_stem: stem,
          answer: r.answer,
          correct_answer: it.answer,
          correct: r.correct,
          primary_skill: it.skill,
          diff_label: diff[0], diff_col: diff[1],
          b_param: round(b, 2),
          theta_before: round(r.theta_before || 0, 3),
          theta_after: round(r.theta_after || 0, 3),
          explanation: it.explanation,
          distractor_rationale: it.rationale,
          choices: it.choices,
          topic_refs: it.topic_refs,
          stimulus_label: (d.stimuli[it.stim] || {}).label || ""
        });
      });

      var overall = overallSummary(session);
      var recs = [];
      if (session.done) {
        recs.push(overall.meets_gate
          ? "Meets the unit gate: overall θ = " + overall.theta.toFixed(2) + " (" + overall.level + ")."
          : "Below the unit gate (Proficient, θ ≥ 0.50): overall θ = " + overall.theta.toFixed(2) +
            ". Book a tutoring session before moving on.");
      }
      gaps.forEach(function (s) {
        recs.push("Focus on **" + s.name + "** (θ = " + s.theta.toFixed(2) + "): student answered " +
          s.n_correct + "/" + s.n_items + " items correctly, review core concepts and re-test with easier items.");
      });
      list.forEach(function (s) {
        if (s.n_items < 2) {
          recs.push("Insufficient data for **" + s.name + "**, fewer than 2 items administered. " +
            "Schedule a focused session on this skill.");
        }
      });

      return {
        session_id: session.id,
        student_name: session.student_name,
        student_id: session.student_id || "",
        student_email: session.student_email || "",
        unit: session.unit,
        done: !!session.done,
        overall: overall,
        summary: {
          total: n,
          correct: correct,
          accuracy_pct: n ? round(correct / n * 100, 1) : 0,
          elapsed_sec: Math.floor(elapsed),
          elapsed_fmt: fmtTime(elapsed),
          avg_sec: n ? round(elapsed / n, 1) : 0
        },
        skill_profile: skills,
        strengths: strengths.map(function (s) { return s.name; }),
        gaps: gaps.map(function (s) { return s.name; }),
        items: items,
        recommendations: recs
      };
    });
  }

  // ------------------------------------------------------ CW/HW + tutor --

  /* Save a finished CW/HW quiz (built by engine/hw/quiz.html). */
  function saveHw(record) {
    var session = Object.assign({}, record, {
      id: newId("HW-"),
      session_type: "hw",
      timestamp: new Date().toISOString(),
      done: true
    });
    save(session);
    return session;
  }

  function accuracy(s) {
    var r = s.responses || [];
    if (!r.length) return 0;
    return Math.round(r.filter(function (x) { return x.correct; }).length / r.length * 100);
  }

  function skillProfile(s) {
    var out = {};
    Object.keys(s.theta_estimates || {}).forEach(function (sk) {
      var theta = s.theta_estimates[sk];
      var n = (s.responses || []).filter(function (r) { return r.primary_skill === sk; }).length;
      out[sk] = {
        theta: theta,
        name: (SKILL_META[sk] || {}).name || sk,
        level: thetaToLevel(theta)[0],
        mastered: theta >= MASTERY_LOGIT && n >= 2
      };
    });
    return out;
  }

  /* One flat row per session for the tutor dashboard. */
  function normalize(s) {
    var hw = s.session_type === "hw";
    var elapsed = s.elapsed_sec ||
      (s.start_time ? Math.floor((s.end_time || now()) - s.start_time) : 0);
    return {
      id: s.id || "",
      session_type: s.session_type || "adaptive",
      name: s.student_name || s.name || "",
      email: s.student_email || s.email || "",
      unit: s.unit || "",
      topic_id: s.topic_id || "",
      n_answered: s.n_answered || (s.administered || []).length || (s.responses || []).length,
      accuracy_pct: hw && s.accuracy_pct != null ? s.accuracy_pct : accuracy(s),
      elapsed_sec: elapsed,
      done: !!s.done,
      overall: hw ? null : overallSummary(s),
      skill_profile: skillProfile(s),
      responses: (s.responses || []).map(function (r) {
        return Object.assign({}, r, { skill: r.primary_skill || r.skill });
      }),
      timestamp: s.timestamp || (s.start_time ? new Date(s.start_time * 1000).toISOString() : "")
    };
  }

  /* Every session: the shared database when Neon is configured, otherwise
     this browser's own. Resolves {source, sessions}. */
  function listSessions() {
    var local = function () {
      var store = loadStore();
      return Object.keys(store).map(function (k) { return store[k]; });
    };
    var sorted = function (list) {
      return list.map(normalize).sort(function (a, b) { return a.timestamp < b.timestamp ? 1 : -1; });
    };
    if (!(global.Neon && global.Neon.isConfigured())) {
      return Promise.resolve({ source: "local", sessions: sorted(local()) });
    }
    return global.Neon.rpc("api_engine_sessions", {}).then(function (rows) {
      return { source: "neon", sessions: sorted(rows || []) };
    }).catch(function (err) {
      console.warn("[Engine] Neon unavailable, showing this device's sessions:", err);
      return { source: "local", sessions: sorted(local()) };
    });
  }

  global.Engine = {
    MAX_ITEMS: MAX_ITEMS,
    SKILL_META: SKILL_META,
    units: function () { return getJson("units.json"); },
    hwIndex: function () { return getJson("hw/index.json"); },
    hwTopic: function (tid) { return getJson("hw/" + encodeURIComponent(tid) + ".json"); },
    start: start,
    next: next,
    respond: respond,
    report: report,
    saveHw: saveHw,
    listSessions: listSessions,
    // exposed for tests
    _eap: eap,
    _info: info
  };
})(window);
