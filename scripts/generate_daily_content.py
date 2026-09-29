#!/usr/bin/env python3
"""
Daily Content Generation Engine for IDE Guide.
Generates 3 AMP HTML blog posts for Blogger and 3 Google Flow video specs for YouTube daily.
Tracks covered IDEs in content/history.json.
"""

import json
import os
import sys
from datetime import datetime, timezone
from typing import Dict, List, Any

# Knowledge base of IDEs and Code Editors
IDE_DATABASE: List[Dict[str, Any]] = [
    {
        "id": "vscode",
        "name": "Visual Studio Code (VS Code)",
        "developer": "Microsoft",
        "pricing_type": "Free / Open Source",
        "is_free": True,
        "pricing_details": "100% Free and open source (Core editor MIT, branded build binary proprietary telemetry).",
        "languages": ["TypeScript", "JavaScript", "Python", "Go", "Rust", "C++", "HTML/CSS"],
        "pros": [
            "Extensive ecosystem with over 50,000 extensions",
            "Blazing fast startup and lightweight memory footprint",
            "Built-in Git integration and terminal",
            "Native support for Remote Containers and SSH"
        ],
        "cons": [
            "Requires configuration and plugins for full IDE experience",
            "High memory consumption when loaded with heavy extension packs",
            "Microsoft telemetry enabled by default (can be turned off)"
        ],
        "best_for": "Web, cloud, and multi-language developers seeking a customizable modern editor.",
        "image_url": "https://images.unsplash.com/photo-1555066931-4365d14bab8c?w=800&auto=format&fit=crop&q=80"
    },
    {
        "id": "cursor",
        "name": "Cursor AI Code Editor",
        "developer": "Anysphere",
        "pricing_type": "Freemium",
        "is_free": False,
        "pricing_details": "Free tier includes basic requests. Pro plan is $20/month for unlimited fast AI models (GPT-4o, Claude 3.5 Sonnet).",
        "languages": ["TypeScript", "Python", "Rust", "Go", "C++", "Java"],
        "pros": [
            "Deep multi-file codebase indexing for contextual AI answers",
            "Native inline AI code generation and instant edits (Cmd+K / Cmd+I)",
            "100% VS Code extension and keybinding compatibility",
            "Terminal AI auto-fixing and agentic command prediction"
        ],
        "cons": [
            "Pro plan required for heavy daily AI usage",
            "Requires internet connection for full AI capabilities",
            "Privacy concerns if sending proprietary codebase chunks to cloud AI models"
        ],
        "best_for": "AI-first software engineers looking to accelerate feature building and refactoring.",
        "image_url": "https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?w=800&auto=format&fit=crop&q=80"
    },
    {
        "id": "pycharm",
        "name": "JetBrains PyCharm",
        "developer": "JetBrains",
        "pricing_type": "Freemium (Free Community / Paid Professional)",
        "is_free": False,
        "pricing_details": "Community Edition is Free. Professional Edition is $249/year (or $24.90/month) for individual developers.",
        "languages": ["Python", "SQL", "HTML/CSS", "JavaScript", "Cython"],
        "pros": [
            "Best-in-class Python static analysis, refactoring, and linting",
            "Deep Django, Flask, FastAPI, and scientific stack (Jupyter, Pandas) integration",
            "Powerful built-in visual debugger and test runner",
            "Advanced database tools and SQL editor built right in"
        ],
        "cons": [
            "Heavy memory and CPU utilization on smaller laptops",
            "Slow initial indexing time on massive repositories",
            "Professional web features locked behind commercial license"
        ],
        "best_for": "Professional Python developers, data scientists, and backend django engineers.",
        "image_url": "https://images.unsplash.com/photo-1515879218367-8466d910aaa4?w=800&auto=format&fit=crop&q=80"
    },
    {
        "id": "neovim",
        "name": "Neovim (Lua Ecosystem)",
        "developer": "Neovim Core Team & Community",
        "pricing_type": "100% Free / Open Source",
        "is_free": True,
        "pricing_details": "100% Free under Apache 2.0 and Vim License.",
        "languages": ["All Languages (via LSP, treesitter, damp syntax)"],
        "pros": [
            "Instant zero-latency editing and ultra-light memory usage (<50MB)",
            "Unlimited customizability using modern Lua configuration",
            "Built-in Language Server Protocol (LSP) and Treesitter parsing",
            "Modal editing speed and keyboard-driven efficiency"
        ],
        "cons": [
            "Steep learning curve for Vim motions and initial Lua setup",
            "No out-of-the-box GUI; requires configuration work",
            "Plugin ecosystem maintenance requires active maintenance"
        ],
        "best_for": "Terminal enthusiasts, backend systems engineers, and Vim keybinding power users.",
        "image_url": "https://images.unsplash.com/photo-1629654297299-c8506221ca97?w=800&auto=format&fit=crop&q=80"
    },
    {
        "id": "intellij_idea",
        "name": "IntelliJ IDEA",
        "developer": "JetBrains",
        "pricing_type": "Freemium (Free Community / Paid Ultimate)",
        "is_free": False,
        "pricing_details": "Community Edition is Free (JVM/Android). Ultimate Edition is $599/year or $59.90/month.",
        "languages": ["Java", "Kotlin", "Scala", "Groovy", "TypeScript", "SQL"],
        "pros": [
            "Industry standard for Enterprise Java and Kotlin development",
            "Smart code completion, automated refactoring, and inspection",
            "Seamless Spring Boot, Maven, Gradle, and Kubernetes support",
            "Superior git branch visualization and merge conflict resolution"
        ],
        "cons": [
            "Resource heavy; requires minimum 16GB RAM for smooth execution",
            "Paid subscription required for enterprise frameworks and JS/TS support",
            "Complex preference panel with hundreds of settings"
        ],
        "best_for": "Enterprise Java developers, Kotlin Android engineers, and microservices architects.",
        "image_url": "https://images.unsplash.com/photo-1542831371-29b0f74f9713?w=800&auto=format&fit=crop&q=80"
    },
    {
        "id": "zed",
        "name": "Zed Editor",
        "developer": "Zed Industries",
        "pricing_type": "Free / Open Source",
        "is_free": True,
        "pricing_details": "Editor is 100% Free & Open Source. Paid collaboration server options for enterprise.",
        "languages": ["Rust", "TypeScript", "Python", "C++", "Go"],
        "pros": [
            "Written in Rust with GPU-accelerated UI rendering at 120 FPS",
            "Blazing fast file scanning, search, and startup (<100ms)",
            "Built-in multiplayer real-time pair programming with voice audio",
            "Native AI chat integration with custom keybindings"
        ],
        "cons": [
            "Currently Linux and macOS primary support (Windows in development)",
            "Smaller extension ecosystem compared to VS Code",
            "Less configurable UI customization options"
        ],
        "best_for": "Developers prioritizing raw performance, instant latency, and high FPS editor responsiveness.",
        "image_url": "https://images.unsplash.com/photo-1504639725590-34d0984388bd?w=800&auto=format&fit=crop&q=80"
    },
    {
        "id": "windsurf",
        "name": "Windsurf Editor (Codeium)",
        "developer": "Codeium",
        "pricing_type": "Freemium",
        "is_free": False,
        "pricing_details": "Generous Free Tier available. Pro plan $15/month for unlimited agentic flows.",
        "languages": ["Python", "TypeScript", "Go", "Java", "C++", "Rust"],
        "pros": [
            "Revolutionary 'Cascade' agentic workflow blending copilot and autonomous coding",
            "Deep understanding of multi-file directory dependencies",
            "Fast indexing with privacy-first encryption options",
            "Full compatibility with VS Code extensions"
        ],
        "cons": [
            "Newer product with frequent rapid update releases",
            "Requires active internet connectivity for AI indexing",
            "Heavy agent operations can consume CPU during index creation"
        ],
        "best_for": "Full-stack developers seeking agentic coding assistance that works alongside human workflow.",
        "image_url": "https://images.unsplash.com/photo-1550751827-4bd374c3f58b?w=800&auto=format&fit=crop&q=80"
    },
    {
        "id": "xcode",
        "name": "Apple Xcode",
        "developer": "Apple Inc.",
        "pricing_type": "100% Free",
        "is_free": True,
        "pricing_details": "100% Free for macOS users (Apple Developer Program is $99/year for App Store publishing).",
        "languages": ["Swift", "Objective-C", "C++", "Metal"],
        "pros": [
            "Official IDE for iOS, macOS, watchOS, visionOS, and tvOS development",
            "Interactive SwiftUI Previews with live canvas editing",
            "Built-in Instruments for precise GPU and memory profiling",
            "Integrated App Store submission and TestFlight pipeline"
        ],
        "cons": [
            "Exclusively available on macOS hardware",
            "Large download footprint (>12GB download size)",
            "Interface can feel cluttered during complex project debugging"
        ],
        "best_for": "Apple platform developers building native iOS, iPadOS, macOS, and Swift applications.",
        "image_url": "https://images.unsplash.com/photo-1512941937669-90a1b58e7e9c?w=800&auto=format&fit=crop&q=80"
    },
    {
        "id": "android_studio",
        "name": "Android Studio",
        "developer": "Google / JetBrains",
        "pricing_type": "100% Free / Open Source",
        "is_free": True,
        "pricing_details": "100% Free under Apache License 2.0.",
        "languages": ["Kotlin", "Java", "C++", "Dart / Flutter"],
        "pros": [
            "Official IDE for Android OS development",
            "Advanced Jetpack Compose visual layout inspector",
            "Built-in high performance Android Emulator",
            "Gemini AI integration for code completion and crash analysis"
        ],
        "cons": [
            "High RAM requirement (16GB+ recommended)",
            "Emulator launch can slow down budget laptops",
            "Long Gradle build times on large Android codebases"
        ],
        "best_for": "Native Android app developers and Flutter cross-platform mobile engineers.",
        "image_url": "https://images.unsplash.com/photo-1607252650355-f7fd0460ccdb?w=800&auto=format&fit=crop&q=80"
    }
]

