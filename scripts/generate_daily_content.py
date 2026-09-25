#!/usr/bin/env python3
"""
IDE Guide - Daily Content Generator
Generates 3 AMP HTML blog posts and 3 Google Flow video specifications daily.
Output directory: content/YYYY-MM-DD/
History tracking: content/history.json
Target Blog: https://ideguide.blogspot.com/
Target YouTube: https://www.youtube.com/@IDEguide
"""

import os
import json
import re
import datetime
import urllib.request
import urllib.error
from typing import List, Dict, Any, Optional

DISCLAIMER_TEXT = (
    "Disclaimer: IDE Guide is an independent technical publication. "
    "This content is not sponsored, endorsed, or affiliated with any software vendor "
    "or editor developer mentioned above. All reviews and assessments are based strictly "
    "on objective developer evaluation."
)

IDE_DATABASE = [
    {
        "id": "vscode",
        "name": "Visual Studio Code",
        "developer": "Microsoft",
        "category": "Extensible General Purpose Editor",
        "license_type": "Free / Open Source Core (MIT / Proprietary build)",
        "pricing": "100% Free",
        "pros": [
            "Massive ecosystem of over 50,000 extensions",
            "Unrivaled language support and LSP integration",
            "Built-in Git GUI, terminal, and debugging capabilities",
            "Fast startup and low resource overhead compared to heavy IDEs"
        ],
        "cons": [
            "Requires heavy extension configuration for full IDE feature parity",
            "Electron-based memory consumption can grow with heavy plugins",
            "Telemetry collection enabled by default (can be disabled)"
        ],
        "best_for": "Web developers, Python scripts, multi-language polyglot engineers",
        "summary": "The gold standard of modern lightweight code editors with unlimited extensibility.",
        "rating": "4.8/5.0",
        "website": "https://code.visualstudio.com/",
        "github_repo": "microsoft/vscode"
    },
    {
        "id": "cursor",
        "name": "Cursor AI",
        "developer": "Anysphere",
        "category": "AI-Native Code Editor",
        "license_type": "Freemium / Proprietary",
        "pricing": "Free tier available; Pro at $20/month",
        "pros": [
            "Deep repository-wide indexing for instant context-aware code generation",
            "Native AI chat, inline edits (Cmd+K), and multi-file auto-refactoring",
            "Forked from VS Code, ensuring 100% extension compatibility",
            "Fast Claude 3.5 Sonnet & GPT-4o integration"
        ],
        "cons": [
            "Requires active internet connection for advanced AI features",
            "Privacy concerns for enterprise codebases without enterprise plan",
            "Free tier request limits exhaust quickly on active coding days"
        ],
        "best_for": "Developers seeking maximum productivity through cutting-edge AI assistance",
        "summary": "The leading AI-native editor revolutionizing software development velocity.",
        "rating": "4.7/5.0",
        "website": "https://www.cursor.com/",
        "github_repo": "getcursor/cursor"
    },
    {
        "id": "zed",
        "name": "Zed Editor",
        "developer": "Zed Industries",
        "category": "High-Performance Rust-Based Editor",
        "license_type": "Open Source (GPL/Apache 2.0)",
        "pricing": "100% Free for local use; Paid server collaboration tiers",
        "pros": [
            "Blazing fast performance written in Rust with GPU acceleration",
            "Sub-millisecond latency and instant startup times",
            "Built-in real-time collaborative editing (multiplayer coding)",
            "Native integrated AI assistant (Anthropic & OpenAI APIs)"
        ],
        "cons": [
            "Smaller extension ecosystem compared to VS Code",
            "Linux and Windows support is newer than macOS build",
            "Fewer built-in debugging visualizers"
        ],
        "best_for": "Systems programmers, Rust/C++/Go devs, and performance enthusiasts",
        "summary": "Next-generation code editor built in Rust for lightning speed.",
        "rating": "4.6/5.0",
        "website": "https://zed.dev/",
        "github_repo": "zed-industries/zed"
    },
    {
        "id": "pycharm",
        "name": "JetBrains PyCharm",
        "developer": "JetBrains",
        "category": "Dedicated Python IDE",
        "license_type": "Freemium (Community / Professional)",
        "pricing": "Free Community Edition; $249/yr Professional Edition",
        "pros": [
            "Unmatched Python code intelligence, refactoring, and linting",
            "Deep Django, Flask, FastAPI, and Data Science tooling",
            "Powerful built-in database management and remote deployment",
            "Excellent visual debugger and test runner"
        ],
        "cons": [
            "Higher memory footprint (JVM-based)",
            "Slower cold startup compared to text editors",
            "Advanced web framework features locked behind paid Professional tier"
        ],
        "best_for": "Professional Python developers, Data Scientists, and Django engineers",
        "summary": "The undisputed titan of Python IDEs offering deep static analysis.",
        "rating": "4.8/5.0",
        "website": "https://www.jetbrains.com/pycharm/",
        "github_repo": "JetBrains/intellij-community"
    },
    {
        "id": "neovim",
        "name": "Neovim",
        "developer": "Neovim Core Team",
        "category": "Modal Terminal-Based Text Editor",
        "license_type": "Open Source (Apache 2.0 / Vim License)",
        "pricing": "100% Free",
        "pros": [
            "Extreme speed, zero bloat, runs inside any SSH session or terminal",
            "Lua scripting engine for limitless custom configurations",
            "Built-in Language Server Protocol (LSP) client",
            "Ergonomic modal editing reduces wrist strain"
        ],
        "cons": [
            "Steep learning curve for Vim keybindings",
            "Requires time investment to configure custom development environment",
            "No out-of-the-box GUI without third-party wrappers like Neovide"
        ],
        "best_for": "Terminal lovers, DevOps engineers, and keyboard power users",
        "summary": "Hyperefficient modal editor engineered for speed and ultimate customizability.",
        "rating": "4.9/5.0",
        "website": "https://neovim.io/",
        "github_repo": "neovim/neovim"
    },
    {
        "id": "sublime",
        "name": "Sublime Text 4",
        "developer": "Sublime HQ",
        "category": "Lightweight High-Speed Editor",
        "license_type": "Proprietary Shareware",
        "pricing": "Free trial (unlimited duration with gentle reminder popups); $99 license",
        "pros": [
            "Instantaneous file loading and lightning-quick Search in Files",
            "GPU rendering engine for fluid 120Hz scrolling",
            "Minimal CPU and RAM consumption",
            "Python API for Package Control plugins"
        ],
        "cons": [
            "Paid license required for continuous commercial pop-up-free use",
            "Out-of-the-box LSP and debugging require plugin setup",
            "Smaller plugin community than VS Code"
        ],
        "best_for": "Developers who prioritize raw editing speed and minimal RAM usage",
        "summary": "The classic benchmark for ultra-responsive desktop code editing.",
        "rating": "4.5/5.0",
        "website": "https://www.sublimetext.com/",
        "github_repo": "sublimehq/sublime_text"
    },
    {
        "id": "windsurf",
        "name": "Windsurf Editor",
        "developer": "Codeium",
        "category": "Agentic AI Cascade Editor",
        "license_type": "Freemium / Proprietary",
        "pricing": "Free tier; Pro plan at $15/month",
        "pros": [
            "Cascade AI agent that performs end-to-end multi-file edits autonomously",
            "Deep context awareness with real-time terminal error auto-fixing",
            "VS Code extension compatibility out of the box",
            "Extremely competitive pricing model"
        ],
        "cons": [
            "Newer platform with rapid weekly updates",
            "Requires internet connectivity for Cascade AI flow",
            "Can occasionally hallucinate complex multi-file refactors"
        ],
        "best_for": "Full-stack developers looking for autonomous AI coding agents",
        "summary": "Next-gen agentic IDE powered by Codeium's Cascade AI workflow.",
        "rating": "4.7/5.0",
        "website": "https://codeium.com/windsurf",
        "github_repo": "Exafunction/codeium"
    },
    {
        "id": "fleet",
        "name": "JetBrains Fleet",
        "developer": "JetBrains",
        "category": "Lightweight Polyglot Smart Editor",
        "license_type": "Freemium / Proprietary",
        "pricing": "Free Preview; Subscription tier for enterprise smart features",
        "pros": [
            "Starts instantly as a lightweight editor, turns into a full IDE on demand",
            "Built from scratch with modern distributed architecture",
            "Native JetBrains Smart Mode engine for code completion",
            "Built-in collaborative pair programming"
        ],
        "cons": [
            "Still evolving during preview phase",
            "Fewer plugins available compared to JetBrains Marketplace",
            "Requires Smart Mode toggle for full intelligence"
        ],
        "best_for": "Polyglot developers wanting JetBrains power in a fast VS Code rival",
        "summary": "JetBrains' sleek, lightweight answer to modern polyglot editors.",
        "rating": "4.4/5.0",
        "website": "https://www.jetbrains.com/fleet/",
        "github_repo": "JetBrains/fleet"
    },
    {
        "id": "replit",
        "name": "Replit Agent",
        "developer": "Replit",
        "category": "Cloud-Based AI IDE",
        "license_type": "Freemium / Cloud Service",
        "pricing": "Free starter tier; Core plan $20/month; Agent usage credits",
        "pros": [
            "Zero local setup required; code runs instantly in cloud containers",
            "Replit Agent can build and deploy full stack web apps from text prompts",
            "Instant live hosting with custom domains and database support",
            "Seamless mobile and tablet browser editing"
        ],
        "cons": [
            "Requires continuous internet connection",
            "Cloud computing limits on free tier",
            "Not suited for offline desktop application development"
        ],
        "best_for": "Beginners, rapid prototypers, hackathons, and cloud-first developers",
        "summary": "Cloud-native AI development platform that builds and deploys in seconds.",
        "rating": "4.6/5.0",
        "website": "https://replit.com/",
        "github_repo": "replit/replit"
    },
    {
        "id": "vscodium",
        "name": "VSCodium",
        "developer": "VSCodium Community",
        "category": "Privacy-Focused Open Source Editor",
        "license_type": "Open Source (MIT)",
        "pricing": "100% Free",
        "pros": [
            "Clean build of VS Code with 0% telemetry and Microsoft tracking disabled",
            "100% free and open-source software license binaries",
            "Uses Open VSX Registry for privacy-respecting extension downloads",
            "Identical UI and core capabilities to VS Code"
        ],
        "cons": [
            "Proprietary Microsoft extensions (like official C# / Pylance) require workaround",
            "Requires manually changing extension market URL for some plugins",
            "Delayed release builds relative to official VS Code by a few hours"
        ],
        "best_for": "Privacy purists, open-source advocates, and enterprise compliance teams",
        "summary": "Telemetry-free open source binary distribution of VS Code.",
        "rating": "4.8/5.0",
        "website": "https://vscodium.com/",
        "github_repo": "VSCodium/vscodium"
    },
    {
        "id": "intellij",
        "name": "JetBrains IntelliJ IDEA",
        "developer": "JetBrains",
        "category": "Enterprise Java & Kotlin IDE",
        "license_type": "Freemium (Community / Ultimate)",
        "pricing": "Free Community Edition; $599/yr Ultimate Edition",
        "pros": [
            "Deepest Java & Kotlin refactoring, static analysis, and code safety",
            "Native Spring Boot, Jakarta EE, MicroProfile, and Kubernetes integrations",
            "Exceptional Git visual conflict resolution and branch manager",
            "Built-in database tooling and HTTP client"
        ],
        "cons": [
            "Resource hungry (2GB+ RAM standard footprint)",
            "Web development features locked in Ultimate edition",
            "Steep learning curve for complex project settings"
        ],
        "best_for": "Enterprise Java developers, Spring Boot engineers, Kotlin specialists",
        "summary": "The premier enterprise Java and polyglot JVM development environment.",
        "rating": "4.9/5.0",
        "website": "https://www.jetbrains.com/idea/",
        "github_repo": "JetBrains/intellij-community"
    },
    {
        "id": "helix",
        "name": "Helix Editor",
        "developer": "Helix Project",
        "category": "Post-Modern Modal Terminal Editor",
        "license_type": "Open Source (MPL 2.0)",
        "pricing": "100% Free",
        "pros": [
            "Zero configuration required out-of-the-box (built-in LSP & Tree-sitter)",
            "Selection-first modal editing model (selection -> action)",
            "Extremely fast Rust implementation with multiple cursor support",
            "Beautiful built-in terminal UI themes"
        ],
        "cons": [
            "Plugin system still under active architectural design",
            "Different keybindings than classic Vim/Neovim",
            "Terminal-only native execution"
        ],
        "best_for": "Developers wanting Neovim power without complex configuration files",
        "summary": "A post-modern modal text editor written in Rust with built-in LSP.",
        "rating": "4.7/5.0",
        "website": "https://helix-editor.com/",
        "github_repo": "helix-editor/helix"
    }
]


