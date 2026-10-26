#!/usr/bin/env python3
"""
Daily Content Generator for IDE Guide.
Generates 3 daily packages (3 AMP blog posts for Blogger & 3 Google Flow Video Specs for YouTube).
Saves output under content/YYYY-MM-DD/ and updates content/history.json.
"""

import json
import os
import sys
from datetime import datetime, timezone
from typing import Dict, List, Any

HISTORY_FILE = "content/history.json"

IDE_DATABASE: List[Dict[str, Any]] = [
    {
        "name": "Visual Studio Code",
        "slug": "vscode",
        "category": "General Code Editor",
        "pricing": "Free (Open Source / Free Build)",
        "is_paid": False,
        "pros": [
            "Massive ecosystem of extensions and themes",
            "Built-in Git integration and terminal",
            "Lightweight with high performance and frequent updates",
            "Great IntelliSense and multi-language support"
        ],
        "cons": [
            "Can become memory intensive with too many extensions",
            "Requires configuration for complex C++/Java environments"
        ],
        "target_audience": "Web developers, Python programmers, Full-stack engineers, and beginner to advanced coders.",
        "overview": "Visual Studio Code (VS Code) is the world's most popular lightweight code editor developed by Microsoft. It combines simplicity with powerful debugging and extension capabilities.",
        "youtube_keywords": "VS Code, Visual Studio Code extensions, best code editor 2026, web development ide"
    },
    {
        "name": "Cursor AI",
        "slug": "cursor-ai",
        "category": "AI-Native IDE",
        "pricing": "Freemium ($20/mo Pro plan)",
        "is_paid": True,
        "pros": [
            "Deep multi-file codebase indexing and contextual AI chat",
            "Native integration with Claude 3.5 Sonnet and GPT-4o",
            "Seamless fork of VS Code with instant migration of extensions",
            "Instant inline AI edit and code generation (CMD+K)"
        ],
        "cons": [
            "Free tier limits fast AI requests",
            "Relies heavily on external cloud AI models"
        ],
        "target_audience": "Developers looking for maximum productivity using state-of-the-art AI coding assistants.",
        "overview": "Cursor is an AI-first code editor built as a fork of VS Code. It brings deep repository understanding, AI auto-edits, and instant code refactoring directly into your workspace.",
        "youtube_keywords": "Cursor AI editor, best AI code editor, Cursor vs VS Code, AI coding tools"
    },
    {
        "name": "IntelliJ IDEA",
        "slug": "intellij-idea",
        "category": "Enterprise Java/JVM IDE",
        "pricing": "Freemium (Community Free / Ultimate $169+/yr)",
        "is_paid": True,
        "pros": [
            "Industry-standard code analysis and refactoring for Java/Kotlin",
            "Out-of-the-box framework support (Spring Boot, Jakarta EE)",
            "Unrivaled static code safety and smart completion"
        ],
        "cons": [
            "Heavy resource usage (RAM and CPU during indexing)",
            "Ultimate features locked behind paid subscription"
        ],
        "target_audience": "Java, Kotlin, Enterprise backend developers, and Spring Boot engineers.",
        "overview": "JetBrains IntelliJ IDEA is the flagship IDE for JVM languages. Known for its intelligent code completion, deep static analysis, and enterprise framework tooling.",
        "youtube_keywords": "IntelliJ IDEA review, JetBrains Java IDE, IntelliJ vs Eclipse, best Java editor"
    },
    {
        "name": "PyCharm",
        "slug": "pycharm",
        "category": "Python IDE",
        "pricing": "Freemium (Community Free / Professional $99+/yr)",
        "is_paid": True,
        "pros": [
            "First-class support for Django, Flask, FastAPI, and Data Science",
            "Powerful visual debugger and database tool integrations",
            "Smart refactoring and virtual environment management"
        ],
        "cons": [
            "Slower startup times compared to text editors",
            "Full web development tools require the paid Pro edition"
        ],
        "target_audience": "Python developers, Data Scientists, Machine Learning engineers, and Django backend developers.",
        "overview": "PyCharm by JetBrains is a dedicated Python IDE equipped with advanced debugging, profiling, testing, and framework integrations for modern Python development.",
        "youtube_keywords": "PyCharm tutorial, Python IDE review, PyCharm Pro vs Free, Python coding"
    },
    {
        "name": "Zed",
        "slug": "zed",
        "category": "High-Performance Editor",
        "pricing": "Free (Open Source)",
        "is_paid": False,
        "pros": [
            "Blazing fast performance written in Rust with GPU rendering",
            "Real-time multiplayer collaborative coding out of the box",
            "Low latency typing and minimal memory footprint"
        ],
        "cons": [
            "Smaller extension ecosystem compared to VS Code",
            "Platform support expanding (primarily macOS/Linux initially)"
        ],
        "target_audience": "Performance enthusiasts, Rust/Go developers, and pair programmers looking for lightning-fast speeds.",
        "overview": "Zed is a next-generation high-performance code editor created by the creators of Atom and Tree-sitter. Written in Rust, it leverages GPU rendering for maximum responsiveness.",
        "youtube_keywords": "Zed editor review, Rust code editor, Zed vs VS Code, ultra fast IDE"
    },
    {
        "name": "Neovim",
        "slug": "neovim",
        "category": "Terminal Modal Editor",
        "pricing": "Free (Open Source)",
        "is_paid": False,
        "pros": [
            "Infinite customizability using Lua configuration scripts",
            "Minimalist, lightning-fast modal editing paradigm",
            "Built-in Language Server Protocol (LSP) and tree-sitter integration"
        ],
        "cons": [
            "Steep learning curve for keybindings and setup",
            "Time required to configure custom workflow"
        ],
        "target_audience": "Keyboard-driven developers, DevOps engineers, Linux enthusiasts, and efficiency power users.",
        "overview": "Neovim is an extensible Vim-based text editor built for extreme speed and keybinding efficiency, featuring native LSP, Lua scripting, and rich plugin ecosystems.",
        "youtube_keywords": "Neovim setup, Neovim review, Vim modal editing, fast terminal IDE"
    },
    {
        "name": "Windsurf Editor",
        "slug": "windsurf",
        "category": "AI Flow Editor",
        "pricing": "Freemium ($15/mo Pro plan)",
        "is_paid": True,
        "pros": [
            "Cascade AI flows combining developer intent with terminal and code execution",
            "Real-time collaborative AI agent integration",
            "VS Code extension compatibility"
        ],
        "cons": [
            "Newer product with evolving feature set",
            "Premium features require monthly subscription"
        ],
        "target_audience": "Developers seeking full AI-driven flow automation and agentic code refactoring.",
        "overview": "Windsurf by Codeium is an AI-native agentic IDE that fuses deep code understanding with execution awareness, enabling fluid developer-AI collaboration.",
        "youtube_keywords": "Windsurf IDE, Codeium Windsurf, AI flow editor, Cursor alternative"
    },
    {
        "name": "WebStorm",
        "slug": "webstorm",
        "category": "JavaScript / TypeScript IDE",
        "pricing": "Paid ($69+/yr or free for non-commercial/students)",
        "is_paid": True,
        "pros": [
            "Deep auto-completion for React, Angular, Vue, Node.js, and TypeScript",
            "Seamless refactoring across complex frontend codebases",
            "Built-in test runner, debugging, and Git integration"
        ],
        "cons": [
            "No permanent free tier for commercial use",
            "Can consume high memory on large monorepos"
        ],
        "target_audience": "Professional JavaScript and TypeScript frontend and Node.js engineers.",
        "overview": "WebStorm is JetBrains' dedicated JavaScript and TypeScript IDE offering out-of-the-box support for modern web frameworks and deep code inspection.",
        "youtube_keywords": "WebStorm review, JetBrains WebStorm, best JavaScript IDE, WebStorm vs VS Code"
    },
    {
        "name": "Sublime Text 4",
        "slug": "sublime-text-4",
        "category": "Lightweight Text Editor",
        "pricing": "Freemium ($99 evaluation licence)",
        "is_paid": True,
        "pros": [
            "Instant startup and rapid file switching",
            "GPU accelerated rendering for butter-smooth scrolling",
            "Extensive plugin capability via Package Control"
        ],
        "cons": [
            "Requires payment popup dismissal in evaluation mode",
            "Lacks built-in terminal and full IDE out-of-the-box"
        ],
        "target_audience": "Developers wanting an ultra-fast, lightweight text editor without IDE bloat.",
        "overview": "Sublime Text 4 is a refined, lightweight editor known for speed, responsiveness, multi-caret editing, and GPU rendering support.",
        "youtube_keywords": "Sublime Text 4 review, lightweight code editor, Sublime vs VS Code"
    }
]

