# AMP Blogger Guidelines for IDE Guide

This document outlines the standard guidelines for generating Accelerated Mobile Pages (AMP) HTML blog posts for **IDE Guide** published on [https://ideguide.blogspot.com/](https://ideguide.blogspot.com/).

---

## 1. AMP HTML Rules & Boilerplate

All blog post outputs must comply strictly with the standard AMP HTML specification to ensure fast rendering and compliance on Blogger.

### Required HTML Structure
- **Root Tag**: `<html ⚡ lang="en">` or `<html amp lang="en">`
- **Charset**: `<meta charset="utf-8">`
- **Viewport**: `<meta name="viewport" content="width=device-width,initial-scale=1,minimum-scale=1">`
- **AMP Runtime Script**: `<script async src="https://cdn.ampproject.org/v0.js"></script>`
- **Canonical Link**: `<link rel="canonical" href="https://ideguide.blogspot.com/...">`
- **AMP Boilerplate**: Required `<style amp-boilerplate>` and `<noscript>` blocks.

### Custom CSS
- All styling must be contained in a single `<style amp-custom>` tag inside `<head>`.
- Inline `style="..."` attributes are strictly prohibited in AMP HTML.
- Max CSS size limit: 75KB.

### Images & Media
- standard `<img>` tags are **prohibited**. Always use `<amp-img>`.
- Required attributes on `<amp-img>`:
  - `src`: URL or path to image
  - `width` and `height`: Explicit integer values
  - `layout="responsive"` (or `fixed`, `intrinsic`)
  - `alt`: Descriptive accessibility alt text

### Disallowed Elements
- Standard custom JavaScript (`<script>` without `type="application/ld+json"` or amp runtime scripts).
- Standard `<img>`, `<video>`, `<audio>`, `<iframe>` tags without their `<amp-*>` counterparts (`<amp-img>`, `<amp-video>`, `<amp-iframe>`).
- Inline `style` attributes on HTML tags.

---

## 2. Blog Post Content Structure

Each blog post generated for **IDE Guide** must include the following sections:

1. **Header / Title**: Clear title showcasing the IDE or Code Editor.
2. **Overview**: Introduction to the tool, developer origin, and primary language ecosystem.
3. **The Good (Pros)**: Standout features, speed, extensibility, AI integration, debugging tools.
4. **The Bad (Cons)**: Memory usage, learning curve, missing extensions, cost, platform restrictions.
5. **Pricing & Licensing**: Clear breakdown of Free vs. Paid tiers, open source vs. commercial licensing.
6. **Verdict & Best For**: Objective assessment of which developers/projects benefit most.
7. **Mandatory Non-Sponsorship Disclaimer**: Must be present at the end of every post.

---

## 3. Mandatory Non-Sponsorship Disclaimer

Every blog post must include the exact disclaimer text below:

> **Disclaimer**: IDE Guide is an independent technical publication. This content is not sponsored, endorsed, or affiliated with any software vendor or editor developer mentioned above. All reviews and assessments are based strictly on objective developer evaluation.
