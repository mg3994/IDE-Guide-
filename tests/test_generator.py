import json
import pytest
from pathlib import Path
from scripts.generate_daily_content import (
    load_database,
    generate_amp_blog_post,
    generate_google_flow_video_spec,
    select_daily_editors,
    DISCLAIMER_TEXT,
)
from scripts.amp_validator import validate_amp_blogger_content

def test_generate_amp_blog_post():
    db = load_database()
    editor = db["editors"][0]
    date_str = "2026-11-01"

    html = generate_amp_blog_post(editor, date_str)
    assert DISCLAIMER_TEXT in html
    assert editor["name"] in html
    assert "amp-img" in html
    assert "<script" not in html
    assert "<img" not in html or "<amp-img" in html

    # Validate against validator
    is_valid, errors, _ = validate_amp_blogger_content(html)
    assert is_valid is True, f"AMP errors: {errors}"

def test_generate_google_flow_video_spec():
    db = load_database()
    editor = db["editors"][0]
    date_str = "2026-11-01"

    spec = generate_google_flow_video_spec(editor, date_str)
    assert "metadata" in spec
    assert spec["metadata"]["disclaimer"] == DISCLAIMER_TEXT
    assert "scenes" in spec
    assert len(spec["scenes"]) >= 5
    for scene in spec["scenes"]:
        assert "visual_prompt" in scene
        assert "camera_motion" in scene
        assert "lighting" in scene
        assert "narration_script" in scene
    assert "youtube_metadata" in spec
    assert DISCLAIMER_TEXT in spec["youtube_metadata"]["description"]

def test_select_daily_editors_count():
    db = load_database()
    editors = db["editors"]
    selected = select_daily_editors(editors, count=3)
    assert len(selected) == 3
    selected_ids = [e["id"] for e in selected]
    assert len(set(selected_ids)) == 3
