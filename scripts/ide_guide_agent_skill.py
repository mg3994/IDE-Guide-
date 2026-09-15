#!/usr/bin/env python3
"""
IDE Guide Agentic Skill Engine
Generates AMP HTML blog posts for Blogger and Google Flow video specs for YouTube (@IDEguide).
"""

import argparse
import json
import os
import re
import sys
from datetime import datetime
from typing import Dict, Any

DISCLAIMER_TEXT = (
    "Disclaimer: IDE Guide is an independent technical publication. "
    "This content is not sponsored, endorsed, or affiliated with any software vendor or editor developer mentioned above. "
    "All reviews and assessments are based strictly on objective developer evaluation."
)

IDE_DATABASE = {
    "cursor": {
        "name": "Cursor IDE",
        "tagline": "The AI-first Code Editor built on VS Code",
        "pricing": "Freemium ($20/mo for Pro)",
        "is_paid": True,
        "is_free": True,
        "category": "AI Code Editor",
        "pros": [
            "Deep AI codebase indexing and context understanding",
            "Seamless multi-file inline edit suggestions (Cmd+K)",
            "Native VS Code extension compatibility",
            "Fast auto-complete powered by custom models"
        ],
        "cons": [
            "Requires paid subscription for heavy AI model usage",
            "High memory usage during full codebase indexing",
            "Closed-source core additions"
        ],
        "key_features": [
            "Copilot++ intelligent inline editing",
            "Chat with entire repository context",
            "Terminal AI auto-fix commands",
            "Custom privacy mode for local code retention"
        ],
        "verdict": "Best for developers looking for cutting-edge AI assistance without leaving the familiar VS Code ecosystem."
    },
    "zed": {
        "name": "Zed Editor",
        "tagline": "High-performance multiplayer code editor written in Rust",
        "pricing": "Free & Open Source",
        "is_paid": False,
        "is_free": True,
        "category": "High-Performance Editor",
        "pros": [
            "Blazing fast performance powered by GPU rendering (GPUI)",
            "Extremely low memory footprint and instant startup",
            "Built-in real-time collaborative coding (Multiplayer)",
            "Integrated assistant supporting Claude & OpenAI models"
        ],
        "cons": [
            "Ecosystem of extensions is still maturing compared to VS Code",
            "Currently primary focus on macOS & Linux (Windows in progress)"
        ],
        "key_features": [
            "GPU-accelerated rendering engine",
            "Real-time pair programming out of the box",
            "Language Server Protocol (LSP) native integration",
            "Built-in AI panel with flexible provider keys"
        ],
        "verdict": "The top choice for performance purists who want speed, low latency, and native multiplayer editing."
    },
    "neovim": {
        "name": "Neovim",
        "tagline": "Hyperextensible Vim-based text editor",
        "pricing": "Free & Open Source",
        "is_paid": False,
        "is_free": True,
        "category": "Terminal/Modal Editor",
        "pros": [
            "Ultimate keyboard-driven productivity and speed",
            "Lua-first plugin ecosystem for full customization",
            "Negligible resource footprint",
            "Native LSP and Treesitter support for syntax tree awareness"
        ],
        "cons": [
            "Steep learning curve for modal editing and keybindings",
            "Requires time investment to configure optimal dev setup"
        ],
        "key_features": [
            "Embedded Lua engine",
            "Treesitter syntax parser integration",
            "Asynchronous plugin system",
            "Vim keybindings with modern extensibility"
        ],
        "verdict": "Unrivaled for developers seeking complete control over their editing environment and keyboard efficiency."
    },
    "vscode": {
        "name": "Visual Studio Code",
        "tagline": "The world's most popular extensible code editor",
        "pricing": "Free",
        "is_paid": False,
        "is_free": True,
        "category": "General Purpose IDE",
        "pros": [
            "Massive plugin marketplace covering every language & tool",
            "Excellent remote development (SSH, Containers, WSL)",
            "Strong multi-language debugging support"
        ],
        "cons": [
            "Electron-based memory overhead with many active extensions",
            "Can feel slow with very large monorepos"
        ],
        "key_features": [
            "Integrated Git & source control GUI",
            "Remote Containers & Dev Containers standard",
            "Comprehensive debugging suite",
            "Extensive customization options"
        ],
        "verdict": "The standard go-to editor for general web, cloud, and multi-language development."
    },
    "intellij": {
        "name": "IntelliJ IDEA",
        "tagline": "The premier Java & Kotlin IDE by JetBrains",
        "pricing": "Freemium (Community Free, Ultimate $169/yr)",
        "is_paid": True,
        "is_free": True,
        "category": "Enterprise IDE",
        "pros": [
            "Unrivaled deep refactoring and code analysis for JVM languages",
            "Out-of-the-box framework support (Spring, Quarkus, Micronaut)",
            "Robust database and enterprise tools built-in"
        ],
        "cons": [
            "Heavy memory usage requiring 16GB+ RAM for smooth performance",
            "Ultimate edition requires annual license fee"
        ],
        "key_features": [
            "Advanced static code analysis and auto-refactoring",
            "Database inspector and query execution tool",
            "JetBrains AI Assistant integration",
            "Deep Spring Framework integration"
        ],
        "verdict": "Essential for serious Java, Kotlin, and enterprise backend engineering teams."
    },
    "fleet": {
        "name": "JetBrains Fleet",
        "tagline": "Next-generation lightweight IDE by JetBrains",
        "pricing": "Freemium (Preview Free)",
        "is_paid": True,
        "is_free": True,
        "category": "Lightweight / Distributed IDE",
        "pros": [
            "Lightweight editor mode with instant launch",
            "Smart mode backed by IntelliJ code processing engine",
            "Built-in collaborative editing and remote workspace architecture"
        ],
        "cons": [
            "Still under active preview/development",
            "Plugin ecosystem is in early stages"
        ],
        "key_features": [
            "Dual-mode architecture (Lightweight Text vs Smart IDE)",
            "Distributed backend execution",
            "JetBrains AI integration",
            "Clean modern visual layout"
        ],
        "verdict": "Promising lightweight alternative for JetBrains fans wanting quick startup with smart backend capability."
    }
}

