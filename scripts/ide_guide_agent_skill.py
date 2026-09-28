#!/usr/bin/env python3
"""
IDE Guide Agentic CLI Skill Tool.
Generates AMP HTML blog post (for ideguide.blogspot.com) and Google Flow AI video specifications
(for @IDEguide YouTube videos and shorts) on demand for a given IDE name or repository URL.
"""

import argparse
import json
import os
import re
import sys
import urllib.request
from typing import Dict, Any

MANDATORY_DISCLAIMER = (
    "Disclaimer: IDE Guide is an independent technical publication. "
    "This content is not sponsored, endorsed, or affiliated with any software vendor or editor developer mentioned above. "
    "All reviews and assessments are based strictly on objective developer evaluation."
)

DEFAULT_IDE_KNOWLEDGE_BASE = {
    "cursor": {
        "name": "Cursor",
        "category": "AI-First Code Editor",
        "pricing_tier": "Freemium (Free hobby tier, $20/mo Pro)",
        "is_paid": True,
        "is_free_tier": True,
        "description": "An AI-first code editor built as a fork of VS Code, featuring inline code generation, multi-file editing (Composer), and terminal AI assistance.",
        "pros": [
            "Deep multi-file codebase indexing and context understanding",
            "Agentic editing capability (Composer)",
            "Seamless transition for VS Code users due to extension compatibility",
            "Fast inline auto-suggestions powered by frontier models"
        ],
        "cons": [
            "Fast AI model usage is capped on free tier",
            "Requires internet connection for full AI capabilities",
            "High token usage cost on heavy commercial projects"
        ],
        "verdict": "Best for developers looking for bleeding-edge AI assistance and multi-file code generation without leaving the familiar VS Code interface.",
        "image_url": "https://images.unsplash.com/photo-1555066931-4365d14bab8c"
    },
    "zed": {
        "name": "Zed Editor",
        "category": "High-Performance Code Editor",
        "pricing_tier": "Free & Open Source (Paid AI features available)",
        "is_paid": False,
        "is_free_tier": True,
        "description": "A high-performance, multi-player code editor written in Rust by the creators of Atom and Tree-sitter, optimized for GPU rendering and sub-millisecond response.",
        "pros": [
            "Extremely fast boot time and lightweight memory footprint",
            "Native GPU-accelerated text rendering",
            "Built-in multiplayer collaborative editing",
            "Open source codebase"
        ],
        "cons": [
            "Ecosystem of extensions is still maturing compared to VS Code",
            "Limited platform availability on older operating systems",
            "AI features require external API key or subscription"
        ],
        "verdict": "Ideal for performance enthusiasts, Rust/C++/Go developers, and teams looking for real-time pair programming speed.",
        "image_url": "https://images.unsplash.com/photo-1542831371-29b0f74f9713"
    },
    "neovim": {
        "name": "Neovim",
        "category": "Extensible Modal Text Editor",
        "pricing_tier": "100% Free & Open Source",
        "is_paid": False,
        "is_free_tier": True,
        "description": "A hyperextensible Vim-based text editor built for high-speed modal editing, Lua plugin ecosystems, and full keyboard-driven productivity.",
        "pros": [
            "Ultra-lightweight, runs in terminal or GUI wrappers",
            "Infinitely customizable via Lua scripting",
            "Native LSP support and fast treesitter syntax highlighting",
            "Completely free with zero telemetry or lock-in"
        ],
        "cons": [
            "Steep learning curve for modal navigation and configuration",
            "Requires manual setup for complex IDE features out of the box",
            "Keybindings require muscle memory investment"
        ],
        "verdict": "Unbeatable for keyboard purists, terminal lovers, and power developers seeking total control over their editing environment.",
        "image_url": "https://images.unsplash.com/photo-1618401471353-b98afee0b2eb"
    },
    "windsurf": {
        "name": "Windsurf Editor",
        "category": "Agentic AI IDE",
        "pricing_tier": "Freemium (Free starter, $15/mo Pro)",
        "is_paid": True,
        "is_free_tier": True,
        "description": "An agentic AI-powered IDE by Codeium featuring Flows and Cascade AI agent for real-time context integration and collaborative development.",
        "pros": [
            "Cascade agent provides deep context-aware code refactoring",
            "Seamless VS Code extension compatibility",
            "Generous free tier provided by Codeium infrastructure",
            "Integrated terminal and command execution assistance"
        ],
        "cons": [
            "Newer product with evolving UI paradigms",
            "Relies on cloud model connectivity for advanced agent flows"
        ],
        "verdict": "Great for developers who want an agentic AI copilot that acts as a true pair programmer rather than just an autocomplete tool.",
        "image_url": "https://images.unsplash.com/photo-1517694712202-14dd9538aa97"
    },
    "pycharm": {
        "name": "PyCharm",
        "category": "Full-Featured Python IDE",
        "pricing_tier": "Freemium (Free Community Edition / $249/yr Professional)",
        "is_paid": True,
        "is_free_tier": True,
        "description": "JetBrains' dedicated Python IDE providing comprehensive code inspection, visual debugging, database tools, and framework support.",
        "pros": [
            "Best-in-class Python refactoring, type checking, and debugging",
            "Out-of-the-box support for Django, Flask, FastAPI, and Jupyter notebooks",
            "Powerful built-in database viewer and git tooling"
        ],
        "cons": [
            "Heavy memory footprint and slower startup compared to light editors",
            "Full feature set requires paid Professional license"
        ],
        "verdict": "The gold standard for professional Python backend, Django, and data engineering developers.",
        "image_url": "https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5"
    }
}


