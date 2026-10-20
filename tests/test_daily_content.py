import os
import json
import tempfile
import pytest
from scripts.generate_daily_content import select_daily_ides, load_history, save_history, IDE_POOL, generate_amp_blog_post, generate_google_flow_spec
from scripts.amp_validator import validate_amp_html

def test_select_daily_ides_selects_3_unique():
    with tempfile.TemporaryDirectory() as tmpdir:
        history_file = os.path.join(tmpdir, "history.json")
        selected, updated_covered = select_daily_ides(history_file, count=3)
        assert len(selected) == 3
        ids = [ide["id"] for ide in selected]
        assert len(set(ids)) == 3
        assert len(updated_covered) == 3

def test_history_deduplication():
    with tempfile.TemporaryDirectory() as tmpdir:
        history_file = os.path.join(tmpdir, "history.json")

        # Mark first 3 IDEs as covered
        covered = [IDE_POOL[0]["id"], IDE_POOL[1]["id"], IDE_POOL[2]["id"]]
        save_history(history_file, covered)

        selected_next, updated_covered = select_daily_ides(history_file, count=3)
        next_ids = [ide["id"] for ide in selected_next]

        for cid in covered:
            assert cid not in next_ids

def test_generated_amp_blog_post_validity():
    ide = IDE_POOL[0]
    post = generate_amp_blog_post(ide, "2026-10-20", 1)
    is_valid, errors = validate_amp_html(post)
    assert is_valid is True, f"Errors: {errors}"

def test_generated_google_flow_spec():
    ide = IDE_POOL[0]
    flow_spec = generate_google_flow_spec(ide, "2026-10-20", 1)
    assert flow_spec["metadata"]["channel"] == "@IDEguide"
    assert "disclaimer_overlay" in flow_spec
    assert "Disclaimer: IDE Guide is an independent technical publication" in flow_spec["disclaimer_overlay"]["text"]
