import json
import urllib.request
import urllib.parse
from typing import Dict, List, Any, Optional

DEFAULT_IDE_CATALOG: List[Dict[str, Any]] = [
    {
        "name": "Visual Studio Code",
        "slug": "vs-code",
        "developer": "Microsoft",
        "license_type": "Free / Open Source (Core)",
        "pricing": "Free",
        "website": "https://code.visualstudio.com",
        "github_repo": "https://github.com/microsoft/vscode",
        "description": "Powerful, extensible lightweight code editor with massive extension ecosystem and native Git/debug integration.",
        "key_features": [
            "Extensive extension marketplace with tens of thousands of extensions",
            "Built-in IntelliSense and debugging engine",
            "Seamless remote development (SSH, Containers, WSL)",
            "Integrated terminal and Git source control interface"
        ],
        "pros": [
            "Massive global community and extension ecosystem",
            "Regular monthly release cycles and constant feature enhancements",
            "Highly customizable keybindings, themes, and settings"
        ],
        "cons": [
            "Electron-based resource footprint can be heavy on modest hardware",
            "Can require extensive configuration for complex multi-language setups"
        ],
        "target_audience": "Full-stack developers, web developers, cloud engineers, and general programmers.",
        "verdict_rating": "9.5/10",
        "verdict_summary": "The undisputed industry standard editor combining lightweight feel with IDE-grade capabilities."
    },
    {
        "name": "Cursor",
        "slug": "cursor",
        "developer": "Anysphere",
        "license_type": "Freemium",
        "pricing": "Free tier / $20/mo Pro",
        "website": "https://www.cursor.com",
        "github_repo": "https://github.com/getcursor/cursor",
        "description": "An AI-first code editor built as a fork of VS Code, natively incorporating Claude 3.5 Sonnet and GPT-4o for codebase indexing and auto-edits.",
        "key_features": [
            "Native multi-file AI code generation and editing (Composer mode)",
            "Full workspace indexing for context-aware coding assistance",
            "Drop-in compatibility with VS Code extensions and settings",
            "Inline terminal error resolution and prompt-based refactoring"
        ],
        "pros": [
            "Incredible developer velocity boost through AI workspace awareness",
            "Flawless migration path for existing VS Code users",
            "Cutting-edge model routing and rapid feature delivery"
        ],
        "cons": [
            "Requires active subscription for high-volume fast model access",
            "Heavy reliance on remote cloud AI services"
        ],
        "target_audience": "Developers seeking maximum AI productivity and automated codebase navigation.",
        "verdict_rating": "9.4/10",
        "verdict_summary": "The leading AI-native code editor setting a new benchmark for software generation."
    },
    {
        "name": "Windsurf",
        "slug": "windsurf",
        "developer": "Codeium",
        "license_type": "Freemium",
        "pricing": "Free tier / $15/mo Pro",
        "website": "https://codeium.com/windsurf",
        "github_repo": "",
        "description": "An agentic AI IDE developed by Codeium featuring Flows and Cascade for autonomous multi-file development and context understanding.",
        "key_features": [
            "Cascade AI agent for deep workspace understanding and terminal execution",
            "Real-time collaborative AI interaction with state synchronization",
            "Supports VS Code extensions and familiar keybindings",
            "Advanced context pinning and semantic search engine"
        ],
        "pros": [
            "Autonomous agent capabilities that execute and test terminal commands",
            "Competitive pricing structure and generous free monthly quota",
            "Polished UI and smooth agent workflow"
        ],
        "cons": [
            "Relatively new tool with evolving edge-case capabilities",
            "Occasional context lag on extremely large mono-repositories"
        ],
        "target_audience": "Engineers looking for autonomous agentic assistance that handles end-to-end coding tasks.",
        "verdict_rating": "9.2/10",
        "verdict_summary": "A powerful agentic IDE pioneer that takes AI assistance from autocomplete to full-suite co-developer."
    },
    {
        "name": "JetBrains IntelliJ IDEA",
        "slug": "intellij-idea",
        "developer": "JetBrains",
        "license_type": "Freemium / Commercial",
        "pricing": "Community (Free) / Ultimate ($169+/yr)",
        "website": "https://www.jetbrains.com/idea/",
        "github_repo": "https://github.com/JetBrains/intellij-community",
        "description": "The gold-standard IDE for Java, Kotlin, and enterprise JVM development, renowned for deep static analysis and refactoring tools.",
        "key_features": [
            "Unrivaled Java & Kotlin static code analysis and structural refactoring",
            "Integrated database tools, framework support (Spring, Jakarta)",
            "Rich built-in debugger, profiler, and decompiler",
            "JetBrains AI Assistant integration"
        ],
        "pros": [
            "Deepest semantic code understanding in the software industry",
            "Bulletproof refactoring and navigation on massive codebases",
            "Robust enterprise framework and database tools out of the box"
        ],
        "cons": [
            "Heavy memory footprint (requires 16GB+ RAM for smooth performance)",
            "Commercial version can be expensive for individual developers"
        ],
        "target_audience": "Enterprise Java, Kotlin, Spring, and JVM software engineers.",
        "verdict_rating": "9.6/10",
        "verdict_summary": "The ultimate IDE for Java and enterprise backends where precision refactoring is mandatory."
    },
    {
        "name": "Zed",
        "slug": "zed",
        "developer": "Zed Industries",
        "license_type": "Open Source",
        "pricing": "Free",
        "website": "https://zed.dev",
        "github_repo": "https://github.com/zed-industries/zed",
        "description": "A high-performance, multi-player code editor written in Rust, leveraging GPU acceleration for lightning-fast rendering and minimal latency.",
        "key_features": [
            "GPU-accelerated metal/vulkan rendering engine operating at 120+ FPS",
            "Native real-time multiplayer pair programming",
            "Built-in AI assistant integration (Claude, OpenAI, Ollama)",
            "Lightweight memory profile and instant startup time"
        ],
        "pros": [
            "Unmatched execution and input speed with zero UI lag",
            "Native Rust architecture engineered from scratch",
            "Seamless multi-user collaboration and pair programming features"
        ],
        "cons": [
            "Extension ecosystem is still growing compared to VS Code",
            "Windows support is in early active preview"
        ],
        "target_audience": "Performance purists, Rust enthusiasts, and developers who prioritize raw speed.",
        "verdict_rating": "9.1/10",
        "verdict_summary": "The fastest modern code editor redefining UI responsiveness through GPU rendering."
    },
    {
        "name": "Neovim",
        "slug": "neovim",
        "developer": "Neovim Community",
        "license_type": "Open Source (Apache 2.0 / Vim)",
        "pricing": "Free",
        "website": "https://neovim.io",
        "github_repo": "https://github.com/neovim/neovim",
        "description": "A hyperextensible Vim-based text editor built for extreme customization via Lua scripts and native LSP integration.",
        "key_features": [
            "Native Lua scripting language engine for hyper-fast config",
            "Built-in Language Server Protocol (LSP) client and Treesitter parsing",
            "Terminal-first workflow with near-zero resource consumption",
            "Massive community plugin ecosystem (Lazy.nvim, Telescope, Mason)"
        ],
        "pros": [
            "Blazing fast performance on any machine setup",
            "Infinite customizability tailored exactly to developer preferences",
            "Keyboard-centric modal editing for maximum typing efficiency"
        ],
        "cons": [
            "Steep learning curve for modal editing and Lua configuration",
            "Requires initial setup effort before reaching full IDE parity"
        ],
        "target_audience": "Terminal power users, modal editing fans, and developer productivity enthusiasts.",
        "verdict_rating": "9.3/10",
        "verdict_summary": "The pinnacle of modal terminal editing providing unparalleled customizability and speed."
    },
    {
        "name": "Sublime Text 4",
        "slug": "sublime-text",
        "developer": "Sublime HQ",
        "license_type": "Shareware / Commercial",
        "pricing": "Free evaluation / $99 license",
        "website": "https://www.sublimetext.com",
        "github_repo": "",
        "description": "A refined, ultra-fast cross-platform code editor known for instant startup, low memory usage, and GPU-rendered text rendering.",
        "key_features": [
            "GPU hardware acceleration for crisp, fluid rendering",
            "Sublime Merge integration and native tab multi-select",
            "Powerful Python API and Package Control ecosystem",
            "Instant indexing and project switching across large codebases"
        ],
        "pros": [
            "Starts up instantly even with hundreds of open tabs",
            "Extremely low CPU and RAM consumption",
            "Clean, distraction-free user interface"
        ],
        "cons": [
            "Lacks built-in debugging without third-party LSP configuration",
            "Paid license model compared to free open-source alternatives"
        ],
        "target_audience": "Developers who value instant startup times and minimal system overhead.",
        "verdict_rating": "8.8/10",
        "verdict_summary": "A timeless classic that remains one of the fastest and lightest GUI code editors available."
    },
    {
        "name": "JetBrains PyCharm",
        "slug": "pycharm",
        "developer": "JetBrains",
        "license_type": "Freemium / Commercial",
        "pricing": "Community (Free) / Professional ($109+/yr)",
        "website": "https://www.jetbrains.com/pycharm/",
        "github_repo": "https://github.com/JetBrains/intellij-community/tree/master/python",
        "description": "The definitive IDE for Python development, data science, and web frameworks like Django, FastApi, and Flask.",
        "key_features": [
            "Smart Python code completion, automated refactoring, and linting",
            "Integrated Jupyter Notebook support and interactive scientific stack",
            "Django, FastAPI, and Flask web development toolset",
            "Built-in visual debugger, profiler, and database management"
        ],
        "pros": [
            "Best-in-class Python static analysis and virtual environment management",
            "Comprehensive out-of-the-box support for data science and web stacks",
            "Seamless Git and database tools integration"
        ],
        "cons": [
            "Can be resource-intensive on low-end machines",
            "Full features restricted to Professional tier"
        ],
        "target_audience": "Python developers, data scientists, machine learning engineers, and Django backend devs.",
        "verdict_rating": "9.4/10",
        "verdict_summary": "The undisputed heavyweight champion for dedicated Python and data science engineering."
    },
    {
        "name": "Helix",
        "slug": "helix",
        "developer": "Helix Community",
        "license_type": "Open Source (MPL 2.0)",
        "pricing": "Free",
        "website": "https://helix-editor.com",
        "github_repo": "https://github.com/helix-editor/helix",
        "description": "A post-modern modal terminal text editor written in Rust, featuring zero-config built-in LSP, Treesitter syntax highlighting, and Kakoune-style selection-first editing.",
        "key_features": [
            "Zero configuration required for LSP, auto-complete, and Treesitter",
            "Selection-first modal editing paradigm",
            "Built with Rust for ultra-fast performance and tiny footprint",
            "Multiple cursors built in natively"
        ],
        "pros": [
            "Works out-of-the-box without requiring complex plugin management",
            "Extremely fast and lightweight terminal interface",
            "Beautiful default themes and keymap discovery overlay"
        ],
        "cons": [
            "Non-standard keybindings for Vim users (selection-action flow)",
            "Plugin system is still under active architectural design"
        ],
        "target_audience": "Developers looking for a zero-config modal editor in the terminal.",
        "verdict_rating": "9.0/10",
        "verdict_summary": "The best out-of-the-box modal terminal editor for developers who want Vim speed without config hassle."
    },
    {
        "name": "JetBrains Fleet",
        "slug": "fleet",
        "developer": "JetBrains",
        "license_type": "Freemium",
        "pricing": "Free preview / Paid tier planned",
        "website": "https://www.jetbrains.com/fleet/",
        "github_repo": "",
        "description": "A lightweight multi-language editor by JetBrains with a distributed architecture, smart code engine, and collaborative cloud workspace support.",
        "key_features": [
            "Switchable lightweight mode vs full IntelliJ smart engine mode",
            "Multi-language support out of the box (Python, Java, Go, Rust, TS, C++)",
            "Built-in collaboration and remote machine development",
            "Modern, sleek minimalistic dark user interface"
        ],
        "pros": [
            "Instant startup with on-demand intelligent code analysis backend",
            "Unified experience across multiple programming languages",
            "Native JetBrains quality without classic IDE bloat"
        ],
        "cons": [
            "Still under active preview and development",
            "Plugin marketplace ecosystem is in early stages"
        ],
        "target_audience": "Developers wanting JetBrains code intelligence in a lightweight, fast editor.",
        "verdict_rating": "8.7/10",
        "verdict_summary": "JetBrains' sleek response to VS Code, bridging lightweight text editing with heavy IDE smarts."
    },
    {
        "name": "Lapce",
        "slug": "lapce",
        "developer": "Lapce Community",
        "license_type": "Open Source (Apache 2.0)",
        "pricing": "Free",
        "website": "https://lapce.dev",
        "github_repo": "https://github.com/lapce/lapce",
        "description": "A lightning-fast GUI code editor written in Rust with Druid UI and WASI plugin system, designed for high performance and remote development.",
        "key_features": [
            "GPU accelerated UI rendering via Rust",
            "Native remote development over SSH",
            "WASI-based sandboxed plugin system for safety",
            "Built-in LSP support and modal editing mode option"
        ],
        "pros": [
            "Extremely fast startup and typing latency",
            "Sandboxed WASM plugins prevent editor crashes",
            "Native cross-platform experience (Linux, macOS, Windows)"
        ],
        "cons": [
            "Plugin ecosystem is still young",
            "Occasional visual glitches during rapid development updates"
        ],
        "target_audience": "Rust enthusiasts and developers searching for a lightweight open-source GUI editor.",
        "verdict_rating": "8.5/10",
        "verdict_summary": "An exciting open-source Rust GUI editor with immense potential for speed and sandboxed extensions."
    },
    {
        "name": "Eclipse IDE",
        "slug": "eclipse",
        "developer": "Eclipse Foundation",
        "license_type": "Open Source (EPL-2.0)",
        "pricing": "Free",
        "website": "https://www.eclipse.org/ide/",
        "github_repo": "https://github.com/eclipse-platform/eclipse.platform",
        "description": "The veteran open-source Java and enterprise C/C++ development environment with extensive OSGi plugin framework.",
        "key_features": [
            "Comprehensive Java Development Tools (JDT)",
            "Massive enterprise ecosystem and plugin marketplace",
            "Advanced workspace management and build tool integrations",
            "Customizable perspective and window layouts"
        ],
        "pros": [
            "100% free and open-source enterprise IDE",
            "Deep history of enterprise toolchain stability",
            "Strong support for legacy Java and C++ codebases"
        ],
        "cons": [
            "Cluttered and dated user interface compared to modern editors",
            "Can suffer performance slow-downs on large workspaces"
        ],
        "target_audience": "Enterprise Java developers, legacy system maintainers, and academic environments.",
        "verdict_rating": "7.8/10",
        "verdict_summary": "A battle-tested open-source giant that remains relevant for enterprise Java ecosystems."
    }
]

