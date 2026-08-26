#!/usr/bin/env python3
"""
Daily Automated IDE & Code Editor Content Generator for IDE Guide.
Generates AMP-compliant blog posts and Google Flow video generation packages.
"""

import argparse
import datetime
import os
import sys

# Catalog of editors to cycle through or pick dynamically
EDITOR_DATABASE = [
    {
        "name": "Cursor",
        "tagline": "The AI-First Code Editor Built for Speed",
        "pricing": "Freemium ($20/mo Pro)",
        "tech_stack": "TypeScript, Python, C++, Web, Multi-language",
        "platforms": "macOS, Linux, Windows",
        "overview": "Cursor is a fork of VS Code engineered from the ground up to integrate AI models deeply into the editing workflow. It features inline code generation, terminal agent commands, and repository-wide codebase indexing.",
        "key_features": [
            "Cmd+K Inline Editing for instant refactoring",
            "Full-repo context retrieval with local embeddings",
            "Multi-file editing capabilities via Cursor Composer",
            "Drop-in VS Code extension and keybinding compatibility"
        ],
        "getting_started": [
            "Download and install Cursor from official build releases.",
            "Import your existing VS Code settings and extensions in one click.",
            "Configure your API keys or activate Cursor Pro for native Claude 3.5 Sonnet & GPT-4o access.",
            "Press `Cmd+K` (or `Ctrl+K`) in any file to generate or edit code using natural language."
        ],
        "pricing_breakdown": "Cursor offers a generous Hobby tier with limited GPT-4/Claude usages per month. The Pro tier ($20/month) unlocks unlimited fast requests and expanded context windows.",
        "verdict": "Ideal for developers seeking cutting-edge AI assistance without abandoning their familiar VS Code extension ecosystem.",
        "hooks": "Is Cursor really replacing VS Code? Here's why developers are switching in 2026!",
    },
    {
        "name": "Zed",
        "tagline": "High-Performance Rust-Based Code Editor",
        "pricing": "Free & Open Source",
        "tech_stack": "Rust, C++, Web Development, Systems Programming",
        "platforms": "macOS, Linux (Windows in preview)",
        "overview": "Zed is a high-performance, multiplayer code editor written in Rust by the creators of Atom and Tree-sitter. Designed to leverage multi-core CPUs and GPU acceleration, Zed renders text at ultra-fast 120 FPS.",
        "key_features": [
            "GPU-accelerated rendering engine for sub-millisecond latency",
            "Built-in multiplayer pair programming and audio sharing",
            "Native Language Server Protocol (LSP) integration out of the box",
            "Minimalist UI with integrated inline AI assistant support"
        ],
        "getting_started": [
            "Install Zed via package manager or direct download (`curl -f https://zed.dev/install.sh | sh`).",
            "Open your project directory (`zed .`).",
            "Configure `settings.json` for keybindings, language servers, and theme customization.",
            "Use `Cmd+Shift+C` to start a collaborative coding session with team members."
        ],
        "pricing_breakdown": "Zed is completely free and open source under GPL/AGPL/Apache licenses. Optional paid cloud features for enterprise team collaboration are available.",
        "verdict": "Best for performance purists and systems developers who want instant startup times and smooth 120fps editing.",
        "hooks": "This Rust-powered editor opens instantly and renders at 120 FPS. Meet Zed!",
    },
    {
        "name": "Helix",
        "tagline": "Post-Modern Modal Text Editor in Rust",
        "pricing": "Free & Open Source",
        "tech_stack": "Rust, Systems, Command-line, Polyglot",
        "platforms": "Linux, macOS, Windows, Terminal",
        "overview": "Helix is a terminal-based modal text editor inspired by Neovim and Kakoune. Written in Rust, it comes with zero-config LSP support, tree-sitter syntax highlighting, and selection-first editing built right in.",
        "key_features": [
            "Selection-first modal editing (manipulate selections before running actions)",
            "Built-in Language Server Protocol (LSP) support with zero plugin config required",
            "Tree-sitter integration for fast syntax tree navigation and structural editing",
            "Pure terminal application with truecolor and mouse support"
        ],
        "getting_started": [
            "Install Helix via homebrew (`brew install helix`) or cargo (`cargo install --path helix-term`).",
            "Run `hx --health` to verify language server dependencies for your active languages.",
            "Launch Helix in any directory (`hx .`).",
            "Run through the built-in interactive tutor by typing `hx --tutor`."
        ],
        "pricing_breakdown": "Helix is 100% free and open source released under the MPL-2.0 license.",
        "verdict": "Perfect for terminal enthusiasts who want modern features like LSP and Tree-sitter without managing complex plugin configurations.",
        "hooks": "Tired of configuring Vim plugins? Helix gives you modern terminal editing out of the box!",
    },
    {
        "name": "Neovim",
        "tagline": "Hyperextensible Vim-based Text Editor",
        "pricing": "Free & Open Source",
        "tech_stack": "Lua, C, Polyglot",
        "platforms": "Linux, macOS, Windows, BSD",
        "overview": "Neovim is an extension of Vim seeking to aggressively refactor and expand Vim's feature set. Powered by Lua scripting, native LSP, and async jobs, Neovim allows developers to build fully customized IDE experiences inside the terminal.",
        "key_features": [
            "First-class Lua API for plugin creation and user configuration",
            "Embedded asynchronous terminal emulator",
            "Built-in Language Server Protocol framework",
            "Massive ecosystem of community-maintained plugins and starter distros (LazyVim, NvChad)"
        ],
        "getting_started": [
            "Install Neovim via system package manager (`brew install neovim` or `sudo apt install neovim`).",
            "Initialize your Lua configuration in `~/.config/nvim/init.lua`.",
            "Install a modern plugin manager such as `lazy.nvim` to manage extensions.",
            "Run `nvim` and use `:checkhealth` to inspect your development toolchain."
        ],
        "pricing_breakdown": "Neovim is completely free and open source under the Apache 2.0 and Vim licenses.",
        "verdict": "The ultimate editor for developers who demand complete control over every keystroke, configuration line, and keymap.",
        "hooks": "Why modern developers are turning Neovim into the ultimate lightning-fast IDE!",
    },
    {
        "name": "JetBrains Fleet",
        "tagline": "Next-Generation Lightweight Distributed IDE",
        "pricing": "Freemium",
        "tech_stack": "Kotlin, Java, Python, Rust, Go, JavaScript",
        "platforms": "macOS, Windows, Linux",
        "overview": "JetBrains Fleet is a lightweight editor built from scratch using JetBrains' decades of IDE expertise. It combines a fast, minimalist text editor mode with full IntelliJ code intelligence engines when expanded.",
        "key_features": [
            "Dual mode: instant lightweight editor or full smart IDE mode",
            "Distributed architecture supporting remote dev, containers, and cloud environments",
            "Native multi-language code intelligence and refactoring",
            "Built-in collaborative space for remote pair programming"
        ],
        "getting_started": [
            "Install JetBrains Fleet via JetBrains Toolbox App.",
            "Launch Fleet and open any repository folder instantly.",
            "Toggle 'Smart Mode' to enable full Kotlin/Java/Python language engine support.",
            "Invite remote collaborators directly via shareable session links."
        ],
        "pricing_breakdown": "Free during preview stages; commercial licensing and subscription options integrated into JetBrains All Products Pack.",
        "verdict": "Great for developers who love JetBrains code intelligence but want a lightweight, quick-starting environment for daily tasks.",
        "hooks": "JetBrains built a lightweight competitor to VS Code. Is Fleet ready for prime time?",
    },
    {
        "name": "Lapce",
        "tagline": "Lightning-Fast Rust GUI Code Editor",
        "pricing": "Free & Open Source",
        "tech_stack": "Rust, WebAssembly, C++",
        "platforms": "Linux, macOS, Windows",
        "overview": "Lapce is an open-source code editor written in Rust with UI rendered using Druid. Designed with native speed and remote development in mind, Lapce features WASM plugin extensions and Modal editing.",
        "key_features": [
            "Native GUI rendering in Rust for lightning responsiveness",
            "WASM-based plugin architecture for isolated and safe extensions",
            "Built-in remote development over SSH",
            "Vim-like modal editing mode natively supported"
        ],
        "getting_started": [
            "Download binary releases or build via `cargo install lapce`.",
            "Launch `lapce` from terminal or application launcher.",
            "Browse and install WASM plugins directly from the embedded marketplace.",
            "Connect seamlessly to remote servers over SSH from the connection bar."
        ],
        "pricing_breakdown": "100% Free and open source under Apache-2.0 license.",
        "verdict": "An exciting Rust GUI editor for users looking for native speed without sacrificing visual UI components.",
        "hooks": "Native Rust GUI and WebAssembly plugins? Lapce might be the future of fast editors!",
    }
]

