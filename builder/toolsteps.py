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


def count_problems(cells, files):
    problems = []
    for c in cells:
        if c.get("t") != "md":
            continue
        for tool, state in steps_in(c.get("s")):
            if tool != "logsearch":
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
