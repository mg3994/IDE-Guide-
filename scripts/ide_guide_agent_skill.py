#!/usr/bin/env python3
"""
Agentic Skill Tool for IDE Guide (@IDEguide & ideguide.blogspot.com).
Generates on-demand AMP HTML Blog Posts and Google Flow Video Specs for given IDEs or GitHub Repository URLs.
"""

import argparse
import json
import os
import re
import sys
from typing import Dict, Any

# Ensure parent path is in sys.path so script can be run directly or via module imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from scripts.amp_validator import NON_SPONSORSHIP_DISCLAIMER, validate_amp_html

# Database of known IDEs with metadata for accurate agentic generation
IDE_DATABASE: Dict[str, Dict[str, Any]] = {
    "VS Code": {
        "full_name": "Visual Studio Code",
        "developer": "Microsoft",
        "pricing": "Free & Open Source (MIT License for core, proprietary build binaries)",
        "paid_tier": "Free for personal & commercial use. Optional Azure integration subscriptions.",
        "pros": ["Massive extension marketplace", "Ubiquitous adoption & community support", "Rich debugging & remote development features"],
        "cons": ["Electron-based memory overhead", "Telemetry enabled by default"],
        "target_audience": "All developers, from beginners to full-stack web and cloud engineers.",
        "key_features": ["IntelliSense auto-complete", "Built-in Git & terminal", "Extension Ecosystem", "Remote - SSH & Containers"]
    },
    "Cursor": {
        "full_name": "Cursor AI Code Editor",
        "developer": "Anysphere",
        "pricing": "Freemium (Free hobby tier with limits, Pro at $20/month)",
        "paid_tier": "$20/mo Pro plan for unlimited fast Claude-3.5 Sonnet & GPT-4o usage.",
        "pros": ["Native AI codebase indexing", "Multi-file edit capabilities (Composer)", "VS Code extension compatibility"],
        "cons": ["Closed-source paid subscription required for heavy AI use", "Occasional visual lag on massive repos"],
        "target_audience": "Developers looking for deep AI-native productivity and multi-file code generation.",
        "key_features": ["Cmd+K Code Generation", "Codebase RAG Indexing", "Cursor Composer", "Instant Terminal Debugging"]
    },
    "Zed": {
        "full_name": "Zed Editor",
        "developer": "Zed Industries",
        "pricing": "Free & Open Source (GPL for editor, AGPL for server components)",
        "paid_tier": "100% Free for local editor; paid cloud collaboration tiers for teams.",
        "pros": ["Blazing-fast GPU-accelerated rendering in Rust", "Sub-millisecond startup & low RAM consumption", "Built-in multiplayer pair programming"],
        "cons": ["Ecosystem is newer compared to VS Code", "Fewer extensions currently available"],
        "target_audience": "Performance enthusiasts, Rust developers, and developers seeking ultra-fast editing.",
        "key_features": ["GPU-accelerated metal rendering", "Native Rust performance", "CRDT multiplayer collaboration", "Integrated AI assistance"]
    },
    "PyCharm": {
        "full_name": "PyCharm IDE",
        "developer": "JetBrains",
        "pricing": "Freemium (Community Edition: Free; Professional Edition: $249/year or $24.90/month)",
        "paid_tier": "Professional Edition includes SQL database support, Django/Web frameworks, and scientific tools.",
        "pros": ["Industry-standard Python refactoring & navigation", "Deep integration with virtual environments & Django", "Powerful built-in debugger & profiler"],
        "cons": ["Resource intensive (JVM memory footprint)", "Longer initial indexing times on huge projects"],
        "target_audience": "Python software engineers, Django developers, and Data Scientists.",
        "key_features": ["Deep Python code analysis", "Django/Flask web tools", "Integrated database viewer", "Scientific NumPy/Pandas support"]
    },
    "Neovim": {
        "full_name": "Neovim",
        "developer": "Community-driven",
        "pricing": "100% Free & Open Source (Apache / Vim License)",
        "paid_tier": "Completely free.",
        "pros": ["Extremely lightweight and lighting fast", "Infinite customization via Lua scripts", "Keyboard-driven modal efficiency"],
        "cons": ["Steep learning curve", "Requires time & setup for full IDE functionality"],
        "target_audience": "Terminal purists, power users, and engineers who love modal editing.",
        "key_features": ["Built-in LSP client", "Lua configuration engine", "Treesitter syntax highlighting", "Asynchronous plugin host"]
    },
    "Fleet": {
        "full_name": "JetBrains Fleet",
        "developer": "JetBrains",
        "pricing": "Freemium (Free preview tier, JetBrains All Products Pack)",
        "paid_tier": "Included in JetBrains subscription plans for commercial use.",
        "pros": ["Lightweight polyglot editor with Smart Mode switch", "Sleek modern minimal UI", "Distributed architecture for remote dev"],
        "cons": ["Plugin ecosystem still maturing", "Requires Smart Mode for full IDE features"],
        "target_audience": "Developers who want JetBrains smarts without the heavyweight IDE UI.",
        "key_features": ["Smart Mode code intelligence", "Collaborative editing", "Multi-language support", "Distributed dev architecture"]
    }
}


