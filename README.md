# IDE Guide (@IDEguide & ideguide.blogspot.com)

Automated Content Generation Pipeline for **IDE Guide** — independent developer evaluation of IDEs, code editors, and software developer tools.

## 🌟 Channel & Website Links
- **YouTube Channel:** [@IDEguide](https://www.youtube.com/@IDEguide)
- **Blogger Website:** [ideguide.blogspot.com](https://ideguide.blogspot.com/)

---

## ⚡ Features & Architecture

1. **AMP (Accelerated Mobile Pages) Blog Posts**
   - Compliant with Google Blogger AMP guidelines (`<html ⚡>`, `<style amp-boilerplate>`, `<style amp-custom>`, `<amp-img>`).
   - Includes Schema.org `TechArticle` JSON-LD structured data for enhanced Google Search indexing.
   - Evaluates IDE pros, cons, target audience, pricing tiers (free vs. paid), and developer details.

2. **Google Flow Video Specifications**
   - Tailored video generation scripts and visual prompts for Google Flow and AI video tools.
   - Generates dual video formats:
     - **YouTube Shorts (9:16 Vertical, ~50s):** Rapid hook, feature summary, cons, verdict, and subscribe CTA.
     - **Long-Form (16:9 4K, ~5 min):** Deep dive overview, features, pros/cons matrix, pricing, and independent review verdict.

3. **Mandatory Non-Sponsorship Disclaimer**
   - Every generated article and video script strictly incorporates the mandatory disclosure:
   > *"Disclaimer: IDE Guide is an independent technical publication. This content is not sponsored, endorsed, or affiliated with any software vendor or editor developer mentioned above. All reviews and assessments are based strictly on objective developer evaluation."*

4. **Agentic Skill CLI Tool**
   - On-demand custom content generation via `scripts/ide_guide_agent_skill.py`.
   - Supports fetching repository metadata directly via GitHub API.

5. **Automated Daily Scheduling**
   - GitHub Actions workflow (`.github/workflows/daily_content_generation.yml`) runs daily at 21:30 UTC (03:00 AM IST) to publish 3 new blog posts and 3 video specs per day.

---

## 🚀 Quick Start & Usage

### Running Daily Generation Manually
To generate today's batch of 3 IDE blog posts and video specs:
```bash
python3 scripts/generate_daily_content.py
```
Output files will be saved in `content/YYYY-MM-DD/` along with updated history in `content/history.json`.

### Using the Agentic Skill CLI
Generate custom content for any IDE or code editor:
```bash
python3 scripts/ide_guide_agent_skill.py \
  --name "Windsurf Editor" \
  --tagline "Agentic AI Code Editor" \
  --pricing "Freemium ($15/mo)" \
  --pros "Flows feature, VS Code extension compatibility, Fast indexing" \
  --cons "Requires subscription for advanced agents"
```

Generate content directly from a GitHub Repository URL:
```bash
python3 scripts/ide_guide_agent_skill.py --github "https://github.com/vscodium/vscodium"
```

---

## 📖 Documentation
For Google Flow visual prompt engineering, camera shot specs, audio settings, and lighting guidelines, refer to `docs/google_flow_spec_guidelines.md`.
