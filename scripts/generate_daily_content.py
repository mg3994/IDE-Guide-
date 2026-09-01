#!/usr/bin/env python3
"""
Daily Content Generation Engine for IDE Guide.
Generates 3 AMP HTML blog posts (for Blogger: https://ideguide.blogspot.com/)
and 3 Google Flow Video & Shorts Specifications (for YouTube: https://www.youtube.com/@IDEguide)
per day, tracking history in content/history.json to ensure no duplicates.
"""

import os
import json
import datetime
import urllib.request
import urllib.parse
import re

HISTORY_FILE = "content/history.json"
DISCLAIMER_TEXT = (
    "Disclaimer: IDE Guide is an independent technical publication. This content is not sponsored, "
    "endorsed, or affiliated with any software vendor or editor developer mentioned above. "
    "All reviews and assessments are based strictly on objective developer evaluation."
)

CURATED_IDES = [
    {
        "name": "Visual Studio Code",
        "category": "General Code Editor",
        "pricing": "Free / Open Source (Core: Code - OSS, Distribution: Proprietary License)",
        "cost_model": "100% Free",
        "pros": [
            "Extensive extensions ecosystem",
            "Built-in Git integration and terminal",
            "Lightweight and fast startup",
            "Strong TypeScript and JavaScript support out of the box"
        ],
        "cons": [
            "Electron-based memory overhead with many extensions",
            "Requires configuration for complex C++/Java setups"
        ],
        "best_for": "Web developers, full-stack engineers, and general multi-language coding",
        "flow_scene": "Close-up of VS Code interface with sleek dark theme, sidebar activity bar glowing, showing live code completion."
    },
    {
        "name": "Cursor",
        "category": "AI-Native Code Editor",
        "pricing": "Freemium (Free tier available; Pro $20/mo, Business $40/user/mo)",
        "cost_model": "Freemium",
        "pros": [
            "Deep AI code prediction (Cursor Tab)",
            "Multi-file codebase indexing and context chat",
            "Seamless fork of VS Code with existing extension compatibility"
        ],
        "cons": [
            "Subscription cost for heavy AI usage",
            "Requires cloud connection for advanced AI features"
        ],
        "best_for": "Developers seeking maximum productivity with state-of-the-art AI assistance",
        "flow_scene": "Macro focus on Cursor AI prompt window generating full multi-file code refactors dynamically."
    },
    {
        "name": "JetBrains IntelliJ IDEA",
        "category": "Full-Featured Java/Kotlin IDE",
        "pricing": "Freemium (Community Edition: Free / Open Source; Ultimate: $169/yr - $599/yr)",
        "cost_model": "Paid / Freemium",
        "pros": [
            "Unrivaled Java, Kotlin, and JVM refactoring tools",
            "Deep static code analysis and inspection",
            "Database tool windows and framework integrations"
        ],
        "cons": [
            "Heavy RAM and CPU resource consumption",
            "Higher subscription cost for Ultimate edition"
        ],
        "best_for": "Enterprise Java/Kotlin back-end engineers and large codebase maintainers",
        "flow_scene": "Pan across IntelliJ IDEA dark UI displaying complex call hierarchy and real-time static analysis warnings."
    },
    {
        "name": "Neovim",
        "category": "Modal Terminal-based Editor",
        "pricing": "100% Free & Open Source (Apache 2.0 / Vim License)",
        "cost_model": "100% Free",
        "pros": [
            "Blazing fast performance and minimal memory footprint",
            "Hyper-customizable via Lua configuration",
            "Native LSP and Treesitter support"
        ],
        "cons": [
            "Steep learning curve for vim keybindings",
            "Requires time investment to configure from scratch"
        ],
        "best_for": "Terminal enthusiasts, Linux power users, and keyboard-driven developers",
        "flow_scene": "Rapid terminal animation of Neovim running in dark Alacritty terminal with Lua syntax highlighting."
    },
    {
        "name": "Zed",
        "category": "High-Performance Code Editor",
        "pricing": "100% Free & Open Source (GPL for editor, AGPL for server)",
        "cost_model": "100% Free",
        "pros": [
            "Written in Rust with GPU-accelerated rendering (60+ FPS)",
            "Built-in collaborative real-time editing",
            "Instant startup time and ultra-low latency"
        ],
        "cons": [
            "Ecosystem and extension registry still growing",
            "Fewer niche language plugins compared to VS Code"
        ],
        "best_for": "Performance purists, Systems/Rust/Go developers, and pair programming teams",
        "flow_scene": "Sleek dark GPU-rendered Zed buffer with instant syntax highlighting and multi-cursor typing."
    },
    {
        "name": "JetBrains PyCharm",
        "category": "Python Dedicated IDE",
        "pricing": "Freemium (Community Edition: Free; Professional: $99/yr - $249/yr)",
        "cost_model": "Paid / Freemium",
        "pros": [
            "World-class Python debugging, profiling, and Jupyter support",
            "Django, Flask, and FastAPI framework support in Pro",
            "Integrated database tools and web developer features"
        ],
        "cons": [
            "Resource hungry on smaller hardware setups",
            "Web framework features locked behind paid tier"
        ],
        "best_for": "Python developers, Data Scientists, AI/ML engineers, and Django backend devs",
        "flow_scene": "Macro shot of PyCharm scientific mode with interactive matplotlib plots and dark syntax themes."
    },
    {
        "name": "Sublime Text 4",
        "category": "Lightweight Text & Code Editor",
        "pricing": "Paid Shareware ($99 for personal license, free evaluation without hard time limit)",
        "cost_model": "Paid Shareware",
        "pros": [
            "GPU accelerated rendering for silky smooth scrolling",
            "Ultra-lightweight RAM footprint",
            "Powerful Package Control ecosystem"
        ],
        "cons": [
            "Paid license popup in evaluation mode",
            "Lacks full out-of-the-box IDE features without plugins"
        ],
        "best_for": "Developers who want an instant-opening, distraction-free fast code editor",
        "flow_scene": "Smooth vertical scroll through 10,000 lines of code in Sublime Text with GPU acceleration visual glow."
    },
    {
        "name": "Fleet by JetBrains",
        "category": "Next-Gen Polyglot Lightweight Editor",
        "pricing": "Freemium (Free preview currently; subscription pricing expected for smart mode)",
        "cost_model": "Freemium",
        "pros": [
            "Lightweight editor mode with optional IntelliJ smart engine backend",
            "Built from scratch with distributed architecture",
            "Collaborative multi-user coding built-in"
        ],
        "cons": [
            "Still evolving feature set and plugin ecosystem",
            "Requires JetBrains account integration"
        ],
        "best_for": "Polyglot developers seeking a lightweight alternative with optional JetBrains intelligence",
        "flow_scene": "Futuristic UI layout of Fleet transitioning between lightweight text mode and smart IDE mode."
    },
    {
        "name": "Xcode",
        "category": "Apple Platform IDE",
        "pricing": "100% Free (Requires macOS; $99/yr for Apple Developer Program to publish)",
        "cost_model": "Free IDE (Apple ecosystem)",
        "pros": [
            "Essential for iOS, iPadOS, macOS, watchOS, and visionOS development",
            "SwiftUI interactive live previews and simulator",
            "Integrated Instruments performance profiler"
        ],
        "cons": [
            "macOS hardware lock-in",
            "Large disk space installation requirement (30GB+)"
        ],
        "best_for": "Apple platform developers, Swift/SwiftUI mobile app creators",
        "flow_scene": "Xcode dark mode with split preview showing SwiftUI canvas live updating side-by-side with code."
    }
]

