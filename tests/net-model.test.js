const test = require("node:test");
const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");
const vm = require("node:vm");

const ROOT = path.resolve(__dirname, "..");
const THEME = path.join(ROOT, "source", "static", "assets", "theme");
const CLINIC = path.join(ROOT, "source", "seminars", "x03-secure-a-small-office");

function load() {
  const sandbox = { console, URL, TextEncoder, TextDecoder, document: { currentScript: null } };
  sandbox.window = sandbox;
  vm.createContext(sandbox);
  for (const n of ["tools.js", "tool-firewall.js", "workstation-net.js"]) vm.runInContext(fs.readFileSync(path.join(THEME, n), "utf8"), sandbox);
  return sandbox.AayatNet;
}
const N = load();

function hostsTxt(file) {
  const dns = path.join(path.dirname(file), "dns.txt");
  return N.parseHosts(fs.readFileSync(file, "utf8"), fs.existsSync(dns) ? fs.readFileSync(dns, "utf8") : "");
}
function clinic() {
  const events = [];
  const base = N.normalize(JSON.parse(fs.readFileSync(path.join(CLINIC, "net", "bench.json"), "utf8")), hostsTxt(path.join(CLINIC, "net", "hosts.txt")));
  const s = N.session(base, null, { emit: (t, d) => events.push([t, d]) });
  return { s, events };
}
const done = (s, id) => s.tasks().find((t) => t.id === id).done;
function console_(s, dev, lines) {
  const sess = {};
  return lines.map((l) => N.cli(s, dev, sess, l).out).join("\n");
}

test("the clinic works as wired, and guests can reach the patient records", () => {
  const { s } = clinic();
  const M = s.model();
  assert.equal(N.route(M, "recep-pc", "nas01").ok, true);
  assert.equal(N.route(M, "recep-pc", "198.51.100.1").ok, true);
  assert.equal(N.route(M, "guest-phone", "nas01", { proto: "tcp", port: 445 }).ok, true);
  assert.equal(done(s, "still-works"), true);
  assert.equal(done(s, "guests-out"), false);
  assert.equal(done(s, "unplug-rogue"), false);
});

test("pulling the rogue's cable takes it off, says what broke and emits events", () => {
  const { s, events } = clinic();
  const base = s.model();
  s.setPort("sw1", "9", { to: null });
  assert.equal(done(s, "unplug-rogue"), true);
  assert.equal(N.route(s.model(), "tl-wr840n", "10.40.0.1").why, "nolink");
  assert.ok(N.impact(base, s.model()).some((l) => /No network at all: TL-WR840N/.test(l)));
  const cable = events.find((e) => e[0] === "rack.cable");
  assert.equal(cable[1].action, "unplug");
  assert.equal(cable[1].ip, "10.40.0.99");
  assert.equal(cable[1].socket, "W1");
  assert.ok(events.some((e) => e[0] === "bench.task" && e[1].id === "unplug-rogue"));
});

test("shutting the trunk to the access point cuts the guest Wi-Fi", () => {
  const { s } = clinic();
  const base = s.model();
  s.setPort("sw1", "12", { shut: true });
  assert.equal(N.route(s.model(), "guest-phone", "198.51.100.1").ok, false);
  assert.ok(N.impact(base, s.model()).some((l) => /Lost the internet: guest-phone/.test(l)));
});

test("removing VLAN 20 from the router trunk leaves guests without a gateway", () => {
  const { s } = clinic();
  s.setPort("sw1", "1", { allowed: "1" });
  const r = N.route(s.model(), "guest-phone", "198.51.100.1");
  assert.equal(r.ok, false);
  assert.equal(r.why, "gwdown");
  assert.equal(N.route(s.model(), "recep-pc", "198.51.100.1").ok, true);
});

