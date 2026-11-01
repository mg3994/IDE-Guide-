import pytest
import shutil
from pathlib import Path
from scripts.ide_guide_agent_skill import find_editor_by_name, generate_for_editor

def test_find_editor_by_name():
    cursor = find_editor_by_name("cursor")
    assert cursor is not None
    assert cursor["name"] == "Cursor"

    zed = find_editor_by_name("Zed")
    assert zed is not None
    assert zed["id"] == "zed"

    missing = find_editor_by_name("NonExistentEditor999")
    assert missing is None

def test_generate_for_editor(tmp_path):
    editor = find_editor_by_name("Neovim")
    assert editor is not None
    res = generate_for_editor(editor, tmp_path, date_str="2026-11-01")

    assert Path(res["blog_path"]).exists()
    assert Path(res["video_path"]).exists()
    assert res["disclaimer_present"] is True
