#!/usr/bin/env python3
"""
IDE Guide Agentic Skill CLI Tool

Allows users or AI agents to generate custom AMP HTML blog posts and
Google Flow video specs on demand for any IDE name, custom parameters, or GitHub repository.

Usage:
  python3 scripts/ide_guide_agent_skill.py --name "Nova Editor" --tagline "Fast Mac IDE" --pricing "Commercial ($99)" --pros "Fast, Native UI, Great Extensions" --cons "macOS only"
  python3 scripts/ide_guide_agent_skill.py --github "https://github.com/vscodium/vscodium"
"""

import os
import sys
import json
import argparse
import urllib.request
from generate_daily_content import (
    generate_amp_html,
    generate_google_flow_spec,
    generate_google_flow_markdown_spec,
    DISCLAIMER_TEXT
)


def fetch_github_repo_info(repo_url: str) -> dict:
    """Extracts owner/repo from GitHub URL and fetches repository details via GitHub API."""
    clean_url = repo_url.rstrip("/")
    parts = clean_url.split("/")
    if len(parts) < 2:
        raise ValueError("Invalid GitHub URL format. Expected https://github.com/owner/repo")

    owner, repo = parts[-2], parts[-1]
    api_url = f"https://api.github.com/repos/{owner}/{repo}"

    req = urllib.request.Request(
        api_url,
        headers={"User-Agent": "IDE-Guide-Agent-Skill/1.0"}
    )

    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            if response.status == 200:
                data = json.loads(response.read().decode("utf-8"))
                description = data.get("description") or f"Open-source software repository {owner}/{repo}"
                license_name = data.get("license", {}).get("name") if data.get("license") else "Open Source"
                stars = data.get("stargazers_count", 0)

                return {
                    "id": repo.lower(),
                    "name": data.get("name", repo).capitalize(),
                    "tagline": description,
                    "developer": data.get("owner", {}).get("login", owner),
                    "pricing_type": "Free / Open Source",
                    "pricing_details": f"Open Source ({license_name}). {stars:,} GitHub stars.",
                    "pros": [
                        f"Transparent open-source codebase on GitHub ({stars:,} stars)",
                        f"Licensed under {license_name}",
                        "Active community contributions and open issue tracking",
                        "Cross-platform extensible architectural design"
                    ],
                    "cons": [
                        "Community-driven support models rather than dedicated corporate SLA",
                        "May require self-compilation or manual extension installation",
                        "Rapid updates may introduce experimental configuration options"
                    ],
                    "target_audience": "Developers who prioritize open-source transparency and community-driven tooling.",
                    "hero_image": "https://images.unsplash.com/photo-1618401471353-b98afee0b2eb?w=1200&auto=format&fit=crop&q=80",
                    "category": "Open-Source Development Environment"
                }
    except Exception as e:
        print(f"Warning: Could not fetch GitHub API for {repo_url}: {e}. Falling back to default data structure.")

    # Fallback if API fails or rate limited
    return {
        "id": repo.lower(),
        "name": repo.capitalize(),
        "tagline": f"Open-source development repository {owner}/{repo}",
        "developer": owner,
        "pricing_type": "Free / Open Source",
        "pricing_details": "Open Source repository on GitHub.",
        "pros": [
            "Open source transparency",
            "Extensible codebase architecture",
            "Active developer community"
        ],
        "cons": [
            "Community-driven issue response time",
            "Requires manual configuration for custom setups"
        ],
        "target_audience": "Developers and open-source software enthusiasts.",
        "hero_image": "https://images.unsplash.com/photo-1555066931-4365d14bab8c?w=1200&auto=format&fit=crop&q=80",
        "category": "Code Editor Repository"
    }


def create_agentic_content(ide_data: dict, output_dir: str = "content/custom"):
    """Generates AMP HTML and Google Flow video specs for a given IDE dictionary."""
    os.makedirs(output_dir, exist_ok=True)
    ide_id = ide_data.get("id", "custom_ide").lower().replace(" ", "_")

    # 1. AMP HTML Blog Post
    amp_html = generate_amp_html(ide_data)
    amp_file = os.path.join(output_dir, f"blog_post_{ide_id}.html")
    with open(amp_file, "w", encoding="utf-8") as f:
        f.write(amp_html)

    # 2. Google Flow Spec (JSON & MD)
    spec_dict = generate_google_flow_spec(ide_data)
    json_file = os.path.join(output_dir, f"video_spec_{ide_id}.json")
    with open(json_file, "w", encoding="utf-8") as f:
        json.dump(spec_dict, f, indent=2)

    md_spec = generate_google_flow_markdown_spec(spec_dict)
    md_file = os.path.join(output_dir, f"video_spec_{ide_id}.md")
    with open(md_file, "w", encoding="utf-8") as f:
        f.write(md_spec)

    print(f"[IDE Guide Agent Skill] Package created successfully in {output_dir}:")
    print(f" - AMP HTML Post: {amp_file}")
    print(f" - Video Spec JSON: {json_file}")
    print(f" - Video Spec Markdown: {md_file}")
    return [amp_file, json_file, md_file]


def main():
    parser = argparse.ArgumentParser(description="IDE Guide Agentic Content Skill")
    parser.add_argument("--name", type=str, help="Name of the IDE/Code Editor")
    parser.add_argument("--tagline", type=str, help="Short description or tagline")
    parser.add_argument("--developer", type=str, default="Independent Developer / Community", help="Developer or Vendor name")
    parser.add_argument("--pricing", type=str, default="Freemium / Open Source", help="Pricing model summary")
    parser.add_argument("--pros", type=str, help="Comma-separated pros")
    parser.add_argument("--cons", type=str, help="Comma-separated cons")
    parser.add_argument("--audience", type=str, default="Software Engineers and Web Developers", help="Target audience")
    parser.add_argument("--github", type=str, help="GitHub repository URL (e.g., https://github.com/vscodium/vscodium)")
    parser.add_argument("--output", type=str, default="content/custom", help="Output directory")

    args = parser.parse_args()

    if args.github:
        print(f"Fetching repository details from GitHub: {args.github}...")
        ide_data = fetch_github_repo_info(args.github)
    elif args.name:
        pros_list = [p.strip() for p in args.pros.split(",")] if args.pros else [
            "High performance development workflows",
            "Extensible environment configuration",
            "Comprehensive developer toolset"
        ]
        cons_list = [c.strip() for c in args.cons.split(",")] if args.cons else [
            "Resource footprint depends on active plugins",
            "Learning curve for advanced keybindings"
        ]
        ide_data = {
            "id": args.name.lower().replace(" ", "_"),
            "name": args.name,
            "tagline": args.tagline or f"Next-generation development environment for {args.name}.",
            "developer": args.developer,
            "pricing_type": args.pricing,
            "pricing_details": args.pricing,
            "pros": pros_list,
            "cons": cons_list,
            "target_audience": args.audience,
            "hero_image": "https://images.unsplash.com/photo-1555066931-4365d14bab8c?w=1200&auto=format&fit=crop&q=80",
            "category": "Code Editor"
        }
    else:
        print("Error: Must provide either --name or --github argument.")
        sys.exit(1)

    create_agentic_content(ide_data, output_dir=args.output)


if __name__ == "__main__":
    main()
