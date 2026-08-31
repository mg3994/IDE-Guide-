#!/usr/bin/env python3
"""
IDE Guide Agentic CLI Skill Tool (scripts/ide_guide_agent_skill.py)

On-demand content generation skill for IDE Guide (https://ideguide.blogspot.com/ & https://www.youtube.com/@IDEguide).
Allows agents or developers to generate AMP-compliant Blogger posts and Google Flow video specs
for any specific IDE or GitHub editor repository.

Usage:
  python3 scripts/ide_guide_agent_skill.py --ide "Visual Studio Code"
  python3 scripts/ide_guide_agent_skill.py --repo "https://github.com/zed-industries/zed"
  python3 scripts/ide_guide_agent_skill.py --ide "Fleet" --out-dir "./custom_output"
"""

import argparse
import json
import os
import sys
import datetime
import urllib.request
import urllib.parse

# Import generators from generate_daily_content
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from generate_daily_content import generate_amp_html, generate_google_flow_video_spec, CURATED_IDE_CATALOG


def fetch_github_repo_info(repo_url: str) -> dict:
    """Extract owner/repo from URL and fetch repo info via GitHub API."""
    parsed = urllib.parse.urlparse(repo_url)
    path_parts = [p for p in parsed.path.strip("/").split("/") if p]
    if len(path_parts) < 2:
        raise ValueError(f"Invalid GitHub repository URL: {repo_url}")

    owner, repo = path_parts[0], path_parts[1]
    api_url = f"https://api.github.com/repos/{owner}/{repo}"
    req = urllib.request.Request(api_url, headers={"User-Agent": "IDE-Guide-Skill/1.0"})

    try:
        with urllib.request.urlopen(req, timeout=5) as resp:
            if resp.status == 200:
                data = json.loads(resp.read().decode('utf-8'))
                name = data.get("name", repo).capitalize()
                desc = data.get("description", "Modern code editor and development tool.") or "Modern code editor."
                return {
                    "name": name,
                    "slug": repo.lower(),
                    "category": f"Open Source Editor ({data.get('language', 'Polyglot')})",
                    "pricing_tier": "Free / Open Source",
                    "pricing_details": f"Open-source software hosted at https://github.com/{owner}/{repo}",
                    "pros": [
                        f"GitHub Stargazers: {data.get('stargazers_count', 0):,}",
                        f"Primary language: {data.get('language', 'Community Driven')}",
                        "Transparent development and community contributions"
                    ],
                    "cons": [
                        "May require manual configuration or building from source for latest edge features",
                        "Ecosystem depth depends on active community plugin developers"
                    ],
                    "best_for": desc,
                    "verdict": f"{name} provides an adaptable open platform for developer productivity."
                }
    except Exception as e:
        print(f"Notice: Failed to fetch GitHub API ({e}). Generating fallback specs for {repo}.")

    # Fallback structure if network request fails
    return {
        "name": repo.capitalize(),
        "slug": repo.lower(),
        "category": "Code Editor / IDE Environment",
        "pricing_tier": "Free / Open Source",
        "pricing_details": f"Repository URL: {repo_url}",
        "pros": [
            "Open source codebase",
            "Customizable features and settings"
        ],
        "cons": [
            "Requires user testing for platform stability"
        ],
        "best_for": f"Developers looking for modern workflows in {repo.capitalize()}.",
        "verdict": f"{repo.capitalize()} is a promising editor choice."
    }


def find_or_build_ide_spec(ide_name: str = None, repo_url: str = None) -> dict:
    """Locate matching IDE from catalog or dynamically build specification."""
    if repo_url:
        return fetch_github_repo_info(repo_url)

    if ide_name:
        normalized = ide_name.lower().replace(" ", "").replace("-", "")
        for cat in CURATED_IDE_CATALOG:
            if cat["name"].lower().replace(" ", "").replace("-", "") == normalized or cat["slug"].replace("-", "") == normalized:
                return cat

        # Generate custom specification for uncatalogued IDE name
        slug = ide_name.lower().replace(" ", "-")
        return {
            "name": ide_name,
            "slug": slug,
            "category": "Specialized Development Environment",
            "pricing_tier": "Freemium / Open Source Options",
            "pricing_details": f"Check official distribution channels for {ide_name} licensing.",
            "pros": [
                f"Tailored feature set specifically built for {ide_name} workflows",
                "Dedicated developer productivity enhancements",
                "Integrates with modern debugging and language tools"
            ],
            "cons": [
                "Ecosystem size may vary compared to general purpose editors",
                "May require adaptation period for keyboard shortcuts"
            ],
            "best_for": f"Software engineers specializing in workflows optimized by {ide_name}.",
            "verdict": f"{ide_name} offers focused capabilities worth evaluating for your stack."
        }

    raise ValueError("Must specify either --ide or --repo")


def run_skill(ide_name: str = None, repo_url: str = None, out_dir: str = None, is_short: bool = False) -> str:
    """Execute Agentic CLI skill generation."""
    ide_spec = find_or_build_ide_spec(ide_name, repo_url)
    date_str = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d")

    if not out_dir:
        out_dir = os.path.join("content", "skill_output", f"{date_str}_{ide_spec['slug']}")

    os.makedirs(out_dir, exist_ok=True)

    # 1. AMP HTML Post
    amp_content = generate_amp_html(ide_spec, date_str)
    amp_path = os.path.join(out_dir, "blog_post_amp.html")
    with open(amp_path, "w", encoding="utf-8") as f:
        f.write(amp_content)

    # 2. Google Flow Spec
    flow_spec = generate_google_flow_video_spec(ide_spec, date_str, is_short=is_short)
    spec_path = os.path.join(out_dir, "google_flow_video_spec.json")
    with open(spec_path, "w", encoding="utf-8") as f:
        json.dump(flow_spec, f, indent=2)

    print(f"IDE Guide Agentic Skill: Output generated successfully at {out_dir}")
    print(f" - AMP HTML Post: {amp_path}")
    print(f" - Google Flow Video Spec: {spec_path}")
    return out_dir


def main():
    parser = argparse.ArgumentParser(description="IDE Guide Agentic Skill Tool")
    parser.add_argument("--ide", type=str, help="Name of the IDE/editor (e.g., 'Visual Studio Code', 'Fleet')")
    parser.add_argument("--repo", type=str, help="GitHub repository URL for the editor")
    parser.add_argument("--out-dir", type=str, help="Target output directory for generated files")
    parser.add_argument("--shorts", action="store_true", help="Format Google Flow video spec for YouTube Shorts (9:16)")

    args = parser.parse_args()

    if not args.ide and not args.repo:
        parser.print_help()
        sys.exit(1)

    run_skill(ide_name=args.ide, repo_url=args.repo, out_dir=args.out_dir, is_short=args.shorts)


if __name__ == "__main__":
    main()
