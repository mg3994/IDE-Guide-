#!/usr/bin/env python3
"""
Agentic CLI Skill Tool for IDE Guide.
Generates on-demand AMP HTML blog posts and Google Flow video specifications for any IDE, code editor, or GitHub repo URL.
"""

import sys
import argparse
import os
import json
import re
from typing import Dict, Any

# Ensure parent directory is in path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from scripts.amp_validator import validate_amp_html, MANDATORY_DISCLAIMER

# Database of detailed IDE profiles for rich content generation
IDE_DATABASE: Dict[str, Dict[str, Any]] = {
    "vs code": {
        "name": "Visual Studio Code",
        "vendor": "Microsoft",
        "pricing": "Free & Open Source (Core / MIT), Free build (VSCodium)",
        "pricing_type": "Free / Open Source",
        "pros": [
            "Massive extension marketplace with thousands of extensions.",
            "Lightweight startup and high extensibility.",
            "Integrated terminal, git controls, and remote development support.",
            "Strong multi-language support out of the box."
        ],
        "cons": [
            "Can consume significant RAM with many heavy extensions active.",
            "Lacks full out-of-the-box IDE features compared to dedicated suites without plugins.",
            "Telemetry enabled by default in official Microsoft build."
        ],
        "best_for": "Web developers, polyglot programmers, and full-stack engineers seeking flexibility.",
        "category": "Code Editor / Light IDE"
    },
    "intellij": {
        "name": "JetBrains IntelliJ IDEA",
        "vendor": "JetBrains",
        "pricing": "Freemium (Community Edition Free / Ultimate Edition Paid $169+/yr)",
        "pricing_type": "Paid / Freemium",
        "pros": [
            "Industry-leading Java, Kotlin, and JVM refactoring tools.",
            "Deep static analysis and intelligent code completion.",
            "Comprehensive built-in database, spring, and framework integrations in Ultimate."
        ],
        "cons": [
            "High memory usage (2GB+ RAM baseline).",
            "Slower indexing on massive codebases.",
            "Ultimate Edition requires paid subscription."
        ],
        "best_for": "Enterprise Java/Kotlin developers and backend microservice engineers.",
        "category": "Integrated Development Environment"
    },
    "cursor": {
        "name": "Cursor AI Code Editor",
        "vendor": "Anysphere",
        "pricing": "Freemium (Free tier available / Pro $20/mo)",
        "pricing_type": "Paid / Freemium",
        "pros": [
            "Deep native AI code generation and multi-file editing context.",
            "Full compatibility with VS Code extensions.",
            "Composer feature for automated project-wide refactoring."
        ],
        "cons": [
            "Requires active internet connection for advanced LLM features.",
            "Pro subscription cost for heavy usage.",
            "Potential privacy concerns for sensitive enterprise codebases without privacy mode."
        ],
        "best_for": "AI-first software engineers and rapid prototyping developers.",
        "category": "AI Code Editor"
    },
    "neovim": {
        "name": "Neovim",
        "vendor": "Community / Open Source",
        "pricing": "Free & Open Source (Apache 2.0)",
        "pricing_type": "Free / Open Source",
        "pros": [
            "Unmatched keyboard speed and modal editing efficiency.",
            "Extensible via Lua with built-in Language Server Protocol (LSP).",
            "Ultra lightweight with near-instant boot times and minimal RAM."
        ],
        "cons": [
            "Steep initial learning curve for modal navigation.",
            "Requires manual configuration and maintenance for IDE-like features.",
            "No native GUI by default (terminal-centric)."
        ],
        "best_for": "Terminal power users, DevOps engineers, and minimalist developers.",
        "category": "Terminal Text Editor"
    },
    "zed": {
        "name": "Zed Editor",
        "vendor": "Zed Industries",
        "pricing": "Free & Open Source (GPL/Apache 2.0)",
        "pricing_type": "Free / Open Source",
        "pros": [
            "Blazing fast Rust-based GPUI rendering at 120 FPS.",
            "Built-in collaborative multiplayer editing.",
            "Native tree-sitter integration and fast startup."
        ],
        "cons": [
            "Ecosystem still growing compared to VS Code.",
            "Currently Linux and macOS focused with ongoing Windows port.",
            "Fewer niche language extensions."
        ],
        "best_for": "Performance enthusiasts, Rust developers, and real-time pair programmers.",
        "category": "Next-Gen Code Editor"
    },
    "sublime text": {
        "name": "Sublime Text 4",
        "vendor": "Sublime HQ",
        "pricing": "Paid ($99 evaluation model)",
        "pricing_type": "Paid",
        "pros": [
            "Instant launch speed and tiny memory footprint.",
            "Smooth GPU rendering and multi-caret editing.",
            "Extensive Package Control system."
        ],
        "cons": [
            "Paid license required for full compliance.",
            "Fewer out-of-the-box AI features compared to newer editors.",
            "Closed source core engine."
        ],
        "best_for": "Developers who prioritize raw speed, low memory footprint, and distraction-free text editing.",
        "category": "High Performance Text Editor"
    },
    "pycharm": {
        "name": "JetBrains PyCharm",
        "vendor": "JetBrains",
        "pricing": "Freemium (Community Free / Professional Paid $99+/yr)",
        "pricing_type": "Paid / Freemium",
        "pros": [
            "Best-in-class Python debugging, profiling, and virtualenv management.",
            "Native Django, Flask, and data science notebook support in Pro.",
            "Superior refactoring and inspection tools."
        ],
        "cons": [
            "Heavier memory footprint.",
            "Slow startup time compared to lightweight editors.",
            "Professional edition needed for full web/database features."
        ],
        "best_for": "Python developers, data engineers, and web backend architects.",
        "category": "Python IDE"
    },
    "windsurf": {
        "name": "Windsurf Editor",
        "vendor": "Codeium",
        "pricing": "Freemium (Free tier / Pro $15/mo)",
        "pricing_type": "Paid / Freemium",
        "pros": [
            "Flow paradigm seamlessly merging human developer intent with AI agent execution.",
            "Deep codebase contextual indexing and instant suggestion response.",
            "Full VS Code plugin ecosystem support."
        ],
        "cons": [
            "Cloud dependency for complex AI reasoning flow.",
            "Paid tier required for high quota AI flows."
        ],
        "best_for": "Developers wanting collaborative AI agents integrated directly into their workspace.",
        "category": "AI Flow Editor"
    }
}


