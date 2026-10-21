#!/usr/bin/env python3
"""
IDE Guide Agentic CLI Skill Tool.
Generates custom AMP HTML blog posts and Google Flow video specs for any given IDE name or Repository URL.
"""

import argparse
import json
import os
import re
import sys
from typing import Dict, Any

REQUIRED_DISCLAIMER = (
    "Disclaimer: IDE Guide is an independent technical publication. "
    "This content is not sponsored, endorsed, or affiliated with any software vendor "
    "or editor developer mentioned above. All reviews and assessments are based "
    "strictly on objective developer evaluation."
)

IDE_DATABASE = {
    "cursor": {
        "name": "Cursor AI",
        "category": "AI Native Code Editor",
        "license": "Proprietary",
        "pricing": "Freemium ($20/mo Pro)",
        "platforms": "Windows, macOS, Linux",
        "key_features": ["AI Agent Mode", "Multi-file edit context", "Codebase indexing", "VS Code Extension compatibility"],
        "pros": ["Unmatched AI productivity", "Seamless VS Code migration", "Instant code generation"],
        "cons": ["Paid subscription for heavy AI usage", "Requires internet for cloud models"],
        "best_for": "Developers seeking maximum AI coding speed and autonomous code generation."
    },
    "zed": {
        "name": "Zed Editor",
        "category": "High-Performance Code Editor",
        "license": "Open Source (GPL / Apache 2.0)",
        "pricing": "Free & Open Source",
        "platforms": "macOS, Linux (Windows in preview)",
        "key_features": ["Rust GPU rendering engine", "Built-in multiplayer pair programming", "Low memory footprint"],
        "pros": ["Blazing fast startup and rendering", "Minimalist aesthetic", "Built-in AI model support"],
        "cons": ["Ecosystem extensions still growing", "Fewer plugins than VS Code"],
        "best_for": "Performance purists and Rust/C++/Web developers wanting maximum UI responsiveness."
    },
    "neovim": {
        "name": "Neovim",
        "category": "Extensible Modal Text Editor",
        "license": "Open Source (Apache 2.0 / Vim)",
        "pricing": "100% Free & Open Source",
        "platforms": "Linux, macOS, Windows, Terminal",
        "key_features": ["Lua configuration API", "Built-in LSP client", "Treesitter syntax engine", "Ultra-fast modal editing"],
        "pros": ["Keyboard-driven efficiency", "Infinitely customizable", "Zero GUI overhead"],
        "cons": ["Steep learning curve", "Requires time to configure setup"],
        "best_for": "Keyboard warriors, sysadmins, and engineers who love total control over their editor."
    },
    "vscode": {
        "name": "Visual Studio Code",
        "category": "General Purpose IDE/Editor",
        "license": "Open Source (Code-OSS) / Free Binary",
        "pricing": "Free",
        "platforms": "Windows, macOS, Linux, Web",
        "key_features": ["Massive extension marketplace", "Integrated debugger and terminal", "GitHub Copilot integration"],
        "pros": ["Huge community support", "Rich language support", "Easy setup"],
        "cons": ["Can become heavy with many extensions", "Electron RAM usage"],
        "best_for": "Developers of all skill levels looking for a flexible, battle-tested code editor."
    },
    "windsurf": {
        "name": "Windsurf Editor",
        "category": "Agentic AI Flow Editor",
        "license": "Proprietary",
        "pricing": "Freemium ($15/mo Pro)",
        "platforms": "Windows, macOS, Linux",
        "key_features": ["Cascade Agentic AI flow", "Deep terminal & codebase integration", "Live prompt reasoning"],
        "pros": ["Context-aware refactoring", "Fluid AI collaborative workflows", "Great UI integration"],
        "cons": ["Subscription required for unlimited agent runs", "Proprietary stack"],
        "best_for": "Full-stack and AI-first engineers wanting agentic AI assistance."
    }
}


def extract_ide_info(input_str: str) -> Dict[str, Any]:
    """Parses input name or git URL to infer or fetch IDE metadata."""
    clean_name = input_str.strip().lower()

    # Check if URL
    if "github.com" in clean_name or "http" in clean_name:
        repo_part = clean_name.rstrip("/").split("/")[-1].replace(".git", "")
        clean_name = repo_part

    for key, data in IDE_DATABASE.items():
        if key in clean_name or clean_name in key:
            return data

    # Default fallback generator for unlisted IDEs
    display_title = input_str.strip().rstrip("/").split("/")[-1].replace(".git", "").replace("-", " ").title()
    return {
        "name": display_title,
        "category": "Developer Code Editor / Tool",
        "license": "Open Source / Vendor Specific",
        "pricing": "Free / Freemium Tier Available",
        "platforms": "Cross-Platform (Windows, macOS, Linux)",
        "key_features": ["Modern Developer UI", "Syntax Highlighting & Formatting", "Extensible Plugin Architecture", "Workspace Management"],
        "pros": ["Specialized developer workflow", "Customizable configuration", "Active developer ecosystem"],
        "cons": ["Learning curve for advanced features", "Niche extension library"],
        "best_for": f"Engineers and developers looking for custom workflows with {display_title}."
    }


