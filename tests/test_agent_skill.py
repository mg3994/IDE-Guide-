import os
import json
import pytest
from scripts.ide_guide_agent_skill import process_ide_request
from scripts.amp_validator import AmpValidator, REQUIRED_DISCLAIMER

def test_agentic_skill_custom_ide(tmp_path):
    output_dir = str(tmp_path)
    res = process_ide_request(
        ide_name="Helix Editor",
        category="Terminal Modal Editor",
        pricing="Free",
        url="https://helix-editor.com",
        output_dir=output_dir
    )

    assert os.path.exists(res["blog_file"])
    assert os.path.exists(res["video_file"])

    with open(res["blog_file"], "r", encoding="utf-8") as f:
        html = f.read()
        assert "Helix Editor" in html
        assert REQUIRED_DISCLAIMER in html
        validator = AmpValidator(html)
        is_valid, errors, _ = validator.validate()
        assert is_valid, f"AMP validation errors: {errors}"

    with open(res["video_file"], "r", encoding="utf-8") as f:
        spec = json.load(f)
        assert spec["pricing_badge"] == "FREE"
        assert spec["disclaimer"] == REQUIRED_DISCLAIMER