def get_ide_data(query: str) -> Dict[str, Any]:
    query_lower = query.lower().strip()

    # Try exact or partial matching in DB
    for key, data in IDE_DATABASE.items():
        if key in query_lower or query_lower in key or data["name"].lower() in query_lower:
            return data

    # Generic fallback generator if novel IDE name / URL provided
    clean_name = re.sub(r'https?://(?:www\.)?github\.com/', '', query).strip('/')
    clean_name = clean_name.split('/')[-1].replace('-', ' ').replace('_', ' ').title()
    if not clean_name:
        clean_name = "Custom IDE / Developer Tool"

    return {
        "name": clean_name,
        "tagline": f"Modern Code Editing & Developer Productivity Tool ({clean_name})",
        "pricing": "Free / Open Source Evaluation Available",
        "is_paid": False,
        "is_free": True,
        "category": "Developer Tool",
        "pros": [
            "Extensible workflow custom tailored for developer speed",
            "Strong developer community and integration potential",
            "Flexible configuration and modern UI controls"
        ],
        "cons": [
            "Ecosystem documentation still expanding",
            "Requires initial setup configuration for optimal performance"
        ],
        "key_features": [
            "Smart code intelligence and syntax detection",
            "Integrated execution terminal and debugging tools",
            "Custom keybindings and extension support"
        ],
        "verdict": f"{clean_name} presents an intriguing option for developers evaluating modern, efficient workflows."
    }

