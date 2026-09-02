import os
import sys
import glob
import json
import pytest

# Add scripts directory to sys.path so modules can be imported directly
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'scripts')))

from generate_daily_content import (
    generate_amp_blog_post,
    generate_google_flow_video_spec,
    DISCLAIMER_TEXT,
    sanitize_slug,
    select_daily_ides,
    CURATED_IDES
)
from ide_guide_agent_skill import fetch_github_repo_info


def test_disclaimer_exact_match():
    expected_disclaimer = (
        "Disclaimer: IDE Guide is an independent technical publication. This content is not sponsored, "
        "endorsed, or affiliated with any software vendor or editor developer mentioned above. "
        "All reviews and assessments are based strictly on objective developer evaluation."
    )
    assert DISCLAIMER_TEXT == expected_disclaimer


def test_amp_blog_post_generation():
    ide_sample = {
        "name": "Test Editor",
        "category": "Test Category",
        "pricing": "Free / Open Source",
        "cost_model": "100% Free",
        "pros": ["Fast startup", "Low memory"],
        "cons": ["Limited plugins"],
        "best_for": "Test engineers",
        "flow_scene": "Dark workspace setup"
    }

    blog_html = generate_amp_blog_post(ide_sample)

    # AMP HTML Validation checks
    assert "<!doctype html>" in blog_html or "<!DOCTYPE html>" in blog_html
    assert "<html amp" in blog_html
    assert '<script async src="https://cdn.ampproject.org/v0.js"></script>' in blog_html
    assert "style amp-boilerplate" in blog_html
    assert "style amp-custom" in blog_html
    assert "ideguide.blogspot.com" in blog_html
    assert DISCLAIMER_TEXT in blog_html


def test_google_flow_video_spec_generation():
    ide_sample = {
        "name": "Test Editor",
        "category": "Test Category",
        "pricing": "Free / Open Source",
        "cost_model": "100% Free",
        "pros": ["Fast startup", "Low memory"],
        "cons": ["Limited plugins"],
        "best_for": "Test engineers",
        "flow_scene": "Dark workspace setup with neon backlighting"
    }

    spec_md = generate_google_flow_video_spec(ide_sample)

    assert "Google Flow Video & Shorts Prompt Specification: Test Editor" in spec_md
    assert "youtube.com/@IDEguide" in spec_md
    assert "Dark workspace setup with neon backlighting" in spec_md
    assert DISCLAIMER_TEXT in spec_md


def test_slug_sanitization():
    assert sanitize_slug("Visual Studio Code") == "visual-studio-code"
    assert sanitize_slug("C++ Editor / IDE!") == "c-editor-ide"
    assert sanitize_slug("JetBrains PyCharm") == "jetbrains-pycharm"


def test_daily_selection_batch():
    selection = select_daily_ides(3)
    assert len(selection) == 3
    names = [item["name"] for item in selection]
    assert len(set(names)) == 3  # All names in batch are unique


def test_generated_content_files_exist():
    # Verify content files generated in content/ directory
    date_dirs = glob.glob("content/20*")
    assert len(date_dirs) > 0, "Expected at least one content/YYYY-MM-DD directory"

    latest_dir = sorted(date_dirs)[-1]
    files = os.listdir(latest_dir)

    # 3 blog posts + 3 video specs = 6 files
    amp_blogs = [f for f in files if f.endswith("_amp_blog.html")]
    video_specs = [f for f in files if f.endswith("_google_flow_spec.md")]

    assert len(amp_blogs) == 3
    assert len(video_specs) == 3
