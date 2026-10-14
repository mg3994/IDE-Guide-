#!/usr/bin/env python3
import os
import sys
import json
import datetime
import re
from pathlib import Path

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from scripts.amp_validator import validate_amp_html, REQUIRED_DISCLAIMER

IDE_POOL = [
    {
        "name": "Cursor",
        "slug": "cursor",
        "tagline": "AI-First Code Editor Built on VS Code",
        "pricing": "Freemium ($20/mo Pro plan)",
        "pros": ["Built-in AI model integration (Claude 3.5, GPT-4o)", "Seamless VS Code extension compatibility", "AI Codebase indexing & multi-file editing"],
        "cons": ["Subscription costs for high API usage", "Requires internet connection for AI features", "Closed-source proprietary extensions"],
        "best_for": "Developers wanting maximum AI coding productivity and automated code generation.",
        "category": "AI Editor"
    },
    {
        "name": "VS Code",
        "slug": "vscode",
        "tagline": "Extensible, Lightweight, and Ubiquitous Code Editor",
        "pricing": "100% Free & Open Source (Core)",
        "pros": ["Massive extension ecosystem", "Cross-platform support with top performance", "Integrated terminal, debugging, and Git control"],
        "cons": ["Requires setup and extensions for full IDE features", "High memory usage with heavy extension stacks", "Telemetry enabled by default"],
        "best_for": "Generalists, web developers, and teams looking for a versatile and free editor.",
        "category": "General Purpose Editor"
    },
    {
        "name": "PyCharm",
        "slug": "pycharm",
        "tagline": "The Intelligent Python IDE by JetBrains",
        "pricing": "Freemium (Community Free / Professional Paid)",
        "pros": ["Unmatched Python auto-completion and refactoring", "Built-in Django, Flask, database & web tools", "Integrated scientific & notebook tooling"],
        "cons": ["Heavy memory usage", "Slower startup time compared to lightweight editors", "Advanced web features locked behind paid tier"],
        "best_for": "Professional Python, Django, and Data Science engineers.",
        "category": "Language-Specific IDE"
    },
    {
        "name": "Neovim",
        "slug": "neovim",
        "tagline": "Hyperextensible Vim-based Text Editor",
        "pricing": "100% Free & Open Source",
        "pros": ["Blazing fast terminal performance", "Lua plugin ecosystem with infinite customization", "Minimal resource footprint"],
        "cons": ["Steep learning curve for keybindings and config", "Requires manual setup for LSP and debugging", "No out-of-the-box GUI"],
        "best_for": "Power users, terminal enthusiasts, and developers who love total workflow customization.",
        "category": "Terminal Editor"
    },
    {
        "name": "IntelliJ IDEA",
        "slug": "intellij-idea",
        "tagline": "The Premier Java & JVM Enterprise IDE",
        "pricing": "Freemium (Community Free / Ultimate Paid)",
        "pros": ["Industry-standard Java refactoring and code analysis", "Deep Framework support (Spring, Kotlin, Java EE)", "Robust build system and database integration"],
        "cons": ["Resource intensive (high RAM footprint)", "Ultimate edition required for full enterprise features", "Complex settings UI"],
        "best_for": "Enterprise Java, Kotlin, and Scala backend engineers.",
        "category": "Enterprise IDE"
    },
    {
        "name": "Zed",
        "slug": "zed",
        "tagline": "High-Performance Multi-Buffer Code Editor Built in Rust",
        "pricing": "100% Free & Open Source",
        "pros": ["Ultra-fast GPU-accelerated rendering", "Native multi-player real-time collaboration", "Low CPU and memory usage"],
        "cons": ["Young ecosystem compared to VS Code", "Fewer extensions currently available", "Linux/Windows support still maturing"],
        "best_for": "Performance purists, Rust enthusiasts, and pair-programming teams.",
        "category": "Next-Gen Editor"
    },
    {
        "name": "Fleet",
        "slug": "fleet",
        "tagline": "Lightweight Polyglot Editor & Distributed IDE by JetBrains",
        "pricing": "Freemium",
        "pros": ["Instant startup with optional smart backend", "Clean minimalist modern UI", "Seamless remote & cloud development"],
        "cons": ["Still in preview/early adoption phase", "Plugin ecosystem in active development", "Lacks some legacy JetBrains depth"],
        "best_for": "Developers desiring JetBrains intelligence in a fast, lightweight footprint.",
        "category": "Polyglot IDE"
    },
    {
        "name": "Sublime Text",
        "slug": "sublime-text",
        "tagline": "Sophisticated Text Editor for Code, Markup and Prose",
        "pricing": "Paid ($99 evaluation license)",
        "pros": ["Lightning fast file opening and fuzzy search", "GPU rendering for silky 60fps scrolling", "Python API for plugin scripting"],
        "cons": ["Paid license required for continuous use", "Lacks out-of-the-box full IDE features", "Smaller plugin ecosystem than VS Code"],
        "best_for": "Developers who value instant file navigation and extreme speed.",
        "category": "Lightweight Editor"
    },
    {
        "name": "WebStorm",
        "slug": "webstorm",
        "tagline": "The Smartest JavaScript & TypeScript IDE",
        "pricing": "Paid (Subscription)",
        "pros": ["Best-in-class JavaScript, React, Vue, & Angular support", "Integrated testing, debugging, and Git UI", "Refactoring across massive frontend codebases"],
        "cons": ["No free community tier (paid subscription only)", "Can be heavy for single-file edits", "Slower startup than VS Code"],
        "best_for": "Frontend and full-stack JavaScript/TypeScript specialists.",
        "category": "Frontend IDE"
    }
]

