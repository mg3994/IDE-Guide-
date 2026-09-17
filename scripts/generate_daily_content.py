#!/usr/bin/env python3
"""
IDE Guide - Daily Content Generation Engine
Generates 3 AMP HTML blog posts (for https://ideguide.blogspot.com/)
and 3 Google Flow video generation specs (for YouTube @IDEguide) daily.
"""

import os
import sys
import json
import re
import urllib.request
import urllib.error
from datetime import datetime, timezone

MANDATORY_DISCLAIMER = (
    "Disclaimer: IDE Guide is an independent technical publication. "
    "This content is not sponsored, endorsed, or affiliated with any software vendor or editor developer mentioned above. "
    "All reviews and assessments are based strictly on objective developer evaluation."
)

CURATED_IDE_DATABASE = [
    {
        "name": "Cursor",
        "slug": "cursor",
        "category": "AI-First Code Editor",
        "description": "An AI-powered code editor built as a fork of VS Code, focusing on deep repository indexing and inline multi-file code generation.",
        "pros": ["Seamless AI code generation & edits across workspace", "Familiar VS Code extension ecosystem", "Fast multi-file context indexing"],
        "cons": ["Subscription costs for high usage AI models", "Closed-source backend AI service dependencies", "High RAM consumption with large context indexing"],
        "pricing": "Freemium ($20/month Pro tier for advanced AI credits)",
        "best_for": "Full-stack developers, AI-assisted development power users",
        "website": "https://cursor.com"
    },
    {
        "name": "Neovim",
        "slug": "neovim",
        "category": "Modal Terminal Text Editor",
        "description": "A hyperextensible Vim-based text editor built for extreme performance, modal editing efficiency, and Lua scriptability.",
        "pros": ["Blazing fast startup time and minimal resource footprint", "Unmatched keyboard-centric modal editing speed", "Rich Lua plugin ecosystem (LSP, Treesitter, Mason)"],
        "cons": ["Steep learning curve for modal navigation", "Requires extensive manual configuration", "Lacks built-in visual UI without terminal extensions"],
        "pricing": "100% Free & Open Source (Apache 2.0 / Vim License)",
        "best_for": "Terminal enthusiasts, backend engineers, systems programmers",
        "website": "https://neovim.io"
    },
    {
        "name": "Zed",
        "slug": "zed",
        "category": "High-Performance Rust-based Editor",
        "description": "A lightweight, high-performance code editor written in Rust with built-in multiplayer real-time collaboration and GPU-accelerated rendering.",
        "pros": ["Blazing fast GPU-accelerated text rendering", "Native real-time collaborative pair programming", "Low memory footprint compared to Electron editors"],
        "cons": ["Ecosystem extensions still maturing", "Fewer extensions than VS Code marketplace", "Linux/Windows support newer than macOS"],
        "pricing": "Free & Open Source (GPL/AGPL/Apache)",
        "best_for": "Performance purists, Rust developers, real-time pair programmers",
        "website": "https://zed.dev"
    },
    {
        "name": "VS Code",
        "slug": "vscode",
        "category": "Extensible General Purpose Editor",
        "description": "Microsoft's ubiquitous open-source code editor featuring a massive marketplace, rich debugging tools, and integrated terminal support.",
        "pros": ["Unrivaled extension marketplace", "Massive global developer community and ecosystem", "Great built-in Git and debug integration"],
        "cons": ["Electron resource consumption with heavy extensions", "Telemetry enabled by default in official builds", "Slower startup compared to native editors"],
        "pricing": "Free & Open Source (MIT License for core)",
        "best_for": "Web developers, beginners, multi-language software engineers",
        "website": "https://code.visualstudio.com"
    },
    {
        "name": "IntelliJ IDEA",
        "slug": "intellij-idea",
        "category": "Enterprise JVM & Polyglot IDE",
        "description": "JetBrains' flagship Integrated Development Environment engineered for Java, Kotlin, Scala, and enterprise backend engineering.",
        "pros": ["Industry leading code refactoring and static analysis", "Deep integration with enterprise build tools (Gradle, Maven)", "Out-of-the-box framework support (Spring, Quarkus)"],
        "cons": ["Heavy memory and CPU usage on large projects", "Ultimate edition requires paid commercial license", "Longer indexing time on huge codebases"],
        "pricing": "Freemium (Community Edition Free, Ultimate $169+/year)",
        "best_for": "Java/Kotlin developers, enterprise backend engineers",
        "website": "https://www.jetbrains.com/idea/"
    },
    {
        "name": "PyCharm",
        "slug": "pycharm",
        "category": "Python Dedicated IDE",
        "description": "JetBrains' dedicated Python IDE featuring intelligent code completion, automated refactorings, Django/Flask integration, and Jupyter Notebook support.",
        "pros": ["Best-in-class Python static analysis and type checking", "Built-in visual debugger and database tools", "Native support for virtual environments, Docker, and Conda"],
        "cons": ["Heavy memory footprint", "Professional features require paid plan", "Slower launch time"],
        "pricing": "Freemium (Community Edition Free, Professional $99+/year)",
        "best_for": "Python developers, data scientists, Django/Flask web developers",
        "website": "https://www.jetbrains.com/pycharm/"
    },
    {
        "name": "Sublime Text",
        "slug": "sublime-text",
        "category": "Lightweight High-Speed Editor",
        "description": "A legendary cross-platform text editor known for ultra-fast performance, multi-cursor editing, and low system resource overhead.",
        "pros": ["Instant startup and ultra-responsive editing", "Extremely low memory footprint", "Powerful multi-caret and regular expression search"],
        "cons": ["Limited out-of-the-box LSP without plugins", "Evaluation popups without paid license", "Smaller ecosystem than VS Code"],
        "pricing": "Paid ($99 perpetual evaluation license)",
        "best_for": "Developers seeking speed, fast log viewing, and lightweight editing",
        "website": "https://www.sublimetext.com"
    },
    {
        "name": "Helix",
        "slug": "helix",
        "category": "Post-Modern Modal Text Editor",
        "description": "A modal text editor written in Rust, inspired by Neovim and Kakoune with selection-first modal editing and zero-config LSP.",
        "pros": ["Zero configuration required for LSP and syntax highlighting", "Written in Rust with high speed and low memory", "Selection-first modal editing flow"],
        "cons": ["Plugin system still under development", "Non-standard modal keybindings for Vim users", "Terminal-only interface"],
        "pricing": "100% Free & Open Source (MPL 2.0)",
        "best_for": "Modal editing fans who want zero-config LSP out of the box",
        "website": "https://helix-editor.com"
    },
    {
        "name": "Lapce",
        "slug": "lapce",
        "category": "Native Lightning-Fast Code Editor",
        "description": "A fast native code editor written in Rust with GPU rendering, modal editing option, and remote development support.",
        "pros": ["Native UI performance powered by Druid and GPU", "Built-in remote development capabilities", "WASM plugin system"],
        "cons": ["Project still early stage with occasional bugs", "Smaller extension library", "Less documentation"],
        "pricing": "100% Free & Open Source (Apache 2.0)",
        "best_for": "Rust enthusiasts, early adopters looking for native open-source editors",
        "website": "https://lapce.dev"
    },
    {
        "name": "Windsurf",
        "slug": "windsurf",
        "category": "Agentic AI Code Editor",
        "description": "An AI-native editor by Codeium incorporating Cascade flow for real-time collaborative agentic code modifications.",
        "pros": ["Deep Cascade agent integration for complex multi-step refactoring", "Fast inline AI autocompletion", "Built on familiar VS Code foundation"],
        "cons": ["Proprietary AI backend", "Requires internet connection for agentic features", "Paid plan required for high model volume"],
        "pricing": "Freemium (Free tier available, Pro $15/month)",
        "best_for": "Developers wanting autonomous agentic AI pair programming",
        "website": "https://codeium.com/windsurf"
    },
    {
        "name": "Fleet",
        "slug": "fleet",
        "category": "Distributed Lightweight IDE",
        "description": "JetBrains' next-generation lightweight, polyglot editor designed for rapid startup and distributed smart architecture.",
        "pros": ["Sleek modern minimal UI", "Seamless switch between lightweight editor and full smart IDE mode", "Built-in collaborative editing"],
        "cons": ["Preview stage features", "Plugin ecosystem still growing", "Requires JetBrains account"],
        "pricing": "Freemium (Public Preview Free, Tiered Pricing Planned)",
        "best_for": "Polyglot developers wanting JetBrains intelligence in a light editor",
        "website": "https://www.jetbrains.com/fleet/"
    },
    {
        "name": "Xcode",
        "slug": "xcode",
        "category": "Apple Platform IDE",
        "description": "Apple's official integrated development suite for iOS, iPadOS, macOS, watchOS, and visionOS development.",
        "pros": ["Deep integration with Swift, SwiftUI, and Apple SDKs", "Native visual UI preview canvases and simulators", "Comprehensive profiling tools (Instruments)"],
        "cons": ["macOS platform exclusive", "Large disk storage requirements (over 10GB)", "Can be resource-intensive during indexing"],
        "pricing": "Free for macOS users (Apple Developer Program $99/year for App Store submission)",
        "best_for": "Apple platform (iOS/macOS/visionOS) developers",
        "website": "https://developer.apple.com/xcode/"
    }
]

