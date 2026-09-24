#!/usr/bin/env python3
"""
Agentic Skill Generator for IDE Guide
Generates valid Blogger AMP HTML blog posts and Google Flow AI Video Specifications
for any given IDE / Code Editor.
"""

import argparse
import json
import os
import sys
from typing import Any, Dict

DISCLAIMER_TEXT = (
    "Disclaimer: IDE Guide is an independent technical publication. "
    "This content is not sponsored, endorsed, or affiliated with any software vendor "
    "or editor developer mentioned above. All reviews and assessments are based strictly "
    "on objective developer evaluation."
)

IDE_DATABASE = {
    "cursor": {
        "name": "Cursor IDE",
        "tagline": "The AI-first Code Editor built for speed and intelligent auto-completion",
        "developer": "Anysphere",
        "pricing_type": "Freemium",
        "pricing_details": "Free Hobby tier (200 GPT-3.5 / 50 slow GPT-4 uses/mo), Pro at $20/mo, Business at $40/user/mo.",
        "license": "Proprietary (VS Code Fork)",
        "target_audience": "Full-stack developers, AI enthusiast engineers, rapid prototyping teams.",
        "pros": [
            "Native multi-file AI edits with Cmd+K and instant inline diffs.",
            "Deep repository indexing with vector embeddings for semantic context search.",
            "Seamless 1-click migration from existing VS Code settings and extension suite.",
            "Fast tab-autocompletion powered by fine-tuned custom language models."
        ],
        "cons": [
            "Requires cloud query processing for advanced AI models (privacy concerns for closed codebases).",
            "Subscription cost can add up for large dev teams.",
            "Occasional context window truncation on massive monolithic repositories."
        ],
        "verdict": "Best overall AI code editor in 2026 for developers seeking seamless LLM integration in a familiar VS Code environment.",
        "primary_color": "#007acc"
    },
    "zed": {
        "name": "Zed Editor",
        "tagline": "Blazingly fast multi-player code editor written in Rust",
        "developer": "Zed Industries",
        "pricing_type": "Free / Open Source (GPL / Apache 2.0)",
        "pricing_details": "100% Free for local usage. Zed Predict AI optional subscription.",
        "license": "Open Source (GPL v3 / Apache 2.0)",
        "target_audience": "Performance-obsessed developers, Rust/C++ engineers, real-time pair programmers.",
        "pros": [
            "GPU-accelerated rendering engine running consistently at 120+ FPS.",
            "Ultralight memory footprint (~100MB RAM vs 1GB+ Electron editors).",
            "Built-in real-time multiplayer collaboration with low latency cursor sharing.",
            "Native Tree-sitter parsing for instant syntax highlighting and error checking."
        ],
        "cons": [
            "Smaller extension ecosystem compared to VS Code Marketplace.",
            "Linux and Windows versions are still rapidly evolving compared to macOS.",
            "Fewer GUI visual debugging tools out of the box."
        ],
        "verdict": "The undisputed performance champion. Essential for developers who demand instant editor responsiveness and low RAM consumption.",
        "primary_color": "#f26522"
    },
    "vscode": {
        "name": "Visual Studio Code",
        "tagline": "The universal code editor powered by an unmatched extension ecosystem",
        "developer": "Microsoft",
        "pricing_type": "Free",
        "pricing_details": "100% Free core editor. Optional paid Copilot subscriptions.",
        "license": "MIT (Core source) / Proprietary (Microsoft Binaries)",
        "target_audience": "All software engineers, web developers, data scientists, beginners & pros.",
        "pros": [
            "Massive marketplace with over 50,000 extensions and themes.",
            "Exceptional remote development features (SSH, Containers, WSL).",
            "Comprehensive integrated debugger and terminal stack.",
            "Massive global community support and active release cycles."
        ],
        "cons": [
            "Electron framework baseline consumes noticeable memory (RAM intensive with 20+ extensions).",
            "Default telemetry collection requires explicit user opt-out.",
            "Can feel heavy or slow when opening multi-gigabyte log or data files."
        ],
        "verdict": "The gold standard for general software development. Versatile, reliable, and backed by the richest ecosystem in tech.",
        "primary_color": "#0078d4"
    },
    "intellij": {
        "name": "JetBrains IntelliJ IDEA",
        "tagline": "The ultimate intelligent IDE for Java, Kotlin, and enterprise polyglot development",
        "developer": "JetBrains",
        "pricing_type": "Freemium",
        "pricing_details": "Community Edition is Free & Open Source. Ultimate Edition is $16.90/mo or $169/yr.",
        "license": "Apache 2.0 (Community) / Commercial (Ultimate)",
        "target_audience": "Enterprise Java/Kotlin engineers, Spring Boot backend developers, large project leads.",
        "pros": [
            "Unrivaled deep AST static code analysis, automated refactoring, and quick-fixes.",
            "Native deep Spring Framework, database, and microservices integration.",
            "Robust built-in version control and merge conflict resolution UI.",
            "First-class Kotlin and JVM ecosystem support."
        ],
        "cons": [
            "High memory and CPU demand on initial project index generation.",
            "Commercial license fee required for enterprise backend web frameworks.",
            "Slower cold launch times compared to lightweight text editors."
        ],
        "verdict": "The king of JVM and enterprise software architecture. Essential for serious backend engineers.",
        "primary_color": "#000000"
    },
    "windsurf": {
        "name": "Windsurf Editor",
        "tagline": "The AI Flow code editor designed for continuous context-aware coding",
        "developer": "Codeium",
        "pricing_type": "Freemium",
        "pricing_details": "Free tier with generous AI credits. Pro tier available at $15/mo.",
        "license": "Proprietary",
        "target_audience": "Full-stack developers and AI-first engineering teams seeking deep agentic workflows.",
        "pros": [
            "Cascade AI flow engine keeps real-time context across entire codebase.",
            "Deep integration with terminal command execution and automatic bug resolution.",
            "Fast response times with low latent token streaming.",
            "Built on familiar VS Code foundation for instant plugin compatibility."
        ],
        "cons": [
            "Relatively new tool with fast-shifting feature iterations.",
            "Cloud reliance for AI reasoning agents.",
            "Occasional context drift during multi-hour refactoring sessions."
        ],
        "verdict": "A revolutionary agentic editor experience that excels at multi-step coding workflows.",
        "primary_color": "#09b6a2"
    },
    "neovim": {
        "name": "Neovim",
        "tagline": "Hyperextensible Vim-based text editor for keyboard-driven efficiency",
        "developer": "Neovim Core Team",
        "pricing_type": "Free / Open Source",
        "pricing_details": "100% Free (Apache 2.0 / Vim license).",
        "license": "Open Source",
        "target_audience": "Terminal purists, DevOps engineers, power users who love modal editing.",
        "pros": [
            "Near-zero startup time and ultra-minimal memory usage (~30MB).",
            "Lua configuration engine allows complete custom editor customization.",
            "Built-in Language Server Protocol (LSP) client for IDE-grade code completion.",
            "Keyboard-centric workflow provides unmatched editing speed once mastered."
        ],
        "cons": [
            "Steep learning curve for new developers non-fluent in modal editing.",
            "Requires manual configuration and maintenance of plugins.",
            "No out-of-the-box GUI controls or mouse-first interaction."
        ],
        "verdict": "The supreme choice for terminal wizards who want complete ownership over their development workflow.",
        "primary_color": "#57a143"
    }
}

