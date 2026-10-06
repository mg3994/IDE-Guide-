#!/usr/bin/env python3
"""
Daily Content Generator for IDE Guide.
Generates 3 daily content packages (3 AMP HTML blog posts and 3 Google Flow video specifications)
and records history in content/history.json.
"""

import os
import sys
import json
import datetime
from typing import Dict, List, Any

# Ensure parent directory is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from scripts.amp_validator import validate_amp_html

DISCLAIMER_TEXT = (
    "Disclaimer: IDE Guide is an independent technical publication. "
    "This content is not sponsored, endorsed, or affiliated with any software vendor "
    "or editor developer mentioned above. All reviews and assessments are based strictly "
    "on objective developer evaluation."
)

IDE_DATABASE: List[Dict[str, Any]] = [
    {
        "name": "Visual Studio Code",
        "slug": "vscode",
        "developer": "Microsoft",
        "pricing_type": "Free / Open Source (Core)",
        "price_summary": "100% Free for individual & commercial use.",
        "pros": ["Massive extension ecosystem", "Excellent multi-language support", "Built-in Git integration & terminal", "Active developer community"],
        "cons": ["Electron-based resource usage can be heavy on large monorepos", "Telemetry enabled by default in binary builds"],
        "best_for": "Web, cloud, and general multi-language software development",
        "overview": "Visual Studio Code is a lightweight yet powerful source code editor that runs on desktop and is available for Windows, macOS and Linux.",
        "rating": "4.8/5.0"
    },
    {
        "name": "Neovim",
        "slug": "neovim",
        "developer": "Community Driven",
        "pricing_type": "Free / Open Source (Apache 2.0 / Vim License)",
        "price_summary": "100% Free and open source.",
        "pros": ["Blazing fast performance", "Extensible Lua API", "Built-in LSP client", "Minimalist, keyboard-driven navigation"],
        "cons": ["Steep learning curve for Vim keybindings", "Requires manual configuration setup"],
        "best_for": "Terminal enthusiasts, backend engineers, and developers seeking maximum speed and modal editing efficiency",
        "overview": "Neovim is a refactored, hyper-extensible Vim fork built to maximize usability and extensibility via Lua configuration and async plugin architectures.",
        "rating": "4.9/5.0"
    },
    {
        "name": "IntelliJ IDEA",
        "slug": "intellij-idea",
        "developer": "JetBrains",
        "pricing_type": "Freemium (Free Community / Paid Ultimate)",
        "price_summary": "Community Edition is free. Ultimate Edition starts at $169/year for individuals.",
        "pros": ["Deep code analysis and refactoring", "First-class Java & Kotlin tooling", "Comprehensive database & framework tools in Ultimate"],
        "cons": ["High memory consumption", "Commercial licensing required for advanced frameworks"],
        "best_for": "Enterprise Java, Kotlin, and full-stack backend developers",
        "overview": "IntelliJ IDEA is JetBrains' flagship IDE providing deep contextual understanding and advanced code assistance for JVM ecosystem development.",
        "rating": "4.7/5.0"
    },
    {
        "name": "Cursor",
        "slug": "cursor",
        "developer": "Anysphere",
        "pricing_type": "Freemium (Free / $20/mo Pro)",
        "price_summary": "Free tier with monthly usage limits; $20/month for unlimited fast AI completions.",
        "pros": ["Deep AI codebase index & multi-file editing", "VS Code extension compatibility", "Instant AI code generation and agentic terminal commands"],
        "cons": ["Proprietary AI cloud dependence", "Paid subscription needed for heavy AI workloads"],
        "best_for": "AI-first software developers and fast-paced product engineers",
        "overview": "Cursor is an AI-native fork of VS Code engineered from the ground up for seamless context-aware AI code generation and editing.",
        "rating": "4.8/5.0"
    },
    {
        "name": "PyCharm",
        "slug": "pycharm",
        "developer": "JetBrains",
        "pricing_type": "Freemium (Free Community / Paid Professional)",
        "price_summary": "Community edition is free; Professional edition starts at $99/year for individuals.",
        "pros": ["Best-in-class Python static analysis", "Native Django, Flask & FastAPI support", "Integrated scientific stack and Jupyter notebooks"],
        "cons": ["Slower startup times on older hardware", "Free edition lacks database & web tools"],
        "best_for": "Python developers, data scientists, and backend API engineers",
        "overview": "PyCharm provides dedicated Python development tools, smart refactoring, code inspection, and full-stack web development features.",
        "rating": "4.7/5.0"
    },
    {
        "name": "Zed",
        "slug": "zed",
        "developer": "Zed Industries",
        "pricing_type": "Free / Open Source (GPL / Apache)",
        "price_summary": "100% Free open-source editor with optional cloud collaboration features.",
        "pros": ["Blazing multi-threaded GPU-accelerated rendering in Rust", "Sub-millisecond latency", "Built-in multiplayer pair programming"],
        "cons": ["Ecosystem extensions still maturing", "Fewer plugins compared to VS Code"],
        "best_for": "Developers who prioritize raw performance, instant responsiveness, and modern Rust design",
        "overview": "Zed is a high-performance, multiplayer code editor created by the original authors of Atom and Tree-sitter, engineered in Rust.",
        "rating": "4.6/5.0"
    },
    {
        "name": "Sublime Text",
        "slug": "sublime-text",
        "developer": "Sublime HQ",
        "pricing_type": "Paid / Free Evaluation",
        "price_summary": "Evaluation is free with persistent prompts; individual license is $99 for 3 years of updates.",
        "pros": ["Ultra lightweight and fast", "GPU rendering engine", "Low memory footprint"],
        "cons": ["Lacks out-of-the-box IDE features like debugging without plugins", "License prompt on unactivated builds"],
        "best_for": "Developers needing a super-fast multi-language text editor for quick file edits and script editing",
        "overview": "Sublime Text is a sophisticated text editor for code, markup and prose with custom markup engines and low-level C++ performance.",
        "rating": "4.5/5.0"
    },
    {
        "name": "Windsurf",
        "slug": "windsurf",
        "developer": "Codeium",
        "pricing_type": "Freemium (Free / $15/mo Pro)",
        "price_summary": "Free tier with daily cascade credits; Pro tier at $15/month.",
        "pros": ["Cascade AI flow integration", "Real-time context sync across files", "VS Code extension ecosystem compatibility"],
        "cons": ["Cloud AI dependence for context features"],
        "best_for": "Developers looking for context-aware AI pairing in an intuitive environment",
        "overview": "Windsurf is an AI agentic editor powered by Codeium's Cascade engine, blending collaborative AI flows with standard IDE workflows.",
        "rating": "4.7/5.0"
    },
    {
        "name": "WebStorm",
        "slug": "webstorm",
        "developer": "JetBrains",
        "pricing_type": "Paid ($69/year for individuals)",
        "price_summary": "$69/year for individual developers; free for verified open-source maintainers and students.",
        "pros": ["Unmatched JavaScript, TypeScript, and web framework smarts", "Automated refactoring across components", "Comprehensive test runner and debugger integration"],
        "cons": ["No official free tier", "Can be resource intensive"],
        "best_for": "Frontend and full-stack JavaScript/TypeScript developers working with React, Vue, Angular, or Node.js",
        "overview": "WebStorm is JetBrains' dedicated IDE for JavaScript and related technologies, offering deep code completion and refactoring capabilities.",
        "rating": "4.8/5.0"
    }
]