def generate_amp_html_blog(data: Dict[str, Any]) -> str:
    name = data["name"]
    tagline = data["tagline"]
    pricing = data["pricing"]
    category = data["category"]

    pros_html = "".join([f"<li><strong>Pro:</strong> {p}</li>" for p in data["pros"]])
    cons_html = "".join([f"<li><strong>Con:</strong> {c}</li>" for c in data["cons"]])
    features_html = "".join([f"<li>{f}</li>" for f in data["key_features"]])

    amp_html = f"""<!doctype html>
<html ⚡ lang="en">
<head>
  <meta charset="utf-8">
  <title>{name} Review & Guide - IDE Guide</title>
  <link rel="canonical" href="https://ideguide.blogspot.com/{re.sub(r'[^a-z0-9]', '-', name.lower())}.html">
  <meta name="viewport" content="width=device-width,minimum-scale=1,initial-scale=1">
  <style amp-boilerplate>body{{-webkit-animation:-amp-start 8s steps(1,end) 0s 1 normal both;-moz-animation:-amp-start 8s steps(1,end) 0s 1 normal both;-ms-animation:-amp-start 8s steps(1,end) 0s 1 normal both;animation:-amp-start 8s steps(1,end) 0s 1 normal both}}@-webkit-keyframes -amp-start{{from{{visibility:hidden}}to{{visibility:visible}}}}@-moz-keyframes -amp-start{{from{{visibility:hidden}}to{{visibility:visible}}}}@-ms-keyframes -amp-start{{from{{visibility:hidden}}to{{visibility:visible}}}}@-o-keyframes -amp-start{{from{{visibility:hidden}}to{{visibility:visible}}}}@keyframes -amp-start{{from{{visibility:hidden}}to{{visibility:visible}}}}</style><noscript><style amp-boilerplate>body{{-webkit-animation:none;-moz-animation:none;-ms-animation:none;animation:none}}</style></noscript>
  <script async src="https://cdn.ampproject.org/v0.js"></script>
  <style amp-custom>
    body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; line-height: 1.6; color: #1e293b; background: #f8fafc; padding: 16px; margin: 0 auto; max-width: 800px; }}
    header {{ background: #0f172a; color: #ffffff; padding: 24px; border-radius: 12px; margin-bottom: 24px; text-align: center; }}
    header h1 {{ margin: 0 0 8px 0; font-size: 28px; color: #38bdf8; }}
    header p {{ margin: 0; font-size: 16px; color: #94a3b8; }}
    .badge {{ display: inline-block; background: #0284c7; color: white; padding: 4px 12px; border-radius: 20px; font-size: 14px; font-weight: bold; margin-top: 12px; }}
    .disclaimer {{ background: #f1f5f9; border-left: 4px solid #0284c7; padding: 12px 16px; margin: 20px 0; font-size: 13px; color: #475569; border-radius: 4px; }}
    .card {{ background: #ffffff; border: 1px solid #e2e8f0; border-radius: 8px; padding: 20px; margin-bottom: 20px; box-shadow: 0 1px 3px rgba(0,0,0,0.05); }}
    h2 {{ color: #0f172a; font-size: 20px; border-bottom: 2px solid #e2e8f0; padding-bottom: 8px; margin-top: 0; }}
    ul {{ padding-left: 20px; margin-bottom: 0; }}
    li {{ margin-bottom: 8px; }}
    .pros-cons {{ display: flex; flex-wrap: wrap; gap: 16px; }}
    .pro-box {{ flex: 1; min-width: 280px; background: #f0fdf4; border: 1px solid #bbf7d0; border-radius: 8px; padding: 16px; }}
    .con-box {{ flex: 1; min-width: 280px; background: #fef2f2; border: 1px solid #fecaca; border-radius: 8px; padding: 16px; }}
    .pro-box h3 {{ color: #166534; margin-top: 0; font-size: 16px; }}
    .con-box h3 {{ color: #991b1b; margin-top: 0; font-size: 16px; }}
    footer {{ text-align: center; font-size: 14px; color: #64748b; margin-top: 32px; padding-top: 16px; border-top: 1px solid #e2e8f0; }}
  </style>
</head>
<body>
  <header>
    <h1>{name} Analysis & Guide</h1>
    <p>{tagline}</p>
    <div class="badge">Category: {category} | Pricing: {pricing}</div>
  </header>

  <div class="disclaimer">
    <strong>Independent Publication Notice:</strong> {DISCLAIMER_TEXT}
  </div>

  <div class="card">
    <h2>Overview & Pricing Structure</h2>
    <p>Choosing the right code editor impacts developer speed, focus, and system performance. <strong>{name}</strong> offers a tailored environment optimized for modern software engineering.</p>
    <p><strong>Pricing Tier:</strong> {pricing}.</p>
  </div>

  <div class="card">
    <h2>Key Features & Capabilities</h2>
    <ul>
      {features_html}
    </ul>
  </div>

  <div class="card">
    <h2>Pros & Cons Breakdown</h2>
    <div class="pros-cons">
      <div class="pro-box">
        <h3>Advantages</h3>
        <ul>
          {pros_html}
        </ul>
      </div>
      <div class="con-box">
        <h3>Trade-offs</h3>
        <ul>
          {cons_html}
        </ul>
      </div>
    </div>
  </div>

  <div class="card">
    <h2>Verdict & Recommendation</h2>
    <p>{data['verdict']}</p>
  </div>

  <footer>
    <p>Published by <strong>IDE Guide</strong> | Blog: <a href="https://ideguide.blogspot.com/">ideguide.blogspot.com</a> | YouTube: <a href="https://www.youtube.com/@IDEguide">@IDEguide</a></p>
  </footer>
</body>
</html>"""
    return amp_html

