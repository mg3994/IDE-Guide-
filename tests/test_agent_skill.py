import os
import subprocess
import tempfile
import pytest

def test_agent_skill_cli():
    with tempfile.TemporaryDirectory() as tmpdir:
        cmd = [
            "python3", "scripts/ide_guide_agent_skill.py",
            "--ide", "Zed",
            "--output-dir", tmpdir,
            "--format", "both"
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)
        assert result.returncode == 0
        assert "Generated AMP HTML Blog Post" in result.stdout
        assert "Generated Google Flow Video Spec" in result.stdout

        generated_files = os.listdir(tmpdir)
        assert any(f.endswith("_amp_post.html") for f in generated_files)
        assert any(f.endswith("_google_flow_shorts_spec.md") for f in generated_files)
        assert any(f.endswith("_google_flow_longform_spec.md") for f in generated_files)
