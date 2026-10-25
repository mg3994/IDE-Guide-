#!/usr/bin/env python3
"""
Daily Content Generator for IDE Guide.
Generates 3 AMP Blog Posts and 3 Google Flow Video Specs daily.
Maintains history tracking in content/history.json to ensure variety across runs.
"""

import datetime
import json
import os
import re
import sys
from typing import List, Dict, Any

# Ensure parent path is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from scripts.amp_validator import validate_amp_html
from scripts.ide_guide_agent_skill import (
    IDE_DATABASE,
    get_ide_info,
    generate_amp_blog_post,
    generate_google_flow_spec
)

# Extended pool of IDEs and editors for daily rotation
EXTENDED_IDE_POOL: List[Dict[str, Any]] = [
    {
        "full_name": "Visual Studio Code",
        "developer": "Microsoft",
        "pricing": "Free & Open Source",
        "paid_tier": "Free for personal & commercial use.",
        "pros": ["Extensive extension library", "Ubiquitous community support", "Integrated debugging"],
        "cons": ["Electron memory consumption", "Default telemetry"],
        "target_audience": "General developers, Web engineers, Cloud developers.",
        "key_features": ["IntelliSense auto-complete", "Built-in Git & terminal", "Extension Ecosystem", "Remote - SSH & Containers"]
    },
    {
        "full_name": "Cursor AI Code Editor",
        "developer": "Anysphere",
        "pricing": "Freemium",
        "paid_tier": "$20/mo Pro subscription for unlimited fast AI models.",
        "pros": ["Native codebase RAG indexing", "Multi-file Composer editing", "VS Code extension compatibility"],
        "cons": ["Subscription required for heavy AI features", "Occasional lag on large codebases"],
        "target_audience": "AI-focused software engineers and fast-paced developers.",
        "key_features": ["Cmd+K Code Generation", "Codebase Indexing", "Cursor Composer", "Instant Terminal Debugging"]
    },
    {
        "full_name": "Zed Editor",
        "developer": "Zed Industries",
        "pricing": "Free & Open Source",
        "paid_tier": "100% Free for local editor.",
        "pros": ["Rust GPU-accelerated editor", "Sub-millisecond startup time", "CRDT multiplayer pair programming"],
        "cons": ["Young plugin ecosystem", "Fewer extensions than VS Code"],
        "target_audience": "Rust developers, performance purists, and collaborative teams.",
        "key_features": ["GPU-accelerated metal rendering", "Native Rust performance", "CRDT multiplayer collaboration", "Integrated AI assistance"]
    },
    {
        "full_name": "PyCharm IDE",
        "developer": "JetBrains",
        "pricing": "Freemium",
        "paid_tier": "Professional Edition: $249/year or $24.90/month.",
        "pros": ["Top-tier Python refactoring", "Django/Flask framework support", "Database management integration"],
        "cons": ["High memory consumption", "Indexing delay on launch"],
        "target_audience": "Python engineers, Data Scientists, Django developers.",
        "key_features": ["Deep Python code analysis", "Django/Flask web tools", "Integrated database viewer", "Scientific NumPy/Pandas support"]
    },
    {
        "full_name": "Neovim",
        "developer": "Community-driven",
        "pricing": "100% Free & Open Source",
        "paid_tier": "Completely free.",
        "pros": ["Ultra-lightweight", "Lua scripting setup", "Modal speed"],
        "cons": ["Steep initial learning curve", "Requires manual plugin setup"],
        "target_audience": "Terminal purists, CLI lovers, and power users.",
        "key_features": ["Built-in LSP client", "Lua configuration engine", "Treesitter syntax highlighting", "Asynchronous plugin host"]
    },
    {
        "full_name": "JetBrains Fleet",
        "developer": "JetBrains",
        "pricing": "Freemium",
        "paid_tier": "Included in JetBrains All Products Pack.",
        "pros": ["Lightweight polyglot editor", "Smart Mode toggle", "Distributed architecture"],
        "cons": ["Ecosystem in early development", "Smart Mode required for full intelligence"],
        "target_audience": "Developers who want JetBrains smarts without bloated UI.",
        "key_features": ["Smart Mode code intelligence", "Collaborative editing", "Multi-language support", "Distributed dev architecture"]
    },
    {
        "full_name": "Sublime Text 4",
        "developer": "Sublime HQ",
        "pricing": "Paid ($99 per license, free indefinite evaluation)",
        "paid_tier": "$99 one-time purchase for 3 years of updates.",
        "pros": ["Instant launch speed", "GPU rendering", "Multi-tab handling capability"],
        "cons": ["Proprietary license", "Smaller ecosystem compared to VS Code"],
        "target_audience": "Developers wanting minimal lag and fast text editing.",
        "key_features": ["GPU rendering engine", "Tab multi-select", "Context-aware auto-complete", "Python API ecosystem"]
    },
    {
        "full_name": "Helix Editor",
        "developer": "Helix Community",
        "pricing": "100% Free & Open Source",
        "paid_tier": "Completely free.",
        "pros": ["Zero config required out of the box", "Built-in LSP support", "Written in Rust"],
        "cons": ["Plugin system still under active design", "Strict kakoune-style modal editing"],
        "target_audience": "Terminal developers looking for zero-config modern vim alternatives.",
        "key_features": ["Built-in LSP auto-complete", "Treesitter syntax highlighting", "Multiple selections", "Rust terminal architecture"]
    },
    {
        "full_name": "Android Studio",
        "developer": "Google / JetBrains",
        "pricing": "Free & Open Source",
        "paid_tier": "Free for Android development.",
        "pros": ["Official IDE for Android development", "Built-in emulator & profilers", "Jetpack Compose live preview"],
        "cons": ["Heavy CPU and RAM consumption", "Large initial download size"],
        "target_audience": "Android and Kotlin mobile app developers.",
        "key_features": ["Jetpack Compose Layout Inspector", "Android Emulator", "APK Analyzer", "Kotlin Multiplatform support"]
    },
    {
        "full_name": "Xcode",
        "developer": "Apple",
        "pricing": "Free (macOS required)",
        "paid_tier": "Free editor; Apple Developer Program ($99/year) required for App Store publishing.",
        "pros": ["Native macOS and iOS development toolchain", "SwiftUI Previews", "Integrated Instruments profiler"],
        "cons": ["macOS lock-in", "Large storage footprint"],
        "target_audience": "iOS, macOS, watchOS, and visionOS software engineers.",
        "key_features": ["SwiftUI Live Canvas", "Xcode Cloud CI/CD", "Instruments performance profiling", "Asset Catalog Manager"]
    }
]

