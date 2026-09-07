#!/usr/bin/env python3
"""
IDE Guide Agentic CLI Skill Tool
Generates AMP (Accelerated Mobile Pages) HTML blog posts for Blogger (ideguide.blogspot.com)
and Google Flow video specifications for YouTube (@IDEguide).
Also provides AMP HTML compliance validation.
"""

import argparse
import json
import os
import re
import sys
from typing import Dict, Any, List, Tuple

DISCLAIMER_TEXT = (
    "Disclaimer: IDE Guide is an independent technical publication. "
    "This content is not sponsored, endorsed, or affiliated with any software vendor "
    "or editor developer mentioned above. All reviews and assessments are based strictly on objective developer evaluation."
)

IDE_KNOWLEDGE_BASE = {
    "visual studio code": {
        "name": "Visual Studio Code (VS Code)",
        "developer": "Microsoft",
        "category": "Extensible Source Code Editor",
        "pricing": "Free (Open Source / Proprietary Build)",
        "pros": [
            "Massive ecosystem with tens of thousands of extensions",
            "Incredible language server protocol (LSP) integration",
            "Built-in Git GUI, terminal, and debugging tools",
            "Seamless AI assistant integration (GitHub Copilot, Codeium, etc.)"
        ],
        "cons": [
            "Electron-based app can consume significant RAM on large workspaces",
            "Requires initial setup & extension configuration for advanced language features",
            "Telemetry enabled by default in official builds"
        ],
        "verdict": "Best all-around code editor for full-stack developers, web developers, and general software engineers.",
        "best_for": "Web Development, TypeScript/JavaScript, Python, and Multi-language projects",
        "official_url": "https://code.visualstudio.com/"
    },
    "cursor": {
        "name": "Cursor AI Editor",
        "developer": "Anysphere",
        "category": "AI-First Code Editor",
        "pricing": "Freemium ($20/mo Pro)",
        "pros": [
            "Native multi-file AI code editing and codebase indexing",
            "Instant inline auto-edits (Cursor Prediction)",
            "Full compatibility with VS Code extensions and settings",
            "Built-in AI chat with vision and web search capabilities"
        ],
        "cons": [
            "Requires subscription or paid API keys for high-tier models",
            "Proprietary modifications on top of open-source VS Code base",
            "Occasional AI hallucination on complex architectural changes"
        ],
        "verdict": "The premier AI-native editor currently available, drastically speeding up development workflows.",
        "best_for": "AI-assisted coding, rapid prototyping, and complex refactoring",
        "official_url": "https://cursor.com/"
    },
    "zed": {
        "name": "Zed Editor",
        "developer": "Zed Industries",
        "category": "High-Performance Code Editor",
        "pricing": "Free (Open Source)",
        "pros": [
            "Written in Rust with GPU-accelerated rendering for lightning-fast speeds",
            "Minimal memory footprint compared to Electron editors",
            "Built-in multiplayer collaborative coding out of the box",
            "Integrated AI assistant support (Claude, OpenAI, Ollama)"
        ],
        "cons": [
            "Ecosystem and extension marketplace still growing compared to VS Code",
            "Fewer legacy plugin integrations available today",
            "Primarily focused on macOS and Linux (Windows support in development)"
        ],
        "verdict": "The fastest modern code editor on the market, perfect for developers prioritizing raw speed.",
        "best_for": "Rust, Go, C++, and performance-critical development",
        "official_url": "https://zed.dev/"
    },
    "pycharm": {
        "name": "JetBrains PyCharm",
        "developer": "JetBrains",
        "category": "Dedicated Python IDE",
        "pricing": "Freemium (Community Free / Professional $249/yr)",
        "pros": [
            "Best-in-class Python static analysis, refactoring, and linting",
            "Built-in database manager, web framework support, and remote debugging",
            "Deep integration with Jupyter Notebooks and Data Science tools",
            "Out-of-the-box support for Django, Flask, and FastAPI"
        ],
        "cons": [
            "Heavy resource usage requires high-RAM machines",
            "Professional features locked behind a commercial license",
            "Slower cold startup time compared to lightweight text editors"
        ],
        "verdict": "The definitive gold standard IDE for professional Python backend and data science engineers.",
        "best_for": "Python Backend Engineering, Django, FastAPI, Data Science",
        "official_url": "https://www.jetbrains.com/pycharm/"
    },
    "neovim": {
        "name": "Neovim",
        "developer": "Neovim Core Team",
        "category": "Hyper-extensible Terminal Text Editor",
        "pricing": "Free (Open Source)",
        "pros": [
            "Unrivaled speed, efficiency, and zero-latency keyboard navigation",
            "Lua-based configuration allowing infinite personalization",
            "Native LSP and Treesitter support for modern IDE capabilities",
            "Extremely lightweight (starts in under 20 milliseconds)"
        ],
        "cons": [
            "Steep learning curve for modal editing and keybindings",
            "Requires time investment to configure custom development environment",
            "Terminal-based GUI might not appeal to developers preferring mouse interaction"
        ],
        "verdict": "The ultimate keyboard-driven editor for developers seeking maximum speed and total setup control.",
        "best_for": "Power users, terminal aficionados, Systems programming, DevOps",
        "official_url": "https://neovim.io/"
    }
}


