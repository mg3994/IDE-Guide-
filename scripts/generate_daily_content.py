#!/usr/bin/env python3
"""
Daily Content Generator for IDE Guide (https://ideguide.blogspot.com & YouTube @IDEguide).
Generates 3 content packages per day (3 AMP blog posts + 3 Google Flow video specifications).
Tracks covered tools in content/history.json to ensure fresh coverage every day.
"""

import json
import os
import sys
from datetime import datetime, timezone
from typing import Dict, List, Any

IDE_DATABASE: List[Dict[str, Any]] = [
    {
        "name": "Visual Studio Code",
        "category": "General Purpose Code Editor",
        "pricing": "Free (Open Source / Proprietary build)",
        "license_type": "Free",
        "pros": [
            "Massive extension marketplace with thousands of plugins",
            "Built-in Git integration and debugging tools",
            "Lightweight with fast performance and customizable themes",
            "Strong multi-language support out of the box"
        ],
        "cons": [
            "Can become memory-heavy with numerous extensions installed",
            "Not a full out-of-the-box IDE without plugin configuration"
        ],
        "target_audience": "Web, cloud, Python, JavaScript/TypeScript, and multi-language developers.",
        "killer_features": ["Copilot Integration", "Extension Ecosystem", "Integrated Terminal", "Remote SSH / Containers"]
    },
    {
        "name": "Cursor AI",
        "category": "AI-Native Code Editor",
        "pricing": "Freemium ($20/mo Pro plan for advanced model usage)",
        "license_type": "Freemium",
        "pros": [
            "Native deep integration of Claude 3.5 Sonnet & GPT-4o",
            "Full codebase context indexing and multi-file editing",
            "Familiar VS Code keybindings and extension compatibility"
        ],
        "cons": [
            "Requires subscription for unlimited fast AI queries",
            "Relies on cloud servers for AI indexing"
        ],
        "target_audience": "Developers looking for maximum AI-assisted velocity and code generation.",
        "killer_features": ["Cmd+K Inline Edit", "Composer Multi-file Generation", "Codebase Context Chat"]
    },
    {
        "name": "JetBrains IntelliJ IDEA",
        "category": "Full-Featured Enterprise IDE",
        "pricing": "Paid ($169+/year Ultimate) / Free (Community Edition)",
        "license_type": "Freemium / Paid",
        "pros": [
            "Unrivaled refactoring and code analysis engine",
            "Out-of-the-box support for Spring, Kotlin, Java, and Enterprise frameworks",
            "Extremely powerful database and version control tooling"
        ],
        "cons": [
            "High RAM and CPU consumption during project indexing",
            "Paid license required for full web & framework capabilities"
        ],
        "target_audience": "Java, Kotlin, Scala, and enterprise backend engineers.",
        "killer_features": ["Advanced Refactoring", "Smart Code Completion", "Built-in Database Tooling"]
    },
    {
        "name": "Neovim",
        "category": "Hyperextensible Terminal Editor",
        "pricing": "100% Free & Open Source",
        "license_type": "Free",
        "pros": [
            "Blazing fast startup time and minimal resource usage",
            "Lua-based configuration allowing unlimited customization",
            "LSP and Treesitter integration for modern IDE functionality"
        ],
        "cons": [
            "Steep learning curve for keybindings and setup",
            "Requires time investment to configure initial workflow"
        ],
        "target_audience": "Power users, terminal enthusiasts, and low-latency coding fans.",
        "killer_features": ["Vim Keybindings", "Lua Configuration", "Treesitter Syntax Parsing"]
    },
    {
        "name": "Zed Editor",
        "category": "High-Performance Rust-based Editor",
        "pricing": "Free & Open Source",
        "license_type": "Free",
        "pros": [
            "Written in Rust with GPU acceleration for 120 FPS scrolling",
            "Built-in multi-user real-time pair programming",
            "Integrated AI assistant capabilities"
        ],
        "cons": [
            "Smaller plugin ecosystem compared to VS Code",
            "Currently primary focus on macOS & Linux (Windows in progress)"
        ],
        "target_audience": "Developers who prioritize raw performance and real-time collaboration.",
        "killer_features": ["GPU Acceleration", "Real-time Pair Programming", "Rust Engine Speed"]
    },
    {
        "name": "PyCharm",
        "category": "Python IDE",
        "pricing": "Paid ($99+/year Professional) / Free (Community Edition)",
        "license_type": "Freemium / Paid",
        "pros": [
            "Comprehensive Python debugging, profiling, and testing suite",
            "Built-in Django, Flask, and FastAPI web framework support",
            "Scientific stack integration with Jupyter Notebooks"
        ],
        "cons": [
            "Slower startup time on larger codebases",
            "Professional features behind a paid subscription"
        ],
        "target_audience": "Python developers, data scientists, and backend AI engineers.",
        "killer_features": ["Python Debugger", "Jupyter Integration", "Django & FastAPI Framework Tools"]
    },
    {
        "name": "Sublime Text 4",
        "category": "Lightweight Text & Code Editor",
        "pricing": "Paid ($99 one-time evaluation license)",
        "license_type": "Paid",
        "pros": [
            "Instant launch time and ultra-responsive editing",
            "GPU rendering for silky smooth display",
            "Multi-caret editing pioneer"
        ],
        "cons": [
            "Requires paid license popup removal for long-term usage",
            "Requires plugin setups for deep IDE features"
        ],
        "target_audience": "Developers wanting an ultra-fast, lightweight editor with minimal bloat.",
        "killer_features": ["GPU Rendering", "Goto Anything", "Simultaneous Editing"]
    },
    {
        "name": "Fleet by JetBrains",
        "category": "Next-Gen Distributed IDE",
        "pricing": "Freemium / Subscription",
        "license_type": "Freemium",
        "pros": [
            "Lightweight editor mode with smart IDE engine on demand",
            "Remote development and collaborative workspace built-in",
            "Clean, modern minimal interface"
        ],
        "cons": [
            "Still evolving feature set compared to IntelliJ",
            "Ecosystem plugins still building up"
        ],
        "target_audience": "Developers seeking a modern lightweight IDE alternative to VS Code.",
        "killer_features": ["Smart Mode Toggle", "Distributed Architecture", "Collaborative Spaces"]
    },
    {
        "name": "Windsurf Editor (Codeium)",
        "category": "AI Flow Editor",
        "pricing": "Freemium ($15/mo Pro plan)",
        "license_type": "Freemium",
        "pros": [
            "Innovative AI Flows that keep human and AI in sync",
            "Fast code completion powered by Codeium models",
            "Deep multi-file context comprehension"
        ],
        "cons": [
            "Requires subscription for higher tier usage",
            "Newer entry in the AI editor ecosystem"
        ],
        "target_audience": "Full-stack developers seeking agentic AI workflows.",
        "killer_features": ["Cascade AI Flow", "Deep Context Awareness", "Inline Agent Directives"]
    }
]

