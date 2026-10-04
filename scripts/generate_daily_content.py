#!/usr/bin/env python3
"""
IDE Guide - Daily Content Generator & Core Skill Engine.
Provides data definitions, generators, and history management for producing
3 daily AMP HTML blog posts and 3 Google Flow video specifications.
"""

import os
import json
from datetime import datetime, timezone
from typing import Dict, Any, List

HISTORY_FILE = "content/history.json"

MANDATORY_DISCLAIMER = (
    "Disclaimer: IDE Guide is an independent technical publication. "
    "This content is not sponsored, endorsed, or affiliated with any software vendor "
    "or editor developer mentioned above. All reviews and assessments are based strictly "
    "on objective developer evaluation."
)

IDE_DATABASE = {
    "VS Code": {
        "tagline": "The ubiquitous extensible code editor by Microsoft.",
        "pricing": "Free & Open Source (Core / VSCodium) / Free (Marketplace build)",
        "pricing_category": "Free",
        "category": "Code Editor",
        "pros": [
            "Massive ecosystem of extensions and themes",
            "Built-in Git integration and terminal",
            "Extremely active community and rapid updates",
            "Excellent language server protocol (LSP) support"
        ],
        "cons": [
            "Electron-based resource overhead under heavy project loads",
            "Can become slow with dozens of active extensions",
            "Telemetry enabled by default in official builds"
        ],
        "best_for": "Web developers, Python programmers, and full-stack engineers seeking flexibility.",
        "site_url": "https://code.visualstudio.com"
    },
    "Cursor": {
        "tagline": "The AI-first code editor built for hyper-productive development.",
        "pricing": "Freemium ($20/mo for Pro plan with unlimited fast AI)",
        "pricing_category": "Freemium",
        "category": "AI Code Editor",
        "pros": [
            "Deep inline AI code editing and multi-file code generation",
            "Native fork of VS Code allowing seamless extension migration",
            "Instant codebase indexing and semantic search",
            "Prompt-driven agentic editing workflow"
        ],
        "cons": [
            "Pro subscription required for heavy AI usage",
            "Requires active internet connection for advanced models",
            "Closed-source proprietary AI extensions"
        ],
        "best_for": "Developers wanting bleeding-edge AI code assistance and context-aware auto-completion.",
        "site_url": "https://cursor.com"
    },
    "IntelliJ IDEA": {
        "tagline": "The flagship Java and Kotlin IDE by JetBrains.",
        "pricing": "Freemium (Community Edition: Free / Ultimate Edition: Paid subscription)",
        "pricing_category": "Freemium / Paid",
        "category": "Full IDE",
        "pros": [
            "Unrivaled refactoring and code analysis for JVM languages",
            "Out-of-the-box framework support (Spring, Jakarta EE, Micronaut)",
            "Deep database management and HTTP client integration",
            "Rock-solid static analysis and inspection engine"
        ],
        "cons": [
            "High RAM and CPU consumption on large codebases",
            "Ultimate features locked behind recurring license",
            "Slower cold startup time compared to lightweight editors"
        ],
        "best_for": "Enterprise Java/Kotlin developers and large multi-module backend engineers.",
        "site_url": "https://www.jetbrains.com/idea/"
    },
    "Neovim": {
        "tagline": "Hyperextensible Vim-based terminal text editor.",
        "pricing": "100% Free & Open Source",
        "pricing_category": "Free",
        "category": "Terminal Editor",
        "pros": [
            "Lightning-fast performance and near-zero memory footprint",
            "Lua-first configuration engine for deep customization",
            "Native LSP and Tree-sitter syntax highlighting",
            "Keyboard-driven modal efficiency"
        ],
        "cons": [
            "Steep learning curve for Vim keybindings",
            "Requires manual configuration and plugin maintenance",
            "No default GUI without external frontends"
        ],
        "best_for": "Terminal enthusiasts, systems programmers, and developers who prioritize speed and modal editing.",
        "site_url": "https://neovim.io"
    },
    "Zed": {
        "tagline": "High-performance, multiplayer code editor written in Rust.",
        "pricing": "Free & Open Source",
        "pricing_category": "Free",
        "category": "Code Editor",
        "pros": [
            "GPU-accelerated rendering yielding silky smooth 120 FPS frame rates",
            "Native real-time collaborative editing (multiplayer)",
            "Built-in AI assistance and super fast startup",
            "Resource-efficient Rust architecture"
        ],
        "cons": [
            "Ecosystem and extension marketplace still maturing",
            "Fewer language tools compared to VS Code or JetBrains",
            "Linux and Windows ports newer than macOS build"
        ],
        "best_for": "Developers seeking ultra-responsive editor performance and pair programming tools.",
        "site_url": "https://zed.dev"
    },
    "PyCharm": {
        "tagline": "The dedicated Python IDE for professional developers.",
        "pricing": "Freemium (Community: Free / Professional: Paid subscription)",
        "pricing_category": "Freemium / Paid",
        "category": "Full IDE",
        "pros": [
            "In-depth Python autocompletion, debugging, and profiling",
            "Built-in Jupyter notebook support and data science tools",
            "First-class Web framework support (Django, Flask, FastAPI)",
            "Integrated virtual environment and conda management"
        ],
        "cons": [
            "Professional tier requires annual or monthly payment",
            "Can be resource heavy on lower-spec machines",
            "Slower indexation on massive virtual environments"
        ],
        "best_for": "Data scientists, Python backend developers, and web app engineers.",
        "site_url": "https://www.jetbrains.com/pycharm/"
    },
    "Sublime Text": {
        "tagline": "A sophisticated text editor for code, markup and prose.",
        "pricing": "Paid ($99 evaluation license / perpetual with updates)",
        "pricing_category": "Paid",
        "category": "Code Editor",
        "pros": [
            "Instant launch speed and snappy file opening",
            "GPU rendering engine for smooth scrolling",
            "Lightweight resource usage across all OS platforms",
            "Package Control for easy extension installation"
        ],
        "cons": [
            "Paid license popup after evaluation period",
            "Out-of-the-box IDE features require plugin setups",
            "Smaller extension ecosystem than VS Code"
        ],
        "best_for": "Developers needing a fast, lightweight secondary editor or quick file inspector.",
        "site_url": "https://www.sublimetext.com"
    },
    "Fleet": {
        "tagline": "Next-generation lightweight IDE by JetBrains built from scratch.",
        "pricing": "Freemium (Public Preview / Free tier)",
        "pricing_category": "Freemium",
        "category": "Lightweight IDE",
        "pros": [
            "Switches smoothly between lightweight editor mode and smart IDE mode",
            "Distributed architecture supporting remote dev and containers",
            "Clean modern UI design",
            "JetBrains code intelligence engine integrated"
        ],
        "cons": [
            "Still under active preview/development",
            "Plugin ecosystem is in early stages",
            "May encounter occasional preview bugs"
        ],
        "best_for": "Developers wanting JetBrains intelligence in a lightweight, modern interface.",
        "site_url": "https://www.jetbrains.com/fleet/"
    },
    "Windsurf": {
        "tagline": "The Agentic IDE by Codeium built for flow-state coding.",
        "pricing": "Freemium ($15/mo Pro tier)",
        "pricing_category": "Freemium",
        "category": "AI Code Editor",
        "pros": [
            "Flow paradigm for seamless AI collaborative coding",
            "Deep codebase awareness and automated multi-step actions",
            "Built on VS Code open source base for familiar extension support",
            "Fast AI response time"
        ],
        "cons": [
            "Paid plan needed for heavy usage quotas",
            "Newer product with evolving UI workflows",
            "Requires cloud connectivity for AI flows"
        ],
        "best_for": "Engineers looking for autonomous agentic pair-programming workflows.",
        "site_url": "https://codeium.com/windsurf"
    }
}

