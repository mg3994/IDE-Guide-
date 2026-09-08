import os
import sys
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'scripts')))

from generate_daily_content import (
    DISCLAIMER,
    generate_google_flow_video_spec,
    select_daily_ides,
    CURATED_IDES
)

def test_google_flow_video_spec_structure():
    ide = CURATED_IDES[0]
    spec = generate_google_flow_video_spec(ide, "2026-09-08", index=1)

    assert spec["channel"] == "@IDEguide"
    assert spec["ide_name"] == ide["name"]
    assert spec["disclaimer"] == DISCLAIMER
    assert len(spec["google_flow_prompts"]) == 4

    for prompt in spec["google_flow_prompts"]:
        assert "scene" in prompt
        assert "prompt" in prompt
        assert "voiceover" in prompt

def test_select_daily_ides():
    history = {"covered_keys": ["vscode"], "daily_logs": []}
    selected = select_daily_ides(history, count=3)

    assert len(selected) == 3
    assert all(ide["key"] != "vscode" for ide in selected)
