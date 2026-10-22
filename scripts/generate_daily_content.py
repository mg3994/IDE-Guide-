#!/usr/bin/env python3
"""
Daily Content Generator for IDE Guide
Generates 3 AMP HTML blog posts and 3 Google Flow video specifications daily.
Outputs generated content into content/YYYY-MM-DD/ and updates content/history.json.
"""

import os
import sys
import json
import datetime
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scripts.amp_validator import REQUIRED_DISCLAIMER, validate_amp_html

IDE_POOL = [
    {
        "id": "vscode",
        "name": "Visual Studio Code",
        "developer": "Microsoft",
        "pricing": "Free & Open Source (Core)",
        "price_category": "Free",
        "pros": [
            "Extensive ecosystem with tens of thousands of extensions",
            "Built-in Git integration, interactive debugger, and terminal",
            "Highly customizable workspace with themes and keybindings"
        ],
        "cons": [
            "Electron-based resource overhead on large monorepos",
            "Can become slow with too many active background plugins"
        ],
        "best_for": "Full-stack web developers, JavaScript/TypeScript engineers, and polyglot programmers.",
        "key_features": "Marketplace extensions, IntelliSense, integrated terminal, remote SSH development."
    },
    {
        "id": "cursor",
        "name": "Cursor Editor",
        "developer": "Anysphere",
        "pricing": "Freemium (Free tier available, Pro at $20/mo)",
        "price_category": "Freemium",
        "pros": [
            "Native deep AI integration powered by Claude 3.5 Sonnet & GPT-4o",
            "Full VS Code extension compatibility",
            "Multi-file repository indexing and instant codebase chat"
        ],
        "cons": [
            "Requires subscription for unlimited fast AI completions",
            "Dependent on cloud AI endpoint connectivity"
        ],
        "best_for": "Developers seeking maximum AI-assisted productivity and full-codebase refactoring.",
        "key_features": "Composer AI agent, codebase semantic search, instant edit applied inline."
    },
    {
        "id": "zed",
        "name": "Zed Editor",
        "developer": "Zed Industries",
        "pricing": "Free & Open Source",
        "price_category": "Free",
        "pros": [
            "Written in Rust for unmatched GPU-accelerated rendering and instant startup",
            "Low RAM consumption compared to Electron editors",
            "Built-in real-time collaborative editing features"
        ],
        "cons": [
            "Extension marketplace is still maturing compared to VS Code",
            "Currently limited advanced debuggers for niche languages"
        ],
        "best_for": "Performance enthusiasts, Systems programmers, and Rust/C++ developers.",
        "key_features": "GPU acceleration, Rust native performance, multiplayer code editing."
    },
    {
        "id": "pycharm",
        "name": "PyCharm",
        "developer": "JetBrains",
        "pricing": "Freemium (Community Free, Professional $249/yr)",
        "price_category": "Freemium",
        "pros": [
            "Industry-leading Python code intelligence, refactoring, and linting",
            "Built-in database tooling, Jupyter Notebook integration, and Django support",
            "Sophisticated visual debugger and profiler"
        ],
        "cons": [
            "Heavy RAM and CPU resource footprint",
            "Slower project indexing times on massive codebases"
        ],
        "best_for": "Python developers, Data Scientists, AI/ML engineers, and Django backend developers.",
        "key_features": "Deep code inspection, visual debugger, built-in database terminal, Django tools."
    },
    {
        "id": "neovim",
        "name": "Neovim",
        "developer": "Neovim Core Team",
        "pricing": "Free & Open Source",
        "price_category": "Free",
        "pros": [
            "Near-zero latency and ultra-lightweight memory footprint",
            "Extensible using Lua with a massive community plugin ecosystem",
            "Built-in LSP (Language Server Protocol) client and Tree-sitter parsing"
        ],
        "cons": [
            "Steep initial learning curve for modal editing and Lua configuration",
            "Requires manual setup for complex visual debugging"
        ],
        "best_for": "Terminal power users, DevOps engineers, and developers who prefer modal editing.",
        "key_features": "Lua scripting, asynchronous architecture, built-in LSP, Tree-sitter syntax engine."
    },
    {
        "id": "intellij",
        "name": "IntelliJ IDEA",
        "developer": "JetBrains",
        "pricing": "Freemium (Community Free, Ultimate $599/yr)",
        "price_category": "Freemium",
        "pros": [
            "Unrivaled Java, Kotlin, and JVM ecosystem code refactoring",
            "Comprehensive enterprise tools for Spring Boot, Microservices, and Kubernetes",
            "Top-tier static analysis and automated code completion"
        ],
        "cons": [
            "Significant memory footprint requiring 8GB+ RAM allocation",
            "Ultimate features are behind commercial licensing"
        ],
        "best_for": "Enterprise Java/Kotlin developers, Android backend creators, and JVM engineers.",
        "key_features": "JVM refactoring, Spring framework support, structural search, enterprise integration."
    },
    {
        "id": "windsurf",
        "name": "Windsurf Editor",
        "developer": "Codeium",
        "pricing": "Freemium (Free tier available, Pro at $15/mo)",
        "price_category": "Freemium",
        "pros": [
            "First agentic IDE featuring Cascade AI contextual workflows",
            "Deep integration with Codeium AI engine for high-accuracy code completion",
            "Seamless VS Code extension compatibility"
        ],
        "cons": [
            "Relatively new tool with evolving user interface patterns",
            "Advanced agentic flows require active subscription"
        ],
        "best_for": "Developers who want AI agents that autonomously execute complex multi-step refactors.",
        "key_features": "Cascade AI agent flow, real-time command execution, full codebase context."
    },
    {
        "id": "xcode",
        "name": "Xcode",
        "developer": "Apple",
        "pricing": "Free (Requires macOS)",
        "price_category": "Free",
        "pros": [
            "Official IDE for iOS, macOS, watchOS, and visionOS development",
            "Integrated SwiftUI live preview interactive canvas and Instruments profiler",
            "Seamless integration with TestFlight and App Store Connect"
        ],
        "cons": [
            "Exclusive to macOS hardware",
            "Large download size (12GB+) and occasional compiler indexing lag"
        ],
        "best_for": "Apple platform engineers, Swift developers, and iOS app creators.",
        "key_features": "SwiftUI live previews, LLDB debugger, Instruments profiler, Simulator."
    },
    {
        "id": "sublime",
        "name": "Sublime Text 4",
        "developer": "Sublime HQ",
        "pricing": "Paid ($99 per license, free evaluation)",
        "price_category": "Paid",
        "pros": [
            "Incredible speed with C++ backend and GPU rendering acceleration",
            "Super-lightweight startup and minimal RAM footprint",
            "Powerful multi-cursor editing and Package Control ecosystem"
        ],
        "cons": [
            "Evaluation popups if unlicenced",
            "Lacks built-in terminal or debugger out of the box without plugins"
        ],
        "best_for": "Developers who prioritize raw editing speed and ultra-lightweight responsiveness.",
        "key_features": "GPU rendering, multi-selection editing, Goto Anything, fast syntax indexing."
    }
]