DISCLAIMER_TEXT = (
    "Disclaimer: IDE Guide is an independent technical publication. "
    "This content is not sponsored, endorsed, or affiliated with any software vendor or editor developer mentioned above. "
    "All reviews and assessments are based strictly on objective developer evaluation."
)


def load_history() -> List[str]:
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data.get("covered_slugs", [])
        except Exception:
            return []
    return []


def save_history(covered_slugs: List[str]):
    os.makedirs(os.path.dirname(HISTORY_FILE), exist_ok=True)
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump({"covered_slugs": covered_slugs, "last_updated": datetime.now(timezone.utc).isoformat()}, f, indent=2)


def select_daily_ides(count: int = 3) -> List[Dict[str, Any]]:
    covered = load_history()
    available = [ide for ide in IDE_DATABASE if ide["slug"] not in covered]

    # If remaining available is less than requested, reset history
    if len(available) < count:
        covered = []
        available = IDE_DATABASE

    selected = available[:count]
    new_covered = list(set(covered + [ide["slug"] for ide in selected]))
    save_history(new_covered)
    return selected


def generate_amp_blog_post(ide: Dict[str, Any]) -> str:
    pros_html = "".join([f"<li>{pro}</li>" for pro in ide["pros"]])
    cons_html = "".join([f"<li>{con}</li>" for con in ide["cons"]])
    pricing_badge_color = "#e74c3c" if ide["is_paid"] else "#2ecc71"

    return f"""<!-- AMP HTML Blogger Post for {ide['name']} -->
<div class="ide-post" style="font-family: Arial, sans-serif; line-height: 1.6; color: #333; max-width: 800px; margin: 0 auto; padding: 15px;">
  <h1 style="color: #2c3e50; border-bottom: 2px solid #3498db; padding-bottom: 10px;">{ide['name']} Review: Is It Best for Your Workflow?</h1>

  <div class="badge-section" style="margin: 15px 0;">
    <span style="background-color: {pricing_badge_color}; color: #fff; padding: 6px 12px; border-radius: 4px; font-weight: bold; font-size: 0.9em;">
      {ide['pricing']}
    </span>
    <span style="background-color: #34495e; color: #fff; padding: 6px 12px; border-radius: 4px; font-weight: bold; font-size: 0.9em; margin-left: 8px;">
      {ide['category']}
    </span>
  </div>

  <h2>Overview</h2>
  <p>{ide['overview']}</p>

  <amp-img src="https://images.unsplash.com/photo-1517694712202-14dd9538aa97?w=800&auto=format&fit=crop" width="800" height="450" layout="responsive" alt="{ide['name']} Coding Workspace"></amp-img>

  <h2>Key Pros & Cons</h2>
  <div style="display: flex; flex-wrap: wrap; gap: 20px; margin: 20px 0;">
    <div style="flex: 1; min-width: 280px; background: #eef9f1; border-left: 4px solid #2ecc71; padding: 15px;">
      <h3 style="color: #27ae60; margin-top: 0;">Pros</h3>
      <ul>
        {pros_html}
      </ul>
    </div>
    <div style="flex: 1; min-width: 280px; background: #fdf2f2; border-left: 4px solid #e74c3c; padding: 15px;">
      <h3 style="color: #c0392b; margin-top: 0;">Cons</h3>
      <ul>
        {cons_html}
      </ul>
    </div>
  </div>

  <h2>Pricing & Licensing</h2>
  <p><strong>Pricing Model:</strong> {ide['pricing']}</p>
  <p>Whether you need a completely free tool or an enterprise subscription, {ide['name']} offers clear options depending on your budget and production scale.</p>

  <h2>Target Audience & Recommendation</h2>
  <p><strong>Who should use {ide['name']}?</strong> {ide['target_audience']}</p>

  <h2>Final Verdict</h2>
  <p>{ide['name']} stands out as a top contender in the {ide['category']} space. Test it with your stack to determine if it fits your development pipeline.</p>

  <div class="disclaimer-box" style="margin-top: 25px; padding: 15px; border-left: 4px solid #f39c12; background-color: #fcf8e3; font-size: 0.9em;">
    <strong>Disclaimer:</strong> {DISCLAIMER_TEXT}
  </div>
</div>
"""