def fetch_github_trending_ides():
    """Attempt to discover IDEs via GitHub Search API with fallback to curated list."""
    url = "https://api.github.com/search/repositories?q=topic:ide+OR+topic:code-editor&sort=stars&order=desc&per_page=15"
    req = urllib.request.Request(url, headers={"User-Agent": "IDEGuideContentBot/1.0"})
    discovered = []
    try:
        with urllib.request.urlopen(req, timeout=5) as response:
            if response.status == 200:
                data = json.loads(response.read().decode('utf-8'))
                for item in data.get("items", []):
                    name = item.get("name", "").strip()
                    desc = item.get("description") or "A modern development environment."
                    repo_url = item.get("html_url", "")
                    slug = re.sub(r'[^a-z0-9]+', '-', name.lower()).strip('-')
                    discovered.append({
                        "name": name.capitalize(),
                        "slug": slug,
                        "category": "Open Source Code Editor",
                        "description": desc,
                        "pros": ["Open source community development", "Extensible codebase", "Active GitHub repository"],
                        "cons": ["Requires setup and configuration", "Varying documentation depth", "Ecosystem dependent"],
                        "pricing": "100% Free & Open Source",
                        "best_for": "Developers interested in open source editors",
                        "website": repo_url
                    })
    except Exception:
        pass
    return discovered

