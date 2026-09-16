#!/usr/bin/env python3
"""
Daily Content Generator for IDE Guide (YouTube: @IDEguide | Blogger: ideguide.blogspot.com)

Generates 3 AMP-compliant blog posts and 3 Google Flow video generation specifications/scripts per day.
Tracks historical output in `content/history.json` to ensure coverage across various IDEs without repetition.
"""

import json
import os
import sys
import datetime
import urllib.request
import urllib.error

BLOGGER_URL = "https://ideguide.blogspot.com/"
YOUTUBE_URL = "https://www.youtube.com/@IDEguide"
DISCLAIMER_TEXT = (
    "Disclaimer: IDE Guide is an independent technical publication. "
    "This content is not sponsored, endorsed, or affiliated with any software vendor "
    "or editor developer mentioned above. All reviews and assessments are based strictly "
    "on objective developer evaluation."
)

DEFAULT_IDE_CATALOG = [
    {
        "name": "Cursor",
        "slug": "cursor",
        "category": "AI-Native Code Editor",
        "pricing": "Freemium ($20/mo Pro)",
        "developer": "Anysphere",
        "summary": "Fork of VS Code built from the ground up for deep AI integration, featuring multi-file edit suggestions, Claude 3.5 Sonnet / GPT-4o integration, and custom repository indexing.",
        "pros": [
            "Seamless multi-file edits and auto-completions",
            "Native codebase indexing and context-aware chat",
            "Full compatibility with VS Code extensions and settings",
            "Privacy mode to keep codebase off AI training sets"
        ],
        "cons": [
            "Requires paid subscription for heavy API usage",
            "Closed-source proprietary extensions layer",
            "Can consume high system memory during indexing"
        ],
        "best_for": "Full-stack and AI-first software engineers seeking maximum auto-completion speed.",
        "verdict": "Best AI-native IDE in 2026 for developers looking to boost output with intelligent multi-file context.",
        "icon_url": "https://images.unsplash.com/photo-1555066931-4365d14bab8c?w=600&auto=format&fit=crop"
    },
    {
        "name": "Visual Studio Code",
        "slug": "vscode",
        "category": "General Purpose Code Editor",
        "pricing": "Free & Open Source (MIT Core)",
        "developer": "Microsoft",
        "summary": "The world's most popular lightweight code editor with an unmatched ecosystem of extensions, GitHub Copilot integration, and remote development capabilities.",
        "pros": [
            "Massive extension marketplace with thousands of plugins",
            "Extremely active open-source community",
            "Top-tier remote development (SSH, Containers, WSL)",
            "Completely free without core limitations"
        ],
        "cons": [
            "Electron-based memory footprint can grow with many extensions",
            "AI features require separate plugin installations",
            "Default build includes telemetry (VSCodium avoids this)"
        ],
        "best_for": "All software developers, from beginners to enterprise engineers across any programming language.",
        "verdict": "The undisputed king of versatility and community support in code editing.",
        "icon_url": "https://images.unsplash.com/photo-1542831371-29b0f74f9713?w=600&auto=format&fit=crop"
    },
    {
        "name": "JetBrains IntelliJ IDEA",
        "slug": "intellij-idea",
        "category": "Full-Featured Java & Kotlin IDE",
        "pricing": "Freemium (Community Free / Ultimate $169+/yr)",
        "developer": "JetBrains",
        "summary": "The gold standard IDE for Java, Kotlin, and JVM ecosystem development, offering unmatched code analysis, refactoring tools, and deep framework support.",
        "pros": [
            "Unrivaled automated refactoring and static code analysis",
            "Built-in database, framework, and Spring tools (Ultimate)",
            "Extremely robust debugging and profiling suite",
            "Native Kotlin language support"
        ],
        "cons": [
            "Heavy resource consumption (RAM and CPU intensive)",
            "Slower startup time compared to lightweight editors",
            "Ultimate tier required for advanced web and database tools"
        ],
        "best_for": "Enterprise Java/Kotlin developers, backend engineers, and large codebase maintainers.",
        "verdict": "The definitive powerhouse for JVM engineering, worth every penny for enterprise teams.",
        "icon_url": "https://images.unsplash.com/photo-1517694712202-14dd9538aa97?w=600&auto=format&fit=crop"
    },
    {
        "name": "Neovim",
        "slug": "neovim",
        "category": "Modal Terminal Text Editor",
        "pricing": "100% Free & Open Source (Apache 2.0)",
        "developer": "Community Driven",
        "summary": "Hyperextensible Vim-based text editor built for extreme speed, keyboard-driven navigation, Lua plugin ecosystem, and embedded LSP support.",
        "pros": [
            "Blazing fast performance and near-zero memory footprint",
            "Unlimited customizability via Lua and modern plugin managers",
            "Pure keyboard efficiency without mouse reliance",
            "Native Language Server Protocol (LSP) and Treesitter support"
        ],
        "cons": [
            "Steep learning curve for Vim keybindings",
            "Requires time and effort to configure a full IDE workflow",
            "Lacks built-in visual UI buttons out of the box"
        ],
        "best_for": "Terminal power users, DevOps engineers, and developers who value lightning-fast modal editing.",
        "verdict": "The ultimate keyboard-driven editor for developers willing to master modal keybindings.",
        "icon_url": "https://images.unsplash.com/photo-1629654297299-c8506221ca97?w=600&auto=format&fit=crop"
    },
    {
        "name": "Zed",
        "slug": "zed",
        "category": "High-Performance Rust Code Editor",
        "pricing": "Free & Open Source (GPL / AGPL)",
        "developer": "Zed Industries",
        "summary": "A high-performance, multiplayer code editor written in Rust by the creators of Atom and Tree-sitter, utilizing GPU acceleration for instant rendering.",
        "pros": [
            "Sub-millisecond startup times and GPU-accelerated rendering",
            "Built-in real-time collaborative editing (multiplayer code)",
            "Integrated AI chat and inline code transformation",
            "Ultra-clean minimalist interface"
        ],
        "cons": [
            "Ecosystem and plugin marketplace still maturing",
            "Limited platform support (macOS primary, Linux in beta, Windows developing)",
            "Fewer extensions compared to VS Code"
        ],
        "best_for": "Developers seeking absolute speed, instant startup, and real-time pair programming.",
        "verdict": "The fastest code editor available today, redefining speed expectations for modern editors.",
        "icon_url": "https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?w=600&auto=format&fit=crop"
    },
    {
        "name": "Windsurf",
        "slug": "windsurf",
        "category": "AI Flow State Editor",
        "pricing": "Freemium ($15/mo Pro)",
        "developer": "Codeium",
        "summary": "An innovative AI-first editor powered by Codeium's Cascade engine, blending collaborative AI agents with developer flow state for seamless code generation.",
        "pros": [
            "Cascade AI flows seamlessly between agentic actions and chat",
            "Fast, highly accurate code completions",
            "Deep awareness of terminal and git commands",
            "Aggressive pricing compared to competitors"
        ],
        "cons": [
            "Relatively new entrant with evolving features",
            "Dependent on cloud AI connection for core agent capabilities"
        ],
        "best_for": "Engineers looking for autonomous AI coding agents integrated into a VS Code-compatible editor.",
        "verdict": "A revolutionary contender in the AI editor space, setting new standards for agentic assistance.",
        "icon_url": "https://images.unsplash.com/photo-1504639725590-34d0984388bd?w=600&auto=format&fit=crop"
    },
    {
        "name": "PyCharm",
        "slug": "pycharm",
        "category": "Dedicated Python IDE",
        "pricing": "Freemium (Community Free / Professional $99+/yr)",
        "developer": "JetBrains",
        "summary": "The premier IDE engineered specifically for Python development, Web frameworks (Django/Flask), Data Science, and scientific computing.",
        "pros": [
            "Deep intelligent Python code completion and type checking",
            "Built-in Jupyter notebook and Scientific interactive view",
            "Native Django, Flask, and FastAPI web development support",
            "Advanced database management integrated out of the box"
        ],
        "cons": [
            "Community edition lacks web framework and database tools",
            "Can be resource heavy on smaller hardware",
            "Overkill for simple script editing"
        ],
        "best_for": "Python developers, Data Scientists, and Django/Flask web backend engineers.",
        "verdict": "The indispensable tool for serious Python engineers and data science teams.",
        "icon_url": "https://images.unsplash.com/photo-1526379879527-8559ecfcaec0?w=600&auto=format&fit=crop"
    },
    {
        "name": "Xcode",
        "slug": "xcode",
        "category": "Apple Platform Native IDE",
        "pricing": "100% Free (Requires Apple Developer account for App Store distribution)",
        "developer": "Apple",
        "summary": "Apple's official integrated development environment for crafting iOS, iPadOS, macOS, watchOS, and visionOS applications using Swift and SwiftUI.",
        "pros": [
            "Essential for native Apple app development and App Store publishing",
            "SwiftUI live preview and visual design tools",
            "Comprehensive Apple simulator and Instruments performance profiler",
            "Predictive code completion with Apple ML"
        ],
        "cons": [
            "Exclusive to macOS hardware",
            "Large download size (15GB+)",
            "Can suffer from slow build times on complex projects"
        ],
        "best_for": "iOS, macOS, and visionOS native developers.",
        "verdict": "The required, feature-packed IDE for building software across Apple's device ecosystem.",
        "icon_url": "https://images.unsplash.com/photo-1607799279861-4dd421887fb3?w=600&auto=format&fit=crop"
    },
    {
        "name": "Android Studio",
        "slug": "android-studio",
        "category": "Android Native Development IDE",
        "pricing": "100% Free (Apache 2.0)",
        "developer": "Google / JetBrains",
        "summary": "Google's official IDE for Android app creation, built on JetBrains IntelliJ IDEA platform and featuring Gemini AI assistant integration.",
        "pros": [
            "Official tools for Android SDK, Jetpack Compose, and NDK",
            "Real-time visual layout editor and UI emulator",
            "Gemini AI integration for code generation and debugging",
            "Built-in APK analyzer and performance profilers"
        ],
        "cons": [
            "High RAM and CPU requirements during compilation and emulation",
            "Complex Gradle build setup"
        ],
        "best_for": "Android app developers building native Kotlin/Java applications.",
        "verdict": "The single standard for official Android application engineering.",
        "icon_url": "https://images.unsplash.com/photo-1607252650355-f7fd0460ccdb?w=600&auto=format&fit=crop"
    }
]

