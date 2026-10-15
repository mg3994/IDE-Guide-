#!/usr/bin/env python3
"""
Agentic CLI Skill Tool for IDE Guide.
Allows on-demand content creation (AMP HTML Blog Post + Google Flow Video Specification)
for any IDE name or repository URL specified via CLI arguments.
"""

import argparse
import json
import os
import re
import sys
from typing import Dict, Any

from scripts.generate_daily_content import build_amp_html, build_google_flow_spec, MANDATORY_DISCLAIMER_PHRASE

def sanitize_id(name: str) -> str:
    cleaned = re.sub(r'[^a-zA-Z0-9\s-]', '', name).strip().lower()
    return re.sub(r'[\s_]+', '-', cleaned)

def create_ide_data_from_args(name: str, pricing: str, developer: str, category: str, primary_use: str) -> Dict[str, Any]:
    pricing_lower = pricing.lower()
    if "free" in pricing_lower and "paid" in pricing_lower:
        pricing_type = "Freemium"
    elif "free" in pricing_lower or "open source" in pricing_lower:
        pricing_type = "Free"
    else:
        pricing_type = "Paid"

    ide_id = sanitize_id(name)

    return {
        "id": ide_id,
        "name": name,
        "developer": developer if developer else "Independent Developer / Community",
        "pricing": pricing,
        "pricing_type": pricing_type,
        "category": category if category else "Code Editor & Development Environment",
        "primary_use": primary_use if primary_use else "Software Engineering and Rapid Prototyping",
        "key_features": [
            f"Optimized workspace environment tailored for {primary_use if primary_use else 'modern software engineering'}",
            "Integrated developer tools, terminal, and extension ecosystem",
            "Customizable keybindings, visual themes, and project configuration",
            "Built-in debugging and code navigation utilities"
        ],
        "pros": [
            f"Tailored productivity features for {name} users",
            "Flexible customization options and active development",
            "Streamlined workflow for rapid developer feedback"
        ],
        "cons": [
            "May require initial setup and configuration tuning for custom project workflows",
            "Ecosystem extensions depend on platform adoption"
        ],
        "target_audience": f"Developers looking for an efficient environment focused on {primary_use if primary_use else 'coding and project execution'}."
    }

def run_agent_skill(args: argparse.Namespace):
    output_dir = args.output_dir if args.output_dir else "content/custom"
    os.makedirs(output_dir, exist_ok=True)

    ide_data = create_ide_data_from_args(
        name=args.name,
        pricing=args.pricing,
        developer=args.developer,
        category=args.category,
        primary_use=args.primary_use
    )

    # Build AMP Blog Post
    blog_html = build_amp_html(ide_data)
    blog_filename = f"{ide_data['id']}_blog_post.html"
    blog_path = os.path.join(output_dir, blog_filename)
    with open(blog_path, "w", encoding="utf-8") as f:
        f.write(blog_html)

    # Build Google Flow Video Spec
    video_spec = build_google_flow_spec(ide_data)
    if args.aspect_ratio:
        video_spec["aspect_ratio"] = args.aspect_ratio

    spec_filename = f"{ide_data['id']}_google_flow_spec.json"
    spec_path = os.path.join(output_dir, spec_filename)
    with open(spec_path, "w", encoding="utf-8") as f:
        json.dump(video_spec, f, indent=2)

    print(f"Agentic skill execution completed successfully for '{args.name}':")
    print(f"  - AMP Blog Post: {blog_path}")
    print(f"  - Google Flow Spec: {spec_path}")

def main():
    parser = argparse.ArgumentParser(description="IDE Guide Agentic CLI Skill Tool for Custom Content Generation")
    parser.add_argument("--name", required=True, help="Name of the IDE, code editor, or repository")
    parser.add_argument("--pricing", default="Free / Open Source", help="Pricing model description (e.g. Free, Freemium $10/mo, Paid $99)")
    parser.add_argument("--developer", default="Software Community", help="Developer or organization name")
    parser.add_argument("--category", default="Code Editor", help="Software category")
    parser.add_argument("--primary-use", default="General Software Engineering", help="Primary target use case")
    parser.add_argument("--aspect-ratio", default="16:9", choices=["16:9", "9:16"], help="Video aspect ratio (16:9 for YouTube, 9:16 for Shorts)")
    parser.add_argument("--output-dir", default="content/custom", help="Output directory path")

    args = parser.parse_args()
    run_agent_skill(args)

if __name__ == "__main__":
    main()
