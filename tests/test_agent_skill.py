import os
import sys
import json
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'scripts')))

from ide_guide_agent_skill import lookup_or_build_ide_data
from generate_daily_content import DISCLAIMER, generate_amp_html_post

def test_lookup_or_build_ide_data():
    known_ide = lookup_or_build_ide_data("Zed Editor")
    assert known_ide["key"] == "zed"

    custom_ide = lookup_or_build_ide_data("Super Novel Code Editor")
    assert custom_ide["key"] == "super_novel_code_editor"
    assert custom_ide["name"] == "Super Novel Code Editor"

def test_agent_skill_disclaimer_integration():
    data = lookup_or_build_ide_data("Custom Editor")
    html = generate_amp_html_post(data, "2026-09-08")
    assert DISCLAIMER in html
