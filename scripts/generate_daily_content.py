#!/usr/bin/env python3
"""
Daily Content Generator Engine for IDE Guide (@IDEguide & ideguide.blogspot.com)
Generates 3 AMP HTML Blog Posts and 3 Google Flow Video Specifications daily.
Maintains content/history.json to track covered tools and prevent immediate duplication.
"""

import os
import sys
import json
import datetime
import re
from typing import List, Dict, Any, Optional

# Add repository root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from scripts.ide_guide_agent_skill import (
    get_ide_info,
    generate_amp_html_blog_post,
    generate_google_flow_video_spec,
    IDE_DATABASE
)

# Extended catalog for daily rotation
EXTENDED_IDE_CATALOG = [
    "Cursor",
    "Zed",
    "Neovim",
    "VS Code",
    "PyCharm",
    "Windsurf",
    "Helix",
    "Sublime Text",
    "WebStorm",
    "IntelliJ IDEA",
    "Lapce",
    "JetBrains Fleet",
    "Android Studio",
    "Xcode",
    "Nova",
    "BBEdit",
    "GNU Emacs",
    "Micro"
]

# Extended metadata fallback for catalog items not in base IDE_DATABASE
ADDITIONAL_METADATA: Dict[str, Dict[str, Any]] = {
    "webstorm": {
        "name": "WebStorm",
        "category": "JavaScript & TypeScript IDE",
        "developer": "JetBrains",
        "pricing": "Paid License ($69/yr)",
        "pricing_type": "Paid",
        "pros": [
            "Best-in-class JavaScript, TypeScript, React, and Vue intelligence",
            "Built-in test runners, linter integration, and smart refactoring",
            "Seamless version control and debugging capabilities"
        ],
        "cons": [
            "Requires paid subscription after trial period",
            "Higher memory footprint compared to minimal text editors"
        ],
        "best_for": "Professional frontend and full-stack JavaScript/TypeScript engineers.",
        "rating": "4.8/5.0",
        "features": ["TypeScript Intelligence", "React/Vue/Svelte Support", "Built-in Debugger", "Git Integration"]
    },
    "intellij idea": {
        "name": "IntelliJ IDEA",
        "category": "Enterprise Java & Kotlin IDE",
        "developer": "JetBrains",
        "pricing": "Freemium (Community Free / Ultimate Paid)",
        "pricing_type": "Freemium",
        "pros": [
            "Industry standard for Java, Kotlin, and enterprise backend engineering",
            "Deep static analysis, inspections, and framework integration",
            "Powerful database client and Spring Boot support"
        ],
        "cons": [
            "Heavy RAM usage on massive multi-module projects",
            "Ultimate features locked behind commercial license"
        ],
        "best_for": "Enterprise Java, Kotlin, and Spring Boot backend developers.",
        "rating": "4.9/5.0",
        "features": ["Java Static Analysis", "Spring Boot Tools", "Database Tooling", "Refactoring Engine"]
    },
    "lapce": {
        "name": "Lapce",
        "category": "Lightning-Fast Rust Code Editor",
        "developer": "Lapce Community",
        "pricing": "100% Free & Open Source",
        "pricing_type": "Free",
        "pros": [
            "Written in Rust with GPU acceleration (Xi-editor backend / Druid UI)",
            "Native modal editing and remote development capabilities",
            "Wasm-based plugin architecture for lightweight extensibility"
        ],
        "cons": [
            "Still under active early development with occasional breaking changes",
            "Plugin ecosystem is in early stages"
        ],
        "best_for": "Developers seeking an open-source GPU-accelerated lightweight editor.",
        "rating": "4.5/5.0",
        "features": ["GPU Acceleration", "Wasm Plugins", "Native Modal Editing", "Remote Development"]
    },
    "jetbrains fleet": {
        "name": "JetBrains Fleet",
        "category": "Distributed Lightweight IDE",
        "developer": "JetBrains",
        "pricing": "Freemium (Preview / Subscription)",
        "pricing_type": "Freemium",
        "pros": [
            "Fast smart mode with distributed remote development architecture",
            "Clean uncluttered UI designed for quick editing and heavy IDE mode",
            "Multi-language support out of the box"
        ],
        "cons": [
            "Ecosystem and extension marketplace still maturing",
            "Requires switching between Light and Smart modes for full LSP"
        ],
        "best_for": "Polyglot developers and cloud-native remote teams.",
        "rating": "4.6/5.0",
        "features": ["Smart Mode", "Distributed Architecture", "Collaborative Editing", "Multi-Language LSP"]
    },
    "android studio": {
        "name": "Android Studio",
        "category": "Official Android Application IDE",
        "developer": "Google / JetBrains",
        "pricing": "100% Free",
        "pricing_type": "Free",
        "pros": [
            "Official IDE for Android development with Kotlin/Java/C++",
            "Advanced visual layout editor, emulator, and profilers",
            "Deep integration with Jetpack Compose and Firebase"
        ],
        "cons": [
            "Requires significant system resources and high RAM",
            "Gradle build indexing can take time on large apps"
        ],
        "best_for": "Android mobile engineers building native apps.",
        "rating": "4.7/5.0",
        "features": ["Jetpack Compose Preview", "Android Emulator", "APK Analyzer", "Gradle Build System"]
    },
    "xcode": {
        "name": "Xcode",
        "category": "Official Apple Platform IDE",
        "developer": "Apple",
        "pricing": "100% Free (macOS)",
        "pricing_type": "Free",
        "pros": [
            "Essential tool for iOS, macOS, watchOS, and visionOS development",
            "Interactive Swift Canvas previews and Instruments profiling",
            "Seamless app store submission and TestFlight integration"
        ],
        "cons": [
            "Exclusively locked to macOS operating system",
            "Large install size (20GB+) and occasional Xcode version glitches"
        ],
        "best_for": "Apple platform developers building Swift and SwiftUI applications.",
        "rating": "4.5/5.0",
        "features": ["SwiftUI Previews", "Instruments Profiler", "Simulator", "App Store Connect"]
    },
    "nova": {
        "name": "Nova",
        "category": "Native macOS Web & Code Editor",
        "developer": "Panic Inc.",
        "pricing": "Paid License ($99)",
        "pricing_type": "Paid",
        "pros": [
            "Beautiful native macOS UI built with high performance and care",
            "Built-in web preview, FTP/SFTP publishing, and task runner",
            "Extremely fast startup and responsive typing"
        ],
        "cons": [
            "Exclusive to macOS",
            "Smaller plugin library compared to VS Code"
        ],
        "best_for": "Mac web developers who appreciate native macOS software quality.",
        "rating": "4.6/5.0",
        "features": ["Native macOS UI", "Built-in Publishing", "Task Workflows", "Extension API"]
    },
    "bbedit": {
        "name": "BBEdit",
        "category": "Professional Text & HTML Editor",
        "developer": "Bare Bones Software",
        "pricing": "Freemium ($59 License)",
        "pricing_type": "Freemium",
        "pros": [
            "Legendary macOS stability and unmatched large-file regex processing",
            "Rich text manipulation tools, multi-file search, and HTML markup",
            "Lightweight footprint and decades of software refinement"
        ],
        "cons": [
            "macOS only",
            "Traditional visual aesthetic compared to modern electron apps"
        ],
        "best_for": "Mac power users, technical writers, and web developers.",
        "rating": "4.6/5.0",
        "features": ["Multi-File Search", "Pattern Matching", "Text Transformation", "HTML Tools"]
    },
    "gnu emacs": {
        "name": "GNU Emacs",
        "category": "Extensible Self-Documenting Text Editor",
        "developer": "GNU Project",
        "pricing": "100% Free & Open Source",
        "pricing_type": "Free",
        "pros": [
            "Infinite customizability via Emacs Lisp (Elisp)",
            "Ecosystem includes Org-mode, Magit, and complete OS-like features",
            "Decades of community stability and keyboard control"
        ],
        "cons": [
            "Steep learning curve and unique default keybindings",
            "Requires initial investment to construct custom config (or Doom/Spacemacs)"
        ],
        "best_for": "Power users, Lisp hackers, and developers who want total software ownership.",
        "rating": "4.8/5.0",
        "features": ["Elisp Engine", "Org-Mode", "Magit Git Interface", "Self-Documenting Architecture"]
    },
    "micro": {
        "name": "Micro",
        "category": "Modern Intuitive Terminal Text Editor",
        "developer": "Micro Editor Community",
        "pricing": "100% Free & Open Source",
        "pricing_type": "Free",
        "pros": [
            "Easy modern terminal editing with standard Ctrl+C / Ctrl+V keybindings",
            "Full mouse support, split screens, and plugin support in Lua",
            "Single binary download with zero dependencies"
        ],
        "cons": [
            "Not meant to replace full complex IDEs for huge enterprise codebases",
            "Simpler feature set than Neovim or Emacs"
        ],
        "best_for": "Developers wanting an instant, user-friendly CLI terminal editor.",
        "rating": "4.7/5.0",
        "features": ["Standard Shortcuts", "Mouse Support", "Lua Plugins", "Single Binary"]
    }
}


