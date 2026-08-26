#!/usr/bin/env python3
"""
IDE Guide Agentic Skill CLI Tool.
Generates targeted AMP HTML blog posts and Google Flow video generation specs
for custom IDEs or code editor GitHub repositories on-demand.
"""

import argparse
import datetime
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from generate_daily_content import (
    generate_amp_blog_post,
    generate_google_flow_spec,
    DISCLAIMER_TEXT
)


def create_custom_editor_profile(name, tagline, pricing, tech_stack, platforms, overview, features, getting_started, verdict, url):
    return {
        "name": name,
        "url": url,
        "tagline": tagline,
        "pricing": pricing,
        "tech_stack": tech_stack,
        "platforms": platforms,
        "overview": overview,
        "key_features": features,
        "getting_started": getting_started,
        "pricing_breakdown": pricing,
        "verdict": verdict,
        "hooks": f"Is {name} the ultimate tool for developers in 2026? Let's break it down!",
    }


def main():
    parser = argparse.ArgumentParser(description="IDE Guide Agentic Skill - Generate custom IDE content package.")
    parser.add_argument("--name", type=str, required=True, help="Name of the IDE or Code Editor")
    parser.add_argument("--tagline", type=str, default="Next-Generation Developer Tool", help="Short tagline")
    parser.add_argument("--pricing", type=str, default="Free & Open Source", help="Pricing information")
    parser.add_argument("--tech-stack", type=str, default="Multi-language, Web, Systems", help="Tech stack")
    parser.add_argument("--platforms", type=str, default="macOS, Linux, Windows", help="Supported platforms")
    parser.add_argument("--url", type=str, default="https://github.com", help="Official site or GitHub repository URL")
    parser.add_argument("--out-dir", type=str, default="content/custom", help="Output directory for generated files")

    args = parser.parse_args()

    overview = f"{args.name} is a modern code editing tool designed for optimal developer experience and high productivity."
    features = [
        f"Customizable workflow tailored for {args.tech_stack}",
        f"Cross-platform support across {args.platforms}",
        "Modern extension architecture and keyboard-centric design",
        "Active open-source community development"
    ]
    getting_started = [
        f"Download or install {args.name} from {args.url}.",
        "Configure your editor settings and keybindings.",
        "Open your workspace and start coding."
    ]
    verdict = f"Recommended for developers looking for high-efficiency tooling in {args.tech_stack}."

    profile = create_custom_editor_profile(
        name=args.name,
        tagline=args.tagline,
        pricing=args.pricing,
        tech_stack=args.tech_stack,
        platforms=args.platforms,
        overview=overview,
        features=features,
        getting_started=getting_started,
        verdict=verdict,
        url=args.url
    )

    os.makedirs(args.out_dir, exist_ok=True)
    slug = args.name.lower().replace(" ", "-")

    blog_html = generate_amp_blog_post(profile)
    flow_spec = generate_google_flow_spec(profile)

    blog_path = os.path.join(args.out_dir, f"{slug}-amp-blog.html")
    spec_path = os.path.join(args.out_dir, f"{slug}-google-flow-spec.md")

    with open(blog_path, "w", encoding="utf-8") as f:
        f.write(blog_html)

    with open(spec_path, "w", encoding="utf-8") as f:
        f.write(flow_spec)

    print(f"[+] Successfully generated Agentic Skill content for '{args.name}'")
    print(f"    AMP Blog Post: {blog_path}")
    print(f"    Google Flow Spec: {spec_path}")


if __name__ == "__main__":
    main()
