#!/usr/bin/env python3
"""
Agentic CLI Skill Tool for IDE Guide.
Generates on-demand custom AMP HTML blog post and Google Flow video specs
for any given IDE name or Repository URL.
"""

import sys
import os
import argparse
import json

# Ensure project root is in python path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from scripts.generate_daily_content import (
    generate_amp_blog_post,
    generate_google_flow_spec,
    generate_video_markdown_script,
    REQUIRED_DISCLAIMER
)
from scripts.amp_validator import validate_amp_html

def build_custom_ide_data(name_or_url: str, pricing: str = "Free / Freemium") -> dict:
    """Constructs structured data for custom requested IDE or Repo."""
    clean_name = name_or_url.split("/")[-1].replace(".git", "").replace("-", " ").title()
    ide_id = clean_name.lower().replace(" ", "-")

    return {
        "id": ide_id,
        "name": clean_name,
        "vendor": "Open Source / Developer Team" if "github" in name_or_url.lower() else "Software Vendor",
        "category": "Code Editor / IDE",
        "pricing_type": pricing,
        "pricing_details": f"{pricing} - See official website for license terms.",
        "target_audience": "Software Developers, Open Source Contributors, Engineering Teams",
        "pros": [
          f"Modern developer workflows for {clean_name}",
          "Extensible architecture and active developer community",
          "Snappy performance and customized development tools"
        ],
        "cons": [
          "Requires setup for specialized enterprise toolchains",
          "Ecosystem documentation continuously expanding"
        ],
        "verdict": f"A promising editor option for developers interested in {clean_name}.",
        "key_features": ["Syntax Highlighting", "Git Integration", "Plugin Support", "Terminal Access"],
        "tags": ["custom", "ide", "agentic-skill"]
    }

def main():
    parser = argparse.ArgumentParser(description="IDE Guide Agentic CLI Skill Tool")
    parser.add_argument("--ide", type=str, required=True, help="IDE Name or Repository URL")
    parser.add_argument("--pricing", type=str, default="Free / Freemium", help="Pricing details (e.g. Free, $15/mo)")
    parser.add_argument("--output-dir", type=str, default="content/custom", help="Output directory path")

    args = parser.parse_args()

    os.makedirs(args.output_dir, exist_ok=True)
    ide_data = build_custom_ide_data(args.ide, args.pricing)

    # 1. AMP Blog Post
    blog_html = generate_amp_blog_post(ide_data)
    is_valid, errors = validate_amp_html(blog_html)
    if not is_valid:
        print(f"⚠️ Warning: AMP HTML validation warnings for custom input: {errors}")

    blog_file = os.path.join(args.output_dir, f"blog_post_{ide_data['id']}.html")
    with open(blog_file, "w", encoding="utf-8") as f:
        f.write(blog_html)

    # 2. Google Flow Spec JSON
    flow_spec = generate_google_flow_spec(ide_data)
    spec_file = os.path.join(args.output_dir, f"video_spec_{ide_data['id']}.json")
    with open(spec_file, "w", encoding="utf-8") as f:
        json.dump(flow_spec, f, indent=2)

    # 3. Video Script Markdown
    script_md = generate_video_markdown_script(ide_data, flow_spec)
    script_file = os.path.join(args.output_dir, f"video_script_{ide_data['id']}.md")
    with open(script_file, "w", encoding="utf-8") as f:
        f.write(script_md)

    print(f"🎉 Successfully generated custom content for '{ide_data['name']}':")
    print(f"   - Blog (AMP): {blog_file}")
    print(f"   - Video Spec: {spec_file}")
    print(f"   - Script:     {script_file}")

if __name__ == "__main__":
    main()
