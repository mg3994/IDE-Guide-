#!/usr/bin/env python3
"""
scripts/generate_daily_content.py

Generates daily content packages for IDE Guide:
- 3 AMP-compliant HTML blog posts for Blogger (ideguide.blogspot.com)
- 3 Google Flow AI video & shorts generation specs for YouTube (@IDEguide)

Features:
- Dynamic discovery of IDEs/editors via GitHub Search API with fallback catalog.
- History tracking in content/history.json to avoid repeating covered tools.
- Output organized in content/YYYY-MM-DD/.
- Exact mandatory non-sponsorship disclaimer embedded in all posts & scripts.
"""

import json
import os
import re
import sys
import datetime
import urllib.request
import urllib.parse

DISCLAIMER = (
    "Disclaimer: IDE Guide is an independent technical publication. "
    "This content is not sponsored, endorsed, or affiliated with any software vendor or editor developer mentioned above. "
    "All reviews and assessments are based strictly on objective developer evaluation."
)

FALLBACK_IDE_CATALOG = [
    {
        "name": "Visual Studio Code",
        "slug": "vscode",
        "type": "Code Editor",
        "pricing": "Free & Open Source (Core)",
        "license": "MIT / Proprietary Binary",
        "pros": ["Extensive extension ecosystem", "Blazing fast performance", "Integrated git & terminal", "Active community support"],
        "cons": ["High memory usage with many extensions", "Telemetry enabled by default"],
        "best_for": "Web developers, polyglot programmers, and general software development",
        "features": ["Built-in IntelliSense", "Debugging tools", "Git integration", "Extensions Marketplace"]
    },
    {
        "name": "Cursor",
        "slug": "cursor",
        "type": "AI Code Editor",
        "pricing": "Freemium ($20/mo Pro)",
        "license": "Proprietary",
        "pros": ["Native AI chat & inline edits", "Deep codebase indexing", "VS Code extension compatibility", "Fast multi-file edits"],
        "cons": ["Subscription required for unlimited AI models", "Closed source core"],
        "best_for": "Developers seeking deep AI-assisted coding and codebase navigation",
        "features": ["Cmd+K Code Generation", "Copilot++ Autocomplete", "Codebase RAG Context", "Terminal AI Commands"]
    },
    {
        "name": "Zed Editor",
        "slug": "zed",
        "type": "Code Editor",
        "pricing": "Free & Open Source",
        "license": "GPL / Apache 2.0",
        "pros": ["Extremely fast (Rust-native, GPU accelerated)", "Built-in real-time collaboration", "Minimalist interface", "Low memory footprint"],
        "cons": ["Ecosystem extensions still growing", "Fewer platform-specific plugins compared to VS Code"],
        "best_for": "Performance purists, Systems programmers, and real-time pair programming",
        "features": ["GPU-accelerated rendering", "Real-time multiplayer coding", "Integrated AI assistance", "Language Server Protocol (LSP) support"]
    },
    {
        "name": "Neovim",
        "slug": "neovim",
        "type": "Modal Terminal Text Editor",
        "pricing": "100% Free & Open Source",
        "license": "Apache 2.0 / Vim License",
        "pros": ["Unmatched keyboard efficiency", "Ultralight resource usage", "Infinite Lua customization", "Blazing execution speed"],
        "cons": ["Steep learning curve", "Requires manual configuration for full IDE features"],
        "best_for": "Terminal enthusiasts, DevOps engineers, and keyboard-centric power users",
        "features": ["Built-in LSP support", "Treesitter syntax parsing", "Lua API extensibility", "Asynchronous job control"]
    },
    {
        "name": "PyCharm",
        "slug": "pycharm",
        "type": "Full-Featured Python IDE",
        "pricing": "Freemium (Community Free / Professional Paid)",
        "license": "Apache 2.0 (Community) / Proprietary (Pro)",
        "pros": ["Deep Python refactoring & static analysis", "First-class Django/Flask support", "Powerful debugger & profiler", "Database tools"],
        "cons": ["Heavy RAM and CPU consumption", "Slower startup time"],
        "best_for": "Python developers, Data Scientists, and Django backend engineers",
        "features": ["Smart Python Code Completion", "Integrated Jupyter Notebooks", "Web development tools", "Database & SQL client"]
    },
    {
        "name": "IntelliJ IDEA",
        "slug": "intellij-idea",
        "type": "JVM & Enterprise IDE",
        "pricing": "Freemium (Community Free / Ultimate Paid)",
        "license": "Apache 2.0 (Community) / Proprietary (Ultimate)",
        "pros": ["Industry-standard Java/Kotlin tools", "Incredible code analysis & refactoring", "Comprehensive framework support", "Rich plugin ecosystem"],
        "cons": ["High memory requirements", "Steep price for Ultimate edition"],
        "best_for": "Java, Kotlin, Scala, and Enterprise backend developers",
        "features": ["Smart static analysis", "Decompiler built-in", "Version control integration", "Spring & Jakarta EE support"]
    },
    {
        "name": "Sublime Text 4",
        "slug": "sublime-text",
        "type": "Lightweight Code Editor",
        "pricing": "Paid ($99 evaluated for free)",
        "license": "Proprietary",
        "pros": ["Instant launch speed", "Minimalist and clean UI", "GPU acceleration", "Multiple selections and powerful search"],
        "cons": ["Paid license required for continuous use", "Smaller extension ecosystem than VS Code"],
        "best_for": "Developers who value instant startup times and lightweight text manipulation",
        "features": ["Goto Anything", "GPU Rendering", "Tab Multi-select", "Context-aware auto complete"]
    },
    {
        "name": "Fleet",
        "slug": "fleet",
        "type": "Next-Gen Polyglot Editor",
        "pricing": "Freemium / Commercial",
        "license": "Proprietary",
        "pros": ["Distributed architecture", "Smart mode powered by IntelliJ engine", "Lightweight default mode", "Modern UI"],
        "cons": ["Still maturing", "Fewer community extensions"],
        "best_for": "Developers who want a lightweight editor with optional full IDE power",
        "features": ["Smart Mode switch", "Remote & Collaborative development", "Multi-language support", "Built-in AI Assistant"]
    },
    {
        "name": "Lapce",
        "slug": "lapce",
        "type": "Lightning-fast Rust Editor",
        "pricing": "100% Free & Open Source",
        "license": "Apache 2.0",
        "pros": ["Written in Rust with GPU rendering", "Native remote development support", "Modal editing support built-in", "Extensible via WASI"],
        "cons": ["Under active initial development", "Plugin marketplace is small"],
        "best_for": "Rust developers and users looking for a modern native open-source editor",
        "features": ["Native GUI with Druid", "WASM Plugin system", "Terminal integration", "Built-in LSP support"]
    },
    {
        "name": "Windsurf",
        "slug": "windsurf",
        "type": "AI Flow Code Editor",
        "pricing": "Freemium ($15-20/mo Pro)",
        "license": "Proprietary",
        "pros": ["Flow state AI agent integration", "Deep context understanding", "Fast multi-file editing", "VS Code extension compatible"],
        "cons": ["Requires subscription for heavy AI usage", "Proprietary AI backend"],
        "best_for": "Developers looking for AI agent collaboration while coding",
        "features": ["Cascade AI Flow Agent", "Supercomplete suggestions", "Deep repo indexing", "Multi-file diff previews"]
    }
]


