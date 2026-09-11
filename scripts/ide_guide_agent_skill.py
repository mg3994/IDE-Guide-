#!/usr/bin/env python3
"""
IDE Guide Agentic Skill Tool
-----------------------------
Generates AMP (Accelerated Mobile Pages) HTML blog posts (for Blogger https://ideguide.blogspot.com/)
and Google Flow video prompt specifications (for YouTube @IDEguide) for any specified IDE or editor repository.

Usage:
  python3 scripts/ide_guide_agent_skill.py --ide "Cursor IDE" --pricing "Freemium" --output-dir "output/"
  python3 scripts/ide_guide_agent_skill.py --repo "https://github.com/zed-industries/zed" --output-dir "output/"
"""

import argparse
import datetime
import json
import os
import re
import sys
import urllib.request

DISCLAIMER_TEXT = (
    "Disclaimer: IDE Guide is an independent technical publication. "
    "This content is not sponsored, endorsed, or affiliated with any software vendor or editor developer mentioned above. "
    "All reviews and assessments are based strictly on objective developer evaluation."
)

KNOWN_IDES_DATABASE = {
    "cursor": {
        "name": "Cursor IDE",
        "description": "An AI-first code editor built as a fork of VS Code, featuring inline AI generation, chat with codebase context, and multi-file editing.",
        "pricing": "Freemium ($20/mo for Pro)",
        "pros": ["Native AI codebase indexing", "Seamless migration from VS Code extensions", "Fast inline AI completions", "Multi-file edit apply"],
        "cons": ["Proprietary closed-source features", "Subscription required for heavy AI usage", "Occasional high memory consumption"],
        "recommendation": "Best for web developers and AI engineers seeking maximum productivity through LLM integration.",
        "category": "AI Code Editor"
    },
    "zed": {
        "name": "Zed Editor",
        "description": "A high-performance, multi-player code editor written in Rust, engineered for speed, responsiveness, and minimal resource overhead.",
        "pricing": "Free & Open Source",
        "pros": ["Blazing fast startup and rendering (120 FPS)", "Low RAM footprint written in Rust", "Built-in collaborative pair programming", "Native AI integration"],
        "cons": ["Ecosystem plugins still maturing", "Linux/Windows support newer than macOS", "Fewer extensions compared to VS Code"],
        "recommendation": "Ideal for performance-obsessed developers and systems programmers wanting instant UI feedback.",
        "category": "High-Performance Editor"
    },
    "vs code": {
        "name": "Visual Studio Code",
        "description": "The world's most popular lightweight, highly extensible open-source code editor developed by Microsoft.",
        "pricing": "Free (Open Source core)",
        "pros": ["Massive extension marketplace", "Ubiquitous community support", "Integrated terminal & debugging", "Rich language support"],
        "cons": ["Electron-based memory usage", "Telemetry enabled by default", "Can become slow with heavily loaded plugins"],
        "recommendation": "The golden standard for general-purpose web, backend, and cloud developers.",
        "category": "General Purpose IDE"
    },
    "neovim": {
        "name": "Neovim",
        "description": "Hyperextensible Vim-based text editor seeking to maximize usability, extensibility, and modern Lua scripting capabilities.",
        "pricing": "Free & Open Source",
        "pros": ["Ultra lightweight and blazing fast", "Infinite customization via Lua", "Keyboard-centric modal workflow", "Zero GUI memory overhead"],
        "cons": ["Steep learning curve", "Requires manual setup/configuration", "Not beginner friendly"],
        "recommendation": "Essential for terminal power users, DevOps engineers, and keyboard purists.",
        "category": "Terminal Editor"
    },
    "fleet": {
        "name": "JetBrains Fleet",
        "description": "A lightweight distributed code editor built by JetBrains with smart completion, smart mode, and multi-language support.",
        "pricing": "Freemium / JetBrains Subscription",
        "pros": ["Sleek minimalist UI", "Smart Mode powered by JetBrains code intelligence", "Lightweight startup", "Remote collaboration support"],
        "cons": ["Still evolving feature set", "Paid subscription needed for full smart mode feature set", "Smaller plugin ecosystem"],
        "recommendation": "Great for JetBrains lovers looking for a lightweight VS Code alternative.",
        "category": "Lightweight IDE"
    },
    "windsurf": {
        "name": "Windsurf Editor",
        "description": "An agentic IDE built by Codeium that combines AI flow states with deep codebase reasoning and interactive cascading edits.",
        "pricing": "Freemium ($15/mo for Pro)",
        "pros": ["Deep agentic codebase understanding", "Real-time AI cascade reasoning", "Smooth VS Code fork UI", "Generous free tier"],
        "cons": ["Requires active internet connection for agent features", "Closed-source server agent", "Resource intensive during deep scans"],
        "recommendation": "Perfect for modern full-stack developers seeking agentic AI workflow integration.",
        "category": "Agentic AI Editor"
    }
}