def load_history():
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {"covered_ides": [], "last_updated": None}

def save_history(history):
    os.makedirs(os.path.dirname(HISTORY_FILE), exist_ok=True)
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=2)

def sanitize_slug(name):
    return re.sub(r'[^a-z0-9]+', '-', name.lower()).strip('-')

def fetch_github_trending_editors(count=3, excluded_names=None):
    if excluded_names is None:
        excluded_names = []

    # Try fetching real popular code editors from GitHub API
    editors = []
    try:
        url = "https://api.github.com/search/repositories?q=topic:editor+topic:ide&sort=stars&order=desc&per_page=15"
        req = urllib.request.Request(url, headers={'User-Agent': 'IDE-Guide-Bot'})
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            for item in data.get('items', []):
                name = item.get('name', '')
                full_name = item.get('full_name', '')
                description = item.get('description', '') or 'A modern code editor / IDE project.'
                homepage = item.get('homepage', '') or item.get('html_url', '')

                # Filter out already covered or non-editor repositories
                if name.lower() in [e.lower() for e in excluded_names]:
                    continue

                editors.append({
                    "name": name.capitalize(),
                    "category": "Open Source Code Editor / IDE",
                    "pricing": "Free & Open Source",
                    "cost_model": "100% Free",
                    "pros": [
                        f"Open source codebase ({item.get('stargazers_count', 0)} stars on GitHub)",
                        "Community driven development and extension support",
                        "Transparent development and active issue tracker"
                    ],
                    "cons": [
                        "May require manual build or configuration",
                        "Ecosystem documentation continuously evolving"
                    ],
                    "best_for": "Open source enthusiasts and developers looking for modern custom editors",
                    "flow_scene": f"Cinematic dark workstation showcasing {name} source repository and interactive editor window.",
                    "repo_url": item.get('html_url')
                })
                if len(editors) >= count:
                    break
    except Exception as e:
        print(f"Note: GitHub API fetch skipped or rate-limited ({e}). Falling back to curated database.")

    return editors