DISCLAIMER_TEXT = (
    "Disclaimer: IDE Guide is an independent technical publication. "
    "This content is not sponsored, endorsed, or affiliated with any software vendor "
    "or editor developer mentioned above. All reviews and assessments are based "
    "strictly on objective developer evaluation."
)


def load_history(history_filepath: str) -> Dict[str, Any]:
    if os.path.exists(history_filepath):
        try:
            with open(history_filepath, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {"reviewed_ides": [], "last_updated": None}


def save_history(history_filepath: str, history_data: Dict[str, Any]):
    os.makedirs(os.path.dirname(history_filepath), exist_ok=True)
    with open(history_filepath, "w", encoding="utf-8") as f:
        json.dump(history_data, f, indent=2)


def select_daily_ides(history_data: Dict[str, Any], count: int = 3) -> List[Dict[str, Any]]:
    reviewed = set(history_data.get("reviewed_ides", []))
    unreviewed = [ide for ide in IDE_DATABASE if ide["id"] not in reviewed]

    # If remaining unreviewed is less than count, reset history list keeping order
    if len(unreviewed) < count:
        history_data["reviewed_ides"] = []
        unreviewed = IDE_DATABASE

    selected = unreviewed[:count]
    return selected


def generate_amp_blog_post(ide: Dict[str, Any], date_str: str) -> str:
    pros_html = "".join([f"<li>{p}</li>" for p in ide["pros"]])
    cons_html = "".join([f"<li>{c}</li>" for c in ide["cons"]])
    langs_str = ", ".join(ide["languages"])
    price_tag = "FREE TOOL" if ide["is_free"] else "PAID / FREEMIUM TOOL"

    amp_html = f"""<!doctype html>
<html ⚡ lang="en">
<head>
  <meta charset="utf-8">
  <title>{ide['name']} Review & Developer Guide ({date_str}) | IDE Guide</title>
  <link rel="canonical" href="https://ideguide.blogspot.com/p/{ide['id']}-review.html">
  <meta name="viewport" content="width=device-width,minimum-scale=1,initial-scale=1">
  <script async src="https://cdn.ampproject.org/v0.js"></script>
  <style amp-boilerplate>body{{-webkit-animation:-amp-start 8s steps(1,end) 0s 1 normal both;-moz-animation:-amp-start 8s steps(1,end) 0s 1 normal both;-ms-animation:-amp-start 8s steps(1,end) 0s 1 normal both;animation:-amp-start 8s steps(1,end) 0s 1 normal both}}@keyframes -amp-start{{from{{visibility:hidden}}to{{visibility:visible}}}}</style><noscript><style amp-boilerplate>body{{-webkit-animation:none;-moz-animation:none;-ms-animation:none;animation:none}}</style></noscript>
  <style amp-custom>
    body {{
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
      line-height: 1.6;
      color: #1e293b;
      background-color: #f8fafc;
      margin: 0;
      padding: 0;
    }}
    header {{
      background: #0f172a;
      color: #ffffff;
      padding: 24px 20px;
      text-align: center;
    }}
    header h1 {{
      margin: 0 0 8px 0;
      font-size: 26px;
    }}
    .badge {{
      display: inline-block;
      padding: 4px 12px;
      border-radius: 12px;
      font-size: 12px;
      font-weight: bold;
      text-transform: uppercase;
      background: #3b82f6;
      color: #ffffff;
    }}
    .badge-free {{ background: #10b981; }}
    .badge-paid {{ background: #f59e0b; }}
    .container {{
      max-width: 800px;
      margin: 20px auto;
      padding: 20px;
      background: #ffffff;
      border-radius: 8px;
      box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }}
    .hero-img {{
      margin-bottom: 20px;
      border-radius: 6px;
      overflow: hidden;
    }}
    h2 {{
      color: #0f172a;
      border-bottom: 2px solid #e2e8f0;
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
      flex: 1 1 300px;
      padding: 16px;
      border-radius: 6px;
    }}
    .pros {{ background: #ecfdf5; border-left: 4px solid #10b981; }}
    .cons {{ background: #fef2f2; border-left: 4px solid #ef4444; }}
    .disclaimer {{
      margin-top: 40px;
      padding: 16px;
      background: #f1f5f9;
      border: 1px solid #cbd5e1;
      border-radius: 6px;
      font-size: 13px;
      color: #64748b;
      font-style: italic;
    }}
    footer {{
      text-align: center;
      padding: 20px;
      font-size: 12px;
      color: #94a3b8;
    }}
  </style>
</head>
<body>
  <header>
    <h1>{ide['name']}</h1>
    <span class="badge {'badge-free' if ide['is_free'] else 'badge-paid'}">{price_tag}</span>
    <p>Published: {date_str} • Developed by {ide['developer']}</p>
  </header>

  <div class="container">
    <div class="hero-img">
      <amp-img src="{ide['image_url']}" width="800" height="400" layout="responsive" alt="{ide['name']} Workspace Screenshot"></amp-img>
    </div>

    <h2>1. Executive Overview</h2>
    <p><strong>{ide['name']}</strong> is a leading code editing solution created by {ide['developer']}. It primarily serves software engineers specializing in <strong>{langs_str}</strong>.</p>

    <h2>2. Pricing & Licensing Breakdown</h2>
    <p><strong>Cost Status:</strong> {'100% Free / Open Source' if ide['is_free'] else 'Paid / Freemium Model'}</p>
    <p>{ide['pricing_details']}</p>

    <h2>3. Developer Pros & Cons</h2>
    <div class="pros-cons">
      <div class="box pros">
        <h3>✅ Core Strengths</h3>
        <ul>{pros_html}</ul>
      </div>
      <div class="box cons">
        <h3>❌ Trade-offs & Limitations</h3>
        <ul>{cons_html}</ul>
      </div>
    </div>

    <h2>4. Final Verdict & Who Should Use It</h2>
    <p>{ide['best_for']}</p>

    <div class="disclaimer">
      {DISCLAIMER_TEXT}
    </div>
  </div>

  <footer>
    <p>© IDE Guide • Independent Developer Tools Publication • <a href="https://ideguide.blogspot.com/">https://ideguide.blogspot.com/</a></p>
  </footer>
</body>
</html>
"""
    return amp_html


def generate_google_flow_spec(ide: Dict[str, Any], date_str: str) -> Dict[str, Any]:
    langs = ", ".join(ide["languages"][:3])
    pricing_status = "100% FREE & OPEN SOURCE" if ide["is_free"] else "PAID / FREEMIUM MODEL"

    spec = {
        "channel": "IDE Guide (@IDEguide)",
        "target_platform": "YouTube Shorts (9:16) & YouTube Video (16:9)",
        "ide_name": ide["name"],
        "date": date_str,
        "pricing_category": pricing_status,
        "disclaimer_required": True,
        "google_flow_prompts": {
            "style_preset": "Dark mode developer workspace, cinematic neon syntax, macro camera movement, 4K resolution, 60fps",
            "scenes": [
                {
                    "scene_number": 1,
                    "timecode": "00:00 - 00:05",
                    "title": "Hook / Editor Intro",
                    "visual_prompt": f"Macro cinematic pan across {ide['name']} user interface showing vibrant dark mode code in {langs}, subtle neon backlight glow, smooth camera track forward, 4k hyper-realistic",
                    "camera_motion": "Slow forward dolly track into editor cursor",
                    "voiceover": f"Is {ide['name']} worth using for your projects in 2026? Let's break down the good, the bad, and the pricing!",
                    "text_overlay": f"{ide['name']} - Complete Review",
                    "audio_sfx": "Upbeat futuristic synth beat with mechanical keyboard clack SFX"
                },
                {
                    "scene_number": 2,
                    "timecode": "00:05 - 00:20",
                    "title": "Pricing & Key Strengths",
                    "visual_prompt": f"Split screen shot showing {ide['name']} handling complex code refactoring on left and floating badge on right reading '{pricing_status}', dramatic studio lighting",
                    "camera_motion": "Rack focus from pricing card to active editor window",
                    "voiceover": f"First off, pricing: {ide['pricing_details']} Main advantage? {ide['pros'][0]} and {ide['pros'][1]}.",
                    "text_overlay": f"STATUS: {pricing_status}\n✅ {ide['pros'][0]}",
                    "audio_sfx": "Digital pop SFX on bullet reveal"
                },
                {
                    "scene_number": 3,
                    "timecode": "00:20 - 00:40",
                    "title": "Limitations & Trade-offs",
                    "visual_prompt": f"Close-up profile of developer reviewing diagnostics panel in {ide['name']}, amber highlight on warnings, sleek dark aesthetic",
                    "camera_motion": "Slow pan right across side dock panels",
                    "voiceover": f"However, keep in mind: {ide['cons'][0]}",
                    "text_overlay": f"⚠️ CONSIDERATION: {ide['cons'][0]}",
                    "audio_sfx": "Subtle warning chime SFX"
                },
                {
                    "scene_number": 4,
                    "timecode": "00:40 - 00:60",
                    "title": "Final Recommendation & Non-Sponsored Callout",
                    "visual_prompt": f"Cinematic wide view of dark developer studio desk with dual monitors displaying {ide['name']} and YouTube IDE Guide logo, soft neon rim lighting",
                    "camera_motion": "Slow tilt upwards and zoom back to end card",
                    "voiceover": f"Verdict? {ide['best_for']} Remember, IDE Guide is independent and not sponsored by any editor vendor. Subscribe to @IDEguide for unbiased developer tools guides!",
                    "text_overlay": "IDE Guide • Independent Review\nSubscribe @IDEguide | ideguide.blogspot.com",
                    "audio_sfx": "Smooth fade out synth music with click subscribe chime"
                }
            ]
        },
        "non_sponsorship_disclaimer": DISCLAIMER_TEXT
    }
    return spec


def main():
    date_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    out_dir = os.path.join("content", date_str)
    os.makedirs(out_dir, exist_ok=True)

    history_file = os.path.join("content", "history.json")
    history_data = load_history(history_file)

    selected_ides = select_daily_ides(history_data, count=3)

    print(f"🚀 Generating daily content package for {date_str}...")

    generated_files = []
    for idx, ide in enumerate(selected_ides, start=1):
        # 1. Generate AMP Blog Post
        amp_html = generate_amp_blog_post(ide, date_str)
        amp_filename = f"blog_{idx}_{ide['id']}.html"
        amp_filepath = os.path.join(out_dir, amp_filename)
        with open(amp_filepath, "w", encoding="utf-8") as f:
            f.write(amp_html)
        generated_files.append(amp_filepath)

        # 2. Generate Google Flow Spec
        flow_spec = generate_google_flow_spec(ide, date_str)
        flow_filename = f"video_flow_{idx}_{ide['id']}.json"
        flow_filepath = os.path.join(out_dir, flow_filename)
        with open(flow_filepath, "w", encoding="utf-8") as f:
            json.dump(flow_spec, f, indent=2)
        generated_files.append(flow_filepath)

        # Update history
        if ide["id"] not in history_data["reviewed_ides"]:
            history_data["reviewed_ides"].append(ide["id"])

    history_data["last_updated"] = date_str
    save_history(history_file, history_data)

    print(f"✅ Successfully generated {len(generated_files)} content files in {out_dir}:")
    for filepath in generated_files:
        print(f"  - {filepath}")


if __name__ == "__main__":
    main()
