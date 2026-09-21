"""Daily Content Generator Engine for IDE Guide.

Fetches/selects 3 distinct IDEs or code editors daily, tracks history in content/history.json
to prevent repetitions, and generates AMP HTML blog posts and Google Flow video specifications in content/YYYY-MM-DD/.
"""

import os
import sys
import json
import datetime
import urllib.request
import urllib.parse
from typing import List, Dict, Any

# Ensure parent directory is in sys.path when running scripts directly
REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from scripts.lib.amp_generator import generate_amp_html
from scripts.lib.google_flow_generator import generate_google_flow_spec, format_google_flow_spec_md

HISTORY_FILE = os.path.join("content", "history.json")

# Fallback catalog of prominent and emerging IDEs/editors
DEFAULT_IDE_CATALOG = [
    {
        "name": "Visual Studio Code",
        "tagline": "Code editing. Redefined.",
        "description": "Visual Studio Code is a lightweight but powerful source code editor which runs on your desktop and is available for Windows, macOS and Linux.",
        "category": "Source Code Editor",
        "pricing_type": "Free",
        "pricing_details": "100% Free and open-source core (MIT license) supported by Microsoft.",
        "features": [
            "Extremely rich extension marketplace with thousands of extensions",
            "Built-in IntelliSense autocomplete and debugging support",
            "Integrated terminal and Git control capabilities",
            "Remote development via SSH, Containers, and WSL"
        ],
        "pros": ["Massive extension ecosystem", "Fast startup speed", "Highly customizable theme and keybindings"],
        "cons": ["Memory footprint grows with many extensions", "Can require manual configuration for complex C++ or Java projects"],
        "best_for": "Web developers, general software engineers, and polyglot programmers."
    },
    {
        "name": "Cursor",
        "tagline": "The AI-first Code Editor",
        "description": "Cursor is an AI-powered code editor built as a fork of VS Code, featuring native deep integration with Claude 3.5 Sonnet and GPT-4o.",
        "category": "AI Code Editor",
        "pricing_type": "Freemium",
        "pricing_details": "Free tier available with limited fast AI requests; Pro tier at $20/month for unlimited fast usage.",
        "features": [
            "Composer mode for multi-file code generation and editing",
            "Repository indexing for deep context-aware answers",
            "Instant inline edit predictions with Cmd+K and Tab completions",
            "Seamless import of all VS Code extensions, themes, and settings"
        ],
        "pros": ["Best-in-class AI agent capabilities", "Familiar VS Code experience", "Multi-file refactoring powered by LLMs"],
        "cons": ["Requires active internet connection for AI features", "Pro subscription needed for heavy usage"],
        "best_for": "Developers wanting maximum productivity gains through cutting-edge AI assistance."
    },
    {
        "name": "Zed",
        "tagline": "The code editor from the creators of Atom and Tree-sitter",
        "description": "Zed is a high-performance, multiplayer code editor written in Rust, engineered to maximize GPU acceleration and multi-core CPU usage.",
        "category": "High-Performance Editor",
        "pricing_type": "Free",
        "pricing_details": "Free open-source editor core with optional paid team collaboration features.",
        "features": [
            "Ultra-fast rendering using GPU hardware acceleration",
            "Native real-time multiplayer pair programming",
            "Built-in AI model support (Anthropic, OpenAI, Ollama)",
            "Minimalist UI with instant file search and indexing"
        ],
        "pros": ["Incredible performance and speed", "Low RAM footprint", "Built-in real-time collaboration"],
        "cons": ["Ecosystem is still growing compared to VS Code", "Extensions marketplace is newer"],
        "best_for": "Systems programmers, Rust/Go/Python developers who value lightning-fast editor performance."
    },
    {
        "name": "Neovim",
        "tagline": "Vim-fork focused on extensibility and usability",
        "description": "Neovim is a hyperextensible Vim-based text editor built for extreme terminal productivity, custom Lua scripting, and modal editing mastery.",
        "category": "Terminal Modal Editor",
        "pricing_type": "Free",
        "pricing_details": "100% Free and open-source under Apache and Vim licenses.",
        "features": [
            "Built-in LSP (Language Server Protocol) client for IDE-level completions",
            "First-class Lua scripting configuration",
            "Tree-sitter integration for fast semantic syntax highlighting",
            "Asynchronous plugin architecture"
        ],
        "pros": ["Zero mouse dependency", "Insanely lightweight and fast", "Unlimited customizability"],
        "cons": ["Steep learning curve for modal editing", "Initial configuration requires time investment"],
        "best_for": "Power users, DevOps engineers, and developers who love modal keyboard-driven editing."
    },
    {
        "name": "JetBrains IntelliJ IDEA",
        "tagline": "The Capable & Ergonomic Java IDE",
        "description": "IntelliJ IDEA is the flagship integrated development environment developed by JetBrains, designed specifically for Java, Kotlin, and JVM ecosystem development.",
        "category": "Full IDE",
        "pricing_type": "Freemium",
        "pricing_details": "Free Community Edition; Paid Ultimate Edition for enterprise frameworks and advanced database tools.",
        "features": [
            "Industry-leading smart code refactoring and static analysis",
            "Deep integration with Spring, Jakarta EE, and database tools",
            "Built-in decompilation and advanced debugging tools",
            "JetBrains AI Assistant integration"
        ],
        "pros": ["Unmatched code intelligence for JVM", "Comprehensive out-of-the-box feature set", "Robust enterprise support"],
        "cons": ["High memory and CPU resource consumption", "Commercial version required for full web framework tools"],
        "best_for": "Java, Kotlin, and enterprise backend developers."
    },
    {
        "name": "Fleet",
        "tagline": "The Next-Generation IDE by JetBrains",
        "description": "JetBrains Fleet is a lightweight editor built from scratch using JetBrains IntelliJ code processing engine, supporting distributed cloud execution and smart mode toggle.",
        "category": "Polyglot Lightweight IDE",
        "pricing_type": "Freemium",
        "pricing_details": "Free public preview; tiered JetBrains subscription model upon full launch.",
        "features": [
            "Smart mode toggle between fast text editor and full JetBrains IDE engine",
            "Distributed architecture for remote machine and cloud development",
            "Collaborative multi-user editing",
            "Polyglot language support out of the box"
        ],
        "pros": ["Sleek modern user interface", "Flexibility between fast editor and full IDE", "Great remote development ergonomics"],
        "cons": ["Still in active preview development", "Plugin ecosystem is still maturing"],
        "best_for": "Developers wanting JetBrains quality in a lightweight VS-Code-like package."
    }
]


