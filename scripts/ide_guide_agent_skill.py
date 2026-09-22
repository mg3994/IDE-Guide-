#!/usr/bin/env python3
"""
IDE Guide Agentic Skill - CLI Tool
Generates AMP HTML blog posts (compatible with Blogger) and Google Flow Video Specifications
for IDEs and Code Editors.

Usage:
  python3 scripts/ide_guide_agent_skill.py --ide "Cursor" --output-dir "./output"
  python3 scripts/ide_guide_agent_skill.py --repo "https://github.com/zed-industries/zed"
"""

import argparse
import os
import sys
import json
import re
from typing import Dict, Any, Optional

DISCLAIMER_TEXT = (
    "Disclaimer: IDE Guide is an independent technical publication. "
    "This content is not sponsored, endorsed, or affiliated with any software vendor or "
    "editor developer mentioned above. All reviews and assessments are based strictly "
    "on objective developer evaluation."
)

BLOGGER_URL = "https://ideguide.blogspot.com/"
YOUTUBE_URL = "https://www.youtube.com/@IDEguide"

# Database of IDE metadata
IDE_DATABASE: Dict[str, Dict[str, Any]] = {
    "vs code": {
        "name": "Visual Studio Code",
        "category": "Extensible Code Editor",
        "developer": "Microsoft",
        "pricing": "Free (Open Source Core / Proprietary Binary)",
        "pricing_type": "Free",
        "pros": [
            "Extremely rich ecosystem of extensions and themes",
            "Built-in Git integration and remote development options",
            "Massive community support and continuous active updates"
        ],
        "cons": [
            "Electron overhead can lead to higher memory consumption",
            "Extension bloat can degrade startup performance over time"
        ],
        "best_for": "Web developers, full-stack engineers, and multi-language software projects.",
        "rating": "4.8/5.0",
        "features": ["GitHub Copilot Integration", "Integrated Terminal", "Debugger", "Remote SSH / Containers"]
    },
    "cursor": {
        "name": "Cursor",
        "category": "AI-First Code Editor",
        "developer": "Anysphere",
        "pricing": "Freemium ($20/mo Pro plan)",
        "pricing_type": "Freemium",
        "pros": [
            "Deep native AI integration with codebase-wide context",
            "Seamless drop-in compatibility with VS Code extensions",
            "Multi-file edit capabilities via Copilot++ and Cmd+K"
        ],
        "cons": [
            "Requires paid plan for unlimited high-tier LLM requests",
            "Dependent on cloud AI models for heavy contextual features"
        ],
        "best_for": "Developers seeking maximum AI-assisted velocity and rapid project prototyping.",
        "rating": "4.9/5.0",
        "features": ["Codebase Indexing", "Cmd+K Inline AI", "Composer Agent", "VS Code Fork"]
    },
    "zed": {
        "name": "Zed",
        "category": "High-Performance Code Editor",
        "developer": "Zed Industries",
        "pricing": "Free & Open Source (GPU Accelerated)",
        "pricing_type": "Free",
        "pros": [
            "Written in Rust with GPU acceleration for instantaneous response",
            "Built-in multiplayer collaborative coding and pairing",
            "Minimalist UI with near-zero latency typing experience"
        ],
        "cons": [
            "Smaller extension ecosystem compared to VS Code",
            "Linux and Windows releases are still evolving"
        ],
        "best_for": "Systems programmers, Rust/Go developers, and latency-sensitive engineers.",
        "rating": "4.7/5.0",
        "features": ["GPU Rendering", "Multiplayer Coding", "CRDT Collaboration", "Built-in Language Server"]
    },
    "neovim": {
        "name": "Neovim",
        "category": "Hyperextensible Terminal Text Editor",
        "developer": "Neovim Core Community",
        "pricing": "100% Free & Open Source",
        "pricing_type": "Free",
        "pros": [
            "Incredible speed, ultra-lightweight footprint and keyboard-centric efficiency",
            "Lua scripting engine allows complete personalized editor tailoring",
            "Built-in Language Server Protocol (LSP) and Treesitter support"
        ],
        "cons": [
            "Steep learning curve for modal editing and custom configuration",
            "Requires initial setup time to configure plugins and keymaps"
        ],
        "best_for": "Terminal power users, CLI purists, and developers who love vim keybindings.",
        "rating": "4.9/5.0",
        "features": ["Modal Editing", "Lua API", "Built-in LSP", "Treesitter Syntax Parsing"]
    },
    "pycharm": {
        "name": "PyCharm",
        "category": "Professional Python IDE",
        "developer": "JetBrains",
        "pricing": "Freemium (Community Free / Professional Paid $249/yr)",
        "pricing_type": "Freemium",
        "pros": [
            "Unrivaled Python refactoring, static analysis, and code inspections",
            "Built-in database tools, Django support, and scientific Jupyter tools",
            "Robust debugger, test runners, and virtualenv management"
        ],
        "cons": [
            "Heavy resource footprint and longer initial indexing time",
            "Full features locked behind Professional subscription"
        ],
        "best_for": "Professional Python developers, data scientists, and Django web engineers.",
        "rating": "4.8/5.0",
        "features": ["Python Refactoring", "Database Client", "Jupyter Support", "Smart Code Inspection"]
    },
    "windsurf": {
        "name": "Windsurf",
        "category": "Agentic AI IDE",
        "developer": "Codeium",
        "pricing": "Freemium ($15/mo Pro plan)",
        "pricing_type": "Freemium",
        "pros": [
            "Flows paradigm blending inline copilot with deep agentic action",
            "Real-time indexing and fast terminal command execution",
            "Full compatibility with VS Code marketplace extensions"
        ],
        "cons": [
            "Credit-based usage limits for complex AI flows",
            "Requires steady internet connection for deep agentic features"
        ],
        "best_for": "Engineers looking for autonomous agentic AI development capabilities.",
        "rating": "4.7/5.0",
        "features": ["Cascade Agent", "Supercomplete", "Flow Paradigm", "Deep Context Indexing"]
    },
    "helix": {
        "name": "Helix",
        "category": "Post-Modern Modal Terminal Editor",
        "developer": "Helix Project",
        "pricing": "100% Free & Open Source",
        "pricing_type": "Free",
        "pros": [
            "Zero-config setup with LSP, Treesitter, and themes out of the box",
            "Selection-first editing paradigm (selection -> action)",
            "Written in Rust for instant startup and low memory footprint"
        ],
        "cons": [
            "Plugin system is still under design/development",
            "Requires learning selection-first keybinding differences from Vim"
        ],
        "best_for": "Developers wanting a powerful modal editor with zero configuration hassle.",
        "rating": "4.6/5.0",
        "features": ["Selection-First Modal", "Zero Config LSP", "Treesitter Integration", "Rust Performance"]
    },
    "sublime text": {
        "name": "Sublime Text",
        "category": "Ultra-Fast Lightweight Text Editor",
        "developer": "Sublime HQ",
        "pricing": "Paid License ($99 / Evaluation mode)",
        "pricing_type": "Paid",
        "pros": [
            "Blazing fast performance, handles multi-gigabyte files effortlessly",
            "Minimalist responsive interface with multiple selections and split views",
            "GPU rendering engine for smooth high-refresh scrolling"
        ],
        "cons": [
            "Proprietary software model with license popup in evaluation",
            "LSP features require plugin installation and setup"
        ],
        "best_for": "Developers who prioritize raw speed, low RAM usage, and instant startup.",
        "rating": "4.5/5.0",
        "features": ["GPU Rendering", "Goto Anything", "Multiple Selections", "Python API"]
    }
}


