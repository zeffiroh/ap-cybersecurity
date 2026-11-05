import ast
import getpass
import ipaddress
import json
import re
import shlex
import shutil
import socket
import struct
import sys
from pathlib import Path

from . import seminars as S
from . import toolsteps as T
from .paths import ROOT, STATIC_SRC

STUDIO = ROOT / ".cache" / "studio"
CASES = STATIC_SRC / "assets" / "linux" / "cases"
TEACHER_CASES = STATIC_SRC.parent / "teacher-cases"
HOME = "/root/case"
NATIVE = {"awk", "base64", "basename", "cat", "cd", "chmod", "cmp", "cp", "cut", "date", "dd", "df", "diff", "dirname", "du", "echo", "env", "expr",
          "false", "find", "fold", "grep", "egrep", "fgrep", "gunzip", "gzip", "head", "hexdump", "id", "ln", "ls", "md5sum", "mkdir", "mv", "nl", "od", "printf",
          "pwd", "readlink", "rm", "rmdir", "sed", "seq", "sha1sum", "sha256sum", "sha512sum", "sleep", "sort", "strings", "tail", "tar", "tee",
          "test", "touch", "tr", "true", "uname", "uniq", "wc", "which", "xargs", "xxd", "zcat", "[", "export", "for", "while", "if", "do", "done", "then", "fi", "else", "elif", "case", "esac", "in"}
SKIP = {"clear", "reset", "exit", "history", "logout", "tput"}
EDITORS = {"vim", "vi", "nvim", "nano", "emacs", "micro", "code"}
ATTACK = {"nmap", "masscan", "nikto", "gobuster", "ffuf", "sqlmap", "hydra", "wpscan", "msfconsole", "crackmapexec", "netexec", "dirb", "enum4linux", "responder"}
SECRET = [(re.compile(p), r) for p, r in (
    (r"-----BEGIN [A-Z ]*PRIVATE KEY-----.*?-----END [A-Z ]*PRIVATE KEY-----", "[private key removed]"),
    (r"\bAKIA[0-9A-Z]{16}\b", "AKIAEXAMPLEEXAMPLE00"),
    (r"\bgh[pousr]_[A-Za-z0-9]{20,}\b", "[token removed]"),
    (r"\bgithub_pat_[A-Za-z0-9_]{20,}\b", "[token removed]"),
    (r"\bsk-[A-Za-z0-9_-]{20,}\b", "[token removed]"),
    (r"\bxox[abprs]-[A-Za-z0-9-]{10,}\b", "[token removed]"),
    (r"\brzp_(live|test)_[A-Za-z0-9]{8,}\b", "[token removed]"),
    (r"(?i)(authorization:\s*bearer\s+)[A-Za-z0-9._~+/=-]{12,}", r"\1[token removed]"),
    (r"(?i)\b(password|passwd|pwd|secret|api[_-]?key|access[_-]?token)(\s*[=:]\s*)(['\"]?)[^\s'\"]{4,}\3", r"\1\2\3[removed]\3"),
)]
IP = re.compile(r"(?<![\d.])(\d{1,3}(?:\.\d{1,3}){3})(?![\d.])")
EMAIL = re.compile(r"\b[A-Za-z0-9._%+-]+@([A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)+)\b")
ANSI = re.compile(r"\x1b(\[[0-9;?<>=]*[ -/]*[@-~]|\][^\x07\x1b]*(\x07|\x1b\\)|[@-Z\\^_()*+][0-9A-Za-z]?)")
SAFE_DOMAIN = re.compile(r"(^|\.)(example(\.(com|org|net))?|test|invalid|localhost|lan|local|internal)$", re.I)


def session_dir(name):
    return STUDIO / name


def slug(text):
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def split_plan(cells):
    plan, cur = [], None
    for kind, text in cells:
        if kind == "md":
            m = re.search(r"(?m)^#{2,3}\s+(.+)$", text)
            if m:
                body = (text[:m.start()] + text[m.end():]).strip()
                cur = {"title": re.sub(r"^\d+[.)]\s*", "", m.group(1)).strip(), "note": body, "code": []}
                plan.append(cur)
            elif cur:
                cur["note"] = (cur["note"] + "\n\n" + text).strip()
            else:
                cur = {"title": "Getting started", "note": re.sub(r"(?m)^#\s+.*$", "", text).strip(), "code": []}
                plan.append(cur)
        elif cur:
            cur["code"].append(text)
    return plan


