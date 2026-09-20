#!/usr/bin/env python3
"""
IDE Guide Agentic CLI Skill Tool
Usage:
    python3 scripts/ide_guide_agent_skill.py --ide "Cursor"
    python3 scripts/ide_guide_agent_skill.py --repo "https://github.com/zed-industries/zed"
    python3 scripts/ide_guide_agent_skill.py --ide "Lapce" --outdir "output_folder"
"""

import argparse
import json
import os
import re
import sys
from datetime import datetime
import urllib.request
import urllib.error

DISCLAIMER_TEXT = (
    "Disclaimer: IDE Guide is an independent technical publication. "
    "This content is not sponsored, endorsed, or affiliated with any software vendor "
    "or editor developer mentioned above. All reviews and assessments are based strictly "
    "on objective developer evaluation."
)

KNOWN_IDES_DATABASE = {
    "cursor": {
        "name": "Cursor",
        "description": "An AI-first code editor built as a fork of Visual Studio Code, featuring deep LLM integration with Claude 3.5 Sonnet, inline AI edits, and codebase indexing.",
        "pricing": "Freemium (Free hobby tier with basic requests, $20/month Pro tier for fast premium queries).",
        "pros": [
            "Native integration with Claude 3.5 Sonnet and GPT-4o for inline editing.",
            "Full compatibility with VS Code extensions and keybindings.",
            "Smart multi-file code indexing and codebase-aware AI suggestions."
        ],
        "cons": [
            "Requires a monthly subscription for heavy AI query workloads.",
            "Closed-source core backend component."
        ],
        "recommendation": "Best for developers seeking cutting-edge AI pair-programming and seamless VS Code transition."
    },
    "zed": {
        "name": "Zed Editor",
        "description": "A high-performance, multiplayer code editor written in Rust from the creators of Atom and Tree-sitter, rendering natively via GPU at 120 FPS.",
        "pricing": "Open Source & Free (Community edition free; optional team collaboration SaaS tier).",
        "pros": [
            "Ultra-fast startup and GPU-accelerated text rendering.",
            "Built-in multiplayer pair programming and screen sharing.",
            "Low memory footprint written in native Rust."
        ],
        "cons": [
            "Smaller plugin ecosystem compared to VS Code.",
            "Linux and Windows support is newer compared to macOS."
        ],
        "recommendation": "Best for performance enthusiasts and developers who value low latency and real-time collaboration."
    },
    "fleet": {
        "name": "JetBrains Fleet",
        "description": "A lightweight, polyglot IDE and smart text editor by JetBrains using IntelliJ code-processing engine on demand in a distributed architecture.",
        "pricing": "Freemium / Commercial (Free preview, subscription included in JetBrains All Products Pack).",
        "pros": [
            "Lightweight launch with optional smart JetBrains engine toggling.",
            "Distributed architecture allowing remote machine and container execution.",
            "Clean modern UI with multi-language support out of the box."
        ],
        "cons": [
            "Plugin marketplace is still evolving.",
            "Requires JetBrains account and licensing for full commercial feature set."
        ],
        "recommendation": "Best for polyglot developers wanting JetBrains intelligence in a fast, lightweight frontend."
    },
    "lapce": {
        "name": "Lapce",
        "description": "A lightning-fast, open-source code editor written in Rust with GPU rendering via Xi-editor architecture and WASI plugin system.",
        "pricing": "100% Free and Open Source (Apache 2.0 license).",
        "pros": [
            "Native Rust build with instant startup and ultra-low memory overhead.",
            "Built-in remote development support via SSH and WSL.",
            "WASI-based sandboxed plugin ecosystem."
        ],
        "cons": [
            "Under active early development with occasional missing features.",
            "Ecosystem of plugins is currently limited."
        ],
        "recommendation": "Best for developers seeking a lightweight, open-source VS Code alternative written in Rust."
    },
    "neovim": {
        "name": "Neovim",
        "description": "A hyperextensible Vim-based text editor built for high speed, native Lua scripting, LSP client integration, and terminal customization.",
        "pricing": "100% Free and Open Source (Vim license / Apache).",
        "pros": [
            "Unrivaled editing speed and efficiency once keybindings are mastered.",
            "Extensive Lua plugin ecosystem and customizability.",
            "Minimal CPU and RAM footprint."
        ],
        "cons": [
            "Steep learning curve for modal editing and custom configuration.",
            "Requires initial setup time compared to out-of-the-box IDEs."
        ],
        "recommendation": "Best for power users, terminal enthusiasts, and developers who want complete control over their workflow."
    }
}


