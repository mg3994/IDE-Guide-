#!/usr/bin/env python3
"""
Daily Content Generator for IDE Guide.
Selects 3 distinct IDEs or comparisons per run, generates 3 AMP HTML blog posts
and 3 Google Flow video generation specs in content/YYYY-MM-DD/, and updates history.
"""

import os
import sys
import json
from datetime import datetime
from typing import List, Dict, Any

from scripts.ide_guide_agent_skill import (
    load_ide_database,
    generate_amp_blog_post,
    generate_google_flow_video_spec
)
from scripts.amp_validator import validate_amp_html

HISTORY_FILE = os.path.join(os.path.dirname(__file__), "..", "content", "history.json")

def load_history() -> List[str]:
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data.get("published_history", [])
        except Exception:
            return []
    return []

def save_history(history: List[str]):
    os.makedirs(os.path.dirname(HISTORY_FILE), exist_ok=True)
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump({"published_history": history}, f, indent=2)

def select_daily_ides(db: Dict[str, Any], history: List[str], count: int = 3) -> List[str]:
    all_keys = list(db.keys())
    uncovered = [k for k in all_keys if k not in history]

    # If all IDEs in database have been published, reset cycle
    if len(uncovered) < count:
        uncovered = all_keys

    selected = uncovered[:count]
    return selected

def generate_daily_package(date_str: str = None) -> List[str]:
    if not date_str:
        date_str = datetime.utcnow().strftime("%Y-%m-%d")

    db = load_ide_database()
    history = load_history()
    selected_keys = select_daily_ides(db, history, count=3)

    target_dir = os.path.join(os.path.dirname(__file__), "..", "content", date_str)
    os.makedirs(target_dir, exist_ok=True)

    generated_files = []

    for idx, key in enumerate(selected_keys, 1):
        ide_info = db[key]
        blog_html = generate_amp_blog_post(ide_info)
        video_spec = generate_google_flow_video_spec(ide_info)

        # Validate AMP
        is_valid, errors = validate_amp_html(blog_html)
        if not is_valid:
            raise ValueError(f"Generated blog post for {key} failed AMP validation: {errors}")

        blog_filename = f"post_{idx}_{key}_amp.html"
        video_filename = f"video_{idx}_{key}_flow_spec.md"

        blog_path = os.path.join(target_dir, blog_filename)
        video_path = os.path.join(target_dir, video_filename)

        with open(blog_path, "w", encoding="utf-8") as f:
            f.write(blog_html)

        with open(video_path, "w", encoding="utf-8") as f:
            f.write(video_spec)

        generated_files.extend([blog_path, video_path])

        if key not in history:
            history.append(key)

    save_history(history)
    print(f"Successfully generated 3 daily content packages in: {target_dir}")
    return generated_files

def main():
    date_str = sys.argv[1] if len(sys.argv) > 1 else None
    generate_daily_package(date_str)

if __name__ == "__main__":
    main()
