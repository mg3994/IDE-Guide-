#!/usr/bin/env python3
"""
Daily Content Generator for IDE Guide.
Generates 3 daily AMP HTML blog posts and 3 Google Flow video specifications into content/YYYY-MM-DD/
and maintains content/history.json to ensure rotating coverage of IDEs and code editors.
"""

import os
import sys
import json
import datetime
import re
from typing import List, Dict, Any

# Ensure parent directory is in path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from scripts.amp_validator import validate_amp_html, MANDATORY_DISCLAIMER
from scripts.ide_guide_agent_skill import (
    IDE_DATABASE,
    generate_amp_blog_post,
    generate_google_flow_spec,
    derive_ide_info
)

# Additional expanded IDE list for rotation
EXTENDED_IDE_POOL = [
    "vs code",
    "intellij",
    "cursor",
    "neovim",
    "zed",
    "sublime text",
    "pycharm",
    "windsurf",
    "webstorm",
    "xcode",
    "fleet",
    "android studio",
    "eclipse",
    "helix",
    "lapce"
]

ADDITIONAL_PROFILES: Dict[str, Dict[str, Any]] = {
    "webstorm": {
        "name": "JetBrains WebStorm",
        "vendor": "JetBrains",
        "pricing": "Paid ($69+/yr subscription)",
        "pricing_type": "Paid",
        "pros": [
            "Out-of-the-box JavaScript, TypeScript, React, and Vue intelligence.",
            "Integrated refactoring, debugging, and test runner.",
            "Seamless version control and code quality analysis."
        ],
        "cons": [
            "Paid license required.",
            "Heavier RAM usage compared to basic text editors."
        ],
        "best_for": "Professional frontend and full-stack JavaScript/TypeScript engineers.",
        "category": "Web Development IDE"
    },
    "xcode": {
        "name": "Apple Xcode",
        "vendor": "Apple Inc.",
        "pricing": "Free (Requires macOS)",
        "pricing_type": "Free",
        "pros": [
            "Native Swift and SwiftUI live preview design canvases.",
            "Built-in iOS, iPadOS, macOS, and visionOS simulators.",
            "Integrated Instruments performance profiling tool."
        ],
        "cons": [
            "Exclusive to macOS.",
            "Large disk space installation footprint (20GB+)."
        ],
        "best_for": "Apple ecosystem iOS, macOS, and visionOS application developers.",
        "category": "Native macOS/iOS IDE"
    },
    "fleet": {
        "name": "JetBrains Fleet",
        "vendor": "JetBrains",
        "pricing": "Freemium (Public Preview Free / Subscription planned)",
        "pricing_type": "Freemium",
        "pros": [
            "Lightweight editor mode with optional smart IDE engine.",
            "Distributed remote development architecture.",
            "Modern aesthetic and collaborative features."
        ],
        "cons": [
            "Ecosystem still in active preview development.",
            "Plugin availability building up slowly."
        ],
        "best_for": "Developers seeking a modern multi-language polyglot editor.",
        "category": "Next-Gen Polyglot IDE"
    },
    "android studio": {
        "name": "Android Studio",
        "vendor": "Google / JetBrains",
        "pricing": "Free & Open Source Core (Apache 2.0)",
        "pricing_type": "Free / Open Source",
        "pros": [
            "Official IDE for Android development with Jetpack Compose previews.",
            "Advanced Android device emulator and APK analyzer.",
            "Comprehensive memory and battery profilers."
        ],
        "cons": [
            "Demanding system requirements (16GB RAM recommended).",
            "Slow Gradle builds on older hardware."
        ],
        "best_for": "Android mobile developers and Kotlin engineers.",
        "category": "Mobile App IDE"
    },
    "eclipse": {
        "name": "Eclipse IDE",
        "vendor": "Eclipse Foundation",
        "pricing": "Free & Open Source (EPL-2.0)",
        "pricing_type": "Free / Open Source",
        "pros": [
            "Extremely mature plugin ecosystem for Enterprise Java.",
            "Flexible workspace customization and build management.",
            "Zero licensing cost for enterprise deployment."
        ],
        "cons": [
            "UI feel can be dated compared to modern editors.",
            "Plugin compatibility conflicts can occur."
        ],
        "best_for": "Enterprise Java developers working with legacy or open-source stacks.",
        "category": "Enterprise Java IDE"
    },
    "helix": {
        "name": "Helix Editor",
        "vendor": "Helix Community",
        "pricing": "Free & Open Source (MPL-2.0)",
        "pricing_type": "Free / Open Source",
        "pros": [
            "Post-fix modal keybindings (select-then-act model).",
            "Built-in tree-sitter syntax highlighting and LSP integration with zero config.",
            "Written in Rust for instant terminal startup."
        ],
        "cons": [
            "Differs from standard Vim modal keybindings.",
            "No plugin architecture by design yet."
        ],
        "best_for": "Terminal power users seeking zero-config LSP editing.",
        "category": "Terminal Modal Editor"
    },
    "lapce": {
        "name": "Lapce",
        "vendor": "Lapce Community",
        "pricing": "Free & Open Source (Apache 2.0)",
        "pricing_type": "Free / Open Source",
        "pros": [
            "Lightning fast GUI rendered in Rust via Druid.",
            "Native remote development over SSH.",
            "Wasm-based plugin architecture."
        ],
        "cons": [
            "Project in active pre-1.0 development stage.",
            "Smaller extension registry."
        ],
        "best_for": "Developers wanting an open-source, fast native GUI editor.",
        "category": "Native Rust Code Editor"
    }
}


