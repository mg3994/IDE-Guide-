#!/usr/bin/env python3
"""
Daily Content Package Generator for IDE Guide.
Generates 3 AMP HTML blog posts and 3 Google Flow video specifications daily.
"""

import os
import json
import yaml
from datetime import datetime, timezone
from scripts.amp_validator import REQUIRED_DISCLAIMER

IDE_CATALOG = [
    {
        "name": "Visual Studio Code",
        "slug": "vs-code",
        "pricing": "Free / Open Source",
        "category": "General Purpose / Web",
        "pros": ["Massive extension marketplace", "Built-in Git and terminal", "Flexible AI integration"],
        "cons": ["High RAM consumption on monorepos", "Telemetry enabled by default"],
        "verdict": "Best overall free code editor for modern web and cloud development."
    },
    {
        "name": "Cursor",
        "slug": "cursor",
        "pricing": "Freemium ($20/mo Pro)",
        "category": "AI-First IDE",
        "pros": ["Deep AI code generation & editing", "Forked from VS Code (supports extensions)", "Multi-file prompt context"],
        "cons": ["Requires subscription for unlimited AI queries", "Dependent on third-party cloud models"],
        "verdict": "The top choice for developers seeking ultra-fast AI-assisted software building."
    },
    {
        "name": "JetBrains PyCharm",
        "slug": "pycharm",
        "pricing": "Freemium / Paid ($249/yr Professional)",
        "category": "Python / Data Science",
        "pros": ["Intelligent refactoring and code navigation", "Deep Django and database integration", "Built-in visual debugger"],
        "cons": ["Heavy memory footprint", "Slower startup times on older hardware"],
        "verdict": "Unrivaled IDE for professional Python backend and data engineering teams."
    },
    {
        "name": "Neovim",
        "slug": "neovim",
        "pricing": "Free / Open Source",
        "category": "Terminal / Modal Editor",
        "pros": ["Blazing fast performance", "Endlessly customizable via Lua", "Extremely low RAM footprint"],
        "cons": ["Steep learning curve", "Requires manual configuration for full IDE features"],
        "verdict": "Ideal for keyboard-driven power users and developers who demand peak speed."
    },
    {
        "name": "Zed",
        "slug": "zed",
        "pricing": "Free / Open Source",
        "category": "High-Performance Native IDE",
        "pros": ["Written in Rust for GPU-accelerated rendering", "Native multi-user collaboration", "Ultra-responsive typing"],
        "cons": ["Ecosystem extensions still maturing", "Limited multi-language features compared to VS Code"],
        "verdict": "The fastest rising next-gen editor for Rust, Go, and high-speed web dev."
    },
    {
        "name": "Sublime Text 4",
        "slug": "sublime-text-4",
        "pricing": "Paid ($99 one-time)",
        "category": "Lightweight Text / Code Editor",
        "pros": ["Instant load times", "Smooth GPU rendering", "Minimal resource consumption"],
        "cons": ["Paid license required for continuous pop-up free use", "Smaller AI plugin ecosystem"],
        "verdict": "Excellent lightweight choice for developers who want instantaneous responsiveness."
    },
    {
        "name": "JetBrains IntelliJ IDEA",
        "slug": "intellij-idea",
        "pricing": "Freemium / Paid ($599/yr Enterprise)",
        "category": "Java / Kotlin / Enterprise",
        "pros": ["Best-in-class Java static analysis", "Robust build tool integration (Maven/Gradle)", "Exceptional refactoring"],
        "cons": ["Resource intensive", "Paid for full Enterprise features"],
        "verdict": "The undisputed benchmark for Java, Kotlin, and enterprise backend engineering."
    },
    {
        "name": "Windsurf",
        "slug": "windsurf",
        "pricing": "Freemium ($15/mo Pro)",
        "category": "AI Agentic IDE",
        "pros": ["Cascade AI flows for multi-file generation", "Seamless terminal execution", "Smooth codebase context sync"],
        "cons": ["Pro subscription needed for high usage", "Newer ecosystem"],
        "verdict": "Powerful agentic IDE for developers leveraging AI workflow automation."
    },
    {
        "name": "Fleet",
        "slug": "fleet",
        "pricing": "Freemium",
        "category": "Polyglot Lightweight IDE",
        "pros": ["Smart mode toggle", "Lightweight startup", "JetBrains smart engine integration"],
        "cons": ["Preview stage features", "Plugin catalog growing"],
        "verdict": "Promising polyglot editor bridging lightweight text editing and full IDE power."
    }
]

