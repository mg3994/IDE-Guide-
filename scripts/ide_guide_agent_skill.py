#!/usr/bin/env python3
"""
IDE Guide Agentic Skill CLI Tool.
Generates AMP-compliant Blogger posts and Google Flow video generation specifications
for any specified IDE or Code Editor on demand.
"""

import argparse
import json
import os
import sys
from datetime import datetime

REQUIRED_DISCLAIMER = (
    "Disclaimer: IDE Guide is an independent technical publication. "
    "This content is not sponsored, endorsed, or affiliated with any "
    "software vendor or editor developer mentioned above. "
    "All reviews and assessments are based strictly on objective developer evaluation."
)


def generate_amp_blog_post(ide_name: str, details: dict = None) -> str:
    """
    Generates fully compliant AMP HTML blog post for Blogger.
    """
    if details is None:
        details = {
            "pricing": "Free Community Edition / Paid Pro License available",
            "category": "Modern Code Editor / IDE",
            "pros": [
                "Advanced AI-assisted code autocompletion and contextual understanding",
                "Extensive plugin ecosystem and customization capabilities",
                "Fast startup and lightweight memory footprint"
            ],
            "cons": [
                "Some advanced features require active internet connection",
                "Paid subscription needed for full cloud model features"
            ],
            "best_for": "Full-stack developers and software engineers looking for peak productivity",
            "image_url": "https://images.unsplash.com/photo-1555066931-4365d14bab8c?w=800&auto=format&fit=crop"
        }

    pros_html = "".join([f"<li>{pro}</li>" for pro in details["pros"]])
    cons_html = "".join([f"<li>{con}</li>" for con in details["cons"]])

    html = f"""<!doctype html>
<html ⚡ lang="en">
<head>
  <meta charset="utf-8">
  <title>{ide_name} - Objective Review, Pricing & Guide | IDE Guide</title>
  <link rel="canonical" href="https://ideguide.blogspot.com/{ide_name.lower().replace(' ', '-')}-review">
  <meta name="viewport" content="width=device-width,minimum-scale=1,initial-scale=1">
  <style amp-boilerplate>body{{-webkit-animation:-amp-start 8s steps(1,end) 0s 1 normal part; -moz-animation:-amp-start 8s steps(1,end) 0s 1 normal part; -ms-animation:-amp-start 8s steps(1,end) 0s 1 normal part; animation:-amp-start 8s steps(1,end) 0s 1 normal part}}@-webkit-keyframes -amp-start{{from{{visibility:hidden}}to{{visibility:visible}}}}@-moz-keyframes -amp-start{{from{{visibility:hidden}}to{{visibility:visible}}}}@-ms-keyframes -amp-start{{from{{visibility:hidden}}to{{visibility:visible}}}}@-o-keyframes -amp-start{{from{{visibility:hidden}}to{{visibility:visible}}}}@keyframes -amp-start{{from{{visibility:hidden}}to{{visibility:visible}}}}</style><noscript><style amp-boilerplate>body{{-webkit-animation:none;-moz-animation:none;-ms-animation:none;animation:none}}</style></noscript>
  <script async src="https://cdn.ampproject.org/v0.js"></script>
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "TechArticle",
    "headline": "{ide_name} Review: Features, Pricing & Comparison",
    "author": {{
      "@type": "Organization",
      "name": "IDE Guide"
    }},
    "publisher": {{
      "@type": "Organization",
      "name": "IDE Guide",
      "url": "https://ideguide.blogspot.com/"
    }}
  }}
  </script>
</head>
<body>
  <article class="blog-post">
    <header>
      <h1>{ide_name} Deep Dive Review: Is It Worth It?</h1>
      <p class="meta">Published by IDE Guide | Category: {details['category']}</p>
    </header>

    <amp-img src="{details['image_url']}" width="800" height="450" layout="responsive" alt="{ide_name} Interface Showcase"></amp-img>

    <section class="overview">
      <h2>Overview</h2>
      <p>Welcome to <strong>IDE Guide</strong>. Today we are exploring <strong>{ide_name}</strong>. Choosing the right development environment directly impacts your coding speed, debugging efficiency, and developer overall comfort.</p>
    </section>

    <section class="pricing">
      <h2>Pricing & License Status</h2>
      <p><strong>Pricing Status:</strong> {details['pricing']}</p>
    </section>

    <section class="pros-cons">
      <h2>Pros & Cons Breakdown</h2>
      <div class="pros">
        <h3>The Good (Pros)</h3>
        <ul>
          {pros_html}
        </ul>
      </div>
      <div class="cons">
        <h3>The Bad (Cons)</h3>
        <ul>
          {cons_html}
        </ul>
      </div>
    </section>

    <section class="verdict">
      <h2>Final Verdict: Who Should Use {ide_name}?</h2>
      <p>{details['best_for']}</p>
    </section>

    <footer class="disclaimer-box">
      <hr>
      <p><strong>{REQUIRED_DISCLAIMER}</strong></p>
    </footer>
  </article>
</body>
</html>"""
    return html


