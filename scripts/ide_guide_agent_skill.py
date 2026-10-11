#!/usr/bin/env python3
"""
Agentic Skill CLI Tool for IDE Guide.
Generates custom AMP blog posts and Google Flow video specs for specific IDE names or GitHub repo URLs.
"""

import argparse
import os
import re
import sys
from datetime import datetime, timezone
from typing import Dict, Any

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from scripts.generate_daily_content import generate_amp_blog_post, generate_google_flow_video_spec, DISCLAIMER_TEXT
from scripts.amp_validator import validate_amp_html

def parse_repo_or_name(target: str) -> Dict[str, Any]:
    """
    Parses a target string (e.g., 'zed-industries/zed' or 'Fleet') into an IDE data dict.
    """
    cleaned_target = target.strip()
    if cleaned_target.startswith("http://") or cleaned_target.startswith("https://") or "/" in cleaned_target:
        # It's a URL or repo identifier (owner/repo)
        repo_name = cleaned_target.rstrip("/").split("/")[-1]
        name = repo_name.replace("-", " ").replace("_", " ").title()
        ide_id = re.sub(r'[^a-z0-9]', '_', repo_name.lower())
        return {
            "id": ide_id,
            "name": name,
            "developer": "Open Source Community / " + (cleaned_target.split("/")[3] if "github.com" in cleaned_target else "Maintainers"),
            "pricing": "Free / Open Source",
            "is_paid": False,
            "category": "Open Source Code Editor / Tool",
            "strengths": [
                f"Modern codebase architecture hosted at {cleaned_target}.",
                "Community driven extension ecosystem and active issue tracker.",
                "Customizable developer experience with cross-platform support."
            ],
            "weaknesses": [
                "May require active setup and configuration for niche tech stacks.",
                "Community-driven updates depending on developer maintenance release cycles."
            ],
            "best_for": "Developers seeking open-source options and custom setups.",
            "image_url": "https://images.unsplash.com/photo-1555066931-4365d14bab8c?w=800&auto=format&fit=crop"
        }
    else:
        name = cleaned_target.title()
        ide_id = re.sub(r'[^a-z0-9]', '_', name.lower())
        return {
            "id": ide_id,
            "name": name,
            "developer": name + " Developers",
            "pricing": "Freemium / Developer License",
            "is_paid": False,
            "category": "Code Editor / IDE Environment",
            "strengths": [
                f"Optimized editing experience engineered for {name}.",
                "Rich plugin ecosystem and smart code intelligence.",
                "Fast startup performance and flexible window management."
            ],
            "weaknesses": [
                "Feature set evaluation recommended based on specific project size.",
                "Plugins may require individual vendor updates."
            ],
            "best_for": "Engineers and software development teams.",
            "image_url": "https://images.unsplash.com/photo-1517694712202-14dd9538aa97?w=800&auto=format&fit=crop"
        }


def generate_custom_content(target: str, output_dir: str):
    os.makedirs(output_dir, exist_ok=True)
    ide = parse_repo_or_name(target)

    # Generate AMP Blog Post
    blog_filename = f"blog_post_{ide['id']}.html"
    blog_path = os.path.join(output_dir, blog_filename)
    blog_content = generate_amp_blog_post(ide)
    with open(blog_path, 'w', encoding='utf-8') as f:
        f.write(blog_content)

    # Validate generated post
    is_valid, errors = validate_amp_html(blog_content)
    if not is_valid:
        print(f"Warning: Generated AMP HTML for {target} has validation issues: {errors}")

    # Generate Google Flow Video Spec
    spec_filename = f"video_spec_{ide['id']}.md"
    spec_path = os.path.join(output_dir, spec_filename)
    spec_content = generate_google_flow_video_spec(ide)
    with open(spec_path, 'w', encoding='utf-8') as f:
        f.write(spec_content)

    print(f"Custom Agentic Skill Content Generated Successfully for '{target}':")
    print(f" - AMP Blog Post: {blog_path}")
    print(f" - Google Flow Spec: {spec_path}")


def main():
    parser = argparse.ArgumentParser(description="Agentic CLI Skill to generate AMP blog posts & video specs for any IDE/repo.")
    parser.add_argument("target", help="IDE Name or GitHub Repo URL (e.g. 'Cursor' or 'https://github.com/zed-industries/zed')")
    parser.add_argument("--outdir", default="content/custom", help="Output directory for generated artifacts")

    args = parser.parse_args()
    generate_custom_content(args.target, args.outdir)


if __name__ == "__main__":
    main()
