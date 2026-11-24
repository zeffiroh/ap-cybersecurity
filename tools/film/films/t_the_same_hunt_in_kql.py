import json

from kit import ROOT, after, build, chapter, clear, close, cmd, files_window, say, term, wait

S = json.loads((ROOT / "source" / "seminars" / "t-the-same-hunt-in-kql" / "seminar.json").read_text(encoding="utf-8"))["script"]

APP = "http://localhost:8099/playground.html?tool=siem&notour=1"
BOX = [0.411, 0.375]
KQL = [0.052, 0.375]


def search(text):
    return [
        {"point": BOX, "in": "web", "secs": 0.7, "click": True},
        {"use": "web", "at": BOX, "keys": ["ctrl+a"], "type": text, "enter": True, "cps": 22, "wait": 4},
    ]


hunt = S["steps"][1]
i = hunt["after"].index("Now the pivot")
a1, a2 = hunt["after"][:i].strip(), hunt["after"][i:].strip()

scenes = [
 chapter("Opening"),
 files_window(),
 say(S["intro"]),
 chapter("1. The setting"),
 {"point": [0.45, 0.3], "in": "files", "secs": 1.0},
 say(S["steps"][0]["say"]),
 close("files"),
 term,
 cmd("head -3 auth.log | cut -c1-150", 3),
 clear,
 chapter("2. The same hunt in KQL"),
 say(hunt["say"]),
 {"open": ["firefox-esr", "--new-window", APP], "window": "Mozilla Firefox|Playground|playground", "as": "web", "geometry": [60, 50, 1800, 960], "timeout": 60, "settle": 5},
 wait(30),
 {"use": "web", "at": [0.5, 0.35], "keys": ["ctrl+minus"], "wait": 1.5},
 {"use": "web", "at": [0.5, 0.35], "keys": ["ctrl+minus"], "wait": 1.5},
 {"use": "web", "at": [0.5, 0.35], "keys": ["ctrl+minus"], "wait": 1.5},
 {"use": "web", "at": [0.5, 0.5], "keys": ["Home"], "wait": 1.5},
 {"point": KQL, "in": "web", "secs": 0.7, "click": True, "wait": 1.5},
 *search('auth | where action == "failure" | summarize count() by src_ip | sort by count_ desc'),
 after(a1),
 *search('auth | where src_ip == "203.0.113.45" and action == "success" | project _time, user, auth_method'),
 after(a2),
 close("web"),
 clear,
 chapter("3. Where next"),
 say(S["steps"][2]["say"]),
 chapter("Wrap-up"),
 say(S["outro"]),
 wait(2),
]

build("t-the-same-hunt-in-kql", scenes, host="chandni-soc",
      setup=["nohup python3 -m http.server 8099 -d /opt/site >/dev/null 2>&1 &"])
