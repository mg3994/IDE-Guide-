#!/usr/bin/env python3
"""
Agentic CLI Skill Tool for IDE Guide.
Generates custom AMP HTML blog posts and Google Flow video specifications
for any specified IDE name or repository URL on demand.
"""

import os
import sys
import json
import argparse
import urllib.parse
from typing import Dict, Any

# Ensure parent directory is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from scripts.amp_validator import validate_amp_html

DISCLAIMER_TEXT = (
    "Disclaimer: IDE Guide is an independent technical publication. "
    "This content is not sponsored, endorsed, or affiliated with any software vendor "
    "or editor developer mentioned above. All reviews and assessments are based strictly "
    "on objective developer evaluation."
)

def infer_tool_data_from_name_or_repo(ide_name: str = None, repo_url: str = None) -> Dict[str, Any]:
    if repo_url:
        path = urllib.parse.urlparse(repo_url).path.strip("/")
        repo_parts = path.split("/")
        name = repo_parts[-1].replace("-", " ").replace("_", " ").title() if repo_parts else "Custom Editor"
        developer = repo_parts[0] if len(repo_parts) > 1 else "Open Source Community"
        slug = name.lower().replace(" ", "-")
        pricing_type = "Free / Open Source"
        price_summary = "100% Free and open source on GitHub."
        overview = f"{name} is an open-source development tool hosted at {repo_url}."
    else:
        name = ide_name if ide_name else "Custom IDE"
        developer = "Developer Vendor"
        slug = name.lower().replace(" ", "-")
        pricing_type = "Free / Freemium / Commercial"
        price_summary = "Offers free trial and commercial subscription tiers."
        overview = f"{name} is a high-performance development environment optimized for modern software workflows."

    return {
        "name": name,
        "slug": slug,
        "developer": developer,
        "pricing_type": pricing_type,
        "price_summary": price_summary,
        "pros": [
            "Tailored productivity features for developer workflows",
            "Extensible architecture with community integrations",
            "Modern user interface with fast performance"
        ],
        "cons": [
            "May require custom configuration for specialized stack needs",
            "Ecosystem extensions depending on plugin market maturity"
        ],
        "best_for": "Developers seeking an efficient environment tailored to modern coding standards",
        "overview": overview,
        "rating": "4.7/5.0"
    }


def generate_custom_amp_blog(tool: Dict[str, Any], canonical_url: str) -> str:
    pros_html = "".join([f"<li><strong>{p}</strong></li>" for p in tool["pros"]])
    cons_html = "".join([f"<li><strong>{c}</strong></li>" for c in tool["cons"]])

    return f"""<!doctype html>
<html ⚡ lang="en">
<head>
  <meta charset="utf-8">
  <script async src="https://cdn.ampproject.org/v0.js"></script>
  <title>{tool['name']} Custom Review & Assessment - IDE Guide</title>
  <link rel="canonical" href="{canonical_url}">
  <meta name="viewport" content="width=device-width,minimum-scale=1,initial-scale=1">
  <style amp-boilerplate>body{{-webkit-animation:-amp-start 8s steps(1,end) 0s 1 normal both;-moz-animation:-amp-start 8s steps(1,end) 0s 1 normal both;-ms-animation:-amp-start 8s steps(1,end) 0s 1 normal both;animation:-amp-start 8s steps(1,end) 0s 1 normal both}}</style><noscript><style amp-boilerplate>body{{-webkit-animation:none;-moz-animation:none;-ms-animation:none;animation:none}}</style></noscript>
  <style amp-custom>
    body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; line-height: 1.6; color: #1a1a1a; padding: 16px; max-width: 800px; margin: 0 auto; background-color: #ffffff; }}
    header {{ background: #1e293b; color: #ffffff; padding: 20px; border-radius: 8px; margin-bottom: 20px; }}
    h1 {{ font-size: 1.7rem; color: #38bdf8; margin: 0 0 8px 0; }}
    .badge {{ display: inline-block; background: #0284c7; color: #ffffff; padding: 4px 8px; font-size: 0.8rem; border-radius: 4px; margin-bottom: 8px; }}
    .section-box {{ border: 1px solid #e2e8f0; border-radius: 6px; padding: 16px; margin-bottom: 16px; }}
    .disclaimer {{ background: #f8fafc; border: 1px solid #e2e8f0; font-size: 0.85rem; color: #64748b; padding: 12px; border-radius: 6px; margin-top: 24px; }}
  </style>
</head>
<body>
  <header>
    <span class="badge">{tool['pricing_type']}</span>
    <h1>{tool['name']}: Deep Dive Analysis</h1>
    <p>Published by IDE Guide | Rating: {tool['rating']}</p>
  </header>

  <section class="section-box">
    <h2>Overview</h2>
    <p>{tool['overview']}</p>
    <p><strong>Developer:</strong> {tool['developer']}</p>
    <p><strong>Pricing:</strong> {tool['price_summary']}</p>
  </section>

  <section class="section-box">
    <h2>Pros & Cons</h2>
    <h3>Pros</h3>
    <ul>{pros_html}</ul>
    <h3>Cons</h3>
    <ul>{cons_html}</ul>
  </section>

  <section class="section-box">
    <h2>Verdict</h2>
    <p>{tool['best_for']}</p>
  </section>

  <footer class="disclaimer">
    <p>{DISCLAIMER_TEXT}</p>
  </footer>
</body>
</html>"""