def get_ide_info(name_or_repo: str) -> Dict[str, Any]:
    """Retrieves or derives metadata for an IDE/repository."""
    clean_key = name_or_repo.strip().lower()

    # Handle repo URL input
    if "github.com/" in clean_key:
        parts = clean_key.rstrip("/").split("/")
        repo_name = parts[-1] if len(parts) > 0 else "Repository"
        clean_key = repo_name.replace("-", " ").replace("_", " ")

    for key, data in IDE_KNOWLEDGE_BASE.items():
        if key in clean_key or clean_key in key:
            return data

    # Default fallback data structure if unknown IDE
    title_name = name_or_repo.split("/")[-1].replace("-", " ").replace("_", " ").title()
    return {
        "name": title_name,
        "developer": "Independent Open Source / Vendor",
        "category": "Code Editor / Developer Tool",
        "pricing": "Free / Freemium",
        "pros": [
            f"Focused feature set tailored for modern {title_name} development",
            "Active developer community and open issue tracker",
            "Streamlined workflow integration and responsive editor interface",
            "Modern syntax highlighting and project workspace navigation"
        ],
        "cons": [
            "May have fewer third-party integrations compared to industry giants",
            "Requires initial configuration for enterprise development setups",
            "Niche extension ecosystem depending on active community maintainers"
        ],
        "verdict": f"{title_name} is a compelling option worth evaluating for developers working on specialized projects.",
        "best_for": "Developers seeking specialized editor workflows and alternative tooling",
        "official_url": f"https://github.com/search?q={title_name}"
    }


