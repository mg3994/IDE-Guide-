#!/usr/bin/env python3
"""
Daily Content Generator for IDE Guide
Generates 3 AMP HTML blog posts for Blogger (ideguide.blogspot.com)
and 3 Google Flow Video Specifications / Scripts for YouTube (@IDEguide).
Outputs into content/YYYY-MM-DD/ and updates content/history.json.
"""

import json
import os
import sys
from datetime import datetime, timezone
from typing import Dict, Any, List

# Standard Non-Sponsorship Disclaimer
DISCLAIMER_TEXT = (
    "Disclaimer: IDE Guide is an independent technical publication. "
    "This content is not sponsored, endorsed, or affiliated with any software vendor or editor developer mentioned above. "
    "All reviews and assessments are based strictly on objective developer evaluation."
)

# Comprehensive IDE & Code Editor Database
IDE_DATABASE: List[Dict[str, Any]] = [
    {
        "id": "vscode",
        "name": "Visual Studio Code (VS Code)",
        "developer": "Microsoft",
        "category": "General Code Editor",
        "pricing": "Free & Open Source (Core) / Freemium Extensions",
        "pros": [
            "Massive ecosystem of extensions and themes",
            "Built-in Git integration and terminal",
            "Excellent TypeScript/JavaScript support out of the box",
            "Highly customizable workspace settings and keybindings"
        ],
        "cons": [
            "Can become memory-heavy with numerous active extensions",
            "Electron-based framework uses more RAM than native editors",
            "Requires initial configuration for complex C++/Rust build setups"
        ],
        "target_audience": "Web developers, full-stack engineers, Python automation engineers, and beginners.",
        "best_for": "Versatile multi-language web and backend development.",
        "image_url": "https://images.unsplash.com/photo-1555066931-4365d14bab8c?w=800&auto=format&fit=crop"
    },
    {
        "id": "cursor",
        "name": "Cursor AI",
        "developer": "Anysphere",
        "category": "AI-Native IDE",
        "pricing": "Freemium ($20/mo for Pro plan)",
        "pros": [
            "Deep multi-file AI codebase indexing and context understanding",
            "Seamless VS Code extension compatibility and setting import",
            "Instant AI diff predictions and inline editing (`Cmd+K`)",
            "Supports advanced models like Claude 3.5 Sonnet and GPT-4o"
        ],
        "cons": [
            "Paid tier required for heavy daily AI usage",
            "Requires internet connectivity for cloud AI features",
            "Occasional context hallucination on custom internal frameworks"
        ],
        "target_audience": "AI-first developers, full-stack engineers, and rapid prototypers.",
        "best_for": "AI-assisted coding, complex refactoring, and rapid feature development.",
        "image_url": "https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?w=800&auto=format&fit=crop"
    },
    {
        "id": "intellij",
        "name": "JetBrains IntelliJ IDEA",
        "developer": "JetBrains",
        "category": "Enterprise Java & Polyglot IDE",
        "pricing": "Free Community Edition / $169-$599/yr Ultimate Edition",
        "pros": [
            "Industry-best Java/Kotlin code analysis and refactoring engines",
            "Comprehensive database tooling, Spring framework support, and debugger",
            "Robust built-in version control and merge conflict resolution",
            "Out-of-the-box support for Maven, Gradle, and Enterprise frameworks"
        ],
        "cons": [
            "High memory footprint; requires 8GB+ RAM for smooth performance",
            "Initial project indexing can be slow on large codebases",
            "Ultimate features locked behind commercial subscription"
        ],
        "target_audience": "Enterprise Java/Kotlin engineers, backend developers, and Spring Boot specialists.",
        "best_for": "Large-scale JVM backend systems and enterprise software architecture.",
        "image_url": "https://images.unsplash.com/photo-1517694712202-14dd9538aa97?w=800&auto=format&fit=crop"
    },
    {
        "id": "pycharm",
        "name": "JetBrains PyCharm",
        "developer": "JetBrains",
        "category": "Python IDE",
        "pricing": "Free Community Edition / $99-$249/yr Professional Edition",
        "pros": [
            "Unrivaled Python code introspection, auto-imports, and static checks",
            "Built-in Jupyter notebook, Django, Flask, and FastAPI integration",
            "Advanced visual debugger and remote SSH / Docker interpreter support",
            "Scientific stack integration with NumPy, Pandas, and Matplotlib viewers"
        ],
        "cons": [
            "Slower launch time compared to lightweight code editors",
            "Professional features (Web & SQL tools) require paid license"
        ],
        "target_audience": "Python developers, Data Scientists, ML engineers, and Django backend developers.",
        "best_for": "Data science pipelines, AI development, and complex Python web apps.",
        "image_url": "https://images.unsplash.com/photo-1526379095098-d400fd0bf935?w=800&auto=format&fit=crop"
    },
    {
        "id": "zed",
        "name": "Zed Editor",
        "developer": "Zed Industries",
        "category": "High-Performance Native Code Editor",
        "pricing": "Free & Open Source",
        "pros": [
            "Written in Rust with GPU acceleration for sub-millisecond response times",
            "Multi-player real-time collaborative editing built directly into core",
            "Extremely low CPU and memory resource consumption",
            "Native tree-sitter syntax highlighting and LSP support"
        ],
        "cons": [
            "Ecosystem of plugins is still growing compared to VS Code",
            "Currently best optimized on macOS / Linux, Windows support in active development"
        ],
        "target_audience": "Performance enthusiasts, Rust/C++ developers, and remote collaborative teams.",
        "best_for": "Ultra-fast text editing, low latency coding, and live collaborative pair programming.",
        "image_url": "https://images.unsplash.com/photo-1542831371-29b0f74f9713?w=800&auto=format&fit=crop"
    },
    {
        "id": "neovim",
        "name": "Neovim",
        "developer": "Open Source Community",
        "category": "Terminal-based Modal Editor",
        "pricing": "Free & Open Source (100%)",
        "pros": [
            "Zero GUI overhead, lightning fast startup and modal keyboard workflow",
            "Extensible using modern Lua script configuration",
            "Built-in Language Server Protocol (LSP) and Treesitter support",
            "Runs seamlessly over SSH and terminal environments"
        ],
        "cons": [
            "Steep learning curve for modal navigation and Vim keybindings",
            "Requires time and effort to build a custom IDE-like setup"
        ],
        "target_audience": "Terminal power users, DevOps engineers, Systems programmers, and Vim enthusiasts.",
        "best_for": "Keyboard-driven development, server remote editing, and tailored developer setups.",
        "image_url": "https://images.unsplash.com/photo-1629654297299-c8506221ca97?w=800&auto=format&fit=crop"
    },
    {
        "id": "sublimetext",
        "name": "Sublime Text 4",
        "developer": "Sublime HQ",
        "category": "Lightweight Code Editor",
        "pricing": "Evaluation Free / $99 per user single purchase",
        "pros": [
            "Instant load speed and super crisp rendering",
            "Multiple selections and powerful Goto Anything navigation",
            "GPU rendering hardware acceleration for high-refresh monitors",
            "Extensive Package Control system"
        ],
        "cons": [
            "Periodic payment prompt popup in evaluation mode",
            "Integrated debugging setup requires extra plugin configuration"
        ],
        "target_audience": "Developers who prioritize raw editor speed, minimal UI distraction, and quick text editing.",
        "best_for": "Quick script edits, massive text file manipulation, and fast lightweight coding.",
        "image_url": "https://images.unsplash.com/photo-1507238691740-187a5b1d37b8?w=800&auto=format&fit=crop"
    },
    {
        "id": "fleet",
        "name": "JetBrains Fleet",
        "developer": "JetBrains",
        "category": "Distributed Polyglot Editor",
        "pricing": "Free Preview / Freemium",
        "pros": [
            "Lightweight smart text editor that can switch to full IDE engine on demand",
            "Distributed architecture allowing remote machine execution and cloud spaces",
            "Clean visual interface with fast modern startup",
            "Built-in Kotlin, Rust, Python, and JS smart features"
        ],
        "cons": [
            "Ecosystem still evolving as a newer product",
            "Some specialized plugin capabilities from IntelliJ are still being migrated"
        ],
        "target_audience": "Polyglot developers seeking a lightweight alternative to full IntelliJ heavy IDEs.",
        "best_for": "Remote cloud workspace development and quick multi-language projects.",
        "image_url": "https://images.unsplash.com/photo-1461749280684-dccba630e2f6?w=800&auto=format&fit=crop"
    },
    {
        "id": "xcode",
        "name": "Apple Xcode",
        "developer": "Apple",
        "category": "Apple Platform IDE",
        "pricing": "Free for macOS users",
        "pros": [
            "Official IDE for iOS, macOS, watchOS, and visionOS development",
            "SwiftUI interactive canvas preview and visual layout editor",
            "Comprehensive Instruments profiling and memory debugging tools",
            "Direct App Store submission and simulator integration"
        ],
        "cons": [
            "Restricted exclusively to macOS operating system",
            "Large download footprint (>12GB) and frequent large updates"
        ],
        "target_audience": "iOS, macOS, iPadOS, watchOS, and visionOS native app developers.",
        "best_for": "Native Apple platform application development and Swift programming.",
        "image_url": "https://images.unsplash.com/photo-1512941937669-90a1b58e7e9c?w=800&auto=format&fit=crop"
    },
    {
        "id": "androidstudio",
        "name": "Android Studio",
        "developer": "Google / JetBrains",
        "category": "Mobile App IDE",
        "pricing": "Free & Open Source",
        "pros": [
            "Official IDE for Android app creation with Jetpack Compose preview",
            "Advanced Android device emulator with multi-screen support",
            "APK analyzer, battery impact monitor, and memory profiler",
            "Full Kotlin and Java first-class support"
        ],
        "cons": [
            "High RAM and CPU resource consumption when running emulator",
            "Build times with Gradle can be slow on older hardware"
        ],
        "target_audience": "Android mobile application developers and Kotlin specialists.",
        "best_for": "Building native Android smartphones, TV, and wear OS applications.",
        "image_url": "https://images.unsplash.com/photo-1607252650355-f7fd0460ccdb?w=800&auto=format&fit=crop"
    },
    {
        "id": "webstorm",
        "name": "JetBrains WebStorm",
        "developer": "JetBrains",
        "category": "JavaScript & Web IDE",
        "pricing": "Free for non-commercial/students / $69/yr Commercial",
        "pros": [
            "Best-in-class JavaScript, TypeScript, React, Vue, and Angular intelligence",
            "Smart refactoring across components, imports, and styling files",
            "Built-in HTTP client, linter integration, and test runners",
            "Now free for non-commercial personal open-source usage"
        ],
        "cons": [
            "Heavier resource usage than plain VS Code",
            "Commercial corporate license required for business employment"
        ],
        "target_audience": "Frontend engineers, React/Vue/Angular framework developers, and Node.js backend developers.",
        "best_for": "Modern frontend single-page web app development and TypeScript projects.",
        "image_url": "https://images.unsplash.com/photo-1581291518857-4e27b48ff24e?w=800&auto=format&fit=crop"
    },
    {
        "id": "windsurf",
        "name": "Windsurf Editor",
        "developer": "Codeium",
        "category": "AI Flow-based IDE",
        "pricing": "Freemium ($15/mo Pro)",
        "pros": [
            "Cascade AI flow engine that blends developer actions with AI execution",
            "Deep contextual awareness of entire repository structure",
            "Fast inline suggestions and real-time terminal command generation",
            "Generous free tier provided by Codeium infrastructure"
        ],
        "cons": [
            "Newer platform with continuous feature updates",
            "Requires active network connection for deep AI Cascade capabilities"
        ],
        "target_audience": "Developers looking for a deeply integrated agentic AI coding environment.",
        "best_for": "Agentic AI-driven web and backend app construction.",
        "image_url": "https://images.unsplash.com/photo-1550751827-4bd374c3f58b?w=800&auto=format&fit=crop"
    }
]


