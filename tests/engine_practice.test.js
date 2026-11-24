const test = require("node:test");
const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");
const vm = require("node:vm");

const ROOT = path.resolve(__dirname, "..");
const DATA = path.join(ROOT, "site", "tests", "data");

function load() {
  const store = {};
  const sandbox = {
    console, Promise, Math, JSON, Date, Uint8Array,
    crypto: require("node:crypto").webcrypto,
    document: { currentScript: { getAttribute: () => "engine.js" } },
    localStorage: { getItem: (k) => (k in store ? store[k] : null), setItem: (k, v) => { store[k] = String(v); } },
    fetch: (p) => {
      const f = path.join(DATA, decodeURIComponent(p.replace(/^data\//, "")));
      return Promise.resolve(fs.existsSync(f) ? { ok: true, json: () => Promise.resolve(JSON.parse(fs.readFileSync(f, "utf8"))) } : { ok: false, status: 404 });
    }
  };
  sandbox.window = sandbox;
  vm.createContext(sandbox);
  vm.runInContext(fs.readFileSync(path.join(ROOT, "source", "static", "tests", "engine.js"), "utf8"), sandbox);
  return sandbox.Engine;
}

function bank(name) {
  return JSON.parse(fs.readFileSync(path.join(DATA, name + ".json"), "utf8"));
}

async function play(E, s, rule) {
  const asked = [];
  for (;;) {
    const q = await E.next(s);
    if (q.done) break;
    asked.push(q);
    const it = s.__bank.byId[q.question_id];
    await E.respond(s, q.question_id, rule(it) ? it.answer : Object.keys(it.choices).find((k) => k !== it.answer), 30);
  }
  return asked;
}

function withBank(s, b) {
  b.byId = {};
  b.items.forEach((it) => { b.byId[it.id] = it; });
  s.__bank = b;
  return s;
}

test("every topic has a practice bank with at least two skills, three tiers and named skills", () => {
  const idx = bank("topic/index");
  assert.ok(idx.topics.length >= 24);
  for (const t of idx.topics) {
    const b = bank("topic/" + t.id);
    assert.equal(b.items.length, t.count);
    assert.ok(b.items.length >= 24, t.id + " has enough questions");
    for (const sk of new Set(b.items.map((x) => x.skill))) for (const tier of [1, 2, 3]) {
      assert.ok(b.items.filter((x) => x.skill === sk && x.tier === tier).length >= 4, t.id + " " + sk + " tier " + tier + " has at least 4 questions");
    }
    const skills = new Set(b.items.map((x) => x.skill));
    assert.ok(skills.size >= 2, t.id + " covers two skills");
    for (const sk of skills) {
      assert.ok(b.skills[sk] && !/^\d\.[A-D]$/.test(b.skills[sk]), t.id + " names skill " + sk);
      assert.deepEqual([...new Set(b.items.filter((x) => x.skill === sk).map((x) => x.tier))].sort(), [1, 2, 3], t.id + " " + sk + " has all three tiers");
    }
    const ids = b.items.map((x) => x.id);
    assert.equal(new Set(ids).size, ids.length, t.id + " ids are unique");
    for (const it of b.items) {
      assert.ok(it.answer in it.choices, it.id + " answer is one of its choices");
      assert.equal(Object.keys(it.choices).length, 4, it.id + " has four choices");
    }
  }
});

test("a practice round stays in its topic, stops between 6 and 10 questions and names the topic's skills", async () => {
  const E = load();
  const s = withBank(E.start({ student_name: "T", student_email: "t@example.org", unit: "U1", topic: "1.1" }), bank("topic/1.1"));
  assert.equal(s.session_type, "practice");
  assert.equal(E.limits(s).max, 10);
  const asked = await play(E, s, () => true);
  assert.ok(asked.length >= 6 && asked.length <= 10, "asked " + asked.length);
  assert.ok(asked.every((q) => q.topic_refs === "1.1"));
  assert.ok(asked.every((q) => q.max_items === 10));
  const r = await E.report(s);
  assert.equal(r.session_type, "practice");
  assert.equal(r.topic, "1.1");
  assert.equal(r.skill_profile["1.A"].name, "Identify cybersecurity concepts");
  assert.ok(!r.recommendations.some((x) => /unit gate/.test(x)));
});

test("the next round starts with the weakest skill and avoids questions already answered correctly", async () => {
  const E = load();
  const b = bank("topic/1.1");
  const s1 = withBank(E.start({ student_name: "T", student_email: "t@example.org", unit: "U1", topic: "1.1" }), b);
  const first = await play(E, s1, (it) => it.skill !== "2.A");
  assert.ok(s1.theta_estimates["2.A"] < s1.theta_estimates["1.A"], "2.A came out weaker");
  const rightBefore = new Set(s1.responses.filter((r) => r.correct).map((r) => r.question_id));
  const s2 = withBank(E.start({ student_name: "T", student_email: "t@example.org", unit: "U1", topic: "1.1" }), b);
  assert.equal(s2.attempt, 2);
  assert.ok(s2.prior["2.A"] < s2.prior["1.A"], "the second round starts from the first round's estimates");
  const q = await E.next(s2);
  assert.equal(q.primary_skill, "2.A", "round two opens on the weak skill");
  const again = await play(E, Object.assign(s2, { current_qid: q.question_id }), () => true);
  const asked2 = [q.question_id].concat(again.map((x) => x.question_id)).filter((v, i, a) => a.indexOf(v) === i);
  const unseen = b.items.filter((it) => !first.some((f) => f.question_id === it.id)).length;
  if (unseen >= asked2.length) assert.ok(asked2.every((id) => !rightBefore.has(id)), "no question answered correctly last round comes back while fresh ones remain");
  const r = await E.report(s2);
  assert.ok(r.skill_profile["2.A"].before != null, "the report shows where each skill started");
});

test("item information follows the 3PL formula and peaks near the item's difficulty", () => {
  const E = load();
  const at = (t) => E._info(t, 1.2, 0.5, 0.25);
  const p = 0.25 + 0.75 / (1 + Math.exp(-1.2 * (0.5 - 0.5)));
  assert.ok(Math.abs(at(0.5) - 1.44 * ((p - 0.25) / 0.75) ** 2 * (1 - p) / p) < 1e-9);
  assert.ok(at(0.7) > at(-2) && at(0.7) > at(3), "information is highest near b, not for items far too easy or too hard");
  assert.ok(E._info(1.5, 1, -1, 0.25) < E._info(1.5, 1, 1.2, 0.25), "for a strong student a hard item tells more than an easy one");
});

test("practice never counts as a unit test, and the unit test keeps its own length and gate", async () => {
  const E = load();
  const s = withBank(E.start({ student_name: "T", student_email: "t@example.org", unit: "U1" }), bank("U1"));
  assert.equal(s.session_type, "adaptive");
  assert.equal(E.limits(s).max, 24);
  const asked = await play(E, s, () => true);
  assert.ok(asked.length >= 8 && asked.length <= 24);
  const r = await E.report(s);
  assert.ok(r.recommendations.some((x) => /unit gate/.test(x)));
  assert.equal(r.session_type, undefined);
  const prog = fs.readFileSync(path.join(ROOT, "source", "static", "assets", "theme", "progress.js"), "utf8");
  assert.match(prog, /session_type !== "practice"/);
  assert.match(fs.readFileSync(path.join(ROOT, "db", "schema.sql"), "utf8"), /in \('hw', 'practice'\)/);
});

test("answering every question right masters the topic within a few rounds", async () => {
  const E = load();
  const b = bank("topic/2.2");
  let r = null;
  for (let i = 0; i < 4 && !(r && r.mastered_all); i++) {
    const s = withBank(E.start({ student_name: "T", student_email: "m@example.org", unit: "U2", topic: "2.2" }), b);
    await play(E, s, () => true);
    r = await E.report(s);
  }
  assert.equal(r.mastered_all, true);
  assert.match(r.recommendations[0], /mastered/);
});