def load_history(history_file="content/history.json"):
    if os.path.exists(history_file):
        try:
            with open(history_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {"covered_slugs": [], "history": []}
    return {"covered_slugs": [], "history": []}


def save_history(history_data, history_file="content/history.json"):
    os.makedirs(os.path.dirname(history_file), exist_ok=True)
    with open(history_file, "w", encoding="utf-8") as f:
        json.dump(history_data, f, indent=2)


def fetch_github_ide_candidates():
    """Dynamically search GitHub for open-source IDEs/editors."""
    url = "https://api.github.com/search/repositories?q=topic:ide+topic:editor+stars:>1000&sort=stars&order=desc"
    req = urllib.request.Request(url, headers={"User-Agent": "IDE-Guide-Bot/1.0"})
    candidates = []
    try:
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            for item in data.get("items", []):
                slug = item["name"].lower().replace("_", "-")
                candidates.append({
                    "name": item["name"],
                    "slug": slug,
                    "type": f"Code Editor / IDE ({item.get('language', 'Polyglot')})",
                    "pricing": "100% Free & Open Source",
                    "license": item.get("license", {}).get("spdx_id", "Open Source") if item.get("license") else "Open Source",
                    "pros": [
                        item.get("description", "Open source editor with vibrant developer community.") or "Community backed editor.",
                        f"Starred by {item.get('stargazers_count', 0)} developers on GitHub",
                        "Fully open-source codebase for customization",
                        "Active open-source maintenance"
                    ],
                    "cons": [
                        "May require manual configuration or plugin setup",
                        "Documentation depends on open-source contributors"
                    ],
                    "best_for": f"Developers interested in {item.get('language', 'modern programming')} and open-source tooling",
                    "features": ["Open-source architecture", "Extensible core", "Community plugins", "Cross-platform support"]
                })
    except Exception as e:
        print(f"GitHub API fetch skipped or failed: {e}. Falling back to curated catalog.")
    return candidates


def select_daily_ides(count=3, history_file="content/history.json"):
    history_data = load_history(history_file)
    covered_slugs = set(history_data.get("covered_slugs", []))

    gh_candidates = fetch_github_ide_candidates()
    all_candidates = gh_candidates + FALLBACK_IDE_CATALOG

    selected = []
    for ide in all_candidates:
        if ide["slug"] not in covered_slugs:
            # Ensure slug is unique in current selection
            if not any(s["slug"] == ide["slug"] for s in selected):
                selected.append(ide)
                if len(selected) == count:
                    break

    # If not enough new candidates, reset or pick from catalog
    if len(selected) < count:
        for ide in FALLBACK_IDE_CATALOG:
            if not any(s["slug"] == ide["slug"] for s in selected):
                selected.append(ide)
                if len(selected) == count:
                    break

    return selected


def generate_amp_html(ide):
    """Generates valid Blogger-compatible AMP HTML for an IDE review."""
    title = f"{ide['name']} Review (2026): Features, Pros & Cons, Pricing, and Developer Guide"

    pros_li = "".join([f"<li><strong>{p}</strong></li>" for p in ide["pros"]])
    cons_li = "".join([f"<li><strong>{c}</strong></li>" for c in ide["cons"]])
    feat_li = "".join([f"<li>{f}</li>" for f in ide["features"]])

    html = f"""<!doctype html>
<html ⚡ lang="en">
<head>
  <meta charset="utf-8">
  <title>{title}</title>
  <link rel="canonical" href="https://ideguide.blogspot.com/{ide['slug']}-review.html">
  <meta name="viewport" content="width=device-width,minimum-scale=1,initial-scale=1">
  <style amp-boilerplate>body{{-webkit-animation:-amp-start 8s steps(1,end) 0s 1 normal part;animation:-amp-start 8s steps(1,end) 0s 1 normal part}}@-webkit-animation -amp-start{{from{{visibility:hidden}}to{{visibility:visible}}}}@keyframes -amp-start{{from{{visibility:hidden}}to{{visibility:visible}}}}</style><noscript><style amp-boilerplate>body{{-webkit-animation:none;animation:none}}</style></noscript>
  <script async src="https://cdn.ampproject.org/v0.js"></script>
  <style amp-custom>
    body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; line-height: 1.6; color: #1f2937; background-color: #f9fafb; padding: 20px; max-width: 800px; margin: 0 auto; }}
    header {{ border-bottom: 2px solid #e5e7eb; padding-bottom: 15px; margin-bottom: 20px; }}
    h1 {{ color: #111827; font-size: 2rem; margin-bottom: 10px; }}
    .badge {{ display: inline-block; background-color: #2563eb; color: #ffffff; font-size: 0.85rem; font-weight: 600; padding: 4px 10px; border-radius: 9999px; margin-right: 8px; }}
    .disclaimer {{ background-color: #fef3c7; border-left: 4px solid #f59e0b; padding: 12px 16px; margin: 20px 0; font-size: 0.9rem; color: #92400e; border-radius: 4px; }}
    .grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin: 20px 0; }}
    .box {{ background: #ffffff; padding: 18px; border-radius: 8px; border: 1px solid #e5e7eb; box-shadow: 0 1px 3px rgba(0,0,0,0.05); }}
    .pros {{ border-top: 4px solid #10b981; }}
    .cons {{ border-top: 4px solid #ef4444; }}
    h2 {{ color: #1f2937; font-size: 1.3rem; margin-top: 0; }}
    ul {{ padding-left: 20px; margin-bottom: 0; }}
    li {{ margin-bottom: 8px; }}
    .verdict {{ background-color: #eff6ff; border: 1px solid #bfdbfe; padding: 16px; border-radius: 8px; margin-top: 20px; }}
    footer {{ text-align: center; margin-top: 40px; font-size: 0.85rem; color: #6b7280; }}
  </style>
</head>
<body>
  <header>
    <span class="badge">{ide['type']}</span>
    <span class="badge" style="background-color: #059669;">{ide['pricing']}</span>
    <h1>{title}</h1>
    <p>Published by <strong>IDE Guide</strong> | Official Review & Assessment</p>
  </header>

  <div class="disclaimer">
    <strong>Notice:</strong> {DISCLAIMER}
  </div>

  <section>
    <h2>Editor Overview</h2>
    <p><strong>{ide['name']}</strong> is a {ide['type'].lower()} tailored for developer efficiency. In this assessment, we analyze its performance, pricing structure ({ide['pricing']}), and key feature set to help you decide if it fits your programming workflow.</p>
  </section>

  <section>
    <h2>Key Specifications</h2>
    <ul>
      <li><strong>Tool Name:</strong> {ide['name']}</li>
      <li><strong>Category:</strong> {ide['type']}</li>
      <li><strong>Pricing Model:</strong> {ide['pricing']}</li>
      <li><strong>License:</strong> {ide['license']}</li>
      <li><strong>Recommended For:</strong> {ide['best_for']}</li>
    </ul>
  </section>

  <section>
    <h2>Standout Features</h2>
    <ul>
      {feat_li}
    </ul>
  </section>

  <div class="grid">
    <div class="box pros">
      <h2>The Good (Pros)</h2>
      <ul>
        {pros_li}
      </ul>
    </div>
    <div class="box cons">
      <h2>The Bad (Cons)</h2>
      <ul>
        {cons_li}
      </ul>
    </div>
  </div>

  <div class="verdict">
    <h2>Final Verdict & Recommendation</h2>
    <p><strong>Is {ide['name']} worth using?</strong></p>
    <p>{ide['name']} is best suited for <strong>{ide['best_for']}</strong>. If you value {ide['pros'][0].lower()}, this tool is a strong contender for your workspace.</p>
  </div>

  <footer>
    <p>Visit our blog at <a href="https://ideguide.blogspot.com/">ideguide.blogspot.com</a> or watch full video breakdowns at <a href="https://www.youtube.com/@IDEguide">youtube.com/@IDEguide</a>.</p>
    <p>{DISCLAIMER}</p>
  </footer>
</body>
</html>
"""
    return html


def generate_google_flow_spec(ide):
    """Generates Google Flow AI video & shorts prompt specification."""
    spec = {
        "channel": "@IDEguide",
        "url": "https://www.youtube.com/@IDEguide",
        "ide_name": ide["name"],
        "ide_slug": ide["slug"],
        "pricing_model": ide["pricing"],
        "disclaimer": DISCLAIMER,
        "video_formats": {
            "youtube_shorts": {
                "aspect_ratio": "9:16",
                "target_duration_seconds": 50,
                "flow_prompt": (
                    f"Create a high-energy 9:16 vertical tech video reviewing {ide['name']} ({ide['type']}). "
                    "Use sleek dark mode code editor interface animations, glowing cyan and purple syntax highlighting, "
                    "fast-paced camera pans over mechanical keyboards, and dynamic text overlays highlighting top features and pricing."
                ),
                "scenes": [
                  {
                    "scene_number": 1,
                    "title": "Hook",
                    "duration": "0-5s",
                    "visual_prompt": f"Close-up cinematic shot of {ide['name']} editor dark interface with glowing neon text.",
                    "voiceover": f"Should you use {ide['name']} for coding in 2026? Let's break it down in 50 seconds!",
                    "text_overlay": f"{ide['name']} - Worth It?"
                  },
                  {
                    "scene_number": 2,
                    "title": "The Good (Pros)",
                    "duration": "5-20s",
                    "visual_prompt": "Fast panning shot over editor features, code autocompletion, and extension marketplace.",
                    "voiceover": f"First, the pros. {ide['pros'][0]}. Plus, {ide['pros'][1] if len(ide['pros']) > 1 else 'great workflow integration'}.",
                    "text_overlay": f"PROS: {ide['pros'][0]}"
                  },
                  {
                    "scene_number": 3,
                    "title": "The Bad (Cons)",
                    "duration": "20-35s",
                    "visual_prompt": "Camera tilt to performance monitor or warning badge overlay.",
                    "voiceover": f"On the downside: {ide['cons'][0]}.",
                    "text_overlay": f"CONS: {ide['cons'][0]}"
                  },
                  {
                    "scene_number": 4,
                    "title": "Pricing & Verdict",
                    "duration": "35-50s",
                    "visual_prompt": "Floating price card badge showing pricing status, transitioning to channel logo and non-sponsorship disclosure.",
                    "voiceover": f"Pricing is {ide['pricing']}. Ideal for {ide['best_for']}. Remember, IDE Guide is an independent publication not sponsored by any vendor. Subscribe to @IDEguide for daily developer reviews!",
                    "text_overlay": f"{ide['pricing']} | Subscribe @IDEguide"
                  }
                ]
            },
            "youtube_horizontal_video": {
                "aspect_ratio": "16:9",
                "target_duration_seconds": 180,
                "flow_prompt": (
                    f"Create a 16:9 4K resolution tech review video for {ide['name']} ({ide['type']}). "
                    "Features dark studio lighting, cyberpunk aesthetic, screen captures of code editing, "
                    "side-by-side pros and cons graphics, and clear lower third titles."
                ),
                "sections": [
                    {"section": "Intro & High-level summary", "duration": "0-30s"},
                    {"section": "Interface & Core Features", "duration": "30-90s"},
                    {"section": "Pros vs Cons Breakdown", "duration": "90-140s"},
                    {"section": "Pricing & Recommendation", "duration": "140-165s"},
                    {"section": "Disclaimer & Channel Outro", "duration": "165-180s"}
                ]
            }
        }
    }
    return spec


def main():
    date_str = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d")
    output_dir = os.path.join("content", date_str)
    os.makedirs(output_dir, exist_ok=True)

    history_file = "content/history.json"
    history_data = load_history(history_file)

    selected_ides = select_daily_ides(count=3, history_file=history_file)
    print(f"Selected {len(selected_ides)} IDEs for daily content ({date_str}):")

    generated_items = []
    for idx, ide in enumerate(selected_ides, 1):
        slug = ide["slug"]
        print(f" [{idx}] Generating content for: {ide['name']} ({slug})")

        # 1. Generate AMP HTML blog post
        amp_html = generate_amp_html(ide)
        blog_filename = f"{slug}_review_amp.html"
        blog_path = os.path.join(output_dir, blog_filename)
        with open(blog_path, "w", encoding="utf-8") as f:
            f.write(amp_html)

        # 2. Generate Google Flow spec
        flow_spec = generate_google_flow_spec(ide)
        spec_filename = f"{slug}_google_flow_spec.json"
        spec_path = os.path.join(output_dir, spec_filename)
        with open(spec_path, "w", encoding="utf-8") as f:
            json.dump(flow_spec, f, indent=2)

        generated_items.append({
            "name": ide["name"],
            "slug": slug,
            "amp_blog_path": blog_path,
            "google_flow_spec_path": spec_path,
            "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat()
        })

        if slug not in history_data.get("covered_slugs", []):
            history_data.setdefault("covered_slugs", []).append(slug)
        history_data.setdefault("history", []).append({
            "date": date_str,
            "ide_name": ide["name"],
            "slug": slug
        })

    save_history(history_data, history_file)
    print(f"Successfully generated 3 AMP posts & 3 Google Flow specs in {output_dir}")
    print(f"Updated history in {history_file}")


if __name__ == "__main__":
    main()
