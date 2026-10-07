import os
import json
import shutil
import pytest
from scripts.generate_daily_content import (
    generate_daily_content_packages,
    load_history,
    DISCLAIMER_TEXT,
    HISTORY_FILE,
)
from scripts.amp_validator import validate_amp_html

@pytest.fixture(autouse=True)
def cleanup_test_content():
    # Setup: remove content directory or history file if needed
    if os.path.exists(HISTORY_FILE):
        os.remove(HISTORY_FILE)
    yield
    # Teardown
    if os.path.exists(HISTORY_FILE):
        os.remove(HISTORY_FILE)

def test_generate_daily_content_packages():
    test_date = "2026-10-08"
    generated_files = generate_daily_content_packages(date_str=test_date)

    # 3 IDEs * 2 assets (1 blog html + 1 video json) = 6 files
    assert len(generated_files) == 6

    # Verify history file updated
    covered = load_history()
    assert len(covered) == 3

    # Check that generated blog posts are valid AMP HTML and contain disclaimer
    for filepath in generated_files:
        if filepath.endswith(".html"):
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
            is_valid, errors = validate_amp_html(content)
            assert is_valid is True, f"AMP Validation failed for {filepath}: {errors}"
            assert DISCLAIMER_TEXT in content
        elif filepath.endswith(".json"):
            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
            assert data["disclaimer"] == DISCLAIMER_TEXT
            assert "youtube_shorts_spec" in data
            assert "youtube_video_spec" in data
