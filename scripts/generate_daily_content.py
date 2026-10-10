#!/usr/bin/env python3
"""
Daily Content Generator for IDE Guide.

Generates 3 daily packages (3 AMP HTML blog posts for Blogger + 3 Google Flow video specs for YouTube)
in content/YYYY-MM-DD/ and updates content/history.json to track covered tools.
"""

import os
import json
import datetime
from typing import Dict, Any, List

DISCLAIMER_TEXT = (
    "Disclaimer: IDE Guide is an independent technical publication. "
    "This content is not sponsored, endorsed, or affiliated with any software vendor or "
    "editor developer mentioned above. All reviews and assessments are based strictly on objective developer evaluation."
)

# Pool of popular and emerging IDEs & Code Editors
IDE_DATABASE = [
    {
        "id": "cursor",
        "name": "Cursor AI Code Editor",
        "category": "AI-First Code Editor",
        "pricing": "Freemium ($20/mo Pro)",
        "is_free": False,
        "license": "Proprietary (VS Code Fork)",
        "developer": "Anysphere",
        "tagline": "The AI-first code editor built for hyper-productive software engineering.",
        "pros": [
            "Deep repository-wide codebase indexing and context understanding.",
            "Native multi-file edits via Cmd+K and Composer.",
            "Seamless drop-in migration for VS Code extensions and settings."
        ],
        "cons": [
            "Requires monthly subscription for high-fast Claude 3.5 Sonnet queries.",
            "Closed-source proprietary layer over open VS Code core.",
            "Higher memory usage when indexing multi-gigabyte repositories."
        ],
        "best_for": "Full-stack and AI-assisted developers seeking ultra-fast code generation and refactoring.",
        "image_url": "https://images.unsplash.com/photo-1555066931-4365d14bab8c?w=800&auto=format&fit=crop&q=80"
    },
    {
        "id": "zed",
        "name": "Zed Code Editor",
        "category": "High-Performance Editor",
        "pricing": "Free / Open Source",
        "is_free": True,
        "license": "GPL-3.0 / Apache-2.0",
        "developer": "Zed Industries",
        "tagline": "Next-generation high-performance multiplayer code editor written in Rust.",
        "pros": [
            "Blazing fast GPU-accelerated rendering at 120+ FPS.",
            "Native multiplayer real-time pair programming.",
            "Extremely low memory footprint compared to Electron editors."
        ],
        "cons": [
            "Ecosystem of plugins and extensions is still maturing.",
            "Linux/Windows support is newer compared to macOS build.",
            "Fewer built-in debugging features out-of-the-box."
        ],
        "best_for": "Developers who prioritize raw editor speed, minimal latency, and native pair programming.",
        "image_url": "https://images.unsplash.com/photo-1517694712202-14dd9538aa97?w=800&auto=format&fit=crop&q=80"
    },
    {
        "id": "windsurf",
        "name": "Windsurf Editor (Codeium)",
        "category": "AI Flow Editor",
        "pricing": "Freemium ($15/mo Pro)",
        "is_free": False,
        "license": "Proprietary",
        "developer": "Codeium",
        "tagline": "Agentic AI code editor featuring Cascade flow technology.",
        "pros": [
            "Cascade AI agent flows combine deep contextual awareness with actions.",
            "Free tier offers generous monthly AI completions.",
            "Rich terminal and command integration."
        ],
        "cons": [
            "Relatively new tool with evolving user interface patterns.",
            "Requires steady cloud network connectivity for AI agent execution.",
            "Occasional context hallucination in niche programming languages."
        ],
        "best_for": "Engineers looking for autonomous agentic AI workflows integrated directly into their editor.",
        "image_url": "https://images.unsplash.com/photo-1542831371-29b0f74f9713?w=800&auto=format&fit=crop&q=80"
    },
    {
        "id": "vscode",
        "name": "Visual Studio Code",
        "category": "General Purpose Editor",
        "pricing": "Free (Open Core)",
        "is_free": True,
        "license": "MIT / Microsoft Binary",
        "developer": "Microsoft",
        "tagline": "The world's most popular extensible code editor.",
        "pros": [
            "Unrivaled ecosystem with tens of thousands of extensions.",
            "Built-in Git control, terminal, and remote SSH / container development.",
            "Backed by huge community and industry standard language servers."
        ],
        "cons": [
            "Electron architecture causes noticeable RAM consumption on large workspaces.",
            "Heavy extension configurations can slow down cold launch times.",
            "Telemetry enabled by default in official Microsoft builds."
        ],
        "best_for": "Developers of all skill levels needing a versatile, ecosystem-rich development environment.",
        "image_url": "https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?w=800&auto=format&fit=crop&q=80"
    },
    {
        "id": "neovim",
        "name": "Neovim",
        "category": "Modal Terminal Editor",
        "pricing": "Free / Open Source",
        "is_free": True,
        "license": "Apache-2.0 / Vim License",
        "developer": "Neovim Core Team",
        "tagline": "Hyperextensible Vim-based text editor for keyboard-driven power users.",
        "pros": [
            "Instant launch times and near-zero memory footprint.",
            "Lua-first configuration engine with asynchronous LSP & Treesitter support.",
            "Runs inside any terminal session or remote SSH headless machine."
        ],
        "cons": [
            "Steep learning curve for modal editing and custom configuration.",
            "Requires manual plugin orchestration and maintenance.",
            "No out-of-the-box GUI unless paired with external frontends like Neovide."
        ],
        "best_for": "Terminal power users, DevOps engineers, and minimalists who demand total control.",
        "image_url": "https://images.unsplash.com/photo-1629654297299-c8506221ca97?w=800&auto=format&fit=crop&q=80"
    },
    {
        "id": "intellij",
        "name": "IntelliJ IDEA",
        "category": "Enterprise Java & Polyglot IDE",
        "pricing": "Freemium ($169/yr Ultimate / Free Community)",
        "is_free": False,
        "license": "Apache-2.0 / Commercial",
        "developer": "JetBrains",
        "tagline": "The premier IDE for Java, Kotlin, and enterprise backend engineering.",
        "pros": [
            "Unmatched deep code analysis, automated refactoring, and static safety.",
            "Comprehensive built-in database management, profiler, and HTTP client.",
            "Industry standard for enterprise microservices and Kotlin development."
        ],
        "cons": [
            "Heavy system resource requirements (requires 16GB+ RAM for smooth usage).",
            "Full feature set locked behind paid Ultimate license.",
            "Initial project indexing can be slow on large monorepos."
        ],
        "best_for": "Enterprise Java/Kotlin developers and backend system architects.",
        "image_url": "https://images.unsplash.com/photo-1516116211223-4c7141326c65?w=800&auto=format&fit=crop&q=80"
    },
    {
        "id": "pycharm",
        "name": "PyCharm",
        "category": "Python Dedicated IDE",
        "pricing": "Freemium ($99/yr Professional / Free Community)",
        "is_free": False,
        "license": "Apache-2.0 / Commercial",
        "developer": "JetBrains",
        "tagline": "The intelligent Python IDE with deep framework and data science support.",
        "pros": [
            "Out-of-the-box support for Django, Flask, FastAPI, and Jupyter notebooks.",
            "Integrated virtualenv/Conda management and scientific interactive mode.",
            "Powerful SQL database tools and remote SSH/Docker interpreters."
        ],
        "cons": [
            "Resource heavy startup and indexing.",
            "Web framework tools locked behind Professional edition.",
            "Can feel overly complex for single-file scripts."
        ],
        "best_for": "Professional Python developers, data scientists, and Django web engineers.",
        "image_url": "https://images.unsplash.com/photo-1526379095098-d400fd0bf935?w=800&auto=format&fit=crop&q=80"
    },
    {
        "id": "helix",
        "name": "Helix Editor",
        "category": "Modal Terminal Editor",
        "pricing": "Free / Open Source",
        "is_free": True,
        "license": "MPL-2.0",
        "developer": "Helix Community",
        "tagline": "Post-modern modal text editor built in Rust with zero configuration needed.",
        "pros": [
            "Built-in Tree-sitter syntax highlighting and LSP integration out of the box.",
            "Selection-first editing paradigm (selection -> action) inspired by Kakoune.",
            "Written in Rust for maximum memory efficiency and speed."
        ],
        "cons": [
            "Plugin system is still under design and development.",
            "Different keybindings than traditional Vim require muscle memory adjustment.",
            "Terminal-only interface by default."
        ],
        "best_for": "Developers wanting Neovim-like speed without spending hours configuring plugins.",
        "image_url": "https://images.unsplash.com/photo-1550751827-4bd374c3f58b?w=800&auto=format&fit=crop&q=80"
    },
    {
        "id": "sublime",
        "name": "Sublime Text 4",
        "category": "Lightweight Code Editor",
        "pricing": "Paid ($99 / Evaluation mode)",
        "is_free": False,
        "license": "Commercial Proprietary",
        "developer": "Sublime HQ",
        "tagline": "A sophisticated text editor for code, markup, and prose with ultra-fast responsiveness.",
        "pros": [
            "Instant launch speed and microscopic RAM usage.",
            "GPU rendering engine for buttery smooth scrolling at high refresh rates.",
            "Extensive Package Control system with Python plugins."
        ],
        "cons": [
            "Persistent pop-ups when using without purchasing a license.",
            "Out-of-the-box LSP features require manual package installation.",
            "Slower release cycle compared to open-source competitors."
        ],
        "best_for": "Developers who want an ultra-fast, lightweight desktop editor for code snippets and large text files.",
        "image_url": "https://images.unsplash.com/photo-1507238691740-187a5b1d37b8?w=800&auto=format&fit=crop&q=80"
    }
]


