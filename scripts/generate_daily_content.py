#!/usr/bin/env python3
"""
Daily Content Generator for IDE Guide (@IDEguide & ideguide.blogspot.com).
Generates 3 AMP HTML blog posts and 3 Google Flow video specifications every day.
Tracks covered IDEs/editors in content/history.json to ensure fresh daily content.
"""

import datetime
import json
import os
import sys
from typing import List, Dict, Any

# Ensure parent path is in sys.path for module imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from scripts.amp_validator import validate_amp_html
from scripts.ide_guide_agent_skill import generate_amp_blog_post, generate_google_flow_video_spec

HISTORY_FILE = "content/history.json"

POOL_OF_IDES = [
    {
        "key": "cursor",
        "name": "Cursor AI",
        "category": "AI-Native Code Editor",
        "license": "Proprietary",
        "pricing": "Freemium ($20/mo Pro)",
        "platforms": "Windows, macOS, Linux",
        "key_features": ["AI Agent Mode", "Multi-file context editing", "Codebase indexing", "VS Code extension ecosystem compatibility"],
        "pros": ["Unmatched AI coding speed", "Seamless migration from VS Code", "Instant multi-file refactoring"],
        "cons": ["Paid subscription required for heavy usage", "Requires internet connectivity"],
        "best_for": "Developers seeking maximum AI coding velocity and automated code generation."
    },
    {
        "key": "zed",
        "name": "Zed Editor",
        "category": "High-Performance Code Editor",
        "license": "Open Source (GPL / Apache 2.0)",
        "pricing": "Free & Open Source",
        "platforms": "macOS, Linux (Windows preview)",
        "key_features": ["Rust GPU acceleration", "Multiplayer real-time pairing", "Ultra-low latency rendering"],
        "pros": ["Blazing instant startup time", "Minimalist visual aesthetic", "Native multi-model AI support"],
        "cons": ["Growing extension ecosystem", "Fewer third-party integrations than VS Code"],
        "best_for": "Systems programmers and web developers prioritizing raw speed and responsive editing."
    },
    {
        "key": "neovim",
        "name": "Neovim",
        "category": "Extensible Modal Text Editor",
        "license": "Open Source (Apache 2.0 / Vim)",
        "pricing": "100% Free & Open Source",
        "platforms": "Linux, macOS, Windows, Terminal",
        "key_features": ["Lua configuration engine", "Built-in LSP client", "Treesitter syntax parsing", "Modal editing workflows"],
        "pros": ["Pure keyboard efficiency", "Infinite customizability", "Zero GUI memory overhead"],
        "cons": ["Steep initial learning curve", "Requires time for custom config setup"],
        "best_for": "Keyboard purists, Linux sysadmins, and power users who demand total control over their IDE."
    },
    {
        "key": "windsurf",
        "name": "Windsurf Editor",
        "category": "Agentic AI Flow Editor",
        "license": "Proprietary",
        "pricing": "Freemium ($15/mo Pro)",
        "platforms": "Windows, macOS, Linux",
        "key_features": ["Cascade Agentic AI flow", "Deep terminal & workspace integration", "Real-time context reasoning"],
        "pros": ["Context-aware intelligent editing", "Fluid AI developer collaboration", "Intuitive user interface"],
        "cons": ["Subscription needed for unlimited AI steps", "Proprietary code base"],
        "best_for": "Full-stack developers and AI-first engineers seeking guided agentic coding workflows."
    },
    {
        "key": "vscode",
        "name": "Visual Studio Code",
        "category": "General Purpose IDE",
        "license": "Open Source (Code-OSS) / Free Binary",
        "pricing": "Free",
        "platforms": "Windows, macOS, Linux, Web",
        "key_features": ["Massive extension marketplace", "Integrated debugger & terminal", "GitHub Copilot deep integration"],
        "pros": ["Unrivaled community ecosystem", "Rich multi-language support out of the box", "Frequent updates"],
        "cons": ["Higher RAM footprint with many extensions", "Electron shell overhead"],
        "best_for": "Developers of all skill levels wanting a reliable, highly extensible code editor."
    },
    {
        "key": "intellij_idea",
        "name": "IntelliJ IDEA",
        "category": "Enterprise Java & Polyglot IDE",
        "license": "Proprietary / Community Edition Open Source",
        "pricing": "Freemium ($16.90/mo Commercial)",
        "platforms": "Windows, macOS, Linux",
        "key_features": ["Deep static code analysis", "Advanced refactoring engine", "Built-in database and spring tools"],
        "pros": ["Unmatched code completion for JVM", "Enterprise-grade tooling", "Deep framework understanding"],
        "cons": ["Resource intensive on memory & CPU", "Paid license for full ultimate suite"],
        "best_for": "Enterprise Java, Kotlin, Scala, and full-stack backend software engineers."
    },
    {
        "key": "pycharm",
        "name": "PyCharm",
        "category": "Dedicated Python IDE",
        "license": "Proprietary / Community Edition Open Source",
        "pricing": "Freemium ($9.90/mo Commercial)",
        "platforms": "Windows, macOS, Linux",
        "key_features": ["Django & FastAPI integration", "Scientific stack Jupyter notebooks", "Automated Python refactoring"],
        "pros": ["Best-in-class Python static inspection", "Integrated virtualenv / conda manager", "Great test runner"],
        "cons": ["Heavy RAM usage", "Community edition lacks web framework tools"],
        "best_for": "Data scientists, machine learning engineers, and Python web developers."
    },
    {
        "key": "sublime_text",
        "name": "Sublime Text 4",
        "category": "Lightweight Text Editor",
        "license": "Proprietary (Evaluation / $99)",
        "pricing": "Paid ($99 perpetual seat)",
        "platforms": "Windows, macOS, Linux",
        "key_features": ["GPU rendering engine", "Supercharged multi-cursor editing", "Package Control ecosystem"],
        "pros": ["Instant open times", "Extremely low RAM footprint", "Smooth handling of huge log files"],
        "cons": ["Paid license required for prolonged use", "Lacks out-of-the-box full IDE features"],
        "best_for": "Developers who value lightning-fast editor performance and clean simplicity."
    },
    {
        "key": "fleet",
        "name": "JetBrains Fleet",
        "category": "Next-Gen Distributed IDE",
        "license": "Proprietary",
        "pricing": "Freemium Preview",
        "platforms": "Windows, macOS, Linux",
        "key_features": ["Lightweight editor / full IDE mode switch", "Distributed collaboration", "Smart JetBrains code engine"],
        "pros": ["Sleek modern UI", "Quick startup compared to heavy JetBrains IDEs", "Remote execution support"],
        "cons": ["Still evolving feature set", "Extension ecosystem in early stages"],
        "best_for": "Developers looking for a lightweight JetBrains experience with distributed capabilities."
    }
]