def select_daily_ides(count=3):
    history = load_history()
    covered = set(history.get("covered_ides", []))

    selected = []
    # 1. Pick from curated list first
    for item in CURATED_IDES:
        if item["name"].lower() not in covered:
            selected.append(item)
            covered.add(item["name"].lower())
            if len(selected) >= count:
                break

    # 2. If curated list runs short, fetch from GitHub API or generate generic structured entries
    if len(selected) < count:
        needed = count - len(selected)
        github_editors = fetch_github_trending_editors(needed, list(covered))
        for g_item in github_editors:
            selected.append(g_item)
            covered.add(g_item["name"].lower())
            if len(selected) >= count:
                break

    return selected

def generate_amp_blog_post(ide_info):
    name = ide_info["name"]
    category = ide_info["category"]
    pricing = ide_info["pricing"]
    cost_model = ide_info["cost_model"]
    pros = ide_info["pros"]
    cons = ide_info["cons"]
    best_for = ide_info["best_for"]

    pros_html = "".join([f"<li><strong>{p}</strong></li>" for p in pros])
    cons_html = "".join([f"<li>{c}</li>" for c in cons])

    html_content = f"""<!doctype html>
<html amp lang="en">
<head>
  <meta charset="utf-8">
  <script async src="https://cdn.ampproject.org/v0.js"></script>
  <title>{name} Review & Evaluation - IDE Guide</title>
  <link rel="canonical" href="https://ideguide.blogspot.com/{sanitize_slug(name)}-review.html">
  <meta name="viewport" content="width=device-width,minimum-scale=1,initial-scale=1">
  <style amp-boilerplate>body{{-webkit-animation:-amp-start 8s steps(1,end) 0s 1 normal partmost;-moz-animation:-amp-start 8s steps(1,end) 0s 1 normal partmost;-ms-animation:-amp-start 8s steps(1,end) 0s 1 normal partmost;animation:-amp-start 8s steps(1,end) 0s 1 normal partmost}}@-webkit-keyframes -amp-start{{from{{visibility:hidden}}to{{visibility:visible}}}}@-moz-keyframes -amp-start{{from{{visibility:hidden}}to{{visibility:visible}}}}@-ms-keyframes -amp-start{{from{{visibility:hidden}}to{{visibility:visible}}}}@-o-keyframes -amp-start{{from{{visibility:hidden}}to{{visibility:visible}}}}@keyframes -amp-start{{from{{visibility:hidden}}to{{visibility:visible}}}}</style><noscript><style amp-boilerplate>body{{-webkit-animation:none;-moz-animation:none;-ms-animation:none;animation:none}}</style></noscript>
  <style amp-custom>
    body {{
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
      line-height: 1.6;
      color: #e0e0e0;
      background-color: #0f111a;
      margin: 0;
      padding: 16px;
    }}
    .header {{
      border-bottom: 2px solid #00f3ff;
      padding-bottom: 12px;
      margin-bottom: 20px;
    }}
    h1 {{
      color: #00f3ff;
      font-size: 1.8rem;
      margin: 0 0 8px 0;
    }}
    .badge {{
      display: inline-block;
      background-color: #7000ff;
      color: #ffffff;
      padding: 4px 8px;
      border-radius: 4px;
      font-size: 0.85rem;
      font-weight: bold;
    }}
    .badge-price {{
      background-color: #00ff88;
      color: #000000;
      margin-left: 8px;
    }}
    .section {{
      background: #1a1d2e;
      border-radius: 8px;
      padding: 16px;
      margin-bottom: 20px;
    }}
    h2 {{
      color: #00f3ff;
      font-size: 1.3rem;
      margin-top: 0;
    }}
    ul {{
      padding-left: 20px;
    }}
    li {{
      margin-bottom: 8px;
    }}
    .disclaimer {{
      background-color: #25283b;
      border-left: 4px solid #00f3ff;
      padding: 12px;
      font-size: 0.85rem;
      color: #a0a5c0;
      margin-top: 24px;
      border-radius: 0 4px 4px 0;
    }}
    .footer {{
      text-align: center;
      font-size: 0.85rem;
      color: #6c7293;
      margin-top: 30px;
    }}
  </style>
</head>
<body>
  <div class="header">
    <h1>{name} - Complete IDE Guide & Evaluation</h1>
    <span class="badge">{category}</span>
    <span class="badge badge-price">{cost_model}</span>
  </div>

  <div class="section">
    <h2>Overview & Pricing</h2>
    <p><strong>Pricing Model:</strong> {pricing}</p>
    <p><strong>Recommended For:</strong> {best_for}</p>
  </div>

  <div class="section">
    <h2>Key Advantages & Strengths (Pros)</h2>
    <ul>
      {pros_html}
    </ul>
  </div>

  <div class="section">
    <h2>Limitations & Considerations (Cons)</h2>
    <ul>
      {cons_html}
    </ul>
  </div>

  <div class="section">
    <h2>Final Verdict</h2>
    <p>Whether you should choose {name} depends on your primary development focus. It stands out in {category.lower()} workflows, offering tailored features for {best_for}.</p>
  </div>

  <div class="disclaimer">
    {DISCLAIMER_TEXT}
  </div>

  <div class="footer">
    Published by <a href="https://ideguide.blogspot.com/" style="color: #00f3ff;">IDE Guide Blog</a> | Watch on <a href="https://www.youtube.com/@IDEguide" style="color: #00f3ff;">YouTube @IDEguide</a>
  </div>
</body>
</html>"""
    return html_content

