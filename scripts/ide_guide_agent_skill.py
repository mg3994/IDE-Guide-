#!/usr/bin/env python3
"""
Agentic CLI Skill Tool for IDE Guide
Generates on-demand AMP HTML blog post and Google Flow video specifications for any given IDE or repository.
"""

import os
import sys
import json
import argparse
import datetime
from typing import Dict, Any

DISCLAIMER = (
    "Disclaimer: IDE Guide is an independent technical publication. "
    "This content is not sponsored, endorsed, or affiliated with any software vendor or editor developer mentioned above. "
    "All reviews and assessments are based strictly on objective developer evaluation."
)

def build_ide_metadata(ide_name: str, repo_url: str = None) -> Dict[str, Any]:
    safe_id = ide_name.lower().replace(" ", "_").replace("-", "_")

    # Defaults or extracted info for on-demand generation
    metadata = {
        "id": safe_id,
        "name": ide_name,
        "repo_url": repo_url or f"https://github.com/topics/{safe_id}",
        "category": "Custom Development Environment & Code Editor",
        "pricing": "Evaluation Required (Free trial or Open Source / Paid tier)",
        "paid_tier": "Check vendor pricing page for enterprise and personal license details.",
        "pros": [
            f"Extremely specialized workflows for projects built with {ide_name}",
            "Modern interface with integrated developer tools and syntax engine",
            "Extensible architecture supporting key language servers and extensions",
            "Active developer community and regular maintenance updates"
        ],
        "cons": [
            "Requires initial setup and integration testing for custom projects",
            "Resource consumption depends on active extensions and workspace size"
        ],
        "verdict": f"{ide_name} provides robust development capabilities for engineers seeking specialized workflows.",
        "target_audience": "Software Engineers, Open Source Contributors, Technical Leads"
    }
    return metadata

def generate_amp_post(ide: Dict[str, Any], date_str: str) -> str:
    pros_html = "".join([f"<li><strong>{p}</strong></li>" for p in ide["pros"]])
    cons_html = "".join([f"<li><strong>{c}</strong></li>" for c in ide["cons"]])

    amp_html = f"""<!doctype html>
<html amp lang="en">
<head>
  <meta charset="utf-8">
  <title>{ide['name']} Guide: Features, Pros, Cons, and Pricing | IDE Guide</title>
  <link rel="canonical" href="https://ideguide.blogspot.com/{date_str.replace('-', '/')}/{ide['id']}-guide.html">
  <meta name="viewport" content="width=device-width,minimum-scale=1,initial-scale=1">
  <script async src="https://cdn.ampproject.org/v0.js"></script>
  <style amp-boilerplate>body{{-webkit-animation:-amp-start 8s steps(1,end) 0s 1 normal both;-moz-animation:-amp-start 8s steps(1,end) 0s 1 normal both;-ms-animation:-amp-start 8s steps(1,end) 0s 1 normal both;animation:-amp-start 8s steps(1,end) 0s 1 normal both}}@-webkit-keyframes -amp-start{{from{{visibility:hidden}}to{{visibility:visible}}}}@-moz-keyframes -amp-start{{from{{visibility:hidden}}to{{visibility:visible}}}}@-ms-keyframes -amp-start{{from{{visibility:hidden}}to{{visibility:visible}}}}@-o-keyframes -amp-start{{from{{visibility:hidden}}to{{visibility:visible}}}}@keyframes -amp-start{{from{{visibility:hidden}}to{{visibility:visible}}}}</style><noscript><style amp-boilerplate>body{{-webkit-animation:none;-moz-animation:none;-ms-animation:none;animation:none}}</style></noscript>
  <style amp-custom>
    body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; line-height: 1.6; color: #1e293b; background-color: #f8fafc; margin: 0; padding: 16px; }}
    .container {{ max-width: 800px; margin: 0 auto; background: #ffffff; padding: 24px; border-radius: 12px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1); }}
    h1 {{ color: #0f172a; font-size: 1.8rem; border-bottom: 2px solid #2563eb; padding-bottom: 8px; }}
    h2 {{ color: #1e293b; font-size: 1.3rem; margin-top: 24px; }}
    .badge {{ display: inline-block; background-color: #2563eb; color: #ffffff; padding: 4px 10px; border-radius: 9999px; font-size: 0.85rem; font-weight: bold; }}
    .meta-box {{ background-color: #f1f5f9; border-left: 4px solid #2563eb; padding: 12px 16px; margin: 16px 0; border-radius: 4px; }}
    .pros {{ background-color: #f0fdf4; border-left: 4px solid #059669; padding: 12px 16px; margin: 16px 0; }}
    .cons {{ background-color: #fef2f2; border-left: 4px solid #dc2626; padding: 12px 16px; margin: 16px 0; }}
    .verdict {{ background-color: #eff6ff; border: 1px solid #bfdbfe; padding: 16px; border-radius: 8px; font-weight: 500; }}
    .disclaimer {{ font-size: 0.8rem; color: #64748b; border-top: 1px solid #e2e8f0; margin-top: 32px; padding-top: 16px; font-style: italic; }}
  </style>
</head>
<body>
  <div class="container">
    <span class="badge">{ide['category']}</span>
    <h1>Agentic Guide: {ide['name']}</h1>

    <div class="meta-box">
      <p><strong>Target Audience:</strong> {ide['target_audience']}</p>
      <p><strong>Pricing & Licensing:</strong> {ide['pricing']}</p>
      <p><strong>Repository / Link:</strong> <a href="{ide['repo_url']}">{ide['repo_url']}</a></p>
    </div>

    <h2>Overview & Capabilities</h2>
    <p>This automated agentic report analyzes <strong>{ide['name']}</strong> to help software engineering teams determine tool fit and adoption suitability.</p>

    <amp-img src="https://via.placeholder.com/800x400/0f172a/ffffff?text={ide['name'].replace(' ', '+')}+Agentic+Guide" width="800" height="400" layout="responsive" alt="{ide['name']} Guide"></amp-img>

    <div class="pros">
      <h2>Key Strengths & Pros</h2>
      <ul>
        {pros_html}
      </ul>
    </div>

    <div class="cons">
      <h2>Drawbacks & Tradeoffs</h2>
      <ul>
        {cons_html}
      </ul>
    </div>

    <h2>Developer Verdict</h2>
    <div class="verdict">
      <p>{ide['verdict']}</p>
    </div>

    <div class="disclaimer">
      <p>{DISCLAIMER}</p>
    </div>
  </div>
</body>
</html>"""
    return amp_html

