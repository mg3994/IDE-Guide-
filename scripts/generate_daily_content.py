#!/usr/bin/env python3
"""
Daily Content Generator for IDE Guide.
Generates 3 AMP HTML blog posts (for Blogger) and 3 Google Flow video specs (for YouTube/@IDEguide).
Outputs to content/YYYY-MM-DD/ and updates content/history.json.
"""

import json
import os
import sys
from datetime import datetime, timezone
from typing import Dict, Any, List

# Ensure scripts directory can be imported directly when run as script
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.amp_validator import validate_amp_html, REQUIRED_DISCLAIMER

IDE_DATABASE: List[Dict[str, Any]] = [
    {
        "id": "vscode",
        "name": "Visual Studio Code",
        "vendor": "Microsoft",
        "pricing_type": "Free / Open Source (Core)",
        "pricing_details": "Completely free core editor with free extension marketplace.",
        "overview": "Visual Studio Code is the industry-standard code editor known for vast extension ecosystem, fast startup, and universal language support.",
        "pros": ["Massive extension ecosystem", "Extremely customizable", "Built-in Git integration and debugging", "Strong community support"],
        "cons": ["High memory usage with heavy extensions", "Can feel bloated compared to minimal editors"],
        "best_for": "Web development, Python, Node.js, and general multi-language full-stack developers.",
        "image_url": "https://images.unsplash.com/photo-1555066931-4365d14bab8c?w=800&auto=format&fit=crop"
    },
    {
        "id": "cursor",
        "name": "Cursor AI",
        "vendor": "Anysphere",
        "pricing_type": "Freemium",
        "pricing_details": "Free tier with limited GPT-4o/Claude queries; Pro plan at $20/month.",
        "overview": "Cursor is a fork of VS Code built from the ground up for deep AI integration, featuring codebase indexing and multi-file code editing.",
        "pros": ["Native codebase context indexing", "Multi-file edit capabilities (Composer)", "Seamless migration from VS Code extensions"],
        "cons": ["Subscription cost for heavy usage", "Requires cloud connection for advanced AI models"],
        "best_for": "Developers wanting maximum AI productivity and seamless code generation directly in their editor.",
        "image_url": "https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?w=800&auto=format&fit=crop"
    },
    {
        "id": "windsurf",
        "name": "Windsurf Editor",
        "vendor": "Codeium",
        "pricing_type": "Freemium",
        "pricing_details": "Free tier with generous AI credits; Pro plan starting at $15/month.",
        "overview": "Windsurf by Codeium introduces Cascade AI, an agentic coding assistant that acts in flow state alongside developers.",
        "pros": ["Cascade agentic workflow", "Ultra-fast response time", "Deep context awareness across directories"],
        "cons": ["Relatively new ecosystem", "Occasional context indexing sync delays"],
        "best_for": "Engineers seeking an agentic IDE experience with low-latency AI interactions.",
        "image_url": "https://images.unsplash.com/photo-1542831371-29b0f74f9713?w=800&auto=format&fit=crop"
    },
    {
        "id": "intellij_idea",
        "name": "IntelliJ IDEA",
        "vendor": "JetBrains",
        "pricing_type": "Freemium / Paid",
        "pricing_details": "Community Edition is free; Ultimate Edition starts at $169/year for individuals.",
        "overview": "IntelliJ IDEA is the premier Java & Kotlin IDE with unmatched static code analysis, refactoring, and enterprise framework tooling.",
        "pros": ["World-class Java/Kotlin refactoring", "Superior static analysis & inspection", "Rich enterprise plugin ecosystem"],
        "cons": ["Heavy memory requirement (RAM hungry)", "Paid subscription required for Ultimate capabilities"],
        "best_for": "Enterprise Java, Kotlin, Spring Boot, and backend software engineers.",
        "image_url": "https://images.unsplash.com/photo-1517694712202-14dd9538aa97?w=800&auto=format&fit=crop"
    },
    {
        "id": "zed",
        "name": "Zed Editor",
        "vendor": "Zed Industries",
        "pricing_type": "Free / Open Source",
        "pricing_details": "Open source code editor; optional team collaboration tier.",
        "overview": "Zed is a high-performance, multiplayer code editor written in Rust, designed to utilize GPU acceleration for lighting-fast frame rates.",
        "pros": ["Blazing fast Startup and file rendering", "Native Rust performance with GPU rendering", "Built-in real-time multiplayer pair programming"],
        "cons": ["Smaller extension ecosystem compared to VS Code", "Fewer UI customization options currently"],
        "best_for": "Performance enthusiasts, Rust/Go developers, and collaborative pair programming teams.",
        "image_url": "https://images.unsplash.com/photo-1515879218367-8466d910aaa4?w=800&auto=format&fit=crop"
    },
    {
        "id": "neovim",
        "name": "Neovim",
        "vendor": "Community / Open Source",
        "pricing_type": "Free / Open Source",
        "pricing_details": "100% free and open source forever.",
        "overview": "Neovim is a hyperextensible Vim-based text editor built for extreme speed, modal editing, and Lua-driven extensibility.",
        "pros": ["Unrivaled keyboard navigation speed", "Zero GUI overhead with minimal memory usage", "Infinite Lua plugin customization"],
        "cons": ["Steep learning curve for modal editing", "Requires initial configuration setup time"],
        "best_for": "Terminal warriors, DevOps engineers, and developers who love modal editing and customization.",
        "image_url": "https://images.unsplash.com/photo-1629654297299-c8506221ca97?w=800&auto=format&fit=crop"
    },
    {
        "id": "pycharm",
        "name": "PyCharm",
        "vendor": "JetBrains",
        "pricing_type": "Freemium / Paid",
        "pricing_details": "Community Edition is free; Professional Edition starts at $99/year.",
        "overview": "PyCharm is the flagship IDE specifically optimized for Python, Django, Data Science, and Web Development.",
        "pros": ["Smart Python autocomplete & inspections", "Built-in scientific notebook and database tools", "Seamless virtualenv and conda environment integration"],
        "cons": ["Higher resource utilization", "Pro features locked behind paywall"],
        "best_for": "Python developers, Data Scientists, and Django backend engineers.",
        "image_url": "https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?w=800&auto=format&fit=crop"
    },
    {
        "id": "sublime_text",
        "name": "Sublime Text",
        "vendor": "Sublime HQ",
        "pricing_type": "Paid (Evaluation available)",
        "pricing_details": "Free evaluation with indefinite nag pop-ups; license costs $99.",
        "overview": "Sublime Text is legendary for its ultra-fast speed, minimal UI, multi-caret editing, and instant file opening.",
        "pros": ["Instant launch speed", "Handles multi-gigabyte files easily", "Clean, distraction-free UI"],
        "cons": ["Proprietary paid license", "Extension ecosystem less active than VS Code"],
        "best_for": "Developers who prioritize raw editor speed and lightweight file editing.",
        "image_url": "https://images.unsplash.com/photo-1461749280684-dccba630e2f6?w=800&auto=format&fit=crop"
    },
    {
        "id": "fleet",
        "name": "Fleet",
        "vendor": "JetBrains",
        "pricing_type": "Freemium",
        "pricing_details": "Free preview mode; upcoming tiered JetBrains subscription integration.",
        "overview": "Fleet is JetBrains' modern lightweight polyglot editor with smart Smart Mode capabilities and cloud workspace support.",
        "pros": ["Sleek modern UI", "Quick toggle between lightweight and full smart mode", "Distributed architecture"],
        "cons": ["Still expanding feature set", "Ecosystem in early stages"],
        "best_for": "Developers wanting JetBrains intelligence in a modern VS Code-like lightweight container.",
        "image_url": "https://images.unsplash.com/photo-1555066931-4365d14bab8c?w=800&auto=format&fit=crop"
    }
]


