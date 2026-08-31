#!/usr/bin/env python3
"""
Daily Content Generator for IDE Guide (https://ideguide.blogspot.com/ & https://www.youtube.com/@IDEguide)

Generates 3 AMP-compliant HTML blog posts for Blogger and 3 Google Flow visual video
specification JSON files for YouTube videos/shorts per day.

Tracks covered IDEs in content/history.json to prevent duplicate coverage.
"""

import json
import os
import sys
import datetime
import urllib.request
import urllib.parse
from typing import List, Dict, Any

DISCLAIMER_TEXT = (
    "Disclaimer: IDE Guide is an independent technical publication. This content is "
    "not sponsored, endorsed, or affiliated with any software vendor or editor developer "
    "mentioned above. All reviews and assessments are based strictly on objective developer evaluation."
)

CURATED_IDE_CATALOG: List[Dict[str, Any]] = [
    {
        "name": "Visual Studio Code",
        "slug": "vscode",
        "category": "General Purpose / Extensible Editor",
        "pricing_tier": "Free / Open Source (Core)",
        "pricing_details": "Free open-source core (VSCodium) and free binary distribution by Microsoft.",
        "pros": [
            "Extensive ecosystem with thousands of extensions",
            "Built-in Git integration and terminal",
            "Powerful remote development capabilities (SSH, Containers, WSL)",
            "Active community and frequent monthly updates"
        ],
        "cons": [
            "Can consume significant RAM with many extensions loaded",
            "Electron-based rendering can feel slightly heavier than native C/Rust editors"
        ],
        "best_for": "Web developers, Python programmers, cloud engineers, and multi-language developers.",
        "verdict": "The undisputed gold standard for modular, extension-driven development."
    },
    {
        "name": "Cursor",
        "slug": "cursor",
        "category": "AI-Native Code Editor",
        "pricing_tier": "Freemium",
        "pricing_details": "Free tier with monthly query limits; Pro tier at $20/month for unlimited fast AI requests.",
        "pros": [
            "Deep codebase-indexing AI chat and inline editing (Cmd+K)",
            "Seamless 1-click import of VS Code settings and extensions",
            "Multi-file editing capabilities with AI Agent mode"
        ],
        "cons": [
            "Requires active internet connection for proprietary AI features",
            "Paid subscription required for heavy power users"
        ],
        "best_for": "Developers looking for cutting-edge AI-assisted pair programming and rapid code generation.",
        "verdict": "The premier AI-first code editor redefining modern software development workflows."
    },
    {
        "name": "Zed",
        "slug": "zed",
        "category": "High-Performance Native Code Editor",
        "pricing_tier": "Free / Open Source",
        "pricing_details": "Free and open-source editor core; optional team collaboration features.",
        "pros": [
            "Blazing fast performance powered by GPU rendering (GPUI) and Rust",
            "Extremely low memory footprint and instantaneous file loading",
            "Built-in multiplayer real-time collaborative editing"
        ],
        "cons": [
            "Smaller extension catalog compared to VS Code",
            "Linux and Windows support is newer compared to macOS build"
        ],
        "best_for": "Systems programmers, Rust/C++ developers, and speed enthusiasts who demand instant response.",
        "verdict": "A modern performance marvel built from scratch in Rust."
    },
    {
        "name": "PyCharm",
        "slug": "pycharm",
        "category": "Python Dedicated IDE",
        "pricing_tier": "Freemium",
        "pricing_details": "Free Community Edition (open source); Professional Edition starting at $249/year.",
        "pros": [
            "Unrivaled intelligent Python code analysis, refactoring, and linting",
            "Deep integration with Django, Flask, FastAPI, and data science toolkits",
            "Powerful database management tools built into Professional edition"
        ],
        "cons": [
            "High memory usage during index building",
            "Commercial features locked behind subscription"
        ],
        "best_for": "Python developers, data engineers, and web framework specialists.",
        "verdict": "The ultimate full-featured IDE for professional Python engineering."
    },
    {
        "name": "Neovim",
        "slug": "neovim",
        "category": "Modal Terminal-Based Text Editor",
        "pricing_tier": "Free / Open Source",
        "pricing_details": "100% free and open-source under Apache and Vim licenses.",
        "pros": [
            "Ultra-lightweight with zero GUI overhead",
            "Extensible via Lua with full Language Server Protocol (LSP) support",
            "Lightning fast keyboard navigation and modal editing workflow"
        ],
        "cons": [
            "Steep learning curve for Vim keybindings and Lua configuration",
            "Requires time investment to build a tailored development environment"
        ],
        "best_for": "Terminal enthusiasts, CLI power users, and keyboard-driven developers.",
        "verdict": "The supreme modal editor for maximum efficiency and total environment control."
    },
    {
        "name": "IntelliJ IDEA",
        "slug": "intellij-idea",
        "category": "Java & JVM Polyglot IDE",
        "pricing_tier": "Freemium",
        "pricing_details": "Free Community Edition; Ultimate Edition starting at $599/year.",
        "pros": [
            "Industry-leading Java, Kotlin, and Scala static analysis and code refactoring",
            "Comprehensive Spring Framework, Maven, and Gradle integration",
            "Built-in profiling, decompiler, and enterprise tools"
        ],
        "cons": [
            "Requires substantial RAM (4GB+ allocated heap recommended)",
            "Slower initial startup and project indexing"
        ],
        "best_for": "Enterprise Java developers, Kotlin Android backends, and JVM ecosystem engineers.",
        "verdict": "The gold standard IDE for enterprise Java and Kotlin application development."
    },
    {
        "name": "Sublime Text 4",
        "slug": "sublime-text",
        "category": "Lightweight GUI Code Editor",
        "pricing_tier": "Paid / Free Evaluation",
        "pricing_details": "Free evaluation without hard time limit; individual license $99.",
        "pros": [
            "Instant startup and rapid file switching across massive projects",
            "GPU accelerated rendering engine for smooth scrolling",
            "Minimalist clean UI with powerful multi-cursor capabilities"
        ],
        "cons": [
            "Requires plugin setup for full IDE features like debugging",
            "Commercial license notification popups during evaluation"
        ],
        "best_for": "Developers who prioritize raw editor speed, minimal UI distractions, and low resource consumption.",
        "verdict": "The quintessential super-fast lightweight editor that remains timelessly reliable."
    },
    {
        "name": "WebStorm",
        "slug": "webstorm",
        "category": "JavaScript & TypeScript IDE",
        "pricing_tier": "Paid",
        "pricing_details": "Commercial license starting at $69/year for individuals.",
        "pros": [
            "Deep, out-of-the-box support for React, Vue, Angular, Next.js, and Node.js",
            "Advanced TypeScript type checking, refactoring, and auto-imports",
            "Integrated unit testing, debugging, and Git tools without configuration"
        ],
        "cons": [
            "No dedicated free tier (30-day trial only)",
            "Higher memory footprint than plain text editors"
        ],
        "best_for": "Full-stack JavaScript/TypeScript engineers and frontend framework specialists.",
        "verdict": "The most intelligent out-of-the-box IDE for complex frontend and Node.js ecosystems."
    },
    {
        "name": "Helix",
        "slug": "helix",
        "category": "Post-Modern Modal Terminal Editor",
        "pricing_tier": "Free / Open Source",
        "pricing_details": "100% free and open-source (MPL-2.0 license).",
        "pros": [
            "Zero-configuration LSP support out of the box",
            "Built in Rust with selection-first modal editing (Kakoune-inspired)",
            "Tree-sitter integration for precise syntax highlighting and structural editing"
        ],
        "cons": [
            "Plugin system still under active development",
            "Keybindings differ slightly from traditional Vim"
        ],
        "best_for": "Developers wanting Neovim-like terminal speed without managing endless plugins.",
        "verdict": "The modern modal editor that delivers out-of-the-box LSP power in the terminal."
    }
]


