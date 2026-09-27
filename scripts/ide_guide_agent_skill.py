#!/usr/bin/env python3
"""
IDE Guide Agentic Skill CLI Tool.
Generates AMP HTML blog posts for Blogger and Google Flow Video Prompt Specs for YouTube.
Usage:
    python3 scripts/ide_guide_agent_skill.py --ide "Visual Studio Code" --category "Full Featured IDE" --price "Free"
    python3 scripts/ide_guide_agent_skill.py --repo "https://github.com/zed-industries/zed"
"""

import argparse
import sys
import json
import re
from pathlib import Path

MANDATORY_DISCLAIMER = (
    "Disclaimer: IDE Guide is an independent technical publication. "
    "This content is not sponsored, endorsed, or affiliated with any software vendor "
    "or editor developer mentioned above. All reviews and assessments are based strictly "
    "on objective developer evaluation."
)

DEFAULT_IDE_DATABASE = {
    "visual studio code": {
        "name": "Visual Studio Code",
        "developer": "Microsoft",
        "license": "Free / Open Source Core (MIT)",
        "ecosystem": "Cross-Platform (Windows, macOS, Linux, Web)",
        "highlights": ["Extensive Extension Marketplace", "Integrated Terminal & Git", "Language Server Protocol (LSP) Support", "Copilot & AI Assistant Integration"],
        "pros": ["Massive community and ecosystem", "Highly customizable", "Fast updates and huge extension library", "Seamless remote development"],
        "cons": ["High memory consumption with many extensions", "Electron framework overhead"],
        "price_tier": "Free",
        "best_for": "Web, Python, TypeScript, Full-stack developers looking for standard industry versatility."
    },
    "cursor": {
        "name": "Cursor",
        "developer": "Anysphere",
        "license": "Freemium ($20/mo Pro)",
        "ecosystem": "Cross-Platform (Fork of VS Code)",
        "highlights": ["AI-native Code Editing", "Repository-wide Context indexing", "Multi-file Auto-edits", "Privacy Mode"],
        "pros": ["Blazing fast AI completions", "Deep repository context comprehension", "Familiar VS Code keybindings & extensions"],
        "cons": ["Paid subscription needed for heavy AI usage", "Closed source AI engine"],
        "price_tier": "Freemium (Free tier + $20/mo Pro)",
        "best_for": "Developers seeking state-of-the-art AI pair programming integrated directly into VS Code workflow."
    },
    "zed": {
        "name": "Zed",
        "developer": "Zed Industries",
        "license": "Open Source (GPL / Apache)",
        "ecosystem": "macOS & Linux (Windows in progress)",
        "highlights": ["Written in Rust", "GPUI High-Performance Rendering", "Built-in Realtime Collaboration", "Integrated AI Assistant"],
        "pros": ["Ultra-fast start time and low latencies", "Low memory footprint compared to Electron", "Sleek modern UI"],
        "cons": ["Ecosystem/extensions still growing", "Fewer plugins than VS Code"],
        "price_tier": "Free / Open Source",
        "best_for": "Developers prioritizing speed, memory efficiency, and real-time pair programming."
    },
    "pycharm": {
        "name": "PyCharm",
        "developer": "JetBrains",
        "license": "Freemium (Free Community / $249/yr Professional)",
        "ecosystem": "Cross-Platform",
        "highlights": ["Smart Python Code Completion", "Django & Web Framework Support", "Scientific Tools & Jupyter Support", "Database Tools"],
        "pros": ["Best-in-class Python refactoring and analysis", "Powerful built-in database management", "Out-of-the-box framework support"],
        "cons": ["Heavy JVM resource usage", "Professional features locked behind subscription"],
        "price_tier": "Freemium (Free Community Edition, Paid Professional)",
        "best_for": "Professional Python, Django, Data Science, and backend engineers."
    },
    "neovim": {
        "name": "Neovim",
        "developer": "Community",
        "license": "Free / Open Source (Apache/Vim)",
        "ecosystem": "Terminal / Cross-Platform",
        "highlights": ["Lua Scriptability", "Built-in Language Server Protocol (LSP)", "Asynchronous Architecture", "Infinite Extensibility"],
        "pros": ["Zero mouse dependency & ultra-fast keyboard navigation", "Minimal resource footprint", "Complete customization freedom"],
        "cons": ["Steep learning curve", "Requires time configuration effort"],
        "price_tier": "Free / Open Source",
        "best_for": "Power users, terminal enthusiasts, and developers seeking ultra-fast modal editing."
    }
}