def get_ide_by_slug_or_name(query: str) -> Optional[Dict[str, Any]]:
    """Look up an IDE in the default catalog by name or slug."""
    clean_query = query.strip().lower().replace(" ", "-")
    for ide in DEFAULT_IDE_CATALOG:
        if ide["slug"] == clean_query or ide["name"].lower() == query.strip().lower():
            return ide
    return None

def fetch_github_repo_info(repo_url: str) -> Dict[str, Any]:
    """Fetch repository metadata from GitHub API given a URL like https://github.com/owner/repo."""
    parsed = urllib.parse.urlparse(repo_url)
    path_parts = [p for p in parsed.path.strip("/").split("/") if p]
    if len(path_parts) < 2:
        raise ValueError("Invalid GitHub URL format. Expected https://github.com/owner/repo")

    owner, repo = path_parts[0], path_parts[1]
    api_url = f"https://api.github.com/repos/{owner}/{repo}"

    req = urllib.request.Request(api_url, headers={"User-Agent": "IDEGuide/1.0"})
    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            repo_name = data.get("name", repo).capitalize()
            description = data.get("description") or f"A modern code editor/IDE repository: {owner}/{repo}."
            license_info = data.get("license", {}) or {}
            license_name = license_info.get("name", "Open Source")
            stargazers = data.get("stargazers_count", 0)

            return {
                "name": repo_name,
                "slug": repo.lower(),
                "developer": owner.capitalize(),
                "license_type": license_name,
                "pricing": "Free / Open Source",
                "website": data.get("homepage") or repo_url,
                "github_repo": repo_url,
                "description": description,
                "key_features": [
                    f"Open source repository with {stargazers:,}+ GitHub stars",
                    f"Active developer community under {owner}",
                    "Customizable source code architecture",
                    "Native cross-platform development support"
                ],
                "pros": [
                    "100% open-source transparency",
                    f"Strong community backing with {stargazers:,} stars",
                    "Active maintenance and open issue tracking"
                ],
                "cons": [
                    "May require building from source or handling manual releases",
                    "Ecosystem extensions depend on community adoption"
                ],
                "target_audience": f"Developers interested in {repo_name} and modern open-source toolchains.",
                "verdict_rating": "8.9/10",
                "verdict_summary": f"An innovative open-source editor making waves in software development with {stargazers:,}+ stars."
            }
    except Exception as e:
        # Fallback if network call fails or API rate limited
        return {
            "name": repo.capitalize(),
            "slug": repo.lower(),
            "developer": owner.capitalize(),
            "license_type": "Open Source",
            "pricing": "Free",
            "website": repo_url,
            "github_repo": repo_url,
            "description": f"Open source code editor repository ({owner}/{repo}).",
            "key_features": [
                "Open source code editor project",
                "Community-driven feature requests and extensions",
                "Cross-platform capability"
            ],
            "pros": ["Open source flexibility", "Transparent development"],
            "cons": ["Ecosystem maturity depending on release state"],
            "target_audience": "Developers and contributors exploring new IDE alternatives.",
            "verdict_rating": "8.5/10",
            "verdict_summary": f"A promising open-source code editor project from {owner}."
        }

