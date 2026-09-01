#!/usr/bin/env python3
"""
IDE Guide Agentic CLI Skill Tool.
Allows on-demand generation of AMP HTML blog posts and Google Flow video specs
for custom IDE names or GitHub repository URLs.

Usage:
  python3 scripts/ide_guide_agent_skill.py --ide "Zed" --pricing "Free / Open Source" --out-dir ./custom_output
  python3 scripts/ide_guide_agent_skill.py --repo "https://github.com/lapce/lapce"
"""

import os
import sys
import argparse
import json
import urllib.request
import urllib.parse
from generate_daily_content import generate_amp_blog_post, generate_google_flow_video_spec, sanitize_slug

def fetch_github_repo_info(repo_url):
    # Extract owner and repo name from URL (e.g. https://github.com/lapce/lapce -> lapce/lapce)
    parts = repo_url.rstrip('/').split('/')
    if len(parts) < 2:
        raise ValueError("Invalid GitHub repository URL format")
    owner, repo = parts[-2], parts[-1]

    api_url = f"https://api.github.com/repos/{owner}/{repo}"
    req = urllib.request.Request(api_url, headers={'User-Agent': 'IDE-Guide-Agent-Skill'})

    with urllib.request.urlopen(req, timeout=10) as resp:
        data = json.loads(resp.read().decode('utf-8'))

    name = data.get('name', repo).capitalize()
    description = data.get('description') or f"A modern code editor / IDE repository ({owner}/{repo})."
    stargazers = data.get('stargazers_count', 0)
    language = data.get('language') or 'Multi-language'
    license_info = data.get('license')
    license_name = license_info.get('name') if license_info else 'Open Source License'

    return {
        "name": name,
        "category": f"Open Source Code Editor / IDE ({language})",
        "pricing": f"Free & Open Source ({license_name})",
        "cost_model": "100% Free",
        "pros": [
            f"Open source project with {stargazers:,} stars on GitHub",
            f"Built primarily with {language}",
            "Community driven development and extension ecosystem"
        ],
        "cons": [
            "Continuous rapid development; may experience active feature additions",
            "Extension catalog continuously expanding"
        ],
        "best_for": f"Developers looking for modern, lightweight open-source software tools in {language}",
        "flow_scene": f"Cinematic dark workspace highlighting {name} repository interface and active buffer.",
        "repo_url": repo_url
    }

def main():
    parser = argparse.ArgumentParser(description="IDE Guide Agentic CLI Tool for generating AMP blog posts and Google Flow video specs.")
    parser.add_argument("--ide", type=str, help="Name of the IDE or Code Editor")
    parser.add_argument("--repo", type=str, help="GitHub Repository URL for the IDE/Editor")
    parser.add_argument("--category", type=str, default="Code Editor / IDE", help="Category description")
    parser.add_argument("--pricing", type=str, default="Free / Open Source", help="Pricing breakdown")
    parser.add_argument("--cost-model", type=str, default="Free / Freemium", help="Brief cost model tag")
    parser.add_argument("--best-for", type=str, default="Developers and software engineers", help="Recommended user profile")
    parser.add_argument("--out-dir", type=str, default="generated_agent_output", help="Output directory path")

    args = parser.parse_args()

    if not args.ide and not args.repo:
        parser.error("Either --ide or --repo must be specified.")

    if args.repo and not args.ide:
        print(f"Fetching repository details from GitHub: {args.repo}...")
        try:
            ide_info = fetch_github_repo_info(args.repo)
        except Exception as e:
            print(f"Could not fetch metadata from GitHub URL ({e}). Using provided flags.")
            repo_name = args.repo.rstrip('/').split('/')[-1].capitalize()
            ide_info = {
                "name": repo_name,
                "category": args.category,
                "pricing": args.pricing,
                "cost_model": args.cost_model,
                "pros": ["Open source development", "Customizable extension framework"],
                "cons": ["Ecosystem expanding"],
                "best_for": args.best_for,
                "flow_scene": f"Dark mode editor canvas showing {repo_name} interface.",
                "repo_url": args.repo
            }
    else:
        ide_info = {
            "name": args.ide,
            "category": args.category,
            "pricing": args.pricing,
            "cost_model": args.cost_model,
            "pros": [
                f"Customizable workflow for {args.ide}",
                "Powerful code navigation and modern editor architecture",
                "Strong plugin and customization capability"
            ],
            "cons": [
                "Requires user configuration for specialized workflows"
            ],
            "best_for": args.best_for,
            "flow_scene": f"Cinematic dark setup displaying {args.ide} interface and code syntax highlighting."
        }

    os.makedirs(args.out_dir, exist_ok=True)
    slug = sanitize_slug(ide_info["name"])

    # Generate AMP Blog Post
    blog_file = os.path.join(args.out_dir, f"{slug}_amp_blog.html")
    blog_content = generate_amp_blog_post(ide_info)
    with open(blog_file, "w", encoding="utf-8") as f:
        f.write(blog_content)

    # Generate Google Flow Video Spec
    spec_file = os.path.join(args.out_dir, f"{slug}_google_flow_spec.md")
    spec_content = generate_google_flow_video_spec(ide_info)
    with open(spec_file, "w", encoding="utf-8") as f:
        f.write(spec_content)

    print(f"Agentic skill successfully generated content for '{ide_info['name']}':")
    print(f" - AMP Blog Post: {blog_file}")
    print(f" - Google Flow Video Spec: {spec_file}")

if __name__ == "__main__":
    main()