DISCLAIMER_TEXT = (
    "Disclaimer: IDE Guide is an independent technical publication. "
    "This content is not sponsored, endorsed, or affiliated with any software vendor "
    "or editor developer mentioned above. All reviews and assessments are based strictly "
    "on objective developer evaluation."
)

HISTORY_FILE = "content/history.json"


def load_history() -> List[str]:
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data.get("covered_ide_names", [])
        except Exception:
            return []
    return []


def save_history(covered_names: List[str]) -> None:
    os.makedirs("content", exist_ok=True)
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump({"covered_ide_names": covered_names, "last_updated": datetime.now(timezone.utc).isoformat()}, f, indent=2)


def select_daily_ides(count: int = 3) -> List[Dict[str, Any]]:
    covered = load_history()
    uncovered = [ide for ide in IDE_DATABASE if ide["name"] not in covered]

    if len(uncovered) < count:
        # Reset cycle if pool exhausted
        covered = []
        uncovered = IDE_DATABASE

    selected = uncovered[:count]
    return selected


def generate_amp_blog_post(ide: Dict[str, Any]) -> str:
    pros_html = "".join(f"<li>{p}</li>" for p in ide["pros"])
    cons_html = "".join(f"<li>{c}</li>" for c in ide["cons"])
    features_html = "".join(f"<li><strong>{f}</strong></li>" for f in ide["killer_features"])

    return f"""<!doctype html>
<html amp lang="en">
<head>
  <meta charset="utf-8">
  <title>{ide['name']} Review & Developer Guide - IDE Guide</title>
  <link rel="canonical" href="https://ideguide.blogspot.com/p/{ide['name'].lower().replace(' ', '-')}.html">
  <meta name="viewport" content="width=device-width,minimum-scale=1,initial-scale=1">
  <script async src="https://cdn.ampproject.org/v0.js"></script>
  <style amp-boilerplate>body{{-webkit-animation:-amp-start 8s steps(1,end) 0s 1 normal both;-moz-animation:-amp-start 8s steps(1,end) 0s 1 normal both;-ms-animation:-amp-start 8s steps(1,end) 0s 1 normal both;animation:-amp-start 8s steps(1,end) 0s 1 normal both}}@-webkit-keyframes -amp-start{{from{{visibility:hidden}}to{{visibility:visible}}}}@-moz-keyframes -amp-start{{from{{visibility:hidden}}to{{visibility:visible}}}}@-ms-keyframes -amp-start{{from{{visibility:hidden}}to{{visibility:visible}}}}@-o-keyframes -amp-start{{from{{visibility:hidden}}to{{visibility:visible}}}}@keyframes -amp-start{{from{{visibility:hidden}}to{{visibility:visible}}}}</style><noscript><style amp-boilerplate>body{{-webkit-animation:none;-moz-animation:none;-ms-animation:none;animation:none}}</style></noscript>
  <style amp-custom>
    body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; line-height: 1.6; color: #1a202c; padding: 20px; max-width: 800px; margin: 0 auto; background-color: #f7fafc; }}
    header {{ border-bottom: 2px solid #e2e8f0; padding-bottom: 15px; margin-bottom: 25px; }}
    h1 {{ color: #2d3748; font-size: 2em; margin-bottom: 8px; }}
    .badge {{ display: inline-block; background-color: #3182ce; color: #ffffff; font-size: 0.85em; font-weight: bold; padding: 4px 10px; border-radius: 4px; margin-bottom: 12px; }}
    .pricing-tag {{ display: inline-block; background-color: #38a169; color: #ffffff; font-size: 0.85em; font-weight: bold; padding: 4px 10px; border-radius: 4px; margin-left: 8px; }}
    .section-title {{ font-size: 1.3em; color: #2b6cb0; border-bottom: 1px solid #cbd5e0; padding-bottom: 5px; margin-top: 20px; }}
    ul {{ padding-left: 20px; }}
    li {{ margin-bottom: 8px; }}
    .disclaimer-box {{ background-color: #edf2f7; border-left: 4px solid #4a5568; padding: 12px 16px; margin: 30px 0; font-size: 0.9em; color: #4a5568; border-radius: 0 4px 4px 0; }}
    .comparison-grid {{ display: flex; gap: 20px; }}
    .column {{ flex: 1; }}
    .pro-title {{ color: #2f855a; }}
    .con-title {{ color: #c53030; }}
  </style>
</head>
<body>
  <header>
    <span class="badge">{ide['category']}</span>
    <span class="pricing-tag">{ide['pricing']}</span>
    <h1>{ide['name']} - Complete Review & Setup Guide</h1>
  </header>

  <main>
    <div class="disclaimer-box">
      <p>{DISCLAIMER_TEXT}</p>
    </div>

    <h2 class="section-title">Overview & Value Proposition</h2>
    <p><strong>{ide['name']}</strong> is classified as a <em>{ide['category']}</em>. It serves a primary audience of: {ide['target_audience']}</p>
    <p>Pricing model: <strong>{ide['pricing']}</strong>.</p>

    <h2 class="section-title">Killer Features</h2>
    <ul>
      {features_html}
    </ul>

    <h2 class="section-title">Pros & Cons Breakdown</h2>
    <div class="comparison-grid">
      <div class="column">
        <h3 class="pro-title">The Good (Pros)</h3>
        <ul>
          {pros_html}
        </ul>
      </div>
      <div class="column">
        <h3 class="con-title">The Bad (Cons)</h3>
        <ul>
          {cons_html}
        </ul>
      </div>
    </div>

    <h2 class="section-title">Verdict & Recommendation</h2>
    <p>If you fit the target profile (<em>{ide['target_audience']}</em>), testing out {ide['name']} will significantly optimize your developer velocity. Review the feature set above to decide if its pricing model ({ide['pricing']}) fits your budget.</p>

    <div class="disclaimer-box">
      <p>{DISCLAIMER_TEXT}</p>
    </div>
  </main>
</body>
</html>"""


