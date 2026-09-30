import os
import json
import pytest
from scripts.generate_daily_content import select_daily_ides, load_history, save_history

def test_select_daily_ides_deduplication(tmp_path):
    history_file = tmp_path / "history.json"

    # First selection
    selected_1 = select_daily_ides(count=3, history_file=str(history_file))
    assert len(selected_1) == 3

    # Update history
    save_history(str(history_file), {"covered_ides": [item["name"] for item in selected_1]})

    # Second selection should pick 3 different IDEs
    selected_2 = select_daily_ides(count=3, history_file=str(history_file))
    assert len(selected_2) == 3

    names_1 = {item["name"] for item in selected_1}
    names_2 = {item["name"] for item in selected_2}

    assert names_1.isdisjoint(names_2)
