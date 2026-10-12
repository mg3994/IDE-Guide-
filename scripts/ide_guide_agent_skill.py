#!/usr/bin/env python3
"""
Agentic CLI Skill Tool for IDE Guide.
Generates AMP HTML Blog Posts and Google Flow Video Specifications on demand for any IDE / Code Editor or Repository URL.
"""

import sys
import json
import argparse
from typing import Dict, Any

MANDATORY_DISCLAIMER = (
    "Disclaimer: IDE Guide is an independent technical publication. "
    "This content is not sponsored, endorsed, or affiliated with any software vendor or editor developer mentioned above. "
    "All reviews and assessments are based strictly on objective developer evaluation."
)

IDE_KNOWLEDGE_BASE = {
    "Cursor": {
        "full_name": "Cursor AI Code Editor",
        "category": "AI-First Code Editor",
        "pricing_type": "Freemium ($20/mo Pro)",
        "developer": "Anysphere",
        "tagline": "The AI-first Code Editor Built for Speed and Flow",
        "pros": ["Deep codebase indexing & context awareness", "In-line AI editing with Cmd+K", "Seamless VS Code extension compatibility"],
        "cons": ["Subscription cost for heavy AI usage", "Requires cloud connection for advanced AI features"],
        "best_for": "Developers wanting maximum AI velocity and automated multi-file editing.",
        "free_tier": "Free plan includes 200 GPT-3.5 / Claude Haiku uses and 50 slow GPT-4 uses per month.",
        "paid_tier": "Pro tier at $20/month with unlimited fast requests and advanced Claude 3.5 Sonnet access."
    },
    "VS Code": {
        "full_name": "Visual Studio Code",
        "category": "Extensible Code Editor",
        "pricing_type": "Free & Open Source Core",
        "developer": "Microsoft",
        "tagline": "Code Editing. Redefined.",
        "pros": ["Massive extension ecosystem", "Lightweight startup with customizable UI", "Built-in Git and terminal integration"],
        "cons": ["High memory consumption with dozens of active extensions", "Requires configuration for heavy multi-file refactoring"],
        "best_for": "Web developers, generalists, and open-source contributors.",
        "free_tier": "100% Free under MIT license / Code-OSS.",
        "paid_tier": "Completely free; optional paid extension integrations like GitHub Copilot."
    },
    "IntelliJ IDEA": {
        "full_name": "JetBrains IntelliJ IDEA",
        "category": "Full-Featured Enterprise IDE",
        "pricing_type": "Freemium / Paid Commercial",
        "developer": "JetBrains",
        "tagline": "The Capable and Ergonomic Java IDE",
        "pros": ["Unmatched Java, Kotlin, and Spring static analysis", "Refactoring suite is industry benchmark", "Deep database and framework integrations"],
        "cons": ["Heavy memory footprint (2GB+ RAM minimum)", "Complex settings and steep learning curve"],
        "best_for": "Enterprise Java, Kotlin, Spring Boot, and backend developers.",
        "free_tier": "Community Edition is free & open source for JVM/Android.",
        "paid_tier": "Ultimate Edition starts at $16.90/month or $169/year."
    },
    "PyCharm": {
        "full_name": "JetBrains PyCharm",
        "category": "Python Dedicated IDE",
        "pricing_type": "Freemium / Paid Professional",
        "developer": "JetBrains",
        "tagline": "The Python IDE for Professional Developers",
        "pros": ["Superior Python autocompletion and type checking", "Built-in Jupyter notebooks & scientific tools", "Django and Flask framework debugging"],
        "cons": ["Slower startup compared to lightweight editors", "Professional features require active subscription"],
        "best_for": "Data scientists, ML engineers, and Django/FastAPI web developers.",
        "free_tier": "Community Edition is free for pure Python development.",
        "paid_tier": "Professional Edition at $10.90/month or $109/year."
    },
    "Neovim": {
        "full_name": "Neovim",
        "category": "Terminal Modal Text Editor",
        "pricing_type": "100% Free & Open Source",
        "developer": "Neovim Core Team",
        "tagline": "Vim-fork focused on extensibility and usability",
        "pros": ["Blazing fast startup and minimal RAM usage (<50MB)", "Lua plugin ecosystem and built-in LSP", "Full keyboard navigation without mouse dependence"],
        "cons": ["Steep modal editing learning curve", "Requires manual configuration setup (e.g. LazyVim, AstroNvim)"],
        "best_for": "Terminal power users, DevOps engineers, and keyboard-driven developers.",
        "free_tier": "100% Free and open-source under Apache / Vim license.",
        "paid_tier": "None. Free forever."
    },
    "Zed": {
        "full_name": "Zed Editor",
        "category": "High-Performance Collaborative Editor",
        "pricing_type": "Free & Open Source",
        "developer": "Zed Industries",
        "tagline": "High-Performance, Multi-Player Code Editor Written in Rust",
        "pros": ["120 FPS GPU-accelerated rendering engine", "Instant startup and microsecond latency", "Built-in real-time multiplayer pair programming"],
        "cons": ["Ecosystem of extensions is still maturing", "Windows support currently in preview/beta"],
        "best_for": "Rust, Go, and TypeScript developers seeking extreme UI responsiveness.",
        "free_tier": "100% Free open-source editor core.",
        "paid_tier": "Optional cloud collaboration and AI token add-ons."
    },
    "Windsurf": {
        "full_name": "Windsurf IDE",
        "category": "Agentic AI Code Editor",
        "pricing_type": "Freemium ($15/mo Pro)",
        "developer": "Codeium",
        "tagline": "The First Agentic IDE Powered by Cascade AI",
        "pros": ["Flow State AI collaborative agent", "Real-time command execution and file edits", "Free tier with generous AI credits"],
        "cons": ["Newer product with evolving UI workflows", "Requires online connection for Cascade AI"],
        "best_for": "Developers seeking autonomous agentic code generation and fast iteration.",
        "free_tier": "Free tier available with daily Cascade agent credits.",
        "paid_tier": "Pro plan at $15/month for unlimited fast agent interactions."
    }
}

