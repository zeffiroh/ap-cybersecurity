const test = require("node:test");
const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");
const vm = require("node:vm");

const ROOT = path.resolve(__dirname, "..");
const THEME = path.join(ROOT, "source", "static", "assets", "theme");
const CASES = path.join(ROOT, "source", "static", "assets", "linux", "cases");

function load() {
  const ctx = { window: {} };
  vm.createContext(ctx);
  vm.runInContext(fs.readFileSync(path.join(THEME, "tools.js"), "utf8"), ctx);
  vm.runInContext(fs.readFileSync(path.join(THEME, "tool-siem.js"), "utf8"), ctx);
  return ctx.window.AayatTools;
}

function caseFiles(id) {
  const dir = path.join(CASES, id, "case"), out = {};
  (function walk(d) {
    for (const n of fs.readdirSync(d)) {
      const p = path.join(d, n);
      if (fs.statSync(p).isDirectory()) walk(p);
      else {
        const body = fs.readFileSync(p).toString("utf8");
        if (!body.includes("\u0000")) out[path.relative(dir, p).split(path.sep).join("/")] = body;
      }
    }
  })(dir);
  return out;
}

const T = load();
const S = T.get("siem");
const E = S.engine;
const go = (idx, q) => E.run(idx, q);
const plain = (v) => JSON.parse(JSON.stringify(v));

test("registers as a console tool", () => {
  assert.equal(S.id, "siem");
  assert.equal(S.title, "SIEM search");
  assert.equal(S.console, true);
  assert.ok(T.list().some((d) => d.id === "siem"));
});

test("reads every kind of case log into events with fields", () => {
  const all = {};
  for (const id of fs.readdirSync(CASES)) {
    if (!fs.existsSync(path.join(CASES, id, "case"))) continue;
    const idx = E.index(caseFiles(id));
    for (const s of idx.sources) all[s.sourcetype] = (all[s.sourcetype] || 0) + 1;
    for (const e of idx.events) {
      assert.equal(typeof e._raw, "string");
      assert.equal(e.index, "main");
      assert.ok(e.source);
    }
  }
  for (const t of ["access_combined", "syslog", "squid", "proxy", "dns_query", "openvpn", "csv", "json", "generic"]) assert.ok(all[t], "no " + t + " source found");
});

test("web01: brute force then a login, found with search and stats", () => {
  const idx = E.index(caseFiles("web01"));
  const failed = go(idx, "sourcetype=syslog action=failure");
  assert.ok(failed.n > 0);
  assert.ok(failed.rows.every((e) => e.action === "failure"));
  const by = go(idx, "action=failure | stats count by src_ip | sort - count");
  assert.equal(by.table, true);
  assert.deepEqual(plain(by.cols), ["src_ip", "count"]);
  assert.equal(by.rows[0].src_ip, "203.0.113.7");
  const ok = go(idx, 'Accepted src_ip=203.0.113.7 | table _time user auth_method');
  assert.equal(ok.n, 1);
  assert.equal(ok.rows[0].user, "deploy");
  assert.equal(ok.rows[0].auth_method, "password");
  const sudo = go(idx, "process=sudo | table user run_as command");
  assert.equal(sudo.rows[0].command, "/bin/cat /etc/shadow");
});

test("keywords match whole words, with * as a wildcard", () => {
  const idx = E.index(caseFiles("web01"));
  assert.equal(go(idx, "source=auth.log fail").n, 0);
  assert.ok(go(idx, "source=auth.log fail*").n > 0);
  assert.equal(go(idx, "source=auth.log Failed").n, go(idx, "source=auth.log fail*").n);
  assert.ok(go(idx, "203.0.113.7").n > 0);
  assert.ok(go(idx, '"Failed password"').n > 0);
});