def generate_amp_blog_html(tool: Dict[str, Any], canonical_url: str) -> str:
    """Generates AMP HTML formatted blog post content for Blogger."""
    pros_html = "".join([f"<li><strong>{p}</strong></li>" for p in tool["pros"]])
    cons_html = "".join([f"<li><strong>{c}</strong></li>" for c in tool["cons"]])

    html = f"""<!doctype html>
<html ⚡ lang="en">
<head>
  <meta charset="utf-8">
  <script async src="https://cdn.ampproject.org/v0.js"></script>
  <title>{tool['name']} Review & Developer Guide - IDE Guide</title>
  <link rel="canonical" href="{canonical_url}">
  <meta name="viewport" content="width=device-width,minimum-scale=1,initial-scale=1">
  <style amp-boilerplate>body{{-webkit-animation:-amp-start 8s steps(1,end) 0s 1 normal both;-moz-animation:-amp-start 8s steps(1,end) 0s 1 normal both;-ms-animation:-amp-start 8s steps(1,end) 0s 1 normal both;animation:-amp-start 8s steps(1,end) 0s 1 normal both}}</style><noscript><style amp-boilerplate>body{{-webkit-animation:none;-moz-animation:none;-ms-animation:none;animation:none}}</style></noscript>
  <style amp-custom>
    body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; line-height: 1.6; color: #1a1a1a; padding: 16px; max-width: 800px; margin: 0 auto; background-color: #fafafa; }}
    header {{ background: #0f172a; color: #ffffff; padding: 24px; border-radius: 8px; margin-bottom: 24px; }}
    h1 {{ font-size: 1.8rem; margin: 0 0 8px 0; color: #38bdf8; }}
    .badge {{ display: inline-block; background: #0284c7; color: #fff; padding: 4px 8px; font-size: 0.85rem; border-radius: 4px; font-weight: bold; margin-bottom: 12px; }}
    .meta-box {{ background: #ffffff; border: 1px solid #e2e8f0; border-radius: 8px; padding: 16px; margin-bottom: 20px; }}
    .pros-cons {{ display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin: 20px 0; }}
    @media (max-width: 600px) {{ .pros-cons {{ grid-template-columns: 1fr; }} }}
    .pros {{ background: #f0fdf4; border-left: 4px solid #22c55e; padding: 12px 16px; border-radius: 4px; }}
    .cons {{ background: #fef2f2; border-left: 4px solid #ef4444; padding: 12px 16px; border-radius: 4px; }}
    .disclaimer {{ background: #f1f5f9; border: 1px solid #cbd5e1; font-size: 0.85rem; color: #475569; padding: 12px; border-radius: 6px; margin-top: 30px; line-height: 1.4; }}
    ul {{ padding-left: 20px; margin: 8px 0; }}
  </style>
</head>
<body>
  <header>
    <span class="badge">{tool['pricing_type']}</span>
    <h1>{tool['name']} Developer Assessment & Feature Guide</h1>
    <p>Published by IDE Guide | Developer Rating: {tool['rating']}</p>
  </header>

  <section class="meta-box">
    <h2>Overview</h2>
    <p>{tool['overview']}</p>
    <p><strong>Developer / Maintainer:</strong> {tool['developer']}</p>
    <p><strong>Pricing Summary:</strong> {tool['price_summary']}</p>
  </section>

  <section>
    <h2>Good & Bad Analysis</h2>
    <div class="pros-cons">
      <div class="pros">
        <h3>The Good (Pros)</h3>
        <ul>{pros_html}</ul>
      </div>
      <div class="cons">
        <h3>The Bad (Cons)</h3>
        <ul>{cons_html}</ul>
      </div>
    </div>
  </section>

  <section class="meta-box">
    <h2>Verdict & Best Use Cases</h2>
    <p><strong>Who should use {tool['name']}?</strong></p>
    <p>{tool['best_for']}</p>
  </section>

  <footer class="disclaimer">
    <p>{DISCLAIMER_TEXT}</p>
  </footer>
</body>
</html>"""
    return html


