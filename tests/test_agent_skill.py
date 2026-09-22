import os
import subprocess
import tempfile
import unittest
from scripts.ide_guide_agent_skill import get_ide_info

class TestAgentSkill(unittest.TestCase):
    def test_known_ide_lookup(self):
        info = get_ide_info("Zed")
        self.assertEqual(info["name"], "Zed")
        self.assertEqual(info["pricing_type"], "Free")
        self.assertIn("pros", info)
        self.assertIn("cons", info)

    def test_repo_url_lookup(self):
        repo_url = "https://github.com/neovim/neovim"
        info = get_ide_info("", repo_url=repo_url)
        self.assertIn("Neovim", info["name"])
        self.assertEqual(info["repo_url"], repo_url)

    def test_cli_execution(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            cmd = [
                "python3",
                "scripts/ide_guide_agent_skill.py",
                "--ide", "PyCharm",
                "--output-dir", temp_dir,
                "--format", "all"
            ]
            result = subprocess.run(cmd, capture_output=True, text=True)
            self.assertEqual(result.returncode, 0)

            created_files = os.listdir(temp_dir)
            self.assertEqual(len(created_files), 2)
            self.assertTrue(any(f.startswith("post_") and f.endswith(".html") for f in created_files))
            self.assertTrue(any(f.startswith("video_spec_") and f.endswith(".md") for f in created_files))

if __name__ == "__main__":
    unittest.main()