def load_history() -> List[str]:
    """Loads history of covered IDEs."""
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data.get("covered_ides", [])
        except Exception:
            return []
    return []

def save_history(covered_ides: List[str]):
    """Saves history of covered IDEs."""
    os.makedirs(os.path.dirname(HISTORY_FILE), exist_ok=True)
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump({"covered_ides": covered_ides, "last_updated": datetime.now(timezone.utc).isoformat()}, f, indent=2)

def generate_amp_blog_post(ide_name: str, info: Dict[str, Any]) -> str:
    """Generates AMP HTML compliant blog post content for Blogger."""
    pros_html = "".join([f"<li><strong>{p}</strong></li>" for p in info["pros"]])
    cons_html = "".join([f"<li><strong>{c}</strong></li>" for c in info["cons"]])

    html = f"""<!doctype html>
<html ⚡ lang="en">
<head>
  <meta charset="utf-8">
  <title>{ide_name} Review & Guide - IDE Guide</title>
  <link rel="canonical" href="{info['site_url']}">
  <meta name="viewport" content="width=device-width,minimum-scale=1,initial-scale=1">
  <script async src="https://cdn.ampproject.org/v0.js"></script>
  <style amp-boilerplate>body{{-webkit-animation:-amp-start 8s steps(1,end) 0s 1 normal both;-moz-animation:-amp-start 8s steps(1,end) 0s 1 normal both;-ms-animation:-amp-start 8s steps(1,end) 0s 1 normal both;animation:-amp-start 8s steps(1,end) 0s 1 normal both}}@-webkit-keyframes -amp-start{{from{{visibility:hidden}}to{{visibility:visible}}}}@-moz-keyframes -amp-start{{from{{visibility:hidden}}to{{visibility:visible}}}}@-ms-keyframes -amp-start{{from{{visibility:hidden}}to{{visibility:visible}}}}@-o-keyframes -amp-start{{from{{visibility:hidden}}to{{visibility:visible}}}}@keyframes -amp-start{{from{{visibility:hidden}}to{{visibility:visible}}}}</style><noscript><style amp-boilerplate>body{{-webkit-animation:none;-moz-animation:none;-ms-animation:none;animation:none}}</style></noscript>
  <style amp-custom>
    body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; line-height: 1.6; color: #1a1a1a; padding: 20px; max-width: 800px; margin: 0 auto; background-color: #fafafa; }}
    header {{ border-bottom: 3px solid #2563eb; padding-bottom: 15px; margin-bottom: 25px; }}
    h1 {{ color: #1e293b; font-size: 2rem; margin-bottom: 5px; }}
    .badge {{ display: inline-block; background: #2563eb; color: #ffffff; padding: 4px 12px; border-radius: 9999px; font-size: 0.875rem; font-weight: bold; margin-bottom: 10px; }}
    .badge-price {{ background: #059669; }}
    .section {{ background: #ffffff; border: 1px solid #e2e8f0; border-radius: 8px; padding: 20px; margin-bottom: 20px; box-shadow: 0 1px 3px rgba(0,0,0,0.05); }}
    .pros {{ border-left: 4px solid #10b981; }}
    .cons {{ border-left: 4px solid #ef4444; }}
    ul {{ padding-left: 20px; }}
    li {{ margin-bottom: 8px; }}
    .disclaimer {{ background: #f1f5f9; border-left: 4px solid #64748b; padding: 15px; font-size: 0.875rem; color: #475569; margin-top: 30px; font-style: italic; }}
  </style>
</head>
<body>

  <header>
    <span class="badge">{info['category']}</span>
    <span class="badge badge-price">{info['pricing_category']}</span>
    <h1>{ide_name} - Detailed Developer Guide & Review</h1>
    <p><em>{info['tagline']}</em></p>
  </header>

  <div class="section">
    <h2>1. Overview & Pricing</h2>
    <p><strong>Pricing Structure:</strong> {info['pricing']}</p>
    <p>When selecting a primary workspace, developers need to balance responsiveness, extension stability, and licensing costs. Here is our comprehensive breakdown of {ide_name}.</p>
  </div>

  <div class="section pros">
    <h2>2. The Good (Key Strengths)</h2>
    <ul>
      {pros_html}
    </ul>
  </div>

  <div class="section cons">
    <h2>3. The Bad (Limitations & Drawbacks)</h2>
    <ul>
      {cons_html}
    </ul>
  </div>

  <div class="section">
    <h2>4. Who Should Choose {ide_name}?</h2>
    <p><strong>Best For:</strong> {info['best_for']}</p>
    <p>Learn more and download directly from official site: <a href="{info['site_url']}" target="_blank" rel="noopener">{info['site_url']}</a></p>
  </div>

  <div class="disclaimer">
    {MANDATORY_DISCLAIMER}
  </div>

</body>
</html>"""
    return html

