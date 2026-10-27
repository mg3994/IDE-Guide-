#!/usr/bin/env python3
"""
IDE Guide Agentic CLI Skill Tool.
Generates customized AMP HTML blog posts and Google Flow video specs on demand
for any specified IDE name, repository URL, or custom feature description.
"""

import sys
import argparse
import os
import yaml
from datetime import datetime
from scripts.amp_validator import validate_amp_html, REQUIRED_DISCLAIMER
from scripts.generate_daily_content import build_amp_html, build_google_flow_spec

def main():
    parser = argparse.ArgumentParser(description="IDE Guide Agentic Content Tool")
    parser.add_argument("--ide", required=True, help="Name of the IDE or Code Editor")
    parser.add_argument("--repo", help="Optional repository URL or web URL")
    parser.add_argument("--pricing", default="Free / Open Source", help="Pricing model (e.g. Free, Freemium, Paid)")
    parser.add_argument("--category", default="Developer Tools", help="Category / Tech domain")
    parser.add_argument("--pros", nargs="+", default=["Fast startup time", "Extensible architecture"], help="List of pros")
    parser.add_argument("--cons", nargs="+", default=["Learning curve for beginners"], help="List of cons")
    parser.add_argument("--verdict", default="Recommended editor for specialized workflows.", help="Final verdict recommendation")
    parser.add_argument("--out-dir", default="content/custom", help="Output directory")

    args = parser.parse_args()

    slug = args.ide.lower().replace(" ", "-").replace("/", "-")
    ide_dict = {
        "name": args.ide,
        "slug": slug,
        "pricing": args.pricing,
        "category": args.category,
        "pros": args.pros,
        "cons": args.cons,
        "verdict": args.verdict
    }

    os.makedirs(args.out_dir, exist_ok=True)

    # 1. Build AMP HTML Blog Post
    amp_html = build_amp_html(ide_dict)
    valid, errors = validate_amp_html(amp_html)
    if not valid:
        print(f"❌ AMP Validation Error for {args.ide}: {errors}")
        sys.exit(1)

    amp_path = os.path.join(args.out_dir, f"{slug}_post.html")
    with open(amp_path, "w", encoding="utf-8") as f:
        f.write(amp_html)

    # 2. Build Google Flow Video Spec
    spec_dict = build_google_flow_spec(ide_dict)
    if args.repo:
        spec_dict["meta"]["repository_url"] = args.repo

    spec_path = os.path.join(args.out_dir, f"{slug}_video_spec.yaml")
    with open(spec_path, "w", encoding="utf-8") as f:
        yaml.dump(spec_dict, f, sort_keys=False)

    print(f"✅ Successfully generated custom AMP post and Google Flow spec:")
    print(f"  - Blog Post (AMP HTML): {amp_path}")
    print(f"  - Video Spec (Google Flow): {spec_path}")

if __name__ == "__main__":
    main()
