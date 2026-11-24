import shutil
import sys
import tempfile
import unittest
import unittest.mock
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from builder import legal as L
from builder import nav as N

DONE = "# Privacy notice\n\nWe keep your email. See [the store](store.html).\n\n| What | Why |\n|---|---|\n| Email | Sign-in |\n"


class LegalPages(unittest.TestCase):
    def setUp(self):
        scratch = ROOT / ".cache" / "tests"
        scratch.mkdir(parents=True, exist_ok=True)
        self.tmp = Path(tempfile.mkdtemp(dir=scratch))
        self.src = self.tmp / "legal"
        self.src.mkdir()
        self.out = {}
        self.patches = [unittest.mock.patch.object(N, "LEGAL_SRC", self.src),
                        unittest.mock.patch.object(L, "emit", lambda p, t: self.out.__setitem__(Path(p).name, t))]
        for p in self.patches:
            p.start()

    def tearDown(self):
        for p in self.patches:
            p.stop()
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_unfinished_text_is_refused(self):
        self.assertEqual(L.problems(DONE), [])
        found = L.problems("> note for you\n\nEmail [contact email] within [7] days. [A link](x.html)")
        self.assertIn("[contact email] still needs filling in", found)
        self.assertIn("[7] still needs filling in", found)
        self.assertIn("a > note line is still in it", found)
        self.assertEqual(len(found), 3)

    def test_the_drafts_are_not_ready_yet(self):
        drafts = ROOT / "reports" / "drafts"
        if not (drafts / "privacy.md").exists():
            self.skipTest("no drafts on this computer")
        self.assertTrue(L.problems((drafts / "privacy.md").read_text(encoding="utf-8")))

    def test_a_half_done_page_stops_the_build(self):
        (self.src / "privacy.md").write_text("Email [contact email]\n", encoding="utf-8")
        with self.assertRaises(SystemExit) as e:
            L.run()
        self.assertIn("source/legal/privacy.md", str(e.exception))
        self.assertNotIn("privacy.html", self.out)

    def test_footer_waits_for_all_four_pages(self):
        page_dir = N.SITE / "unit-1"
        self.assertEqual(N.footer_html(page_dir), N.AP_NOTE)
        for k in N.LEGAL_NEEDED[:-1]:
            (self.src / f"{k}.md").write_text(DONE, encoding="utf-8")
        self.assertEqual(N.footer_html(page_dir), N.AP_NOTE)
        (self.src / "contact.md").write_text(DONE, encoding="utf-8")
        (self.src / "footer.md").write_text("© 2026 Mitali Aayat Mahnoor Sharma · Aayat-AP-Prep · Pune, India", encoding="utf-8")
        foot = N.footer_html(page_dir)
        self.assertIn('href="../privacy.html"', foot)
        self.assertIn('href="../third-party.html"', foot)
        self.assertIn("Pune, India", foot)
        self.assertTrue(foot.endswith(N.AP_NOTE))
        L.run()
        self.assertIn("<table>", self.out["privacy.html"])
        self.assertIn("Privacy · ", self.out["privacy.html"])
        self.assertIn('href="privacy.html"', self.out["terms.html"])
        self.assertIn("third-party.html", self.out)


if __name__ == "__main__":
    unittest.main()
