#!/usr/bin/env python3
"""
Daily Content Generator for IDE Guide (Blogger AMP Posts & YouTube Google Flow Video Specs).
Generates 3 AMP blog posts and 3 video specs daily, maintaining history in content/history.json.
"""

import json
import os
import sys
from datetime import datetime, timezone
from typing import Dict, List, Any

DISCLAIMER_TEXT = (
    "Disclaimer: IDE Guide is an independent technical publication. "
    "This content is not sponsored, endorsed, or affiliated with any software vendor "
    "or editor developer mentioned above. All reviews and assessments are based strictly "
    "on objective developer evaluation."
)

# IDE catalog pool with facts, features, pricing, pros, cons, and recommendations
IDE_CATALOG: List[Dict[str, Any]] = [
    {
        "id": "vscode",
        "name": "Visual Studio Code (VS Code)",
        "developer": "Microsoft",
        "pricing": "Free / Open Source (MIT core build)",
        "is_paid": False,
        "category": "General Purpose / Extensible Editor",
        "strengths": [
            "Massive extension marketplace with over 50,000 extensions.",
            "Built-in Git integration, terminal, and debugging tools.",
            "Lightweight resource usage compared to traditional full IDEs."
        ],
        "weaknesses": [
            "Requires extensive extension configuration for complex C++/Java projects.",
            "Default builds include Microsoft telemetry (use VSCodium for zero telemetry)."
        ],
        "best_for": "Web developers, Python developers, polyglot engineers, and students.",
        "image_url": "https://images.unsplash.com/photo-1555066931-4365d14bab8c?w=800&auto=format&fit=crop"
    },
    {
        "id": "cursor",
        "name": "Cursor AI Editor",
        "developer": "Anysphere",
        "pricing": "Freemium ($20/mo Pro for unlimited fast Claude 3.5 Sonnet & GPT-4o)",
        "is_paid": True,
        "category": "AI-Native Code Editor",
        "strengths": [
            "Deep codebase indexing with @Codebase context query.",
            "Multi-file edits with Composer and fast Inline Edits (Ctrl+K).",
            "100% compatible with all VS Code extensions and themes."
        ],
        "weaknesses": [
            "Free tier requests run out quickly on heavy projects.",
            "Requires active internet connection for advanced AI models."
        ],
        "best_for": "Full-stack developers, rapid prototyping, and AI-assisted workflows.",
        "image_url": "https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?w=800&auto=format&fit=crop"
    },
    {
        "id": "intellij_idea",
        "name": "IntelliJ IDEA",
        "developer": "JetBrains",
        "pricing": "Freemium (Community Free / Ultimate $169+/yr)",
        "is_paid": True,
        "category": "Enterprise Java / Kotlin / Polyglot IDE",
        "strengths": [
            "Unrivaled refactoring tools and static code analysis.",
            "Deep framework integration for Spring Boot, Jakarta EE, and Kotlin.",
            "Comprehensive database client and HTTP client built-in."
        ],
        "weaknesses": [
            "High RAM and CPU consumption during indexing.",
            "Community edition lacks advanced enterprise framework features."
        ],
        "best_for": "Enterprise Java developers, Spring Boot engineers, and Kotlin backend teams.",
        "image_url": "https://images.unsplash.com/photo-1517694712202-14dd9538aa97?w=800&auto=format&fit=crop"
    },
    {
        "id": "pycharm",
        "name": "PyCharm",
        "developer": "JetBrains",
        "pricing": "Freemium (Community Free / Professional $99+/yr)",
        "is_paid": True,
        "category": "Python / Data Science IDE",
        "strengths": [
            "First-class support for Django, FastAPI, Flask, and NumPy/Pandas.",
            "Built-in Jupyter notebook environment and scientific mode.",
            "Intelligent virtualenv, conda, and poetry management."
        ],
        "weaknesses": [
            "Slower cold startup time compared to lightweight text editors.",
            "Professional features (remote deployment, database editor) require subscription."
        ],
        "best_for": "Python developers, Data Scientists, and Machine Learning engineers.",
        "image_url": "https://images.unsplash.com/photo-1526379095098-d400fd0bf935?w=800&auto=format&fit=crop"
    },
    {
        "id": "zed",
        "name": "Zed Editor",
        "developer": "Zed Industries",
        "pricing": "Free / Open Source (GPL / Apache 2.0)",
        "is_paid": False,
        "category": "High-Performance Rust-based Editor",
        "strengths": [
            "Blazing fast 120 FPS render pipeline powered by GPU execution.",
            "Built-in real-time collaborative editing (multiplayer code pairing).",
            "Minimalist clean UI with native Tree-sitter syntax highlighting."
        ],
        "weaknesses": [
            "Smaller extension ecosystem compared to VS Code.",
            "Linux and Windows ports are newer compared to macOS build."
        ],
        "best_for": "Performance enthusiasts, Rust/Go/TypeScript developers, and remote pair programmers.",
        "image_url": "https://images.unsplash.com/photo-1542831371-29b0f74f9713?w=800&auto=format&fit=crop"
    },
    {
        "id": "neovim",
        "name": "Neovim",
        "developer": "Neovim Core Team",
        "pricing": "Free / Open Source (Apache 2.0)",
        "is_paid": False,
        "category": "Terminal Modal Text Editor",
        "strengths": [
            "Near-zero latency and ultra-lightweight memory footprint.",
            "Lua-based ecosystem for hyper-customizable configurations (LazyVim, NvChad).",
            "Native LSP support and asynchronous plugin execution."
        ],
        "weaknesses": [
            "Steep learning curve for vim keybindings and modal navigation.",
            "Requires initial setup time to build custom development workflow."
        ],
        "best_for": "Terminal warriors, systems engineers, Linux power users, and keyboard purists.",
        "image_url": "https://images.unsplash.com/photo-1629654297299-c8506221ca97?w=800&auto=format&fit=crop"
    },
    {
        "id": "windsurf",
        "name": "Windsurf Editor",
        "developer": "Codeium",
        "pricing": "Freemium ($15/mo Pro for advanced Cascade flows)",
        "is_paid": True,
        "category": "Agentic AI Code Editor",
        "strengths": [
            "Cascade Agentic workflow seamlessly combines inline edits with terminal actions.",
            "Real-time deep indexing of local and remote codebases.",
            "Generous free tier provided by Codeium infrastructure."
        ],
        "weaknesses": [
            "Agentic AI executions can occasionally suggest redundant refactor steps.",
            "Requires tuning context rules for non-standard project layouts."
        ],
        "best_for": "Full-stack web developers seeking autonomous agentic coding assistance.",
        "image_url": "https://images.unsplash.com/photo-1531403009284-440f080d1e12?w=800&auto=format&fit=crop"
    },
    {
        "id": "helix",
        "name": "Helix Editor",
        "developer": "Helix Contributors",
        "pricing": "Free / Open Source (MPL-2.0)",
        "is_paid": False,
        "category": "Post-Modern Terminal Text Editor",
        "strengths": [
            "Zero config needed: Native LSP, Tree-sitter, and auto-complete out of the box.",
            "Selection-first modal editing model (Kakoune inspired).",
            "Extremely fast startup time written in Rust."
        ],
        "weaknesses": [
            "No plugin architecture yet (currently in design proposal).",
            "Different keybinding sequence compared to standard Vim/Neovim."
        ],
        "best_for": "Developers who want zero-config terminal editing without tweaking Lua scripts.",
        "image_url": "https://images.unsplash.com/photo-1515879218367-8466d910aaa4?w=800&auto=format&fit=crop"
    },
    {
        "id": "webstorm",
        "name": "WebStorm",
        "developer": "JetBrains",
        "pricing": "Paid ($69+/yr or included in All Products Pack / Free for non-commercial/students)",
        "is_paid": True,
        "category": "JavaScript / TypeScript & Web IDE",
        "strengths": [
            "Unrivaled auto-imports, refactoring, and static analysis for React, Vue, Angular, Next.js.",
            "Built-in tailwind, GraphQL, and CSS inspections.",
            "Integrated unit testing runner (Jest, Vitest, Cypress) and debugger."
        ],
        "weaknesses": [
            "Commercial product requiring subscription for corporate use.",
            "Slower launch times than lightweight text editors."
        ],
        "best_for": "Professional frontend developers, full-stack JS/TS engineers, and web teams.",
        "image_url": "https://images.unsplash.com/photo-1507238691740-187a5b1d37b8?w=800&auto=format&fit=crop"
    }
]