def parse_repo_url(url: str) -> dict:
    match = re.search(r'github\.com/([^/]+)/([^/]+)', url)
    if match:
        org, repo = match.group(1), match.group(2)
        name = repo.replace("-", " ").replace("_", " ").title()
        developer = org.replace("-", " ").replace("_", " ").title()
        return {
            "name": name,
            "developer": developer,
            "license": "Open Source / GitHub Repository",
            "ecosystem": "Cross-Platform",
            "highlights": [f"Source code hosted on GitHub ({org}/{repo})", "Community driven development", "Extensible architecture"],
            "pros": ["Transparent source code", "Active open source contributions", "Customizable build options"],
            "cons": ["May require self-building or beta testing", "Community support timeline"],
            "price_tier": "Free / Open Source",
            "best_for": "Developers interested in bleeding-edge open source code editors."
        }
    name = url.split("/")[-1].replace("-", " ").replace("_", " ").title() or "Custom Code Editor"
    return {
        "name": name,
        "developer": "Independent / Open Source",
        "license": "Open Source",
        "ecosystem": "Cross-Platform",
        "highlights": ["Modern developer workflow", "Lightweight design"],
        "pros": ["Flexible configuration", "Fast execution"],
        "cons": ["Niche extension ecosystem"],
        "price_tier": "Free",
        "best_for": "Engineers exploring new developer tooling options."
    }


def get_ide_info(ide_name: str = None, repo_url: str = None, price: str = None, category: str = None) -> dict:
    if repo_url:
        info = parse_repo_url(repo_url)
    elif ide_name and ide_name.lower() in DEFAULT_IDE_DATABASE:
        info = DEFAULT_IDE_DATABASE[ide_name.lower()]
    elif ide_name:
        info = {
            "name": ide_name,
            "developer": "Vendor / Community",
            "license": price if price else "Free / Paid Tiers",
            "ecosystem": "Cross-Platform",
            "highlights": [f"Feature-rich code editing for {category or 'developers'}", "Intelligent code completion", "Plugin ecosystem"],
            "pros": ["Focused workflow features", "Modern developer interface", "Active update cycle"],
            "cons": ["Feature trade-offs depending on usage", "Learning curve for advanced workflows"],
            "price_tier": price if price else "Free / Paid options",
            "best_for": f"Software engineers working with {category or 'modern tech stacks'}."
        }
    else:
        info = DEFAULT_IDE_DATABASE["visual studio code"]

    if price and "price_tier" in info and not price.lower() in info["price_tier"].lower():
        info["price_tier"] = price

    return info


