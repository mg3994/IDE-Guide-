#!/usr/bin/env python3
"""
Daily Content Generator for IDE Guide
Generates 3 AMP HTML blog posts (for Blogger) and 3 Google Flow Video Specification files (for YouTube) daily.
Output directory: content/YYYY-MM-DD/
History tracker: content/history.json
"""

import json
import os
import sys
import datetime
import urllib.request
import urllib.error

DISCLAIMER_TEXT = (
    "Disclaimer: IDE Guide is an independent technical publication. "
    "This content is not sponsored, endorsed, or affiliated with any software vendor or editor developer mentioned above. "
    "All reviews and assessments are based strictly on objective developer evaluation."
)

CURATED_IDE_DATABASE = [
    {
        "name": "Cursor",
        "tagline": "AI-first Code Editor built on VS Code fork",
        "pricing": "Freemium ($20/mo for Pro)",
        "open_source": False,
        "primary_language": "TypeScript / Multi-language",
        "good_points": [
            "Native AI agent integration with deep codebase indexing",
            "Full compatibility with VS Code extensions and settings",
            "Multi-file editing and prompt-based diff generation",
            "Instant inline autocomplete with auto-imports"
        ],
        "bad_points": [
            "Requires active internet connection for advanced AI models",
            "Free tier requests run out quickly during heavy development",
            "Higher memory overhead compared to lightweight editors like Zed"
        ],
        "best_for": "Developers seeking maximum AI assistance for rapid prototyping and large codebases",
        "verdict": "Best AI-powered code editor for VS Code users looking for seamless AI completion.",
        "repo": "getcursor/cursor"
    },
    {
        "name": "Zed Editor",
        "tagline": "High-performance multi-player code editor written in Rust",
        "pricing": "Free & Open Source",
        "open_source": True,
        "primary_language": "Rust / C++ / Multi-language",
        "good_points": [
            "Blazing fast startup times and sub-millisecond input response",
            "GPU-accelerated rendering using Metal / Vulkan",
            "Built-in collaborative pair programming (multi-player)",
            "Integrated LLM assistance with custom key bindings"
        ],
        "bad_points": [
            "Smaller extension ecosystem compared to VS Code",
            "Windows support is still maturing compared to macOS / Linux",
            "Fewer graphical GUI configuration options"
        ],
        "best_for": "Rust, C++, and Web developers prioritizing ultra-low latency and minimalist editing",
        "verdict": "Best open-source ultra-fast lightweight code editor in 2025.",
        "repo": "zed-industries/zed"
    },
    {
        "name": "VS Code (Visual Studio Code)",
        "tagline": "The world's most popular extensible source code editor",
        "pricing": "Free (Open Source Core - Code-OSS)",
        "open_source": True,
        "primary_language": "TypeScript / Python / Polyglot",
        "good_points": [
            "Unrivaled ecosystem with over 50,000 extensions",
            "Rich built-in debugging, Git integration, and remote SSH / containers",
            "Supported by massive global community and enterprise tooling",
            "Robust multi-language IntelliSense and language servers (LSP)"
        ],
        "bad_points": [
            "Electron base can consume significant RAM with many extensions",
            "Telemetry enabled by default in official Microsoft binary",
            "Can feel heavy on low-spec hardware"
        ],
        "best_for": "Full-stack developers, team collaboration, and general multi-language software engineering",
        "verdict": "The undisputed best all-rounder editor for general software development.",
        "repo": "microsoft/vscode"
    },
    {
        "name": "JetBrains IntelliJ IDEA",
        "tagline": "The premier IDE for Java, Kotlin, and enterprise software engineering",
        "pricing": "Paid ($169/yr) / Community edition free",
        "open_source": False,
        "primary_language": "Java / Kotlin / Scala",
        "good_points": [
            "Deepest semantic code understanding and automated refactoring",
            "Comprehensive enterprise framework support (Spring, Jakarta EE, Quarkus)",
            "Incredible database tooling and profilers built-in",
            "Robust static analysis catching complex bugs before compile time"
        ],
        "bad_points": [
            "Heavy RAM consumption (requires 16GB+ RAM recommended)",
            "Slower indexing process on massive monolithic repositories",
            "Ultimate edition is commercial with annual licensing"
        ],
        "best_for": "Java, Kotlin, and enterprise backend engineers working on complex systems",
        "verdict": "The best enterprise Java & Kotlin IDE available.",
        "repo": "JetBrains/intellij-community"
    },
    {
        "name": "Neovim",
        "tagline": "Hyperextensible Vim-based text editor built for power users",
        "pricing": "Free & Open Source",
        "open_source": True,
        "primary_language": "Lua / Vimscript",
        "good_points": [
            "Near-zero memory footprint and instantaneous startup",
            "Complete keyboard navigation without touch of mouse",
            "Highly customizable via Lua ecosystem (Treesitter, Telescope, LSP)",
            "Runs seamlessly in any terminal environment or SSH connection"
        ],
        "bad_points": [
            "Steep learning curve for modal editing and Lua configuration",
            "Requires time investment to configure custom IDE features",
            "No native visual GUI out-of-the-box"
        ],
        "best_for": "Terminal power users, DevOps engineers, and developers who love modal keybindings",
        "verdict": "Best terminal-based modal code editor for ultimate speed and customizability.",
        "repo": "neovim/neovim"
    },
    {
        "name": "Windsurf Editor",
        "tagline": "AI flow editor with deep agentic cascade contextual awareness",
        "pricing": "Freemium ($15/mo for Pro)",
        "open_source": False,
        "primary_language": "Polyglot / Web / Python",
        "good_points": [
            "Cascade AI flow that keeps context across terminal and editor",
            "Seamless VS Code extension compatibility",
            "Smart automated command execution in terminal with safety checks",
            "Fluid agentic workspace navigation"
        ],
        "bad_points": [
            "Proprietary AI features require paid subscription",
            "Dependency on remote AI servers for indexing",
            "Relatively newer product with evolving ecosystem"
        ],
        "best_for": "Developers wanting autonomous agentic AI flows embedded directly into their IDE",
        "verdict": "Best editor for agentic context-aware AI workflows.",
        "repo": "codeium/windsurf"
    },
    {
        "name": "Helix Editor",
        "tagline": "Post-modern modal text editor built in Rust with built-in LSP",
        "pricing": "Free & Open Source",
        "open_source": True,
        "primary_language": "Rust / Tree-sitter",
        "good_points": [
            "Zero configuration required for LSP, Tree-sitter syntax highlighting, and auto-pairs",
            "Selection-first (selection -> action) modal editing philosophy",
            "Blazing speed written entirely in Rust with minimal dependencies",
            "Built-in theme switcher and fuzzy finder out of the box"
        ],
        "bad_points": [
            "No plugin plugin architecture yet (currently in design phase)",
            "Modal commands differ from traditional Vim keybindings",
            "Strictly terminal UI (TUI)"
        ],
        "best_for": "Developers who want Neovim-like terminal modal editing without spending hours configuring plugins",
        "verdict": "Best out-of-the-box modal terminal editor.",
        "repo": "helix-editor/helix"
    },
    {
        "name": "JetBrains Fleet",
        "tagline": "Next-generation lightweight distributed polyglot IDE",
        "pricing": "Freemium / Commercial subscription",
        "open_source": False,
        "primary_language": "Kotlin / Polyglot",
        "good_points": [
            "Lightweight smart editor with optional full JetBrains IntelliJ backend engine",
            "Built from scratch for remote and collaborative development",
            "Sleek modern UI with minimal distraction",
            "Multi-language support in a single unified editor window"
        ],
        "bad_points": [
            "Still in preview/maturation stage with evolving feature set",
            "Requires JetBrains account and licensing model integration",
            "Ecosystem of plugins is smaller than VS Code or IntelliJ"
        ],
        "best_for": "Developers working in remote environments wanting lightweight startup with heavy JetBrains power on demand",
        "verdict": "Best modern hybrid lightweight/heavyweight IDE.",
        "repo": "JetBrains/fleet"
    },
    {
        "name": "Lapce",
        "tagline": "Lightning-fast open-source GUI code editor written in Rust",
        "pricing": "Free & Open Source",
        "open_source": True,
        "primary_language": "Rust / WASI",
        "good_points": [
            "Native GUI rendered with GPU acceleration (Druid / Floem)",
            "Built-in remote development support similar to VS Code Remote",
            "WASI-based plugin system allowing plugins in any compiled language",
            "Incredibly low CPU and RAM footprint"
        ],
        "bad_points": [
            "Fewer mature extensions available compared to VS Code",
            "Occasional visual glitches in pre-release builds",
            "Community ecosystem still growing"
        ],
        "best_for": "Developers looking for a fast, native Rust GUI editor with remote editing capabilities",
        "verdict": "Most promising open-source Rust GUI editor.",
        "repo": "lapce/lapce"
    }
]