def find_source(source):
    case = CASES / source
    if (case / "template.json").exists():
        cells = json.loads((case / "template.json").read_text(encoding="utf-8"))
        return [(c["t"], c["s"]) for c in cells], case / "case", case / "net"
    teacher = TEACHER_CASES / f"{source.removeprefix('tc-')}.json"
    if teacher.exists():
        bundle = json.loads(teacher.read_text(encoding="utf-8"))
        return [(c["t"], c["s"]) for c in bundle["template"]], bundle["files"], None
    folder = S.SEMINARS / source
    if (folder / "seminar.json").exists():
        info = S.about(folder)
        return [(c["t"], c["s"]) for c in S.cells_of(folder, info)], folder / "files", folder / "net"
    from . import course as C
    from . import tutor as T
    for a in C.atom_order():
        if a["id"] == source and (a["src"] / "problem").is_dir():
            return [("md" if k == "markdown" else "py", s) for k, s in T.notebook_cells(a, False)], None, None
    sys.exit(f"Nothing called {source}. Use a case (phish), a seminar folder, or a lesson with a code book.")


def prepare(name, title="", source=""):
    folder = session_dir(name)
    work = folder / "case"
    plan_path = folder / "plan.json"
    fresh = not folder.exists()
    work.mkdir(parents=True, exist_ok=True)
    plan = []
    if source and fresh:
        cells, files, net = find_source(source)
        plan = split_plan(cells)
        if isinstance(files, dict):
            for rel, body in files.items():
                if rel.startswith("case/"):
                    dest = work / rel[5:]
                    dest.parent.mkdir(parents=True, exist_ok=True)
                    dest.write_text(body, encoding="utf-8", newline="\n")
        elif files and files.is_dir():
            shutil.copytree(files, work, dirs_exist_ok=True)
        if net and net.is_dir():
            shutil.copytree(net, folder / "seed-net", dirs_exist_ok=True)
        plan_path.write_text(json.dumps(plan, ensure_ascii=False, indent=1), encoding="utf-8")
    elif plan_path.exists():
        plan = json.loads(plan_path.read_text(encoding="utf-8"))
    elif fresh and (S.SEMINARS / name / "files").is_dir():
        shutil.copytree(S.SEMINARS / name / "files", work, dirs_exist_ok=True)
    return plan


def load_events(folder):
    path = folder / "events.jsonl"
    if not path.exists():
        return []
    events = []
    for line in path.read_text(encoding="utf-8").splitlines():
        try:
            events.append(json.loads(line))
        except ValueError:
            continue
    events.sort(key=lambda e: e["t"])
    out = []
    for e in events:
        if e["k"] == "undo":
            for i in range(len(out) - 1, -1, -1):
                if out[i]["k"] in ("cmd", "step", "note", "hint", "ask", "file", "tool"):
                    del out[i]
                    break
        else:
            out.append(e)
    return out


def summary(folder):
    out = []
    for e in load_events(folder):
        if e["k"] == "cmd":
            out.append({"k": "cmd", "t": e["t"], "cmd": e["cmd"], "code": e["code"], "changed": e.get("changed", [])})
        elif e["k"] in ("step", "note", "hint", "ask", "file"):
            out.append({x: e[x] for x in ("k", "t", "text", "q", "name") if x in e})
    return out


def is_public(ip):
    try:
        a = ipaddress.ip_address(ip)
    except ValueError:
        return False
    reserved = any(a in ipaddress.ip_network(n) for n in ("192.0.2.0/24", "198.51.100.0/24", "203.0.113.0/24"))
    return a.is_global and not reserved


