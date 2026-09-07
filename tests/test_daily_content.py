import json
import os
import sys
import tempfile

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../scripts")))

from generate_daily_content import (
    load_history,
    save_history,
    select_daily_ides,
    generate_daily_package,
)
from ide_guide_agent_skill import DISCLAIMER_TEXT, validate_amp_html


def test_history_load_and_save():
    with tempfile.TemporaryDirectory() as tmpdir:
        history_file = os.path.join(tmpdir, "history.json")
        data = load_history(history_file)
        assert data == {"covered_ides": [], "daily_logs": {}}

        data["covered_ides"].append("Test IDE")
        save_history(history_file, data)

        loaded = load_history(history_file)
        assert loaded["covered_ides"] == ["Test IDE"]


def test_select_daily_ides_uniqueness():
    history_data = {"covered_ides": ["Visual Studio Code"], "daily_logs": {}}
    selected = select_daily_ides(history_data, count=3)
    assert len(selected) == 3
    assert "Visual Studio Code" not in selected


def test_generate_daily_package():
    with tempfile.TemporaryDirectory() as tmpdir:
        history_file = os.path.join(tmpdir, "history.json")
        date_str = "2026-09-07"

        result = generate_daily_package(date_str, history_file, force=True, base_dir=tmpdir)
        assert result["status"] == "success"
        assert len(result["files"]) == 6

        # Verify files exist and contain disclaimer
        for filepath in result["files"]:
            assert os.path.exists(filepath)
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
                assert DISCLAIMER_TEXT in content

            if filepath.endswith(".amp.html"):
                is_valid, errors = validate_amp_html(content)
                assert is_valid is True, f"AMP errors in {filepath}: {errors}"

        # Verify history file updated
        history = load_history(history_file)
        assert len(history["covered_ides"]) == 3
        assert date_str in history["daily_logs"]
