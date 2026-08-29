#!/usr/bin/env python3
"""
Generate Daily Content Package for IDE Guide.

Outputs 3 AMP HTML blog posts and 3 Google Flow Video Specs under content/YYYY-MM-DD/
Tracks covered IDEs in content/history.json to avoid duplicates.
"""

import json
import os
import sys
import datetime
import urllib.request
import urllib.error

DISCLAIMER_TEXT = (
    "Disclaimer: IDE Guide is an independent technical publication. "
    "This content is not sponsored, endorsed, or affiliated with any software vendor or editor developer "
    "mentioned above. All reviews and assessments are based strictly on objective developer evaluation."
)

IDE_CATALOG = [
    {
        "name": "Visual Studio Code",
        "slug": "vscode",
        "developer": "Microsoft",
        "pricing_model": "Free / Open Source (Core)",
        "license_type": "MIT (Core) / Proprietary distribution",
        "category": "General Purpose Code Editor",
        "pros": [
            "Extremely rich ecosystem with thousands of extensions",
            "Built-in Git integration and terminal",
            "Active community and frequent monthly updates",
            "Superior Remote Development (SSH, Containers, WSL)"
        ],
        "cons": [
            "Electron overhead can lead to high RAM consumption on large projects",
            "Telemetry enabled by default (requires opt-out)",
            "Heavy extension setups can slow down startup times"
        ],
        "verdict": "Best overall general-purpose editor for web, cloud, and full-stack developers looking for maximum flexibility and community support."
    },
    {
        "name": "Cursor",
        "slug": "cursor",
        "developer": "Anysphere",
        "pricing_model": "Freemium ($20/mo Pro)",
        "license_type": "Proprietary",
        "category": "AI-Native Code Editor",
        "pros": [
            "Deep inline AI code editing and multi-file code generation",
            "Native codebase indexing for natural language search",
            "Seamless VS Code extension compatibility",
            "Agentic AI capabilities for complex codebase refactoring"
        ],
        "cons": [
            "Paid tier required for high-volume fast AI requests",
            "Requires internet connectivity for advanced AI model features",
            "Proprietary cloud model dependencies for peak performance"
        ],
        "verdict": "Best for software engineers who want cutting-edge AI pair programming directly inside a familiar VS Code environment."
    },
    {
        "name": "Neovim",
        "slug": "neovim",
        "developer": "Neovim Core Team",
        "pricing_model": "Free / Open Source",
        "license_type": "Apache 2.0 / Vim",
        "category": "Terminal Modal Editor",
        "pros": [
            "Ultra-lightweight with near-instant startup speeds",
            "First-class Lua API for deep customization and plugin building",
            "Built-in LSP (Language Server Protocol) client and Treesitter parsing",
            "Extremely low memory footprint (< 50MB RAM)"
        ],
        "cons": [
            "Steep learning curve for modal editing and keybindings",
            "Requires time investment to configure initial environment",
            "No GUI by default (terminal-first)"
        ],
        "verdict": "Best for keyboard purists, terminal lovers, and power users seeking maximum performance and total control over their editor."
    },
    {
        "name": "Zed",
        "slug": "zed",
        "developer": "Zed Industries",
        "pricing_model": "Free / Open Source (Core)",
        "license_type": "GPL-3.0 / AGPL-3.0",
        "category": "High-Performance Code Editor",
        "pros": [
            "Written in Rust, utilizing GPU hardware acceleration for 120 FPS rendering",
            "Blazing fast file scanning and instant project open times",
            "Built-in collaborative multiplayer coding features",
            "Low CPU and RAM resource usage compared to Electron apps"
        ],
        "cons": [
            "Ecosystem is newer compared to VS Code",
            "Extension market still expanding",
            "Currently Linux and macOS focused"
        ],
        "verdict": "Best for developers demanding peak responsiveness and low latency without sacrificing modern editor features."
    },
    {
        "name": "JetBrains PyCharm",
        "slug": "pycharm",
        "developer": "JetBrains",
        "pricing_model": "Freemium (Free Community / $249/yr Professional)",
        "license_type": "Apache 2.0 (Community) / Proprietary (Professional)",
        "category": "Python Specialized IDE",
        "pros": [
            "Unrivaled code navigation, refactoring, and static code inspection",
            "Built-in Django, Flask, FastAPI support in Professional edition",
            "Integrated database tool window and scientific notebooks",
            "Comprehensive visual debugger and test runner"
        ],
        "cons": [
            "Heavy RAM consumption (~1.5GB+ active usage)",
            "Indexing large codebases can take time on initial launch",
            "Advanced features locked behind paid Professional tier"
        ],
        "verdict": "Best for serious Python developers and data engineers needing end-to-end tooling and deep code analysis."
    },
    {
        "name": "Helix",
        "slug": "helix",
        "developer": "Helix Contributors",
        "pricing_model": "Free / Open Source",
        "license_type": "MPL-2.0",
        "category": "Post-Modern Terminal Editor",
        "pros": [
            "Zero-configuration required: LSP, Treesitter, and themes built-in",
            "Selection-first (selection -> action) editing model",
            "Written in Rust with zero startup delay",
            "Pure terminal experience with modern UI overlays"
        ],
        "cons": [
            "Different keybinding paradigm than standard Vim/Vimscript",
            "No plugin system yet (all features built into core)",
            "Terminal graphics limitations depending on emulator"
        ],
        "verdict": "Best for terminal-centric developers looking for an out-of-the-box modal editor without spending hours writing config files."
    }
]

