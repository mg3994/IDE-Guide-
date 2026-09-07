#!/usr/bin/env python3
"""
Daily Content Generator Script for IDE Guide
Generates 3 Blogger AMP HTML blog posts and 3 Google Flow video specs daily.
Maintains content/history.json to ensure non-repeating IDE coverage across days.
"""

import argparse
import datetime
import json
import os
import sys
from typing import List, Dict, Any

from ide_guide_agent_skill import (
    DISCLAIMER_TEXT,
    get_ide_info,
    generate_amp_blog_post,
    generate_google_flow_video_spec,
    validate_amp_html,
)

CURATED_IDE_CATALOG = [
    "Visual Studio Code",
    "Cursor",
    "Zed",
    "PyCharm",
    "Neovim",
    "Windsurf AI",
    "Helix Editor",
    "IntelliJ IDEA",
    "Sublime Text",
    "WebStorm",
    "CLion",
    "JetBrains Fleet",
    "Lapce",
    "GNU Emacs",
    "Apple Xcode",
    "Microsoft Visual Studio",
    "Eclipse IDE",
    "Panic Nova",
    "Android Studio",
    "Spyder IDE",
    "Kate Editor",
    "Geany",
    "BBEdit",
    "TextMate",
    "CodeLite",
    "SlickEdit",
]


def load_history(history_file: str) -> Dict[str, Any]:
    if os.path.exists(history_file):
        try:
            with open(history_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {"covered_ides": [], "daily_logs": {}}


def save_history(history_file: str, history_data: Dict[str, Any]):
    os.makedirs(os.path.dirname(os.path.abspath(history_file)), exist_ok=True)
    with open(history_file, "w", encoding="utf-8") as f:
        json.dump(history_data, f, indent=2)


def select_daily_ides(history_data: Dict[str, Any], count: int = 3) -> List[str]:
    already_covered = set(history_data.get("covered_ides", []))
    available = [ide for ide in CURATED_IDE_CATALOG if ide not in already_covered]

    if len(available) < count:
        # Reset covered set if catalog exhausted
        already_covered = set()
        available = CURATED_IDE_CATALOG.copy()

    selected = available[:count]
    return selected


def generate_daily_package(date_str: str, history_file: str, force: bool = False, base_dir: str = None) -> Dict[str, Any]:
    if base_dir is None:
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    content_dir = os.path.join(base_dir, "content", date_str)

    if os.path.exists(content_dir) and not force:
        print(f"Notice: Content directory '{content_dir}' already exists. Use --force to overwrite.")
        return {"status": "skipped", "date": date_str}

    os.makedirs(content_dir, exist_ok=True)
    history_data = load_history(history_file)

    selected_ides = select_daily_ides(history_data, count=3)
    generated_files = []

    for idx, ide_name in enumerate(selected_ides, start=1):
        ide_info = get_ide_info(ide_name)
        slug = ide_info["name"].lower().replace(" ", "_").replace("(", "").replace(")", "").replace("-", "_")

        # 1. AMP Blog Post
        amp_html = generate_amp_blog_post(ide_info)
        blog_filename = f"ide_{idx}_{slug}_blog_post.amp.html"
        blog_path = os.path.join(content_dir, blog_filename)
        with open(blog_path, "w", encoding="utf-8") as f:
            f.write(amp_html)

        # Validate AMP
        is_valid, errors = validate_amp_html(amp_html)
        if not is_valid:
            print(f"Warning: AMP validation warnings for {blog_filename}: {errors}")

        # 2. Google Flow Video Spec
        video_spec = generate_google_flow_video_spec(ide_info)
        video_filename = f"ide_{idx}_{slug}_google_flow_video.json"
        video_path = os.path.join(content_dir, video_filename)
        with open(video_path, "w", encoding="utf-8") as f:
            json.dump(video_spec, f, indent=2)

        generated_files.extend([blog_path, video_path])

        if ide_info["name"] not in history_data["covered_ides"]:
            history_data["covered_ides"].append(ide_info["name"])

    history_data["daily_logs"][date_str] = {
        "generated_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "ides": selected_ides,
        "files_count": len(generated_files)
    }

    save_history(history_file, history_data)

    print(f"✨ Daily Content Package successfully created for {date_str}:")
    for filepath in generated_files:
        print(f"  - {os.path.basename(filepath)}")

    return {
        "status": "success",
        "date": date_str,
        "ides": selected_ides,
        "files": generated_files
    }


def main():
    parser = argparse.ArgumentParser(description="IDE Guide Daily Content Generator")
    parser.add_argument("--date", type=str, default=None, help="Target date in YYYY-MM-DD format (defaults to UTC today)")
    parser.add_argument("--force", action="store_true", help="Force regenerate even if target directory exists")
    args = parser.parse_args()

    date_str = args.date or datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d")
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    history_file = os.path.join(base_dir, "content", "history.json")

    result = generate_daily_package(date_str, history_file, force=args.force)
    if result.get("status") == "skipped":
        sys.exit(0)


if __name__ == "__main__":
    main()
