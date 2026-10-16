# AMP HTML Guidelines for Blogger Posts (IDE Guide)

This document specifies the AMP (Accelerated Mobile Pages) HTML formatting guidelines and structural requirements for all blog posts published on [IDE Guide Blogger](https://ideguide.blogspot.com/).

---

## 1. AMP HTML Rules & Specifications

All generated blog post content targeting Blogger must strictly conform to AMP HTML specifications:

### Boilerplate & Structural Requirements
1. **HTML Tag:** Must begin with `<html ⚡>` or `<html amp>`.
2. **Head Elements:**
   - `<meta charset="utf-8">`
   - `<script async src="https://cdn.ampproject.org/v0.js"></script>`
   - `<meta name="viewport" content="width=device-width,minimum-scale=1,initial-scale=1">`
   - Canonical URL link (`<link rel="canonical" href="...">`).
   - AMP Boilerplate style tag (`<style amp-boilerplate>...</style>`).
3. **Custom CSS:** Allowed exclusively within a single `<style amp-custom>...</style>` block inside `<head>`. Total inline style size must not exceed 75KB.
4. **No Disallowed HTML Tags:**
   - `<script>` tags are strictly forbidden unless they load an AMP component or are `type="application/json"`.
   - `<img>` tags are replaced with `<amp-img width="..." height="..." layout="responsive">`.
   - Inline `style="..."` attributes on standard elements are strictly prohibited.

---

## 2. Standard Blog Post Structure

Each daily blog post generated for IDE Guide must follow this structured template:

1. **Title:** Clean, keyword-focused title formatted as `<h1>` (e.g. `VS Code vs Cursor: Detailed Developer Guide`).
2. **Introduction:** High-level summary of the IDE / Code Editor, target language/ecosystem support, and key highlights.
3. **Key Features & Pros / Cons:**
   - **Good (Pros):** Speed, extension ecosystem, AI integration, debugging capability, auto-complete, multi-platform support.
   - **Bad (Cons):** Memory overhead, learning curve, closed-source elements, pricing model, latency.
4. **Pricing Breakdown:**
   - Clear classification: **Free**, **Paid**, **Freemium**, or **Open Source**.
   - Price tiers (if applicable) and subscription options.
5. **Verdict & Recommendation:** "Which one is best for you?" guidance categorized by developer workflow (e.g., beginner, web developer, enterprise team, backend engineer).
6. **Non-Sponsorship Disclaimer:** Mandatory exact text placed at the end of every post:
   > *Disclaimer: IDE Guide is an independent technical publication. This content is not sponsored, endorsed, or affiliated with any software vendor or editor developer mentioned above. All reviews and assessments are based strictly on objective developer evaluation.*
