#!/usr/bin/env python3
"""
IDE Guide Agentic Skill CLI tool.
Generates AMP HTML blog posts and Google Flow video specs for any target IDE or repository.
"""

import argparse
import json
import os
import sys
from typing import Dict, Any

from scripts.amp_validator import validate_amp_html, DISCLAIMER_TEXT

# Built-in dataset for IDE knowledge
DEFAULT_IDE_KNOWLEDGE: Dict[str, Dict[str, Any]] = {
    "VS Code": {
        "category": "General Code Editor",
        "pricing": "Free (Open Source / MIT License)",
        "summary": "The world's most popular lightweight, extensible code editor with massive extension ecosystem.",
        "pros": ["Massive marketplace", "Lightweight & responsive", "Integrated terminal & Git", "Cross-platform"],
        "cons": ["Electron resource consumption with heavy plugins", "Requires configuration for full IDE features"],
        "best_for": "Web, Node.js, Python, and multi-language software engineers"
    },
    "Cursor": {
        "category": "AI-Native IDE",
        "pricing": "Freemium (Free tier available, $20/mo Pro)",
        "summary": "An AI-first code editor fork of VS Code with deeply integrated AI codebase context and instant edits.",
        "pros": ["Superior multi-file AI context indexing", "Composer agent mode for building features", "VS Code extension compatibility"],
        "cons": ["Usage caps on expensive AI models", "Proprietary backend server dependencies"],
        "best_for": "Developers seeking maximum AI-assisted velocity and rapid prototyping"
    },
    "Windsurf": {
        "category": "AI Flow IDE",
        "pricing": "Freemium (Free tier available, $15/mo Pro)",
        "summary": "Codeium's next-generation AI editor featuring Cascade flow state and deep codebase understanding.",
        "pros": ["Cascade contextual AI assistant", "Blazing fast real-time autocompletion", "Seamless VS Code keybinding support"],
        "cons": ["Relatively new ecosystem", "Pro tier required for unlimited premium flows"],
        "best_for": "Full-stack web and backend developers looking for smooth AI flow states"
    },
    "IntelliJ IDEA": {
        "category": "Enterprise Java / Polyglot IDE",
        "pricing": "Freemium (Community Free, Ultimate $169/yr)",
        "summary": "The gold standard IDE for Java, Kotlin, and enterprise backend engineering.",
        "pros": ["Unmatched static code analysis & refactoring", "Deep framework integrations", "Robust database & profiling tools"],
        "cons": ["Heavy memory footprint", "Steep learning curve for advanced settings"],
        "best_for": "Java, Kotlin, Scala, and enterprise backend developers"
    },
    "PyCharm": {
        "category": "Python IDE",
        "pricing": "Freemium (Community Free, Professional $108/yr)",
        "summary": "The premier dedicated IDE for Python, Django, Data Science, and AI/ML workflows.",
        "pros": ["Out-of-the-box Python environment management", "Powerful debugger & scientific mode", "Django/Flask tooling"],
        "cons": ["Higher RAM usage than lightweight editors", "Professional tier required for web frameworks"],
        "best_for": "Python developers, data scientists, and backend engineers"
    },
    "Zed": {
        "category": "High-Performance Code Editor",
        "pricing": "Free (Open Source)",
        "summary": "A high-performance, multi-player code editor written in Rust by the creators of Atom.",
        "pros": ["Insanely fast sub-millisecond startup & typing", "Built-in multiplayer pair programming", "GPU-accelerated rendering"],
        "cons": ["Ecosystem extensions still maturing", "Fewer extensions than VS Code"],
        "best_for": "Performance purists, Rust, C++, and Go engineers who value speed"
    },
    "Neovim": {
        "category": "Terminal Modal Editor",
        "pricing": "Free (Open Source)",
        "summary": "Hyperextensible Vim-based text editor built for high keyboard efficiency and custom Lua configuration.",
        "pros": ["Minimal resource footprint", "Unmatched keyboard efficiency", "Infinite Lua customization & LSP support"],
        "cons": ["Steep learning curve", "Requires manual setup and maintenance"],
        "best_for": "Terminal enthusiasts, systems programmers, and devops engineers"
    }
}


