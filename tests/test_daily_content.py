import os
import json
import pytest
from scripts.generate_daily_content import (
    generate_daily_package,
    IDE_CATALOG,
    DISCLAIMER_TEXT
)
from scripts.amp_validator import AmpValidator

def test_ide_catalog_structure():
    assert len(IDE_CATALOG) >= 10
    for item in IDE_CATALOG:
        assert "id" in item
        assert "name" in item
        assert "category" in item
        assert "pricing_type" in item
        assert item["pricing_type"] in ["Free", "Paid", "Freemium"]
        assert len(item["pros"]) > 0
        assert len(item["cons"]) > 0

def test_daily_package_generation(tmp_path):
    test_date = "2026-10-18"
    files = generate_daily_package(target_date=test_date)
    assert len(files) == 6  # 3 blog posts + 3 video specs

    for filepath in files:
        assert os.path.exists(filepath)
        if filepath.endswith(".html"):
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
                assert DISCLAIMER_TEXT in content
                validator = AmpValidator(content)
                is_valid, errors, _ = validator.validate()
                assert is_valid, f"AMP validation failed for {filepath}: {errors}"
        elif filepath.endswith(".json"):
            with open(filepath, "r", encoding="utf-8") as f:
                spec = json.load(f)
                assert spec["disclaimer"] == DISCLAIMER_TEXT
                assert len(spec["scenes"]) == 4
