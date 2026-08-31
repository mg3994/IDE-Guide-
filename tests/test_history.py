import pytest
import os
import json
from scripts.generate_daily_content import load_history, save_history

def test_history_load_save(tmp_path):
    history_file = str(tmp_path / "history.json")

    # Initial load should be empty
    assert load_history(history_file) == []

    # Save initial history
    save_history(history_file, ["vscode", "cursor"])

    # Reload history
    loaded = load_history(history_file)
    assert loaded == ["vscode", "cursor"]

    # Verify JSON structure
    with open(history_file, "r", encoding="utf-8") as f:
        data = json.load(f)
        assert data["total_covered"] == 2
        assert "updated_at" in data