def derive_ide_info(ide_name: str = "", repo_url: str = "") -> Dict[str, Any]:
    """Extracts or builds structured profile data for an IDE or repository URL."""
    target_key = (ide_name or "").strip().lower()

    if not target_key and repo_url:
        # Extract repo name from URL
        clean_url = repo_url.rstrip("/")
        repo_name = clean_url.split("/")[-1].replace(".git", "")
        target_key = repo_name.lower()

    # Search in database
    for key, data in IDE_DATABASE.items():
        if key in target_key or target_key in key:
            return data

    # Default fallback profile for unknown IDEs or repos
    formatted_name = ide_name or (repo_url.split("/")[-1] if repo_url else "Custom Code Editor")
    return {
        "name": formatted_name,
        "vendor": "Independent / Open Source",
        "pricing": "Free / Open Source or Proprietary (Check Official Repository)",
        "pricing_type": "Free / Paid",
        "pros": [
            f"Tailored developer tools and workflows for {formatted_name}.",
            "Modern syntax highlighting and project workspace management.",
            "Active developer community and configurable settings."
        ],
        "cons": [
            "Specialized feature set that may require plugin extensions.",
            "Resource usage varies based on loaded files and dependencies."
        ],
        "best_for": f"Software engineers interested in exploring {formatted_name}.",
        "category": "Code Editor / Software Development Environment"
    }


def generate_amp_blog_post(info: Dict[str, Any]) -> str:
    """Generates AMP HTML compliant blog post string for Blogger."""
    name = info["name"]
    vendor = info["vendor"]
    pricing = info["pricing"]
    best_for = info["best_for"]
    category = info["category"]

    pros_lis = "".join([f"<li><strong>{p.split(':')[0] if ':' in p else 'Key Advantage'}:</strong> {p}</li>" for p in info["pros"]])
    cons_lis = "".join([f"<li><strong>{c.split(':')[0] if ':' in c else 'Consideration'}:</strong> {c}</li>" for c in info["cons"]])

    post_html = f"""<article class="ide-guide-post">
  <header>
    <h1>{name} Review: Features, Good & Bad, Pricing, and Recommendation</h1>
    <p class="meta">Category: {category} | Developer: {vendor} | Evaluation Date: 2025</p>
  </header>

  <section class="overview">
    <h2>Overview of {name}</h2>
    <p>In this technical breakdown by <strong>IDE Guide</strong>, we evaluate <strong>{name}</strong>—a popular {category} developed by {vendor}. Selecting the right development environment directly impacts productivity, code quality, and daily developer ergonomics.</p>

    <figure class="ide-media">
      <amp-img src="https://images.unsplash.com/photo-1555066931-4365d14bab8c?auto=format&fit=crop&w=1200&q=80" width="800" height="450" layout="responsive" alt="{name} Code Editor Screenshot"></amp-img>
      <figcaption>{name} Workspace & Code Editing Interface</figcaption>
    </figure>
  </section>

  <section class="good-and-bad">
    <h2>The Good & The Bad (Pros and Cons)</h2>

    <div class="pros-section">
      <h3>The Good (Pros)</h3>
      <ul>
        {pros_lis}
      </ul>
    </div>

    <div class="cons-section">
      <h3>The Bad (Cons)</h3>
      <ul>
        {cons_lis}
      </ul>
    </div>
  </section>

  <section class="pricing">
    <h2>Pricing Model & License</h2>
    <p><strong>Pricing:</strong> {pricing}</p>
    <p>Understanding whether an IDE is free, open source, or subscription-based is critical for team budgeting and developer adoption.</p>
  </section>

  <section class="verdict">
    <h2>Verdict: Is {name} Best For You?</h2>
    <p><strong>Recommendation:</strong> {name} is best suited for {best_for}</p>
    <p>When selecting your core editor, balance memory consumption and startup speed against the depth of native refactoring tools you need daily.</p>
  </section>

  <footer class="disclaimer-footer">
    <hr>
    <p class="disclaimer">{MANDATORY_DISCLAIMER}</p>
  </footer>
</article>"""

    return post_html