def generate_amp_blog_post(ide: Dict[str, Any]) -> str:
    """Generates valid AMP HTML content for Blogger."""
    pros_html = "".join([f"<li>✅ {pro}</li>" for pro in ide["pros"]])
    cons_html = "".join([f"<li>❌ {con}</li>" for con in ide["cons"]])

    html = f"""<!doctype html>
<html ⚡ lang="en">
<head>
  <meta charset="utf-8">
  <title>{ide['name']} Review & Developer Guide | IDE Guide</title>
  <meta name="viewport" content="width=device-width,minimum-scale=1,initial-scale=1">
  <script async src="https://cdn.ampproject.org/v0.js"></script>
  <style amp-custom>
    body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; line-height: 1.6; color: #1a1a1a; padding: 15px; background-color: #fafafa; }}
    .container {{ max-width: 800px; margin: 0 auto; background: #ffffff; padding: 25px; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.05); }}
    h1 {{ color: #0d1117; font-size: 1.8rem; margin-bottom: 10px; border-bottom: 2px solid #2563eb; padding-bottom: 8px; }}
    h2 {{ color: #1e293b; font-size: 1.3rem; margin-top: 20px; }}
    .badge {{ display: inline-block; padding: 4px 10px; background: #e0e7ff; color: #3730a3; border-radius: 4px; font-weight: bold; font-size: 0.85rem; margin-bottom: 15px; }}
    .pros-cons {{ display: flex; flex-direction: column; gap: 15px; margin: 20px 0; }}
    .pros, .cons {{ padding: 15px; border-radius: 6px; }}
    .pros {{ background-color: #f0fdf4; border-left: 4px solid #16a34a; }}
    .cons {{ background-color: #fef2f2; border-left: 4px solid #dc2626; }}
    ul {{ margin: 5px 0 0 20px; padding: 0; }}
    .disclaimer-box {{ background-color: #f8fafc; border: 1px solid #cbd5e1; padding: 15px; border-radius: 6px; font-size: 0.85rem; color: #475569; margin-top: 30px; line-height: 1.5; }}
  </style>
</head>
<body>
  <div class="container">
    <div class="badge">{ide['pricing_type']} • Vendor: {ide['vendor']}</div>
    <h1>{ide['name']} Guide: Features, Pricing & Developer Verdict</h1>

    <amp-img src="{ide['image_url']}" width="800" height="450" layout="responsive" alt="{ide['name']} Code Editor"></amp-img>

    <h2>Overview</h2>
    <p>{ide['overview']}</p>

    <h2>Pricing Model & License</h2>
    <p><strong>License Type:</strong> {ide['pricing_type']}</p>
    <p>{ide['pricing_details']}</p>

    <h2>Pros & Cons Breakdown</h2>
    <div class="pros-cons">
      <div class="pros">
        <strong>The Good (Pros):</strong>
        <ul>
          {pros_html}
        </ul>
      </div>
      <div class="cons">
        <strong>The Bad (Cons):</strong>
        <ul>
          {cons_html}
        </ul>
      </div>
    </div>

    <h2>Developer Verdict & Recommendation</h2>
    <p><strong>Best For:</strong> {ide['best_for']}</p>

    <div class="disclaimer-box">
      Disclaimer: IDE Guide is an independent technical publication. This content is not sponsored, endorsed, or affiliated with any software vendor or editor developer mentioned above. All reviews and assessments are based strictly on objective developer evaluation.
    </div>
  </div>
</body>
</html>"""
    return html


