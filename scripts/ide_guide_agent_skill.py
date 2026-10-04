#!/usr/bin/env python3
"""
IDE Guide - Agentic Skill Tool.
Enables on-demand generation of custom AMP HTML blog posts and Google Flow video specs
for any given IDE name or custom IDE information provided via command line.
"""

import sys
import argparse
import os
from scripts.generate_daily_content import (
    IDE_DATABASE, generate_amp_blog_post, generate_google_flow_spec
)
from scripts.amp_validator import validate_amp_html

def generate_custom_ide_content(
    ide_name: str,
    output_dir: str = "custom_content",
    category: str = "Code Editor",
    pricing: str = "Free",
    pricing_category: str = "Free",
    pros: str = None,
    cons: str = None,
    best_for: str = "Software developers seeking efficient workflows.",
    site_url: str = "https://ideguide.blogspot.com"
):
    """
    Generates custom AMP blog post and Google Flow video spec on demand for any IDE/editor.
    """
    if ide_name in IDE_DATABASE:
        info = IDE_DATABASE[ide_name].copy()
    else:
        pros_list = [p.strip() for p in pros.split(";")] if pros else ["Fast code editing", "Extensible architecture"]
        cons_list = [c.strip() for c in cons.split(";")] if cons else ["Learning curve", "Memory overhead on large projects"]
        info = {
            "tagline": f"An evaluation of {ide_name} editor and development environment.",
            "pricing": pricing,
            "pricing_category": pricing_category,
            "category": category,
            "pros": pros_list,
            "cons": cons_list,
            "best_for": best_for,
            "site_url": site_url
        }

    os.makedirs(output_dir, exist_ok=True)
    slug = ide_name.lower().replace(" ", "_")

    blog_file = os.path.join(output_dir, f"post_{slug}.html")
    blog_html = generate_amp_blog_post(ide_name, info)

    # Validate AMP compliance before saving
    is_valid, errors = validate_amp_html(blog_html)
    if not is_valid:
        raise ValueError(f"Generated HTML failed AMP validation: {errors}")

    with open(blog_file, "w", encoding="utf-8") as f:
        f.write(blog_html)

    video_file = os.path.join(output_dir, f"video_{slug}_spec.md")
    video_spec = generate_google_flow_spec(ide_name, info)
    with open(video_file, "w", encoding="utf-8") as f:
        f.write(video_spec)

    print(f"✅ Created AMP Blog Post: {blog_file}")
    print(f"✅ Created Google Flow Video Spec: {video_file}")
    return blog_file, video_file

def main():
    parser = argparse.ArgumentParser(description="Agentic Skill Tool for IDE Guide")
    parser.add_argument("--ide", required=True, help="Name of the IDE/Code Editor (e.g. Cursor, Neovim, Zed)")
    parser.add_argument("--outdir", default="custom_content", help="Directory to save output files")
    parser.add_argument("--category", default="Code Editor", help="Category (e.g. AI Code Editor, Full IDE)")
    parser.add_argument("--pricing", default="Free", help="Full pricing description")
    parser.add_argument("--pricing-category", default="Free", help="Short pricing category (Free, Paid, Freemium)")
    parser.add_argument("--pros", help="Semicolon separated pros (e.g. 'Fast LSP; Great extensions')")
    parser.add_argument("--cons", help="Semicolon separated cons (e.g. 'High memory usage; Proprietary')")
    parser.add_argument("--best-for", default="Developers looking for productivity improvements.", help="Target developer audience")
    parser.add_argument("--site-url", default="https://ideguide.blogspot.com", help="Official site or reference URL")

    args = parser.parse_args()

    generate_custom_ide_content(
        ide_name=args.ide,
        output_dir=args.outdir,
        category=args.category,
        pricing=args.pricing,
        pricing_category=args.pricing_category,
        pros=args.pros,
        cons=args.cons,
        best_for=args.best_for,
        site_url=args.site_url
    )

if __name__ == "__main__":
    main()
