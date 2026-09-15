#!/usr/bin/env python3
"""
Daily Content Generator Engine for IDE Guide
Generates 3 AMP HTML blog posts and 3 Google Flow video specifications daily,
tracking history to prevent duplicates across days.
"""

import os
import json
import random
from datetime import datetime
from typing import List, Dict, Any

from ide_guide_agent_skill import IDE_DATABASE, generate_amp_html_blog, generate_google_flow_video_spec

CONTENT_DIR = "content"
HISTORY_FILE = os.path.join(CONTENT_DIR, "history.json")

def load_history() -> Dict[str, Any]:
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {"covered_keys": []}
    return {"covered_keys": []}

def save_history(history: Dict[str, Any]) -> None:
    os.makedirs(CONTENT_DIR, exist_ok=True)
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=2)

def select_daily_ides(count: int = 3) -> List[Dict[str, Any]]:
    history = load_history()
    covered = set(history.get("covered_keys", []))

    available = [k for k in IDE_DATABASE.keys() if k not in covered]

    # If all IDEs covered, reset history cycle
    if len(available) < count:
        covered = set()
        available = list(IDE_DATABASE.keys())

    selected_keys = available[:count]

    # Update covered list
    history["covered_keys"] = list(covered.union(set(selected_keys)))
    save_history(history)

    return [IDE_DATABASE[k] for k in selected_keys]

def generate_daily_batch(date_str: str = None) -> List[str]:
    if not date_str:
        date_str = datetime.now().strftime("%Y-%m-%d")

    day_dir = os.path.join(CONTENT_DIR, date_str)
    blogs_dir = os.path.join(day_dir, "blogs")
    videos_dir = os.path.join(day_dir, "videos")

    os.makedirs(blogs_dir, exist_ok=True)
    os.makedirs(videos_dir, exist_ok=True)

    selected_ides = select_daily_ides(count=3)
    generated_files = []

    for idx, ide_data in enumerate(selected_ides, 1):
        slug = ide_data["name"].lower().replace(" ", "_").replace("-", "_")

        # 1. Generate AMP HTML blog post
        amp_html = generate_amp_html_blog(ide_data)
        blog_file = os.path.join(blogs_dir, f"post_{idx}_{slug}_amp.html")
        with open(blog_file, "w", encoding="utf-8") as f:
            f.write(amp_html)
        generated_files.append(blog_file)

        # 2. Generate Google Flow video spec
        video_spec = generate_google_flow_video_spec(ide_data)
        video_file = os.path.join(videos_dir, f"video_{idx}_{slug}_google_flow_spec.json")
        with open(video_file, "w", encoding="utf-8") as f:
            json.dump(video_spec, f, indent=2)
        generated_files.append(video_file)

    return generated_files

def main():
    date_str = datetime.now().strftime("%Y-%m-%d")
    print(f"🚀 Generating Daily Content Batch for {date_str}...")
    files = generate_daily_batch(date_str)
    print(f"✅ Generated {len(files)} content artifacts in content/{date_str}/")
    for f in files:
        print(f"  - {f}")

if __name__ == "__main__":
    main()
