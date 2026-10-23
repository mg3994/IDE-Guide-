#!/usr/bin/env python3
"""
Agentic CLI Skill Tool for IDE Guide.
Generates custom AMP HTML blog posts and Google Flow video specs on demand
for any specified IDE name or GitHub repository URL.
"""

import argparse
import os
import sys
from typing import Dict, Any

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.amp_validator import validate_amp_html, REQUIRED_DISCLAIMER
from scripts.generate_daily_content import generate_amp_blog_post, generate_google_flow_video_spec, IDE_DATABASE


def analyze_custom_ide(name_or_url: str, pricing_type: str = "Freemium / Open Source") -> Dict[str, Any]:
    """Builds a structured IDE profile from a custom IDE name or repo URL."""
    clean_name = name_or_url.strip().rstrip('/')
    if '/' in clean_name and ('github.com' in clean_name or 'git' in clean_name):
        repo_parts = clean_name.split('/')
        ide_name = repo_parts[-1].replace('-', ' ').replace('_', ' ').title()
        vendor = repo_parts[-2].title() if len(repo_parts) >= 2 else "Open Source Community"
        overview = f"{ide_name} is an open-source code editing tool available on GitHub ({clean_name})."
    else:
        ide_name = clean_name.title()
        vendor = "Software Vendor"
        overview = f"{ide_name} is a high-performance code editor and development tool."

    # Look up in database if available
    for existing in IDE_DATABASE:
        if existing["name"].lower() == ide_name.lower() or existing["id"].lower() == ide_name.lower().replace(" ", ""):
            return existing

    return {
        "id": ide_name.lower().replace(" ", "_"),
        "name": ide_name,
        "vendor": vendor,
        "pricing_type": pricing_type,
        "pricing_details": f"Check official vendor resources for details ({pricing_type}).",
        "overview": overview,
        "pros": [
            "Tailored workflow for modern software development",
            "Extensible architecture with community plugin support",
            "High performance code navigation"
        ],
        "cons": [
            "Requires initial configuration for specific stack setups",
            "Varying plugin quality across community contributions"
        ],
        "best_for": "Developers seeking an effective code editing environment for their tech stack.",
        "image_url": "https://images.unsplash.com/photo-1555066931-4365d14bab8c?w=800&auto=format&fit=crop"
    }


def generate_custom_package(target: str, output_dir: str = "output", pricing: str = "Freemium"):
    os.makedirs(output_dir, exist_ok=True)
    ide_info = analyze_custom_ide(target, pricing_type=pricing)

    blog_html = generate_amp_blog_post(ide_info)
    is_valid, errors = validate_amp_html(blog_html)

    blog_file = os.path.join(output_dir, f"amp_blog_{ide_info['id']}.html")
    with open(blog_file, 'w', encoding='utf-8') as f:
        f.write(blog_html)

    video_spec = generate_google_flow_video_spec(ide_info)
    video_file = os.path.join(output_dir, f"google_flow_spec_{ide_info['id']}.md")
    with open(video_file, 'w', encoding='utf-8') as f:
        f.write(video_spec)

    print(f"✅ Generated Agentic Skill Artifacts for '{ide_info['name']}':")
    print(f"  - AMP Blog Post: {blog_file} (AMP Valid: {is_valid})")
    print(f"  - Google Flow Spec: {video_file}")
    if not is_valid:
        print(f"  - AMP Warnings: {errors}")


def main():
    parser = argparse.ArgumentParser(description="IDE Guide Agentic CLI Tool: Generate AMP Blog Posts & Google Flow Specs")
    parser.add_argument("--ide", type=str, required=True, help="IDE/Editor name or GitHub repo URL (e.g., 'Helix' or 'https://github.com/helix-editor/helix')")
    parser.add_argument("--output-dir", type=str, default="output", help="Output directory for generated files")
    parser.add_argument("--pricing", type=str, default="Free / Open Source", help="Pricing tier (Free, Paid, Freemium)")

    args = parser.parse_args()
    generate_custom_package(args.ide, args.output_dir, args.pricing)


if __name__ == "__main__":
    main()