def generate_amp_blog_post(ide: dict) -> str:
    html = f"""<!doctype html>
<html ⚡ lang="en">
<head>
  <meta charset="utf-8">
  <title>{ide['name']} Review & Complete Guide - IDE Guide</title>
  <link rel="canonical" href="https://ideguide.blogspot.com/reviews/{ide['slug']}.html">
  <meta name="viewport" content="width=device-width,minimum-scale=1,initial-scale=1">
  <style amp-boilerplate>body{{-webkit-animation:-amp-start 8s steps(1,end) 0s 1 normal both;-moz-animation:-amp-start 8s steps(1,end) 0s 1 normal both;-ms-animation:-amp-start 8s steps(1,end) 0s 1 normal both;animation:-amp-start 8s steps(1,end) 0s 1 normal both}}@-webkit-keyframes -amp-start{{from{{visibility:hidden}}to{{visibility:visible}}}}@-moz-keyframes -amp-start{{from{{visibility:hidden}}to{{visibility:visible}}}}@-ms-keyframes -amp-start{{from{{visibility:hidden}}to{{visibility:visible}}}}@-o-keyframes -amp-start{{from{{visibility:hidden}}to{{visibility:visible}}}}@keyframes -amp-start{{from{{visibility:hidden}}to{{visibility:visible}}}}</style><noscript><style amp-boilerplate>body{{-webkit-animation:none;-moz-animation:none;-ms-animation:none;animation:none}}</style></noscript>
  <script async src="https://cdn.ampproject.org/v0.js"></script>
  <style amp-custom>
    body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; line-height: 1.6; color: #1e293b; background: #f8fafc; padding: 16px; max-width: 800px; margin: 0 auto; }}
    header {{ background: #0f172a; color: #fff; padding: 24px; border-radius: 12px; margin-bottom: 24px; text-align: center; }}
    h1 {{ margin: 0 0 8px 0; font-size: 28px; font-weight: 800; }}
    .tagline {{ color: #94a3b8; font-size: 16px; font-style: italic; }}
    .badge {{ display: inline-block; background: #3b82f6; color: white; padding: 4px 12px; border-radius: 9999px; font-size: 13px; font-weight: 600; margin-top: 10px; }}
    .card {{ background: white; border: 1px solid #e2e8f0; border-radius: 12px; padding: 20px; margin-bottom: 20px; box-shadow: 0 1px 3px rgba(0,0,0,0.05); }}
    .pros-cons {{ display: flex; flex-wrap: wrap; gap: 16px; margin-bottom: 20px; }}
    .pro-box, .con-box {{ flex: 1 1 300px; padding: 16px; border-radius: 8px; }}
    .pro-box {{ background: #f0fdf4; border: 1px solid #bbf7d0; color: #166534; }}
    .con-box {{ background: #fef2f2; border: 1px solid #fecaca; color: #991b1b; }}
    ul {{ padding-left: 20px; margin: 8px 0; }}
    .disclaimer {{ background: #f1f5f9; border-left: 4px solid #64748b; padding: 16px; font-size: 13px; color: #475569; margin-top: 32px; border-radius: 4px; }}
  </style>
</head>
<body>
  <header>
    <h1>{ide['name']} Guide & Review</h1>
    <div class="tagline">{ide['tagline']}</div>
    <span class="badge">{ide['category']}</span>
  </header>

  <article>
    <div class="card">
      <h2>Overview & Architecture</h2>
      <p>Welcome to <strong>IDE Guide</strong>'s breakdown of <strong>{ide['name']}</strong>. Finding the right code editor is critical for developer velocity, code accuracy, and daily workflow comfort.</p>
      <amp-img src="https://images.unsplash.com/photo-1555066931-4365d14bab8c" width="800" height="450" layout="responsive" alt="{ide['name']} Workspace Banner"></amp-img>
      <p><strong>Pricing Model:</strong> {ide['pricing']}</p>
    </div>

    <div class="pros-cons">
      <div class="pro-box">
        <h3>The Good (Pros)</h3>
        <ul>
          {"".join([f"<li>{pro}</li>" for pro in ide['pros']])}
        </ul>
      </div>
      <div class="con-box">
        <h3>The Bad (Cons)</h3>
        <ul>
          {"".join([f"<li>{con}</li>" for con in ide['cons']])}
        </ul>
      </div>
    </div>

    <div class="card">
      <h2>Best For & Verdict</h2>
      <p>{ide['best_for']}</p>
    </div>

    <div class="disclaimer">
      {REQUIRED_DISCLAIMER}
    </div>
  </article>
</body>
</html>"""

    is_valid, errors = validate_amp_html(html)
    if not is_valid:
        raise ValueError(f"Generated AMP HTML for {ide['name']} failed validation: {errors}")
    return html

