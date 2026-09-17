import os
import sys
import subprocess
import tempfile
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'scripts')))

from generate_daily_content import MANDATORY_DISCLAIMER

def test_cli_skill_ide_flag():
    with tempfile.TemporaryDirectory() as tmpdir:
        cmd = [
            sys.executable,
            os.path.join("scripts", "ide_guide_agent_skill.py"),
            "--ide", "Neovim",
            "--output-dir", tmpdir
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, env=dict(os.environ, PYTHONPATH="scripts"))
        assert result.returncode == 0

        blog_file = os.path.join(tmpdir, "blog_neovim.html")
        video_file = os.path.join(tmpdir, "video_neovim.md")

        assert os.path.exists(blog_file)
        assert os.path.exists(video_file)

        with open(blog_file, 'r', encoding='utf-8') as f:
            blog_content = f.read()
            assert MANDATORY_DISCLAIMER in blog_content
            assert "Neovim" in blog_content

        with open(video_file, 'r', encoding='utf-8') as f:
            video_content = f.read()
            assert MANDATORY_DISCLAIMER in video_content
            assert "Neovim" in video_content

def test_cli_skill_repo_flag():
    with tempfile.TemporaryDirectory() as tmpdir:
        cmd = [
            sys.executable,
            os.path.join("scripts", "ide_guide_agent_skill.py"),
            "--repo", "https://github.com/zed-industries/zed",
            "--output-dir", tmpdir
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, env=dict(os.environ, PYTHONPATH="scripts"))
        assert result.returncode == 0

        blog_file = os.path.join(tmpdir, "blog_zed.html")
        video_file = os.path.join(tmpdir, "video_zed.md")

        assert os.path.exists(blog_file)
        assert os.path.exists(video_file)