def get_ide_info(ide_name_or_url: str) -> Dict[str, Any]:
    """Retrieves or builds metadata for a given IDE name or repository URL."""
    # Check exact/fuzzy match in database
    for key, data in IDE_DATABASE.items():
        if key.lower() in ide_name_or_url.lower() or ide_name_or_url.lower() in key.lower():
            return data

    # Extract name from URL if repository provided
    clean_name = ide_name_or_url.rstrip('/').split('/')[-1].replace('-', ' ').title()
    if clean_name.lower().endswith('.git'):
        clean_name = clean_name[:-4]

    return {
        "full_name": clean_name,
        "developer": "Open Source / Independent Developer",
        "pricing": "Free & Open Source",
        "paid_tier": "Free for general software development.",
        "pros": ["Modern lightweight architecture", "Community driven development", "High flexibility"],
        "cons": ["Smaller plugin ecosystem", "May require custom setup"],
        "target_audience": "Developers interested in exploring modern specialized coding tools.",
        "key_features": ["Syntax highlighting", "Fast startup time", "Custom configuration options", "Cross-platform support"]
    }


def generate_amp_blog_post(ide_info: Dict[str, Any], canonical_url: str = "https://ideguide.blogspot.com/") -> str:
    """Generates a fully compliant AMP HTML blog post string."""
    title = f"{ide_info['full_name']} in 2025: Features, Performance & Developer Guide"
    pros_html = "".join([f"<li>{p}</li>" for p in ide_info['pros']])
    cons_html = "".join([f"<li>{c}</li>" for c in ide_info['cons']])
    features_html = "".join([f"<li><strong>{f.split(':')[0]}:</strong> {f}</li>" for f in ide_info['key_features']])

    amp_html = f"""<!doctype html>
<html ⚡ lang="en">
<head>
  <meta charset="utf-8">
  <title>{title}</title>
  <link rel="canonical" href="{canonical_url}">
  <meta name="viewport" content="width=device-width,minimum-scale=1,initial-scale=1">
  <script async src="https://cdn.ampproject.org/v0.js"></script>
  <style amp-boilerplate>body{{-webkit-animation:-amp-start 8s steps(1,end) 0s 1 normal both;-moz-animation:-amp-start 8s steps(1,end) 0s 1 normal both;-ms-animation:-amp-start 8s steps(1,end) 0s 1 normal both;animation:-amp-start 8s steps(1,end) 0s 1 normal both}}@-webkit-keyframes -amp-start{{from{{visibility:hidden}}to{{visibility:visible}}}}@-moz-keyframes -amp-start{{from{{visibility:hidden}}to{{visibility:visible}}}}@-ms-keyframes -amp-start{{from{{visibility:hidden}}to{{visibility:visible}}}}@-o-keyframes -amp-start{{from{{visibility:hidden}}to{{visibility:visible}}}}@keyframes -amp-start{{from{{visibility:hidden}}to{{visibility:visible}}}}</style><noscript><style amp-boilerplate>body{{-webkit-animation:none;-moz-animation:none;-ms-animation:none;animation:none}}</style></noscript>
  <style amp-custom>
    body {{
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
      line-height: 1.6;
      color: #24292e;
      max-width: 800px;
      margin: 0 auto;
      padding: 16px;
      background-color: #f6f8fa;
    }}
    .article-header {{
      background-color: #0d1117;
      color: #58a6ff;
      padding: 24px;
      border-radius: 8px;
      margin-bottom: 24px;
    }}
    .article-header h1 {{
      margin: 0 0 8px 0;
      font-size: 1.8rem;
    }}
    .tag {{
      display: inline-block;
      background-color: #238636;
      color: #ffffff;
      padding: 4px 8px;
      border-radius: 4px;
      font-size: 0.85rem;
      font-weight: bold;
    }}
    .section-card {{
      background: #ffffff;
      padding: 20px;
      border-radius: 8px;
      border: 1px solid #e1e4e8;
      margin-bottom: 20px;
    }}
    .section-title {{
      color: #0969da;
      border-bottom: 2px solid #eaecef;
      padding-bottom: 8px;
      margin-top: 0;
    }}
    .grid {{
      display: flex;
      flex-wrap: wrap;
      gap: 16px;
    }}
    .col {{
      flex: 1;
      min-width: 280px;
    }}
    .pro-box {{ background-color: #dafbe1; padding: 12px; border-radius: 6px; border-left: 4px solid #1a7f37; }}
    .con-box {{ background-color: #ffebe9; padding: 12px; border-radius: 6px; border-left: 4px solid #cf222e; }}
    .disclaimer-box {{
      background-color: #fff8c5;
      border: 1px solid #d4a72c;
      padding: 16px;
      border-radius: 6px;
      font-size: 0.9rem;
      color: #4c3e09;
      margin-top: 30px;
    }}
  </style>
</head>
<body>
  <div class="article-header">
    <span class="tag">IDE REVIEW & GUIDE</span>
    <h1>{title}</h1>
    <p>Developer: <strong>{ide_info['developer']}</strong> | Pricing: <strong>{ide_info['pricing']}</strong></p>
  </div>

  <div class="section-card">
    <h2 class="section-title">Overview & Pricing Guidance</h2>
    <p><strong>{ide_info['full_name']}</strong> is evaluated based on performance, memory usage, AI support, and productivity tools.</p>
    <p><strong>Pricing & License:</strong> {ide_info['pricing']}. {ide_info['paid_tier']}</p>
  </div>

  <div class="section-card">
    <h2 class="section-title">Key Features</h2>
    <ul>
      {features_html}
    </ul>
  </div>

  <div class="section-card">
    <h2 class="section-title">Pros & Cons Evaluation</h2>
    <div class="grid">
      <div class="col pro-box">
        <h3>Good (Pros)</h3>
        <ul>
          {pros_html}
        </ul>
      </div>
      <div class="col con-box">
        <h3>Bad (Cons)</h3>
        <ul>
          {cons_html}
        </ul>
      </div>
    </div>
  </div>

  <div class="section-card">
    <h2 class="section-title">Target Audience & Recommendation</h2>
    <p>{ide_info['target_audience']}</p>
  </div>

  <div class="disclaimer-box">
    <strong>{NON_SPONSORSHIP_DISCLAIMER}</strong>
  </div>
</body>
</html>"""
    return amp_html


