#!/usr/bin/env python3
"""
IDE Guide Content Generator Core Module

Generates AMP HTML blog posts for Blogger (ideguide.blogspot.com)
and Google Flow video specifications for YouTube (@IDEguide).
"""

import os
import json
import datetime
import urllib.request
import re

DISCLAIMER_TEXT = (
    "Disclaimer: IDE Guide is an independent technical publication. "
    "This content is not sponsored, endorsed, or affiliated with any software vendor "
    "or editor developer mentioned above. All reviews and assessments are based strictly "
    "on objective developer evaluation."
)

YOUTUBE_URL = "https://www.youtube.com/@IDEguide"
BLOGGER_URL = "https://ideguide.blogspot.com/"

# Pre-curated database of IDEs and Code Editors for automated daily coverage
IDE_DATABASE = [
    {
        "id": "vscode",
        "name": "Visual Studio Code",
        "tagline": "The ubiquitous extensible open-source code editor from Microsoft.",
        "developer": "Microsoft",
        "pricing_type": "Free / Open Source (Core)",
        "pricing_details": "Free (MIT License core / Freeware distribution build). Optional GitHub Copilot paid subscription.",
        "pros": [
            "Vast extension ecosystem with thousands of plugins",
            "Exceptional multi-language and framework support",
            "Built-in Git integration and terminal",
            "Lightweight resource usage compared to full IDEs"
        ],
        "cons": [
            "Can consume significant RAM with many active extensions",
            "Requires configuration tuning for out-of-the-box C++/Java environments",
            "Telemetry enabled by default (can be disabled or avoided via VSCodium)"
        ],
        "target_audience": "Full-stack web developers, Python programmers, and general software engineers.",
        "hero_image": "https://images.unsplash.com/photo-1555066931-4365d14bab8c?w=1200&auto=format&fit=crop&q=80",
        "category": "General Code Editor"
    },
    {
        "id": "cursor",
        "name": "Cursor AI Code Editor",
        "tagline": "The AI-first fork of VS Code built for rapid AI pair programming.",
        "developer": "Anysphere",
        "pricing_type": "Freemium",
        "pricing_details": "Free tier (Hobby) with 200 GPT-3.5 / Claude 3.5 Sonnet uses/mo; Pro tier ($20/mo) for unlimited fast AI queries.",
        "pros": [
            "Seamless codebase indexing with multi-file edit capabilities (Cmd+K / Chat)",
            "Native integration with Claude 3.5 Sonnet and GPT-4o models",
            "Full compatibility with all VS Code extensions and settings",
            "Predictive inline code completion ('Cursor Tab')"
        ],
        "cons": [
            "Pro tier required for heavy daily AI usage",
            "Requires internet connectivity for cloud AI indexing",
            "Closed-source privacy-sensitive codebases require strict privacy mode settings"
        ],
        "target_audience": "Developers looking to maximize coding speed with cutting-edge AI assistance.",
        "hero_image": "https://images.unsplash.com/photo-1618401471353-b98afee0b2eb?w=1200&auto=format&fit=crop&q=80",
        "category": "AI Code Editor"
    },
    {
        "id": "intellij-idea",
        "name": "JetBrains IntelliJ IDEA",
        "tagline": "The gold-standard integrated development environment for Java and Kotlin.",
        "developer": "JetBrains",
        "pricing_type": "Freemium / Commercial",
        "pricing_details": "Community Edition is Free & Open Source; Ultimate Edition starts at $169/year for individuals.",
        "pros": [
            "Unrivaled static code analysis, refactoring, and auto-completion",
            "Built-in database tooling, framework assistance (Spring, Jakarta EE)",
            "Deep debugging and profiling capabilities",
            "Robust version control and database browser UI"
        ],
        "cons": [
            "Heavy memory and CPU footprint requiring modern hardware",
            "Ultimate features are behind a paid subscription",
            "Slower initial project indexing time on large codebases"
        ],
        "target_audience": "Enterprise Java/Kotlin developers, backend engineers, and Android developers.",
        "hero_image": "https://images.unsplash.com/photo-1542831371-29b0f74f9713?w=1200&auto=format&fit=crop&q=80",
        "category": "Enterprise IDE"
    },
    {
        "id": "zed",
        "name": "Zed Editor",
        "tagline": "High-performance, GPU-accelerated multiplayer code editor written in Rust.",
        "developer": "Zed Industries",
        "pricing_type": "Free / Open Source",
        "pricing_details": "Free & Open Source (GPL/AGPL/Apache). Zed AI features offer free tiers and pay-as-you-go API keys.",
        "pros": [
            "Blazing fast startup and instant 120 FPS rendering via GPU acceleration",
            "Built-in collaborative multiplayer pair-programming out of the box",
            "Integrated language server protocol (LSP) and Tree-sitter syntax parsing",
            "Minimalist, low-latency interface written in Rust"
        ],
        "cons": [
            "Ecosystem of extensions is still growing compared to VS Code",
            "Linux/Windows support is newer compared to macOS build history",
            "Fewer niche language plugins out of the box"
        ],
        "target_audience": "Performance enthusiasts, Rust/Go/TypeScript developers, and collaborative teams.",
        "hero_image": "https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?w=1200&auto=format&fit=crop&q=80",
        "category": "High-Performance Code Editor"
    },
    {
        "id": "neovim",
        "name": "Neovim",
        "tagline": "Hyperextensible Vim-based text editor built for extreme terminal productivity.",
        "developer": "Neovim Core Team",
        "pricing_type": "Free / Open Source",
        "pricing_details": "100% Free & Open Source (Apache 2.0 / Vim License).",
        "pros": [
            "Ultra-lightweight with zero GPU/GUI overhead",
            "Full Lua plugin ecosystem with built-in LSP client",
            "Lightning-fast modal editing keyboard navigation",
            "Fully customizable terminal-native interface"
        ],
        "cons": [
            "Steep learning curve for modal keybindings",
            "Requires time investment to configure custom config files (init.lua)",
            "No native graphical mouse UI out of the box"
        ],
        "target_audience": "Terminal power users, DevOps engineers, and keyboard-centric developers.",
        "hero_image": "https://images.unsplash.com/photo-1629654297299-c8506221ca97?w=1200&auto=format&fit=crop&q=80",
        "category": "Modal Text Editor"
    },
    {
        "id": "pycharm",
        "name": "JetBrains PyCharm",
        "tagline": "The intelligent Python IDE built specifically for data science and web development.",
        "developer": "JetBrains",
        "pricing_type": "Freemium / Commercial",
        "pricing_details": "Community Edition is free; Professional Edition starts at $99/year for individuals.",
        "pros": [
            "Deepest Python code inspection, refactoring, and virtualenv management",
            "Native Jupyter Notebook support and Scientific mode",
            "Integrated web framework tooling (Django, Flask, FastAPI)",
            "Built-in SQL database browser and REST client"
        ],
        "cons": [
            "Resource-intensive setup for basic quick scripts",
            "Web development features restricted to paid Professional Edition",
            "Requires high RAM allocation for large data science projects"
        ],
        "target_audience": "Python engineers, Data Scientists, ML developers, and Django/FastAPI developers.",
        "hero_image": "https://images.unsplash.com/photo-1515879218367-8466d910aaa4?w=1200&auto=format&fit=crop&q=80",
        "category": "Python Specialist IDE"
    },
    {
        "id": "windsurf",
        "name": "Windsurf Editor",
        "tagline": "The agentic AI IDE by Codeium featuring Flows and collaborative AI agents.",
        "developer": "Codeium",
        "pricing_type": "Freemium",
        "pricing_details": "Free tier with generous AI credits; Pro tier at $15/mo for advanced agentic flows.",
        "pros": [
            "Innovative 'Flows' architecture blending co-pilot inline edits and multi-file agents",
            "Fast local and cloud codebase indexing",
            "Built-in visual timeline and real-time step execution",
            "Compatible with VS Code extension ecosystem"
        ],
        "cons": [
            "Relatively new tool in active rapid development",
            "Advanced agent features require paid plan credits",
            "Can occasionally suggest overly complex multi-file edits"
        ],
        "target_audience": "Developers seeking autonomous agentic code generation and refactoring.",
        "hero_image": "https://images.unsplash.com/photo-1550745165-9bc0b252726f?w=1200&auto=format&fit=crop&q=80",
        "category": "AI Code Editor"
    },
    {
        "id": "sublime-text",
        "name": "Sublime Text 4",
        "tagline": "Super-fast, sleek text editor for code, markup, and prose.",
        "developer": "Sublime HQ",
        "pricing_type": "Shareware / Commercial",
        "pricing_details": "Free evaluation without time limit; Personal License costs $99 per user.",
        "pros": [
            "Instant startup and lightweight C++ native speed",
            "GPU rendering engine for smooth scrolling and ultra-crisp fonts",
            "Multiple selection editing and powerful command palette",
            "Cross-platform (macOS, Windows, Linux) consistency"
        ],
        "cons": [
            "Periodic evaluation popup prompt on the free version",
            "Fewer built-in features out of the box compared to IDEs (requires Package Control)",
            "Paid license required for continuous commercial use"
        ],
        "target_audience": "Developers who value minimalist interface, instant launch speed, and low memory consumption.",
        "hero_image": "https://images.unsplash.com/photo-1507238691740-187a5b1d37b8?w=1200&auto=format&fit=crop&q=80",
        "category": "Lightweight Code Editor"
    },
    {
        "id": "helix",
        "name": "Helix Editor",
        "tagline": "A post-modern modal text editor written in Rust with built-in LSP and tree-sitter.",
        "developer": "Helix Open Source Community",
        "pricing_type": "Free / Open Source",
        "pricing_details": "100% Free & Open Source (MPL-2.0).",
        "pros": [
            "Zero setup required for syntax highlighting and LSP (selection -> action workflow)",
            "Written in Rust for optimal terminal responsiveness",
            "Built-in tree-sitter textobjects and multi-cursor support out of the box",
            "Clean terminal UI with helpful keybinding discoverability menus"
        ],
        "cons": [
            "Different modal keybinding scheme (selection-first) compared to Vim/Neovim",
            "No plugin architecture by default yet (focus on built-in functionality)",
            "Strictly terminal-focused with no GUI wrapper standard"
        ],
        "target_audience": "Terminal developers wanting LSP capabilities out-of-the-box without complex configuration.",
        "hero_image": "https://images.unsplash.com/photo-1517694712202-14dd9538aa97?w=1200&auto=format&fit=crop&q=80",
        "category": "Modal Text Editor"
    }
]