def generate_amp_blog_post(ide_info: Dict[str, Any]) -> str:
    """Generates a Blogger-compatible AMP HTML blog post."""
    title = f"{ide_info['name']} Review & Developer Guide: Is It Right for You?"

    pros_html = "\n".join([f"<li>✅ <strong>{pro}</strong></li>" for pro in ide_info["pros"]])
    cons_html = "\n".join([f"<li>❌ <strong>{con}</strong></li>" for con in ide_info["cons"]])

    amp_html = f"""<!doctype html>
<html ⚡ lang="en">
<head>
  <meta charset="utf-8">
  <title>{title} | IDE Guide</title>
  <link rel="canonical" href="https://ideguide.blogspot.com/{ide_info['name'].lower().replace(' ', '-')}-review.html">
  <meta name="viewport" content="width=device-width,minimum-scale=1,initial-scale=1">
  <style amp-boilerplate>body{{-webkit-animation:-amp-start 8s steps(1,end) 0s 1 normal both;-moz-animation:-amp-start 8s steps(1,end) 0s 1 normal both;-ms-animation:-amp-start 8s steps(1,end) 0s 1 normal both;animation:-amp-start 8s steps(1,end) 0s 1 normal both}}@-webkit-keyframes -amp-start{{from{{visibility:hidden}}to{{visibility:visible}}}}@-moz-keyframes -amp-start{{from{{visibility:hidden}}to{{visibility:visible}}}}@-ms-keyframes -amp-start{{from{{visibility:hidden}}to{{visibility:visible}}}}@-o-keyframes -amp-start{{from{{visibility:hidden}}to{{visibility:visible}}}}@keyframes -amp-start{{from{{visibility:hidden}}to{{visibility:visible}}}}</style><noscript><style amp-boilerplate>body{{-webkit-animation:none;-moz-animation:none;-ms-animation:none;animation:none}}</style></noscript>
  <script async src="https://cdn.ampproject.org/v0.js"></script>
  <style amp-custom>
    body {{
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
      line-height: 1.6;
      color: #e2e8f0;
      background-color: #0f172a;
      padding: 16px;
      max-width: 800px;
      margin: 0 auto;
    }}
    header {{
      text-align: center;
      padding-bottom: 20px;
      border-bottom: 2px solid #1e293b;
      margin-bottom: 24px;
    }}
    .channel-tag {{
      color: #00f3ff;
      text-transform: uppercase;
      font-size: 0.85rem;
      letter-spacing: 1.5px;
      font-weight: bold;
    }}
    h1 {{
      color: #f8fafc;
      font-size: 2rem;
      margin-top: 8px;
    }}
    .badge-container {{
      margin: 16px 0;
    }}
    .badge {{
      display: inline-block;
      padding: 6px 12px;
      background-color: #1e293b;
      color: #38bdf8;
      border-radius: 6px;
      font-size: 0.85rem;
      font-weight: 600;
      margin-right: 8px;
    }}
    .badge-pricing {{
      background-color: #064e3b;
      color: #34d399;
    }}
    .hero-img {{
      margin: 20px 0;
      border-radius: 8px;
      overflow: hidden;
    }}
    .card {{
      background-color: #1e293b;
      border-radius: 8px;
      padding: 20px;
      margin-bottom: 20px;
      box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.3);
    }}
    h2 {{
      color: #38bdf8;
      border-bottom: 1px solid #334155;
      padding-bottom: 8px;
      margin-top: 0;
    }}
    ul {{
      padding-left: 20px;
    }}
    li {{
      margin-bottom: 10px;
    }}
    .verdict-box {{
      background-color: #172554;
      border-left: 4px solid #3b82f6;
      padding: 16px;
      border-radius: 4px;
      margin-top: 24px;
    }}
    .disclaimer-box {{
      background-color: #0f172a;
      border: 1px solid #334155;
      color: #94a3b8;
      font-size: 0.82rem;
      padding: 14px;
      border-radius: 6px;
      margin-top: 32px;
      font-style: italic;
    }}
    footer {{
      text-align: center;
      margin-top: 40px;
      color: #64748b;
      font-size: 0.85rem;
    }}
  </style>
</head>
<body>

  <header>
    <div class="channel-tag">IDE Guide • Objective Editor Review</div>
    <h1>{ide_info['name']} Review</h1>
    <div class="badge-container">
      <span class="badge">Category: {ide_info['category']}</span>
      <span class="badge badge-pricing">Pricing: {ide_info['pricing']}</span>
    </div>
  </header>

  <main>
    <div class="hero-img">
      <amp-img src="https://images.unsplash.com/photo-1555066931-4365d14bab8c?w=800&auto=format&fit=crop"
               width="800"
               height="450"
               layout="responsive"
               alt="{ide_info['name']} Interface Preview">
      </amp-img>
    </div>

    <div class="card">
      <h2>Overview</h2>
      <p><strong>{ide_info['name']}</strong> (developed by {ide_info['developer']}) is a popular tool in the {ide_info['category']} landscape. In this comprehensive review, we evaluate its key features, performance metrics, strengths, limitations, and pricing model to help you decide if it fits your developer stack.</p>
    </div>

    <div class="card">
      <h2>The Good (Pros)</h2>
      <ul>
        {pros_html}
      </ul>
    </div>

    <div class="card">
      <h2>The Bad (Cons)</h2>
      <ul>
        {cons_html}
      </ul>
    </div>

    <div class="card">
      <h2>Pricing & Free vs Paid Breakdown</h2>
      <p><strong>Model:</strong> {ide_info['pricing']}</p>
      <p>Whether you are a solo developer or an enterprise software engineer, understanding the cost structure is crucial. {ide_info['name']} offers a competitive feature balance across its tiers.</p>
    </div>

    <div class="verdict-box">
      <h3 style="margin-top:0; color:#60a5fa;">IDE Guide Final Verdict</h3>
      <p style="margin-bottom:0;">{ide_info['verdict']}</p>
      <p style="margin-top:8px; font-size:0.9rem; color:#93c5fd;"><strong>Best Suited For:</strong> {ide_info['best_for']}</p>
    </div>

    <div class="disclaimer-box">
      {DISCLAIMER_TEXT}
    </div>
  </main>

  <footer>
    <p>© IDE Guide. Technical Reviews for Modern Software Engineers. Watch our video walkthroughs on <a href="https://www.youtube.com/@IDEguide" style="color:#38bdf8;">YouTube (@IDEguide)</a>.</p>
  </footer>

</body>
</html>
"""
    return amp_html