def get_ide_data(ide_key_or_name: str) -> Dict[str, Any]:
    key = ide_key_or_name.lower().strip()
    if key in IDE_DATABASE:
        return IDE_DATABASE[key]

    # Fallback/dynamic generator for unknown IDE / repo
    clean_name = ide_key_or_name.strip().title()
    return {
        "name": f"{clean_name} Editor",
        "tagline": f"Modern code editor tailored for developer efficiency and clean workflow.",
        "developer": f"{clean_name} Open Source Community",
        "pricing_type": "Free / Open Source",
        "pricing_details": "Free community edition with optional commercial upgrades.",
        "license": "Open Source / Community",
        "target_audience": "Software engineers and technology enthusiasts.",
        "pros": [
            "Modern user interface with responsive code execution.",
            "Flexible plugin framework and customizable themes.",
            "Active developer community and regular maintenance."
        ],
        "cons": [
            "Ecosystem still growing compared to legacy editors.",
            "May require initial configuration setup."
        ],
        "verdict": f"A promising editor option for developers interested in trying fresh developer tooling for {clean_name}.",
        "primary_color": "#4a90e2"
    }

def generate_amp_blog(ide_data: Dict[str, Any], blog_url: str = "https://ideguide.blogspot.com/") -> str:
    """
    Generates standard Blogger-compliant AMP HTML post.
    """
    pros_html = "".join([f"<li><strong>{p.split(':')[0] if ':' in p else 'Feature'}:</strong> {p}</li>" for p in ide_data["pros"]])
    cons_html = "".join([f"<li><strong>{c.split(':')[0] if ':' in c else 'Limitation'}:</strong> {c}</li>" for c in ide_data["cons"]])

    amp_html = f"""<!doctype html>
<html ⚡ lang="en">
<head>
  <meta charset="utf-8">
  <title>{ide_data['name']} Comprehensive Review - Good, Bad, Pricing & Verdict | IDE Guide</title>
  <link rel="canonical" href="{blog_url}">
  <meta name="viewport" content="width=device-width,minimum-scale=1,initial-scale=1">
  <style amp-boilerplate>body{{-webkit-animation:-amp-start 8s steps(1,end) 0s 1 normal both;-moz-animation:-amp-start 8s steps(1,end) 0s 1 normal both;-ms-animation:-amp-start 8s steps(1,end) 0s 1 normal both;animation:-amp-start 8s steps(1,end) 0s 1 normal both}}@-webkit-keyframes -amp-start{{from{{visibility:hidden}}to{{visibility:visible}}}}@-moz-keyframes -amp-start{{from{{visibility:hidden}}to{{visibility:visible}}}}@-ms-keyframes -amp-start{{from{{visibility:hidden}}to{{visibility:visible}}}}@-o-keyframes -amp-start{{from{{visibility:hidden}}to{{visibility:visible}}}}@keyframes -amp-start{{from{{visibility:hidden}}to{{visibility:visible}}}}</style><noscript><style amp-boilerplate>body{{-webkit-animation:none;-moz-animation:none;-ms-animation:none;animation:none}}</style></noscript>
  <script async src="https://cdn.ampproject.org/v0.js"></script>
  <style amp-custom>
    body {{
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
      line-height: 1.6;
      color: #1a1a1a;
      background-color: #f9f9fb;
      margin: 0;
      padding: 0;
    }}
    .container {{
      max-width: 800px;
      margin: 20px auto;
      padding: 24px;
      background: #ffffff;
      border-radius: 12px;
      box-shadow: 0 4px 20px rgba(0, 0, 0, 0.06);
    }}
    .header-badge {{
      display: inline-block;
      background-color: {ide_data['primary_color']};
      color: #ffffff;
      font-size: 13px;
      font-weight: 700;
      padding: 4px 12px;
      border-radius: 20px;
      text-transform: uppercase;
      letter-spacing: 0.5px;
    }}
    h1 {{
      font-size: 28px;
      color: #111111;
      margin-top: 12px;
      margin-bottom: 8px;
    }}
    .tagline {{
      font-size: 16px;
      color: #555555;
      font-style: italic;
      margin-bottom: 24px;
    }}
    .info-card {{
      background: #f0f4f8;
      border-left: 5px solid {ide_data['primary_color']};
      padding: 16px;
      border-radius: 6px;
      margin-bottom: 24px;
    }}
    .info-card p {{
      margin: 6px 0;
    }}
    h2 {{
      font-size: 20px;
      color: #222222;
      border-bottom: 2px solid #eaeaea;
      padding-bottom: 6px;
      margin-top: 28px;
    }}
    ul {{
      padding-left: 20px;
    }}
    li {{
      margin-bottom: 10px;
    }}
    .pros-box {{
      background-color: #f0fff4;
      border: 1px solid #c6f6d5;
      border-radius: 8px;
      padding: 16px;
      margin-bottom: 20px;
    }}
    .cons-box {{
      background-color: #fff5f5;
      border: 1px solid #fed7d7;
      border-radius: 8px;
      padding: 16px;
      margin-bottom: 20px;
    }}
    .verdict-box {{
      background-color: #f7fafc;
      border: 2px dashed {ide_data['primary_color']};
      padding: 20px;
      border-radius: 8px;
      margin-top: 24px;
      text-align: center;
    }}
    .disclaimer {{
      font-size: 12px;
      color: #777777;
      background: #eee;
      padding: 12px;
      border-radius: 6px;
      margin-top: 32px;
      line-height: 1.4;
    }}
  </style>
</head>
<body>
  <div class="container">
    <span class="header-badge">{ide_data['pricing_type']}</span>
    <h1>{ide_data['name']} Evaluation Guide</h1>
    <p class="tagline">"{ide_data['tagline']}"</p>

    <div class="info-card">
      <p><strong>Developer / Creator:</strong> {ide_data['developer']}</p>
      <p><strong>License:</strong> {ide_data['license']}</p>
      <p><strong>Pricing:</strong> {ide_data['pricing_details']}</p>
      <p><strong>Target Audience:</strong> {ide_data['target_audience']}</p>
    </div>

    <h2>The Good (Key Advantages)</h2>
    <div class="pros-box">
      <ul>
        {pros_html}
      </ul>
    </div>

    <h2>The Bad (Drawbacks & Considerations)</h2>
    <div class="cons-box">
      <ul>
        {cons_html}
      </ul>
    </div>

    <h2>Verdict & Recommendation</h2>
    <div class="verdict-box">
      <h3>Who Should Use {ide_data['name']}?</h3>
      <p>{ide_data['verdict']}</p>
    </div>

    <div class="disclaimer">
      {DISCLAIMER_TEXT}
    </div>
  </div>
</body>
</html>"""
    return amp_html

