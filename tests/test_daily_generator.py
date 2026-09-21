"""Tests for Daily Content Generator Engine."""

import os
import json
import tempfile
import shutil
from scripts.generate_daily_content import generate_daily_content_package, load_history, save_history, select_daily_ides
from scripts.lib.amp_generator import DISCLAIMER_TEXT


def test_select_daily_ides():
    ides = select_daily_ides(count=3)
    assert len(ides) == 3
    assert all("name" in ide for ide in ides)


def test_generate_daily_content_package(tmp_path, monkeypatch):
    test_content_dir = tmp_path / "content"
    history_file = test_content_dir / "history.json"

    monkeypatch.setattr("scripts.generate_daily_content.HISTORY_FILE", str(history_file))

    target_date = "2026-10-10"
    files = generate_daily_content_package(target_date=target_date)

    # 3 IDEs -> 3 amp html + 3 json specs + 3 md specs = 9 files
    assert len(files) == 9

    # Check AMP HTML content
    amp_files = [f for f in files if f.endswith(".amp.html")]
    assert len(amp_files) == 3
    with open(amp_files[0], "r", encoding="utf-8") as f:
        amp_content = f.read()
        assert "<html ⚡" in amp_content
        assert DISCLAIMER_TEXT in amp_content

    # Check history update
    history = load_history()
    assert len(history) >= 3
