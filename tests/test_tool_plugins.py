import json
import re
import shutil
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from builder import levels as LV
from builder import toolsteps as T

CASES = ROOT / "source" / "static" / "assets" / "linux" / "cases"
THEME = ROOT / "source" / "static" / "assets" / "theme"
TSHARK = ROOT / "source" / "static" / "assets" / "linux" / "tools" / "tshark"
NODE = shutil.which("node")


def node(cmd, jobs=None):
    r = subprocess.run([NODE, str(ROOT / "tests" / "tools_js.js"), cmd], input=json.dumps(jobs or []), capture_output=True, text=True, encoding="utf-8", check=True)
    return json.loads(r.stdout)


def git_bash():
    for p in (Path("C:/Program Files/Git/bin/bash.exe"), Path("C:/Program Files/Git/usr/bin/bash.exe")):
        if p.exists():
            return str(p)
    b = shutil.which("bash")
    return b if b and "System32" not in b else None


BASH = git_bash()

SHARED_FILTERS = [
    "", "http", "dns", "tls", "smb2", "smtp", "http.request", "ip.addr==198.51.100.140", "ip.src==10.20.0.14 and http.request",
    "not dns", "frame.len > 1000", "frame.len < 100", "ip.dst==10.20.0.1", "dns.qry.name contains cdn", "http.host==kestrel-logistlcs.com",
    "http.request.method==GET", "(dns or http) and not ip.addr==10.20.0.1", "tcp.srcport==445 or tcp.dstport==445", "ip.addr!=10.20.0.14",
]


class ToolFiles(unittest.TestCase):
    def test_every_tool_is_one_registered_file(self):
        if not NODE:
            self.skipTest("node isn't installed")
        self.assertEqual(node("list"), ["events", "packets"])
        ids = set()
        for name in T.TOOL_FILES:
            text = (THEME / name).read_text(encoding="utf-8")
            self.assertIn("AayatTools.register", text)
            self.assertIsNone(re.search(r"^\s*//|/\*", text, re.M), f"{name} has a comment")
            self.assertIsNone(re.search(r"wireshark|burp|portswigger|microsoft", text, re.I), f"{name} names another company's product")
            m = re.search(r'register\(\{\s*id:\s*"([a-z0-9-]+)"', text)
            self.assertTrue(m, f"{name} registers a tool with an id")
            self.assertNotIn(m.group(1), ids)
            ids.add(m.group(1))
            self.assertIn(m.group(1), T.TITLES, f"{m.group(1)} needs a title in builder/toolsteps.py")

    def test_pages_and_studio_load_the_tools(self):
        pages = (ROOT / "builder" / "pages.py").read_text(encoding="utf-8")
        studio = (ROOT / "tools" / "studio" / "ui" / "index.html").read_text(encoding="utf-8")
        self.assertIn("*TS.TOOL_FILES", pages)
        for name in T.TOOL_FILES:
            self.assertTrue((THEME / name).exists(), name)
            self.assertIn(f"/site/assets/theme/{name}", studio)
            self.assertLess(studio.index("tools.js"), studio.index(name))
            self.assertLess(studio.index(name), studio.index("studio.js"))


class PacketFilters(unittest.TestCase):
    def setUp(self):
        if not NODE:
            self.skipTest("node isn't installed")

    def test_filters_match_the_lab_tshark(self):
        if not BASH:
            self.skipTest("Git Bash isn't installed")
        jobs, want = [], []
        for case in ("phish", "web01", "quietdns", "insider"):
            cap = CASES / case / "case" / "capture.pcap"
            for f in SHARED_FILTERS:
                args = [BASH, str(TSHARK).replace("\\", "/"), "-r", str(cap).replace("\\", "/")] + (["-Y", f] if f else [])
                r = subprocess.run(args, capture_output=True, text=True, encoding="utf-8")
                self.assertEqual(r.returncode, 0, f"{case} {f}: {r.stderr}")
                jobs.append([str(cap), f])
                want.append(len([l for l in r.stdout.splitlines() if l.strip()]))
        got = node("packets", jobs)
        for (cap, f), g, w in zip(jobs, got, want):
            self.assertEqual(g, w, f"{Path(cap).parent.parent.name}: {f!r}")

    def test_bad_filters_are_refused(self):
        cap = str(CASES / "phish" / "case" / "capture.pcap")
        got = node("packets", [[cap, f] for f in ("htttp", "ip.addr==", "(dns", "frame.len > big", "ip.src ==", "dns and")])
        for g in got:
            self.assertTrue(str(g).startswith("ERR"), g)

    def test_extra_fields(self):
        cap = str(CASES / "phish" / "case" / "capture.pcap")
        got = node("packets", [[cap, 'http.request.uri matches "\\.docm$"'], [cap, "tls.handshake.extensions_server_name == cdn-update-check.net"],
                               [cap, "http.response.code == 200"], [cap, "udp"], [cap, "tcp.stream == 0"]])
        self.assertEqual(got[0], 1)
        self.assertGreater(got[1], 0)
        self.assertGreater(got[2], 0)
        self.assertGreater(got[3], 0)
        self.assertGreater(got[4], 0)


