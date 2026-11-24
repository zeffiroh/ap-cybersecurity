#!/usr/bin/env python3
USAGE = """Encrypted backups of the database.

    python db/backup.py dump FOLDER              save an encrypted backup of the database into FOLDER
    python db/backup.py fetch                    download the newest weekly backup from GitHub into .cache/backups
    python db/backup.py check FILE               open a backup and list its tables and row counts (changes nothing)
    python db/backup.py restore FILE --to URL    put a backup into the database at URL (a Neon branch, or a test database)
    python db/backup.py restore FILE --live      put a backup into the live database (asks you to type RESTORE)

The password comes from BACKUP_PASSWORD, or BACKUP_PASSWORD in the project's .env, or it is asked for.
The database comes from DATABASE_URL, or NEON_DATABASE_URL in .env (the same as db/sql.py).
Needs:  pip install "psycopg[binary]==3.2.3" cryptography
"""
import getpass
import gzip
import json
import os
import secrets
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

import psycopg

ROOT = Path(__file__).resolve().parent.parent
MAGIC = b"AAYATDB1"
FETCHED = ROOT / ".cache" / "backups"


def env_value(key):
    if os.environ.get(key):
        return os.environ[key]
    env = ROOT / ".env"
    for line in env.read_text(encoding="utf-8").splitlines() if env.exists() else []:
        k, _, v = line.partition("=")
        if k.strip() == key:
            return v.strip().strip('"')
    return ""


def password(ask=True):
    pw = env_value("BACKUP_PASSWORD")
    if not pw and ask and sys.stdin.isatty():
        pw = getpass.getpass("Backup password: ")
    if not pw:
        sys.exit("No BACKUP_PASSWORD. Set it in .env or as a GitHub secret (gh secret set BACKUP_PASSWORD).")
    return pw


def key_of(pw, salt):
    from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
    return Scrypt(salt=salt, length=32, n=2 ** 15, r=8, p=1).derive(pw.encode("utf-8"))


def seal(data, pw):
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM
    salt, nonce = secrets.token_bytes(16), secrets.token_bytes(12)
    return MAGIC + salt + nonce + AESGCM(key_of(pw, salt)).encrypt(nonce, gzip.compress(data), MAGIC)


def unseal(blob, pw):
    from cryptography.exceptions import InvalidTag
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM
    if not blob.startswith(MAGIC):
        sys.exit("That file isn't one of our database backups.")
    salt, nonce, body = blob[8:24], blob[24:36], blob[36:]
    try:
        return gzip.decompress(AESGCM(key_of(pw, salt)).decrypt(nonce, body, MAGIC))
    except InvalidTag:
        sys.exit("Wrong password, or the file is damaged.")


def tables(db):
    names = [r[0] for r in db.execute("select tablename from pg_tables where schemaname = 'public' order by tablename")]
    links = db.execute("""select ch.relname, pa.relname from pg_constraint c
                          join pg_class ch on ch.oid = c.conrelid join pg_class pa on pa.oid = c.confrelid
                          join pg_namespace n on n.oid = c.connamespace
                          where c.contype = 'f' and n.nspname = 'public' and ch.relname <> pa.relname""").fetchall()
    needs = {t: {p for c, p in links if c == t and p in names} for t in names}
    out = []
    while needs:
        ready = sorted(t for t, deps in needs.items() if not deps - set(out))
        if not ready:
            ready = sorted(needs)
        for t in ready:
            out.append(t)
            needs.pop(t)
    return out


def columns(db, table):
    return [r[0] for r in db.execute("""select column_name from information_schema.columns
                                        where table_schema = 'public' and table_name = %s and is_generated = 'NEVER'
                                        order by ordinal_position""", (table,))]


def quoted(names):
    return ", ".join('"' + n.replace('"', '""') + '"' for n in names)


def dump(url):
    out = {"format": 1, "made": datetime.now(timezone.utc).isoformat(timespec="seconds"), "tables": []}
    with psycopg.connect(url) as db:
        db.execute("set transaction isolation level repeatable read, read only")
        for t in tables(db):
            cols = columns(db, t)
            with db.cursor() as cur:
                with cur.copy(f'copy public."{t}" ({quoted(cols)}) to stdout') as cp:
                    data = b"".join(bytes(chunk) for chunk in cp)
            out["tables"].append({"name": t, "columns": cols, "rows": data.count(b"\n"), "copy": data.decode("utf-8")})
    return json.dumps(out, ensure_ascii=False).encode("utf-8")


def load(blob, pw):
    data = json.loads(unseal(blob, pw).decode("utf-8"))
    if data.get("format") != 1:
        sys.exit("This backup was made by a newer version of this script.")
    return data