def generate_amp_blog_post(ide: Dict[str, Any]) -> str:
    """Generates a valid AMP HTML blog post for Blogger compliant with AMP specs."""
    pros_html = "\n".join([f"      <li><strong>Pro:</strong> {pro}</li>" for pro in ide["pros"]])
    cons_html = "\n".join([f"      <li><strong>Con:</strong> {con}</li>" for con in ide["cons"]])

    pricing_badge_color = "#2e7d32" if ide["is_free"] else "#d84315"

    html = f"""<!doctype html>
<html ⚡ lang="en">
<head>
  <meta charset="utf-8">
  <title>{ide['name']} Review & Developer Guide - IDE Guide</title>
  <link rel="canonical" href="https://ideguide.blogspot.com/">
  <meta name="viewport" content="width=device-width,minimum-scale=1,initial-scale=1">
  <script async src="https://cdn.ampproject.org/v0.js"></script>
  <style amp-boilerplate>body{{-webkit-animation:-amp-start 8s steps(1,end) 0s 1 normal both;-moz-animation:-amp-start 8s steps(1,end) 0s 1 normal both;-ms-animation:-amp-start 8s steps(1,end) 0s 1 normal both;animation:-amp-start 8s steps(1,end) 0s 1 normal both}}@-webkit-keyframes -amp-start{{from{{visibility:hidden}}to{{visibility:visible}}}}@-moz-keyframes -amp-start{{from{{visibility:hidden}}to{{visibility:visible}}}}@-ms-keyframes -amp-start{{from{{visibility:hidden}}to{{visibility:visible}}}}@-o-keyframes -amp-start{{from{{visibility:hidden}}to{{visibility:visible}}}}@keyframes -amp-start{{from{{visibility:hidden}}to{{visibility:visible}}}}</style><noscript><style amp-boilerplate>body{{-webkit-animation:none;-moz-animation:none;-ms-animation:none;animation:none}}</style></noscript>
  <style amp-custom>
    body {{
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
      line-height: 1.6;
      color: #1a1a1a;
      background-color: #f8f9fa;
      margin: 0;
      padding: 16px;
    }}
    article {{
      max-width: 800px;
      margin: 0 auto;
      background: #ffffff;
      padding: 24px;
      border-radius: 8px;
      box-shadow: 0 2px 8px rgba(0,0,0,0.08);
    }}
    header {{
      border-bottom: 2px solid #e0e0e0;
      padding-bottom: 16px;
      margin-bottom: 20px;
    }}
    h1 {{
      font-size: 28px;
      color: #0f172a;
      margin-bottom: 8px;
    }}
    .badge {{
      display: inline-block;
      padding: 4px 12px;
      border-radius: 16px;
      color: #ffffff;
      font-size: 14px;
      font-weight: bold;
      background-color: {pricing_badge_color};
    }}
    .meta-tag {{
      display: inline-block;
      padding: 4px 10px;
      background-color: #e2e8f0;
      color: #334155;
      border-radius: 4px;
      font-size: 13px;
      margin-left: 8px;
    }}
    .tagline {{
      font-style: italic;
      color: #475569;
      font-size: 16px;
      margin-top: 12px;
    }}
    h2 {{
      font-size: 20px;
      color: #1e293b;
      margin-top: 24px;
      border-left: 4px solid #2563eb;
      padding-left: 10px;
    }}
    ul {{
      padding-left: 20px;
    }}
    li {{
      margin-bottom: 8px;
    }}
    .verdict-box {{
      background-color: #eff6ff;
      border: 1px solid #bfdbfe;
      padding: 16px;
      border-radius: 6px;
      margin-top: 20px;
    }}
    footer {{
      margin-top: 32px;
      padding-top: 16px;
      border-top: 1px solid #e2e8f0;
      font-size: 13px;
      color: #64748b;
    }}
    .disclaimer {{
      background-color: #f1f5f9;
      padding: 12px;
      border-radius: 6px;
      border-left: 3px solid #64748b;
      margin-top: 20px;
    }}
  </style>
</head>
<body>
  <article>
    <header>
      <h1>{ide['name']} Complete Developer Guide & Analysis</h1>
      <div>
        <span class="badge">{ide['pricing']}</span>
        <span class="meta-tag">{ide['category']}</span>
        <span class="meta-tag">Developer: {ide['developer']}</span>
      </div>
      <p class="tagline">"{ide['tagline']}"</p>
    </header>

    <section>
      <amp-img src="{ide['image_url']}" width="800" height="450" layout="responsive" alt="{ide['name']} screenshot preview"></amp-img>
    </section>

    <section>
      <h2>Overview</h2>
      <p>{ide['name']} ({ide['license']}) is a leading solution in the {ide['category']} category. Developed by {ide['developer']}, it aims to streamline modern software engineering workflows with targeted developer tools and editor optimizations.</p>
    </section>

    <section>
      <h2>The Good (Pros)</h2>
      <ul>
{pros_html}
      </ul>
    </section>

    <section>
      <h2>The Bad (Cons)</h2>
      <ul>
{cons_html}
      </ul>
    </section>

    <section>
      <h2>Pricing & Licensing Breakdown</h2>
      <p><strong>Licensing Model:</strong> {ide['license']}</p>
      <p><strong>Pricing:</strong> {ide['pricing']}</p>
      <p>Whether you are working on open-source projects or enterprise applications, evaluating {ide['name']}'s pricing structure ensures you pick the most cost-effective developer tool for your stack.</p>
    </section>

    <section class="verdict-box">
      <h2>Best For & Verdict</h2>
      <p><strong>Ideal Use Case:</strong> {ide['best_for']}</p>
      <p>If your project demands high efficiency and strong ecosystem integration, {ide['name']} is a top-tier choice in today's software development landscape.</p>
    </section>

    <footer>
      <div class="disclaimer">
        <p>{DISCLAIMER_TEXT}</p>
      </div>
    </footer>
  </article>
</body>
</html>
"""
    return html


