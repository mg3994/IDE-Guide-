#!/usr/bin/env python3
"""
IDE Guide - Daily Content Generator
Generates 3 AMP HTML Blogger posts and 3 Google Flow Video Generation Specs every day.
Stores history in content/history.json and outputs to content/YYYY-MM-DD/
"""

import json
import os
import sys
import datetime
import urllib.request
import urllib.error
import re

DISCLAIMER_TEXT = (
    "Disclaimer: IDE Guide is an independent technical publication. "
    "This content is not sponsored, endorsed, or affiliated with any software vendor or editor developer mentioned above. "
    "All reviews and assessments are based strictly on objective developer evaluation."
)

CURATED_IDES = [
    {
        "id": "vscode",
        "name": "Visual Studio Code",
        "vendor": "Microsoft",
        "category": "General Purpose Code Editor",
        "pricing_type": "Free / Open Source (Core)",
        "pricing_details": "Free community edition under MIT/proprietary binaries. Rich marketplace.",
        "pros": [
            "Massive extension ecosystem with thousands of plugins and themes.",
            "Exceptional language support with LSP (Language Server Protocol).",
            "Native Git integration, remote SSH development, and dev containers.",
            "Fast performance with lightweight Electron engine."
        ],
        "cons": [
            "Can consume significant memory with many active extensions.",
            "Microsoft telemetry enabled by default (can be disabled or avoided with VSCodium).",
            "Not a full out-of-the-box heavy IDE without initial setup."
        ],
        "best_for": "Developers seeking a highly customizable, fast, all-purpose editor with huge ecosystem support.",
        "github_repo": "microsoft/vscode",
        "official_url": "https://code.visualstudio.com/"
    },
    {
        "id": "cursor",
        "name": "Cursor AI Code Editor",
        "vendor": "Anysphere",
        "category": "AI-First Code Editor",
        "pricing_type": "Freemium ($20/mo Pro)",
        "pricing_details": "Free tier with monthly fast requests; Pro tier at $20/month for unlimited fast AI usage.",
        "pros": [
            "Deeply integrated Claude 3.5 Sonnet & GPT-4o multi-file codebase editing.",
            "Instant codebase indexing with semantic search (.cursorrules support).",
            "Full VS Code extension compatibility with zero migration friction.",
            "Predictive inline edits with smart cursor positioning."
        ],
        "cons": [
            "Requires active subscription for heavy power-user AI indexing.",
            "Proprietary cloud features require sending code embeddings to backend.",
            "Fork of VS Code, dependent on upstream VS Code release syncs."
        ],
        "best_for": "Software engineers wanting high-productivity AI coding assistance with full VS Code extension support.",
        "github_repo": "getcursor/cursor",
        "official_url": "https://cursor.com/"
    },
    {
        "id": "intellij-idea",
        "name": "JetBrains IntelliJ IDEA",
        "vendor": "JetBrains",
        "category": "Enterprise Java / Polyglot IDE",
        "pricing_type": "Freemium (Free Community / Paid Ultimate)",
        "pricing_details": "Free Community Edition; Ultimate Edition from $16.90/month or $169/year.",
        "pros": [
            "Unrivaled refactoring, static code analysis, and smart code completion.",
            "First-class framework integration (Spring, Jakarta EE, React, Angular).",
            "Built-in database tooling, profilers, and visual debugger.",
            "Deep static analysis catches subtle logic bugs before compilation."
        ],
        "cons": [
            "Heavy RAM and CPU resource consumption on huge monorepos.",
            "Steep learning curve with extensive toolbars and configuration panels.",
            "Full feature set locked behind paid Ultimate subscription."
        ],
        "best_for": "Enterprise Java, Kotlin, and full-stack developers requiring top-tier refactoring and deep static analysis.",
        "github_repo": "JetBrains/intellij-community",
        "official_url": "https://www.jetbrains.com/idea/"
    },
    {
        "id": "zed",
        "name": "Zed Editor",
        "vendor": "Zed Industries",
        "category": "High-Performance GPU-Accelerated Editor",
        "pricing_type": "Free / Open Source",
        "pricing_details": "Free open-source editor; optional cloud multiplayer features.",
        "pros": [
            "Blazing fast startup and rendering written in Rust with GPU rendering.",
            "Built-in collaborative multiplayer coding with instant screen control.",
            "Native AI assistance integrating OpenAI, Anthropic, and local Ollama models.",
            "Extremely low memory footprint and responsive typing latency."
        ],
        "cons": [
            "Ecosystem and extension library still growing compared to VS Code.",
            "Linux and macOS supported; Windows support in active development.",
            "Fewer niche language debuggers out-of-the-box."
        ],
        "best_for": "Developers prioritizing raw performance, minimal latency, Rust reliability, and real-time multiplayer pair programming.",
        "github_repo": "zed-industries/zed",
        "official_url": "https://zed.dev/"
    },
    {
        "id": "windsurf",
        "name": "Windsurf Editor",
        "vendor": "Codeium",
        "category": "Agentic AI Code Editor",
        "pricing_type": "Freemium ($15/mo Pro)",
        "pricing_details": "Free tier with daily cascade requests; Pro tier at $15/month.",
        "pros": [
            "Innovative 'Cascade' agentic AI workflow blending editor state and deep terminal control.",
            "Real-time synchronized understanding of code edits and command output.",
            "Extremely responsive local-first search indexing.",
            "Seamless VS Code extension compatibility."
        ],
        "cons": [
            "Newer product with rapid UI iterations.",
            "Agentic autonomous edits require developer verification.",
            "Pro features rely on Codeium cloud models."
        ],
        "best_for": "Developers looking for autonomous AI agentic workflows that execute terminal commands and multi-file code modifications.",
        "github_repo": "Exafunction/codeium",
        "official_url": "https://codeium.com/windsurf"
    },
    {
        "id": "neovim",
        "name": "Neovim",
        "vendor": "Neovim Community",
        "category": "Modal Terminal-Based Text Editor",
        "pricing_type": "Free / Open Source (Apache 2.0)",
        "pricing_details": "100% Free and open source.",
        "pros": [
            "Ultra-lightweight, modal keybindings for unmatched editing speed.",
            "Built-in Lua scripting engine for unlimited extensibility.",
            "Native LSP, Treesitter syntax parsing, and async jobs.",
            "Runs anywhere over SSH, terminal, or GUI frontends."
        ],
        "cons": [
            "Steep learning curve requiring modal vim muscle memory.",
            "Requires manual configuration (or distros like LazyVim, NvChad).",
            "No default GUI mouse interaction out of the box."
        ],
        "best_for": "Keyboard-driven power users, terminal enthusiasts, and developers who demand complete control over their editing environment.",
        "github_repo": "neovim/neovim",
        "official_url": "https://neovim.io/"
    },
    {
        "id": "sublime-text",
        "name": "Sublime Text 4",
        "vendor": "Sublime HQ",
        "category": "Lightweight High-Speed Text Editor",
        "pricing_type": "Paid ($99 per license, free evaluation)",
        "pricing_details": "$99 one-time purchase with 3 years of updates; free evaluation mode.",
        "pros": [
            "Extremely fast startup time and instant file opening even on multi-GB files.",
            "GPU accelerated rendering for buttery smooth scrolling.",
            "Multi-tab side-by-side split layouts with powerful regex search.",
            "Python API and Package Control extension system."
        ],
        "cons": [
            "Proprietary single-developer company backend.",
            "Lacks native out-of-the-box AI autocompletion without third-party plugins.",
            "Requires $99 license key after evaluation period."
        ],
        "best_for": "Developers who value instant startup speed, zero lag, minimal memory usage, and simple multi-file search.",
        "github_repo": "sublimehq/sublime_text",
        "official_url": "https://www.sublimetext.com/"
    },
    {
        "id": "pycharm",
        "name": "JetBrains PyCharm",
        "vendor": "JetBrains",
        "category": "Dedicated Python & Data Science IDE",
        "pricing_type": "Freemium (Free Community / Paid Professional)",
        "pricing_details": "Free Community Edition; Professional Edition at $9.90/month or $99/year.",
        "pros": [
            "Best-in-class Python code analysis, type checking, and virtual environment management.",
            "Native Jupyter Notebook support, SQL database tools, and Django/FastAPI integration.",
            "Powerful visual debugger, test runner, and coverage analyzer.",
            "Smart refactoring tailored specifically for Python dynamic code bases."
        ],
        "cons": [
            "Resource heavy on machines with limited RAM (8GB or under).",
            "Web framework tools locked behind Professional tier.",
            "Overkill for small single-file Python scripts."
        ],
        "best_for": "Professional Python engineers, web developers (Django/FastAPI), and data scientists needing deep environment tooling.",
        "github_repo": "JetBrains/intellij-community",
        "official_url": "https://www.jetbrains.com/pycharm/"
    },
    {
        "id": "fleet",
        "name": "JetBrains Fleet",
        "vendor": "JetBrains",
        "category": "Lightweight Distributed Polyglot Editor",
        "pricing_type": "Freemium",
        "pricing_details": "Free preview tier; subscription integration with JetBrains ecosystem.",
        "pros": [
            "Lightweight architecture that transforms into a full IDE engine on demand.",
            "Built-in remote development, space integration, and collaborative editing.",
            "Smart AI assistant built directly into the UI.",
            "Clean, modern, distraction-free minimalist user interface."
        ],
        "cons": [
            "Still maturing relative to classic JetBrains IDEs.",
            "Fewer plugin extensions than VS Code marketplace.",
            "Requires JetBrains backend for smart engine mode."
        ],
        "best_for": "Developers looking for a modern, lightweight JetBrains alternative with flexible remote and cloud dev workflows.",
        "github_repo": "JetBrains/fleet",
        "official_url": "https://www.jetbrains.com/fleet/"
    },
    {
        "id": "lapce",
        "name": "Lapce",
        "vendor": "Lapce Community",
        "category": "Lightning-Fast Native Rust Editor",
        "pricing_type": "Free / Open Source (Apache 2.0)",
        "pricing_details": "100% Free open-source editor.",
        "pros": [
            "Native UI written in Rust (Druid/Floem) with GPU acceleration.",
            "Built-in LSP support with zero plugin setup required for basic languages.",
            "Remote development over SSH natively built in.",
            "Wasm plugin system for safe sandboxed extensions."
        ],
        "cons": [
            "Community plugin ecosystem is still in early growth stages.",
            "Occasional visual glitches on experimental features.",
            "Fewer advanced enterprise integrations."
        ],
        "best_for": "Developers wanting an open-source, lightning-fast native desktop editor with modern LSP capabilities.",
        "github_repo": "lapce/lapce",
        "official_url": "https://lapce.dev/"
    },
    {
        "id": "helix",
        "name": "Helix Editor",
        "vendor": "Helix Community",
        "category": "Post-Modern Terminal Modal Editor",
        "pricing_type": "Free / Open Source (MPL 2.0)",
        "pricing_details": "100% Free and open source.",
        "pros": [
            "Selection-first (Kakoune-style) modal editing model.",
            "Built-in Tree-sitter syntax highlighting and LSP support out of the box with zero config.",
            "Written in Rust for instant execution and minimal memory footprint.",
            "Built-in fuzzy finder, multi-cursor editing, and theme support."
        ],
        "cons": [
            "Plugin system still under active architectural design.",
            "Different muscle memory from standard Vim keybindings.",
            "Pure terminal interface (no native desktop GUI elements)."
        ],
        "best_for": "Terminal developers looking for an out-of-the-box modal editor that requires no plugin setup for full LSP support.",
        "github_repo": "helix-editor/helix",
        "official_url": "https://helix-editor.com/"
    },
    {
        "id": "replit",
        "name": "Replit Agent & IDE",
        "vendor": "Replit Inc.",
        "category": "Cloud-Native Collaborative AI IDE",
        "pricing_type": "Freemium ($10-$20/mo Core)",
        "pricing_details": "Free tier available; Replit Core subscription for AI Agent and cloud deployments.",
        "pros": [
            "Zero installation needed—runs entirely inside browser with instant cloud containers.",
            "Replit AI Agent can build and deploy full stack web applications from natural language prompts.",
            "Instant multiplayer real-time collaboration with custom URL sharing.",
            "Built-in database, authentication, and push-button deployment hosting."
        ],
        "cons": [
            "Requires continuous internet connection to cloud environment.",
            "Resource limits on free container instances.",
            "Can become costly for heavy compute or persistent hosted apps."
        ],
        "best_for": "Beginners, educators, rapid prototypers, and web developers building full-stack cloud applications with AI agents.",
        "github_repo": "replit/replit",
        "official_url": "https://replit.com/"
    }
]


