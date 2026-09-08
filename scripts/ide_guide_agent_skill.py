#!/usr/bin/env python3
"""
IDE Guide Agentic CLI Skill Tool
CLI skill tool that allows AI agents or humans to on-demand generate Blogger AMP HTML posts and YouTube Google Flow video specs for a given IDE name or repository URL.
"""

import argparse
import datetime
import json
import os
import re
import sys
import urllib.request
import urllib.parse

from generate_daily_content import (
    DISCLAIMER,
    generate_amp_html_post,
    generate_google_flow_video_spec,
    CURATED_IDES
)

def fetch_github_repo_info(repo_url: str) -> dict:
    """Extract owner/repo and fetch metadata from GitHub API."""
    match = re.search(r"github\.com/([^/]+)/([^/]+)", repo_url)
    if not match:
        raise ValueError(f"Invalid GitHub repository URL: {repo_url}")
    owner, repo = match.group(1), match.group(2).rstrip(".git")
    api_url = f"https://api.github.com/repos/{owner}/{repo}"

    req = urllib.request.Request(api_url, headers={"User-Agent": "IDEGuide-Agent-Skill"})
    try:
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return {
                "name": data.get("name", repo).capitalize(),
                "key": repo.lower().replace("-", "_").replace(".", "_"),
                "tagline": data.get("description") or f"Open-source code editor repository {owner}/{repo}",
                "license": data.get("license", {}).get("name") if data.get("license") else "Open Source",
                "pricing": "100% Free & Open Source",
                "pros": [
                    f"Over {data.get('stargazers_count', 0)} stars on GitHub",
                    "Fully customizable open-source codebase",
                    f"Written primarily in {data.get('language') or 'modern language'}"
                ],
                "cons": [
                    "Community-driven documentation and support",
                    "Requires build or installation step"
                ],
                "ideal_for": f"Developers interested in {data.get('language') or 'open-source'} software development",
                "description": data.get("description") or f"{repo} is an open source software project.",
                "html_url": data.get("html_url")
            }
    except Exception as e:
        # Fallback dictionary if API fails or offline
        key = repo.lower().replace("-", "_").replace(".", "_")
        return {
            "name": repo.capitalize(),
            "key": key,
            "tagline": f"Open-source repository for {repo}",
            "license": "Open Source",
            "pricing": "100% Free & Open Source",
            "pros": ["Open source flexibility", "Developer community support"],
            "cons": ["Self-managed setup"],
            "ideal_for": "Developers seeking open source IDE tools",
            "description": f"{repo} custom editor or development environment tool."
        }

def lookup_or_build_ide_data(ide_name: str) -> dict:
    for item in CURATED_IDES:
        if item["name"].lower() == ide_name.lower() or item["key"] == ide_name.lower().replace(" ", "_"):
            return item

    # Generic structured data if not in curated list
    key = ide_name.lower().replace(" ", "_").replace("-", "_")
    return {
        "name": ide_name,
        "key": key,
        "tagline": f"Modern developer environment and code editor: {ide_name}",
        "license": "Freemium / Open Source / Commercial",
        "pricing": "Free / Subscription available",
        "pros": [
            f"Tailored developer workflows in {ide_name}",
            "Extensible architecture and configuration options",
            "Modern user interface"
        ],
        "cons": [
            "Learning curve for specialized features",
            "System resource consumption varies by workload"
        ],
        "ideal_for": "Software engineers and technical developers",
        "description": f"{ide_name} is a feature-packed software development tool designed to streamline coding and debugging."
    }

def main():
    parser = argparse.ArgumentParser(description="IDE Guide Agentic Skill Tool for generating AMP posts and Google Flow video specs.")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--ide", help="Name of the IDE or Code Editor (e.g., 'Zed', 'Cursor', 'VS Code')")
    group.add_argument("--repo", help="GitHub repository URL (e.g., 'https://github.com/zed-industries/zed')")

    parser.add_argument("--output-dir", help="Directory where generated content will be saved", default=None)

    args = parser.parse_args()

    if args.repo:
        ide_data = fetch_github_repo_info(args.repo)
    else:
        ide_data = lookup_or_build_ide_data(args.ide)

    date_str = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d")

    amp_post = generate_amp_html_post(ide_data, date_str)
    video_spec = generate_google_flow_video_spec(ide_data, date_str, index=1)

    output_dir = args.output_dir
    if not output_dir:
        root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        output_dir = os.path.join(root_dir, "content", "agent_generated", ide_data["key"])

    os.makedirs(output_dir, exist_ok=True)

    post_path = os.path.join(output_dir, f"{ide_data['key']}_amp_post.html")
    video_path = os.path.join(output_dir, f"{ide_data['key']}_google_flow_spec.json")

    with open(post_path, "w", encoding="utf-8") as f:
        f.write(amp_post)
    with open(video_path, "w", encoding="utf-8") as f:
        json.dump(video_spec, f, indent=2)

    print(f"Agent Skill Execution Complete!")
    print(f" IDE Target: {ide_data['name']}")
    print(f" AMP Post: {post_path}")
    print(f" Video Spec: {video_path}")

if __name__ == "__main__":
    main()