def generate_google_flow_video_spec(ide: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "channel": "@IDEguide",
        "title": f"{ide['name']} in 60 Seconds: Best Features & Honest Review",
        "target_ide": ide["name"],
        "pricing": ide["pricing"],
        "category": ide["category"],
        "aspect_ratio": "9:16",
        "keywords": ide["youtube_keywords"],
        "prompts_google_flow": {
            "scene_1_hook": f"Cinematic macro shot of dark-mode code editor with glowing cursor typing in {ide['name']}, studio neon lighting, high detail 4k.",
            "scene_2_features": f"Dynamic over-the-shoulder shot of developer smoothly using {ide['name']} interface with sleek floating UI elements.",
            "scene_3_pros_cons": f"Split screen visual contrast showing positive workflow green light vs warning red badge for {ide['name']} features.",
            "scene_4_outro": "Sleek minimalist tech desk with IDE Guide logo overlay, 9:16 vertical video framing."
        },
        "narration_script": (
            f"Looking for the best code editor? Let's talk about {ide['name']}. "
            f"{ide['overview']} "
            f"On the plus side: {', '.join(ide['pros'][:2])}. "
            f"However, keep in mind: {ide['cons'][0]}. "
            f"Pricing details: {ide['pricing']}. "
            f"Is it right for you? It's best for {ide['target_audience']} "
            "Disclaimer: IDE Guide is an independent technical publication. This content is not sponsored, endorsed, or affiliated with any software vendor or editor developer mentioned above. All reviews and assessments are based strictly on objective developer evaluation. "
            "Subscribe to IDE Guide on YouTube and check ideguide.blogspot.com for more!"
        ),
        "on_screen_text": [
            f"Tool: {ide['name']}",
            f"Price: {ide['pricing']}",
            f"Pros: {ide['pros'][0]}",
            f"Cons: {ide['cons'][0]}",
            "Non-Sponsored Independent Review"
        ],
        "disclaimer": DISCLAIMER_TEXT
    }


def generate_daily_content_package(date_str: str = None) -> List[str]:
    if not date_str:
        date_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    target_dir = os.path.join("content", date_str)
    os.makedirs(target_dir, exist_ok=True)

    selected_ides = select_daily_ides(3)
    generated_files = []

    for idx, ide in enumerate(selected_ides, 1):
        slug = ide["slug"]

        # 1. Generate AMP Blog Post
        blog_html = generate_amp_blog_post(ide)
        blog_path = os.path.join(target_dir, f"blog_post_{idx}_{slug}.amp.html")
        with open(blog_path, "w", encoding="utf-8") as f:
            f.write(blog_html)
        generated_files.append(blog_path)

        # 2. Generate Google Flow Video Spec JSON
        video_spec = generate_google_flow_video_spec(ide)
        video_path = os.path.join(target_dir, f"video_spec_{idx}_{slug}.json")
        with open(video_path, "w", encoding="utf-8") as f:
            json.dump(video_spec, f, indent=2)
        generated_files.append(video_path)

    print(f"Generated {len(generated_files)} content items for date {date_str} in '{target_dir}'.")
    return generated_files


if __name__ == "__main__":
    date_arg = sys.argv[1] if len(sys.argv) > 1 else None
    generate_daily_content_package(date_arg)
