"""Tests for Google Flow Video Specification Generator module."""

from scripts.lib.google_flow_generator import generate_google_flow_spec, format_google_flow_spec_md, DISCLAIMER_TEXT


def test_generate_google_flow_spec_structure():
    sample_ide = {
        "name": "Zed",
        "tagline": "High-performance editor",
        "features": ["GPU accelerated rendering", "Multiplayer coding"],
        "pros": ["Extremely fast", "Low memory footprint"],
        "cons": ["Smaller extension library"],
        "pricing_type": "Free"
    }

    spec = generate_google_flow_spec(sample_ide)

    assert "title" in spec
    assert "Zed" in spec["title"]
    assert spec["channel"] == "@IDEguide"
    assert "visual_style" in spec
    assert len(spec["scenes"]) == 4
    assert spec["disclaimer"] == DISCLAIMER_TEXT


def test_format_google_flow_spec_md():
    sample_ide = {"name": "Neovim"}
    spec = generate_google_flow_spec(sample_ide)
    md = format_google_flow_spec_md(spec)

    assert "# Google Flow Video Generation Spec:" in md
    assert "Scene 1: Hook" in md
    assert DISCLAIMER_TEXT in md
