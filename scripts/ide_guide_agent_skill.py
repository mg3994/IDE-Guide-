#!/usr/bin/env python3
"""
IDE Guide Agentic CLI Skill Tool.
Enables agents and users to generate custom AMP HTML blog posts and Google Flow AI video specs
for any specific IDE or repository URL on demand.
"""

import argparse
import json
import os
import sys
from datetime import datetime, timezone
from typing import Dict, Any

# Allow execution both as module and direct script
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from scripts.generate_daily_content import (
    generate_amp_blog_post,
    generate_google_flow_spec,
    DISCLAIMER_TEXT,
)


def build_custom_ide_data(
    name: str,
    category: str = "Code Editor",
    pricing: str = "Free",
    repo_url: str = None,
    pros: list = None,
    cons: list = None,
    target_audience: str = "Developers",
    killer_features: list = None,
) -> Dict[str, Any]:
    return {
        "name": name,
        "category": category,
        "pricing": pricing,
        "license_type": "Free" if "free" in pricing.lower() else "Paid",
        "repo_url": repo_url or "",
        "pros": pros or [f"High performance for {name}", "Modern developer experience", "Extensible architecture"],
        "cons": cons or ["Requires initial environment configuration", "Ecosystem actively evolving"],
        "target_audience": target_audience,
        "killer_features": killer_features or ["Smart Autocomplete", "Fast Navigation", "Custom Extensions"],
    }


def run_agent_skill(args: argparse.Namespace) -> None:
    ide_data = build_custom_ide_data(
        name=args.ide_name,
        category=args.category,
        pricing=args.pricing,
        repo_url=args.repo_url,
        pros=args.pros.split(",") if args.pros else None,
        cons=args.cons.split(",") if args.cons else None,
        target_audience=args.target_audience,
        killer_features=args.killer_features.split(",") if args.killer_features else None,
    )

    output_dir = args.output_dir or f"content/custom_{datetime.now(timezone.utc).strftime('%Y-%m-%d')}"
    os.makedirs(output_dir, exist_ok=True)

    slug = args.ide_name.lower().replace(" ", "_").replace("/", "_")

    # 1. AMP Blog Post
    blog_html = generate_amp_blog_post(ide_data)
    blog_path = os.path.join(output_dir, f"blogpost_{slug}.html")
    with open(blog_path, "w", encoding="utf-8") as f:
        f.write(blog_html)

    # 2. Google Flow Video Spec
    flow_spec = generate_google_flow_spec(ide_data)
    if args.repo_url:
        flow_spec["repo_url"] = args.repo_url
    flow_path = os.path.join(output_dir, f"video_flow_spec_{slug}.json")
    with open(flow_path, "w", encoding="utf-8") as f:
        json.dump(flow_spec, f, indent=2)

    print(f"[AGENT SKILL SUCCESS] Generated custom assets for '{args.ide_name}':")
    print(f"  - AMP Blog Post: {blog_path}")
    print(f"  - Google Flow Spec: {flow_path}")


def main():
    parser = argparse.ArgumentParser(description="IDE Guide Agentic CLI Skill Generator")
    parser.add_argument("--ide-name", required=True, help="Name of the IDE or Code Editor")
    parser.add_argument("--category", default="Code Editor / IDE", help="IDE Category")
    parser.add_argument("--pricing", default="Free", help="Pricing model (Free, Paid, Freemium)")
    parser.add_argument("--repo-url", default="", help="Optional GitHub repository URL")
    parser.add_argument("--pros", help="Comma-separated pros list")
    parser.add_argument("--cons", help="Comma-separated cons list")
    parser.add_argument("--target-audience", default="Software Developers", help="Target user description")
    parser.add_argument("--killer-features", help="Comma-separated killer features list")
    parser.add_argument("--output-dir", help="Directory to save generated outputs")

    args = parser.parse_args()
    run_agent_skill(args)


if __name__ == "__main__":
    main()
