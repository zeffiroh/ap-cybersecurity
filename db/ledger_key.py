#!/usr/bin/env python3
"""Make a private link to the ledger page. The database keeps only a hash of the key.

    python db/ledger_key.py "who it's for"            a random key
    python db/ledger_key.py "who it's for" mykey      a key you choose

Anyone with the link sees the ledger. To cut a link off:
    python db/sql.py "delete from ledger_keys where note = 'who it was for'"
"""
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
