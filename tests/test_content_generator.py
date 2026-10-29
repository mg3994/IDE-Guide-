import os
import pytest
from unittest.mock import patch
from scripts.generate_daily_content import generate_daily_package, load_history

def test_generate_daily_package(tmp_path):
    test_date = "2026-09-01"
    temp_history_file = str(tmp_path / "history.json")

    with patch("scripts.generate_daily_content.HISTORY_FILE", temp_history_file):
        files = generate_daily_package(test_date)
        assert len(files) == 6  # 3 blog posts + 3 video specs

        for file_path in files:
            assert os.path.exists(file_path)

        history = load_history()
        assert len(history) >= 3

    # Clean up created content folder after test
    content_dir = os.path.join(os.path.dirname(__file__), "..", "content", test_date)
    if os.path.exists(content_dir):
        import shutil
        shutil.rmtree(content_dir)