def load_history(history_file: str = "content/history.json") -> Dict[str, Any]:
    if os.path.exists(history_file):
        try:
            with open(history_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"Warning: Could not read history file {history_file}: {e}")
    return {"generated_dates": {}, "covered_ides": []}


def save_history(history_data: Dict[str, Any], history_file: str = "content/history.json") -> None:
    os.makedirs(os.path.dirname(os.path.abspath(history_file)), exist_ok=True)
    with open(history_file, "w", encoding="utf-8") as f:
        json.dump(history_data, f, indent=2)


def select_daily_ides(count: int = 3, history_file: str = "content/history.json") -> List[Dict[str, Any]]:
    history = load_history(history_file)
    covered_ids = set(history.get("covered_ides", []))

    uncovered = [ide for ide in IDE_DATABASE if ide["id"] not in covered_ids]

    if len(uncovered) < count:
        # Reset covered if running low, while prioritizing remaining uncovered
        selected = uncovered + [ide for ide in IDE_DATABASE if ide["id"] in covered_ids]
        selected = selected[:count]
    else:
        selected = uncovered[:count]

    return selected


def generate_amp_blog_post(ide: Dict[str, Any], date_str: str, index: int) -> str:
    """Generates AMP (Accelerated Mobile Pages) HTML post content for Blogger (ideguide.blogspot.com)"""
    title = f"{ide['name']} Review: The Good, The Bad, and Free vs Paid Verdict ({datetime.datetime.now().year})"
    pros_html = "".join([f"<li><strong>{pro}</strong></li>" for pro in ide["pros"]])
    cons_html = "".join([f"<li><strong>{con}</strong></li>" for con in ide["cons"]])

    amp_html = f"""<!doctype html>
<html ⚡ lang="en">
<head>
  <meta charset="utf-8">
  <title>{title} - IDE Guide</title>
  <link rel="canonical" href="https://ideguide.blogspot.com/{date_str}/{ide['id']}-review.html">
  <meta name="viewport" content="width=device-width,minimum-scale=1,initial-scale=1">
  <script async src="https://cdn.ampproject.org/v0.js"></script>
  <style amp-boilerplate>body{{-webkit-animation:-amp-start 8s steps(1,end) 0s 1 normal both;-moz-animation:-amp-start 8s steps(1,end) 0s 1 normal both;-ms-animation:-amp-start 8s steps(1,end) 0s 1 normal both;animation:-amp-start 8s steps(1,end) 0s 1 normal both}}@-webkit-keyframes -amp-start{{from{{visibility:hidden}}to{{visibility:visible}}}}@-moz-keyframes -amp-start{{from{{visibility:hidden}}to{{visibility:visible}}}}@-ms-keyframes -amp-start{{from{{visibility:hidden}}to{{visibility:visible}}}}@-o-keyframes -amp-start{{from{{visibility:hidden}}to{{visibility:visible}}}}@keyframes -amp-start{{from{{visibility:hidden}}to{{visibility:visible}}}}</style><noscript><style amp-boilerplate>body{{-webkit-animation:none;-moz-animation:none;-ms-animation:none;animation:none}}</style></noscript>
  <style amp-custom>
    body {{
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
      line-height: 1.6;
      color: #1e293b;
      background-color: #f8fafc;
      padding: 16px;
      margin: 0 auto;
      max-width: 800px;
    }}
    header {{
      background: linear-gradient(135deg, #1e1b4b 0%, #312e81 100%);
      color: #ffffff;
      padding: 24px;
      border-radius: 12px;
      margin-bottom: 24px;
      text-align: center;
    }}
    header h1 {{
      margin: 0 0 10px 0;
      font-size: 28px;
    }}
    .badge {{
      display: inline-block;
      background: #6366f1;
      color: #ffffff;
      padding: 4px 12px;
      border-radius: 20px;
      font-size: 14px;
      font-weight: 600;
    }}
    .disclaimer-box {{
      background-color: #f1f5f9;
      border-left: 4px solid #6366f1;
      padding: 14px 18px;
      margin: 20px 0;
      font-size: 13px;
      color: #475569;
      border-radius: 4px;
    }}
    .grid-container {{
      display: flex;
      flex-wrap: wrap;
      gap: 16px;
      margin: 20px 0;
    }}
    .card {{
      flex: 1 1 300px;
      background: #ffffff;
      padding: 20px;
      border-radius: 8px;
      box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }}
    .pros {{ border-top: 4px solid #22c55e; }}
    .cons {{ border-top: 4px solid #ef4444; }}
    h2 {{
      color: #0f172a;
      border-bottom: 2px solid #e2e8f0;
      padding-bottom: 8px;
      margin-top: 28px;
    }}
    ul {{ padding-left: 20px; }}
    li {{ margin-bottom: 8px; }}
    .verdict-box {{
      background: #e0e7ff;
      border: 1px solid #c7d2fe;
      padding: 20px;
      border-radius: 8px;
      margin-top: 24px;
    }}
    .price-tag {{
      font-size: 18px;
      font-weight: bold;
      color: #4338ca;
    }}
    .cta-button {{
      display: block;
      width: 100%;
      text-align: center;
      background: #4f46e5;
      color: #ffffff;
      text-decoration: none;
      padding: 12px 0;
      border-radius: 6px;
      font-weight: bold;
      margin-top: 16px;
    }}
  </style>
</head>
<body>

  <header>
    <div class="badge">{ide['category']}</div>
    <h1>{ide['name']} Guide & In-Depth Developer Evaluation</h1>
    <p>Developer: {ide['developer']} | Score: {ide['rating']}</p>
  </header>

  <div class="disclaimer-box">
    <strong>Editorial Transparency:</strong> {DISCLAIMER_TEXT}
  </div>

  <section>
    <h2>Overview</h2>
    <p>Welcome to today's edition of <strong>IDE Guide</strong>. In this review, we dive deep into <strong>{ide['name']}</strong> ({ide['category']}). {ide['summary']}</p>
    <p>Whether you are building complex distributed backend systems, crafting web apps, or writing scripts, picking the right code editor determines your daily flow and bug-hunting efficiency.</p>
  </section>

  <amp-img src="https://images.unsplash.com/photo-1555066931-4365d14bab8c?w=800&auto=format&fit=crop&q=80"
           width="800"
           height="450"
           layout="responsive"
           alt="{ide['name']} Development Environment"></amp-img>

  <h2>The Good & The Bad</h2>
  <div class="grid-container">
    <div class="card pros">
      <h3 style="color: #166534; margin-top: 0;">👍 The Good (Pros)</h3>
      <ul>
        {pros_html}
      </ul>
    </div>
    <div class="card cons">
      <h3 style="color: #991b1b; margin-top: 0;">👎 The Bad (Cons)</h3>
      <ul>
        {cons_html}
      </ul>
    </div>
  </div>

  <h2>Pricing Model: Free or Paid?</h2>
  <p>Understanding cost structures is vital when adopting software tools for individual projects or enterprise development teams.</p>
  <p class="price-tag">License & Pricing: {ide['pricing']}</p>
  <p><strong>License Type:</strong> {ide['license_type']}</p>

  <h2>Best For</h2>
  <p><strong>{ide['best_for']}</strong></p>

  <div class="verdict-box">
    <h3 style="margin-top: 0; color: #1e1b4b;">IDE Guide Final Verdict</h3>
    <p>{ide['name']} earns a solid rating of <strong>{ide['rating']}</strong>. {ide['summary']} If you match the profile of <em>{ide['best_for']}</em>, it is well worth adding to your developer toolkit.</p>
    <a href="https://www.youtube.com/@IDEguide" class="cta-button" target="_blank" rel="noopener">Subscribe to @IDEguide on YouTube for Visual IDE Benchmarks</a>
  </div>

  <div class="disclaimer-box" style="margin-top: 30px;">
    <p>{DISCLAIMER_TEXT}</p>
    <p>© {datetime.datetime.now().year} IDE Guide (https://ideguide.blogspot.com/ & https://www.youtube.com/@IDEguide). All rights reserved.</p>
  </div>

</body>
</html>
"""
    return amp_html


