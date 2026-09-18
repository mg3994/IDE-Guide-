#!/usr/bin/env python3
"""
IDE Guide Agentic Skill Tool
Generates AMP HTML Blog Posts for Blogger (ideguide.blogspot.com)
and Google Flow Video Specifications for YouTube (@IDEguide).
"""

import argparse
import datetime
import json
import os
import re
import sys
from typing import Any, Dict, Optional

DISCLAIMER_TEXT = (
    "Disclaimer: IDE Guide is an independent technical publication. "
    "This content is not sponsored, endorsed, or affiliated with any software vendor "
    "or editor developer mentioned above. All reviews and assessments are based strictly "
    "on objective developer evaluation."
)

BLOGGER_URL = "https://ideguide.blogspot.com/"
YOUTUBE_URL = "https://www.youtube.com/@IDEguide"

KNOWN_IDES_DATABASE: Dict[str, Dict[str, Any]] = {
    "zed": {
        "name": "Zed Editor",
        "category": "High-Performance Code Editor",
        "developer": "Zed Industries",
        "pricing_type": "Free / Open Source (Community) & Paid (Zed AI / Collaboration)",
        "pricing_details": "Core editor is free and open-source under GPL/Apache licenses. Zed AI features and team collaboration plans start at $10/month.",
        "description": "Zed is a high-performance, multi-player code editor written in Rust. Designed for ultra-fast startup times, low latency typing, and native AI integration.",
        "key_features": [
            "Written in Rust with GPU-accelerated rendering (Metal/Vulkan)",
            "Native multiplayer remote pair programming",
            "Built-in AI model support (Claude 3.5 Sonnet, GPT-4o, Ollama)",
            "Blazing fast speed with sub-millisecond input latency",
            "Built-in terminal and language server protocol (LSP) integration"
        ],
        "pros": [
            "Extremely fast and lightweight memory footprint",
            "Native multiplayer real-time collaboration",
            "Modern UI with seamless AI completion workflow"
        ],
        "cons": [
            "Smaller plugin ecosystem compared to VS Code",
            "Platform support expanding (macOS native, Linux & Windows in active rollout)"
        ],
        "who_is_it_for": "Developers seeking ultra-fast editing, native Rust performance, and seamless AI pair programming without browser overhead.",
        "website": "https://zed.dev",
        "repo": "https://github.com/zed-industries/zed"
    },
    "cursor": {
        "name": "Cursor",
        "category": "AI-First Code Editor",
        "developer": "Anysphere",
        "pricing_type": "Freemium (Free Hobby tier, $20/mo Pro, $40/mo Business)",
        "pricing_details": "Free Hobby plan includes 2,000 completions and 50 slow premium requests. Pro plan ($20/month) offers 500 fast premium requests/mo and unlimited slow requests.",
        "description": "Cursor is a VS Code fork built from the ground up for AI-first software development, featuring codebase indexing, fast inline generation, and AI agent capabilities.",
        "key_features": [
            "Full codebase indexing for intelligent context retrieval",
            "Cmd+K inline code editing and Ctrl+I full-file prompt generation",
            "Cursor Agent mode for multi-file code editing and bug fixing",
            "100% compatible with VS Code extensions and settings",
            "Support for Claude 3.5 Sonnet, GPT-4o, and custom API keys"
        ],
        "pros": [
            "Unmatched codebase-aware context and inline AI generation",
            "Zero friction migration from VS Code",
            "Powerful agent mode for autonomous refactoring"
        ],
        "cons": [
            "Requires active internet connection for cloud AI features",
            "Subscription cost for heavy daily AI usage"
        ],
        "who_is_it_for": "Software engineers and tech leads who want maximum productivity boost using cutting-edge AI assistant workflows.",
        "website": "https://cursor.com",
        "repo": "https://github.com/getcursor/cursor"
    },
    "neovim": {
        "name": "Neovim",
        "category": "Hyperextensible Vim-based Text Editor",
        "developer": "Neovim Community",
        "pricing_type": "100% Free & Open Source",
        "pricing_details": "Completely free under Apache 2.0 and Vim licenses. No hidden costs or subscriptions.",
        "description": "Neovim is a refactored extension of Vim, focusing on extensibility, modern Lua scripting, embedded terminal capabilities, and asynchronous plugin architecture.",
        "key_features": [
            "First-class Lua 5.1 / LuaJIT plugin API",
            "Built-in Language Server Protocol (LSP) client",
            "Treesitter integration for precise syntax parsing and structural highlighting",
            "Terminal emulator and headless server mode",
            "Massive community ecosystem (Lazy.nvim, Mason, Telescope)"
        ],
        "pros": [
            "Unbeatable keyboard efficiency and modal editing speed",
            "Near-zero memory footprint and instantaneous startup",
            "Infinitely customizable to fit any developer workflow"
        ],
        "cons": [
            "Steep learning curve for Vim keybindings",
            "Requires manual configuration and maintenance"
        ],
        "who_is_it_for": "Terminal enthusiasts, systems programmers, and developers who demand total control over their editing environment.",
        "website": "https://neovim.io",
        "repo": "https://github.com/neovim/neovim"
    },
    "vscodium": {
        "name": "VSCodium",
        "category": "Telemetry-Free Open Source Editor",
        "developer": "VSCodium Community",
        "pricing_type": "100% Free & Open Source",
        "pricing_details": "Completely free binaries built under the MIT license without Microsoft proprietary tracking.",
        "description": "VSCodium is a community-driven release of Microsoft's VS Code source code with telemetry, tracking, and proprietary licensing stripped out.",
        "key_features": [
            "100% open-source MIT build of VS Code",
            "Zero telemetry, tracking, or data collection",
            "Clean binary builds for Windows, macOS, and Linux",
            "Open VSX Registry support for extensions",
            "Identical UI and keyboard shortcuts as standard VS Code"
        ],
        "pros": [
            "Privacy-preserving and lightweight",
            "Familiar VS Code user experience without background tracking",
            "Free for enterprise and personal use"
        ],
        "cons": [
            "Microsoft Marketplace extensions require manual configuration or Open VSX equivalent",
            "Some Microsoft proprietary extensions (e.g., C# debugger, Remote-SSH) are restricted"
        ],
        "who_is_it_for": "Privacy-conscious developers and corporate environments requiring open-source compliance.",
        "website": "https://vscodium.com",
        "repo": "https://github.com/VSCodium/vscodium"
    },
    "lapce": {
        "name": "Lapce",
        "category": "Lightning Fast Rust GUI Editor",
        "developer": "Lapce Community",
        "pricing_type": "100% Free & Open Source",
        "pricing_details": "Completely free under the Apache 2.0 license.",
        "description": "Lapce is an ultra-fast code editor written in Rust with Druid GUI. It features modal editing support, LSP support, and remote development capabilities out of the box.",
        "key_features": [
            "Native GUI built with Rust and GPU acceleration",
            "Vim-like modal editing mode built-in",
            "Built-in Language Server Protocol (LSP) for code intelligence",
            "Wasm plugin system for multi-language extensions",
            "Remote development over SSH without server setup"
        ],
        "pros": [
            "Minimal CPU and RAM consumption",
            "Native cross-platform GUI rendering",
            "Built-in terminal and LSP integration"
        ],
        "cons": [
            "Plugin ecosystem is still in early development phase",
            "Occasional visual glitches on certain window managers"
        ],
        "who_is_it_for": "Developers seeking a lightweight, modern Rust GUI editor with Vim keybinding support.",
        "website": "https://lapce.dev",
        "repo": "https://github.com/lapce/lapce"
    },
    "fleet": {
        "name": "JetBrains Fleet",
        "category": "Next-Gen Distributed IDE",
        "developer": "JetBrains",
        "pricing_type": "Freemium / Commercial Preview",
        "pricing_details": "Free during Public Preview. Pricing model upon official release will include personal and commercial tier options.",
        "description": "JetBrains Fleet is a lightweight editor built from scratch using IntelliJ code processing engine, offering smart polyglot editing and distributed execution.",
        "key_features": [
            "Lightweight code editor mode that turns into a full IDE when enabled",
            "Multi-language smart code completion and refactoring",
            "Distributed architecture allowing execution on remote cloud servers or containers",
            "Built-in collaborative pair programming",
            "Clean minimalist interface designed for high screen real estate"
        ],
        "pros": [
            "Power of JetBrains static analysis in a lightweight shell",
            "Seamless cloud and container development integration",
            "Fast responsiveness"
        ],
        "cons": [
            "Still in preview with evolving feature set",
            "Requires JetBrains account for full sync features"
        ],
        "who_is_it_for": "JetBrains users looking for a fast, modern alternative to heavy IDEs for quick editing and remote cloud dev.",
        "website": "https://www.jetbrains.com/fleet/",
        "repo": "https://github.com/JetBrains/fleet"
    }
}


