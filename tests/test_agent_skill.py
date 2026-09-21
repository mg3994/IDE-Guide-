"""Tests for Agentic CLI Skill Tool."""

from scripts.ide_guide_agent_skill import generate_custom_ide_content
from scripts.lib.amp_generator import DISCLAIMER_TEXT


def test_generate_custom_ide_content_by_name(tmp_path):
    outdir = str(tmp_path / "custom")
    result = generate_custom_ide_content(ide_name="Sublime Text 4", output_dir=outdir)

    assert "amp_post" in result
    assert "video_spec_json" in result
    assert "video_spec_md" in result

    with open(result["amp_post"], "r", encoding="utf-8") as f:
        amp_text = f.read()
        assert "Sublime Text 4" in amp_text
        assert DISCLAIMER_TEXT in amp_text
