import os
import tempfile
import pytest
from scripts.ide_guide_agent_skill import build_ide_metadata, generate_amp_post, generate_flow_spec
from scripts.amp_validator import validate_amp_html

def test_build_ide_metadata():
    meta = build_ide_metadata("Fleet", "https://github.com/JetBrains/Fleet")
    assert meta["id"] == "fleet"
    assert meta["name"] == "Fleet"
    assert meta["repo_url"] == "https://github.com/JetBrains/Fleet"

def test_agent_skill_amp_validity():
    meta = build_ide_metadata("Sublime Text")
    post_html = generate_amp_post(meta, "2026-10-20")
    is_valid, errors = validate_amp_html(post_html)
    assert is_valid is True, f"Errors: {errors}"

def test_agent_skill_flow_spec():
    meta = build_ide_metadata("Nova")
    spec = generate_flow_spec(meta, "2026-10-20")
    assert spec["metadata"]["ide_name"] == "Nova"
    assert "disclaimer_overlay" in spec
    assert "Disclaimer: IDE Guide is an independent technical publication" in spec["disclaimer_overlay"]["text"]
