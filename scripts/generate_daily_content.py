#!/usr/bin/env python3
"""
Daily Content Generation Engine for IDE Guide.
Generates 3 daily packages (3 AMP HTML Blog Posts + 3 Google Flow Video Specifications).
Saves outputs in content/YYYY-MM-DD/ and updates content/history.json.
"""

import json
import os
import datetime
import re
from typing import Dict, List, Any

MANDATORY_DISCLAIMER_PHRASE = (
    "Disclaimer: IDE Guide is an independent technical publication. "
    "This content is not sponsored, endorsed, or affiliated with any software vendor or editor developer mentioned above. "
    "All reviews and assessments are based strictly on objective developer evaluation."
)

IDE_DATABASE: List[Dict[str, Any]] = [
    {
        "id": "vscode",
        "name": "Visual Studio Code",
        "developer": "Microsoft",
        "pricing": "Free / Open Source (MIT core)",
        "pricing_type": "Free",
        "category": "Code Editor / Lightweight IDE",
        "primary_use": "Web Development, Python, TypeScript, Cloud Native",
        "key_features": [
            "Extensive extension ecosystem with over 50,000 extensions",
            "Built-in Git and GitHub integration",
            "Integrated terminal and multi-root workspaces",
            "IntelliSense smart code completion and refactoring"
        ],
        "pros": [
            "Massive community support and extension availability",
            "Highly customizable interface and keybindings",
            "Frequent monthly updates with active active development",
            "Seamless remote development via SSH, Containers, and WSL"
        ],
        "cons": [
            "Can consume significant RAM with many active extensions",
            "Requires configuration tuning out of the box for complex enterprise setups"
        ],
        "target_audience": "Full-stack web developers, Python programmers, DevOps engineers, and students."
    },
    {
        "id": "cursor-ai",
        "name": "Cursor AI",
        "developer": "Anysphere",
        "pricing": "Freemium ($20/mo Pro plan)",
        "pricing_type": "Freemium",
        "category": "AI-Native Code Editor",
        "primary_use": "AI-assisted Software Development, Full-Stack Coding",
        "key_features": [
            "Deep repository-wide context indexing for AI assistance",
            "Inline AI code editing (Cmd+K) and terminal agent mode",
            "VS Code extension compatibility via fork architecture",
            "Multi-file edits and automated bug resolution"
        ],
        "pros": [
            "Unrivaled speed for AI code generation and workspace queries",
            "Familiar layout for existing VS Code users",
            "Smart prediction model for next-line code autocompletion"
        ],
        "cons": [
            "Paid tier required for heavy LLM usage",
            "Closed-source proprietary extensions"
        ],
        "target_audience": "Developers seeking maximum productivity through deeply integrated AI code agents."
    },
    {
        "id": "intellij-idea",
        "name": "JetBrains IntelliJ IDEA",
        "developer": "JetBrains",
        "pricing": "Freemium (Community Free / Ultimate $169+/yr)",
        "pricing_type": "Freemium",
        "category": "Enterprise Java & Kotlin IDE",
        "primary_use": "Java, Kotlin, Enterprise Spring Boot, Microservices",
        "key_features": [
            "Deep static code analysis and automated refactoring",
            "Native Spring Boot, Kubernetes, and database tools",
            "Advanced debugger with expression evaluation and stack frame inspection",
            "Out-of-the-box build tool integration (Maven, Gradle)"
        ],
        "pros": [
            "Unmatched intelligence for Java/JVM ecosystem development",
            "Powerful enterprise refactoring tools",
            "Comprehensive built-in database and HTTP client tooling"
        ],
        "cons": [
            "Heavy memory footprint requiring robust hardware",
            "Steeper learning curve for novice programmers"
        ],
        "target_audience": "Enterprise Java engineers, Kotlin developers, and backend microservice architects."
    },
    {
        "id": "neovim",
        "name": "Neovim",
        "developer": "Neovim Core Team (Community)",
        "pricing": "100% Free / Open Source (Apache/Vim License)",
        "pricing_type": "Free",
        "category": "Modal Terminal Text Editor",
        "primary_use": "Terminal-first High Performance Editing, C, Rust, Go, Web",
        "key_features": [
            "Embedded Lua 5.1 runtime for lightning-fast configuration",
            "Native Language Server Protocol (LSP) client support",
            "Tree-sitter integration for fast AST-based syntax highlighting",
            "Blazing fast startup time (< 20ms)"
        ],
        "pros": [
            "Near-zero memory footprint and extreme responsiveness",
            "Complete modal keyboard control without touching a mouse",
            "Vast ecosystem of user-maintained Lua plugins"
        ],
        "cons": [
            "High learning curve requiring modal editing proficiency",
            "Requires time investment to configure custom development setup"
        ],
        "target_audience": "Command-line power users, systems programmers, and Vim enthusiasts."
    },
    {
        "id": "zed-editor",
        "name": "Zed Editor",
        "developer": "Zed Industries",
        "pricing": "Free / Open Source (GPL/Apache)",
        "pricing_type": "Free",
        "category": "High-Performance Code Editor",
        "primary_use": "Rust, C++, Web Development, Real-time Pair Programming",
        "key_features": [
            "GPU-accelerated rendering pipeline built in Rust",
            "Built-in multi-user real-time collaborative coding",
            "Integrated AI assistant support (Claude 3.5, GPT-4o)",
            "Instant startup and 120 FPS rendering"
        ],
        "pros": [
            "Extremely fluid UI responsiveness and lower latency",
            "Native multiplayer pair-programming capabilities",
            "Clean minimal aesthetic"
        ],
        "cons": [
            "Ecosystem of plugins is still maturing compared to VS Code",
            "Linux and Windows ports in active ongoing refinement"
        ],
        "target_audience": "Developers who prioritize raw performance, low latency, and real-time team collaboration."
    },
    {
        "id": "pycharm",
        "name": "PyCharm",
        "developer": "JetBrains",
        "pricing": "Freemium (Community Free / Professional $99+/yr)",
        "pricing_type": "Freemium",
        "category": "Python Dedicated IDE",
        "primary_use": "Python Data Science, Django/FastAPI Web Apps, AI/ML",
        "key_features": [
            "Smart Python code completion and type checking",
            "Integrated Jupyter Notebook support and Data Viewer",
            "Built-in virtual environment and Docker support",
            "Visual debugger with interactive console"
        ],
        "pros": [
            "Best-in-class tooling for Python frameworks like Django and Flask",
            "Seamless data science tooling and dataframe inspection",
            "Out-of-the-box virtualenv and Conda environment handling"
        ],
        "cons": [
            "Can be resource intensive on mid-range laptops",
            "Professional edition needed for full web framework features"
        ],
        "target_audience": "Python developers, data scientists, AI engineers, and web developers."
    },
    {
        "id": "windsurf",
        "name": "Windsurf Editor",
        "developer": "Codeium",
        "pricing": "Freemium (Free tier / $10-$15/mo Pro)",
        "pricing_type": "Freemium",
        "category": "AI Flow Code Editor",
        "primary_use": "AI-Agentic Coding, Collaborative Web Development",
        "key_features": [
            "Cascade AI agent with deep contextual understanding",
            "Real-time terminal execution and AI command correction",
            "VS Code extension compatibility",
            "Multi-file synchronous edits and refactoring"
        ],
        "pros": [
            "Innovative Cascade flow state for agentic coding",
            "Generous free usage tier provided by Codeium",
            "Fast context retrieval across repository files"
        ],
        "cons": [
            "Relatively new tool with evolving user interface features",
            "Requires active internet connectivity for full AI capabilities"
        ],
        "target_audience": "Developers looking for high-velocity agentic AI pair programming."
    },
    {
        "id": "sublime-text",
        "name": "Sublime Text 4",
        "developer": "Sublime HQ",
        "pricing": "Paid ($99 evaluation allowed)",
        "pricing_type": "Paid",
        "category": "Lightweight Text & Code Editor",
        "primary_use": "Fast Scripting, Web Development, C/C++ Editing",
        "key_features": [
            "GPU rendering engine for ultra-smooth UI scrolling",
            "Multiple selection and simultaneous edits",
            "Goto Anything instant file navigation (Cmd+P)",
            "Package Control plugin manager"
        ],
        "pros": [
            "Instantaneous file loading even for massive multi-gigabyte log files",
            "Very light on system CPU and memory usage",
            "Cross-platform support (macOS, Windows, Linux)"
        ],
        "cons": [
            "Paid license required for continuous commercial use",
            "Lacks built-in terminal and full IDE out-of-the-box features without plugins"
        ],
        "target_audience": "Developers seeking a blazingly fast, lightweight code editor for everyday scripting."
    },
    {
        "id": "replit",
        "name": "Replit",
        "developer": "Replit Inc.",
        "pricing": "Freemium ($12-$25/mo Core)",
        "pricing_type": "Freemium",
        "category": "Cloud-Based Collaborative IDE",
        "primary_use": "Browser Coding, Prototyping, Instant Cloud Hosting",
        "key_features": [
            "Instant browser-based environment with zero local setup",
            "Replit AI Agent for full app prototyping from text prompts",
            "Instant cloud deployment and database provisioning",
            "Multiplayer real-time editing"
        ],
        "pros": [
            "Zero local environment installation required",
            "Ideal for rapid prototyping and classroom collaboration",
            "Integrated deployment and database backend"
        ],
        "cons": [
            "Dependent on stable internet connection",
            "Resource limits on free computing tier"
        ],
        "target_audience": "Beginners, educators, hackathon teams, and rapid cloud prototypers."
    }
]