def generate_amp_blog_post(info: dict) -> str:
    name = info["name"]
    developer = info["developer"]
    license_type = info["license"]
    price_tier = info["price_tier"]
    best_for = info["best_for"]

    pros_html = "".join([f"<li><strong>Pro:</strong> {p}</li>" for p in info["pros"]])
    cons_html = "".join([f"<li><strong>Con:</strong> {c}</li>" for c in info["cons"]])
    highlights_html = "".join([f"<li>{h}</li>" for h in info["highlights"]])

    html = f"""<!doctype html>
<html ⚡ lang="en">
<head>
  <meta charset="utf-8">
  <title>{name} Review & Evaluation - IDE Guide</title>
  <link rel="canonical" href="https://ideguide.blogspot.com/reviews/{name.lower().replace(' ', '-')}.html">
  <meta name="viewport" content="width=device-width,minimum-scale=1,initial-scale=1">
  <script async src="https://cdn.ampproject.org/v0.js"></script>
  <style amp-boilerplate>body{{-webkit-animation:-amp-start 8s steps(1,end) 0s 1 normal both;-moz-animation:-amp-start 8s steps(1,end) 0s 1 normal both;-ms-animation:-amp-start 8s steps(1,end) 0s 1 normal both;animation:-amp-start 8s steps(1,end) 0s 1 normal both}}@-webkit-keyframes -amp-start{{from{{visibility:hidden}}to{{visibility:visible}}}}@-moz-keyframes -amp-start{{from{{visibility:hidden}}to{{visibility:visible}}}}@-ms-keyframes -amp-start{{from{{visibility:hidden}}to{{visibility:visible}}}}@-o-keyframes -amp-start{{from{{visibility:hidden}}to{{visibility:visible}}}}@keyframes -amp-start{{from{{visibility:hidden}}to{{visibility:visible}}}}</style><noscript><style amp-boilerplate>body{{-webkit-animation:none;-moz-animation:none;-ms-animation:none;animation:none}}</style></noscript>
  <style amp-custom>
    body {{
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
      line-height: 1.6;
      color: #1f2937;
      background-color: #f9fafb;
      margin: 0;
      padding: 16px;
    }}
    .container {{
      max-width: 800px;
      margin: 0 auto;
      background: #ffffff;
      padding: 24px;
      border-radius: 8px;
      box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }}
    h1 {{
      color: #111827;
      font-size: 1.8rem;
      border-bottom: 2px solid #3b82f6;
      padding-bottom: 8px;
    }}
    h2 {{
      color: #1e40af;
      font-size: 1.3rem;
      margin-top: 24px;
    }}
    .badge-bar {{
      display: flex;
      gap: 8px;
      margin-bottom: 16px;
      flex-wrap: wrap;
    }}
    .badge {{
      background-color: #e0e7ff;
      color: #3730a3;
      padding: 4px 10px;
      border-radius: 9999px;
      font-size: 0.85rem;
      font-weight: 600;
    }}
    ul {{
      padding-left: 20px;
    }}
    li {{
      margin-bottom: 8px;
    }}
    .disclaimer-box {{
      background-color: #f3f4f6;
      border-left: 4px solid #6b7280;
      padding: 12px 16px;
      margin-top: 32px;
      font-size: 0.88rem;
      color: #4b5563;
      font-style: italic;
    }}
    .cta-box {{
      background-color: #eff6ff;
      border: 1px solid #bfdbfe;
      border-radius: 6px;
      padding: 16px;
      margin-top: 24px;
      text-align: center;
    }}
    .cta-box a {{
      color: #2563eb;
      font-weight: bold;
      text-decoration: none;
    }}
  </style>
</head>
<body>
  <div class="container">
    <h1>{name}: In-Depth Developer Guide & Assessment</h1>

    <div class="badge-bar">
      <span class="badge">Developer: {developer}</span>
      <span class="badge">Price: {price_tier}</span>
      <span class="badge">License: {license_type}</span>
    </div>

    <p>Welcome to <strong>IDE Guide</strong>. Today we evaluate <strong>{name}</strong> to determine its performance, feature set, pricing tier, and whether it fits your software development workflow.</p>

    <h2>Key Highlights & Features</h2>
    <ul>
      {highlights_html}
    </ul>

    <h2>Objective Evaluation: Pros & Cons</h2>
    <h3>What Makes It Great (Pros)</h3>
    <ul>
      {pros_html}
    </ul>

    <h3>Areas for Improvement (Cons)</h3>
    <ul>
      {cons_html}
    </ul>

    <h2>Who Should Use {name}?</h2>
    <p><strong>Ideal Use Case:</strong> {best_for}</p>

    <div class="cta-box">
      <p>📺 Watch our complete visual breakdown and dynamic AI comparison on YouTube: <a href="https://www.youtube.com/@IDEguide" target="_blank" rel="noopener">@IDEguide Channel</a></p>
    </div>

    <div class="disclaimer-box">
      <p>{MANDATORY_DISCLAIMER}</p>
    </div>
  </div>
</body>
</html>
"""
    return html