def sanitize_slug(name: str) -> str:
    """Creates a clean URL/filename slug from string."""
    slug = re.sub(r'[^a-zA-Z0-9\s-]', '', name.lower())
    slug = re.sub(r'[\s_]+', '-', slug)
    return slug.strip('-')


def fetch_or_build_ide_data(ide_query: str) -> Dict[str, Any]:
    """Retrieves existing IDE metadata or constructs structured entry."""
    slug = sanitize_slug(ide_query)
    if slug in KNOWN_IDES_DATABASE:
        return KNOWN_IDES_DATABASE[slug]

    # Check partial match
    for k, v in KNOWN_IDES_DATABASE.items():
        if slug in k or k in slug:
            return v

    # Fallback template if unknown IDE is provided
    formatted_title = ide_query.replace("-", " ").replace("_", " ").title()
    return {
        "name": formatted_title,
        "category": "Modern Code Editor / Development Tool",
        "developer": f"{formatted_title} Development Team",
        "pricing_type": "Free / Open Source & Commercial Options Available",
        "pricing_details": "Offers standard community edition alongside premium pro features.",
        "description": f"{formatted_title} is a specialized code editor designed for modern software development, code refactoring, and productive developer workflows.",
        "key_features": [
            "Intelligent code navigation and syntax highlighting",
            "Extensible extension and theme ecosystem",
            "Integrated terminal and version control support",
            "Customizable keybindings and developer preferences",
            "Multi-language source code support"
        ],
        "pros": [
            "Modern ergonomic user interface",
            "Active developer community and frequent updates",
            "Streamlined workflow for multi-file projects"
        ],
        "cons": [
            "Resource utilization under heavy project workloads",
            "Learning curve for advanced configuration settings"
        ],
        "who_is_it_for": "Developers seeking an effective, modern workspace tailored for rapid software creation.",
        "website": f"https://github.com/search?q={slug}",
        "repo": f"https://github.com/search?q={slug}"
    }


