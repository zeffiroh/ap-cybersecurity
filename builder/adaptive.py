"""Adaptive unit tests and CW/HW review quizzes: question banks -> the JSON the pages in tests/ fetch.

source/tests/quizbanks/unit_quizbank_U*.xml -> tests/data/units.json, tests/data/U1.json ... U5.json
    (stimulus artifacts pre-rendered to HTML by quizbank_loader, each stimulus stored once)
source/tests/hw/U<n>-<k>.json (unit n, review quiz k) -> tests/data/hw/U<n>-<k>.json, tests/data/hw/index.json
"""
import json

from . import quizbank_loader
from .paths import TESTS, TESTS_SRC
from .util import dump_json, emit

OUT = TESTS / "data"


def unit_bank(loader, uid):
    """Items for one unit, with each shared stimulus written once."""
    stimuli, stim_ids, items = {}, {}, []
    for it in loader.get_items(uid):
        key = id(it["stimulus"])  # items of one stimulus set share the dict
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