def generate_google_flow_video_spec(tool: Dict[str, Any]) -> Dict[str, Any]:
    """Generates Google Flow AI video creation specification JSON."""
    return {
        "channel": "@IDEguide",
        "tool_name": tool["name"],
        "pricing_category": tool["pricing_type"],
        "target_aspect_ratio": "16:9 Widescreen (YouTube Main) & 9:16 Vertical (Shorts)",
        "visual_prompt_specifications": {
            "framing": "Cinematic close-up of developer workstation, active dark theme interface, responsive syntax highlighting",
            "lighting": "Cool studio ambient light (6000K) with subtle neon accent rim lights reflecting on keycaps",
            "camera_motion": "Smooth push-in shot toward terminal output, followed by dynamic slow pan across code completions",
            "color_palette": "Deep dark navy blue, cyan highlights, green code success accents"
        },
        "narration_script": [
            {
                "scene": 1,
                "duration_sec": 5,
                "visual_prompt": f"Ultra close up shot of {tool['name']} dark mode UI launching with high contrast syntax theme",
                "text_overlay": f"{tool['name']} - Ultimate Overview",
                "voiceover": f"Looking for your next code editor? Today we analyze {tool['name']} by {tool['developer']}."
            },
            {
                "scene": 2,
                "duration_sec": 8,
                "visual_prompt": "Dynamic split screen highlighting top performance metrics and key features",
                "text_overlay": f"Pricing: {tool['pricing_type']}",
                "voiceover": f"Pricing model: {tool['price_summary']}"
            },
            {
                "scene": 3,
                "duration_sec": 12,
                "visual_prompt": "Side-by-side graphical checklist highlighting key strengths vs limitations",
                "text_overlay": "Pros & Cons Breakdown",
                "voiceover": f"Key advantages include {tool['pros'][0]} and {tool['pros'][1]}. However, keep in mind {tool['cons'][0]}."
            },
            {
                "scene": 4,
                "duration_sec": 7,
                "visual_prompt": "Futuristic overlay showing target developer profile and final rating badge",
                "text_overlay": f"Rating: {tool['rating']} | Best For: Developer Workflows",
                "voiceover": f"Ideal choice if you are: {tool['best_for']}."
            }
        ],
        "non_sponsorship_disclaimer": DISCLAIMER_TEXT
    }