def scope_warning(cmd):
    tools = tools_of(cmd)
    if not tools or not tools & ATTACK:
        return ""
    for token in cmd.replace("/", " ").split():
        if IP.fullmatch(token) and is_public(token):
            return f"Check this is in scope: {token} is a public address. Only scan machines you have written permission to test."
        host = token.split(":")[0]
        if re.fullmatch(r"[a-z0-9-]+(\.[a-z0-9-]+)+", host, re.I) and not IP.fullmatch(host) and not SAFE_DOMAIN.search(host) and "." in host and not re.search(r"\.(txt|xml|json|log|nmap|gnmap|lst)$", host):
            return f"Check this is in scope: {host} looks like a real site. Only scan machines you have written permission to test."
    return ""


class Scrubber:
    def __init__(self, work):
        self.literals = []
        self.safe_domains = set()
        self.report = {}
        self.ips = {}
        self.emails = {}
        posix = work.resolve().as_posix()
        m = re.match(r"^([A-Za-z]):/(.*)$", posix)
        self.paths = [(posix, HOME), (str(work.resolve()), HOME)]
        if m:
            self.paths.insert(0, (f"/mnt/{m.group(1).lower()}/{m.group(2)}", HOME))
        env = ROOT / ".env"
        if env.exists():
            for line in env.read_text(encoding="utf-8", errors="ignore").splitlines():
                if "=" in line and not line.lstrip().startswith("#"):
                    value = line.split("=", 1)[1].strip().strip("\"'")
                    if len(value) >= 6:
                        self.literals.append((value, "[secret removed]"))
        for value, name in ((getpass.getuser(), "student"), (socket.gethostname(), "lab-host"), (str(Path.home()), "/root")):
            if value and len(value) >= 3:
                self.literals.append((value, name))
        self.literals.sort(key=lambda p: -len(p[0]))

    def count(self, what, n=1):
        self.report[what] = self.report.get(what, 0) + n

    def map_ip(self, m):
        ip = m.group(1)
        if not is_public(ip):
            return ip
        if ip not in self.ips:
            n = len(self.ips)
            self.ips[ip] = f"{'203.0.113' if n < 250 else '198.51.100'}.{n % 250 + 1}"
            self.count("public IP addresses changed to reserved test ones")
        return self.ips[ip]

    def map_email(self, m):
        if SAFE_DOMAIN.search(m.group(1)) or m.group(1).lower().endswith(".example") or m.group(1).lower() in self.safe_domains:
            return m.group(0)
        if m.group(0) not in self.emails:
            self.emails[m.group(0)] = f"user{len(self.emails) + 1}@example.com"
            self.count("email addresses changed to example ones")
        return self.emails[m.group(0)]

    def __call__(self, text):
        for old, new in self.paths:
            text = text.replace(old, new)
        for pattern, repl in SECRET:
            text, n = pattern.subn(repl, text)
            if n:
                self.count("secrets removed", n)
        for old, new in self.literals:
            if old in text:
                self.count("names, paths or saved secrets removed", text.count(old))
                text = text.replace(old, new)
        text = re.sub(r"/home/[A-Za-z0-9._-]+", "/root", text)
        text = IP.sub(self.map_ip, text)
        return EMAIL.sub(self.map_email, text)

    def leaks(self, text):
        return [old for old, _ in self.literals if old in text]


def tools_of(cmd):
    first = cmd.split("\n", 1)[0] if "<<" in cmd else cmd
    try:
        lex = shlex.shlex(first, posix=True, punctuation_chars=True)
        lex.whitespace_split = True
        tokens = list(lex)
    except ValueError:
        return None
    tools, start = set(), True
    for tok in tokens:
        if tok in ("|", "||", "&&", ";", "&", "|&", ";;", "(", ")"):
            start = True
        elif start and not re.match(r"^[A-Za-z_][A-Za-z0-9_]*=", tok):
            if tok == "sudo":
                tools.add("sudo")
            tools.add(tok.rsplit("/", 1)[-1] if tok.startswith(("/", "./")) and tok.startswith("/") else tok)
            start = tok in ("do", "then", "else", "if", "while", "sudo", "time", "!")
    return tools


def outside(cmd):
    for tok in re.split(r"[\s'\"=]+", cmd):
        if tok.startswith(("/", "~")) and not tok.startswith(("/root/case", "~/case", "/dev/null", "/tmp")):
            return True
        if tok.startswith("../"):
            return True
    return False