def generate_video_spec(ide_data: Dict[str, Any], youtube_channel: str = "https://www.youtube.com/@IDEguide") -> Dict[str, Any]:
    """
    Generates structured video script and Google Flow visual prompt specs.
    """
    video_title_1 = f"{ide_data['name']} in 2026: Is It Worth It? (Honest Review)"
    video_title_2 = f"Why Developers Are (Or Aren't) Switching to {ide_data['name']}"
    video_title_3 = f"{ide_data['name']} - Good vs Bad Breakdown ({ide_data['pricing_type']})"

    shorts_script = (
        f"Thinking of using {ide_data['name']}? Here is what you need to know in 60 seconds! "
        f"The GOOD: {ide_data['pros'][0]} "
        f"The BAD: {ide_data['cons'][0]} "
        f"PRICING: {ide_data['pricing_type']}. "
        f"VERDICT: {ide_data['verdict']} "
        f"Subscribe to IDE Guide for daily developer tool breakdowns!"
    )

    scenes = [
        {
            "scene_number": 1,
            "duration": "0:00 - 0:10",
            "section": "Hook & Introduction",
            "voiceover": f"Is {ide_data['name']} the editor you should be using today? Let's break down the good, the bad, and the pricing.",
            "google_flow_prompt": (
                f"Cinematic close-up tracking shot of a glowing mechanical keyboard and sleek dark monitor "
                f"displaying {ide_data['name']} code editor with vibrant dynamic syntax highlighting, "
                f"cyberpunk neon ambient desk lighting ({ide_data['primary_color']}), 4K resolution, 60fps."
            ),
            "aspect_ratio": "16:9 for YouTube / 9:16 for Shorts"
        },
        {
            "scene_number": 2,
            "duration": "0:10 - 0:40",
            "section": "The Good (Pros)",
            "voiceover": f"Key strengths include: {ide_data['pros'][0]} Also, {ide_data['pros'][1]}",
            "google_flow_prompt": (
                f"Split-screen comparison shot showing smooth UI performance, instant code autocompletion, "
                f"and rapid file search in {ide_data['name']}. Macro lens camera movement over glowing editor UI elements."
            ),
            "aspect_ratio": "16:9 for YouTube / 9:16 for Shorts"
        },
        {
            "scene_number": 3,
            "duration": "0:40 - 1:10",
            "section": "The Bad (Cons) & Pricing",
            "voiceover": f"On the flip side: {ide_data['cons'][0]} Regarding pricing, it is {ide_data['pricing_type']}.",
            "google_flow_prompt": (
                f"Aesthetic over-the-shoulder shot of a software developer pondering code on screen, "
                f"subtle orange warning accents highlighting performance/pricing breakdown charts, cinematic soft focus background."
            ),
            "aspect_ratio": "16:9 for YouTube / 9:16 for Shorts"
        },
        {
            "scene_number": 4,
            "duration": "1:10 - 1:30",
            "section": "Final Verdict & Outro",
            "voiceover": f"Our verdict: {ide_data['verdict']} Check out our full AMP article on ideguide.blogspot.com and subscribe to @IDEguide!",
            "google_flow_prompt": (
                f"Dynamic push-in shot of IDE Guide channel branding logo end-screen with high-tech particles, "
                f"links to @IDEguide channel and blog, professional tech studio aesthetic."
            ),
            "aspect_ratio": "16:9 for YouTube / 9:16 for Shorts"
        }
    ]

    return {
        "ide_name": ide_data["name"],
        "youtube_channel": youtube_channel,
        "title_options": [video_title_1, video_title_2, video_title_3],
        "shorts_script_60s": shorts_script,
        "full_video_scenes": scenes,
        "disclaimer": DISCLAIMER_TEXT
    }

def main():
    parser = argparse.ArgumentParser(description="IDE Guide Agentic Skill Generator")
    parser.add_argument("--ide", type=str, required=True, help="IDE name (e.g., cursor, zed, vscode, intellij, windsurf, neovim)")
    parser.add_argument("--outdir", type=str, default=".", help="Output directory for generated files")
    args = parser.parse_args()

    ide_data = get_ide_data(args.ide)
    amp_html = generate_amp_blog(ide_data)
    video_spec = generate_video_spec(ide_data)

    os.makedirs(args.outdir, exist_ok=True)
    slug = ide_data["name"].lower().replace(" ", "_")

    html_path = os.path.join(args.outdir, f"{slug}_amp_blog.html")
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(amp_html)

    spec_path = os.path.join(args.outdir, f"{slug}_video_spec.json")
    with open(spec_path, "w", encoding="utf-8") as f:
        json.dump(video_spec, f, indent=2)

    print(f"✨ Successfully generated content for {ide_data['name']}:")
    print(f"  📄 AMP Blog Post HTML: {html_path}")
    print(f"  🎬 Google Flow Video Spec: {spec_path}")

if __name__ == "__main__":
    main()