def generate_amp_blog_post(ide_name: str, ide_info: Dict[str, Any]) -> str:
    """Generates a fully valid Blogger AMP HTML post for the given IDE."""
    title = f"{ide_name} Deep Dive: Features, Pricing, and Developer Evaluation"
    canonical_url = f"https://ideguide.blogspot.com/p/{ide_name.lower().replace(' ', '-')}-guide.html"

    pros_lis = "\n".join([f"          <li><strong>{p}</strong></li>" for p in ide_info.get("pros", [])])
    cons_lis = "\n".join([f"          <li><strong>{c}</strong></li>" for c in ide_info.get("cons", [])])

    html_content = f"""<!doctype html>
<html ⚡ lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1,minimum-scale=1">
  <title>{title} | IDE Guide</title>
  <link rel="canonical" href="{canonical_url}">
  <script async src="https://cdn.ampproject.org/v0.js"></script>
  <style amp-boilerplate>body{{-webkit-animation:-amp-start 8s steps(1,end) 0s 1 normal both;-moz-animation:-amp-start 8s steps(1,end) 0s 1 normal both;-ms-animation:-amp-start 8s steps(1,end) 0s 1 normal both;animation:-amp-start 8s steps(1,end) 0s 1 normal both}}@-webkit-keyframes -amp-start{{from{{visibility:hidden}}to{{visibility:visible}}}}-moz-keyframes -amp-start{{from{{visibility:hidden}}to{{visibility:visible}}}}-ms-keyframes -amp-start{{from{{visibility:hidden}}to{{visibility:visible}}}}-o-keyframes -amp-start{{from{{visibility:hidden}}to{{visibility:visible}}}}@keyframes -amp-start{{from{{visibility:hidden}}to{{visibility:visible}}}}</style><noscript><style amp-boilerplate>body{{-webkit-animation:none;-moz-animation:none;-ms-animation:none;animation:none}}</style></noscript>
  <style amp-custom>
    body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; line-height: 1.6; color: #1e293b; background: #f8fafc; margin: 0; padding: 16px; }}
    .container {{ max-width: 800px; margin: 0 auto; background: #ffffff; padding: 24px; border-radius: 8px; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1); }}
    h1 {{ color: #0f172a; font-size: 1.8rem; border-bottom: 2px solid #e2e8f0; padding-bottom: 8px; }}
    h2 {{ color: #2563eb; font-size: 1.3rem; margin-top: 24px; }}
    .badge {{ display: inline-block; background: #e0e7ff; color: #3730a3; padding: 4px 8px; border-radius: 4px; font-weight: bold; font-size: 0.85rem; margin-bottom: 12px; }}
    .pro-con-grid {{ display: flex; flex-wrap: wrap; gap: 16px; margin-top: 16px; }}
    .pro-box, .con-box {{ flex: 1 1 300px; padding: 16px; border-radius: 6px; }}
    .pro-box {{ background-color: #f0fdf4; border: 1px solid #bbf7d0; }}
    .con-box {{ background-color: #fef2f2; border: 1px solid #fecaca; }}
    ul {{ padding-left: 20px; }}
    .disclaimer {{ font-size: 0.85rem; color: #64748b; background: #f1f5f9; padding: 12px; border-left: 4px solid #94a3b8; margin-top: 32px; border-radius: 4px; }}
  </style>
</head>
<body>
  <div class="container">
    <div class="badge">Category: {ide_info.get("category", "Code Editor")}</div>
    <h1>{ide_name}: Comprehensive Developer Review</h1>
    <p><em>Published by IDE Guide | Pricing: <strong>{ide_info.get("pricing", "Free")}</strong></em></p>

    <h2>Overview</h2>
    <p>{ide_info.get("summary", "")}</p>

    <h2>Pricing & Licensing Model</h2>
    <p><strong>Tier:</strong> {ide_info.get("pricing", "Free")}</p>

    <h2>Strengths and Limitations</h2>
    <div class="pro-con-grid">
      <div class="pro-box">
        <h3>Pros</h3>
        <ul>
{pros_lis}
        </ul>
      </div>
      <div class="con-box">
        <h3>Cons</h3>
        <ul>
{cons_lis}
        </ul>
      </div>
    </div>

    <h2>Developer Verdict: Who Should Use {ide_name}?</h2>
    <p><strong>Best fit for:</strong> {ide_info.get("best_for", "Software Developers")}</p>

    <div class="disclaimer">
      <p>{DISCLAIMER_TEXT}</p>
    </div>
  </div>
</body>
</html>"""
    return html_content


