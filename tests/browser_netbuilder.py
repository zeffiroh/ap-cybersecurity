import functools
import socketserver
import sys
import threading
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import browser_soc as B

check, msg, mount = B.check, B.msg, B.mount

LAB1 = "sem-n01-filius-your-first-network"
LAB3 = "sem-n03-filius-dns-web-and-a-fault"
LAB4 = "sem-n04-pt-vlans-staff-and-guest"
LAB8 = "sem-n08-gns3-capture-a-link"


def dev(page, name):
    return page.locator(f'.nbd-dev[data-id="{name}"]')


def cable(page, a, b, pick=False):
    page.click('[data-r="mode-cable"]')
    dev(page, a).click()
    dev(page, b).click()
    if pick:
        page.click('[data-r="cdo"]')
    page.click('[data-r="mode-select"]')


def set_field(page, device, name, value):
    dev(page, device).click()
    box = page.locator(f'[data-r="side"] [data-f="{name}"]')
    box.fill(value)
    box.press("Tab")


def type_in(page, line):
    page.fill('[data-r="cin"]', line)
    page.press('[data-r="cin"]', "Enter")


def note(page):
    return page.inner_text('[data-r="note"]')


def out(page):
    return page.inner_text('[data-r="cout"]')


def starter(page, files):
    mount(page, "netstarter", files)
    check(dev(page, "sw1").count() == 1 and page.locator(".nbd-dev").count() == 5, "Network Starter opens lab 1 with its switch and four computers")
    check(note(page).startswith("0 of 5 goals"), f"no goal is met at the start ({note(page)})")
    for name in ("till-1", "till-2", "office", "stray"):
        cable(page, name, "sw1")
    check(page.locator(".nbd-cable").count() == 4, "cables join on the first free port with no port dialog")
    check(note(page).startswith("1 of 5 goals"), "cabling all four ticks the first goal")
    for name, ip in (("till-1", "192.168.1.11"), ("till-2", "192.168.1.12"), ("office", "192.168.1.13"), ("stray", "192.168.2.14")):
        set_field(page, name, "ip", ip)
    page.click('[data-t="desktop"]')
    check("Simulation" in page.inner_text('[data-r="pane"]'), "the desktop asks for Simulation mode while in Design mode")
    page.click('[data-r="simulate"]')
    check(page.locator('[data-r="edit"]').is_hidden(), "Simulation mode hides the building tools")
    dev(page, "till-1").click()
    check("Desktop of till-1" in page.inner_text('[data-r="pane"]'), "clicking a computer in Simulation mode opens its desktop")
    type_in(page, "ping 192.168.1.12")
    check("Reply from 192.168.1.12: bytes" in out(page), f"ping from the Command line reaches till-2 ({out(page)[-80:]})")
    check(page.locator(".nbd-cable.live").count() >= 1, "the cable flashes while data crosses it")
    type_in(page, "ping 192.168.1.13")
    type_in(page, "ping 192.168.2.14")
    check("General failure" in out(page).split("ping 192.168.2.14")[-1], "stray, in another network, does not answer")
    page.click('[data-t="exchange"]')
    rows = page.locator(".nst-ex tr.pk")
    check(rows.count() >= 8, f"the data exchange lists till-1's packets ({rows.count()})")
    page.locator(".nst-ex tr.pk.icmp").first.click()
    check(msg(page).startswith("Data exchange row") and "Internet Control Message Protocol" in page.inner_text(".nbd-det"), "clicking a row shows its layers")
    page.click('[data-r="design"]')
    set_field(page, "stray", "ip", "192.168.1.14")
    page.click('[data-r="simulate"]')
    dev(page, "till-1").click()
    type_in(page, "ping 192.168.1.14")
    check("Reply from 192.168.1.14: bytes" in out(page), "fixing stray's address makes it answer")
    check(note(page).startswith("5 of 5 goals"), f"all five goals are met ({note(page)})")
    page.click('[data-r="reset"]')
    check(page.locator(".nbd-cable").count() == 0, "starting the lab again clears the cables")