def generate_google_flow_spec(ide: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "title": f"Is {ide['name']} Worth It? (Honest Developer Review)",
        "channel": "@IDEguide",
        "category": ide["category"],
        "pricing_model": ide["pricing"],
        "disclaimer": DISCLAIMER_TEXT,
        "youtube_shorts_spec": {
            "aspect_ratio": "9:16",
            "duration_seconds": 60,
            "scenes": [
                {
                  "scene_number": 1,
                  "duration_seconds": 10,
                  "visual_prompt": f"Cinematic dark setup showing {ide['name']} launching rapidly with vivid syntax highlighting.",
                  "camera_motion": "Fast push-in towards code window",
                  "lighting": "Dark ambient aesthetic with blue accent neon lighting",
                  "voiceover_script": f"Is {ide['name']} the ultimate code editor for you? Let's break down the truth in 60 seconds."
                },
                {
                  "scene_number": 2,
                  "duration_seconds": 25,
                  "visual_prompt": f"Close-up demonstration of key feature: {ide['killer_features'][0]} in action.",
                  "camera_motion": "Smooth pan across the active editing workspace",
                  "lighting": "High clarity monitor glow with sharp high contrast",
                  "voiceover_script": f"What makes it stand out? Features like {', '.join(ide['killer_features'][:2])} deliver serious productivity gains."
                },
                {
                  "scene_number": 3,
                  "duration_seconds": 15,
                  "visual_prompt": "Split screen comparison showing pros on left green highlights and cons on right red highlights.",
                  "camera_motion": "Static macro camera angle",
                  "lighting": "Balanced studio illumination",
                  "voiceover_script": f"On the downside: {ide['cons'][0]} Pricing is: {ide['pricing']}."
                },
                {
                  "scene_number": 4,
                  "duration_seconds": 10,
                  "visual_prompt": "Closing screen with YouTube channel brand badge @IDEguide and independent disclaimer text.",
                  "camera_motion": "Slow zoom out to full logo setup",
                  "lighting": "Bright cinematic spotlight effect",
                  "voiceover_script": "Subscribe to IDE Guide for unbiased tech breakdowns. Disclaimer: This review is completely independent and not sponsored."
                }
            ]
        },
        "youtube_video_spec": {
            "aspect_ratio": "16:9",
            "duration_seconds": 180,
            "scenes": [
                {
                  "scene_number": 1,
                  "duration_seconds": 30,
                  "visual_prompt": f"Full screen workspace overview of {ide['name']} running a complex developer project.",
                  "camera_motion": "Slow panning across the full 4K workstation monitor",
                  "lighting": "Modern tech studio atmosphere",
                  "voiceover_script": f"Welcome back to IDE Guide. Today we're taking an in-depth look at {ide['name']}, a {ide['category']}."
                },
                {
                  "scene_number": 2,
                  "duration_seconds": 90,
                  "visual_prompt": f"Deep dive recording demonstrating top features: {', '.join(ide['killer_features'])}.",
                  "camera_motion": "Dynamic zooms into code execution terminal and autocomplete menus",
                  "lighting": "Focused workstation lighting",
                  "voiceover_script": f"Let's explore its core features. {ide['pros'][0]} Furthermore, {ide['pros'][1]}."
                },
                {
                  "scene_number": 3,
                  "duration_seconds": 40,
                  "visual_prompt": "Critique segment displaying memory benchmark, pricing charts, and potential bottlenecks.",
                  "camera_motion": "Pan across performance analytics graph",
                  "lighting": "Neutral contrast display",
                  "voiceover_script": f"Now for the trade-offs: {ide['cons'][0]} Regarding costs, {ide['name']} uses a {ide['pricing']} model."
                },
                {
                  "scene_number": 4,
                  "duration_seconds": 20,
                  "visual_prompt": "Final verdict summary slide with non-sponsorship guarantee badge.",
                  "camera_motion": "Smooth center fade",
                  "lighting": "Clean studio lighting",
                  "voiceover_script": f"Verdict: Ideal for {ide['target_audience']} Remember, IDE Guide is fully independent and never sponsored by editor vendors."
                }
            ]
        }
    }