def generate_amp_blog_post(ide_info: Dict[str, Any]) -> str:
    """Generates AMP compliant HTML for Blogger."""
    name = ide_info["name"]
    category = ide_info["category"]
    license_type = ide_info["license"]
    pricing = ide_info["pricing"]
    platforms = ide_info["platforms"]

    features_html = "".join([f"<li><strong>{feat}</strong></li>" for feat in ide_info["key_features"]])
    pros_html = "".join([f"<li>{pro}</li>" for pro in ide_info["pros"]])
    cons_html = "".join([f"<li>{con}</li>" for con in ide_info["cons"]])

    amp_html = f"""<!doctype html>
<html amp lang="en">
<head>
  <meta charset="utf-8">
  <script async src="https://cdn.ampproject.org/v0.js"></script>
  <title>{name} Review & Deep Dive - IDE Guide</title>
  <link rel="canonical" href="https://ideguide.blogspot.com/reviews/{name.lower().replace(' ', '-')}.html">
  <meta name="viewport" content="width=device-width,minimum-scale=1,initial-scale=1">
  <style amp-boilerplate>body{{-webkit-animation:-amp-start 8s steps(1,end) 0s 1 normal both;-moz-animation:-amp-start 8s steps(1,end) 0s 1 normal both;-ms-animation:-amp-start 8s steps(1,end) 0s 1 normal both;animation:-amp-start 8s steps(1,end) 0s 1 normal both}}@-webkit-keyframes -amp-start{{from{{visibility:hidden}}to{{visibility:visible}}}}@-moz-keyframes -amp-start{{from{{visibility:hidden}}to{{visibility:visible}}}}@-ms-keyframes -amp-start{{from{{visibility:hidden}}to{{visibility:visible}}}}@-o-keyframes -amp-start{{from{{visibility:hidden}}to{{visibility:visible}}}}@keyframes -amp-start{{from{{visibility:hidden}}to{{visibility:visible}}}}</style><noscript><style amp-boilerplate>body{{-webkit-animation:none;-moz-animation:none;-ms-animation:none;animation:none}}</style></noscript>
  <style amp-custom>
    body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; line-height: 1.6; color: #1e293b; padding: 16px; max-width: 800px; margin: 0 auto; background-color: #f8fafc; }}
    header {{ border-bottom: 2px solid #0f172a; padding-bottom: 12px; margin-bottom: 24px; }}
    h1 {{ color: #0f172a; font-size: 2rem; margin-bottom: 8px; }}
    .badge {{ display: inline-block; background: #2563eb; color: #fff; padding: 4px 10px; border-radius: 4px; font-size: 0.85rem; font-weight: bold; margin-bottom: 12px; }}
    table {{ width: 100%; border-collapse: collapse; margin: 20px 0; background: #fff; border-radius: 8px; overflow: hidden; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }}
    th, td {{ padding: 12px 16px; text-align: left; border-bottom: 1px solid #e2e8f0; }}
    th {{ background: #f1f5f9; color: #334155; font-weight: 600; }}
    .grid {{ display: flex; flex-wrap: wrap; gap: 16px; margin: 20px 0; }}
    .card {{ flex: 1; min-width: 280px; background: #fff; padding: 16px; border-radius: 8px; border: 1px solid #e2e8f0; }}
    .card h3 {{ margin-top: 0; font-size: 1.2rem; }}
    .pro-title {{ color: #16a34a; }}
    .con-title {{ color: #dc2626; }}
    .disclaimer {{ background: #fffbe3; border-left: 4px solid #eab308; padding: 14px; margin-top: 32px; font-size: 0.9rem; color: #713f12; border-radius: 0 4px 4px 0; }}
  </style>
</head>
<body>
  <header>
    <div class="badge">{category}</div>
    <h1>{name}: Comprehensive Developer Analysis & Overview</h1>
    <p>An objective, technical breakdown of {name} for software engineers, developers, and code enthusiasts.</p>
  </header>

  <main>
    <h2>At-a-Glance Summary</h2>
    <table>
      <tr><th>Property</th><th>Details</th></tr>
      <tr><td><strong>Software License</strong></td><td>{license_type}</td></tr>
      <tr><td><strong>Pricing Tier</strong></td><td>{pricing}</td></tr>
      <tr><td><strong>Supported OS</strong></td><td>{platforms}</td></tr>
      <tr><td><strong>Primary Focus</strong></td><td>{category}</td></tr>
    </table>

    <h2>Key Standout Features</h2>
    <ul>
      {features_html}
    </ul>

    <div class="grid">
      <div class="card">
        <h3 class="pro-title">Pros & Strengths</h3>
        <ul>
          {pros_html}
        </ul>
      </div>
      <div class="card">
        <h3 class="con-title">Cons & Limitations</h3>
        <ul>
          {cons_html}
        </ul>
      </div>
    </div>

    <h2>Verdict & Recommendation</h2>
    <p><strong>Who should use {name}?</strong> {ide_info['best_for']}</p>

    <div class="disclaimer">
      {REQUIRED_DISCLAIMER}
    </div>
  </main>
</body>
</html>"""
    return amp_html


