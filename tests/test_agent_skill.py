import os
import pytest
from scripts.ide_guide_agent_skill import (
    load_ide_database,
    generate_amp_blog_post,
    generate_google_flow_video_spec
)
from scripts.amp_validator import validate_amp_html, DISCLAIMER_TEXT

def test_load_ide_database():
    db = load_ide_database()
    assert isinstance(db, dict)
    assert "vscode" in db
    assert "cursor" in db
    assert "zed" in db

def test_generate_amp_blog_post():
    db = load_ide_database()
    ide_info = db["vscode"]
    blog_html = generate_amp_blog_post(ide_info)
    assert "Visual Studio Code" in blog_html
    assert "<amp-img" in blog_html
    is_valid, errors = validate_amp_html(blog_html)
    assert is_valid is True, f"AMP Validation errors: {errors}"

def test_generate_google_flow_video_spec():
    db = load_ide_database()
    ide_info = db["cursor"]
    spec = generate_google_flow_video_spec(ide_info)
    assert "Cursor" in spec
    assert "LONG-FORM VIDEO SPEC" in spec
    assert "YOUTUBE SHORTS SPEC" in spec
    assert "Google Flow Visual Prompt" in spec
    assert "independent technical publication" in spec.lower()