def generate_amp_html(ide_info: dict) -> str:
    """Generates valid AMP HTML content adhering strictly to Google AMP specs and Blogger formatting."""
    name = ide_info["name"]
    tagline = ide_info["tagline"]
    developer = ide_info["developer"]
    pricing_type = ide_info["pricing_type"]
    pricing_details = ide_info["pricing_details"]
    pros = ide_info["pros"]
    cons = ide_info["cons"]
    target_audience = ide_info["target_audience"]
    hero_image = ide_info["hero_image"]
    category = ide_info.get("category", "Development Environment")

    pros_html = "\n".join([f"      <li><strong>PRO:</strong> {p}</li>" for p in pros])
    cons_html = "\n".join([f"      <li><strong>CON:</strong> {c}</li>" for c in cons])

    html = f"""<!doctype html>
<html ⚡ lang="en">
<head>
  <meta charset="utf-8">
  <title>{name} Review & Guide 2026 - Pros, Cons, and Pricing | IDE Guide</title>
  <link rel="canonical" href="{BLOGGER_URL}posts/{ide_info['id']}.html">
  <meta name="viewport" content="width=device-width,minimum-scale=1,initial-scale=1">
  <script async src="https://cdn.ampproject.org/v0.js"></script>

  <!-- Schema.org Structured Data -->
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "TechArticle",
    "headline": "{name} Review: Features, Pros & Cons, and Developer Breakdown",
    "image": ["{hero_image}"],
    "author": {{
      "@type": "Organization",
      "name": "IDE Guide",
      "url": "{BLOGGER_URL}"
    }},
    "publisher": {{
      "@type": "Organization",
      "name": "IDE Guide",
      "url": "{BLOGGER_URL}"
    }},
    "description": "{tagline}",
    "mainEntityOfPage": "{BLOGGER_URL}"
  }}
  </script>

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
      background: #ffffff;
      box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }}
    header {{
      border-bottom: 2px solid #e2e8f0;
      padding-bottom: 16px;
      margin-bottom: 24px;
    }}
    .badge {{
      display: inline-block;
      background-color: #0284c7;
      color: #ffffff;
      font-size: 12px;
      font-weight: 700;
      padding: 4px 10px;
      border-radius: 9999px;
      text-transform: uppercase;
      letter-spacing: 0.05em;
    }}
    h1 {{
      font-size: 2rem;
      color: #0f172a;
      margin: 12px 0 8px 0;
    }}
    .tagline {{
      font-size: 1.1rem;
      color: #475569;
      font-style: italic;
    }}
    .hero-img {{
      margin: 20px 0;
      border-radius: 8px;
      overflow: hidden;
    }}
    .meta-box {{
      background-color: #f1f5f9;
      border-left: 4px solid #0284c7;
      padding: 16px;
      margin: 20px 0;
      border-radius: 0 8px 8px 0;
    }}
    .meta-item {{
      margin-bottom: 8px;
    }}
    .meta-item:last-child {{
      margin-bottom: 0;
    }}
    h2 {{
      font-size: 1.4rem;
      color: #0f172a;
      border-bottom: 1px solid #cbd5e1;
      padding-bottom: 6px;
      margin-top: 32px;
    }}
    ul.pros-cons {{
      list-style: none;
      padding-left: 0;
    }}
    ul.pros-cons li {{
      padding: 10px 14px;
      margin-bottom: 8px;
      border-radius: 6px;
    }}
    ul.pros li {{
      background-color: #f0fdf4;
      border: 1px solid #bbf7d0;
      color: #166534;
    }}
    ul.cons li {{
      background-color: #fef2f2;
      border: 1px solid #fecaca;
      color: #991b1b;
    }}
    .disclaimer-box {{
      background-color: #fffbe0;
      border: 1px solid #fef08a;
      color: #854d0e;
      padding: 16px;
      border-radius: 8px;
      font-size: 0.9rem;
      margin-top: 40px;
      font-weight: 500;
    }}
    .footer-links {{
      margin-top: 30px;
      padding-top: 16px;
      border-top: 1px solid #e2e8f0;
      text-align: center;
      font-size: 0.95rem;
    }}
    .footer-links a {{
      color: #0284c7;
      text-decoration: none;
      font-weight: 600;
      margin: 0 10px;
    }}
    .footer-links a:hover {{
      text-decoration: underline;
    }}
  </style>
</head>
<body>
  <div class="container">
    <header>
      <span class="badge">{category}</span>
      <h1>{name} Evaluation & Technical Guide</h1>
      <p class="tagline">{tagline}</p>
    </header>

    <div class="hero-img">
      <amp-img src="{hero_image}" width="1200" height="675" layout="responsive" alt="{name} Banner Image"></amp-img>
    </div>

    <div class="meta-box">
      <div class="meta-item"><strong>Developer / Vendor:</strong> {developer}</div>
      <div class="meta-item"><strong>Licensing Model:</strong> {pricing_type}</div>
      <div class="meta-item"><strong>Pricing Breakdown:</strong> {pricing_details}</div>
      <div class="meta-item"><strong>Ideal For:</strong> {target_audience}</div>
    </div>

    <h2>1. Executive Summary & Overview</h2>
    <p>
      In modern software engineering, selecting the right code editor directly impacts developer productivity, memory overhead, and AI-assisted velocity.
      <strong>{name}</strong> stands out in the <strong>{category}</strong> ecosystem. Developed by {developer}, it offers specialized workflows designed to meet contemporary development standards.
    </p>

    <h2>2. Key Strengths (The Good)</h2>
    <ul class="pros-cons pros">
{pros_html}
    </ul>

    <h2>3. Trade-offs & Weaknesses (The Bad)</h2>
    <ul class="pros-cons cons">
{cons_html}
    </ul>

    <h2>4. Pricing & Licensing Breakdown</h2>
    <p>
      Understanding the financial and licensing commitments of your tools is critical:
    </p>
    <p>
      <strong>Model:</strong> {pricing_type}<br>
      <strong>Details:</strong> {pricing_details}
    </p>

    <h2>5. Verdict: Who Should Use {name}?</h2>
    <p>
      <strong>{name}</strong> is best suited for <strong>{target_audience}</strong>. If your daily workflow prioritizes speed, extensibility, and modern tooling, evaluating {name} is highly recommended.
    </p>

    <!-- Mandatory Non-Sponsorship Disclaimer -->
    <div class="disclaimer-box">
      <strong>Independent Review Notice:</strong><br>
      {DISCLAIMER_TEXT}
    </div>

    <div class="footer-links">
      <p>Explore more IDE reviews on <a href="{BLOGGER_URL}">IDE Guide Blog</a> | Subscribe to our <a href="{YOUTUBE_URL}">YouTube Channel (@IDEguide)</a></p>
    </div>
  </div>
</body>
</html>
"""
    return html


