import unittest
import os
import json
from scripts.generate_daily_content import (
    generate_amp_blog_post,
    generate_google_flow_video_spec,
    IDE_DATABASE,
    DISCLAIMER_TEXT
)
from scripts.amp_validator import validate_amp_html

class TestContentGeneration(unittest.TestCase):

    def test_database_structure(self):
        self.assertGreaterEqual(len(IDE_DATABASE), 3)
        for ide in IDE_DATABASE:
            self.assertIn("id", ide)
            self.assertIn("name", ide)
            self.assertIn("category", ide)
            self.assertIn("pricing", ide)
            self.assertIn("is_free", ide)
            self.assertIn("pros", ide)
            self.assertIn("cons", ide)

    def test_amp_blog_post_generation(self):
        sample_ide = IDE_DATABASE[0]
        html_output = generate_amp_blog_post(sample_ide)
        self.assertIn(sample_ide["name"], html_output)
        self.assertIn(DISCLAIMER_TEXT, html_output)

        is_valid, errors = validate_amp_html(html_output)
        self.assertTrue(is_valid, f"Generated AMP HTML is invalid: {errors}")

    def test_google_flow_video_spec(self):
        sample_ide = IDE_DATABASE[0]
        video_spec = generate_google_flow_video_spec(sample_ide)
        self.assertEqual(video_spec["channel"], "@IDEguide")
        self.assertEqual(video_spec["duration_seconds"], 60)
        self.assertIn("scenes", video_spec)
        self.assertGreaterEqual(len(video_spec["scenes"]), 5)

        for scene in video_spec["scenes"]:
            self.assertIn("google_flow_prompt", scene)
            self.assertIn("voiceover_script", scene)
            self.assertIn("screen_action", scene)

if __name__ == "__main__":
    unittest.main()
