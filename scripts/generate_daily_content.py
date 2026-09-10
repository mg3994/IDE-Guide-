#!/usr/bin/env python3
"""
IDE Guide - Daily Content Generator
Generates 3 AMP HTML blog posts for Blogger and 3 Google Flow video generation specs
for YouTube per day, ensuring fresh content without duplicate coverage.
"""

import json
import os
import sys
import datetime
import urllib.request
import urllib.error

HISTORY_FILE = os.path.join(os.path.dirname(__file__), "..", "content", "history.json")
CONTENT_DIR = os.path.join(os.path.dirname(__file__), "..", "content")

MANDATORY_DISCLAIMER = (
    "Disclaimer: IDE Guide is an independent technical publication. This content is not sponsored, "
    "endorsed, or affiliated with any software vendor or editor developer mentioned above. "
    "All reviews and assessments are based strictly on objective developer evaluation."
)

CURATED_IDE_DATABASE = [
    {
        "name": "Cursor AI",
        "category": "AI Code Editor",
        "tagline": "The AI-first Code Editor built for hyper-productive developers",
        "description": "Cursor is a fork of VS Code deeply integrated with OpenAI GPT-4o, Claude 3.5 Sonnet, and custom codebase indexing for instant inline edits and multi-file code generation.",
        "pricing_model": "Freemium",
        "pricing_details": "Free tier with limited fast AI uses; Pro plan at $20/month with unlimited fast queries and Claude 3.5 Sonnet access.",
        "pros": [
            "Native codebase indexing with instant context aware answers",
            "Full VS Code extension and theme ecosystem compatibility",
            "Cursor Agent mode for multi-file editing and autonomous bug fixing"
        ],
        "cons": [
            "Requires active subscription for heavy AI query usage",
            "Proprietary cloud processing required for codebase embedding"
        ],
        "best_for": "Developers wanting seamless AI auto-completion, multi-file refactoring, and natural language code generation.",
        "url": "https://www.cursor.com"
    },
    {
        "name": "Zed Editor",
        "category": "High-Performance Code Editor",
        "tagline": "High-performance, multiplayer code editor written in Rust",
        "description": "Created by the original team behind Atom and Tree-sitter, Zed leverages GPU acceleration and Rust concurrency to offer lightning-fast typing latency and real-time collaboration.",
        "pricing_model": "Free & Open Source",
        "pricing_details": "Core editor is 100% free and open-source (GPL/AGPL/Apache). Optional cloud teamwork server subscriptions available.",
        "pros": [
            "Blazing fast startup time and low memory footprint GPU rendering",
            "Built-in multiplayer pair-programming and real-time screen sharing",
            "Native inline AI assistants supporting Claude, OpenAI, and Ollama"
        ],
        "cons": [
            "Ecosystem of third-party extensions is still maturing",
            "Non-macOS platforms support is under active rapid development"
        ],
        "best_for": "Developers seeking ultra-fast responsiveness, zero input lag, and built-in pair programming.",
        "url": "https://zed.dev"
    },
    {
        "name": "Windsurf Editor",
        "category": "AI Flow State Editor",
        "tagline": "The first agentic IDE powered by Cascade AI flow engine",
        "description": "Developed by Codeium, Windsurf combines deep understanding of developer context with AI agents that keep you in flow state, featuring realtime file sync and command execution.",
        "pricing_model": "Freemium",
        "pricing_details": "Generous free tier with Cascade AI features; Pro plan starting at $15/month for unlimited agentic execution.",
        "pros": [
            "Cascade AI agent understands entire repository context dynamically",
            "Superb free tier compared to competitors",
            "Rich VS Code ecosystem extension compatibility"
        ],
        "cons": [
            "Newer platform with evolving UI features",
            "Heavy agent operations require steady internet connectivity"
        ],
        "best_for": "Full-stack developers looking for an AI agent that automates complex multi-step refactoring.",
        "url": "https://codeium.com/windsurf"
    },
    {
        "name": "Neovim",
        "category": "Terminal Modal Editor",
        "tagline": "Hyperextensible Vim-based text editor for power terminal users",
        "description": "Neovim seeks to aggressively refactor Vim to simplify maintenance, enable modern Lua configuration, and embed rich asynchronous terminal workflows.",
        "pricing_model": "100% Free & Open Source",
        "pricing_details": "Completely free open-source software maintained by community sponsors.",
        "pros": [
            "Extremely lightweight, modal navigation, runs on remote SSH seamlessly",
            "Powerful Lua configuration ecosystem with Lazy.nvim and Mason.nvim",
            "Built-in Language Server Protocol (LSP) and Treesitter support"
        ],
        "cons": [
            "Steep learning curve for keyboard shortcut mastery",
            "Requires initial setup time to configure tailored development environment"
        ],
        "best_for": "Power keyboard-centric developers, DevOps engineers, and Linux terminal enthusiasts.",
        "url": "https://neovim.io"
    },
    {
        "name": "Fleet by JetBrains",
        "category": "Polyglot Lightweight IDE",
        "tagline": "Lightweight editor with full JetBrains smart engine integration",
        "description": "Fleet is JetBrains' modern polyglot editor built from scratch using Kotlin. It starts as a lightning-fast editor and morphs into a full IDE with Smart Mode on demand.",
        "pricing_model": "Freemium / Paid",
        "pricing_details": "Free during preview; available standalone or via JetBrains All Products Pack subscription.",
        "pros": [
            "Clean minimal modern interface with distributed architecture",
            "Seamless switch between fast text editor and full JetBrains smart code engine",
            "Built-in collaborative editing and remote machine connectivity"
        ],
        "cons": [
            "Plugins ecosystem still smaller than IntelliJ IDEA platform",
            "Requires JetBrains account ecosystem connection"
        ],
        "best_for": "Developers working with Kotlin, Java, Python, and Rust who want a fast, minimal JetBrains experience.",
        "url": "https://www.jetbrains.com/fleet"
    },
    {
        "name": "Lapce",
        "category": "Open Source GPU Editor",
        "tagline": "Lightning fast and powerful code editor written in Rust with Druid GUI",
        "description": "Lapce is designed with native GUI performance using Rust, Druid, and Xi-Editor concepts, featuring remote development capabilities and WASI plugin system.",
        "pricing_model": "100% Free & Open Source",
        "pricing_details": "Completely free open-source software under Apache License 2.0.",
        "pros": [
            "Native GPU-accelerated interface with near-zero input latency",
            "Built-in terminal and LSP protocol support without bloated web views",
            "WASI sandboxed plugins for secure custom extensions"
        ],
        "cons": [
            "Earlier stage of development compared to VS Code",
            "Community plugin market is steadily growing"
        ],
        "best_for": "Rust enthusiasts and developers seeking a non-Electron native open source code editor.",
        "url": "https://lapce.dev"
    }
]

