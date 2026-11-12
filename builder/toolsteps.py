import json
import re

FENCE = re.compile(r"^```tool ([a-z0-9][a-z0-9-]*)\n(.*?)\n```$", re.M | re.S)


def fence(tool, state):
    return f"```tool {tool}\n{json.dumps(state, ensure_ascii=False)}\n```"


def steps_in(text):
    out = []
    for m in FENCE.finditer(text or ""):
        try:
            state = json.loads(m.group(2))
        except ValueError:
            continue
        if isinstance(state, dict):
            out.append((m.group(1), state))
    return out


def rewrite(text, change):
    def one(m):
        try:
            state = json.loads(m.group(2))
        except ValueError:
            return m.group(0)
        return fence(m.group(1), change(state)) if isinstance(state, dict) else m.group(0)
    return FENCE.sub(one, text or "")


def map_strings(value, change):
    if isinstance(value, str):
        return change(value)
    if isinstance(value, list):
        return [map_strings(v, change) for v in value]
    if isinstance(value, dict):
        return {k: map_strings(v, change) for k, v in value.items()}
    return value


def scrubbed(text, change):
    return rewrite(text, lambda state: map_strings(state, change))


def files_used(state):
    names = [state.get("file")] + list(state.get("files") or [])
    return {n for n in names if isinstance(n, str) and n}


def blanked(text):
    def hide(state):
        fields = [f for f in state.get("blank", []) if isinstance(f, str) and f in state]
        if fields:
            state = dict(state)
            state["a"] = {f: state[f] for f in fields}
            for f in fields:
                state[f] = ""
        return state
    return rewrite(text, hide)


TITLES = {"siem": "SIEM search", "logsearch": "Log search tool", "packets": "Packet viewer", "proxy": "Web proxy", "events": "Event viewer",
          "yara": "YARA rules", "sigma": "Sigma rules", "sql": "SQL over logs", "alerts": "Alert queue", "hunt": "Threat hunt",
          "ioc": "Indicators and ATT&CK", "email": "Email triage",
          "timeline": "Merged timeline", "proctree": "Process tree", "hex": "Hex, strings and hashes", "tabletop": "Tabletop exercise", "report": "Report builder",
          "firewall": "Firewall and segmentation", "ids": "IDS rules", "harden": "Hardening audit", "patch": "CVSS and patch priority",
          "identity": "Identity and access", "mailauth": "SPF, DKIM and DMARC", "soar": "SOAR playbook", "parse": "Log parser",
          "cloudiam": "Cloud IAM simulator", "codescan": "Code and config scanner", "jwt": "JWT inspector", "regex": "Regex tester",
          "crack": "Password cracking lab", "risk": "Risk register", "threatmodel": "Threat model", "compliance": "Compliance gap check",
          "certin": "CERT-In filing and inbox", "aisec": "AI security simulator"}

TOOL_FILES = ["tool-logsearch.js", "tool-siem.js", "tool-packets.js", "tool-proxy.js", "tool-events.js",
              "tool-yara.js", "tool-sigma.js", "tool-sql.js", "tool-alerts.js", "tool-hunt.js", "tool-ioc.js", "tool-email.js",
              "tool-timeline.js", "tool-proctree.js", "tool-hex.js", "tool-tabletop.js", "tool-report.js",
              "tool-firewall.js", "tool-ids.js", "tool-harden.js", "tool-patch.js", "tool-identity.js", "tool-mailauth.js", "tool-soar.js", "tool-parse.js",
              "tool-cloudiam.js", "tool-codescan.js", "tool-jwt.js", "tool-regex.js", "tool-crack.js", "tool-risk.js", "tool-threatmodel.js", "tool-compliance.js",
              "tool-certin.js", "tool-aisec.js"]


def printable(text):
    def one(m):
        try:
            state = json.loads(m.group(2))
        except ValueError:
            return m.group(0)
        if m.group(1) == "siem" and isinstance(state, dict):
            query = str(state.get("q") or "").replace("`", "'")
            lang = " (KQL)" if state.get("lang") == "kql" else ""
            return f"**Use {TITLES[m.group(1)]}{lang}.** Search: `{query}`" if query else f"**Use {TITLES[m.group(1)]}{lang}.**"
        name = state.get("file", "") if isinstance(state, dict) else ""
        title = TITLES.get(m.group(1), f"{m.group(1)} tool")
        return f"**Use the {title} on {name}.**" if name else f"**Use the {title}.**"
    return FENCE.sub(one, text or "")


def count_problems(cells, files):
    problems = []
    for c in cells:
        if c.get("t") != "md":
            continue
        for tool, state in steps_in(c.get("s")):
            if tool == "siem":
                for name in state.get("files") or []:
                    if name not in files:
                        problems.append(f"The SIEM search {state.get('q', '')!r} used {name}, which isn't in the lab's files. Add it, or students get a different count.")
                continue
            if tool != "logsearch":
                name = state.get("file")
                if name and name not in files:
                    problems.append(f"A {TITLES.get(tool, tool + ' tool')} step uses {name}, which isn't in the lab's files. Add it, or students can't run the step.")
                continue
            name, query = state.get("file"), state.get("q", "")
            if name not in files:
                problems.append(f"A log search uses {name}, which isn't in the lab's files. Add it, or students can't run the search.")
                continue
            try:
                pattern = re.compile(query, re.I)
            except re.error:
                pattern = re.compile(re.escape(query), re.I)
            lines = files[name].replace("\r", "").removesuffix("\n").split("\n")
            found = sum(1 for line in lines if pattern.search(line))
            if found != state.get("n"):
                problems.append(f"The log search {query!r} found {state.get('n')} lines when recorded and {found} in the published file. Check it.")
    return problems
