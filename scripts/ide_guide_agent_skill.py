#!/usr/bin/env python3
"""
IDE Guide Agentic Skill CLI Tool
Allows on-demand generation of custom AMP HTML blog posts and Google Flow video specs
for any specified IDE name, custom code editor, or GitHub repository URL.
"""

import argparse
import json
import os
import sys
from datetime import datetime, timezone

# Ensure parent directory is in sys.path if invoked directly
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from scripts.generate_daily_content import (
    IDE_DATABASE,
    DISCLAIMER_TEXT,
    generate_amp_blog_post,
    generate_google_flow_video_spec,
    spec_to_markdown
)
from scripts.amp_validator import validate_amp_html


def build_custom_ide_data(name: str, repo_url: str = None) -> dict:
    # Check if IDE exists in database
    for item in IDE_DATABASE:
        if item["name"].lower() == name.lower() or item["id"].lower() == name.lower():
            return item

    # Derive safe ID
    safe_id = name.lower().replace(" ", "").replace("-", "").replace("_", "")

    # Generic template for on-demand custom IDE or repo URL
    ide_data = {
        "id": safe_id,
        "name": name,
        "developer": "Open Source Community / Vendor" if not repo_url else repo_url.split("/")[3] if len(repo_url.split("/")) > 3 else "Community",
        "category": "Code Editor / IDE",
        "pricing": "Free / Open Source / Commercial",
        "pros": [
            f"Tailored feature set for modern software development workflows in {name}",
            "Flexible plugin and workspace customization support",
            "Active developer ecosystem and continuous version updates"
        ],
        "cons": [
            "Requires initial configuration for specialized project build tools",
            "Resource usage varies depending on active extensions and project size"
        ],
        "target_audience": f"Developers, software engineers, and technical teams using {name}.",
        "best_for": f"Building scalable applications with {name}.",
        "image_url": "https://images.unsplash.com/photo-1555066931-4365d14bab8c?w=800&auto=format&fit=crop"
    }

    if repo_url:
        ide_data["pros"].append(f"Direct source repository available at {repo_url}")

    return ide_data


def generate_custom_package(name: str, repo_url: str = None, output_dir: str = None):
    date_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    ide_data = build_custom_ide_data(name, repo_url)

    if not output_dir:
        output_dir = os.path.join("content", f"custom_{date_str}")
    os.makedirs(output_dir, exist_ok=True)

    # 1. AMP Blog Post
    amp_html = generate_amp_blog_post(ide_data, date_str)
    is_valid, errors = validate_amp_html(amp_html)
    if not is_valid:
        print(f"Warning: AMP validation failed with errors: {errors}", file=sys.stderr)

    post_path = os.path.join(output_dir, f"post_{ide_data['id']}.html")
    with open(post_path, "w", encoding="utf-8") as f:
        f.write(amp_html)

    # 2. Google Flow Video Spec
    video_spec = generate_google_flow_video_spec(ide_data, date_str)
    json_path = os.path.join(output_dir, f"video_spec_{ide_data['id']}.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(video_spec, f, indent=2)

    md_spec = spec_to_markdown(video_spec)
    md_path = os.path.join(output_dir, f"video_spec_{ide_data['id']}.md")
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(md_spec)

    print(f"Successfully generated agentic skill package for '{name}':")
    print(f" - AMP Blog Post: {post_path}")
    print(f" - Google Flow Spec (JSON): {json_path}")
    print(f" - Google Flow Spec (Markdown): {md_path}")


def main():
    parser = argparse.ArgumentParser(description="IDE Guide Agentic Skill - On-demand AMP Post & Google Flow Spec Generator")
    parser.add_argument("--name", required=True, help="Name of the IDE, editor, or tool (e.g. 'Helix', 'Zed', 'VS Code')")
    parser.add_argument("--repo", help="Optional GitHub repository URL (e.g. 'https://github.com/helix-editor/helix')")
    parser.add_argument("--output-dir", help="Optional custom output directory path")

    args = parser.parse_args()
    generate_custom_package(args.name, args.repo, args.output_dir)


if __name__ == "__main__":
    main()
