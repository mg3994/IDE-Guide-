#!/usr/bin/env python3
"""
IDE Guide Daily Content Generator
Generates 3 AMP HTML blog posts (for ideguide.blogspot.com) and 3 Google Flow video specifications (for YouTube @IDEguide) daily.
"""

import json
import os
import re
import sys
import datetime
import urllib.request
import urllib.parse
from typing import Dict, List, Any, Optional

DISCLAIMER = (
    "Disclaimer: IDE Guide is an independent technical publication. "
    "This content is not sponsored, endorsed, or affiliated with any software vendor or editor developer mentioned above. "
    "All reviews and assessments are based strictly on objective developer evaluation."
)

CURATED_IDES: List[Dict[str, Any]] = [
    {
        "name": "Visual Studio Code",
        "key": "vscode",
        "tagline": "The ubiquitous open-source code editor with massive extension ecosystem",
        "license": "Freeware / Open Source core (MIT)",
        "pricing": "Free",
        "pros": ["Massive extension ecosystem", "Excellent multi-language support", "Integrated terminal and Git tools"],
        "cons": ["Memory footprint can grow with many extensions", "Electron-based overhead"],
        "ideal_for": "Web developers, full-stack engineers, and multi-language programmers",
        "description": "Visual Studio Code remains the benchmark for modern code editing with seamless AI integration and extension flexibility."
    },
    {
        "name": "Cursor",
        "key": "cursor",
        "tagline": "The AI-first code editor built for extreme developer velocity",
        "license": "Proprietary",
        "pricing": "Freemium ($20/mo Pro)",
        "pros": ["Native AI codebase indexing", "Multi-file diff generation", "VS Code extension compatibility"],
        "cons": ["Requires paid plan for unlimited fast AI models", "Closed source core"],
        "ideal_for": "Developers seeking deep AI agentic coding assistance and rapid prototyping",
        "description": "Cursor fork of VS Code embeds LLMs deep into code generation and project-wide context awareness."
    },
    {
        "name": "Zed Editor",
        "key": "zed",
        "tagline": "High-performance GPU-accelerated code editor written in Rust",
        "license": "Open Source (GPL / Apache 2.0)",
        "pricing": "Free / Open Source (Optional paid collaboration team features)",
        "pros": ["Blazing fast startup and sub-millisecond typing latency", "Real-time multiplayer collaborative editing", "Low memory footprint"],
        "cons": ["Extension ecosystem still maturing", "Fewer platform integrations than VS Code"],
        "ideal_for": "Performance purists, Rust enthusiasts, and teams wanting real-time pair programming",
        "description": "Zed redefines code editor performance by leveraging GPU rendering and Rust safety."
    },
    {
        "name": "Neovim",
        "key": "neovim",
        "tagline": "Hyperextensible Lua-based Vim text editor for terminal power users",
        "license": "Open Source (Apache 2.0 / Vim License)",
        "pricing": "100% Free & Open Source",
        "pros": ["Extremely lightweight and fast", "Unlimited modal editing customization via Lua", "Native LSP and tree-sitter support"],
        "cons": ["Steep learning curve for modal navigation", "Manual configuration required"],
        "ideal_for": "Terminal power users, DevOps engineers, and keyboard-driven developers",
        "description": "Neovim modernizes classic Vim with native Lua scriptability, asynchronous LSP, and modal mastery."
    },
    {
        "name": "JetBrains PyCharm",
        "key": "pycharm",
        "tagline": "The premier Python IDE for data science, web development, and backend services",
        "license": "Commercial / Community (Apache 2.0)",
        "pricing": "Freemium (Community Edition Free, Professional $249/yr)",
        "pros": ["Unmatched Python refactoring and code analysis", "Built-in database tools and Django support", "Robust debugging & profiler"],
        "cons": ["Higher RAM footprint", "Slower cold startup compared to lightweight editors"],
        "ideal_for": "Professional Python developers, data scientists, and backend engineers",
        "description": "PyCharm offers deep static code analysis and specialized tooling for Python production software."
    },
    {
        "name": "Windsurf Editor",
        "key": "windsurf",
        "tagline": "The agentic AI editor with Cascade flow state awareness",
        "license": "Proprietary",
        "pricing": "Freemium ($15/mo Pro)",
        "pros": ["Cascade AI flow state deep integration", "Collaborative agentic command execution", "VS Code compatibility"],
        "cons": ["Subscription required for high-volume LLM usage", "Proprietary AI engine"],
        "ideal_for": "Developers wanting seamless interactive AI command execution and multi-file editing",
        "description": "Windsurf combines traditional editing with Cascade flow AI agents that understand full project trees."
    },
    {
        "name": "Lapce",
        "key": "lapce",
        "tagline": "Lightning-fast native GUI code editor written in Rust with WASM plugin engine",
        "license": "Open Source (Apache 2.0)",
        "pricing": "100% Free & Open Source",
        "pros": ["Native GPU rendering with xi-rope backend", "WASM extension system for isolation", "Built-in modal Vim mode"],
        "cons": ["Plugin ecosystem in early growth stage", "Occasional visual UI glitches on cutting-edge features"],
        "ideal_for": "Developers wanting a lightweight native desktop UI editor faster than Electron",
        "description": "Lapce brings native desktop performance and WASM modularity to cross-platform code editing."
    },
    {
        "name": "Helix Editor",
        "key": "helix",
        "tagline": "Post-modern modal text editor built in Rust with built-in LSP and Tree-sitter",
        "license": "Open Source (MPL-2.0)",
        "pricing": "100% Free & Open Source",
        "pros": ["Zero config needed for LSP and syntax highlighting", "Selection-first modal editing model", "Extremely low resource usage"],
        "cons": ["No plugin system yet (in development)", "Terminal-only interface"],
        "ideal_for": "Developers who want modal editing out-of-the-box without editing 1,000 lines of config",
        "description": "Helix simplifies modal editing with Kakoune-inspired selection mechanics and native LSP integration."
    },
    {
        "name": "JetBrains WebStorm",
        "key": "webstorm",
        "tagline": "The smartest JavaScript and TypeScript IDE for modern web development",
        "license": "Commercial",
        "pricing": "Paid ($69/yr individual)",
        "pros": ["Incredible refactoring and auto-imports for JS/TS", "Seamless framework integration (React, Vue, Angular)", "Integrated test runner & debugger"],
        "cons": ["Commercial paid license required", "Resource intensive on smaller devices"],
        "ideal_for": "Enterprise frontend and full-stack JavaScript/TypeScript developers",
        "description": "WebStorm provides intelligent code completion and automated refactoring across complex frontend codebases."
    },
    {
        "name": "Sublime Text 4",
        "key": "sublime_text",
        "tagline": "Sophisticated text editor for code, markup, and prose with custom C++ UI toolkit",
        "license": "Commercial Evaluation",
        "pricing": "Paid ($99 one-time license)",
        "pros": ["Instant launch speed and microsecond responsiveness", "GPU rendering engine", "Python API for rich extensions"],
        "cons": ["Paid license popup in free evaluation", "Smaller AI ecosystem than newer competitors"],
        "ideal_for": "Developers who value speed, minimal UI, and instant file opening",
        "description": "Sublime Text 4 continues to set the gold standard for launch speed and native keyboard responsiveness."
    },
    {
        "name": "JetBrains Fleet",
        "key": "fleet",
        "tagline": "Next-generation lightweight distributed editor and IDE by JetBrains",
        "license": "Freemium / Commercial",
        "pricing": "Freemium (Free preview / Pro subscription)",
        "pros": ["Lightweight start mode with full Smart IDE mode toggle", "Distributed cloud development architecture", "Multi-language support"],
        "cons": ["Still in active development preview", "Plugins ecosystem still building"],
        "ideal_for": "Developers wanting a flexible editor that scales from simple text file editing to heavy cloud IDE capabilities",
        "description": "Fleet breaks down JetBrains IDE intelligence into a light, distributed, cross-platform architecture."
    },
    {
        "name": "Eclipse IDE",
        "key": "eclipse",
        "tagline": "Classic extensible Java enterprise development platform",
        "license": "Open Source (EPL-2.0)",
        "pricing": "100% Free & Open Source",
        "pros": ["Deep Java ecosystem and enterprise compiler integration", "Massive plugin library", "Comprehensive workspace management"],
        "cons": ["Heavier and dated visual interface", "Higher startup latency"],
        "ideal_for": "Enterprise Java developers and legacy code maintainers",
        "description": "Eclipse IDE remains a cornerstone of enterprise Java application development and open-source tooling."
    }
]

