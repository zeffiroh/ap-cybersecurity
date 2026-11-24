import json

from . import course as C
from . import quizbank_loader
from .materials import topic_quiz
from .paths import TESTS, TESTS_SRC
from .util import dump_json, emit

OUT = TESTS / "data"
TIER = {"1": (1.0, -1.0, 45), "2": (1.1, 0.4, 60), "3": (1.2, 1.2, 75)}


def topic_banks():
    banks = []
    for tid in C.order():
        x = C.topic(tid)["src"] / "quizbank.xml"
        if x.exists():
            banks.append(topic_quiz(x))
    names = {}
    for b in banks:
        for q in b["questions"]:
            names.setdefault(q["skill_code"], set()).add(q["skill_name"])
    names = {k: min(v, key=len) for k, v in names.items()}
    index = []
    for b in banks:
        tid, items = b["topic_id"], []
        for q in b["questions"]:
            a, bb, t = TIER.get(str(q.get("difficulty", "2")), TIER["2"])
            items.append({"id": q["id"], "stim": "", "topic_refs": tid, "skill": q["skill_code"], "weight": 1.0,
                          "sec_skill": None, "sec_weight": 0.0, "a": a, "b": bb, "c": 0.25, "est_time": t,
                          "tier": int(q.get("difficulty", 2)), "lo": q.get("lo_ref", ""), "stem": q["stem"],
                          "choices": {c["key"]: c["text"] for c in q["choices"]}, "answer": q["answer_key"],
                          "explanation": q["explanation"], "rationale": q["distractor_rationale"]})
        skills = sorted({it["skill"] for it in items})
        topic = {"id": tid, "title": b["topic_title"], "unit": b["unit"]}
        emit(OUT / "topic" / f"{tid}.json", dump_json({"topic": topic, "unit": b["unit"], "skills": {s: names[s] for s in skills},
                                                     "stimuli": {}, "items": items}, compact=True))
        index.append(dict(topic, count=len(items), skills=[{"code": s, "name": names[s]} for s in skills]))
    emit(OUT / "topic" / "index.json", dump_json({"topics": index, "skills": names}, compact=True))
    return index


def unit_bank(loader, uid):
    stimuli, stim_ids, items = {}, {}, []
    for it in loader.get_items(uid):
        key = id(it["stimulus"])
        if key not in stim_ids:
            stim_ids[key] = "S%02d" % (len(stim_ids) + 1)
            s = it["stimulus"]
            stimuli[stim_ids[key]] = {"label": s.get("label", ""), "context": s.get("context", ""),
                                      "html": s.get("artifact_html", "")}
        sv = it["skill_vector"]
        sec = sv.get("secondary")
        items.append({
            "id": it["id"], "stim": stim_ids[key], "topic_refs": it["topic_refs"],
            "skill": sv["primary"]["skill"], "weight": float(sv["primary"]["weight"]),
            "sec_skill": sec["skill"] if sec else None, "sec_weight": float(sec["weight"]) if sec else 0.0,
            "a": float(it["a_param"]), "b": float(it["b_param"]), "c": float(it["c_param"]),
            "est_time": int(float(it["est_time"])), "stem": it["stem"], "choices": it["choices"],
            "answer": it["correct_answer"], "explanation": it["explanation"], "rationale": it["distractor_rationale"],
        })
    return {"unit": loader.units[uid], "stimuli": stimuli, "items": items}


def run():
    topic_banks()
    loader = quizbank_loader.QuizLoader(str(TESTS_SRC / "quizbanks"))
    emit(OUT / "units.json", dump_json(loader.unit_list(), compact=True))
    for uid in loader.units:
        emit(OUT / f"{uid}.json", dump_json(unit_bank(loader, uid), compact=True))
    index, n_topics, n_questions = [], 0, 0
    for uid in loader.units:
        topics = []
        for path in sorted((TESTS_SRC / "hw").glob(f"{uid}-*.json"), key=lambda p: int(p.stem.split("-")[1])):
            data = json.loads(path.read_text(encoding="utf-8"))
            emit(OUT / "hw" / f"{path.stem}.json", dump_json(data, compact=True))
            topics.append({"topic_id": path.stem, "title": data["title"], "count": len(data["questions"])})
            n_topics += 1
            n_questions += len(data["questions"])
        index.append({"unit_id": uid, "title": loader.units.get(uid, {}).get("title", uid), "topics": topics})
    emit(OUT / "hw" / "index.json", dump_json({"units": index, "total_topics": n_topics, "total_questions": n_questions},
                                              compact=True))