HISTORY_FILE = "content/history.json"

def load_history() -> list[str]:
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []
    return []

def save_history(covered_slugs: list[str]):
    os.makedirs(os.path.dirname(HISTORY_FILE), exist_ok=True)
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(covered_slugs, f, indent=2)

def select_daily_ides(count: int = 3) -> list[dict]:
    history = load_history()
    available = [ide for ide in IDE_CATALOG if ide["slug"] not in history]

    # If exhausted, reset history cycle
    if len(available) < count:
        history = []
        available = IDE_CATALOG.copy()

    selected = available[:count]
    updated_history = history + [ide["slug"] for ide in selected]
    save_history(updated_history)
    return selected

def build_amp_html(ide: dict) -> str:
    pricing_badge_class = "badge-free" if "Free" in ide["pricing"] else "badge-paid"
    pros_html = "".join(f"<li>{p}</li>" for p in ide["pros"])
    cons_html = "".join(f"<li>{c}</li>" for c in ide["cons"])

    return f"""<!doctype html>
<html ⚡ lang="en">
<head>
  <meta charset="utf-8">
  <script async src="https://cdn.ampproject.org/v0.js"></script>
  <title>{ide['name']} Review & Complete Developer Guide - IDE Guide</title>
  <link rel="canonical" href="https://ideguide.blogspot.com/{ide['slug']}-review.html">
  <meta name="viewport" content="width=device-width,minimum-scale=1,initial-scale=1">
  <style amp-boilerplate>body{{-webkit-animation:-amp-start 8s steps(1,end) 0s 1 normal both;-moz-animation:-amp-start 8s steps(1,end) 0s 1 normal both;-ms-animation:-amp-start 8s steps(1,end) 0s 1 normal both;animation:-amp-start 8s steps(1,end) 0s 1 normal both}}@-webkit-keyframes -amp-start{{from{{visibility:hidden}}to{{visibility:visible}}}}@-moz-keyframes -amp-start{{from{{visibility:hidden}}to{{visibility:visible}}}}@-ms-keyframes -amp-start{{from{{visibility:hidden}}to{{visibility:visible}}}}@-o-keyframes -amp-start{{from{{visibility:hidden}}to{{visibility:visible}}}}@keyframes -amp-start{{from{{visibility:hidden}}to{{visibility:visible}}}}</style><noscript><style amp-boilerplate>body{{-webkit-animation:none;-moz-animation:none;-ms-animation:none;animation:none}}</style></noscript>
  <style amp-custom>
    body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; line-height: 1.6; color: #1e293b; padding: 20px; max-width: 800px; margin: 0 auto; }}
    h1 {{ color: #0f172a; border-bottom: 2px solid #e2e8f0; padding-bottom: 10px; }}
    h2 {{ color: #1e293b; margin-top: 24px; }}
    .badge-free {{ background: #10b981; color: white; padding: 4px 10px; border-radius: 4px; font-weight: bold; display: inline-block; }}
    .badge-paid {{ background: #f59e0b; color: white; padding: 4px 10px; border-radius: 4px; font-weight: bold; display: inline-block; }}
    .pros-cons {{ display: flex; gap: 16px; margin: 20px 0; }}
    .pros {{ flex: 1; background: #f0fdf4; border: 1px solid #bbf7d0; padding: 16px; border-radius: 8px; }}
    .cons {{ flex: 1; background: #fef2f2; border: 1px solid #fecaca; padding: 16px; border-radius: 8px; }}
    .verdict {{ background: #eff6ff; border-left: 4px solid #3b82f6; padding: 16px; border-radius: 4px; margin: 20px 0; }}
    .disclaimer {{ background: #f8fafc; border-left: 4px solid #64748b; padding: 12px; margin-top: 32px; font-size: 0.9em; color: #475569; }}
  </style>
</head>
<body>
  <h1>{ide['name']} Review & Developer Guide</h1>
  <p><strong>Pricing Model:</strong> <span class="{pricing_badge_class}">{ide['pricing']}</span></p>
  <p><strong>Category:</strong> {ide['category']}</p>

  <amp-img src="https://images.unsplash.com/photo-1555066931-4365d14bab8c?w=800" width="800" height="450" layout="responsive" alt="{ide['name']} Code Editor Preview"></amp-img>

  <h2>Overview & Key Capabilities</h2>
  <p>{ide['name']} is a premier tool in the {ide['category']} space. Here is an in-depth breakdown of its performance, developer productivity features, pros, cons, and license breakdown.</p>

  <div class="pros-cons">
    <div class="pros">
      <h3>Pros</h3>
      <ul>
        {pros_html}
      </ul>
    </div>
    <div class="cons">
      <h3>Cons</h3>
      <ul>
        {cons_html}
      </ul>
    </div>
  </div>

  <h2>Pricing & Licensing Details</h2>
  <p>{ide['name']} operates under a <strong>{ide['pricing']}</strong> model. Make sure to choose the right plan based on your professional software engineering workflow requirements.</p>

  <div class="verdict">
    <h2>Final Verdict</h2>
    <p>{ide['verdict']}</p>
  </div>

  <div class="disclaimer">
    {REQUIRED_DISCLAIMER}
  </div>
</body>
</html>
"""

