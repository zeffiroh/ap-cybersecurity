import hashlib
import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from builder import levels, seminars as S

STEP = """## 2. Find the facts

Look in the log.

> Hint: the answer is in mail.log.

?> How many people? :: 3
"""
TOOL_STEP = """## 3. Use a program

```tool report
{"tpl": "triage", "text": "model answer", "n": 6, "blank": ["text"]}
```
"""


def sha(text):
    return "sha256:" + hashlib.sha256(S.norm(text).encode("utf-8")).hexdigest()


class PracticeLevel(unittest.TestCase):
    def setUp(self):
        scratch = Path(__file__).resolve().parents[1] / ".cache" / "tests"
        scratch.mkdir(parents=True, exist_ok=True)
        self.tmp = Path(tempfile.mkdtemp(dir=scratch))
        self.sem = self.tmp / "s99-test"
        (self.sem / "files").mkdir(parents=True)
        (self.sem / "files" / "mail.log").write_text("first evidence\n", encoding="utf-8")
        (self.sem / "seminar.json").write_text(json.dumps({"title": "Test", "summary": "Walkthrough summary", "seminar_id": 99}), encoding="utf-8")
        (self.sem / "02-find-the-facts.md").write_text(STEP, encoding="utf-8")
        (self.sem / "02-find-the-facts.sh").write_text("grep x mail.log", encoding="utf-8")
        (self.sem / "03-use-a-program.md").write_text(TOOL_STEP, encoding="utf-8")
        self.info = S.about(self.sem)

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def practice(self, data=None):
        (self.sem / "practice").mkdir(exist_ok=True)
        if data is not None:
            (self.sem / "practice" / "practice.json").write_text(json.dumps(data), encoding="utf-8")

    def md(self, cells):
        return "\n".join(c["s"] for c in cells if c["t"] == "md")

    def test_hints_go_without_any_practice_folder(self):
        cells, files, notes = S.practice_cells(self.sem, self.info)
        self.assertNotIn("> Hint:", self.md(cells))
        self.assertIn(sha("3"), self.md(cells))
        self.assertEqual(files, [])
        self.assertEqual(notes, [])

    def test_harder_questions_replace_the_walkthrough_ones(self):
        self.practice({"steps": {"02": {"ask": [["How many minutes?", "43"]], "hint": "Count from the ticket."}}})
        text = self.md(S.practice_cells(self.sem, self.info)[0])
        self.assertNotIn(sha("3"), text)
        self.assertIn("?> How many minutes? :: " + sha("43"), text)
        self.assertIn("> Hint: Count from the ticket.", text)
        self.assertNotIn("the answer is in mail.log", text)

    def test_second_evidence_needs_every_question_step_rewritten(self):
        self.practice({})
        (self.sem / "practice" / "files").mkdir()
        (self.sem / "practice" / "files" / "mail.log").write_text("second evidence\n", encoding="utf-8")
        cells, files, notes = S.practice_cells(self.sem, self.info)
        self.assertEqual(files, [])
        self.assertTrue(any("step 02" in n for n in notes))
        self.assertTrue(any("step 03" in n for n in notes))

    def test_complete_second_evidence_is_used(self):
        self.practice({"intro": "A new case."})
        (self.sem / "practice" / "files").mkdir()
        (self.sem / "practice" / "files" / "mail.log").write_text("second evidence\n", encoding="utf-8")
        (self.sem / "practice" / "02-find-the-facts.md").write_text("## 2. Find the facts\n\n?> How many people? :: 5\n", encoding="utf-8")
        (self.sem / "practice" / "03-use-a-program.md").write_text("## 3. Use a program\n\nNew model.\n", encoding="utf-8")
        cells, files, notes = S.practice_cells(self.sem, self.info)
        self.assertEqual(notes, [])
        self.assertEqual([p.name for p in files], ["mail.log"])
        text = self.md(cells)
        self.assertIn("A new case.", text)
        self.assertIn(sha("5"), text)
        self.assertNotIn("model answer", text)
        self.assertFalse([c for c in cells if c["t"] == "sh"])

    def test_publish_points_practice_at_its_own_folder(self):
        old = levels.GUIDES
        levels.GUIDES = self.tmp / "guides"
        try:
            man = {"id": "sem-s99-test", "title": "Test", "files": ["case/mail.log"], "replay": True, "handin": "old",
                   "template": [{"t": "md", "s": "# Test"}]}
            practice = {"template": [{"t": "md", "s": "# Test (Practice)"}], "files": ["case/mail.log"], "caseDir": "sem-s99-test--guided", "handin": "new"}
            levels.publish(man, practice, cases_dir=self.tmp / "cases")
            guided = json.loads((self.tmp / "cases" / "sem-s99-test--guided" / "manifest.json").read_text(encoding="utf-8"))
            solo = json.loads((self.tmp / "cases" / "sem-s99-test--solo" / "manifest.json").read_text(encoding="utf-8"))
        finally:
            levels.GUIDES = old
        self.assertEqual(guided["caseDir"], "sem-s99-test--guided")
        self.assertEqual(guided["practice"], "evidence")
        self.assertEqual(guided["handin"], "new")
        self.assertNotIn("replay", guided)
        self.assertIn("(Practice)", guided["template"][0]["s"])
        self.assertNotIn("caseDir", solo)
        self.assertEqual(solo["handin"], "old")

    def test_every_real_seminar_builds_a_practice_level(self):
        for folder in S.folders():
            info = S.about(folder)
            if not info.get("seminar_id"):
                continue
            cells, files, notes = S.practice_cells(folder, info)
            self.assertEqual(notes, [], folder.name)
            practice_md = self.md(cells)
            walk_hints = [h.strip() for c in S.cells_of(folder, info) if c["t"] == "md" for h in S.HINT_BLOCK.findall(c["s"])]
            for hint in walk_hints:
                self.assertNotIn(hint, practice_md, folder.name)
            data = S.practice_info(folder)[0]
            for stem, rule in (data.get("steps") or {}).items():
                for pair in rule.get("ask", []):
                    self.assertEqual(len(pair), 2, f"{folder.name} step {stem}")
                    self.assertTrue(str(pair[1]).strip(), f"{folder.name} step {stem}")


if __name__ == "__main__":
    unittest.main()