def get_ide_info(ide_name: str, repo_url: Optional[str] = None) -> Dict[str, Any]:
    key = ide_name.strip().lower()
    if key in IDE_DATABASE:
        data = IDE_DATABASE[key].copy()
        if repo_url:
            data["repo_url"] = repo_url
        return data

    clean_name = ide_name.strip().title() if ide_name else "Developer Code Editor"
    if repo_url and not ide_name:
        parts = repo_url.rstrip("/").split("/")
        if len(parts) >= 1:
            clean_name = parts[-1].replace("-", " ").replace("_", " ").title()

    return {
        "name": clean_name,
        "category": "Modern Code Editor & IDE",
        "developer": "Community / Vendor",
        "pricing": "Free / Paid Available",
        "pricing_type": "Freemium",
        "pros": [
            f"Tailored productivity features for modern development in {clean_name}",
            "Strong developer tools and custom extension support",
            "Active maintenance and performance optimizations"
        ],
        "cons": [
            "Specific configuration required for niche language tooling",
            "Ecosystem maturity varies depending on plugin availability"
        ],
        "best_for": f"Software engineers evaluating modern editor workflows with {clean_name}.",
        "rating": "4.6/5.0",
        "features": ["Smart Syntax Highlighting", "Language Server Support", "Custom Keybindings", "Project Workspace"],
        "repo_url": repo_url
    }


