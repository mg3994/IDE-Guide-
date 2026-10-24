#!/usr/bin/env python3
"""
Daily Content Generator for IDE Guide.
Generates 3 AMP HTML blog posts and 3 Google Flow video specifications daily.
Tracks covered IDEs in content/history.json to ensure fresh daily content.
"""

import os
import json
import datetime
from typing import Dict, Any, List
from scripts.amp_validator import validate_amp_html, REQUIRED_DISCLAIMER

HISTORY_FILE = "content/history.json"

IDE_DATABASE: Dict[str, Dict[str, Any]] = {
    "VS Code": {
        "name": "Visual Studio Code",
        "slug": "vs-code",
        "pricing": "Free & Open Source (MIT core / Proprietary build)",
        "is_free": True,
        "tagline": "The ubiquitous extensible code editor for modern development.",
        "pros": [
            "Massive extension marketplace with thousands of plugins.",
            "Lightweight, customizable interface with built-in Git integration.",
            "Strong multi-language support and Remote SSH / Container development."
        ],
        "cons": [
            "High memory usage when running multiple heavy extensions.",
            "Requires configuration tweaking out of the box for complex language servers."
        ],
        "best_for": "Web, Node.js, Python, TypeScript, and general multi-language developers.",
        "image_url": "https://images.unsplash.com/photo-1555066931-4365d14bab8c?w=800&auto=format&fit=crop"
    },
    "Cursor": {
        "name": "Cursor",
        "slug": "cursor-ai",
        "pricing": "Freemium ($20/mo Pro plan)",
        "is_free": False,
        "tagline": "The AI-first fork of VS Code built for native LLM pair programming.",
        "pros": [
            "Deep codebase indexing for instant context-aware AI edits.",
            "Cmd+K in-line code generation and multi-file editing capabilities.",
            "Full compatibility with all VS Code extensions."
        ],
        "cons": [
            "Pro tier required for fast request limits and premium model access.",
            "Requires trusting third-party cloud infrastructure for codebase indexing."
        ],
        "best_for": "Developers seeking maximum speed and AI-driven automation in full-stack engineering.",
        "image_url": "https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?w=800&auto=format&fit=crop"
    },
    "Zed": {
        "name": "Zed Editor",
        "slug": "zed-editor",
        "pricing": "Free & Open Source (GPL/Apache 2.0)",
        "is_free": True,
        "tagline": "Blazingly fast, Rust-built, GPU-accelerated code editor.",
        "pros": [
            "Extremely fast startup time and low memory footprint.",
            "Built-in collaborative editing and multiplayer screen-sharing.",
            "Sleek minimalist UI with native Tree-sitter parsing."
        ],
        "cons": [
            "Plugin ecosystem is still maturing compared to VS Code.",
            "Currently limited advanced debugging tools for non-mainstream targets."
        ],
        "best_for": "Rust, Go, and C++ developers looking for maximum UI responsiveness.",
        "image_url": "https://images.unsplash.com/photo-1542831371-29b0f74f9713?w=800&auto=format&fit=crop"
    },
    "PyCharm": {
        "name": "PyCharm",
        "slug": "pycharm",
        "pricing": "Freemium (Community Edition Free / Professional Paid)",
        "is_free": False,
        "tagline": "The heavy-duty Python IDE by JetBrains for professional data science & web apps.",
        "pros": [
            "Unrivaled Python refactoring, code navigation, and static analysis.",
            "Built-in database tooling, Django support, and Jupyter notebook integration.",
            "Comprehensive debugging and profiler built-in."
        ],
        "cons": [
            "Heavy resource consumption (RAM and CPU during indexing).",
            "Slow startup time on older hardware."
        ],
        "best_for": "Professional Python backend developers, Django engineers, and Data Scientists.",
        "image_url": "https://images.unsplash.com/photo-1515879218367-8466d910aaa4?w=800&auto=format&fit=crop"
    },
    "Neovim": {
        "name": "Neovim",
        "slug": "neovim",
        "pricing": "Free & Open Source (Apache 2.0 / Vim License)",
        "is_free": True,
        "tagline": "Hyperextensible Lua-based terminal text editor built for keyboard-driven efficiency.",
        "pros": [
            "Zero GUI overhead; runs blazing fast in terminal or SSH.",
            "Infinite customizability with Lua plugins (LSP, Treesitter, Telescope).",
            "Minimal resource footprint and modal editing mastery."
        ],
        "cons": [
            "Steep learning curve and initial configuration effort.",
            "Requires user maintenance of plugin ecosystem updates."
        ],
        "best_for": "Power users, CLI enthusiasts, and developers who prefer keyboard-only navigation.",
        "image_url": "https://images.unsplash.com/photo-1629654297299-c8506221ca97?w=800&auto=format&fit=crop"
    },
    "Windsurf": {
        "name": "Windsurf Editor",
        "slug": "windsurf",
        "pricing": "Freemium (Free tier / $15/mo Pro)",
        "is_free": False,
        "tagline": "Agentic IDE by Codeium designed for real-time human-AI flow.",
        "pros": [
            "Cascade AI agent with continuous codebase awareness.",
            "Smooth transition between command generation and automated refactoring.",
            "Fast responsiveness with intuitive interface."
        ],
        "cons": [
            "Requires subscription for high-frequency agent requests.",
            "Newer product relative to traditional IDEs."
        ],
        "best_for": "Engineers wanting agentic multi-step code execution directly inside the editor.",
        "image_url": "https://images.unsplash.com/photo-1517694712202-14dd9538aa97?w=800&auto=format&fit=crop"
    },
    "JetBrains Fleet": {
        "name": "JetBrains Fleet",
        "slug": "jetbrains-fleet",
        "pricing": "Freemium (Free preview / Subscription)",
        "is_free": False,
        "tagline": "Next-generation lightweight distributed polyglot IDE.",
        "pros": [
            "Lightweight editor mode with optional IntelliJ smart engine backend.",
            "Built-in collaborative pair programming.",
            "Sleek modern UI across Kotlin, Java, Python, Rust, and TypeScript."
        ],
        "cons": [
            "Still in active development preview with changing feature set.",
            "Fewer extension options compared to standard IntelliJ IDEA or VS Code."
        ],
        "best_for": "Developers wanting JetBrains intelligence in a fast modern UI.",
        "image_url": "https://images.unsplash.com/photo-1531403009284-440f080d1e12?w=800&auto=format&fit=crop"
    },
    "WebStorm": {
        "name": "WebStorm",
        "slug": "webstorm",
        "pricing": "Paid / Freemium for Non-Commercial",
        "is_free": False,
        "tagline": "The smartest JavaScript and TypeScript IDE by JetBrains.",
        "pros": [
            "Best-in-class refactoring for React, Vue, Angular, and Node.js.",
            "Integrated unit testing, debugging, and git visual tools.",
            "Superior type checking and auto-imports out of the box."
        ],
        "cons": [
            "Commercial paid license for enterprise usage.",
            "Consumes more RAM than VS Code or Zed."
        ],
        "best_for": "Frontend and full-stack JavaScript/TypeScript engineers.",
        "image_url": "https://images.unsplash.com/photo-1507238691740-187a5b1d37b8?w=800&auto=format&fit=crop"
    },
    "Lapce": {
        "name": "Lapce",
        "slug": "lapce",
        "pricing": "Free & Open Source (Apache 2.0)",
        "is_free": True,
        "tagline": "Lightning-fast Rust-based modal code editor with GPU rendering.",
        "pros": [
            "Native Rust speed with low latency response.",
            "Built-in LSP support and Modal Vim editing option.",
            "Wasm plugin architecture for safe extensibility."
        ],
        "cons": [
            "Early stage project; plugin ecosystem still expanding.",
            "Occasional visual glitches in complex layout settings."
        ],
        "best_for": "Open-source enthusiasts seeking a Rust-native VS Code alternative.",
        "image_url": "https://images.unsplash.com/photo-1550745165-9bc0b252726f?w=800&auto=format&fit=crop"
    }
}


