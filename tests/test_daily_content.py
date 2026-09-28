import json
import os
import pytest
from scripts.generate_daily_content import select_daily_ides, load_history, save_history, HISTORY_FILE


def test_select_daily_ides():
    history = ["cursor", "zed"]
    selected = select_daily_ides(history, count=3)
    assert len(selected) == 3
    assert "cursor" not in selected
    assert "zed" not in selected


def test_load_and_save_history(tmp_path, monkeypatch):
    test_history_path = os.path.join(tmp_path, "history.json")
    monkeypatch.setattr("scripts.generate_daily_content.HISTORY_FILE", test_history_path)

    save_history(["pycharm", "vscode"])
    loaded = load_history()
    assert loaded == ["pycharm", "vscode"]
