import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from studio import lecture as L


def deck(minutes, units, each=45.0):
    n = int(minutes * 60 / each)
    step = max(1, n // units)
    return [{"lines": [], "dur": each, "unit": f"U{i // step + 1}"} for i in range(n)]


class Split(unittest.TestCase):
    def test_short_lecture_stays_one_video(self):
        rows = deck(18, 3)
        self.assertEqual(L.split_parts(rows), [list(range(len(rows)))])
        self.assertEqual(L.part_name("05_x", 1, 1), "05_x")

    def test_whole_flag_keeps_one_video(self):
        rows = deck(120, 8)
        self.assertEqual(len(L.split_parts(rows, whole=True)), 1)

    def test_long_lectures_split_into_parts_of_about_15_to_25_minutes(self):
        for minutes, units in [(26, 3), (60, 6), (110, 9), (130, 12), (80, 3), (125, 2)]:
            rows = deck(minutes, units)
            parts = L.split_parts(rows)
            self.assertGreater(len(parts), 1)
            self.assertEqual([i for p in parts for i in p], list(range(len(rows))))
            for p in parts[:-1]:
                secs = sum(rows[i]["dur"] for i in p)
                self.assertLessEqual(secs, L.LONGEST + 180)
                self.assertGreaterEqual(secs, 12 * 60)

    def test_parts_are_named_in_order(self):
        self.assertEqual([L.part_name("05_x", n, 3) for n in (1, 2, 3)], ["05_x-p1", "05_x-p2", "05_x-p3"])


if __name__ == "__main__":
    unittest.main()
