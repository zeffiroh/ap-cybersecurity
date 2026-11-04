import re

KINDS = {"labs": ("labs_page", "labs_gumroad"), "video": ("video_page", "video_gumroad"),
         "tickets": ("tickets_page", "tickets_gumroad"), "seminars": ("seminars_page", "seminars_gumroad"),
         "class": ("class_page", "class_gumroad"), "bundle": ("bundle_page", "bundle_gumroad")}
KEYS = tuple(k for pair in KINDS.values() for k in pair) + ("ticket_price_inr", "ticket_price_usd", "seminar_sub_days",
                                                         "ticket_packs_inr", "ticket_packs_usd")
CLASS_FIELD = re.compile(r"class", re.I)
TICKET_FIELD = re.compile(r"ticket", re.I)
CODE_RE = re.compile(r"\bC-?(\d{1,7})\b", re.I)
COUNT_RE = re.compile(r"(\d{1,4})\s*tickets?\b", re.I)


def products(db):
    return {k: v.strip() for k, v in db.execute("select key, value from settings where key = any(%s)", (list(KEYS),)).fetchall() if v.strip()}


def kind_razorpay(prod, src):
    for kind, (page, _) in KINDS.items():
        if prod.get(page) and prod[page] in src:
            return kind
    return ""


def kind_gumroad(prod, links):
    for kind, (_, link) in KINDS.items():
        if prod.get(link) and prod[link] in links:
            return kind
    return ""


def class_id(fields):
    for k, v in fields.items():
        if CLASS_FIELD.search(str(k)):
            m = CODE_RE.search(str(v).strip())
            if m:
                return int(m.group(1))
    return None


def packs(prod, currency):
    out = {}
    for part in str(prod.get("ticket_packs_" + str(currency).lower()) or "").split(","):
        n, _, price = part.partition("=")
        try:
            out[round(float(price) * 100)] = int(n)
        except ValueError:
            continue
    return out


def ticket_count(prod, amount, currency, fields, quantity=1):
    times = max(1, int(quantity or 1))
    for k, v in fields.items():
        if TICKET_FIELD.search(str(k)) and str(v).strip().isdigit():
            return max(1, min(int(str(v).strip()), 500))
    for v in fields.values():
        m = COUNT_RE.search(str(v))
        if m:
            return max(1, min(int(m.group(1)) * times, 500))
    pack = packs(prod, currency).get(int(amount) // times)
    if pack:
        return min(pack * times, 500)
    if times > 1:
        return min(times, 500)
    price = prod.get("ticket_price_" + str(currency).lower())
    try:
        each = round(float(price) * 100)
    except (TypeError, ValueError):
        each = 0
    return max(1, min(int(amount) // each, 500)) if each > 0 else 1


def grant(db, kind, email, ref, via, paid, cid=None, count=1, prod=None):
    if kind == "bundle":
        if paid:
            db.execute("insert into unlocks (email, via, ref) select %s, %s, %s "
                       "where not exists (select 1 from unlocks where via = %s and ref = %s)", (email, via, ref, via, ref))
        else:
            db.execute("update unlocks set revoked = true where via = %s and ref = %s", (via, ref))
        kind = "labs"
    if kind in ("labs", "video"):
        if paid:
            db.execute("insert into labs_access (email, via, ref) select %s, %s, %s "
                       "where not exists (select 1 from labs_access where via = %s and ref = %s)",
                       (email, via, ref, via, ref))
        else:
            db.execute("update labs_access set revoked = true where via = %s and ref = %s", (via, ref))
    elif kind == "tickets":
        if paid:
            db.execute("insert into ticket_ledger (email, delta, reason, ref) select %s, %s, %s, %s "
                       "where not exists (select 1 from ticket_ledger where ref = %s)",
                       (email, count, via, "pay:" + ref, "pay:" + ref))
        else:
            db.execute("insert into ticket_ledger (email, delta, reason, ref) "
                       "select email, -delta, 'refund', %s from ticket_ledger where ref = %s "
                       "and not exists (select 1 from ticket_ledger where ref = %s)",
                       ("rev:" + ref, "pay:" + ref, "rev:" + ref))
    elif kind == "seminars":
        days = int((prod or {}).get("seminar_sub_days") or 365)
        if paid:
            db.execute("insert into seminar_subs (email, via, ref, until) "
                       "select %s, %s, %s, greatest(now(), coalesce((select max(until) from seminar_subs "
                       "where email = %s and not revoked), now())) + make_interval(days => %s) "
                       "where not exists (select 1 from seminar_subs where via = %s and ref = %s)",
                       (email, via, ref, email, days, via, ref))
        else:
            db.execute("update seminar_subs set revoked = true where via = %s and ref = %s", (via, ref))
    elif kind == "class" and cid:
        if paid:
            db.execute("insert into class_seats (class_id, email, paid, via, ref) "
                       "select %s, %s, true, %s, %s where exists (select 1 from live_classes where id = %s) "
                       "on conflict (class_id, email) do update set paid = true, via = excluded.via, ref = excluded.ref",
                       (cid, email, via, ref, cid))
        else:
            db.execute("update class_seats set paid = false where via = %s and ref = %s", (via, ref))
