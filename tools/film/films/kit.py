import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]

TREE = '''import csv
import sys

rows = [r for r in csv.DictReader(open("process.csv")) if r["host"] == sys.argv[1]]
kids = {}
for r in rows:
    kids.setdefault(r["ppid"], []).append(r)
pids = {r["pid"] for r in rows}


def show(r, depth):
    print("    " * depth + r["time"][11:] + "  " + r["pid"].rjust(5) + "  " + r["command_line"][:84])
    for k in sorted(kids.get(r["pid"], []), key=lambda x: x["time"]):
        show(k, depth + 1)


for r in sorted(rows, key=lambda x: x["time"]):
    if r["ppid"] not in pids:
        show(r, 0)
'''

REPLAY = '''import fnmatch
import json
import sys

pol = json.load(open(sys.argv[1]))
log = json.load(open("cloud/audit.json"))


def allowed(e):
    ident = {i["name"]: i for i in pol["identities"]}.get(e["identity"])
    stmts = [s for p in (ident or {}).get("policies", []) for s in p["statements"]]
    stmts += [s for g in pol.get("org_guardrails", []) for s in g["statements"]]

    def hit(s):
        return any(a in ("*", e["action"]) for a in s["actions"]) and any(fnmatch.fnmatch(e.get("resource") or "*", r) for r in s["resources"])
    if any(s["effect"] == "Deny" and hit(s) for s in stmts):
        return False
    return any(s["effect"] == "Allow" and hit(s) for s in stmts)


bad = [e for e in log if e["source_ip"] == sys.argv[2] and allowed(e)]
broken = [e for e in log if e["source_ip"] != sys.argv[2] and e["result"] == "success" and not allowed(e)]
print("attacker actions still allowed:", len(bad))
print("normal actions broken:        ", len(broken))
for e in bad + broken:
    print("  ", e["time"][11:19], e["identity"], e["action"], e.get("resource", ""))
'''

term = {"open": "xfce4-terminal --working-directory=/case --title=Terminal --zoom=1.5 --hide-menubar", "window": "Terminal", "as": "term", "geometry": [60, 50, 1800, 960]}
clear = {"keys": ["ctrl+l"]}


def files_window(path="/case"):
    return {"open": f"thunar {path}", "window": "Thunar", "as": "files", "geometry": [260, 120, 1400, 820], "settle": 1.5}


def cmd(text, wait=2.0, cps=16):
    return {"use": "term", "at": [0.5, 0.45], "keys": ["ctrl+u"], "type": text, "wait": wait, "cps": cps}


def say(t):
    return {"say": t}


def after(t):
    return {"after": t}


def chapter(t):
    return {"chapter": t}


def edit(path, name="note", geometry=(160, 90, 1600, 900)):
    return {"open": f"mousepad {path}", "window": Path(path).name, "as": name, "geometry": list(geometry), "settle": 1.5}


def write(text, name="note", cps=30, enter=False):
    return {"use": name, "at": [0.5, 0.3], "type": text, "enter": enter, "cps": cps}


def save_note(name="note"):
    return {"use": name, "at": [0.5, 0.3], "keys": ["ctrl+s"], "wait": 1}


def close(name):
    return {"close": name, "wait": 0.8}


def wait(s):
    return {"wait": s}


def build(folder, scenes, host="analyst-ws", files=None, setup=None, pcap=None, hosts=None):
    film = {"host": host, "setup": list(setup or []), "files": dict(files or {}), "scenes": scenes}
    if hosts:
        film["hosts"] = dict(hosts)
    if pcap:
        film["pcap"] = list(pcap)
    out = ROOT / "source" / "seminars" / folder / "film.json"
    out.write_text(json.dumps(film, ensure_ascii=False, indent=1) + "\n", encoding="utf-8", newline="\n")
    words = sum(len((s.get("say") or s.get("after") or "").split()) for s in scenes)
    print(folder, "scenes", len(scenes), "words", words, "about", round(words / 2.5 / 60, 1), "min of narration")
