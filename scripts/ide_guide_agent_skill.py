#!/usr/bin/env python3
"""
Agentic CLI Skill Tool for IDE Guide.
Generates on-demand AMP HTML blog post and Google Flow video spec for any specified IDE or GitHub repository URL.
Usage:
  python3 scripts/ide_guide_agent_skill.py --ide "Helix Editor" --pricing "Free (Open Source)" --category "Modal Terminal Editor"
  python3 scripts/ide_guide_agent_skill.py --repo "https://github.com/helix-editor/helix"
"""

import argparse
import json
import os
import sys
from datetime import datetime, timezone
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from scripts.generate_daily_content import generate_amp_blog_post, generate_google_flow_video_spec, DISCLAIMER_TEXT
from scripts.amp_validator import validate_amp_content


def generate_skill_content(ide_info: dict, output_dir: str = "output"):
    os.makedirs(output_dir, exist_ok=True)
    slug = ide_info.get("slug", "custom-ide")

    # Generate AMP Blog Post
    blog_html = generate_amp_blog_post(ide_info)
    is_valid, errors = validate_amp_content(blog_html)
    if not is_valid:
        print(f"Warning: AMP validation failed for agent output: {errors}")

    blog_path = os.path.join(output_dir, f"agent_blog_{slug}.amp.html")
    with open(blog_path, "w", encoding="utf-8") as f:
        f.write(blog_html)

    # Generate Google Flow Spec
    video_spec = generate_google_flow_video_spec(ide_info)
    video_path = os.path.join(output_dir, f"agent_video_spec_{slug}.json")
    with open(video_path, "w", encoding="utf-8") as f:
        json.dump(video_spec, f, indent=2)

    print(f"Successfully generated agentic skill content in '{output_dir}':")
    print(f"  - Blog Post (AMP HTML): {blog_path}")
    print(f"  - Google Flow Video Spec: {video_path}")
    return blog_path, video_path


def parse_repo_url(repo_url: str) -> dict:
    repo_name = repo_url.rstrip("/").split("/")[-1].replace("-", " ").replace("_", " ").title()
    slug = repo_url.rstrip("/").split("/")[-1].lower()
    return {
        "name": repo_name,
        "slug": slug,
        "category": "Open Source Code Editor / IDE",
        "pricing": "Free (Open Source)",
        "is_paid": False,
        "pros": [
            "Open source community driven development",
            "Customizable architecture and high extensibility",
            "Transparent source code and security oversight"
        ],
        "cons": [
            "May require self-configuration for specialized language toolchains"
        ],
        "target_audience": "Developers looking for open source, community-supported development environments.",
        "overview": f"{repo_name} is an open-source development tool hosted at {repo_url}. It offers flexible coding capabilities for modern developer workflows.",
        "youtube_keywords": f"{repo_name}, {slug} review, open source IDE, code editor tutorial"
    }


def main():
    parser = argparse.ArgumentParser(description="Agentic skill generator for IDE Guide channel & blog.")
    parser.add_argument("--ide", type=str, help="Name of the IDE/Code Editor")
    parser.add_argument("--repo", type=str, help="Repository URL for an open source IDE/Editor")
    parser.add_argument("--pricing", type=str, default="Free / Paid Options Available", help="Pricing details (e.g. Free, $15/mo)")
    parser.add_argument("--category", type=str, default="Code Editor", help="Category of the editor")
    parser.add_argument("--is-paid", action="store_true", help="Set flag if primary version is paid")
    parser.add_argument("--outdir", type=str, default="content/custom", help="Output directory path")

    args = parser.parse_args()

    if args.repo:
        ide_info = parse_repo_url(args.repo)
    elif args.ide:
        slug = args.ide.lower().replace(" ", "-").replace("/", "-")
        ide_info = {
            "name": args.ide,
            "slug": slug,
            "category": args.category,
            "pricing": args.pricing,
            "is_paid": args.is_paid,
            "pros": [
                f"Tailored capabilities for {args.category} workflows",
                "Responsive editor UI with modern code navigation",
                "Extensible setup options for various stacks"
            ],
            "cons": [
                "Ecosystem size depends on community adoption"
            ],
            "target_audience": f"Developers seeking specialized performance in {args.category.lower()} environments.",
            "overview": f"{args.ide} is a specialized {args.category.lower()} designed to streamline developer code editing and debugging.",
            "youtube_keywords": f"{args.ide}, {args.category}, IDE review, developer productivity"
        }
    else:
        print("Error: Please specify either --ide <Name> or --repo <URL>.")
        sys.exit(1)

    generate_skill_content(ide_info, args.outdir)


if __name__ == "__main__":
    main()
