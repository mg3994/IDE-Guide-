#!/usr/bin/env python3
"""
Daily Content Generator for IDE Guide.
Generates 3 daily packages (3 AMP Blog Posts + 3 Google Flow Video Specs).
Tracks covered IDEs in content/history.json to ensure new tools are reviewed each day.
"""

import json
import os
import sys
from datetime import datetime, timezone
from scripts.ide_guide_agent_skill import generate_amp_blog_post, generate_google_flow_video_spec
from scripts.amp_validator import validate_amp_html

IDE_DATABASE = [
    {
        "name": "Visual Studio Code",
        "pricing": "Free & Open Source (MIT / Proprietary build)",
        "category": "Extensible Code Editor",
        "pros": ["Massive extension ecosystem", "Lightweight core performance", "Built-in Git integration"],
        "cons": ["High memory usage with many active extensions", "Telemetry enabled by default"],
        "best_for": "Web, cloud, and multi-language developers seeking maximum flexibility",
        "image_url": "https://images.unsplash.com/photo-1555066931-4365d14bab8c?w=800&auto=format&fit=crop"
    },
    {
        "name": "Cursor AI Editor",
        "pricing": "Free Tier available / $20/mo Pro Subscription",
        "category": "AI-Native Code Editor",
        "pros": ["Deep repository indexing", "AI agent multi-file editing", "Seamless VS Code extension compatibility"],
        "cons": ["Requires subscription for unlimited fast queries", "Depends on cloud model uptime"],
        "best_for": "Developers wanting bleeding-edge AI pair programming and automated refactoring",
        "image_url": "https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?w=800&auto=format&fit=crop"
    },
    {
        "name": "JetBrains PyCharm",
        "pricing": "Free Community Edition / Paid Professional ($249/yr)",
        "category": "Dedicated Python IDE",
        "pros": ["Unmatched code analysis & refactoring", "Built-in database and Django tools", "Powerful debugger"],
        "cons": ["Heavy RAM footprint", "Slower startup time compared to lightweight editors"],
        "best_for": "Professional Python, Django, and Data Science engineers",
        "image_url": "https://images.unsplash.com/photo-1515879218367-8466d910aaa4?w=800&auto=format&fit=crop"
    },
    {
        "name": "Neovim",
        "pricing": "100% Free & Open Source (Vim License)",
        "category": "Terminal-based Modal Editor",
        "pros": ["Blazing fast execution", "Infinite Lua customization", "Zero GUI resource overhead"],
        "cons": ["Steep learning curve for modal navigation", "Time-consuming initial configuration"],
        "best_for": "Terminal enthusiasts and keyboard-driven power users",
        "image_url": "https://images.unsplash.com/photo-1629654297299-c8506221ca97?w=800&auto=format&fit=crop"
    },
    {
        "name": "Zed Editor",
        "pricing": "100% Free & Open Source (GPL / Apache 2.0)",
        "category": "High-Performance GPU-Accelerated Editor",
        "pros": ["Written in Rust for instant response times", "Built-in multiplayer pair programming", "Low memory consumption"],
        "cons": ["Ecosystem extensions still maturing", "Platform support expanding gradually"],
        "best_for": "Developers prioritizing raw editor responsiveness and real-time collaboration",
        "image_url": "https://images.unsplash.com/photo-1542831371-29b0f74f9713?w=800&auto=format&fit=crop"
    },
    {
        "name": "JetBrains IntelliJ IDEA",
        "pricing": "Free Community Edition / Paid Ultimate ($599/yr)",
        "category": "Enterprise Java & Kotlin IDE",
        "pros": ["Industry standard for Enterprise Java", "Deep framework integrations (Spring, Quarkus)", "Robust refactoring tools"],
        "cons": ["High memory requirements (min 8GB+ RAM recommended)", "Paid license required for full web stack"],
        "best_for": "Enterprise backend developers and JVM ecosystem engineers",
        "image_url": "https://images.unsplash.com/photo-1517694712202-14dd9538aa97?w=800&auto=format&fit=crop"
    },
    {
        "name": "Sublime Text 4",
        "pricing": "Free evaluation with popup / $99 Commercial License",
        "category": "Lightweight Text & Code Editor",
        "pros": ["Near-instant launch speed", "Smooth rendering on massive files", "Low system resource footprint"],
        "cons": ["Smaller plugin ecosystem than VS Code", "Infrequent feature updates"],
        "best_for": "Developers needing a fast secondary editor for quick file edits and high-performance text manipulation",
        "image_url": "https://images.unsplash.com/photo-1504639725590-34d0984388bd?w=800&auto=format&fit=crop"
    },
    {
        "name": "Windsurf Editor",
        "pricing": "Free Tier / Paid Pro Subscription",
        "category": "Agentic AI IDE",
        "pros": ["Cascade flow real-time code reasoning", "Contextual terminal command suggestion", "Deep codebase graph awareness"],
        "cons": ["Newer product under active development", "Proprietary AI engine reliance"],
        "best_for": "Developers seeking full AI-agent automation across complex multi-file codebases",
        "image_url": "https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=800&auto=format&fit=crop"
    },
    {
        "name": "Eclipse IDE",
        "pricing": "100% Free & Open Source (EPL)",
        "category": "Enterprise Java IDE",
        "pros": ["Extensive open source plugin universe", "Strong legacy Java & C++ project support", "Completely free for commercial use"],
        "cons": ["Cluttered legacy UI", "Higher resource utilization on modern OS"],
        "best_for": "Enterprise Java developers working with open source tooling constraints",
        "image_url": "https://images.unsplash.com/photo-1531403009284-440f080d1e12?w=800&auto=format&fit=crop"
    }
]