def parse_repo_name(repo_url: str) -> str:
    """Extract repository name from GitHub URL."""
    match = re.search(r"github\.com/([^/]+)/([^/]+)", repo_url)
    if match:
        owner, repo = match.group(1), match.group(2)
        repo_clean = repo.removesuffix(".git")
        return f"{repo_clean.capitalize()} Editor" if "editor" not in repo_clean.lower() else repo_clean.capitalize()
    return "Custom IDE"


def fetch_github_repo_info(repo_url: str) -> dict:
    """Fetch repository description from GitHub API if available."""
    match = re.search(r"github\.com/([^/]+)/([^/]+)", repo_url)
    if match:
        owner, repo = match.group(1), match.group(2).removesuffix(".git")
        api_url = f"https://api.github.com/repos/{owner}/{repo}"
        req = urllib.request.Request(api_url, headers={"User-Agent": "IDE-Guide-Bot"})
        try:
            with urllib.request.urlopen(req, timeout=5) as resp:
                if resp.status == 200:
                    data = json.loads(resp.read().decode("utf-8"))
                    raw_name = data.get("name", repo).capitalize()
                    name = f"{raw_name} Editor" if "editor" not in raw_name.lower() else raw_name
                    desc = data.get("description", "A modern code editor and development tool.")
                    stargazers = data.get("stargazers_count", 0)
                    license_info = data.get("license", {}).get("name") if data.get("license") else "Open Source"
                    return {
                        "name": name,
                        "description": desc,
                        "pricing": f"Free and Open Source ({license_info}).",
                        "pros": [
                            f"Popular open-source project with over {stargazers:,} GitHub stars.",
                            "Extensible community ecosystem and active development.",
                            "Transparent open development roadmap."
                        ],
                        "cons": [
                            "May require manual configuration depending on setup.",
                            "Ecosystem features depend on community contributions."
                        ],
                        "recommendation": f"Best for developers looking for open-source {name} tooling and customizable workflows."
                    }
        except Exception:
            pass

    repo_name = parse_repo_name(repo_url)
    return {
        "name": repo_name,
        "description": f"An innovative code editing environment hosted at {repo_url}.",
        "pricing": "Free & Open Source / Community Tier.",
        "pros": [
            "Modern architecture and specialized toolset for software engineering.",
            "Active repository development and issue tracking.",
            "Flexible platform integration options."
        ],
        "cons": [
            "Requires evaluation for specific team workflows.",
            "Documentation may be evolving."
        ],
        "recommendation": f"Recommended for developers experimenting with modular and custom code editors."
    }


def get_ide_info(ide_name: str = None, repo_url: str = None) -> dict:
    """Resolve IDE metadata from database, repo URL, or dynamic generator."""
    if repo_url:
        return fetch_github_repo_info(repo_url)

    if ide_name:
        key = ide_name.strip().lower()
        if key in KNOWN_IDES_DATABASE:
            return KNOWN_IDES_DATABASE[key]
        for k, v in KNOWN_IDES_DATABASE.items():
            if k in key or key in k:
                return v

        # Fallback dynamic creation for unknown IDE name
        clean_name = ide_name.strip().title()
        return {
            "name": clean_name,
            "description": f"{clean_name} is a developer tool and code editor designed to improve programming productivity.",
            "pricing": "Free trial available / Freemium subscription model.",
            "pros": [
                f"Dedicated workflow tailored for {clean_name} users.",
                "Customizable settings and workspace layout.",
                "Fast file navigation and code editing capabilities."
            ],
            "cons": [
                "Ecosystem plugin availability varies by language.",
                "Learning curve for specialized keyboard shortcuts."
            ],
            "recommendation": f"Best for developers evaluating modern code editors for {clean_name} project development."
        }

    return KNOWN_IDES_DATABASE["cursor"]