def generate_video_spec(ide: dict) -> dict:
    return {
        "channel": "@IDEguide",
        "video_title": f"{ide['name']} in 60 Seconds: Pros, Cons, and Verdict!",
        "target_platform": "YouTube Shorts / Google Flow AI Video",
        "aspect_ratio": "9:16",
        "duration_seconds": 60,
        "ide_metadata": {
            "name": ide['name'],
            "pricing": ide['pricing'],
            "category": ide['category']
        },
        "prompts": [
            {
                "scene_id": 1,
                "timeframe": "0-10s",
                "visual_prompt": f"Close-up high-tech macro shot of code syntax on dark screen inside {ide['name']} editor interface. Dramatic blue and neon purple rim light. Cinematic slow zoom in.",
                "audio_script": f"Are you thinking about switching to {ide['name']}? Here is what you need to know in 60 seconds!",
                "on_screen_text": f"{ide['name']}: Ultimate Guide"
            },
            {
                "scene_id": 2,
                "timeframe": "10-25s",
                "visual_prompt": f"Smooth screen recording animation showcasing key feature of {ide['name']}. Clean developer desk with mechanical keyboard in foreground.",
                "audio_script": f"The Good: {ide['pros'][0]}, and {ide['pros'][1]}.",
                "on_screen_text": f"PROS: {ide['pros'][0]}"
            },
            {
                "scene_id": 3,
                "timeframe": "25-40s",
                "visual_prompt": "Red subtle glow accent light focusing on developer terminal window with speed test comparison graphics.",
                "audio_script": f"The Bad: Keep in mind that {ide['cons'][0]}.",
                "on_screen_text": f"CONS: {ide['cons'][0]}"
            },
            {
                "scene_id": 4,
                "timeframe": "40-55s",
                "visual_prompt": "Split screen showing pricing badge and developer typing smoothly at high speed.",
                "audio_script": f"Pricing model is {ide['pricing']}. Best for: {ide['best_for']}",
                "on_screen_text": f"Pricing: {ide['pricing']}"
            },
            {
                "scene_id": 5,
                "timeframe": "55-60s",
                "visual_prompt": "IDE Guide logo animation with YouTube subscribe prompt overlay.",
                "audio_script": "Subscribe to IDE Guide for daily objective editor reviews!",
                "on_screen_text": "Subscribe to @IDEguide"
            }
        ],
        "disclaimer": REQUIRED_DISCLAIMER
    }