def generate_google_flow_spec(ide_info: Dict[str, Any]) -> Dict[str, Any]:
    """Generates Google Flow AI video prompt specification structure."""
    video_title = f"{ide_info['full_name']} Review: Is it Worth Using in 2025?"

    return {
        "channel": "@IDEguide",
        "video_title": video_title,
        "target_ide": ide_info['full_name'],
        "developer": ide_info['developer'],
        "pricing_summary": ide_info['pricing'],
        "formats": {
            "youtube_shorts": {
                "aspect_ratio": "9:16",
                "target_duration_seconds": 45,
                "scenes": [
                    {
                        "scene_number": 1,
                        "duration_sec": 5,
                        "visual_prompt": f"Cinematic camera tilt, dark setup studio with neon blue backlighting, close-up code editor showing {ide_info['full_name']} interface with glowing cursor, 4K resolution.",
                        "voiceover_script": f"Looking for your next code editor? Here is everything you need to know about {ide_info['full_name']}.",
                        "on_screen_text": f"{ide_info['full_name']} Review"
                    },
                    {
                        "scene_number": 2,
                        "duration_sec": 15,
                        "visual_prompt": "Ultra-fast dynamic zoom into code auto-completion and key feature demonstration on dual 4K monitors.",
                        "voiceover_script": f"Top feature: {ide_info['key_features'][0]}. Plus, {ide_info['pros'][0]}.",
                        "on_screen_text": f"Pros: {ide_info['pros'][0]}"
                    },
                    {
                        "scene_number": 3,
                        "duration_sec": 15,
                        "visual_prompt": "Macro shot of telemetry memory performance chart and trade-off comparison graphics.",
                        "voiceover_script": f"Pricing is {ide_info['pricing']}. But watch out for: {ide_info['cons'][0]}.",
                        "on_screen_text": f"Pricing: {ide_info['pricing']}"
                    },
                    {
                        "scene_number": 4,
                        "duration_sec": 10,
                        "visual_prompt": "Wide cinematic tracking shot of clean desk workstation with IDE Guide logo overlay.",
                        "voiceover_script": f"Best for: {ide_info['target_audience']} Subscribe to IDE Guide for more technical editor guides!",
                        "on_screen_text": "Subscribe to @IDEguide"
                    }
                ]
            },
            "youtube_longform": {
                "aspect_ratio": "16:9",
                "target_duration_seconds": 240,
                "scenes": [
                    {
                        "scene_number": 1,
                        "duration_sec": 30,
                        "visual_prompt": f"Cinematic wide angle shot of a modern dark-themed developer workstation displaying {ide_info['full_name']} open with syntax highlighted code, soft rim light, cyberpunk aesthetics.",
                        "voiceover_script": f"Welcome back to IDE Guide. Today we are conducting a deep-dive technical evaluation of {ide_info['full_name']}.",
                        "on_screen_text": f"IDE Guide: {ide_info['full_name']} Deep Dive"
                    },
                    {
                        "scene_number": 2,
                        "duration_sec": 90,
                        "visual_prompt": "Over-the-shoulder camera view of real-time coding session, demonstrating key features, terminal execution, and extension usage.",
                        "voiceover_script": f"Let's break down the core features: {', '.join(ide_info['key_features'])}.",
                        "on_screen_text": "Key Features & Real-Time Performance"
                    },
                    {
                        "scene_number": 3,
                        "duration_sec": 90,
                        "visual_prompt": "Side-by-side comparative graphics showing performance metrics, RAM allocation, and pricing breakdown.",
                        "voiceover_script": f"In terms of pricing, {ide_info['pricing']}. Here is how it compares to other editors on the market.",
                        "on_screen_text": "Pricing & Performance Comparison"
                    },
                    {
                        "scene_number": 4,
                        "duration_sec": 30,
                        "visual_prompt": "Cinematic outro with neon glow effects, channel social handles, and disclaimers.",
                        "voiceover_script": "That wraps up our assessment. Check the link in description for our full AMP blog review on ideguide.blogspot.com.",
                        "on_screen_text": "ideguide.blogspot.com | @IDEguide"
                    }
                ]
            }
        },
        "disclaimer": "Disclaimer: IDE Guide is an independent technical publication. This content is not sponsored, endorsed, or affiliated with any software vendor or editor developer mentioned above. All reviews and assessments are based strictly on objective developer evaluation."
    }