test("the router rules, in the Firewall program's syntax, keep guests out", () => {
  const { s } = clinic();
  s.setRules("gw", "zone clinic 10.40.0.0/24\nzone guest 10.40.1.0/24\nzone internet any\nallow any clinic -> any\nallow udp guest -> 10.40.0.1:53\nallow tcp guest -> internet:80,443\ndeny any guest -> clinic\ndefault deny\n");
  const r = N.route(s.model(), "guest-phone", "nas01", { proto: "tcp", port: 445 });
  assert.equal(r.ok, false);
  assert.equal(r.why, "filtered");
  assert.equal(done(s, "guests-out"), true);
  assert.equal(done(s, "still-works"), true);
});

test("the switch console uses real commands and shuts the empty rooms", () => {
  const { s } = clinic();
  const out = console_(s, "sw1", ["enable", "configure terminal", "interface range fa0/7, fa0/11", "shutdown", "end", "show interfaces status", "show vlan brief"]);
  assert.equal(done(s, "empty-rooms"), true);
  assert.match(out, /Fa0\/7\s+consult room 3\s+disabled/);
  assert.match(out, /Fa0\/10\s+surgery 2\s+disabled/);
  assert.match(out, /^20\s+guest\s+active/m);
  assert.match(out, /Fa0\/9\s+waiting room\s+connected/);
});

test("a new access VLAN is created the way a real switch does it", () => {
  const { s } = clinic();
  const out = console_(s, "sw1", ["en", "conf t", "int fa0/4", "switchport access vlan 30", "do show vlan brief"]);
  assert.match(out, /Creating vlan 30/);
  assert.match(out, /^30\s+VLAN0030\s+active\s+Fa0\/4/m);
  assert.equal(N.route(s.model(), "recep-pc", "nas01").ok, false);
  assert.equal(done(s, "still-works"), false);
});

test("router console: subinterfaces, routes and show commands", () => {
  const { s } = clinic();
  const out = console_(s, "gw", ["enable", "show ip interface brief", "show ip route", "show access-lists"]);
  assert.match(out, /GigabitEthernet0\/0\.20\s+10\.40\.1\.1\s+YES manual up/);
  assert.match(out, /S\*\s+0\.0\.0\.0\/0 \[1\/0\] via 100\.64\.0\.1/);
  assert.match(out, /allow any guest -> any/);
  console_(s, "gw", ["en", "conf t", "interface g0/0.20", "shutdown"]);
  assert.equal(N.route(s.model(), "guest-phone", "198.51.100.1").why, "gwdown");
});

test("ping and traceroute print the real formats for each system", () => {
  const { s } = clinic();
  const M = s.model();
  const win = N.pingText(M, "recep-pc", "nas01", 4, "windows").text;
  assert.match(win, /Pinging nas01 \[10\.40\.0\.10\] with 32 bytes of data:/);
  assert.match(win, /Reply from 10\.40\.0\.10: bytes=32 time[<=]\d+ms TTL=64/);
  assert.match(win, /Lost = 0 \(0% loss\)/);
  const lin = N.pingText(M, "nas01", "recep-pc", 2, "linux").text;
  assert.match(lin, /64 bytes from recep-pc \(10\.40\.0\.21\): icmp_seq=1 ttl=128/);
  const tr = N.traceText(M, "guest-phone", "198.51.100.1", "linux").text;
  assert.match(tr, /1  gw\.saffron\.lan \(10\.40\.1\.1\)/);
  assert.match(tr, /2  isp-gateway \(100\.64\.0\.1\)/);
  assert.match(tr, /3  198\.51\.100\.1 \(198\.51\.100\.1\)/);
  s.setPort("sw1", "4", { to: null });
  assert.match(N.pingText(s.model(), "recep-pc", "nas01", 4, "windows").text, /General failure/);
  assert.match(N.hostShell(s.model(), "recep-pc", "ipconfig", "windows"), /Media disconnected/);
});