def generate_amp_html_blog_post(info: Dict[str, Any]) -> str:
    name = info["name"]
    category = info["category"]
    developer = info["developer"]
    pricing = info["pricing"]
    pricing_type = info["pricing_type"]
    pros = info["pros"]
    cons = info["cons"]
    best_for = info["best_for"]
    rating = info["rating"]
    features = info["features"]

    pros_html = "".join([f"<li><strong>✓</strong> {p}</li>" for p in pros])
    cons_html = "".join([f"<li><strong>✗</strong> {c}</li>" for c in cons])
    features_html = "".join([f"<span class=\"badge\">{f}</span>" for f in features])

    amp_html = f"""<!doctype html>
<html ⚡ lang="en">
<head>
  <meta charset="utf-8">
  <title>{name} Review & Deep Dive - IDE Guide</title>
  <link rel="canonical" href="{BLOGGER_URL}">
  <meta name="viewport" content="width=device-width,minimum-scale=1,initial-scale=1">
  <script async src="https://cdn.ampproject.org/v0.js"></script>
  <style amp-boilerplate>body{{-webkit-animation:-amp-start 8s steps(1,end) 0s 1 normal both;-moz-animation:-amp-start 8s steps(1,end) 0s 1 normal both;-ms-animation:-amp-start 8s steps(1,end) 0s 1 normal both;animation:-amp-start 8s steps(1,end) 0s 1 normal both}}@-webkit-keyframes -amp-start{{from{{visibility:hidden}}to{{visibility:visible}}}}@-moz-keyframes -amp-start{{from{{visibility:hidden}}to{{visibility:visible}}}}@-ms-keyframes -amp-start{{from{{visibility:hidden}}to{{visibility:visible}}}}@-o-keyframes -amp-start{{from{{visibility:hidden}}to{{visibility:visible}}}}@keyframes -amp-start{{from{{visibility:hidden}}to{{visibility:visible}}}}</style><noscript><style amp-boilerplate>body{{-webkit-animation:none;-moz-animation:none;-ms-animation:none;animation:none}}</style></noscript>
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
    .header {{
      background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
      color: #ffffff;
      padding: 30px 20px;
      border-radius: 12px;
      margin-bottom: 24px;
    }}
    .header h1 {{
      margin: 0 0 10px 0;
      font-size: 28px;
    }}
    .meta-tag {{
      display: inline-block;
      background-color: #3b82f6;
      color: #ffffff;
      font-size: 12px;
      font-weight: bold;
      padding: 4px 10px;
      border-radius: 20px;
      text-transform: uppercase;
      letter-spacing: 0.5px;
    }}
    .pricing-badge {{
      display: inline-block;
      background-color: #10b981;
      color: #ffffff;
      font-size: 12px;
      font-weight: bold;
      padding: 4px 10px;
      border-radius: 20px;
      margin-left: 8px;
    }}
    .card {{
      background: #ffffff;
      border: 1px solid #e2e8f0;
      border-radius: 12px;
      padding: 24px;
      margin-bottom: 24px;
      box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }}
    .card h2 {{
      margin-top: 0;
      color: #0f172a;
      font-size: 20px;
      border-bottom: 2px solid #f1f5f9;
      padding-bottom: 10px;
    }}
    .pros-cons-grid {{
      display: flex;
      flex-wrap: wrap;
      gap: 16px;
    }}
    .pros-box, .cons-box {{
      flex: 1;
      min-width: 280px;
      padding: 16px;
      border-radius: 8px;
    }}
    .pros-box {{
      background-color: #f0fdf4;
      border: 1px solid #bbf7d0;
    }}
    .cons-box {{
      background-color: #fef2f2;
      border: 1px solid #fecaca;
    }}
    .pros-box h3 {{ color: #166534; margin-top: 0; }}
    .cons-box h3 {{ color: #991b1b; margin-top: 0; }}
    ul {{ padding-left: 20px; margin: 0; }}
    li {{ margin-bottom: 8px; list-style: none; }}
    .pros-box li strong {{ color: #16a34a; }}
    .cons-box li strong {{ color: #dc2626; }}
    .badge {{
      display: inline-block;
      background-color: #e2e8f0;
      color: #334155;
      padding: 6px 12px;
      border-radius: 6px;
      font-size: 13px;
      margin-right: 8px;
      margin-bottom: 8px;
      font-weight: 500;
    }}
    .disclaimer-box {{
      background-color: #fffbebfb;
      border: 1px solid #fef3c7;
      border-left: 4px solid #f59e0b;
      padding: 16px;
      border-radius: 6px;
      font-size: 13px;
      color: #78350f;
      margin-top: 30px;
    }}
    .footer-links {{
      text-align: center;
      margin-top: 24px;
      font-size: 14px;
    }}
    .footer-links a {{
      color: #2563eb;
      text-decoration: none;
      font-weight: 600;
      margin: 0 10px;
    }}
  </style>
</head>
<body>
  <div class="container">
    <div class="header">
      <span class="meta-tag">{category}</span>
      <span class="pricing-badge">{pricing_type}</span>
      <h1>{name}: Comprehensive Developer Review & Features Breakdown</h1>
      <p>Developer / Vendor: <strong>{developer}</strong> | Rating: <strong>{rating}</strong> | Pricing: <strong>{pricing}</strong></p>
    </div>

    <div class="card">
      <h2>Overview & Architecture</h2>
      <p><strong>{name}</strong> is designed to streamline modern programming workflows. Whether you are building large-scale backend systems, fast web applications, or CLI tools, selecting the right code editor significantly impacts developer ergonomics and velocity.</p>

      <div style="margin-top: 16px;">
        <strong>Key Highlights & Capabilities:</strong><br>
        <div style="margin-top: 8px;">
          {features_html}
        </div>
      </div>
    </div>

    <div class="card">
      <h2>Pros & Cons Analysis</h2>
      <div class="pros-cons-grid">
        <div class="pros-box">
          <h3>Advantages (The Good)</h3>
          <ul>
            {pros_html}
          </ul>
        </div>
        <div class="cons-box">
          <h3>Considerations (The Bad)</h3>
          <ul>
            {cons_html}
          </ul>
        </div>
      </div>
    </div>

    <div class="card">
      <h2>Best Use Cases & Verdict</h2>
      <p><strong>Ideal For:</strong> {best_for}</p>
      <p><strong>Pricing Model Breakdown:</strong> {pricing}. Developers can select the option that best fits their project complexity and team needs.</p>
    </div>

    <div class="disclaimer-box">
      <strong>Independent Publication Notice:</strong><br>
      {DISCLAIMER_TEXT}
    </div>

    <div class="footer-links">
      <a href="{BLOGGER_URL}" target="_blank" rel="noopener">IDE Guide Blog</a> |
      <a href="{YOUTUBE_URL}" target="_blank" rel="noopener">YouTube @IDEguide</a>
    </div>
  </div>
</body>
</html>
"""
    return amp_html


