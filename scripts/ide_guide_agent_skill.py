#!/usr/bin/env python3
"""
IDE Guide - Agentic CLI Skill Tool
Enables on-demand generation of AMP HTML blog posts (for https://ideguide.blogspot.com/)
and Google Flow video specifications (for YouTube @IDEguide) for any IDE name or repository URL.
"""

import os
import sys
import argparse
import re
from datetime import datetime, timezone
from generate_daily_content import (
    generate_amp_blog_html,
    generate_google_flow_video_spec,
    MANDATORY_DISCLAIMER,
    CURATED_IDE_DATABASE
)

def parse_args():
    parser = argparse.ArgumentParser(
        description="IDE Guide Agentic Skill - Generate custom AMP HTML blog posts & Google Flow video specs."
    )
    parser.add_argument(
        "--ide",
        type=str,
        help="Name of the IDE or Code Editor (e.g., 'Cursor', 'Neovim', 'Helix')"
    )
    parser.add_argument(
        "--repo",
        type=str,
        help="GitHub Repository URL for the IDE/Editor (e.g., 'https://github.com/zed-industries/zed')"
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default="generated_skills",
        help="Directory to save generated blog post and video spec (default: 'generated_skills')"
    )
    parser.add_argument(
        "--date",
        type=str,
        default=None,
        help="Target date string YYYY-MM-DD (default: current date)"
    )
    return parser.parse_args()

def construct_ide_spec(ide_name=None, repo_url=None):
    if not ide_name and not repo_url:
        raise ValueError("Must specify either --ide or --repo")

    if ide_name:
        for db_ide in CURATED_IDE_DATABASE:
            if db_ide["name"].lower() == ide_name.lower() or db_ide["slug"] == ide_name.lower():
                return db_ide

    name = ide_name if ide_name else repo_url.split("/")[-1].replace("-", " ").title()
    slug = re.sub(r'[^a-z0-9]+', '-', name.lower()).strip('-')
    website = repo_url if repo_url else f"https://{slug}.dev"

    return {
        "name": name,
        "slug": slug,
        "category": "Code Editor / IDE",
        "description": f"{name} is a modern development editor designed to enhance software developer productivity.",
        "pros": [
            f"Extensible feature set tailored for modern development in {name}",
            "Customizable UI and workflow keyboard shortcuts",
            "Active developer community support"
        ],
        "cons": [
            "Learning curve for advanced workflow configurations",
            "Ecosystem plugin compatibility varies by language"
        ],
        "pricing": "Freemium / Open Source options available",
        "best_for": f"Software engineers, web developers, and power users evaluating {name}",
        "website": website
    }

def main():
    args = parse_args()
    date_str = args.date if args.date else datetime.now(timezone.utc).strftime("%Y-%m-%d")

    ide_spec = construct_ide_spec(args.ide, args.repo)

    os.makedirs(args.output_dir, exist_ok=True)

    # 1. Generate AMP HTML Blog Post
    amp_html = generate_amp_blog_html(ide_spec, date_str)
    blog_file = os.path.join(args.output_dir, f"blog_{ide_spec['slug']}.html")
    with open(blog_file, 'w', encoding='utf-8') as f:
        f.write(amp_html)

    # 2. Generate Google Flow Video Spec
    video_spec = generate_google_flow_video_spec(ide_spec, date_str)
    video_file = os.path.join(args.output_dir, f"video_{ide_spec['slug']}.md")
    with open(video_file, 'w', encoding='utf-8') as f:
        f.write(video_spec)

    print(f"Agentic skill generation completed successfully for {ide_spec['name']}!")
    print(f"AMP Blog Post: {blog_file}")
    print(f"Google Flow Video Spec: {video_file}")

if __name__ == "__main__":
    main()