def generate_google_flow_video_spec(ide_info: Dict[str, Any]) -> Dict[str, Any]:
    """Generates structured JSON spec for Google Flow AI video creation."""
    name = ide_info["name"]
    category = ide_info["category"]

    return {
        "video_meta": {
            "title": f"{name} - Is It Worth Your Code Time? (IDE Guide)",
            "channel": "@IDEguide",
            "target_platform": "YouTube Shorts & Video",
            "aspect_ratio": "9:16",
            "duration_seconds": 60,
            "topic": name,
            "category": category
        },
        "style_guidelines": {
            "visual_theme": "Modern Dark Mode Code Editor Aesthetic with Cyber Neon Accents",
            "camera_style": "Macro zooms on editor code blocks, dynamic fluid panning, 4K crisp code UI rendering",
            "lighting": "Volumetric ambient purple/blue dark mode studio glow",
            "audio": {
                "voiceover_persona": "Tech-savvy, articulate, energetic developer advocate",
                "background_track": "Upbeat minimalist lo-fi tech groove"
            }
        },
        "scenes": [
            {
                "scene_id": 1,
                "timestamp": "00:00 - 00:10",
                "flow_prompt": f"Close-up macro lens panning over ultra-clean dark theme UI of {name}. Neon highlighted syntax code streaming on screen.",
                "camera_motion": "Slow inward push zoom towards active line cursor.",
                "voiceover": f"Looking for the ultimate coding tool? Meet {name}, the {category} taking developer workflows by storm.",
                "text_overlay": f"{name}: Ultimate Overview"
            },
            {
                "scene_id": 2,
                "timestamp": "00:10 - 00:30",
                "flow_prompt": f"Split screen visual displaying key features of {name}: {', '.join(ide_info['key_features'][:2])}. Smooth UI interaction graphics.",
                "camera_motion": "Fluid side whip pan between code generation and terminal output.",
                "voiceover": f"What makes it special? Key highlights include {ide_info['key_features'][0]} and {ide_info['key_features'][1]}.",
                "text_overlay": "Key Features Breakdown"
            },
            {
                "scene_id": 3,
                "timestamp": "00:30 - 00:45",
                "flow_prompt": "Side-by-side comparison card comparing pros vs cons with glowing green checkmarks and subtle red indicators.",
                "camera_motion": "Static focus with dynamic text pop-ins.",
                "voiceover": f"On pricing: {ide_info['pricing']}. Major pro: {ide_info['pros'][0]}. But watch out for: {ide_info['cons'][0]}.",
                "text_overlay": f"Pricing: {ide_info['pricing']}"
            },
            {
                "scene_id": 4,
                "timestamp": "00:45 - 00:60",
                "flow_prompt": "Cinematic pull-back shot showing full developer dual-monitor workstation with glowing code on screen.",
                "camera_motion": "Smooth pull back and fade to channel brand card.",
                "voiceover": f"Is {name} right for you? {ide_info['best_for']} Subscribe to IDE Guide for daily editor breakdowns!",
                "text_overlay": "Subscribe @IDEguide for Daily IDE Insights"
            }
        ],
        "disclaimer": REQUIRED_DISCLAIMER
    }


def main():
    parser = argparse.ArgumentParser(description="IDE Guide Agentic CLI Tool - Generate AMP Blog & Google Flow Video Spec.")
    parser.add_argument("ide", type=str, help="IDE Name or Repository URL (e.g. 'Cursor', 'Zed', 'https://github.com/neovim/neovim')")
    parser.add_argument("--output-dir", type=str, default=".", help="Directory to output generated files")
    args = parser.parse_args()

    ide_info = extract_ide_info(args.ide)
    slug = ide_info["name"].lower().replace(" ", "_")

    os.makedirs(args.output_dir, exist_ok=True)

    # 1. Generate AMP Blog Post
    amp_content = generate_amp_blog_post(ide_info)
    amp_filepath = os.path.join(args.output_dir, f"blog_{slug}.amp.html")
    with open(amp_filepath, "w", encoding="utf-8") as f:
        f.write(amp_content)

    # 2. Generate Google Flow Video Spec
    flow_spec = generate_google_flow_video_spec(ide_info)
    flow_filepath = os.path.join(args.output_dir, f"video_spec_{slug}.json")
    with open(flow_filepath, "w", encoding="utf-8") as f:
        json.dump(flow_spec, indent=2, fp=f)

    print(f"✨ Successfully generated content for {ide_info['name']}:")
    print(f"  📄 Blogger AMP Post: {amp_filepath}")
    print(f"  🎬 Google Flow Video Spec: {flow_filepath}")


if __name__ == "__main__":
    main()