def load_history(history_file: str) -> dict:
    if os.path.exists(history_file):
        try:
            with open(history_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {"covered_ides": []}
    return {"covered_ides": []}


def save_history(history_file: str, history_data: dict):
    os.makedirs(os.path.dirname(history_file), exist_ok=True)
    with open(history_file, "w", encoding="utf-8") as f:
        json.dump(history_data, f, indent=2)


def select_daily_ides(count: int = 3, history_file: str = "content/history.json") -> list:
    history = load_history(history_file)
    covered = set(history.get("covered_ides", []))

    available = [ide for ide in IDE_DATABASE if ide["name"] not in covered]

    if len(available) < count:
        # Reset cycle if all IDEs covered
        history["covered_ides"] = []
        covered = set()
        available = list(IDE_DATABASE)

    selected = available[:count]
    return selected


def generate_daily_content():
    today_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    out_dir = os.path.join("content", today_str)
    os.makedirs(out_dir, exist_ok=True)

    history_file = "content/history.json"
    history = load_history(history_file)

    selected_ides = select_daily_ides(3, history_file)

    generated_files = []
    for idx, ide_info in enumerate(selected_ides, start=1):
        slug = ide_info["name"].lower().replace(" ", "_")

        # 1. AMP Blog Post
        amp_html = generate_amp_blog_post(ide_info["name"], ide_info)
        is_valid, errors = validate_amp_html(amp_html)
        if not is_valid:
            print(f"AMP Validation warning for {ide_info['name']}: {errors}")

        amp_filename = f"post_{idx}_{slug}_amp.html"
        amp_path = os.path.join(out_dir, amp_filename)
        with open(amp_path, "w", encoding="utf-8") as f:
            f.write(amp_html)
        generated_files.append(amp_path)

        # 2. Google Flow Video Spec
        video_spec = generate_google_flow_video_spec(ide_info["name"], {
            "pricing": ide_info["pricing"],
            "key_feature": f"{ide_info['category']} - {ide_info['pros'][0]}",
            "pro": ide_info["pros"][0],
            "con": ide_info["cons"][0]
        })
        spec_filename = f"video_{idx}_{slug}_flow_spec.json"
        spec_path = os.path.join(out_dir, spec_filename)
        with open(spec_path, "w", encoding="utf-8") as f:
            json.dump(video_spec, f, indent=2)
        generated_files.append(spec_path)

        if ide_info["name"] not in history["covered_ides"]:
            history["covered_ides"].append(ide_info["name"])

    save_history(history_file, history)

    print(f"Generated {len(generated_files)} content items in '{out_dir}':")
    for filepath in generated_files:
        print(f"  - {filepath}")


if __name__ == "__main__":
    generate_daily_content()