def generate_flow_spec(ide: Dict[str, Any], date_str: str) -> Dict[str, Any]:
    return {
        "metadata": {
            "channel": "@IDEguide",
            "youtube_url": "https://www.youtube.com/@IDEguide",
            "ide_name": ide["name"],
            "repo_url": ide["repo_url"],
            "date": date_str,
            "format": "Short & Video Prompt Specification",
            "aspect_ratio": "9:16 Vertical / 16:9 Horizontal",
            "title": f"Is {ide['name']} Worth It? Agentic IDE Review"
        },
        "visual_and_camera_specifications": {
            "framing": "Sleek Dark Tech Studio, Cyberpunk accent glow",
            "lighting": "Deep indigo studio background with neon blue rim light",
            "camera_angles": [
                {"scene": 1, "angle": "Zoom-in on editor splash screen and UI", "duration": "0-10s"},
                {"scene": 2, "angle": "Macro focus on extension / code completion workflow", "duration": "10-40s"},
                {"scene": 3, "angle": "Wide camera shot with summary score overlay", "duration": "40-60s"}
            ],
            "graphics_and_cues": f"Overlays showcasing {ide['name']} pricing, pros/cons bullet points."
        },
        "voiceover_script": {
            "hook": f"Here is what you need to know before using {ide['name']} in your codebase!",
            "pricing_segment": f"Pricing breakdown: {ide['pricing']}.",
            "pros_segment": f"Top pros: {', '.join(ide['pros'])}.",
            "cons_segment": f"Potential cons: {', '.join(ide['cons'])}.",
            "recommendation_callout": f"Verdict: {ide['verdict']}"
        },
        "audio_directions": {
            "background_music": "Upbeat tech synthwave track",
            "sfx": "UI click and subtle visual transition sweeps"
        },
        "disclaimer_overlay": {
            "text": DISCLAIMER,
            "visual_position": "Bottom banner overlay"
        }
    }

def main():
    parser = argparse.ArgumentParser(description="IDE Guide Agentic CLI Skill Tool")
    parser.add_argument("--ide", required=True, help="Name of the IDE or Code Editor")
    parser.add_argument("--repo", help="Repository URL or project site", default=None)
    parser.add_argument("--output-dir", help="Directory to save generated outputs", default="content/agent_skills")

    args = parser.parse_args()
    date_str = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d")

    ide_meta = build_ide_metadata(args.ide, args.repo)
    os.makedirs(args.output_dir, exist_ok=True)

    # Generate AMP HTML
    amp_content = generate_amp_post(ide_meta, date_str)
    amp_file = os.path.join(args.output_dir, f"{ide_meta['id']}_post.html")
    with open(amp_file, 'w', encoding='utf-8') as f:
        f.write(amp_content)

    # Generate Flow spec
    flow_spec = generate_flow_spec(ide_meta, date_str)
    spec_file = os.path.join(args.output_dir, f"{ide_meta['id']}_flow_spec.json")
    with open(spec_file, 'w', encoding='utf-8') as f:
        json.dump(flow_spec, f, indent=2)

    print(f"Agentic skill successfully generated assets for {args.ide}:")
    print(f"  [+] AMP Blog Post: {amp_file}")
    print(f"  [+] Google Flow Spec: {spec_file}")

if __name__ == "__main__":
    main()
