#!/usr/bin/env python3
"""
Daily Content Generation Script for IDE Guide
Generates 3 daily packages (3 AMP HTML blog posts + 3 Google Flow video specs)
Output directory: content/YYYY-MM-DD/
"""

import sys
import os
from datetime import datetime, timezone

# Ensure src path is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.ide_guide.catalog import DEFAULT_IDE_CATALOG
from src.ide_guide.amp_generator import generate_amp_blog_post
from src.ide_guide.google_flow_generator import generate_google_flow_video_spec
from src.ide_guide.history_tracker import HistoryTracker

DAILY_BATCH_COUNT = 3

def main():
    date_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    target_dir = os.path.join("content", date_str)
    os.makedirs(target_dir, exist_ok=True)

    tracker = HistoryTracker()
    uncovered_ides = tracker.get_uncovered_from_catalog(DEFAULT_IDE_CATALOG, count=DAILY_BATCH_COUNT)

    if not uncovered_ides:
        print("⚠️ All catalog items have been covered! Resetting or using fallback catalog...")
        # Fallback to catalog items if all covered
        uncovered_ides = DEFAULT_IDE_CATALOG[:DAILY_BATCH_COUNT]

    print(f"🚀 Running Daily Content Generation for Date: {date_str}")
    print(f"📦 Generating content packages for {len(uncovered_ides)} IDEs...\n")

    generated_summary = []

    for idx, ide_data in enumerate(uncovered_ides, start=1):
        slug = ide_data.get("slug", f"ide-{idx}")
        name = ide_data.get("name", "Code Editor")

        # 1. Generate AMP Blog Post
        amp_html = generate_amp_blog_post(ide_data)
        blog_file = os.path.join(target_dir, f"{slug}_amp_post.html")
        with open(blog_file, "w", encoding="utf-8") as f:
            f.write(amp_html)

        # 2. Generate Google Flow Video Spec (Shorts format)
        video_spec = generate_google_flow_video_spec(ide_data, format_type="shorts")
        video_file = os.path.join(target_dir, f"{slug}_google_flow_spec.md")
        with open(video_file, "w", encoding="utf-8") as f:
            f.write(video_spec)

        # 3. Mark as covered in history tracker
        tracker.mark_covered(ide_data, date_str=date_str)

        generated_summary.append((name, blog_file, video_file))
        print(f"  [{idx}/{len(uncovered_ides)}] {name}")
        print(f"      📄 Blog:  {blog_file}")
        print(f"      🎥 Video: {video_file}")

    print(f"\n✅ Daily generation completed! Total packages created: {len(generated_summary)}")

if __name__ == "__main__":
    main()