def stdlib_only(code):
    try:
        tree = ast.parse(code)
    except SyntaxError:
        return False
    for node in ast.walk(tree):
        names = [a.name for a in node.names] if isinstance(node, ast.Import) else [node.module or ""] if isinstance(node, ast.ImportFrom) else []
        if any(n.split(".")[0] not in sys.stdlib_module_names for n in names):
            return False
    return True


def text_of(path):
    try:
        return path.read_bytes().decode("utf-8")
    except (OSError, UnicodeDecodeError):
        return None


def pcap_packets(blob):
    if blob[:4] in (b"\xd4\xc3\xb2\xa1", b"\xa1\xb2\xc3\xd4"):
        end = "<" if blob[:4] == b"\xd4\xc3\xb2\xa1" else ">"
        link = struct.unpack(end + "I", blob[20:24])[0]
        pos = 24
        while pos + 16 <= len(blob):
            sec, usec, cap, _ = struct.unpack(end + "IIII", blob[pos:pos + 16])
            yield sec + usec / 1e6, link, blob[pos + 16:pos + 16 + cap]
            pos += 16 + cap
    elif blob[:4] == b"\x0a\x0d\x0d\x0a":
        end = "<" if blob[8:12] == b"\x4d\x3c\x2b\x1a" else ">"
        pos, links = 0, []
        while pos + 12 <= len(blob):
            kind, size = struct.unpack(end + "II", blob[pos:pos + 8])
            if size < 12:
                return
            if kind == 1:
                links.append(struct.unpack(end + "H", blob[pos + 8:pos + 10])[0])
            elif kind == 6:
                iface, high, low, cap, _ = struct.unpack(end + "IIIII", blob[pos + 8:pos + 28])
                yield ((high << 32) | low) / 1e6, links[iface] if iface < len(links) else 1, blob[pos + 28:pos + 28 + cap]
            pos += size


def dns_name(data):
    labels, pos = [], 12
    while pos < len(data) and data[pos] and data[pos] < 64:
        labels.append(data[pos + 1:pos + 1 + data[pos]].decode("ascii", "replace"))
        pos += data[pos] + 1
    return ".".join(labels)


def capture_text(blob, title):
    rows, first = [], None
    for when, link, pkt in pcap_packets(blob):
        off = {1: 14, 113: 16, 276: 20, 0: 4, 101: 0}.get(link)
        if off is None or len(pkt) < off + 20:
            continue
        if link == 1 and pkt[12:14] == b"\x81\x00":
            off = 18
        ip = pkt[off:]
        if ip[0] >> 4 != 4:
            continue
        hdr, proto = (ip[0] & 15) * 4, ip[9]
        src, dst = str(ipaddress.ip_address(ip[12:16])), str(ipaddress.ip_address(ip[16:20]))
        length = len(pkt)
        first = when if first is None else first
        row = {"proto": "IP", "sp": "", "dp": "", "info": "", "method": "", "uri": "", "host": "", "ua": "", "qname": ""}
        seg = ip[hdr:]
        if proto == 6 and len(seg) >= 20:
            row["sp"], row["dp"] = struct.unpack(">HH", seg[:4])
            data, flags = seg[(seg[12] >> 4) * 4:], seg[13]
            names = [n for bit, n in ((2, "SYN"), (16, "ACK"), (1, "FIN"), (4, "RST"), (8, "PSH")) if flags & bit]
            row["proto"], row["info"] = "TCP", f"{row['sp']} > {row['dp']} [{', '.join(names)}]"
            head = data[:2000].decode("latin-1")
            m = re.match(r"(GET|POST|PUT|DELETE|HEAD|OPTIONS|PATCH) (\S+) HTTP/", head)
            if m:
                row.update(proto="HTTP", info=head.split("\r\n", 1)[0], method=m.group(1), uri=m.group(2))
                h = re.search(r"(?im)^host:\s*(.+?)\r?$", head)
                a = re.search(r"(?im)^user-agent:\s*(.+?)\r?$", head)
                row.update(host=h.group(1) if h else "", ua=a.group(1) if a else "")
            elif head.startswith("HTTP/"):
                row.update(proto="HTTP", info=head.split("\r\n", 1)[0])
            elif data[:1] == b"\x16" and data[1:2] == b"\x03":
                row.update(proto="TLSv1.3" if data[2:3] == b"\x04" else "TLS", info="Handshake")
            elif data[:3] == b"\x17\x03\x03":
                row.update(proto="TLSv1.3", info="Application Data")
        elif proto == 17 and len(seg) >= 8:
            row["sp"], row["dp"] = struct.unpack(">HH", seg[:4])
            data = seg[8:]
            row["proto"], row["info"] = "UDP", f"{row['sp']} > {row['dp']}"
            if 53 in (row["sp"], row["dp"]) and len(data) > 12:
                name = dns_name(data)
                answer = data[2] & 0x80
                row.update(proto="DNS", qname=name, info=("Standard query response " if answer else "Standard query ") + f"0x{data[0]:02x}{data[1]:02x} {name}")
        elif proto == 1:
            row.update(proto="ICMP", info="Echo")
        info = row["info"].replace("|", "/")
        rows.append(f"{when - first:.6f}|{src}|{row['sp']}|{dst}|{row['dp']}|{row['proto']}|{length}|{info}|{row['method']}|{row['uri']}|{row['host']}|{row['ua']}|{row['qname']}")
    return "\n".join([f"#aayat-capture v1 {title}"] + rows) + "\n" if rows else None