def load_history(history_path: str = "content/history.json") -> Dict[str, Any]:
    if os.path.exists(history_path):
        try:
            with open(history_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {"covered_ids": [], "runs": []}

def save_history(history_data: Dict[str, Any], history_path: str = "content/history.json"):
    os.makedirs(os.path.dirname(history_path), exist_ok=True)
    with open(history_path, "w", encoding="utf-8") as f:
        json.dump(history_data, f, indent=2)

def select_daily_ides(history: Dict[str, Any], count: int = 3) -> List[Dict[str, Any]]:
    covered = set(history.get("covered_ids", []))
    available = [ide for ide in IDE_DATABASE if ide["id"] not in covered]

    # If not enough unvisited IDEs remain, reset the covered list pool
    if len(available) < count:
        history["covered_ids"] = []
        covered = set()
        available = IDE_DATABASE[:]

    selected = available[:count]
    for ide in selected:
        history.setdefault("covered_ids", []).append(ide["id"])
    return selected

def build_amp_html(ide: Dict[str, Any]) -> str:
    pros_html = "\n".join([f"      <li>{pro}</li>" for pro in ide["pros"]])
    cons_html = "\n".join([f"      <li>{con}</li>" for con in ide["cons"]])
    features_html = "\n".join([f"      <li><strong>Feature:</strong> {feat}</li>" for feat in ide["key_features"]])

    return f"""<!doctype html>
<html ⚡ lang="en">
<head>
  <meta charset="utf-8">
  <title>{ide['name']} Review: Pros, Cons & Verdict | IDE Guide</title>
  <link rel="canonical" href="https://ideguide.blogspot.com/{ide['id']}-review.html">
  <meta name="viewport" content="width=device-width,minimum-scale=1,initial-scale=1">
  <style amp-boilerplate>body{{-webkit-animation:-amp-start 8s steps(1,end) 0s 1 normal both;-moz-animation:-amp-start 8s steps(1,end) 0s 1 normal both;-ms-animation:-amp-start 8s steps(1,end) 0s 1 normal both;animation:-amp-start 8s steps(1,end) 0s 1 normal both}}@-webkit-keyframes -amp-start{{from{{visibility:hidden}}to{{visibility:visible}}}}@-moz-keyframes -amp-start{{from{{visibility:hidden}}to{{visibility:visible}}}}@-ms-keyframes -amp-start{{from{{visibility:hidden}}to{{visibility:visible}}}}@-o-keyframes -amp-start{{from{{visibility:hidden}}to{{visibility:visible}}}}@keyframes -amp-start{{from{{visibility:hidden}}to{{visibility:visible}}}}</style><noscript><style amp-boilerplate>body{{-webkit-animation:none;-moz-animation:none;-ms-animation:none;animation:none}}</style></noscript>
  <style amp-custom>
    body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; line-height: 1.6; color: #1a1a1a; padding: 15px; max-width: 800px; margin: 0 auto; }}
    h1 {{ color: #0f172a; border-bottom: 2px solid #3b82f6; padding-bottom: 8px; font-size: 1.8rem; }}
    h2 {{ color: #1e293b; margin-top: 24px; font-size: 1.4rem; }}
    h3 {{ color: #334155; font-size: 1.1rem; }}
    ul {{ padding-left: 20px; }}
    li {{ margin-bottom: 8px; }}
    .badge {{ display: inline-block; background: #e0f2fe; color: #0369a1; padding: 4px 8px; border-radius: 4px; font-size: 0.85rem; font-weight: bold; margin-bottom: 12px; }}
    .disclaimer-box {{ background: #f8fafc; border-left: 4px solid #64748b; padding: 12px 16px; margin-top: 30px; font-size: 0.9rem; color: #475569; font-style: italic; }}
  </style>
</head>
<body>
  <article class="ide-review">
    <header>
      <span class="badge">{ide['category']} | {ide['pricing_type']}</span>
      <h1>{ide['name']} Review: Features, Pricing, Pros & Cons</h1>
      <p><em>Developer: {ide['developer']} | Primary Target: {ide['primary_use']}</em></p>
    </header>

    <section class="overview">
      <h2>Overview</h2>
      <p>{ide['name']} is a prominent solution developed by {ide['developer']}. It targets software engineers working on {ide['primary_use']}. In this independent review, IDE Guide evaluates its architecture, developer experience, and cost structure.</p>
    </section>

    <section class="features">
      <h2>Key Features & Capabilities</h2>
      <ul>
{features_html}
      </ul>
    </section>

    <section class="pros-cons">
      <h2>Pros & Cons</h2>
      <h3>Pros</h3>
      <ul>
{pros_html}
      </ul>
      <h3>Cons</h3>
      <ul>
{cons_html}
      </ul>
    </section>

    <section class="pricing">
      <h2>Pricing Model: Free vs Paid</h2>
      <p><strong>Pricing Structure:</strong> {ide['pricing']}</p>
      <p>Understanding licensing cost is critical when selecting developer tooling. {ide['name']} falls under the <strong>{ide['pricing_type']}</strong> category.</p>
    </section>

    <section class="verdict">
      <h2>Verdict: Who Should Use {ide['name']}?</h2>
      <p>{ide['target_audience']}</p>
    </section>

    <footer class="disclaimer-box">
      <p>{MANDATORY_DISCLAIMER_PHRASE}</p>
    </footer>
  </article>
</body>
</html>
"""

def build_google_flow_spec(ide: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "title": f"{ide['name']} Deep Dive: Features, Pros & Cons Review",
        "ide_id": ide["id"],
        "ide_name": ide["name"],
        "developer": ide["developer"],
        "aspect_ratio": "16:9",
        "target_platform": "YouTube / YouTube Shorts",
        "channel": "@IDEguide",
        "disclaimer": MANDATORY_DISCLAIMER_PHRASE,
        "scenes": [
            {
                "scene_id": 1,
                "duration_seconds": 5,
                "visual_prompt": f"Cinematic dark mode developer studio desk showing {ide['name']} open on a high-res curved OLED display with vibrant syntax highlighting.",
                "camera_framing": "Medium Shot",
                "camera_movement": "Slow smooth push-in dolly towards code cursor",
                "lighting_and_mood": "Cyberpunk neon accents with soft ambient blue lighting",
                "voiceover_script": f"Welcome to IDE Guide! Today we take an in-depth, objective look at {ide['name']} by {ide['developer']}.",
                "on_screen_text": f"{ide['name']} Review | IDE Guide"
            },
            {
                "scene_id": 2,
                "duration_seconds": 8,
                "visual_prompt": f"Close-up screen view showcasing top features of {ide['name']}: {ide['key_features'][0]}.",
                "camera_framing": "Extreme Close-Up on code editor window",
                "camera_movement": "Horizontal pan left to right across editor sidebar",
                "lighting_and_mood": "High contrast dark mode IDE theme with glowing status bar",
                "voiceover_script": f"{ide['name']} excels in {ide['primary_use']}. Key highlights include {ide['key_features'][0]} and {ide['key_features'][1]}.",
                "on_screen_text": f"Key Capabilities | {ide['pricing_type']}"
            },
            {
                "scene_id": 3,
                "duration_seconds": 8,
                "visual_prompt": "Split screen layout showing Pros on the left green panel and Cons on the right red accent panel with modern animated checkmarks.",
                "camera_framing": "Wide Frontal Shot",
                "camera_movement": "Static clean grid view",
                "lighting_and_mood": "Clean futuristic studio lighting",
                "voiceover_script": f"On the positive side, developers praise its {ide['pros'][0]}. However, keep in mind {ide['cons'][0]}.",
                "on_screen_text": "Pros vs Cons Breakdown"
            },
            {
                "scene_id": 4,
                "duration_seconds": 6,
                "visual_prompt": f"High tech summary card showing pricing model: {ide['pricing']} and target developer audience.",
                "camera_framing": "Medium Close-Up",
                "camera_movement": "Slow pull-out reveal",
                "lighting_and_mood": "Sleek metallic and ambient LED backdrop",
                "voiceover_script": f"Pricing is {ide['pricing']}. Is it right for you? {ide['target_audience']}",
                "on_screen_text": f"Verdict: {ide['pricing_type']}"
            },
            {
                "scene_id": 5,
                "duration_seconds": 4,
                "visual_prompt": "Outro screen with IDE Guide logo, Subscribe button graphic, and disclaimers.",
                "camera_framing": "Centered Logo View",
                "camera_movement": "Stationary centered view with subtle logo glow pulsation",
                "lighting_and_mood": "Deep dark slate background with neon accent text",
                "voiceover_script": "IDE Guide is an independent technical publication. Subscribe for daily objective code editor reviews!",
                "on_screen_text": "Subscribe to @IDEguide | ideguide.blogspot.com"
            }
        ]
    }

def generate_daily_content(output_dir: str = None) -> List[str]:
    today_str = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d")
    if output_dir is None:
        output_dir = os.path.join("content", today_str)

    os.makedirs(output_dir, exist_ok=True)

    history = load_history()
    selected_ides = select_daily_ides(history, count=3)

    generated_files = []
    run_entry = {
        "date": today_str,
        "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "generated_items": []
    }

    for ide in selected_ides:
        # Generate AMP Blog Post
        blog_html = build_amp_html(ide)
        blog_filename = f"{ide['id']}_blog_post.html"
        blog_path = os.path.join(output_dir, blog_filename)
        with open(blog_path, "w", encoding="utf-8") as f:
            f.write(blog_html)
        generated_files.append(blog_path)

        # Generate Google Flow Video Spec
        video_spec = build_google_flow_spec(ide)
        spec_filename = f"{ide['id']}_google_flow_spec.json"
        spec_path = os.path.join(output_dir, spec_filename)
        with open(spec_path, "w", encoding="utf-8") as f:
            json.dump(video_spec, f, indent=2)
        generated_files.append(spec_path)

        run_entry["generated_items"].append({
            "ide_id": ide["id"],
            "ide_name": ide["name"],
            "blog_post": blog_path,
            "google_flow_spec": spec_path
        })

    history.setdefault("runs", []).append(run_entry)
    save_history(history)

    print(f"Daily content generated successfully for {today_str} in '{output_dir}'.")
    for filepath in generated_files:
        print(f"  - {filepath}")

    return generated_files

if __name__ == "__main__":
    generate_daily_content()
