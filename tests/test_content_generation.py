#!/usr/bin/env python3
"""
Unit tests for IDE Guide Content Generation System
"""

import os
import sys
import json
import shutil
import unittest

# Ensure scripts directory is in python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../scripts")))

from generate_daily_content import (
    generate_amp_html,
    generate_google_flow_spec,
    generate_google_flow_markdown_spec,
    run_daily_generation,
    DISCLAIMER_TEXT,
    IDE_DATABASE
)
from ide_guide_agent_skill import create_agentic_content


class TestContentGeneration(unittest.TestCase):

    def setUp(self):
        self.test_dir = "tests/test_output"
        os.makedirs(self.test_dir, exist_ok=True)
        self.sample_ide = {
            "id": "test_editor",
            "name": "Test Editor AI",
            "tagline": "Experimental testing editor",
            "developer": "Test Org",
            "pricing_type": "Freemium",
            "pricing_details": "Free tier available; $10/mo pro plan.",
            "pros": ["Ultra fast loading", "Built-in debugger"],
            "cons": ["High memory consumption"],
            "target_audience": "Software engineers and QA testers.",
            "hero_image": "https://images.unsplash.com/photo-1555066931-4365d14bab8c?w=1200",
            "category": "Testing IDE"
        }

    def tearDown(self):
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    def test_amp_html_compliance(self):
        html = generate_amp_html(self.sample_ide)

        # Check required AMP tags
        self.assertIn("<html ⚡ lang=\"en\">", html)
        self.assertIn("https://cdn.ampproject.org/v0.js", html)
        self.assertIn("<style amp-boilerplate>", html)
        self.assertIn("<amp-img", html)
        self.assertIn("application/ld+json", html)

        # Check non-sponsorship disclaimer presence
        self.assertIn(DISCLAIMER_TEXT, html)

        # Check IDE info rendered
        self.assertIn("Test Editor AI", html)
        self.assertIn("Ultra fast loading", html)
        self.assertIn("High memory consumption", html)

    def test_google_flow_spec_structure(self):
        spec = generate_google_flow_spec(self.sample_ide)

        self.assertEqual(spec["ide_name"], "Test Editor AI")
        self.assertEqual(spec["disclaimer"], DISCLAIMER_TEXT)
        self.assertIn("shorts_9_16", spec["formats"])
        self.assertIn("long_form_16_9", spec["formats"])

        # Check Shorts scenes
        shorts_scenes = spec["formats"]["shorts_9_16"]["scenes"]
        self.assertTrue(len(shorts_scenes) >= 4)
        for scene in shorts_scenes:
            self.assertIn("visual_prompt", scene)
            self.assertIn("voiceover", scene)
            self.assertIn("text_overlay", scene)

    def test_google_flow_markdown_conversion(self):
        spec = generate_google_flow_spec(self.sample_ide)
        md = generate_google_flow_markdown_spec(spec)

        self.assertIn("# Google Flow Video Generation Spec: Test Editor AI", md)
        self.assertIn("## Non-Sponsorship Disclaimer", md)
        self.assertIn(DISCLAIMER_TEXT, md)
        self.assertIn("YouTube Shorts", md)

    def test_daily_generation_run(self):
        output_dir = os.path.join(self.test_dir, "daily")
        generated_files = run_daily_generation(output_base_dir=output_dir, count=2)

        self.assertEqual(len(generated_files), 6) # 2 IDEs * (AMP + JSON + MD)
        for file_path in generated_files:
            self.assertTrue(os.path.exists(file_path))

        history_path = os.path.join(output_dir, "history.json")
        self.assertTrue(os.path.exists(history_path))
        with open(history_path, "r", encoding="utf-8") as f:
            history = json.load(f)
            self.assertEqual(len(history), 2)

    def test_agentic_skill_creation(self):
        custom_dir = os.path.join(self.test_dir, "custom")
        files = create_agentic_content(self.sample_ide, output_dir=custom_dir)

        self.assertEqual(len(files), 3)
        for f in files:
            self.assertTrue(os.path.exists(f))


if __name__ == "__main__":
    unittest.main()
