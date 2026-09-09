import pytest
from src.ide_guide.catalog import (
    DEFAULT_IDE_CATALOG,
    get_ide_by_slug_or_name,
    construct_custom_ide_data
)

def test_default_catalog_not_empty():
    assert len(DEFAULT_IDE_CATALOG) >= 10

def test_catalog_items_schema():
    for ide in DEFAULT_IDE_CATALOG:
        assert "name" in ide
        assert "slug" in ide
        assert "developer" in ide
        assert "license_type" in ide
        assert "pricing" in ide
        assert "description" in ide
        assert "key_features" in ide
        assert "pros" in ide
        assert "cons" in ide
        assert "target_audience" in ide
        assert "verdict_rating" in ide
        assert "verdict_summary" in ide

def test_get_ide_by_slug_or_name():
    vscode = get_ide_by_slug_or_name("vs-code")
    assert vscode is not None
    assert vscode["name"] == "Visual Studio Code"

    cursor = get_ide_by_slug_or_name("Cursor")
    assert cursor is not None
    assert cursor["slug"] == "cursor"

    non_existent = get_ide_by_slug_or_name("non-existent-editor-12345")
    assert non_existent is None

def test_construct_custom_ide_data():
    custom = construct_custom_ide_data("Super IDE")
    assert custom["name"] == "Super IDE"
    assert custom["slug"] == "super-ide"
    assert len(custom["key_features"]) > 0