def generate_google_flow_video_spec(info: Dict[str, Any]) -> str:
    name = info["name"]
    category = info["category"]
    pricing = info["pricing"]
    pros = info["pros"]
    cons = info["cons"]
    best_for = info["best_for"]

    pros_str = "; ".join(pros)
    cons_str = "; ".join(cons)

    spec = f"""# Google Flow Video Specification: {name}

## 1. Video Metadata
- **Title:** Should You Use {name}? (Honest Review & Best Features)
- **Target Channels:** YouTube Shorts (@IDEguide) & YouTube Long-Form
- **Aspect Ratio:** 9:16 Vertical (Shorts) & 16:9 Landscape
- **Duration:** 60 Seconds (Shorts) / 3-5 Minutes (Full Review)
- **Category:** Developer Tools / IDE Review

---

## 2. Google Flow Scene-by-Scene Prompt Script

### Scene 1 (0:00 - 0:05) - The Hook
- **Visual Prompt:**
  `Cinematic macro shot of a developer typing at top speed on an RGB mechanical keyboard, camera zooming into glowing dark mode IDE screen displaying {name} logo with smooth cyan neon glow, 4k 60fps --ar 9:16`
- **Voiceover Narration:**
  "Is {name} actually the best code editor for developers today? Let's break down what makes it stand out!"
- **On-Screen Text:**
  `{name}: Best IDE in 2026?`

### Scene 2 (0:05 - 0:25) - Core Features & Workflow
- **Visual Prompt:**
  `Cinematic screen pan of {name} UI showing lightning fast code autocompletion, file navigation, and sleek dark syntax highlighting, soft studio rim lighting --ar 9:16`
- **Voiceover Narration:**
  "{name} is a {category} built for modern software engineering. It excels at {pros_str}."
- **On-Screen Text:**
  `Key Strength: Fast, Powerful & Modern`

### Scene 3 (0:25 - 0:42) - Pros & Cons (The Good & Bad)
- **Visual Prompt:**
  `Split screen visual graphic showing green checkmarks for performance and orange caution tags highlighting potential trade-offs like {cons_str}, clean minimalist developer desk backdrop --ar 9:16`
- **Voiceover Narration:**
  "The good? Unmatched speed and productivity. The bad? Keep in mind {cons_str}."
- **On-Screen Text:**
  `Pros & Cons Breakdown`

### Scene 4 (0:42 - 0:52) - Pricing & Recommendation
- **Visual Prompt:**
  `Sleek graphical overlay comparing Free vs Paid tier badges, fading to target developer persona coding happily --ar 9:16`
- **Voiceover Narration:**
  "{name} operates on a {pricing} model. It is best for {best_for}"
- **On-Screen Text:**
  `Pricing: {pricing}`

### Scene 5 (0:52 - 1:00) - CTA & Non-Sponsorship Disclosure
- **Visual Prompt:**
  `Minimalist animated IDE Guide badge with subscribe notification bell and non-sponsorship disclosure banner at bottom --ar 9:16`
- **Voiceover Narration:**
  "Subscribe to IDE Guide on YouTube and visit ideguide.blogspot.com for daily developer reviews. 100% independent and unsponsored!"
- **On-Screen Text:**
  `Subscribe @IDEguide | ideguide.blogspot.com`

---

## 3. Mandatory Non-Sponsorship Disclosure
{DISCLAIMER_TEXT}
"""
    return spec