def get_ide_info(ide_name: str) -> Dict[str, Any]:
    for name, data in IDE_KNOWLEDGE_BASE.items():
        if ide_name.lower() in name.lower() or name.lower() in ide_name.lower():
            return data

    # Generic fallback for unknown IDEs / Repositories
    return {
        "full_name": f"{ide_name} Editor/IDE",
        "category": "Developer Tool / IDE",
        "pricing_type": "Free / Commercial Options Available",
        "developer": "Open Source / Independent Developer",
        "tagline": f"Streamlined developer environment for {ide_name}",
        "pros": ["Modern code navigation", "Customizable extension support", "Developer productivity tools"],
        "cons": ["Configuration required for specialized frameworks", "Ecosystem adoption variations"],
        "best_for": f"Software engineers working with {ide_name}.",
        "free_tier": "Check official website or repository for free community downloads.",
        "paid_tier": "Commercial licenses available for enterprise use."
    }

def generate_amp_blog_post(ide_name: str) -> str:
    info = get_ide_info(ide_name)

    amp_html = f"""<article class="ide-guide-post">
  <header>
    <h1>{info['full_name']} Review: Is It Worth It in 2026?</h1>
    <p class="subtitle"><em>{info['tagline']}</em></p>
  </header>

  <style amp-custom>
    article.ide-guide-post {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; line-height: 1.6; color: #222; max-width: 800px; margin: 0 auto; padding: 15px; }}
    .badge {{ display: inline-block; background-color: #007acc; color: #fff; padding: 4px 10px; border-radius: 4px; font-size: 0.85em; font-weight: bold; }}
    .pricing-box {{ background-color: #f4f6f8; border-left: 4px solid #007acc; padding: 12px; margin: 20px 0; }}
    .pros-cons {{ display: flex; flex-wrap: wrap; gap: 15px; margin: 20px 0; }}
    .pros, .cons {{ flex: 1; min-width: 280px; padding: 12px; border-radius: 6px; }}
    .pros {{ background-color: #eef9f2; border: 1px solid #b7ebc6; }}
    .cons {{ background-color: #fdf2f2; border: 1px solid #f8c4c4; }}
    .disclaimer {{ font-size: 0.85em; color: #666; background-color: #fafafa; border: 1px solid #eee; padding: 10px; border-radius: 4px; margin-top: 30px; line-height: 1.4; }}
  </style>

  <section class="overview">
    <h2>Overview & Target Audience</h2>
    <p><strong>Category:</strong> <span class="badge">{info['category']}</span></p>
    <p><strong>Developer:</strong> {info['developer']}</p>
    <p><strong>Best For:</strong> {info['best_for']}</p>
    <p>{info['full_name']} has captured significant attention in the software engineering space. Designed to streamline workflow efficiency, it targets developers looking for reliability, high performance, and ergonomic coding experience.</p>
  </section>

  <section class="pros-cons">
    <div class="pros">
      <h3>🟢 The Good (Strengths)</h3>
      <ul>
        {''.join(f'<li>{p}</li>' for p in info['pros'])}
      </ul>
    </div>
    <div class="cons">
      <h3>🔴 The Bad (Limitations)</h3>
      <ul>
        {''.join(f'<li>{c}</li>' for c in info['cons'])}
      </ul>
    </div>
  </section>

  <section class="pricing">
    <h2>Pricing & Plan Options</h2>
    <div class="pricing-box">
      <p><strong>Pricing Model:</strong> {info['pricing_type']}</p>
      <p><strong>Free Tier:</strong> {info['free_tier']}</p>
      <p><strong>Paid Options:</strong> {info['paid_tier']}</p>
    </div>
  </section>

  <section class="verdict">
    <h2>Final Verdict</h2>
    <p>If you are looking for an editor tailored for high velocity, <strong>{info['full_name']}</strong> is definitely worth evaluating. Check your team's workflow requirements and trial the free tier first.</p>
  </section>

  <footer class="disclaimer">
    <p>{MANDATORY_DISCLAIMER}</p>
  </footer>
</article>"""
    return amp_html

