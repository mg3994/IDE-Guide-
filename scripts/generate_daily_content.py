#!/usr/bin/env python3
"""
Daily Content Generator for IDE Guide
Generates 3 daily AMP HTML blog posts for Blogger and 3 Google Flow video/shorts specifications.
Maintains history in content/history.json to ensure new IDEs are covered each day.
"""

import os
import json
import datetime
from typing import Dict, Any, List, Tuple

DISCLAIMER = (
    "Disclaimer: IDE Guide is an independent technical publication. "
    "This content is not sponsored, endorsed, or affiliated with any software vendor or editor developer mentioned above. "
    "All reviews and assessments are based strictly on objective developer evaluation."
)

IDE_POOL: List[Dict[str, Any]] = [
    {
        "id": "vscode",
        "name": "Visual Studio Code",
        "category": "General Purpose / Extensible Editor",
        "pricing": "Free (Open Source / MIT Core)",
        "paid_tier": "Free / Optional Paid AI Plugins",
        "pros": [
            "Massive extension marketplace with thousands of extensions",
            "Extremely fast startup and responsive typing latency",
            "Native Git integration and multi-language support out of the box",
            "Robust remote development capabilities (SSH, Containers, WSL)"
        ],
        "cons": [
            "High RAM consumption with heavily stacked plugins",
            "Requires configuration tuning for complex project setups"
        ],
        "verdict": "The best overall free editor for web, cloud, and multi-language developers.",
        "target_audience": "Web Developers, Full-Stack Engineers, DevOps & Scripting"
    },
    {
        "id": "cursor",
        "name": "Cursor AI Editor",
        "category": "AI-Native IDE",
        "pricing": "Freemium ($20/mo Pro tier)",
        "paid_tier": "Paid ($20/month for unlimited fast Claude 3.5 Sonnet & GPT-4o queries)",
        "pros": [
            "Seamless AI code generation and deep repo-wide context indexing",
            "Forked directly from VS Code, compatible with all VS Code extensions",
            "Multi-file automated inline editing (Cmd+K / Cmd+I)"
        ],
        "cons": [
            "Subscription cost for unlimited high-speed AI queries",
            "Requires active cloud connection for full AI agent capabilities"
        ],
        "verdict": "The premiere choice for developers seeking deep AI-driven agentic pair programming.",
        "target_audience": "AI-Focused Engineers, Web Developers, Rapid Prototypers"
    },
    {
        "id": "neovim",
        "name": "Neovim",
        "category": "Terminal Modal Editor",
        "pricing": "Free (Open Source / Apache 2.0)",
        "paid_tier": "100% Free and Open Source",
        "pros": [
            "Ultra-lightweight with near-zero memory footprint (<30MB RAM)",
            "Unrivaled keyboard navigation speed and customizable Lua ecosystem",
            "Built-in LSP (Language Server Protocol) and Tree-sitter AST syntax"
        ],
        "cons": [
            "Steep learning curve for non-modal editor users",
            "Significant initial effort required for custom Lua configuration"
        ],
        "verdict": "The absolute best choice for terminal purists and keyboard-driven efficiency power users.",
        "target_audience": "Systems Programmers, Linux/Unix Power Users, Terminal Enthusiasts"
    },
    {
        "id": "intellij_idea",
        "name": "IntelliJ IDEA",
        "category": "JVM & Enterprise IDE",
        "pricing": "Freemium (Community Free / Ultimate $169+/yr)",
        "paid_tier": "Paid Ultimate Edition for Full Enterprise & Framework Support",
        "pros": [
            "Industry-leading Java, Kotlin, and Spring framework code intelligence",
            "Incredible automated refactoring and static analysis engines",
            "Deep database management, HTTP client, and enterprise tooling integration"
        ],
        "cons": [
            "Heavy memory footprint (requires 8GB+ RAM allocation)",
            "Ultimate features locked behind commercial annual license"
        ],
        "verdict": "Unmatched industry standard for Java, Kotlin, and enterprise backend engineering.",
        "target_audience": "Java/Kotlin Backend Developers, Enterprise System Architects"
    },
    {
        "id": "pycharm",
        "name": "PyCharm",
        "category": "Python & Data Science IDE",
        "pricing": "Freemium (Community Free / Professional $99+/yr)",
        "paid_tier": "Paid Professional Edition for Web Frameworks & Scientific Tools",
        "pros": [
            "Deep Python virtual environment, Conda, and Docker debugging",
            "Built-in Jupyter Notebook support and database browser",
            "First-class Django, Flask, and FastAPI web integration"
        ],
        "cons": [
            "Can be resource intensive on large monorepos",
            "Community edition lacks web framework tools"
        ],
        "verdict": "The definitive specialized IDE for serious Python developers and data scientists.",
        "target_audience": "Python Developers, Data Scientists, AI/ML Engineers"
    },
    {
        "id": "zed",
        "name": "Zed Editor",
        "category": "High-Performance GPU-Accelerated Editor",
        "pricing": "Free (Open Source Core)",
        "paid_tier": "Free Core / Optional Cloud Team Features",
        "pros": [
            "Blazing fast performance written in Rust with GPU rendering",
            "Built-in real-time collaborative editing (multiplayer)",
            "Integrated AI coding assistant features and low latency"
        ],
        "cons": [
            "Extension ecosystem is still growing compared to VS Code",
            "Currently limited advanced debugging tools for specialized languages"
        ],
        "verdict": "The fastest modern GUI text editor available, perfect for lightweight high-speed coding.",
        "target_audience": "Performance Enthusiasts, Rust/Go Devs, Real-Time Collaborators"
    },
    {
        "id": "windsurf",
        "name": "Windsurf Editor",
        "category": "Agentic AI Flow IDE",
        "pricing": "Freemium ($15/mo Pro tier)",
        "paid_tier": "Paid Pro subscription for unlimited Cascade Agent flows",
        "pros": [
            "Innovative Cascade Flow for real-time human-AI collaborative coding",
            "Deep context awareness across terminals, diffs, and codebase structure",
            "VS Code extension ecosystem compatibility"
        ],
        "cons": [
            "Requires subscription for high-volume agentic cascade calls",
            "Newer ecosystem with rapidly evolving features"
        ],
        "verdict": "An exceptional AI-native editor for developers looking for continuous agentic execution.",
        "target_audience": "Full-Stack Devs, AI Developers, Rapid Product Builders"
    },
    {
        "id": "webstorm",
        "name": "WebStorm",
        "category": "JavaScript & Web Development IDE",
        "pricing": "Paid ($69+/yr or Subscription)",
        "paid_tier": "Commercial Paid License (Free for non-commercial/students)",
        "pros": [
            "Unrivaled JavaScript, TypeScript, React, and Vue language intelligence",
            "Out-of-the-box refactoring and debugging without plugin hassle",
            "Seamless integration with testing frameworks (Jest, Vitest, Cypress)"
        ],
        "cons": [
            "Proprietary license required for commercial enterprise use",
            "Slightly heavier startup time than lightweight text editors"
        ],
        "verdict": "The top choice for professional frontend and Node.js full-stack developers.",
        "target_audience": "Frontend Engineers, Node.js Developers, TypeScript Specialists"
    },
    {
        "id": "xcode",
        "name": "Xcode",
        "category": "Apple Platform IDE",
        "pricing": "Free (Mac App Store)",
        "paid_tier": "100% Free (Requires Apple Developer Account for App Store publishing)",
        "pros": [
            "Essential all-in-one suite for iOS, macOS, watchOS, and visionOS apps",
            "Interactive SwiftUI Previews and visual layout design",
            "Built-in simulator, performance instruments, and metal debugging"
        ],
        "cons": [
            "Exclusive to macOS hardware",
            "Large download size and occasional slow build indexing"
        ],
        "verdict": "Mandatory and comprehensive IDE for building Apple ecosystem applications.",
        "target_audience": "iOS Developers, macOS Engineers, SwiftUI Builders"
    }
]