class EventLogs(unittest.TestCase):
    def setUp(self):
        if not NODE:
            self.skipTest("node isn't installed")
        self.dir = CASES / "phish" / "case" / "eventlogs"

    def lines(self, name):
        return [json.loads(l) for l in (self.dir / name).read_text(encoding="utf-8").splitlines() if l.strip()]

    def test_logs_are_made_up_and_consistent(self):
        sec = self.lines("Security.jsonl")
        made = [e["Data"]["CommandLine"] for e in sec if e["EventID"] == 4688]
        self.assertTrue(any("INV-30412.docm" in c for c in made))
        self.assertTrue(any("svchost-upd.exe --walk" in c for c in made))
        for name in ("Security.jsonl", "System.jsonl", "Application.jsonl"):
            for e in self.lines(name):
                for ip in re.findall(r"\b\d+\.\d+\.\d+\.\d+\b", json.dumps(e)):
                    if all(int(p) < 256 for p in ip.split(".")):
                        self.assertTrue(ip.startswith(("10.", "127.", "198.51.100.", "203.0.113.", "192.0.2.")), ip)

    def test_filters_count_like_python(self):
        sec = self.dir / "Security.jsonl"
        events = self.lines("Security.jsonl")
        cases = [
            ({"ids": "4688"}, lambda e: e["EventID"] == 4688),
            ({"ids": "4720-4732"}, lambda e: 4720 <= e["EventID"] <= 4732),
            ({"ids": "4624, -4624"}, lambda e: False),
            ({"ids": "-4624,-4634,-5379"}, lambda e: e["EventID"] not in (4624, 4634, 5379)),
            ({"lv": "Audit Failure"}, lambda e: e.get("Keywords") == "Audit Failure"),
            ({"q": "svchost-upd"}, lambda e: "svchost-upd" in (e["Message"] + json.dumps(e["Data"])).lower()),
            ({"ids": "4688", "q": "net.exe"}, lambda e: e["EventID"] == 4688 and "net.exe" in e["Message"].lower()),
        ]
        got = node("events", [[str(sec), q] for q, _ in cases])
        for (q, fn), g in zip(cases, got):
            self.assertEqual(g, sum(1 for e in events if fn(e)), q)
        bad = node("events", [[str(sec), {"ids": "46x"}], [str(sec), {"ids": "4732-4720"}], [str(sec), {"lv": "Loud"}]])
        for b in bad:
            self.assertTrue(str(b).startswith("ERR"), b)


class Steps(unittest.TestCase):
    def test_blanking_hides_each_tool_answer(self):
        text = "\n\n".join([
            T.fence("packets", {"file": "capture.pcap", "f": "http.request", "n": 3, "v": "list", "blank": ["f"]}),
            T.fence("packets", {"file": "capture.pcap", "f": "", "n": 9, "v": "stream", "s": "tcp 10.0.0.1:1 10.0.0.2:80", "blank": ["f", "s"]}),
            T.fence("proxy", {"m": "POST", "p": "/api/login", "h": "Content-Type: application/json", "b": "{\"email\":\"x' --\"}", "s": 200, "blank": ["p", "b"]}),
            T.fence("events", {"file": "eventlogs/Security.jsonl", "ids": "4720", "src": "", "q": "", "lv": "", "n": 1, "blank": ["ids", "src", "q"]}),
        ])
        for level in ("guided", "solo"):
            out = LV.variant([{"t": "md", "s": text}], level)[0]["s"]
            steps = T.steps_in(out)
            self.assertEqual(len(steps), 4)
            self.assertEqual(steps[0][1]["f"], "")
            self.assertEqual(steps[0][1]["a"], {"f": "http.request"})
            self.assertEqual(steps[1][1]["s"], "")
            self.assertEqual(steps[2][1]["p"], "")
            self.assertEqual(steps[2][1]["b"], "")
            self.assertEqual(steps[2][1]["m"], "POST")
            self.assertEqual(steps[3][1]["ids"], "")
            self.assertNotIn("4720", out.replace('"a": {"ids": "4720"', ""))

    def test_printable_names_each_tool(self):
        out = T.printable(T.fence("packets", {"file": "capture.pcap"}) + "\n" + T.fence("proxy", {"m": "GET"}) + "\n" + T.fence("events", {"file": "eventlogs/Security.jsonl"}))
        self.assertIn("**Use the Packet viewer on capture.pcap.**", out)
        self.assertIn("**Use the Web proxy.**", out)
        self.assertIn("**Use the Event viewer on eventlogs/Security.jsonl.**", out)

    def test_missing_files_are_reported_for_any_tool(self):
        cells = [{"t": "md", "s": T.fence("packets", {"file": "gone.pcap", "f": "", "n": 1})}, {"t": "md", "s": T.fence("events", {"file": "eventlogs/Security.jsonl", "n": 1})}]
        problems = T.count_problems(cells, {"eventlogs/Security.jsonl": "{}"})
        self.assertEqual(len(problems), 1)
        self.assertIn("gone.pcap", problems[0])


if __name__ == "__main__":
    unittest.main()