def generate_google_flow_video_spec(ide: Dict[str, Any]) -> Dict[str, Any]:
    """Generates a complete Google Flow video specification JSON for YouTube (@IDEguide)."""
    return {
        "channel": "@IDEguide",
        "title": f"Should You Use {ide['name']} in 2026? Pros, Cons & Paid vs Free Breakdown!",
        "ide_name": ide["name"],
        "category": ide["category"],
        "pricing_status": ide["pricing"],
        "is_free": ide["is_free"],
        "license": ide["license"],
        "target_audience": "Software Developers, Devs, Computer Science Students",
        "target_format": "YouTube Short / Reel (9:16 vertical) & Widescreen (16:9)",
        "duration_seconds": 60,
        "visual_style": {
            "environment": "Dark mode modern developer studio, glowing ultra-wide monitor, subtle neon rim lighting",
            "camera": "Dynamic 4K camera movements, smooth dolly push-ins, macro closeups on editor UI",
            "pacing": "Fast-paced, energetic technical commentary"
        },
        "scenes": [
            {
                "scene_id": 1,
                "timestamp": "0:00 - 0:10",
                "purpose": "Hook & IDE Introduction",
                "google_flow_prompt": f"Cinematic dark-mode developer setup with a glowing screen showing {ide['name']} UI. Cyberpunk dark blue and purple ambient lighting. Smooth slow zoom into the editor code interface, crisp syntax highlighting, 8k resolution, photorealistic.",
                "screen_action": f"Display {ide['name']} logo with title overlay: '{ide['name']}: Best choice or overrated?'",
                "voiceover_script": f"Is {ide['name']} actually worth your time, or is it just hype? Let's break down the pros, cons, and pricing in 60 seconds!",
                "text_overlay": f"{ide['name']} Review"
            },
            {
                "scene_id": 2,
                "timestamp": "0:10 - 0:25",
                "purpose": "The Good (Pros)",
                "google_flow_prompt": f"Ultra-detailed close up shot of developer hands typing rapidly on a mechanical keyboard in a modern illuminated desk setting. On-screen interface showing lightning fast code suggestions and refactoring in {ide['name']}.",
                "screen_action": f"Highlight top feature: {ide['pros'][0]}",
                "voiceover_script": f"Here's what makes it awesome: First, {ide['pros'][0]} Plus, {ide['pros'][1]}",
                "text_overlay": "PROS: High Efficiency & Great UX"
            },
            {
                "scene_id": 3,
                "timestamp": "0:25 - 0:40",
                "purpose": "The Bad (Cons)",
                "google_flow_prompt": f"Split screen transition showing memory monitor graph peaking alongside developer inspecting code settings. Dynamic camera tilt with subtle warm warning orange lighting accents.",
                "screen_action": f"Show caution badge and callout: {ide['cons'][0]}",
                "voiceover_script": f"But watch out for the downside: {ide['cons'][0]}",
                "text_overlay": "CONS: Key Drawbacks"
            },
            {
                "scene_id": 4,
                "timestamp": "0:40 - 0:55",
                "purpose": "Pricing & Who It's Best For",
                "google_flow_prompt": f"Clean sleek 3D graphic overlay of pricing card floating above developer workstation with smooth light reflections. Text badges for {ide['pricing']}.",
                "screen_action": f"Display Pricing Badge: {ide['pricing']} | Best For: {ide['best_for']}",
                "voiceover_script": f"Pricing-wise, it's {ide['pricing']}. It is best suited for {ide['best_for']}.",
                "text_overlay": f"PRICING: {ide['pricing']}"
            },
            {
                "scene_id": 5,
                "timestamp": "0:55 - 1:00",
                "purpose": "Call to Action & Non-Sponsorship Disclaimer",
                "google_flow_prompt": "Cinematic end screen with IDE Guide logo bouncing subtly over a clean dark ambient coding background. On-screen disclaimer text box.",
                "screen_action": "Subscribe to @IDEguide & Read Full Review on ideguide.blogspot.com",
                "voiceover_script": "Subscribe to IDE Guide for daily unbiased dev tool reviews! We are 100% independent and unsponsored.",
                "text_overlay": "Subscribe to @IDEguide | ideguide.blogspot.com"
            }
        ],
        "disclaimer": DISCLAIMER_TEXT
    }


