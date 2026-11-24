import json

from kit import ROOT, after, build, chapter, clear, close, cmd, files_window, say, term, wait

S = json.loads((ROOT / "source" / "seminars" / "t-your-first-spl-search" / "seminar.json").read_text(encoding="utf-8"))["script"]

APP = "http://localhost:8099/playground.html?tool=siem&notour=1"
BOX = [0.411, 0.375]
GO = [0.809, 0.375]


def search(text):
    return [
        {"point": BOX, "in": "web", "secs": 0.7, "click": True},
        {"use": "web", "at": BOX, "keys": ["ctrl+a"], "type": text, "enter": True, "cps": 22, "wait": 4},
    ]


def cut(text, anchors):
    parts, rest = [], text
    for a in anchors:
        i = rest.index(a)
        parts.append(rest[:i].strip())
        rest = rest[i:]
    parts.append(rest.strip())
    return parts


setting, count = S["steps"][0]["say"], S["steps"][1]
a1, a2, a3, a4 = cut(count["after"], ["Now the second move", "Now pivot again", "The last search"])

scenes = [
 chapter("Opening"),
 files_window(),
 say(S["intro"]),
 chapter("1. The setting"),
 {"point": [0.45, 0.3], "in": "files", "secs": 1.0},
 say(setting),
 close("files"),
 term,
 cmd("head -3 auth.log | cut -c1-150", 3),
 clear,
 chapter("2. SPL: count, then pivot"),
 say(count["say"]),
 {"open": ["firefox-esr", "--new-window", APP], "window": "Mozilla Firefox|Playground|playground", "as": "web", "geometry": [60, 50, 1800, 960], "timeout": 60, "settle": 5},
 wait(30),
 {"use": "web", "at": [0.5, 0.35], "keys": ["ctrl+minus"], "wait": 1.5},
 {"use": "web", "at": [0.5, 0.35], "keys": ["ctrl+minus"], "wait": 1.5},
 {"use": "web", "at": [0.5, 0.35], "keys": ["ctrl+minus"], "wait": 1.5},
 {"use": "web", "at": [0.5, 0.5], "keys": ["Home"], "wait": 1.5},
 *search("sourcetype=syslog action=failure | stats count by src_ip | sort - count"),
 after(a1),
 *search("Accepted src_ip=203.0.113.45 | table _time user auth_method"),
 after(a2),
 *search("process=sshd user=catalog | table _time src_ip action"),
 after(a3),
 *search("process=sudo | table _time user run_as command"),
 after(a4),
 close("web"),
 clear,
 chapter("3. Where next"),
 say(S["steps"][2]["say"]),
 chapter("Wrap-up"),
 say(S["outro"]),
 wait(2),
]

build("t-your-first-spl-search", scenes, host="chandni-soc",
      setup=["nohup python3 -m http.server 8099 -d /opt/site >/dev/null 2>&1 &"])