def generate_google_flow_video_spec(ide: Dict[str, Any]) -> str:
    """Generates structured visual prompts and script specs for Google Flow / YouTube shorts and long-form."""
    spec = f"""# Google Flow Video Generation Spec: {ide['name']}

## 1. Metadata & Target Channels
- **Channel**: [@IDEguide](https://www.youtube.com/@IDEguide)
- **Video Title**: {ide['name']} Review: Is It Worth It in 2026? (Pros, Cons & Pricing)
- **Target Format**: YouTube Shorts (9:16 vertical) & YouTube Long-form (16:9 horizontal)
- **Pricing Category**: {ide['pricing_type']}

## 2. Google Flow Visual & Aesthetic Prompts
- **Overall Aesthetic**: Sleek dark mode tech aesthetic, 4k ultra-high definition, cinematic lighting, neon blue/purple contrast accents, developer workspace.
- **Scene 1 (Hook - 0:00 to 0:05)**:
  - *Prompt*: Close-up overhead shot of a modern clean desk with a mechanical keyboard, illuminated code editor interface on an ultrawide monitor displaying `{ide['name']}` logo with glowing glowing neon ambient backlight. Dynamic camera zoom inwards.
- **Scene 2 (Overview & Features - 0:05 to 0:25)**:
  - *Prompt*: Over-the-shoulder view of software engineer coding in `{ide['name']}`, smooth sliding camera movement showcasing code autocompletion and rapid UI response.
- **Scene 3 (Pros & Cons - 0:25 to 0:45)**:
  - *Prompt*: Split screen comparison UI displaying high tech green checkmarks for strengths ({", ".join(ide['pros'][:2])}) and red warning indicators for drawbacks ({ide['cons'][0]}).
- **Scene 4 (Pricing & Verdict - 0:45 to 0:60)**:
  - *Prompt*: Clean animated card showing pricing tier: **{ide['pricing_type']}** ({ide['pricing_details']}). Transition to clean logo badge and subscription button call to action.

## 3. Voiceover & Script Specification

**[0:00 - 0:05] HOOK:**
"Looking for the ultimate coding editor? Here is everything you need to know about {ide['name']} in 60 seconds!"

**[0:05 - 0:20] OVERVIEW & PRICING:**
"{ide['overview']} Pricing status: It operates as {ide['pricing_type']}. {ide['pricing_details']}"

**[0:20 - 0:40] PROS & CONS:**
"On the positive side: {ide['pros'][0]}, and {ide['pros'][1]}. But keep in mind: {ide['cons'][0]}."

**[0:40 - 0:55] VERDICT:**
"Our verdict: {ide['name']} is best for {ide['best_for']}."

**[0:55 - 1:00] NON-SPONSORSHIP DISCLAIMER:**
"IDE Guide is an independent technical publication. This content is not sponsored, endorsed, or affiliated with any software vendor or editor developer mentioned above. All reviews and assessments are based strictly on objective developer evaluation."
"""
    return spec


