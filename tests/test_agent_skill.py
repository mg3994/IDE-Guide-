import unittest
import os
import shutil
import json
from scripts.ide_guide_agent_skill import generate_custom_package
from scripts.amp_validator import validate_amp_html

class TestAgentSkill(unittest.TestCase):

    def setUp(self):
        self.test_dir = "content/test_skill_tmp"

    def tearDown(self):
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    def test_generate_custom_package(self):
        post_path, video_path = generate_custom_package(
            ide_name="Lapce Code Editor",
            category="Lightning Fast Native Editor",
            pricing="Free / Open Source",
            is_free=True,
            output_dir=self.test_dir
        )

        self.assertTrue(os.path.exists(post_path))
        self.assertTrue(os.path.exists(video_path))

        with open(post_path, "r", encoding="utf-8") as f:
            html = f.read()
        is_valid, errors = validate_amp_html(html)
        self.assertTrue(is_valid, f"Custom skill AMP HTML failed validation: {errors}")

        with open(video_path, "r", encoding="utf-8") as f:
            video_spec = json.load(f)
        self.assertEqual(video_spec["ide_name"], "Lapce Code Editor")
        self.assertEqual(video_spec["channel"], "@IDEguide")

if __name__ == "__main__":
    unittest.main()