def generate_google_flow_video_spec(ide_info: Dict[str, Any]) -> Dict[str, Any]:
    """Generates a Google Flow video generation specification JSON."""
    return {
        "title": f"{ide_info['name']} Review in 60 Seconds - Is It Worth It?",
        "target_platform": "YouTube Shorts (9:16) & YouTube Video (@IDEguide)",
        "duration_seconds": 60,
        "ide_name": ide_info["name"],
        "developer": ide_info["developer"],
        "pricing_model": ide_info["pricing"],
        "visual_style": {
            "theme": "Cybernetic Modern Developer Studio Dark Mode",
            "primary_color": "#00f3ff",
            "secondary_color": "#8a2be2",
            "background_color": "#0f172a",
            "lighting": "Low key dark ambient lighting with subtle neon rim glow"
        },
        "scenes": [
            {
                "scene_number": 1,
                "duration_seconds": 8,
                "narration_script": f"Is {ide_info['name']} actually worth switching to in 2025? Here is what you need to know in under 60 seconds.",
                "visual_prompt": f"Cinematic close up tracking shot of glowing dark mode code editor displaying {ide_info['name']} UI with neon syntax highlighting, 4k ultra detailed, photorealistic.",
                "camera_motion": "Smooth push-in zoom towards code editor screen",
                "overlay_text": f"{ide_info['name']}\nWorth Switching?"
            },
            {
                "scene_number": 2,
                "duration_seconds": 18,
                "narration_script": f"First, the good points. {ide_info['pros'][0]}. Plus, {ide_info['pros'][1]}.",
                "visual_prompt": f"Macro shot of fast glowing cursor moving across code syntax, high contrast code completion popup appearing dynamically, cinematic lighting.",
                "camera_motion": "Horizontal pan left to right across editor interface",
                "overlay_text": f"PROS:\n• {ide_info['pros'][0][:35]}...\n• {ide_info['pros'][1][:35]}..."
            },
            {
                "scene_number": 3,
                "duration_seconds": 16,
                "narration_script": f"However, keep in mind the drawbacks. {ide_info['cons'][0]}.",
                "visual_prompt": "Slow motion close up of developer workspace with dark minimalist dual wide monitors and mechanical keyboard, subtle blue ambient backlight.",
                "camera_motion": "Macro zoom on benchmark graphs on screen",
                "overlay_text": f"CONS:\n• {ide_info['cons'][0][:45]}..."
            },
            {
                "scene_number": 4,
                "duration_seconds": 10,
                "narration_script": f"Pricing is {ide_info['pricing']}. {ide_info['verdict']}",
                "visual_prompt": "Sleek pricing badge badge pop-up over dark gradient background with glowing checkmarks.",
                "camera_motion": "Static punch-in center focus",
                "overlay_text": f"PRICING: {ide_info['pricing']}\nVERDICT: {ide_info['best_for']}"
            },
            {
                "scene_number": 5,
                "duration_seconds": 8,
                "narration_script": "Check out our full in-depth review on ideguide.blogspot.com and subscribe to IDE Guide for unsponsored developer tooling reviews.",
                "visual_prompt": "End screen showing IDE Guide logo, YouTube subscribe animation, and Blogger site url over dark futuristic grid.",
                "camera_motion": "Slow pull-out zoom",
                "overlay_text": "IDE Guide | ideguide.blogspot.com\nIndependent & Unsponsored"
            }
        ],
        "disclaimer": DISCLAIMER_TEXT
    }


