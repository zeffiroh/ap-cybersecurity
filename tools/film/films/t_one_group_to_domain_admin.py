from kit import after, build, chapter, clear, close, cmd, edit, files_window, save_note, say, term, wait, write

PATHS = '''import csv
import sys

start, goal = sys.argv[1], sys.argv[2]
edges = []
for r in csv.DictReader(open("identity/ad_edges.csv")):
    if r["relation"] == "HasSessionOn":
        edges.append((r["target"], "takes saved password of", r["source"]))
    else:
        edges.append((r["source"], r["relation"], r["target"]))


def walk(node, path):
    if node == goal:
        yield path
        return
    for a, rel, b in edges:
        if a == node and b not in [p[2] for p in path] and b != start:
            yield from walk(b, path + [(a, rel, b)])


best = min(walk(start, []), key=len)
for a, rel, b in best:
    print(f"{a:12} --{rel}-->  {b}")
on = {(a, b) for a, _, b in best}
with open("graph.dot", "w") as f:
    f.write("digraph AD {\\n rankdir=LR; node [shape=box, style=rounded, fontname=\\"DejaVu Sans\\", fontsize=16];\\n")
    for a, rel, b in edges:
        hot = (a, b) in on
        f.write(f' "{a}" -> "{b}" [label="{rel}", fontsize=12, color="{"red" if hot else "gray60"}", penwidth={3 if hot else 1}];\\n')
    f.write("}\\n")
'''

FIX = """FIX, HOP BY HOP   Nimbus Analytics   10 Nov 2026 (UTC)
Hop 1  Helpdesk can reset svc-sql           remove the old reset right on the Service Accounts folder
Hop 4  adm.k.nair's saved login on app02    run Nightly KPI export as a low-privilege account
Both together close every path to Domain-Admins that goes through app02.
"""

scenes = [
 chapter("Opening"),
 files_window(),
 say("Hello, and welcome. In most companies, the attacker's goal is Domain Admins, the group that controls every Windows computer and account. They rarely get there with a single trick. They walk there, one permission at a time. Today you'll follow that walk from a helpdesk account to the top."),
 {"point": [0.45, 0.3], "in": "files", "secs": 1.0},
 say("The setting. Nimbus Analytics in Hyderabad, Tuesday the tenth of November 2026. All times are UTC. A helpdesk worker, h.verma, fell for a phishing email, so the attacker has that account's password. The case folder has the company's identity data: which accounts are in which groups, and what each group is allowed to do."),
 close("files"),
 term,

 chapter("1. The identity data"),
 say("First, who's who, and which accounts are protected by multi-factor sign-in."),
 cmd("column -t -s, identity/users.csv | cut -c1-170", 4),
 cmd("column -t -s, identity/ad_edges.csv | cut -c1-150", 4),
 after("Look at line two: Helpdesk can force a password change on svc-sql, inherited since 2023. And adm.k.nair has a session on app02, because a scheduled task runs as that account with a saved password."),
 clear,

 chapter("2. Walk it like an attacker"),
 say("Switch sides and think like the attacker. Defenders think in lists. Attackers think in graphs: from where I am, what can I reach? This short Python script follows the edges from h.verma, the phished account, to Domain-Admins, and writes the whole graph for Graphviz to draw."),
 edit("paths.py", "code", (200, 60, 1500, 950)),
 wait(4),
 after("A saved password on a machine you control counts as an edge, because an administrator can take it from memory or the registry."),
 close("code"),
 cmd("python3 paths.py h.verma Domain-Admins", 3),
 after("Let's read the path, hop by hop. h.verma is a member of Helpdesk. Helpdesk has ForceChangePassword on svc-sql, a service account. That hop needs no new password: the attacker simply sets a new one. svc-sql is a member of Server-Admins. Server-Admins is admin on app02. adm.k.nair has a saved login on app02, and adm.k.nair is a member of Domain-Admins."),
 cmd("dot -Tpng graph.dot -o graph.png && echo drawn", 3),
 {"open": ["firefox-esr", "--new-window", "file:///case/graph.png"], "window": "graph.png", "as": "img", "geometry": [60, 50, 1800, 960], "timeout": 60, "settle": 2},
 wait(4),
 after("The red path: phished helpdesk account, reset a service account's password, admin on a server, take the saved Domain Admin login. Game over, and no exploit anywhere. Every arrow is a setting someone chose."),
 close("img"),
 clear,

 chapter("3. Break the path"),
 say("So which single change breaks the most paths? Removing the saved Domain Admin login from app02, by running that task as a low-privilege account, breaks every path that goes through it. Removing the old helpdesk reset right closes the door at the start. Do both."),
 edit("fix.txt"),
 write(FIX, cps=44),
 save_note(),
 close("note"),
 clear,

 chapter("Where next"),
 say("That was one step from Seminar 7, Identity from both sides: AD, Entra and cloud IAM. The full seminar has a longer video, every step at three levels, a graded hand-in that I mark myself, and a certificate at the end. The links are on your screen."),
 chapter("Wrap-up"),
 say("To recap. Attackers think in graphs, not lists. Follow each permission one hop at a time, and remember that a saved password is an edge. Then fix the hop that breaks the most paths. Thank you for watching."),
 wait(2),
]

build("t-one-group-to-domain-admin", scenes, host="nimbus-soc", files={"paths.py": PATHS})