def generate_amp_html_blogpost(ide_data: Dict[str, Any]) -> str:
    """Generates AMP-compliant HTML for Blogger posts."""
    name = ide_data["name"]
    category = ide_data["category"]
    developer = ide_data["developer"]
    pricing_type = ide_data["pricing_type"]
    pricing_details = ide_data["pricing_details"]
    description = ide_data["description"]
    features = ide_data["key_features"]
    pros = ide_data["pros"]
    cons = ide_data["cons"]
    who_for = ide_data["who_is_it_for"]
    website = ide_data["website"]
    slug = sanitize_slug(name)

    features_html = "".join([f"<li><strong>{f.split(':')[0] if ':' in f else 'Feature'}:</strong> {f}</li>" for f in features])
    pros_html = "".join([f"<li>✅ {p}</li>" for p in pros])
    cons_html = "".join([f"<li>⚠️ {c}</li>" for c in cons])

    html_content = f"""<!str>
<!DOCTYPE html>
<html ⚡ lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,minimum-scale=1,initial-scale=1">
  <title>{name} Review & Guide - IDE Guide</title>
  <link rel="canonical" href="{BLOGGER_URL}posts/{slug}.html">
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
    .container {{
      max-width: 800px;
      margin: 0 auto;
      padding: 20px;
    }}
    header {{
      background: #0f172a;
      color: #ffffff;
      padding: 30px 20px;
      border-radius: 12px;
      margin-bottom: 24px;
    }}
    header h1 {{
      margin: 0 0 10px 0;
      font-size: 2rem;
      color: #38bdf8;
    }}
    .badge {{
      display: inline-block;
      background: #0284c7;
      color: #ffffff;
      padding: 4px 12px;
      border-radius: 9999px;
      font-size: 0.85rem;
      font-weight: 600;
      margin-right: 8px;
    }}
    .badge-price {{
      background: #16a34a;
    }}
    .card {{
      background: #ffffff;
      border: 1px solid #e2e8f0;
      border-radius: 12px;
      padding: 24px;
      margin-bottom: 24px;
      box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }}
    h2 {{
      color: #0f172a;
      border-bottom: 2px solid #38bdf8;
      padding-bottom: 8px;
      margin-top: 0;
    }}
    ul {{
      padding-left: 20px;
    }}
    li {{
      margin-bottom: 8px;
    }}
    .pros-cons {{
      display: flex;
      flex-wrap: wrap;
      gap: 16px;
    }}
    .pro-box, .con-box {{
      flex: 1;
      min-width: 280px;
      padding: 16px;
      border-radius: 8px;
    }}
    .pro-box {{
      background: #f0fdf4;
      border: 1px solid #bbf7d0;
    }}
    .con-box {{
      background: #fff1f2;
      border: 1px solid #fecdd3;
    }}
    .disclaimer-box {{
      background: #f1f5f9;
      border-left: 4px solid #64748b;
      padding: 16px;
      font-size: 0.9rem;
      color: #475569;
      margin-top: 30px;
      border-radius: 0 8px 8px 0;
    }}
    .cta-button {{
      display: inline-block;
      background: #2563eb;
      color: #ffffff;
      text-decoration: none;
      padding: 12px 24px;
      border-radius: 8px;
      font-weight: 600;
      margin-top: 12px;
    }}
  </style>
</head>
<body>
  <div class="container">
    <header>
      <span class="badge">{category}</span>
      <span class="badge badge-price">{pricing_type.split('(')[0]}</span>
      <h1>{name}: Comprehensive Developer Review & Guide</h1>
      <p>Independent analysis of features, performance, pricing, and key benefits by IDE Guide.</p>
    </header>

    <div class="card">
      <h2>Overview & Developer Mission</h2>
      <p>{description}</p>
      <p><strong>Developed by:</strong> {developer}</p>
      <p><strong>Official Website:</strong> <a href="{website}" target="_blank" rel="noopener">{website}</a></p>
    </div>

    <div class="card">
      <h2>Pricing & License Structure</h2>
      <p><strong>Pricing Tier:</strong> {pricing_type}</p>
      <p>{pricing_details}</p>
    </div>

    <div class="card">
      <h2>Key Features & Highlights</h2>
      <ul>
        {features_html}
      </ul>
    </div>

    <div class="card">
      <h2>Pros & Cons Breakdown</h2>
      <div class="pros-cons">
        <div class="pro-box">
          <h3>Pros</h3>
          <ul>{pros_html}</ul>
        </div>
        <div class="con-box">
          <h3>Cons</h3>
          <ul>{cons_html}</ul>
        </div>
      </div>
    </div>

    <div class="card">
      <h2>Who Is {name} Best For?</h2>
      <p>{who_for}</p>
    </div>

    <div class="card">
      <h2>Watch Video Showcase & Subscribe</h2>
      <p>Check out our daily video breakdowns and hands-on editor showcases on YouTube!</p>
      <a class="cta-button" href="{YOUTUBE_URL}" target="_blank" rel="noopener">Visit IDE Guide YouTube Channel (@IDEguide)</a>
    </div>

    <div class="disclaimer-box">
      <strong>Independent Publication Statement:</strong><br>
      {DISCLAIMER_TEXT}
    </div>
  </div>
</body>
</html>"""
    return html_content.replace("<!str>\n", "")


