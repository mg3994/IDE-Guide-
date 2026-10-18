#!/usr/bin/env python3
"""
Daily Content Generator for IDE Guide.
Generates 3 daily content packages (3 videos, 3 blog posts) covering code editors and IDEs.
Outputs AMP HTML blog posts for Blogger (ideguide.blogspot.com)
and Google Flow video generation specs for YouTube (@IDEguide).
Tracks covered tools in `content/history.json` to prevent repeated coverage.
"""

import os
import json
import datetime
from typing import List, Dict, Any

HISTORY_FILE = os.path.join("content", "history.json")

DISCLAIMER_TEXT = (
    "Disclaimer: IDE Guide is an independent technical publication. "
    "This content is not sponsored, endorsed, or affiliated with any software vendor "
    "or editor developer mentioned above. All reviews and assessments are based strictly "
    "on objective developer evaluation."
)

# Rich pool of IDEs and Code Editors
IDE_CATALOG: List[Dict[str, Any]] = [
    {
        "id": "cursor",
        "name": "Cursor IDE",
        "category": "AI Code Editor",
        "pricing_type": "Freemium",
        "pricing_details": "Free tier available; Pro at $20/month for unlimited Claude 3.5 Sonnet & GPT-4o usage.",
        "tagline": "The AI-first Code Editor built as a fork of VS Code.",
        "pros": [
            "Native AI agent integration with repository indexing",
            "Multi-file edit suggestions (Composer mode)",
            "Seamless extension migration from VS Code"
        ],
        "cons": [
            "Pro subscription required for high-frequency AI features",
            "Heavy RAM usage on massive multi-repo workspaces"
        ],
        "target_audience": "Full-stack developers, AI-assisted coders, and web engineers.",
        "verdict": "Best overall AI-enhanced code editor for developers seeking modern speed and workspace-wide AI context."
    },
    {
        "id": "vscode",
        "name": "Visual Studio Code",
        "category": "Open-Source Code Editor",
        "pricing_type": "Free",
        "pricing_details": "100% Free and open-source (MIT license core).",
        "tagline": "The world's most popular code editor backed by a vast ecosystem.",
        "pros": [
            "Unrivaled extension marketplace",
            "Extremely lightweight and highly configurable",
            "Massive global community support"
        ],
        "cons": [
            "Requires third-party plugins for advanced AI features",
            "Extension bloat can degrade startup performance"
        ],
        "target_audience": "All software engineers, students, and open-source contributors.",
        "verdict": "The undisputed benchmark for general programming, flexibility, and ecosystem breadth."
    },
    {
        "id": "intellij_idea",
        "name": "JetBrains IntelliJ IDEA",
        "category": "Full-Featured Enterprise IDE",
        "pricing_type": "Freemium",
        "pricing_details": "Community Edition is Free; Ultimate Edition at $169/year.",
        "tagline": "The gold standard IDE for Java, Kotlin, and enterprise backend engineering.",
        "pros": [
            "Deep static code analysis and refactoring tools",
            "Built-in database, Git, and profiler integration",
            "Top-tier Kotlin and Java ecosystem support"
        ],
        "cons": [
            "High memory footprint (requires 16GB+ RAM recommended)",
            "Paid license required for full enterprise web frameworks"
        ],
        "target_audience": "Java, Kotlin, Enterprise, and Android backend developers.",
        "verdict": "Unbeatable for large-scale enterprise Java and Kotlin projects where refactoring precision is critical."
    },
    {
        "id": "neovim",
        "name": "Neovim",
        "category": "Modal Terminal Code Editor",
        "pricing_type": "Free",
        "pricing_details": "100% Free and Open Source.",
        "tagline": "Hyperspeed terminal-based modal editor powered by Lua.",
        "pros": [
            "Blazing fast startup and near-zero memory footprint",
            "Limitless customizability via Lua scripting",
            "Native LSP and Tree-sitter integration"
        ],
        "cons": [
            "Steep learning curve for keybindings and config setup",
            "No out-of-the-box GUI interface"
        ],
        "target_audience": "DevOps engineers, terminal purists, and speed-driven developers.",
        "verdict": "The ultimate editor for developers who value keyboard navigation, speed, and absolute customization."
    },
    {
        "id": "zed",
        "name": "Zed Editor",
        "category": "High-Performance Code Editor",
        "pricing_type": "Freemium",
        "pricing_details": "Free open-source editor; Zed Industry Cloud collaboration plans optional.",
        "tagline": "Next-generation multiplayer code editor written in Rust.",
        "pros": [
            "GPU-accelerated rendering at 120+ FPS",
            "Instant startup time with minimal CPU footprint",
            "Built-in multiplayer real-time pairing"
        ],
        "cons": [
            "Ecosystem and plugin gallery still growing compared to VS Code",
            "Currently macOS & Linux primary (Windows support in development)"
        ],
        "target_audience": "Performance enthusiasts, Rust developers, and collaborative teams.",
        "verdict": "The fastest modern code editor available today, engineered for fluid UI rendering and multiplayer pair programming."
    },
    {
        "id": "pycharm",
        "name": "JetBrains PyCharm",
        "category": "Python IDE",
        "pricing_type": "Freemium",
        "pricing_details": "Community Edition is Free; Professional Edition at $99/year.",
        "tagline": "The premier IDE dedicated to Python and Data Science.",
        "pros": [
            "Intelligent code completion, refactoring, and debugging",
            "Built-in Jupyter notebook and scientific stack integration",
            "Django, Flask, and FastAPI web framework support in Pro"
        ],
        "cons": [
            "Can be resource heavy on smaller machines",
            "Pro features locked behind subscription"
        ],
        "target_audience": "Python developers, Data Scientists, and Backend Web Engineers.",
        "verdict": "The definitive IDE for serious Python engineers and data science workflows."
    },
    {
        "id": "webstorm",
        "name": "JetBrains WebStorm",
        "category": "JavaScript / TypeScript IDE",
        "pricing_type": "Paid",
        "pricing_details": "Paid subscription at $69/year (Free for students/non-commercial open source).",
        "tagline": "The smartest JavaScript and TypeScript IDE.",
        "pros": [
            "Out-of-the-box support for React, Vue, Angular, Node.js",
            "Superior refactoring and auto-import features",
            "Powerful integrated test runner and debugger"
        ],
        "cons": [
            "Paid commercial licensing",
            "Higher memory footprint compared to VS Code"
        ],
        "target_audience": "Frontend and full-stack JavaScript/TypeScript engineers.",
        "verdict": "Top choice for full-stack JavaScript developers requiring advanced refactoring without configuring plugins."
    },
    {
        "id": "sublime_text",
        "name": "Sublime Text 4",
        "category": "Lightweight Text Editor",
        "pricing_type": "Freemium",
        "pricing_details": "Free evaluation without time limit; Personal license at $99.",
        "tagline": "A sophisticated text editor for code, markup, and prose.",
        "pros": [
            "GPU acceleration for ultra-smooth scrolling",
            "Instant file opening across huge codebases",
            "Extremely low CPU and memory usage"
        ],
        "cons": [
            "Lacks out-of-the-box AI and deep IDE features",
            "Nag popups in free evaluation mode"
        ],
        "target_audience": "Developers looking for speed, light weight, and quick editing.",
        "verdict": "Ideal for fast editing, low-resource environments, and developers who prioritize instant file searching."
    },
    {
        "id": "windsurf",
        "name": "Windsurf Editor (Codeium)",
        "category": "AI-Agentic Code Editor",
        "pricing_type": "Freemium",
        "pricing_details": "Free tier with generous AI credits; Pro at $15/month.",
        "tagline": "First agentic IDE with Cascade AI flow.",
        "pros": [
            "Deep context awareness via Cascade agentic flows",
            "Seamless terminal command execution suggestions",
            "Fast real-time inline completions"
        ],
        "cons": [
            "Relatively new tool in rapid development",
            "Requires cloud AI connectivity for full capabilities"
        ],
        "target_audience": "AI-native developers and rapid product builders.",
        "verdict": "Innovative agentic IDE offering intuitive developer-AI collaboration."
    },
    {
        "id": "xcode",
        "name": "Apple Xcode",
        "category": "Native iOS / macOS IDE",
        "pricing_type": "Free",
        "pricing_details": "100% Free for macOS users via Mac App Store.",
        "tagline": "The official IDE for building Apple platform apps.",
        "pros": [
            "Native SwiftUI canvas preview and visual layout editor",
            "Integrated iOS/iPadOS simulator and Instruments profiler",
            "Direct App Store deployment pipeline"
        ],
        "cons": [
            "macOS exclusive only",
            "Large disk space requirement (30GB+)"
        ],
        "target_audience": "iOS, macOS, watchOS, and visionOS developers.",
        "verdict": "Essential and mandatory tool for any developer publishing to the Apple ecosystem."
    },
    {
        "id": "replit",
        "name": "Replit Agent & Cloud IDE",
        "category": "Cloud / Browser IDE",
        "pricing_type": "Freemium",
        "pricing_details": "Free basic tier; Core subscription at $20/month.",
        "tagline": "Build, deploy, and collaborate directly from the browser.",
        "pros": [
            "Zero local setup required; runs instantly in browser",
            "Replit Agent auto-builds full-stack applications from prompts",
            "Instant hosting and database deployment"
        ],
        "cons": [
            "Requires active internet connection",
            "Compute limits on free tier"
        ],
        "target_audience": "Beginners, hackathon builders, and web developers on Chromebooks/light laptops.",
        "verdict": "The best browser-native cloud IDE for instant prototyping and deployment."
    },
    {
        "id": "fleet",
        "name": "JetBrains Fleet",
        "category": "Lightweight Next-Gen IDE",
        "pricing_type": "Freemium",
        "pricing_details": "Free public preview; integrated with JetBrains subscription.",
        "tagline": "Lightweight editor transformed into a full IDE on demand.",
        "pros": [
            "Fast dual-mode architecture (Lightweight Editor vs Smart IDE)",
            "Distributed remote development and cloud workspace support",
            "Clean, modern minimal UI"
        ],
        "cons": [
            "Still under active preview development",
            "Fewer plugins compared to traditional JetBrains IDEs"
        ],
        "target_audience": "Developers who want JetBrains smarts with lightweight editor speed.",
        "verdict": "Promising hybrid editor combining instant startup with JetBrains code intelligence."
    }
]

