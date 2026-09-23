#!/usr/bin/env python3
"""
IDE Guide Agentic CLI Skill
Generates Blogger-compliant AMP HTML blog posts and Google Flow video specifications/scripts for IDE Guide.
"""

import argparse
import json
import os
import sys
import re

DISCLAIMER_TEXT = (
    "Disclaimer: IDE Guide is an independent technical publication. "
    "This content is not sponsored, endorsed, or affiliated with any software vendor "
    "or editor developer mentioned above. All reviews and assessments are based strictly "
    "on objective developer evaluation."
)

DEFAULT_IDE_KNOWLEDGE = {
    "cursor": {
        "name": "Cursor",
        "tagline": "The AI-first Code Editor built on VS Code",
        "price_model": "Freemium",
        "summary": "Cursor is an AI-powered code editor built as a fork of VS Code. It integrates advanced LLM capabilities directly into editing, codebase indexing, and multi-file code generation.",
        "pros": ["Deep codebase semantic indexing", "Native Claude 3.5 Sonnet & GPT-4o integration", "Seamless VS Code extension compatibility", "Multi-file edit apply"],
        "cons": ["Usage quota limits on free tier", "Requires cloud indexing for full context"],
        "best_for": "Developers seeking maximum AI coding velocity with familiar VS Code keybindings.",
        "official_url": "https://www.cursor.com"
    },
    "zed": {
        "name": "Zed",
        "tagline": "High-performance, multiplayer code editor from the creators of Atom",
        "price_model": "Free / Open Source",
        "summary": "Zed is a next-generation code editor written in Rust. It leverages GPU acceleration to deliver sub-millisecond latency and built-in multiplayer pair programming.",
        "pros": ["Blazing fast Rust-native GPU rendering", "Built-in real-time collaboration/multiplayer", "Low memory footprint", "Integrated AI assistance"],
        "cons": ["Ecosystem plugins still maturing", "Fewer extensions than VS Code"],
        "best_for": "Developers who prioritize speed, performance, and real-time pair programming.",
        "official_url": "https://zed.dev"
    },
    "vscode": {
        "name": "Visual Studio Code",
        "tagline": "The ubiquitous extensible code editor by Microsoft",
        "price_model": "Free / Open Source",
        "summary": "Visual Studio Code (VS Code) is the industry standard open-source editor, backed by a massive marketplace of extensions, debugging tools, and Copilot integration.",
        "pros": ["Massive extension ecosystem", "Excellent language server protocol (LSP) support", "Universal community adoption", "Free and open source"],
        "cons": ["Higher resource usage on large monorepos compared to native editors"],
        "best_for": "Generalist software engineers, web developers, and polyglot programmers.",
        "official_url": "https://code.visualstudio.com"
    },
    "neovim": {
        "name": "Neovim",
        "tagline": "Vim-fork focused on extensibility and Lua scripting",
        "price_model": "Free / Open Source",
        "summary": "Neovim is a refactored, highly extensible hyperextensible Vim-based text editor with native Lua configuration, LSP support, and async I/O.",
        "pros": ["Incredible speed and minimal RAM footprint", "Infinite customizability via Lua", "Native LSP and Treesitter support", "Terminal-native keyboard workflow"],
        "cons": ["Steep learning curve", "Requires time and effort to configure"],
        "best_for": "Keyboard purists, terminal lovers, and developers seeking full control over their editing environment.",
        "official_url": "https://neovim.io"
    },
    "jetbrains fleet": {
        "name": "JetBrains Fleet",
        "tagline": "Next-generation lightweight IDE and smart text editor",
        "price_model": "Freemium",
        "summary": "Fleet is JetBrains' lightweight polyglot editor built from scratch with a fast architecture, smart mode powered by IntelliJ code engine, and collaborative spaces.",
        "pros": ["Lightweight editor mode + full IDE smart engine", "Multi-language support out of the box", "JetBrains UI polish and AI Assistant"],
        "cons": ["Still evolving feature set compared to IntelliJ IDEA"],
        "best_for": "Developers wanting JetBrains intelligence without the full weight of traditional IDEs.",
        "official_url": "https://www.jetbrains.com/fleet/"
    }
}