def fetch_github_repo_info(repo_url):
    """Optionally fetch basic repository information from GitHub API if URL provided."""
    match = re.search(r"github\.com/([^/]+)/([^/]+)", repo_url)
    if not match:
        return None
    owner, repo = match.group(1), match.group(2).rstrip(".git")
    api_url = f"https://api.github.com/repos/{owner}/{repo}"
    try:
        req = urllib.request.Request(api_url, headers={"User-Agent": "IDEGuide-Agent"})
        with urllib.request.urlopen(req, timeout=5) as resp:
            if resp.status == 200:
                data = json.loads(resp.read().decode("utf-8"))
                return {
                    "name": data.get("name", repo).capitalize(),
                    "description": data.get("description", "A modern code editor / development environment."),
                    "stars": data.get("stargazers_count", 0),
                    "license": (data.get("license") or {}).get("spdx_id", "Open Source"),
                    "language": data.get("language", "Software"),
                    "html_url": data.get("html_url", repo_url)
                }
    except Exception as e:
        sys.stderr.write(f"Note: GitHub API fetch skipped or failed ({e}). Using default templates.\n")
    return None


def resolve_ide_data(ide_query=None, repo_url=None, custom_pricing=None):
    """Build a complete data structure for an IDE review."""
    info = None
    query_key = (ide_query or "").strip().lower()

    # Search in database first
    for key, data in KNOWN_IDES_DATABASE.items():
        if key in query_key or query_key in key:
            info = data.copy()
            break

    # If repo URL given or not found in known database
    if repo_url:
        gh_data = fetch_github_repo_info(repo_url)
        if gh_data:
            if not info:
                info = {
                    "name": gh_data["name"],
                    "description": gh_data["description"],
                    "pricing": "Free & Open Source" if gh_data["license"] != "NOASSERTION" else "Freemium",
                    "pros": [
                        f"Open source codebase ({gh_data['stars']:,} stars on GitHub)",
                        f"Primary stack built in {gh_data['language']}",
                        "Active community development and rapid updates",
                        "Transparent development model"
                    ],
                    "cons": [
                        "May require manual build/configuration for full customization",
                        "Extension ecosystem may be smaller than legacy IDEs",
                        "Evolving feature set with active updates"
                    ],
                    "recommendation": f"Recommended for developers who prefer open source toolchains built in {gh_data['language']}.",
                    "category": f"{gh_data['language']} Editor"
                }
            else:
                info["description"] += f" (GitHub: {gh_data['stars']:,} stars)"

    if not info:
        title = ide_query.strip() if ide_query else "Modern Code Editor"
        info = {
            "name": title,
            "description": f"{title} is an innovative coding environment designed to streamline software development.",
            "pricing": custom_pricing or "Free / Paid Options Available",
            "pros": [
                "Modern intuitive developer user interface",
                "Built-in productivity and code assistance tools",
                "Cross-platform compatibility (macOS, Linux, Windows)",
                "Customizable themes and keyboard shortcuts"
            ],
            "cons": [
                "Learning curve for specialized keyboard workflows",
                "Resource consumption depends on active project scale",
                "Plugin coverage varies by programming language"
            ],
            "recommendation": f"Great choice for developers exploring new editor workflows and enhanced productivity.",
            "category": "Code Editor"
        }

    if custom_pricing:
        info["pricing"] = custom_pricing

    return info