def load_history() -> List[str]:
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data.get("covered_ids", [])
        except Exception:
            return []
    return []

def save_history(history: List[str]) -> None:
    os.makedirs(os.path.dirname(HISTORY_FILE), exist_ok=True)
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump({"covered_ids": history, "last_updated": datetime.date.today().isoformat()}, f, indent=2)

def select_daily_ides(count: int = 3) -> List[Dict[str, Any]]:
    history = load_history()
    available = [item for item in IDE_CATALOG if item["id"] not in history]

    # Reset history if all catalog items have been covered
    if len(available) < count:
        history = []
        available = list(IDE_CATALOG)

    selected = available[:count]
    updated_history = history + [item["id"] for item in selected]
    save_history(updated_history)
    return selected

def generate_amp_blog_post(ide: Dict[str, Any], date_str: str) -> str:
    pros_html = "\n".join([f"      <li><strong>{p}</strong></li>" for p in ide["pros"]])
    cons_html = "\n".join([f"      <li><strong>{c}</strong></li>" for c in ide["cons"]])

    return f"""<!doctype html>
<html amp lang="en">
<head>
  <meta charset="utf-8">
  <title>{ide['name']} Guide & Deep Dive ({date_str}) | IDE Guide</title>
  <link rel="canonical" href="https://ideguide.blogspot.com/p/{ide['id']}-review-{date_str}.html">
  <meta name="viewport" content="width=device-width,minimum-scale=1,initial-scale=1">
  <script async src="https://cdn.ampproject.org/v0.js"></script>
  <style amp-boilerplate>body{{-webkit-animation:-amp-start 8s steps(1,end) 0s 1 normal both;-moz-animation:-amp-start 8s steps(1,end) 0s 1 normal both;-ms-animation:-amp-start 8s steps(1,end) 0s 1 normal both;animation:-amp-start 8s steps(1,end) 0s 1 normal both}}@-webkit-keyframes -amp-start{{from{{visibility:hidden}}to{{visibility:visible}}}}@-moz-keyframes -amp-start{{from{{visibility:hidden}}to{{visibility:visible}}}}@-ms-keyframes -amp-start{{from{{visibility:hidden}}to{{visibility:visible}}}}@-o-keyframes -amp-start{{from{{visibility:hidden}}to{{visibility:visible}}}}@keyframes -amp-start{{from{{visibility:hidden}}to{{visibility:visible}}}}</style><noscript><style amp-boilerplate>body{{-webkit-animation:none;-moz-animation:none;-ms-animation:none;-animation:none}}</style></noscript>
  <style amp-custom>
    body {{
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
      line-height: 1.6;
      color: #0f172a;
      background-color: #f8fafc;
      margin: 0;
      padding: 0;
    }}
    header {{
      background-color: #0f172a;
      color: #ffffff;
      padding: 24px 16px;
      text-align: center;
    }}
    header h1 {{
      margin: 0 0 8px 0;
      font-size: 26px;
    }}
    .badge {{
      display: inline-block;
      background-color: #0284c7;
      color: #ffffff;
      padding: 4px 12px;
      border-radius: 12px;
      font-size: 14px;
      font-weight: bold;
      text-transform: uppercase;
    }}
    .container {{
      max-width: 800px;
      margin: 24px auto;
      padding: 0 16px;
    }}
    .card {{
      background: #ffffff;
      border-radius: 8px;
      padding: 20px;
      box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);
      margin-bottom: 20px;
    }}
    h2 {{
      color: #0369a1;
      border-bottom: 2px solid #e2e8f0;
      padding-bottom: 8px;
    }}
    ul {{
      padding-left: 20px;
    }}
    .price-box {{
      background-color: #f0fdf4;
      border-left: 4px solid #16a34a;
      padding: 12px 16px;
      margin: 16px 0;
    }}
    .disclaimer {{
      background-color: #f1f5f9;
      border: 1px solid #cbd5e1;
      padding: 14px;
      border-radius: 6px;
      font-size: 13px;
      color: #475569;
      margin-top: 30px;
    }}
  </style>
</head>
<body>

  <header>
    <span class="badge">{ide['category']}</span>
    <h1>{ide['name']}: Comprehensive Technical Assessment</h1>
    <p>{ide['tagline']}</p>
  </header>

  <div class="container">
    <div class="card">
      <amp-img src="https://images.unsplash.com/photo-1555066931-4365d14bab8c?auto=format&fit=crop&w=800&q=80" width="800" height="450" layout="responsive" alt="{ide['name']} workspace preview"></amp-img>

      <h2>Overview & Target Audience</h2>
      <p><strong>{ide['name']}</strong> is categorized as a <strong>{ide['category']}</strong>. It is designed specifically for <em>{ide['target_audience']}</em>.</p>

      <div class="price-box">
        <strong>Pricing Model:</strong> {ide['pricing_type']}<br>
        <strong>Details:</strong> {ide['pricing_details']}
      </div>

      <h2>Key Strengths & Advantages</h2>
      <ul>
{pros_html}
      </ul>

      <h2>Areas for Improvement & Cons</h2>
      <ul>
{cons_html}
      </ul>

      <h2>Final Verdict</h2>
      <p>{ide['verdict']}</p>
    </div>

    <div class="disclaimer">
      {DISCLAIMER_TEXT}
    </div>
  </div>

</body>
</html>"""

