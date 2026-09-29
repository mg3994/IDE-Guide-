import os
import json
import pytest
from scripts.amp_validator import validate_amp_html, DISCLAIMER_TEXT
from scripts.generate_daily_content import (
    IDE_DATABASE,
    generate_amp_blog_post,
    generate_google_flow_spec,
    load_history,
    save_history,
    select_daily_ides,
)
from scripts.ide_guide_agent_skill import run_agentic_skill, create_custom_ide_entry


def test_amp_validator_success():
    sample_ide = IDE_DATABASE[0]
    amp_html = generate_amp_blog_post(sample_ide, "2026-09-29")
    is_valid, errors = validate_amp_html(amp_html)
    assert is_valid, f"Validation errors: {errors}"
    assert len(errors) == 0


def test_amp_validator_failures():
    # Missing amp attribute and missing disclaimer
    invalid_html = "<html><head><meta charset='utf-8'></head><body><img src='test.jpg'></body></html>"
    is_valid, errors = validate_amp_html(invalid_html)
    assert not is_valid
    assert any("Missing `<html ⚡>`" in e for e in errors)
    assert any("Forbidden standard `<img>`" in e for e in errors)
    assert any("Missing required non-sponsorship disclaimer" in e for e in errors)


def test_google_flow_spec_generation():
    sample_ide = IDE_DATABASE[1]  # Cursor AI
    spec = generate_google_flow_spec(sample_ide, "2026-09-29")

    assert spec["ide_name"] == sample_ide["name"]
    assert spec["disclaimer_required"] is True
    assert spec["non_sponsorship_disclaimer"] == DISCLAIMER_TEXT
    assert len(spec["google_flow_prompts"]["scenes"]) == 4

    for scene in spec["google_flow_prompts"]["scenes"]:
        assert "visual_prompt" in scene
        assert "voiceover" in scene
        assert "text_overlay" in scene
        assert "audio_sfx" in scene


test_disclaimer_phrase = "Disclaimer: IDE Guide is an independent technical publication."


def test_non_sponsorship_disclaimer_presence():
    sample_ide = IDE_DATABASE[0]
    amp_html = generate_amp_blog_post(sample_ide, "2026-09-29")
    flow_spec = generate_google_flow_spec(sample_ide, "2026-09-29")

    assert test_disclaimer_phrase in amp_html
    assert test_disclaimer_phrase in flow_spec["non_sponsorship_disclaimer"]


def test_history_tracking_and_selection(tmp_path):
    history_file = tmp_path / "history.json"
    history_data = load_history(str(history_file))
    assert history_data["reviewed_ides"] == []

    selected_1 = select_daily_ides(history_data, count=3)
    assert len(selected_1) == 3
    selected_ids_1 = [ide["id"] for ide in selected_1]

    history_data["reviewed_ides"].extend(selected_ids_1)
    save_history(str(history_file), history_data)

    reloaded_history = load_history(str(history_file))
    assert reloaded_history["reviewed_ides"] == selected_ids_1

    selected_2 = select_daily_ides(reloaded_history, count=3)
    assert len(selected_2) == 3
    selected_ids_2 = [ide["id"] for ide in selected_2]

    # No overlapping IDEs in consecutive 3-pick runs when unreviewed pool is available
    assert set(selected_ids_1).isdisjoint(set(selected_ids_2))


def test_agentic_skill_custom_generation(tmp_path):
    output_dir = str(tmp_path / "custom_out")
    result = run_agentic_skill(
        target_ide="Neovim Lua",
        output_dir=output_dir,
        is_free=True
    )

    assert os.path.exists(result["blog_path"])
    assert os.path.exists(result["flow_path"])

    with open(result["blog_path"], "r", encoding="utf-8") as f:
        html_content = f.read()

    is_valid, errors = validate_amp_html(html_content)
    assert is_valid, f"Generated custom AMP HTML failed validation: {errors}"