def load_history() -> List[str]:
    """Loads history of covered IDE names from HISTORY_FILE."""
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data.get("covered_ides", [])
        except Exception:
            return []
    return []


def save_history(covered_ides: List[str]) -> None:
    """Saves updated history to HISTORY_FILE."""
    os.makedirs(os.path.dirname(HISTORY_FILE), exist_ok=True)
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump({"covered_ides": covered_ides, "last_updated": datetime.date.today().isoformat()}, f, indent=2)


def select_daily_ides(count: int = 3) -> List[Dict[str, Any]]:
    """Selects `count` IDEs from the database that haven't been covered recently."""
    history = load_history()
    available_keys = [k for k in IDE_DATABASE.keys() if k not in history]

    # If all IDEs in database were covered, reset history cycle
    if len(available_keys) < count:
        history = []
        available_keys = list(IDE_DATABASE.keys())

    selected_keys = available_keys[:count]
    return [IDE_DATABASE[k] for k in selected_keys]


def generate_amp_blog_html(ide: Dict[str, Any], canonical_url: str) -> str:
    """Generates valid AMP HTML string for Blogger for given IDE details."""
    pros_html = "".join([f"<li>{p}</li>" for p in ide["pros"]])
    cons_html = "".join([f"<li>{c}</li>" for c in ide["cons"]])

    html = f"""<!doctype html>
<html amp lang="en">
<head>
  <meta charset="utf-8">
  <title>{ide['name']} - Comprehensive Review & Developer Guide | IDE Guide</title>
  <link rel="canonical" href="{canonical_url}">
  <meta name="viewport" content="width=device-width,initial-scale=1,minimum-scale=1,maximum-scale=1,user-scalable=no,minimal-ui">
  <script async src="https://cdn.ampproject.org/v0.js"></script>
  <style amp-boilerplate>body{{-webkit-animation:-amp-start 8s steps(1,end) 0s 1 normal both;-moz-animation:-amp-start 8s steps(1,end) 0s 1 normal both;-ms-animation:-amp-start 8s steps(1,end) 0s 1 normal both;animation:-amp-start 8s steps(1,end) 0s 1 normal both}}@-webkit-keyframes -amp-start{{from{{visibility:hidden}}to{{visibility:visible}}}}@-moz-keyframes -amp-start{{from{{visibility:hidden}}to{{visibility:visible}}}}@-ms-keyframes -amp-start{{from{{visibility:hidden}}to{{visibility:visible}}}}@-o-keyframes -amp-start{{from{{visibility:hidden}}to{{visibility:visible}}}}@keyframes -amp-start{{from{{visibility:hidden}}to{{visibility:visible}}}}</style><noscript><style amp-boilerplate>body{{-webkit-animation:none;-moz-animation:none;-ms-animation:none;animation:none}}</style></noscript>
  <style amp-custom>
    body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; line-height: 1.6; color: #1e293b; background-color: #f8fafc; margin: 0; padding: 0; }}
    header {{ background-color: #0f172a; color: #ffffff; padding: 2rem 1rem; text-align: center; }}
    header h1 {{ margin: 0 0 0.5rem 0; font-size: 2rem; color: #38bdf8; }}
    header p {{ margin: 0; font-size: 1.1rem; color: #94a3b8; }}
    main {{ max-width: 800px; margin: 2rem auto; padding: 0 1rem; }}
    .badge {{ display: inline-block; background-color: #0284c7; color: white; padding: 0.25rem 0.75rem; border-radius: 9999px; font-size: 0.875rem; font-weight: 600; margin-bottom: 1rem; }}
    .hero-img {{ width: 100%; height: auto; border-radius: 8px; margin-bottom: 1.5rem; }}
    .section {{ background: #ffffff; padding: 1.5rem; border-radius: 8px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); margin-bottom: 1.5rem; }}
    h2 {{ color: #0f172a; border-bottom: 2px solid #e2e8f0; padding-bottom: 0.5rem; font-size: 1.4rem; }}
    ul {{ padding-left: 1.25rem; }}
    li {{ margin-bottom: 0.5rem; }}
    .disclaimer {{ background-color: #f1f5f9; border-left: 4px solid #64748b; padding: 1rem; font-size: 0.875rem; color: #475569; margin-top: 2rem; border-radius: 4px; }}
    footer {{ text-align: center; padding: 2rem 1rem; color: #64748b; font-size: 0.875rem; }}
  </style>
</head>
<body>
  <header>
    <h1>{ide['name']} Deep Dive</h1>
    <p>{ide['tagline']}</p>
  </header>
  <main>
    <div class="section">
      <span class="badge">Pricing: {ide['pricing']}</span>
      <amp-img src="{ide['image_url']}" width="800" height="450" layout="responsive" alt="{ide['name']} screenshot" class="hero-img"></amp-img>
      <h2>Overview</h2>
      <p>{ide['tagline']} In this review, we examine whether {ide['name']} aligns with your daily software development workflow.</p>
    </div>

    <div class="section">
      <h2>Key Strengths & Pros</h2>
      <ul>{pros_html}</ul>
    </div>

    <div class="section">
      <h2>Drawbacks & Trade-offs</h2>
      <ul>{cons_html}</ul>
    </div>

    <div class="section">
      <h2>Verdict & Ideal Audience</h2>
      <p><strong>Best For:</strong> {ide['best_for']}</p>
      <p>If you fit this persona, {ide['name']} provides exceptional value and speed.</p>
    </div>

    <div class="disclaimer">
      <p>{REQUIRED_DISCLAIMER}</p>
    </div>
  </main>
  <footer>
    <p>© {datetime.date.today().year} IDE Guide (ideguide.blogspot.com). Independent Developer Reviews.</p>
  </footer>
</body>
</html>"""
    return html