def load_history(history_path):
    if os.path.exists(history_path):
        try:
            with open(history_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Warning: Failed to read history file: {e}")
            return {"covered_ides": [], "daily_logs": []}
    return {"covered_ides": [], "daily_logs": []}

def save_history(history_path, history_data):
    os.makedirs(os.path.dirname(history_path), exist_ok=True)
    with open(history_path, 'w', encoding='utf-8') as f:
        json.dump(history_data, f, indent=2)

def fetch_github_trending_ides():
    """Dynamically discover trending IDE repositories from GitHub Search API as optional dynamic data."""
    url = "https://api.github.com/search/repositories?q=ide+OR+code-editor+in:name,description&sort=stars&order=desc&per_page=10"
    req = urllib.request.Request(url, headers={"User-Agent": "IDEGuide-Generator/1.0"})
    discovered = []
    try:
        with urllib.request.urlopen(req, timeout=5) as response:
            if response.status == 200:
                data = json.loads(response.read().decode('utf-8'))
                for item in data.get('items', []):
                    discovered.append({
                        "name": item.get('name', 'Developer Tool'),
                        "tagline": item.get('description', 'Modern developer editor'),
                        "pricing": "Free & Open Source" if not item.get('private') else "Proprietary",
                        "open_source": not item.get('private'),
                        "primary_language": item.get('language') or "Multi-language",
                        "good_points": [
                            f"Active open-source community with {item.get('stargazers_count', 0)} GitHub stars",
                            f"Primary language written in {item.get('language') or 'polyglot'}",
                            "Modern modular architecture and active releases"
                        ],
                        "bad_points": [
                            "Ecosystem requires community extension development",
                            "Evolving documentation and workflow patterns"
                        ],
                        "best_for": "Early adopters and open-source enthusiasts seeking modern code editing tools",
                        "verdict": f"Top trending developer tool with {item.get('stargazers_count', 0)} stars.",
                        "repo": item.get('full_name', '')
                    })
    except Exception as e:
        print(f"Notice: GitHub API fetch skipped ({e}). Falling back to curated database.")
    return discovered

def select_daily_ides(history_data, count=3):
    covered_names = set(history_data.get("covered_ides", []))
    available = [ide for ide in CURATED_IDE_DATABASE if ide["name"] not in covered_names]

    if len(available) < count:
        # Try dynamic lookup
        dynamic = fetch_github_trending_ides()
        for d in dynamic:
            if d["name"] not in covered_names and d["name"] not in [a["name"] for a in available]:
                available.append(d)

    if len(available) < count:
        # Reset history pool if exhausted
        available = CURATED_IDE_DATABASE.copy()
        history_data["covered_ides"] = []

    selected = available[:count]
    return selected

def generate_amp_html(ide_data, date_str, post_index):
    """Generates 100% valid AMP HTML blog post for Blogger."""
    name = ide_data["name"]
    tagline = ide_data["tagline"]
    pricing = ide_data["pricing"]
    good_points = ide_data["good_points"]
    bad_points = ide_data["bad_points"]
    best_for = ide_data["best_for"]
    verdict = ide_data["verdict"]

    good_items_html = "".join([f"<li>✅ <strong>{item}</strong></li>" for item in good_points])
    bad_items_html = "".join([f"<li>❌ <strong>{item}</strong></li>" for item in bad_points])

    amp_html = f"""<!doctype html>
<html ⚡ lang="en">
<head>
  <meta charset="utf-8">
  <title>{name} Review: Features, Pros & Cons, Pricing | IDE Guide</title>
  <link rel="canonical" href="https://ideguide.blogspot.com/{date_str.replace('-','/')}/{name.lower().replace(' ', '-')}-review.html">
  <meta name="viewport" content="width=device-width,minimum-scale=1,initial-scale=1">
  <script async src="https://cdn.ampproject.org/v0.js"></script>
  <style amp-boilerplate>body{{-webkit-animation:-amp-start 8s steps(1,end) 0s 1 normal both;-moz-animation:-amp-start 8s steps(1,end) 0s 1 normal both;-ms-animation:-amp-start 8s steps(1,end) 0s 1 normal both;animation:-amp-start 8s steps(1,end) 0s 1 normal both}}@-webkit-keyframes -amp-start{{from{{visibility:hidden}}to{{visibility:visible}}}}@-moz-keyframes -amp-start{{from{{visibility:hidden}}to{{visibility:visible}}}}@-ms-keyframes -amp-start{{from{{visibility:hidden}}to{{visibility:visible}}}}@-o-keyframes -amp-start{{from{{visibility:hidden}}to{{visibility:visible}}}}@keyframes -amp-start{{from{{visibility:hidden}}to{{visibility:visible}}}}</style><noscript><style amp-boilerplate>body{{-webkit-animation:none;-moz-animation:none;-ms-animation:none;animation:none}}</style></noscript>
  <style amp-custom>
    body {{
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
      line-height: 1.6;
      color: #1a1a1a;
      background-color: #f8f9fa;
      margin: 0;
      padding: 16px;
    }}
    .container {{
      max-width: 800px;
      margin: 0 auto;
      background: #ffffff;
      padding: 24px;
      border-radius: 12px;
      box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    }}
    .badge {{
      display: inline-block;
      padding: 4px 12px;
      border-radius: 20px;
      font-size: 0.85rem;
      font-weight: 600;
      background-color: #e3f2fd;
      color: #0d47a1;
      margin-bottom: 12px;
    }}
    h1 {{
      font-size: 1.8rem;
      color: #0d1117;
      margin-top: 0;
      margin-bottom: 8px;
    }}
    .tagline {{
      font-size: 1.1rem;
      color: #57606a;
      font-style: italic;
      margin-bottom: 20px;
    }}
    .pricing-card {{
      background: #f1f8e9;
      border-left: 4px solid #558b2f;
      padding: 12px 16px;
      margin: 20px 0;
      border-radius: 4px;
    }}
    .section-title {{
      font-size: 1.3rem;
      margin-top: 24px;
      margin-bottom: 12px;
      color: #1f2328;
      border-bottom: 2px solid #eaeef2;
      padding-bottom: 6px;
    }}
    ul {{
      padding-left: 20px;
    }}
    li {{
      margin-bottom: 8px;
    }}
    .recommendation {{
      background: #fff8e1;
      border-left: 4px solid #ff8f00;
      padding: 16px;
      border-radius: 4px;
      margin-top: 24px;
    }}
    .disclaimer {{
      margin-top: 32px;
      padding: 14px;
      background: #f6f8fa;
      border: 1px solid #d0d7de;
      border-radius: 6px;
      font-size: 0.85rem;
      color: #57606a;
    }}
  </style>
</head>
<body>
  <div class="container">
    <span class="badge">IDE Guide #{post_index} • Daily Review</span>
    <h1>{name} - Complete Developer Review & Comparison</h1>
    <p class="tagline">{tagline}</p>

    <div class="pricing-card">
      <strong>Pricing & License:</strong> {pricing}
    </div>

    <h2 class="section-title">The Good (Key Advantages)</h2>
    <ul>
      {good_items_html}
    </ul>

    <h2 class="section-title">The Bad (Drawbacks & Limitations)</h2>
    <ul>
      {bad_items_html}
    </ul>

    <h2 class="section-title">Who is {name} Best For?</h2>
    <p>{best_for}</p>

    <div class="recommendation">
      <strong>Final Verdict:</strong> {verdict}
    </div>

    <div class="disclaimer">
      <strong>Notice:</strong> {DISCLAIMER_TEXT}
    </div>
  </div>
</body>
</html>
"""
    return amp_html

def generate_google_flow_spec(ide_data, date_str, video_index):
    """Generates Google Flow Video Spec in both JSON and Markdown formats."""
    name = ide_data["name"]
    tagline = ide_data["tagline"]
    pricing = ide_data["pricing"]
    good_points = ide_data["good_points"]
    bad_points = ide_data["bad_points"]
    best_for = ide_data["best_for"]

    spec_dict = {
        "channel": "@IDEguide",
        "video_index": video_index,
        "date": date_str,
        "ide_name": name,
        "title": f"Should You Use {name} in 2025? (Pros, Cons & Pricing Explained)",
        "target_formats": [
            {"aspect_ratio": "16:9", "resolution": "1920x1080", "platform": "YouTube Main Video"},
            {"aspect_ratio": "9:16", "resolution": "1080x1920", "platform": "YouTube Shorts / TikTok"}
        ],
        "visual_style_prompt": (
            f"Cinematic tech studio lighting, dark modern developer workspace with aesthetic RGB backlight "
            f"(cyan and purple), macro closeups of code typing on dark IDE interface '{name}', "
            f"crystal clear UI overlays, photorealistic 8K render, smooth 60fps movement."
        ),
        "scenes": [
            {
                "scene_id": 1,
                "time_start": "00:00",
                "time_end": "00:06",
                "camera_motion": "Fast push-in zoom into pulsing neon logo of " + name,
                "visual_description": f"Glowing logo of {name} centered on dark carbon fiber texture with floating code particles.",
                "voiceover": f"Is {name} actually worth switching to? Here is everything developers need to know in 60 seconds!"
            },
            {
                "scene_id": 2,
                "time_start": "00:06",
                "time_end": "00:25",
                "camera_motion": "Smooth right-to-left pan over editor interface",
                "visual_description": f"Macro visual of editor UI highlighting features: {good_points[0]} and {good_points[1] if len(good_points)>1 else 'fast workflow'}.",
                "voiceover": f"{name} promises {tagline.lower()}. The standout feature is {good_points[0]}."
            },
            {
                "scene_id": 3,
                "time_start": "00:25",
                "time_end": "00:45",
                "camera_motion": "Split screen transition comparing Pros (Green) vs Cons (Red)",
                "visual_description": "Left panel shows checkmarks for speed and extensions; right panel highlights memory or setup limitations.",
                "voiceover": f"On the good side: {good_points[0]}. On the downside: {bad_points[0]}."
            },
            {
                "scene_id": 4,
                "time_start": "00:45",
                "time_end": "00:55",
                "camera_motion": "Static wide overlay card with pricing tag animation",
                "visual_description": f"Pricing card popping up: '{pricing}' with breakdown graphics.",
                "voiceover": f"Pricing update: {name} is {pricing}."
            },
            {
                "scene_id": 5,
                "time_start": "00:55",
                "time_end": "01:05",
                "camera_motion": "Slow pull-back zoom showing sleek dual-monitor setup",
                "visual_description": "Final recommendation card overlaying sleek developer desk.",
                "voiceover": f"Final verdict: Ideal for {best_for}. {DISCLAIMER_TEXT}"
            }
        ],
        "disclaimer": DISCLAIMER_TEXT
    }

    # Markdown format
    md_content = f"""# Google Flow Video Specification - {name}

**Channel:** @IDEguide
**Date:** {date_str}
**Video Slot:** #{video_index}
**Topic:** {name} - Honest Review & Comparison

---

## 1. Video Prompts & Technical Rules

- **Prompt Target:** Google Flow / Sora / Runway Gen-3
- **Aspect Ratios:** `16:9` (Main Video) and `9:16` (YouTube Shorts)
- **Visual Style Prompt:**
  > `{spec_dict["visual_style_prompt"]}`

---

## 2. Scene Breakdown & Audio Script

### Scene 1 (00:00 - 00:06) - The Hook
- **Visual:** {spec_dict["scenes"][0]["visual_description"]}
- **Camera:** {spec_dict["scenes"][0]["camera_motion"]}
- **Voiceover Script:** "{spec_dict["scenes"][0]["voiceover"]}"

### Scene 2 (00:06 - 00:25) - Core Showcase
- **Visual:** {spec_dict["scenes"][1]["visual_description"]}
- **Camera:** {spec_dict["scenes"][1]["camera_motion"]}
- **Voiceover Script:** "{spec_dict["scenes"][1]["voiceover"]}"

### Scene 3 (00:25 - 00:45) - The Good & The Bad
- **Visual:** {spec_dict["scenes"][2]["visual_description"]}
- **Camera:** {spec_dict["scenes"][2]["camera_motion"]}
- **Voiceover Script:** "{spec_dict["scenes"][2]["voiceover"]}"

### Scene 4 (00:45 - 00:55) - Pricing Breakdown
- **Visual:** {spec_dict["scenes"][3]["visual_description"]}
- **Camera:** {spec_dict["scenes"][3]["camera_motion"]}
- **Voiceover Script:** "{spec_dict["scenes"][3]["voiceover"]}"

### Scene 5 (00:55 - 01:05) - Final Recommendation & Disclaimer
- **Visual:** {spec_dict["scenes"][4]["visual_description"]}
- **Camera:** {spec_dict["scenes"][4]["camera_motion"]}
- **Voiceover Script:** "{spec_dict["scenes"][4]["voiceover"]}"

---

## 3. Mandatory Non-Sponsorship Disclaimer
> *{DISCLAIMER_TEXT}*
"""

    return spec_dict, md_content

def run_daily_generation(target_date=None, output_base_dir="content", history_file="content/history.json"):
    if target_date is None:
        target_date = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d")

    history = load_history(history_file)
    selected_ides = select_daily_ides(history, count=3)

    day_dir = os.path.join(output_base_dir, target_date)
    os.makedirs(day_dir, exist_ok=True)

    generated_summary = []

    for idx, ide in enumerate(selected_ides, start=1):
        slug = ide["name"].lower().replace(' ', '-').replace('(', '').replace(')', '')

        # 1. AMP HTML Blog post
        amp_content = generate_amp_html(ide, target_date, idx)
        amp_filename = f"post_{idx}_{slug}_amp.html"
        amp_path = os.path.join(day_dir, amp_filename)
        with open(amp_path, 'w', encoding='utf-8') as f:
            f.write(amp_content)

        # 2. Google Flow Video specs
        flow_json, flow_md = generate_google_flow_spec(ide, target_date, idx)
        json_filename = f"video_{idx}_{slug}_flow.json"
        md_filename = f"video_{idx}_{slug}_flow.md"

        json_path = os.path.join(day_dir, json_filename)
        md_path = os.path.join(day_dir, md_filename)

        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(flow_json, f, indent=2)

        with open(md_path, 'w', encoding='utf-8') as f:
            f.write(flow_md)

        generated_summary.append({
            "index": idx,
            "ide": ide["name"],
            "amp_html": amp_path,
            "flow_json": json_path,
            "flow_md": md_path
        })

        if ide["name"] not in history.get("covered_ides", []):
            history.setdefault("covered_ides", []).append(ide["name"])

    history.setdefault("daily_logs", []).append({
        "date": target_date,
        "count": len(selected_ides),
        "ides": [ide["name"] for ide in selected_ides]
    })

    save_history(history_file, history)

    print(f"✅ Daily content generation complete for {target_date}!")
    print(f"📁 Directory: {day_dir}")
    for item in generated_summary:
        print(f"  #{item['index']} {item['ide']}:")
        print(f"    - AMP HTML: {item['amp_html']}")
        print(f"    - Google Flow JSON: {item['flow_json']}")
        print(f"    - Google Flow MD: {item['flow_md']}")

    return generated_summary

if __name__ == "__main__":
    run_daily_generation()
