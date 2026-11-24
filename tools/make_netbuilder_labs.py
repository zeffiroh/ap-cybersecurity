import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SEM = ROOT / "source" / "seminars"


PROGRAM = {"n01": "netstarter", "n02": "netstarter", "n03": "netstarter", "n04": "netsim", "n05": "netsim", "n06": "netsim", "n07": "netsim", "n08": "netemu"}
PROGRAM_NAME = {"netstarter": "Network Starter", "netsim": "Network Simulator", "netemu": "Network Emulator"}


def host(id, kind, x, y, os="windows", ip="", bits=24, gw="", dns="", **kw):
    d = {"id": id, "kind": kind, "name": id, "x": x, "y": y, "os": os, "ip": ip, "bits": bits, "gw": gw, "dns": dns}
    d.update(kw)
    return d


def switch(id, x, y, ports=26, **kw):
    d = {"id": id, "kind": "switch", "name": id, "x": x, "y": y, "ports": ports}
    d.update(kw)
    return d


def router(id, x, y, ifs=None, **kw):
    d = {"id": id, "kind": "router", "name": id, "x": x, "y": y, "ifs": ifs or {"g0/0": {}, "g0/1": {}, "g0/2": {}, "g0/3": {}}}
    d.update(kw)
    return d


def linked(a, b):
    return {"linked": [a, b]}


def ipis(id, ip, bits=24, gw=None):
    c = {"dev": id, "ip": ip, "bits": bits}
    if gw is not None:
        c["gw"] = gw
    return c


def task(id, text, check, hint="", keep=False):
    t = {"id": id, "text": text, "check": check}
    if hint:
        t["hint"] = hint
    if keep:
        t["keep"] = True
    return t


def doc(lab, title, intro, devices, cables, tasks, swports=None, vlan_names=None):
    return {"lab": lab, "program": PROGRAM[lab], "title": title, "intro": intro, "devices": devices, "cables": cables, "swports": swports or {}, "vlanNames": vlan_names or {}, "tasks": tasks}


def lab1():
    devs = [switch("sw1", 380, 190, ports=8), host("till-1", "pc", 150, 80, "windows"), host("till-2", "pc", 150, 290, "windows"), host("office", "pc", 610, 80, "windows"), host("stray", "pc", 610, 290, "windows")]
    tasks = [
        task("t1", "Cable all four computers to the switch", {"all": [linked(p, "sw1") for p in ("till-1", "till-2", "office", "stray")]}, "Design mode: choose Cable, click a computer, then click the switch."),
        task("t2", "Give till-1, till-2 and office the addresses in the plan (192.168.1.11, .12 and .13, mask 255.255.255.0)", {"all": [ipis("till-1", "192.168.1.11"), ipis("till-2", "192.168.1.12"), ipis("office", "192.168.1.13")]}, "Design mode: click a computer and fill in its panel on the right."),
        task("t3", "Give stray 192.168.2.14, then ping till-2 and office from till-1", {"all": [{"flag": "ping:till-1>till-2:ok"}, {"flag": "ping:till-1>office:ok"}]}, "Press Simulation, click till-1, open Command line and type ping 192.168.1.12.", True),
        task("t4", "Ping stray (192.168.2.14) from till-1 and see why it fails", {"flag": "ping:till-1>stray:fail"}, "stray is in network 192.168.2, a different network from the other three.", True),
        task("t5", "Fix stray's address (192.168.1.14) and ping it from till-1", {"all": [ipis("stray", "192.168.1.14"), {"ping": ["till-1", "stray"]}]}, "Back in Design mode, change the address in stray's panel, then ping it again from till-1 in Simulation mode."),
    ]
    return doc("n01", "Network lab 1: Your first network", "Banyan Books front office: cable four computers to a switch, give them addresses, and prove with ping which can talk and why one cannot.", devs, [], tasks)


def lab2_devices():
    return [switch("sw-shop", 215, 190, ports=8), router("r1", 380, 190, name="router"), switch("sw-back", 545, 190, ports=8),
            host("till-1", "pc", 90, 90, "windows"), host("till-2", "pc", 90, 290, "windows"), host("accounts", "pc", 670, 90, "windows"), host("manager", "pc", 670, 290, "windows")]