DISCLAIMER_TEXT = (
    "Disclaimer: IDE Guide is an independent technical publication. "
    "This content is not sponsored, endorsed, or affiliated with any software vendor "
    "or editor developer mentioned above. All reviews and assessments are based strictly "
    "on objective developer evaluation."
)


def generate_amp_blog_post(editor):
    features_html = "".join([f"<li>{feat}</li>" for feat in editor["key_features"]])
    getting_started_html = "".join([f"<li>{step}</li>" for step in editor["getting_started"]])

    html_content = f"""<article class="ide-guide-post">
<header>
  <h1>{editor['name']}: {editor['tagline']}</h1>
  <section class="metadata">
    <p><strong>Pricing:</strong> {editor['pricing']}</p>
    <p><strong>Primary Tech Stack:</strong> {editor['tech_stack']}</p>
    <p><strong>Platform Support:</strong> {editor['platforms']}</p>
  </section>
</header>

<section class="overview">
  <h2>Overview &amp; Why Use It</h2>
  <p>{editor['overview']}</p>
</section>

<section class="features">
  <h2>Key Features &amp; Language Ecosystem</h2>
  <ul>
    {features_html}
  </ul>
</section>

<section class="getting-started">
  <h2>How to Get Started</h2>
  <ol>
    {getting_started_html}
  </ol>
</section>

<section class="pricing-breakdown">
  <h2>Free vs. Paid Breakdown</h2>
  <p>{editor['pricing_breakdown']}</p>
</section>

<section class="verdict">
  <h2>Verdict &amp; Best Use Cases</h2>
  <p>{editor['verdict']}</p>
</section>

<footer class="disclaimer-footer">
  <p><em>{DISCLAIMER_TEXT}</em></p>
</footer>
</article>"""
    return html_content