def fetch_github_metadata(repo_url: str) -> Dict[str, Any]:
    """Extracts metadata from a GitHub repository URL if provided."""
    match = re.search(r"github\.com/([^/]+)/([^/]+)", repo_url)
    if not match:
        return {}
    owner, repo = match.group(1), match.group(2).replace(".git", "")
    api_url = f"https://api.github.com/repos/{owner}/{repo}"

    try:
        req = urllib.request.Request(api_url, headers={"User-Agent": "IDEGuideAgentSkill"})
        with urllib.request.urlopen(req, timeout=5) as resp:
            if resp.status == 200:
                data = json.loads(resp.read().decode('utf-8'))
                return {
                    "name": data.get("name", repo).capitalize(),
                    "description": data.get("description") or f"A modern code editor / tool repository: {owner}/{repo}.",
                    "stars": data.get("stargazers_count", 0),
                    "license": (data.get("license") or {}).get("name", "Open Source"),
                    "category": "Open Source Editor / Tool"
                }
    except Exception:
        pass
    return {}


def get_ide_info(query: str) -> Dict[str, Any]:
    """Resolves IDE information from local knowledge base or GitHub API fallback."""
    query_clean = query.strip().lower()

    # Check direct key or sub-match
    for key, data in DEFAULT_IDE_KNOWLEDGE_BASE.items():
        if key in query_clean or query_clean in key or data["name"].lower() in query_clean:
            return data

    # Check if query is a GitHub URL
    if "github.com" in query_clean:
        gh_meta = fetch_github_metadata(query)
        if gh_meta:
            return {
                "name": gh_meta["name"],
                "category": gh_meta["category"],
                "pricing_tier": f"Free & Open Source ({gh_meta['license']})",
                "is_paid": False,
                "is_free_tier": True,
                "description": gh_meta["description"],
                "pros": [
                    f"Open source community backed ({gh_meta['stars']:,} GitHub stars)",
                    "Transparent codebase and community driven development",
                    "Customizable and flexible integration"
                ],
                "cons": [
                    "May require self-building or manual setup for edge features",
                    "Community support reliance for bug resolutions"
                ],
                "verdict": f"A promising open-source development tool with active community interest on GitHub.",
                "image_url": "https://images.unsplash.com/photo-1555066931-4365d14bab8c"
            }

    # Generic Fallback
    formatted_name = query.strip().title()
    return {
        "name": formatted_name,
        "category": "Development Environment & Code Editor",
        "pricing_tier": "Freemium / Proprietary (Check official vendor site)",
        "is_paid": True,
        "is_free_tier": True,
        "description": f"{formatted_name} is a modern development environment designed to streamline software engineering workflows.",
        "pros": [
            f"Tailored workflow optimizations for modern software stacks",
            "Comprehensive developer tool integrations",
            "Active developer community and plugin ecosystem"
        ],
        "cons": [
            "Requires evaluation for specific team workflows",
            "Resource usage varies depending on active extensions"
        ],
        "verdict": f"Worth testing for developers seeking modern features tailored for {formatted_name}.",
        "image_url": "https://images.unsplash.com/photo-1555066931-4365d14bab8c"
    }


