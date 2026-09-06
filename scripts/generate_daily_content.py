#!/usr/bin/env python3
"""
Daily Content Generator for IDE Guide
Generates 3 AMP HTML blog posts (for Blogger https://ideguide.blogspot.com/)
and 3 Google Flow Video Specifications (for YouTube @IDEguide).
Tracks covered IDEs in content/history.json to avoid duplicates.
"""

import os
import json
import urllib.request
import urllib.error
from datetime import datetime, timezone

NON_SPONSORSHIP_DISCLAIMER = (
    "Disclaimer: IDE Guide is an independent technical publication. "
    "This content is not sponsored, endorsed, or affiliated with any software vendor or editor developer mentioned above. "
    "All reviews and assessments are based strictly on objective developer evaluation."
)

CURATED_IDES = [
    {
        "name": "Visual Studio Code",
        "description": "Extensible, lightweight open-source code editor developed by Microsoft.",
        "pricing": "Free / Open Source",
        "category": "General Code Editor",
        "pros": ["Massive extension ecosystem", "Integrated terminal and Git tools", "Lightning-fast performance"],
        "cons": ["High memory usage with heavy extensions", "Telemetry enabled by default"],
        "best_for": "Web development, Python, TypeScript, and general programming."
    },
    {
        "name": "Neovim",
        "description": "Vim-fork focused on extensibility and usability with Lua scripting.",
        "pricing": "Free / Open Source (Apache 2.0 / Vim License)",
        "category": "Terminal Modal Editor",
        "pros": ["Blazing fast modal editing", "Highly customizable via Lua", "Extremely lightweight footprint"],
        "cons": ["Steep learning curve", "Requires manual configuration setup"],
        "best_for": "Power users, terminal enthusiasts, and high-speed modal editing."
    },
    {
        "name": "Cursor IDE",
        "description": "AI-first code editor built on top of VS Code with deep LLM integration.",
        "pricing": "Freemium ($20/mo for Pro)",
        "category": "AI Code Editor",
        "pros": ["Seamless multi-file AI code generation", "Natural language terminal commands", "VS Code extension compatibility"],
        "cons": ["Proprietary AI features behind subscription", "Requires active internet connection for AI features"],
        "best_for": "Developers seeking AI-assisted coding and automated refactoring."
    },
    {
        "name": "JetBrains IntelliJ IDEA",
        "description": "Premier Java and Kotlin IDE with rich refactoring and static analysis tools.",
        "pricing": "Freemium (Community Free / Ultimate Paid $169/yr)",
        "category": "Full IDE",
        "pros": ["Unmatched code intelligence and refactoring", "Out-of-the-box build system support", "Rich framework integrations"],
        "cons": ["Resource intensive (high RAM usage)", "Ultimate features require paid license"],
        "best_for": "Enterprise Java, Kotlin, and full-stack backend development."
    },
    {
        "name": "Zed Editor",
        "description": "High-performance multiplayer code editor written in Rust.",
        "pricing": "Free / Open Source (GPL / Apache 2.0)",
        "category": "High-Performance Editor",
        "pros": ["GPU-accelerated rendering at 120 FPS", "Native real-time pair programming", "Ultra-fast startup"],
        "cons": ["Smaller extension ecosystem compared to VS Code", "Fewer platform-specific features currently"],
        "best_for": "Rust developers, real-time collaboration, and performance purists."
    },
    {
        "name": "Sublime Text 4",
        "description": "Slick, lightweight user interface with extraordinary performance.",
        "pricing": "Paid ($99 evaluation license)",
        "category": "Lightweight Text Editor",
        "pros": ["Instant startup time", "Handles huge log files with ease", "Cross-platform support"],
        "cons": ["Proprietary closed-source code", "Fewer out-of-the-box IDE capabilities"],
        "best_for": "Fast text editing, heavy file manipulation, and minimalists."
    },
    {
        "name": "Fleet by JetBrains",
        "description": "Next-generation lightweight IDE with distributed architecture.",
        "pricing": "Freemium",
        "category": "Lightweight IDE",
        "pros": ["Clean minimal UI", "Smart mode toggles full JetBrains engine", "Remote development support"],
        "cons": ["Still in preview/active development", "Ecosystem still growing"],
        "best_for": "Polyglot developers wanting light footprint with optional full IDE power."
    },
    {
        "name": "Helix Editor",
        "description": "Post-modern modal text editor built in Rust with built-in LSP support.",
        "pricing": "Free / Open Source (MPL-2.0)",
        "category": "Terminal Modal Editor",
        "pros": ["Zero configuration required for LSP", "Selection-first modal editing", "Ultra fast Rust execution"],
        "cons": ["Different keybindings from Vim", "No plugin API yet"],
        "best_for": "Developers wanting out-of-the-box modal editing with language server integration."
    },
    {
        "name": "Lapce",
        "description": "Lightning-fast native GUI text editor written in Rust with UI in Druid.",
        "pricing": "Free / Open Source (Apache 2.0)",
        "category": "Native GUI Editor",
        "pros": ["GPU acceleration", "Built-in terminal and LSP", "Wasm plugin system"],
        "cons": ["Under active development", "Fewer plugins currently"],
        "best_for": "Developers looking for a fast, native VS Code alternative."
    }
]


