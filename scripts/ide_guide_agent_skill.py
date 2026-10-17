#!/usr/bin/env python3
"""
IDE Guide Agentic CLI Skill Tool.
Allows on-demand generation of custom AMP HTML blog posts and Google Flow video specs
for specific IDE names or custom repo URLs provided via CLI parameters.
"""

import argparse
import json
import sys
import os

# Support running script directly or as a package
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from scripts.generate_daily_content import generate_amp_blog_post, generate_google_flow_spec

def build_custom_ide_data(name: str, repo_url: str = "", pricing: str = "Free", category: str = "Code Editor / IDE") -> dict:
    clean_id = name.lower().replace(" ", "_").replace("-", "_")
    return {
        "id": clean_id,
        "name": name,
        "category": category,
        "pricing_type": pricing,
        "price_detail": f"Details for {name} ({'Repository: ' + repo_url if repo_url else 'Standard release'}).",
        "pros": [
            f"Tailored for efficient {category.lower()} workflows",
            "Extensible architecture and modern development features",
            "Active community support and regular software updates"
        ],
        "cons": [
            "Requires initial setup and workflow adjustment",
            "Resource usage varies based on project size and active extensions"
        ],
        "best_for": f"Developers looking for a modern {category} solution with customizable project options."
    }

def main():
    parser = argparse.ArgumentParser(description="IDE Guide Agentic Skill - Generate custom AMP blog posts & Flow video specs.")
    parser.add_argument("--name", required=True, help="Name of the IDE or Code Editor")
    parser.add_argument("--repo", default="", help="Optional repository URL")
    parser.add_argument("--pricing", default="Free", help="Pricing model (Free, Paid, Freemium, Open Source)")
    parser.add_argument("--category", default="Code Editor / IDE", help="Category of tool")
    parser.add_argument("--outdir", default="content/custom", help="Output directory")

    args = parser.parse_args()

    ide_data = build_custom_ide_data(args.name, args.repo, args.pricing, args.category)
    os.makedirs(args.outdir, exist_ok=True)

    blog_html = generate_amp_blog_post(ide_data)
    blog_file = os.path.join(args.outdir, f"{ide_data['id']}_blog.amp.html")
    with open(blog_file, "w", encoding="utf-8") as f:
        f.write(blog_html)

    flow_spec = generate_google_flow_spec(ide_data)
    spec_file = os.path.join(args.outdir, f"{ide_data['id']}_flow_spec.json")
    with open(spec_file, "w", encoding="utf-8") as f:
        json.dump(flow_spec, f, indent=2)

    print(f"Agentic skill successfully generated content for '{args.name}':")
    print(f"  - Blog Post (AMP): {blog_file}")
    print(f"  - Video Spec (Flow): {spec_file}")

if __name__ == "__main__":
    main()