def fetch_trending_github_ides():
    """Optionally discover emerging open-source IDEs via GitHub API."""
    url = "https://api.github.com/search/repositories?q=topic:ide+topic:editor&sort=stars&order=desc&per_page=5"
    req = urllib.request.Request(url, headers={"User-Agent": "IDEGuide-Generator/1.0"})
    discovered = []
    try:
        with urllib.request.urlopen(req, timeout=5) as response:
            data = json.loads(response.read().decode('utf-8'))
            for item in data.get('items', []):
                name = item.get('name', '').capitalize()
                discovered.append({
                    "name": f"{name} (GitHub)",
                    "slug": item.get('name', '').lower(),
                    "category": "Open-Source Code Editor",
                    "pricing": "100% Free & Open Source",
                    "developer": item.get('owner', {}).get('login', 'Community'),
                    "summary": item.get('description', 'An open-source code editor project on GitHub.'),
                    "pros": ["Open-source transparency", f"Active community with {item.get('stargazers_count', 0)} stars", "Customizable and moddable"],
                    "cons": ["Ecosystem may be early stage", "Fewer official extensions"],
                    "best_for": "Open-source enthusiasts and early adopters.",
                    "verdict": "A promising open-source editor worth keeping on your radar.",
                    "icon_url": "https://images.unsplash.com/photo-1618401471353-b98afee0b2eb?w=600&auto=format&fit=crop"
                })
    except Exception as e:
        # Fallback silently if offline or rate limited
        pass
    return discovered