def load_history(history_file: str) -> List[str]:
    if os.path.exists(history_file):
        try:
            with open(history_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get("covered_ides", [])
        except Exception:
            return []
    return []

def save_history(history_file: str, covered_ides: List[str]) -> None:
    os.makedirs(os.path.dirname(history_file), exist_ok=True)
    with open(history_file, 'w', encoding='utf-8') as f:
        json.dump({"covered_ides": covered_ides}, f, indent=2)

def select_daily_ides(history_file: str, count: int = 3) -> Tuple[List[Dict[str, Any]], List[str]]:
    covered = load_history(history_file)
    available = [ide for ide in IDE_POOL if ide["id"] not in covered]

    # If pool exhausted or fewer than required, reset cycle
    if len(available) < count:
        covered = []
        available = IDE_POOL[:]

    selected = available[:count]
    updated_covered = list(set(covered + [ide["id"] for ide in selected]))
    return selected, updated_covered

def generate_amp_blog_post(ide: Dict[str, Any], date_str: str, index: int) -> str:
    pros_html = "".join([f"<li><strong>{p}</strong></li>" for p in ide["pros"]])
    cons_html = "".join([f"<li><strong>{c}</strong></li>" for c in ide["cons"]])

    amp_html = f"""<!doctype html>
<html amp lang="en">
<head>
  <meta charset="utf-8">
  <title>{ide['name']} Review ({date_str}): Good, Bad, and Pricing Breakdown | IDE Guide</title>
  <link rel="canonical" href="https://ideguide.blogspot.com/{date_str.replace('-', '/')}/{ide['id']}-review.html">
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
    <h1>{ide['name']}: Developer Evaluation & Review</h1>

    <div class="meta-box">
      <p><strong>Target Audience:</strong> {ide['target_audience']}</p>
      <p><strong>Pricing & Licensing:</strong> {ide['pricing']} ({ide['paid_tier']})</p>
    </div>

    <h2>Overview</h2>
    <p>Welcome to IDE Guide's objective developer evaluation for <strong>{ide['name']}</strong>. Choosing the right code editor determines daily developer productivity, workflow speed, and system resource management.</p>

    <amp-img src="https://via.placeholder.com/800x400/1e293b/ffffff?text={ide['name'].replace(' ', '+')}+IDE+Guide" width="800" height="400" layout="responsive" alt="{ide['name']} Overview"></amp-img>

    <div class="pros">
      <h2>The Good (Strengths & Key Pros)</h2>
      <ul>
        {pros_html}
      </ul>
    </div>

    <div class="cons">
      <h2>The Bad (Cons & Drawbacks)</h2>
      <ul>
        {cons_html}
      </ul>
    </div>

    <h2>Final Verdict: Which Developers Should Pick This?</h2>
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

def generate_google_flow_spec(ide: Dict[str, Any], date_str: str, index: int) -> Dict[str, Any]:
    is_short = (index % 2 != 0)
    format_type = "Short (9:16 Vertical)" if is_short else "Video (16:9 Horizontal)"
    aspect_ratio = "9:16" if is_short else "16:9"
    duration = "60 Seconds" if is_short else "3-5 Minutes"

    flow_spec = {
        "metadata": {
            "channel": "@IDEguide",
            "youtube_url": "https://www.youtube.com/@IDEguide",
            "ide_name": ide["name"],
            "date": date_str,
            "format": format_type,
            "aspect_ratio": aspect_ratio,
            "target_duration": duration,
            "title": f"The Truth About {ide['name']} in 2026! (Pros, Cons & Pricing)"
        },
        "visual_and_camera_specifications": {
            "framing": f"Cyberpunk Tech Studio, Vertical/Horizontal {aspect_ratio}",
            "lighting": "Deep indigo studio background with vibrant emerald green and electric blue rim lights",
            "camera_angles": [
                {"scene": 1, "angle": "Dynamic Zoom-in on IDE startup screen and main logo", "duration": "0-10s"},
                {"scene": 2, "angle": "Split-screen split view showing memory/RAM graph vs coding speed", "duration": "10-30s"},
                {"scene": 3, "angle": "Macro close-up on code auto-complete and extension panel", "duration": "30-50s"},
                {"scene": 4, "angle": "Wide camera shot with graphical overlay summary box", "duration": "50-60s"}
            ],
            "graphics_and_cues": "Holographic text overlays showing 'FREE vs PAID', top pros tick list, and final score banner."
        },
        "voiceover_script": {
            "hook": f"Stop choosing the wrong editor in 2026! Here is the honest developer verdict on {ide['name']}.",
            "pricing_segment": f"Pricing breakdown: {ide['pricing']}. {ide['paid_tier']}.",
            "pros_segment": f"Why developers love it: {', '.join(ide['pros'])}.",
            "cons_segment": f"What you need to watch out for: {', '.join(ide['cons'])}.",
            "recommendation_callout": f"Final Recommendation: {ide['verdict']}"
        },
        "audio_directions": {
            "background_music": "Energetic upbeat tech synthwave beat (BPM: 120)",
            "sfx": "Subtle digital click SFX on text overlays and transition sweeps"
        },
        "disclaimer_overlay": {
            "text": DISCLAIMER,
            "visual_position": "Bottom overlay text banner throughout ending sequence"
        }
    }
    return flow_spec

def main():
    date_str = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d")
    output_dir = os.path.join("content", date_str)
    os.makedirs(output_dir, exist_ok=True)

    history_file = os.path.join("content", "history.json")
    selected_ides, updated_covered = select_daily_ides(history_file, count=3)

    print(f"Generating content for {date_str} in {output_dir}:")

    for i, ide in enumerate(selected_ides, 1):
        # 1. Generate AMP HTML blog post
        amp_html = generate_amp_blog_post(ide, date_str, i)
        html_filename = f"post_{i}_{ide['id']}.html"
        html_path = os.path.join(output_dir, html_filename)
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(amp_html)
        print(f"  [+] Blog Post (AMP): {html_path}")

        # 2. Generate Google Flow video spec
        flow_spec = generate_google_flow_spec(ide, date_str, i)
        json_filename = f"flow_spec_{i}_{ide['id']}.json"
        json_path = os.path.join(output_dir, json_filename)
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(flow_spec, f, indent=2)
        print(f"  [+] Google Flow Spec: {json_path}")

    save_history(history_file, updated_covered)
    print("Daily content generation complete!")

if __name__ == "__main__":
    main()
