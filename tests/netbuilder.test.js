const test = require("node:test");
const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");
const vm = require("node:vm");

const ROOT = path.resolve(__dirname, "..");
const THEME = path.join(ROOT, "source", "static", "assets", "theme");
const SEM = path.join(ROOT, "source", "seminars");

function load() {
  const sandbox = { console, URL, TextEncoder, TextDecoder, document: { currentScript: null } };
  sandbox.window = sandbox;
  vm.createContext(sandbox);
  for (const n of ["tools.js", "tool-firewall.js", "workstation-net.js", "netkit.js", "tool-netstarter.js", "tool-netsim.js", "tool-netemu.js"]) vm.runInContext(fs.readFileSync(path.join(THEME, n), "utf8"), sandbox);
  return { N: sandbox.AayatNet, C: sandbox.AayatNetKit.core, T: sandbox.AayatTools };
}
const { N, C, T } = load();

function lab(folder) {
  const j = JSON.parse(fs.readFileSync(path.join(SEM, folder, "files", "netbuilder.json"), "utf8"));
  const D = Object.assign(C.emptyDoc(), JSON.parse(JSON.stringify(j)));
  const env = { D, flags: {}, flows: [], sess: {}, S: C.makeSession(D) };
  env.goals = () => C.evalTasks(env.D, env.S, env.flags);
  env.rebuild = () => { env.S = C.makeSession(env.D); env.goals(); };
  env.cable = (a, b) => { env.D.cables.push([a, b]); env.rebuild(); };
  env.set = (id, props) => { Object.assign(C.dev(env.D, id), props); env.rebuild(); };
  env.cli = (id, lines) => {
    const out = [];
    const sess = (env.sess[id] = env.sess[id] || {});
    lines.forEach((l) => {
      out.push(N.cli(env.S, id, sess, l).out);
      if (C.dirty(env.S.state)) { C.fold(env.D, env.S.state); env.rebuild(); }
    });
    return out.join("\n");
  };
  env.run = (id, line) => {
    const out = C.hostOutput(env.D, env.S, id, line, (f) => { env.flows.push(f); C.noteFlow(env.S.model(), env.flags, f); });
    if (C.dev(env.D, id).changed) { delete C.dev(env.D, id).changed; env.rebuild(); }
    env.goals();
    return out;
  };
  env.done = () => env.goals().filter((t) => t.done).length;
  env.undone = () => env.goals().filter((t) => !t.done).map((t) => t.id);
  return env;
}

test("every lab has a starting network with goals that are not already met", () => {
  const folders = fs.readdirSync(SEM).filter((n) => /^n0[1-8]-/.test(n));
  assert.equal(folders.length, 8);
  for (const f of folders) {
    const e = lab(f);
    const goals = e.goals();
    assert.ok(goals.length >= 4, f + " has goals");
    assert.ok(goals.some((g) => !g.done), f + " starts unfinished");
    assert.ok(e.D.devices.length >= 3, f + " has devices");
  }
});

test("lab 1: cable, address, ping, and the stray computer", () => {
  const e = lab("n01-filius-your-first-network");
  ["till-1", "till-2", "office", "stray"].forEach((p, i) => e.cable(p + ":eth0", "sw1:" + (i + 1)));
  e.set("till-1", { ip: "192.168.1.11" });
  e.set("till-2", { ip: "192.168.1.12" });
  e.set("office", { ip: "192.168.1.13" });
  e.set("stray", { ip: "192.168.2.14" });
  assert.match(e.run("till-1", "ipconfig"), /IPv4 Address[ .]*: 192\.168\.1\.11/);
  assert.match(e.run("till-1", "ping 192.168.1.12"), /Reply from 192\.168\.1\.12: bytes/);
  assert.match(e.run("till-1", "ping 192.168.1.13"), /Reply from 192\.168\.1\.13: bytes/);
  assert.match(e.run("till-1", "ping 192.168.2.14"), /General failure/);
  assert.equal(e.goals().find((g) => g.id === "t4").done, true);
  e.set("stray", { ip: "192.168.1.14" });
  assert.match(e.run("till-1", "ping 192.168.1.14"), /Reply from 192\.168\.1\.14: bytes/);
  assert.deepEqual(e.undone(), []);
});

