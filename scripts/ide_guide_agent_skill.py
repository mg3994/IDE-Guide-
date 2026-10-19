#!/usr/bin/env python3
"""
Agentic CLI Skill Tool for IDE Guide.
Provides an agentic skill interface for generating AMP HTML blog posts and Google Flow video specs on-demand
for custom IDE names, URLs, or daily batch runs.
"""

import sys
import os
import argparse
import datetime
from typing import Dict, Any

from scripts.generate_daily_content import (
    generate_amp_blog_post,
    generate_google_flow_spec,
    generate_daily_package,
    IDE_CATALOG,
    DISCLAIMER_TEXT
)
from scripts.amp_validator import AmpValidator

def create_custom_ide_data(name: str, category: str = "Code Editor", pricing_type: str = "Freemium", url: str = "") -> Dict[str, Any]:
    slug = name.lower().replace(" ", "_").replace(".", "_")
    return {
        "id": slug,
        "name": name,
        "category": category,
        "pricing_type": pricing_type,
        "pricing_details": f"Check official details at {url if url else name}",
        "tagline": f"An advanced developer environment for {name}.",
        "pros": [
            f"Optimized workflow and performance for {name}",
            "Modern developer experience and high visual clarity",
            "Extensible plugin and configuration options"
        ],
        "cons": [
            "Requires initial configuration for specific workflows",
            "Hardware resource requirements vary depending on extension load"
        ],
        "target_audience": f"Developers, software engineers, and technology teams working with {name}.",
        "verdict": f"A solid, feature-rich choice for engineers utilizing {name} in modern software workflows."
    }

def process_ide_request(ide_name: str, category: str, pricing: str, url: str, output_dir: str = None) -> Dict[str, str]:
    today_str = datetime.date.today().isoformat()
    if not output_dir:
        output_dir = os.path.join("content", today_str)

    os.makedirs(output_dir, exist_ok=True)

    # Check if IDE exists in catalog, else build custom data
    existing = next((item for item in IDE_CATALOG if item["name"].lower() == ide_name.lower() or item["id"] == ide_name.lower()), None)
    ide_data = existing if existing else create_custom_ide_data(ide_name, category, pricing, url)

    slug = ide_data["id"]

    # Generate AMP Blog Post
    amp_post = generate_amp_blog_post(ide_data, today_str)
    blog_file = os.path.join(output_dir, f"skill_{slug}_amp.html")
    with open(blog_file, "w", encoding="utf-8") as f:
        f.write(amp_post)

    # Validate AMP
    validator = AmpValidator(amp_post)
    is_valid, errors, _ = validator.validate()
    if not is_valid:
        raise ValueError(f"Generated AMP post failed validation: {errors}")

    # Generate Google Flow Video Spec
    flow_spec = generate_google_flow_spec(ide_data, today_str)
    video_file = os.path.join(output_dir, f"skill_{slug}_google_flow_spec.json")
    import json
    with open(video_file, "w", encoding="utf-8") as f:
        json.dump(flow_spec, f, indent=2)

    return {
        "blog_file": blog_file,
        "video_file": video_file,
        "ide_name": ide_data["name"],
        "pricing_type": ide_data["pricing_type"]
    }

def main():
    parser = argparse.ArgumentParser(description="IDE Guide Agentic CLI Skill Tool")
    parser.add_argument("--ide", type=str, help="Name of the IDE or Code Editor to cover")
    parser.add_argument("--category", type=str, default="Code Editor", help="Category (e.g., AI Editor, Terminal IDE, Full IDE)")
    parser.add_argument("--pricing", type=str, default="Freemium", help="Pricing model (Free, Paid, Freemium)")
    parser.add_argument("--url", type=str, default="", help="Website or repo URL for the IDE")
    parser.add_argument("--daily", action="store_true", help="Run full daily 3-package generator")
    parser.add_argument("--output-dir", type=str, default=None, help="Custom output directory")

    args = parser.parse_args()

    if args.daily:
        generate_daily_package()
        return

    if not args.ide:
        print("Error: Please specify an IDE name with --ide or run with --daily")
        sys.exit(1)

    result = process_ide_request(
        ide_name=args.ide,
        category=args.category,
        pricing=args.pricing,
        url=args.url,
        output_dir=args.output_dir
    )

    print(f"✨ Agentic Skill executed successfully for '{result['ide_name']}'!")
    print(f"  - AMP Blog Post: {result['blog_file']}")
    print(f"  - Google Flow Spec: {result['video_file']}")

if __name__ == "__main__":
    main()