def generate_video_spec_markdown(spec: dict) -> str:
    md = f"""# Google Flow Video Generation Spec: {spec['ide_metadata']['name']}

**Channel**: {spec['channel']}
**Target Platform**: {spec['target_platform']} ({spec['aspect_ratio']})
**Pricing**: {spec['ide_metadata']['pricing']}

## Video Script & Scene Prompts

"""
    for prompt in spec['prompts']:
        md += f"""### Scene {prompt['scene_id']} ({prompt['timeframe']})
- **Visual Prompt**: {prompt['visual_prompt']}
- **Audio Script**: {prompt['audio_script']}
- **On-Screen Text**: {prompt['on_screen_text']}

"""

    md += f"""## Non-Sponsorship Disclaimer

{spec['disclaimer']}
"""
    return md

def main():
    date_str = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d")
    out_dir = PROJECT_ROOT / "content" / date_str
    out_dir.mkdir(parents=True, exist_ok=True)

    history_file = PROJECT_ROOT / "content" / "history.json"
    covered_ides = []
    if history_file.exists():
        try:
            with open(history_file, 'r', encoding='utf-8') as f:
                history_data = json.load(f)
                covered_ides = history_data.get("covered_ides", [])
        except Exception:
            covered_ides = []

    # Pick 3 uncovered IDEs
    uncovered = [ide for ide in IDE_POOL if ide['slug'] not in covered_ides]
    if len(uncovered) < 3:
        # Reset cycle if all pool items used
        covered_ides = []
        uncovered = IDE_POOL

    selected = uncovered[:3]

    generated_files = []
    for ide in selected:
        slug = ide['slug']

        # 1. AMP Blog Post
        amp_html = generate_amp_blog_post(ide)
        blog_post_path = out_dir / f"blog_post_{slug}.amp.html"
        with open(blog_post_path, 'w', encoding='utf-8') as f:
            f.write(amp_html)
        generated_files.append(blog_post_path)

        # 2. Google Flow Video Spec (JSON)
        spec = generate_video_spec(ide)
        spec_path = out_dir / f"video_spec_{slug}.json"
        with open(spec_path, 'w', encoding='utf-8') as f:
            json.dump(spec, f, indent=2)
        generated_files.append(spec_path)

        # 3. Google Flow Video Spec (Markdown)
        spec_md = generate_video_spec_markdown(spec)
        spec_md_path = out_dir / f"video_spec_{slug}.md"
        with open(spec_md_path, 'w', encoding='utf-8') as f:
            f.write(spec_md)
        generated_files.append(spec_md_path)

        covered_ides.append(slug)

    # Update history
    with open(history_file, 'w', encoding='utf-8') as f:
        json.dump({
            "covered_ides": covered_ides,
            "last_updated": datetime.datetime.now(datetime.timezone.utc).isoformat()
        }, f, indent=2)

    print(f"Successfully generated 3 daily content packages in '{out_dir}':")
    for filepath in generated_files:
        print(f"  - {filepath.relative_to(PROJECT_ROOT)}")

if __name__ == "__main__":
    main()