def generate_google_flow_spec(editor):
    shorts_spec = f"""### Short-Form Video Spec (YouTube Shorts / 60s)

**Hook (0-3s):**
"{editor['hooks']}"

**Google Flow Visual Prompts (Scene-by-Scene):**
1. **Scene 1 (Hook 0-5s):** Close-up macro 45-degree shot of high-contrast editor UI on glowing dark background, fast terminal text stream, ambient purple neon rim lighting, cinematic 4K 60fps render.
2. **Scene 2 (Core Demo 5-25s):** Smooth camera push-in showing active code auto-completion and key feature highlights for {editor['name']}, dark mode developer environment, soft bokeh background office setup.
3. **Scene 3 (Workflow 25-45s):** Fast-paced UI interaction showing command palette and fast keyboard shortcuts in action, minimalist high-tech aesthetic, subtle lens flare.
4. **Scene 4 (CTA / Outro 45-60s):** Clean animated title card displaying "{editor['name']}: {editor['tagline']}", dark cyber theme, floating code snippets, ending on IDE Guide watermark.

**Voiceover Script (60 Seconds):**
"Looking for a game-changing code editor? Meet {editor['name']} — {editor['tagline'].lower()}. {editor['overview']} Key highlights include {editor['key_features'][0].lower()} and {editor['key_features'][1].lower()}. Whether you are working with {editor['tech_stack']}, {editor['name']} delivers unmatched developer experience. Check out our full review on IDE Guide!"

**Video Description & Disclaimer:**
Explore {editor['name']} ({editor['pricing']}). Platform support: {editor['platforms']}.

{DISCLAIMER_TEXT}"""

    longform_spec = f"""### Full-Length Video Spec (YouTube Long-Form / 3-5 Mins)

**Video Outline & Timestamps:**
- 00:00 - Introduction & Key Takeaways
- 00:45 - Overview & Core Architecture
- 01:45 - Standout Features & Workflow Efficiency
- 03:00 - Installation & Setup Guide
- 04:00 - Licensing, Pricing & Final Verdict

**Google Flow Visual Prompts (Background & Scenes):**
1. **Intro Chapter (00:00 - 00:45):** Cinematic wide shot of futuristic developer workstation with dark ambient neon lighting, smooth overhead tracking shot onto high-resolution display displaying {editor['name']}.
2. **Architecture & Features (00:45 - 03:00):** High-tech 3D motion graphic visualization showing code execution flow, LSP language servers connecting to {editor['name']}, GPU rendering pipeline graphics in crisp neon vector aesthetic.
3. **Hands-on Setup (03:00 - 04:00):** Screen capture style render showing terminal installation commands and instant configuration loading, soft studio lighting contrast.
4. **Verdict & Outro (04:00 - 05:00):** Minimalist summary card showing Pros & Cons breakdown, smooth camera zoom-out returning to studio desk environment with IDE Guide branding.

**Voiceover Script (3-5 Minutes Full Script):**
"Welcome back to IDE Guide. Today we're diving deep into {editor['name']} — {editor['tagline']}.

In this review, we cover everything you need to know about {editor['name']}, from its performance characteristics to platform availability across {editor['platforms']}.

{editor['overview']}

Let's break down the key features. First, {editor['key_features'][0]}. Second, {editor['key_features'][1]}. Third, {editor['key_features'][2]}.

For pricing, {editor['pricing_breakdown']}

Our verdict: {editor['verdict']}

If you found this breakdown helpful, hit subscribe to IDE Guide for daily editor reviews and dev tool updates."

**Video Description & Disclaimer:**
Full technical review of {editor['name']}.

{DISCLAIMER_TEXT}"""

    return f"{shorts_spec}\n\n---\n\n{longform_spec}"