def main():
    parser = argparse.ArgumentParser(description="Agentic CLI Skill Tool for IDE Guide (@IDEguide & ideguide.blogspot.com)")
    parser.add_argument("--ide", type=str, required=True, help="IDE Name or GitHub Repository URL (e.g., 'VS Code', 'Cursor', 'https://github.com/zed-industries/zed')")
    parser.add_argument("--outdir", type=str, default="output", help="Directory to save generated AMP blog HTML and Google Flow JSON spec")

    args = parser.parse_args()

    os.makedirs(args.outdir, exist_ok=True)
    ide_info = get_ide_info(args.ide)

    # 1. Generate AMP Blog Post
    amp_content = generate_amp_blog_post(ide_info)
    is_valid, amp_errors = validate_amp_html(amp_content)
    if not is_valid:
        print(f"⚠️ AMP Validation warning for {ide_info['full_name']}: {amp_errors}", file=sys.stderr)

    safe_filename = re.sub(r'[^a-zA-Z0-9_-]', '_', ide_info['full_name'].lower())
    blog_filename = os.path.join(args.outdir, f"blog_{safe_filename}.html")
    with open(blog_filename, 'w', encoding='utf-8') as f:
        f.write(amp_content)

    # 2. Generate Google Flow Spec
    flow_spec = generate_google_flow_spec(ide_info)
    spec_filename = os.path.join(args.outdir, f"flow_spec_{safe_filename}.json")
    with open(spec_filename, 'w', encoding='utf-8') as f:
        json.dump(flow_spec, f, indent=2)

    print(f"✅ Generated AMP Blog Post: {blog_filename} (AMP Valid: {is_valid})")
    print(f"✅ Generated Google Flow Spec: {spec_filename}")


if __name__ == "__main__":
    main()
