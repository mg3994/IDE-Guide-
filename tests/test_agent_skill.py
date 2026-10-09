import os
import json
import shutil
import pytest
from scripts.ide_guide_agent_skill import (
    derive_ide_info,
    generate_amp_blog_post,
    generate_google_flow_spec
)
from scripts.amp_validator import validate_amp_html, MANDATORY_DISCLAIMER


def test_derive_ide_info():
    vscode_info = derive_ide_info("VS Code")
    assert vscode_info["name"] == "Visual Studio Code"
    assert vscode_info["vendor"] == "Microsoft"
    assert len(vscode_info["pros"]) > 0
    assert len(vscode_info["cons"]) > 0

    custom_info = derive_ide_info(repo_url="https://github.com/example/my-custom-editor")
    assert custom_info["name"] == "my-custom-editor"


def test_generate_amp_blog_post():
    info = derive_ide_info("Neovim")
    blog_html = generate_amp_blog_post(info)

    is_valid, errors = validate_amp_html(blog_html)
    assert is_valid is True, f"Errors: {errors}"
    assert "Neovim" in blog_html
    assert "The Good (Pros)" in blog_html
    assert "The Bad (Cons)" in blog_html
    assert "Pricing" in blog_html
    assert MANDATORY_DISCLAIMER in blog_html


def test_generate_google_flow_spec():
    info = derive_ide_info("Sublime Text")
    flow_spec = generate_google_flow_spec(info)

    assert flow_spec["channel"] == "IDE Guide (@IDEguide)"
    assert flow_spec["ide_name"] == "Sublime Text 4"
    assert flow_spec["disclaimer"] == MANDATORY_DISCLAIMER
    assert len(flow_spec["timeline_scenes"]) >= 5
    for scene in flow_spec["timeline_scenes"]:
        assert "google_flow_prompt" in scene
        assert "narration" in scene
        assert "timestamp" in scene