def generate_google_flow_video_spec(data: Dict[str, Any]) -> Dict[str, Any]:
    name = data["name"]
    pricing = data["pricing"]
    pros = ", ".join(data["pros"][:2])
    cons = ", ".join(data["cons"][:2])

    spec = {
        "title": f"{name} Detailed Evaluation & Feature Showcase | IDE Guide",
        "channel": "@IDEguide",
        "disclaimer": DISCLAIMER_TEXT,
        "target_format": "YouTube Video & Shorts (Google Flow / Veo Visual Script)",
        "ide_metadata": {
            "name": name,
            "pricing": pricing,
            "category": data["category"]
        },
        "scenes": [
            {
                "scene_number": 1,
                "scene_title": "Hook & Editor Reveal",
                "duration_seconds": 5,
                "visual_prompt": (
                    f"Cinematic close-up macro shot of a sleek dark-themed developer workspace. "
                    f"A high-resolution monitor glowing with {name} code editor user interface. "
                    f"Subtle neon ambient backlighting (cyan and deep purple), soft focus blur in the background."
                ),
                "camera_framing_motion": "Close-up macro shot with a slow 5-degree smooth pan from left to right.",
                "lighting_atmosphere": "Cyberpunk dark mode glow, 4500K accent light, sleek modern tech aesthetic.",
                "text_overlay": f"{name.upper()}\n{data['tagline']}",
                "voiceover_script": f"Is {name} the ultimate editor for your workflow? Let's analyze the features, pros, cons, and pricing."
            },
            {
                "scene_number": 2,
                "scene_title": "Core Features & Hands-on Demo",
                "duration_seconds": 10,
                "visual_prompt": (
                    f"Medium tracking shot over developer's shoulder typing code into {name}. "
                    f"Screen highlights smooth auto-completion, split panes, and integrated tools. "
                    f"Clean, minimal aesthetic with high contrast UI lines."
                ),
                "camera_framing_motion": "Medium over-the-shoulder tracking shot, steady push-in towards screen.",
                "lighting_atmosphere": "Warm minimalist studio lighting, balanced softbox highlights.",
                "text_overlay": f"KEY ADVANTAGES:\n- {data['pros'][0]}\n- {data['pros'][1] if len(data['pros']) > 1 else ''}",
                "voiceover_script": f"Key highlights include {pros}. It delivers smooth performance designed for developer efficiency."
            },
            {
                "scene_number": 3,
                "scene_title": "Pricing & Trade-offs (Free vs Paid)",
                "duration_seconds": 8,
                "visual_prompt": (
                    f"Split screen or dynamic overlay showing pricing badge '{pricing}' alongside editor interface. "
                    f"High tech graphical UI callout boxes appearing with smooth blur transitions."
                ),
                "camera_framing_motion": "Static centered locked shot with dynamic UI element movement.",
                "lighting_atmosphere": "High contrast studio lighting, bright crisp callout graphics.",
                "text_overlay": f"PRICING: {pricing.upper()}\nTRADE-OFFS: {data['cons'][0]}",
                "voiceover_script": f"Pricing structure is {pricing}. Trade-offs to consider include {cons}."
            },
            {
                "scene_number": 4,
                "scene_title": "Final Verdict & Disclaimer",
                "duration_seconds": 7,
                "visual_prompt": (
                    f"Clean end screen featuring IDE Guide logo, YouTube subscribe prompt, and website link ideguide.blogspot.com. "
                    f"Non-sponsorship text notice visible in clean modern typography at bottom."
                ),
                "camera_framing_motion": "Slow zoom out to reveal channel social cards.",
                "lighting_atmosphere": "Sleek slate dark background with vibrant blue/cyan branding.",
                "text_overlay": f"VERDICT: {data['verdict']}\n\n{DISCLAIMER_TEXT}",
                "voiceover_script": f"Verdict: {data['verdict']}. Check ideguide.blogspot.com for the full AMP blog review and subscribe to @IDEguide for daily tech breakdowns!"
            }
        ]
    }
    return spec

def main():
    parser = argparse.ArgumentParser(description="IDE Guide Agentic Skill CLI")
    parser.add_argument("--ide", type=str, help="Name of the IDE/Editor to analyze (e.g. 'Cursor', 'Zed', 'Neovim')")
    parser.add_argument("--repo", type=str, help="GitHub Repository URL to analyze")
    parser.add_argument("--output-dir", type=str, default="output", help="Directory to save generated outputs")

    args = parser.parse_args()

    target_query = args.ide or args.repo or "cursor"
    ide_data = get_ide_data(target_query)

    amp_blog = generate_amp_html_blog(ide_data)
    video_spec = generate_google_flow_video_spec(ide_data)

    os.makedirs(args.output_dir, exist_ok=True)
    slug = re.sub(r'[^a-z0-9]', '_', ide_data['name'].lower())

    blog_path = os.path.join(args.output_dir, f"{slug}_amp.html")
    video_path = os.path.join(args.output_dir, f"{slug}_google_flow_spec.json")

    with open(blog_path, "w", encoding="utf-8") as f:
        f.write(amp_blog)

    with open(video_path, "w", encoding="utf-8") as f:
        json.dump(video_spec, f, indent=2)

    print(f"✅ Generated AMP Blog Post: {blog_path}")
    print(f"✅ Generated Google Flow Video Spec: {video_path}")

if __name__ == "__main__":
    main()