def parse_network(events, scrub):
    hosts, dns, routes, www = {}, {}, [], {}
    for e in events:
        out = scrub(e.get("out", ""))
        tools = tools_of(e["cmd"]) or set()
        if "nmap" in tools:
            ip = name = None
            for line in out.splitlines():
                m = re.match(r"Nmap scan report for (?:(\S+) \()?([\d.]+)\)?", line)
                if m:
                    name, ip = m.group(1) or "", m.group(2)
                    hosts.setdefault(ip, {"name": name, "ports": {}})
                    if name:
                        dns[name] = ip
                    continue
                p = re.match(r"(\d+)/(tcp|udp)\s+open\s+(\S+)\s*(.*)$", line)
                if p and ip:
                    hosts[ip]["ports"][(int(p.group(1)), p.group(2))] = (p.group(3), p.group(4).strip())
        if tools & {"dig", "nslookup", "host"}:
            for name, ip in re.findall(r"(?m)^([A-Za-z0-9.-]+)\.?\s+\d+\s+IN\s+A\s+([\d.]+)", out):
                dns[name.rstrip(".")] = ip
        if "curl" in tools:
            url = re.search(r"https?://([^/\s'\"]+)(/\S*)?", scrub(e["cmd"]))
            m = re.match(r"HTTP/[\d.]+ (\d+[^\n]*)\n(.*?)\n\n(.*)", out.replace("\r", ""), re.S)
            if url and m:
                host = url.group(1).split(":")[0]
                path = url.group(2) or "/"
                ctype = re.search(r"(?im)^content-type:\s*(.+)$", m.group(2))
                server = re.search(r"(?im)^server:\s*(.+)$", m.group(2))
                page = f"page{len(www) + 1}.htm"
                www[page] = m.group(3)
                ip = dns.get(host, host)
                port = "443" if url.group(0).startswith("https") else "80"
                routes.append(f"{ip},{host}|{port}|*|^{re.escape(path)}$|{m.group(1).strip()}|{ctype.group(1).strip() if ctype else 'text/html'}|{server.group(1).strip() if server else 'nginx'}|{page}")
    lines = []
    for ip, h in sorted(hosts.items()):
        for (port, proto), (service, version) in sorted(h["ports"].items()):
            lines.append("|".join([ip, h["name"], str(port), proto, service, version.replace("|", "/"), "0", ""]))
    dns_lines = [f"A {n} {ip}" for n, ip in sorted(dns.items())]
    return {"hosts.txt": "\n".join(lines) + "\n" if lines else "", "dns.txt": "\n".join(dns_lines) + "\n" if dns_lines else "",
            "routes.txt": "\n".join(routes) + "\n" if routes else "", "www": www}