test("a wrong gateway at the far end loses the reply, but the same subnet still works", () => {
  const { s } = clinic();
  s.setDev("dr-pc", { gw: "10.40.0.254" });
  const r = N.route(s.model(), "guest-phone", "dr-pc");
  assert.equal(r.why, "noreturn");
  assert.equal(N.route(s.model(), "recep-pc", "dr-pc").ok, true);
  assert.match(N.pingText(s.model(), "dr-pc", "198.51.100.1", 2, "windows").text, /Request timed out/);
});

test("USB, power, the rack door and reset", () => {
  const { s, events } = clinic();
  s.setDev("recep-pc", { usb: false });
  s.setDoor(true);
  assert.equal(done(s, "usb"), true);
  assert.equal(done(s, "rack"), true);
  s.setDev("nas01", { power: false });
  assert.equal(done(s, "still-works"), false);
  assert.ok(events.some((e) => e[0] === "bench.usb"));
  s.reset();
  assert.equal(done(s, "usb"), false);
  assert.equal(done(s, "still-works"), true);
});

const BENCH = path.join(ROOT, "source", "static", "assets", "bench");
function practice(id) { return N.session(N.normalize(JSON.parse(fs.readFileSync(path.join(BENCH, id + ".json"), "utf8")), []), null); }
const SOLVE = {
  "first-network": (s) => { s.setPort("sw1", "5", { to: "office-pc:eth0" }); s.setDev("room2-pc", { ip: "10.1.1.13", bits: 24 }); },
  "two-vlans": (s) => console_(s, "sw1", ["en", "conf t", "vlan 20", "name guest", "exit", "interface range fa0/4-6", "switchport access vlan 20", "end"]),
  "router-on-a-stick": (s) => {
    console_(s, "sw1", ["en", "conf t", "int fa0/1", "switchport mode trunk", "switchport trunk allowed vlan 10,20", "end"]);
    console_(s, "r1", ["en", "conf t", "interface g0/0.20", "encapsulation dot1Q 20", "ip address 10.0.20.1 255.255.255.0", "end"]);
    s.setDev("guest2", { gw: "10.0.20.1" });
    s.setRules("r1", "zone staff 10.0.10.0/24\nzone guest 10.0.20.0/24\nzone internet any\nallow any staff -> any\nallow tcp guest -> internet:80,443\ndeny any guest -> staff\ndefault deny\n");
  },
  "lock-down": (s) => { s.setPort("sw1", "7", { to: null }); console_(s, "sw1", ["en", "conf t", "interface range fa0/7-9", "shutdown", "end"]); s.setDev("reception-pc", { usb: false }); s.setDoor(true); }
};

test("every practice bench starts unsolved and its hints solve it", () => {
  const list = JSON.parse(fs.readFileSync(path.join(BENCH, "index.json"), "utf8"));
  assert.equal(list.length, Object.keys(SOLVE).length);
  for (const b of list) {
    const s = practice(b.id);
    const open = s.tasks().filter((t) => !t.done);
    assert.ok(open.length >= s.tasks().length - 1, `${b.id}: ${s.tasks().filter((t) => t.done).map((t) => t.id)} done before starting`);
    SOLVE[b.id](s);
    assert.deepEqual(Array.from(s.tasks().filter((t) => !t.done).map((t) => t.id)), [], `${b.id} still open`);
  }
});

test("the clinic bench can be finished the way the hints say", () => {
  const { s } = clinic();
  s.setPort("sw1", "9", { to: null });
  console_(s, "sw1", ["en", "conf t", "interface range fa0/7, fa0/11", "shutdown", "end"]);
  s.setRules("gw", "zone clinic 10.40.0.0/24\nzone guest 10.40.1.0/24\nzone internet any\nallow any clinic -> any\nallow udp guest -> 10.40.0.1:53\nallow tcp guest -> internet:80,443\ndeny any guest -> clinic\ndefault deny\n");
  s.setDev("recep-pc", { usb: false });
  s.setDoor(true);
  assert.deepEqual(Array.from(s.tasks().filter((t) => !t.done).map((t) => t.id)), []);
});