def generate_google_flow_video_spec(ide_info):
    name = ide_info["name"]
    category = ide_info["category"]
    pricing = ide_info["pricing"]
    cost_model = ide_info["cost_model"]
    pros = ide_info["pros"]
    cons = ide_info["cons"]
    best_for = ide_info["best_for"]
    flow_scene = ide_info["flow_scene"]

    pros_summary = ", ".join(pros[:2])
    cons_summary = ", ".join(cons)

    spec = f"""# Google Flow Video & Shorts Prompt Specification: {name}

## Channel Metadata
- **YouTube Channel**: https://www.youtube.com/@IDEguide
- **Target Formats**: YouTube Shorts (9:16 vertical) & YouTube Long-form (16:9 horizontal)
- **Target Audience**: Software Engineers, Developers, Computer Science Students

---

## 1. Visual Generation Prompts for Google Flow AI

### Prompt 1: Hook & Opening Scene (0:00 - 0:05)
```
[Style]: Cinematic dark mode software engineering workstation, 8K ultra-detailed.
[Subject]: Close-up shot of monitor glowing with {name} UI logo and editor dark theme.
[Lighting]: Neon cyan (#00f3ff) ambient backlighting, high contrast code syntax illumination.
[Camera]: Slow push-in shot toward editor tab showing clean code structure.
```

### Prompt 2: Core Feature Showcase (0:05 - 0:25)
```
[Style]: Dynamic tech product demonstration style, 8K, crisp UI rendering.
[Subject]: {flow_scene}
[Lighting]: Soft overhead studio key light with vibrant electric purple (#7000ff) accent backlight.
[Camera]: Horizontal pan tracking across sidebar extensions, terminal, and AI prompt overlays.
```

### Prompt 3: Verdict & Outro (0:25 - 0:40)
```
[Style]: Minimalist developer review card display, dark futuristic cyber aesthetic.
[Subject]: Text overlay showing '{name}' rating badge, '{cost_model}' tag, and IDE Guide logo.
[Lighting]: Cyber emerald (#00ff88) glow highlight around recommendation box.
[Camera]: Subtle zoom out to dark workstation setup with YouTube subscribe callout.
```

---

## 2. Audio & Voiceover Script

### Voiceover Script (Pacing: ~140 words/min)
"Looking for the best code editor for your workflow? Let's talk about {name}.

{name} is a {category} available as {pricing}.

Here's what makes it great: {pros_summary}.

However, keep in mind: {cons_summary}.

**Who is this best for?** It's ideal for {best_for}.

Check out our full breakdown on ideguide.blogspot.com and subscribe to @IDEguide for daily editor guides!"

---

## 3. Shorts & Reel Metadata
- **Title**: Is {name} Worth It? ({cost_model} Editor Guide)
- **Description**: Detailed look at {name} ({category}). Pros, cons, pricing, and recommendations.
- **Hashtags**: #{sanitize_slug(name)} #IDEGuide #Coding #Programming #SoftwareEngineering #CodeEditor

---

## 4. Non-Sponsorship Disclaimer

{DISCLAIMER_TEXT}
"""
    return spec

