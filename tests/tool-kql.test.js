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
  return ctx.window.AayatTools.get("siem").engine;
}

const E = load();
const plain = (v) => JSON.parse(JSON.stringify(v));
const web = E.index({
  "auth.log": fs.readFileSync(path.join(CASES, "web01", "case", "auth.log"), "utf8"),
  "access.log": fs.readFileSync(path.join(CASES, "web01", "case", "access.log"), "utf8")
});
const kq = (q) => E.run(web, E.kql(web, q).spl);
const sp = (q) => E.run(web, q);
const same = (k, s) => assert.deepEqual(plain(kq(k).rows), plain(sp(s).rows));

test("a table name picks that log", () => {
  assert.equal(kq("auth").n, 12);
  assert.equal(kq("access").n, 13);
  assert.equal(kq("syslog").n, 12);
  assert.equal(kq("union *").n, 25);
});

test("unknown tables name the real ones", () => {
  assert.throws(() => E.kql(web, "SigninLogs | take 5"), /Tables here: access, auth/);
});

test("where, summarize and order match the SPL search", () => {
  same("auth | where action == \"failure\" | summarize count() by src_ip, user | order by count_ desc",
    "source=auth.log action=failure | stats count as count_ by src_ip user | sort - count_");
});

test("summarize names results the KQL way", () => {
  const r = kq("auth | summarize dcount(user), tries = count() by src_ip");
  assert.deepEqual(plain(r.cols), ["src_ip", "dcount_user", "tries"]);
});

test("string operators ignore case like KQL", () => {
  assert.equal(kq("auth | where _raw contains \"FAILED PASSWORD\"").n, sp("source=auth.log \"Failed password\"").n);
  assert.equal(kq("auth | where _raw contains_cs \"FAILED PASSWORD\"").n, 0);
  assert.equal(kq("auth | where user =~ \"ROOT\"").n, sp("source=auth.log user=root").n);
  assert.equal(kq("auth | where src_ip startswith \"203.0.113.\"").n, sp("source=auth.log src_ip=203.0.113.*").n);
  assert.equal(kq("auth | where user in (\"root\", \"admin\")").n, sp("source=auth.log (user=root OR user=admin)").n);
  assert.equal(kq("auth | where user !in (\"root\", \"admin\")").n + kq("auth | where user in (\"root\", \"admin\")").n, kq("auth | where isnotempty(user)").n);
  assert.equal(kq("auth | where _raw has \"Failed\"").n, kq("auth | where _raw has \"failed\"").n);
  assert.equal(kq("auth | where _raw has \"Fail\"").n, 0);
});

test("single quotes and verbatim strings work", () => {
  assert.equal(kq("auth | where user == 'root'").n, kq("auth | where user == \"root\"").n);
  assert.equal(kq("auth | where _raw matches regex @\"port \\d{5}\"").n, sp("source=auth.log | where match(_raw, \"port \\\\d{5}\")").n);
});

test("time bins become a timechart", () => {
  const t = E.kql(web, "auth | summarize count() by bin(TimeGenerated, 1h) | render timechart");
  assert.match(t.spl, /timechart span=1h count as count_/);
  assert.equal(t.viz, true);
  const long = kq("union * | summarize count() by bin(TimeGenerated, 1h), source");
  assert.ok(long.rows.every((r) => typeof r._time === "number" && r._time % 3600 === 0));
});

test("between, datetime and ago", () => {
  const all = kq("auth").n;
  assert.equal(kq("auth | where TimeGenerated between (datetime(2000-01-01) .. datetime(2100-01-01))").n, all);
  assert.throws(() => E.kql(web, "auth | where TimeGenerated > ago(1h)"), /from the past/);
});

test("project, extend, take, top, distinct and count", () => {
  const p = kq("auth | extend who = toupper(user) | project TimeGenerated, who | take 3");
  assert.deepEqual(plain(p.cols), ["_time", "who"]);
  assert.equal(p.rows.length, 3);
  assert.equal(kq("auth | distinct src_ip").rows.length, sp("source=auth.log | stats count by src_ip").rows.length);
  assert.deepEqual(Object.keys(kq("auth | distinct src_ip").rows[0]), ["src_ip"]);
  assert.equal(kq("auth | count").rows[0].Count, 12);
  same("access | summarize count() by clientip | top 2 by count_", "source=access.log | stats count as count_ by clientip | sort - count_ | head 2");
  assert.ok(!("user" in kq("auth | project-away user").rows[0]));
  assert.ok("attacker" in kq("auth | project-rename attacker = src_ip").rows[0]);
});

test("comments and line breaks are fine", () => {
  assert.equal(kq("auth // the SSH log\n| where action == \"failure\"\n| count").rows[0].Count, sp("source=auth.log action=failure").n);
});

test("clear messages for what it doesn't know", () => {
  assert.throws(() => E.kql(web, "auth | join (access) on src_ip"), /doesn't know join/);
  assert.throws(() => E.kql(web, "auth | summarize countif(user == \"root\")"), /countif/);
  assert.throws(() => E.kql(web, "auth | where foo(user)"), /doesn't know foo/);
});

test("clicking a value adds a where after the table", () => {
  assert.equal(E.kqlAdd("auth | summarize count() by user", "src_ip", "203.0.113.7"), "auth | where src_ip == \"203.0.113.7\" | summarize count() by user");
  assert.equal(E.kqlAdd("auth | where a == 1 | take 5", "port", "22"), "auth | where a == 1 | where port == 22 | take 5");
});