test("lab 2: a router joins two networks, and a missing gateway cuts one off", () => {
  const e = lab("n02-filius-two-networks-and-a-router");
  e.D.cables = [["till-1:eth0", "sw-shop:1"], ["till-2:eth0", "sw-shop:2"], ["r1:g0/0", "sw-shop:3"], ["r1:g0/1", "sw-back:1"], ["accounts:eth0", "sw-back:2"], ["manager:eth0", "sw-back:3"]];
  e.set("till-1", { ip: "192.168.1.11", gw: "192.168.1.1" });
  e.set("till-2", { ip: "192.168.1.12", gw: "192.168.1.1" });
  e.set("accounts", { ip: "192.168.2.21", gw: "192.168.2.1" });
  e.set("manager", { ip: "192.168.2.22", gw: "192.168.2.1" });
  e.D.devices.find((d) => d.id === "r1").ifs["g0/0"] = { ip: "192.168.1.1", bits: 24 };
  e.D.devices.find((d) => d.id === "r1").ifs["g0/1"] = { ip: "192.168.2.1", bits: 24 };
  e.rebuild();
  e.flows.length = 0;
  assert.match(e.run("till-1", "ping 192.168.2.21"), /Reply from 192\.168\.2\.21: bytes/);
  const far = C.frames(e.D, e.S.model(), e.flows, ["accounts:eth0", "sw-back:2"]).find((x) => x.proto === "ICMP" && !x.reply);
  assert.equal(far.ttl, 127);
  assert.equal(far.src, "192.168.1.11");
  e.set("manager", { gw: "" });
  assert.match(e.run("manager", "ping 192.168.2.21"), /Reply from 192\.168\.2\.21: bytes/);
  assert.doesNotMatch(e.run("manager", "ping 192.168.1.11"), /Reply from 192\.168\.1\.11: bytes/);
  e.set("manager", { gw: "192.168.2.1" });
  assert.deepEqual(e.undone(), []);
});