def generate_google_flow_spec(ide_name: str, info: Dict[str, Any]) -> str:
    """Generates Google Flow visual video generation spec markdown."""
    spec = f"""# Google Flow Video Generation Spec: {ide_name}

## 1. Video Metadata
- **Channel**: IDE Guide (@IDEguide)
- **Target IDE**: {ide_name}
- **Category**: {info['category']}
- **Pricing Model**: {info['pricing']}
- **Format**: YouTube Short / Reel (9:16 aspect ratio)
- **Duration**: 60 Seconds
- **Audio Aesthetic**: Upbeat technical ambient synth, subtle mechanical keyboard audio cues

---

## 2. Scene-by-Scene Prompt Breakdown

### Scene 1: Hook (0:00 - 0:10)
- **Visual Prompt**: Cinematic macro close-up shot of a modern dark-mode editor displaying code on a high-refresh monitor. Vibrant RGB ambient backlighting, subtle camera pan from left to right.
- **Framing**: Vertical 9:16, tight close-up, shallow depth of field.
- **On-Screen Text**: "Should You Use {ide_name} in 2026?"
- **Voiceover Script**: "Is {ide_name} worth your development time, or is it just hype? Let's break down the good, the bad, and the pricing."

### Scene 2: The Pricing & Overview (0:10 - 0:25)
- **Visual Prompt**: Sleek 3D isometric animation of software tiers floating above a clean glass desk, transitioning into screen recordings of {ide_name}'s core UI.
- **Framing**: Medium shot, smooth downward tilt.
- **On-Screen Text**: "Pricing: {info['pricing_category']}"
- **Voiceover Script**: "{ide_name} is categorized as a {info['category']}. Pricing model: {info['pricing']}."

### Scene 3: The Good - Top Strengths (0:25 - 0:40)
- **Visual Prompt**: Energetic screen montage showing rapid code editing, AI autocompletion triggers, and crisp interface animations inside {ide_name}. Glowing green highlight effects.
- **Framing**: Screen capture zoom-in with smooth pan.
- **On-Screen Text**: "THE GOOD: {info['pros'][0]}"
- **Voiceover Script**: "The good: {info['pros'][0]}. Plus, {info['pros'][1]}."

### Scene 4: The Bad - Key Drawbacks (0:40 - 0:50)
- **Visual Prompt**: Close-up of code editor error diagnostics or loading progress indicators with warm red accents and subtle warning badge overlays.
- **Framing**: Center-focused macro shot.
- **On-Screen Text**: "THE BAD: {info['cons'][0]}"
- **Voiceover Script**: "The bad: Keep in mind that {info['cons'][0]}."

### Scene 5: Verdict & Non-Sponsorship Disclaimer (0:50 - 1:00)
- **Visual Prompt**: Clean graphic card showing {ide_name} logo, badge 'IDE Guide Approved Verdict', transitioning to standard end screen with social handles @IDEguide.
- **Framing**: Static centered full frame.
- **On-Screen Text**: "Verdict: Best for {info['best_for'][:30]}...\n\n{MANDATORY_DISCLAIMER}"
- **Voiceover Script**: "Verdict: Best for {info['best_for']}. {MANDATORY_DISCLAIMER}"

---

## 3. Mandatory Non-Sponsorship Disclaimer
> {MANDATORY_DISCLAIMER}
"""
    return spec

