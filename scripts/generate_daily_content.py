#!/usr/bin/env python3
"""
IDE Guide Daily Content Generator
Generates daily content packages (3 AMP HTML blog posts and 3 Google Flow video specifications)
under content/YYYY-MM-DD/ and updates content/history.json.
"""

import json
import os
import re
import sys
from datetime import datetime, timezone
import urllib.request
import urllib.error

# Import generation helpers from ide_guide_agent_skill
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
from ide_guide_agent_skill import (
    DISCLAIMER_TEXT,
    get_ide_info,
    generate_amp_html,
    generate_google_flow_spec
)

HISTORY_FILE = os.path.join(os.path.dirname(__file__), "..", "content", "history.json")

IDE_CANDIDATE_POOL = [
    {"name": "Cursor", "key": "cursor"},
    {"name": "Zed Editor", "key": "zed"},
    {"name": "JetBrains Fleet", "key": "fleet"},
    {"name": "Lapce", "key": "lapce"},
    {"name": "Neovim", "key": "neovim"},
    {"name": "Helix Editor", "key": "helix"},
    {"name": "VSCodium", "key": "vscodium"},
    {"name": "Sublime Text", "key": "sublime"},
    {"name": "Pulsar Edit", "key": "pulsar"},
    {"name": "Eclipse Theia", "key": "theia"},
    {"name": "Nova Editor", "key": "nova"},
    {"name": "Micro Editor", "key": "micro"},
    {"name": "Acode", "key": "acode"},
    {"name": "Kakoune", "key": "kakoune"},
    {"name": "Geany", "key": "geany"}
]