def load_history(history_filepath: str) -> List[str]:
    """Load list of previously generated IDE slugs."""
    if os.path.exists(history_filepath):
        try:
            with open(history_filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get("covered_slugs", [])
        except Exception as e:
            print(f"Warning: Failed to load history ({e}), starting fresh.")
    return []


def save_history(history_filepath: str, covered_slugs: List[str]):
    """Save updated list of covered IDE slugs to history.json."""
    os.makedirs(os.path.dirname(history_filepath), exist_ok=True)
    with open(history_filepath, 'w', encoding='utf-8') as f:
        json.dump({
            "updated_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "total_covered": len(covered_slugs),
            "covered_slugs": covered_slugs
        }, f, indent=2)


def discover_ides_from_github(count: int = 3) -> List[Dict[str, Any]]:
    """
    Attempt to fetch trending IDE repositories from GitHub Search API.
    Returns fallback curated IDEs if network request fails or returns insufficient results.
    """
    url = "https://api.github.com/search/repositories?q=topic:ide+topic:editor&sort=stars&order=desc"
    req = urllib.request.Request(url, headers={"User-Agent": "IDE-Guide-Bot/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=5) as response:
            if response.status == 200:
                data = json.loads(response.read().decode('utf-8'))
                discovered = []
                for item in data.get("items", []):
                    name = item.get("name", "")
                    desc = item.get("description", "") or "A modern code editor environment."
                    slug = name.lower().replace(".", "-").replace(" ", "-")
                    discovered.append({
                        "name": name.capitalize(),
                        "slug": slug,
                        "category": "Community Code Editor / IDE",
                        "pricing_tier": "Free / Open Source",
                        "pricing_details": f"Open source repository: {item.get('html_url', '')}",
                        "pros": [
                            f"Stars on GitHub: {item.get('stargazers_count', 0):,}",
                            "Open-source community driven development",
                            "Transparent source code and issue tracker"
                        ],
                        "cons": [
                            "May require building from source or experimental setup",
                            "Ecosystem size depends on community contributions"
                        ],
                        "best_for": desc,
                        "verdict": f"{name} offers an open, community-driven approach to modern editing."
                    })
                    if len(discovered) >= count:
                        break
                if len(discovered) >= count:
                    return discovered
    except Exception as e:
        print(f"GitHub discovery fallback notice ({e}). Using curated catalog.")
    return CURATED_IDE_CATALOG


def generate_amp_html(ide: Dict[str, Any], date_str: str) -> str:
    """Generate AMP HTML compliant blog post strictly formatted for Blogger."""
    pros_html = "".join([f"<li>✅ <strong>{p}</strong></li>" for p in ide["pros"]])
    cons_html = "".join([f"<li>❌ <strong>{c}</strong></li>" for c in ide["cons"]])

    amp_html = f"""<!doctype html>
<html ⚡ lang="en">
<head>
  <meta charset="utf-8">
  <script async src="https://cdn.ampproject.org/v0.js"></script>
  <title>IDE Guide Review: {ide['name']} ({date_str})</title>
  <link rel="canonical" href="https://ideguide.blogspot.com/{date_str}/{ide['slug']}.html">
  <meta name="viewport" content="width=device-width,minimum-scale=1,initial-scale=1">
  <style amp-boilerplate>body{{-webkit-animation:-amp-start 8s steps(1,end) 0s 1 normal both;-moz-animation:-amp-start 8s steps(1,end) 0s 1 normal both;-ms-animation:-amp-start 8s steps(1,end) 0s 1 normal both;animation:-amp-start 8s steps(1,end) 0s 1 normal both}}@-webkit-keyframes -amp-start{{from{{visibility:hidden}}to{{visibility:visible}}}}@-moz-keyframes -amp-start{{from{{visibility:hidden}}to{{visibility:visible}}}}@-ms-keyframes -amp-start{{from{{visibility:hidden}}to{{visibility:visible}}}}@-o-keyframes -amp-start{{from{{visibility:hidden}}to{{visibility:visible}}}}@keyframes -amp-start{{from{{visibility:hidden}}to{{visibility:visible}}}}</style><noscript><style amp-boilerplate>body{{-webkit-animation:none;-moz-animation:none;-ms-animation:none;animation:none}}</style></noscript>
  <style amp-custom>
    body {{
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
      line-height: 1.6;
      color: #1e293b;
      background-color: #f8fafc;
      padding: 0;
      margin: 0;
    }}
    header {{
      background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
      color: #ffffff;
      padding: 2.5rem 1.5rem;
      text-align: center;
    }}
    header h1 {{
      margin: 0 0 0.5rem 0;
      font-size: 2rem;
      font-weight: 800;
      color: #38bdf8;
    }}
    header p {{
      margin: 0;
      color: #94a3b8;
      font-size: 1.1rem;
    }}
    .container {{
      max-width: 800px;
      margin: 2rem auto;
      padding: 0 1.5rem;
    }}
    .card {{
      background: #ffffff;
      border-radius: 12px;
      padding: 1.75rem;
      margin-bottom: 1.5rem;
      box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
    }}
    .badge {{
      display: inline-block;
      padding: 0.25rem 0.75rem;
      border-radius: 9999px;
      font-size: 0.875rem;
      font-weight: 600;
      background-color: #e0f2fe;
      color: #0369a1;
      margin-bottom: 1rem;
    }}
    h2 {{
      color: #0f172a;
      border-bottom: 2px solid #e2e8f0;
      padding-bottom: 0.5rem;
      margin-top: 0;
    }}
    ul {{
      padding-left: 1.25rem;
    }}
    li {{
      margin-bottom: 0.5rem;
    }}
    .pricing-box {{
      background-color: #f0fdf4;
      border-left: 4px solid #22c55e;
      padding: 1rem;
      margin: 1rem 0;
      border-radius: 0 8px 8px 0;
    }}
    .disclaimer-box {{
      background-color: #fffbeb;
      border: 1px solid #fde68a;
      border-radius: 8px;
      padding: 1rem;
      font-size: 0.875rem;
      color: #92400e;
      margin-top: 2rem;
      text-align: center;
    }}
    footer {{
      text-align: center;
      padding: 2rem;
      color: #64748b;
      font-size: 0.875rem;
    }}
    footer a {{
      color: #0284c7;
      text-decoration: none;
    }}
  </style>
</head>
<body>
  <header>
    <h1>IDE Guide: {ide['name']} Evaluation</h1>
    <p>Comprehensive Developer Breakdown & Feature Analysis</p>
  </header>

  <div class="container">
    <div class="card">
      <span class="badge">{ide['category']}</span>
      <h2>Overview</h2>
      <p>Welcome to <strong>IDE Guide</strong>. Today we are conducting an in-depth evaluation of <strong>{ide['name']}</strong>. Whether you are building web apps, systems tools, or AI models, selecting the optimal development environment directly impacts productivity and code quality.</p>
    </div>

    <div class="card pricing-box">
      <h2>Pricing Model & License</h2>
      <p><strong>Tier:</strong> {ide['pricing_tier']}</p>
      <p>{ide['pricing_details']}</p>
    </div>

    <div class="card">
      <h2>Pros & Strengths</h2>
      <ul>
        {pros_html}
      </ul>
    </div>

    <div class="card">
      <h2>Cons & Considerations</h2>
      <ul>
        {cons_html}
      </ul>
    </div>

    <div class="card">
      <h2>Target Use Case & Verdict</h2>
      <p><strong>Best For:</strong> {ide['best_for']}</p>
      <p><strong>Final Verdict:</strong> {ide['verdict']}</p>
    </div>

    <div class="disclaimer-box">
      <p><strong>Independent Publication Notice</strong></p>
      <p>{DISCLAIMER_TEXT}</p>
    </div>
  </div>

  <footer>
    <p>Published by <a href="https://ideguide.blogspot.com/" target="_blank">IDE Guide Blog</a> | Watch our video reviews on <a href="https://www.youtube.com/@IDEguide" target="_blank">YouTube @IDEguide</a></p>
  </footer>
</body>
</html>
"""
    return amp_html


def generate_google_flow_video_spec(ide: Dict[str, Any], date_str: str, is_short: bool = False) -> Dict[str, Any]:
    """Generate visual video specification JSON compatible with Google Flow AI visual pipelines."""
    fmt = "shorts" if is_short else "long_form"
    aspect = "9:16" if is_short else "16:9"

    scenes = [
        {
          "scene_number": 1,
          "duration_seconds": 5,
          "title": "Hook & IDE Showcase",
          "narration_script": f"Is {ide['name']} the best code editor for your developer workflow in 2026? Let's break down the pros, cons, and pricing!",
          "visual_prompt": f"Cinematic macro close-up shot of a dark-mode code editor interface showing syntax-highlighted code for {ide['name']}. Smooth camera push-in towards the cursor blinking on line 12. Soft blue LED backlight reflecting on mechanical keycaps.",
          "camera_angle": "45-degree macro close-up, slow steady zoom-in",
          "lighting": "Low key ambient room lighting, cyan accent backlight (5600K key light on keyboard)"
        },
        {
          "scene_number": 2,
          "duration_seconds": 15,
          "title": "Core Strengths & Pros",
          "narration_script": f"Here is what makes {ide['name']} stand out: {', '.join(ide['pros'][:2])}.",
          "visual_prompt": f"High-speed screencast style visualization of {ide['name']} displaying file tree navigation, fast auto-complete popups, and instant split-pane window layout. Smooth visual transition between editor panels.",
          "camera_angle": "Direct eye-level screen perspective, slight tilt shift depth-of-field",
          "lighting": "High clarity digital screen illumination"
        },
        {
          "scene_number": 3,
          "duration_seconds": 15,
          "title": "Cons & Tradeoffs",
          "narration_script": f"However, keep in mind: {', '.join(ide['cons'])}.",
          "visual_prompt": "Cinematic shot of system resource monitor graphs showing memory allocation alongside editor configuration windows, highlighted with modern warning badges and crisp typography overlay.",
          "camera_angle": "Over-the-shoulder view of developer setup, warm ambient lighting",
          "lighting": "Cool color tone temperature (4000K)"
        },
        {
          "scene_number": 4,
          "duration_seconds": 15,
          "title": "Pricing & Recommendation",
          "narration_script": f"Pricing tier: {ide['pricing_tier']}. Best suited for {ide['best_for']} {ide['verdict']}",
          "visual_prompt": f"Split screen score graphic displaying {ide['pricing_tier']} badge on the left, and a sleek summary rating card for {ide['name']} on the right with subscribe button animation.",
          "camera_angle": "Centered graphics card layout, dynamic motion graphics pop",
          "lighting": "Bright studio graphics lighting"
        },
        {
          "scene_number": 5,
          "duration_seconds": 5,
          "title": "Outro & Independent Disclaimer",
          "narration_script": "Subscribe to IDE Guide on YouTube and visit ideguide.blogspot.com for daily technical editor reviews!",
          "visual_prompt": "Elegant ending title card displaying IDE Guide logo, YouTube channel link (@IDEguide), and Blogger website URL with soft animated particle background.",
          "camera_angle": "Static front view",
          "lighting": "Balanced neutral studio light"
        }
    ]

    return {
        "channel": "IDE Guide (@IDEguide)",
        "date": date_str,
        "ide_name": ide["name"],
        "ide_slug": ide["slug"],
        "format": fmt,
        "aspect_ratio": aspect,
        "title": f"IDE Guide Review: {ide['name']} ({'Shorts' if is_short else 'Full Review'})",
        "pricing": {
            "tier": ide["pricing_tier"],
            "details": ide["pricing_details"]
        },
        "recommendation": {
            "best_for": ide["best_for"],
            "verdict": ide["verdict"]
        },
        "disclaimer": DISCLAIMER_TEXT,
        "google_flow_settings": {
            "model_target": "Google Flow / Veo 2",
            "frame_rate": 30,
            "resolution": "1080x1920" if is_short else "1920x1080",
            "style_preset": "Cinematic Tech Review / Developer Dark Mode"
        },
        "scenes": scenes
    }


def run_daily_generation(output_root: str = "content", target_date: str = None) -> List[str]:
    """
    Generate daily batch of 3 AMP blog posts and 3 Google Flow video specs.
    Returns list of generated directory paths.
    """
    if not target_date:
        target_date = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d")

    date_dir = os.path.join(output_root, target_date)
    os.makedirs(date_dir, exist_ok=True)

    history_filepath = os.path.join(output_root, "history.json")
    covered_slugs = load_history(history_filepath)

    # Filter candidates out of history
    available_ides = [ide for ide in CURATED_IDE_CATALOG if ide["slug"] not in covered_slugs]
    if len(available_ides) < 3:
        # Try dynamic discovery
        discovered = discover_ides_from_github(count=3)
        for disc in discovered:
            if disc["slug"] not in covered_slugs and disc not in available_ides:
                available_ides.append(disc)

    if len(available_ides) < 3:
        # Reset covered history if exhausted
        print("Notice: Covered catalog exhausted. Re-cycling IDE catalog.")
        covered_slugs = []
        available_ides = list(CURATED_IDE_CATALOG)

    selected_ides = available_ides[:3]
    generated_dirs = []

    for idx, ide in enumerate(selected_ides, start=1):
        item_dir = os.path.join(date_dir, f"post_{idx}_{ide['slug']}")
        os.makedirs(item_dir, exist_ok=True)

        # 1. AMP HTML Post for Blogger
        amp_content = generate_amp_html(ide, target_date)
        amp_path = os.path.join(item_dir, "blog_post_amp.html")
        with open(amp_path, "w", encoding="utf-8") as f:
            f.write(amp_content)

        # 2. Google Flow Video Spec for YouTube
        is_short = (idx == 3) # 2 long form videos, 1 Short per day
        video_spec = generate_google_flow_video_spec(ide, target_date, is_short=is_short)
        spec_path = os.path.join(item_dir, "google_flow_video_spec.json")
        with open(spec_path, "w", encoding="utf-8") as f:
            json.dump(video_spec, f, indent=2)

        covered_slugs.append(ide["slug"])
        generated_dirs.append(item_dir)

    save_history(history_filepath, covered_slugs)
    print(f"Successfully generated 3 daily content packages for {target_date} in {date_dir}")
    return generated_dirs


if __name__ == "__main__":
    run_daily_generation()