def generate_google_flow_video_spec(ide: Dict[str, Any]) -> Dict[str, Any]:
    """Generates Google Flow AI video specification for given IDE."""
    spec = {
        "title": f"Is {ide['name']} Worth Using in {datetime.date.today().year}? | IDE Guide Review",
        "target_ide": ide["name"],
        "format": "9:16 vertical (YouTube Shorts) / 16:9 widescreen compatible",
        "duration_seconds": 60,
        "scenes": [
            {
                "scene_id": 1,
                "timecode": "00:00 - 00:05",
                "visual_prompt": f"Cinematic dark mode coding workstation with glowing neon cyan lighting. Close-up shot showing code typing rapidly on screen with {ide['name']} UI visible.",
                "camera_movement": "Slow zoom in towards code editor cursor",
                "narration_script": f"Looking for the best code editor in {datetime.date.today().year}? Let's talk about {ide['name']}.",
                "on_screen_text": f"IDE GUIDE: {ide['name']}",
                "audio_cues": "Upbeat high-tech synth drop."
            },
            {
                "scene_id": 2,
                "timecode": "00:05 - 00:20",
                "visual_prompt": f"Split screen visual showcasing pricing model label '{ide['pricing']}' alongside IDE key interface features with clean motion graphics.",
                "camera_movement": "Smooth pan across feature panel",
                "narration_script": f"{ide['name']} is {ide['pricing']}. Here is what makes it stand out for developers.",
                "on_screen_text": f"Pricing: {ide['pricing']}",
                "audio_cues": "Rhythmic ambient beat."
            },
            {
                "scene_id": 3,
                "timecode": "00:20 - 00:40",
                "visual_prompt": f"Demonstration scene showing rapid code autocompletion, multi-file refactoring, and smooth navigation in {ide['name']}.",
                "camera_movement": "Dynamic tracking shot across code editor panel",
                "narration_script": f"Pros: {ide['pros'][0]} Plus, {ide['pros'][1]}",
                "on_screen_text": "PROS: Speed & Intelligence",
                "audio_cues": "Energetic background track."
            },
            {
                "scene_id": 4,
                "timecode": "00:40 - 00:50",
                "visual_prompt": f"Close-up analytical view showing trade-offs, resource consumption meters, or plugin setup panel.",
                "camera_movement": "Static high-contrast macro view",
                "narration_script": f"On the downside: {ide['cons'][0]}",
                "on_screen_text": "CONS: Key Limitations",
                "audio_cues": "Subtle low bass chime."
            },
            {
                "scene_id": 5,
                "timecode": "00:50 - 01:00",
                "visual_prompt": f"End card featuring IDE Guide branding (@IDEguide), website ideguide.blogspot.com, and prominent non-sponsorship disclosure text.",
                "camera_movement": "Fade in overlay with sleek animation",
                "narration_script": f"Verdict: Best for {ide['best_for']}. Subscribe to IDE Guide for unbiased editor reviews!",
                "on_screen_text": f"Best For: {ide['best_for']}\nideguide.blogspot.com",
                "audio_cues": "Outro music swell."
            }
        ],
        "disclaimer": REQUIRED_DISCLAIMER
    }
    return spec