def generate_google_flow_spec(info: Dict[str, Any]) -> Dict[str, Any]:
    """Generates Google Flow video generation specification JSON object."""
    name = info["name"]
    pricing = info["pricing"]
    best_for = info["best_for"]

    spec = {
        "channel": "IDE Guide (@IDEguide)",
        "video_title": f"{name} - Is It Worth Using? (Good vs Bad & Pricing)",
        "target_platform": "YouTube Shorts (9:16) & YouTube Video (16:9)",
        "aspect_ratio": "16:9 / 9:16",
        "duration_seconds": 60,
        "ide_name": name,
        "visual_style": {
            "lighting": "Modern tech studio ambient lighting, dark theme editor contrast with cyan/teal neon accents",
            "camera_framing": "Close-up macro of code cursor typing, over-the-shoulder coding shot, side-by-side spec comparison card",
            "color_palette": ["#1e1e2e", "#89dceb", "#cdd6f4", "#f38ba8"]
        },
        "timeline_scenes": [
            {
                "scene": 1,
                "timestamp": "00:00 - 00:10",
                "narration": f"Is {name} the ultimate code editor for your workflow, or does it hog too much memory? Let's break down the good, the bad, and the pricing.",
                "google_flow_prompt": f"Macro cinematic zoom into a dark-themed computer monitor displaying {name} code editor with syntax highlighted Python code, soft background depth of field, neon key lighting, 4k ultra realistic."
            },
            {
                "scene": 2,
                "timestamp": "00:10 - 00:25",
                "narration": f"First, the good: {info['pros'][0]} Plus, {info['pros'][1]}",
                "google_flow_prompt": f"Split screen visual showing high speed developer workflow, glowing checkmarks appearing next to speed and extensibility metrics, sleek dark UI animation."
            },
            {
                "scene": 3,
                "timestamp": "00:25 - 00:40",
                "narration": f"Now for the bad: {info['cons'][0]} Be mindful when running massive projects.",
                "google_flow_prompt": f"Close up camera shift to memory graph meter turning amber red, showing high RAM usage warning overlay on clean developer desk setup."
            },
            {
                "scene": 4,
                "timestamp": "00:40 - 00:55",
                "narration": f"Pricing breakdown: {pricing}. Verdict: {best_for}",
                "google_flow_prompt": f"Futuristic holographic badge displaying '{info['pricing_type']}' floating over mechanical keyboard on dark wooden studio table."
            },
            {
                "scene": 5,
                "timestamp": "00:55 - 01:00",
                "narration": f"Subscribe to IDE Guide for daily objective IDE breakdowns!",
                "google_flow_prompt": f"Sleek ending card with YouTube subscribe animation, text displaying IDE Guide, dark mode aesthetic."
            }
        ],
        "disclaimer": MANDATORY_DISCLAIMER
    }
    return spec


def main():
    parser = argparse.ArgumentParser(description="IDE Guide Agentic Skill Tool")
    parser.add_argument("--ide", type=str, default="", help="Name of the IDE or Code Editor (e.g., 'VS Code', 'Neovim')")
    parser.add_argument("--repo", type=str, default="", help="GitHub repository URL of the editor")
    parser.add_argument("--out-dir", type=str, default="output", help="Directory to save generated files")
    parser.add_argument("--format", type=str, choices=["html", "flow_spec", "all"], default="all", help="Output format")

    args = parser.parse_args()

    if not args.ide and not args.repo:
        parser.print_help()
        print("\nError: Please specify either --ide or --repo")
        sys.exit(1)

    info = derive_ide_info(args.ide, args.repo)
    os.makedirs(args.out_dir, exist_ok=True)

    slug = re.sub(r'[^a-z0-9]+', '_', info["name"].lower()).strip('_')

    if args.format in ["html", "all"]:
        blog_html = generate_amp_blog_post(info)
        # Validate AMP HTML
        is_valid, errors = validate_amp_html(blog_html)
        if not is_valid:
            print("⚠️ AMP Validation Errors detected during generation:")
            for err in errors:
                print(f"  - {err}")

        html_path = os.path.join(args.out_dir, f"{slug}_post.html")
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(blog_html)
        print(f"✅ Generated AMP Blog Post saved to: {html_path}")

    if args.format in ["flow_spec", "all"]:
        flow_spec = generate_google_flow_spec(info)
        spec_path = os.path.join(args.out_dir, f"{slug}_flow_spec.json")
        with open(spec_path, "w", encoding="utf-8") as f:
            json.dump(flow_spec, f, indent=2)
        print(f"✅ Generated Google Flow Video Spec saved to: {spec_path}")


if __name__ == "__main__":
    main()