def generate_google_flow_spec(ide_info: dict) -> dict:
    """Generates structured Google Flow video specification (for Shorts & Long-Form)."""
    name = ide_info["name"]
    tagline = ide_info["tagline"]
    developer = ide_info["developer"]
    pricing_type = ide_info["pricing_type"]
    target_audience = ide_info["target_audience"]
    pros = ide_info["pros"]
    cons = ide_info["cons"]

    spec = {
        "title": f"{name} - The Ultimate Developer Breakdown | IDE Guide",
        "target_channel": "@IDEguide",
        "ide_name": name,
        "developer": developer,
        "pricing_model": pricing_type,
        "disclaimer": DISCLAIMER_TEXT,
        "formats": {
            "shorts_9_16": {
                "resolution": "1080x1920",
                "target_duration_sec": 50,
                "scenes": [
                    {
                        "scene_id": 1,
                        "time_range": "0-5s",
                        "visual_prompt": f"Macro cinematic close up shot of source code on a glowing monitor in a dark developer studio, camera zooms quickly into {name} logo with blue neon glow, 4k render.",
                        "voiceover": f"Should you be using {name} in 2026? Here is everything you need to know in 60 seconds!",
                        "text_overlay": f"IS {name.upper()} WORTH IT?",
                        "audio": "Upbeat high-tempo electronic pulse beat"
                    },
                    {
                        "scene_id": 2,
                        "time_range": "5-25s",
                        "visual_prompt": f"Split screen visual showing high speed typing in {name} with code autocompletion popups, high tech futuristic UI overlays highlighting key features.",
                        "voiceover": f"Developed by {developer}, {name} offers {pros[0].lower()} and {pros[1].lower()}.",
                        "text_overlay": f"PROS:\n- {pros[0]}\n- {pros[1]}",
                        "audio": "Tech synth rhythm"
                    },
                    {
                        "scene_id": 3,
                        "time_range": "25-40s",
                        "visual_prompt": "Close-up of computer RAM usage gauge rising, dramatic warning pulse animation on dark background.",
                        "voiceover": f"However, keep in mind: {cons[0].lower()}.",
                        "text_overlay": f"CONS:\n- {cons[0]}",
                        "audio": "Bass drop transition"
                    },
                    {
                        "scene_id": 4,
                        "time_range": "40-50s",
                        "visual_prompt": f"Cinematic shot of developer nodding thoughtfully at multi-monitor setup, ending with IDE Guide YouTube banner and Blogger URL badge.",
                        "voiceover": f"Ideal for {target_audience}. Licensing model: {pricing_type}. Subscribe to IDE Guide for daily editor reviews!",
                        "text_overlay": f"Verdict: Great for {target_audience}\nSubscribe @IDEguide",
                        "audio": "Channel outro melody sound"
                    }
                ]
            },
            "long_form_16_9": {
                "resolution": "3840x2160",
                "target_duration_sec": 300,
                "scenes": [
                    {
                        "scene_id": 1,
                        "time_range": "0-30s",
                        "visual_prompt": f"Over the shoulder cinematic camera movement of developer opening {name} on a sleek modern workstation setup with ambient dark lighting.",
                        "voiceover": f"Welcome back to IDE Guide! Today we are conducting an in-depth developer review of {name}. {tagline}",
                        "text_overlay": f"{name} Complete Review - IDE Guide",
                        "audio": "Ambient chill synthwave background music (-18dB)"
                    },
                    {
                        "scene_id": 2,
                        "time_range": "30s-150s",
                        "visual_prompt": f"Smooth screen pan across {name} interface showing syntax highlighting, terminal execution, and key feature workflows.",
                        "voiceover": f"Let us break down the standout features. First, {pros[0]}. Second, {pros[1] if len(pros)>1 else pros[0]}.",
                        "text_overlay": "Key Features & Benchmarks",
                        "audio": "Smooth tech background track"
                    },
                    {
                        "scene_id": 3,
                        "time_range": "150s-240s",
                        "visual_prompt": "Clean side-by-side comparison table showing Pros vs Cons with sleek glowing chart elements.",
                        "voiceover": f"On the trade-offs side: {cons[0]}. Regarding pricing, {ide_info['pricing_details']}.",
                        "text_overlay": "Pros, Cons & Pricing Matrix",
                        "audio": "Analytical subtle rhythm"
                    },
                    {
                        "scene_id": 4,
                        "time_range": "240s-300s",
                        "visual_prompt": "Cinematic studio shot displaying non-sponsorship badge followed by IDE Guide social links.",
                        "voiceover": f"Final Verdict: {name} is an excellent choice for {target_audience}. Remember, IDE Guide is an independent technical publication and is not sponsored by any vendor.",
                        "text_overlay": f"INDEPENDENT REVIEW\nSubscribe @IDEguide | ideguide.blogspot.com",
                        "audio": "Upbeat outro transition track"
                    }
                ]
            }
        }
    }
    return spec