def starter_servers(page, files):
    mount(page, "netstarter", files)
    set_field(page, "web01", "ip", "192.168.2.80")
    set_field(page, "web01", "gw", "192.168.2.1")
    check(page.locator('[data-r="side"] [data-f="svcweb"]').count() == 0, "services are not ticked in Design mode")
    page.click('[data-r="simulate"]')
    dev(page, "web01").click()
    page.click('[data-app="wsrv"]')
    page.click('[data-r="nst-ws"]')
    check("Web server started on web01" in msg(page), f"the web server starts from web01's desktop ({msg(page)})")
    dev(page, "till-1").click()
    page.click('[data-app="web"]')
    page.fill('[data-r="nst-url"]', "192.168.2.80")
    page.click('[data-r="nst-go"]')
    check("Welcome to Banyan Books" in page.inner_text(".nst-page"), "till-1's browser opens the page across the router")
    dev(page, "dns01").click()
    page.click('[data-app="dsrv"]')
    page.fill('[data-r="nst-dn"]', "www.banyan.lan")
    page.fill('[data-r="nst-di"]', "192.168.2.80")
    page.click('[data-r="nst-dadd"]')
    check("Record added" in msg(page) and "www.banyan.lan" in page.inner_text('[data-r="nst-app"]'), "a DNS record is added on dns01's desktop")


def simulator(page, files):
    mount(page, "netsim", files)
    check(page.locator('[data-r="ctype"]').count() == 1 and page.locator('[data-r="sm"]').count() == 1, "Network Simulator shows the cable chooser and the Realtime and Simulation switch")
    cable(page, "staff-1", "sw1")
    cable(page, "staff-2", "sw1")
    check(page.locator('.nbd-lamp[fill="#e69a1c"]').count() >= 2, "a new switch link shows amber lights while it gets ready")
    set_field(page, "staff-1", "ip", "192.168.10.11")
    set_field(page, "staff-2", "ip", "192.168.10.12")
    page.wait_for_timeout(3400)
    check(page.locator('.nbd-lamp[fill="#e69a1c"]').count() == 0, "the lights turn green after a few seconds")
    page.select_option('[data-r="ctype"]', "cross")
    page.click('[data-r="mode-cable"]')
    dev(page, "guest-1").click()
    dev(page, "sw1").click()
    check(page.locator('[data-r="cdo"]').count() == 1, "a chosen cable type asks for the ports")
    page.click('[data-r="cdo"]')
    check("wrong kind of cable" in msg(page), f"a cross-over cable from a PC to a switch stays down ({msg(page)[:80]})")
    page.select_option('[data-r="ctype"]', "auto")
    page.click('[data-r="mode-pdu"]')
    dev(page, "staff-1").click()
    dev(page, "staff-2").click()
    check("Simple PDU staff-1 to staff-2: Successful" in msg(page), f"a simple PDU succeeds ({msg(page)})")
    page.click('[data-r="sm"]')
    page.click('[data-r="mode-pdu"]')
    dev(page, "staff-2").click()
    dev(page, "staff-1").click()
    check(page.locator(".nsm-ev tr.ev").count() >= 4, f"Simulation mode queues the packet's events ({page.locator('.nsm-ev tr.ev').count()})")
    page.click('[data-r="sfwd"]')
    check(msg(page).startswith("Event 1:") and page.locator(".nsm-env").count() == 1, "Capture / Forward moves the envelope one step")
    check("PDU Information at Device" in page.inner_text(".nsm-pdu"), "the PDU panel shows the layers at that device")
    page.uncheck('[data-f="ARP"]')
    page.click('[data-r="sfwd"]')
    check(" ICMP at " in msg(page), f"filtering out ARP jumps to the ICMP events ({msg(page)})")
    page.click('[data-t="console"]')
    page.select_option('[data-r="cdev"]', "sw1")
    type_in(page, "enable")
    type_in(page, "show vlan brief")
    check("VLAN" in out(page) and page.inner_text('[data-r="cps"]').strip().endswith("#"), "the switch CLI answers IOS commands")