def step_markdown(step, n):
    parts = [f"## {n}. {step['title']}"]
    parts += step["notes"]
    parts += [f"> Hint: {h}" for h in step["hints"]]
    parts += [f"?> {q} :: {a or 'see the recorded output'}" for q, a in step["asks"]]
    return "\n\n".join(parts)


def make_steps(events):
    steps = [{"title": "Getting started", "notes": [], "hints": [], "asks": [], "cmds": [], "t": 0}]
    for e in events:
        if e["k"] == "step":
            if not (steps[-1]["cmds"] or steps[-1]["notes"]) and len(steps) == 1:
                steps[0].update(title=e["text"], t=e["t"])
            else:
                steps.append({"title": e["text"], "notes": [], "hints": [], "asks": [], "cmds": [], "t": e["t"]})
        elif e["k"] == "note":
            steps[-1]["notes"].append(e["text"])
        elif e["k"] == "hint":
            steps[-1]["hints"].append(e["text"])
        elif e["k"] == "ask":
            steps[-1]["asks"].append((e["q"], e.get("a", "")))
        elif e["k"] in ("cmd", "tool"):
            steps[-1]["cmds"].append(e)
    return steps


def compile_cells(steps, work, snaps, scrub, review, out_dir):
    cells, replay_index, replay_files, tools_used, made = [], [], {}, set(), set()
    prefix = scrub(work.resolve().as_posix())
    group_cwd = prefix
    for n, step in enumerate(steps, 1):
        cells.append({"t": "md", "s": step_markdown(step, n)})
        group, group_out = [], []

        def flush():
            nonlocal group, group_out
            if group:
                cells.append({"t": "sh", "s": "\n".join(group), "e": "\n".join(x for x in group_out if x)})
                group, group_out = [], []

        for e in step["cmds"]:
            if e["k"] == "tool":
                flush()
                cells.append({"t": "md", "s": T.fence(e["tool"], T.map_strings(e["state"], scrub))})
                continue
            cmd, code = scrub(e["cmd"]).strip(), e["code"]
            tools = tools_of(e["cmd"])
            out = scrub(e.get("out", ""))
            if not cmd:
                continue
            if tools and tools <= SKIP:
                continue
            rel_files = e.get("files", [])
            made.update(e.get("changed", []))
            if tools and tools & EDITORS:
                flush()
                for rel in rel_files:
                    body = text_of(snaps / f"{e['seq']:05d}" / rel)
                    if body is None:
                        continue
                    body = scrub(body).rstrip("\n")
                    cells.append({"t": "sh", "s": f"cat > {shlex.quote(rel)} <<'AAYAT_EOF'\n{body}\nAAYAT_EOF", "e": ""})
                continue
            if e.get("interactive"):
                review.append(f"Left out a full-screen program, because it can't replay as text: {cmd}")
                continue
            if code and not (code == 1 and tools and tools & {"grep", "egrep", "fgrep", "diff", "cmp", "test", "["}):
                review.append(f"Left out a command that failed (exit {code}): {cmd}")
                continue
            cwd = scrub(e.get("cwd", ""))
            inside = cwd == prefix or cwd.startswith(prefix + "/")
            native = tools is not None and tools <= NATIVE and inside and not outside(cmd)
            if native:
                if cwd != group_cwd:
                    group.append(f"cd {shlex.quote(cwd)}")
                group_cwd = cwd
                group.append(cmd)
                group_out.append(out)
                continue
            py = re.fullmatch(r"python3? +([\w./-]+\.py)", cmd)
            body = text_of(work / py.group(1)) if py and inside else None
            uses_made = body is not None and any(Path(m).name in body for m in made - {py.group(1)})
            if body is not None and stdlib_only(body) and not uses_made:
                flush()
                script = scrub(body).rstrip("\n")
                cells.append({"t": "py", "s": f"import os\nos.chdir('/home/pyodide/case')\n{script}", "e": out})
                continue
            flush()
            rid = f"c{e['seq']:05d}"
            single = re.fullmatch(r"(?:sudo +)?([A-Za-z0-9_.+-]+)((?: +[^|;&<>]*)?)", cmd.split("\n", 1)[0]) if "\n" not in cmd else None
            tool, args = (single.group(1), single.group(2).strip()) if single and not re.search(r"[|;&<>]", cmd) else ("", "")
            if tool:
                tools_used.add(tool)
            replay_index.append(f"{rid}|{tool}|{code}|{args}")
            replay_files[f"replay/{rid}.out"] = out + ("\n" if out else "")
            for rel in rel_files:
                body = text_of(snaps / f"{e['seq']:05d}" / rel)
                if body is not None:
                    replay_files[f"replay/{rid}.files/{rel}"] = scrub(body)
            cells.append({"t": "sh", "s": cmd, "e": out, "r": rid, "a": cmd})
        flush()
    if replay_index:
        replay_files["replay/index.txt"] = "\n".join(replay_index) + "\n"
    return cells, replay_files, sorted(tools_used), made