def generate_google_flow_spec(ide_name: str) -> Dict[str, Any]:
    info = get_ide_info(ide_name)

    spec = {
        "title": f"{info['full_name']} - Complete Developer Breakdown",
        "target_platform": "YouTube Shorts & Standard Video (@IDEguide)",
        "ratio": "9:16 vertical & 16:9 widescreen",
        "ide_name": info['full_name'],
        "pricing_type": info['pricing_type'],
        "google_flow_prompts": [
            {
                "scene_number": 1,
                "scene_title": "Hook & Visual Intro",
                "duration_seconds": 5,
                "visual_prompt": f"Ultra-detailed 4K cinematic close-up of {info['full_name']} interface on a dark curved monitor, vivid neon code highlight animation, camera slow pan right with shallow depth of field.",
                "camera_movement": "Cinematic slow pan right",
                "lighting": "Dark aesthetic workspace, neon blue and ambient LED desktop backlighting",
                "voiceover_script": f"Is {info['full_name']} the best code editor for developers right now? Here is the honest breakdown in 60 seconds.",
                "text_overlay": f"{info['full_name']} Review | IDE Guide"
            },
            {
                "scene_number": 2,
                "scene_title": "Overview & Best Use Case",
                "duration_seconds": 15,
                "visual_prompt": f"Over-the-shoulder shot of a software developer typing code in {info['full_name']}, showing smooth autocompletion and file explorer navigation.",
                "camera_movement": "Over-the-shoulder steady tracking shot",
                "lighting": "Clean studio lighting, crisp high-contrast monitor output",
                "voiceover_script": f"Developed as a {info['category']}, {info['full_name']} excels at fast iteration. It's best for {info['best_for']}",
                "text_overlay": f"Category: {info['category']}\nBest For: {info['best_for']}"
            },
            {
                "scene_number": 3,
                "scene_title": "The Good (Key Features)",
                "duration_seconds": 18,
                "visual_prompt": f"Split dynamic screen highlighting key strengths of {info['full_name']}: {', '.join(info['pros'])}. Smooth green checkmark graphic overlay.",
                "camera_movement": "Dynamic screen split transition",
                "lighting": "Bright green accent glow on features list",
                "voiceover_script": f"The good? You get {info['pros'][0]}, plus {info['pros'][1]}. Efficiency and speed are top-notch.",
                "text_overlay": f"PROS:\n- {info['pros'][0]}\n- {info['pros'][1]}"
            },
            {
                "scene_number": 4,
                "scene_title": "The Bad & Pricing",
                "duration_seconds": 12,
                "visual_prompt": f"Red accent screen callout showing trade-offs: {info['cons'][0]}. Followed by price tag display: {info['pricing_type']}.",
                "camera_movement": "Fast push zoom to price tag badge",
                "lighting": "Subtle dark red ambient accent lighting",
                "voiceover_script": f"The bad? Watch out for {info['cons'][0]}. Price-wise, it offers {info['pricing_type']}.",
                "text_overlay": f"CONS: {info['cons'][0]}\nPRICING: {info['pricing_type']}"
            },
            {
                "scene_number": 5,
                "scene_title": "Verdict & Non-Sponsorship Disclaimer",
                "duration_seconds": 10,
                "visual_prompt": "Clean studio camera view of modern developer desk with glowing IDE Guide logo. Clear transparent banner with objective disclaimer text.",
                "camera_movement": "Slow zoom out to full studio desk",
                "lighting": "Warm ambient studio illumination",
                "voiceover_script": f"Subscribe to IDE Guide for daily editor reviews. {MANDATORY_DISCLAIMER}",
                "text_overlay": "IDE Guide - Independent Review\nSubscribe @IDEguide"
            }
        ],
        "disclaimer": MANDATORY_DISCLAIMER
    }
    return spec

def main():
    parser = argparse.ArgumentParser(description="IDE Guide Agentic CLI Skill Tool")
    parser.add_argument("--ide", type=str, required=True, help="Name of the IDE, Code Editor, or repo to process")
    parser.add_argument("--out-blog", type=str, help="Path to save output AMP HTML blog post")
    parser.add_argument("--out-video", type=str, help="Path to save output Google Flow video spec JSON")
    args = parser.parse_args()

    blog_content = generate_amp_blog_post(args.ide)
    video_spec = generate_google_flow_spec(args.ide)

    if args.out_blog:
        with open(args.out_blog, "w", encoding="utf-8") as f:
            f.write(blog_content)
        print(f"Generated AMP blog post saved to {args.out_blog}")
    else:
        print("--- AMP BLOG POST ---")
        print(blog_content)

    if args.out_video:
        with open(args.out_video, "w", encoding="utf-8") as f:
            json.dump(video_spec, f, indent=2)
        print(f"Generated Google Flow video spec saved to {args.out_video}")
    else:
        print("\n--- GOOGLE FLOW VIDEO SPEC ---")
        print(json.dumps(video_spec, indent=2))

if __name__ == "__main__":
    main()