def generate_google_flow_video_spec(info: dict) -> dict:
    name = info["name"]
    developer = info["developer"]
    price_tier = info["price_tier"]

    long_form_script = {
        "title": f"Is {name} Worth It? Complete Developer Guide & Feature Breakdown",
        "aspect_ratio": "16:9",
        "target_platform": "YouTube Long-Form",
        "channel": "@IDEguide",
        "prompts_and_scenes": [
            {
                "scene_id": 1,
                "duration_sec": 10,
                "visual_prompt": f"Macro cinematic pan of a sleek mechanical keyboard with glowing RGB illumination, transitioning to dark mode IDE window showing {name} interface with vibrant syntax highlighting.",
                "framing_and_lighting": "35mm anamorphic, dramatic side lighting, rich dark blue and neon purple glow, smooth 24fps motion.",
                "voiceover_transcript": f"Looking for your next primary code editor? Today on IDE Guide, we're diving deep into {name} by {developer}."
            },
            {
                "scene_id": 2,
                "duration_sec": 20,
                "visual_prompt": f"Split screen visual displaying key features of {name}: rapid code completion popups, terminal commands executing, and extension settings.",
                "framing_and_lighting": "Clean UI showcase, crisp screen recording overlay, slate gray studio backdrop.",
                "voiceover_transcript": f"Here are the standout features. {name} offers strong developer ergonomics, fast execution, and integrated productivity tooling."
            },
            {
                "scene_id": 3,
                "duration_sec": 15,
                "visual_prompt": f"Close up on system metrics monitor showing RAM and CPU usage gauges alongside {name} workload.",
                "framing_and_lighting": "Technical futuristic UI overlay, orange and amber lighting accents.",
                "voiceover_transcript": f"On the flip side, consider memory consumption and ecosystem maturity before making the switch."
            },
            {
                "scene_id": 4,
                "duration_sec": 15,
                "visual_prompt": f"Graphic card popup showing pricing details ({price_tier}) and license tier.",
                "framing_and_lighting": "Minimalist graphic card design, smooth glassmorphism motion.",
                "voiceover_transcript": f"Pricing breakdown: {name} is available under {price_tier}. Make sure to evaluate if free vs paid features align with your team size."
            },
            {
                "scene_id": 5,
                "duration_sec": 10,
                "visual_prompt": f"Final montage with subscribe button, channel branding @IDEguide, and on-screen disclaimer text.",
                "framing_and_lighting": "Modern YouTube endscreen slate with subtle animated particles.",
                "voiceover_transcript": f"Subscribe to @IDEguide for daily editor breakdowns. {MANDATORY_DISCLAIMER}"
            }
        ],
        "non_sponsorship_disclaimer": MANDATORY_DISCLAIMER
    }

    shorts_script = {
        "title": f"Should You Switch to {name}? (60s Review)",
        "aspect_ratio": "9:16",
        "target_platform": "YouTube Shorts",
        "channel": "@IDEguide",
        "prompts_and_scenes": [
            {
                "scene_id": 1,
                "duration_sec": 5,
                "visual_prompt": f"Vertical 9:16 vertical video showing hands typing at lightning speed on a backlit keyboard with {name} UI on a ultra-wide monitor.",
                "voiceover_transcript": f"Should you switch to {name} in 2026?"
            },
            {
                "scene_id": 2,
                "duration_sec": 20,
                "visual_prompt": f"Fast-paced cuts showing code autocomplete, instant search, and extensions panel in {name}.",
                "voiceover_transcript": f"Pros: Extremely responsive workflow, great language support, and clean developer experience."
            },
            {
                "scene_id": 3,
                "duration_sec": 20,
                "visual_prompt": f"Quick cons callout overlay with badge: {price_tier}.",
                "voiceover_transcript": f"Cons and Pricing: Available under {price_tier}. Watch out for extension compatibility depending on your language stack."
            },
            {
                "scene_id": 4,
                "duration_sec": 15,
                "visual_prompt": f"Full screen @IDEguide subscribe graphic and disclaimer block.",
                "voiceover_transcript": f"Hit subscribe for more IDE comparisons! {MANDATORY_DISCLAIMER}"
            }
        ],
        "non_sponsorship_disclaimer": MANDATORY_DISCLAIMER
    }

    return {
        "ide_name": name,
        "long_form_video": long_form_script,
        "shorts_video": shorts_script
    }


def main():
    parser = argparse.ArgumentParser(description="IDE Guide Agentic Skill CLI")
    parser.add_argument("--ide", type=str, help="Name of the IDE/Code Editor")
    parser.add_argument("--repo", type=str, help="GitHub Repository URL of the IDE")
    parser.add_argument("--price", type=str, help="Price Tier (Free / Paid / Freemium)")
    parser.add_argument("--category", type=str, help="IDE Category / Main language")
    parser.add_argument("--output-dir", type=str, default="output", help="Output directory path")

    args = parser.parse_args()

    if not args.ide and not args.repo:
        parser.print_help()
        sys.exit(1)

    info = get_ide_info(ide_name=args.ide, repo_url=args.repo, price=args.price, category=args.category)
    amp_html = generate_amp_blog_post(info)
    video_spec = generate_google_flow_video_spec(info)

    out_dir = Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    slug = info["name"].lower().replace(" ", "_")
    blog_file = out_dir / f"{slug}_blog_post_amp.html"
    video_file = out_dir / f"{slug}_video_spec.json"

    blog_file.write_text(amp_html, encoding="utf-8")
    video_file.write_text(json.dumps(video_spec, indent=2), encoding="utf-8")

    print(f"✨ Successfully generated agentic skills content for {info['name']}:")
    print(f"  - AMP Blog Post: {blog_file}")
    print(f"  - Video Prompt Spec: {video_file}")


if __name__ == "__main__":
    main()