def generate_amp_html_post(ide_info, post_num):
    """Generate Blogger-compatible AMP HTML post."""
    name = ide_info["name"]
    category = ide_info["category"]
    pricing = ide_info["pricing"]
    developer = ide_info["developer"]
    summary = ide_info["summary"]
    pros = ide_info["pros"]
    cons = ide_info["cons"]
    best_for = ide_info["best_for"]
    verdict = ide_info["verdict"]
    icon_url = ide_info["icon_url"]

    pros_lis = "".join([f"<li>✅ <strong>{p}</strong></li>" for p in pros])
    cons_lis = "".join([f"<li>❌ <strong>{c}</strong></li>" for c in cons])

    html_content = f"""<!doctype html>
<html ⚡ lang="en">
<head>
  <meta charset="utf-8">
  <title>{name} Review & Evaluation | IDE Guide</title>
  <link rel="canonical" href="{BLOGGER_URL}">
  <meta name="viewport" content="width=device-width,minimum-scale=1,initial-scale=1">
  <script async src="https://cdn.ampproject.org/v0.js"></script>
  <style amp-boilerplate>body{{-webkit-animation:-amp-start 8s steps(1,end) 0s 1 normal both;-moz-animation:-amp-start 8s steps(1,end) 0s 1 normal both;-ms-animation:-amp-start 8s steps(1,end) 0s 1 normal both;animation:-amp-start 8s steps(1,end) 0s 1 normal both}}@-webkit-keyframes -amp-start{{from{{visibility:hidden}}to{{visibility:visible}}}}@-moz-keyframes -amp-start{{from{{visibility:hidden}}to{{visibility:visible}}}}@-ms-keyframes -amp-start{{from{{visibility:hidden}}to{{visibility:visible}}}}@-o-keyframes -amp-start{{from{{visibility:hidden}}to{{visibility:visible}}}}@keyframes -amp-start{{from{{visibility:hidden}}to{{visibility:visible}}}}</style><noscript><style amp-boilerplate>body{{-webkit-animation:none;-moz-animation:none;-ms-animation:none;animation:none}}</style></noscript>
  <style amp-custom>
    body {{
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
      line-height: 1.6;
      color: #1a202c;
      background-color: #f7fafc;
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
      border-radius: 16px;
      font-size: 14px;
      font-weight: 600;
      background-color: #00f3ff;
      color: #0d1117;
      margin-bottom: 12px;
    }}
    .pricing-badge {{
      background-color: #e2e8f0;
      color: #2d3748;
      font-weight: bold;
      padding: 4px 8px;
      border-radius: 4px;
    }}
    h1 {{
      color: #0f172a;
      font-size: 28px;
      margin-top: 0;
    }}
    .hero-img {{
      margin: 16px 0;
      border-radius: 8px;
      overflow: hidden;
    }}
    .grid-table {{
      width: 100%;
      border-collapse: collapse;
      margin: 20px 0;
    }}
    .grid-table th, .grid-table td {{
      border: 1px solid #e2e8f0;
      padding: 12px;
      text-align: left;
    }}
    .grid-table th {{
      background-color: #f1f5f9;
    }}
    ul {{
      padding-left: 20px;
    }}
    li {{
      margin-bottom: 8px;
    }}
    .verdict-box {{
      background: #f0fdf4;
      border-left: 4px solid #22c55e;
      padding: 16px;
      border-radius: 4px;
      margin: 20px 0;
    }}
    .disclaimer {{
      font-size: 12px;
      color: #64748b;
      background-color: #f8fafc;
      border: 1px solid #e2e8f0;
      padding: 12px;
      border-radius: 6px;
      margin-top: 30px;
    }}
    .channel-link {{
      display: inline-block;
      margin-top: 16px;
      padding: 10px 20px;
      background-color: #ff0000;
      color: #ffffff;
      text-decoration: none;
      border-radius: 6px;
      font-weight: bold;
    }}
  </style>
</head>
<body>
  <div class="container">
    <span class="badge">{category}</span>
    <h1>{name} - Complete Review, Evaluation & Pricing Guide</h1>
    <p><strong>Developer / Creator:</strong> {developer} | <span class="pricing-badge">{pricing}</span></p>

    <div class="hero-img">
      <amp-img src="{icon_url}" width="800" height="400" layout="responsive" alt="{name} Code Editor Overview"></amp-img>
    </div>

    <h2>Executive Overview</h2>
    <p>{summary}</p>

    <h2>Key Specifications & Feature Breakdown</h2>
    <table class="grid-table">
      <tr>
        <th>Attribute</th>
        <th>Details</th>
      </tr>
      <tr>
        <td><strong>Editor Name</strong></td>
        <td>{name}</td>
      </tr>
      <tr>
        <td><strong>Primary Category</strong></td>
        <td>{category}</td>
      </tr>
      <tr>
        <td><strong>Pricing Structure</strong></td>
        <td>{pricing}</td>
      </tr>
      <tr>
        <td><strong>Target Audience</strong></td>
        <td>{best_for}</td>
      </tr>
    </table>

    <h2>Pros & Advantages</h2>
    <ul>
      {pros_lis}
    </ul>

    <h2>Cons & Trade-offs</h2>
    <ul>
      {cons_lis}
    </ul>

    <div class="verdict-box">
      <h3>💡 Final Verdict</h3>
      <p>{verdict}</p>
    </div>

    <p>Watch video reviews and tutorials on our official YouTube channel:</p>
    <a href="{YOUTUBE_URL}" target="_blank" class="channel-link">▶ Watch on YouTube @IDEguide</a>

    <div class="disclaimer">
      <p>{DISCLAIMER_TEXT}</p>
    </div>
  </div>
</body>
</html>
"""
    return html_content


