import contextlib
import io
import shutil
import sys
import tempfile
import unittest
import unittest.mock
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "tools"))

import set_address as A
from builder import course as C
from builder import seminars as S
from builder import static

DUMMY = "https://courses.example.test/"


class SetAddress(unittest.TestCase):
    def setUp(self):
        scratch = ROOT / ".cache" / "tests"
        scratch.mkdir(parents=True, exist_ok=True)
        self.tmp = Path(tempfile.mkdtemp(dir=scratch))
        self.real = C.SITE_URL

    def tearDown(self):
        C.SITE_URL = self.real
        shutil.rmtree(self.tmp, ignore_errors=True)

    def copy_repo(self):
        for name in ("builder", "tools", "db", "tests", ".github", "publish", "build.py"):
            src = ROOT / name
            if src.is_dir():
                shutil.copytree(src, self.tmp / name, ignore=shutil.ignore_patterns("__pycache__"))
            elif src.is_file():
                shutil.copy2(src, self.tmp / name)
        shutil.copytree(ROOT / "source" / "seminars", self.tmp / "source" / "seminars",
                        ignore=shutil.ignore_patterns("files", "net", "*.pcap", "*.png", "*.jpg", "*.mp4"))
        for rel in ("assets/config.js", "buy/index.html"):
            dest = self.tmp / "source" / "static" / rel
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(ROOT / "source" / "static" / rel, dest)

    def test_only_the_setting_writes_the_address(self):
        self.assertEqual(A.leftovers(ROOT, C.SITE_URL), [])

    def test_change_on_a_copy_leaves_no_old_address(self):
        self.copy_repo()
        old = A.current(self.tmp)
        self.assertEqual(old, self.real)
        with contextlib.redirect_stdout(io.StringIO()):
            code = A.main([DUMMY, "--no-build", "--root", str(self.tmp)])
        self.assertEqual(code, 0)
        self.assertEqual(A.current(self.tmp), DUMMY)
        self.assertEqual(A.leftovers(self.tmp, old), [])

    def test_same_address_changes_nothing(self):
        (self.tmp / "builder").mkdir()
        shutil.copy2(ROOT / "builder" / "course.py", self.tmp / "builder" / "course.py")
        before = (self.tmp / "builder" / "course.py").read_bytes()
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            code = A.main([self.real, "--root", str(self.tmp)])
        self.assertEqual(code, 0)
        self.assertIn("Nothing changed", out.getvalue())
        self.assertEqual((self.tmp / "builder" / "course.py").read_bytes(), before)

    def test_addresses_are_normalised(self):
        self.assertEqual(A.normalise("example.com"), "https://example.com/")
        self.assertEqual(A.normalise("https://Example.com/course"), "https://example.com/course/")
        with self.assertRaises(ValueError):
            A.normalise("https://")

    def test_pages_are_filled_with_the_setting(self):
        C.SITE_URL = DUMMY
        folder = S.SEMINARS / "t-a-login-bypass"
        text = "\n".join(c["s"] for c in S.cells_of(folder, S.about(folder)) if c["t"] == "md")
        self.assertIn(DUMMY + "seminars.html?id=", text)
        self.assertNotIn(C.SITE_TOKEN, text)
        self.assertNotIn(A.host_of(self.real), text)
        dest = self.tmp / "config.js"
        with unittest.mock.patch.object(static, "emit", lambda p, t: p.write_text(t, encoding="utf-8")):
            static.copy(ROOT / "source" / "static" / "assets" / "config.js", dest)
        built = dest.read_text(encoding="utf-8")
        self.assertIn(f'pageUrl: "{DUMMY}store.html"', built)
        self.assertNotIn(C.SITE_TOKEN, built)

    def test_redirect_site(self):
        site = self.tmp / "site"
        (site / "unit-1").mkdir(parents=True)
        (site / "index.html").write_text("home", encoding="utf-8")
        (site / "unit-1" / "topic.html").write_text("t", encoding="utf-8")
        made = A.redirect_site(site, self.tmp / "redirect", self.real, DUMMY)
        self.assertEqual(made, 3)
        page = (self.tmp / "redirect" / "unit-1" / "topic.html").read_text(encoding="utf-8")
        self.assertIn(f'url={DUMMY}unit-1/topic.html"', page)
        self.assertIn("location.search + location.hash", page)
        self.assertIn(f'url={DUMMY}"', (self.tmp / "redirect" / "index.html").read_text(encoding="utf-8"))
        self.assertIn(f'b = "{urlsplit(self.real).path}"', (self.tmp / "redirect" / "404.html").read_text(encoding="utf-8"))

    def test_pages_workflow_can_point_at_the_redirect(self):
        wf = self.tmp / ".github" / "workflows"
        wf.mkdir(parents=True)
        shutil.copy2(ROOT / ".github" / "workflows" / "pages.yml", wf / "pages.yml")
        self.assertTrue(A.point_pages_at(self.tmp, "redirect"))
        text = (wf / "pages.yml").read_text(encoding="utf-8")
        self.assertIn("path: redirect\n", text.replace("\r\n", "\n"))
        self.assertNotIn("path: site", text)


if __name__ == "__main__":
    unittest.main()