def load_history(history_file="content/history.json"):
    if os.path.exists(history_file):
        try:
            with open(history_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {"covered_ides": [], "last_updated": ""}

def save_history(history_data, history_file="content/history.json"):
    os.makedirs(os.path.dirname(history_file), exist_ok=True)
    with open(history_file, "w", encoding="utf-8") as f:
        json.dump(history_data, f, indent=2)

def fetch_trending_github_ides():
    """Attempt to discover IDE projects from GitHub API; fallback gracefully."""
    url = "https://api.github.com/search/repositories?q=topic:ide+topic:code-editor&sort=stars&order=desc"
    req = urllib.request.Request(url, headers={"User-Agent": "IDE-Guide-Bot"})
    discovered = []
    try:
        with urllib.request.urlopen(req, timeout=5) as response:
            if response.status == 200:
                data = json.loads(response.read().decode())
                for item in data.get("items", []):
                    discovered.append({
                        "name": item.get("name").capitalize(),
                        "slug": item.get("name").lower(),
                        "developer": item.get("owner", {}).get("login", "Open Source Community"),
                        "pricing_model": "Free / Open Source",
                        "license_type": (item.get("license") or {}).get("spdx_id", "Open Source") or "Open Source",
                        "category": "Open Source Code Editor",
                        "pros": [
                            f"Popular repository with {item.get('stargazers_count', 0):,} GitHub stars",
                            f"Description: {item.get('description', 'Modern code editor')}",
                            "Active open-source community development",
                            "Transparent codebase and community-driven features"
                        ],
                        "cons": [
                            "May require building from source or setup configuration",
                            "Ecosystem depends on community contributions",
                            "Documentation may vary across releases"
                        ],
                        "verdict": f"A highly promising open-source editor project ({item.get('name')}) worth watching for developers who value community-driven software."
                    })
    except Exception as e:
        print(f"GitHub API discovery skipped or offline ({e}). Using curated catalog fallback.")
    return discovered

def get_target_ides(count=3, history_file="content/history.json"):
    history = load_history(history_file)
    covered = set(history.get("covered_ides", []))

    available = []
    # Combine github discovered + curated catalog
    github_ides = fetch_trending_github_ides()
    candidates = github_ides + IDE_CATALOG

    seen_slugs = set()
    for ide in candidates:
        slug = ide["slug"]
        if slug not in covered and slug not in seen_slugs:
            available.append(ide)
            seen_slugs.add(slug)

    # If we ran out of new IDEs, reset covered list to allow rotation
    if len(available) < count:
        print("All catalog IDEs covered! Resetting covered list to enable rotation cycle.")
        covered = set()
        history["covered_ides"] = []
        available = []
        for ide in IDE_CATALOG:
            if ide["slug"] not in seen_slugs:
                available.append(ide)
                seen_slugs.add(ide["slug"])

    return available[:count]

def generate_amp_html_blog_post(ide):
    def format_list_item(item, default_label):
        if ":" in item:
            label, rest = item.split(":", 1)
            return f"      <li><strong>{label.strip()}:</strong> {rest.strip()}</li>"
        return f"      <li><strong>{default_label}:</strong> {item}</li>"

    pros_html = "\n".join([format_list_item(p, "Feature") for p in ide['pros']])
    cons_html = "\n".join([format_list_item(c, "Drawback") for c in ide['cons']])

    html_content = f"""<!doctype html>
<html ⚡ lang="en">
<head>
  <meta charset="utf-8">
  <title>{ide['name']} Review & Developer Guide | IDE Guide</title>
  <link rel="canonical" href="https://ideguide.blogspot.com/p/{ide['slug']}-review.html">
  <meta name="viewport" content="width=device-width,minimum-scale=1,initial-scale=1">
  <script async src="https://cdn.ampproject.org/v0.js"></script>
  <style amp-boilerplate>body{{-webkit-animation:-amp-start 8s steps(1,end) 0s 1 normal both;-moz-animation:-amp-start 8s steps(1,end) 0s 1 normal both;-ms-animation:-amp-start 8s steps(1,end) 0s 1 normal both;animation:-amp-start 8s steps(1,end) 0s 1 normal both}}@-webkit-keyframes -amp-start{{from{{visibility:hidden}}to{{visibility:visible}}}}@-moz-keyframes -amp-start{{from{{visibility:hidden}}to{{visibility:visible}}}}@-ms-keyframes -amp-start{{from{{visibility:hidden}}to{{visibility:visible}}}}@-o-keyframes -amp-start{{from{{visibility:hidden}}to{{visibility:visible}}}}@keyframes -amp-start{{from{{visibility:hidden}}to{{visibility:visible}}}}</style><noscript><style amp-boilerplate>body{{-webkit-animation:none;-moz-animation:none;-ms-animation:none;animation:none}}</style></noscript>
  <style amp-custom>
    body {{
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
      line-height: 1.6;
      color: #1e1e2e;
      background-color: #f8f9fa;
      margin: 0;
      padding: 0;
    }}
    header {{
      background: #181825;
      color: #cba6f7;
      padding: 24px;
      text-align: center;
    }}
    header h1 {{
      margin: 0;
      font-size: 2rem;
    }}
    header p {{
      color: #a6adc8;
      margin: 8px 0 0 0;
    }}
    .container {{
      max-width: 800px;
      margin: 30px auto;
      background: #ffffff;
      padding: 30px;
      border-radius: 12px;
      box-shadow: 0 4px 15px rgba(0,0,0,0.05);
    }}
    .badge {{
      display: inline-block;
      background: #89b4fa;
      color: #11111b;
      padding: 4px 12px;
      border-radius: 16px;
      font-weight: bold;
      font-size: 0.85rem;
      margin-bottom: 16px;
    }}
    h2 {{
      color: #11111b;
      border-bottom: 2px solid #89b4fa;
      padding-bottom: 6px;
      margin-top: 28px;
    }}
    .pros-cons {{
      display: flex;
      flex-wrap: wrap;
      gap: 20px;
      margin: 20px 0;
    }}
    .box {{
      flex: 1;
      min-width: 280px;
      padding: 20px;
      border-radius: 8px;
    }}
    .pros {{ background: #e6ffed; border-left: 5px solid #2da44e; }}
    .cons {{ background: #ffebe9; border-left: 5px solid #cf222e; }}
    .verdict-box {{
      background: #f1f5f9;
      border-left: 5px solid #89b4fa;
      padding: 20px;
      margin-top: 25px;
      border-radius: 6px;
    }}
    .disclaimer-box {{
      background: #fff8e6;
      border: 1px solid #ffe0b2;
      color: #795548;
      font-size: 0.85rem;
      padding: 16px;
      border-radius: 8px;
      margin-top: 35px;
    }}
  </style>
</head>
<body>
  <header>
    <h1>IDE Guide: {ide['name']} Assessment</h1>
    <p>Objective Technical Review for Developers | Blogger Edition (AMP Compliant)</p>
  </header>

  <div class="container">
    <span class="badge">{ide['category']}</span>
    <p>Welcome to this comprehensive technical analysis of <strong>{ide['name']}</strong>, developed by <em>{ide['developer']}</em>.</p>

    <h2>Pricing & Licensing Model</h2>
    <p><strong>Pricing:</strong> {ide['pricing_model']}</p>
    <p><strong>License:</strong> {ide['license_type']}</p>

    <h2>Pros & Cons Breakdown</h2>
    <div class="pros-cons">
      <div class="box pros">
        <h3>What Makes It Great (Pros)</h3>
        <ul>
{pros_html}
        </ul>
      </div>
      <div class="box cons">
        <h3>Areas for Improvement (Cons)</h3>
        <ul>
{cons_html}
        </ul>
      </div>
    </div>

    <h2>Final Verdict & Recommendation</h2>
    <div class="verdict-box">
      <p>{ide['verdict']}</p>
    </div>

    <div class="disclaimer-box">
      <strong>Notice:</strong> {DISCLAIMER_TEXT}
    </div>
  </div>
</body>
</html>
"""
    return html_content

def generate_google_flow_video_spec(ide):
    spec = {
        "channel": "@IDEguide",
        "video_title": f"{ide['name']} Review: Is It The Best Code Editor in 2026? (Pros, Cons & Pricing)",
        "ide_name": ide["name"],
        "developer": ide["developer"],
        "pricing": ide["pricing_model"],
        "target_formats": [
            {
                "type": "YouTube Main Video",
                "aspect_ratio": "16:9",
                "resolution": "3840x2160 (4K UHD)",
                "duration_seconds": 180
            },
            {
                "type": "YouTube Shorts",
                "aspect_ratio": "9:16",
                "resolution": "1080x1920",
                "duration_seconds": 59
            }
        ],
        "google_flow_visual_prompts": {
            "style_preset": "Cyberpunk Dark Tech",
            "lighting": "Soft volumetric dark-room glow with vibrant syntax highlight neon tones",
            "camera_angles": [
                "Macro close-up on IDE editor cursor and code completion popups",
                "Over-the-shoulder shot of developer working in modern dark workspace",
                "Split-screen comparison showing side-by-side performance benchmarks"
            ],
            "scene_sequence": [
                {
                    "scene": 1,
                    "name": "Hook & Title",
                    "visual_prompt": f"Cinematic close-up of {ide['name']} UI loading code on a curved OLED monitor, dark aesthetic, neon glowing code syntax.",
                    "audio_script": f"Is {ide['name']} worth switching to today? Let's analyze its pros, cons, and performance in 60 seconds."
                },
                {
                    "scene": 2,
                    "name": "Pricing & Overview",
                    "visual_prompt": f"Clean graphic overlay listing pricing model: {ide['pricing_model']}. High tech UI graphics.",
                    "audio_script": f"{ide['name']} is created by {ide['developer']}. It operates under a {ide['pricing_model']} model."
                },
                {
                    "scene": 3,
                    "name": "Pros & Standout Features",
                    "visual_prompt": f"Dynamic camera panning across {ide['name']} interface highlighting features: {', '.join(ide['pros'][:2])}.",
                    "audio_script": f"Top strengths include: {ide['pros'][0]}. Plus, {ide['pros'][1]}."
                },
                {
                    "scene": 4,
                    "name": "Cons & Limitations",
                    "visual_prompt": "Split red-tinted UI overlay showing potential resource bottlenecks or configuration challenges.",
                    "audio_script": f"However, keep in mind: {ide['cons'][0]}."
                },
                {
                    "scene": 5,
                    "name": "Verdict & Recommendation",
                    "visual_prompt": f"Final score badge popping up over sleek desk setup with {ide['name']} on screen.",
                    "audio_script": f"Our verdict: {ide['verdict']}"
                },
                {
                    "scene": 6,
                    "name": "Disclaimer Banner",
                    "visual_prompt": "Clean text overlay displaying non-sponsorship disclosure at bottom third of frame.",
                    "audio_script": DISCLAIMER_TEXT
                }
            ]
        },
        "disclaimer": DISCLAIMER_TEXT
    }
    return spec

def main():
    date_str = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d")
    output_dir = os.path.join("content", date_str)
    os.makedirs(output_dir, exist_ok=True)

    history_file = "content/history.json"
    history = load_history(history_file)

    target_ides = get_target_ides(count=3, history_file=history_file)
    print(f"Generating content for {len(target_ides)} IDEs for date: {date_str}")

    generated_slugs = []
    for idx, ide in enumerate(target_ides, 1):
        slug = ide["slug"]
        print(f"[{idx}/3] Processing {ide['name']} ({slug})...")

        # AMP HTML Blog Post
        amp_html = generate_amp_html_blog_post(ide)
        blog_filename = f"blog_post_{idx}_{slug}.html"
        with open(os.path.join(output_dir, blog_filename), "w", encoding="utf-8") as f:
            f.write(amp_html)

        # Google Flow Video Spec
        video_spec = generate_google_flow_video_spec(ide)
        spec_filename = f"video_spec_{idx}_{slug}.json"
        with open(os.path.join(output_dir, spec_filename), "w", encoding="utf-8") as f:
            json.dump(video_spec, f, indent=2)

        generated_slugs.append(slug)

    # Update history
    covered = history.get("covered_ides", [])
    for s in generated_slugs:
        if s not in covered:
            covered.append(s)
    history["covered_ides"] = covered
    history["last_updated"] = date_str
    save_history(history, history_file)

    print(f"Successfully generated 3 blog posts and 3 video specs in {output_dir}/")
    print(f"Updated {history_file}")

if __name__ == "__main__":
    main()