def load_history() -> List[str]:
    """Loads list of processed IDE names from content/history.json."""
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data.get("processed_ides", [])
        except Exception:
            return []
    return []


def save_history(processed_ides: List[str]) -> None:
    """Saves updated list of processed IDE names to content/history.json."""
    os.makedirs(os.path.dirname(HISTORY_FILE), exist_ok=True)
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump({"processed_ides": processed_ides}, f, indent=2)


def fetch_trending_github_ides() -> List[Dict[str, Any]]:
    """Attempts to discover IDE/code editor projects via GitHub Search API with fallback."""
    discovered = []
    url = "https://api.github.com/search/repositories?q=topic:editor+topic:ide&sort=stars&order=desc&per_page=10"
    headers = {"User-Agent": "IDE-Guide-Generator"}
    req = urllib.request.Request(url, headers=headers)

    try:
        with urllib.request.urlopen(req, timeout=5) as response:
            if response.status == 200:
                data = json.loads(response.read().decode("utf-8"))
                for item in data.get("items", []):
                    name = item.get("name", "").capitalize()
                    desc = item.get("description") or f"An open-source code editor project available on GitHub ({item.get('html_url')})."
                    discovered.append({
                        "name": name,
                        "tagline": f"Open-source code editor on GitHub ({item.get('stargazers_count', 0):,} stars)",
                        "description": desc,
                        "category": "Open-Source Code Editor",
                        "pricing_type": "Free",
                        "pricing_details": f"Open-source software published on GitHub ({item.get('license', {}).get('name', 'Open Source') if item.get('license') else 'Open Source'}).",
                        "features": [
                            "Open-source code base accessible for community contributions",
                            "Cross-platform compatibility",
                            "Active developer community with GitHub star recognition",
                            "Customizable build and extension capabilities"
                        ],
                        "pros": ["Transparent open-source development", "Community driven features", "Free to use and adapt"],
                        "cons": ["Documentation varies by contributor activity", "May require self-building for bleeding edge features"],
                        "best_for": "Developers seeking open-source code editing tools."
                    })
    except Exception as e:
        print(f"Notice: GitHub API fetch skipped or limited ({e}). Using catalog.")

    return discovered