def main():
    date_str = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d")
    out_dir = os.path.join("content", date_str)
    os.makedirs(out_dir, exist_ok=True)

    history = load_history()
    covered = history.get("covered_ides", [])

    selected_ides = select_daily_ides(3)
    print(f"Generating content for date: {date_str}")

    generated_files = []
    for i, ide_info in enumerate(selected_ides, 1):
        slug = sanitize_slug(ide_info["name"])

        # 1. AMP Blog Post
        blog_filename = f"{i:02d}_{slug}_amp_blog.html"
        blog_path = os.path.join(out_dir, blog_filename)
        blog_content = generate_amp_blog_post(ide_info)
        with open(blog_path, "w", encoding="utf-8") as f:
            f.write(blog_content)
        generated_files.append(blog_path)

        # 2. Google Flow Video Spec
        video_filename = f"{i:02d}_{slug}_google_flow_spec.md"
        video_path = os.path.join(out_dir, video_filename)
        video_content = generate_google_flow_video_spec(ide_info)
        with open(video_path, "w", encoding="utf-8") as f:
            f.write(video_content)
        generated_files.append(video_path)

        if ide_info["name"].lower() not in [c.lower() for c in covered]:
            covered.append(ide_info["name"].lower())

    history["covered_ides"] = covered
    history["last_updated"] = date_str
    save_history(history)

    print(f"Successfully generated {len(generated_files)} files in {out_dir}:")
    for filepath in generated_files:
        print(f" - {filepath}")

if __name__ == "__main__":
    main()