function caseBench(dir) {
  const hosts = hostsTxt(path.join(dir, "net", "hosts.txt"));
  const bench = path.join(dir, "net", "bench.json");
  return N.session(N.normalize(fs.existsSync(bench) ? JSON.parse(fs.readFileSync(bench, "utf8")) : null, hosts), null);
}
function unplug(s, id) {
  const M = s.model();
  Object.keys(M.sw).forEach((sw) => Object.keys(M.sw[sw]).forEach((n) => { const p = M.sw[sw][n]; if (p.to && p.to.split(":")[0] === id) s.setPort(sw, n, { to: null }); }));
}
const CASE_WORK = {
  "source/static/assets/linux/cases/phish": ["hr-pc07"],
  "source/static/assets/linux/cases/miner": ["build01"],
  "source/static/assets/linux/cases/web01": ["web01"],
  "source/seminars/x01-phish-to-containment": ["hr-pc07"],
  "source/seminars/x04-ransomware-night-shift": ["fs02", "eng-ws14"]
};

test("servers on a second subnet are reachable through the router", () => {
  const s = caseBench(path.join(ROOT, "source", "seminars", "x01-phish-to-containment"));
  const M = s.model();
  assert.equal(N.route(M, "hr-pc07", "fs01").ok, true);
  assert.equal(N.route(M, "hr-pc07", "fs01").hops.length, 2);
  const x4 = caseBench(path.join(ROOT, "source", "seminars", "x04-ransomware-night-shift")).model();
  assert.equal(N.route(x4, "eng-ws14", "fs02").ok, true);
  assert.equal(N.route(x4, "eng-ws14", "dc01").ok, true);
});

test("each case's work order starts open and is met by pulling the right cables", () => {
  for (const [dir, ids] of Object.entries(CASE_WORK)) {
    const s = caseBench(path.join(ROOT, dir));
    const tasks = s.tasks();
    assert.ok(tasks.length >= 2, dir + " has a work order");
    assert.equal(tasks[0].done, false, dir + " starts open");
    assert.ok(tasks.slice(1).every((t) => t.done), dir + ": the keep-working checks hold at the start");
    ids.forEach((id) => unplug(s, id));
    assert.deepEqual(Array.from(s.tasks().filter((t) => !t.done).map((t) => t.id)), [], dir + " solved");
  }
});

test("a case without a bench is wired from its nmap scan", () => {
  const hosts = hostsTxt(path.join(ROOT, "source", "static", "assets", "linux", "cases", "phish", "net", "hosts.txt"));
  const s = N.session(N.normalize(null, hosts), null);
  const M = s.model();
  assert.equal(M.dev["gw"].kind, "router");
  assert.equal(M.dev["hr-pc07"].kind, "pc");
  assert.equal(M.dev["fs01"].kind, "server");
  assert.equal(M.sw.sw1["1"].to, "gw:g0/0");
  assert.equal(N.route(M, "hr-pc07", "fs01").ok, true);
  const t = N.route(M, "hr-pc07", "vps-118.bulkhost.example");
  assert.equal(t.ok, true);
  assert.equal(t.hops.length, 3);
  const port = Object.keys(M.sw.sw1).find((n) => M.sw.sw1[n].to === "hr-pc07:eth0");
  s.setPort("sw1", port, { to: null });
  assert.equal(N.route(s.model(), "hr-pc07", "fs01").why, "nolink");
});

