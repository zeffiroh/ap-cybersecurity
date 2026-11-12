import argparse
import hashlib
import io
import json
import re
import sys
import tarfile
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
VENDOR = ROOT / "source" / "static" / "assets" / "vendor"
PYO = VENDOR / "pyodide-0.26.1"
PYO_CDN = "https://cdn.jsdelivr.net/pyodide/v0.26.1/full/"
UA = {"User-Agent": "aayat-vendor/1.0"}

PY_PACKAGES = ["cryptography", "pyyaml", "pandas", "numpy", "regex", "bcrypt", "pyparsing",
               "packaging", "jinja2", "typing-extensions", "sqlite3"]

FILES = {
    "codemirror-5.65.16": ("https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.16/",
                           ["mode/shell/shell.min.js", "addon/edit/matchbrackets.min.js", "addon/edit/closebrackets.min.js",
                            "addon/comment/comment.min.js", "mode/python/python.min.js"]),
    "chartjs-4.4.0": ("https://cdn.jsdelivr.net/npm/chart.js@4.4.0/", ["dist/chart.umd.min.js", "LICENSE.md"]),
    "qrcode-generator-1.4.4": ("https://cdn.jsdelivr.net/npm/qrcode-generator@1.4.4/", ["qrcode.min.js", "package.json"]),
}

NPM_TARBALLS = {
    "yara-x-1.23.0": ("https://registry.npmjs.org/@virustotal/yara-x/-/yara-x-1.23.0.tgz", None),
}

WHEELS = {
    "pysigma-1.0.0-py3-none-any.whl": "https://files.pythonhosted.org/packages/b7/d1/1da9e9cbd0b9b5e2729a1049ee0f5db6d1277e9734db960a6b2dbfad7efd/pysigma-1.0.0-py3-none-any.whl",
    "pysigma_backend_splunk-1.0.0-py3-none-any.whl": "https://files.pythonhosted.org/packages/d0/42/8bc5a034e1a8a0169064421aeba32ec484b3fa95ea8da6bfd03e8dde14ed/pysigma_backend_splunk-1.0.0-py3-none-any.whl",
}


def get(url):
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=120) as r:
        return r.read()


def deps(pkgs, name, seen):
    if name in seen:
        return
    seen.add(name)
    for d in pkgs[name]["depends"]:
        deps(pkgs, d, seen)


def pyodide(dry):
    lock_path = PYO / "pyodide-lock.json"
    lock = json.loads(lock_path.read_text(encoding="utf-8"))
    pkgs = lock["packages"]
    keep = set()
    for p in PY_PACKAGES:
        deps(pkgs, p, keep)
    for name, info in sorted(pkgs.items()):
        base = info["file_name"].rsplit("/", 1)[-1]
        if name in keep:
            dst = PYO / base
            if not dst.exists():
                print("get", base)
                if not dry:
                    data = get(PYO_CDN + base)
                    if hashlib.sha256(data).hexdigest() != info["sha256"]:
                        sys.exit("checksum mismatch: " + base)
                    dst.write_bytes(data)
            info["file_name"] = base
        else:
            info["file_name"] = PYO_CDN + base
    if not dry:
        lock_path.write_text(json.dumps(lock, separators=(",", ":")), encoding="utf-8")
    print("pyodide packages kept on the site:", len(keep))


def files(dry):
    for folder, (base, names) in FILES.items():
        for n in names:
            dst = VENDOR / folder / n
            if dst.exists():
                continue
            print("get", folder, n)
            if not dry:
                dst.parent.mkdir(parents=True, exist_ok=True)
                dst.write_bytes(get(base + n))


def yjs(dry):
    out = VENDOR / "yjs-13.6.20"
    if (out / "yjs.js").exists():
        return
    seen = {}
    queue = [("/npm/yjs@13.6.20/+esm", "yjs.js")]
    while queue:
        path, name = queue.pop()
        if path in seen:
            continue
        seen[path] = name
        print("get", path)
        if dry:
            continue
        text = get("https://cdn.jsdelivr.net" + path).decode("utf-8")

        def swap(m):
            dep = m.group(2)
            local = re.sub(r"[^A-Za-z0-9.]+", "_", dep.strip("/").replace("/+esm", "")) + ".js"
            queue.append((dep, local))
            return m.group(1) + '"./' + local + '"'
        text = re.sub(r'((?:from|import)\s*)"(/npm/[^"]+)"', swap, text)
        out.mkdir(parents=True, exist_ok=True)
        (out / name).write_text(text, encoding="utf-8")
    if not dry:
        lic = get("https://cdn.jsdelivr.net/npm/yjs@13.6.20/LICENSE") + b"\n\nlib0:\n" + get("https://cdn.jsdelivr.net/npm/lib0@0.2.98/LICENSE")
        (out / "LICENSE").write_bytes(lic)