def generate_amp_blog_post(tool: dict) -> str:
    """Generates valid AMP HTML blog post string for Blogger."""
    good_items = "".join([f"<li><strong>{p}</strong></li>" for p in tool["pros"]])
    bad_items = "".join([f"<li><strong>{c}</strong></li>" for c in tool["cons"]])

    html = f"""<!DOCTYPE html>
<html ⚡ lang="en">
<head>
  <meta charset="utf-8">
  <title>{tool['name']} Review & Comparison - IDE Guide</title>
  <link rel="canonical" href="https://ideguide.blogspot.com/p/{tool['id']}-review.html">
  <meta name="viewport" content="width=device-width,initial-scale=1,minimum-scale=1">
  <script async src="https://cdn.ampproject.org/v0.js"></script>
  <style amp-boilerplate>body{{-webkit-animation:-amp-start 8s steps(1,end) 0s 1 normal both;-moz-animation:-amp-start 8s steps(1,end) 0s 1 normal both;-ms-animation:-amp-start 8s steps(1,end) 0s 1 normal both;animation:-amp-start 8s steps(1,end) 0s 1 normal both}}@-webkit-keyframes -amp-start{{from{{visibility:hidden}}to{{visibility:visible}}}}@-moz-keyframes -amp-start{{from{{visibility:hidden}}to{{visibility:visible}}}}@-ms-keyframes -amp-start{{from{{visibility:hidden}}to{{visibility:visible}}}}@-o-keyframes -amp-start{{from{{visibility:hidden}}to{{visibility:visible}}}}@keyframes -amp-start{{from{{visibility:hidden}}to{{visibility:visible}}}}</style><noscript><style amp-boilerplate>body{{-webkit-animation:none;-moz-animation:none;-ms-animation:none;animation:none}}</style></noscript>
  <style amp-custom>
    body {{
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
      line-height: 1.6;
      color: #222222;
      background-color: #f8f9fa;
      margin: 0;
      padding: 16px;
    }}
    .container {{
      max-width: 800px;
      margin: 0 auto;
      background: #ffffff;
      padding: 24px;
      border-radius: 8px;
      box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }}
    h1 {{
      color: #1a73e8;
      font-size: 28px;
      margin-bottom: 8px;
    }}
    .meta-badge {{
      display: inline-block;
      background: #e8f0fe;
      color: #1a73e8;
      padding: 4px 12px;
      border-radius: 16px;
      font-weight: 600;
      font-size: 14px;
      margin-bottom: 20px;
    }}
    .section-title {{
      font-size: 20px;
      border-bottom: 2px solid #e0e0e0;
      padding-bottom: 6px;
      margin-top: 24px;
    }}
    .good-list li {{
      color: #1e8e3e;
      margin-bottom: 8px;
    }}
    .bad-list li {{
      color: #d93025;
      margin-bottom: 8px;
    }}
    .price-box {{
      background: #f1f3f4;
      padding: 16px;
      border-left: 4px solid #1a73e8;
      border-radius: 4px;
      margin: 16px 0;
    }}
    .verdict-box {{
      background: #e6f4ea;
      padding: 16px;
      border-left: 4px solid #1e8e3e;
      border-radius: 4px;
      margin: 16px 0;
    }}
    .disclaimer-box {{
      background: #fce8e6;
      border: 1px solid #fad2cf;
      padding: 16px;
      border-radius: 6px;
      margin-top: 32px;
      font-size: 13px;
      color: #5f6368;
    }}
  </style>
</head>
<body>
  <div class="container">
    <h1>{tool['name']} Comprehensive Review</h1>
    <div class="meta-badge">Developer: {tool['developer']} | Tier: {tool['price_category']}</div>

    <p>Welcome to <strong>IDE Guide</strong>! Today we perform an objective developer evaluation of <strong>{tool['name']}</strong>, exploring its core capabilities, strengths, weaknesses, pricing model, and best use cases.</p>

    <amp-img src="https://images.unsplash.com/photo-1555066931-4365d14bab8c?w=800&auto=format&fit=crop" width="800" height="450" layout="responsive" alt="{tool['name']} Code Editor Setup"></amp-img>

    <h2 class="section-title">The Good (Pros)</h2>
    <ul class="good-list">
      {good_items}
    </ul>

    <h2 class="section-title">The Bad (Cons)</h2>
    <ul class="bad-list">
      {bad_items}
    </ul>

    <h2 class="section-title">Pricing & Licensing Model</h2>
    <div class="price-box">
      <strong>Pricing structure:</strong> {tool['pricing']}<br>
      Key highlights: {tool['key_features']}
    </div>

    <h2 class="section-title">Recommendation: Who is it best for?</h2>
    <div class="verdict-box">
      <strong>Verdict:</strong> {tool['best_for']}
    </div>

    <div class="disclaimer-box">
      <p>{REQUIRED_DISCLAIMER}</p>
    </div>
  </div>
</body>
</html>"""
    return html