def parse_repo_url(repo_url: str) -> str:
    """Extract IDE name from GitHub repo URL."""
    cleaned = repo_url.rstrip("/").removesuffix(".git")
    parts = cleaned.split("/")
    if len(parts) >= 1:
        repo_name = parts[-1]
        return repo_name.replace("-", " ").replace("_", " ").title()
    return "Custom IDE"


def get_ide_data(ide_name: str, price_model: str = None) -> dict:
    key = ide_name.lower().strip()
    if key in DEFAULT_IDE_KNOWLEDGE:
        data = DEFAULT_IDE_KNOWLEDGE[key].copy()
        if price_model:
            data["price_model"] = price_model
        return data

    # Fallback for dynamic/custom IDEs
    model = price_model if price_model else "Free / Paid Options Available"
    return {
        "name": ide_name,
        "tagline": f"Comprehensive Developer Tool Review: {ide_name}",
        "price_model": model,
        "summary": f"{ide_name} is a modern development environment designed to streamline software engineering workflows with targeted developer tools.",
        "pros": [f"Specialized feature set tailored for {ide_name}", "Modern developer interface", "Extensible architecture"],
        "cons": ["Ecosystem context depends on specific language toolchains"],
        "best_for": f"Software engineers exploring high-efficiency tools in {ide_name}.",
        "official_url": f"https://github.com/search?q={ide_name.replace(' ', '+')}"
    }


