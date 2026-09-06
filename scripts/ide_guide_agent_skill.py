#!/usr/bin/env python3
"""
Agentic CLI Skill Tool for IDE Guide.
Enables on-demand generation of AMP HTML blog posts and Google Flow video specs
for a specified IDE name, tool, or repository URL.
Usage:
    python3 scripts/ide_guide_agent_skill.py --ide "Windsurf Editor" --pricing "Freemium" --output-dir "./custom_output"
"""

import os
import json
import argparse
from datetime import datetime, timezone
from generate_daily_content import (
    generate_amp_html_post,
    generate_google_flow_video_spec,
    NON_SPONSORSHIP_DISCLAIMER
)


def run_agentic_skill(ide_name, pricing="Freemium", category="Code Editor", description=None, pros=None, cons=None, output_dir="./output"):
    if not description:
        description = f"Agentic analysis and showcase for {ide_name} editor."
    if not pros:
        pros = ["Advanced developer productivity", "Modern extension framework", "Fast code completion"]
    if not cons:
        cons = ["Requires learning custom hotkeys", "Resource demands depend on workspace size"]

    ide_data = {
        "name": ide_name,
        "description": description,
        "pricing": pricing,
        "category": category,
        "pros": pros,
        "cons": cons,
        "best_for": f"Developers looking to evaluate {ide_name} for their stack."
    }

    os.makedirs(output_dir, exist_ok=True)
    slug = ide_name.lower().replace(" ", "_")

    # Generate AMP HTML Post
    amp_html = generate_amp_html_post(ide_data)
    blog_file = os.path.join(output_dir, f"blog_post_{slug}.html")
    with open(blog_file, "w", encoding="utf-8") as f:
        f.write(amp_html)

    # Generate Google Flow Video Spec
    video_spec = generate_google_flow_video_spec(ide_data)
    video_file = os.path.join(output_dir, f"video_spec_{slug}.json")
    with open(video_file, "w", encoding="utf-8") as f:
        json.dump(video_spec, f, indent=2)

    result = {
        "status": "success",
        "ide_name": ide_name,
        "blog_post_path": blog_file,
        "video_spec_path": video_file,
        "disclaimer_included": NON_SPONSORSHIP_DISCLAIMER in amp_html and video_spec["disclaimer"] == NON_SPONSORSHIP_DISCLAIMER
    }
    return result


def main():
    parser = argparse.ArgumentParser(description="IDE Guide Agentic Skill: Custom AMP Blog & Video Spec Generator")
    parser.add_argument("--ide", required=True, help="Name of the IDE / Code Editor")
    parser.add_argument("--pricing", default="Freemium", help="Pricing model (Free, Paid, Freemium)")
    parser.add_argument("--category", default="Code Editor", help="Category (AI Editor, Full IDE, Modal Editor, etc.)")
    parser.add_argument("--description", default=None, help="Brief overview description")
    parser.add_argument("--output-dir", default="./output", help="Output directory for generated files")

    args = parser.parse_args()

    res = run_agentic_skill(
        ide_name=args.ide,
        pricing=args.pricing,
        category=args.category,
        description=args.description,
        output_dir=args.output_dir
    )

    print(json.dumps(res, indent=2))


if __name__ == "__main__":
    main()