def load_history() -> List[str]:
    """Loads covered IDE keys from history.json."""
    if not os.path.exists(HISTORY_FILE):
        return []
    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data.get("covered_ides", [])
    except Exception:
        return []


def save_history(covered_ides: List[str]):
    """Saves updated covered IDE keys to history.json."""
    os.makedirs(os.path.dirname(HISTORY_FILE), exist_ok=True)
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump({"covered_ides": covered_ides, "last_updated": datetime.date.today().isoformat()}, f, indent=2)


def select_daily_ides(count: int = 3) -> List[Dict[str, Any]]:
    """Selects 3 unique IDEs that have not been covered recently."""
    history = load_history()
    available = [ide for ide in POOL_OF_IDES if ide["key"] not in history]

    # Reset history if pool exhausted
    if len(available) < count:
        history = []
        available = POOL_OF_IDES

    selected = available[:count]
    return selected, history


def main():
    today_str = datetime.date.today().isoformat()
    output_dir = os.path.join("content", today_str)
    os.makedirs(output_dir, exist_ok=True)

    selected_ides, history = select_daily_ides(count=3)
    generated_files = []

    print(f"🚀 Generating 3 daily content packages for {today_str}...")

    for idx, ide_info in enumerate(selected_ides, start=1):
        key = ide_info["key"]
        slug = key

        # 1. Generate AMP Blog Post
        amp_html = generate_amp_blog_post(ide_info)
        amp_filename = f"post_{idx}_{slug}.amp.html"
        amp_path = os.path.join(output_dir, amp_filename)
        with open(amp_path, "w", encoding="utf-8") as f:
            f.write(amp_html)

        # Validate AMP HTML
        is_valid, errors = validate_amp_html(amp_html)
        if not is_valid:
            print(f"❌ AMP validation failed for {amp_filename}: {errors}")
            sys.exit(1)

        # 2. Generate Google Flow Video Spec
        flow_spec = generate_google_flow_video_spec(ide_info)
        flow_filename = f"video_spec_{idx}_{slug}.json"
        flow_path = os.path.join(output_dir, flow_filename)
        with open(flow_path, "w", encoding="utf-8") as f:
            json.dump(flow_spec, f, indent=2)

        generated_files.extend([amp_path, flow_path])
        if key not in history:
            history.append(key)

        print(f"  [{idx}/3] Prepared {ide_info['name']} -> {amp_filename} & {flow_filename}")

    save_history(history)
    print(f"✅ Successfully generated daily package in {output_dir}/")


if __name__ == "__main__":
    main()