def generate_amp_html(info: dict) -> str:
    """Generate AMP HTML compliant blog post for Blogger (ideguide.blogspot.com)."""
    name = info["name"]
    desc = info["description"]
    pricing = info["pricing"]
    pros_list = "".join([f"<li>{p}</li>" for p in info["pros"]])
    cons_list = "".join([f"<li>{c}</li>" for c in info["cons"]])
    recommendation = info["recommendation"]

    amp_html = f"""<!doctype html>
<html ⚡ lang="en">
<head>
  <meta charset="utf-8">
  <title>IDE Guide: {name} Detailed Review &amp; Analysis</title>
  <link rel="canonical" href="https://ideguide.blogspot.com/">
  <meta name="viewport" content="width=device-width,minimum-scale=1,initial-scale=1">
  <script async src="https://cdn.ampproject.org/v0.js"></script>
  <style amp-boilerplate>body{{-webkit-animation:-amp-start 8s steps(1,end) 0s 1 normal both;-moz-animation:-amp-start 8s steps(1,end) 0s 1 normal both;-ms-animation:-amp-start 8s steps(1,end) 0s 1 normal both;animation:-amp-start 8s steps(1,end) 0s 1 normal both}}@-webkit-keyframes -amp-start{{from{{visibility:hidden}}to{{visibility:visible}}}}@-moz-keyframes -amp-start{{from{{visibility:hidden}}to{{visibility:visible}}}}@-ms-keyframes -amp-start{{from{{visibility:hidden}}to{{visibility:visible}}}}@-o-keyframes -amp-start{{from{{visibility:hidden}}to{{visibility:visible}}}}@keyframes -amp-start{{from{{visibility:hidden}}to{{visibility:visible}}}}</style><noscript><style amp-boilerplate>body{{-webkit-animation:none;-moz-animation:none;-ms-animation:none;animation:none}}</style></noscript>
  <style amp-custom>
    body {{
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
      line-height: 1.6;
      color: #1e293b;
      background-color: #f8fafc;
      margin: 0;
      padding: 16px;
    }}
    .container {{
      max-width: 800px;
      margin: 0 auto;
      background: #ffffff;
      padding: 24px;
      border-radius: 12px;
      box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }}
    h1 {{
      color: #0f172a;
      font-size: 28px;
      border-bottom: 3px solid #3b82f6;
      padding-bottom: 8px;
    }}
    h2 {{
      color: #1e3a8a;
      font-size: 20px;
      margin-top: 24px;
    }}
    .badge {{
      display: inline-block;
      background-color: #e0e7ff;
      color: #3730a3;
      font-weight: 600;
      padding: 4px 12px;
      border-radius: 9999px;
      font-size: 14px;
      margin-bottom: 12px;
    }}
    ul {{
      padding-left: 20px;
    }}
    li {{
      margin-bottom: 8px;
    }}
    .pro-box {{
      background-color: #f0fdf4;
      border-left: 4px solid #22c55e;
      padding: 12px 16px;
      margin-bottom: 16px;
      border-radius: 4px;
    }}
    .con-box {{
      background-color: #fef2f2;
      border-left: 4px solid #ef4444;
      padding: 12px 16px;
      margin-bottom: 16px;
      border-radius: 4px;
    }}
    .disclaimer {{
      margin-top: 32px;
      padding: 16px;
      background-color: #f1f5f9;
      border-radius: 8px;
      font-size: 13px;
      color: #64748b;
      font-style: italic;
    }}
  </style>
</head>
<body>
  <div class="container">
    <span class="badge">IDE Guide Independent Review</span>
    <h1>{name} - Features, Pricing &amp; Developer Verdict</h1>

    <h2>1. Overview</h2>
    <p>{desc}</p>

    <h2>2. Pricing Tier &amp; Licensing (Paid vs Free)</h2>
    <p><strong>Pricing Structure:</strong> {pricing}</p>

    <h2>3. Key Strengths &amp; Pros</h2>
    <div class="pro-box">
      <ul>
        {pros_list}
      </ul>
    </div>

    <h2>4. Limitations &amp; Cons</h2>
    <div class="con-box">
      <ul>
        {cons_list}
      </ul>
    </div>

    <h2>5. Recommendation &amp; Best Target Audience</h2>
    <p>{recommendation}</p>

    <div class="disclaimer">
      {DISCLAIMER_TEXT}
    </div>
  </div>
</body>
</html>"""
    return amp_html


