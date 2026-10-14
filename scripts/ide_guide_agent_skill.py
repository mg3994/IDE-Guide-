#!/usr/bin/env python3
import argparse
import os
import sys
import json
import re
from pathlib import Path

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from scripts.amp_validator import validate_amp_html, REQUIRED_DISCLAIMER
from scripts.generate_daily_content import generate_amp_blog_post, generate_video_spec, generate_video_spec_markdown, IDE_POOL

def parse_args():
    parser = argparse.ArgumentParser(description="IDE Guide Agentic Skill - Generate custom AMP Blog Post and Google Flow Video Specs")
    parser.add_argument("--ide", type=str, help="Name of the IDE or Code Editor")
    parser.add_argument("--repo-url", type=str, help="Repository URL (e.g., https://github.com/zed-industries/zed)")
    parser.add_argument("--output-dir", type=str, default="content/custom", help="Output directory for generated files")
    parser.add_argument("--pricing", type=str, default="Freemium / Open Source", help="Pricing information")
    return parser.parse_args()

def extract_name_from_repo(repo_url: str) -> str:
    cleaned = repo_url.rstrip("/")
    repo_name = cleaned.split("/")[-1]
    return repo_name.replace("-", " ").replace("_", " ").title()

def get_or_create_ide_meta(ide_name: str, pricing: str) -> dict:
    slug = re.sub(r'[^a-z0-9]+', '-', ide_name.lower()).strip('-')

    # Check if in IDE_POOL
    for existing in IDE_POOL:
        if existing['slug'] == slug or existing['name'].lower() == ide_name.lower():
            return existing

    # Default fallback construct
    return {
        "name": ide_name,
        "slug": slug,
        "tagline": f"Modern Developer Tools & Workflow for {ide_name}",
        "pricing": pricing,
        "pros": [f"High performance workflow optimized for {ide_name}", "Active developer community and ecosystem", "Modern customizable user interface"],
        "cons": ["Ecosystem extensions in active development", "Learning curve for specific advanced configurations"],
        "best_for": f"Developers looking for modern, scalable workflows with {ide_name}.",
        "category": "Code Editor / IDE"
    }

def main():
    args = parse_args()

    if not args.ide and not args.repo_url:
        print("Error: You must specify either --ide or --repo-url")
        sys.exit(1)

    ide_name = args.ide
    if not ide_name and args.repo_url:
        ide_name = extract_name_from_repo(args.repo_url)

    ide_meta = get_or_create_ide_meta(ide_name, args.pricing)

    out_dir = PROJECT_ROOT / args.output_dir
    out_dir.mkdir(parents=True, exist_ok=True)

    slug = ide_meta['slug']

    # 1. Generate AMP HTML blog post
    amp_html = generate_amp_blog_post(ide_meta)
    blog_path = out_dir / f"blog_post_{slug}.amp.html"
    with open(blog_path, 'w', encoding='utf-8') as f:
        f.write(amp_html)

    # 2. Generate Google Flow video spec JSON
    spec = generate_video_spec(ide_meta)
    spec_path = out_dir / f"video_spec_{slug}.json"
    with open(spec_path, 'w', encoding='utf-8') as f:
        json.dump(spec, f, indent=2)

    # 3. Generate Google Flow video spec Markdown
    spec_md = generate_video_spec_markdown(spec)
    spec_md_path = out_dir / f"video_spec_{slug}.md"
    with open(spec_md_path, 'w', encoding='utf-8') as f:
        f.write(spec_md)

    print(f"🚀 IDE Guide Skill Execution Successful for '{ide_meta['name']}':")
    print(f"  - AMP Blog Post: {blog_path.relative_to(PROJECT_ROOT)}")
    print(f"  - Video Spec JSON: {spec_path.relative_to(PROJECT_ROOT)}")
    print(f"  - Video Spec MD: {spec_md_path.relative_to(PROJECT_ROOT)}")

if __name__ == "__main__":
    main()
