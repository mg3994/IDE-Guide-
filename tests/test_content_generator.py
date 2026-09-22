import os
import json
import tempfile
import unittest
from scripts.generate_daily_content import (
    generate_daily_content,
    load_history,
    select_daily_ides
)

class TestContentGenerator(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()

    def test_daily_generation_file_counts(self):
        today_date = "2026-03-30"
        created_files = generate_daily_content(output_date=today_date, base_dir=self.test_dir)

        # Expecting 3 posts + 3 video specs = 6 files total
        self.assertEqual(len(created_files), 6)

        day_dir = os.path.join(self.test_dir, today_date)
        self.assertTrue(os.path.isdir(day_dir))

        dir_files = os.listdir(day_dir)
        self.assertEqual(len(dir_files), 6)

        amp_posts = [f for f in dir_files if f.startswith("post_") and f.endswith(".html")]
        video_specs = [f for f in dir_files if f.startswith("video_spec_") and f.endswith(".md")]

        self.assertEqual(len(amp_posts), 3)
        self.assertEqual(len(video_specs), 3)

    def test_history_tracking(self):
        date_1 = "2026-03-30"
        date_2 = "2026-03-31"

        files_1 = generate_daily_content(output_date=date_1, base_dir=self.test_dir)
        history_file = os.path.join(self.test_dir, "history.json")
        self.assertTrue(os.path.exists(history_file))

        history_data = load_history(history_file)
        self.assertEqual(len(history_data["history"]), 1)
        day1_ides = history_data["history"][0]["ides"]
        self.assertEqual(len(day1_ides), 3)

        files_2 = generate_daily_content(output_date=date_2, base_dir=self.test_dir)
        history_data_2 = load_history(history_file)
        self.assertEqual(len(history_data_2["history"]), 2)
        day2_ides = history_data_2["history"][1]["ides"]

        # Ensure Day 2 didn't immediately re-select Day 1 IDEs
        for ide in day2_ides:
            self.assertNotIn(ide, day1_ides)

if __name__ == "__main__":
    unittest.main()