def validate_amp_html(content: str) -> Tuple[bool, List[str]]:
    """Validates whether an HTML string meets Blogger AMP requirements."""
    errors = []

    # Check AMP HTML attribute
    if not re.search(r'<html\s+[^>]*?(⚡|amp\b)[^>]*?>', content, re.IGNORECASE):
        errors.append("Missing <html ⚡> or <html amp> tag.")

    # Check AMP boilerplate JS
    if 'https://cdn.ampproject.org/v0.js' not in content:
        errors.append("Missing AMP core runtime script: https://cdn.ampproject.org/v0.js.")

    # Check amp-boilerplate style
    if '<style amp-boilerplate>' not in content:
        errors.append("Missing <style amp-boilerplate> tag.")

    # Check style amp-custom
    if '<style amp-custom>' not in content:
        errors.append("Missing <style amp-custom> tag.")

    # Disallow standard img tags
    disallowed_imgs = re.findall(r'<img\s+[^>]*?>', content, re.IGNORECASE)
    if disallowed_imgs:
        errors.append(f"Found {len(disallowed_imgs)} standard <img> tag(s). AMP requires <amp-img> instead.")

    # Check amp-img presence
    if '<amp-img' not in content:
        errors.append("Missing <amp-img> element for responsive images.")

    # Check non-sponsorship disclaimer
    if DISCLAIMER_TEXT not in content:
        errors.append("Missing exact mandatory non-sponsorship disclaimer text.")

    return len(errors) == 0, errors


def main():
    parser = argparse.ArgumentParser(description="IDE Guide Agentic Skill CLI Tool")
    subparsers = parser.add_subparsers(dest="command", help="Sub-command to run")

    # Command: generate
    gen_parser = subparsers.add_parser("generate", help="Generate AMP blog post and Google Flow video spec")
    gen_parser.add_argument("--ide", type=str, help="Name of the IDE or editor (e.g. 'Cursor')")
    gen_parser.add_argument("--repo", type=str, help="GitHub repository URL (e.g. 'https://github.com/zed-industries/zed')")
    gen_parser.add_argument("--output-dir", type=str, default=".", help="Output directory path")

    # Command: validate-amp
    val_parser = subparsers.add_parser("validate-amp", help="Validate HTML file for AMP compliance")
    val_parser.add_argument("--file", type=str, required=True, help="Path to AMP HTML file")

    args = parser.parse_args()

    if args.command == "generate":
        target = args.ide or args.repo
        if not target:
            print("Error: Please specify either --ide or --repo.")
            sys.exit(1)

        ide_info = get_ide_info(target)
        output_dir = args.output_dir
        os.makedirs(output_dir, exist_ok=True)

        slug = ide_info["name"].lower().replace(" ", "_").replace("(", "").replace(")", "").replace("-", "_")

        # Generate AMP Blog Post
        blog_content = generate_amp_blog_post(ide_info)
        blog_filename = f"{slug}_blog_post.amp.html"
        blog_path = os.path.join(output_dir, blog_filename)
        with open(blog_path, "w", encoding="utf-8") as f:
            f.write(blog_content)

        # Generate Google Flow Video Spec
        video_spec = generate_google_flow_video_spec(ide_info)
        video_filename = f"{slug}_google_flow_video.json"
        video_path = os.path.join(output_dir, video_filename)
        with open(video_path, "w", encoding="utf-8") as f:
            json.dump(video_spec, f, indent=2)

        print(f"✅ Generated AMP Blog Post: {blog_path}")
        print(f"✅ Generated Google Flow Video Spec: {video_path}")

        # Validate generated AMP HTML
        is_valid, errors = validate_amp_html(blog_content)
        if is_valid:
            print("✨ AMP Validation Passed successfully!")
        else:
            print(f"❌ AMP Validation Warnings: {errors}")

    elif args.command == "validate-amp":
        if not os.path.exists(args.file):
            print(f"Error: File not found: {args.file}")
            sys.exit(1)

        with open(args.file, "r", encoding="utf-8") as f:
            content = f.read()

        is_valid, errors = validate_amp_html(content)
        if is_valid:
            print(f"✅ AMP Validation PASSED for '{args.file}'")
        else:
            print(f"❌ AMP Validation FAILED for '{args.file}':")
            for err in errors:
                print(f"  - {err}")
            sys.exit(1)

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