def load_history(history_file: str) -> Dict[str, Any]:
    if os.path.exists(history_file):
        try:
            with open(history_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            pass
    return {"covered": [], "history": []}


def save_history(history_file: str, data: Dict[str, Any]) -> None:
    os.makedirs(os.path.dirname(history_file), exist_ok=True)
    with open(history_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)


def run_daily_generation(base_dir: str = ".") -> List[str]:
    now_utc = datetime.now(timezone.utc)
    today_str = now_utc.strftime("%Y-%m-%d")
    output_dir = os.path.join(base_dir, "content", today_str)
    history_file = os.path.join(base_dir, "content", "history.json")
    os.makedirs(output_dir, exist_ok=True)

    history = load_history(history_file)
    covered_set = set(history.get("covered", []))

    # Select 3 IDEs from database not recently covered
    available_ides = [ide for ide in IDE_DATABASE if ide["id"] not in covered_set]
    if len(available_ides) < 3:
        # Reset covered if pool exhausted
        covered_set = set()
        available_ides = IDE_DATABASE

    selected_ides = available_ides[:3]

    generated_files = []
    run_record = {
        "date": today_str,
        "timestamp": now_utc.isoformat(),
        "selected_ides": [ide["id"] for ide in selected_ides]
    }

    for idx, ide in enumerate(selected_ides, 1):
        # Generate Blog Post AMP HTML
        amp_html = generate_amp_blog_post(ide)
        is_valid, errors = validate_amp_html(amp_html)
        if not is_valid:
            print(f"Warning: Generated AMP HTML for {ide['id']} had validation issues: {errors}")

        blog_filename = f"blog_post_{idx}_{ide['id']}.html"
        blog_path = os.path.join(output_dir, blog_filename)
        with open(blog_path, 'w', encoding='utf-8') as f:
            f.write(amp_html)
        generated_files.append(blog_path)

        # Generate Video Spec for Google Flow
        video_spec = generate_google_flow_video_spec(ide)
        video_filename = f"video_spec_{idx}_{ide['id']}.md"
        video_path = os.path.join(output_dir, video_filename)
        with open(video_path, 'w', encoding='utf-8') as f:
            f.write(video_spec)
        generated_files.append(video_path)

        # Update covered
        if ide["id"] not in history.get("covered", []):
            history.setdefault("covered", []).append(ide["id"])

    history.setdefault("history", []).append(run_record)
    save_history(history_file, history)

    print(f"Successfully generated {len(generated_files)} files in {output_dir}")
    return generated_files


if __name__ == "__main__":
    generated = run_daily_generation()
    for g in generated:
        print(f" - {g}")