def generate_google_flow_video_spec(ide_info, post_num):
    """Generate Google Flow JSON & Markdown specification for YouTube videos/Shorts."""
    name = ide_info["name"]
    category = ide_info["category"]
    pricing = ide_info["pricing"]
    summary = ide_info["summary"]
    pros = ", ".join(ide_info["pros"])
    cons = ", ".join(ide_info["cons"])
    verdict = ide_info["verdict"]

    scenes = [
        {
            "scene_number": 1,
            "start_time": "00:00",
            "end_time": "00:05",
            "title": "Hook & Introduction",
            "prompt": f"Cinematic close-up of a developer keyboard glowing with custom RGB lighting in a dark room. The screen displays the logo and interface of {name} ({category}). Soft cyan neon accent lights, 4k ultra-detailed developer workstation.",
            "camera_motion": "slow_pan_right",
            "framing": "medium_close_up",
            "aspect_ratio": "16:9 and 9:16",
            "voiceover_text": f"Should you upgrade to {name} in 2026? Here is everything you need to know about this {category} in under 60 seconds!"
        },
        {
            "scene_number": 2,
            "start_time": "00:05",
            "end_time": "00:20",
            "title": "Core Features & Pros",
            "prompt": f"Direct macro shot of crisp code editor text being typed at super-fast speed in {name}. Neon syntax highlighting, multi-file side-by-side view, smooth modern developer desktop UI.",
            "camera_motion": "zoom_in_slow",
            "framing": "extreme_close_up",
            "aspect_ratio": "16:9 and 9:16",
            "voiceover_text": f"{summary} Key benefits include: {pros}."
        },
        {
            "scene_number": 3,
            "start_time": "00:20",
            "end_time": "00:35",
            "title": "Cons & Trade-offs",
            "prompt": "Split screen technical visualization showing memory usage graphs and code execution comparison in a modern dark-mode software interface.",
            "camera_motion": "static_hero",
            "framing": "wide_angle",
            "aspect_ratio": "16:9 and 9:16",
            "voiceover_text": f"However, keep in mind these trade-offs: {cons}."
        },
        {
            "scene_number": 4,
            "start_time": "00:35",
            "end_time": "00:50",
            "title": "Pricing & Comparison",
            "prompt": "Clean infographic visual on a sleek monitor showing Free tier vs Paid subscription features with metallic neon checkmarks.",
            "camera_motion": "tilt_up",
            "framing": "medium_shot",
            "aspect_ratio": "16:9 and 9:16",
            "voiceover_text": f"Pricing Model: {pricing}. Is it free or paid? We break down the value for independent developers and teams."
        },
        {
            "scene_number": 5,
            "start_time": "00:50",
            "end_time": "01:00",
            "title": "Verdict & Outro CTA",
            "prompt": "Dynamic end screen with YouTube @IDEguide subscribe button prompt and Blogger URL overlay on top of an elegant mechanical keyboard shot.",
            "camera_motion": "pull_back",
            "framing": "medium_shot",
            "aspect_ratio": "16:9 and 9:16",
            "voiceover_text": f"Final Verdict: {verdict} Subscribe to @IDEguide for daily tool breakdowns and read the full AMP review at ideguide.blogspot.com!"
        }
    ]

    video_spec_data = {
        "title": f"{name} Review - Pros, Cons, Free vs Paid & Best Use Cases",
        "ide_name": name,
        "category": category,
        "pricing": pricing,
        "youtube_channel": YOUTUBE_URL,
        "blogger_url": BLOGGER_URL,
        "disclaimer": DISCLAIMER_TEXT,
        "scenes": scenes
    }

    # Generate Markdown Script format
    md_content = f"""# Google Flow Video Spec & Script: {name}

**Channel:** YouTube `@IDEguide` | **Blog:** `https://ideguide.blogspot.com/`
**Topic:** {name} ({category})
**Pricing:** {pricing}

---

## Non-Sponsorship Disclaimer
> {DISCLAIMER_TEXT}

---

## Scene-by-Scene Prompt Specification for Google Flow / AI Synthesis

"""
    for sc in scenes:
        md_content += f"""### Scene {sc['scene_number']}: {sc['title']} (`{sc['start_time']} - {sc['end_time']}`)
- **Visual Prompt:** {sc['prompt']}
- **Camera Motion:** `{sc['camera_motion']}` | **Framing:** `{sc['framing']}` | **Aspect Ratio:** `{sc['aspect_ratio']}`
- **Voiceover Script:** "{sc['voiceover_text']}"

"""

    md_content += f"""---
## YouTube Shorts / Video Metadata
- **Title:** {name} Review: Is it Free or Paid? (Pros & Cons Explained)
- **Description:**
  Full evaluation of {name} ({category}).
  Read full AMP article: {BLOGGER_URL}
  Subscribe to @IDEguide: {YOUTUBE_URL}

  {DISCLAIMER_TEXT}
- **Hashtags:** #{name.replace(' ', '')} #IDE #CodeEditor #DeveloperTools #Programming #IDEGuide
"""

    return video_spec_data, md_content