def generate_amp_html(ide_info: dict) -> str:
    """Generates valid Blogger AMP HTML blog post."""
    name = ide_info["name"]
    tagline = ide_info["tagline"]
    price_model = ide_info["price_model"]
    summary = ide_info["summary"]
    pros = "".join([f"<li>{p}</li>" for p in ide_info["pros"]])
    cons = "".join([f"<li>{c}</li>" for c in ide_info["cons"]])
    best_for = ide_info["best_for"]
    official_url = ide_info.get("official_url", "#")

    amp_html = f"""<!doctype html>
<html ⚡ lang="en">
<head>
  <meta charset="utf-8">
  <title>{name} Review &amp; Developer Guide - IDE Guide</title>
  <link rel="canonical" href="https://ideguide.blogspot.com/p/{name.lower().replace(' ', '-')}-review.html">
  <meta name="viewport" content="width=device-width,minimum-scale=1,initial-scale=1">
  <script async src="https://cdn.ampproject.org/v0.js"></script>
  <style amp-boilerplate>body{{-webkit-animation:-amp-start 8s steps(1,end) 0s 1 normal both;-moz-animation:-amp-start 8s steps(1,end) 0s 1 normal both;-ms-animation:-amp-start 8s steps(1,end) 0s 1 normal both;animation:-amp-start 8s steps(1,end) 0s 1 normal both}}@-webkit-keyframes -amp-start{{from{{visibility:hidden}}to{{visibility:visible}}}}@-moz-keyframes -amp-start{{from{{visibility:hidden}}to{{visibility:visible}}}}@-ms-keyframes -amp-start{{from{{visibility:hidden}}to{{visibility:visible}}}}@-o-keyframes -amp-start{{from{{visibility:hidden}}to{{visibility:visible}}}}@keyframes -amp-start{{from{{visibility:hidden}}to{{visibility:visible}}}}</style><noscript><style amp-boilerplate>body{{-webkit-animation:none;-moz-animation:none;-ms-animation:none;animation:none}}</style></noscript>
  <style amp-custom>
    body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; line-height: 1.6; color: #1e293b; background-color: #f8fafc; margin: 0; padding: 0; }}
    .container {{ max-width: 800px; margin: 0 auto; padding: 24px 16px; background: #ffffff; border-radius: 8px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }}
    header {{ border-bottom: 2px solid #e2e8f0; padding-bottom: 16px; margin-bottom: 24px; }}
    h1 {{ color: #0f172a; font-size: 2rem; margin: 0 0 8px 0; }}
    .subtitle {{ color: #64748b; font-size: 1.1rem; margin: 0; }}
    .badge {{ display: inline-block; padding: 4px 12px; font-size: 0.85rem; font-weight: 700; border-radius: 9999px; text-transform: uppercase; margin-top: 12px; background: #2563eb; color: #ffffff; }}
    .disclaimer-box {{ background-color: #f1f5f9; border-left: 4px solid #64748b; padding: 12px 16px; margin: 20px 0; font-size: 0.9rem; color: #475569; font-style: italic; }}
    .section {{ margin-bottom: 28px; }}
    h2 {{ color: #1e293b; border-bottom: 1px solid #cbd5e1; padding-bottom: 6px; font-size: 1.4rem; }}
    ul {{ padding-left: 20px; }}
    li {{ margin-bottom: 8px; }}
    .pro-con-grid {{ display: flex; flex-wrap: wrap; gap: 16px; margin: 20px 0; }}
    .pro-card, .con-card {{ flex: 1; min-width: 260px; padding: 16px; border-radius: 6px; }}
    .pro-card {{ background-color: #f0fdf4; border: 1px solid #bbf7d0; }}
    .con-card {{ background-color: #fef2f2; border: 1px solid #fecaca; }}
    .pro-card h3 {{ color: #166534; margin-top: 0; }}
    .con-card h3 {{ color: #991b1b; margin-top: 0; }}
    footer {{ border-top: 1px solid #e2e8f0; padding-top: 16px; font-size: 0.85rem; color: #94a3b8; text-align: center; margin-top: 40px; }}
  </style>
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "TechArticle",
    "headline": "{name} Review & Developer Guide",
    "description": "{summary}",
    "publisher": {{
      "@type": "Organization",
      "name": "IDE Guide",
      "url": "https://ideguide.blogspot.com/"
    }}
  }}
  </script>
</head>
<body>
  <div class="container">
    <header>
      <h1>{name} - Full Developer Breakdown</h1>
      <p class="subtitle">{tagline}</p>
      <span class="badge">{price_model}</span>
    </header>

    <div class="disclaimer-box">
      <strong>Notice:</strong> {DISCLAIMER_TEXT}
    </div>

    <div class="section">
      <h2>Overview &amp; Core Value</h2>
      <p>{summary}</p>
      <p>Visit official portal: <a href="{official_url}" target="_blank" rel="noopener">{official_url}</a></p>
    </div>

    <div class="section">
      <h2>Pros &amp; Cons</h2>
      <div class="pro-con-grid">
        <div class="pro-card">
          <h3>✅ What Makes It Great</h3>
          <ul>
            {pros}
          </ul>
        </div>
        <div class="con-card">
          <h3>❌ Drawbacks &amp; Limits</h3>
          <ul>
            {cons}
          </ul>
        </div>
      </div>
    </div>

    <div class="section">
      <h2>Pricing &amp; Accessibility</h2>
      <p><strong>Pricing Model:</strong> {price_model}</p>
      <p>Whether you are looking for zero-cost open source flexibility or advanced enterprise features, {name} provides a clear model suited for modern engineering teams.</p>
    </div>

    <div class="section">
      <h2>Final Recommendation: Who Should Use {name}?</h2>
      <p><strong>Ideal Choice For:</strong> {best_for}</p>
    </div>

    <footer>
      <p>&copy; IDE Guide (ideguide.blogspot.com). Independent technical evaluations for software engineers.</p>
    </footer>
  </div>
</body>
</html>"""
    return amp_html


