"""
Unit tests for agent skill tool and daily content generation logic.
"""

import os
import json
import tempfile
import pytest
from scripts.ide_guide_agent_skill import extract_ide_info, generate_amp_blog_post, generate_google_flow_video_spec
from scripts.amp_validator import validate_amp_html
from scripts.generate_daily_content import select_daily_ides, POOL_OF_IDES


def test_extract_ide_info_known():
    info = extract_ide_info("neovim")
    assert info["name"] == "Neovim"
    assert "Open Source" in info["license"]


def test_extract_ide_info_github_url():
    info = extract_ide_info("https://github.com/zed-industries/zed")
    assert info["name"] == "Zed Editor"


def test_extract_ide_info_fallback():
    info = extract_ide_info("Custom Unknown Editor")
    assert info["name"] == "Custom Unknown Editor"


def test_generate_amp_blog_post():
    info = extract_ide_info("cursor")
    html = generate_amp_blog_post(info)
    is_valid, errors = validate_amp_html(html)
    assert is_valid is True, f"Errors: {errors}"


def test_generate_google_flow_video_spec():
    info = extract_ide_info("cursor")
    spec = generate_google_flow_video_spec(info)
    assert spec["video_meta"]["channel"] == "@IDEguide"
    assert len(spec["scenes"]) == 4
    assert "disclaimer" in spec


def test_select_daily_ides():
    selected, history = select_daily_ides(count=3)
    assert len(selected) == 3
    keys = [item["key"] for item in selected]
    assert len(set(keys)) == 3