def select_editors_for_date(date_obj, count=3):
    """Dynamically rotates through the editor database based on the day of year."""
    day_of_year = date_obj.timetuple().tm_yday
    num_editors = len(EDITOR_DATABASE)
    start_index = ((day_of_year - 1) * count) % num_editors

    selected = []
    for i in range(count):
        idx = (start_index + i) % num_editors
        selected.append(EDITOR_DATABASE[idx])
    return selected


def generate_daily_package(date_str=None, count=3):
    if date_str:
        dt = datetime.datetime.strptime(date_str, "%Y-%m-%d").replace(tzinfo=datetime.timezone.utc)
    else:
        dt = datetime.datetime.now(datetime.timezone.utc)
        date_str = dt.strftime("%Y-%m-%d")

    target_dir = os.path.join("content", date_str)
    os.makedirs(target_dir, exist_ok=True)

    selected_editors = select_editors_for_date(dt, count=count)

    readme_content = f"# IDE Guide Daily Package - {date_str}\n\n"
    readme_content += f"Generated content package for {count} editors scheduled for publishing on {date_str}.\n\n"
    readme_content += "## Included Editors:\n"

    for idx, editor in enumerate(selected_editors, 1):
        slug = editor['name'].lower().replace(" ", "-")
        blog_filename = f"{idx:02d}-{slug}-amp-blog.html"
        video_filename = f"{idx:02d}-{slug}-google-flow-spec.md"

        blog_path = os.path.join(target_dir, blog_filename)
        video_path = os.path.join(target_dir, video_filename)

        blog_html = generate_amp_blog_post(editor)
        flow_spec = generate_google_flow_spec(editor)

        with open(blog_path, "w", encoding="utf-8") as f:
            f.write(blog_html)

        with open(video_path, "w", encoding="utf-8") as f:
            f.write(flow_spec)

        readme_content += f"{idx}. **{editor['name']}**: [{blog_filename}](./{blog_filename}) | [{video_filename}](./{video_filename})\n"

    readme_path = os.path.join(target_dir, "README.md")
    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(readme_content)

    print(f"Successfully generated package for {date_str} with editors: {[e['name'] for e in selected_editors]}")


def main():
    parser = argparse.ArgumentParser(description="Generate daily IDE Guide publishing package.")
    parser.add_argument("--date", type=str, help="Target date in YYYY-MM-DD format", default=None)
    parser.add_argument("--count", type=int, help="Number of editors to generate", default=3)
    args = parser.parse_args()

    generate_daily_package(date_str=args.date, count=args.count)


if __name__ == "__main__":
    main()