def generate_google_flow_spec(ide: Dict[str, Any], date_str: str) -> Dict[str, Any]:
    return {
        "title": f"{ide['name']} Review & Comparison ({date_str}) | IDE Guide",
        "channel": "@IDEguide",
        "target_platform": "YouTube Shorts & Main Video",
        "pricing_badge": ide["pricing_type"].upper(),
        "pricing_details": ide["pricing_details"],
        "disclaimer": DISCLAIMER_TEXT,
        "scenes": [
            {
                "scene_id": 1,
                "duration_seconds": 5,
                "google_flow_prompt": f"Cinematic 4K close-up shot of code editor interface showing {ide['name']} logo and crisp syntax highlighting on dark mode screen with glowing neon cyan accents.",
                "camera_movement": "Slow subtle push-in zoom towards code editor tab",
                "lighting": "Cyberpunk dark room glow with soft key light on mechanical keyboard",
                "on_screen_text": f"IS {ide['name'].upper()} WORTH IT IN {date_str[:4]}?",
                "voiceover_script": f"Is {ide['name']} actually worth switching to right now? Let's break down the pros, cons, and pricing in 60 seconds."
            },
            {
                "scene_id": 2,
                "duration_seconds": 15,
                "google_flow_prompt": f"Smooth screen recording style animation showing {ide['name']} executing fast code auto-completion and file indexing in dark theme UI.",
                "camera_movement": "Static high-definition screen focus with floating feature cards",
                "lighting": "Clean studio lighting on monitor frame",
                "on_screen_text": f"PROS: {ide['pros'][0]}",
                "voiceover_script": f"{ide['name']} excels at {ide['pros'][0].lower()} and {ide['pros'][1].lower()}."
            },
            {
                "scene_id": 3,
                "duration_seconds": 15,
                "google_flow_prompt": f"Split screen visual contrast showing code editor benchmarking performance and memory usage graphs in dark theme.",
                "camera_movement": "Pan left to right across feature matrix",
                "lighting": "Balanced volumetric display lighting",
                "on_screen_text": f"PRICING: {ide['pricing_type']} ({ide['pricing_details']})",
                "voiceover_script": f"Pricing-wise, it's {ide['pricing_type']}. {ide['pricing_details']}"
            },
            {
                "scene_id": 4,
                "duration_seconds": 10,
                "google_flow_prompt": f"High tech summary graphic showing final score badge and target audience card on minimalist dark workspace.",
                "camera_movement": "Gentle pull-back shot showing laptop workspace",
                "lighting": "Warm desk lamp contrast with dark blue background",
                "on_screen_text": f"VERDICT: {ide['verdict']}",
                "voiceover_script": f"Our verdict: {ide['verdict']} Subscribe to IDE Guide for daily developer comparisons!"
            }
        ]
    }

