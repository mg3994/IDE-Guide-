#!/usr/bin/env python3
"""
Daily Content Generator for IDE Guide
--------------------------------------
Generates 3 daily AMP HTML blog posts (for Blogger https://ideguide.blogspot.com/)
and 3 daily Google Flow video specifications (for YouTube @IDEguide).

Tracks covered IDEs in content/history.json to ensure new editors are featured daily.

Outputs:
  content/YYYY-MM-DD/
    ├── blogpost_1_<ide_name>.html
    ├── blogpost_2_<ide_name>.html
    ├── blogpost_3_<ide_name>.html
    ├── video_spec_1_<ide_name>.json
    ├── video_spec_2_<ide_name>.json
    └── video_spec_3_<ide_name>.json
"""

import datetime
import json
import os
import re
import sys
import urllib.request

# Add parent directory to sys.path to import agent skill module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from scripts.ide_guide_agent_skill import (
    KNOWN_IDES_DATABASE,
    generate_amp_html,
    generate_google_flow_video_spec,
    resolve_ide_data
)

HISTORY_FILE = "content/history.json"


def load_history():
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {"covered_ides": [], "daily_runs": []}


def save_history(history):
    os.makedirs(os.path.dirname(HISTORY_FILE), exist_ok=True)
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=2)


def fetch_github_trending_editors():
    """Attempt to discover code editor repositories dynamically via GitHub API."""
    queries = ["topic:text-editor", "topic:code-editor", "topic:ide"]
    discovered = []
    for q in queries:
        url = f"https://api.github.com/search/repositories?q={q}+stars:>2000&sort=stars&order=desc&per_page=10"
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "IDEGuide-Generator"})
            with urllib.request.urlopen(req, timeout=5) as resp:
                if resp.status == 200:
                    data = json.loads(resp.read().decode("utf-8"))
                    for item in data.get("items", []):
                        discovered.append({
                            "name": item["name"].capitalize(),
                            "repo_url": item["html_url"],
                            "description": item.get("description", ""),
                            "stars": item.get("stargazers_count", 0),
                            "language": item.get("language", "Code")
                        })
        except Exception as e:
            sys.stderr.write(f"GitHub search query '{q}' skipped: {e}\n")
    return discovered


def select_daily_ides(history, target_count=3):
    covered = set(history.get("covered_ides", []))
    selected = []

    # 1. First pick from KNOWN_IDES_DATABASE if not yet covered
    for key, data in KNOWN_IDES_DATABASE.items():
        if data["name"] not in covered:
            selected.append(data)
            covered.add(data["name"])
            if len(selected) == target_count:
                return selected

    # 2. Try fetching from GitHub API
    gh_editors = fetch_github_trending_editors()
    for item in gh_editors:
        if item["name"] not in covered:
            ide_info = resolve_ide_data(ide_query=item["name"], repo_url=item["repo_url"])
            selected.append(ide_info)
            covered.add(ide_info["name"])
            if len(selected) == target_count:
                return selected

    # 3. Fallback list if all known entries were exhausted
    fallback_pool = [
        "Lapce", "Sublime Text", "Helix Editor", "JetBrains PyCharm", "Emacs",
        "Nova Editor", "Geany", "Micro Text Editor", "VSCodium", "Kate Editor"
    ]
    for name in fallback_pool:
        if name not in covered:
            ide_info = resolve_ide_data(ide_query=name)
            selected.append(ide_info)
            covered.add(name)
            if len(selected) == target_count:
                return selected

    # 4. If still under target, recycle oldest items
    if len(selected) < target_count:
        for key, data in KNOWN_IDES_DATABASE.items():
            selected.append(data)
            if len(selected) == target_count:
                break

    return selected


def main():
    today_str = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d")
    output_dir = os.path.join("content", today_str)
    os.makedirs(output_dir, exist_ok=True)

    history = load_history()
    selected_ides = select_daily_ides(history, target_count=3)

    run_record = {
        "date": today_str,
        "timestamp_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "generated_items": []
    }

    for idx, ide_info in enumerate(selected_ides, 1):
        slug = re.sub(r'[^a-z0-9]+', '_', ide_info['name'].lower()).strip('_')

        # Save AMP HTML blog post
        amp_html = generate_amp_html(ide_info)
        blog_filename = f"blogpost_{idx}_{slug}.html"
        blog_path = os.path.join(output_dir, blog_filename)
        with open(blog_path, "w", encoding="utf-8") as f:
            f.write(amp_html)

        # Save Google Flow video spec
        flow_spec = generate_google_flow_video_spec(ide_info)
        spec_filename = f"video_spec_{idx}_{slug}.json"
        spec_path = os.path.join(output_dir, spec_filename)
        with open(spec_path, "w", encoding="utf-8") as f:
            json.dump(flow_spec, f, indent=2)

        if ide_info["name"] not in history["covered_ides"]:
            history["covered_ides"].append(ide_info["name"])

        run_record["generated_items"].append({
            "index": idx,
            "ide_name": ide_info["name"],
            "blog_path": blog_path,
            "spec_path": spec_path
        })

    history["daily_runs"].append(run_record)
    save_history(history)

    print(f"🎉 Successfully generated daily content package for {today_str} in '{output_dir}':")
    for item in run_record["generated_items"]:
        print(f"   [{item['index']}] {item['ide_name']}")
        print(f"       - Blog Post:  {item['blog_path']}")
        print(f"       - Video Spec: {item['spec_path']}")


if __name__ == "__main__":
    main()
