#!/usr/bin/env python3
"""
Daily Content Generation Pipeline for IDE Guide.
Generates 3 AMP blog posts and 3 Google Flow video specifications daily,
tracking covered topics in history.json to ensure variety.
"""

import datetime
import json
import os
from typing import List, Dict, Any, Tuple

from scripts.amp_validator import validate_amp_html
from scripts.ide_guide_agent_skill import (
    DEFAULT_IDE_KNOWLEDGE,
    generate_amp_blog_post,
    generate_google_flow_video_spec
)

HISTORY_FILE = "content/history.json"


def load_history() -> List[str]:
    """Loads previously covered IDE names from history log."""
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data.get("covered_ides", [])
        except Exception as e:
            print(f"Warning loading history file: {e}")
            return []
    return []


def save_history(covered_ides: List[str]) -> None:
    """Saves updated covered IDE names back to history log."""
    os.makedirs(os.path.dirname(HISTORY_FILE), exist_ok=True)
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump({"covered_ides": covered_ides, "last_updated": datetime.date.today().isoformat()}, f, indent=2)


def select_daily_ides(count: int = 3) -> Tuple[List[str], List[str]]:
    """
    Selects `count` unvisited IDEs from DEFAULT_IDE_KNOWLEDGE or resets history if exhausted.
    Returns (selected_ides, updated_history).
    """
    history = load_history()
    available = [ide for ide in DEFAULT_IDE_KNOWLEDGE if ide not in history]

    if len(available) < count:
        # Reset history pool if exhausted
        history = []
        available = list(DEFAULT_IDE_KNOWLEDGE.keys())

    selected = available[:count]
    return selected, history


def generate_daily_content_package(target_date: str = None) -> List[Dict[str, str]]:
    """Generates 3 daily packages (AMP HTML blog posts + Google Flow video specs)."""
    if not target_date:
        target_date = datetime.date.today().isoformat()

    output_dir = os.path.join("content", target_date)
    os.makedirs(output_dir, exist_ok=True)

    selected_ides, history = select_daily_ides(count=3)
    generated_results = []

    print(f"Generating daily content package for {target_date}...")
    for idx, ide_name in enumerate(selected_ides, start=1):
        slug = ide_name.lower().replace(" ", "_")
        ide_info = DEFAULT_IDE_KNOWLEDGE[ide_name]

        # 1. Generate Blog Post
        amp_html = generate_amp_blog_post(ide_name, ide_info)
        is_valid, errors = validate_amp_html(amp_html)
        if not is_valid:
            raise ValueError(f"Generated AMP HTML for {ide_name} failed validation: {errors}")

        blog_filename = f"post_{idx}_{slug}_amp.html"
        blog_filepath = os.path.join(output_dir, blog_filename)
        with open(blog_filepath, "w", encoding="utf-8") as f:
            f.write(amp_html)

        # 2. Generate Video Spec
        video_spec = generate_google_flow_video_spec(ide_name, ide_info)
        video_filename = f"video_{idx}_{slug}_spec.json"
        video_filepath = os.path.join(output_dir, video_filename)
        with open(video_filepath, "w", encoding="utf-8") as f:
            f.write(json.dumps(video_spec, indent=2))

        generated_results.append({
            "ide": ide_name,
            "blog_post": blog_filepath,
            "video_spec": video_filepath
        })

        if ide_name not in history:
            history.append(ide_name)

    save_history(history)
    print(f"Successfully generated {len(generated_results)} content packages in {output_dir}")
    return generated_results


if __name__ == "__main__":
    generate_daily_content_package()