EXPANDED_DETAILS = {
    "helix": {
        "name": "Helix Editor",
        "description": "A post-modern modal text editor written in Rust, built with terminal UI, Tree-sitter integration, and built-in Language Server Protocol (LSP) support without plugins.",
        "pricing": "100% Free and Open Source (MPL-2.0 license).",
        "pros": [
            "Built-in Language Server Protocol (LSP) integration out of the box.",
            "Tree-sitter syntax highlighting and structural navigation.",
            "Selection-first modal editing model for intuitive multi-cursor manipulation."
        ],
        "cons": [
            "No plugin architecture by design; features must be built into core.",
            "Terminal-only user interface may not suit GUI-focused developers."
        ],
        "recommendation": "Best for developers who love modal editing with zero-config LSP and instant terminal startup."
    },
    "vscodium": {
        "name": "VSCodium",
        "description": "A community-driven, free-licensed binary distribution of Microsoft's editor VS Code, built without telemetry or proprietary tracking code.",
        "pricing": "100% Free and Open Source (MIT license).",
        "pros": [
            "100% telemetry-free and privacy-focused default build.",
            "Full compatibility with VS Code UI, keybindings, and extensions via Open VSX Registry.",
            "Clean open-source licensing."
        ],
        "cons": [
            "Some proprietary Microsoft extensions (e.g., C# Debugger) restrict usage outside official VS Code.",
            "Manual configuration required for proprietary marketplace backends."
        ],
        "recommendation": "Best for privacy-conscious developers wanting the VS Code interface without telemetry."
    },
    "sublime": {
        "name": "Sublime Text 4",
        "description": "A sophisticated cross-platform text editor for code, markup, and prose with custom GPU rendering engine and fluid responsiveness.",
        "pricing": "Commercial ($99 individual license with unlimited evaluation period).",
        "pros": [
            "GPU-accelerated interface rendering ultra-responsive 120Hz editing.",
            "Extremely low CPU and memory footprint.",
            "Rich Python plugin ecosystem via Package Control."
        ],
        "cons": [
            "Commercial license required for continuous professional use.",
            "Built-in AI assistance features require custom third-party plugins."
        ],
        "recommendation": "Best for developers needing an ultra-fast, lightweight text editor with rich extension capabilities."
    },
    "pulsar": {
        "name": "Pulsar Edit",
        "description": "A community-led hyper-hackable text editor built as the direct open-source successor to Atom Editor.",
        "pricing": "100% Free and Open Source (MIT license).",
        "pros": [
            "Hyper-hackable architecture with complete web tech customization.",
            "Active community preserving and updating the Atom extension ecosystem.",
            "Cross-platform support across macOS, Linux, and Windows."
        ],
        "cons": [
            "Electron architecture results in higher memory footprint than native Rust/C++ editors.",
            "Startup time can be slower with numerous installed packages."
        ],
        "recommendation": "Best for developers who miss Atom and value maximum CSS/JS editor hackability."
    },
    "theia": {
        "name": "Eclipse Theia",
        "description": "An open-source cloud and desktop IDE framework designed to build customizable IDEs using Language Server Protocol and VS Code extension protocol.",
        "pricing": "100% Free and Open Source (EPL-2.0 license).",
        "pros": [
            "Flexible platform support for both cloud browser-based and native desktop IDEs.",
            "Full support for VS Code extensions and Language Server Protocol.",
            "Vendor-neutral governance under the Eclipse Foundation."
        ],
        "cons": [
            "Primarily intended as a framework for building custom IDEs rather than a single end-user app.",
            "Initial setup requires framework configuration."
        ],
        "recommendation": "Best for enterprise teams and developers building customized domain-specific IDEs."
    },
    "nova": {
        "name": "Panic Nova",
        "description": "A sleek, native macOS code editor built from the ground up for speed, featuring built-in web preview, local/remote file management, and extension API.",
        "pricing": "Commercial ($99 single purchase with 1 year of free updates).",
        "pros": [
            "Truly native macOS UI built with Cocoa and Metal graphics acceleration.",
            "Built-in FTP, SFTP, and web staging tools.",
            "Fast extensions engine powered by JavaScript and WebAssembly."
        ],
        "cons": [
            "Exclusive to macOS platform only.",
            "Smaller extension library compared to cross-platform editors."
        ],
        "recommendation": "Best for Mac-focused web developers who want a fast, beautiful, native macOS editing experience."
    },
    "micro": {
        "name": "Micro Editor",
        "description": "A modern and intuitive terminal-based text editor written in Go, featuring standard micro keybindings, mouse support, and multi-cursor editing.",
        "pricing": "100% Free and Open Source (MIT license).",
        "pros": [
            "Familiar Ctrl+C / Ctrl+V keybindings inside the terminal without learning modal Vim keys.",
            "Full terminal mouse support, scrolling, and tab splitting.",
            "Lua plugin system and built-in split terminal."
        ],
        "cons": [
            "Focused primarily on quick terminal file editing rather than large project workspace indexing.",
            "No native graphical UI."
        ],
        "recommendation": "Best for sysadmins and developers needing a modern, hassle-free terminal text editor."
    },
    "acode": {
        "name": "Acode",
        "description": "A powerful, lightweight code editor for Android devices supporting HTML, JavaScript, Python, and mobile web development on the go.",
        "pricing": "Freemium (Free open-source version on F-Droid / Play Store paid tier).",
        "pros": [
            "Optimized touch interface for code editing on Android phones and tablets.",
            "Plugin system supporting syntax highlighting and FTP file management.",
            "Low battery and RAM usage."
        ],
        "cons": [
            "Mobile screen real estate limits heavy multi-window development.",
            "Compilation depends on external terminal apps like Termux."
        ],
        "recommendation": "Best for developers editing web code and quick scripts on Android mobile devices."
    },
    "kakoune": {
        "name": "Kakoune",
        "description": "A modal text editor inspired by Vim with a selection-first interactive model and powerful orthogonal design principles.",
        "pricing": "100% Free and Open Source (Unlicense).",
        "pros": [
            "Selection-first editing paradigm provides instant visual feedback for regex operations.",
            "Multiple selections are a first-class citizen across all editing primitives.",
            "Lightweight C++ implementation."
        ],
        "cons": [
            "Modal philosophy differs from standard Vim, requiring relearning muscle memory.",
            "Terminal-only design."
        ],
        "recommendation": "Best for advanced terminal power users seeking an alternative to Vim with better selection feedback."
    },
    "geany": {
        "name": "Geany",
        "description": "A small and lightweight Integrated Development Environment using GTK+ with basic IDE features and fast startup time.",
        "pricing": "100% Free and Open Source (GPL-2.0).",
        "pros": [
            "Loads instantly with minimal system RAM overhead.",
            "Built-in class browser, symbol lists, and code folding.",
            "Cross-platform support for Linux, Windows, and macOS."
        ],
        "cons": [
            "Classic GTK interface appearance.",
            "Lacks modern AI autocompletion out of the box."
        ],
        "recommendation": "Best for developers on resource-constrained hardware needing a lightweight classic IDE."
    }
}


def load_history() -> dict:
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {"covered_ides": [], "generations": []}


def save_history(history: dict) -> None:
    os.makedirs(os.path.dirname(HISTORY_FILE), exist_ok=True)
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=2)


def fetch_github_trending_editors() -> list:
    """Fetch code editor repositories from GitHub API."""
    url = "https://api.github.com/search/repositories?q=topic:code-editor+sort:stars&per_page=10"
    req = urllib.request.Request(url, headers={"User-Agent": "IDE-Guide-Bot"})
    editors = []
    try:
        with urllib.request.urlopen(req, timeout=5) as resp:
            if resp.status == 200:
                data = json.loads(resp.read().decode("utf-8"))
                for item in data.get("items", []):
                    name = item.get("name", "").capitalize()
                    editors.append({
                        "name": f"{name} Editor" if "editor" not in name.lower() else name,
                        "key": item.get("name", "").lower(),
                        "repo": item.get("html_url")
                    })
    except Exception:
        pass
    return editors


