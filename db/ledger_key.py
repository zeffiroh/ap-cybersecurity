#!/usr/bin/env python3
import secrets
import sys
from urllib.parse import quote

import psycopg

from sql import url

SITE = "https://zeffiroh.github.io/ap-cybersecurity/"


def main():
    note = sys.argv[1] if len(sys.argv) > 1 else ""
    key = sys.argv[2] if len(sys.argv) > 2 else secrets.token_urlsafe(24)
    with psycopg.connect(url()) as db:
        db.execute("insert into ledger_keys (hash, note) "
                   "values (encode(sha256(convert_to(%s, 'UTF8')), 'hex'), %s)", (key, note))
    print(f"{SITE}ledger/#{quote(key, safe='')}")


if __name__ == "__main__":
    main()
