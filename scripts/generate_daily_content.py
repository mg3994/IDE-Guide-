#!/usr/bin/env python3
"""
Daily Content Generator for IDE Guide
Generates 3 daily AMP HTML blog posts for Blogger and 3 Google Flow video specification files.
"""

import os
import sys
import json
import datetime
from pathlib import Path

REQUIRED_DISCLAIMER = (
    "IDE Guide is an independent technical publication. This content is not sponsored, "
    "endorsed, or affiliated with any software vendor or editor developer mentioned above. "
    "All reviews and assessments are based strictly on objective developer evaluation."
)

IDE_DATABASE = [
    {
        "name": "Visual Studio Code",
        "slug": "vscode",
        "category": "Code Editor / Lightweight IDE",
        "pricing": "Free / Open Source (Core)",
        "pricing_type": "Free",
        "pros": [
            "Massive extension marketplace with thousands of plugins.",
            "Exceptional performance and lightweight footprint.",
            "Built-in Git integration and terminal.",
            "First-class TypeScript and JavaScript support."
        ],
        "cons": [
            "Requires configuration and plugins to reach full IDE status.",
            "Can suffer from high memory consumption with bloated extensions.",
            "Telemetry collection by default (requires opt-out)."
        ],
        "summary": "VS Code remains the reigning champion of general-purpose code editors due to its infinite customizability and vibrant plugin ecosystem.",
        "best_for": "Web developers, full-stack engineers, and multi-language programmers looking for a lightweight setup.",
        "icon_url": "https://raw.githubusercontent.com/vscode-icons/vscode-icons/master/icons/file_type_vscode.svg"
    },
    {
        "name": "Cursor IDE",
        "slug": "cursor",
        "category": "AI-Native Code Editor",
        "pricing": "Freemium ($20/mo for Pro)",
        "pricing_type": "Freemium",
        "pros": [
            "Deeply integrated AI context aware of entire codebase.",
            "Seamless VS Code extension compatibility.",
            "Instant inline AI code editing and natural language prompts.",
            "Multi-model selection (Claude 3.5 Sonnet, GPT-4o)."
        ],
        "cons": [
            "Pro tier required for heavy production usage.",
            "Requires active internet connection for advanced AI features.",
            "Closed source layer built on top of VSCodium."
        ],
        "summary": "Cursor is pioneering the AI-native editor space by turning the code editor into an intelligent pair programmer with codebase-wide awareness.",
        "best_for": "Developers wanting maximum AI productivity and seamless transition from VS Code.",
        "icon_url": "https://raw.githubusercontent.com/vscode-icons/vscode-icons/master/icons/file_type_cursor.svg"
    },
    {
        "name": "JetBrains IntelliJ IDEA",
        "slug": "intellij-idea",
        "category": "Full-Featured Java/Kotlin IDE",
        "pricing": "Freemium (Community Free / Ultimate Paid)",
        "pricing_type": "Freemium",
        "pros": [
            "Unrivaled refactoring and static analysis tools.",
            "Deep language understanding out of the box without complex setup.",
            "Comprehensive database and framework support in Ultimate edition.",
            "Superior debugger and profiler tools."
        ],
        "cons": [
            "Heavy RAM and CPU usage.",
            "Slower indexing on massive codebases.",
            "Ultimate license cost can be steep for individual developers."
        ],
        "summary": "IntelliJ IDEA is the gold standard for Java and Kotlin enterprise development, delivering unrivaled code intelligence.",
        "best_for": "Enterprise backend developers, Java/Kotlin engineers, and large enterprise codebases.",
        "icon_url": "https://raw.githubusercontent.com/vscode-icons/vscode-icons/master/icons/file_type_idea.svg"
    },
    {
        "name": "Zed Editor",
        "slug": "zed",
        "category": "Ultra-Fast High-Performance Editor",
        "pricing": "Free / Open Source",
        "pricing_type": "Free",
        "pros": [
            "Written in Rust with GPU-accelerated rendering.",
            "Instant startup time and zero UI latency.",
            "Built-in real-time collaborative editing features.",
            "Native AI integration."
        ],
        "cons": [
            "Ecosystem and extension marketplace still growing.",
            "Limited platform availability on certain legacy platforms.",
            "Fewer complex debugger integrations compared to mature IDEs."
        ],
        "summary": "Zed is a next-generation high-performance editor designed to leverage GPU acceleration and Rust to eliminate editor lag entirely.",
        "best_for": "Developers who value raw performance, instantaneous responsiveness, and minimal lag.",
        "icon_url": "https://raw.githubusercontent.com/vscode-icons/vscode-icons/master/icons/file_type_zed.svg"
    },
    {
        "name": "Neovim",
        "slug": "neovim",
        "category": "Modal Terminal-based Editor",
        "pricing": "Free / Open Source",
        "pricing_type": "Free",
        "pros": [
            "Blazing fast modal navigation and mouse-free productivity.",
            "Lua-based configuration for limitless customization.",
            "Built-in Language Server Protocol (LSP) client.",
            "Minimal resource footprint."
        ],
        "cons": [
            "Steep learning curve for keybindings.",
            "Significant time investment required to build custom setup.",
            "Not user-friendly for beginners without distribution setups (LazyVim, AstroNvim)."
        ],
        "summary": "Neovim modernizes classic Vim with extensible Lua scripting and built-in LSP, offering the ultimate keyboard-centric developer experience.",
        "best_for": "Command-line power users, sysadmins, and keyboard enthusiasts who demand total customization.",
        "icon_url": "https://raw.githubusercontent.com/vscode-icons/vscode-icons/master/icons/file_type_vim.svg"
    },
    {
        "name": "JetBrains PyCharm",
        "slug": "pycharm",
        "category": "Dedicated Python IDE",
        "pricing": "Freemium (Community Free / Professional Paid)",
        "pricing_type": "Freemium",
        "pros": [
            "Best-in-class Python code completion and inspection.",
            "Built-in Django, Flask, and FastAPI framework support.",
            "Integrated Jupyter Notebooks and Data Science tools in Pro edition.",
            "Seamless virtual environment and Conda management."
        ],
        "cons": [
            "High memory usage during indexing.",
            "Commercial tier required for web frameworks and database management.",
            "Slow launch time on older hardware."
        ],
        "summary": "PyCharm provides an environment specifically tuned for Python developers, from web backend development to data science.",
        "best_for": "Python developers, data engineers, and web backend specialists working with Django/Flask.",
        "icon_url": "https://raw.githubusercontent.com/vscode-icons/vscode-icons/master/icons/file_type_pycharm.svg"
    },
    {
        "name": "Fleet by JetBrains",
        "slug": "fleet",
        "category": "Lightweight Polyglot Editor",
        "pricing": "Freemium / Preview",
        "pricing_type": "Freemium",
        "pros": [
            "Lightweight UI with smart backend processing when needed.",
            "Multi-language support out of the box.",
            "Collaborative remote development enabled.",
            "Clean and clutter-free modern aesthetic."
        ],
        "cons": [
            "Still in active preview/development.",
            "Smaller plugin ecosystem than IntelliJ or VS Code.",
            "Some advanced IDE features still being added."
        ],
        "summary": "Fleet reimagines JetBrains' smart engine inside a sleek, lightweight editor that can transform from a quick editor into a full IDE.",
        "best_for": "Developers seeking JetBrains smart code intelligence in a minimal, modern interface.",
        "icon_url": "https://raw.githubusercontent.com/vscode-icons/vscode-icons/master/icons/file_type_fleet.svg"
    },
    {
        "name": "Sublime Text 4",
        "slug": "sublime-text",
        "category": "High-Speed Code Editor",
        "pricing": "Paid ($99 evaluated with free trial)",
        "pricing_type": "Paid",
        "pros": [
            "Lightning fast file loading and multi-cursor editing.",
            "GPU rendering engine for fluid 60+ FPS scrolling.",
            "Low CPU and memory usage.",
            "Cross-platform support."
        ],
        "cons": [
            "Evaluation popups if unlicensed.",
            "Lacks full out-of-the-box IDE features without manual Package Control plugins.",
            "One-time payment cost vs free alternatives."
        ],
        "summary": "Sublime Text remains the benchmark for raw speed and responsiveness in text editing, ideal for quick file tweaks or heavy coding.",
        "best_for": "Developers who want an instant-open editor with multi-cursor mastery and zero distraction.",
        "icon_url": "https://raw.githubusercontent.com/vscode-icons/vscode-icons/master/icons/file_type_sublime.svg"
    },
    {
        "name": "Helix Editor",
        "slug": "helix",
        "category": "Post-Modern Modal Terminal Editor",
        "pricing": "Free / Open Source",
        "pricing_type": "Free",
        "pros": [
            "Zero configuration required for LSP, syntax highlighting, and auto-complete.",
            "Written in Rust, incredibly responsive.",
            "Kakoune-inspired selection-first modal editing.",
            "Built-in tree-sitter integration."
        ],
        "cons": [
            "No plugin system yet (deliberately minimal design).",
            "Modal editing required, learning curve for traditional GUI users.",
            "Terminal-only UI."
        ],
        "summary": "Helix delivers a post-modern modal terminal editor experience that works out of the box with zero plugin configuration required.",
        "best_for": "Terminal enthusiasts looking for a batteries-included modal editor alternative to Vim.",
        "icon_url": "https://raw.githubusercontent.com/vscode-icons/vscode-icons/master/icons/file_type_helix.svg"
    }
]

