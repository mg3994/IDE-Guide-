import os
import json
import shutil
from scripts.generate_daily_content import (
    select_daily_ides,
    generate_amp_blog_post,
    generate_google_flow_spec,
    IDE_DATABASE,
    DISCLAIMER_TEXT
)
from scripts.amp_validator import validate_amp_html

def test_generate_amp_blog_post():
    ide = IDE_DATABASE[0]
    html = generate_amp_blog_post(ide)
    is_valid, errors = validate_amp_html(html)
    assert is_valid, f"Generated blog post failed AMP validation: {errors}"
    assert ide['name'] in html
    assert DISCLAIMER_TEXT in html

def test_generate_google_flow_spec():
    ide = IDE_DATABASE[0]
    spec = generate_google_flow_spec(ide)
    assert spec["target_channel"] == "@IDEguide"
    assert len(spec["flow_visual_prompts"]) >= 4
    assert spec["disclaimer"] == DISCLAIMER_TEXT
    for prompt in spec["flow_visual_prompts"]:
        assert "visual_prompt" in prompt
        assert "voiceover_script" in prompt

def test_select_daily_ides(tmp_path):
    history_file = os.path.join(tmp_path, "history.json")

    # First day selection (3 items)
    day1 = select_daily_ides(history_file, count=3)
    assert len(day1) == 3

    # Second day selection (3 items, no overlap)
    day2 = select_daily_ides(history_file, count=3)
    assert len(day2) == 3

    day1_ids = {item["id"] for item in day1}
    day2_ids = {item["id"] for item in day2}
    assert len(day1_ids.intersection(day2_ids)) == 0
