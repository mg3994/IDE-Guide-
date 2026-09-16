#!/usr/bin/env python3
"""
Agentic CLI Skill Tool for IDE Guide

Allows on-demand generation of AMP-compliant Blogger HTML content and Google Flow AI Video Specs
for any given IDE name, repository URL, or custom feature prompt.
"""

import argparse
import os
import sys
import json

try:
    from scripts.generate_daily_content import generate_amp_html_post, generate_google_flow_video_spec
except ImportError:
    from generate_daily_content import generate_amp_html_post, generate_google_flow_video_spec

def run_agentic_skill(ide_name, category="Developer Code Editor", pricing="Freemium / Open Source",
                      developer="Independent", summary=None, pros=None, cons=None, output_dir=None):
    """Executes the agentic skill to build structured AMP HTML and Google Flow specs."""

    slug = ide_name.lower().replace(" ", "-").replace("/", "-")

    if not summary:
        summary = f"{ide_name} is an advanced code editor and development environment designed to enhance software engineering workflows."
    if not pros:
        pros = [
            f"Optimized user interface for modern software projects",
            f"Extensible plugin ecosystem and custom configurations",
            f"High performance code syntax highlighting and navigation"
        ]
    if not cons:
        cons = [
            f"May require initial setup for complex project builds",
            f"Ecosystem features depend on active community extensions"
        ]

    ide_info = {
        "name": ide_name,
        "slug": slug,
        "category": category,
        "pricing": pricing,
        "developer": developer,
        "summary": summary,
        "pros": pros,
        "cons": cons,
        "best_for": f"Software developers evaluating modern tools like {ide_name}.",
        "verdict": f"A powerful and feature-rich tool in the modern developer ecosystem.",
        "icon_url": "https://images.unsplash.com/photo-1555066931-4365d14bab8c?w=600&auto=format&fit=crop"
    }

    if not output_dir:
        output_dir = os.path.join("content", "agentic_builds")
    os.makedirs(output_dir, exist_ok=True)

    # Generate AMP HTML
    amp_html = generate_amp_html_post(ide_info, post_num=1)
    amp_path = os.path.join(output_dir, f"amp_{slug}.html")
    with open(amp_path, "w", encoding="utf-8") as f:
        f.write(amp_html)

    # Generate Video Specs
    video_json, video_md = generate_google_flow_video_spec(ide_info, post_num=1)
    json_path = os.path.join(output_dir, f"video_{slug}.json")
    md_path = os.path.join(output_dir, f"video_{slug}.md")

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(video_json, f, indent=2)
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(video_md)

    print(f"✨ [IDE Guide Agentic Skill] Generated assets for '{ide_name}':")
    print(f" - AMP HTML Article: {amp_path}")
    print(f" - Google Flow Video Spec (JSON): {json_path}")
    print(f" - Video Script (Markdown): {md_path}")

    return {
        "amp_path": amp_path,
        "json_path": json_path,
        "md_path": md_path
    }

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="IDE Guide Agentic Skill CLI")
    parser.add_argument("--name", required=True, help="Name of the IDE/Editor (e.g. 'Helix', 'Lapce', 'Cursor')")
    parser.add_argument("--category", default="Developer Tool & Code Editor", help="Primary category")
    parser.add_argument("--pricing", default="Free / Open Source", help="Pricing model (Free/Paid/Freemium)")
    parser.add_argument("--developer", default="Open Source Community", help="Creator or maintaining organization")
    parser.add_argument("--output-dir", default=None, help="Directory to save generated assets")

    args = parser.parse_args()
    run_agentic_skill(
        ide_name=args.name,
        category=args.category,
        pricing=args.pricing,
        developer=args.developer,
        output_dir=args.output_dir
    )
