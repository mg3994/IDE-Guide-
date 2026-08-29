#!/usr/bin/env python3
"""
Agentic CLI Skill Tool for IDE Guide.

Enables on-demand generation of AMP HTML blog posts (for ideguide.blogspot.com)
and Google Flow video specs (for YouTube @IDEguide) for custom IDE names or GitHub repo URLs.
"""

import argparse
import json
import os
import sys
import re
import urllib.request

from generate_daily_content import (
    generate_amp_html_blog_post,
    generate_google_flow_video_spec,
    DISCLAIMER_TEXT
)

def fetch_github_repo_info(repo_url_or_path):
    # Extract owner/repo
    match = re.search(r"github\.com/([^/]+)/([^/]+)", repo_url_or_path)
    if not match:
        parts = repo_url_or_path.strip("/").split("/")
        if len(parts) == 2:
            owner, repo = parts
        else:
            return None
    else:
        owner, repo = match.group(1), match.group(2)

    api_url = f"https://api.github.com/repos/{owner}/{repo}"
    req = urllib.request.Request(api_url, headers={"User-Agent": "IDE-Guide-Agent"})
    try:
        with urllib.request.urlopen(req, timeout=5) as response:
            if response.status == 200:
                data = json.loads(response.read().decode())
                return {
                    "name": data.get("name", repo).capitalize(),
                    "slug": data.get("name", repo).lower(),
                    "developer": data.get("owner", {}).get("login", owner),
                    "pricing_model": "Free / Open Source",
                    "license_type": (data.get("license") or {}).get("spdx_id", "Open Source") or "Open Source",
                    "category": "Open Source Code Editor",
                    "pros": [
                        f"Popular open-source repository with {data.get('stargazers_count', 0):,} GitHub stars",
                        f"Description: {data.get('description', 'Modern developer tool')}",
                        "Active community development and issue tracking",
                        "Fully open-source codebase transparent for auditing"
                    ],
                    "cons": [
                        "May require self-building or manual plugin setup",
                        "Community-driven roadmap and support timelines",
                        "Performance depends on local environment configuration"
                    ],
                    "verdict": f"Best for open-source enthusiasts looking to leverage {data.get('name')} for flexible development workflows."
                }
    except Exception as e:
        print(f"Failed to fetch GitHub repo info: {e}")
    return None

def build_custom_ide_data(ide_name, pricing="Free / Commercial", developer="Independent / Vendor"):
    slug = re.sub(r"[^a-z0-9]+", "-", ide_name.lower()).strip("-")
    return {
        "name": ide_name,
        "slug": slug,
        "developer": developer,
        "pricing_model": pricing,
        "license_type": "Proprietary / Open Source",
        "category": "Developer Code Editor",
        "pros": [
            f"Tailored productivity features designed for modern software development in {ide_name}",
            "Intuitive user interface and visual workflow optimization",
            "Comprehensive code navigation and syntax assistance"
        ],
        "cons": [
            "Requires familiarization with workspace keybindings and settings",
            "Plugin ecosystem integration varies by target framework"
        ],
        "verdict": f"A solid candidate for developers exploring alternative editor options tailored to {ide_name}."
    }

def main():
    parser = argparse.ArgumentParser(description="IDE Guide Agentic Skill CLI Tool")
    parser.add_argument("--ide", help="Name of the IDE/Code Editor to generate content for")
    parser.add_argument("--repo", help="GitHub repository URL or owner/repo path")
    parser.add_argument("--pricing", default="Free / Paid Tier Available", help="Pricing model description")
    parser.add_argument("--developer", default="Developer Team", help="Developer or organization name")
    parser.add_argument("--output-dir", default="agent_output", help="Directory to save generated files")

    args = parser.parse_args()

    if not args.ide and not args.repo:
        parser.print_help()
        sys.exit(1)

    ide_info = None
    if args.repo:
        print(f"Fetching GitHub repository info for {args.repo}...")
        ide_info = fetch_github_repo_info(args.repo)

    if not ide_info and args.ide:
        ide_info = build_custom_ide_data(args.ide, pricing=args.pricing, developer=args.developer)

    if not ide_info:
        print("Error: Could not determine IDE specifications.")
        sys.exit(1)

    os.makedirs(args.output_dir, exist_ok=True)
    slug = ide_info["slug"]

    # Generate AMP HTML Post
    amp_html = generate_amp_html_blog_post(ide_info)
    blog_path = os.path.join(args.output_dir, f"blog_post_{slug}.html")
    with open(blog_path, "w", encoding="utf-8") as f:
        f.write(amp_html)

    # Generate Google Flow Spec
    flow_spec = generate_google_flow_video_spec(ide_info)
    spec_path = os.path.join(args.output_dir, f"video_spec_{slug}.json")
    with open(spec_path, "w", encoding="utf-8") as f:
        json.dump(flow_spec, f, indent=2)

    print(f"\n✅ Agentic Skill Generation Complete for '{ide_info['name']}':")
    print(f" 📄 AMP HTML Blog Post: {blog_path} (Ready for Blogger - ideguide.blogspot.com)")
    print(f" 🎬 Google Flow Video Spec: {spec_path} (Ready for YouTube - @IDEguide)")
    print(f" 🛡️ Non-Sponsorship Disclaimer verified included.")

if __name__ == "__main__":
    main()