def generate_google_flow_video_spec(ide_data: Dict[str, Any]) -> Dict[str, Any]:
    """Generates Google Flow AI video prompts and script specifications."""
    name = ide_data["name"]
    category = ide_data["category"]
    pricing_type = ide_data["pricing_type"]
    description = ide_data["description"]
    features = ide_data["key_features"]
    pros = ide_data["pros"]
    cons = ide_data["cons"]
    who_for = ide_data["who_is_it_for"]

    top_feature_1 = features[0] if len(features) > 0 else "Intelligent coding interface"
    top_feature_2 = features[1] if len(features) > 1 else "Fast performance"
    top_pro = pros[0] if len(pros) > 0 else "Great user interface"
    top_con = cons[0] if len(cons) > 0 else "Niche feature set"

    flow_spec = {
        "channel": "IDE Guide (@IDEguide)",
        "video_title": f"{name} Showcase: Is it worth using? (Free vs Paid Review)",
        "target_platforms": ["YouTube Shorts (9:16)", "YouTube Longform (16:9)", "TikTok"],
        "ide_metadata": {
            "name": name,
            "category": category,
            "pricing": pricing_type
        },
        "prompts_and_scenes": [
            {
                "scene_number": 1,
                "title": "Hook & Editor Reveal",
                "timecode": "00:00 - 00:05",
                "flow_prompt": f"Close-up cinematic shot of a dark mode workspace monitor rendering {name} code editor. Code autocompletes with luminous neon blue highlights. Camera performs a subtle smooth zoom forward. Cyberpunk aesthetic ambient LED background lighting.",
                "voiceover_script": f"Looking for an upgraded code editor? Let's check out {name}!",
                "camera": "Slow forward dolly / subtle zoom-in",
                "lighting": "Dark room, 6500K desk lamp, cyan ambient backlight",
                "aspect_ratio_preset": "9:16 vertical & 16:9 landscape"
            },
            {
                "scene_number": 2,
                "title": "Core Feature Demonstration",
                "timecode": "00:05 - 00:15",
                "flow_prompt": f"High-resolution screen capture style visualization of {name} interface. Split-screen view showcasing {top_feature_1} and {top_feature_2}. Crisp text rendering with fast terminal execution.",
                "voiceover_script": f"Here is what sets {name} apart: {top_feature_1}, plus {top_feature_2}.",
                "camera": "Pan right across editor UI panels",
                "lighting": "Clean studio lighting, high contrast IDE interface",
                "aspect_ratio_preset": "9:16 vertical & 16:9 landscape"
            },
            {
                "scene_number": 3,
                "title": "Pros & Cons Honest Evaluation",
                "timecode": "00:15 - 00:25",
                "flow_prompt": f"Minimalist sleek HUD graphic overlay on top of editor background. Green checkmark glowing icon for PRO: {top_pro}. Transition to subtle amber caution icon for CON: {top_con}.",
                "voiceover_script": f"The biggest advantage? {top_pro}. On the flip side, keep in mind: {top_con}.",
                "camera": "Static center shot with animated UI cards",
                "lighting": "Soft key light, balanced color contrast",
                "aspect_ratio_preset": "9:16 vertical & 16:9 landscape"
            },
            {
                "scene_number": 4,
                "title": "Pricing & Target Audience Verdict",
                "timecode": "00:25 - 00:35",
                "flow_prompt": f"Dynamic rating badge HUD appearing over developer setup screen with mechanical keyboard. Text badge displays {pricing_type.split('(')[0]}. Final recommendation card slides in.",
                "voiceover_script": f"Pricing breakdown: {pricing_type}. Who is this best for? {who_for}",
                "camera": "Cinematic pull-back tilt shot",
                "lighting": "Warm ambient desktop illumination",
                "aspect_ratio_preset": "9:16 vertical & 16:9 landscape"
            },
            {
                "scene_number": 5,
                "title": "Disclaimer & Channel Call to Action",
                "timecode": "00:35 - 00:40",
                "flow_prompt": f"Elegant dark background with YouTube subscribe animation button and IDE Guide logo. Transparent text card with non-sponsorship disclosure.",
                "voiceover_script": "Subscribe to IDE Guide for daily editor breakdowns! This review is independent and not sponsored.",
                "camera": "Subtle float animation",
                "lighting": "Branded dark studio theme",
                "aspect_ratio_preset": "9:16 vertical & 16:9 landscape"
            }
        ],
        "disclaimer": DISCLAIMER_TEXT,
        "channel_links": {
            "blogger": BLOGGER_URL,
            "youtube": YOUTUBE_URL
        }
    }
    return flow_spec