def generate_google_flow_video_spec(ide: Dict[str, Any], date_str: str, index: int) -> Dict[str, Any]:
    """Generates detailed Google Flow AI video specification & script for YouTube (@IDEguide)"""
    year = datetime.datetime.now().year

    spec = {
        "metadata": {
            "title": f"Is {ide['name']} Worth It in {year}? The Good, The Bad & Pricing Explained",
            "target_channel": "https://www.youtube.com/@IDEguide",
            "target_blog": "https://ideguide.blogspot.com/",
            "ide_name": ide["name"],
            "category": ide["category"],
            "disclaimer": DISCLAIMER_TEXT,
            "generated_date": date_str,
            "package_index": index
        },
        "google_flow_prompt_config": {
            "style": "Cinematic modern tech review, clean 4K workstation, cyber neon subtle lighting",
            "aspect_ratio_shorts": "9:16 (1080x1920)",
            "aspect_ratio_long": "16:9 (3840x2160)",
            "camera_style": "Macro depth-of-field, sleek panning over mechanical keyboard and high-res code display",
            "audio_voiceover_tone": "Energetic, articulate, objective technical guide"
        },
        "youtube_shorts_spec_60s": {
            "duration": "60 Seconds",
            "scenes": [
                {
                    "scene_number": 1,
                    "timestamp": "00:00 - 00:05",
                    "google_flow_video_prompt": (
                        f"Close-up high-fps shot of hands typing code in {ide['name']} on an ultra-wide curved monitor. "
                        f"Cyberpunk dark blue accent lighting, soft neon backlight, cinematic shallow depth of field. "
                        f"Text overlay in bold electric white: '{ide['name']} in 60 SECONDS!'"
                    ),
                    "camera_motion": "Slow zoom in toward glowing IDE interface",
                    "voiceover_script": f"Is {ide['name']} actually worth using in {year}? Let's break down the good, the bad, and whether it's free or paid!"
                },
                {
                    "scene_number": 2,
                    "timestamp": "00:05 - 00:25",
                    "google_flow_video_prompt": (
                        f"Split screen graphic showing {ide['name']} key feature highlights with green checkmarks. "
                        f"Sleek futuristic glassmorphism UI cards popping up on screen with smooth animations. "
                        f"Show code snippets flashing with syntax highlighting."
                    ),
                    "camera_motion": "Pan left to right smoothly across feature metrics",
                    "voiceover_script": (
                        f"First, the good! {ide['pros'][0]}. Plus, {ide['pros'][1]}."
                    )
                },
                {
                    "scene_number": 3,
                    "timestamp": "00:25 - 00:45",
                    "google_flow_video_prompt": (
                        f"Clean dark slate background with red warning aura. Sleek glass card showing limitations with red X icons. "
                        f"Macro lens panning down glowing mechanical keyboard switches."
                    ),
                    "camera_motion": "Tilt down with subtle camera shake on transition",
                    "voiceover_script": (
                        f"Now for the catch! {ide['cons'][0]}."
                    )
                },
                {
                    "scene_number": 4,
                    "timestamp": "00:45 - 00:60",
                    "google_flow_video_prompt": (
                        f"3D dollar sign graphic transforming into '{ide['pricing']}'. "
                        f"YouTube subscriber button graphic for @IDEguide animated with pulse effect, "
                        f"along with Blogger link ideguide.blogspot.com."
                    ),
                    "camera_motion": "Fast forward zoom ending on subscribe badge",
                    "voiceover_script": (
                        f"Pricing check: {ide['pricing']}. Ideal for {ide['best_for']}. "
                        f"Subscribe to @IDEguide and visit ideguide.blogspot.com for the full breakdown! "
                        f"Remember, IDE Guide is 100% independent and non-sponsored!"
                    )
                }
            ]
        },
        "youtube_longform_spec_3min": {
            "duration": "3 - 5 Minutes",
            "visual_style": "Pro Developer Studio Review",
            "scene_breakdown": [
                {
                    "section": "Hook & Non-Sponsorship Disclosure",
                    "flow_prompt": f"Professional dark studio setup, RGB lighting backdrop, macro lens shot of IDE interface {ide['name']} running on macOS / Linux workspace.",
                    "narration": f"Welcome back to IDE Guide! Today we are taking an objective look at {ide['name']}. Quick disclaimer before we start: IDE Guide is completely independent and not sponsored by any editor developer. All opinions are strictly objective."
                },
                {
                    "section": "Key Strengths & Features",
                    "flow_prompt": f"Dynamic screen recording overlay with glowing highlighted code lines in {ide['name']}. Cinematic camera drift across developer desk with code flowing.",
                    "narration": f"{ide['name']} is categorized as a {ide['category']}. Here are the top reasons developers choose it: " + "; ".join(ide["pros"])
                },
                {
                    "section": "Cons & Weaknesses",
                    "flow_prompt": f"Minimalist UI illustration showing performance meters, RAM consumption, and feature gaps highlighted in subtle amber red.",
                    "narration": f"However, no editor is perfect. Here are the main drawbacks you need to know: " + "; ".join(ide["cons"])
                },
                {
                    "section": "Free vs Paid & Target Audience",
                    "flow_prompt": f"Comparison matrix table animated on dark futuristic HUD display showing pricing tiers: {ide['pricing']} under {ide['license_type']}.",
                    "narration": f"In terms of cost: {ide['pricing']}. Who is it best for? {ide['best_for']}."
                },
                {
                    "section": "Final Verdict & Outro",
                    "flow_prompt": f"Cinematic logo reveal of @IDEguide and Blogger URL ideguide.blogspot.com with floating code particles.",
                    "narration": f"Final rating: {ide['rating']}. Check out the full written AMP post on ideguide.blogspot.com and don't forget to hit subscribe on @IDEguide for daily editor comparisons!"
                }
            ]
        }
    }
    return spec