def restore(data, url, schema=ROOT / "db" / "schema.sql"):
    with psycopg.connect(url, autocommit=True) as db:
        if not {t["name"] for t in data["tables"]} <= set(tables(db)):
            db.execute(schema.read_text(encoding="utf-8"))
    with psycopg.connect(url) as db:
        have = set(tables(db))
        missing = [t["name"] for t in data["tables"] if t["name"] not in have]
        if missing:
            sys.exit("The database has no tables called " + ", ".join(missing) + ". Run python db/sql.py db/schema.sql on it first.")
        for t in data["tables"]:
            gone = set(t["columns"]) - set(columns(db, t["name"]))
            if gone:
                sys.exit(f"Table {t['name']} no longer has the column(s) {', '.join(sorted(gone))}. Restore into a database made from the old schema.")
        names = [t["name"] for t in data["tables"]]
        db.execute("truncate " + ", ".join(f'public."{n}"' for n in names) + " restart identity cascade")
        for t in data["tables"]:
            if not t["copy"]:
                continue
            with db.cursor() as cur:
                with cur.copy(f'copy public."{t["name"]}" ({quoted(t["columns"])}) from stdin') as cp:
                    cp.write(t["copy"].encode("utf-8"))
        for t in data["tables"]:
            for col in t["columns"]:
                seq = db.execute("select pg_get_serial_sequence(%s, %s)", (f'public."{t["name"]}"', col)).fetchone()[0]
                if seq:
                    db.execute(f'select setval(%s, coalesce((select max("{col}") from public."{t["name"]}"), 0) + 1, false)', (seq,))
        db.commit()
        try:
            db.execute("notify pgrst, 'reload schema'")
            db.commit()
        except psycopg.Error:
            pass


def summary(data):
    lines = [f"Backup made {data['made']}, {len(data['tables'])} tables:"]
    lines += [f"  {t['name']:<22} {t['rows']:>7} rows" for t in data["tables"]]
    return "\n".join(lines)


def cmd_dump(folder):
    from sql import url
    folder = Path(folder)
    folder.mkdir(parents=True, exist_ok=True)
    pw = password(ask=False)
    raw = dump(url())
    name = folder / f"aayat-db-{datetime.now(timezone.utc):%Y-%m-%d-%H%M}.bak"
    name.write_bytes(seal(raw, pw))
    data = json.loads(raw)
    print(f"Saved {name} ({name.stat().st_size // 1024} KB, {sum(t['rows'] for t in data['tables'])} rows in {len(data['tables'])} tables).")


def cmd_fetch():
    run = subprocess.run(["gh", "run", "list", "-w", "backup.yml", "--status", "success", "-L", "1", "--json", "databaseId,createdAt",
                          "-q", ".[0] | \"\\(.databaseId) \\(.createdAt)\""], capture_output=True, text=True, cwd=ROOT)
    if run.returncode != 0 or not run.stdout.strip():
        sys.exit("No finished backup on GitHub yet. Start one with: gh workflow run backup.yml" + (f"\n{run.stderr.strip()}" if run.stderr.strip() else ""))
    rid, when = run.stdout.split()
    dest = FETCHED / rid
    if not dest.exists():
        got = subprocess.run(["gh", "run", "download", rid, "-n", "db-backup", "-D", str(dest)], cwd=ROOT)
        if got.returncode != 0:
            sys.exit("The download failed (above).")
    files = sorted(dest.glob("*.bak"))
    print(f"Backup from {when}: " + ", ".join(str(f.relative_to(ROOT)) for f in files))
    print(f"Check it:  python db/backup.py check {files[-1].relative_to(ROOT)}" if files else "The download had no .bak file in it.")


def main(argv):
    if not argv or argv[0] not in ("dump", "fetch", "check", "restore"):
        sys.exit(USAGE)
    cmd, rest = argv[0], argv[1:]
    if cmd == "dump" and len(rest) == 1:
        return cmd_dump(rest[0])
    if cmd == "fetch" and not rest:
        return cmd_fetch()
    if cmd == "check" and len(rest) == 1:
        print(summary(load(Path(rest[0]).read_bytes(), password())))
        return
    if cmd == "restore" and len(rest) >= 2:
        data = load(Path(rest[0]).read_bytes(), password())
        if rest[1] == "--to" and len(rest) == 3:
            target = rest[2]
        elif rest[1] == "--live" and len(rest) == 2:
            from sql import url
            target = url()
            print(summary(data))
            print("\nThis replaces EVERYTHING in the live database with this backup. Payments, sign-ups and grades since then are lost")
            print("(the payment sync puts payments back within 5 minutes).")
            if input("Type RESTORE to go on: ").strip() != "RESTORE":
                sys.exit("Nothing changed.")
        else:
            sys.exit(USAGE)
        restore(data, target)
        print(f"Restored {sum(t['rows'] for t in data['tables'])} rows in {len(data['tables'])} tables from the backup made {data['made']}.")
        return
    sys.exit(USAGE)


if __name__ == "__main__":
    main(sys.argv[1:])