HISTORY_FILE = os.path.join("content", "history.json")


def load_history() -> List[str]:
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get("covered_ides", [])
        except Exception:
            return []
    return []


def save_history(history: List[str]):
    os.makedirs(os.path.dirname(HISTORY_FILE), exist_ok=True)
    with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
        json.dump({"covered_ides": history, "last_updated": datetime.datetime.now(datetime.timezone.utc).isoformat()}, f, indent=2)


def select_daily_ides(count: int = 3) -> List[Dict[str, Any]]:
    history = load_history()
    available = [ide for ide in EXTENDED_IDE_POOL if ide["full_name"] not in history]

    # If pool is exhausted, reset history tracking
    if len(available) < count:
        history = []
        available = EXTENDED_IDE_POOL

    selected = available[:count]
    updated_history = history + [ide["full_name"] for ide in selected]
    save_history(updated_history)
    return selected


def generate_daily_package(target_date: str = None) -> str:
    if not target_date:
        target_date = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d")

    output_dir = os.path.join("content", target_date)
    os.makedirs(output_dir, exist_ok=True)

    selected_ides = select_daily_ides(3)
    print(f"🚀 Generating daily content package for {target_date} with IDEs: {[i['full_name'] for i in selected_ides]}")

    manifest = {
        "date": target_date,
        "items": []
    }

    for idx, ide_info in enumerate(selected_ides, start=1):
        safe_name = re.sub(r'[^a-zA-Z0-9_-]', '_', ide_info['full_name'].lower())

        # 1. Generate AMP Blog
        amp_html = generate_amp_blog_post(ide_info, canonical_url=f"https://ideguide.blogspot.com/{target_date}/{safe_name}")
        is_valid, errors = validate_amp_html(amp_html)
        if not is_valid:
            print(f"⚠️ AMP warning for {ide_info['full_name']}: {errors}", file=sys.stderr)

        blog_path = os.path.join(output_dir, f"post_{idx}_{safe_name}.html")
        with open(blog_path, 'w', encoding='utf-8') as f:
            f.write(amp_html)

        # 2. Generate Google Flow Video Spec
        flow_spec = generate_google_flow_spec(ide_info)
        spec_path = os.path.join(output_dir, f"video_{idx}_{safe_name}.json")
        with open(spec_path, 'w', encoding='utf-8') as f:
            json.dump(flow_spec, f, indent=2)

        manifest["items"].append({
            "index": idx,
            "ide": ide_info['full_name'],
            "blog_file": blog_path,
            "video_spec_file": spec_path,
            "amp_valid": is_valid
        })

    manifest_path = os.path.join(output_dir, "manifest.json")
    with open(manifest_path, 'w', encoding='utf-8') as f:
        json.dump(manifest, f, indent=2)

    print(f"✨ Daily content package generation complete! Output folder: {output_dir}")
    return output_dir


if __name__ == "__main__":
    generate_daily_package()
