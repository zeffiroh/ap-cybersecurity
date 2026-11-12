const test = require("node:test");
const assert = require("node:assert");
const fs = require("fs");
const path = require("path");
const vm = require("vm");

const ROOT = path.resolve(__dirname, "..");
const THEME = path.join(ROOT, "source", "static", "assets", "theme");
const CASES = path.join(ROOT, "source", "static", "assets", "linux", "cases");

function load() {
  const sandbox = { console, URL, TextEncoder, TextDecoder, document: { currentScript: null } };
  sandbox.window = sandbox;
  vm.createContext(sandbox);
  for (const n of ["tools.js", "tool-siem.js", "tool-sigma.js"]) vm.runInContext(fs.readFileSync(path.join(THEME, n), "utf8"), sandbox);
  return sandbox.AayatTools.get("sigma");
}

function caseFiles(id) {
  const base = path.join(CASES, id, "case"), out = {};
  (function walk(d) {
    for (const e of fs.readdirSync(d, { withFileTypes: true })) {
      const p = path.join(d, e.name);
      if (e.isDirectory()) walk(p);
      else {
        const t = fs.readFileSync(p, "utf8");
        if (t.indexOf("\u0000") < 0) out[path.relative(base, p).split(path.sep).join("/")] = t;
      }
    }
  })(base);
  return out;
}

const S = load();
const evs = S.events(caseFiles("phish"));

function hits(rule, ls = true) { return S.run(S.compile(rule), evs, ls).hits; }

test("the YAML reader handles lists, maps in lists, quotes and block text", () => {
  const d = S.yaml("title: 'It''s a test'\ntags:\n  - attack.t1053\n  - \"x\\ty\"\ndetection:\n  sel:\n    - A: 1\n      B: [x, 'y z']\n    - C: null\n  condition: sel\ndescription: |\n  line one\n  line two\n");
  assert.strictEqual(d.title, "It's a test");
  assert.deepStrictEqual(Array.from(d.tags), ["attack.t1053", "x\ty"]);
  assert.strictEqual(d.detection.sel[0].B[1], "y z");
  assert.strictEqual(d.detection.sel[1].C, null);
  assert.strictEqual(d.description, "line one\nline two\n");
});

test("event logs and other logs both become events", () => {
  assert.ok(evs.filter((e) => e._kind === "windows").length >= 120);
  assert.ok(evs.some((e) => /proxy/.test(e._src)));
});

test("the starter-style rule finds the scheduled task from a public folder", () => {
  const rule = "title: t\nlogsource:\n  product: windows\ndetection:\n  selection:\n    EventID: 4698\n  odd:\n    Action|contains:\n      - '\\Users\\Public\\'\n  condition: selection and odd\n";
  const h = hits(rule);
  assert.ok(h.length >= 1);
  assert.ok(h.every((e) => e.EventID === 4698 && /Users\\Public/i.test(e.Action)));
});

test("not, 1 of, all of them and wildcards work", () => {
  const all = hits("title: t\nlogsource:\n  product: windows\ndetection:\n  a:\n    EventID: 4624\n  condition: a\n");
  const notA = hits("title: t\nlogsource:\n  product: windows\ndetection:\n  a:\n    EventID: 4624\n  b:\n    EventID: 4625\n  condition: not a and not b\n");
  const either = hits("title: t\nlogsource:\n  product: windows\ndetection:\n  sel_a:\n    EventID: 4624\n  sel_b:\n    EventID: 4625\n  condition: 1 of sel_*\n");
  const windows = evs.filter((e) => e._kind === "windows").length;
  const b = hits("title: t\nlogsource:\n  product: windows\ndetection:\n  b:\n    EventID: 4625\n  condition: b\n").length;
  assert.strictEqual(either.length, all.length + b);
  assert.strictEqual(notA.length, windows - all.length - b);
  const wild = hits("title: t\nlogsource:\n  product: windows\ndetection:\n  a:\n    Computer: 'HR-PC0?.*'\n  condition: a\n");
  assert.ok(wild.length > 0);
});

test("keywords search the raw event, and logsource off searches every log", () => {
  const h = hits("title: t\nlogsource:\n  category: proxy\ndetection:\n  kw:\n    - '.docm'\n  condition: kw\n", false);
  assert.ok(h.length >= 1);
});

test("bad rules give a clear message", () => {
  assert.throws(() => S.compile("title: t\ndetection:\n  a:\n    X: 1\n  condition: b\n"), /no search with that name/);
  assert.throws(() => S.compile("title: t\ndetection:\n  a:\n    X|base64: 1\n  condition: a\n"), /isn't supported/);
  assert.throws(() => S.compile("title: t\ndetection:\n  a:\n    X: 1\n  condition: a | count() > 5\n"), /Aggregations/);
  assert.throws(() => S.compile("title: t\n"), /detection/);
});

test("cidr, re and numeric comparisons", () => {
  const ev = [{ ip: "10.20.0.14", n: "12", c: "powershell -enc AAA", _raw: "", _kind: "other", _src: "x", _key: "x#1" }];
  const one = (sel) => S.run(S.compile("title: t\ndetection:\n  a:\n" + sel + "\n  condition: a\n"), ev, false).hits.length;
  assert.strictEqual(one("    ip|cidr: 10.20.0.0/16"), 1);
  assert.strictEqual(one("    ip|cidr: 10.21.0.0/16"), 0);
  assert.strictEqual(one("    n|gt: 10"), 1);
  assert.strictEqual(one("    c|re: '-e(nc)?\\s'"), 1);
  assert.strictEqual(one("    c|contains|all:\n      - powershell\n      - '-enc'"), 1);
  assert.strictEqual(one("    c|windash|contains: '-enc'"), 1);
});