def compress_cast(folder, scrub, steps, size):
    path = folder / "terminal.cast"
    if not path.exists():
        return None, []
    lines = path.read_text(encoding="utf-8").splitlines()
    if not lines:
        return None, []
    head = json.loads(lines[0])
    clock, last, chunks, marks, buf, pending = 0.0, None, [], [], "", list(steps)
    for line in lines[1:]:
        try:
            when, _, data = json.loads(line)
        except ValueError:
            continue
        if last is not None:
            clock += min(when - last, 1.5)
        last = when
        while pending and pending[0]["t"] <= when:
            marks.append({"t": round(clock, 2), "title": pending.pop(0)["title"]})
        buf += data
        cut = buf.rfind("\n")
        if cut >= 0:
            chunks.append([round(clock, 2), scrub(re.sub(r"\x1b\][02];[^\x07\x1b]*(\x07|\x1b\\)", "", buf[:cut + 1]))])
            buf = buf[cut + 1:]
    if buf:
        chunks.append([round(clock, 2), scrub(buf)])
    for s in pending:
        marks.append({"t": round(clock, 2), "title": s["title"]})
    text = ANSI.sub("", "".join(c[1] for c in chunks))
    if scrub.leaks(text):
        return None, ["The terminal replay was left out, because a private value is still in it after cleaning. The codebook is still fine."]
    return {"width": size.get("c", head.get("width", 120)), "height": size.get("r", head.get("height", 34)), "duration": round(clock, 2), "chunks": chunks, "steps": marks}, []


def chapters(events):
    out, start = [], None
    for e in events:
        if e["k"] == "video_start":
            start = e["t"]
            out.append([f"Take {e.get('take') or 'OBS'}", ["0:00 Introduction"]])
        elif e["k"] == "video_stop":
            start = None
        elif e["k"] == "step" and start is not None:
            s = int(e["t"] - start)
            stamp = f"{s // 3600}:{s % 3600 // 60:02d}:{s % 60:02d}" if s >= 3600 else f"{s // 60}:{s % 60:02d}"
            out[-1][1].append(f"{stamp} {e['text']}")
    return out