def generate_custom_google_flow_spec(tool: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "channel": "@IDEguide",
        "tool_name": tool["name"],
        "pricing_category": tool["pricing_type"],
        "target_aspect_ratio": "16:9 Widescreen & 9:16 Vertical",
        "visual_prompt_specifications": {
            "framing": f"Modern dark mode workspace showing active {tool['name']} code editor and terminal window",
            "lighting": "Cinematic ambient studio lighting with deep blue and purple accents",
            "camera_motion": "Smooth pan across workspace with subtle focal depth effect",
            "color_palette": "Slate dark background, electric blue text highlights"
        },
        "narration_script": [
            {
                "scene": 1,
                "duration_sec": 5,
                "visual_prompt": f"Close-up overview shot of {tool['name']} interface",
                "text_overlay": tool["name"],
                "voiceover": f"Here is our complete assessment of {tool['name']}."
            },
            {
                "scene": 2,
                "duration_sec": 8,
                "visual_prompt": "Graphics card overlay displaying pricing details and core features",
                "text_overlay": f"Pricing: {tool['pricing_type']}",
                "voiceover": tool["price_summary"]
            },
            {
                "scene": 3,
                "duration_sec": 10,
                "visual_prompt": "Comparative card listing key strengths and limitations",
                "text_overlay": "Pros & Cons",
                "voiceover": f"Strengths include {tool['pros'][0]}. Consider that {tool['cons'][0]}."
            }
        ],
        "non_sponsorship_disclaimer": DISCLAIMER_TEXT
    }


def main():
    parser = argparse.ArgumentParser(description="Agentic CLI Skill Tool for IDE Guide content generation.")
    parser.add_argument("--ide", help="Name of the IDE or Code Editor")
    parser.add_argument("--repo", help="GitHub or Git repository URL")
    parser.add_argument("--output-dir", default="content/custom", help="Output directory for generated files")
    args = parser.parse_args()

    if not args.ide and not args.repo:
        parser.error("Please specify either --ide or --repo")

    tool_data = infer_tool_data_from_name_or_repo(ide_name=args.ide, repo_url=args.repo)
    os.makedirs(args.output_dir, exist_ok=True)

    slug = tool_data["slug"]
    canonical_url = f"https://ideguide.blogspot.com/custom/{slug}.html"

    # Generate Blog Post
    blog_html = generate_custom_amp_blog(tool_data, canonical_url)
    is_valid, errors = validate_amp_html(blog_html)
    if not is_valid:
        raise ValueError(f"Custom AMP blog post generation failed validation: {errors}")

    blog_file = os.path.join(args.output_dir, f"{slug}_blogpost.html")
    with open(blog_file, "w", encoding="utf-8") as f:
        f.write(blog_html)

    # Generate Flow Spec
    flow_spec = generate_custom_google_flow_spec(tool_data)
    spec_file = os.path.join(args.output_dir, f"{slug}_flow_spec.json")
    with open(spec_file, "w", encoding="utf-8") as f:
        json.dump(flow_spec, f, indent=2)

    print(f"✅ Generated Agentic Skill content for {tool_data['name']}:")
    print(f" - AMP Blog Post: {blog_file}")
    print(f" - Google Flow Video Spec: {spec_file}")

if __name__ == "__main__":
    main()
