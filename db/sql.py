#!/usr/bin/env python3
"""Run SQL on the Neon database from the command line (no psql needed).

    python db/sql.py db/schema.sql                       run a file
    python db/sql.py "select * from unlock_codes"        run a statement and print the rows

The connection string comes from DATABASE_URL, or NEON_DATABASE_URL in the project's .env.
Needs:  pip install "psycopg[binary]==3.2.3"
"""
import os
import sys
from pathlib import Path

import psycopg


def url():
    if os.environ.get("DATABASE_URL"):
        return os.environ["DATABASE_URL"]
    env = Path(__file__).resolve().parent.parent / ".env"
    for line in env.read_text(encoding="utf-8").splitlines() if env.exists() else []:
        key, _, value = line.partition("=")
        if key.strip() == "NEON_DATABASE_URL":
            return value.strip().strip('"')
    sys.exit("No DATABASE_URL, and no NEON_DATABASE_URL in .env")


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    arg = sys.argv[1]
    sql = Path(arg).read_text(encoding="utf-8") if arg.endswith(".sql") else arg
    with psycopg.connect(url(), autocommit=True) as db:
        cur = db.execute(sql)
        if cur.description:
            names = [d.name for d in cur.description]
            print(" | ".join(names))
            for row in cur.fetchall():
                print(" | ".join("" if v is None else str(v) for v in row))
        else:
            print("done" + (f", {cur.rowcount} row(s)" if cur.rowcount >= 0 else ""))


if __name__ == "__main__":
    main()