def render_amp_blog_post(ide: dict, date_str: str) -> str:
    canonical_url = f"https://ideguide.blogspot.com/{date_str.replace('-', '/')}/{ide['slug']}-review.html"

    pros_html = "\n".join([f"        <li>✅ {p}</li>" for p in ide["pros"]])
    cons_html = "\n".join([f"        <li>❌ {c}</li>" for c in ide["cons"]])

    html = f"""<!doctype html>
<html ⚡ lang="en">
<head>
  <meta charset="utf-8">
  <title>{ide['name']} Review & Complete Developer Guide - IDE Guide</title>
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
    <p>{ide['name']} is best suited for <strong>{ide['best_for']}</strong>. If you prioritize {ide['pros'][0].lower()}, this is an outstanding candidate for your workflow.</p>
  </div>

  <div class="disclaimer-box">
    <strong>Disclaimer:</strong> {REQUIRED_DISCLAIMER}
  </div>
</body>
</html>"""
    return html

def render_google_flow_spec(ide: dict, date_str: str) -> dict:
    return {
        "channel": "@IDEguide",
        "date": date_str,
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
                "script": f"Is {ide['name']} still the best choice for your developer workflow in 2026? Let's break down the pros, cons, and pricing!"
            },
            {
                "scene_id": 2,
                "scene_type": "The Good (Strengths)",
                "duration_seconds": 12,
                "visual_prompt": f"Macro lens view of {ide['name']} interface showing fast code execution, intelligent auto-completion, and slick UI panels.",
                "camera_motion": "Smooth horizontal pan left to right across code view",
                "lighting": "Clean studio rim light highlighting screen details",
                "script": f"Here is what makes {ide['name']} great: {ide['pros'][0]} Plus, {ide['pros'][1]}"
            },
            {
                "scene_id": 3,
                "scene_type": "The Bad (Limitations)",
                "duration_seconds": 10,
                "visual_prompt": f"Close-up tilted frame highlighting complex settings menu or system resource usage indicators in {ide['name']}.",
                "camera_motion": "Subtle slow zoom out with slight tilt",
                "lighting": "Warm warning tint accent",
                "script": f"However, keep in mind: {ide['cons'][0]}"
            },
            {
                "scene_id": 4,
                "scene_type": "Pricing & Verdict",
                "duration_seconds": 8,
                "visual_prompt": f"High contrast motion graphics card displaying {ide['pricing']} badge, pros vs cons checklist, and final recommendation rating.",
                "camera_motion": "Static front-facing center focus",
                "lighting": "Bright balanced daylight setup",
                "script": f"Pricing model: {ide['pricing']}. Verdict: Best for {ide['best_for']}. Subscribe to IDE Guide for daily developer tool breakdowns!"
            }
        ],
        "disclaimer": REQUIRED_DISCLAIMER
    }