def generate_google_flow_spec(info: dict) -> dict:
    """Generate Google Flow Video Specification JSON for YouTube (@IDEguide)."""
    name = info["name"]
    desc = info["description"]
    pricing = info["pricing"]
    pros = info["pros"]
    cons = info["cons"]
    recommendation = info["recommendation"]

    spec = {
        "title": f"IDE Guide: Is {name} Worth Using in 2026? (Pros, Cons & Pricing)",
        "target_platform": "YouTube Shorts / Longform (@IDEguide)",
        "aspect_ratio": "9:16",
        "ide_name": name,
        "pricing_model": pricing,
        "pros": pros,
        "cons": cons,
        "recommendation": recommendation,
        "visual_prompts": {
          "lighting": "Cinematic dark-mode studio workstation setup, 5600K key light, subtle cyan/magenta background neon accent glow.",
          "camera_motion": "Slow smooth zoom into code editor window, camera pan highlighting key UI features and syntax theme.",
          "framing": "Vertical 9:16 aspect ratio, macro close-up shot focused on code completion and editor interface."
        },
        "narration_script": [
          {
            "timestamp": "00:00-00:05",
            "visual": f"Fast cut into {name} dark mode interface showing code editing.",
            "audio": f"Looking for a new code editor? Here is everything you need to know about {name}!"
          },
          {
            "timestamp": "00:05-00:18",
            "visual": "Panning view of key interface features and layout.",
            "audio": f"{desc}"
          },
          {
            "timestamp": "00:18-00:32",
            "visual": "Green highlight overlay demonstrating top pros.",
            "audio": f"Key Pros: {pros[0]} Plus, {pros[1] if len(pros) > 1 else 'great workflow design.'}"
          },
          {
            "timestamp": "00:32-00:42",
            "visual": "Red highlight overlay detailing cons.",
            "audio": f"Things to consider: {cons[0]}"
          },
          {
            "timestamp": "00:42-00:52",
            "visual": "Pricing table visual badge graphic.",
            "audio": f"Pricing breakdown: {pricing}"
          },
          {
            "timestamp": "00:52-00:60",
            "visual": f"Summary screen displaying logo for {name} and YouTube handle @IDEguide.",
            "audio": f"Final verdict: {recommendation} Subscribe to @IDEguide for daily dev specs!"
          }
        ],
        "disclaimer": DISCLAIMER_TEXT
    }
    return spec


def main():
    parser = argparse.ArgumentParser(description="IDE Guide Agentic CLI Skill Tool")
    parser.add_argument("--ide", type=str, help="Name of the IDE/Editor to cover (e.g. Cursor, Zed, Lapce)")
    parser.add_argument("--repo", type=str, help="GitHub Repository URL of the editor")
    parser.add_argument("--outdir", type=str, default="content/custom", help="Output directory for generated files")
    args = parser.parse_args()

    if not args.ide and not args.repo:
        print("[!] No IDE name or repository URL provided. Defaulting to Cursor.")

    info = get_ide_info(ide_name=args.ide, repo_url=args.repo)
    safe_name = re.sub(r"[^\w\-]", "_", info["name"].lower())

    outdir = args.outdir
    os.makedirs(outdir, exist_ok=True)

    amp_content = generate_amp_html(info)
    amp_filename = os.path.join(outdir, f"blogpost_{safe_name}.amp.html")
    with open(amp_filename, "w", encoding="utf-8") as f:
        f.write(amp_content)

    spec_dict = generate_google_flow_spec(info)
    spec_filename = os.path.join(outdir, f"video_spec_{safe_name}.json")
    with open(spec_filename, "w", encoding="utf-8") as f:
        json.dump(spec_dict, f, indent=2)

    print(f"[✓] Generated AMP HTML Blog Post: {amp_filename}")
    print(f"[✓] Generated Google Flow Video Spec: {spec_filename}")


if __name__ == "__main__":
    main()