def run_daily_generation(date_str: str = None):
    if not date_str:
        date_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    history = load_history()
    available_keys = [k for k in IDE_DATABASE.keys() if k not in history]

    if len(available_keys) < 3:
        print("All IDEs covered in previous cycles. Resetting history cycle.")
        history = []
        available_keys = list(IDE_DATABASE.keys())

    selected = available_keys[:3]
    output_dir = os.path.join("content", date_str)
    os.makedirs(output_dir, exist_ok=True)

    print(f"Generating content for date: {date_str}")
    print(f"Selected IDEs: {selected}")

    for idx, ide_name in enumerate(selected, start=1):
        info = IDE_DATABASE[ide_name]
        slug = ide_name.lower().replace(" ", "_")

        blog_file = os.path.join(output_dir, f"post_{idx}_{slug}.html")
        blog_html = generate_amp_blog_post(ide_name, info)
        with open(blog_file, "w", encoding="utf-8") as f:
            f.write(blog_html)

        video_file = os.path.join(output_dir, f"video_{idx}_{slug}_spec.md")
        video_spec = generate_google_flow_spec(ide_name, info)
        with open(video_file, "w", encoding="utf-8") as f:
            f.write(video_spec)

        print(f" -> Created {blog_file}")
        print(f" -> Created {video_file}")

        if ide_name not in history:
            history.append(ide_name)

    save_history(history)
    print("Daily content generation successfully completed.")

if __name__ == "__main__":
    run_daily_generation()