def generate_google_flow_spec(ide_info: dict) -> dict:
    """Generates Google Flow video generation specification structure."""
    name = ide_info["name"]
    price_model = ide_info["price_model"]

    spec = {
        "title": f"Should You Use {name}? ({price_model} Editor Guide)",
        "channel": "@IDEguide",
        "youtube_url": "https://www.youtube.com/@IDEguide",
        "disclaimer": DISCLAIMER_TEXT,
        "format": "YouTube Video & Shorts Spec",
        "resolutions": {
            "shorts": "1080x1920 (9:16)",
            "standard": "1920x1080 (16:9)"
        },
        "scenes": [
            {
                "scene_number": 1,
                "duration_seconds": 5,
                "scene_title": "Hook & Visual Showcase",
                "camera_angle_and_framing": "Cinematic over-the-shoulder shot of developer workstation with dark room ambient glowing LEDs.",
                "lighting_and_atmosphere": "Soft neon cyan key light highlighting keycaps and ultra-wide monitor displaying editor UI.",
                "action_and_motion": "Smooth camera zoom toward screen showing code auto-completing smoothly in real-time.",
                "visual_cues_and_badges": [f"IDE Badge: {name}", f"Price Tag: {price_model}"],
                "google_flow_prompt": f"Cinematic medium close-up of dark mode editor software {name} running on a high resolution screen, neon ambient lighting, smooth zoom in, clean developer aesthetics, 4k resolution.",
                "narration_voiceover": f"Looking for your next primary code editor? Today we are breaking down {name}, rated as {price_model}.",
                "on_screen_text_overlays": [f"{name.upper()}", f"Pricing: {price_model}"]
            },
            {
                "scene_number": 2,
                "duration_seconds": 15,
                "scene_title": "Core Strengths & Features Showcase",
                "camera_angle_and_framing": "Split screen screen-recording and studio developer workstation close-up.",
                "lighting_and_atmosphere": "Bright, high contrast dark theme editor interface with highlighted syntax tree.",
                "action_and_motion": "Fast-paced panning across key strengths: " + ", ".join(ide_info["pros"][:2]),
                "visual_cues_and_badges": ["PROS HIGHLIGHT"],
                "google_flow_prompt": f"Close-up screen animation of code editing interface in {name}, fast responsive typing, sleek UI elements pop up with green checkmarks, professional tech review video style.",
                "narration_voiceover": f"Here is what sets {name} apart: {ide_info['pros'][0]}. Plus, {ide_info['pros'][-1]}.",
                "on_screen_text_overlays": ide_info["pros"][:3]
            },
            {
                "scene_number": 3,
                "duration_seconds": 10,
                "scene_title": "Cons & Tradeoffs",
                "camera_angle_and_framing": "Focused close-up on monitor with subtle amber highlight warning indicator.",
                "lighting_and_atmosphere": "Slight moody warm lighting overlaying screen corner.",
                "action_and_motion": "Smooth slide-in of drawbacks card.",
                "visual_cues_and_badges": ["TRADEOFFS"],
                "google_flow_prompt": f"Clean UI mockup screen showcasing technical configuration panel in {name}, subtle red warning icon overlay, high quality modern visual graphics.",
                "narration_voiceover": f"What are the downsides? {ide_info['cons'][0]} is something to keep in mind.",
                "on_screen_text_overlays": ide_info["cons"]
            },
            {
                "scene_number": 4,
                "duration_seconds": 10,
                "scene_title": "Verdict & Best Use Case",
                "camera_angle_and_framing": "Full frame high-impact visual card with channel branding @IDEguide.",
                "lighting_and_atmosphere": "Balanced studio lights, vibrant tech theme background.",
                "action_and_motion": "Checkmark animation sealing the final recommendation.",
                "visual_cues_and_badges": ["FINAL VERDICT", "NOT SPONSORED"],
                "google_flow_prompt": f"Sleek modern scorecard graphics overlay displaying final recommendation for {name}, subscribe button animation for @IDEguide channel, studio lighting.",
                "narration_voiceover": f"Final verdict: {name} is best for {ide_info['best_for']}. Subscribe to IDE Guide for daily developer tool breakdowns!",
                "on_screen_text_overlays": [f"Best For: {ide_info['best_for']}", "Subscribe @IDEguide"]
            }
        ]
    }
    return spec