def generate_amp_html(ide_info):
    """
    Generates strict AMP (Accelerated Mobile Pages) HTML post content for Blogger (https://ideguide.blogspot.com/).
    Must include mandatory AMP boilerplate, inline CSS <= 75KB, and non-sponsorship disclaimer.
    """
    today_iso = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d")
    canonical_slug = re.sub(r'[^a-z0-9]+', '-', ide_info['name'].lower()).strip('-')
    canonical_url = f"https://ideguide.blogspot.com/{datetime.datetime.now().strftime('%Y/%m')}/{canonical_slug}.html"

    pros_html = "\n".join([f"<li><strong>Good:</strong> {p}</li>" for p in ide_info["pros"]])
    cons_html = "\n".join([f"<li><strong>Bad:</strong> {c}</li>" for c in ide_info["cons"]])

    amp_html = f"""<!doctype html>
<html ⚡ lang="en">
<head>
  <meta charset="utf-8">
  <script async src="https://cdn.ampproject.org/v0.js"></script>
  <title>{ide_info['name']} Review & Breakdown - IDE Guide</title>
  <link rel="canonical" href="{canonical_url}">
  <meta name="viewport" content="width=device-width,minimum-scale=1,initial-scale=1">
  <style amp-boilerplate>body{{-webkit-animation:-amp-start 8s steps(1,end) 0s 1 normal both;-moz-animation:-amp-start 8s steps(1,end) 0s 1 normal both;-ms-animation:-amp-start 8s steps(1,end) 0s 1 normal both;animation:-amp-start 8s steps(1,end) 0s 1 normal both}}@-webkit-keyframes -amp-start{{from{{visibility:hidden}}to{{visibility:visible}}}}@-moz-keyframes -amp-start{{from{{visibility:hidden}}to{{visibility:visible}}}}@-ms-keyframes -amp-start{{from{{visibility:hidden}}to{{visibility:visible}}}}@-o-keyframes -amp-start{{from{{visibility:hidden}}to{{visibility:visible}}}}@keyframes -amp-start{{from{{visibility:hidden}}to{{visibility:visible}}}}</style><noscript><style amp-boilerplate>body{{-webkit-animation:none;-moz-animation:none;-ms-animation:none;animation:none}}</style></noscript>
  <style amp-custom>
    body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; line-height: 1.6; color: #1e293b; background-color: #f8fafc; margin: 0; padding: 16px; }}
    .container {{ max-width: 800px; margin: 0 auto; background: #ffffff; padding: 24px; border-radius: 12px; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1); }}
    h1 {{ color: #0f172a; font-size: 1.8rem; margin-top: 0; border-bottom: 3px solid #0284c7; padding-bottom: 8px; }}
    h2 {{ color: #1e293b; font-size: 1.3rem; margin-top: 24px; border-left: 4px solid #0284c7; padding-left: 8px; }}
    .badge {{ display: inline-block; padding: 4px 12px; border-radius: 9999px; font-size: 0.85rem; font-weight: 600; background-color: #e0f2fe; color: #0369a1; margin-bottom: 12px; }}
    .price-tag {{ display: inline-block; padding: 4px 12px; border-radius: 9999px; font-size: 0.85rem; font-weight: 600; background-color: #fef3c7; color: #92400e; margin-bottom: 12px; margin-left: 8px; }}
    .disclaimer {{ background-color: #f1f5f9; border-left: 4px solid #64748b; padding: 12px; margin: 20px 0; font-size: 0.875rem; color: #475569; font-style: italic; }}
    ul.pros {{ list-style-type: none; padding-left: 0; }}
    ul.pros li {{ background: #f0fdf4; border-left: 4px solid #16a34a; margin: 8px 0; padding: 10px 14px; border-radius: 0 6px 6px 0; }}
    ul.cons {{ list-style-type: none; padding-left: 0; }}
    ul.cons li {{ background: #fef2f2; border-left: 4px solid #dc2626; margin: 8px 0; padding: 10px 14px; border-radius: 0 6px 6px 0; }}
    .verdict-box {{ background: #eff6ff; border: 1px solid #bfdbfe; padding: 16px; border-radius: 8px; margin-top: 20px; }}
    .footer {{ margin-top: 30px; font-size: 0.8rem; text-align: center; color: #94a3b8; border-top: 1px solid #e2e8f0; padding-top: 16px; }}
  </style>
</head>
<body>
  <div class="container">
    <span class="badge">{ide_info['category']}</span>
    <span class="price-tag">Pricing: {ide_info['pricing']}</span>
    <h1>{ide_info['name']}: Objective Developer Breakdown & Evaluation</h1>

    <div class="disclaimer">
      {DISCLAIMER_TEXT}
    </div>

    <p>{ide_info['description']}</p>

    <h2>The Good (Pros & Advantages)</h2>
    <ul class="pros">
      {pros_html}
    </ul>

    <h2>The Bad (Cons & Drawbacks)</h2>
    <ul class="cons">
      {cons_html}
    </ul>

    <h2>Is {ide_info['name']} Best for You?</h2>
    <div class="verdict-box">
      <p><strong>Verdict & Recommendation:</strong> {ide_info['recommendation']}</p>
      <p><strong>Pricing Model:</strong> {ide_info['pricing']}</p>
    </div>

    <div class="footer">
      Published by <a href="https://ideguide.blogspot.com/">IDE Guide</a> | YouTube: <a href="https://www.youtube.com/@IDEguide">@IDEguide</a> | Updated: {today_iso}
    </div>
  </div>
</body>
</html>"""
    return amp_html


