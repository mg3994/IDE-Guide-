#!/usr/bin/env python3
"""
Daily Content Generation Script for IDE Guide.
Generates 3 AMP blog posts and 3 Google Flow AI video specifications per day.
Tracks generated tools in `content/history.json` to ensure distinct coverage.
"""

import json
import os
import re
import sys
from datetime import datetime, timezone
from typing import List, Dict, Any

# Ensure parent path is in sys.path when executed directly
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from scripts.ide_guide_agent_skill import (
    DEFAULT_IDE_KNOWLEDGE_BASE,
    get_ide_info,
    generate_amp_blog_post,
    generate_google_flow_video_spec
)

HISTORY_FILE = "content/history.json"

EXTENDED_IDE_POOL = [
    "cursor", "zed", "neovim", "windsurf", "pycharm",
    "vscode", "fleet", "sublime_text", "lapce", "helix",
    "visual_studio", "xcode", "android_studio", "replit", "nova"
]


def load_history() -> List[str]:
    """Loads previously covered IDE keys from history.json."""
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data.get("covered_ides", [])
        except Exception:
            return []
    return []


def save_history(covered_ides: List[str]):
    """Saves updated covered IDE keys to history.json."""
    os.makedirs(os.path.dirname(HISTORY_FILE), exist_ok=True)
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump({"covered_ides": covered_ides, "last_updated": datetime.now(timezone.utc).isoformat()}, f, indent=2)


def select_daily_ides(history: List[str], count: int = 3) -> List[str]:
    """Selects `count` IDEs that have not been covered recently."""
    available = [ide for ide in EXTENDED_IDE_POOL if ide not in history]
    if len(available) < count:
        # Reset or cycle if pool exhausted
        available = EXTENDED_IDE_POOL

    selected = available[:count]
    return selected


def main():
    date_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    out_dir = os.path.join("content", date_str)
    os.makedirs(out_dir, exist_ok=True)

    history = load_history()
    selected_keys = select_daily_ides(history, count=3)

    print(f"🚀 Generating daily content package for {date_str}...")
    print(f"Selected IDEs/Editors: {', '.join(selected_keys)}")

    generated_items = []

    for idx, key in enumerate(selected_keys, 1):
        info = get_ide_info(key)
        safe_name = re.sub(r'[^a-zA-Z0-9_-]', '_', info['name'].lower())

        amp_html = generate_amp_blog_post(info)
        video_spec = generate_google_flow_video_spec(info)

        blog_filename = f"post_{idx}_{safe_name}_amp.html"
        video_filename = f"video_{idx}_{safe_name}_flow_spec.json"

        blog_path = os.path.join(out_dir, blog_filename)
        video_path = os.path.join(out_dir, video_filename)

        with open(blog_path, "w", encoding="utf-8") as f:
            f.write(amp_html)

        with open(video_path, "w", encoding="utf-8") as f:
            json.dump(video_spec, f, indent=2)

        generated_items.append(key)
        print(f"  [{idx}/3] Created {info['name']}: {blog_filename} & {video_filename}")

    # Update history
    updated_history = list(set(history + generated_items))
    save_history(updated_history)

    print(f"✅ Daily content package complete for {date_str} in {out_dir}/")


if __name__ == "__main__":
    main()