def main():
    parser = argparse.ArgumentParser(
        description="IDE Guide Agentic Tool: Generate AMP HTML blog post and Google Flow video spec."
    )
    parser.add_argument(
        "--ide",
        type=str,
        required=True,
        help="IDE or Code Editor name (e.g. 'Zed', 'Cursor', 'Neovim', 'VSCodium')"
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default="./output",
        help="Directory where files will be saved (default: ./output)"
    )

    args = parser.parse_args()

    ide_data = fetch_or_build_ide_data(args.ide)
    slug = sanitize_slug(ide_data["name"])

    os.makedirs(args.output_dir, exist_ok=True)

    amp_html = generate_amp_html_blogpost(ide_data)
    amp_filename = os.path.join(args.output_dir, f"{slug}_amp_blogpost.html")
    with open(amp_filename, "w", encoding="utf-8") as f:
        f.write(amp_html)

    flow_spec = generate_google_flow_video_spec(ide_data)
    flow_filename = os.path.join(args.output_dir, f"{slug}_google_flow_spec.json")
    with open(flow_filename, "w", encoding="utf-8") as f:
        json.dump(flow_spec, f, indent=2)

    # Also generate human-readable markdown version of Google Flow spec
    md_filename = os.path.join(args.output_dir, f"{slug}_google_flow_spec.md")
    with open(md_filename, "w", encoding="utf-8") as f:
        f.write(f"# Google Flow Video Spec: {ide_data['name']}\n\n")
        f.write(f"**Channel:** {flow_spec['channel']}\n")
        f.write(f"**Video Title:** {flow_spec['video_title']}\n")
        f.write(f"**Target Platforms:** {', '.join(flow_spec['target_platforms'])}\n\n")
        f.write("--- \n\n")
        for scene in flow_spec["prompts_and_scenes"]:
            f.write(f"### Scene {scene['scene_number']}: {scene['title']} ({scene['timecode']})\n")
            f.write(f"- **Google Flow Prompt:** `{scene['flow_prompt']}`\n")
            f.write(f"- **Voiceover Script:** \"{scene['voiceover_script']}\"\n")
            f.write(f"- **Camera Motion:** {scene['camera']}\n")
            f.write(f"- **Lighting & Environment:** {scene['lighting']}\n\n")
        f.write("---\n\n")
        f.write(f"**Disclaimer:**\n>{DISCLAIMER_TEXT}\n")

    print(f"[SUCCESS] Content generated for '{ide_data['name']}':")
    print(f"  - AMP HTML Blogpost: {amp_filename}")
    print(f"  - Google Flow Spec (JSON): {flow_filename}")
    print(f"  - Google Flow Spec (MD): {md_filename}")


if __name__ == "__main__":
    main()