def run_daily_generation(target_date=None):
    """Main execution engine generating 3 daily blog posts & 3 daily video specs."""
    if not target_date:
        target_date = datetime.date.today().strftime("%Y-%m-%d")

    content_dir = os.path.join("content", target_date)
    os.makedirs(content_dir, exist_ok=True)

    history_path = os.path.join("content", "history.json")
    history = {"covered_slugs": []}
    if os.path.exists(history_path):
        try:
            with open(history_path, "r", encoding="utf-8") as f:
                history = json.load(f)
        except Exception:
            history = {"covered_slugs": []}

    covered_set = set(history.get("covered_slugs", []))

    # Catalog candidate selection
    full_catalog = list(DEFAULT_IDE_CATALOG)

    # Try discovering additional IDEs from GitHub if available
    discovered = fetch_trending_github_ides()
    for disc in discovered:
        if not any(item['slug'] == disc['slug'] for item in full_catalog):
            full_catalog.append(disc)

    # Filter out already covered IDEs
    uncovered = [item for item in full_catalog if item["slug"] not in covered_set]

    # Reset covered history if all catalog items have been covered
    if len(uncovered) < 3:
        covered_set = set()
        uncovered = full_catalog

    selected_ides = uncovered[:3]

    results = []
    for idx, ide_info in enumerate(selected_ides, start=1):
        slug = ide_info["slug"]
        covered_set.add(slug)

        # 1. AMP HTML Blog Post
        amp_html = generate_amp_html_post(ide_info, idx)
        amp_file = os.path.join(content_dir, f"post_{idx}_{slug}.html")
        with open(amp_file, "w", encoding="utf-8") as f:
            f.write(amp_html)

        # 2. Google Flow Video Spec (JSON & Markdown)
        video_spec_json, video_spec_md = generate_google_flow_video_spec(ide_info, idx)
        json_file = os.path.join(content_dir, f"video_{idx}_{slug}.json")
        with open(json_file, "w", encoding="utf-8") as f:
            json.dump(video_spec_json, f, indent=2)

        md_file = os.path.join(content_dir, f"video_{idx}_{slug}.md")
        with open(md_file, "w", encoding="utf-8") as f:
            f.write(video_spec_md)

        results.append({
            "index": idx,
            "ide": ide_info["name"],
            "amp_post": amp_file,
            "video_spec_json": json_file,
            "video_spec_md": md_file
        })

    # Update history file
    history["covered_slugs"] = list(covered_set)
    history["last_generated_date"] = target_date
    with open(history_path, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=2)

    print(f"Successfully generated daily content for {target_date} in '{content_dir}':")
    for res in results:
        print(f" [{res['index']}] {res['ide']}")
        print(f"     Blog Post (AMP): {res['amp_post']}")
        print(f"     Video Spec (JSON): {res['video_spec_json']}")
        print(f"     Video Spec (MD): {res['video_spec_md']}")

    return results


if __name__ == "__main__":
    date_arg = sys.argv[1] if len(sys.argv) > 1 else None
    run_daily_generation(date_arg)