def load_history(history_path: str) -> List[str]:
    if os.path.exists(history_path):
        try:
            with open(history_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data.get("covered_ide_ids", [])
        except Exception:
            return []
    return []


def save_history(history_path: str, history_ids: List[str]):
    os.makedirs(os.path.dirname(history_path), exist_ok=True)
    with open(history_path, "w", encoding="utf-8") as f:
        json.dump({"covered_ide_ids": history_ids, "last_updated": datetime.now(timezone.utc).isoformat()}, f, indent=2)


def select_daily_ides(count: int = 3, history_path: str = "content/history.json") -> List[Dict[str, Any]]:
    history = load_history(history_path)
    # Filter out recent IDEs if possible
    available = [ide for ide in IDE_DATABASE if ide["id"] not in history]
    if len(available) < count:
        # Reset history if we cycled through all IDEs
        history = []
        available = IDE_DATABASE

    selected = available[:count]
    new_history = history + [ide["id"] for ide in selected]
    save_history(history_path, new_history)
    return selected


def generate_amp_blog_post(ide: Dict[str, Any], date_str: str) -> str:
    pros_html = "".join([f"<li><strong>{p.split(' ')[0]}</strong> {' '.join(p.split(' ')[1:])}</li>" for p in ide["pros"]])
    cons_html = "".join([f"<li><strong>{c.split(' ')[0]}</strong> {' '.join(c.split(' ')[1:])}</li>" for c in ide["cons"]])

    canonical_url = f"https://ideguide.blogspot.com/{date_str.replace('-', '/')}/{ide['id']}-review.html"

    amp_html = f"""<!doctype html>
<html amp lang="en">
<head>
  <meta charset="utf-8">
  <title>{ide['name']} Review: Good, Bad, and Pricing Breakdown - IDE Guide</title>
  <link rel="canonical" href="{canonical_url}">
  <meta name="viewport" content="width=device-width,initial-scale=1,minimum-scale=1,maximum-scale=1,user-scalable=no,minimal-ui">
  <script async src="https://cdn.ampproject.org/v0.js"></script>
  <style amp-boilerplate>body{{-webkit-animation:-amp-start 8s steps(1,end) 0s 1 normal both;-moz-animation:-amp-start 8s steps(1,end) 0s 1 normal both;-ms-animation:-amp-start 8s steps(1,end) 0s 1 normal both;animation:-amp-start 8s steps(1,end) 0s 1 normal both}}@-webkit-keyframes -amp-start{{from{{visibility:hidden}}to{{visibility:visible}}}}@-moz-keyframes -amp-start{{from{{visibility:hidden}}to{{visibility:visible}}}}@-ms-keyframes -amp-start{{from{{visibility:hidden}}to{{visibility:visible}}}}@-o-keyframes -amp-start{{from{{visibility:hidden}}to{{visibility:visible}}}}@keyframes -amp-start{{from{{visibility:hidden}}to{{visibility:visible}}}}</style><noscript><style amp-boilerplate>body{{-webkit-animation:none;-moz-animation:none;-ms-animation:none;animation:none}}</style></noscript>
  <style amp-custom>
    body {{
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
      line-height: 1.6;
      color: #1e293b;
      background-color: #f8fafc;
      margin: 0;
      padding: 0;
    }}
    .container {{
      max-width: 800px;
      margin: 0 auto;
      padding: 24px 16px;
    }}
    .header {{
      background: #0f172a;
      color: #ffffff;
      padding: 32px 24px;
      border-radius: 12px;
      margin-bottom: 24px;
    }}
    .badge {{
      background: #0284c7;
      color: #ffffff;
      padding: 4px 12px;
      font-size: 12px;
      font-weight: 700;
      border-radius: 100px;
      text-transform: uppercase;
      display: inline-block;
      margin-bottom: 12px;
    }}
    h1 {{
      margin: 0 0 12px 0;
      font-size: 28px;
    }}
    .card {{
      background: #ffffff;
      border: 1px solid #e2e8f0;
      border-radius: 12px;
      padding: 24px;
      margin-bottom: 24px;
      box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }}
    .pros-list li {{
      color: #15803d;
      margin-bottom: 8px;
    }}
    .cons-list li {{
      color: #b91c1c;
      margin-bottom: 8px;
    }}
    .price-box {{
      background: #eff6ff;
      border-left: 4px solid #2563eb;
      padding: 16px;
      margin-top: 16px;
      border-radius: 0 8px 8px 0;
    }}
    .disclaimer {{
      background: #f1f5f9;
      border: 1px solid #cbd5e1;
      padding: 16px;
      border-radius: 8px;
      font-size: 13px;
      color: #475569;
      margin-top: 32px;
      font-style: italic;
    }}
    .media-hero {{
      margin-bottom: 20px;
      border-radius: 8px;
      overflow: hidden;
    }}
  </style>
</head>
<body>
  <div class="container">
    <div class="header">
      <span class="badge">{ide['category']}</span>
      <h1>{ide['name']} - Complete Developer Evaluation</h1>
      <p>Developer: {ide['developer']} | Published: {date_str}</p>
    </div>

    <div class="card">
      <div class="media-hero">
        <amp-img src="{ide['image_url']}" width="800" height="450" layout="responsive" alt="{ide['name']} Interface Preview"></amp-img>
      </div>
      <h2>Overview</h2>
      <p>{ide['name']} is designed specifically for modern engineering teams. {ide['best_for']}</p>
    </div>

    <div class="card">
      <h2>The Good (Pros)</h2>
      <ul class="pros-list">
        {pros_html}
      </ul>

      <h2>The Bad (Cons)</h2>
      <ul class="cons-list">
        {cons_html}
      </ul>
    </div>

    <div class="card">
      <h2>Target Audience & Use Cases</h2>
      <p><strong>Who should use it:</strong> {ide['target_audience']}</p>

      <div class="price-box">
        <h3>Pricing Breakdown</h3>
        <p><strong>Model:</strong> {ide['pricing']}</p>
      </div>
    </div>

    <div class="disclaimer">
      {DISCLAIMER_TEXT}
    </div>
  </div>
</body>
</html>
"""
    return amp_html


def generate_google_flow_video_spec(ide: Dict[str, Any], date_str: str) -> Dict[str, Any]:
    spec = {
        "metadata": {
            "title": f"Is {ide['name']} Actually Worth It in 2026? (Good vs Bad)",
            "channel": "@IDEguide",
            "target_ide": ide["name"],
            "format": "Shorts (9:16 vertical) & YouTube Showcase",
            "date": date_str,
            "duration_seconds": 60
        },
        "google_flow_prompts": {
            "style_preset": "High-Tech Dark OLED Studio",
            "lighting_environment": "Cyberpunk Cyan & Blue LED backlight, subtle dark ambient contrast",
            "camera_framing": "Vertical 9:16 macro closeups, smooth panning across developer monitor and keyboard",
            "rendering_quality": "4K 60fps photorealistic UI demonstration with neon light reflections"
        },
        "shots": [
            {
                "shot_number": 1,
                "timestamp": "00:00 - 00:08",
                "visual_description": f"Cinematic fast zoom into a glowing ultra-wide monitor displaying {ide['name']}. Code lines populate smoothly with real-time syntax highlighting.",
                "voiceover_script": f"Looking for your next primary code editor? Today on IDE Guide, we review {ide['name']} by {ide['developer']}.",
                "b_roll": "Close-up macro shot of mechanical keyboard keypresses and IDE splash screen."
            },
            {
                "shot_number": 2,
                "timestamp": "00:08 - 00:22",
                "visual_description": "Split-screen glowing highlight showing key features and top positive pros with green checkmark graphics floating in 3D.",
                "voiceover_script": f"Here is what makes it great: {ide['pros'][0]}. Plus, {ide['pros'][1]}.",
                "b_roll": "Screen recording demonstrating quick code auto-completion and key editor shortcuts."
            },
            {
                "shot_number": 3,
                "timestamp": "00:22 - 00:38",
                "visual_description": "Overlay shifts to dark red accents with subtle animated warning badge icons highlighting limitations.",
                "voiceover_script": f"However, keep these drawbacks in mind: {ide['cons'][0]}",
                "b_roll": "CPU/RAM resource monitor gauge overlay showing memory footprint."
            },
            {
                "shot_number": 4,
                "timestamp": "00:38 - 00:50",
                "visual_description": "Comparison matrix UI showing free vs paid tier badges and target audience profiles.",
                "voiceover_script": f"Pricing model: {ide['pricing']}. It is best suited for {ide['target_audience']}",
                "b_roll": "Clean pricing card graphic and developer avatar icon."
            },
            {
                "shot_number": 5,
                "timestamp": "00:50 - 01:00",
                "visual_description": "Outro card displaying IDE Guide logo, YouTube subscribe prompt (@IDEguide), and text disclaimer banner.",
                "voiceover_script": "Subscribe to IDE Guide for daily objective editor breakdowns! Full non-sponsorship disclaimer in description.",
                "b_roll": "Animated Subscribe button click and URL callout to ideguide.blogspot.com."
            }
        ],
        "disclaimer": DISCLAIMER_TEXT
    }
    return spec


def spec_to_markdown(spec: Dict[str, Any]) -> str:
    md = f"# Google Flow Video Generation Spec: {spec['metadata']['target_ide']}\n\n"
    md += f"**Title:** {spec['metadata']['title']}\n"
    md += f"**Channel:** {spec['metadata']['channel']}\n"
    md += f"**Format:** {spec['metadata']['format']}\n"
    md += f"**Date:** {spec['metadata']['date']}\n\n"

    md += "## 🎬 Google Flow Visual Prompts\n"
    for k, v in spec["google_flow_prompts"].items():
        md += f"- **{k.replace('_', ' ').title()}:** {v}\n"
    md += "\n"

    md += "## ⏱️ Scene & Voiceover Breakdown\n\n"
    for shot in spec["shots"]:
        md += f"### Shot {shot['shot_number']} ({shot['timestamp']})\n"
        md += f"- **Visual Prompt:** {shot['visual_description']}\n"
        md += f"- **Voiceover Script:** \"{shot['voiceover_script']}\"\n"
        md += f"- **B-Roll / Action Notes:** {shot['b_roll']}\n\n"

    md += f"## ⚖️ Non-Sponsorship Disclaimer\n> {spec['disclaimer']}\n"
    return md


def run_daily_generation(date_str: str = None) -> List[str]:
    if not date_str:
        date_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    output_dir = os.path.join("content", date_str)
    os.makedirs(output_dir, exist_ok=True)

    selected_ides = select_daily_ides(count=3)
    generated_files = []

    for idx, ide in enumerate(selected_ides, 1):
        # 1. Generate AMP HTML blog post
        amp_html = generate_amp_blog_post(ide, date_str)
        post_path = os.path.join(output_dir, f"post_{idx}_{ide['id']}.html")
        with open(post_path, "w", encoding="utf-8") as f:
            f.write(amp_html)
        generated_files.append(post_path)

        # 2. Generate Google Flow video spec (JSON & Markdown)
        video_spec = generate_google_flow_video_spec(ide, date_str)
        json_path = os.path.join(output_dir, f"video_spec_{idx}_{ide['id']}.json")
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(video_spec, f, indent=2)
        generated_files.append(json_path)

        md_spec = spec_to_markdown(video_spec)
        md_path = os.path.join(output_dir, f"video_spec_{idx}_{ide['id']}.md")
        with open(md_path, "w", encoding="utf-8") as f:
            f.write(md_spec)
        generated_files.append(md_path)

    print(f"Generated {len(generated_files)} content items under {output_dir}:")
    for filepath in generated_files:
        print(f" - {filepath}")

    return generated_files


if __name__ == "__main__":
    target_date = sys.argv[1] if len(sys.argv) > 1 else None
    run_daily_generation(target_date)