def lab2_cables():
    return [["till-1:eth0", "sw-shop:1"], ["till-2:eth0", "sw-shop:2"], ["r1:g0/0", "sw-shop:3"], ["r1:g0/1", "sw-back:1"], ["accounts:eth0", "sw-back:2"], ["manager:eth0", "sw-back:3"]]


def lab2_config(devs):
    by = {d["id"]: d for d in devs}
    for i, (id, ip, gw) in enumerate([("till-1", "192.168.1.11", "192.168.1.1"), ("till-2", "192.168.1.12", "192.168.1.1"), ("accounts", "192.168.2.21", "192.168.2.1"), ("manager", "192.168.2.22", "192.168.2.1")]):
        by[id]["ip"], by[id]["gw"] = ip, gw
    by["r1"]["ifs"]["g0/0"] = {"ip": "192.168.1.1", "bits": 24}
    by["r1"]["ifs"]["g0/1"] = {"ip": "192.168.2.1", "bits": 24}


def lab2():
    devs = lab2_devices()
    tasks = [
        task("t1", "Cable both networks and the router", {"all": [linked("till-1", "sw-shop"), linked("till-2", "sw-shop"), linked("r1", "sw-shop"), linked("r1", "sw-back"), linked("accounts", "sw-back"), linked("manager", "sw-back")]}, "Design mode, Cable. Cable the router to the shop switch first, so its first interface, G0/0, faces the shop; G0/1 then faces the back office."),
        task("t2", "Give the router 192.168.1.1 on the shop side and 192.168.2.1 on the back-office side", {"all": [{"ifip": ["r1", "g0/0", "192.168.1.1/24"]}, {"ifip": ["r1", "g0/1", "192.168.2.1/24"]}]}, "Click the router and fill in its interface table."),
        task("t3", "Address the four computers and set each one's gateway to the router on its own side", {"all": [ipis("till-1", "192.168.1.11", 24, "192.168.1.1"), ipis("till-2", "192.168.1.12", 24, "192.168.1.1"), ipis("accounts", "192.168.2.21", 24, "192.168.2.1"), ipis("manager", "192.168.2.22", 24, "192.168.2.1")]}),
        task("t4", "Ping accounts from till-1 across the router", {"all": [{"flag": "ping:till-1>accounts:ok"}]}, "Simulation mode, till-1's desktop, Command line: ping 192.168.2.21", True),
        task("t5", "Break the gateway on manager and see it lose the shop network", {"all": [{"flag": "ping:manager>till-1:fail"}]}, "In Design mode clear manager's gateway, then in Simulation mode ping 192.168.1.11 from manager's Command line.", True),
    ]
    return doc("n02", "Network lab 2: Two networks and a router", "Banyan Books has opened a back office. Join the shop and the back office with one router.", devs, lab2_cables(), tasks)