def generate_google_flow_video_spec(ide_name: str, details: dict = None) -> dict:
    """
    Generates Google Flow AI video generation specification.
    """
    if details is None:
        details = {
            "pricing": "Free & Paid Options Available",
            "key_feature": "Contextual AI coding assistant & fast multi-file indexing",
            "pro": "Extreme speed and intelligent completion",
            "con": "Higher memory consumption under heavy load"
        }

    spec = {
        "title": f"IDE Guide: {ide_name} - Quick Review & Guide",
        "channel": "@IDEguide",
        "target_platform": "YouTube Shorts / Video",
        "aspect_ratio": "9:16 (Shorts) / 16:9 (Standard)",
        "visual_style": {
            "theme": "Sleek Dark Mode Developer Aesthetics",
            "lighting": "Cinematic soft studio neon, high contrast code syntax highlighting",
            "color_palette": ["#1e1e1e", "#00d2ff", "#7b2cbf"],
            "framing": "Macro zooms on code snippets, smooth scrolling camera pans"
        },
        "scenes": [
            {
                "scene_number": 1,
                "duration_seconds": 5,
                "visual_description": f"Dynamic zoom shot into modern dark-mode IDE interface showing {ide_name} logo and syntax highlighting with neon cyan lighting.",
                "voiceover_narration": f"Looking for your next code editor? Let's break down {ide_name} in 60 seconds on IDE Guide!",
                "text_overlay": f"IDE REVIEW: {ide_name.upper()}"
            },
            {
                "scene_number": 2,
                "duration_seconds": 10,
                "visual_description": f"Close-up screen recording of {ide_name} autocompleting complex Python/TypeScript code seamlessly.",
                "voiceover_narration": f"{ide_name} offers {details['key_feature']}. It is designed to boost developer flow.",
                "text_overlay": "KEY FEATURE: AI Productivity & Speed"
            },
            {
                "scene_number": 3,
                "duration_seconds": 12,
                "visual_description": "Split screen graph showing Price vs Performance metrics.",
                "voiceover_narration": f"Pricing model: {details['pricing']}. Great value depending on your project scale.",
                "text_overlay": f"PRICING: {details['pricing']}"
            },
            {
                "scene_number": 4,
                "duration_seconds": 12,
                "visual_description": "Side-by-side comparative green checkmark and red x icon overlay over IDE workspace.",
                "voiceover_narration": f"The Good: {details['pro']}. The Bad: {details['con']}.",
                "text_overlay": "PROS vs CONS"
            },
            {
                "scene_number": 5,
                "duration_seconds": 8,
                "visual_description": f"Subtle pan to IDE Guide channel brand card with YouTube channel @IDEguide and Blogger link.",
                "voiceover_narration": f"Subscribe to @IDEguide on YouTube and check ideguide.blogspot.com for full technical breakdown!",
                "text_overlay": "SUBSCRIBE @IDEguide | ideguide.blogspot.com"
            }
        ],
        "disclaimer": REQUIRED_DISCLAIMER
    }
    return spec


def main():
    parser = argparse.ArgumentParser(description="IDE Guide Agentic Skill Tool")
    parser.add_argument("--ide", type=str, required=True, help="Name of the IDE or Code Editor")
    parser.add_argument("--outdir", type=str, default="./output", help="Output directory path")

    args = parser.parse_args()

    os.makedirs(args.outdir, exist_ok=True)
    slug = args.ide.lower().replace(" ", "_")

    amp_html = generate_amp_blog_post(args.ide)
    amp_filepath = os.path.join(args.outdir, f"{slug}_amp_blog.html")
    with open(amp_filepath, "w", encoding="utf-8") as f:
        f.write(amp_html)

    video_spec = generate_google_flow_video_spec(args.ide)
    spec_filepath = os.path.join(args.outdir, f"{slug}_google_flow_spec.json")
    with open(spec_filepath, "w", encoding="utf-8") as f:
        json.dump(video_spec, f, indent=2)

    print(f"Successfully generated agentic assets for '{args.ide}':")
    print(f"  - AMP Blog Post: {amp_filepath}")
    print(f"  - Google Flow Video Spec: {spec_filepath}")


if __name__ == "__main__":
    main()