def main():
    today_str = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d")
    output_dir = os.path.join("content", today_str)
    os.makedirs(output_dir, exist_ok=True)

    history_path = os.path.join("content", "history.json")
    history = {"covered_ides": [], "daily_logs": {}}
    if os.path.exists(history_path):
        try:
            with open(history_path, 'r', encoding='utf-8') as f:
                history = json.load(f)
        except Exception:
            pass

    covered_ids = set(history.get("covered_ides", []))

    # Pick 3 IDEs from database not yet covered if possible
    available_ides = [ide for ide in IDE_DATABASE if ide["id"] not in covered_ids]
    if len(available_ides) < 3:
        # Reset pool if exhausted
        covered_ids.clear()
        available_ides = IDE_DATABASE

    selected_ides = available_ides[:3]

    summary_lines = [
        f"# IDE Guide Daily Content Summary - {today_str}",
        "",
        "Target Platforms:",
        "- Blogger: [ideguide.blogspot.com](https://ideguide.blogspot.com/)",
        "- YouTube: [@IDEguide](https://www.youtube.com/@IDEguide)",
        "",
        "## Today's Generated Packages (3 Blog Posts + 3 Google Flow Video Specs)",
        ""
    ]

    daily_entry = []

    for idx, ide in enumerate(selected_ides, 1):
        slug = ide["id"]

        # 1. Generate AMP HTML blog post
        amp_html = generate_amp_blog_post(ide)
        post_filename = f"post{idx}_{slug}.html"
        post_path = os.path.join(output_dir, post_filename)
        with open(post_path, 'w', encoding='utf-8') as f:
            f.write(amp_html)

        # 2. Generate Google Flow video spec
        video_spec = generate_google_flow_video_spec(ide)
        video_filename = f"video{idx}_{slug}_google_flow.json"
        video_path = os.path.join(output_dir, video_filename)
        with open(video_path, 'w', encoding='utf-8') as f:
            json.dump(video_spec, f, indent=2)

        covered_ids.add(slug)
        daily_entry.append({"id": slug, "name": ide["name"], "post": post_filename, "video_spec": video_filename})

        summary_lines.append(f"### Package {idx}: {ide['name']}")
        summary_lines.append(f"- **Category:** {ide['category']}")
        summary_lines.append(f"- **Pricing:** {ide['pricing']}")
        summary_lines.append(f"- **AMP Blog Post:** `{post_filename}`")
        summary_lines.append(f"- **Google Flow Spec:** `{video_filename}`")
        summary_lines.append("")

    history["covered_ides"] = list(covered_ids)
    history.setdefault("daily_logs", {})[today_str] = daily_entry

    with open(history_path, 'w', encoding='utf-8') as f:
        json.dump(history, f, indent=2)

    summary_path = os.path.join(output_dir, "summary.md")
    with open(summary_path, 'w', encoding='utf-8') as f:
        f.write("\n".join(summary_lines))

    print(f" Successfully generated 3 daily content packages in {output_dir}")

if __name__ == "__main__":
    main()
