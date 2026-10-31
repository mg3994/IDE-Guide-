import json
import os
import shutil
import tempfile
import pytest

from scripts.ide_guide_agent_skill import (
    generate_content_package,
    get_default_ide_data,
    DISCLAIMER_TEXT
)
from scripts.amp_validator import validate_amp_html


def test_agent_skill_known_ide():
    with open("data/ide_database.json", "r", encoding="utf-8") as f:
        db = json.load(f)

    cursor_data = next(item for item in db if item["id"] == "cursor")
    pkg = generate_content_package(cursor_data)

    assert pkg["ide_id"] == "cursor"
    assert pkg["ide_name"] == "Cursor"
    assert DISCLAIMER_TEXT in pkg["amp_blog_post_html"]
    assert DISCLAIMER_TEXT in pkg["video_flow_spec"]["mandatory_disclaimer"]

    # Verify AMP compliance
    is_valid, errors = validate_amp_html(pkg["amp_blog_post_html"], require_disclaimer=True)
    assert is_valid is True, f"Errors: {errors}"

    # Verify Google Flow spec details
    flow = pkg["video_flow_spec"]
    assert flow["channel"] == "IDE Guide (@IDEguide)"
    assert flow["blog_url"] == "https://ideguide.blogspot.com/"
    assert "Cursor" in flow["video_title"]
    assert len(flow["scenes"]) == 6


def test_agent_skill_custom_ad_hoc_ide():
    custom_name = "NovaEditor"
    custom_data = get_default_ide_data(custom_name)
    pkg = generate_content_package(custom_data)

    assert pkg["ide_id"] == "novaeditor"
    assert pkg["ide_name"] == "NovaEditor"

    # Verify AMP compliance
    is_valid, errors = validate_amp_html(pkg["amp_blog_post_html"], require_disclaimer=True)
    assert is_valid is True, f"Errors: {errors}"

    flow = pkg["video_flow_spec"]
    assert flow["pricing_tier"] == custom_data["pricing_tier"]
    assert len(flow["scenes"]) == 6
