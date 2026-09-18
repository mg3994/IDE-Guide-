import json
import os
import pytest
import sys

sys.path.insert(0, os.path.abspath("scripts"))

from ide_guide_agent_skill import (
    fetch_or_build_ide_data,
    generate_amp_html_blogpost,
    generate_google_flow_video_spec,
    sanitize_slug,
    DISCLAIMER_TEXT,
    KNOWN_IDES_DATABASE
)
from generate_daily_content import (
    load_history,
    save_history,
    select_daily_ides,
    generate_daily_content_package
)


def test_sanitize_slug():
    assert sanitize_slug("Zed Editor") == "zed-editor"
    assert sanitize_slug("VS Code 2026") == "vs-code-2026"


def test_known_ide_fetch():
    data = fetch_or_build_ide_data("zed")
    assert data["name"] == "Zed Editor"
    assert "Rust" in data["description"]


def test_unknown_ide_fetch():
    data = fetch_or_build_ide_data("Custom-New-IDE")
    assert data["name"] == "Custom New Ide"
    assert "key_features" in data


def test_amp_html_compliance():
    data = fetch_or_build_ide_data("cursor")
    html = generate_amp_html_blogpost(data)

    # AMP standard checks
    assert "<html ⚡ lang=\"en\">" in html or "<html amp lang=\"en\">" in html
    assert "<script async src=\"https://cdn.ampproject.org/v0.js\"></script>" in html
    assert "amp-boilerplate" in html
    assert DISCLAIMER_TEXT in html
    assert "https://ideguide.blogspot.com/" in html


def test_google_flow_spec_structure():
    data = fetch_or_build_ide_data("neovim")
    spec = generate_google_flow_video_spec(data)

    assert spec["channel"] == "IDE Guide (@IDEguide)"
    assert len(spec["prompts_and_scenes"]) == 5
    assert spec["disclaimer"] == DISCLAIMER_TEXT

    scene1 = spec["prompts_and_scenes"][0]
    assert "Neovim" in scene1["flow_prompt"]
    assert "flow_prompt" in scene1
    assert "voiceover_script" in scene1


def test_daily_generation_package(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    day_dir, summary = generate_daily_content_package("2026-09-18")

    assert os.path.exists(day_dir)
    assert len(summary) == 3

    history = load_history()
    assert len(history["covered_slugs"]) == 3
    assert "2026-09-18" in history["daily_logs"]

    # Check generated files existence
    for item in summary:
        assert os.path.exists(item["amp_html"])
        assert os.path.exists(item["video_spec_json"])
        assert os.path.exists(item["video_spec_md"])

        with open(item["amp_html"], "r", encoding="utf-8") as f:
            content = f.read()
            assert "<html ⚡" in content
            assert DISCLAIMER_TEXT in content
