"""Comprehensive IDE and Code Editor Database for IDE Guide.

Contains rich metadata on modern code editors, integrated development environments,
pricing models, pros, cons, target audiences, and visual descriptors for Google Flow.
"""

from typing import Dict, Any, List

IDE_CATALOG: Dict[str, Dict[str, Any]] = {
    "Cursor": {
        "name": "Cursor",
        "tagline": "The AI-First Code Editor Built on VS Code",
        "category": "AI Code Editor",
        "pricing_model": "Freemium",
        "pricing_details": "Free tier with 2,000 completions and 50 slow premium requests; Pro tier at $20/month; Business tier at $40/seat/month.",
        "is_paid": True,
        "has_free_tier": True,
        "is_open_source": False,
        "official_url": "https://www.cursor.com",
        "pros": [
            "Native multi-file AI codebase indexing and context awareness",
            "Composer mode allows rapid full-stack scaffolding and autonomous multi-file edits",
            "Drop-in compatibility with the entire VS Code extension ecosystem and keybindings",
            "Cursor Tab offers intelligent multi-character and next-action autocomplete"
        ],
        "cons": [
            "Proprietary fork of VS Code with cloud dependency for flagship LLM models",
            "Subscription cost ($20/mo) can become steep for hobbyists or students",
            "Occasional privacy and enterprise governance concerns when sending proprietary code upstream",
            "Performance hits during large codebase indexing"
        ],
        "best_for": "Developers seeking state-of-the-art AI pair programming and fast multi-file refactoring without leaving VS Code shortcuts.",
        "visual_theme": "Modern cyberpunk neon teal accents on charcoal gray editor, glowing prompt bar, AI generation diff highlights",
        "flow_broll_prompt": "Cinematic slow dolly forward towards a dual-monitor dark coding setup showing Cursor AI composer generating React components simultaneously across multiple files with emerald green and cyan diff lines."
    },
    "Visual Studio Code": {
        "name": "Visual Studio Code (VS Code)",
        "tagline": "The Industry Standard Extensible Code Editor",
        "category": "General Purpose Code Editor",
        "pricing_model": "Free / Open Core",
        "pricing_details": "Completely free binaries distributed by Microsoft; core source available under MIT as VSCodium.",
        "is_paid": False,
        "has_free_tier": True,
        "is_open_source": True,
        "official_url": "https://code.visualstudio.com",
        "pros": [
            "Massive global ecosystem with tens of thousands of extensions and themes",
            "Exceptional remote development via SSH, Dev Containers, and WSL",
            "Consistent monthly updates, stellar stability, and active community backing",
            "Highly customizable keybindings, settings sync, and workspace profiles"
        ],
        "cons": [
            "Default official build includes Microsoft telemetry and proprietary marketplace licensing",
            "Electron overhead can consume significant RAM with many extensions installed",
            "Out-of-the-box experience requires manual extension configuration for specific language toolchains",
            "Can feel cluttered when overloaded with dozens of plugins"
        ],
        "best_for": "Web, cloud, and polyglot developers wanting maximum flexibility, extensive tooling, and community support.",
        "visual_theme": "Clean classic VS Code dark modern theme with blue status bar, rich syntax highlighting and active sidebar",
        "flow_broll_prompt": "Over-the-shoulder shot of a modern engineer navigating a complex TypeScript project in VS Code with seamless extension sidebar and integrated debugger panels active."
    },
    "Zed": {
        "name": "Zed",
        "tagline": "High-Performance Multiplayer Code Editor Written in Rust",
        "category": "High Performance Editor",
        "pricing_model": "Free / Open Source",
        "pricing_details": "100% Free and Open Source (GPL/Apache 2.0); optional hosted AI model proxy features with pay-per-token or bring-your-own-key.",
        "is_paid": False,
        "has_free_tier": True,
        "is_open_source": True,
        "official_url": "https://zed.dev",
        "pros": [
            "Engineered in Rust with GPU-accelerated rendering for instantaneous startup and zero keystroke latency",
            "Native real-time collaborative editing (multiplayer pairing) without third-party plugins",
            "Built-in semantic code search and integrated LLM assistant panels",
            "Extremely low memory footprint compared to Electron-based editors"
        ],
        "cons": [
            "Extension ecosystem is still young and catching up to VS Code",
            "Historically focused on macOS, with Linux and Windows support in active rollout",
            "Fewer niche language debuggers and GUI profiling tools available",
            "Configuration relies heavily on JSON and keyboard shortcuts rather than graphical menus"
        ],
        "best_for": "Developers who prioritize raw editing speed, instantaneous responsiveness, and minimal system resource consumption.",
        "visual_theme": "Minimalist sleek gray theme, zero-bloat UI, ultra-crisp GPU typography, subtle collaborative user avatars",
        "flow_broll_prompt": "Ultra-smooth 60fps tracking shot of text editing in Zed with buttery smooth cursor animations and zero latency typing under soft studio lighting."
    },
    "Windsurf": {
        "name": "Windsurf",
        "tagline": "The Agentic IDE by Codeium with Flows and Deep Context",
        "category": "AI Code Editor",
        "pricing_model": "Freemium",
        "pricing_details": "Generous free tier with Cascade AI agent; Pro tier at $15/month for unlimited advanced models and priority routing.",
        "is_paid": True,
        "has_free_tier": True,
        "is_open_source": False,
        "official_url": "https://codeium.com/windsurf",
        "pros": [
            "Innovative 'Cascade' agent that collaborates bidirectionally with the developer in real time",
            "Deep context awareness tracking user edits, terminal commands, and file changes automatically",
            "Lower monthly price ($15/mo) compared to traditional competitors",
            "Seamless compatibility with VS Code extensions and settings"
        ],
        "cons": [
            "Relatively newer entry in the agentic IDE space with evolving feature parity",
            "Requires internet connectivity for proprietary Codeium cloud reasoning backend",
            "Can occasionally suggest overly eager file changes without explicit confirmation prompts",
            "Telemetry and cloud processing requirements for full agent abilities"
        ],
        "best_for": "Developers seeking an intelligent AI companion that actively understands their workflow in terminal and editor simultaneously.",
        "visual_theme": "Ocean wave teal and deep obsidian palette, interactive Cascade chat drawer, animated thought-process indicators",
        "flow_broll_prompt": "Cinematic close-up of a developer interacting with the Windsurf Cascade panel, visual terminal commands executing autonomously with emerald status ticks."
    },
    "JetBrains IntelliJ IDEA": {
        "name": "JetBrains IntelliJ IDEA",
        "tagline": "The Capable & Ergonomic Java and Kotlin IDE",
        "category": "Full Integrated Development Environment",
        "pricing_model": "Commercial / Freemium (Community Edition)",
        "pricing_details": "Community Edition is free and open-source (Apache 2.0); Ultimate Edition starts at $16.90/month or $169/first year.",
        "is_paid": True,
        "has_free_tier": True,
        "is_open_source": True,
        "official_url": "https://www.jetbrains.com/idea/",
        "pros": [
            "Unrivaled static code analysis, refactoring safety, and deep language understanding for JVM stacks",
            "Industry-leading built-in database tools, Git client, profiler, and enterprise framework support",
            "Consistent experience across all JetBrains ecosystem IDEs",
            "Integrated JetBrains AI Assistant with local and cloud models"
        ],
        "cons": [
            "High RAM and CPU usage, especially during initial project indexing",
            "Ultimate Edition requires a paid commercial license for enterprise Java/Spring and web frameworks",
            "Slower startup time compared to lightweight code editors",
            "Complex interface with a steep learning curve for beginner developers"
        ],
        "best_for": "Enterprise Java, Kotlin, Spring, and full-stack enterprise engineers who value robust refactoring and deep code inspections.",
        "visual_theme": "JetBrains Darcula or New UI with crisp icons, deep purple and blue accents, rich structural inspection gutter",
        "flow_broll_prompt": "Wide studio camera panning slowly over an enterprise developer station showcasing IntelliJ IDEA performing complex architectural refactoring across microservices."
    },
    "JetBrains PyCharm": {
        "name": "JetBrains PyCharm",
        "tagline": "The Dedicated Python IDE for Professional Developers",
        "category": "Full Integrated Development Environment",
        "pricing_model": "Commercial / Freemium (Community Edition)",
        "pricing_details": "Community Edition is free for pure Python; Professional Edition starts at $10.90/month or $109/first year.",
        "is_paid": True,
        "has_free_tier": True,
        "is_open_source": True,
        "official_url": "https://www.jetbrains.com/pycharm/",
        "pros": [
            "World-class Python code completion, visual debugger, and testing runner",
            "First-class support for scientific computing, Jupyter notebooks, and Pandas dataframe viewers in Pro",
            "Built-in support for Django, FastAPI, Flask, and SQL databases in Professional Edition",
            "Virtual environment, Poetry, Conda, and Docker remote interpreter integration"
        ],
        "cons": [
            "Heavy memory footprint on machines with under 16GB RAM",
            "Community Edition lacks web frameworks and database tools",
            "Can feel sluggish when opening single standalone script files",
            "Indexing large virtual environments can pause or slow down editor performance"
        ],
        "best_for": "Python developers, data scientists, and backend engineers building complex Python APIs and machine learning models.",
        "visual_theme": "Pythonic green and amber status accents, interactive scientific mode data tables, clean dark theme",
        "flow_broll_prompt": "Dynamic focus pull from a glowing mechanical keyboard to PyCharm scientific view inspecting high-dimensional Pandas arrays with interactive 3D plots."
    },
    "Neovim": {
        "name": "Neovim",
        "tagline": "Hyperextensible Vim-Based Text Editor Built for Speed",
        "category": "Terminal Modal Editor",
        "pricing_model": "Free / Open Source",
        "pricing_details": "100% Free and Open Source (Apache 2.0 / Vim license).",
        "is_paid": False,
        "has_free_tier": True,
        "is_open_source": True,
        "official_url": "https://neovim.io",
        "pros": [
            "Instantaneous launch speed with virtually undetectable memory footprint (often under 50MB)",
            "Extensible via modern Lua scripting, enabling custom developer environments (IDE-level configs via AstroNvim/LazyVim)",
            "Modal editing paradigms offer unparalleled keyboard-driven velocity",
            "Runs natively over SSH, tmux, and low-spec remote headless environments"
        ],
        "cons": [
            "Extremely steep learning curve for non-modal editor users",
            "Requires substantial upfront investment in configuration and Lua plugins",
            "No out-of-the-box GUI controls, file dialogs, or mouse-driven menus",
            "Plugin breaking changes during major API updates"
        ],
        "best_for": "Keyboard purists, terminal lovers, systems programmers, and developers who refuse to touch a mouse.",
        "visual_theme": "Terminal monochrome or Gruvbox/Catppuccin color scheme, ASCII status line, blazing fast floating diagnostics",
        "flow_broll_prompt": "High-contrast cinematic macro shot of hands flying across an ergonomic split mechanical keyboard, terminal Neovim buffer shifting modes with green normal mode indicator."
    },
    "Helix": {
        "name": "Helix",
        "tagline": "A Post-Modern Modal Text Editor Written in Rust",
        "category": "Terminal Modal Editor",
        "pricing_model": "Free / Open Source",
        "pricing_details": "100% Free and Open Source (Mozilla Public License 2.0).",
        "is_paid": False,
        "has_free_tier": True,
        "is_open_source": True,
        "official_url": "https://helix-editor.com",
        "pros": [
            "Zero configuration required: native LSP, Tree-sitter syntax highlighting, and debug adapter support out of the box",
            "Intuitive selection-first modal editing model (Kakoune-style) rather than Vim action-first model",
            "Written in Rust for exceptional speed and minuscule resource usage",
            "Modern multiple-selection system built natively into core editing"
        ],
        "cons": [
            "Plugin architecture is still in development; custom scripting is limited compared to Neovim Lua",
            "Strict terminal-only interface without native GUI frontend",
            "Different muscle memory for seasoned Vim users due to selection -> verb sequence",
            "Smaller plugin ecosystem"
        ],
        "best_for": "Developers wanting Neovim-like speed and modal editing without spending days writing Lua configuration files.",
        "visual_theme": "Crisp terminal pastel color scheme (Tokyo Night or Solarized Dark), minimal status badges, clean typography",
        "flow_broll_prompt": "Cinematic vertical 9:16 macro shot of a sleek command-line interface highlighting Rust code using Helix editor with instantaneous syntax jumping."
    },
    "Sublime Text": {
        "name": "Sublime Text 4",
        "tagline": "Sophisticated Text Editor for Code, Markup and Prose",
        "category": "Native Lightweight Editor",
        "pricing_model": "Paid / Nagware Trial",
        "pricing_details": "Free unconstrained trial with periodic purchase prompt; Individual license is $99 for 3 years of updates.",
        "is_paid": True,
        "has_free_tier": True,
        "is_open_source": False,
        "official_url": "https://www.sublimetext.com",
        "pros": [
            "GPU-rendered native UI with blazing fast file opening and instantaneous multi-megabyte file handling",
            "Tiny memory and battery footprint on laptops",
            "Superb multi-cursor implementation and Goto Anything navigation (`Cmd+P`)",
            "Python-based plugin API with Package Control"
        ],
        "cons": [
            "Commercial closed-source software with $99 personal license",
            "Evaluation popups can become annoying if unlicensed",
            "LSP integration requires external community package configuration rather than built-in",
            "Slower pace of new feature releases compared to web-tech editors"
        ],
        "best_for": "Developers wanting a blisteringly fast native GUI text editor that easily opens huge log files and codebases without lagging.",
        "visual_theme": "Classic Mariana dark theme, smooth mini-map scrollbar, subtle neon accents, ultra-responsive native font rendering",
        "flow_broll_prompt": "Smooth dolly shot revealing Sublime Text effortlessly scrolling through a 500,000-line code file without a single frame drop under warm studio lighting."
    },
    "Lapce": {
        "name": "Lapce",
        "tagline": "Lightning-Fast and Powerful Code Editor Built in Rust",
        "category": "Native Modern Editor",
        "pricing_model": "Free / Open Source",
        "pricing_details": "100% Free and Open Source (Apache 2.0).",
        "is_paid": False,
        "has_free_tier": True,
        "is_open_source": True,
        "official_url": "https://lapce.dev",
        "pros": [
            "Native GUI written in Rust with GPU rendering via Floem / WGPU",
            "Built-in Vim modal mode support for developers who love keyboard navigation",
            "Remote development built directly into the core design (SSH and local container)",
            "Non-blocking UI with background LSP and Tree-sitter parsing"
        ],
        "cons": [
            "Still in relatively early development phase compared to mature options",
            "Plugin ecosystem is small but growing via WASM plugins",
            "Occasional instability or missing corner-case features",
            "Documentation is sparse for custom configuration"
        ],
        "best_for": "Adventurous developers looking for an open-source, ultra-fast native Rust alternative to VS Code with built-in modal editing.",
        "visual_theme": "Dark slate minimalist interface, clean vector iconography, vibrant syntax highlighting with native OS window decoration",
        "flow_broll_prompt": "Close-up cinematic tracking shot of Lapce native editor starting up in under 100 milliseconds with clean Rust code highlighted on a 4K OLED monitor."
    },
    "Fleet": {
        "name": "JetBrains Fleet",
        "tagline": "Next-Generation Smart Polyglot IDE by JetBrains",
        "category": "Hybrid Lightweight / Full IDE",
        "pricing_model": "Freemium / In Preview",
        "pricing_details": "Currently in free public preview; will transition to tiered pricing with JetBrains All Products Pack inclusion.",
        "is_paid": False,
        "has_free_tier": True,
        "is_open_source": False,
        "official_url": "https://www.jetbrains.com/fleet/",
        "pros": [
            "Lightweight editor mode with instant startup, switchable to full JetBrains Smart Mode on demand",
            "Distributed architecture allowing execution on remote machines or clouds",
            "Built-in collaborative pair programming and clean modern typography",
            "Fleet Code Assistant with integrated AI smarts"
        ],
        "cons": [
            "Still in preview with occasional rough edges and evolving pricing",
            "Smart Mode activation requires RAM and CPU comparable to standard JetBrains IDEs",
            "Plugin ecosystem is in early rollout",
            "Closed source proprietary software"
        ],
        "best_for": "Developers who want JetBrains code intelligence without the heavyweight IDE shell when working on fast tasks.",
        "visual_theme": "Clean Nordic minimalist aesthetic, translucent glass UI elements, modern rounded fonts and elegant gutters",
        "flow_broll_prompt": "Cinematic camera sweep showing Fleet toggling between lightweight text editor mode and full Smart Mode, diagnostics lighting up like neon circuits."
    },
    "Android Studio": {
        "name": "Android Studio",
        "tagline": "The Official IDE for Android App Development",
        "category": "Mobile Development Environment",
        "pricing_model": "Free / Open Source (Based on IntelliJ)",
        "pricing_details": "100% Free official software distributed by Google.",
        "is_paid": False,
        "has_free_tier": True,
        "is_open_source": True,
        "official_url": "https://developer.android.com/studio",
        "pros": [
            "Official, fully supported development tool for Android and WearOS",
            "Interactive visual layout editor and Jetpack Compose live preview",
            "Integrated Android Virtual Device (AVD) emulator, memory profiler, and APK analyzer",
            "Gemini in Android Studio provides contextual Android code assistance"
        ],
        "cons": [
            "Resource monster: requires minimum 16GB RAM for smooth emulator and Gradle builds",
            "Gradle build sync can take noticeable time on complex multi-module projects",
            "Not suited for general web or backend non-mobile tasks",
            "Frequent large updates with heavy download sizes"
        ],
        "best_for": "Native Android, Kotlin, and Flutter developers building production mobile experiences.",
        "visual_theme": "Android green accents, visual preview split screen with interactive smartphone mockup rendering UI in real time",
        "flow_broll_prompt": "Split screen cinematic shot showing Kotlin Jetpack Compose code updating live on a virtual Android device emulator with instant hot reload."
    }
}


def get_all_ide_names() -> List[str]:
    """Return all cataloged IDE names."""
    return list(IDE_CATALOG.keys())


def get_ide_by_name(name: str) -> Dict[str, Any]:
    """Retrieve IDE details by exact or case-insensitive name match."""
    normalized = name.strip().lower()
    for key, data in IDE_CATALOG.items():
        if key.lower() == normalized or data["name"].lower() == normalized:
            return data
    raise KeyError(f"IDE '{name}' not found in catalog.")
