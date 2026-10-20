# AMP HTML Guidelines for Blogger Posts (IDE Guide)

This document specifies the mandatory structure, rules, and visual style guidelines for AMP (Accelerated Mobile Pages) HTML blog posts targeting Blogger (`https://ideguide.blogspot.com/`).

## 1. Core AMP HTML Rules

All generated blog posts must strictly conform to AMP HTML specifications:
1. **AMP Boilerplate & Root**: Include `<html ⚡>` or `<html amp>` root tag.
2. **Metadata & Head Rules**:
   - `<meta charset="utf-8">`
   - `<script async src="https://cdn.ampproject.org/v0.js"></script>`
   - `<link rel="canonical" href="...">`
   - `<meta name="viewport" content="width=device-width,minimum-scale=1,initial-scale=1">`
   - Canonical AMP boilerplate styling inside `<style amp-boilerplate>...</style>`.
3. **Custom Styles**: Custom CSS must be inline inside `<style amp-custom>...</style>` and strictly under 75KB.
4. **Image Elements**: Use `<amp-img>` with explicit `width`, `height`, and `layout="responsive"` instead of standard `<img>` tags.
5. **No Disallowed Elements**: No inline `style` attributes on tags, no custom JavaScript `<script>` tags, no forms without `amp-form`.

## 2. Structured Article Layout

Every IDE review or comparison post must follow this clear, developer-centric structure:

1. **Header & Meta Section**:
   - Post Title (e.g., `VS Code in 2026: Pros, Cons, and Best Use Cases`)
   - Target Audience & IDE Overview summary box
2. **Pricing & Licensing Breakdown**:
   - Explicit Free vs. Paid vs. Freemium classification.
   - License type (Open Source, Proprietary, Enterprise).
3. **Pros & Strengths (Good)**:
   - Key features, performance, ecosystem, extensions, agentic AI integration.
4. **Cons & Limitations (Bad)**:
   - Memory footprint, learning curve, missing features, setup overhead.
5. **Verdict & Best For (Which to Choose)**:
   - Practical developer guidance on who should use this editor (e.g. beginners, backend devs, web teams).
6. **Non-Sponsorship Disclaimer**:
   - Every post MUST end with the explicit disclaimer:
     > "Disclaimer: IDE Guide is an independent technical publication. This content is not sponsored, endorsed, or affiliated with any software vendor or editor developer mentioned above. All reviews and assessments are based strictly on objective developer evaluation."

## 3. Styling & Color Theme

- Modern dark/light responsive layout with clean monospaced code blocks.
- Primary Accent: `#2563EB` (Royal Blue)
- Secondary Accent: `#059669` (Emerald Green)
- Warning/Cons Accent: `#DC2626` (Red)