def lab3():
    devs = lab2_devices()
    lab2_config(devs)
    devs.append(host("web01", "server", 670, 190, "linux", services={"web": False, "dns": False}, records="", page="Welcome to Banyan Books"))
    devs.append(host("dns01", "server", 545, 330, "linux", services={"web": False, "dns": False}, records=""))
    cables = lab2_cables() + [["web01:eth0", "sw-back:4"], ["dns01:eth0", "sw-back:5"]]
    names = ["till-1", "till-2", "accounts", "manager", "web01", "dns01"]
    tasks = [
        task("t1", "Address web01 (192.168.2.80) and dns01 (192.168.2.53), gateway 192.168.2.1", {"all": [ipis("web01", "192.168.2.80", 24, "192.168.2.1"), ipis("dns01", "192.168.2.53", 24, "192.168.2.1")]}, "Design mode: click each server and fill in its panel."),
        task("t2", "Turn on the web server on web01 and the DNS server on dns01, with a record www.banyan.lan 192.168.2.80", {"all": [{"svc": ["web01", "web"]}, {"svc": ["dns01", "dns"]}, {"resolve": ["till-1", "www.banyan.lan", "192.168.2.80"]}]}, "Simulation mode: on web01's desktop open Web server and press Start; on dns01 open DNS server, add the record and press Start."),
        task("t3", "Set the DNS server to 192.168.2.53 on every computer", {"all": [{"dev": n, "dns": "192.168.2.53"} for n in names]}),
        task("t4", "Open http://www.banyan.lan from till-1 and from accounts", {"all": [{"web": ["till-1", "www.banyan.lan"]}, {"web": ["accounts", "www.banyan.lan"]}]}, "Simulation mode, till-1's desktop, Web browser: www.banyan.lan"),
        task("t5", "Break till-2 in one way: change its gateway to 192.168.1.100, and see the site fail for it", {"all": [{"dev": "till-2", "gw": "192.168.1.100"}, {"web": ["till-2", "www.banyan.lan"], "ok": False}]}, "Then walk the layers from till-2's Command line: ipconfig, ping the gateway, ping the DNS server, nslookup, then the Web browser.", True),
        task("t6", "Find the fault and fix it: till-2's gateway is 192.168.1.1 again and the site opens", {"all": [{"flag": "keep:t5"}, {"dev": "till-2", "gw": "192.168.1.1"}, {"web": ["till-2", "www.banyan.lan"]}]}),
    ]
    d = doc("n03", "Network lab 3: DNS, a web server and a fault", "Give the Banyan Books network names and a web server, then find a deliberate fault the way a help desk does: cable, address, gateway, DNS, service.", devs, cables, tasks)
    return d


def vlan_swports(staff, guest, extra=None):
    sw = {}
    for p in range(1, 13):
        sw[str(p)] = {"mode": "access", "vlan": 10}
    for p in range(13, 21):
        sw[str(p)] = {"mode": "access", "vlan": 20}
    if extra:
        sw.update(extra)
    return {"sw1": sw}


def office_devices(addressed, cabled_router=False):
    d = [switch("sw1", 380, 190, ports=26),
         host("staff-1", "pc", 100, 70, "windows"), host("staff-2", "pc", 100, 220, "windows"),
         host("guest-1", "pc", 660, 70, "windows"), host("guest-2", "pc", 660, 220, "windows")]
    if addressed:
        gw = lambda v: "192.168.%d.1" % v if cabled_router else ""
        by = {x["id"]: x for x in d}
        for id, ip, v in (("staff-1", "192.168.10.11", 10), ("staff-2", "192.168.10.12", 10), ("guest-1", "192.168.20.31", 20), ("guest-2", "192.168.20.32", 20)):
            by[id]["ip"], by[id]["gw"] = ip, gw(v)
    return d


def office_cables():
    return [["staff-1:eth0", "sw1:1"], ["staff-2:eth0", "sw1:2"], ["guest-1:eth0", "sw1:13"], ["guest-2:eth0", "sw1:14"]]


