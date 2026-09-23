#!/usr/bin/env python3
"""
Daily Content Generation Engine for IDE Guide.
Generates 3 AMP HTML blog posts & 3 Google Flow video specifications every day.
"""

import datetime
import json
import os
import sys
import re
from urllib.request import Request, urlopen
from urllib.error import URLError

# Ensure repo root is on python path for importing scripts
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from scripts.ide_guide_agent_skill import (
    DEFAULT_IDE_KNOWLEDGE,
    run_agent_skill,
    DISCLAIMER_TEXT
)

HISTORY_FILE = "content/history.json"

# Candidate IDEs pool to ensure endless fresh daily content
POPULAR_IDES = [
    {"name": "Cursor", "price_model": "Freemium"},
    {"name": "Zed", "price_model": "Free / Open Source"},
    {"name": "Visual Studio Code", "price_model": "Free / Open Source"},
    {"name": "Neovim", "price_model": "Free / Open Source"},
    {"name": "JetBrains Fleet", "price_model": "Freemium"},
    {"name": "IntelliJ IDEA", "price_model": "Freemium"},
    {"name": "PyCharm", "price_model": "Freemium"},
    {"name": "Sublime Text", "price_model": "Paid / Free Evaluation"},
    {"name": "Helix", "price_model": "Free / Open Source"},
    {"name": "Lapce", "price_model": "Free / Open Source"},
    {"name": "Emacs", "price_model": "Free / Open Source"},
    {"name": "Android Studio", "price_model": "Free"},
    {"name": "Xcode", "price_model": "Free"},
    {"name": "Eclipse", "price_model": "Free / Open Source"},
    {"name": "Code::Blocks", "price_model": "Free / Open Source"}
]


def load_history() -> dict:
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {"covered_ides": [], "last_updated": None}


def save_history(history: dict):
    os.makedirs(os.path.dirname(HISTORY_FILE), exist_ok=True)
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=2)


def fetch_github_trending_editors() -> list:
    """Discovers code editor repos on GitHub via public API if available."""
    url = "https://api.github.com/search/repositories?q=topic:code-editor+topic:ide&sort=stars&order=desc&per_page=10"
    headers = {"User-Agent": "IDEGuide-Generator"}
    try:
        req = Request(url, headers=headers)
        with urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            items = data.get("items", [])
            discovered = []
            for item in items:
                discovered.append({
                    "name": item["name"].replace("-", " ").replace("_", " ").title(),
                    "price_model": "Free / Open Source"
                })
            return discovered
    except Exception:
        return []


def select_daily_ides(count: int = 3) -> list:
    history = load_history()
    covered = set(history.get("covered_ides", []))

    candidates = POPULAR_IDES.copy()
    github_editors = fetch_github_trending_editors()
    for g_editor in github_editors:
        if not any(c["name"].lower() == g_editor["name"].lower() for c in candidates):
            candidates.append(g_editor)

    selected = []
    for cand in candidates:
        if cand["name"].lower() not in covered:
            selected.append(cand)
            if len(selected) == count:
                break

    # If all candidate IDEs have been covered, reset history cycle
    if len(selected) < count:
        history["covered_ides"] = []
        save_history(history)
        covered = set()
        for cand in candidates:
            if cand["name"].lower() not in covered and not any(s["name"].lower() == cand["name"].lower() for s in selected):
                selected.append(cand)
                if len(selected) == count:
                    break

    return selected


def generate_daily_batch():
    today_str = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d")
    daily_dir = os.path.join("content", today_str)

    selected_ides = select_daily_ides(3)
    history = load_history()

    print(f"Generating 3 daily content packages for date: {today_str}")

    for idx, ide_item in enumerate(selected_ides, start=1):
        slug = re.sub(r"[^a-z0-9]+", "-", ide_item["name"].lower()).strip("-")
        package_dir = os.path.join(daily_dir, f"{idx:02d}_{slug}")

        run_agent_skill(
            ide_name=ide_item["name"],
            price_model=ide_item["price_model"],
            output_dir=package_dir
        )

        history["covered_ides"].append(ide_item["name"].lower())

    history["last_updated"] = datetime.datetime.now(datetime.timezone.utc).isoformat()
    save_history(history)
    print(f"Successfully completed daily generation for {today_str}.")


if __name__ == "__main__":
    generate_daily_batch()