test("access log fields, comparisons, OR, NOT and top", () => {
  const idx = E.index(caseFiles("web01"));
  const all = go(idx, "sourcetype=access_combined");
  const errs = go(idx, "sourcetype=access_combined status>=400");
  assert.ok(errs.rows.every((e) => Number(e.status) >= 400));
  const notErr = go(idx, "sourcetype=access_combined NOT status>=400");
  assert.equal(errs.n + notErr.n, all.n);
  const either = go(idx, "sourcetype=access_combined (clientip=203.0.113.7 OR clientip=198.51.100.20)");
  assert.equal(either.n, go(idx, "sourcetype=access_combined clientip=203.0.113.7").n + go(idx, "sourcetype=access_combined clientip=198.51.100.20").n);
  const top = go(idx, "sourcetype=access_combined | top limit=1 useragent");
  assert.deepEqual(plain(top.cols), ["useragent", "count", "percent"]);
  assert.equal(top.n, 1);
  const rare = go(idx, "sourcetype=access_combined | rare limit=1 clientip");
  assert.ok(rare.rows[0].count <= top.rows[0].count);
});

test("stats functions: dc, sum, avg, min, max, values", () => {
  const idx = E.index(caseFiles("insider"));
  const r = go(idx, "source=proxy.log | stats count, dc(dest_host) as hosts, sum(bytes_out) as out, avg(bytes_out), min(bytes_out), max(bytes_out), values(user) as users");
  assert.equal(r.n, 1);
  const row = r.rows[0];
  assert.equal(row.count, 4);
  assert.equal(row.hosts, 3);
  const raw = caseFiles("insider")["proxy.log"];
  const want = [...raw.matchAll(/bytes_out=(\d+)/g)].reduce((a, m) => a + Number(m[1]), 0);
  assert.equal(row.out, want);
  assert.equal(row["max(bytes_out)"], 1932735283);
  assert.deepEqual(plain(row.users), ["r.menon"]);
  assert.equal(row["avg(bytes_out)"], row.out / 4);
});

test("CSV and JSON logs become fields; times come from the time column", () => {
  const idx = E.index(caseFiles("insider"));
  const badge = go(idx, "source=badge.csv result=denied | table _time user door");
  for (const row of badge.rows) assert.equal(typeof row._time, "number");
  const dlp = go(idx, "source=dlp_alerts.json severity=high | stats count by rule");
  assert.ok(dlp.n > 0);
  const multi = go(idx, "source=dlp_alerts.json sample=*thrust* | head 1");
  assert.equal(multi.n, 1);
  assert.ok(Array.isArray(multi.rows[0].sample));
});

test("timechart buckets by span and splits by a field", () => {
  const idx = E.index(caseFiles("ddos"));
  const r = go(idx, "sourcetype=access_combined | timechart span=1m count");
  assert.deepEqual(plain(r.cols), ["_time", "count"]);
  assert.equal(r.span, 60);
  const total = r.rows.reduce((a, b) => a + b.count, 0);
  assert.equal(total, go(idx, "sourcetype=access_combined").n);
  for (let i = 1; i < r.rows.length; i++) assert.equal(r.rows[i]._time - r.rows[i - 1]._time, 60);
  const by = go(idx, "sourcetype=access_combined | timechart span=5m limit=2 count by status");
  assert.equal(by.cols[0], "_time");
  assert.ok(by.cols.length <= 4);
  const sum = by.rows.reduce((a, row) => a + by.cols.slice(1).reduce((x, c) => x + row[c], 0), 0);
  assert.equal(sum, total);
});