def load_history(history_file="content/history.json"):
    if os.path.exists(history_file):
        try:
            with open(history_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"Warning: Could not read {history_file}: {e}")
    return {"covered_ides": [], "history": []}


def save_history(history_data, history_file="content/history.json"):
    os.makedirs(os.path.dirname(os.path.abspath(history_file)), exist_ok=True)
    with open(history_file, "w", encoding="utf-8") as f:
        json.dump(history_data, f, indent=2, ensure_ascii=False)


def build_amp_html(ide_info):
    name = ide_info["name"]
    vendor = ide_info["vendor"]
    category = ide_info["category"]
    pricing_type = ide_info["pricing_type"]
    pricing_details = ide_info["pricing_details"]
    best_for = ide_info["best_for"]
    official_url = ide_info.get("official_url", "https://ideguide.blogspot.com/")
    pros_lis = "".join([f"<li><strong>{p.split(':')[0] if ':' in p else p}</strong>: {p.split(':', 1)[1] if ':' in p else ''}</li>" if ':' in p else f"<li>{p}</li>" for p in ide_info["pros"]])
    cons_lis = "".join([f"<li><strong>{c.split(':')[0] if ':' in c else c}</strong>: {c.split(':', 1)[1] if ':' in c else ''}</li>" if ':' in c else f"<li>{c}</li>" for c in ide_info["cons"]])

    canonical_url = f"https://ideguide.blogspot.com/p/{ide_info['id']}.html"

    amp_html = f"""<!doctype html>
<html ⚡ lang="en">
<head>
  <meta charset="utf-8">
  <script async src="https://cdn.ampproject.org/v0.js"></script>
  <title>{name} Review & Guide - IDE Guide</title>
  <link rel="canonical" href="{canonical_url}">
  <meta name="viewport" content="width=device-width,minimum-scale=1,initial-scale=1">
  <style amp-boilerplate>body{{-webkit-animation:-amp-start 8s steps(1,end) 0s 1 normal partway;-moz-animation:-amp-start 8s steps(1,end) 0s 1 normal partway;-ms-animation:-amp-start 8s steps(1,end) 0s 1 normal partway;animation:-amp-start 8s steps(1,end) 0s 1 normal partway}}@-webkit-keyframes -amp-start{{from{{visibility:hidden}}to{{visibility:visible}}}}@-moz-keyframes -amp-start{{from{{visibility:hidden}}to{{visibility:visible}}}}@-ms-keyframes -amp-start{{from{{visibility:hidden}}to{{visibility:visible}}}}@-o-keyframes -amp-start{{from{{visibility:hidden}}to{{visibility:visible}}}}@keyframes -amp-start{{from{{visibility:hidden}}to{{visibility:visible}}}}</style><noscript><style amp-boilerplate>body{{-webkit-animation:none;-moz-animation:none;-ms-animation:none;animation:none}}</style></noscript>
  <style amp-custom>
    body {{
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
      line-height: 1.6;
      color: #1a202c;
      background-color: #f7fafc;
      margin: 0;
      padding: 0;
    }}
    .container {{
      max-width: 800px;
      margin: 0 auto;
      padding: 24px 16px;
    }}
    .card {{
      background: #ffffff;
      border-radius: 12px;
      padding: 32px 24px;
      box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
      margin-bottom: 24px;
    }}
    .badge {{
      display: inline-block;
      padding: 4px 12px;
      border-radius: 9999px;
      font-size: 0.85rem;
      font-weight: 600;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      margin-right: 8px;
    }}
    .badge-primary {{ background: #ebf8ff; color: #2b6cb0; }}
    .badge-price {{ background: #e6fffa; color: #234e52; }}
    h1 {{ font-size: 2.2rem; color: #2d3748; margin-top: 12px; margin-bottom: 8px; font-weight: 800; }}
    .subtitle {{ color: #718096; font-size: 1.1rem; margin-bottom: 24px; }}
    h2 {{ color: #2b6cb0; border-bottom: 2px solid #e2e8f0; padding-bottom: 8px; margin-top: 32px; font-size: 1.5rem; }}
    ul {{ padding-left: 20px; }}
    li {{ margin-bottom: 10px; }}
    .good-box {{ background-color: #f0fff4; border-left: 4px solid #38a169; padding: 16px 20px; border-radius: 4px; margin-bottom: 20px; }}
    .bad-box {{ background-color: #fff5f5; border-left: 4px solid #e53e3e; padding: 16px 20px; border-radius: 4px; margin-bottom: 20px; }}
    .verdict-box {{ background-color: #f7fafc; border: 1px solid #e2e8f0; border-radius: 8px; padding: 20px; margin-top: 24px; }}
    .official-btn {{
      display: inline-block;
      background: #3182ce;
      color: #ffffff;
      text-decoration: none;
      padding: 12px 24px;
      border-radius: 6px;
      font-weight: 600;
      margin-top: 16px;
    }}
    .disclaimer-box {{
      background: #edf2f7;
      border: 1px solid #cbd5e0;
      border-radius: 8px;
      padding: 16px;
      font-size: 0.88rem;
      color: #4a5568;
      margin-top: 40px;
    }}
  </style>
</head>
<body>
  <div class="container">
    <div class="card">
      <div>
        <span class="badge badge-primary">{category}</span>
        <span class="badge badge-price">{pricing_type}</span>
      </div>
      <h1>{name} Evaluation & Developer Guide</h1>
      <p class="subtitle">Developed by {vendor} | Independent Assessment by IDE Guide</p>

      <h2>1. Overview & Architecture</h2>
      <p>{name} is a {category.lower()} built by {vendor}. In this guide, we evaluate its performance, developer productivity features, licensing model, and key pros and cons.</p>

      <h2>2. Key Advantages (The Good)</h2>
      <div class="good-box">
        <ul>
          {pros_lis}
        </ul>
      </div>

      <h2>3. Drawbacks & Limitations (The Bad)</h2>
      <div class="bad-box">
        <ul>
          {cons_lis}
        </ul>
      </div>

      <h2>4. Pricing & Licensing Breakdown</h2>
      <p><strong>License Model:</strong> {pricing_type}</p>
      <p>{pricing_details}</p>

      <h2>5. Recommendation: Is {name} Right for You?</h2>
      <div class="verdict-box">
        <p><strong>Target Developer Audience:</strong> {best_for}</p>
        <p><a href="{official_url}" target="_blank" rel="noopener" class="official-btn">Visit Official {name} Website</a></p>
      </div>

      <div class="disclaimer-box">
        <p><strong>Independent Publication Disclosure:</strong></p>
        <p>{DISCLAIMER_TEXT}</p>
      </div>
    </div>
  </div>
</body>
</html>"""
    return amp_html


