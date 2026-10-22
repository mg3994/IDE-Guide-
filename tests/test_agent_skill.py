import json
from pathlib import Path
import pytest
from scripts.ide_guide_agent_skill import generate_custom_content
from scripts.amp_validator import validate_file, REQUIRED_DISCLAIMER


def test_generate_custom_content_with_ide(tmp_path):
    outdir = str(tmp_path / "custom_out")
    res = generate_custom_content(ide_name="Helix Editor", outdir=outdir)

    assert Path(res["blog_file"]).exists()
    assert Path(res["spec_json_file"]).exists()
    assert Path(res["spec_md_file"]).exists()

    # AMP Validation
    val_res = validate_file(res["blog_file"])
    assert val_res["valid"] is True, f"AMP validation failed: {val_res['errors']}"

    # Disclaimer check
    with open(res["spec_json_file"], "r", encoding="utf-8") as f:
        data = json.load(f)
        assert data["disclaimer"] == REQUIRED_DISCLAIMER


def test_generate_custom_content_with_repo(tmp_path):
    outdir = str(tmp_path / "repo_out")
    repo_url = "https://github.com/lapce/lapce"
    res = generate_custom_content(ide_name="Lapce", repo_url=repo_url, outdir=outdir)

    assert Path(res["blog_file"]).exists()
    val_res = validate_file(res["blog_file"])
    assert val_res["valid"] is True

    with open(res["blog_file"], "r", encoding="utf-8") as f:
        html = f.read()
        assert repo_url in html
        assert REQUIRED_DISCLAIMER in html