def npm(dry):
    for folder, (url, _) in NPM_TARBALLS.items():
        out = VENDOR / folder
        if out.exists():
            continue
        print("get", url)
        if dry:
            continue
        with tarfile.open(fileobj=io.BytesIO(get(url)), mode="r:gz") as t:
            for m in t.getmembers():
                if not m.isfile():
                    continue
                rel = m.name.split("/", 1)[1]
                if not re.search(r"\.(js|mjs|wasm|d\.ts)$|LICENSE|package\.json$", rel):
                    continue
                dst = out / rel
                if ".." in Path(rel).parts:
                    continue
                dst.parent.mkdir(parents=True, exist_ok=True)
                dst.write_bytes(t.extractfile(m).read())


def wheels(dry):
    for name, url in WHEELS.items():
        dst = PYO / name
        if dst.exists():
            continue
        print("get", name)
        if not dry:
            dst.write_bytes(get(url))


ATTACK_URL = "https://raw.githubusercontent.com/mitre-attack/attack-stix-data/master/enterprise-attack/enterprise-attack.json"
ATTACK_OUT = ROOT / "source" / "static" / "assets" / "attack" / "enterprise.json"


def attack(dry):
    if ATTACK_OUT.exists():
        return
    print("get", ATTACK_URL)
    if dry:
        return
    bundle = json.loads(get(ATTACK_URL))
    objs = bundle["objects"]
    version = next((o.get("x_mitre_version") for o in objs if o.get("type") == "x-mitre-collection"), "")
    tactics, by_ref = {}, {}
    for o in objs:
        if o.get("type") == "x-mitre-tactic" and not o.get("revoked") and not o.get("x_mitre_deprecated"):
            ext = next(r["external_id"] for r in o["external_references"] if r.get("source_name") == "mitre-attack")
            tactics[o["x_mitre_shortname"]] = {"id": ext, "name": o["name"]}
            by_ref[o["id"]] = o["x_mitre_shortname"]
    matrix = next((o for o in objs if o.get("type") == "x-mitre-matrix" and not o.get("revoked")), {})
    order = [by_ref[r] for r in matrix.get("tactic_refs", []) if r in by_ref]
    order += sorted(t for t in tactics if t not in order)
    techs = []
    for o in objs:
        if o.get("type") != "attack-pattern" or o.get("revoked") or o.get("x_mitre_deprecated"):
            continue
        ext = next((r["external_id"] for r in o.get("external_references", []) if r.get("source_name") == "mitre-attack"), None)
        if not ext:
            continue
        ph = [p["phase_name"] for p in o.get("kill_chain_phases", []) if p.get("kill_chain_name") == "mitre-attack"]
        techs.append([ext, o["name"], [p for p in order if p in ph]])
    techs.sort(key=lambda t: [int(x) if x.isdigit() else x for x in re.split(r"[T.]", t[0]) if x])
    out = {"source": "MITRE ATT&CK Enterprise", "version": version, "url": "https://attack.mitre.org/",
           "terms": "MITRE ATT&CK is a registered trademark of The MITRE Corporation. Used under the ATT&CK Terms of Use: https://attack.mitre.org/resources/legal-and-branding/terms-of-use/",
           "tactics": [dict(tactics[t], short=t) for t in order if t in tactics], "techniques": techs}
    ATTACK_OUT.parent.mkdir(parents=True, exist_ok=True)
    ATTACK_OUT.write_text(json.dumps(out, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")


def main():
    ap = argparse.ArgumentParser(description="Download the libraries the site hosts itself.")
    ap.add_argument("-n", "--dry-run", action="store_true")
    a = ap.parse_args()
    pyodide(a.dry_run)
    files(a.dry_run)
    yjs(a.dry_run)
    npm(a.dry_run)
    wheels(a.dry_run)
    attack(a.dry_run)


if __name__ == "__main__":
    main()