def emulator(page, files):
    mount(page, "netemu", files)
    check(page.locator(".nbd-dev.off").count() == 3, "Network Emulator opens lab 8 with its three nodes stopped")
    check("Topology summary" in page.inner_text('[data-r="side"]'), "the side panel is a topology summary")
    dev(page, "pc1").dblclick()
    check("stopped" in msg(page), f"a stopped node has no console ({msg(page)})")
    page.click('[data-r="startall"]')
    check(msg(page).startswith("Started 3 nodes") and page.locator(".nbd-dev.off").count() == 0, f"Start all starts every node ({msg(page)})")
    cable(page, "pc1", "sw1", pick=True)
    cable(page, "pc2", "sw1", pick=True)
    dev(page, "pc1").dblclick()
    check("Virtual PC Simulator" in out(page), "PC1's console opens with the VPCS banner")
    type_in(page, "ip 10.0.0.1/24 10.0.0.254")
    dev(page, "pc2").dblclick()
    type_in(page, "ip 10.0.0.2/24 10.0.0.254")
    check(page.locator('[data-r="ctabs"] [data-c]').count() == 2, "each open console has its own tab")
    page.locator(".nbd-cable").first.click(button="right", force=True)
    page.locator(".nbd-menu button", has_text="Start capture").click()
    check("Capturing on" in msg(page) and page.locator(".nem-cap").count() == 1, f"right-click, Start capture marks the link ({msg(page)[:60]})")
    page.click('[data-t="console"]')
    page.click('[data-r="ctabs"] [data-c="pc1"]')
    type_in(page, "ping 10.0.0.2")
    page.click('[data-t="capture"]')
    check(page.locator(".nbd-pk tr.pk").count() >= 12, f"the capture lists ARP and ten ICMP frames ({page.locator('.nbd-pk tr.pk').count()})")
    page.fill('[data-r="capfilter"]', "arp")
    page.press('[data-r="capfilter"]', "Enter")
    check(page.locator(".nbd-pk tr.pk").count() == 2, "the arp filter keeps the request and the reply")
    page.locator(".nbd-pk tr.pk").first.click()
    check("Address Resolution Protocol" in page.inner_text('[data-r="capdet"]'), "clicking a frame shows its layers")
    page.fill('[data-r="capfilter"]', "icmp")
    page.press('[data-r="capfilter"]', "Enter")
    page.locator(".nbd-pk tr.pk").nth(1).click()
    check(note(page).startswith("7 of 7 goals"), f"all seven goals are met ({note(page)})")
    page.locator(".nbd-cable").first.click(button="right", force=True)
    page.locator(".nbd-menu button", has_text="Suspend").click()
    check(page.locator(".nbd-cable.down").count() == 1, "a suspended link goes down")


def main():
    from playwright.sync_api import sync_playwright
    sys.stdout.reconfigure(encoding="utf-8")
    handler = functools.partial(B.Quiet, directory=str(B.SITE))
    with socketserver.ThreadingTCPServer(("127.0.0.1", 0), handler) as server:
        base = f"http://127.0.0.1:{server.server_address[1]}"
        threading.Thread(target=server.serve_forever, daemon=True).start()
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page, errors = B.open_page(browser, base)
            page.add_script_tag(url=f"{base}/assets/theme/workstation-net.js")
            for name, fn, case in (("Network Starter, lab 1", starter, LAB1), ("Network Starter, lab 3 servers", starter_servers, LAB3),
                                   ("Network Simulator, lab 4", simulator, LAB4), ("Network Emulator, lab 8", emulator, LAB8)):
                print(name)
                page.evaluate("() => { try { localStorage.clear(); } catch (e) {} }")
                try:
                    fn(page, B.case_files(case))
                except Exception as e:
                    check(False, f"{name} ran without an exception ({e.__class__.__name__}: {str(e)[:240]})")
            check(not errors, f"no page errors ({errors[:3]})")
            browser.close()
        server.shutdown()
    print(f"\n{len(B.FAILS)} failed" if B.FAILS else "\nall passed")
    return 1 if B.FAILS else 0


if __name__ == "__main__":
    raise SystemExit(main())
