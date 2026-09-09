"""
History Tracker Module for IDE Guide
Tracks evaluated IDEs in content/history.json to prevent duplicate coverage.
"""

import os
import json
from datetime import datetime, timezone
from typing import Dict, List, Any, Optional

HISTORY_FILE_PATH = os.path.join("content", "history.json")

class HistoryTracker:
    def __init__(self, history_file: str = HISTORY_FILE_PATH):
        self.history_file = history_file
        self.data = self.load_history()

    def load_history(self) -> Dict[str, Any]:
        if os.path.exists(self.history_file):
            try:
                with open(self.history_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass
        return {"covered_ides": {}, "last_updated": ""}

    def save_history(self) -> None:
        os.makedirs(os.path.dirname(self.history_file), exist_ok=True)
        self.data["last_updated"] = datetime.now(timezone.utc).isoformat()
        with open(self.history_file, "w", encoding="utf-8") as f:
            json.dump(self.data, f, indent=2)

    def is_covered(self, slug: str) -> bool:
        return slug.lower() in self.data.get("covered_ides", {})

    def mark_covered(self, ide_data: Dict[str, Any], date_str: Optional[str] = None) -> None:
        if date_str is None:
            date_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")

        slug = ide_data.get("slug", "").lower()
        if not slug:
            return

        self.data["covered_ides"][slug] = {
            "name": ide_data.get("name"),
            "developer": ide_data.get("developer"),
            "license_type": ide_data.get("license_type"),
            "date_covered": date_str
        }
        self.save_history()

    def get_uncovered_from_catalog(self, catalog: List[Dict[str, Any]], count: int = 3) -> List[Dict[str, Any]]:
        uncovered = []
        for ide in catalog:
            if not self.is_covered(ide.get("slug", "")):
                uncovered.append(ide)
                if len(uncovered) == count:
                    break
        return uncovered