def normalize_key(text: str) -> str:
    """Normalize IDE name or key for robust history comparison."""
    cleaned = text.lower()
    cleaned = re.sub(r"\beditor\b", "", cleaned)
    cleaned = re.sub(r"[^\w]", "", cleaned)
    return cleaned.strip()


def select_daily_ides(history: dict, count: int = 3) -> list:
    covered_keys = set()
    for item in history.get("covered_ides", []):
        covered_keys.add(item.lower().strip())
        covered_keys.add(normalize_key(item))

    selected = []

    def is_covered(ed_item: dict) -> bool:
        name_lower = ed_item["name"].lower().strip()
        key_lower = ed_item["key"].lower().strip()
        norm_name = normalize_key(ed_item["name"])
        norm_key = normalize_key(ed_item["key"])

        return (
            name_lower in covered_keys or
            key_lower in covered_keys or
            norm_name in covered_keys or
            norm_key in covered_keys
        )

    # Attempt GitHub discovery first
    github_editors = fetch_github_trending_editors()
    for ed in github_editors:
        if not is_covered(ed) and len(selected) < count:
            selected.append(ed)
            covered_keys.add(ed["name"].lower().strip())
            covered_keys.add(normalize_key(ed["name"]))

    # Fill remaining from static pool
    for ed in IDE_CANDIDATE_POOL:
        if not is_covered(ed) and len(selected) < count:
            selected.append(ed)
            covered_keys.add(ed["name"].lower().strip())
            covered_keys.add(normalize_key(ed["name"]))

    # Fallback if pool is exhausted
    if len(selected) < count:
        for idx in range(1, count - len(selected) + 1):
            fallback_name = f"Custom Editor {len(history.get('covered_ides', [])) + idx}"
            selected.append({"name": fallback_name, "key": fallback_name.lower()})

    return selected[:count]


def generate_daily_package(date_str: str = None, outdir: str = None) -> dict:
    if not date_str:
        date_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    history = load_history()
    selected_ides = select_daily_ides(history, count=3)

    if not outdir:
        outdir = os.path.join(os.path.dirname(__file__), "..", "content", date_str)
    os.makedirs(outdir, exist_ok=True)

    generated_files = []
    covered_names = []

    for idx, item in enumerate(selected_ides, 1):
        key = item["key"]
        repo = item.get("repo")
        ide_name = item["name"]

        # Retrieve rich info
        if key in EXPANDED_DETAILS:
            info = EXPANDED_DETAILS[key]
        else:
            info = get_ide_info(ide_name=ide_name, repo_url=repo)

        safe_name = re.sub(r"[^\w\-]", "_", info["name"].lower())

        # Generate AMP HTML Post
        amp_html = generate_amp_html(info)
        amp_path = os.path.join(outdir, f"post_{idx}_{safe_name}.amp.html")
        with open(amp_path, "w", encoding="utf-8") as f:
            f.write(amp_html)
        generated_files.append(amp_path)

        # Generate Google Flow Video Spec
        video_spec = generate_google_flow_spec(info)
        spec_path = os.path.join(outdir, f"video_spec_{idx}_{safe_name}.json")
        with open(spec_path, "w", encoding="utf-8") as f:
            json.dump(video_spec, f, indent=2)
        generated_files.append(spec_path)

        covered_names.append(info["name"])

    # Update history
    history.setdefault("covered_ides", [])
    history.setdefault("generations", [])

    for name in covered_names:
        if name not in history["covered_ides"]:
            history["covered_ides"].append(name)

    history["generations"].append({
        "date": date_str,
        "ides_covered": covered_names,
        "files_count": len(generated_files),
        "timestamp": datetime.now(timezone.utc).isoformat()
    })

    save_history(history)

    return {
        "date": date_str,
        "ides": covered_names,
        "files": generated_files,
        "outdir": outdir
    }


def main():
    date_arg = sys.argv[1] if len(sys.argv) > 1 else None
    result = generate_daily_package(date_arg)
    print(f"[✓] Daily content generated successfully for date: {result['date']}")
    print(f"    Covered IDEs ({len(result['ides'])}): {', '.join(result['ides'])}")
    print(f"    Output directory: {result['outdir']}")
    print(f"    Total files generated: {len(result['files'])}")


if __name__ == "__main__":
    main()