def generate_daily_package(target_date: str = None) -> List[str]:
    if target_date is None:
        target_date = datetime.date.today().isoformat()

    output_dir = os.path.join("content", target_date)
    os.makedirs(output_dir, exist_ok=True)

    selected_ides = select_daily_ides(count=3)
    generated_files = []

    for idx, ide in enumerate(selected_ides, 1):
        slug = ide['id']

        # Generate AMP HTML Blog Post
        amp_html_content = generate_amp_blog_post(ide, target_date)
        blog_filename = f"post_{idx}_{slug}_amp.html"
        blog_path = os.path.join(output_dir, blog_filename)
        with open(blog_path, "w", encoding="utf-8") as f:
            f.write(amp_html_content)
        generated_files.append(blog_path)

        # Generate Google Flow Video Spec
        flow_spec_content = generate_google_flow_spec(ide, target_date)
        video_filename = f"video_{idx}_{slug}_google_flow_spec.json"
        video_path = os.path.join(output_dir, video_filename)
        with open(video_path, "w", encoding="utf-8") as f:
            json.dump(flow_spec_content, f, indent=2)
        generated_files.append(video_path)

    print(f"Successfully generated 3 daily content packages in '{output_dir}':")
    for filepath in generated_files:
        print(f"  - {filepath}")

    return generated_files

if __name__ == "__main__":
    generate_daily_package()
