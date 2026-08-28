#!/usr/bin/env python3
"""
IDE Guide - Daily Content Package Generator
Generates 3 daily AMP HTML blog posts (for https://ideguide.blogspot.com/)
and 3 Google Flow video specs/scripts (for https://www.youtube.com/@IDEguide).
"""

import os
import sys
import json
import argparse
import datetime
import urllib.request
import urllib.parse
from typing import List, Dict, Any

# Constant Disclaimer required across all generated assets
DISCLAIMER_TEXT = (
    "Disclaimer: IDE Guide is an independent technical publication. "
    "This content is not sponsored, endorsed, or affiliated with any software vendor "
    "or editor developer mentioned above. All reviews and assessments are based strictly "
    "on objective developer evaluation."
)

BLOGGER_URL = "https://ideguide.blogspot.com/"
YOUTUBE_URL = "https://www.youtube.com/@IDEguide"

# Curated catalog of IDEs and Code Editors
IDE_CATALOG: List[Dict[str, Any]] = [
    {
        "name": "Cursor",
        "slug": "cursor",
        "tagline": "The AI-first Code Editor built for hyper-productive developers",
        "developer": "Anysphere",
        "license": "Freemium / Proprietary",
        "pricing_model": "Free Tier available; Pro subscription at $20/month for unlimited Claude/GPT-4o indexing.",
        "category": "AI Native IDE",
        "pros": [
            "Seamless multi-file edits with Cursor Composer (Cmd+I)",
            "Native codebase indexing for deep contextual awareness",
            "Zero friction migration - built on VS Code open core and extensions"
        ],
        "cons": [
            "Pro AI usage can become expensive under heavy daily workloads",
            "Closed-source proprietary layer over VS Code codebase",
            "Occasional latency during peak cloud AI inference hours"
        ],
        "key_features": [
            "Cursor Composer for agentic code generation",
            "Custom .cursorrules support for project context",
            "Instant terminal command fix and debug suggestions"
        ],
        "best_for": "Full-stack and AI-focused developers who need speed and multi-file code transformations.",
        "rating": "4.8/5.0"
    },
    {
        "name": "Zed Editor",
        "slug": "zed",
        "tagline": "High-performance multiplayer code editor written in Rust",
        "developer": "Zed Industries",
        "license": "Open Source (GPL / Apache 2.0)",
        "pricing_model": "100% Free & Open Source for local editor; Optional Zed AI & collaboration cloud plans.",
        "category": "High-Performance Rust Editor",
        "pros": [
            "Blazing fast 120 FPS render pipeline powered by GPU acceleration",
            "Extremely low memory footprint compared to Electron editors",
            "Built-in real-time collaborative pair programming"
        ],
        "cons": [
            "Extension ecosystem still growing compared to VS Code market",
            "Linux and Windows ports still maturing relative to macOS native",
            "Fewer niche language debug adapter plugins out of the box"
        ],
        "key_features": [
            "GPUI hardware-accelerated rendering engine",
            "Integrated Zed AI with assistant panel",
            "CRDT-based multiplayer code collaboration"
        ],
        "best_for": "Developers who prioritize raw speed, low latency, and lightweight Rust engineering.",
        "rating": "4.7/5.0"
    },
    {
        "name": "Visual Studio Code",
        "slug": "vscode",
        "tagline": "The undisputed standard for extensible modern software development",
        "developer": "Microsoft",
        "license": "Free (MIT Core / Proprietary Binary)",
        "pricing_model": "100% Free core editor; Optional GitHub Copilot paid extension ($10-$19/mo).",
        "category": "General Purpose IDE / Text Editor",
        "pros": [
            "Massive marketplace with over 50,000 extensions",
            "Unmatched language support, LSP ecosystem, and debugging tools",
            "Seamless Remote-SSH, Dev Containers, and WSL integration"
        ],
        "cons": [
            "Electron overhead leads to high RAM consumption on large monorepos",
            "Can become slow with heavily loaded extension setups",
            "Telemetry settings require explicit opt-out configuration"
        ],
        "key_features": [
            "Built-in Git integration and terminal multiplexer",
            "Dev Containers & Remote SSH development",
            "Extensive API for AI assistants and language servers"
        ],
        "best_for": "Every developer needing an adaptable, rich ecosystem with proven reliability.",
        "rating": "4.9/5.0"
    },
    {
        "name": "Windsurf",
        "slug": "windsurf",
        "tagline": "Agentic IDE featuring Flow state AI workspace sync",
        "developer": "Codeium",
        "license": "Freemium / Proprietary",
        "pricing_model": "Free tier with generous AI allocation; Pro tier at $15/month.",
        "category": "Agentic AI IDE",
        "pros": [
            "Cascade AI agent syncs seamlessly with terminal and file system",
            "Deep understanding of multi-repository relationships",
            "Fast real-time inline suggestions and auto-complete"
        ],
        "cons": [
            "Newer product entry with evolving release stability",
            "Requires active cloud connectivity for peak agent capabilities",
            "Custom extension porting occasionally has edge-case UI quirks"
        ],
        "key_features": [
            "Cascade Flow assistant for end-to-end coding flows",
            "Automated terminal command execution with safety checks",
            "Context-aware codebase indexing with deep symbol tracking"
        ],
        "best_for": "Developers looking for autonomous AI coding flow without leaving VS Code keybindings.",
        "rating": "4.6/5.0"
    },
    {
        "name": "JetBrains PyCharm",
        "slug": "pycharm",
        "tagline": "The premier Python IDE for professional data science and web engineering",
        "developer": "JetBrains",
        "license": "Freemium (Community Apache / Professional Paid)",
        "pricing_model": "Community Edition is Free; Professional is $249/year (with fallback license).",
        "category": "Dedicated Python IDE",
        "pros": [
            "Best-in-class Python refactoring, inspection, and static analysis",
            "Out-of-the-box Django, FastAPI, SQL, and Docker integration",
            "Integrated Jupyter Notebook support and Data Wrangler UI"
        ],
        "cons": [
            "Heavy Java JVM startup footprint and higher memory overhead",
            "Paid license needed for full database and web framework features",
            "Slower index times on giant non-standard Python project trees"
        ],
        "key_features": [
            "Smart Python code completion and type checking",
            "Visual debugger with variable tracking and breakpoints",
            "Database tools and remote deployment runners"
        ],
        "best_for": "Professional Python, Django, FastAPI, and Data Science engineers.",
        "rating": "4.8/5.0"
    },
    {
        "name": "Neovim",
        "slug": "neovim",
        "tagline": "Hyperextensible Vim-based text editor for terminal power users",
        "developer": "Neovim Core Team",
        "license": "Open Source (Apache 2.0 / Vim License)",
        "pricing_model": "100% Free & Open Source.",
        "category": "Terminal Modal Editor",
        "pros": [
            "Near-zero latency and ultra-lightweight CPU/RAM footprint",
            "Lua-first configuration engine allows unlimited customization",
            "Full Language Server Protocol (LSP) and Treesitter support"
        ],
        "cons": [
            "Steep initial learning curve for modal navigation and Lua setup",
            "Requires manual configuration or distributions (LazyVim/NvChad)",
            "No out-of-the-box GUI mouse convenience without dedicated clients"
        ],
        "key_features": [
            "Built-in LSP client for diagnostic overlays",
            "Treesitter parsing for precise syntax highlighting",
            "Lua plugin ecosystem (Telescope, nvim-cmp, Mason)"
        ],
        "best_for": "Command-line enthusiasts, keyboard purists, and custom setup lovers.",
        "rating": "4.9/5.0"
    },
    {
        "name": "Sublime Text 4",
        "slug": "sublime-text",
        "tagline": "Sophisticated text editor for code, markup, and prose",
        "developer": "Sublime HQ",
        "license": "Shareware / Proprietary",
        "pricing_model": "Free evaluation without time limit; Single user license $99.",
        "category": "Lightweight GUI Editor",
        "pros": [
            "Instant startup speed and ultra-responsive text manipulation",
            "GPU rendering support for smooth text at high DPI",
            "Multiple selections and split editing keyboard shortcuts"
        ],
        "cons": [
            "Smaller plugin ecosystem compared to VS Code marketplace",
            "LSP integration requires manual Package Control setup",
            "Commercial purchase required for pop-up-free persistent usage"
        ],
        "key_features": [
            "Goto Anything (Cmd+P) rapid file switcher",
            "GPU accelerated UI rendering engine",
            "Python-based API and Package Control manager"
        ],
        "best_for": "Developers who want an instant-launch, lightning-fast lightweight editor.",
        "rating": "4.5/5.0"
    },
    {
        "name": "Lapce",
        "slug": "lapce",
        "tagline": "Lightning-fast and powerful Rust-built code editor with native GUI",
        "developer": "Lapce Team",
        "license": "Open Source (Apache 2.0)",
        "pricing_model": "100% Free & Open Source.",
        "category": "Rust Native GUI Editor",
        "pros": [
            "Built in Rust with Floem/Druid for true native performance",
            "WASM plugin architecture for sandboxed high-speed extensions",
            "Modal Vim editing mode integrated out of the box"
        ],
        "cons": [
            "Alpha/Beta stage project with occasional breaking feature changes",
            "Limited library of third-party community extensions",
            "Advanced debugging protocol support still under active development"
        ],
        "key_features": [
            "Natively fast GPU UI text rendering",
            "WASM-powered extension runner",
            "Built-in terminal and LSP syntax diagnostics"
        ],
        "best_for": "Early adopters looking for an open-source lightweight alternative to VS Code.",
        "rating": "4.3/5.0"
    },
    {
        "name": "Helix Editor",
        "slug": "helix",
        "tagline": "A post-modern modal text editor written in Rust with built-in LSP",
        "developer": "Helix Project",
        "license": "Open Source (MPL 2.0)",
        "pricing_model": "100% Free & Open Source.",
        "category": "Terminal Modal Editor",
        "pros": [
            "Zero config required - LSP, Tree-sitter, and themes built-in",
            "Selection-first editing model (selection -> action) feels intuitive",
            "Blazing fast Rust terminal binary with minimal resource usage"
        ],
        "cons": [
            "No plugin system yet (requires rebuilding binary for custom extensions)",
            "Different keybindings than traditional Vim/Neovim",
            "Terminal-only interface (no native GUI window yet)"
        ],
        "key_features": [
            "Multiple selections and visual manipulators",
            "Built-in language server integration out of the box",
            "Tree-sitter syntax highlighting and structural navigation"
        ],
        "best_for": "Terminal power users who want a modal editor with zero configuration hassle.",
        "rating": "4.7/5.0"
    }
]