def build_google_flow_spec(ide_info):
    name = ide_info["name"]
    category = ide_info["category"]
    pricing_type = ide_info["pricing_type"]
    best_for = ide_info["best_for"]

    pros_str = "; ".join(ide_info["pros"][:2])
    cons_str = "; ".join(ide_info["cons"][:2])

    voiceover_script = (
        f"Thinking about trying {name}? Let's break down the good, the bad, and who it's actually best for in 60 seconds! "
        f"{name} is a powerful {category.lower()}. "
        f"On the positive side, {pros_str}. "
        f"However, keep in mind: {cons_str}. "
        f"Pricing structure is {pricing_type}. "
        f"Our verdict: {best_for}. "
        f"Subscribe to IDE Guide on YouTube and visit ideguide.blogspot.com for full technical breakdowns!"
    )

    scenes = [
        {
            "scene_number": 1,
            "timestamp": "00:00 - 00:06",
            "camera_framing": "Extreme close-up macro lens macro shot, rack focus onto mechanical keyboard and glowing dark mode monitor code editor.",
            "lighting": "High-contrast dark developer studio, cyan and magenta ambient backlight glow.",
            "visual_prompt": f"Cinematic 4K shot of modern code editor displaying {name} interface with vibrant syntax highlighting in dark workstation room, neon LED rim light.",
            "narration": f"Thinking about trying {name}? Let's break down the good, the bad, and who it's actually best for in 60 seconds!"
        },
        {
            "scene_number": 2,
            "timestamp": "00:06 - 00:20",
            "camera_framing": "Over-the-shoulder medium shot, fast typing and smooth screen recording simulation showing code completion.",
            "lighting": "Soft screen glow highlighting developer face and hands, subtle background bokeh.",
            "visual_prompt": f"A skilled developer typing rapidly in {name}, showcasing smooth UI animations, auto-completion popups, and crisp code layout on high-resolution monitor.",
            "narration": f"{name} is a {category.lower()}. On the positive side: {pros_str}."
        },
        {
            "scene_number": 3,
            "timestamp": "00:20 - 00:35",
            "camera_framing": "Side angle close-up with dynamic split-screen comparison aesthetic, subtle red warning accent hue.",
            "lighting": "Deep dark theme with soft amber accent lighting on desk setup.",
            "visual_prompt": f"Close-up of developer reviewing telemetry settings and resource usage metrics for {name} on sleek laptop screen.",
            "narration": f"However, keep in mind: {cons_str}."
        },
        {
            "scene_number": 4,
            "timestamp": "00:35 - 00:50",
            "camera_framing": "Medium wide desktop setup pan, showing dual monitors and clean developer setup.",
            "lighting": "Warm ambient studio lighting, balanced desk lamp highlight.",
            "visual_prompt": f"Elegant widescreen view of a modern software engineering desk setup with {name} open, highlighting pricing badge: {pricing_type}.",
            "narration": f"Pricing structure is {pricing_type}. Our verdict: {best_for}."
        },
        {
            "scene_number": 5,
            "timestamp": "00:50 - 01:00",
            "camera_framing": "Frontal card graphics overlay with channel branding @IDEguide and Blogger URL.",
            "lighting": "Bright cinematic backlight with subtle particle float.",
            "visual_prompt": "Clean motion graphics displaying YouTube handle @IDEguide and Website ideguide.blogspot.com with non-sponsorship disclosure badge.",
            "narration": "Subscribe to IDE Guide on YouTube and visit ideguide.blogspot.com for full technical breakdowns!"
        }
    ]

    spec_data = {
        "title": f"{name} Review: Good vs Bad | IDE Guide",
        "youtube_channel": "@IDEguide",
        "blogger_url": "https://ideguide.blogspot.com/",
        "target_format": "YouTube Short (9:16 vertical 1080x1920) & Main Video (16:9)",
        "ide_name": name,
        "vendor": ide_info["vendor"],
        "category": category,
        "pricing_type": pricing_type,
        "voiceover_script": voiceover_script,
        "scenes": scenes,
        "disclaimer": DISCLAIMER_TEXT
    }

    return spec_data


