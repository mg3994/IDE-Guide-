#!/usr/bin/env python3
"""
Daily Content Generator for IDE Guide.
Generates 3 daily AMP blog posts and 3 Google Flow video specs every day.
Stores outputs in content/YYYY-MM-DD/ and updates content/history.json.
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path

# Add parent directory to sys.path
sys.path.insert(0, str(Path(__file__).parent.parent))

from scripts.ide_guide_agent_skill import (
    load_ide_database,
    get_or_create_ide_info,
    generate_amp_blog_post,
    generate_google_flow_spec
)
from scripts.amp_validator import validate_amp_html

HISTORY_FILE = Path(__file__).parent.parent / "content" / "history.json"

def load_history() -> dict:
    if HISTORY_FILE.exists():
        try:
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {"covered_ids": [], "daily_runs": []}
    return {"covered_ids": [], "daily_runs": []}

def save_history(history: dict):
    HISTORY_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=2)

def select_daily_editors(count: int = 3) -> list[dict]:
    editors = load_ide_database()
    history = load_history()
    covered = set(history.get("covered_ids", []))

    selected = []
    # Select available un-covered editors from database first
    for ed in editors:
        if ed["id"] not in covered and len(selected) < count:
            selected.append(ed)

    # If database runs out of un-covered editors, reset covered or recycle
    if len(selected) < count:
        for ed in editors:
            if ed not in selected and len(selected) < count:
                selected.append(ed)

    return selected

def generate_daily_package(date_str: str = None) -> list[Path]:
    if not date_str:
        date_str = datetime.now().strftime("%Y-%m-%d")

    target_dir = Path(__file__).parent.parent / "content" / date_str
    target_dir.mkdir(parents=True, exist_ok=True)

    editors = select_daily_editors(count=3)
    history = load_history()
    generated_paths = []

    daily_entry = {
        "date": date_str,
        "posts": []
    }

    for idx, ed in enumerate(editors, start=1):
        slug = ed["id"]
        post_dir = target_dir / f"post_{idx}_{slug}"
        post_dir.mkdir(parents=True, exist_ok=True)

        # 1. AMP Blog Post
        amp_html = generate_amp_blog_post(ed)
        is_valid, errors = validate_amp_html(amp_html)
        if not is_valid:
            print(f"Warning: AMP validation warnings for {ed['name']}: {errors}")

        amp_file = post_dir / f"{slug}_blogger_amp.html"
        amp_file.write_text(amp_html, encoding="utf-8")
        generated_paths.append(amp_file)

        # 2. Google Flow Video Spec
        video_spec = generate_google_flow_spec(ed)
        spec_json_file = post_dir / f"{slug}_google_flow_spec.json"
        spec_json_file.write_text(json.dumps(video_spec, indent=2), encoding="utf-8")
        generated_paths.append(spec_json_file)

        # 3. Google Flow Markdown Spec
        spec_md = f"# Google Flow Video Spec: {video_spec['title']}\n\n"
        spec_md += f"**Target IDE**: {video_spec['target_ide']}\n"
        spec_md += f"**Pricing**: {video_spec['pricing_model']}\n\n"
        spec_md += "## YouTube Description\n```\n" + video_spec['description'] + "\n```\n\n"
        spec_md += "## Scene-by-Scene Visual Prompts\n\n"
        for scene in video_spec["scenes"]:
            spec_md += f"### Scene {scene['scene_number']} ({scene['timecode']})\n"
            spec_md += f"- **Visual Prompt**: `{scene['visual_prompt']}`\n"
            spec_md += f"- **Camera Movement**: {scene['camera_movement']}\n"
            spec_md += f"- **On-Screen Text**: {scene['onscreen_text'].replace('\n', ' | ')}\n"
            spec_md += f"- **Voiceover Script**: \"{scene['voiceover_script']}\"\n\n"

        spec_md_file = post_dir / f"{slug}_google_flow_spec.md"
        spec_md_file.write_text(spec_md, encoding="utf-8")
        generated_paths.append(spec_md_file)

        if slug not in history.get("covered_ids", []):
            history.setdefault("covered_ids", []).append(slug)

        daily_entry["posts"].append({
            "idx": idx,
            "ide_id": slug,
            "ide_name": ed["name"],
            "post_dir": str(post_dir.relative_to(Path(__file__).parent.parent))
        })

    history.setdefault("daily_runs", []).append(daily_entry)
    save_history(history)

    print(f"Daily content generation completed for {date_str}. Generated {len(editors)} posts (3 AMP HTML + 3 Video Specs).")
    return generated_paths

def main():
    date_arg = sys.argv[1] if len(sys.argv) > 1 else None
    generate_daily_package(date_arg)

if __name__ == "__main__":
    main()
