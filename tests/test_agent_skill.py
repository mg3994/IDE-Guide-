"""Tests for IDE Guide Agent Skill CLI and custom IDE generation."""

import os
import subprocess
import tempfile
import json
import pytest
from scripts.ide_guide_agent_skill import generate_custom_ide_data
from data.ide_database import get_ide_by_name


def test_custom_ide_synthesis():
    custom_data = generate_custom_ide_data(
        name="MicroEditor",
        url="https://github.com/zyedidia/micro",
        category="Terminal Text Editor",
    )
    assert custom_data["name"] == "MicroEditor"
    assert custom_data["official_url"] == "https://github.com/zyedidia/micro"
    assert custom_data["category"] == "Terminal Text Editor"
    assert len(custom_data["pros"]) > 0
    assert len(custom_data["cons"]) > 0
    assert "visual_theme" in custom_data
    assert "flow_broll_prompt" in custom_data


def test_cli_execution_known_ide():
    with tempfile.TemporaryDirectory() as tmpdir:
        res = subprocess.run(
            [
                "python3",
                "scripts/ide_guide_agent_skill.py",
                "--ide",
                "Windsurf",
                "--output-dir",
                tmpdir,
            ],
            capture_output=True,
            text=True,
        )
        assert res.returncode == 0
        assert "Found pre-configured entry for 'Windsurf'" in res.stdout

        expected_files = [
            os.path.join(tmpdir, "windsurf_amp_blogger_post.html"),
            os.path.join(tmpdir, "windsurf_google_flow_16x9.json"),
            os.path.join(tmpdir, "windsurf_google_flow_shorts_9x16.json"),
        ]
        for f in expected_files:
            assert os.path.exists(f)


def test_cli_execution_custom_unknown_ide():
    with tempfile.TemporaryDirectory() as tmpdir:
        res = subprocess.run(
            [
                "python3",
                "scripts/ide_guide_agent_skill.py",
                "--ide",
                "NovaEditor",
                "--repo-url",
                "https://nova.app",
                "--output-dir",
                tmpdir,
            ],
            capture_output=True,
            text=True,
        )
        assert res.returncode == 0
        assert "Synthesizing custom model" in res.stdout

        post_file = os.path.join(tmpdir, "novaeditor_amp_blogger_post.html")
        assert os.path.exists(post_file)
        with open(post_file, "r", encoding="utf-8") as f:
            content = f.read()
            assert "NovaEditor" in content
            assert "Disclaimer: IDE Guide is an independent technical publication." in content