def load_history(history_file: str) -> Dict[str, Any]:
    if os.path.exists(history_file):
        try:
            with open(history_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"Warning: Could not read history file: {e}")
    return {"history": [], "covered_ides": []}


def save_history(history_file: str, data: Dict[str, Any]) -> None:
    os.makedirs(os.path.dirname(os.path.abspath(history_file)), exist_ok=True)
    with open(history_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def select_daily_ides(history_data: Dict[str, Any], count: int = 3) -> List[str]:
    covered = set(history_data.get("covered_ides", []))
    selected = []

    # Priority 1: Pick items from EXTENDED_IDE_CATALOG not yet covered
    for item in EXTENDED_IDE_CATALOG:
        if item.lower() not in covered and item not in selected:
            selected.append(item)
            if len(selected) == count:
                return selected

    # Priority 2: If all catalog items covered, pick least recently covered items
    history_entries = history_data.get("history", [])
    usage_count: Dict[str, int] = {item.lower(): 0 for item in EXTENDED_IDE_CATALOG}
    for entry in history_entries:
        for ide in entry.get("ides", []):
            k = ide.lower()
            usage_count[k] = usage_count.get(k, 0) + 1

    sorted_by_usage = sorted(EXTENDED_IDE_CATALOG, key=lambda x: usage_count.get(x.lower(), 0))
    for item in sorted_by_usage:
        if item not in selected:
            selected.append(item)
            if len(selected) == count:
                break

    return selected


def resolve_ide_metadata(ide_name: str) -> Dict[str, Any]:
    key = ide_name.strip().lower()
    if key in IDE_DATABASE:
        return IDE_DATABASE[key].copy()
    if key in ADDITIONAL_METADATA:
        return ADDITIONAL_METADATA[key].copy()
    return get_ide_info(ide_name)


def generate_daily_content(output_date: Optional[str] = None, base_dir: str = "content") -> List[str]:
    today_str = output_date or datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d")
    history_file = os.path.join(base_dir, "history.json")
    history_data = load_history(history_file)

    selected_ides = select_daily_ides(history_data, count=3)
    target_dir = os.path.join(base_dir, today_str)
    os.makedirs(target_dir, exist_ok=True)

    generated_files = []

    for idx, ide_name in enumerate(selected_ides, start=1):
        info = resolve_ide_metadata(ide_name)
        slug = re.sub(r'[^a-z0-9]+', '_', info['name'].lower()).strip('_')

        # Generate AMP HTML blog post
        amp_content = generate_amp_html_blog_post(info)
        amp_filename = f"post_{idx}_{slug}.html"
        amp_filepath = os.path.join(target_dir, amp_filename)
        with open(amp_filepath, "w", encoding="utf-8") as f:
            f.write(amp_content)
        generated_files.append(amp_filepath)

        # Generate Google Flow video spec
        video_spec = generate_google_flow_video_spec(info)
        video_filename = f"video_spec_{idx}_{slug}.md"
        video_filepath = os.path.join(target_dir, video_filename)
        with open(video_filepath, "w", encoding="utf-8") as f:
            f.write(video_spec)
        generated_files.append(video_filepath)

    # Update history tracking
    history_data["history"].append({
        "date": today_str,
        "ides": selected_ides
    })
    covered_set = set(history_data.get("covered_ides", []))
    for ide in selected_ides:
        covered_set.add(ide.lower())
    history_data["covered_ides"] = list(covered_set)

    save_history(history_file, history_data)

    print(f"=== Daily Content Generation Complete for {today_str} ===")
    print(f"Featured IDEs: {', '.join(selected_ides)}")
    print(f"Saved {len(generated_files)} files in: {target_dir}")
    for f in generated_files:
        print(f"  - {f}")

    return generated_files


if __name__ == "__main__":
    generate_daily_content()