def generate_google_flow_markdown_spec(spec: dict) -> str:
    """Converts a Google Flow spec dictionary to Markdown format for quick human reading and video workflow prompt copying."""
    md = f"""# Google Flow Video Generation Spec: {spec['ide_name']}

**Channel:** {spec['target_channel']}
**Title:** {spec['title']}
**Developer:** {spec['developer']}
**Pricing Model:** {spec['pricing_model']}

---

## Non-Sponsorship Disclaimer
> {spec['disclaimer']}

---

## 1. YouTube Shorts (9:16 Vertical)
- **Resolution:** {spec['formats']['shorts_9_16']['resolution']}
- **Target Duration:** {spec['formats']['shorts_9_16']['target_duration_sec']}s

### Scene Flow & Prompts:
"""
    for s in spec['formats']['shorts_9_16']['scenes']:
        md += f"""
### Scene {s['scene_id']} ({s['time_range']})
- **Google Flow Visual Prompt:** `{s['visual_prompt']}`
- **Voiceover Script:** "{s['voiceover']}"
- **Text Overlay:** `{s['text_overlay']}`
- **Audio/SFX:** {s['audio']}
"""

    md += f"""
---

## 2. Long-Form Video (16:9 4K)
- **Resolution:** {spec['formats']['long_form_16_9']['resolution']}
- **Target Duration:** {spec['formats']['long_form_16_9']['target_duration_sec']}s

### Scene Flow & Prompts:
"""
    for s in spec['formats']['long_form_16_9']['scenes']:
        md += f"""
### Scene {s['scene_id']} ({s['time_range']})
- **Google Flow Visual Prompt:** `{s['visual_prompt']}`
- **Voiceover Script:** "{s['voiceover']}"
- **Text Overlay:** `{s['text_overlay']}`
- **Audio/SFX:** {s['audio']}
"""
    return md


