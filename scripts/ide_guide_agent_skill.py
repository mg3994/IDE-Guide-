#!/usr/bin/env python3
"""
Agentic Skill Tool for IDE Guide.
Provides command-line interface and reusable python module functions to generate:
- AMP HTML compliant blog posts for Blogger (https://ideguide.blogspot.com/)
- Google Flow video prompt specifications for YouTube (@IDEguide)

Allows generating content on-demand for custom IDEs, repo URLs, or standard daily batches.
"""

import argparse
import json
import os
import sys
from datetime import datetime, timezone
from typing import Dict, Any, Optional

from scripts.generate_daily_content import (
    IDE_DATABASE,
    generate_amp_blog_post,
    generate_google_flow_spec,
    DISCLAIMER_TEXT,
)


def create_custom_ide_entry(
    name: str,
    developer: str = "Independent / Community",
    pricing_type: str = "Free / Freemium",
    is_free: bool = True,
    pricing_details: str = "Free tier or open source license available.",
    languages: Optional[list] = None,
    pros: Optional[list] = None,
    cons: Optional[list] = None,
    best_for: str = "Developers seeking customized workflow solutions.",
    image_url: str = "https://images.unsplash.com/photo-1555066931-4365d14bab8c?w=800&auto=format&fit=crop&q=80"
) -> Dict[str, Any]:
    safe_id = name.lower().replace(" ", "_").replace("-", "_")
    return {
        "id": safe_id,
        "name": name,
        "developer": developer,
        "pricing_type": pricing_type,
        "is_free": is_free,
        "pricing_details": pricing_details,
        "languages": languages or ["General Purpose", "Web", "Systems"],
        "pros": pros or [
            "Extensible architecture with rich plugin capabilities",
            "High performance code navigation and syntax parsing",
            "Active developer community and frequent updates"
        ],
        "cons": cons or [
            "Initial configuration curve for custom setups",
            "Resource usage depends on active extension ecosystem"
        ],
        "best_for": best_for,
        "image_url": image_url
    }


def find_ide_by_name(query: str) -> Optional[Dict[str, Any]]:
    query_lower = query.lower()
    for ide in IDE_DATABASE:
        if query_lower in ide["name"].lower() or query_lower in ide["id"].lower():
            return ide
    return None


def run_agentic_skill(
    target_ide: str,
    output_dir: str = "content/custom",
    is_free: bool = True,
    pricing_details: Optional[str] = None
) -> Dict[str, str]:
    os.makedirs(output_dir, exist_ok=True)
    date_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    found = find_ide_by_name(target_ide)
    if not found:
        print(f"ℹ️ IDE '{target_ide}' not in built-in database. Constructing custom agent entry...")
        found = create_custom_ide_entry(
            name=target_ide,
            is_free=is_free,
            pricing_details=pricing_details or ("100% Free Open Source Tool" if is_free else "Freemium / Paid Tier Available")
        )

    # Generate AMP HTML Post
    amp_html = generate_amp_blog_post(found, date_str)
    blog_path = os.path.join(output_dir, f"blog_{found['id']}.html")
    with open(blog_path, "w", encoding="utf-8") as f:
        f.write(amp_html)

    # Generate Google Flow Spec
    flow_spec = generate_google_flow_spec(found, date_str)
    flow_path = os.path.join(output_dir, f"video_flow_{found['id']}.json")
    with open(flow_path, "w", encoding="utf-8") as f:
        json.dump(flow_spec, f, indent=2)

    return {"blog_path": blog_path, "flow_path": flow_path}


def main():
    parser = argparse.ArgumentParser(
        description="IDE Guide Agentic Skill: On-demand AMP Blog Post & Google Flow Video Spec Generator."
    )
    parser.add_argument("--ide", type=str, help="Name of the IDE/Editor to generate content for (e.g. 'Cursor', 'Sublime Text', 'Zed').")
    parser.add_argument("--output-dir", type=str, default="content/custom", help="Directory to save generated outputs.")
    parser.add_argument("--paid", action="store_true", help="Mark tool as paid/freemium (default is free).")
    parser.add_argument("--pricing-details", type=str, help="Custom pricing description string.")

    args = parser.parse_args()

    if not args.ide:
        print("Usage: python3 scripts/ide_guide_agent_skill.py --ide '<IDE_NAME>' [--paid] [--pricing-details '...']")
        sys.exit(1)

    result = run_agentic_skill(
        target_ide=args.ide,
        output_dir=args.output_dir,
        is_free=not args.paid,
        pricing_details=args.pricing_details
    )

    print(f"✨ Agentic Skill Execution Finished for '{args.ide}':")
    print(f"  - AMP Blog Post: {result['blog_path']}")
    print(f"  - Google Flow Video Spec: {result['flow_path']}")


if __name__ == "__main__":
    main()
