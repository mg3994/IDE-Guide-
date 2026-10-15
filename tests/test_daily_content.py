"""
Unit tests for daily content generation script.
"""

import os
import json
import shutil
import tempfile
from scripts.generate_daily_content import (
    generate_daily_content,
    load_history,
    save_history,
    select_daily_ides,
    IDE_DATABASE,
    MANDATORY_DISCLAIMER_PHRASE
)
from scripts.amp_validator import validate_amp_html

def test_select_daily_ides():
    history = {"covered_ids": [], "runs": []}
    selected = select_daily_ides(history, count=3)
    assert len(selected) == 3
    assert len(history["covered_ids"]) == 3
    assert set(history["covered_ids"]) == {ide["id"] for ide in selected}

def test_daily_content_generation_outputs():
    temp_dir = tempfile.mkdtemp()
    temp_history = os.path.join(temp_dir, "test_history.json")

    try:
        files = generate_daily_content(output_dir=temp_dir)
        # Should generate 6 files (3 blog posts + 3 video specs)
        assert len(files) == 6

        blog_files = [f for f in files if f.endswith(".html")]
        spec_files = [f for f in files if f.endswith(".json")]

        assert len(blog_files) == 3
        assert len(spec_files) == 3

        # Validate generated AMP HTML content
        for blog_file in blog_files:
            with open(blog_file, "r", encoding="utf-8") as f:
                content = f.read()
            is_valid, errors = validate_amp_html(content)
            assert is_valid is True, f"Errors in {blog_file}: {errors}"

        # Validate Google Flow spec content
        for spec_file in spec_files:
            with open(spec_file, "r", encoding="utf-8") as f:
                spec = json.load(f)
            assert "title" in spec
            assert spec["disclaimer"] == MANDATORY_DISCLAIMER_PHRASE
            assert len(spec["scenes"]) >= 4
            for scene in spec["scenes"]:
                assert "visual_prompt" in scene
                assert "camera_movement" in scene
                assert "voiceover_script" in scene
    finally:
        shutil.rmtree(temp_dir)
