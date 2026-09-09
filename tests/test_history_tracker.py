import os
import tempfile
import pytest
from src.ide_guide.history_tracker import HistoryTracker
from src.ide_guide.catalog import DEFAULT_IDE_CATALOG

def test_history_tracker_flow():
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_history_file = os.path.join(tmpdir, "history.json")
        tracker = HistoryTracker(history_file=tmp_history_file)

        assert not tracker.is_covered("vs-code")

        sample_ide = DEFAULT_IDE_CATALOG[0]
        tracker.mark_covered(sample_ide, date_str="2025-01-01")

        assert tracker.is_covered("vs-code")

        # Reload from file to ensure persistence
        reloaded_tracker = HistoryTracker(history_file=tmp_history_file)
        assert reloaded_tracker.is_covered("vs-code")

        # Test uncovered retrieval
        uncovered = reloaded_tracker.get_uncovered_from_catalog(DEFAULT_IDE_CATALOG, count=2)
        assert len(uncovered) == 2
        assert uncovered[0]["slug"] != "vs-code"
