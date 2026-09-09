#!/usr/bin/env python3
"""
IDE Guide Agentic CLI Skill Tool
Usage:
  python3 scripts/ide_guide_agent_skill.py --ide "Cursor"
  python3 scripts/ide_guide_agent_skill.py --repo "https://github.com/zed-industries/zed"
  python3 scripts/ide_guide_agent_skill.py --ide "Helix" --output-dir "content/custom"
"""

import sys
import os
import argparse
from datetime import datetime, timezone

# Ensure src path is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.ide_guide.catalog import (
    get_ide_by_slug_or_name,
    fetch_github_repo_info,
    construct_custom_ide_data
)
from src.ide_guide.amp_generator import generate_amp_blog_post
from src.ide_guide.google_flow_generator import generate_google_flow_video_spec
from src.ide_guide.history_tracker import HistoryTracker

def main():
    parser = argparse.ArgumentParser(
        description="Agentic CLI Skill to generate AMP HTML blog posts and Google Flow video specs for IDE Guide."
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--ide", type=str, help="Name of the IDE or Code Editor (e.g. Cursor, Neovim, Windsurf)")
    group.add_argument("--repo", type=str, help="GitHub repository URL (e.g. https://github.com/zed-industries/zed)")

    parser.add_argument("--date", type=str, default=datetime.now(timezone.utc).strftime("%Y-%m-%d"), help="Target date YYYY-MM-DD")
    parser.add_argument("--output-dir", type=str, default="", help="Custom output directory")
    parser.add_argument("--format", type=str, choices=["shorts", "longform", "both"], default="both", help="Video spec format")

    args = parser.parse_args()

    # Determine IDE Data
    if args.repo:
        print(f"🔍 Fetching repository metadata for {args.repo}...")
        ide_data = fetch_github_repo_info(args.repo)
    else:
        print(f"🔍 Locating catalog details or building profile for IDE: {args.ide}...")
        existing = get_ide_by_slug_or_name(args.ide)
        if existing:
            ide_data = existing
        else:
            ide_data = construct_custom_ide_data(args.ide)

    slug = ide_data.get("slug", "ide")
    target_dir = args.output_dir or os.path.join("content", args.date)
    os.makedirs(target_dir, exist_ok=True)

    # 1. Generate AMP HTML blog post
    amp_html_content = generate_amp_blog_post(ide_data)
    blog_file_path = os.path.join(target_dir, f"{slug}_amp_post.html")
    with open(blog_file_path, "w", encoding="utf-8") as f:
        f.write(amp_html_content)
    print(f"📄 Generated AMP HTML Blog Post: {blog_file_path}")

    # 2. Generate Google Flow Video Spec(s)
    created_video_files = []
    formats = ["shorts", "longform"] if args.format == "both" else [args.format]
    for fmt in formats:
        spec_content = generate_google_flow_video_spec(ide_data, format_type=fmt)
        video_file_path = os.path.join(target_dir, f"{slug}_google_flow_{fmt}_spec.md")
        with open(video_file_path, "w", encoding="utf-8") as f:
            f.write(spec_content)
        created_video_files.append(video_file_path)
        print(f"🎥 Generated Google Flow Video Spec ({fmt}): {video_file_path}")

    # 3. Update History Tracker
    tracker = HistoryTracker()
    tracker.mark_covered(ide_data, date_str=args.date)
    print(f"✅ History updated in content/history.json for {ide_data.get('name')}")

    print("\n🎉 Skill execution completed successfully!")

if __name__ == "__main__":
    main()
