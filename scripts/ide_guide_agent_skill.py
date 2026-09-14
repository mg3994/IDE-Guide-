#!/usr/bin/env python3
"""
IDE Guide Agentic Skill Tool
CLI skill tool that allows on-demand generation of custom AMP HTML blog posts
and Google Flow video prompt specifications for any specified IDE or GitHub repository URL.
"""

import argparse
import json
import os
import sys
import datetime
from generate_daily_content import (
    generate_amp_html,
    generate_google_flow_spec,
    CURATED_IDE_DATABASE,
    DISCLAIMER_TEXT
)

def build_custom_ide_data(name, tagline=None, pricing=None, repo=None):
    # Check if exists in curated database
    for item in CURATED_IDE_DATABASE:
        if item["name"].lower() == name.lower():
            return item.copy()

    # Create dynamic entry
    return {
        "name": name,
        "tagline": tagline or f"Modern IDE & Code Editor - {name}",
        "pricing": pricing or "Free / Freemium",
        "open_source": True,
        "primary_language": "Multi-language / Polyglot",
        "good_points": [
            f"Optimized workflow and developer ergonomics for {name}",
            "Extensible plugin/extension system for language support",
            "Modern interface with dark mode and keybindings",
            "Active community support and regular updates"
        ],
        "bad_points": [
            "Learning curve for specialized keyboard shortcuts and configuration",
            "Resource usage depends on active plugins and extension setup"
        ],
        "best_for": f"Developers looking for modern productivity gains using {name}",
        "verdict": f"Highly recommended tool for modern development workflows using {name}.",
        "repo": repo or ""
    }

def main():
    parser = argparse.ArgumentParser(description="IDE Guide Agentic CLI Skill - On-demand Content Generator")
    parser.add_argument("--ide", required=True, help="Name of the IDE / Code Editor (e.g. Cursor, Sublime Text, Emacs)")
    parser.add_argument("--tagline", help="Tagline description of the IDE")
    parser.add_argument("--pricing", help="Pricing model (e.g., Free & Open Source, Paid $15/mo)")
    parser.add_argument("--repo", help="GitHub repo full path (e.g., zed-industries/zed)")
    parser.add_argument("--type", choices=["amp", "flow", "both"], default="both", help="Output type (amp, flow, or both)")
    parser.add_argument("--output-dir", default="content/custom", help="Output directory path")

    args = parser.parse_args()

    ide_data = build_custom_ide_data(args.ide, tagline=args.tagline, pricing=args.pricing, repo=args.repo)
    date_str = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d")
    slug = ide_data["name"].lower().replace(' ', '-').replace('(', '').replace(')', '')

    os.makedirs(args.output_dir, exist_ok=True)
    created_files = []

    if args.type in ["amp", "both"]:
        amp_html = generate_amp_html(ide_data, date_str, post_index=1)
        amp_path = os.path.join(args.output_dir, f"{slug}_amp.html")
        with open(amp_path, 'w', encoding='utf-8') as f:
            f.write(amp_html)
        created_files.append(amp_path)

    if args.type in ["flow", "both"]:
        flow_json, flow_md = generate_google_flow_spec(ide_data, date_str, video_index=1)
        json_path = os.path.join(args.output_dir, f"{slug}_flow.json")
        md_path = os.path.join(args.output_dir, f"{slug}_flow.md")

        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(flow_json, f, indent=2)
        with open(md_path, 'w', encoding='utf-8') as f:
            f.write(flow_md)

        created_files.append(json_path)
        created_files.append(md_path)

    print(f"🤖 Agentic Skill execution complete for '{ide_data['name']}'!")
    print("Files created:")
    for filepath in created_files:
        print(f"  - {filepath}")

if __name__ == "__main__":
    main()
