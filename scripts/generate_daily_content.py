#!/usr/bin/env python3
"""
IDE Database & Content Generator for IDE Guide.
Generates 3 daily AMP HTML blog posts and 3 Google Flow video specifications.
Tracks covered IDEs/editors in content/history.json to ensure fresh daily coverage.
"""

import json
import os
import sys
from datetime import datetime, timezone

DISCLAIMER_TEXT = "Disclaimer: IDE Guide is an independent technical publication. This content is not sponsored, endorsed, or affiliated with any software vendor or editor developer mentioned above. All reviews and assessments are based strictly on objective developer evaluation."

IDE_DATABASE = [
    {
        "id": "cursor",
        "name": "Cursor AI",
        "category": "AI-Powered Code Editor",
        "pricing_type": "Freemium",
        "price_detail": "Free tier available; Pro plan at $20/month for unlimited Claude 3.5 Sonnet & GPT-4o usage.",
        "pros": [
            "Native AI integration built directly into VS Code fork",
            "Multi-file edit prediction and agentic repository chat",
            "Instant indexing of codebase for semantic search",
            "Full compatibility with existing VS Code extensions"
        ],
        "cons": [
            "Proprietary backend for AI features",
            "Requires monthly subscription for heavy AI feature access",
            "Occasional context window limits on extremely large repos"
        ],
        "best_for": "Developers wanting bleeding-edge AI code generation directly integrated into a familiar VS Code workflow."
    },
    {
        "id": "vscode",
        "name": "Visual Studio Code",
        "category": "Extensible Code Editor",
        "pricing_type": "Free / Open Source (Core)",
        "price_detail": "100% Free under MIT license (Code-OSS) with official Microsoft builds available at no charge.",
        "pros": [
            "Massive extension marketplace with over 50,000 extensions",
            "Lightweight core with exceptional startup speed",
            "Built-in Git integration, terminal, and debugging support",
            "Universal adoption across web, cloud, and backend development"
        ],
        "cons": [
            "Heavy memory footprint when loading numerous extensions",
            "Microsoft telemetry included in default binary releases",
            "Requires configuration and extensions for out-of-the-box IDE functionality"
        ],
        "best_for": "Web developers, polyglot programmers, and anyone needing a fast, customizable code editor."
    },
    {
        "id": "neovim",
        "name": "Neovim",
        "category": "Terminal-based Modal Text Editor",
        "pricing_type": "Free & Open Source",
        "price_detail": "100% Free (Apache / Vim License).",
        "pros": [
            "Blazing fast startup time and minimal RAM usage (< 50MB)",
            "Extensible via Lua scripting and rich ecosystem (Lazy.nvim, Mason)",
            "Native LSP (Language Server Protocol) and Treesitter support",
            "Runs entirely in command line / terminal environments"
        ],
        "cons": [
            "Steep learning curve for modal editing and custom configuration",
            "No native GUI out of the box",
            "Initial setup time can take several hours to tweak to perfection"
        ],
        "best_for": "Power users, terminal enthusiasts, and developers who prioritize raw speed and keyboard-driven workflows."
    },
    {
        "id": "zed",
        "name": "Zed Editor",
        "category": "High-Performance Code Editor",
        "pricing_type": "Free & Open Source",
        "price_detail": "Free for local use; optional paid cloud collaboration tiers.",
        "pros": [
            "Written in Rust with GPU-accelerated rendering at 120+ FPS",
            "Ultra-low latency typing and lightning-fast file searching",
            "Real-time multiplayer collaborative editing built-in",
            "Integrated AI assistant support (Claude, OpenAI, Ollama)"
        ],
        "cons": [
            "Smaller plugin ecosystem compared to VS Code",
            "Linux and Windows support is still evolving relative to macOS base",
            "Fewer niche language toolings available out-of-the-box"
        ],
        "best_for": "Performance-obsessed developers and real-time remote engineering teams."
    },
    {
        "id": "intellij_idea",
        "name": "IntelliJ IDEA",
        "category": "Full-Featured Java & Kotlin IDE",
        "pricing_type": "Freemium / Paid",
        "price_detail": "Community Edition is free & open source; Ultimate Edition starts at $169/year.",
        "pros": [
            "Industry standard for Enterprise Java, Kotlin, and Spring Boot",
            "Unrivaled automated refactoring and static code analysis",
            "Deep database management, profiler, and HTTP client integration",
            "Robust out-of-the-box setup requiring zero extension hunting"
        ],
        "cons": [
            "High RAM and CPU consumption (requires 16GB+ RAM for best experience)",
            "Steep license cost for individual Ultimate edition users",
            "Slower project indexing times on huge monorepos"
        ],
        "best_for": "Enterprise Java/Kotlin developers and backend software engineers."
    },
    {
        "id": "windsurf",
        "name": "Windsurf IDE (Codeium)",
        "category": "Agentic AI IDE",
        "pricing_type": "Freemium",
        "price_detail": "Free tier with generous AI credits; Pro tier at $15/month.",
        "pros": [
            "Cascade AI agent capable of multi-step codebase refactoring",
            "Deep awareness of terminal output, git diffs, and codebase structure",
            "Fast responsiveness powered by Codeium infrastructure",
            "Built on VS Code architecture for instant migration"
        ],
        "cons": [
            "Newer product with rapid feature updates and minor UI shifts",
            "Requires active internet connection for Cascade agentic features",
            "Paid tiers required for heavy enterprise token usage"
        ],
        "best_for": "Developers seeking an AI-first IDE with autonomous agent capabilities for complex refactoring tasks."
    },
    {
        "id": "pycharm",
        "name": "PyCharm",
        "category": "Python & Data Science IDE",
        "pricing_type": "Freemium / Paid",
        "price_detail": "Community Edition is free; Professional Edition starts at $99/year.",
        "pros": [
            "Premier Python development environment with Django, Flask, and FastAPI support",
            "Integrated Jupyter notebook interface and scientific data view",
            "Powerful Python debugger and virtualenv / Conda environment manager",
            "Refactoring tools specifically tailored for dynamic Python code"
        ],
        "cons": [
            "Heavier memory footprint than lightweight text editors",
            "Web framework and database tools locked behind paid Professional edition",
            "Project startup can be delayed by package indexing"
        ],
        "best_for": "Python developers, data scientists, and Django web engineers."
    },
    {
        "id": "xcode",
        "name": "Xcode",
        "category": "Apple Platform IDE",
        "pricing_type": "Free (macOS only)",
        "price_detail": "100% Free on Mac App Store (Apple Developer Program $99/yr needed for App Store submission).",
        "pros": [
            "Essential official IDE for iOS, macOS, watchOS, and visionOS development",
            "Seamless SwiftUI interactive visual canvas and simulator integration",
            "Built-in Instruments tool for deep memory and CPU performance profiling",
            "Integrated Metal shader tools and Asset Catalogs"
        ],
        "cons": [
            "Exclusive to macOS (cannot be run on Windows/Linux natively)",
            "Large download size (>12 GB) and frequent large updates",
            "Occasional simulator glitches and indexing hangs"
        ],
        "best_for": "iOS, iPadOS, macOS, and Swift/SwiftUI developers."
    },
    {
        "id": "android_studio",
        "name": "Android Studio",
        "category": "Android Platform IDE",
        "pricing_type": "Free & Open Source",
        "price_detail": "100% Free under Apache / JetBrains Community base.",
        "pros": [
            "Official IDE for Android with Jetpack Compose preview rendering",
            "Comprehensive Android Emulator and APK/AAB analyzer",
            "Built-in Gemini AI assistant for Android code generation",
            "Powerful Gradle build tool system integration"
        ],
        "cons": [
            "Very high system resource usage (16GB RAM minimum recommended)",
            "Gradle syncs can be slow on large multi-module projects",
            "Emulator requires hardware virtualization support"
        ],
        "best_for": "Android app developers building native Kotlin or Java applications."
    }
]

