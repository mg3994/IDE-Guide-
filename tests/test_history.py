import os
import sys
import json
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'scripts')))

from generate_daily_content import load_history, save_history

def test_load_and_save_history(tmp_path):
    history_file = tmp_path / "test_history.json"

    data = load_history(str(history_file))
    assert data["covered_keys"] == []

    data["covered_keys"].append("neovim")
    save_history(str(history_file), data)

    reloaded = load_history(str(history_file))
    assert "neovim" in reloaded["covered_keys"]