def generate_google_flow_video_spec(ide_info):
    """
    Generates a Google Flow video creation spec JSON object for YouTube / YouTube Shorts (@IDEguide).
    Includes precise prompt scenes, framing, lighting, overlay text, and voiceover scripts.
    """
    spec = {
        "channel": "@IDEguide",
        "ide_name": ide_info["name"],
        "category": ide_info["category"],
        "pricing": ide_info["pricing"],
        "disclaimer": DISCLAIMER_TEXT,
        "youtube_shorts_spec": {
            "aspect_ratio": "9:16",
            "resolution": "1080x1920",
            "target_duration_seconds": 55,
            "scenes": [
                {
                    "scene": 1,
                    "duration_seconds": 5,
                    "visual_prompt": f"Cinematic vertical shot of modern glowing dark mode code editor interface showing {ide_info['name']} UI. Neon blue and cyan atmospheric rim lighting. Smooth slow zoom into source code.",
                    "overlay_text": f"Is {ide_info['name']} Worth Using in 2026?",
                    "voiceover_script": f"Looking for a new code editor? Today we are breaking down {ide_info['name']}."
                },
                {
                    "scene": 2,
                    "duration_seconds": 15,
                    "visual_prompt": f"Close-up high-fps screen capture style animation of {ide_info['name']} feature execution, syntax highlighting, and fast editor response.",
                    "overlay_text": "Key Highlights & Capabilities",
                    "voiceover_script": f"{ide_info['description']}"
                },
                {
                    "scene": 3,
                    "duration_seconds": 15,
                    "visual_prompt": "Dynamic split screen visual showing Green checkmarks for Pros and Red crosses for Cons on a sleek dark background with glowing particle effect.",
                    "overlay_text": f"GOOD: {ide_info['pros'][0]} | BAD: {ide_info['cons'][0]}",
                    "voiceover_script": f"On the good side: {ide_info['pros'][0]}. But watch out for: {ide_info['cons'][0]}."
                },
                {
                    "scene": 4,
                    "duration_seconds": 10,
                    "visual_prompt": "Clean graphic displaying Pricing status and target audience badge with smooth modern typography motion.",
                    "overlay_text": f"Pricing: {ide_info['pricing']}",
                    "voiceover_script": f"Pricing is {ide_info['pricing']}. {ide_info['recommendation']}"
                },
                {
                    "scene": 5,
                    "duration_seconds": 10,
                    "visual_prompt": "YouTube subscribe button animation and Blogger website URL glowing banner: ideguide.blogspot.com",
                    "overlay_text": "Subscribe @IDEguide | Full AMP Review in Description",
                    "voiceover_script": f"Subscribe to IDE Guide on YouTube and read the full breakdown on ideguide.blogspot.com! {DISCLAIMER_TEXT}"
                }
            ]
        },
        "youtube_video_spec": {
            "aspect_ratio": "16:9",
            "resolution": "3840x2160",
            "target_duration_seconds": 180,
            "prompt_style_guide": {
                "lighting": "Volumetric soft studio rim light, neon teal (#0284c7) and deep navy (#0f172a)",
                "camera_motion": "Smooth motorized slider pan, slow macro zoom into IDE terminal prompt",
                "color_grading": "High contrast dark mode cyberpunk aesthetics"
            },
            "narration_outline": [
                {"section": "Intro & Non-Sponsorship Disclaimer", "duration_seconds": 20},
                {"section": "Core Architecture & Feature Walkthrough", "duration_seconds": 60},
                {"section": "The Good vs The Bad (Deep Evaluation)", "duration_seconds": 50},
                {"section": "Pricing Structure & Best Developer Persona", "duration_seconds": 30},
                {"section": "Final Verdict & Channel Call to Action", "duration_seconds": 20}
            ]
        }
    }
    return spec