def generate_video_script_markdown(spec: dict) -> str:
    """Formats Google Flow spec into readable markdown video script."""
    lines = []
    lines.append(f"# Video Script & Google Flow Prompts: {spec['title']}")
    lines.append(f"**Channel**: {spec['channel']} ({spec['youtube_url']})")
    lines.append(f"**Format**: {spec['format']}")
    lines.append(f"**Disclaimer**: {spec['disclaimer']}\n")
    lines.append("---")

    for s in spec["scenes"]:
        lines.append(f"## Scene {s['scene_number']}: {s['scene_title']} ({s['duration_seconds']}s)")
        lines.append(f"- **Camera Framing**: {s['camera_angle_and_framing']}")
        lines.append(f"- **Lighting & Mood**: {s['lighting_and_atmosphere']}")
        lines.append(f"- **Visual Cues**: {', '.join(s['visual_cues_and_badges'])}")
        lines.append(f"- **Google Flow Generation Prompt**:\n  > `{s['google_flow_prompt']}`")
        lines.append(f"- **Voiceover / Script**: \"{s['narration_voiceover']}\"")
        lines.append(f"- **On-Screen Text**: {', '.join(s['on_screen_text_overlays'])}\n")

    return "\n".join(lines)


def run_agent_skill(ide_name: str = None, repo_url: str = None, price_model: str = None, output_dir: str = None):
    if repo_url:
        target_name = parse_repo_url(repo_url)
    elif ide_name:
        target_name = ide_name
    else:
        target_name = "VS Code"

    ide_info = get_ide_data(target_name, price_model=price_model)
    amp_html = generate_amp_html(ide_info)
    spec = generate_google_flow_spec(ide_info)
    script_md = generate_video_script_markdown(spec)

    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
        amp_path = os.path.join(output_dir, "blog_post.amp.html")
        spec_path = os.path.join(output_dir, "video_spec.json")
        script_path = os.path.join(output_dir, "video_script.md")

        with open(amp_path, "w", encoding="utf-8") as f:
            f.write(amp_html)
        with open(spec_path, "w", encoding="utf-8") as f:
            json.dump(spec, f, indent=2)
        with open(script_path, "w", encoding="utf-8") as f:
            f.write(script_md)

        print(f"Generated IDE Guide package for '{target_name}' in '{output_dir}':")
        print(f"  - AMP Post: {amp_path}")
        print(f"  - Video Spec: {spec_path}")
        print(f"  - Video Script: {script_path}")
    else:
        print("=== AMP HTML POST ===")
        print(amp_html[:500] + "\n...[truncated]\n")
        print("=== GOOGLE FLOW VIDEO SPEC ===")
        print(json.dumps(spec, indent=2))

    return {
        "ide_info": ide_info,
        "amp_html": amp_html,
        "video_spec": spec,
        "video_script": script_md
    }


def main():
    parser = argparse.ArgumentParser(description="IDE Guide Agentic Skill - Generate AMP HTML and Google Flow specs.")
    parser.add_argument("--ide", type=str, help="Name of the IDE or Code Editor (e.g., Cursor, Zed, Neovim)")
    parser.add_argument("--repo", type=str, help="GitHub repository URL (e.g., https://github.com/zed-industries/zed)")
    parser.add_argument("--price-model", type=str, help="Pricing model (Free, Paid, Freemium)")
    parser.add_argument("--output-dir", type=str, help="Directory path to save generated artifacts")

    args = parser.parse_args()
    run_agent_skill(ide_name=args.ide, repo_url=args.repo, price_model=args.price_model, output_dir=args.output_dir)


if __name__ == "__main__":
    main()