def generate_google_flow_video_spec(ide_name: str, ide_info: Dict[str, Any]) -> Dict[str, Any]:
    """Generates Google Flow video creation specifications with visual prompts and scripts."""
    spec = {
        "video_title": f"Should You Use {ide_name}? 60-Second IDE Guide",
        "target_platform": "YouTube Shorts (9:16) & Main Video (16:9)",
        "ide_name": ide_name,
        "pricing_model": ide_info.get("pricing", "Free / Freemium"),
        "voiceover_script": (
            f"Looking for the perfect code editor? Today on IDE Guide, we're testing {ide_name}! "
            f"{ide_info.get('summary', '')} "
            f"Pricing model is {ide_info.get('pricing', 'Free')}. "
            f"Top strengths include {', '.join(ide_info.get('pros', [])[:2])}. "
            f"However, keep in mind {ide_info.get('cons', ['some performance trade-offs'])[0]}. "
            f"Best suited for {ide_info.get('best_for', 'developers')}. "
            f"{DISCLAIMER_TEXT}"
        ),
        "google_flow_scenes": [
            {
                "scene": 1,
                "timestamp": "00:00 - 00:05",
                "visual_prompt": (
                    f"Cinematic ultra-sharp close up of modern dark mode IDE interface displaying {ide_name} logo, "
                    "glowing neon cyan syntax highlights, fluid code cursor movement, soft purple rim lighting, 4k digital render."
                ),
                "framing_motion": "Slow zoom into code cursor with rack focus",
                "text_overlay": f"Is {ide_name} Worth It?",
                "audio_script": f"Looking for the perfect code editor? Today on IDE Guide, we're testing {ide_name}!"
            },
            {
                "scene": 2,
                "timestamp": "00:05 - 00:20",
                "visual_prompt": (
                    f"Isometric 3D view of developer workstation with double monitors showing {ide_name} editor, "
                    "fast autocompletion popup appearing, smooth terminal execution window below, dark slate color palette."
                ),
                "framing_motion": "Pan left across active code editor window",
                "text_overlay": f"Pricing: {ide_info.get('pricing', 'Free')}",
                "audio_script": f"{ide_info.get('summary', '')} Pricing model is {ide_info.get('pricing', 'Free')}."
            },
            {
                "scene": 3,
                "timestamp": "00:20 - 00:45",
                "visual_prompt": (
                    "Split screen visualization of pros and cons, glowing green checkmarks alongside red speed/memory gauges, "
                    "high contrast dark futuristic UI background."
                ),
                "framing_motion": "Static macro shot with animated side-by-side comparison graphics",
                "text_overlay": "Pros vs Cons Breakdown",
                "audio_script": f"Top strengths include {', '.join(ide_info.get('pros', [])[:2])}."
            },
            {
                "scene": 4,
                "timestamp": "00:45 - 00:60",
                "visual_prompt": (
                    "Clean studio background with subtle floating code particles, clear text summary overlay with YouTube channel logo @IDEguide, "
                    "disclaimer footer banner visible."
                ),
                "framing_motion": "Fade out to channel watermark",
                "text_overlay": f"Verdict: Great for {ide_info.get('best_for', 'Developers')}",
                "audio_script": f"Best suited for {ide_info.get('best_for', 'developers')}. {DISCLAIMER_TEXT}"
            }
        ],
        "disclaimer": DISCLAIMER_TEXT
    }
    return spec


def run_agent_skill(target_ide: str, output_dir: str = "content/custom") -> Dict[str, str]:
    """Runs agentic skill to generate blog post & video spec for target IDE."""
    ide_info = DEFAULT_IDE_KNOWLEDGE.get(target_ide, {
        "category": "Code Editor / IDE",
        "pricing": "Free / Commercial",
        "summary": f"A specialized software development tool designed for building applications in {target_ide}.",
        "pros": ["Powerful editing capabilities", "Extensible setup", "Rich developer tooling"],
        "cons": ["Requires setup and configuration"],
        "best_for": "Software engineering and web development teams"
    })

    os.makedirs(output_dir, exist_ok=True)
    slug = target_ide.lower().replace(" ", "_")

    # Generate Blog Post HTML
    amp_html = generate_amp_blog_post(target_ide, ide_info)
    is_valid, errors = validate_amp_html(amp_html)
    if not is_valid:
        raise ValueError(f"Generated AMP HTML failed validation: {errors}")

    blog_file = os.path.join(output_dir, f"{slug}_blogger_amp.html")
    with open(blog_file, "w", encoding="utf-8") as f:
        f.write(amp_html)

    # Generate Video Spec JSON
    video_spec = generate_google_flow_video_spec(target_ide, ide_info)
    spec_file = os.path.join(output_dir, f"{slug}_google_flow_spec.json")
    with open(spec_file, "w", encoding="utf-8") as f:
        f.write(json.dumps(video_spec, indent=2))

    print(f"✓ Successfully generated custom AMP blog post: {blog_file}")
    print(f"✓ Successfully generated Google Flow video spec: {spec_file}")

    return {"blog_post": blog_file, "video_spec": spec_file}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="IDE Guide Agentic Skill CLI")
    parser.add_argument("--ide", required=True, help="Target IDE or editor name (e.g. 'Cursor', 'Zed')")
    parser.add_argument("--output", default="content/custom", help="Output directory for generated files")
    args = parser.parse_args()

    run_agent_skill(args.ide, args.output)
