import json
import pytest
from pathlib import Path
from scripts.generate_daily_content import DATA_PATH, load_database

def test_database_loads_successfully():
    db = load_database()
    assert "editors" in db
    assert len(db["editors"]) >= 10
    assert "disclaimer" in db
    assert "channel_info" in db

def test_database_editor_fields():
    db = load_database()
    required_fields = [
        "id", "name", "tagline", "category", "pricing", "url",
        "pros", "cons", "target_audience", "verdict", "rating",
        "featured_features", "visual_prompts"
    ]
    seen_ids = set()
    for editor in db["editors"]:
        for field in required_fields:
            assert field in editor, f"Editor {editor.get('id')} missing field {field}"
        assert editor["id"] not in seen_ids, f"Duplicate ID: {editor['id']}"
        seen_ids.add(editor["id"])

        # Pricing check
        assert "tier" in editor["pricing"]
        assert "is_free" in editor["pricing"]
        assert "details" in editor["pricing"]

        # Visual prompts check
        assert "hero_shot" in editor["visual_prompts"]
        assert "color_palette" in editor["visual_prompts"]

        # Content substance
        assert len(editor["pros"]) >= 3
        assert len(editor["cons"]) >= 2
        assert 1.0 <= editor["rating"] <= 5.0
