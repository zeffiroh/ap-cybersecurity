import re

KEYS = ("video_page", "class_page", "video_gumroad", "class_gumroad")
CLASS_FIELD = re.compile(r"class", re.I)
CODE_RE = re.compile(r"\bC-?(\d{1,7})\b", re.I)


def products(db):
    return {k: v.strip() for k, v in db.execute("select key, value from settings where key = any(%s)", (list(KEYS),)).fetchall() if v.strip()}


def class_id(fields):
    for k, v in fields.items():
        if CLASS_FIELD.search(str(k)):
            m = CODE_RE.search(str(v).strip())
            if m:
                return int(m.group(1))
    return None


def grant(db, kind, email, ref, via, paid, cid=None):
    if kind == "video":
        if paid:
            db.execute("insert into video_access (email, via, ref) select %s, %s, %s "
                       "where not exists (select 1 from video_access where via = %s and ref = %s)",
                       (email, via, ref, via, ref))
        else:
            db.execute("update video_access set revoked = true where via = %s and ref = %s", (via, ref))
    elif kind == "class" and cid:
        if paid:
            db.execute("insert into class_seats (class_id, email, paid, via, ref) "
                       "select %s, %s, true, %s, %s where exists (select 1 from live_classes where id = %s) "
                       "on conflict (class_id, email) do update set paid = true, via = excluded.via, ref = excluded.ref",
                       (cid, email, via, ref, cid))
        else:
            db.execute("update class_seats set paid = false where via = %s and ref = %s", (via, ref))
