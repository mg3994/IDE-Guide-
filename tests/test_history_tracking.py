import json
import os
import shutil
import tempfile
import pytest

from scripts.generate_daily_content import generate_daily_batch, load_history


@pytest.fixture
def temp_environment():
    tmp_dir = tempfile.mkdtemp()
    db_file = os.path.join(tmp_dir, "ide_database.json")
    history_file = os.path.join(tmp_dir, "history.json")
    content_dir = os.path.join(tmp_dir, "content")

    shutil.copy("data/ide_database.json", db_file)

    yield {
        "db_file": db_file,
        "history_file": history_file,
        "content_dir": content_dir
    }

    shutil.rmtree(tmp_dir)


def test_history_tracking_prevents_immediate_duplicates(temp_environment):
    env = temp_environment

    # Day 1: Run batch
    day1 = generate_daily_batch(
        date_str="2025-06-01",
        db_path=env["db_file"],
        history_path=env["history_file"],
        content_dir=env["content_dir"]
    )
    day1_ids = {pkg["ide_id"] for pkg in day1["packages"]}
    assert len(day1_ids) == 3

    # Day 2: Run batch
    day2 = generate_daily_batch(
        date_str="2025-06-02",
        db_path=env["db_file"],
        history_path=env["history_file"],
        content_dir=env["content_dir"]
    )
    day2_ids = {pkg["ide_id"] for pkg in day2["packages"]}
    assert len(day2_ids) == 3

    # Day 2 should NOT repeat Day 1's IDEs
    overlap = day1_ids.intersection(day2_ids)
    assert len(overlap) == 0, f"Unexpected repeat IDEs across consecutive days: {overlap}"

    # Day 3: Run batch
    day3 = generate_daily_batch(
        date_str="2025-06-03",
        db_path=env["db_file"],
        history_path=env["history_file"],
        content_dir=env["content_dir"]
    )
    day3_ids = {pkg["ide_id"] for pkg in day3["packages"]}
    assert len(day3_ids) == 3

    # Total 9 distinct IDEs covered over 3 days (out of 10 in database)
    all_covered = day1_ids.union(day2_ids).union(day3_ids)
    assert len(all_covered) == 9

    # Verify history file was written correctly
    history = load_history(env["history_file"])
    assert len(history["daily_logs"]) == 3
    assert len(history["covered_ide_ids"]) == 9