def load_history():
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {"covered_ides": [], "daily_runs": []}

def save_history(history):
    os.makedirs(os.path.dirname(HISTORY_FILE), exist_ok=True)
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=2)

def fetch_github_trending_editors():
    """Attempt to discover code editor repositories on GitHub."""
    url = "https://api.github.com/search/repositories?q=topic:code-editor+topic:ide&sort=stars&order=desc"
    req = urllib.request.Request(url, headers={"User-Agent": "IDEGuide-Generator"})
    discovered = []
    try:
        with urllib.request.urlopen(req, timeout=5) as response:
            if response.status == 200:
                data = json.loads(response.read().decode("utf-8"))
                for item in data.get("items", [])[:10]:
                    discovered.append({
                        "name": item.get("name").capitalize(),
                        "category": "Open Source Code Editor",
                        "tagline": item.get("description", "Modern code editor repository on GitHub"),
                        "description": item.get("description", "High quality open source development environment."),
                        "pricing_model": "Free & Open Source",
                        "pricing_details": f"100% Open source project under {item.get('license', {}).get('name', 'Open Source License')}.",
                        "pros": [
                            f"Over {item.get('stargazers_count', 0)} stars on GitHub",
                            "Active open source community development",
                            "Transparent source code and extensible architecture"
                        ],
                        "cons": [
                            "Community-driven support and fast evolving release cycle"
                        ],
                        "best_for": "Developers wanting an open-source, flexible coding environment.",
                        "url": item.get("html_url")
                    })
    except Exception:
        pass
    return discovered

