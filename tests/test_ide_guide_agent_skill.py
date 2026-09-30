import json
from scripts.ide_guide_agent_skill import generate_amp_blog_post, generate_google_flow_video_spec
from scripts.amp_validator import validate_amp_html

def test_agent_skill_amp_blog_generation():
    html = generate_amp_blog_post("Test IDE")
    assert "Test IDE" in html
    is_valid, errors = validate_amp_html(html)
    assert is_valid is True, f"Errors: {errors}"

def test_agent_skill_video_spec_generation():
    spec = generate_google_flow_video_spec("Test IDE")
    assert spec["title"] == "IDE Guide: Test IDE - Quick Review & Guide"
    assert spec["channel"] == "@IDEguide"
    assert len(spec["scenes"]) == 5
    assert "Disclaimer: IDE Guide is an independent technical publication." in spec["disclaimer"]