def lab4():
    devs = office_devices(False)
    tasks = [
        task("t1", "Cable staff-1 and staff-2 to Fa0/1 and Fa0/2, guest-1 and guest-2 to Fa0/13 and Fa0/14, and give them the plan's addresses", {"all": [{"cable": "sw1:1", "to": "staff-1"}, {"cable": "sw1:2", "to": "staff-2"}, {"cable": "sw1:13", "to": "guest-1"}, {"cable": "sw1:14", "to": "guest-2"},
              ipis("staff-1", "192.168.10.11"), ipis("staff-2", "192.168.10.12"), ipis("guest-1", "192.168.20.31"), ipis("guest-2", "192.168.20.32")]}, "Set Cable to Copper Straight-Through so you can pick the switch port. Addresses go in each PC's panel on the right.", True),
        task("t2", "Create VLAN 10 named STAFF and VLAN 20 named GUEST", {"all": [{"vlanName": "sw1:10", "is": "STAFF"}, {"vlanName": "sw1:20", "is": "GUEST"}]}, "CLI and Desktop tab, sw1: enable, configure terminal, vlan 10, name STAFF."),
        task("t3", "Put ports 1 to 12 in VLAN 10 and ports 13 to 20 in VLAN 20, all as access ports", {"all": [{"port": "sw1:%d" % p, "vlan": 10, "mode": "access"} for p in range(1, 13)] + [{"port": "sw1:%d" % p, "vlan": 20, "mode": "access"} for p in range(13, 21)]}, "interface range fa0/1-12, then switchport mode access, switchport access vlan 10."),
        task("t4", "Ping staff-2 from staff-1, and see guest-1 fail", {"all": [{"flag": "ping:staff-1>staff-2:ok"}, {"flag": "ping:staff-1>guest-1:fail"}]}, "CLI and Desktop tab, staff-1: ping 192.168.10.12 then ping 192.168.20.31.", True),
        task("t5", "Give guest-1 the staff address 192.168.10.99 and see that ping to staff-1 still fails", {"all": [ipis("guest-1", "192.168.10.99"), {"ping": ["guest-1", "staff-1"], "ok": False}]}, "The switch port decides the VLAN, not the address.", True),
    ]
    return doc("n04", "Network lab 4: VLANs for staff and guests", "Tulsi Travels' front office has one switch. Staff and visiting customers must not share a network.", devs, [], tasks)


def lab4_done():
    devs = office_devices(True, False)
    return devs, office_cables(), vlan_swports(12, 8), {"sw1:10": "STAFF", "sw1:20": "GUEST"}


def lab5():
    devs, cables, swp, vn = lab4_done()
    devs.append(router("r1", 380, 330, {"g0/0": {"shut": True}, "g0/1": {"shut": True}, "g0/2": {"shut": True}, "g0/3": {"shut": True}}))
    tasks = [
        task("t1", "Cable switch Gi0/1 to router G0/0 and make the switch port a trunk", {"all": [{"cable": "sw1:25", "to": "r1"}, {"port": "sw1:25", "mode": "trunk"}]}, "Set Cable to Copper Straight-Through, click the switch then the router, and pick Gi0/1 and G0/0. On the switch: interface gi0/1, switchport mode trunk."),
        task("t2", "Bring G0/0 up and make subinterface g0/0.10 (VLAN 10, 192.168.10.1/24)", {"all": [{"ifup": ["r1", "g0/0"]}, {"ifvlan": ["r1", "g0/0.10", 10]}, {"ifip": ["r1", "g0/0.10", "192.168.10.1/24"]}]}, "Router console: interface g0/0, no shutdown, then interface g0/0.10, encapsulation dot1Q 10, ip address 192.168.10.1 255.255.255.0."),
        task("t3", "Make subinterface g0/0.20 (VLAN 20, 192.168.20.1/24)", {"all": [{"ifvlan": ["r1", "g0/0.20", 20]}, {"ifip": ["r1", "g0/0.20", "192.168.20.1/24"]}]}),
        task("t4", "Set every computer's gateway to the router address for its VLAN", {"all": [{"dev": "staff-1", "gw": "192.168.10.1"}, {"dev": "staff-2", "gw": "192.168.10.1"}, {"dev": "guest-1", "gw": "192.168.20.1"}, {"dev": "guest-2", "gw": "192.168.20.1"}]}),
        task("t5", "Ping staff-1 from guest-1 and notice the new risk", {"flag": "ping:guest-1>staff-1:ok"}, "CLI and Desktop tab, guest-1: ping 192.168.10.11. Guests can now reach staff, which lab 7 fixes.", True),
    ]
    return doc("n05", "Network lab 5: Routing between VLANs", "Carry both VLANs to a router over one trunk, give each VLAN a gateway on a subinterface, and route between them.", devs, cables, tasks, swp, vn)


def lab5_done():
    devs, cables, swp, vn = lab4_done()
    by = {d["id"]: d for d in devs}
    for id in ("staff-1", "staff-2"):
        by[id]["gw"] = "192.168.10.1"
    for id in ("guest-1", "guest-2"):
        by[id]["gw"] = "192.168.20.1"
    devs.append(router("r1", 380, 330, {"g0/0": {}, "g0/1": {}, "g0/2": {}, "g0/3": {}, "g0/0.10": {"vlan": 10, "ip": "192.168.10.1", "bits": 24}, "g0/0.20": {"vlan": 20, "ip": "192.168.20.1", "bits": 24}}))
    cables = cables + [["sw1:25", "r1:g0/0"]]
    swp["sw1"]["25"] = {"mode": "trunk"}
    return devs, cables, swp, vn


