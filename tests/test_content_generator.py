import json
import pytest
from pathlib import Path
from scripts.generate_daily_content import generate_daily_package, load_history

def test_daily_content_generation(tmp_path, monkeypatch):
    test_date = "2026-09-27"

    paths = generate_daily_package(test_date)
    assert len(paths) >= 9  # 3 posts * (AMP HTML + Spec JSON + Spec MD)

    # Verify history file updated
    history = load_history()
    assert len(history.get("covered_ids", [])) >= 3
    dates = [entry["date"] for entry in history.get("daily_runs", [])]
    assert test_date in dates
