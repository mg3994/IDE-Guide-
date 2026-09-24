#!/usr/bin/env python3
"""
Daily Batch Content Generator for IDE Guide
Generates 3 daily AMP blog posts and 3 Google Flow video specifications daily,
tracking history in content/history.json to ensure topic diversity without repeats.
"""

import datetime
import json
import os
import sys

# Ensure repository root is in PYTHONPATH
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from scripts.amp_validator import validate_amp_html
from scripts.ide_guide_agent_skill import IDE_DATABASE, generate_amp_blog, generate_video_spec, get_ide_data

HISTORY_FILE = "content/history.json"

AVAILABLE_IDES = list(IDE_DATABASE.keys()) + [
    "sublime_text",
    "fleet",
    "lapce",
    "emacs",
    "helix",
    "pycharm",
    "webstorm",
    "clion",
    "xcode",
    "android_studio"
]

def load_history() -> dict:
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"Warning: Failed to load history: {e}")
    return {"covered_ides": [], "daily_logs": {}}

def save_history(history: dict):
    os.makedirs(os.path.dirname(HISTORY_FILE), exist_ok=True)
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=2)

def select_daily_ides(history: dict, count: int = 3) -> list:
    covered = set(history.get("covered_ides", []))
    uncovered = [ide for ide in AVAILABLE_IDES if ide not in covered]

    if len(uncovered) < count:
        # Reset covered list if we run out of unique IDEs
        history["covered_ides"] = []
        uncovered = AVAILABLE_IDES

    selected = uncovered[:count]
    return selected

def generate_daily_batch(target_date_str: str = None) -> str:
    if not target_date_str:
        target_date_str = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d")

    date_dir = os.path.join("content", target_date_str)
    os.makedirs(date_dir, exist_ok=True)

    history = load_history()
    selected_ides = select_daily_ides(history, count=3)

    generated_summary = []

    for idx, ide_key in enumerate(selected_ides, 1):
        ide_data = get_ide_data(ide_key)
        slug = ide_data["name"].lower().replace(" ", "_")

        # 1. AMP Blog HTML
        amp_html = generate_amp_blog(ide_data)
        is_valid, errors = validate_amp_html(amp_html)
        if not is_valid:
            raise ValueError(f"Generated AMP HTML for {ide_key} is invalid: {errors}")

        blog_filename = f"post_{idx}_{slug}_amp.html"
        blog_path = os.path.join(date_dir, blog_filename)
        with open(blog_path, "w", encoding="utf-8") as f:
            f.write(amp_html)

        # 2. Google Flow Video Spec
        video_spec = generate_video_spec(ide_data)
        spec_filename = f"video_{idx}_{slug}_spec.json"
        spec_path = os.path.join(date_dir, spec_filename)
        with open(spec_path, "w", encoding="utf-8") as f:
            json.dump(video_spec, f, indent=2)

        generated_summary.append({
            "ide": ide_data["name"],
            "blog_path": blog_path,
            "video_spec_path": spec_path
        })

        if ide_key not in history["covered_ides"]:
            history["covered_ides"].append(ide_key)

    history.setdefault("daily_logs", {})[target_date_str] = [item["ide"] for item in generated_summary]
    save_history(history)

    print(f"🎉 Generated 3 daily packages for {target_date_str} in '{date_dir}':")
    for item in generated_summary:
        print(f"  • {item['ide']}:")
        print(f"      - Blog (AMP HTML): {item['blog_path']}")
        print(f"      - Video Spec (Google Flow): {item['video_spec_path']}")

    return date_dir

if __name__ == "__main__":
    date_arg = sys.argv[1] if len(sys.argv) > 1 else None
    generate_daily_batch(date_arg)
