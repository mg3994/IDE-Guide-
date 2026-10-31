#!/usr/bin/env python3
"""
Daily Content Generator for IDE Guide
Generates exactly 3 distinct content packages (3 AMP blog posts + 3 Google Flow video scripts)
every day, rotating through the IDE database and recording history to prevent duplicates.
"""

import datetime
import json
import os
import sys
from typing import List, Dict, Any

# Ensure project root is in sys.path for direct script execution
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from scripts.ide_guide_agent_skill import generate_content_package
from scripts.amp_validator import validate_amp_html

DATABASE_PATH = "data/ide_database.json"
HISTORY_PATH = "content/history.json"
CONTENT_BASE_DIR = "content"


def load_database(filepath: str = DATABASE_PATH) -> List[Dict[str, Any]]:
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"IDE database not found at {filepath}")
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)


def load_history(filepath: str = HISTORY_PATH) -> Dict[str, Any]:
    if not os.path.exists(filepath):
        return {"covered_ide_ids": [], "daily_logs": []}
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {"covered_ide_ids": [], "daily_logs": []}


def save_history(history: Dict[str, Any], filepath: str = HISTORY_PATH) -> None:
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=2)


def select_daily_ides(
    db: List[Dict[str, Any]],
    covered_ids: List[str],
    count: int = 3
) -> List[Dict[str, Any]]:
    """
    Selects `count` IDEs that haven't been recently covered.
    If all IDEs have been covered, resets the cycle while maintaining fairness.
    """
    uncovered = [ide for ide in db if ide["id"] not in covered_ids]

    if len(uncovered) < count:
        # Reset cycle: clear old history items, take remaining uncovered plus wrap around
        needed = count - len(uncovered)
        # Sort previously covered by their position in covered_ids (least recently covered first)
        wrapped = [ide for ide in db if ide["id"] in covered_ids]
        wrapped.sort(key=lambda ide: covered_ids.index(ide["id"]))
        selected = uncovered + wrapped[:needed]
    else:
        selected = uncovered[:count]

    return selected


def generate_daily_batch(
    date_str: str = None,
    db_path: str = DATABASE_PATH,
    history_path: str = HISTORY_PATH,
    content_dir: str = CONTENT_BASE_DIR
) -> Dict[str, Any]:
    """Generates 3 blog posts and 3 video specs for the given day."""
    if date_str is None:
        date_str = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d")

    db = load_database(db_path)
    history = load_history(history_path)

    covered_ids = history.get("covered_ide_ids", [])
    selected_ides = select_daily_ides(db, covered_ids, count=3)

    daily_folder = os.path.join(content_dir, date_str)
    os.makedirs(daily_folder, exist_ok=True)

    generated_packages = []
    daily_covered_ids = []

    for index, ide in enumerate(selected_ides, start=1):
        pkg = generate_content_package(ide)
        ide_id = ide["id"]
        daily_covered_ids.append(ide_id)

        # Validate AMP HTML before saving
        is_amp_valid, amp_errors = validate_amp_html(pkg["amp_blog_post_html"], require_disclaimer=True)
        if not is_amp_valid:
            raise ValueError(f"AMP Validation failed for {ide['name']}: {amp_errors}")

        # Save AMP HTML Blog Post
        blog_filename = f"post_{index}_{ide_id}_amp_blogger.html"
        blog_path = os.path.join(daily_folder, blog_filename)
        with open(blog_path, "w", encoding="utf-8") as f:
            f.write(pkg["amp_blog_post_html"])

        # Save Google Flow Video Specification
        video_filename = f"video_{index}_{ide_id}_google_flow_spec.json"
        video_path = os.path.join(daily_folder, video_filename)
        with open(video_path, "w", encoding="utf-8") as f:
            json.dump(pkg["video_flow_spec"], f, indent=2)

        # Save Human-Readable Markdown Script for Studio Voiceover Recording
        script_filename = f"script_{index}_{ide_id}_voiceover.md"
        script_path = os.path.join(daily_folder, script_filename)
        with open(script_path, "w", encoding="utf-8") as f:
            f.write(f"# Voiceover & Flow Production Script: {ide['name']}\n\n")
            f.write(f"**Channel:** YouTube @IDEguide | **Blog:** ideguide.blogspot.com\n\n")
            f.write(f"**Pricing Tier:** {ide.get('pricing_tier')}\n\n")
            f.write("## Scene-by-Scene Breakdown\n\n")
            for scene in pkg["video_flow_spec"]["scenes"]:
                f.write(f"### Scene {scene['scene_number']}: {scene['scene_title']} ({scene['duration_seconds']}s)\n")
                f.write(f"- **Google Flow Prompt:** *{scene['google_flow_prompt']}*\n")
                f.write(f"- **On-Screen Text:** `{scene['on_screen_text']}`\n")
                f.write(f"- **Voiceover Audio:** \"{scene['voiceover_script']}\"\n")
                f.write(f"- **Visual B-Roll:** {scene['b_roll_suggestion']}\n")
                f.write(f"- **Audio SFX Cue:** {scene['audio_cue']}\n\n")
            f.write("## Mandatory Disclaimer\n\n")
            f.write(f"> {pkg['mandatory_disclaimer']}\n")

        generated_packages.append({
            "slot": index,
            "ide_id": ide_id,
            "ide_name": ide["name"],
            "blog_path": blog_path,
            "video_path": video_path,
            "script_path": script_path
        })

    # Update history tracking
    new_covered = [cid for cid in covered_ids if cid not in daily_covered_ids] + daily_covered_ids
    # Keep covered list up to date
    history["covered_ide_ids"] = new_covered
    daily_entry = {
        "date": date_str,
        "ides_covered": [ide["name"] for ide in selected_ides],
        "generated_files": [pkg["blog_path"] for pkg in generated_packages]
    }
    history["daily_logs"].append(daily_entry)
    save_history(history, history_path)

    return {
        "date": date_str,
        "packages": generated_packages
    }


def main():
    date_override = sys.argv[1] if len(sys.argv) > 1 else None
    print(f"Starting daily content generation pipeline for IDE Guide (3 posts & 3 videos)...")
    res = generate_daily_batch(date_str=date_override)
    print(f"Successfully generated 3 daily content packages for date: {res['date']}")
    for pkg in res["packages"]:
        print(f"Slot {pkg['slot']}: {pkg['ide_name']}")
        print(f"  - Blog (AMP HTML): {pkg['blog_path']}")
        print(f"  - Flow Spec (JSON): {pkg['video_path']}")
        print(f"  - Production Script (MD): {pkg['script_path']}")


if __name__ == "__main__":
    main()
