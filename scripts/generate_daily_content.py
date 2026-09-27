#!/usr/bin/env python3
"""
Daily Content Generator for IDE Guide.
Generates 3 daily packages (3 AMP blog posts and 3 Google Flow video specs)
for different IDEs, tracks history in content/history.json, and outputs to content/YYYY-MM-DD/
"""

import os
import sys
import json
import urllib.request
import urllib.error
from datetime import datetime, timezone
from pathlib import Path

from scripts.ide_guide_agent_skill import (
    get_ide_info,
    generate_amp_blog_post,
    generate_google_flow_video_spec,
    DEFAULT_IDE_DATABASE,
)
from scripts.amp_validator import validate_amp_html

HISTORY_FILE = Path("content/history.json")

# Dynamic list of potential IDE topics / search queries if history is exhausted
POPULAR_IDE_TOPICS = [
    "visual studio code",
    "cursor",
    "zed",
    "pycharm",
    "neovim",
    "intellij idea",
    "webstorm",
    "clion",
    "sublime text",
    "emacs",
    "eclipse",
    "fleet",
    "lapce",
    "helix",
    "xcode",
    "android studio",
    "nova",
    "codeblocks",
    "qt creator",
    "rad studio",
]


def load_history() -> dict:
    if HISTORY_FILE.exists():
        try:
            return json.loads(HISTORY_FILE.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            pass
    return {"covered_ides": [], "daily_runs": []}


def save_history(history: dict) -> None:
    HISTORY_FILE.parent.mkdir(parents=True, exist_ok=True)
    HISTORY_FILE.write_text(json.dumps(history, indent=2), encoding="utf-8")


def fetch_github_ide_candidates() -> list[dict]:
    """
    Attempts to discover trending open source IDEs/code editors on GitHub using GitHub API.
    """
    url = "https://api.github.com/search/repositories?q=topic:ide+topic:editor&sort=stars&order=desc&per_page=15"
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "IDE-Guide-Generator/1.0"}
    )
    candidates = []
    try:
        with urllib.request.urlopen(req, timeout=5) as response:
            data = json.loads(response.read().decode("utf-8"))
            for item in data.get("items", []):
                candidates.append({
                    "name": item["name"].replace("-", " ").replace("_", " ").title(),
                    "repo_url": item["html_url"],
                    "description": item.get("description", ""),
                    "category": item.get("language", "Software Development")
                })
    except Exception as e:
        print(f"Notice: GitHub Search API fallback engaged ({e})")
    return candidates


def select_daily_ides(count: int = 3) -> list[dict]:
    history = load_history()
    covered = set(item.lower() for item in history.get("covered_ides", []))

    selected = []

    # First, pick from default database if not covered
    for key, info in DEFAULT_IDE_DATABASE.items():
        if key.lower() not in covered and info["name"].lower() not in covered:
            selected.append({"ide_name": info["name"]})
            covered.add(key.lower())
            covered.add(info["name"].lower())
            if len(selected) >= count:
                break

    # If still need more, pick from POPULAR_IDE_TOPICS list
    if len(selected) < count:
        for topic in POPULAR_IDE_TOPICS:
            if topic.lower() not in covered:
                selected.append({"ide_name": topic.title()})
                covered.add(topic.lower())
                if len(selected) >= count:
                    break

    # If still need more, pick from GitHub candidates
    if len(selected) < count:
        github_candidates = fetch_github_ide_candidates()
        for cand in github_candidates:
            if cand["name"].lower() not in covered:
                selected.append({
                    "ide_name": cand["name"],
                    "repo_url": cand["repo_url"],
                    "category": cand["category"]
                })
                covered.add(cand["name"].lower())
                if len(selected) >= count:
                    break

    # Fallback if all lists were exhausted (rotate topics)
    if len(selected) < count:
        for topic in POPULAR_IDE_TOPICS:
            selected.append({"ide_name": f"{topic.title()} Update"})
            if len(selected) >= count:
                break

    return selected[:count]


def run_daily_generation():
    today_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    output_dir = Path(f"content/{today_str}")
    output_dir.mkdir(parents=True, exist_ok=True)

    history = load_history()
    selected_targets = select_daily_ides(count=3)

    daily_summary = {
        "date": today_str,
        "items": []
    }

    for idx, target in enumerate(selected_targets, 1):
        ide_name = target.get("ide_name")
        repo_url = target.get("repo_url")
        category = target.get("category")

        info = get_ide_info(ide_name=ide_name, repo_url=repo_url, category=category)
        amp_html = generate_amp_blog_post(info)
        video_spec = generate_google_flow_video_spec(info)

        # Validate AMP HTML
        is_valid, errors = validate_amp_html(amp_html)
        if not is_valid:
            print(f"Warning: AMP validation warnings for {info['name']}: {errors}")

        slug = info["name"].lower().replace(" ", "_").replace("-", "_")
        blog_filename = f"post_{idx}_{slug}_amp.html"
        video_filename = f"video_{idx}_{slug}_spec.json"

        blog_path = output_dir / blog_filename
        video_path = output_dir / video_filename

        blog_path.write_text(amp_html, encoding="utf-8")
        video_path.write_text(json.dumps(video_spec, indent=2), encoding="utf-8")

        print(f"✅ Generated Item {idx}: {info['name']}")
        print(f"   Blog: {blog_path}")
        print(f"   Video Spec: {video_path}")

        daily_summary["items"].append({
            "ide_name": info["name"],
            "blog_file": str(blog_path),
            "video_file": str(video_path)
        })

        if info["name"] not in history["covered_ides"]:
            history["covered_ides"].append(info["name"])

    history["daily_runs"].append(daily_summary)
    save_history(history)

    print(f"\n🎉 Daily content generation complete for {today_str}! Output saved in content/{today_str}/")


if __name__ == "__main__":
    run_daily_generation()