def main():
    parser = argparse.ArgumentParser(description="IDE Guide Agentic Skill CLI Tool")
    parser.add_argument("--ide", type=str, help="Name of the IDE or Code Editor (e.g. Cursor, Zed, VS Code, PyCharm)")
    parser.add_argument("--repo", type=str, help="Repository URL (e.g. https://github.com/zed-industries/zed)")
    parser.add_argument("--output-dir", type=str, default="./output", help="Directory where generated content will be saved")
    parser.add_argument("--format", type=str, choices=["amp-blog", "video-spec", "all"], default="all", help="Output format selection")

    args = parser.parse_args()

    if not args.ide and not args.repo:
        parser.error("At least one of --ide or --repo must be provided.")

    ide_name = args.ide or ""
    info = get_ide_info(ide_name, args.repo)

    os.makedirs(args.output_dir, exist_ok=True)
    slug = re.sub(r'[^a-z0-9]+', '_', info['name'].lower()).strip('_')

    created_files = []

    if args.format in ["amp-blog", "all"]:
        amp_content = generate_amp_html_blog_post(info)
        amp_file = os.path.join(args.output_dir, f"post_{slug}.html")
        with open(amp_file, "w", encoding="utf-8") as f:
            f.write(amp_content)
        created_files.append(amp_file)

    if args.format in ["video-spec", "all"]:
        video_spec = generate_google_flow_video_spec(info)
        video_file = os.path.join(args.output_dir, f"video_spec_{slug}.md")
        with open(video_file, "w", encoding="utf-8") as f:
            f.write(video_spec)
        created_files.append(video_file)

    print(f"Successfully generated content for {info['name']}:")
    for fpath in created_files:
        print(f"  - {fpath}")


if __name__ == "__main__":
    main()
