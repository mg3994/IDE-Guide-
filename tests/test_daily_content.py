import json
import os
import pytest
from scripts.generate_daily_content import generate_daily_package, load_history, HISTORY_FILE


def test_generate_daily_package(tmp_path, monkeypatch):
    test_date = "2026-09-04"
    test_history_path = tmp_path / "history.json"
    test_outdir = str(tmp_path / "content" / test_date)

    # Initialize empty history file
    with open(test_history_path, "w", encoding="utf-8") as f:
        json.dump({"covered_ides": [], "generations": []}, f)

    monkeypatch.setattr("scripts.generate_daily_content.HISTORY_FILE", str(test_history_path))

    result = generate_daily_package(test_date, outdir=test_outdir)

    assert result["date"] == test_date
    assert len(result["ides"]) == 3
    assert len(result["files"]) == 6  # 3 AMP posts + 3 Video specs

    # Verify files created physically inside isolated tmp_path
    for fpath in result["files"]:
        assert os.path.exists(fpath)
        assert str(tmp_path) in fpath

    # Verify history updated
    with open(test_history_path, "r", encoding="utf-8") as f:
        hist_data = json.load(f)

    assert len(hist_data["covered_ides"]) == 3
    assert len(hist_data["generations"]) == 1
    assert hist_data["generations"][0]["date"] == test_date


def test_no_duplicate_ides_generated(tmp_path, monkeypatch):
    test_history_path = tmp_path / "history.json"
    with open(test_history_path, "w", encoding="utf-8") as f:
        json.dump({"covered_ides": [], "generations": []}, f)

    monkeypatch.setattr("scripts.generate_daily_content.HISTORY_FILE", str(test_history_path))

    outdir1 = str(tmp_path / "content" / "2026-09-05")
    outdir2 = str(tmp_path / "content" / "2026-09-06")

    res1 = generate_daily_package("2026-09-05", outdir=outdir1)
    res2 = generate_daily_package("2026-09-06", outdir=outdir2)

    ides_day1 = set(res1["ides"])
    ides_day2 = set(res2["ides"])

    # Day 2 should not repeat any IDE from Day 1
    assert ides_day1.isdisjoint(ides_day2)