def build_google_flow_spec(ide: dict) -> dict:
    return {
        "meta": {
            "ide_name": ide["name"],
            "slug": ide["slug"],
            "pricing": ide["pricing"],
            "category": ide["category"],
            "video_type": "Short",
            "aspect_ratio": "9:16",
            "duration_seconds": 60,
            "target_channel": "YouTube @IDEguide"
        },
        "google_flow_prompts": [
            {
                "scene_id": 1,
                "timestamp": "00:00 - 00:05",
                "prompt": f"Cinematic ultra-HD vertical shot of {ide['name']} dark mode UI with glowing syntax highlighting, smooth camera zoom-in, 4K resolution, studio lighting.",
                "camera_movement": "Slow push-in zoom",
                "lighting": "Dark mode neon ambient backlight",
                "caption": f"Is {ide['name']} Right For You in 2026?"
            },
            {
                "scene_id": 2,
                "timestamp": "00:05 - 00:25",
                "prompt": f"Macro view of software engineer coding fast in {ide['name']} on dark mechanical keyboard, high frame rate.",
                "camera_movement": "Tracking pan left to right",
                "lighting": "Warm key light with dark background contrast",
                "caption": f"Top Feature: {ide['pros'][0]}"
            },
            {
                "scene_id": 3,
                "timestamp": "00:25 - 00:45",
                "prompt": f"Split screen high-tech dynamic graphic comparing {ide['name']} benchmark metrics.",
                "camera_movement": "Static center focus",
                "lighting": "Clean studio lighting",
                "caption": f"Watch Out: {ide['cons'][0]}"
            },
            {
                "scene_id": 4,
                "timestamp": "00:45 - 00:60",
                "prompt": f"Sleek studio setup showing dual vertical monitors, fading into IDE Guide brand end-screen.",
                "camera_movement": "Tilt overhead",
                "lighting": "Soft diffuse ambient",
                "caption": f"Verdict: {ide['verdict']}"
            }
        ],
        "script": {
            "voiceover_text": (
                f"Is {ide['name']} worth using? Let's break it down in 60 seconds! "
                f"Pricing: {ide['pricing']}. "
                f"Pros: {', '.join(ide['pros'])}. "
                f"Cons: {', '.join(ide['cons'])}. "
                f"Verdict: {ide['verdict']} "
                f"{REQUIRED_DISCLAIMER}"
            ),
            "disclaimer": REQUIRED_DISCLAIMER
        }
    }

def generate_daily_package(date_str: str = None) -> list[str]:
    if not date_str:
        date_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    out_dir = os.path.join("content", date_str)
    os.makedirs(out_dir, exist_ok=True)

    selected_ides = select_daily_ides(3)
    generated_files = []

    for idx, ide in enumerate(selected_ides, 1):
        # 1. Generate AMP HTML blog post
        amp_filename = f"post_{idx}_{ide['slug']}.html"
        amp_filepath = os.path.join(out_dir, amp_filename)
        amp_content = build_amp_html(ide)
        with open(amp_filepath, "w", encoding="utf-8") as f:
            f.write(amp_content)
        generated_files.append(amp_filepath)

        # 2. Generate Google Flow video spec
        spec_filename = f"video_{idx}_{ide['slug']}_spec.yaml"
        spec_filepath = os.path.join(out_dir, spec_filename)
        flow_spec = build_google_flow_spec(ide)
        with open(spec_filepath, "w", encoding="utf-8") as f:
            yaml.dump(flow_spec, f, sort_keys=False)
        generated_files.append(spec_filepath)

    return generated_files

def main():
    date_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    print(f"🚀 Generating Daily Content Package for {date_str}...")
    files = generate_daily_package(date_str)
    print(f"✅ Generated {len(files)} content files in content/{date_str}:")
    for f in files:
        print(f"  - {f}")

if __name__ == "__main__":
    main()
