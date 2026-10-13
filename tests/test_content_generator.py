import pytest
import os
import json
import shutil
from scripts.generate_daily_content import (
    run_daily_generation,
    load_ide_database,
    REQUIRED_DISCLAIMER
)
from scripts.amp_validator import validate_amp_html

def test_load_ide_database():
    ides = load_ide_database()
    assert len(ides) >= 10
    for ide in ides:
        assert "id" in ide
        assert "name" in ide
        assert "pros" in ide
        assert "cons" in ide
        assert "pricing_type" in ide

def test_run_daily_generation(tmp_path):
    test_date = "2026-10-14"
    generated_files = run_daily_generation(test_date)
    assert len(generated_files) == 9  # 3 blog posts, 3 specs, 3 scripts

    for file_path in generated_files:
        assert os.path.exists(file_path)
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
            assert REQUIRED_DISCLAIMER in content

        if file_path.endswith(".html"):
            is_valid, errors = validate_amp_html(content)
            assert is_valid, f"Generated blog post {file_path} failed AMP validation: {errors}"