def build_google_flow_markdown(spec_data):
    md = f"""# Google Flow Video Spec: {spec_data['ide_name']}

- **Title:** {spec_data['title']}
- **Channel:** {spec_data['youtube_channel']}
- **Blogger:** {spec_data['blogger_url']}
- **Target Format:** {spec_data['target_format']}
- **Category:** {spec_data['category']}
- **Pricing:** {spec_data['pricing_type']}

---

## Complete Voiceover Script

> "{spec_data['voiceover_script']}"

---

## Scene-by-Scene Visual Prompts (Google Flow Engine Specs)

"""
    for sc in spec_data["scenes"]:
        md += f"""### Scene {sc['scene_number']} ({sc['timestamp']})
- **Framing:** {sc['camera_framing']}
- **Lighting:** {sc['lighting']}
- **Visual AI Prompt:** `{sc['visual_prompt']}`
- **Matching Narration:** "{sc['narration']}"

"""

    md += f"""---

## Non-Sponsorship Disclosure

{spec_data['disclaimer']}
"""
    return md


def select_daily_ides(history_data, count=3):
    covered = set(history_data.get("covered_ides", []))
    selected = []
    for ide in CURATED_IDES:
        if ide["id"] not in covered:
            selected.append(ide)
            if len(selected) == count:
                break

    # If we run out of unvisited curated IDEs, fallback to resetting or picking least recently covered
    if len(selected) < count:
        for ide in CURATED_IDES:
            if ide not in selected:
                selected.append(ide)
                if len(selected) == count:
                    break
    return selected