def load_history(history_file="content/history.json"):
    if os.path.exists(history_file):
        try:
            with open(history_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            pass
    return {"covered_ides": [], "generation_log": []}

def save_history(history_data, history_file="content/history.json"):
    os.makedirs(os.path.dirname(history_file), exist_ok=True)
    with open(history_file, 'w', encoding='utf-8') as f:
        json.dump(history_data, f, indent=2)

def select_daily_ides(count=3, history_file="content/history.json"):
    history = load_history(history_file)
    covered_slugs = set(history.get("covered_ides", []))

    discovered = fetch_github_trending_ides()
    candidates = discovered + CURATED_IDE_DATABASE

    selected = []
    seen_in_run = set()

    for ide in candidates:
        slug = ide["slug"]
        if slug not in covered_slugs and slug not in seen_in_run:
            selected.append(ide)
            seen_in_run.add(slug)
            if len(selected) == count:
                break

    # If all candidates covered, reset history or pick candidates
    if len(selected) < count:
        for ide in CURATED_IDE_DATABASE:
            slug = ide["slug"]
            if slug not in seen_in_run:
                selected.append(ide)
                seen_in_run.add(slug)
                if len(selected) == count:
                    break

    return selected

def generate_amp_blog_html(ide, date_str):
    """Generates valid AMP HTML blog post formatted specifically for Blogger (ideguide.blogspot.com)."""
    title = f"{ide['name']} Guide (2026): Good, Bad, Pricing & Developer Review"
    canonical_url = f"https://ideguide.blogspot.com/{date_str.replace('-', '/')}/{ide['slug']}-review.html"

    pros_li = "".join([f"<li><strong>Good:</strong> {p}</li>" for p in ide['pros']])
    cons_li = "".join([f"<li><strong>Bad:</strong> {c}</li>" for c in ide['cons']])

    html = f"""<!doctype html>
<html ⚡ lang="en">
<head>
  <meta charset="utf-8">
  <title>{title}</title>
  <link rel="canonical" href="{canonical_url}">
  <meta name="viewport" content="width=device-width,minimum-scale=1,initial-scale=1">
  <script async src="https://cdn.ampproject.org/v0.js"></script>
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "BlogPosting",
    "headline": "{title}",
    "description": "{ide['description']}",
    "author": {{
      "@type": "Organization",
      "name": "IDE Guide"
    }},
    "publisher": {{
      "@type": "Organization",
      "name": "IDE Guide",
      "url": "https://ideguide.blogspot.com/"
    }},
    "mainEntityOfPage": "{canonical_url}"
  }}
  </script>
  <style amp-boilerplate>body{{-webkit-animation:-amp-start 8s steps(1,end) 0s 1 normal both;-moz-animation:-amp-start 8s steps(1,end) 0s 1 normal both;-ms-animation:-amp-start 8s steps(1,end) 0s 1 normal both;animation:-amp-start 8s steps(1,end) 0s 1 normal both}}@-webkit-keyframes -amp-start{{from{{visibility:hidden}}to{{visibility:visible}}}}@-moz-keyframes -amp-start{{from{{visibility:hidden}}to{{visibility:visible}}}}@-ms-keyframes -amp-start{{from{{visibility:hidden}}to{{visibility:visible}}}}@-o-keyframes -amp-start{{from{{visibility:hidden}}to{{visibility:visible}}}}@keyframes -amp-start{{from{{visibility:hidden}}to{{visibility:visible}}}}</style><noscript><style amp-boilerplate>body{{-webkit-animation:none;-moz-animation:none;-ms-animation:none;animation:none}}</style></noscript>
  <style amp-custom>
    body {{
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
      line-height: 1.6;
      color: #e0e6ed;
      background-color: #0d1117;
      margin: 0;
      padding: 16px;
    }}
    header {{
      background: #161b22;
      padding: 20px;
      border-radius: 8px;
      border: 1px solid #30363d;
      margin-bottom: 20px;
    }}
    h1 {{
      color: #58a6ff;
      font-size: 24px;
      margin: 0 0 10px 0;
    }}
    .badge {{
      display: inline-block;
      background: #238636;
      color: #ffffff;
      padding: 4px 8px;
      border-radius: 4px;
      font-size: 12px;
      font-weight: bold;
    }}
    .section {{
      background: #161b22;
      padding: 20px;
      border-radius: 8px;
      border: 1px solid #30363d;
      margin-bottom: 16px;
    }}
    h2 {{
      color: #79c0ff;
      border-bottom: 1px solid #30363d;
      padding-bottom: 8px;
      font-size: 18px;
    }}
    ul {{
      padding-left: 20px;
    }}
    li {{
      margin-bottom: 8px;
    }}
    .pricing-box {{
      background: #1c2128;
      border-left: 4px solid #a371f7;
      padding: 12px;
      border-radius: 4px;
    }}
    .disclaimer {{
      background: #161b22;
      border: 1px solid #d29922;
      color: #d29922;
      padding: 12px;
      border-radius: 6px;
      font-size: 12px;
      margin-top: 24px;
    }}
  </style>
</head>
<body>
  <header>
    <span class="badge">{ide['category']}</span>
    <h1>{title}</h1>
    <p>Published on {date_str} by IDE Guide</p>
  </header>

  <div class="section">
    <h2>1. Overview & Key Capabilities</h2>
    <p>{ide['description']}</p>
    <p><strong>Official Website:</strong> <a href="{ide['website']}" style="color: #58a6ff;">{ide['website']}</a></p>
  </div>

  <div class="section">
    <h2>2. The Good & The Bad (Honest Evaluation)</h2>
    <h3>Strengths (Good)</h3>
    <ul>
      {pros_li}
    </ul>
    <h3>Limitations (Bad)</h3>
    <ul>
      {cons_li}
    </ul>
  </div>

  <div class="section">
    <h2>3. Pricing & Licensing Breakdown</h2>
    <div class="pricing-box">
      <p><strong>Tier Structure:</strong> {ide['pricing']}</p>
      <p>Whether you are choosing free open-source software or commercial subscriptions, inspect your team's workflow requirements before upgrading.</p>
    </div>
  </div>

  <div class="section">
    <h2>4. Final Verdict & Who Should Use It</h2>
    <p><strong>Ideal For:</strong> {ide['best_for']}</p>
    <p>For more detailed editor breakdowns and visual tutorials, visit our YouTube channel at <a href="https://www.youtube.com/@IDEguide" style="color:#58a6ff;">@IDEguide</a>.</p>
  </div>

  <div class="disclaimer">
    {MANDATORY_DISCLAIMER}
  </div>
</body>
</html>
"""
    return html

def generate_google_flow_video_spec(ide, date_str):
    """Generates Google Flow video generation script & specification for YouTube (@IDEguide)."""
    spec = f"""# Google Flow Video Generation Spec: {ide['name']} Review

**Target Channel:** IDE Guide ([https://www.youtube.com/@IDEguide](https://www.youtube.com/@IDEguide))
**Date:** {date_str}
**IDE Target:** {ide['name']} ({ide['category']})
**Primary Aspect Ratios:** 16:9 (YouTube Video) & 9:16 (YouTube Shorts)

---

## 1. Visual Generation Parameters (Google Flow / Veo Prompts)

### Scene 1: Hook & Hero Opening (0:00 - 0:05)
* **Visual Prompt:** "Cinematic overhead shot of modern dark workstation illuminated by blue neon desk light. Close-up on sleek modern code editor {ide['name']} displaying glowing syntax highlighting on dark theme. 4k resolution, 60fps, smooth camera push-in."
* **Audio Voiceover:** "Should you upgrade your workflow to {ide['name']} in 2026? Let's inspect the good, the bad, and the pricing model."

### Scene 2: Feature Showcase & Capabilities (0:05 - 0:25)
* **Visual Prompt:** "Macro camera zoom into editor UI showcasing {ide['category']} features, smooth scrolling code editor with high contrast text, sleek glassmorphism card overlays highlighting key strengths. Ultra high definition."
* **Audio Voiceover:** "{ide['description']}"

### Scene 3: The Good vs The Bad (0:25 - 0:45)
* **Visual Prompt:** "Split visual screen graphic. Left side glowing emerald green labeled 'THE GOOD', right side glowing amber labeled 'THE BAD'. Dynamic animated motion graphics with sleek developer aesthetics."
* **Audio Voiceover:**
  * *Strengths:* "On the positive side: {', '.join(ide['pros'])}."
  * *Limitations:* "However, keep in mind: {', '.join(ide['cons'])}."

### Scene 4: Pricing Tier & Final Verdict (0:45 - 0:58)
* **Visual Prompt:** "Sleek price tag metric graphic displaying '{ide['pricing']}'. Smooth camera transition to target developer audience card labeled '{ide['best_for']}'."
* **Audio Voiceover:** "Pricing status: {ide['pricing']}. Best suited for {ide['best_for']}. Subscribe to IDE Guide for daily editor comparisons."

---

## 2. On-Screen Overlay & Non-Sponsorship Disclaimer

**Footer Overlay Graphic:**
`{MANDATORY_DISCLAIMER}`

---

## 3. Google Flow Execution Notes
* **Lighting Style:** Cool 5600K key light with deep cyan accent rim light.
* **Text Fonts:** Inter / Fira Code monospace font for UI overlays.
* **Audio FX:** Soft mechanical keyboard clicking under quiet ambient synth pad track.
"""
    return spec

def run_daily_generation(target_date=None, output_base="content"):
    if target_date is None:
        target_date = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    date_folder = os.path.join(output_base, target_date)
    os.makedirs(date_folder, exist_ok=True)

    history_path = os.path.join(output_base, "history.json")
    history = load_history(history_path)

    selected_ides = select_daily_ides(count=3, history_file=history_path)

    generated_files = []
    new_covered = list(history.get("covered_ides", []))

    for idx, ide in enumerate(selected_ides, start=1):
        slug = ide["slug"]

        # 1. Generate AMP HTML blog post
        amp_html = generate_amp_blog_html(ide, target_date)
        blog_filename = f"post_{idx}_{slug}.html"
        blog_path = os.path.join(date_folder, blog_filename)
        with open(blog_path, 'w', encoding='utf-8') as f:
            f.write(amp_html)
        generated_files.append(blog_path)

        # 2. Generate Google Flow video spec
        video_spec = generate_google_flow_video_spec(ide, target_date)
        video_filename = f"video_{idx}_{slug}.md"
        video_path = os.path.join(date_folder, video_filename)
        with open(video_path, 'w', encoding='utf-8') as f:
            f.write(video_spec)
        generated_files.append(video_path)

        if slug not in new_covered:
            new_covered.append(slug)

    history["covered_ides"] = new_covered
    history["generation_log"].append({
        "date": target_date,
        "generated_count": len(selected_ides),
        "ides": [ide["name"] for ide in selected_ides]
    })
    save_history(history, history_path)

    print(f"Daily content generation complete for {target_date}!")
    print(f"Generated {len(generated_files)} content files under {date_folder}:")
    for filepath in generated_files:
        print(f"  - {filepath}")

if __name__ == "__main__":
    run_daily_generation()
