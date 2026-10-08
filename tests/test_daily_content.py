import os
import json
import shutil
import pytest
from scripts.generate_daily_content import generate_daily_package, load_history
from scripts.amp_validator import validate_amp_html, MANDATORY_DISCLAIMER


@pytest.fixture
def temp_output_dir(tmp_path):
    out_dir = tmp_path / "content"
    history_file = out_dir / "history.json"
    yield str(out_dir), str(history_file)
    if out_dir.exists():
        shutil.rmtree(out_dir)


def test_generate_daily_package(temp_output_dir):
    out_dir, history_file = temp_output_dir
    target_date = "2025-05-10"

    generate_daily_package(target_date=target_date, output_root=out_dir, history_path=history_file)

    day_dir = os.path.join(out_dir, target_date)
    assert os.path.exists(day_dir)

    files = os.listdir(day_dir)
    html_files = [f for f in files if f.endswith(".html")]
    json_files = [f for f in files if f.endswith(".json")]

    assert len(html_files) == 3
    assert len(json_files) == 3

    # Check AMP validation and disclaimer on each generated blog post
    for html_file in html_files:
        html_path = os.path.join(day_dir, html_file)
        with open(html_path, "r", encoding="utf-8") as f:
            content = f.read()

        is_valid, errors = validate_amp_html(content)
        assert is_valid is True, f"AMP errors in {html_file}: {errors}"
        assert MANDATORY_DISCLAIMER in content

    # Check Google Flow specs
    for json_file in json_files:
        json_path = os.path.join(day_dir, json_file)
        with open(json_path, "r", encoding="utf-8") as f:
            spec_data = json.load(f)

        assert "disclaimer" in spec_data
        assert spec_data["disclaimer"] == MANDATORY_DISCLAIMER
        assert "timeline_scenes" in spec_data
        assert len(spec_data["timeline_scenes"]) > 0

    # Verify history tracking
    history = load_history(history_file)
    assert len(history["covered_ides"]) == 3
    assert len(history["daily_logs"]) == 1
    assert history["daily_logs"][0]["date"] == target_date


def test_daily_rotation(temp_output_dir):
    out_dir, history_file = temp_output_dir

    generate_daily_package(target_date="2025-05-10", output_root=out_dir, history_path=history_file)
    generate_daily_package(target_date="2025-05-11", output_root=out_dir, history_path=history_file)

    history = load_history(history_file)
    assert len(history["covered_ides"]) == 6
    assert len(history["daily_logs"]) == 2

    day1_ides = set(history["daily_logs"][0]["generated_ides"])
    day2_ides = set(history["daily_logs"][1]["generated_ides"])

    # Ensure no overlap between consecutive days
    assert len(day1_ides.intersection(day2_ides)) == 0