def generate_google_flow_spec(tool: dict) -> tuple:
    """Generates Google Flow video specification dict and markdown string."""
    flow_dict = {
        "channel": "@IDEguide",
        "tool_id": tool["id"],
        "tool_name": tool["name"],
        "target_formats": [
            {"type": "YouTube Standard", "aspect_ratio": "16:9", "resolution": "1920x1080", "fps": 60},
            {"type": "YouTube Shorts", "aspect_ratio": "9:16", "resolution": "1080x1920", "fps": 60}
        ],
        "visual_aesthetics": {
            "style": "Dark mode code editor with neon highlight accents (cyan, magenta, yellow)",
            "lighting": "Soft studio ambient backlight with cool blue edge glow on matte desk setup",
            "environment": "Sleek developer workspace with high-refresh monitor showcasing code editor UI"
        },
        "scenes": [
            {
                "scene_number": 1,
                "title": "Hook & Fast Introduction",
                "duration_seconds": 7,
                "visual_prompt": f"Macro fast camera zoom-in on {tool['name']} clean dark interface launching instantly on crisp monitor screen.",
                "camera_motion": "Fast smooth push-in",
                "narration_script": f"Is {tool['name']} the best code editor for your developer stack? Let's break down the good, the bad, and the pricing in 60 seconds!"
            },
            {
                "scene_number": 2,
                "title": "The Good (Pros Showcase)",
                "duration_seconds": 18,
                "visual_prompt": f"Slow tracking pan across {tool['name']} code editor showing syntax highlighting, intelligent code completion, and extension panel.",
                "camera_motion": "Smooth left-to-right tracking pan",
                "narration_script": f"The Good: {tool['pros'][0]}. Plus, {tool['pros'][1]}."
            },
            {
                "scene_number": 3,
                "title": "The Bad (Cons & Limitations)",
                "duration_seconds": 15,
                "visual_prompt": "Close-up shot of system monitor RAM allocation or complex keybinding config overlay.",
                "camera_motion": "Static close-up with subtle drift",
                "narration_script": f"The Bad: {tool['cons'][0]}."
            },
            {
                "scene_number": 4,
                "title": "Pricing & Licensing",
                "duration_seconds": 10,
                "visual_prompt": f"Infographic visual graphic highlighting price model: {tool['pricing']}.",
                "camera_motion": "Gentle zoom out to reveal comparison badge",
                "narration_script": f"Pricing: {tool['pricing']}."
            },
            {
                "scene_number": 5,
                "title": "Verdict & Non-Sponsorship Disclaimer",
                "duration_seconds": 10,
                "visual_prompt": "Wide shot of sleek workspace with prominent disclaimer overlay: 'Not Sponsored - Objective Review'.",
                "camera_motion": "Steady static wide shot",
                "narration_script": f"Verdict: {tool['best_for']} Visit ideguide.blogspot.com for the full AMP breakdown!"
            }
        ],
        "disclaimer": REQUIRED_DISCLAIMER
    }

    markdown = f"""# Google Flow Video Generation Spec: {tool['name']}

**Channel**: @IDEguide
**Formats**: 16:9 (YouTube Video) & 9:16 (YouTube Shorts)

---

## Visual Aesthetics & Prompt Configuration
- **Visual Style**: Dark mode editor UI with neon syntax highlighting.
- **Lighting**: Cool studio ambient lighting with violet backlighting.
- **Environment**: Clean developer setup with high-resolution monitor.

---

## Storyboard & Narration Script

### Scene 1: Hook (0s - 7s)
- **Visual Prompt**: Macro fast camera zoom-in on {tool['name']} clean dark interface launching instantly.
- **Camera**: Fast smooth push-in
- **Narration**: *"Is {tool['name']} the best code editor for your developer stack? Let's break down the good, the bad, and the pricing in 60 seconds!"*

### Scene 2: The Good (7s - 25s)
- **Visual Prompt**: Slow tracking pan across {tool['name']} code editor showing syntax highlighting.
- **Camera**: Smooth left-to-right tracking pan
- **Narration**: *"The Good: {tool['pros'][0]}. Plus, {tool['pros'][1]}."*

### Scene 3: The Bad (25s - 40s)
- **Visual Prompt**: Close-up shot of resource allocation or configuration files.
- **Camera**: Static close-up
- **Narration**: *"The Bad: {tool['cons'][0]}."*

### Scene 4: Pricing (40s - 50s)
- **Visual Prompt**: Visual graphic showing price model: {tool['pricing']}.
- **Camera**: Gentle zoom out
- **Narration**: *"Pricing: {tool['pricing']}."*

### Scene 5: Verdict & Disclaimer (50s - 60s)
- **Visual Prompt**: Wide shot with overlay: 'Not Sponsored - Objective Evaluation'.
- **Camera**: Static wide shot
- **Narration**: *"Verdict: {tool['best_for']} Visit ideguide.blogspot.com for full AMP breakdown!"*

---

## Non-Sponsorship Disclaimer
> {REQUIRED_DISCLAIMER}
"""
    return flow_dict, markdown


