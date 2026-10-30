#!/usr/bin/env python3
"""IDE Guide Agent Skill CLI.

Agentic tool allowing AI agents or human operators to generate tailored AMP Blogger
posts and Google Flow video production packages on demand for any specified IDE,
code editor, or GitHub repository URL.
"""

import argparse
import sys
import os
import json
from typing import Dict, Any

# Ensure project root is in sys.path when invoked directly as a standalone script
REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from data.ide_database import IDE_CATALOG, get_ide_by_name, get_all_ide_names
from scripts.generate_daily_content import (
    generate_amp_blog_post,
    generate_flow_video_spec,
    DISCLAIMER_TEXT,
)
from scripts.amp_validator import validate_amp_blogger_content


def generate_custom_ide_data(name: str, url: str = None, category: str = None) -> Dict[str, Any]:
    """Generate intelligent default metadata for an IDE not currently in the catalog."""
    return {
        "name": name,
        "tagline": f"The Modern Code Editor Designed for Developer Velocity",
        "category": category or "Integrated Development Environment",
        "pricing_model": "Open Source / Community",
        "pricing_details": "Free community edition with optional developer extensions.",
        "is_paid": False,
        "has_free_tier": True,
        "is_open_source": True,
        "official_url": url or f"https://github.com/search?q={name}",
        "pros": [
            f"Optimized keyboard-centric workflows tailored for {name}",
            "Strong developer productivity features with responsive editing",
            "Active community and growing package/theme ecosystem",
            "Cross-platform support across Linux, macOS, and Windows",
        ],
        "cons": [
            "Configuration may require technical familiarity with modern developer toolchains",
            "Ecosystem maturity still expanding compared to legacy monolithic IDEs",
            "Resource usage varies depending on active project size and plugins",
        ],
        "best_for": "Developers seeking an adaptable, high-efficiency editor that matches their custom engineering workflow.",
        "visual_theme": "Modern high-contrast dark theme, neon syntax accents, ultra-sharp typography",
        "flow_broll_prompt": f"Cinematic slow dolly-in shot of a developer's workstation showing {name} displaying clean syntax highlighting on an OLED monitor with ambient teal studio rim lighting.",
    }


def main():
    parser = argparse.ArgumentParser(
        description="IDE Guide Agent Skill: Generate AMP Blogger content and Google Flow video specs."
    )
    parser.add_argument(
        "--ide",
        type=str,
        help="Name of the IDE/code editor to analyze (e.g. 'Cursor', 'VS Code', 'Zed').",
    )
    parser.add_argument(
        "--repo-url",
        type=str,
        default=None,
        help="Optional GitHub or official repository URL for new or custom editors.",
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default="generated_skills_output",
        help="Directory to save generated outputs (default: 'generated_skills_output').",
    )
    parser.add_argument(
        "--list-catalog",
        action="store_true",
        help="List all known pre-configured IDEs in the database.",
    )
    parser.add_argument(
        "--shorts-only",
        action="store_true",
        help="Generate only YouTube Shorts (9:16) video specifications.",
    )

    args = parser.parse_args()

    if args.list_catalog:
        print("Cataloged IDEs in IDE Guide Database:")
        for name in get_all_ide_names():
            print(f" - {name}")
        sys.exit(0)

    if not args.ide:
        parser.print_help()
        sys.exit(1)

    # Resolve IDE data
    try:
        ide_data = get_ide_by_name(args.ide)
        print(f"[Agent Skill] Found pre-configured entry for '{ide_data['name']}' in catalog.")
    except KeyError:
        print(f"[Agent Skill] IDE '{args.ide}' not in static catalog. Synthesizing custom model...")
        ide_data = generate_custom_ide_data(name=args.ide, url=args.repo_url)

    os.makedirs(args.output_dir, exist_ok=True)
    safe_name = ide_data["name"].lower().replace(" ", "_").replace("(", "").replace(")", "")

    # 1. Generate AMP Blog Post
    amp_post_html = generate_amp_blog_post(ide_data)
    is_valid, validation_errors = validate_amp_blogger_content(amp_post_html)
    if not is_valid:
        print(f"[Error] Generated AMP post failed validation: {validation_errors}", file=sys.stderr)
        sys.exit(2)

    post_output_path = os.path.join(args.output_dir, f"{safe_name}_amp_blogger_post.html")
    with open(post_output_path, "w", encoding="utf-8") as f:
        f.write(amp_post_html)
    print(f"[Success] AMP Blogger Post written to: {post_output_path}")

    # 2. Generate Google Flow Specs
    if not args.shorts_only:
        flow_spec_16_9 = generate_flow_video_spec(ide_data, is_short=False)
        video_out_path = os.path.join(args.output_dir, f"{safe_name}_google_flow_16x9.json")
        with open(video_out_path, "w", encoding="utf-8") as f:
            json.dump(flow_spec_16_9, f, indent=2)
        print(f"[Success] Google Flow 16:9 Video Spec written to: {video_out_path}")

    flow_shorts_spec = generate_flow_video_spec(ide_data, is_short=True)
    shorts_out_path = os.path.join(args.output_dir, f"{safe_name}_google_flow_shorts_9x16.json")
    with open(shorts_out_path, "w", encoding="utf-8") as f:
        json.dump(flow_shorts_spec, f, indent=2)
    print(f"[Success] Google Flow Shorts (9:16) Spec written to: {shorts_out_path}")


if __name__ == "__main__":
    main()