def generate_amp_blog_post(info: Dict[str, Any]) -> str:
    """Generates a strict Blogger AMP HTML post."""
    name = info["name"]
    category = info["category"]
    pricing = info["pricing_tier"]
    description = info["description"]
    pros_html = "".join([f"<li><strong>{p}</strong></li>" for p in info["pros"]])
    cons_html = "".join([f"<li>{c}</li>" for c in info["cons"]])
    verdict = info["verdict"]
    img_url = info.get("image_url", "https://images.unsplash.com/photo-1555066931-4365d14bab8c")

    paid_status_badge = "FREE" if not info["is_paid"] else ("FREEMIUM" if info["is_free_tier"] else "PAID")

    html = f"""<!-- Blogger AMP HTML Post for ideguide.blogspot.com -->
<div class="ide-guide-post">
  <div class="header-banner">
    <span class="badge badge-{paid_status_badge.lower()}">{paid_status_badge}</span>
    <span class="category-tag">{category}</span>
    <h1>{name} Review: Features, Pros & Cons, and Pricing Guide</h1>
    <p class="pricing-summary"><strong>Pricing Model:</strong> {pricing}</p>
  </div>

  <div class="visual-hero">
    <amp-img src="{img_url}"
             width="800"
             height="450"
             layout="responsive"
             alt="{name} Code Editor Interface Overview">
    </amp-img>
  </div>

  <section class="overview-section">
    <h2>Overview</h2>
    <p>{description}</p>
  </section>

  <section class="analysis-section">
    <h2>Pros & Strengths</h2>
    <ul>
      {pros_html}
    </ul>

    <h2>Cons & Tradeoffs</h2>
    <ul>
      {cons_html}
    </ul>
  </section>

  <section class="verdict-section">
    <h2>Final Verdict & Recommendation</h2>
    <p>{verdict}</p>
  </section>

  <footer class="disclaimer-footer">
    <hr />
    <p><strong>{MANDATORY_DISCLAIMER}</strong></p>
  </footer>
</div>"""
    return html