def select_daily_ides(count: int = 3) -> List[Dict[str, Any]]:
    """Selects `count` unprocessed IDEs from online discovery and catalog."""
    history = load_history()
    selected = []

    # 1. Try discovery first
    github_ides = fetch_trending_github_ides()
    for ide in github_ides:
        if ide["name"].lower() not in [h.lower() for h in history] and ide["name"].lower() not in [s["name"].lower() for s in selected]:
            selected.append(ide)
            if len(selected) >= count:
                break

    # 2. Fill remaining from catalog
    if len(selected) < count:
        for ide in DEFAULT_IDE_CATALOG:
            if ide["name"].lower() not in [h.lower() for h in history] and ide["name"].lower() not in [s["name"].lower() for s in selected]:
                selected.append(ide)
                if len(selected) >= count:
                    break

    # 3. If catalog exhausted, reuse least recently processed catalog items to satisfy daily requirement
    if len(selected) < count:
        for ide in DEFAULT_IDE_CATALOG:
            if ide["name"].lower() not in [s["name"].lower() for s in selected]:
                selected.append(ide)
                if len(selected) >= count:
                    break

    return selected[:count]


def generate_daily_content_package(target_date: str = None) -> List[str]:
    """Generates 3 daily blog post AMP HTML files & 3 Google Flow video spec files."""
    if not target_date:
        target_date = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d")

    out_dir = os.path.join("content", target_date)
    os.makedirs(out_dir, exist_ok=True)

    ides = select_daily_ides(count=3)
    history = load_history()
    generated_files = []

    for i, ide in enumerate(ides, 1):
        slug = ide["name"].lower().replace(" ", "-").replace("/", "-")

        # 1. Generate AMP HTML for Blogger
        amp_html = generate_amp_html(ide)
        amp_filename = f"{i:02d}_{slug}_post.amp.html"
        amp_path = os.path.join(out_dir, amp_filename)
        with open(amp_path, "w", encoding="utf-8") as f:
            f.write(amp_html)
        generated_files.append(amp_path)

        # 2. Generate Google Flow Spec (JSON & MD) for YouTube
        video_spec = generate_google_flow_spec(ide)
        spec_json_path = os.path.join(out_dir, f"{i:02d}_{slug}_video_spec.json")
        with open(spec_json_path, "w", encoding="utf-8") as f:
            json.dump(video_spec, f, indent=2)
        generated_files.append(spec_json_path)

        spec_md = format_google_flow_spec_md(video_spec)
        spec_md_path = os.path.join(out_dir, f"{i:02d}_{slug}_video_spec.md")
        with open(spec_md_path, "w", encoding="utf-8") as f:
            f.write(spec_md)
        generated_files.append(spec_md_path)

        # Track history
        if ide["name"] not in history:
            history.append(ide["name"])

    save_history(history)
    print(f"Successfully generated {len(generated_files)} files for {target_date} in {out_dir}:")
    for filepath in generated_files:
        print(f" - {filepath}")

    return generated_files


if __name__ == "__main__":
    generate_daily_content_package()