def get_todays_ides(count=3):
    history = load_history()
    covered = set(history.get("covered_ides", []))
    selected = []

    # Check curated list first
    for item in CURATED_IDE_DATABASE:
        if item["name"].lower() not in covered:
            selected.append(item)
            if len(selected) == count:
                break

    # If count not met, try GitHub API
    if len(selected) < count:
        gh_items = fetch_github_trending_editors()
        for item in gh_items:
            if item["name"].lower() not in covered and not any(s["name"].lower() == item["name"].lower() for s in selected):
                selected.append(item)
                if len(selected) == count:
                    break

    # Fallback to curated cycling if all covered
    if len(selected) < count:
        for item in CURATED_IDE_DATABASE:
            if not any(s["name"].lower() == item["name"].lower() for s in selected):
                selected.append(item)
                if len(selected) == count:
                    break

    return selected[:count]

def generate_amp_html(ide_info):
    name = ide_info["name"]
    category = ide_info["category"]
    tagline = ide_info["tagline"]
    desc = ide_info["description"]
    pricing_model = ide_info["pricing_model"]
    pricing_details = ide_info["pricing_details"]
    pros_html = "".join([f"<li>{p}</li>" for p in ide_info["pros"]])
    cons_html = "".join([f"<li>{c}</li>" for c in ide_info["cons"]])
    best_for = ide_info["best_for"]
    official_url = ide_info["url"]

    amp_content = f"""<!doctype html>
<html ⚡ lang="en">
<head>
  <meta charset="utf-8">
  <title>{name} Review - Best Features, Pricing, Good & Bad | IDE Guide</title>
  <link rel="canonical" href="{official_url}">
  <meta name="viewport" content="width=device-width,minimum-scale=1,initial-scale=1">
  <script async src="https://cdn.ampproject.org/v0.js"></script>
  <style amp-boilerplate>body{{-webkit-animation:-amp-start 8s steps(1,end) 0s 1 normal both;-moz-animation:-amp-start 8s steps(1,end) 0s 1 normal both;-ms-animation:-amp-start 8s steps(1,end) 0s 1 normal both;animation:-amp-start 8s steps(1,end) 0s 1 normal both}}@-webkit-keyframes -amp-start{{from{{visibility:hidden}}to{{visibility:visible}}}}@-moz-keyframes -amp-start{{from{{visibility:hidden}}to{{visibility:visible}}}}@-ms-keyframes -amp-start{{from{{visibility:hidden}}to{{visibility:visible}}}}@-o-keyframes -amp-start{{from{{visibility:hidden}}to{{visibility:visible}}}}@keyframes -amp-start{{from{{visibility:hidden}}to{{visibility:visible}}}}</style><noscript><style amp-boilerplate>body{{-webkit-animation:none;-moz-animation:none;-ms-animation:none;animation:none}}</style></noscript>
  <style amp-custom>
    body {{
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
      line-height: 1.6;
      color: #e0e6ed;
      background-color: #0f172a;
      padding: 16px;
      max-width: 800px;
      margin: 0 auto;
    }}
    header {{
      text-align: center;
      border-bottom: 2px solid #334155;
      padding-bottom: 20px;
      margin-bottom: 24px;
    }}
    .badge {{
      background-color: #0284c7;
      color: #ffffff;
      font-size: 0.85rem;
      padding: 4px 12px;
      border-radius: 9999px;
      text-transform: uppercase;
      font-weight: bold;
      display: inline-block;
      margin-bottom: 8px;
    }}
    h1 {{
      color: #f8fafc;
      font-size: 2rem;
      margin-top: 8px;
    }}
    .tagline {{
      color: #94a3b8;
      font-style: italic;
      font-size: 1.1rem;
    }}
    .hero-img-container {{
      text-align: center;
      margin: 24px 0;
    }}
    .section-card {{
      background: #1e293b;
      padding: 20px;
      border-radius: 12px;
      margin-bottom: 20px;
      border: 1px solid #334155;
    }}
    .section-title {{
      color: #38bdf8;
      margin-top: 0;
      font-size: 1.3rem;
      border-bottom: 1px solid #334155;
      padding-bottom: 8px;
    }}
    .pros-cons-grid {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 16px;
    }}
    @media(max-width: 600px) {{
      .pros-cons-grid {{ grid-template-columns: 1fr; }}
    }}
    .pros-box {{ background: #064e3b; padding: 12px; border-radius: 8px; border-left: 4px solid #10b981; }}
    .cons-box {{ background: #7f1d1d; padding: 12px; border-radius: 8px; border-left: 4px solid #ef4444; }}
    .pros-box h3, .cons-box h3 {{ margin-top: 0; color: #ffffff; }}
    ul {{ padding-left: 20px; margin-bottom: 0; }}
    li {{ margin-bottom: 6px; }}
    .pricing-tag {{
      display: inline-block;
      background: #8b5cf6;
      color: #ffffff;
      padding: 4px 10px;
      border-radius: 6px;
      font-weight: bold;
      margin-bottom: 8px;
    }}
    .disclaimer {{
      background: #0f172a;
      border: 1px solid #f59e0b;
      color: #fbbf24;
      padding: 16px;
      border-radius: 8px;
      font-size: 0.88rem;
      margin-top: 32px;
      text-align: center;
    }}
    .cta-btn {{
      display: block;
      width: 100%;
      text-align: center;
      background: #2563eb;
      color: #ffffff;
      padding: 12px;
      border-radius: 8px;
      text-decoration: none;
      font-weight: bold;
      margin-top: 16px;
    }}
  </style>
</head>
<body>

  <header>
    <span class="badge">{category}</span>
    <h1>{name} Complete Developer Guide & Assessment</h1>
    <p class="tagline">"{tagline}"</p>
  </header>

  <div class="hero-img-container">
    <amp-img src="https://images.unsplash.com/photo-1555066931-4365d14bab8c?w=800&auto=format&fit=crop" width="800" height="450" layout="responsive" alt="{name} Code Editor Overview"></amp-img>
  </div>

  <div class="section-card">
    <h2 class="section-title">Overview & What Makes It Unique</h2>
    <p>{desc}</p>
  </div>

  <div class="section-card">
    <h2 class="section-title">The Good & The Bad (Pros & Cons)</h2>
    <div class="pros-cons-grid">
      <div class="pros-box">
        <h3>👍 The Good (Pros)</h3>
        <ul>
          {pros_html}
        </ul>
      </div>
      <div class="cons-box">
        <h3>👎 The Bad (Cons)</h3>
        <ul>
          {cons_html}
        </ul>
      </div>
    </div>
  </div>

  <div class="section-card">
    <h2 class="section-title">Pricing Model & Value Breakdown</h2>
    <span class="pricing-tag">{pricing_model}</span>
    <p>{pricing_details}</p>
  </div>

  <div class="section-card">
    <h2 class="section-title">Verdict & Recommendation</h2>
    <p><strong>Who is {name} best for?</strong> {best_for}</p>
    <a href="{official_url}" target="_blank" rel="noopener" class="cta-btn">Try {name} Official Website</a>
  </div>

  <div class="disclaimer">
    <p>{MANDATORY_DISCLAIMER}</p>
  </div>

</body>
</html>
"""
    return amp_content

