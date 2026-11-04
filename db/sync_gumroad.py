#!/usr/bin/env python3
import json
import os
import re
import sys
import urllib.parse
import urllib.request
from datetime import date, timedelta

import psycopg
from psycopg.types.json import Jsonb

import extras
from sql import url

API = "https://api.gumroad.com/v2"
COURSE = {"cybersecurity-kickstarter", "bvztyv"}
EMAIL_FIELD = re.compile(r"e-?mail", re.I)
EARLIEST = "2020-01-01"
EMAIL_RE = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]+$")


def get(path, **query):
    token = os.environ["GUMROAD_ACCESS_TOKEN"].strip()
    query["access_token"] = token
    req = urllib.request.Request(f"{API}/{path}?{urllib.parse.urlencode(query)}",
                                 headers={"Authorization": f"Bearer {token}"})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        sys.exit(f"Gumroad said {e.code}: {e.read().decode(errors='replace')[:300]}")


def sales(after):
    query = {"after": after}
    while True:
        page = get("sales", **query)
        yield from page.get("sales") or []
        if not page.get("next_page_key"):
            return
        query["page_key"] = page["next_page_key"]


def fields(s):
    f = s.get("custom_fields") or {}
    if isinstance(f, list):
        f = {str(x.get("name", "")): x.get("value") for x in f if isinstance(x, dict)}
    return {str(k)[:100]: str(v)[:500] for k, v in f.items()} if isinstance(f, dict) else {}


def cents(v):
    try:
        return int(round(float(str(v).replace(",", "")) * 100))
    except ValueError:
        return 0


def refunded(s, amount):
    if s.get("refunded") or s.get("chargedback") or (s.get("disputed") and not s.get("dispute_won")):
        return amount
    if s.get("partially_refunded"):
        left = s.get("amount_refundable_in_currency")
        return max(0, amount - cents(left)) if left is not None else 0
    return 0


def main():
    if not os.environ.get("GUMROAD_ACCESS_TOKEN"):
        print("No GUMROAD_ACCESS_TOKEN; Gumroad sync skipped.")
        return
    with psycopg.connect(url()) as db:
        empty = db.execute("select not exists (select 1 from payments where provider = 'gumroad')").fetchone()[0]
        after = EARLIEST if empty or "--all" in sys.argv else (date.today() - timedelta(days=60)).isoformat()
        rows, unlocks, extra = [], [], []
        prod = extras.products(db)
        for s in sales(after):
            sid = "gumroad_" + str(s["id"])
            amount = int(s.get("price") or 0)
            back = refunded(s, amount)
            f = fields(s)
            given = next((v for k, v in f.items() if EMAIL_FIELD.search(k) and EMAIL_RE.match(v.strip())), "")
            email = (given or s.get("email") or s.get("purchase_email") or "").strip().lower()[:200]
            status = "refunded" if back else ("captured" if s.get("paid", True) else "failed")
            notes = dict(f, product=str(s.get("product_name") or "")[:200])
            rows.append((sid, status, amount, back, int(s.get("gumroad_fee") or 0),
                         str(s.get("currency") or "usd").upper()[:3], email,
                         str(s.get("product_name") or "")[:300], Jsonb(notes), s["created_at"]))
            links = {str(s.get("product_permalink") or ""), str(s.get("custom_permalink") or "")}
            course = links & COURSE
            kind = extras.kind_gumroad(prod, links)
            if kind and EMAIL_RE.match(email):
                extra.append((kind, email, sid, status in ("captured", "refunded") and back < amount, extras.class_id(f),
                              extras.ticket_count(prod, amount, s.get("currency") or "usd", f, s.get("quantity") or 1)))
            if course and EMAIL_RE.match(email):
                unlocks.append((email, sid, status in ("captured", "refunded") and back < amount))
        db.cursor().executemany(
            """insert into payments (id, provider, status, amount, amount_refunded, fee, tax, currency, method,
                                     email, description, notes, created_at)
               values (%s, 'gumroad', %s, %s, %s, %s, 0, %s, 'gumroad', %s, %s, %s, %s::timestamptz)
               on conflict (id) do update set
                 status = excluded.status, amount_refunded = excluded.amount_refunded, fee = excluded.fee,
                 email = excluded.email, notes = excluded.notes, synced_at = now()""",
            rows)
        for email, ref, paid in unlocks:
            if paid:
                db.execute("insert into unlocks (email, via, ref) select %s, 'gumroad', %s "
                           "where not exists (select 1 from unlocks where via = 'gumroad' and ref = %s)",
                           (email, ref, ref))
            else:
                db.execute("update unlocks set revoked = true where via = 'gumroad' and ref = %s", (ref,))
        for kind, email, ref, paid, cid, count in extra:
            extras.grant(db, kind, email, ref, "gumroad", paid, cid, count, prod)
        db.execute("insert into payments (id, status, created_at) values ('_sync', 'sync', now()) "
                   "on conflict (id) do update set synced_at = now()")
    print(f"Gumroad sync done ({len(rows)} sales, {len(unlocks)} course).")


if __name__ == "__main__":
    main()