test("where, eval, rex, rename, dedup, head, sort and table", () => {
  const idx = E.index(caseFiles("quietdns"));
  const long = go(idx, 'sourcetype=dns_query | eval n=len(query) | where n > 40 AND like(query, "%.%") | dedup query | sort - n | head 3 | table query n');
  assert.ok(long.n > 0 && long.n <= 3);
  for (let i = 1; i < long.n; i++) assert.ok(long.rows[i - 1].n >= long.rows[i].n);
  assert.deepEqual(plain(long.cols), ["query", "n"]);
  const rx = go(idx, 'sourcetype=dns_query | rex field=query "^\\d+\\.(?<label>[^.]+)\\.(?<zone>.+)$" | stats dc(label) as labels by zone | sort - labels | head 1 | rename zone as domain');
  assert.deepEqual(plain(rx.cols), ["domain", "labels"]);
  assert.ok(rx.rows[0].labels > 5);
  assert.equal(rx.rows[0].domain, "k7q2.t.cloudmetric.example");
  const ip = go(idx, 'sourcetype=dns_query | where cidrmatch("10.70.0.0/16", src_ip) | stats count');
  assert.equal(ip.rows[0].count, go(idx, "sourcetype=dns_query").n);
  const hour = go(idx, 'sourcetype=dns_query | eval hour=strftime(_time, "%H") | stats count by hour');
  assert.ok(hour.rows.every((r) => /^\d\d$/.test(r.hour)));
});

test("syslog lines without a year take the year the other logs use", () => {
  const idx = E.index(caseFiles("web01"));
  const e = go(idx, "source=auth.log | head 1").rows[0];
  assert.equal(new Date(e._time * 1000).getUTCFullYear(), 2026);
  assert.equal(E.timeOf("1793609890.000   120 10.20.0.15", 2026), 1793609890);
  assert.equal(E.timeOf("[03/Nov/2026:09:00:05 +0530]", 2026), Date.UTC(2026, 10, 3, 3, 30, 5) / 1000);
  assert.equal(E.timeOf("05-Nov-2026 11:00:13.466 queries", 2026), Date.UTC(2026, 10, 5, 11, 0, 13, 466) / 1000);
});

test("events come newest first; head takes the newest", () => {
  const idx = E.index(caseFiles("web01"));
  const r = go(idx, "source=auth.log");
  for (let i = 1; i < r.n; i++) assert.ok(r.rows[i - 1]._time >= r.rows[i]._time);
  assert.equal(go(idx, "source=auth.log | head 1").rows[0]._time, r.rows[0]._time);
  assert.equal(go(idx, "source=auth.log | tail 1").rows[0]._time, r.rows[r.n - 1]._time);
});

test("mistakes give a plain message, not a crash", () => {
  const idx = E.index(caseFiles("web01"));
  const bad = ["status=200 |", "| nosuch x", '"open', "(status=200", "x | stats", "x | stats foo(bytes)", "x | where (", "x | rex field=uri \"(\"", "x | timechart span=0m count", "x | sort"];
  for (const q of bad) {
    assert.throws(() => go(idx, q), (e) => e.user === true && typeof e.message === "string" && e.message.length > 5, q);
  }
});

test("clicking a value adds it to the base search, before any pipes", () => {
  assert.equal(E.addTerm("", "status=404"), "status=404");
  assert.equal(E.addTerm("index=main | stats count by src_ip", "user=root"), "index=main user=root | stats count by src_ip");
  assert.equal(E.addTerm("*", 'useragent="sqlmap/1.8 x"'), 'useragent="sqlmap/1.8 x"');
});

test("the recorded state is a fence the notebook can read back", () => {
  const state = { q: "action=failure | stats count by src_ip", n: 2, files: ["auth.log"], blank: ["q"] };
  const text = T.fence("siem", state);
  assert.ok(text.startsWith("```tool siem\n"));
  assert.deepEqual(plain(T.parse(text.split("\n")[1])), state);
});

test("a teacher case with only made-up data indexes", () => {
  const dir = path.join(ROOT, "source", "teacher-cases");
  for (const n of fs.readdirSync(dir).filter((f) => f.endsWith(".json"))) {
    const c = JSON.parse(fs.readFileSync(path.join(dir, n), "utf8"));
    const files = {};
    const src = c.files || (c.bundle && c.bundle.files) || {};
    for (const [k, v] of Object.entries(src)) if (typeof v === "string") files[k.replace(/^case\//, "")] = v;
    const idx = E.index(files);
    assert.ok(Array.isArray(idx.events));
    go(idx, "index=main | stats count by source");
  }
});