def generate_google_flow_spec(ide_info):
    name = ide_info["name"]
    tagline = ide_info["tagline"]
    category = ide_info["category"]
    pricing_model = ide_info["pricing_model"]
    pros = ide_info["pros"]
    cons = ide_info["cons"]
    best_for = ide_info["best_for"]

    spec = {
        "title": f"{name} Code Editor Review | Is It Best for You? (@IDEguide)",
        "target_platform": "YouTube / Shorts / Google Flow",
        "aspect_ratio": "9:16 Vertical (Shorts) & 16:9 Horizontal (Long form)",
        "branding": {
            "channel_name": "IDE Guide",
            "youtube_handle": "@IDEguide",
            "blog_url": "https://ideguide.blogspot.com/"
        },
        "non_sponsorship_disclaimer": MANDATORY_DISCLAIMER,
        "editor_metadata": {
            "name": name,
            "category": category,
            "pricing": pricing_model,
            "tagline": tagline
        },
        "scenes": [
            {
                "scene_number": 1,
                "duration_seconds": 5,
                "scene_type": "Hook & Title",
                "visual_prompt": f"Cinematic close-up macro shot of dark-mode code editor interface showing high contrast glowing syntax highlighting. Overlay bold title: '{name}: Is it Worth It?'. Sleek studio desk environment with cyan and purple LED backlight.",
                "camera_motion": "Slow zoom in on the glowing editor cursor",
                "lighting": "Dark room key light with vibrant 5600K cyan and purple accent lighting",
                "voiceover": f"Looking for the ultimate coding setup? Today on IDE Guide, we are breaking down {name}—the {category.lower()} that claims to revolutionize your workflow.",
                "on_screen_text": f"{name} Review | IDE Guide"
            },
            {
                "scene_number": 2,
                "duration_seconds": 15,
                "scene_type": "Key Features & The Good",
                "visual_prompt": f"Split screen view of {name} executing code seamlessly. Visual overlay icons highlighting feature performance. Smooth high tech UI animation.",
                "camera_motion": "Smooth pan right across code editor panels",
                "lighting": "Clean modern developer aesthetic with emerald green highlight glow",
                "voiceover": f"Here is what makes {name} stand out: {pros[0] if pros else tagline}. Plus, {pros[1] if len(pros) > 1 else 'great performance'}.",
                "on_screen_text": f"Pros: {pros[0] if pros else 'High performance'}"
            },
            {
                "scene_number": 3,
                "duration_seconds": 15,
                "scene_type": "The Bad & Drawbacks",
                "visual_prompt": f"Close up on error log or complex settings panel in {name} with a subtle amber highlight overlay indicating potential friction points.",
                "camera_motion": "Static macro focus with subtle floating red indicator callouts",
                "lighting": "Moody warm ambient light with subtle red/orange rim lighting",
                "voiceover": f"However, it is not perfect. The drawbacks you should know: {cons[0] if cons else 'minor learning curve'}.",
                "on_screen_text": f"Cons: {cons[0] if cons else 'Learning Curve'}"
            },
            {
                "scene_number": 4,
                "duration_seconds": 10,
                "scene_type": "Pricing & Recommendation",
                "visual_prompt": f"High quality graphic card displaying '{pricing_model}' tag over a sleek dark developer workspace background.",
                "camera_motion": "Direct pull-back shot framing workspace setup",
                "lighting": "Balanced neutral white studio key light",
                "voiceover": f"Pricing wise, {name} is {pricing_model}. Bottom line: {best_for}",
                "on_screen_text": f"Pricing: {pricing_model}"
            },
            {
                "scene_number": 5,
                "duration_seconds": 10,
                "scene_type": "CTA & Disclaimer",
                "visual_prompt": "Clean graphic displaying IDE Guide YouTube logo, Subscribe button animation, and Blogger site URL. Text overlay for disclaimer.",
                "camera_motion": "Gentle zoom out",
                "lighting": "Soft glow branding backlight",
                "voiceover": "Subscribe to IDE Guide for daily unbiased code editor reviews. Visit ideguide.blogspot.com for the full AMP post!",
                "on_screen_text": "Subscribe @IDEguide | ideguide.blogspot.com\nIndependent & Non-Sponsored Review"
            }
        ]
    }
    return spec