def construct_custom_ide_data(name: str) -> Dict[str, Any]:
    """Construct a default data structure for any custom IDE name requested by user."""
    slug = name.strip().lower().replace(" ", "-")
    existing = get_ide_by_slug_or_name(name)
    if existing:
        return existing

    return {
        "name": name,
        "slug": slug,
        "developer": f"{name} Team",
        "license_type": "Free / Paid Options",
        "pricing": "Freemium / Commercial",
        "website": f"https://{slug}.dev",
        "github_repo": "",
        "description": f"{name} is a modern code editor and development environment designed to enhance developer productivity.",
        "key_features": [
            f"Tailored editing experience with {name} smart tools",
            "Syntax highlighting, code navigation, and project search",
            "Integrated terminal and extension capabilities",
            "Custom themes, keybindings, and user workspace settings"
        ],
        "pros": [
            f"Focused development workflow with {name} core features",
            "Smooth UI responsiveness and project navigation",
            "Active developer tools integration"
        ],
        "cons": [
            "Requires time to learn custom keymap shortcuts",
            "May have a smaller extension ecosystem compared to market leaders"
        ],
        "target_audience": f"Software engineers, web developers, and coding enthusiasts interested in {name}.",
        "verdict_rating": "8.8/10",
        "verdict_summary": f"{name} presents a solid development environment capable of accelerating modern software workflows."
    }