def lab6():
    devs, cables, swp, vn = lab5_done()
    sec = [task("p%d" % p, "", {"sec": "sw1:%d" % p, "on": True, "max": 1, "sticky": True, "viol": "shutdown"}) for p in range(1, 13)]
    tasks = [
        task("t1", "Create VLAN 999 named PARKING and move ports 21 to 24 into it, shut down", {"all": [{"vlanName": "sw1:999", "is": "PARKING"}] + [{"port": "sw1:%d" % p, "vlan": 999, "shut": True, "mode": "access"} for p in range(21, 25)]}, "interface range fa0/21-24, switchport access vlan 999, shutdown."),
        task("t2", "Turn on port security on ports 1 to 12: maximum 1, sticky, violation shutdown", {"all": [t["check"] for t in sec]}, "interface range fa0/1-12, then switchport port-security, switchport port-security maximum 1, switchport port-security mac-address sticky, switchport port-security violation shutdown."),
        task("t3", "Unplug staff-2 from Fa0/2, plug an unknown laptop into it, and watch the port err-disable", {"errdis": "sw1:2"}, "Click staff-2's cable and Unplug it. Add a laptop, give it 192.168.10.50, and cable it to Fa0/2 with Copper Straight-Through. show interfaces status then shows err-disabled.", True),
        task("t4", "Set an enable secret and a console password on the switch", {"all": [{"secret": ["sw1", "enable"]}, {"secret": ["sw1", "console"]}]}, "enable secret WORD, then line console 0, password WORD, login."),
    ]
    return doc("n06", "Network lab 6: Lock down the switch", "Park and shut unused ports, allow one known device per staff port, and protect management access.", devs, cables, tasks, swp, vn)


def lab6_done():
    devs, cables, swp, vn = lab5_done()
    for p in range(21, 25):
        swp["sw1"][str(p)] = {"mode": "access", "vlan": 999, "shut": True}
    for p in range(1, 13):
        swp["sw1"][str(p)]["sec"] = {"on": True, "max": 1, "viol": "shutdown", "sticky": True}
    vn["sw1:999"] = "PARKING"
    for d in devs:
        if d["id"] == "sw1":
            d["secrets"] = {"enable": True, "console": True}
    return devs, cables, swp, vn


def lab7():
    devs, cables, swp, vn = lab6_done()
    devs.append(host("files01", "server", 230, 330, "linux", services={"web": False, "dns": False}))
    devs.append(host("web-out", "server", 560, 330, "linux", services={"web": True, "dns": False}, page="Public web server"))
    tasks = [
        task("t1", "Cable files01 to a staff port and address it (192.168.10.10, gateway 192.168.10.1)", {"all": [linked("files01", "sw1"), ipis("files01", "192.168.10.10", 24, "192.168.10.1")]}, "Staff ports are the VLAN 10 ports 1 to 12. Use Copper Straight-Through and pick Fa0/3."),
        task("t2", "Cable web-out to router G0/1, address both ends (router 203.0.113.1/24, web-out 203.0.113.10 gateway 203.0.113.1)", {"all": [linked("web-out", "r1"), {"ifip": ["r1", "g0/1", "203.0.113.1/24"]}, {"ifup": ["r1", "g0/1"]}, ipis("web-out", "203.0.113.10", 24, "203.0.113.1")]}),
        task("t3", "Write access list 120 and apply it inbound on g0/0.20", {"all": [{"aclin": ["r1", "g0/0.20", "120"]}, {"acl": ["r1", "120", 4]}]}, "access-list 120 deny ip 192.168.20.0 0.0.0.255 192.168.10.0 0.0.0.255, then permit tcp ... any eq 80, permit udp ... any eq 53, deny ip any any."),
        task("t4", "From guest-1, open web-out in the browser, then ping files01 and see it blocked", {"all": [{"web": ["guest-1", "203.0.113.10"]}, {"ping": ["guest-1", "files01"], "ok": False}]}, "CLI and Desktop tab, guest-1: curl 203.0.113.10, then ping 192.168.10.10."),
        task("t5", "Check staff are not restricted: staff-1 reaches files01 and web-out", {"all": [{"ping": ["staff-1", "files01"]}, {"web": ["staff-1", "203.0.113.10"]}]}),
    ]
    return doc("n07", "Network lab 7: An access list that keeps guests out", "Write the policy as an access list: guests may browse the web but may not reach anything in the staff network.", devs, cables, tasks, swp, vn)