def run_daily_generation(output_base_dir="content", count=3):
    """Executes daily generation for count IDEs, updating history.json."""
    today_str = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d")
    target_dir = os.path.join(output_base_dir, today_str)
    os.makedirs(target_dir, exist_ok=True)

    history_file = os.path.join(output_base_dir, "history.json")
    history = []
    if os.path.exists(history_file):
        try:
            with open(history_file, "r", encoding="utf-8") as f:
                history = json.load(f)
        except Exception:
            history = []

    # Pick count IDEs not in recent history, or cycle back if exhausted
    covered_ids = set(item.get("id") for item in history)
    available = [ide for ide in IDE_DATABASE if ide["id"] not in covered_ids]

    if len(available) < count:
        # Reset cycle if needed
        available = IDE_DATABASE

    selected = available[:count]
    generated_files = []

    for ide in selected:
        ide_id = ide["id"]

        # 1. Generate AMP HTML blog post
        amp_html = generate_amp_html(ide)
        amp_path = os.path.join(target_dir, f"blog_post_{ide_id}.html")
        with open(amp_path, "w", encoding="utf-8") as f:
            f.write(amp_html)
        generated_files.append(amp_path)

        # 2. Generate Google Flow Video Spec (JSON & MD)
        spec_dict = generate_google_flow_spec(ide)
        spec_json_path = os.path.join(target_dir, f"video_spec_{ide_id}.json")
        with open(spec_json_path, "w", encoding="utf-8") as f:
            json.dump(spec_dict, f, indent=2)
        generated_files.append(spec_json_path)

        spec_md = generate_google_flow_markdown_spec(spec_dict)
        spec_md_path = os.path.join(target_dir, f"video_spec_{ide_id}.md")
        with open(spec_md_path, "w", encoding="utf-8") as f:
            f.write(spec_md)
        generated_files.append(spec_md_path)

        # Record history
        history.append({
            "id": ide_id,
            "name": ide["name"],
            "date": today_str
        })

    with open(history_file, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=2)

    print(f"Successfully generated {len(selected)} IDE packages in {target_dir}")
    return generated_files


if __name__ == "__main__":
    run_daily_generation()
