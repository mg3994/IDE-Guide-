#!/usr/bin/env python3
"""
Daily Content Generation Script for IDE Guide
Generates 3 AMP HTML Blog posts and 3 Google Flow Video Specs per day.
Maintains history in content/history.json to prevent repetitive coverage.
"""

import datetime
import json
import os
import sys
import urllib.request
import urllib.parse
from typing import List, Dict, Any, Optional

from ide_guide_agent_skill import (
    fetch_or_build_ide_data,
    generate_amp_html_blogpost,
    generate_google_flow_video_spec,
    sanitize_slug,
    KNOWN_IDES_DATABASE,
    DISCLAIMER_TEXT
)

HISTORY_FILE = os.path.join("content", "history.json")

CURATED_IDE_POOL = [
    "zed", "cursor", "neovim", "vscodium", "lapce", "fleet",
    "helix", "pulsar", "pycharm", "vscode", "sublime-text", "emacs",
    "intellij-idea", "webstorm", "clion", "rider", "eclipse", "kate",
    "geany", "brackets", "nova", "panic-nova", "cadium", "codeblocks"
]


def load_history() -> Dict[str, Any]:
    """Loads historical coverage record."""
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"[WARN] Error loading history file: {e}. Reinitializing.")
    return {"covered_slugs": [], "daily_logs": {}}


def save_history(history: Dict[str, Any]) -> None:
    """Saves updated history record."""
    os.makedirs("content", exist_ok=True)
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=2)


def discover_trending_ides_github() -> List[str]:
    """Attempts to discover code editor repositories on GitHub."""
    discovered = []
    url = "https://api.github.com/search/repositories?q=topic:text-editor+topic:ide&sort=stars&order=desc&per_page=15"
    headers = {"User-Agent": "IDE-Guide-Bot/1.0"}
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=5) as response:
            if response.status == 200:
                data = json.loads(response.read().decode())
                items = data.get("items", [])
                for item in items:
                    name = item.get("name", "")
                    if name and len(name) >= 3:
                        discovered.append(name)
    except Exception as e:
        print(f"[INFO] GitHub API search skipped/unavailable ({e}). Using curated fallback pool.")
    return discovered


def select_daily_ides(count: int = 3) -> List[str]:
    """Selects target IDEs for today ensuring no duplicate coverage."""
    history = load_history()
    covered = set(history.get("covered_slugs", []))

    candidate_list = []

    # First check GitHub discovery
    github_candidates = discover_trending_ides_github()
    for item in github_candidates:
        slug = sanitize_slug(item)
        if slug not in covered and slug not in candidate_list:
            candidate_list.append(item)

    # Next add curated list candidates
    for item in CURATED_IDE_POOL:
        slug = sanitize_slug(item)
        if slug not in covered and slug not in candidate_list:
            candidate_list.append(item)

    # If all items are covered, reset history cycle gracefully
    if len(candidate_list) < count:
        print("[INFO] All curated IDEs covered. Resetting history cycle for new coverage.")
        history["covered_slugs"] = []
        save_history(history)
        return select_daily_ides(count=count)

    selected = candidate_list[:count]
    return selected


def generate_daily_content_package(target_date: Optional[str] = None):
    """Generates full daily content package (3 AMP posts + 3 Video specs)."""
    if not target_date:
        target_date = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d")

    day_dir = os.path.join("content", target_date)
    os.makedirs(day_dir, exist_ok=True)

    history = load_history()
    covered_slugs = set(history.get("covered_slugs", []))

    selected_ides = select_daily_ides(count=3)
    print(f"--- IDE Guide Daily Content Generation ({target_date}) ---")
    print(f"Selected IDEs for today: {', '.join(selected_ides)}")

    daily_summary = []

    for idx, ide_name in enumerate(selected_ides, 1):
        ide_data = fetch_or_build_ide_data(ide_name)
        slug = sanitize_slug(ide_data["name"])

        # Write AMP HTML post
        amp_html = generate_amp_html_blogpost(ide_data)
        amp_file = os.path.join(day_dir, f"post_{idx}_{slug}_amp.html")
        with open(amp_file, "w", encoding="utf-8") as f:
            f.write(amp_html)

        # Write Google Flow Video spec JSON
        flow_spec = generate_google_flow_video_spec(ide_data)
        flow_json_file = os.path.join(day_dir, f"video_{idx}_{slug}_flow_spec.json")
        with open(flow_json_file, "w", encoding="utf-8") as f:
            json.dump(flow_spec, f, indent=2)

        # Write Google Flow Video spec Markdown
        flow_md_file = os.path.join(day_dir, f"video_{idx}_{slug}_flow_spec.md")
        with open(flow_md_file, "w", encoding="utf-8") as f:
            f.write(f"# Google Flow Video Spec #{idx}: {ide_data['name']}\n\n")
            f.write(f"**Target Date:** {target_date}\n")
            f.write(f"**Video Title:** {flow_spec['video_title']}\n")
            f.write(f"**Pricing Tier:** {ide_data['pricing_type']}\n\n")
            f.write("--- \n\n")
            for scene in flow_spec["prompts_and_scenes"]:
                f.write(f"### Scene {scene['scene_number']}: {scene['title']} ({scene['timecode']})\n")
                f.write(f"- **Google Flow Prompt:** `{scene['flow_prompt']}`\n")
                f.write(f"- **Voiceover Script:** \"{scene['voiceover_script']}\"\n")
                f.write(f"- **Camera:** {scene['camera']}\n")
                f.write(f"- **Lighting:** {scene['lighting']}\n\n")
            f.write("---\n\n")
            f.write(f"**Disclaimer:**\n>{DISCLAIMER_TEXT}\n")

        covered_slugs.add(slug)
        daily_summary.append({
            "slot": idx,
            "ide_name": ide_data["name"],
            "slug": slug,
            "amp_html": amp_file,
            "video_spec_json": flow_json_file,
            "video_spec_md": flow_md_file
        })

    history["covered_slugs"] = list(covered_slugs)
    if "daily_logs" not in history:
        history["daily_logs"] = {}
    history["daily_logs"][target_date] = daily_summary
    save_history(history)

    print(f"[SUCCESS] Successfully generated daily package in '{day_dir}'.")
    return day_dir, daily_summary


if __name__ == "__main__":
    generate_daily_content_package()
