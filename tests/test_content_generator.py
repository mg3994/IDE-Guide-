#!/usr/bin/env python3
"""
Unit tests for IDE Guide daily content generator and agentic skill CLI.
"""

import os
import sys
import json
import shutil
import tempfile
import unittest
import subprocess

# Add project root to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from scripts.generate_daily_content import DISCLAIMER_TEXT, generate_amp_html, generate_google_flow_spec, IDE_CATALOG
from scripts.ide_guide_agent_skill import build_ide_profile, generate_agent_amp_post, generate_agent_flow_spec

class TestIDEGuideContentGenerator(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.test_date = "2026-08-28"

    def tearDown(self):
        shutil.rmtree(self.temp_dir)

    def test_disclaimer_constant(self):
        expected_disclaimer = (
            "Disclaimer: IDE Guide is an independent technical publication. "
            "This content is not sponsored, endorsed, or affiliated with any software vendor "
            "or editor developer mentioned above. All reviews and assessments are based strictly "
            "on objective developer evaluation."
        )
        self.assertEqual(DISCLAIMER_TEXT, expected_disclaimer)

    def test_amp_html_structure_and_disclaimer(self):
        sample_ide = IDE_CATALOG[0]
        amp_html = generate_amp_html(sample_ide, 1, self.test_date)

        # AMP compliance checks
        self.assertIn("<html ⚡ lang=\"en\">", amp_html)
        self.assertIn("<script async src=\"https://cdn.ampproject.org/v0.js\"></script>", amp_html)
        self.assertIn("<style amp-boilerplate>", amp_html)
        self.assertIn("<style amp-custom>", amp_html)
        self.assertIn("<link rel=\"canonical\"", amp_html)
        self.assertIn("https://ideguide.blogspot.com/", amp_html)
        self.assertIn("https://www.youtube.com/@IDEguide", amp_html)
        self.assertIn(DISCLAIMER_TEXT, amp_html)

    def test_google_flow_spec_structure(self):
        sample_ide = IDE_CATALOG[0]
        spec = generate_google_flow_spec(sample_ide, 1, self.test_date)

        self.assertEqual(spec["ide_name"], sample_ide["name"])
        self.assertEqual(spec["channel"], "@IDEguide")
        self.assertEqual(spec["disclaimer"], DISCLAIMER_TEXT)
        self.assertEqual(len(spec["scenes"]), 6)

        # Verify scene prompt fields
        for scene in spec["scenes"]:
            self.assertIn("google_flow_prompt", scene)
            self.assertIn("voiceover_script", scene)
            self.assertIn("on_screen_text", scene)
            self.assertIn("audio_cue", scene)

    def test_daily_generator_cli_execution(self):
        out_dir = os.path.join(self.temp_dir, "content", self.test_date)
        history_file = os.path.join(self.temp_dir, "history.json")

        cmd = [
            sys.executable,
            "scripts/generate_daily_content.py",
            "--date", self.test_date,
            "--history-path", history_file,
            "--output-dir", out_dir
        ]

        result = subprocess.run(cmd, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, f"Script failed with output:\n{result.stderr}")

        # Check generated files
        files = os.listdir(out_dir)
        amp_files = [f for f in files if f.endswith(".amp.html")]
        spec_json_files = [f for f in files if f.endswith("_flow_spec.json")]
        spec_md_files = [f for f in files if f.endswith("_flow_spec.md")]

        self.assertEqual(len(amp_files), 3)
        self.assertEqual(len(spec_json_files), 3)
        self.assertEqual(len(spec_md_files), 3)

        # Check history was updated
        self.assertTrue(os.path.exists(history_file))
        with open(history_file, "r", encoding="utf-8") as f:
            hist_data = json.load(f)
            self.assertEqual(len(hist_data["covered_ides"]), 3)

    def test_agent_skill_cli(self):
        out_dir = os.path.join(self.temp_dir, "skill_out")
        cmd = [
            sys.executable,
            "scripts/ide_guide_agent_skill.py",
            "--ide", "Zed Editor",
            "--output-dir", out_dir
        ]

        result = subprocess.run(cmd, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, f"Skill CLI failed with error:\n{result.stderr}")

        amp_path = os.path.join(out_dir, "zed-editor-review.amp.html")
        flow_path = os.path.join(out_dir, "zed-editor-flow-spec.json")

        self.assertTrue(os.path.exists(amp_path))
        self.assertTrue(os.path.exists(flow_path))

        with open(amp_path, "r", encoding="utf-8") as f:
            content = f.read()
            self.assertIn(DISCLAIMER_TEXT, content)
            self.assertIn("<html ⚡ lang=\"en\">", content)

if __name__ == "__main__":
    unittest.main()