def main():
    date_str = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d")
    output_dir = os.path.join(CONTENT_DIR, date_str)
    os.makedirs(output_dir, exist_ok=True)

    history = load_history()
    selected_ides = get_todays_ides(3)

    print(f"Generating content for date: {date_str}")
    for idx, ide in enumerate(selected_ides, 1):
        clean_name = ide["name"].lower().replace(" ", "_").replace("/", "_")

        # 1. Generate AMP HTML Post
        amp_html = generate_amp_html(ide)
        blog_filename = f"blog_post_{idx}_{clean_name}.amp.html"
        blog_filepath = os.path.join(output_dir, blog_filename)
        with open(blog_filepath, "w", encoding="utf-8") as f:
            f.write(amp_html)
        print(f"  [+] Created AMP HTML Post: {blog_filepath}")

        # 2. Generate Google Flow Video Spec
        flow_spec = generate_google_flow_spec(ide)
        video_filename = f"video_spec_{idx}_{clean_name}.json"
        video_filepath = os.path.join(output_dir, video_filename)
        with open(video_filepath, "w", encoding="utf-8") as f:
            json.dump(flow_spec, f, indent=2)
        print(f"  [+] Created Google Flow Spec: {video_filepath}")

        # Record in history
        if ide["name"].lower() not in [x.lower() for x in history.get("covered_ides", [])]:
            history.setdefault("covered_ides", []).append(ide["name"].lower())

    history.setdefault("daily_runs", []).append({
        "date": date_str,
        "ides_covered": [i["name"] for i in selected_ides]
    })
    save_history(history)
    print("Daily content generation successfully completed!")

if __name__ == "__main__":
    main()