def main():
    parser = argparse.ArgumentParser(description="IDE Guide Agentic Skill - Generate AMP Blog Posts & Google Flow Specs")
    parser.add_argument("--ide", type=str, help="Name of the IDE/editor (e.g. 'Cursor IDE', 'Zed Editor', 'Neovim')")
    parser.add_argument("--repo", type=str, help="GitHub repository URL of the editor")
    parser.add_argument("--pricing", type=str, help="Custom pricing description (e.g. 'Free', 'Freemium', 'Paid $10/mo')")
    parser.add_argument("--output-dir", type=str, default="output", help="Directory to save generated AMP HTML and Flow Spec files")

    args = parser.parse_args()

    if not args.ide and not args.repo:
        parser.print_help()
        sys.exit(1)

    ide_info = resolve_ide_data(ide_query=args.ide, repo_url=args.repo, custom_pricing=args.pricing)

    os.makedirs(args.output_dir, exist_ok=True)
    slug = re.sub(r'[^a-z0-9]+', '_', ide_info['name'].lower()).strip('_')

    amp_content = generate_amp_html(ide_info)
    amp_filepath = os.path.join(args.output_dir, f"{slug}_amp_blogpost.html")
    with open(amp_filepath, "w", encoding="utf-8") as f:
        f.write(amp_content)

    flow_spec = generate_google_flow_video_spec(ide_info)
    spec_filepath = os.path.join(args.output_dir, f"{slug}_google_flow_spec.json")
    with open(spec_filepath, "w", encoding="utf-8") as f:
        json.dump(flow_spec, f, indent=2)

    print(f"✅ Successfully generated content for '{ide_info['name']}':")
    print(f"   - AMP HTML Blog Post : {amp_filepath}")
    print(f"   - Google Flow Video Spec: {spec_filepath}")


if __name__ == "__main__":
    main()