def load_history(history_file: str) -> List[str]:
    if os.path.exists(history_file):
        try:
            with open(history_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get("covered_ide_ids", [])
        except Exception:
            return []
    return []


def save_history(history_file: str, covered_ids: List[str]):
    os.makedirs(os.path.dirname(history_file), exist_ok=True)
    with open(history_file, 'w', encoding='utf-8') as f:
        json.dump({"covered_ide_ids": covered_ids, "last_updated": datetime.now(timezone.utc).isoformat()}, f, indent=2)


def select_daily_ides(count: int = 3, history_file: str = "content/history.json") -> List[Dict[str, Any]]:
    covered_ids = load_history(history_file)
    available = [ide for ide in IDE_CATALOG if ide["id"] not in covered_ids]

    # Reset history if pool exhausted
    if len(available) < count:
        covered_ids = []
        available = IDE_CATALOG

    selected = available[:count]
    updated_ids = covered_ids + [ide["id"] for ide in selected]
    save_history(history_file, updated_ids)
    return selected


def generate_amp_blog_post(ide: Dict[str, Any]) -> str:
    paid_badge = "PAID / SUBSCRIPTION" if ide["is_paid"] else "FREE / OPEN SOURCE"

    strengths_html = "".join([f"<li><strong>{s.split(':')[0] if ':' in s else 'Feature'}:</strong> {s}</li>" for s in ide["strengths"]])
    weaknesses_html = "".join([f"<li><strong>{w.split(':')[0] if ':' in w else 'Drawback'}:</strong> {w}</li>" for w in ide["weaknesses"]])

    return f"""<!-- AMP HTML Post for ideguide.blogspot.com -->
<h2>{ide['name']} Review: Pros, Cons, Pricing & Best Use Cases</h2>

<p>Welcome to <strong>IDE Guide</strong>! Today we evaluate <code>{ide['name']}</code> developed by <strong>{ide['developer']}</strong>. In this review, we cover key features, performance benchmark insights, pricing tier details, and help you determine whether it fits your developer workflow.</p>

<p><amp-img width="800" height="450" layout="responsive" src="{ide['image_url']}" alt="{ide['name']} workspace preview"></amp-img></p>

<h3>Key Details at a Glance</h3>
<ul>
  <li><strong>Category:</strong> {ide['category']}</li>
  <li><strong>Developer:</strong> {ide['developer']}</li>
  <li><strong>Pricing Model:</strong> {ide['pricing']} ({paid_badge})</li>
  <li><strong>Recommended Target:</strong> {ide['best_for']}</li>
</ul>

<h3>The Good: Key Strengths</h3>
<ul>
  {strengths_html}
</ul>

<h3>The Bad: Drawbacks & Limitations</h3>
<ul>
  {weaknesses_html}
</ul>

<h3>Pricing & Licensing Breakdown</h3>
<p><strong>{ide['name']}</strong> is offered as <em>{ide['pricing']}</em>. {"Keep in mind that paid tiers unlock advanced team collaboration, high-priority AI latency, or specialized database tools." if ide['is_paid'] else "As a free tool, it provides high accessibility for open-source developers and students without licensing costs."}</p>

<h3>Final Verdict: Who Should Use {ide['name']}?</h3>
<p>If you are looking for <strong>{ide['category']}</strong>, {ide['name']} is a top-tier candidate. It is especially ideal for <strong>{ide['best_for']}</strong>.</p>

<hr />
<p><em>{DISCLAIMER_TEXT}</em></p>
"""


def generate_google_flow_video_spec(ide: Dict[str, Any]) -> str:
    return f"""# Google Flow Video Generation Spec: {ide['name']}
# Target Platform: YouTube (@IDEguide Shorts / Video)
# Aspect Ratio: 9:16 (Shorts) / 16:9 (Full Review)
# Duration: ~60 Seconds

## Scene Breakdown & AI Camera Prompts

### Scene 1: Hook (0:00 - 0:08)
- **Visual Prompt**: Cinematic close-up of a developer typing dark-mode code on a mechanical keyboard with RGB ambient backlight, camera sweeping smoothly across the screen displaying {ide['name']} interface.
- **On-Screen Text**: Is {ide['name']} Worth It in 2026?
- **Voiceover Script**: "Looking for the ultimate code editor? Today on IDE Guide, we review {ide['name']} by {ide['developer']}."
- **B-Roll Prompt**: Fast cut of IDE launch animation and syntax highlighting preview.

### Scene 2: Top Features & Pros (0:08 - 0:28)
- **Visual Prompt**: Macro split-screen shot showing high-speed autocomplete, extension marketplace, and responsive terminal execution in {ide['name']}.
- **On-Screen Text**: Strengths: {ide['strengths'][0][:40]}
- **Voiceover Script**: "Here is why developers love it: First, {ide['strengths'][0]} Second, {ide['strengths'][1]}"
- **B-Roll Prompt**: High-tech UI workflow rendering with glowing cursor trail.

### Scene 3: Drawbacks & Gotchas (0:28 - 0:42)
- **Visual Prompt**: High-contrast dark tone overlay showing memory/CPU load gauge or setup panel.
- **On-Screen Text**: Limitations & Drawbacks
- **Voiceover Script**: "What about the downsides? {ide['weaknesses'][0]}"
- **B-Roll Prompt**: System monitor graph animation with warning icon highlight.

### Scene 4: Pricing & Verdict (0:42 - 0:60)
- **Visual Prompt**: Sleek clean card graphic showing '{ide['pricing']}' and recommended user profiles.
- **On-Screen Text**: Pricing: {ide['pricing']} | Best For: {ide['best_for']}
- **Voiceover Script**: "Pricing is {ide['pricing']}. It is best for {ide['best_for']}. Visit ideguide.blogspot.com for the full detailed writeup!"
- **B-Roll Prompt**: Channel end-screen with YouTube subscribe button and Blogspot URL overlay.

---
{DISCLAIMER_TEXT}
"""


def main():
    date_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    out_dir = os.path.join("content", date_str)
    os.makedirs(out_dir, exist_ok=True)

    selected_ides = select_daily_ides(count=3, history_file="content/history.json")

    print(f"Generating 3 content packages for date: {date_str}...")

    for i, ide in enumerate(selected_ides, 1):
        slug = ide["id"]

        # 1. AMP Blog Post
        blog_post_path = os.path.join(out_dir, f"blog_post_{i}_{slug}.html")
        blog_content = generate_amp_blog_post(ide)
        with open(blog_post_path, 'w', encoding='utf-8') as f:
            f.write(blog_content)

        # 2. Google Flow Video Spec
        video_spec_path = os.path.join(out_dir, f"video_spec_{i}_{slug}.md")
        video_spec_content = generate_google_flow_video_spec(ide)
        with open(video_spec_path, 'w', encoding='utf-8') as f:
            f.write(video_spec_content)

        print(f" Package {i}: {ide['name']}")
        print(f"   - Blog Post: {blog_post_path}")
        print(f"   - Video Spec: {video_spec_path}")

    print("Daily content generation complete!")


if __name__ == "__main__":
    main()