def run_daily_content_generation(date_str: str = None) -> List[str]:
    """Runs content generation for 3 daily IDE blog posts & video specs."""
    if not date_str:
        date_str = datetime.date.today().isoformat()

    output_dir = os.path.join("content", date_str)
    os.makedirs(output_dir, exist_ok=True)

    selected_ides = select_daily_ides(3)
    covered_names = load_history()
    generated_files = []

    for idx, ide in enumerate(selected_ides, 1):
        slug = ide["slug"]
        canonical_url = f"https://ideguide.blogspot.com/{date_str.replace('-', '/')}/{slug}.html"

        # 1. Generate AMP HTML blog post
        blog_html = generate_amp_blog_html(ide, canonical_url)
        is_valid, errs = validate_amp_html(blog_html)
        if not is_valid:
            raise ValueError(f"Generated AMP HTML for {ide['name']} failed validation: {errs}")

        blog_filename = os.path.join(output_dir, f"post_{idx}_{slug}_amp.html")
        with open(blog_filename, "w", encoding="utf-8") as f:
            f.write(blog_html)
        generated_files.append(blog_filename)

        # 2. Generate Google Flow video spec
        video_spec = generate_google_flow_video_spec(ide)
        video_filename = os.path.join(output_dir, f"video_{idx}_{slug}_google_flow.json")
        with open(video_filename, "w", encoding="utf-8") as f:
            json.dump(video_spec, f, indent=2)
        generated_files.append(video_filename)

        if ide["name"] not in covered_names:
            covered_names.append(ide["name"])

    save_history(covered_names)
    return generated_files


if __name__ == "__main__":
    files = run_daily_content_generation()
    print(f" Successfully generated {len(files)} content files:")
    for f in files:
        print(f"  - {f}")
