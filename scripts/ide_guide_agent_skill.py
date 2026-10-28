#!/usr/bin/env python3
"""
Agentic Skill Tool for IDE Guide
Generates on-demand AMP HTML blog post and Google Flow video spec for a given IDE name or Repository URL.
"""

import sys
import os
import json
import argparse
import datetime
from urllib.parse import urlparse

REQUIRED_DISCLAIMER = (
    "IDE Guide is an independent technical publication. This content is not sponsored, "
    "endorsed, or affiliated with any software vendor or editor developer mentioned above. "
    "All reviews and assessments are based strictly on objective developer evaluation."
)

def infer_ide_details(input_name_or_url: str) -> dict:
    name = input_name_or_url.strip()
    if name.startswith("http://") or name.startswith("https://"):
        parsed = urlparse(name)
        path_parts = [p for p in parsed.path.split("/") if p]
        if path_parts:
            repo_name = path_parts[-1]
            name = repo_name.replace("-", " ").replace("_", " ").title()

    slug = name.lower().replace(" ", "-").replace("/", "-")

    return {
        "name": name,
        "slug": slug,
        "category": "Developer Tool / Code Editor",
        "pricing": "Free / Open Source",
        "pricing_type": "Free",
        "pros": [
            f"Powerful extensibility and developer-focused features in {name}.",
            "High performance and customizable workspace configuration.",
            "Strong developer ecosystem and community support."
        ],
        "cons": [
            "Requires initial setup to tailor to custom workflows.",
            "May require learning project-specific keybindings or settings."
        ],
        "summary": f"{name} is an efficient development tool designed to streamline software engineering and enhance coding productivity.",
        "best_for": "Software engineers, open-source contributors, and developers seeking flexible tooling.",
        "icon_url": "https://raw.githubusercontent.com/vscode-icons/vscode-icons/master/icons/file_type_vscode.svg"
    }

