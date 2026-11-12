import json
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from builder import levels, toolsteps as T

STATE = {"q": "action=failure | stats count by src_ip", "n": 2, "files": ["auth.log"], "blank": ["q"]}


def cell(state=STATE):
    return {"t": "md", "s": "Find the brute force.\n\n" + T.fence("siem", state)}


class SiemSteps(unittest.TestCase):
    def test_guided_and_solo_hide_the_query(self):
        for level in ("guided", "solo"):
            out = levels.variant([cell()], level)[0]["s"]
            (tool, state), = T.steps_in(out)
            self.assertEqual(tool, "siem")
            self.assertEqual(state["q"], "")
            self.assertEqual(state["a"], {"q": STATE["q"]})
            self.assertEqual(state["n"], 2)

    def test_worked_example_keeps_the_query(self):
        (tool, state), = T.steps_in(levels.variant([cell()], "worked")[0]["s"])
        self.assertEqual(state["q"], STATE["q"])

    def test_files_used_keeps_searched_logs(self):
        self.assertEqual(T.files_used(STATE), {"auth.log"})
        self.assertEqual(T.files_used({"file": "a.log", "q": "x"}), {"a.log"})
        self.assertEqual(T.files_used({"q": "x"}), set())

    def test_missing_log_is_reported(self):
        self.assertEqual(T.count_problems([cell()], {"auth.log": "x"}), [])
        problems = T.count_problems([cell()], {"access.log": "x"})
        self.assertEqual(len(problems), 1)
        self.assertIn("auth.log", problems[0])

    def test_printable_guide_names_the_tool(self):
        self.assertIn("**Use SIEM search.** Search: `action=failure", T.printable(cell()["s"]))
        blank = dict(STATE, q="")
        self.assertIn("**Use SIEM search.**", T.printable(cell(blank)["s"]))
        self.assertNotIn("Search:", T.printable(cell(blank)["s"]))

    def test_logsearch_still_checked(self):
        md = {"t": "md", "s": T.fence("logsearch", {"file": "a.log", "q": "fail", "n": 1})}
        self.assertEqual(T.count_problems([md], {"a.log": "fail\nok\n"}), [])
        self.assertEqual(len(T.count_problems([md], {"a.log": "fail\nfail\n"})), 1)

    def test_fence_round_trip(self):
        (tool, state), = T.steps_in(T.fence("siem", STATE))
        self.assertEqual((tool, state), ("siem", json.loads(json.dumps(STATE))))


if __name__ == "__main__":
    unittest.main()