const CASES = path.join(ROOT, "source", "static", "assets", "linux", "cases");
const CASE_SOLVE = {
  quietdns: (s) => {
    unplug(s, "fin-lt04");
    s.setRules("dns", "zone office 10.70.0.0/24\nzone proxy 10.70.0.5\nzone internet any\n\nallow tcp proxy -> internet:80,443\ndefault deny\n");
  },
  insider: (s) => {
    unplug(s, "eng-ws57");
    s.setDev("eng-ws57", { usb: false });
    s.setDev("eng-ws61", { usb: false });
    s.setRules("gw", "zone office 10.30.0.0/24\nzone internet any\n\ndeny tcp office -> 203.0.113.80:443\nallow any office -> internet\ndeny tcp 198.51.100.200 -> 10.30.0.99:443\nallow tcp internet -> 10.30.0.99:443\ndefault deny\n");
  },
  ddos: (s) => {
    s.setRules("edge-fw01", "zone office 10.50.0.0/24\nzone internet any\n\nallow any office -> internet\ndeny any 203.0.113.0/24 -> office\nallow tcp internet -> 10.50.0.10:80,443\ndefault deny\n");
  },
  cloudkey: (s) => {
    s.setRules("gw", "zone app 10.40.0.0/24\nzone workers 10.40.1.0/24\nzone internet any\n\ndeny any workers -> any\nallow any app -> internet\nallow tcp internet -> 10.40.0.20:443\ndefault deny\n");
  },
  first: (s) => {
    s.setDoor(true);
    for (let n = 3; n <= 8; n++) s.setPort("sw1", String(n), { shut: true });
  },
  trial: (s) => {
    unplug(s, "till-pc");
    s.setRules("router", "zone cafe 10.9.0.0/24\nzone internet any\n\ndeny tcp internet -> 10.9.0.10:22\nallow any cafe -> internet\nallow any internet -> cafe\ndefault deny\n");
  }
};

test("the six scan-built benches have a work order a student can finish", () => {
  for (const [name, solve] of Object.entries(CASE_SOLVE)) {
    const s = caseBench(path.join(CASES, name));
    assert.ok(s.tasks().length >= 3, name + " has a work order");
    assert.ok(s.tasks().some((t) => !t.done), name + " starts open");
    solve(s);
    assert.deepEqual(Array.from(s.tasks().filter((t) => !t.done).map((t) => t.id)), [], name + " solved");
  }
});

test("the wrong moves fail the keep-working checks", () => {
  const q = caseBench(path.join(CASES, "quietdns"));
  q.setRules("dns", "default deny\n");
  assert.equal(q.tasks().find((t) => t.id === "work").done, false, "blocking everything stops the proxy");
  const c = caseBench(path.join(CASES, "cloudkey"));
  c.setDev("worker-03", { power: false });
  assert.equal(c.tasks().find((t) => t.id === "keep").done, false, "a miner switched off loses its evidence");
  const d = caseBench(path.join(CASES, "ddos"));
  d.setRules("edge-fw01", "zone office 10.50.0.0/24\nzone internet any\n\ndeny any internet -> office\ndefault allow\n");
  assert.equal(d.tasks().find((t) => t.id === "students").done, false, "blocking the internet stops the students too");
});

test("traffic from the internet comes in through the edge router and its rules", () => {
  const s = caseBench(path.join(CASES, "trial"));
  let r = N.route(s.model(), "203.0.113.66", "portal01", { proto: "tcp", port: 22 });
  assert.equal(r.ok, true);
  assert.equal(r.hops[0].id, "out");
  assert.equal(r.hops[1].id, "router");
  s.setRules("router", "deny tcp 203.0.113.66 -> any:22\ndefault allow\n");
  r = N.route(s.model(), "203.0.113.66", "portal01", { proto: "tcp", port: 22 });
  assert.equal(r.why, "filtered");
  assert.equal(N.route(s.model(), "203.0.113.67", "portal01", { proto: "tcp", port: 22 }).ok, true);
  s.setDev("router", { power: false });
  assert.equal(N.route(s.model(), "203.0.113.67", "portal01").why, "gwdown");
});

test("Windows 11 laptops in a scan are Windows on the bench", () => {
  const M = caseBench(path.join(CASES, "quietdns")).model();
  assert.equal(M.dev["fin-lt04"].os, "windows");
  assert.equal(M.dev["proxy"].os, "linux");
});