def generate_google_flow_video_spec(info: Dict[str, Any]) -> Dict[str, Any]:
    """Generates Google Flow AI video specification and prompts for YouTube & Shorts."""
    name = info["name"]
    category = info["category"]
    pricing = info["pricing_tier"]
    pros = ", ".join(info["pros"][:2])
    cons = ", ".join(info["cons"][:2])

    return {
        "channel": "@IDEguide",
        "ide_name": name,
        "category": category,
        "pricing_model": pricing,
        "google_flow_prompts": {
            "landscape_16_9": [
                {
                    "scene": 1,
                    "title": "Hook & Intro",
                    "duration_seconds": 15,
                    "visual_prompt": f"Cinematic slow push-in camera movement over a modern dark mode code editor displaying {name} interface. Neon cyan syntax highlighting glowing on high resolution 8K screen, soft bokeh studio background.",
                    "voiceover_script": f"Is {name} the ultimate {category} for your dev setup? Let's break down the good, the bad, and whether it is worth your time!"
                },
                {
                    "scene": 2,
                    "title": "Key Features & Showcase",
                    "duration_seconds": 30,
                    "visual_prompt": f"Dynamic pan left to right across {name} code window showing rapid autocomplete and crisp text rendering. Minimalist mahogany desk setup, warm aesthetic ambient backlighting.",
                    "voiceover_script": f"Here is what makes {name} stand out: {pros}."
                },
                {
                    "scene": 3,
                    "title": "Pros, Cons & Pricing Tier",
                    "duration_seconds": 30,
                    "visual_prompt": f"Clean glassmorphic split screen infographic showing Free vs Paid features for {name}. Left side highlights pros, right side highlights tradeoffs. Modern tech typography.",
                    "voiceover_script": f"When it comes to pricing, {name} operates under a {pricing} model. Important tradeoffs to keep in mind include {cons}."
                },
                {
                    "scene": 4,
                    "title": "Verdict & Outro",
                    "duration_seconds": 15,
                    "visual_prompt": f"Smooth tilt up to developer smiling in modern workspace, lower third showing ideguide.blogspot.com and YouTube @IDEguide subscription button.",
                    "voiceover_script": f"Final Verdict: {info['verdict']} Read our full AMP article at ideguide.blogspot.com and subscribe to @IDEguide for daily editor breakdowns!"
                }
            ],
            "vertical_shorts_9_16": [
                {
                    "scene": 1,
                    "duration_seconds": 15,
                    "visual_prompt": f"Vertical 9:16 macro shot of {name} IDE interface with glowing syntax animations and fast-paced motion graphics overlaying key specs.",
                    "voiceover_script": f"Should you switch to {name}? Here is the 30-second breakdown on this {category}!"
                },
                {
                    "scene": 2,
                    "duration_seconds": 30,
                    "visual_prompt": f"Vertical fast-cuts between code editing in {name}, feature checklist, and price comparison badge: {pricing}.",
                    "voiceover_script": f"Top Pros: {pros}. Main Tradeoff: {cons}. Pricing tier: {pricing}."
                },
                {
                    "scene": 3,
                    "duration_seconds": 15,
                    "visual_prompt": f"Vertical closing frame with animated text 'Full Review at ideguide.blogspot.com' and @IDEguide handle.",
                    "voiceover_script": "Check the link in bio for our full AMP review on Blogger and subscribe to @IDEguide!"
                }
            ]
        },
        "disclaimer": MANDATORY_DISCLAIMER
    }


def main():
    parser = argparse.ArgumentParser(description="IDE Guide Agentic CLI Skill Tool")
    parser.add_argument("query", help="IDE Name or GitHub repo URL (e.g., 'Cursor', 'Zed', 'https://github.com/lapce/lapce')")
    parser.add_argument("--output-dir", help="Directory to save generated AMP post and Video spec JSON", default=".")

    args = parser.parse_args()
    info = get_ide_info(args.query)

    amp_html = generate_amp_blog_post(info)
    video_spec = generate_google_flow_video_spec(info)

    safe_name = re.sub(r'[^a-zA-Z0-9_-]', '_', info['name'].lower())
    os.makedirs(args.output_dir, exist_ok=True)

    blog_file = os.path.join(args.output_dir, f"{safe_name}_amp_blog.html")
    video_file = os.path.join(args.output_dir, f"{safe_name}_video_spec.json")

    with open(blog_file, "w", encoding="utf-8") as f:
        f.write(amp_html)

    with open(video_file, "w", encoding="utf-8") as f:
        json.dump(video_spec, f, indent=2)

    print(f"✨ IDE Guide Agent Skill completed for: {info['name']}")
    print(f"  - AMP Blog Post: {blog_file}")
    print(f"  - Google Flow Video Spec: {video_file}")


if __name__ == "__main__":
    main()