test("lab 3: names resolve through the DNS server and the web page opens, and a bad gateway breaks one computer", () => {
  const e = lab("n03-filius-dns-web-and-a-fault");
  e.set("web01", { ip: "192.168.2.80", gw: "192.168.2.1", services: { web: true, dns: false } });
  e.set("dns01", { ip: "192.168.2.53", gw: "192.168.2.1", services: { web: false, dns: true }, records: "www.banyan.lan 192.168.2.80" });
  ["till-1", "till-2", "accounts", "manager", "web01", "dns01"].forEach((id) => e.set(id, { dns: "192.168.2.53" }));
  assert.match(e.run("till-1", "curl www.banyan.lan"), /HTTP\/1.1 200 OK/);
  assert.match(e.run("accounts", "curl www.banyan.lan"), /Welcome to Banyan Books/);
  assert.match(e.run("till-1", "nslookup www.banyan.lan"), /192\.168\.2\.80/);
  e.set("till-2", { gw: "192.168.1.100" });
  assert.match(e.run("till-2", "curl www.banyan.lan"), /curl: \(/);
  e.goals();
  e.set("till-2", { gw: "192.168.1.1" });
  assert.match(e.run("till-2", "curl www.banyan.lan"), /200 OK/);
  assert.deepEqual(e.undone(), []);
});

test("lab 4: VLANs separate staff from guests even when a guest guesses a staff address", () => {
  const e = lab("n04-pt-vlans-staff-and-guest");
  e.D.cables = [["staff-1:eth0", "sw1:1"], ["staff-2:eth0", "sw1:2"], ["guest-1:eth0", "sw1:13"], ["guest-2:eth0", "sw1:14"]];
  e.set("staff-1", { ip: "192.168.10.11" });
  e.set("staff-2", { ip: "192.168.10.12" });
  e.set("guest-1", { ip: "192.168.20.31" });
  e.set("guest-2", { ip: "192.168.20.32" });
  e.cli("sw1", ["enable", "configure terminal", "vlan 10", "name STAFF", "exit", "vlan 20", "name GUEST", "exit", "interface range fa0/1-12", "switchport mode access", "switchport access vlan 10", "exit", "interface range fa0/13-20", "switchport mode access", "switchport access vlan 20", "end"]);
  assert.match(e.cli("sw1", ["show vlan brief"]), /STAFF\s+active\s+Fa0\/1, Fa0\/2/);
  assert.match(e.run("staff-1", "ping 192.168.10.12"), /Reply from 192\.168\.10\.12/);
  assert.doesNotMatch(e.run("staff-1", "ping 192.168.20.31"), /Reply from 192\.168\.20\.31: bytes/);
  e.set("guest-1", { ip: "192.168.10.99" });
  assert.doesNotMatch(e.run("guest-1", "ping 192.168.10.11"), /Reply from 192\.168\.10\.11: bytes/);
  assert.deepEqual(e.undone(), []);
});

function routerOnAStick(e) {
  e.cable("sw1:25", "r1:g0/0");
  e.cli("sw1", ["enable", "configure terminal", "interface gi0/1", "switchport mode trunk", "end"]);
  e.cli("r1", ["enable", "configure terminal", "interface g0/0", "no shutdown", "exit", "interface g0/0.10", "encapsulation dot1Q 10", "ip address 192.168.10.1 255.255.255.0", "exit", "interface g0/0.20", "encapsulation dot1Q 20", "ip address 192.168.20.1 255.255.255.0", "end"]);
}

test("lab 5: a trunk and two subinterfaces route between the VLANs", () => {
  const e = lab("n05-pt-router-on-a-stick");
  routerOnAStick(e);
  e.set("staff-1", { gw: "192.168.10.1" });
  e.set("staff-2", { gw: "192.168.10.1" });
  e.set("guest-1", { gw: "192.168.20.1" });
  e.set("guest-2", { gw: "192.168.20.1" });
  assert.match(e.run("guest-1", "ping 192.168.10.11"), /Reply from 192\.168\.10\.11: bytes/);
  assert.match(e.cli("sw1", ["enable", "show interfaces trunk"]), /Gi0\/1\s+on\s+802\.1q/);
  assert.match(e.cli("r1", ["enable", "show ip interface brief"]), /GigabitEthernet0\/0\.10\s+192\.168\.10\.1/);
  assert.deepEqual(e.undone(), []);
});

test("lab 6: parked ports, sticky port security that err-disables a stranger, and management passwords", () => {
  const e = lab("n06-pt-lock-down-the-switch");
  e.cli("sw1", ["enable", "configure terminal", "vlan 999", "name PARKING", "exit", "interface range fa0/21-24", "switchport mode access", "switchport access vlan 999", "shutdown", "exit",
    "interface range fa0/1-12", "switchport port-security", "switchport port-security maximum 1", "switchport port-security mac-address sticky", "switchport port-security violation shutdown", "exit",
    "enable secret s3cret", "line console 0", "password cons0le", "login", "end"]);
  assert.match(e.cli("sw1", ["show port-security"]), /Fa0\/1\s+1\s+1\s+0\s+Shutdown/);
  assert.equal(e.goals().find((g) => g.id === "t3").done, false);
  e.D.cables = e.D.cables.filter((c) => c[0] !== "staff-2:eth0");
  e.D.devices.push({ id: "laptop1", kind: "laptop", name: "laptop1", os: "windows", ip: "192.168.10.50", bits: 24, gw: "192.168.10.1", dns: "", x: 100, y: 330 });
  e.cable("laptop1:eth0", "sw1:2");
  assert.match(e.cli("sw1", ["show interfaces status"]), /Fa0\/2\s+\S*\s*err-disabled/);
  assert.doesNotMatch(e.run("laptop1", "ping 192.168.10.11"), /Reply from 192\.168\.10\.11: bytes/);
  assert.match(e.cli("sw1", ["show running-config"]), /enable secret/);
  assert.deepEqual(e.undone(), []);
});

test("lab 7: access list 120 lets guests browse but not reach staff, and leaves staff free", () => {
  const e = lab("n07-pt-acl-guests-stay-out");
  e.cable("files01:eth0", "sw1:3");
  e.set("files01", { ip: "192.168.10.10", gw: "192.168.10.1" });
  e.cable("web-out:eth0", "r1:g0/1");
  e.set("web-out", { ip: "203.0.113.10", gw: "203.0.113.1" });
  e.cli("r1", ["enable", "configure terminal", "interface g0/1", "ip address 203.0.113.1 255.255.255.0", "no shutdown", "exit",
    "access-list 120 deny ip 192.168.20.0 0.0.0.255 192.168.10.0 0.0.0.255", "access-list 120 permit tcp 192.168.20.0 0.0.0.255 any eq 80",
    "access-list 120 permit udp 192.168.20.0 0.0.0.255 any eq 53", "access-list 120 deny ip any any", "interface g0/0.20", "ip access-group 120 in", "end"]);
  assert.match(e.cli("r1", ["show access-lists"]), /Extended IP access list 120\n\s+10 deny ip 192\.168\.20\.0 0\.0\.0\.255 192\.168\.10\.0 0\.0\.0\.255/);
  assert.match(e.run("guest-1", "curl 203.0.113.10"), /200 OK/);
  assert.doesNotMatch(e.run("guest-1", "ping 192.168.10.10"), /Reply from 192\.168\.10\.10: bytes/);
  assert.match(e.run("staff-1", "ping 192.168.10.10"), /Reply from 192\.168\.10\.10: bytes/);
  assert.match(e.run("staff-1", "curl 203.0.113.10"), /200 OK/);
  assert.match(e.cli("r1", ["show running-config"]), /ip access-group 120 in/);
  assert.deepEqual(e.undone(), []);
});

test("global commands typed inside a sub-mode drop back to configuration mode, as on a real switch", () => {
  const e = lab("n04-pt-vlans-staff-and-guest");
  e.D.cables = [["staff-1:eth0", "sw1:1"], ["guest-1:eth0", "sw1:13"]];
  e.rebuild();
  const out = e.cli("sw1", ["enable", "configure terminal", "vlan 10", "name STAFF", "vlan 20", "name GUEST", "interface range fa0/1 - 12", "switchport mode access", "switchport access vlan 10", "interface range fa0/13 - 20", "switchport mode access", "switchport access vlan 20", "end", "show vlan brief"]);
  assert.doesNotMatch(out, /Invalid input/);
  assert.match(out, /10\s+STAFF\s+active\s+Fa0\/1, Fa0\/2/);
  assert.match(out, /20\s+GUEST\s+active\s+Fa0\/13/);
  const r = lab("n05-pt-router-on-a-stick");
  assert.doesNotMatch(r.cli("r1", ["enable", "configure terminal", "interface g0/0", "no shutdown", "access-list 120 deny ip any any", "line console 0", "password x", "enable secret y", "end"]), /Invalid input/);
  assert.match(r.cli("r1", ["show running-config"]), /enable secret/);
});

test("an access list is read from the top: a permit above the deny lets guests through", () => {
  const e = lab("n07-pt-acl-guests-stay-out");
  e.cable("files01:eth0", "sw1:3");
  e.set("files01", { ip: "192.168.10.10", gw: "192.168.10.1" });
  e.cli("r1", ["enable", "configure terminal", "access-list 120 permit ip any any", "access-list 120 deny ip 192.168.20.0 0.0.0.255 192.168.10.0 0.0.0.255", "interface g0/0.20", "ip access-group 120 in", "end"]);
  assert.match(e.run("guest-1", "ping 192.168.10.10"), /Reply from 192\.168\.10\.10: bytes/);
});

test("lab 8: a capture on the PC1 link shows ARP and the ICMP echo request and reply", () => {
  const e = lab("n08-gns3-capture-a-link");
  e.cable("pc1:eth0", "sw1:1");
  e.cable("pc2:eth0", "sw1:2");
  assert.ok(e.goals().some((g) => g.id === "t0" && !g.done));
  ["pc1", "pc2", "sw1"].forEach((id) => e.set(id, { power: true }));
  assert.ok(e.goals().some((g) => g.id === "t0" && g.done));
  assert.match(e.run("pc1", "ip 10.0.0.1/24 10.0.0.254"), /10\.0\.0\.1 255\.255\.255\.0 gateway 10\.0\.0\.254/);
  e.run("pc2", "ip 10.0.0.2/24 10.0.0.254");
  assert.match(e.run("pc1", "show ip"), /IP\/MASK\s+: 10\.0\.0\.1\/24/);
  e.flows.length = 0;
  assert.match(e.run("pc1", "ping 10.0.0.2"), /icmp_seq=1 ttl=64/);
  const f = C.frames(e.D, e.S.model(), e.flows, ["pc1:eth0", "sw1:1"]);
  const protos = f.map((x) => x.proto + (x.reply ? "-reply" : ""));
  assert.ok(protos.includes("ARP"));
  assert.ok(protos.includes("ICMP"));
  assert.ok(protos.includes("ICMP-reply"));
  assert.equal(f.filter((x) => x.proto === "ICMP").length, 10);
  assert.equal(C.filterFrames(f, "arp").length, 2);
  assert.equal(C.filterFrames(f, "arp || icmp").length, f.length);
  const arp = f.find((x) => x.proto === "ARP");
  assert.equal(arp.dmac, "ff:ff:ff:ff:ff:ff");
  assert.match(arp.info, /Who has 10\.0\.0\.2\? Tell 10\.0\.0\.1/);
  assert.deepEqual(C.frames(e.D, e.S.model(), e.flows, ["pc2:eth0", "sw1:2"]).length, f.length);
  e.flags["cap:start"] = 1;
  e.flags["cap:filter:arp"] = 1;
  e.flags["cap:saw:arp"] = 1;
  e.flags["cap:saw:icmpreply"] = 1;
  assert.deepEqual(e.undone(), []);
});

test("frames on a trunk carry the 802.1Q VLAN tag and routed frames change their MAC at the router", () => {
  const e = lab("n05-pt-router-on-a-stick");
  routerOnAStick(e);
  e.set("staff-1", { gw: "192.168.10.1" });
  e.set("guest-1", { gw: "192.168.20.1" });
  e.run("guest-1", "ping 192.168.10.11");
  const trunk = C.frames(e.D, e.S.model(), e.flows, ["sw1:25", "r1:g0/0"]);
  assert.ok(trunk.length > 0);
  assert.ok(trunk.every((x) => x.vlan === 10 || x.vlan === 20));
  const edge = C.frames(e.D, e.S.model(), e.flows, ["guest-1:eth0", "sw1:13"]);
  assert.ok(edge.every((x) => !x.vlan));
  const req = edge.find((x) => x.proto === "ICMP" && !x.reply);
  const toStaff = trunk.find((x) => x.proto === "ICMP" && !x.reply && x.vlan === 10);
  assert.notEqual(req.dmac, toStaff.dmac);
  assert.equal(req.dst, "192.168.10.11");
  assert.equal(toStaff.dst, "192.168.10.11");
});

test("the engine's switch ports name gigabit uplinks and the clinic bench still behaves", () => {
  assert.equal(N.portLabel(25), "Gi0/1");
  assert.equal(N.portLabel(3), "Fa0/3");
  const r = N.aclEntry("deny ip 192.168.20.0 0.0.0.255 192.168.10.0 0.0.0.255", false);
  assert.equal(r.src, "192.168.20.0/24");
  assert.equal(r.dst, "192.168.10.0/24");
  assert.equal(N.aclEntry("permit tcp host 10.0.0.5 any eq www", false).port, "80");
  assert.equal(N.aclEntry("permit nonsense", false), null);
});

test("saved lab files are valid JSON the tool can read", () => {
  for (const f of fs.readdirSync(SEM).filter((n) => /^n0[1-8]-/.test(n))) {
    const text = fs.readFileSync(path.join(SEM, f, "files", "netbuilder.json"), "utf8");
    const j = JSON.parse(text);
    assert.ok(Array.isArray(j.devices) && Array.isArray(j.cables) && Array.isArray(j.tasks));
    const want = { n01: "netstarter", n02: "netstarter", n03: "netstarter", n04: "netsim", n05: "netsim", n06: "netsim", n07: "netsim", n08: "netemu" }[f.slice(0, 3)];
    assert.equal(j.program, want);
    assert.ok(T.get(want), want + " is registered");
    const readme = fs.readFileSync(path.join(SEM, f, "files", "README.txt"), "utf8");
    assert.match(readme, new RegExp("Where: this lab runs in the Hacker Room's Network (Starter|Simulator|Emulator)"));
    assert.doesNotMatch(readme, /Filius|Packet Tracer|GNS3|Wireshark|netacad|download/i);
  }
});

test("simulation mode steps a ping hop by hop: ARP floods, then the echo request and reply cross each cable", () => {
  const e = lab("n05-pt-router-on-a-stick");
  e.cable("sw1:25", "r1:g0/0");
  e.cli("sw1", ["enable", "configure terminal", "interface gi0/1", "switchport mode trunk", "end"]);
  e.cli("r1", ["enable", "configure terminal", "interface g0/0", "no shutdown", "interface g0/0.10", "encapsulation dot1Q 10", "ip address 192.168.10.1 255.255.255.0", "interface g0/0.20", "encapsulation dot1Q 20", "ip address 192.168.20.1 255.255.255.0", "end"]);
  ["staff-1", "staff-2"].forEach((id) => e.set(id, { gw: "192.168.10.1" }));
  ["guest-1", "guest-2"].forEach((id) => e.set(id, { gw: "192.168.20.1" }));
  const M = e.S.model();
  const r = N.route(M, "guest-1", "192.168.10.11");
  assert.ok(r.ok);
  const ev = C.simEvents(e.D, M, { kind: "icmp", from: "guest-1", to: "192.168.10.11", ok: true, r, count: 1 }, {});
  const arps = ev.filter((x) => x.proto === "ARP" && x.arp === "req");
  assert.ok(arps.length >= 2 && arps.every((x) => x.bcast));
  assert.ok(arps.some((x) => x.drop), "a computer that does not own the address drops the ARP request");
  const req = ev.filter((x) => x.proto === "ICMP" && !x.reply), rep = ev.filter((x) => x.proto === "ICMP" && x.reply);
  assert.ok(req.length >= 3 && rep.length === req.length);
  assert.equal(req[0].last, "guest-1");
  assert.equal(req[req.length - 1].at, "staff-1");
  assert.ok(req.some((x) => x.vlan === 20) && req.some((x) => x.vlan === 10), "the trunk carries the request tagged 20 in and 10 out");
  assert.equal(rep[rep.length - 1].at, "guest-1");
  const again = C.simEvents(e.D, M, { kind: "icmp", from: "guest-1", to: "192.168.10.11", ok: true, r, count: 1 }, { "guest-1>sw1": 1, "sw1>guest-1": 1, "guest-1>r1": 1, "r1>guest-1": 1, "r1>staff-1": 1, "staff-1>r1": 1 });
  assert.equal(again.filter((x) => x.proto === "ARP").length, 0, "with the ARP caches filled, no ARP is sent");
  const off = Object.assign(C.dev(e.D, "r1"), {});
  off.ifs["g0/0"].shut = true;
  e.rebuild();
  const M2 = e.S.model(), r2 = N.route(M2, "guest-1", "192.168.10.11");
  assert.equal(r2.ok, false);
  const ev2 = C.simEvents(e.D, M2, { kind: "icmp", from: "guest-1", to: "192.168.10.11", ok: false, r: r2, count: 1 }, {});
  assert.ok(ev2.length && ev2[ev2.length - 1].drop, "a failed ping ends in a dropped event with a reason");
});

test("cables of the wrong type stay down and suspended links carry nothing", () => {
  const e = lab("n04-pt-vlans-staff-and-guest");
  ["staff-1", "staff-2"].forEach((id, i) => e.set(id, { ip: "192.168.10.1" + (i + 1) }));
  e.D.cables.push(["staff-1:eth0", "sw1:1", "cross"]);
  e.D.cables.push(["staff-2:eth0", "sw1:2", "straight"]);
  e.rebuild();
  assert.equal(C.cableFits(e.D, e.D.cables[0]), false);
  assert.equal(C.cableFits(e.D, e.D.cables[1]), true);
  assert.equal(N.route(e.S.model(), "staff-2", "192.168.10.11").ok, false);
  e.D.cables[0][2] = "straight";
  e.rebuild();
  assert.equal(N.route(e.S.model(), "staff-2", "192.168.10.11").ok, true);
  e.D.suspended = { [C.ckey(e.D.cables[0])]: 1 };
  e.rebuild();
  assert.equal(N.route(e.S.model(), "staff-2", "192.168.10.11").ok, false);
});

test("the three network programs are registered and none of them is a second copy of the engine", () => {
  for (const id of ["netstarter", "netsim", "netemu"]) {
    const d = T.get(id);
    assert.ok(d && d.console && typeof d.mount === "function");
    const src = fs.readFileSync(path.join(THEME, "tool-" + id + ".js"), "utf8");
    assert.doesNotMatch(src, /function (route|cli|normalize|jsonOf|frames|simEvents)\(/);
  }
  assert.equal(T.get("netbuilder"), null);
});
