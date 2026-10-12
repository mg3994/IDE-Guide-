#!/usr/bin/env python3
"""
Daily Content Generator Engine for IDE Guide.
Generates 3 AMP Blog Posts and 3 Google Flow Video Specs daily, tracks history in content/history.json,
and validates AMP HTML compliance.
"""

import os
import json
import datetime
import sys
from typing import List

from scripts.ide_guide_agent_skill import generate_amp_blog_post, generate_google_flow_spec, IDE_KNOWLEDGE_BASE
from scripts.amp_validator import validate_amp_html

IDE_POOL = list(IDE_KNOWLEDGE_BASE.keys())

def load_history(history_path: str) -> List[str]:
    if os.path.exists(history_path):
        try:
            with open(history_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data.get("history", [])
        except Exception as e:
            print(f"Warning: Could not read history file ({e}). Starting fresh.")
    return []

def save_history(history_path: str, history: List[str]):
    os.makedirs(os.path.dirname(history_path), exist_ok=True)
    with open(history_path, "w", encoding="utf-8") as f:
        json.dump({"history": history}, f, indent=2)

def generate_daily(date_str: str = None) -> List[str]:
    if not date_str:
        date_str = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d")

    history_path = "content/history.json"
    history = load_history(history_path)

    # Select 3 candidates not recently selected, or reset if pool exhausted
    available = [ide for ide in IDE_POOL if ide not in history]
    if len(available) < 3:
        print("IDE pool exhausted in history tracking. Resetting history pool rotation.")
        history = []
        available = list(IDE_POOL)

    selected_ides = available[:3]
    output_dir = os.path.join("content", date_str)
    os.makedirs(output_dir, exist_ok=True)

    generated_files = []

    for idx, ide in enumerate(selected_ides, 1):
        slug = ide.lower().replace(" ", "_")

        # 1. Generate AMP Blog Post
        blog_content = generate_amp_blog_post(ide)
        blog_filename = f"blog_{idx}_{slug}.html"
        blog_filepath = os.path.join(output_dir, blog_filename)

        with open(blog_filepath, "w", encoding="utf-8") as f:
            f.write(blog_content)

        # Validate AMP
        is_valid, errors = validate_amp_html(blog_content)
        if not is_valid:
            print(f"❌ Error validating AMP HTML for {blog_filepath}: {errors}")
            sys.exit(1)

        generated_files.append(blog_filepath)

        # 2. Generate Google Flow Video Spec
        video_spec = generate_google_flow_spec(ide)
        video_filename = f"video_{idx}_{slug}.json"
        video_filepath = os.path.join(output_dir, video_filename)

        with open(video_filepath, "w", encoding="utf-8") as f:
            json.dump(video_spec, f, indent=2)

        generated_files.append(video_filepath)

        # Record in history
        history.append(ide)

    save_history(history_path, history)
    print(f"✅ Daily content successfully generated for {date_str} in {output_dir}:")
    for file in generated_files:
        print(f"  - {file}")

    return generated_files

if __name__ == "__main__":
    target_date = sys.argv[1] if len(sys.argv) > 1 else None
    generate_daily(target_date)