def load_history(history_filepath: str) -> Dict[str, Any]:
    if os.path.exists(history_filepath):
        try:
            with open(history_filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            pass
    return {"covered_keys": [], "daily_logs": []}

def save_history(history_filepath: str, history_data: Dict[str, Any]) -> None:
    os.makedirs(os.path.dirname(history_filepath), exist_ok=True)
    with open(history_filepath, 'w', encoding='utf-8') as f:
        json.dump(history_data, f, indent=2)

def fetch_trending_ides_from_github() -> List[Dict[str, Any]]:
    """Fetch additional IDEs/editors from GitHub search API if available."""
    url = "https://api.github.com/search/repositories?q=topic:ide+topic:editor&sort=stars&order=desc&per_page=10"
    req = urllib.request.Request(url, headers={"User-Agent": "IDEGuide-Generator"})
    discovered = []
    try:
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            for item in data.get("items", []):
                key = item["name"].lower().replace("-", "_").replace(".", "_")
                discovered.append({
                    "name": item["name"],
                    "key": key,
                    "tagline": item.get("description") or f"Open source code editor repository {item['full_name']}",
                    "license": item.get("license", {}).get("name") if item.get("license") else "Open Source",
                    "pricing": "100% Free & Open Source",
                    "pros": ["Active open source community", f"Over {item.get('stargazers_count', 0)} GitHub stars", "Customizable source code"],
                    "cons": ["Requires setup from source or releases", "Community-driven support"],
                    "ideal_for": "Open source developers and custom workflow builders",
                    "description": item.get("description") or f"{item['name']} is a high-performance open-source code editing project on GitHub.",
                    "html_url": item.get("html_url")
                })
    except Exception as e:
        # Fallback to curated if offline or rate limited
        pass
    return discovered

def select_daily_ides(history_data: Dict[str, Any], count: int = 3) -> List[Dict[str, Any]]:
    covered = set(history_data.get("covered_keys", []))

    # Attempt GitHub discovery first
    discovered = fetch_trending_ides_from_github()
    all_candidates = CURATED_IDES + [d for d in discovered if d["key"] not in {c["key"] for c in CURATED_IDES}]

    uncovered = [ide for ide in all_candidates if ide["key"] not in covered]

    if len(uncovered) < count:
        # Reset memory cycle if we ran out of unique IDEs
        covered.clear()
        uncovered = all_candidates

    selected = uncovered[:count]
    return selected

def generate_amp_html_post(ide: Dict[str, Any], date_str: str) -> str:
    title = f"{ide['name']} Guide: Features, Pros & Cons, and Pricing ({date_str})"
    canonical_url = f"https://ideguide.blogspot.com/{date_str.replace('-', '/')}/{ide['key']}-guide.html"

    pros_html = "".join([f"<li>{p}</li>" for p in ide['pros']])
    cons_html = "".join([f"<li>{c}</li>" for c in ide['cons']])

    amp_html = f"""<!doctype html>
<html ⚡ lang="en">
<head>
  <meta charset="utf-8">
  <title>{title}</title>
  <link rel="canonical" href="{canonical_url}">
  <meta name="viewport" content="width=device-width,minimum-scale=1,initial-scale=1">
  <style amp-boilerplate>body{{-webkit-animation:-amp-start 8s steps(1,end) 0s 1 normal both;-moz-animation:-amp-start 8s steps(1,end) 0s 1 normal both;-ms-animation:-amp-start 8s steps(1,end) 0s 1 normal both;animation:-amp-start 8s steps(1,end) 0s 1 normal both}}@-webkit-keyframes -amp-start{{from{{visibility:hidden}}to{{visibility:visible}}}}@-moz-keyframes -amp-start{{from{{visibility:hidden}}to{{visibility:visible}}}}@-ms-keyframes -amp-start{{from{{visibility:hidden}}to{{visibility:visible}}}}@-o-keyframes -amp-start{{from{{visibility:hidden}}to{{visibility:visible}}}}@keyframes -amp-start{{from{{visibility:hidden}}to{{visibility:visible}}}}</style><noscript><style amp-boilerplate>body{{-webkit-animation:none;-moz-animation:none;-ms-animation:none;animation:none}}</style></noscript>
  <script async src="https://cdn.ampproject.org/v0.js"></script>
  <style amp-custom>
    body {{
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
      line-height: 1.6;
      color: #1f2328;
      background-color: #ffffff;
      padding: 16px;
      max-width: 800px;
      margin: 0 auto;
    }}
    .header {{
      border-bottom: 2px solid #0969da;
      padding-bottom: 12px;
      margin-bottom: 20px;
    }}
    .title {{
      font-size: 28px;
      color: #0969da;
      margin: 0 0 8px 0;
    }}
    .tagline {{
      font-size: 16px;
      color: #57606a;
      font-style: italic;
    }}
    .badge-container {{
      display: flex;
      gap: 10px;
      margin: 16px 0;
    }}
    .badge {{
      background: #f6f8fa;
      border: 1px solid #d0d7de;
      border-radius: 6px;
      padding: 6px 12px;
      font-size: 14px;
      font-weight: 600;
    }}
    .section {{
      margin-bottom: 24px;
    }}
    h2 {{
      font-size: 20px;
      color: #1f2328;
      border-left: 4px solid #0969da;
      padding-left: 8px;
    }}
    ul {{
      padding-left: 20px;
    }}
    .disclaimer {{
      background-color: #fff8c5;
      border: 1px solid #d4a72c;
      border-radius: 6px;
      padding: 14px;
      font-size: 13px;
      color: #4d3800;
      margin-top: 32px;
    }}
  </style>
</head>
<body>
  <div class="header">
    <h1 class="title">{ide['name']} Guide</h1>
    <div class="tagline">{ide['tagline']}</div>
  </div>

  <div class="badge-container">
    <span class="badge">Pricing: {ide['pricing']}</span>
    <span class="badge">License: {ide['license']}</span>
  </div>

  <div class="section">
    <h2>Overview</h2>
    <p>{ide['description']}</p>
  </div>

  <div class="section">
    <h2>Best Suited For</h2>
    <p>{ide['ideal_for']}</p>
  </div>

  <div class="section">
    <h2>Key Advantages (Pros)</h2>
    <ul>
      {pros_html}
    </ul>
  </div>

  <div class="section">
    <h2>Considerations & Trade-offs (Cons)</h2>
    <ul>
      {cons_html}
    </ul>
  </div>

  <div class="disclaimer">
    <strong>Notice:</strong> {DISCLAIMER}
  </div>
</body>
</html>"""
    return amp_html

def generate_google_flow_video_spec(ide: Dict[str, Any], date_str: str, index: int) -> Dict[str, Any]:
    spec = {
        "channel": "@IDEguide",
        "video_index": index,
        "ide_name": ide["name"],
        "date": date_str,
        "format": "YouTube Short (9:16) & YouTube Video Spec (16:9)",
        "disclaimer": DISCLAIMER,
        "google_flow_prompts": [
            {
                "scene": 1,
                "title": "Hook & Code Editor Visual",
                "timecode": "00:00 - 00:05",
                "prompt": f"Macro cinematic close-up shot of dark mode UI of {ide['name']} displaying syntax highlighted code on a high refresh rate curved display. Dynamic soft pan, neon ambient lighting, photorealistic 8k, 60fps.",
                "voiceover": f"Looking for the best editor? Here is what you need to know about {ide['name']} in 45 seconds!"
            },
            {
                "scene": 2,
                "title": "Feature & Workflow Showcase",
                "timecode": "00:05 - 00:25",
                "prompt": f"Smooth screen recording animation showcasing key feature of {ide['name']}: {ide['pros'][0]}. Fluid zooming into interface controls with cybernetic UI accent glows.",
                "voiceover": f"{ide['name']} shines with {ide['pros'][0]} and {ide['pros'][1]}."
            },
            {
                "scene": 3,
                "title": "Pricing & Comparison",
                "timecode": "00:25 - 00:38",
                "prompt": f"Split screen holographic card showing pricing model '{ide['pricing']}' and licensing '{ide['license']}'. Modern dark theme glassmorphism graphic.",
                "voiceover": f"Pricing is {ide['pricing']}. It is best suited for {ide['ideal_for']}."
            },
            {
                "scene": 4,
                "title": "Outro & Disclaimer",
                "timecode": "00:38 - 00:45",
                "prompt": "Call to action graphic displaying YouTube channel @IDEguide and website ideguide.blogspot.com with animated subscribe motion button.",
                "voiceover": f"Subscribe to IDE Guide on YouTube and visit ideguide.blogspot.com for full technical breakdown. {DISCLAIMER}"
            }
        ]
    }
    return spec

def main():
    dry_run = "--dry-run" in sys.argv
    date_str = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d")

    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    history_filepath = os.path.join(root_dir, "content", "history.json")
    output_dir = os.path.join(root_dir, "content", date_str)

    history_data = load_history(history_filepath)
    selected_ides = select_daily_ides(history_data, count=3)

    print(f"Generating content for date: {date_str}")
    for idx, ide in enumerate(selected_ides, start=1):
        print(f" [{idx}/3] Processing IDE: {ide['name']} ({ide['key']})")
        amp_post = generate_amp_html_post(ide, date_str)
        video_spec = generate_google_flow_video_spec(ide, date_str, idx)

        if not dry_run:
            os.makedirs(output_dir, exist_ok=True)
            post_filename = f"post_{idx}_{ide['key']}.html"
            video_filename = f"video_spec_{idx}_{ide['key']}.json"

            with open(os.path.join(output_dir, post_filename), "w", encoding="utf-8") as f:
                f.write(amp_post)
            with open(os.path.join(output_dir, video_filename), "w", encoding="utf-8") as f:
                json.dump(video_spec, f, indent=2)

            if ide["key"] not in history_data["covered_keys"]:
                history_data["covered_keys"].append(ide["key"])

    if not dry_run:
        history_data["daily_logs"].append({
            "date": date_str,
            "ides": [ide["key"] for ide in selected_ides]
        })
        save_history(history_filepath, history_data)
        print(f"Successfully generated daily content package in {output_dir}")
    else:
        print("[Dry Run] Generation completed successfully without writing files.")

if __name__ == "__main__":
    main()