def get_history(history_file: str) -> list[str]:
    if os.path.exists(history_file):
        try:
            with open(history_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []
    return []

def save_history(history_file: str, history: list[str]):
    os.makedirs(os.path.dirname(history_file), exist_ok=True)
    with open(history_file, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=2)

def generate_daily_content(target_date: str = None) -> list[str]:
    if not target_date:
        target_date = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d")

    content_dir = os.path.join("content", target_date)
    os.makedirs(content_dir, exist_ok=True)

    history_file = os.path.join("content", "history.json")
    history = get_history(history_file)

    # Filter available IDEs not in recent history if possible
    available = [item for item in IDE_DATABASE if item["slug"] not in history]
    if len(available) < 3:
        # Reset or fallback if pool is depleted
        history = []
        available = IDE_DATABASE

    selected = available[:3]
    generated_files = []

    for idx, ide in enumerate(selected, 1):
        # Blog post filename
        blog_filename = f"post_{idx}_{ide['slug']}.html"
        blog_path = os.path.join(content_dir, blog_filename)
        blog_content = render_amp_blog_post(ide, target_date)
        with open(blog_path, "w", encoding="utf-8") as f:
            f.write(blog_content)
        generated_files.append(blog_path)

        # Video spec filename
        video_filename = f"video_{idx}_{ide['slug']}_google_flow.json"
        video_path = os.path.join(content_dir, video_filename)
        video_content = render_google_flow_spec(ide, target_date)
        with open(video_path, "w", encoding="utf-8") as f:
            json.dump(video_content, f, indent=2)
        generated_files.append(video_path)

        history.append(ide["slug"])

    save_history(history_file, history)
    return generated_files

def main():
    date_arg = sys.argv[1] if len(sys.argv) > 1 else None
    files = generate_daily_content(date_arg)
    print(f"Successfully generated {len(files)} content files:")
    for f in files:
        print(f"  - {f}")

if __name__ == "__main__":
    main()