def generate_daily_content_packages(date_str: str = None) -> List[str]:
    if not date_str:
        date_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    target_dir = os.path.join("content", date_str)
    os.makedirs(target_dir, exist_ok=True)

    selected_ides = select_daily_ides(3)
    covered_history = load_history()
    generated_paths = []

    for idx, ide in enumerate(selected_ides, start=1):
        slug = ide["name"].lower().replace(" ", "_").replace("/", "_")

        # 1. Generate AMP Blog Post
        blog_html = generate_amp_blog_post(ide)
        blog_file = os.path.join(target_dir, f"blogpost_{idx}_{slug}.html")
        with open(blog_file, "w", encoding="utf-8") as f:
            f.write(blog_html)
        generated_paths.append(blog_file)

        # 2. Generate Google Flow Spec
        flow_spec = generate_google_flow_spec(ide)
        flow_file = os.path.join(target_dir, f"video_flow_spec_{idx}_{slug}.json")
        with open(flow_file, "w", encoding="utf-8") as f:
            json.dump(flow_spec, f, indent=2)
        generated_paths.append(flow_file)

        if ide["name"] not in covered_history:
            covered_history.append(ide["name"])

    save_history(covered_history)
    print(f"[SUCCESS] Generated 3 daily packages for date: {date_str} in '{target_dir}'")
    return generated_paths


if __name__ == "__main__":
    generate_daily_content_packages()