def load_history(history_path: str) -> list[str]:
    if os.path.exists(history_path):
        try:
            with open(history_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data.get("covered_ide_ids", [])
        except Exception:
            return []
    return []

def save_history(history_path: str, covered_ids: list[str]) -> None:
    os.makedirs(os.path.dirname(history_path), exist_ok=True)
    with open(history_path, "w", encoding="utf-8") as f:
        json.dump({"covered_ide_ids": covered_ids, "last_updated": datetime.now(timezone.utc).isoformat()}, f, indent=2)

def select_daily_ides(history_path: str, count: int = 3) -> list[dict]:
    covered = load_history(history_path)
    available = [ide for ide in IDE_DATABASE if ide["id"] not in covered]

    # Reset history if pool is exhausted
    if len(available) < count:
        covered = []
        available = IDE_DATABASE[:]

    selected = available[:count]
    new_covered = covered + [ide["id"] for ide in selected]
    save_history(history_path, new_covered)
    return selected

def generate_amp_blog_post(ide: dict) -> str:
    pros_li = "\n".join([f"      <li>{p}</li>" for p in ide["pros"]])
    cons_li = "\n".join([f"      <li>{c}</li>" for c in ide["cons"]])

    html = f"""<!doctype html>
<html ⚡ lang="en">
<head>
  <meta charset="utf-8">
  <title>{ide['name']} Review & Developer Guide - IDE Guide</title>
  <link rel="canonical" href="https://ideguide.blogspot.com/reviews/{ide['id']}.html">
  <meta name="viewport" content="width=device-width,minimum-scale=1,initial-scale=1">
  <script async src="https://cdn.ampproject.org/v0.js"></script>
  <style amp-boilerplate>body{{-webkit-animation:-amp-start 8s steps(1,end) 0s 1 normal both;-moz-animation:-amp-start 8s steps(1,end) 0s 1 normal both;-ms-animation:-amp-start 8s steps(1,end) 0s 1 normal both;animation:-amp-start 8s steps(1,end) 0s 1 normal both}}@-webkit-keyframes -amp-start{{from{{visibility:hidden}}to{{visibility:visible}}}}@-moz-keyframes -amp-start{{from{{visibility:hidden}}to{{visibility:visible}}}}@-ms-keyframes -amp-start{{from{{visibility:hidden}}to{{visibility:visible}}}}@keyframes -amp-start{{from{{visibility:hidden}}to{{visibility:visible}}}}</style><noscript><style amp-boilerplate>body{{-webkit-animation:none;-moz-animation:none;-ms-animation:none;animation:none}}</style></noscript>
  <style amp-custom>
    body {{
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
      line-height: 1.6;
      color: #1a1a1a;
      background-color: #f8f9fa;
      margin: 0;
      padding: 16px;
    }}
    header {{
      background: #0f172a;
      color: #ffffff;
      padding: 20px;
      border-radius: 8px;
      margin-bottom: 24px;
    }}
    h1 {{
      font-size: 1.8rem;
      margin: 0 0 8px 0;
    }}
    .badge {{
      display: inline-block;
      background: #00f0ff;
      color: #0f172a;
      padding: 4px 10px;
      font-size: 0.85rem;
      font-weight: bold;
      border-radius: 4px;
    }}
    .section-card {{
      background: #ffffff;
      padding: 20px;
      border-radius: 8px;
      margin-bottom: 20px;
      box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }}
    .pros {{ border-left: 5px solid #10b981; }}
    .cons {{ border-left: 5px solid #ef4444; }}
    .pricing {{ border-left: 5px solid #3b82f6; }}
    .verdict {{ border-left: 5px solid #8b5cf6; }}
    h2 {{ font-size: 1.3rem; margin-top: 0; }}
    ul {{ padding-left: 20px; }}
    .disclaimer {{
      font-size: 0.85rem;
      color: #64748b;
      background: #e2e8f0;
      padding: 12px;
      border-radius: 6px;
      margin-top: 30px;
    }}
  </style>
</head>
<body>
  <header>
    <span class="badge">{ide['category']}</span>
    <h1>{ide['name']}: Complete Developer Overview</h1>
    <p>In-depth breakdown of features, pros, cons, pricing, and workflow recommendations from IDE Guide.</p>
  </header>

  <article>
    <div class="section-card pros">
      <h2>The Good (Key Advantages)</h2>
      <ul>
{pros_li}
      </ul>
    </div>

    <div class="section-card cons">
      <h2>The Bad (Drawbacks & Limitations)</h2>
      <ul>
{cons_li}
      </ul>
    </div>

    <div class="section-card pricing">
      <h2>Pricing Model & License</h2>
      <p><strong>Category:</strong> {ide['pricing_type']}</p>
      <p>{ide['price_detail']}</p>
    </div>

    <div class="section-card verdict">
      <h2>Verdict: Is {ide['name']} Best for You?</h2>
      <p>{ide['best_for']}</p>
    </div>
  </article>

  <div class="disclaimer">
    {DISCLAIMER_TEXT}
  </div>
</body>
</html>"""
    return html

def generate_google_flow_spec(ide: dict) -> dict:
    return {
        "title": f"{ide['name']} - Pros, Cons & Pricing Breakdown | IDE Guide",
        "target_channel": "@IDEguide",
        "formats": ["YouTube Shorts (9:16)", "YouTube Video (16:9)"],
        "ide_metadata": {
            "id": ide["id"],
            "name": ide["name"],
            "category": ide["category"],
            "pricing_type": ide["pricing_type"]
        },
        "flow_visual_prompts": [
            {
                "scene": 1,
                "name": "Hook & Overview",
                "duration_seconds": 5,
                "visual_prompt": f"Cinematic 4K dolly shot of modern dark-mode desk setup showing {ide['name']} code editor on ultra-wide monitor with ambient neon purple and cyan LED backlight, sleek developer vibe, sharp focus.",
                "voiceover_script": f"Is {ide['name']} the best {ide['category']} for your coding setup today? Let's break down the good, the bad, and the pricing in 60 seconds!"
            },
            {
                "scene": 2,
                "name": "The Good (Pros)",
                "duration_seconds": 15,
                "visual_prompt": f"Macro close-up screen recording effect of {ide['name']} showcasing fast code completion, smooth syntax highlighting, and instant response. Modern high-tech UI graphic overlays.",
                "voiceover_script": f"First, the good: {ide['pros'][0]}. Plus, {ide['pros'][1]}."
            },
            {
                "scene": 3,
                "name": "The Bad (Cons)",
                "duration_seconds": 15,
                "visual_prompt": f"Split contrast screen animation with high-tech red glow warning indicator highlighting drawbacks of {ide['name']}, fast camera pan across workspace.",
                "voiceover_script": f"On the downside: {ide['cons'][0]}. Keep in mind that {ide['cons'][1]}."
            },
            {
                "scene": 4,
                "name": "Pricing & Verdict",
                "duration_seconds": 15,
                "visual_prompt": f"Dynamic graphic card animated in 3D displaying '{ide['pricing_type'].upper()}' price tag and key recommendation badge, transitioning to IDE Guide YouTube subscribe button.",
                "voiceover_script": f"Pricing model is {ide['pricing_type']}. {ide['price_detail']} Final verdict: {ide['best_for']}"
            }
        ],
        "disclaimer": DISCLAIMER_TEXT
    }

def main():
    date_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    output_dir = os.path.join("content", date_str)
    os.makedirs(output_dir, exist_ok=True)
    history_path = os.path.join("content", "history.json")

    selected_ides = select_daily_ides(history_path, count=3)

    for i, ide in enumerate(selected_ides, 1):
        # Blog post
        blog_html = generate_amp_blog_post(ide)
        blog_file = os.path.join(output_dir, f"post_{i}_{ide['id']}.amp.html")
        with open(blog_file, "w", encoding="utf-8") as f:
            f.write(blog_html)

        # Video flow spec
        flow_spec = generate_google_flow_spec(ide)
        spec_file = os.path.join(output_dir, f"video_flow_{i}_{ide['id']}.json")
        with open(spec_file, "w", encoding="utf-8") as f:
            json.dump(flow_spec, f, indent=2)

    print(f"Successfully generated 3 daily content packages in {output_dir}")

if __name__ == "__main__":
    main()
