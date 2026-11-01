#!/usr/bin/env python3
"""
IDE Guide - Agentic Skill CLI.

Allows autonomous agents and human developers to on-demand synthesize:
1. Blogger AMP-compliant blog post HTML
2. Google Flow Video specification & YouTube script

Usage:
  python3 scripts/ide_guide_agent_skill.py --name "Cursor"
  python3 scripts/ide_guide_agent_skill.py --list
  python3 scripts/ide_guide_agent_skill.py --custom --name "Zed" --out-dir ./custom_output
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Any, Dict, Optional

# Ensure repository root is in python path
ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

from scripts.generate_daily_content import (
    DATA_PATH,
    DISCLAIMER_TEXT,
    generate_amp_blog_post,
    generate_google_flow_video_spec,
    load_database,
)
from scripts.amp_validator import validate_amp_blogger_content


def find_editor_by_name(name_query: str) -> Optional[Dict[str, Any]]:
    db = load_database()
    name_clean = name_query.strip().lower()
    for editor in db.get("editors", []):
        if (
            name_clean == editor["id"].lower()
            or name_clean in editor["name"].lower()
            or editor["name"].lower() in name_clean
        ):
            return editor
    return None


def generate_for_editor(
    editor_data: Dict[str, Any],
    out_dir: Path,
    date_str: str = "2026-11-01",
) -> Dict[str, str]:
    out_dir.mkdir(parents=True, exist_ok=True)
    ed_id = editor_data["id"]

    # 1. Generate AMP HTML
    amp_html = generate_amp_blog_post(editor_data, date_str)
    blog_file = out_dir / f"{ed_id}_blogger_amp.html"
    with open(blog_file, "w", encoding="utf-8") as f:
        f.write(amp_html)

    # Validate AMP
    is_valid, errors, _ = validate_amp_blogger_content(amp_html)
    if not is_valid:
        raise ValueError(f"Generated AMP failed validation: {errors}")

    # 2. Generate Google Flow Video Spec
    flow_spec = generate_google_flow_video_spec(editor_data, date_str)
    video_file = out_dir / f"{ed_id}_google_flow_spec.json"
    with open(video_file, "w", encoding="utf-8") as f:
        json.dump(flow_spec, f, indent=2)

    return {
        "blog_path": str(blog_file),
        "video_path": str(video_file),
        "disclaimer_present": DISCLAIMER_TEXT in amp_html and flow_spec["metadata"]["disclaimer"] == DISCLAIMER_TEXT,
    }


def main():
    parser = argparse.ArgumentParser(
        description="IDE Guide Agentic Skill CLI - Generates Blogger AMP content & Google Flow video prompts."
    )
    parser.add_argument("--name", "-n", type=str, help="Name or ID of the editor to generate for (e.g. Cursor, Zed, VS Code)")
    parser.add_argument("--list", "-l", action="store_true", help="List all available IDEs in the catalog")
    parser.add_argument("--out-dir", "-o", type=str, default="./agent_output", help="Output directory for generated assets")
    parser.add_argument("--date", "-d", type=str, default=None, help="Target publication date (YYYY-MM-DD)")

    args = parser.parse_args()

    if args.list:
        db = load_database()
        print(f"Available IDEs and Code Editors ({len(db['editors'])} total):")
        for e in db["editors"]:
            pricing = "FREE" if e["pricing"]["is_free"] else f"PAID ({e['pricing']['tier']})"
            print(f"  • {e['name']} [{e['id']}] - {pricing} - {e['category']}")
        return

    if not args.name:
        parser.print_help()
        sys.exit(1)

    editor = find_editor_by_name(args.name)
    if not editor:
        print(f"Error: Editor '{args.name}' not found in database.", file=sys.stderr)
        print("Tip: Run with --list to see all available IDEs.", file=sys.stderr)
        sys.exit(1)

    from datetime import datetime
    date_str = args.date or datetime.now().strftime("%Y-%m-%d")
    out_path = Path(args.out_dir)

    print(f"Synthesizing content package for '{editor['name']}'...")
    results = generate_for_editor(editor, out_path, date_str=date_str)

    print("\nGeneration Successful!")
    print(f"  Blogger AMP HTML : {results['blog_path']}")
    print(f"  Google Flow Spec : {results['video_path']}")
    print(f"  Independent Disclaimer Verified: {results['disclaimer_present']}")


if __name__ == "__main__":
    main()