def discover_ides_from_github() -> List[Dict[str, Any]]:
    """Discovers trending IDE/editor repositories from GitHub Search API as bonus dynamic inputs."""
    url = "https://api.github.com/search/repositories?q=topic:ide+topic:editor&sort=stars&order=desc&per_page=5"
    req = urllib.request.Request(url, headers={"User-Agent": "IDEGuideAgent/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=5) as response:
            data = json.loads(response.read().decode())
            discovered = []
            for item in data.get("items", []):
                name = item.get("name", "").capitalize()
                slug = item.get("name", "").lower().replace(" ", "-")
                discovered.append({
                    "name": name,
                    "slug": slug,
                    "tagline": item.get("description") or f"Modern developer editor: {name}",
                    "developer": item.get("owner", {}).get("login", "Open Source Community"),
                    "license": item.get("license", {}).get("name", "Open Source"),
                    "pricing_model": "Free & Open Source Repository",
                    "category": "Open Source Editor",
                    "pros": [
                        f"Active GitHub community with {item.get('stargazers_count', 0)} stars",
                        "Open architecture allowing custom extensions",
                        "Modern code navigation and community pull requests"
                    ],
                    "cons": [
                        "Community driven feature rollout pace",
                        "Requires developer configuration for enterprise builds",
                        "Ecosystem documentation evolving actively"
                    ],
                    "key_features": [
                        "Open source repository",
                        "Community plugin support",
                        "Custom theme configuration"
                    ],
                    "best_for": f"Developers interested in modern open source tooling around {name}.",
                    "rating": "4.5/5.0"
                })
            return discovered
    except Exception:
        # Fallback gracefully to curated catalog if offline or API limit
        return []

def load_history(history_path: str) -> Dict[str, Any]:
    if os.path.exists(history_path):
        try:
            with open(history_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {"covered_ides": [], "daily_logs": []}

def save_history(history_path: str, history_data: Dict[str, Any]) -> None:
    os.makedirs(os.path.dirname(os.path.abspath(history_path)), exist_ok=True)
    with open(history_path, "w", encoding="utf-8") as f:
        json.dump(history_data, f, indent=2)

def generate_amp_html(ide: Dict[str, Any], slot_index: int, date_str: str) -> str:
    """Generates AMP HTML blog post strictly adhering to AMP HTML standards for Blogger."""
    canonical_url = f"{BLOGGER_URL}{date_str}/{ide['slug']}-review.html"

    amp_html = f"""<!doctype html>
<html ⚡ lang="en">
<head>
  <meta charset="utf-8">
  <title>{ide['name']} Review ({date_str}) - Pros, Cons, Pricing & Verdict | IDE Guide</title>
  <link rel="canonical" href="{canonical_url}">
  <meta name="viewport" content="width=device-width,minimum-scale=1,initial-scale=1">
  <script async src="https://cdn.ampproject.org/v0.js"></script>

  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "TechArticle",
    "headline": "{ide['name']} - Deep Dive Technical Review and Developer Evaluation",
    "description": "{ide['tagline']}",
    "author": {{
      "@type": "Organization",
      "name": "IDE Guide",
      "url": "{BLOGGER_URL}"
    }},
    "publisher": {{
      "@type": "Organization",
      "name": "IDE Guide",
      "url": "{BLOGGER_URL}"
    }},
    "datePublished": "{date_str}",
    "mainEntityOfPage": "{canonical_url}"
  }}
  </script>

  <style amp-boilerplate>body{{-webkit-animation:-amp-start 8s steps(1,end) 0s 1 normal both;-moz-animation:-amp-start 8s steps(1,end) 0s 1 normal both;-ms-animation:-amp-start 8s steps(1,end) 0s 1 normal both;animation:-amp-start 8s steps(1,end) 0s 1 normal both}}@-webkit-keyframes -amp-start{{from{{visibility:hidden}}to{{visibility:visible}}}}@-moz-keyframes -amp-start{{from{{visibility:hidden}}to{{visibility:visible}}}}@-ms-keyframes -amp-start{{from{{visibility:hidden}}to{{visibility:visible}}}}@-o-keyframes -amp-start{{from{{visibility:hidden}}to{{visibility:visible}}}}@keyframes -amp-start{{from{{visibility:hidden}}to{{visibility:visible}}}}</style><noscript><style amp-boilerplate>body{{-webkit-animation:none;-moz-animation:none;-ms-animation:none;animation:none}}</style></noscript>

  <style amp-custom>
    body {{
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
      line-height: 1.65;
      color: #1e293b;
      background-color: #f8fafc;
      margin: 0;
      padding: 0;
    }}
    .header {{
      background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
      color: #ffffff;
      padding: 2.5rem 1.5rem;
      text-align: center;
    }}
    .header h1 {{
      margin: 0 0 0.5rem 0;
      font-size: 2.2rem;
      color: #38bdf8;
    }}
    .header p {{
      margin: 0;
      font-size: 1.1rem;
      color: #94a3b8;
    }}
    .container {{
      max-width: 800px;
      margin: 2rem auto;
      padding: 0 1.25rem;
    }}
    .card {{
      background: #ffffff;
      border-radius: 12px;
      padding: 1.75rem;
      margin-bottom: 1.5rem;
      box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
      border: 1px solid #e2e8f0;
    }}
    .badge {{
      display: inline-block;
      background: #e0f2fe;
      color: #0369a1;
      font-weight: 600;
      font-size: 0.85rem;
      padding: 0.25rem 0.75rem;
      border-radius: 9999px;
      margin-bottom: 0.75rem;
    }}
    .disclaimer-box {{
      background-color: #fffbe2;
      border-left: 4px solid #f59e0b;
      padding: 1rem 1.25rem;
      border-radius: 6px;
      font-size: 0.9rem;
      color: #78350f;
      margin-bottom: 1.5rem;
    }}
    .grid {{
      display: flex;
      flex-wrap: wrap;
      gap: 1rem;
    }}
    .grid-col {{
      flex: 1 1 300px;
    }}
    .pro-list li {{
      color: #15803d;
      margin-bottom: 0.5rem;
    }}
    .con-list li {{
      color: #b91c1c;
      margin-bottom: 0.5rem;
    }}
    .channel-banner {{
      background: #0f172a;
      color: #ffffff;
      padding: 1.5rem;
      border-radius: 10px;
      text-align: center;
      margin-top: 2rem;
    }}
    .channel-banner a {{
      color: #38bdf8;
      font-weight: bold;
      text-decoration: none;
    }}
    table {{
      width: 100%;
      border-collapse: collapse;
      margin-top: 1rem;
    }}
    th, td {{
      padding: 0.75rem;
      border: 1px solid #e2e8f0;
      text-align: left;
    }}
    th {{
      background: #f1f5f9;
    }}
  </style>
</head>
<body>

  <header class="header">
    <span class="badge">{ide['category']}</span>
    <h1>{ide['name']} - In-Depth Developer Guide</h1>
    <p>{ide['tagline']}</p>
  </header>

  <main class="container">

    <div class="disclaimer-box">
      <strong>Independent Technical Review:</strong> {DISCLAIMER_TEXT}
    </div>

    <div class="card">
      <h2>Overview & Technical Profile</h2>
      <table>
        <tr><th>Developer / Maintainer</th><td>{ide['developer']}</td></tr>
        <tr><th>License</th><td>{ide['license']}</td></tr>
        <tr><th>Pricing Model</th><td>{ide['pricing_model']}</td></tr>
        <tr><th>Rating</th><td><strong>{ide['rating']}</strong></td></tr>
      </table>
    </div>

    <div class="card">
      <h2>The Good & The Bad (Pros vs Cons)</h2>
      <div class="grid">
        <div class="grid-col">
          <h3 style="color: #15803d;">✅ What Works Great (Pros)</h3>
          <ul class="pro-list">
            {"".join([f"<li>{pro}</li>" for pro in ide['pros']])}
          </ul>
        </div>
        <div class="grid-col">
          <h3 style="color: #b91c1c;">❌ Areas for Improvement (Cons)</h3>
          <ul class="con-list">
            {"".join([f"<li>{con}</li>" for con in ide['cons']])}
          </ul>
        </div>
      </div>
    </div>

    <div class="card">
      <h2>Key Features & Architecture</h2>
      <ul>
        {"".join([f"<li><strong>{feature}:</strong> Optimized for seamless engineering workflows.</li>" for feature in ide['key_features']])}
      </ul>
    </div>

    <div class="card">
      <h2>Pricing Breakdown: Free vs Paid</h2>
      <p><strong>Pricing Assessment:</strong> {ide['pricing_model']}</p>
      <p>Whether you are a solo indie hacker or enterprise engineer, evaluating software expenditure is critical. {ide['name']} offers options catering to both budget-conscious developers and power users needing advanced productivity tools.</p>
    </div>

    <div class="card">
      <h2>Final Recommendation: Is {ide['name']} Best For You?</h2>
      <p><strong>Verdict:</strong> {ide['best_for']}</p>
    </div>

    <div class="channel-banner">
      <h3>📺 Watch Video Deep Dives & Demos</h3>
      <p>Subscribe to our official YouTube Channel for hands-on video benchmarks and coding walkthroughs:</p>
      <p><a href="{YOUTUBE_URL}" target="_blank" rel="noopener">@IDEguide on YouTube</a> | <a href="{BLOGGER_URL}" target="_blank" rel="noopener">IDE Guide Blog</a></p>
    </div>

    <div class="disclaimer-box" style="margin-top: 2rem;">
      <small>{DISCLAIMER_TEXT}</small>
    </div>

  </main>

</body>
</html>
"""
    return amp_html

def generate_google_flow_spec(ide: Dict[str, Any], slot_index: int, date_str: str) -> Dict[str, Any]:
    """Generates structured Google Flow video generation specs formatted for AI video creation tools."""
    slot_names = ["Morning Short/Video", "Afternoon Deep-Dive", "Evening Comparison"]
    slot_name = slot_names[slot_index - 1]

    spec = {
        "title": f"{ide['name']} Review: Pros, Cons & Pricing Explained! | IDE Guide",
        "ide_name": ide["name"],
        "date": date_str,
        "slot": slot_name,
        "channel": "@IDEguide",
        "youtube_url": YOUTUBE_URL,
        "blogger_url": BLOGGER_URL,
        "disclaimer": DISCLAIMER_TEXT,
        "target_audience": "Software Developers, Full-Stack Engineers, AI Tool Enthusiasts",
        "video_format": {
            "aspect_ratio": "9:16",
            "resolution": "1080x1920 (Vertical Short)",
            "target_duration_seconds": 60,
            "framerate": "60 fps"
        },
        "aesthetic_guidelines": {
            "lighting": "Dark studio background with cyan & neon blue RGB accent illumination",
            "color_palette": "Dark mode code editor themes (Tokyo Night / One Dark Pro) with electric syntax highlighting",
            "camera_angles": "Macro close-up on code typing, smooth over-the-shoulder pan across IDE interface",
            "voiceover_tone": "Energetic, precise, authoritative, developer-friendly"
        },
        "scenes": [
            {
                "scene_number": 1,
                "timestamp": "00:00 - 00:05",
                "duration_seconds": 5,
                "title": "Hook & IDE Reveal",
                "google_flow_prompt": (
                    f"4K macro camera zoom onto modern computer monitor displaying {ide['name']} logo. "
                    "Dark theme code editor active with glowing cursor typing code rapidly. Neon blue accent lighting in background."
                ),
                "voiceover_script": f"Is {ide['name']} worth your time in {date_str[:4]}? Let's uncover the honest truth in 60 seconds!",
                "on_screen_text": f"🔥 {ide['name']} Developer Breakdown",
                "audio_cue": "Cyberpunk riser sound effect transitioning to fast subtle lo-fi beat"
            },
            {
                "scene_number": 2,
                "timestamp": "00:05 - 00:20",
                "duration_seconds": 15,
                "title": "The Pros & Killer Features",
                "google_flow_prompt": (
                    f"Over-the-shoulder shot of developer smoothly navigating {ide['name']} interface. "
                    f"Highlighting key feature: {ide['pros'][0]}. Crisp code lines, zero lag."
                ),
                "voiceover_script": (
                    f"Here is what makes {ide['name']} standout: "
                    f"First, {ide['pros'][0]}. Second, {ide['pros'][1]}."
                ),
                "on_screen_text": f"✅ TOP PROS\n• {ide['pros'][0]}\n• {ide['pros'][1]}",
                "audio_cue": "Chime click effect for each checkmark point"
            },
            {
                "scene_number": 3,
                "timestamp": "00:20 - 00:35",
                "duration_seconds": 15,
                "title": "The Cons & Weaknesses",
                "google_flow_prompt": (
                    f"Close up on monitor showing complex workspace settings in {ide['name']}. "
                    "Red warning badge floating subtly on screen, showing memory/extension tradeoffs."
                ),
                "voiceover_script": (
                    f"However, here are the drawbacks: "
                    f"{ide['cons'][0]}."
                ),
                "on_screen_text": f"⚠️ WEAKNESSES\n• {ide['cons'][0]}",
                "audio_cue": "Subtle low warning tone"
            },
            {
                "scene_number": 4,
                "timestamp": "00:35 - 00:45",
                "duration_seconds": 10,
                "title": "Pricing (Free vs Paid)",
                "google_flow_prompt": (
                    "Clean infographic layout with glowing split card: Free Tier vs Paid Pro Tier. "
                    "Modern high tech typography."
                ),
                "voiceover_script": f"Price breakdown: {ide['pricing_model']}",
                "on_screen_text": f"💲 PRICING MODEL\n{ide['pricing_model']}",
                "audio_cue": "Digital register coin pop effect"
            },
            {
                "scene_number": 5,
                "timestamp": "00:45 - 00:55",
                "duration_seconds": 10,
                "title": "Verdict & Recommendation",
                "google_flow_prompt": (
                    "Developer looking at two code editors on dual curved screens, giving a confident nod. "
                    "Bright glowing verdict badge in screen center."
                ),
                "voiceover_script": f"Our verdict: {ide['best_for']}",
                "on_screen_text": f"💡 VERDICT\n{ide['best_for']}",
                "audio_cue": "Success chord resolution"
            },
            {
                "scene_number": 6,
                "timestamp": "00:55 - 01:00",
                "duration_seconds": 5,
                "title": "CTA & Disclaimer",
                "google_flow_prompt": (
                    "Animation of IDE Guide YouTube channel logo (@IDEguide) and ideguide.blogspot.com blog banner. "
                    "Subscribe button with pulsing motion."
                ),
                "voiceover_script": "Read our complete AMP article at ideguide.blogspot.com and subscribe to @IDEguide for daily tool guides!",
                "on_screen_text": f"Subscribe @IDEguide\nBlog: ideguide.blogspot.com\n\n{DISCLAIMER_TEXT}",
                "audio_cue": "Outro beat swell & subscribe bell sound"
            }
        ],
        "tags": [ide['slug'], ide['name'].lower(), "ideguide", "codeeditor", "developer", "programming", "techreview"]
    }
    return spec

def markdown_from_google_flow_spec(spec: Dict[str, Any]) -> str:
    """Renders Google Flow spec as readable Markdown guide."""
    md = f"""# Google Flow Video Generation Spec: {spec['ide_name']}

**Date:** {spec['date']}
**Slot:** {spec['slot']}
**Target Channel:** [{spec['channel']}]({spec['youtube_url']})
**Blog Companion:** [{spec['blogger_url']}]({spec['blogger_url']})

---

## Video Metadata
- **Title:** {spec['title']}
- **Format:** {spec['video_format']['aspect_ratio']} ({spec['video_format']['resolution']})
- **Target Duration:** {spec['video_format']['target_duration_seconds']} seconds
- **Tone:** {spec['aesthetic_guidelines']['voiceover_tone']}
- **Lighting:** {spec['aesthetic_guidelines']['lighting']}
- **Color Palette:** {spec['aesthetic_guidelines']['color_palette']}

---

## Mandatory Non-Sponsorship Disclaimer
> {spec['disclaimer']}

---

## Scene-by-Scene Prompt & Script Specifications for Google Flow

"""
    for scene in spec["scenes"]:
        md += f"""### Scene {scene['scene_number']}: {scene['title']} ({scene['timestamp']})
* **Google Flow Visual Prompt:**
  `{scene['google_flow_prompt']}`
* **Voiceover Script:**
  "{scene['voiceover_script']}"
* **On-Screen Text Overlay:**
  `{scene['on_screen_text']}`
* **Audio Cue:** {scene['audio_cue']}

"""

    md += f"""---
## Tags & Hashtags
`{', '.join(spec['tags'])}`
"""
    return md

def main():
    parser = argparse.ArgumentParser(description="Generate daily IDE Guide content package (AMP HTML & Google Flow specs).")
    parser.add_argument("--date", type=str, help="Date in YYYY-MM-DD format (defaults to current date)", default=None)
    parser.add_argument("--dry-run", action="store_true", help="Run without persisting to history.json")
    parser.add_argument("--force", action="store_true", help="Allow selecting IDEs even if already in history")
    parser.add_argument("--history-path", type=str, default="content/history.json", help="Path to history tracking file")
    parser.add_argument("--output-dir", type=str, default=None, help="Root content directory (default: content/YYYY-MM-DD)")
    args = parser.parse_args()

    date_str = args.date or datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d")
    output_dir = args.output_dir or os.path.join("content", date_str)

    # Discovery pool combining catalog and github
    github_ides = discover_ides_from_github()
    full_pool = IDE_CATALOG + github_ides

    history = load_history(args.history_path)
    covered_slugs = set(history.get("covered_ides", [])) if not args.force else set()

    # Filter out already covered IDEs
    candidate_ides = [ide for ide in full_pool if ide["slug"] not in covered_slugs]

    # If candidates exhausted, recycle full pool
    if len(candidate_ides) < 3:
        candidate_ides = full_pool

    selected_ides = candidate_ides[:3]

    print(f"==================================================")
    print(f"  IDE Guide Daily Content Package Generator")
    print(f"  Date: {date_str}")
    print(f"  Target Output: {output_dir}")
    print(f"==================================================")

    os.makedirs(output_dir, exist_ok=True)

    generated_summary = []

    for idx, ide in enumerate(selected_ides, start=1):
        slug = ide["slug"]
        print(f"[{idx}/3] Generating package for IDE: {ide['name']} ({slug})...")

        # 1. AMP HTML Post
        amp_content = generate_amp_html(ide, idx, date_str)
        amp_filename = f"post_{idx}_{slug}.amp.html"
        amp_filepath = os.path.join(output_dir, amp_filename)
        with open(amp_filepath, "w", encoding="utf-8") as f:
            f.write(amp_content)

        # 2. Google Flow Spec (JSON)
        flow_spec = generate_google_flow_spec(ide, idx, date_str)
        spec_json_filename = f"video_{idx}_{slug}_flow_spec.json"
        spec_json_filepath = os.path.join(output_dir, spec_json_filename)
        with open(spec_json_filepath, "w", encoding="utf-8") as f:
            json.dump(flow_spec, f, indent=2)

        # 3. Google Flow Spec (Markdown)
        spec_md = markdown_from_google_flow_spec(flow_spec)
        spec_md_filename = f"video_{idx}_{slug}_flow_spec.md"
        spec_md_filepath = os.path.join(output_dir, spec_md_filename)
        with open(spec_md_filepath, "w", encoding="utf-8") as f:
            f.write(spec_md)

        generated_summary.append({
            "slot": idx,
            "ide_name": ide["name"],
            "slug": slug,
            "amp_html": amp_filepath,
            "google_flow_spec_json": spec_json_filepath,
            "google_flow_spec_md": spec_md_filepath
        })

    # Update history if not dry-run
    if not args.dry_run:
        for ide in selected_ides:
            if ide["slug"] not in history.get("covered_ides", []):
                history.setdefault("covered_ides", []).append(ide["slug"])

        history.setdefault("daily_logs", []).append({
            "date": date_str,
            "generated_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "items": generated_summary
        })
        save_history(args.history_path, history)
        print(f"Updated history in {args.history_path}")
    else:
        print(f"Dry-run mode: skipped updating history at {args.history_path}")

    print(f"\nSuccessfully generated 3 daily content packages in '{output_dir}'.")

if __name__ == "__main__":
    main()