def main():
    date_str = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d")
    out_dir = os.path.join("content", date_str)
    os.makedirs(out_dir, exist_ok=True)

    history_file = os.path.join("content", "history.json")
    history_data = load_history(history_file)

    ides = select_daily_ides(history_data, count=3)
    print(f"Generating 3 daily content packages for date: {date_str}")

    generated_items = []

    for idx, ide in enumerate(ides, start=1):
        item_dir = os.path.join(out_dir, f"item-{idx}-{ide['id']}")
        os.makedirs(item_dir, exist_ok=True)

        amp_html = build_amp_html(ide)
        flow_spec_json = build_google_flow_spec(ide)
        flow_spec_md = build_google_flow_markdown(flow_spec_json)

        amp_path = os.path.join(item_dir, "amp_post.html")
        json_path = os.path.join(item_dir, "google_flow_spec.json")
        md_path = os.path.join(item_dir, "google_flow_spec.md")

        with open(amp_path, "w", encoding="utf-8") as f:
            f.write(amp_html)

        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(flow_spec_json, f, indent=2, ensure_ascii=False)

        with open(md_path, "w", encoding="utf-8") as f:
            f.write(flow_spec_md)

        # Record history
        if ide["id"] not in history_data["covered_ides"]:
            history_data["covered_ides"].append(ide["id"])

        item_record = {
            "id": ide["id"],
            "name": ide["name"],
            "date": date_str,
            "path": item_dir
        }
        history_data.setdefault("history", []).append(item_record)
        generated_items.append(item_record)

        print(f"  [{idx}/3] Created package for '{ide['name']}' in {item_dir}")

    save_history(history_data, history_file)
    print(f"Daily generation complete. History updated in {history_file}.")


if __name__ == "__main__":
    main()