def lab8():
    devs = [host("pc1", "pc", 130, 190, "vpcs", name="PC1", power=False), host("pc2", "pc", 640, 190, "vpcs", name="PC2", power=False), switch("sw1", 385, 190, ports=8, name="SW1", builtin=True, power=False)]
    tasks = [
        task("t0", "Start all three nodes", {"all": [{"power": n} for n in ("pc1", "pc2", "sw1")]}, "Press Start all, or right-click each node and pick Start."),
        task("t1", "Cable PC1 and PC2 to SW1", {"all": [linked("pc1", "sw1"), linked("pc2", "sw1")]}),
        task("t2", "Give PC1 10.0.0.1/24 and PC2 10.0.0.2/24, gateway 10.0.0.254", {"all": [ipis("pc1", "10.0.0.1", 24, "10.0.0.254"), ipis("pc2", "10.0.0.2", 24, "10.0.0.254")]}, "Double-click PC1 to open its console, then type: ip 10.0.0.1/24 10.0.0.254"),
        task("t3", "Start a capture on the link between PC1 and SW1", {"flag": "cap:start"}, "Right-click the link between PC1 and SW1 and pick Start capture.", True),
        task("t4", "Ping PC2 from PC1 while capturing", {"flag": "ping:pc1>pc2:ok"}, "", True),
        task("t5", "Filter on arp, then click the ARP request and read who is asking", {"all": [{"flag": "cap:filter:arp"}, {"flag": "cap:saw:arp"}]}, "In the Capture tab, type arp in the Display filter box and press Enter, then click a row.", True),
        task("t6", "Find an ICMP echo reply and read its TTL", {"flag": "cap:saw:icmpreply"}, "Filter icmp, then click a reply row.", True),
    ]
    return doc("n08", "Network lab 8: Capture a link", "Two virtual PCs and a switch. Capture the cable between PC1 and the switch and read the packets of one ping.", devs, [], tasks)


LABS = {
    "n01-filius-your-first-network": lab1,
    "n02-filius-two-networks-and-a-router": lab2,
    "n03-filius-dns-web-and-a-fault": lab3,
    "n04-pt-vlans-staff-and-guest": lab4,
    "n05-pt-router-on-a-stick": lab5,
    "n06-pt-lock-down-the-switch": lab6,
    "n07-pt-acl-guests-stay-out": lab7,
    "n08-gns3-capture-a-link": lab8,
}

NOTE = "\nWhere: this lab runs in the Hacker Room's {prog}, with its starting network and goals. Nothing to install. In the Hacker Room open Start, Workplace, Network lab and pick this lab, or open netbuilder.json from Files.\n"


def main():
    for folder, fn in LABS.items():
        d = fn()
        out = SEM / folder / "files" / "netbuilder.json"
        out.write_text(json.dumps(d, indent=1) + "\n", encoding="utf-8")
        readme = SEM / folder / "files" / "README.txt"
        text = readme.read_text(encoding="utf-8")
        for mark in ("Browser version:", "Where: this lab runs"):
            if mark in text:
                text = text[:text.index(mark)]
        readme.write_text(text.rstrip("\n") + "\n" + NOTE.format(prog=PROGRAM_NAME[d["program"]]), encoding="utf-8")
        print("wrote", out.relative_to(ROOT))


if __name__ == "__main__":
    main()
