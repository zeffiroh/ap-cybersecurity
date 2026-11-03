#!/usr/bin/env python3
import secrets
import sys

import psycopg

from sql import url


def main():
    note = sys.argv[1] if len(sys.argv) > 1 else ""
    key = sys.argv[2] if len(sys.argv) > 2 else secrets.token_urlsafe(18)
    with psycopg.connect(url()) as db:
        db.execute("insert into teacher_keys (hash, note) "
                   "values (encode(sha256(convert_to(%s, 'UTF8')), 'hex'), %s)", (key, note))
    print(f"Teacher key ({note or 'no note'}): {key}")


if __name__ == "__main__":
    main()
