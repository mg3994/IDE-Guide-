#!/usr/bin/env python3
"""
Agentic CLI Skill Tool for IDE Guide.

Enables on-demand generation of custom AMP HTML blog posts (for Blogger ideguide.blogspot.com)
and Google Flow video prompt specifications (for YouTube @IDEguide) for any custom IDE or repo URL.
"""

import os
import sys
import json
import argparse
from typing import Dict, Any

# Import shared generator function from generate_daily_content
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from generate_daily_content import generate_amp_blog_post, generate_google_flow_video_spec
from amp_validator import validate_amp_html

def build_custom_ide_dict(name: str, category: str = "Code Editor", pricing: str = "Freemium", is_free: bool = False, developer: str = "Developer Community", pros: list = None, cons: list = None) -> Dict[str, Any]:
    """Constructs a standardized IDE dict for content generation."""
    slug = name.lower().replace(" ", "_").replace("/", "_")
    if not pros:
        pros = [
            f"Optimized workflow and responsive developer interface in {name}.",
            f"Extensible feature set tailored for modern language stacks.",
            f"Active community support and regular updates."
        ]
    if not cons:
        cons = [
            f"Requires initial setup time to customize settings for {name}.",
            f"Plugin ecosystem may be smaller than mainstream competitors."
        ]

    return {
        "id": slug,
        "name": name,
        "category": category,
        "pricing": pricing,
        "is_free": is_free,
        "license": "Open Source / Proprietary",
        "developer": developer,
        "tagline": f"The high-efficiency {category} for modern software developers.",
        "pros": pros,
        "cons": cons,
        "best_for": f"Software engineers, devops practitioners, and open-source contributors using {name}.",
        "image_url": "https://images.unsplash.com/photo-1555066931-4365d14bab8c?w=800&auto=format&fit=crop&q=80"
    }

def generate_custom_package(ide_name: str, category: str, pricing: str, is_free: bool, output_dir: str):
    os.makedirs(output_dir, exist_ok=True)
    ide_dict = build_custom_ide_dict(
        name=ide_name,
        category=category,
        pricing=pricing,
        is_free=is_free
    )

    # 1. AMP Blog Post
    amp_html = generate_amp_blog_post(ide_dict)
    is_valid, errors = validate_amp_html(amp_html)
    if not is_valid:
        raise ValueError(f"Generated AMP HTML failed validation: {errors}")

    post_filename = f"post_{ide_dict['id']}.html"
    post_path = os.path.join(output_dir, post_filename)
    with open(post_path, 'w', encoding='utf-8') as f:
        f.write(amp_html)

    # 2. Google Flow Video Spec
    video_spec = generate_google_flow_video_spec(ide_dict)
    video_filename = f"video_{ide_dict['id']}_google_flow.json"
    video_path = os.path.join(output_dir, video_filename)
    with open(video_path, 'w', encoding='utf-8') as f:
        json.dump(video_spec, f, indent=2)

    print(f"✅ Successfully generated custom skill package in '{output_dir}':")
    print(f"  - Blog Post (AMP HTML): {post_path}")
    print(f"  - Video Spec (Google Flow): {video_path}")
    return post_path, video_path


def main():
    parser = argparse.ArgumentParser(description="Agentic CLI Tool for generating AMP blog posts and Google Flow video specs.")
    parser.add_argument("--name", type=str, required=True, help="Name of the IDE or Code Editor (e.g., 'Lapce Editor')")
    parser.add_argument("--category", type=str, default="Code Editor", help="Category (e.g. 'Modal Editor', 'AI IDE')")
    parser.add_argument("--pricing", type=str, default="Free / Open Source", help="Pricing status (e.g. 'Free', 'Paid', '$15/mo')")
    parser.add_argument("--is-free", action="store_true", help="Flag if editor is 100% free")
    parser.add_argument("--outdir", type=str, default="content/custom_generated", help="Directory to save generated files")

    args = parser.parse_args()
    generate_custom_package(
        ide_name=args.name,
        category=args.category,
        pricing=args.pricing,
        is_free=args.is_free,
        output_dir=args.outdir
    )

if __name__ == "__main__":
    main()
