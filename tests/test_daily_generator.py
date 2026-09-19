import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import json
import shutil
import tempfile
import datetime
from scripts.generate_daily_content import main, load_history, save_history, CURATED_IDES, DISCLAIMER_TEXT

def test_daily_generation_runs_successfully(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    # Run main generator
    main()

    date_str = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d")
    daily_dir = os.path.join("content", date_str)
    assert os.path.exists(daily_dir)

    # Verify 3 item packages generated
    items = [d for d in os.listdir(daily_dir) if os.path.isdir(os.path.join(daily_dir, d))]
    assert len(items) == 3

    for item in items:
        item_path = os.path.join(daily_dir, item)
        amp_file = os.path.join(item_path, "amp_post.html")
        json_file = os.path.join(item_path, "google_flow_spec.json")
        md_file = os.path.join(item_path, "google_flow_spec.md")

        assert os.path.isfile(amp_file)
        assert os.path.isfile(json_file)
        assert os.path.isfile(md_file)

        with open(amp_file, "r", encoding="utf-8") as f:
            content = f.read()
            assert DISCLAIMER_TEXT in content

        with open(json_file, "r", encoding="utf-8") as f:
            data = json.load(f)
            assert data["disclaimer"] == DISCLAIMER_TEXT
            assert "@IDEguide" in data["youtube_channel"]

    # Check history file
    history_file = os.path.join("content", "history.json")
    assert os.path.isfile(history_file)
    history_data = load_history(history_file)
    assert len(history_data["covered_ides"]) == 3