def generate_agentic_content(input_val: str, output_dir: str = None) -> tuple[str, str]:
    ide = infer_ide_details(input_val)
    date_str = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d")

    if not output_dir:
        output_dir = os.path.join("content", "agentic", ide["slug"])
    os.makedirs(output_dir, exist_ok=True)

    # Render AMP HTML Blog Post
    canonical_url = f"https://ideguide.blogspot.com/{date_str.replace('-', '/')}/{ide['slug']}-review.html"
    pros_html = "\n".join([f"        <li>✅ {p}</li>" for p in ide["pros"]])
    cons_html = "\n".join([f"        <li>❌ {c}</li>" for c in ide["cons"]])

    html_content = f"""<!doctype html>
<html ⚡ lang="en">
<head>
  <meta charset="utf-8">
  <title>{ide['name']} Review & Developer Guide - IDE Guide</title>
  <link rel="canonical" href="{canonical_url}">
  <meta name="viewport" content="width=device-width,minimum-scale=1,initial-scale=1">
  <script async src="https://cdn.ampproject.org/v0.js"></script>
  <style amp-boilerplate>body{{-webkit-animation:-amp-start 8s steps(1,end) 0s 1 normal both;-moz-animation:-amp-start 8s steps(1,end) 0s 1 normal both;-ms-animation:-amp-start 8s steps(1,end) 0s 1 normal both;animation:-amp-start 8s steps(1,end) 0s 1 normal both}}@-webkit-keyframes -amp-start{{from{{visibility:hidden}}to{{visibility:visible}}}}@-moz-keyframes -amp-start{{from{{visibility:hidden}}to{{visibility:visible}}}}@-ms-keyframes -amp-start{{from{{visibility:hidden}}to{{visibility:visible}}}}@-o-keyframes -amp-start{{from{{visibility:hidden}}to{{visibility:visible}}}}@keyframes -amp-start{{from{{visibility:hidden}}to{{visibility:visible}}}}</style><noscript><style amp-boilerplate>body{{-webkit-animation:none;-moz-animation:none;-ms-animation:none;animation:none}}</style></noscript>
  <style amp-custom>
    body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; line-height: 1.6; color: #1f2937; padding: 16px; max-width: 800px; margin: 0 auto; background-color: #f9fafb; }}
    .header {{ text-align: center; border-bottom: 2px solid #e5e7eb; padding-bottom: 20px; margin-bottom: 24px; }}
    .badge {{ display: inline-block; background-color: #2563eb; color: #ffffff; padding: 4px 12px; border-radius: 12px; font-size: 0.85rem; font-weight: bold; margin-bottom: 8px; }}
    .pricing-badge {{ background-color: #059669; }}
    h1 {{ font-size: 2rem; color: #111827; margin: 8px 0; }}
    .summary {{ font-size: 1.1rem; color: #4b5563; font-style: italic; background: #ffffff; padding: 16px; border-left: 4px solid #2563eb; border-radius: 4px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); margin-bottom: 24px; }}
    .grid {{ display: flex; flex-direction: column; gap: 16px; margin-bottom: 24px; }}
    .card {{ background: #ffffff; padding: 20px; border-radius: 8px; box-shadow: 0 1px 3px rgba(0,0,0,0.08); border: 1px solid #e5e7eb; }}
    .card-verdict {{ margin-top: 24px; }}
    .card h3 {{ margin-top: 0; color: #111827; border-bottom: 1px solid #f3f4f6; padding-bottom: 8px; }}
    ul {{ padding-left: 20px; margin: 8px 0; }}
    li {{ margin-bottom: 8px; }}
    .table-wrapper {{ overflow-x: auto; margin-bottom: 24px; }}
    table {{ width: 100%; border-collapse: collapse; background: #ffffff; border-radius: 8px; overflow: hidden; box-shadow: 0 1px 3px rgba(0,0,0,0.08); }}
    th, td {{ padding: 12px 16px; text-align: left; border-bottom: 1px solid #e5e7eb; }}
    th {{ background-color: #f3f4f6; color: #374151; font-weight: bold; }}
    .disclaimer-box {{ background-color: #eff6ff; border: 1px solid #bfdbfe; color: #1e40af; padding: 16px; border-radius: 8px; font-size: 0.9rem; margin-top: 32px; }}
  </style>
</head>
<body>
  <div class="header">
    <span class="badge">{ide['category']}</span>
    <span class="badge pricing-badge">{ide['pricing_type']}</span>
    <h1>{ide['name']}: Complete Developer Guide</h1>
    <amp-img src="{ide['icon_url']}" width="64" height="64" layout="fixed" alt="{ide['name']} logo"></amp-img>
  </div>

  <div class="summary">
    {ide['summary']}
  </div>

  <div class="grid">
    <div class="card">
      <h3>The Good (Pros)</h3>
      <ul>
{pros_html}
      </ul>
    </div>

    <div class="card">
      <h3>The Bad (Cons)</h3>
      <ul>
{cons_html}
      </ul>
    </div>
  </div>

  <div class="card">
    <h3>Pricing & License Breakdown</h3>
    <div class="table-wrapper">
      <table>
        <thead>
          <tr>
            <th>Tier</th>
            <th>Details & Features</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td><strong>Pricing Model</strong></td>
            <td>{ide['pricing']}</td>
          </tr>
          <tr>
            <td><strong>Recommended Audience</strong></td>
            <td>{ide['best_for']}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>

  <div class="card card-verdict">
    <h3>Final Verdict</h3>
    <p>{ide['name']} is best suited for <strong>{ide['best_for']}</strong>.</p>
  </div>

  <div class="disclaimer-box">
    <strong>Disclaimer:</strong> {REQUIRED_DISCLAIMER}
  </div>
</body>
</html>"""

    blog_file = os.path.join(output_dir, f"{ide['slug']}_blog.html")
    with open(blog_file, "w", encoding="utf-8") as f:
        f.write(html_content)

    # Render Google Flow Spec
    video_spec = {
        "channel": "@IDEguide",
        "title": f"{ide['name']} - Pros, Cons & Pricing Developer Guide",
        "ide_name": ide["name"],
        "category": ide["category"],
        "pricing_tier": ide["pricing"],
        "target_audience": ide["best_for"],
        "google_flow_prompts": [
            {
                "scene_id": 1,
                "scene_type": "Hook & Overview",
                "duration_seconds": 5,
                "visual_prompt": f"Cinematic wide angle shot of modern high-tech developer setup displaying {ide['name']} UI, dark mode aesthetic, vibrant syntax highlighting, ultra realistic 4k render.",
                "camera_motion": "Slow forward push-in toward monitor screen",
                "lighting": "Cyberpunk volumetric ambient blue/cyan lighting",
                "script": f"Is {ide['name']} the right developer tool for you? Let's break down the pros, cons, and pricing!"
            },
            {
                "scene_id": 2,
                "scene_type": "The Good (Strengths)",
                "duration_seconds": 12,
                "visual_prompt": f"Macro lens view of {ide['name']} interface showing fast code execution and slick UI panels.",
                "camera_motion": "Smooth horizontal pan left to right across code view",
                "lighting": "Clean studio rim light highlighting screen details",
                "script": f"Here is what makes {ide['name']} great: {ide['pros'][0]}"
            },
            {
                "scene_id": 3,
                "scene_type": "The Bad (Limitations)",
                "duration_seconds": 10,
                "visual_prompt": f"Close-up tilted frame highlighting complex settings menu or system resource usage in {ide['name']}.",
                "camera_motion": "Subtle slow zoom out with slight tilt",
                "lighting": "Warm warning tint accent",
                "script": f"Things to keep in mind: {ide['cons'][0]}"
            },
            {
                "scene_id": 4,
                "scene_type": "Pricing & Verdict",
                "duration_seconds": 8,
                "visual_prompt": f"High contrast motion graphics card displaying {ide['pricing']} badge and final recommendation rating.",
                "camera_motion": "Static front-facing center focus",
                "lighting": "Bright balanced daylight setup",
                "script": f"Pricing model: {ide['pricing']}. Best for {ide['best_for']}. Subscribe to IDE Guide for more technical guides!"
            }
        ],
        "disclaimer": REQUIRED_DISCLAIMER
    }

    video_file = os.path.join(output_dir, f"{ide['slug']}_google_flow.json")
    with open(video_file, "w", encoding="utf-8") as f:
        json.dump(video_spec, f, indent=2)

    return blog_file, video_file

def main():
    parser = argparse.ArgumentParser(description="Agentic Skill Tool for IDE Guide")
    parser.add_argument("--ide", type=str, required=True, help="IDE Name or Github Repository URL")
    parser.add_argument("--output-dir", type=str, default=None, help="Directory path to save output files")
    args = parser.parse_args()

    blog, video = generate_agentic_content(args.ide, args.output_dir)
    print(f"Agentic generation complete:")
    print(f"  - AMP Blog Post: {blog}")
    print(f"  - Google Flow Video Spec: {video}")

if __name__ == "__main__":
    main()