def load_history(history_path: str) -> Dict[str, Any]:
    if os.path.exists(history_path):
        try:
            with open(history_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {"covered_tools": [], "last_updated": None}


def save_history(history_path: str, history: Dict[str, Any]) -> None:
    os.makedirs(os.path.dirname(history_path), exist_ok=True)
    with open(history_path, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=2)


def generate_daily_content_packages(date_str: str = None, output_base_dir: str = "content", history_file: str = "content/history.json"):
    if not date_str:
        date_str = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d")

    history = load_history(history_file)
    covered_slugs = set(history.get("covered_tools", []))

    # Pick 3 tools that haven't been covered, or reset if all tools covered
    available_tools = [t for t in IDE_DATABASE if t["slug"] not in covered_slugs]
    if len(available_tools) < 3:
        covered_slugs = set()
        available_tools = IDE_DATABASE

    selected_tools = available_tools[:3]

    day_dir = os.path.join(output_base_dir, date_str)
    os.makedirs(day_dir, exist_ok=True)

    generated_files = []

    for tool in selected_tools:
        slug = tool["slug"]
        canonical_url = f"https://ideguide.blogspot.com/{date_str[:4]}/{date_str[5:7]}/{slug}-review.html"

        # Generate Blog Post
        blog_html = generate_amp_blog_html(tool, canonical_url)
        blog_file = os.path.join(day_dir, f"{slug}_blogpost.html")
        with open(blog_file, "w", encoding="utf-8") as f:
            f.write(blog_html)

        # Validate AMP compliance
        is_valid, errors = validate_amp_html(blog_html)
        if not is_valid:
            raise ValueError(f"Generated blog HTML for {slug} failed AMP validation: {errors}")

        generated_files.append(blog_file)

        # Generate Google Flow Video Spec
        video_spec = generate_google_flow_video_spec(tool)
        video_file = os.path.join(day_dir, f"{slug}_flow_spec.json")
        with open(video_file, "w", encoding="utf-8") as f:
            json.dump(video_spec, f, indent=2)

        generated_files.append(video_file)

        # Track in history
        if slug not in history.get("covered_tools", []):
            history.setdefault("covered_tools", []).append(slug)

    history["last_updated"] = datetime.datetime.now(datetime.timezone.utc).isoformat()
    save_history(history_file, history)

    print(f"Successfully generated 3 daily content packages in {day_dir}:")
    for filepath in generated_files:
        print(f" - {filepath}")

    return generated_files


if __name__ == "__main__":
    generate_daily_content_packages()
