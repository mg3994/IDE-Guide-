"""
Unit tests for agentic CLI skill script.
"""

import os
import json
import shutil
import tempfile
import argparse
from scripts.ide_guide_agent_skill import run_agent_skill
from scripts.amp_validator import validate_amp_html

def test_run_agent_skill():
    temp_dir = tempfile.mkdtemp()
    try:
        args = argparse.Namespace(
            name="Fleet IDE",
            pricing="Freemium ($12/mo)",
            developer="JetBrains",
            category="Next-gen Lightweight IDE",
            primary_use="Distributed & Polyglot Coding",
            aspect_ratio="16:9",
            output_dir=temp_dir
        )
        run_agent_skill(args)

        blog_path = os.path.join(temp_dir, "fleet-ide_blog_post.html")
        spec_path = os.path.join(temp_dir, "fleet-ide_google_flow_spec.json")

        assert os.path.exists(blog_path)
        assert os.path.exists(spec_path)

        with open(blog_path, "r", encoding="utf-8") as f:
            blog_content = f.read()
        is_valid, errors = validate_amp_html(blog_content)
        assert is_valid is True, f"AMP validation failed: {errors}"

        with open(spec_path, "r", encoding="utf-8") as f:
            spec_data = json.load(f)
        assert spec_data["ide_name"] == "Fleet IDE"
        assert spec_data["aspect_ratio"] == "16:9"
        assert len(spec_data["scenes"]) >= 4

    finally:
        shutil.rmtree(temp_dir)