def load_history(history_file="content/history.json"):
    if os.path.exists(history_file):
        try:
            with open(history_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {"covered_ides": [], "daily_logs": []}
    return {"covered_ides": [], "daily_logs": []}


def save_history(history, history_file="content/history.json"):
    os.makedirs(os.path.dirname(history_file), exist_ok=True)
    with open(history_file, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=2)


def fetch_github_ides():
    """Fetch popular code editors / IDE repositories from GitHub API."""
    url = "https://api.github.com/search/repositories?q=topic:editor+OR+topic:ide&sort=stars&order=desc&per_page=15"
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "IDEGuide-ContentGenerator/1.0"}
    )
    discovered = []
    try:
        with urllib.request.urlopen(req, timeout=5) as response:
            data = json.loads(response.read().decode())
            for item in data.get("items", []):
                discovered.append({
                    "name": item.get("name").replace("-", " ").title(),
                    "description": item.get("description") or "Modern developer code editor.",
                    "pricing": "Free / Open Source" if not item.get("private") else "Paid / Proprietary",
                    "category": "Open Source Editor",
                    "pros": ["Active open source community", "High star count on GitHub", "Transparent codebase"],
                    "cons": ["May require self-compilation or manual plugins", "Ecosystem varies"],
                    "best_for": "Developers exploring cutting-edge open source tools."
                })
    except Exception as e:
        print(f"Notice: GitHub API fetch skipped/failed ({e}), using curated list.")
    return discovered


def select_ides_for_today(history, count=3):
    covered = set(history.get("covered_ides", []))
    candidates = []

    # Try curated list first
    for ide in CURATED_IDES:
        if ide["name"].lower() not in covered:
            candidates.append(ide)

    # Try GitHub API if needed
    if len(candidates) < count:
        gh_ides = fetch_github_ides()
        for ide in gh_ides:
            if ide["name"].lower() not in covered and not any(c["name"].lower() == ide["name"].lower() for c in candidates):
                candidates.append(ide)

    # Fallback to curated if all covered
    if len(candidates) < count:
        candidates = CURATED_IDES[:count]

    return candidates[:count]