def generate_daily_package(target_date: Optional[str] = None) -> List[str]:
    if not target_date:
        target_date = datetime.datetime.now().strftime("%Y-%m-%d")

    output_dir = os.path.join("content", target_date)
    os.makedirs(output_dir, exist_ok=True)

    history_file = "content/history.json"
    history = load_history(history_file)

    selected_ides = select_daily_ides(count=3, history_file=history_file)
    created_files = []

    for idx, ide in enumerate(selected_ides, start=1):
        slug = ide["id"]

        # 1. AMP Blog Post
        amp_content = generate_amp_blog_post(ide, target_date, idx)
        amp_filename = f"0{idx}_amp_{slug}_blog_post.html"
        amp_path = os.path.join(output_dir, amp_filename)
        with open(amp_path, "w", encoding="utf-8") as f:
            f.write(amp_content)
        created_files.append(amp_path)

        # 2. Google Flow Video Spec
        flow_spec = generate_google_flow_video_spec(ide, target_date, idx)
        flow_filename = f"0{idx}_flow_{slug}_video_spec.json"
        flow_path = os.path.join(output_dir, flow_filename)
        with open(flow_path, "w", encoding="utf-8") as f:
            json.dump(flow_spec, f, indent=2)
        created_files.append(flow_path)

        # 3. Readable Flow Spec Markdown Version
        flow_md_filename = f"0{idx}_flow_{slug}_video_spec.md"
        flow_md_path = os.path.join(output_dir, flow_md_filename)
        flow_md_content = f"""# Google Flow Video Generation Spec: {ide['name']}

> **Channel:** https://www.youtube.com/@IDEguide
> **Blog:** https://ideguide.blogspot.com/
> **Date:** {target_date}

## Editorial Disclaimer
{DISCLAIMER_TEXT}

## Video Metadata
- **IDE Name:** {ide['name']}
- **Category:** {ide['category']}
- **Pricing:** {ide['pricing']}
- **Rating:** {ide['rating']}

---

## 🎬 YouTube Shorts (60 Seconds Script & Google Flow Prompts)

"""
        for s in flow_spec["youtube_shorts_spec_60s"]["scenes"]:
            flow_md_content += f"""### Scene {s['scene_number']} ({s['timestamp']})
* **Google Flow Prompt:** `{s['google_flow_video_prompt']}`
* **Camera Motion:** {s['camera_motion']}
* **Voiceover Script:** "{s['voiceover_script']}"

"""

        flow_md_content += f"""---

## 📹 YouTube Long-Form Spec (3-5 Minutes)

"""
        for sec in flow_spec["youtube_longform_spec_3min"]["scene_breakdown"]:
            flow_md_content += f"""### {sec['section']}
* **Flow Prompt:** `{sec['flow_prompt']}`
* **Narration Script:** "{sec['narration']}"

"""
        with open(flow_md_path, "w", encoding="utf-8") as f:
            f.write(flow_md_content)
        created_files.append(flow_md_path)

        # Update history
        if ide["id"] not in history.get("covered_ides", []):
            history.setdefault("covered_ides", []).append(ide["id"])

    history.setdefault("generated_dates", {})[target_date] = [
        os.path.basename(p) for p in created_files
    ]
    save_history(history, history_file)

    print(f"Successfully generated {len(created_files)} content artifacts for date {target_date} in '{output_dir}'.")
    return created_files


if __name__ == "__main__":
    generated = generate_daily_package()
    for g in generated:
        print(f" - Created: {g}")