def load_history(history_file: str) -> Dict[str, Any]:
    """Loads historical coverage log."""
    if os.path.exists(history_file):
        try:
            with open(history_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {"covered_ides": [], "daily_logs": []}


def save_history(history_file: str, history_data: Dict[str, Any]) -> None:
    """Saves updated historical coverage log."""
    os.makedirs(os.path.dirname(history_file) or ".", exist_ok=True)
    with open(history_file, "w", encoding="utf-8") as f:
        json.dump(history_data, f, indent=2)


def select_daily_ides(history_data: Dict[str, Any], count: int = 3) -> List[str]:
    """Selects `count` IDE keys from the pool that haven't been covered recently."""
    covered = set(history_data.get("covered_ides", []))

    # Priority 1: Uncovered IDEs
    uncovered = [ide for ide in EXTENDED_IDE_POOL if ide not in covered]

    selected = []
    if len(uncovered) >= count:
        selected = uncovered[:count]
    else:
        # If running out of uncovered IDEs, cycle back least recently covered
        selected = uncovered[:]
        remaining_needed = count - len(selected)
        for ide in EXTENDED_IDE_POOL:
            if ide not in selected:
                selected.append(ide)
                if len(selected) == count:
                    break
    return selected


def get_profile(ide_key: str) -> Dict[str, Any]:
    """Retrieves profile from IDE_DATABASE or ADDITIONAL_PROFILES or fallback."""
    if ide_key in IDE_DATABASE:
        return IDE_DATABASE[ide_key]
    if ide_key in ADDITIONAL_PROFILES:
        return ADDITIONAL_PROFILES[ide_key]
    return derive_ide_info(ide_key)


def generate_daily_package(target_date: str = None, output_root: str = "content", history_path: str = "content/history.json"):
    """Generates 3 AMP blog posts and 3 Google Flow video specs for the given date."""
    if not target_date:
        target_date = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d")

    day_dir = os.path.join(output_root, target_date)
    os.makedirs(day_dir, exist_ok=True)

    history = load_history(history_path)
    selected_keys = select_daily_ides(history, count=3)

    generated_items = []

    for ide_key in selected_keys:
        profile = get_profile(ide_key)
        slug = re.sub(r'[^a-z0-9]+', '_', profile["name"].lower()).strip('_')

        # Generate AMP Blog Post
        blog_html = generate_amp_blog_post(profile)
        is_valid, errors = validate_amp_html(blog_html)
        if not is_valid:
            print(f"⚠️ Validation warnings for {profile['name']}: {errors}")

        post_path = os.path.join(day_dir, f"{slug}_post.html")
        with open(post_path, "w", encoding="utf-8") as f:
            f.write(blog_html)

        # Generate Google Flow Spec
        flow_spec = generate_google_flow_spec(profile)
        spec_path = os.path.join(day_dir, f"{slug}_flow_spec.json")
        with open(spec_path, "w", encoding="utf-8") as f:
            json.dump(flow_spec, f, indent=2)

        generated_items.append({
            "ide_key": ide_key,
            "name": profile["name"],
            "post_path": post_path,
            "spec_path": spec_path
        })

        if ide_key not in history["covered_ides"]:
            history["covered_ides"].append(ide_key)

    log_entry = {
        "date": target_date,
        "timestamp_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "generated_ides": [item["name"] for item in generated_items]
    }
    history.setdefault("daily_logs", []).append(log_entry)

    save_history(history_path, history)

    print(f"🎉 Successfully generated 3 daily packages for IDE Guide ({target_date}) in '{day_dir}':")
    for item in generated_items:
        print(f"  - {item['name']}:")
        print(f"      AMP Blog Post: {item['post_path']}")
        print(f"      Flow Spec:     {item['spec_path']}")


if __name__ == "__main__":
    date_arg = sys.argv[1] if len(sys.argv) > 1 else None
    generate_daily_package(target_date=date_arg)