def generate_amp_html_post(ide):
    """Generates valid AMP HTML snippet formatted for Blogger."""
    pros_html = "".join([f"<li>{p}</li>" for p in ide["pros"]])
    cons_html = "".join([f"<li>{c}</li>" for c in ide["cons"]])

    slug = ide["name"].lower().replace(" ", "-")

    amp_content = f"""<!doctype html>
<html ⚡ lang="en">
<head>
  <meta charset="utf-8">
  <title>IDE Guide Review: {ide['name']} - Pricing, Features, Pros & Cons</title>
  <link rel="canonical" href="https://ideguide.blogspot.com/{datetime.now().strftime('%Y/%m')}/{slug}.html">
  <meta name="viewport" content="width=device-width,minimum-scale=1,initial-scale=1">
  <style amp-boilerplate>body{{-webkit-animation:-amp-start 8s steps(1,end) 0s 1 normal both;-moz-animation:-amp-start 8s steps(1,end) 0s 1 normal both;-ms-animation:-amp-start 8s steps(1,end) 0s 1 normal both;animation:-amp-start 8s steps(1,end) 0s 1 normal both}}@-webkit-keyframes -amp-start{{from{{visibility:hidden}}to{{visibility:visible}}}}@-moz-keyframes -amp-start{{from{{visibility:hidden}}to{{visibility:visible}}}}@-ms-keyframes -amp-start{{from{{visibility:hidden}}to{{visibility:visible}}}}@-o-keyframes -amp-start{{from{{visibility:hidden}}to{{visibility:visible}}}}@keyframes -amp-start{{from{{visibility:hidden}}to{{visibility:visible}}}}</style><noscript><style amp-boilerplate>body{{-webkit-animation:none;-moz-animation:none;-ms-animation:none;animation:none}}</style></noscript>
  <script async src="https://cdn.ampproject.org/v0.js"></script>
  <style amp-custom>
    body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; line-height: 1.6; color: #222; padding: 15px; max-width: 800px; margin: 0 auto; background-color: #fcfcfc; }}
    h1 {{ color: #111; font-size: 1.8rem; border-bottom: 2px solid #0066cc; padding-bottom: 8px; }}
    h2 {{ color: #0066cc; font-size: 1.3rem; margin-top: 20px; }}
    .badge {{ display: inline-block; padding: 4px 8px; border-radius: 4px; font-weight: bold; background-color: #e1f5fe; color: #0288d1; font-size: 0.9rem; margin-right: 8px; }}
    .disclaimer {{ background-color: #fff3cd; border-left: 4px solid #ffc107; padding: 12px; font-size: 0.85rem; color: #856404; margin: 20px 0; border-radius: 2px; }}
    .pro-con-grid {{ display: flex; flex-wrap: wrap; gap: 15px; margin: 15px 0; }}
    .pro-box {{ flex: 1; min-width: 250px; background: #e8f5e9; border-left: 4px solid #2e7d32; padding: 10px 15px; border-radius: 4px; }}
    .con-box {{ flex: 1; min-width: 250px; background: #ffebee; border-left: 4px solid #c62828; padding: 10px 15px; border-radius: 4px; }}
  </style>
</head>
<body>
  <article>
    <h1>IDE Guide Review: {ide['name']}</h1>
    <p><span class="badge">{ide['category']}</span><span class="badge">{ide['pricing']}</span></p>

    <p><strong>Overview:</strong> {ide['description']}</p>

    <div class="disclaimer">
      {NON_SPONSORSHIP_DISCLAIMER}
    </div>

    <h2>Key Features & Analysis</h2>
    <p>When selecting the ideal editor for your development workflow, evaluating performance, extension capabilities, and licensing is critical. <strong>{ide['name']}</strong> is best suited for: <em>{ide['best_for']}</em>.</p>

    <h2>Pros & Cons Breakdown</h2>
    <div class="pro-con-grid">
      <div class="pro-box">
        <h3>👍 Pros</h3>
        <ul>
          {pros_html}
        </ul>
      </div>
      <div class="con-box">
        <h3>👎 Cons</h3>
        <ul>
          {cons_html}
        </ul>
      </div>
    </div>

    <h2>Free vs Paid Verdict</h2>
    <p><strong>Pricing Model:</strong> {ide['pricing']}</p>
    <p>Whether you should adopt {ide['name']} depends on your project scale and feature requirements. Always weigh the open-source freedom vs paid ecosystem features before committing.</p>

    <p><em>For more video walkthroughs and IDE breakdowns, check out our YouTube channel <a href="https://www.youtube.com/@IDEguide">@IDEguide</a> and bookmark <a href="https://ideguide.blogspot.com/">IDE Guide Blog</a>.</em></p>
  </article>
</body>
</html>"""
    return amp_content