def finish(name):
    folder = session_dir(name)
    if not folder.is_dir():
        raise RuntimeError(f"No recording called {name}.")
    work, snaps = folder / "case", folder / "snapshots"
    info = json.loads((folder / "session.json").read_text(encoding="utf-8"))
    events = load_events(folder)
    scrub = Scrubber(work)
    review = []
    baseline = set(json.loads((folder / "baseline.json").read_text(encoding="utf-8"))) if (folder / "baseline.json").exists() else set()
    if (folder / "plan.json").exists():
        for rel in baseline:
            body = text_of(work / rel)
            if body:
                scrub.safe_domains |= {d.lower() for d in EMAIL.findall(body)}
    steps = make_steps(events)
    out = S.SEMINARS / name
    out.mkdir(parents=True, exist_ok=True)
    if (out / "lesson.json").exists():
        shutil.copy2(out / "lesson.json", folder / "lesson.previous.json")
    cells, replay_files, tools_used, made = compile_cells(steps, work, snaps, scrub, review, out)
    cmds = [e for e in events if e["k"] == "cmd"]
    net = parse_network(cmds, scrub)
    files, skipped = {}, []
    searched = {state.get("file") for c in cells if c["t"] == "md" for _, state in T.steps_in(c["s"])}
    for path in sorted(p for p in work.rglob("*") if p.is_file()):
        rel = path.relative_to(work).as_posix()
        if rel in made and rel not in baseline and rel not in searched:
            continue
        blob = path.read_bytes()
        if path.suffix.lower() in (".pcap", ".pcapng", ".cap"):
            converted = capture_text(blob, f"{path.name} from {info['title']}")
            if converted:
                files[rel] = scrub(converted)
                continue
        try:
            files[rel] = scrub(blob.decode("utf-8"))
        except UnicodeDecodeError:
            skipped.append(rel)
    review += T.count_problems(cells, files)
    for rel in skipped:
        review.append(f"Not added, because it isn't text: {rel}. Use ./teach media to offer it as a download, after checking it.")
    for k in ("files", "net", "replay"):
        if (out / k).is_dir() and ((out / "lesson.json").exists() or k != "files"):
            shutil.rmtree(out / k)
    for rel, body in files.items():
        dest = out / "files" / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(body, encoding="utf-8", newline="\n")
    seed = folder / "seed-net"
    if seed.is_dir():
        shutil.copytree(seed, out / "net", dirs_exist_ok=True)
    for rel, body in net.items():
        if rel == "www":
            for page, text in body.items():
                dest = out / "net" / "www" / page
                dest.parent.mkdir(parents=True, exist_ok=True)
                dest.write_text(text, encoding="utf-8", newline="\n")
        elif body:
            dest = out / "net" / rel
            dest.parent.mkdir(parents=True, exist_ok=True)
            existing = dest.read_text(encoding="utf-8") if dest.exists() else ""
            dest.write_text(existing + body, encoding="utf-8", newline="\n")
    for rel, body in replay_files.items():
        dest = out / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(body, encoding="utf-8", newline="\n")
    (out / "lesson.json").write_text(json.dumps(cells, ensure_ascii=False, indent=1) + "\n", encoding="utf-8", newline="\n")
    about_path = out / "seminar.json"
    about = json.loads(about_path.read_text(encoding="utf-8")) if about_path.exists() else {
        "title": info["title"], "summary": "", "units": [], "level": "Intermediate", "minutes": max(10, round(info.get("elapsed", 0) / 60)), "seminar_id": None, "published": False}
    about["replayTools"] = tools_used
    about_path.write_text(json.dumps(about, ensure_ascii=False, indent=1) + "\n", encoding="utf-8", newline="\n")
    sizes = [e for e in events if e["k"] == "size"]
    cast, notes = compress_cast(folder, scrub, [s for s in steps if s["t"]], sizes[-1] if sizes else {})
    review += notes
    if cast:
        size = len(json.dumps(cast))
        if size > 8_000_000:
            review.append(f"The terminal replay was left out: it is {size // 1_000_000} MB, over the 8 MB limit. A command printed too much.")
            cast = None
    if cast:
        (out / "replay.json").write_text(json.dumps(cast, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
    elif (out / "replay.json").exists():
        (out / "replay.json").unlink()
    chap = chapters(events)
    if chap:
        text = "\n\n".join(t + "\n" + "\n".join(lines) for t, lines in chap) + "\n"
        (out / "chapters.txt").write_text(text, encoding="utf-8", newline="\n")
    for what, n in sorted(scrub.report.items()):
        review.append(f"{n} {what}. Read the lab before you publish it.")
    if not about.get("summary"):
        review.append("Add a summary in seminar.json before you publish.")
    (folder / "review.txt").write_text("\n".join(review) + "\n", encoding="utf-8")
    problems = S.problems(out)
    return {"name": name, "folder": str(out.relative_to(ROOT)), "steps": len(steps), "commands": len(cmds), "notebookCells": len(cells),
            "recordedOnly": sum(1 for c in cells if c.get("r")), "files": len(files), "replay": bool(cast), "review": review, "problems": problems,
            "chapters": bool(chap), "published": bool(about.get("published")), "next": f"./teach build {name}"}