def generate_daily_content(today_str: str = None) -> list:
    if not today_str:
        today_str = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d")

    history_path = Path("content/history.json")
    history_path.parent.mkdir(parents=True, exist_ok=True)

    history = {"covered_ids": [], "history_log": []}
    if history_path.exists():
        try:
            with open(history_path, "r", encoding="utf-8") as f:
                history = json.load(f)
        except Exception:
            pass

    covered = set(history.get("covered_ids", []))
    available = [t for t in IDE_POOL if t["id"] not in covered]

    if len(available) < 3:
        # Reset covered if pool runs low
        covered = set()
        history["covered_ids"] = []
        available = IDE_POOL

    selected_tools = available[:3]

    day_dir = Path(f"content/{today_str}")
    day_dir.mkdir(parents=True, exist_ok=True)

    generated_dirs = []

    for idx, tool in enumerate(selected_tools, start=1):
        tool_slug = f"post-{idx}-{tool['id']}"
        post_dir = day_dir / tool_slug
        post_dir.mkdir(parents=True, exist_ok=True)

        # 1. Generate AMP HTML blog post
        amp_html = generate_amp_blog_post(tool)
        amp_val = validate_amp_html(amp_html)
        if not amp_val["valid"]:
            raise ValueError(f"Generated AMP HTML for {tool['name']} failed validation: {amp_val['errors']}")

        amp_file = post_dir / "blog_post.amp.html"
        with open(amp_file, "w", encoding="utf-8") as f:
            f.write(amp_html)

        # 2. Generate Google Flow video spec
        flow_json, flow_md = generate_google_flow_spec(tool)
        with open(post_dir / "video_flow_spec.json", "w", encoding="utf-8") as f:
            json.dump(flow_json, f, indent=2)

        with open(post_dir / "video_flow_spec.md", "w", encoding="utf-8") as f:
            f.write(flow_md)

        generated_dirs.append(str(post_dir))

        # Track history
        if tool["id"] not in history["covered_ids"]:
            history["covered_ids"].append(tool["id"])

    history["history_log"].append({
        "date": today_str,
        "tools": [t["id"] for t in selected_tools]
    })

    with open(history_path, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=2)

    return generated_dirs


if __name__ == "__main__":
    dirs = generate_daily_content()
    print(f"Successfully generated 3 daily content packages:")
    for d in dirs:
        print(f" - {d}")