def generate_google_flow_video_spec(ide):
    """Generates Google Flow visual script specification for YouTube @IDEguide."""
    spec = {
        "channel": "@IDEguide",
        "website": "https://ideguide.blogspot.com/",
        "title": f"{ide['name']} Review: Is It Worth It? | IDE Guide",
        "ide_name": ide["name"],
        "pricing": ide["pricing"],
        "category": ide["category"],
        "disclaimer": NON_SPONSORSHIP_DISCLAIMER,
        "format_specs": {
            "shorts": {
                "aspect_ratio": "9:16",
                "resolution": "1080x1920",
                "fps": 60,
                "target_duration_sec": 45
            },
            "longform": {
                "aspect_ratio": "16:9",
                "resolution": "3840x2160",
                "fps": 60,
                "target_duration_sec": 300
            }
        },
        "google_flow_prompts": [
            {
                "scene_id": 1,
                "duration_sec": 5,
                "narration": f"Is {ide['name']} the best editor for your setup? Let's break down the pros, cons, and pricing in 45 seconds!",
                "visual_prompt": f"Macro shot of developer desk with glowing dark theme running {ide['name']} interface, cinematic lighting, purple RGB backlight.",
                "framing": "9:16 Vertical Close-up",
                "lighting": "Cyberpunk dark mode studio lighting",
                "camera_motion": "Slow push-in zoom towards code editor UI",
                "text_overlay": f"{ide['name']} Review - IDE Guide"
            },
            {
                "scene_id": 2,
                "duration_sec": 10,
                "narration": f"{ide['description']} Best used for {ide['best_for']}",
                "visual_prompt": f"Smooth screen recording animation showing fast code typing and syntax highlighting inside {ide['name']}.",
                "framing": "9:16 Vertical UI Capture",
                "lighting": "Clean high contrast display glow",
                "camera_motion": "Static focus with dynamic text overlays",
                "text_overlay": f"Category: {ide['category']}"
            },
            {
                "scene_id": 3,
                "duration_sec": 15,
                "narration": f"Here are the top advantages: {', '.join(ide['pros'])}. However, consider these drawbacks: {', '.join(ide['cons'])}.",
                "visual_prompt": f"Split screen transition showing Pros badge in emerald green and Cons badge in crimson red on top of {ide['name']} dark UI background.",
                "framing": "9:16 Split layout",
                "lighting": "Dual tone green/red accent lighting",
                "camera_motion": "Fast slide-in transition from right",
                "text_overlay": "PROS vs CONS"
            },
            {
                "scene_id": 4,
                "duration_sec": 10,
                "narration": f"Pricing model: {ide['pricing']}. Check our full AMP blog post on ideguide.blogspot.com!",
                "visual_prompt": f"Final title card with IDE Guide logo, YouTube subscribe animation, and link badge for ideguide.blogspot.com.",
                "framing": "9:16 Centered Graphic",
                "lighting": "Bright sleek neon glow",
                "camera_motion": "Smooth fade to black",
                "text_overlay": "Subscribe @IDEguide | ideguide.blogspot.com"
            }
        ]
    }
    return spec


def main():
    date_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    output_dir = os.path.join("content", date_str)
    os.makedirs(output_dir, exist_ok=True)

    history = load_history()
    selected_ides = select_ides_for_today(history, count=3)

    print(f"Generating content for date: {date_str}")
    generated_summary = []

    for idx, ide in enumerate(selected_ides, 1):
        slug = ide["name"].lower().replace(" ", "_")

        # 1. AMP Blog Post
        amp_html = generate_amp_html_post(ide)
        blog_file = os.path.join(output_dir, f"blog_post_{idx}_{slug}.html")
        with open(blog_file, "w", encoding="utf-8") as f:
            f.write(amp_html)

        # 2. Google Flow Video Spec
        video_spec = generate_google_flow_video_spec(ide)
        video_file = os.path.join(output_dir, f"video_spec_{idx}_{slug}.json")
        with open(video_file, "w", encoding="utf-8") as f:
            json.dump(video_spec, f, indent=2)

        history.setdefault("covered_ides", [])
        if ide["name"].lower() not in history["covered_ides"]:
            history["covered_ides"].append(ide["name"].lower())

        generated_summary.append({
            "ide": ide["name"],
            "blog_post": blog_file,
            "video_spec": video_file
        })
        print(f"[{idx}/3] Generated AMP blog & video spec for: {ide['name']}")

    history.setdefault("daily_logs", []).append({
        "date": date_str,
        "items": generated_summary
    })
    save_history(history)
    print("Successfully generated daily content package.")

if __name__ == "__main__":
    main()
