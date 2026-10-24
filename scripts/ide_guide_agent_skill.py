#!/usr/bin/env python3
"""
Agentic Skill Tool for IDE Guide.
Generates custom AMP HTML blog posts and Google Flow video specs on demand
for any specified IDE name, tool, or GitHub repository URL.
"""

import sys
import argparse
import os
import json
import datetime
from scripts.amp_validator import validate_amp_html, REQUIRED_DISCLAIMER
from scripts.generate_daily_content import generate_amp_blog_html, generate_google_flow_video_spec, IDE_DATABASE


def generate_custom_ide_content(target: str, output_dir: str = ".") -> dict:
    """
    Generates AMP HTML and Google Flow Video Spec for a given target IDE or repository.
    """
    os.makedirs(output_dir, exist_ok=True)

    # Check if target matches existing IDE database entry or build dynamically
    target_key = None
    for k in IDE_DATABASE:
        if k.lower() in target.lower() or target.lower() in k.lower():
            target_key = k
            break

    if target_key:
        ide_data = IDE_DATABASE[target_key]
    else:
        # Build custom IDE entry from target name/repo
        clean_name = target.rstrip('/').split('/')[-1].replace('-', ' ').replace('_', ' ').title()
        slug = clean_name.lower().replace(' ', '-')
        ide_data = {
            "name": clean_name,
            "slug": slug,
            "pricing": "Free / Open Source Evaluation",
            "is_free": True,
            "tagline": f"Developer tool review and analysis for {clean_name}.",
            "pros": [
                f"Modern developer workflow integration for {clean_name}.",
                "Strong performance and customizable configuration options.",
                "Active developer community and ongoing updates."
            ],
            "cons": [
                "Requires initial setup to align with specialized project requirements.",
                "Ecosystem extensions still evolving."
            ],
            "best_for": f"Developers exploring {clean_name} for their development stack.",
            "image_url": "https://images.unsplash.com/photo-1555066931-4365d14bab8c?w=800&auto=format&fit=crop"
        }

    date_str = datetime.date.today().isoformat()
    canonical_url = f"https://ideguide.blogspot.com/{date_str.replace('-', '/')}/{ide_data['slug']}.html"

    # Generate Blog AMP HTML
    amp_html = generate_amp_blog_html(ide_data, canonical_url)
    is_valid, errs = validate_amp_html(amp_html)
    if not is_valid:
        raise ValueError(f"Generated AMP HTML failed validation: {errs}")

    html_path = os.path.join(output_dir, f"{ide_data['slug']}_amp.html")
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(amp_html)

    # Generate Video Spec
    video_spec = generate_google_flow_video_spec(ide_data)
    video_path = os.path.join(output_dir, f"{ide_data['slug']}_google_flow.json")
    with open(video_path, "w", encoding="utf-8") as f:
        json.dump(video_spec, f, indent=2)

    return {
        "ide_name": ide_data["name"],
        "html_file": html_path,
        "video_spec_file": video_path,
        "amp_valid": is_valid
    }


def main():
    parser = argparse.ArgumentParser(description="IDE Guide Agentic Skill - Generate AMP HTML & Google Flow Specs")
    parser.add_argument("--target", required=True, help="IDE Name or GitHub repository URL (e.g., 'Zed', 'https://github.com/vscodium/vscodium')")
    parser.add_argument("--output-dir", default="./custom_output", help="Directory to save generated assets")

    args = parser.parse_args()
    result = generate_custom_ide_content(args.target, args.output_dir)

    print(f"✨ Custom Content Generated Successfully for {result['ide_name']}:")
    print(f"  - AMP HTML Blog Post: {result['html_file']}")
    print(f"  - Google Flow Video Spec: {result['video_spec_file']}")


if __name__ == "__main__":
    main()
