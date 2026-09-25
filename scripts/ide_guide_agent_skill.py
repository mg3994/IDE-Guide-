#!/usr/bin/env python3
"""
IDE Guide - Agentic Skill Tool
Allows on-demand generation of AMP HTML blog posts and Google Flow video specs
for any IDE name or GitHub repository URL.

Usage:
  python3 scripts/ide_guide_agent_skill.py --ide "Cursor" --output-dir "./custom_output"
  python3 scripts/ide_guide_agent_skill.py --repo "zed-industries/zed"
"""

import os
import sys
import argparse
import json
import datetime
from typing import Dict, Any, Optional

# Ensure repository root is on sys.path
REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from scripts.generate_daily_content import (
    generate_amp_blog_post,
    generate_google_flow_video_spec,
    IDE_DATABASE,
    DISCLAIMER_TEXT
)


def find_or_build_ide_spec(ide_name: Optional[str] = None, repo_url: Optional[str] = None) -> Dict[str, Any]:
    target_query = (ide_name or repo_url or "Custom Editor").lower()

    # Check if existing in built-in DB
    for ide in IDE_DATABASE:
        if ide["id"].lower() in target_query or ide["name"].lower() in target_query or ide["github_repo"].lower() in target_query:
            return ide

    # If not found, build dynamically based on input
    clean_title = ide_name or (repo_url.split("/")[-1].replace("-", " ").title() if repo_url else "Modern Code Editor")
    slug = clean_title.lower().replace(" ", "-")

    return {
        "id": slug,
        "name": clean_title,
        "developer": "Open Source Community / Independent Developer",
        "category": "Modern Code Editor",
        "license_type": "Open Source / Proprietary",
        "pricing": "Free Community Tier / Optional Enterprise License",
        "pros": [
            f"Optimized workflow and modern developer ergonomics for {clean_title}",
            "Extensible architecture with rich plugin / theme customization",
            "Fast responsiveness and modern UI layout"
        ],
        "cons": [
            "Ecosystem and extension registry still expanding",
            "Requires initial configuration for complex enterprise projects"
        ],
        "best_for": f"Software engineers and power users evaluating {clean_title}",
        "summary": f"A featured technical evaluation of {clean_title} code editor.",
        "rating": "4.5/5.0",
        "website": f"https://github.com/{repo_url}" if repo_url else "https://ideguide.blogspot.com/",
        "github_repo": repo_url or f"ideguide/{slug}"
    }


def validate_amp_html(html_content: str) -> bool:
    """Validates basic AMP HTML compliance rules"""
    checks = [
        "<!doctype html>" in html_content.lower(),
        "<html ⚡" in html_content or "<html amp" in html_content,
        '<script async src="https://cdn.ampproject.org/v0.js"></script>' in html_content,
        "<style amp-boilerplate>" in html_content,
        "<style amp-custom>" in html_content,
        "<img " not in html_content,  # Enforce amp-img over standard img tags
        "<amp-img " in html_content,
        DISCLAIMER_TEXT in html_content
    ]
    return all(checks)


def run_agentic_skill(
    ide_name: Optional[str] = None,
    repo: Optional[str] = None,
    output_dir: str = "output",
    output_format: str = "all",
    validate: bool = False
) -> Dict[str, Any]:
    os.makedirs(output_dir, exist_ok=True)
    date_str = datetime.datetime.now().strftime("%Y-%m-%d")

    ide = find_or_build_ide_spec(ide_name=ide_name, repo_url=repo)
    slug = ide["id"]

    results = {
        "ide_name": ide["name"],
        "output_directory": output_dir,
        "generated_files": [],
        "validation_passed": True
    }

    if output_format in ["all", "amp"]:
        amp_html = generate_amp_blog_post(ide, date_str, index=1)
        amp_file = os.path.join(output_dir, f"amp_{slug}_blog_post.html")
        with open(amp_file, "w", encoding="utf-8") as f:
            f.write(amp_html)
        results["generated_files"].append(amp_file)

        if validate:
            is_valid_amp = validate_amp_html(amp_html)
            if not is_valid_amp:
                results["validation_passed"] = False
                print(f"Validation Warning: {amp_file} failed AMP HTML rules check.")

    if output_format in ["all", "flow"]:
        flow_spec = generate_google_flow_video_spec(ide, date_str, index=1)
        flow_json_file = os.path.join(output_dir, f"flow_{slug}_video_spec.json")
        with open(flow_json_file, "w", encoding="utf-8") as f:
            json.dump(flow_spec, f, indent=2)
        results["generated_files"].append(flow_json_file)

        flow_md_file = os.path.join(output_dir, f"flow_{slug}_video_spec.md")
        flow_md_content = f"# Google Flow Video Spec: {ide['name']}\n\n"
        flow_md_content += f"> Channel: https://www.youtube.com/@IDEguide\n\n"
        flow_md_content += f"## Editorial Disclaimer\n{DISCLAIMER_TEXT}\n\n"
        flow_md_content += f"## 🎬 Shorts 60s Script & Flow Prompts\n"
        for s in flow_spec["youtube_shorts_spec_60s"]["scenes"]:
            flow_md_content += f"### Scene {s['scene_number']} ({s['timestamp']})\n"
            flow_md_content += f"- **Prompt:** `{s['google_flow_video_prompt']}`\n"
            flow_md_content += f"- **Voiceover:** \"{s['voiceover_script']}\"\n\n"

        with open(flow_md_file, "w", encoding="utf-8") as f:
            f.write(flow_md_content)
        results["generated_files"].append(flow_md_file)

    return results


def main():
    parser = argparse.ArgumentParser(description="IDE Guide Agentic Skill CLI")
    parser.add_argument("--ide", type=str, help="Name of the IDE/Editor to generate skills for (e.g., 'Cursor')")
    parser.add_argument("--repo", type=str, help="GitHub repo (e.g., 'zed-industries/zed')")
    parser.add_argument("--output-dir", type=str, default="output", help="Directory to save output artifacts")
    parser.add_argument("--format", type=str, choices=["all", "amp", "flow"], default="all", help="Output format")
    parser.add_argument("--validate", action="store_true", help="Run validation checks on generated files")

    args = parser.parse_args()

    if not args.ide and not args.repo:
        args.ide = "Cursor"  # Default fallback for testing

    print(f"🤖 IDE Guide Agentic Skill invoked for IDE: '{args.ide or args.repo}'...")
    res = run_agentic_skill(
        ide_name=args.ide,
        repo=args.repo,
        output_dir=args.output_dir,
        output_format=args.format,
        validate=args.validate
    )

    print("\n✅ Skill execution complete!")
    print(f"IDE Target: {res['ide_name']}")
    print("Files created:")
    for filepath in res["generated_files"]:
        print(f"  - {filepath}")


if __name__ == "__main__":
    main()
