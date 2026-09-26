# AMP HTML Guidelines for Blogger - IDE Guide

## Overview
This document specifies the AMP (Accelerated Mobile Pages) HTML formatting rules for blog posts published on [IDE Guide (ideguide.blogspot.com)](https://ideguide.blogspot.com/). All blog posts produced by automated tools or agentic skills must adhere strictly to these rules to ensure valid AMP markup and clean rendering on mobile and desktop devices.

## AMP Core Rules for Blogger
1. **No Custom JavaScript**: Custom `<script>` tags are strictly prohibited unless they load official AMP components (e.g., `<script async src="https://cdn.ampproject.org/v0.js"></script>`).
2. **Image Handling (`<amp-img>`)**:
   - Standard HTML `<img>` tags must NOT be used.
   - Use `<amp-img>` with explicit `width`, `height`, and `layout="responsive"` attributes.
   - Example:
     ```html
     <amp-img src="https://images.unsplash.com/photo-1555066931-4365d14bab8c" width="800" height="450" layout="responsive" alt="VS Code Interface"></amp-img>
     ```
3. **Styling (`<style amp-custom>`)**:
   - All custom CSS must be placed within a single `<style amp-custom>` tag.
   - Total CSS size must not exceed 75KB.
   - Inline `style="..."` attributes are disallowed in strict AMP. Use CSS classes instead.
4. **Semantic HTML Structure**:
   - Post wrapper class: `.ide-guide-post`
   - Headers: `<h1>`, `<h2>`, `<h3>`
   - Highlights & Badges: `.badge-free`, `.badge-paid`, `.badge-freemium`
   - Section containers: `.pro-con-grid`, `.verdict-box`, `.spec-table`, `.disclaimer-box`

## Mandatory Non-Sponsorship Disclaimer
Every single blog post published on IDE Guide MUST end with the exact non-sponsorship disclaimer box:

```html
<div class="disclaimer-box">
  <p><strong>Disclaimer:</strong> IDE Guide is an independent technical publication. This content is not sponsored, endorsed, or affiliated with any software vendor or editor developer mentioned above. All reviews and assessments are based strictly on objective developer evaluation.</p>
</div>
```

## Daily Content Output Structure
Each blog post must contain the following core sections:
1. **Header & Title**: Descriptive title containing the IDE name and category (e.g., "Cursor AI IDE: Pros, Cons, Pricing & Is It Worth It?").
2. **At-a-Glance Summary & Pricing Tier**:
   - Category badge (Free / Paid / Freemium)
   - Primary target developer audience (Web, Python, Systems, AI engineering)
3. **The Good (Pros)**: Highlighted bulleted list with key strengths (Performance, Extension Ecosystem, AI capabilities, Refactoring).
4. **The Bad (Cons)**: Highlighted bulleted list with weaknesses (Memory usage, Privacy concerns, Licensing cost, Closed source).
5. **Pricing Breakdown**: Exact pricing model (Free, Pro monthly/yearly subscription, Enterprise, Perpetual license).
6. **Verdict & Recommendations**: "Who should use this IDE?" clear buying/choice advice.
7. **YouTube Channel Call to Action**: Link to [YouTube @IDEguide](https://www.youtube.com/@IDEguide) for companion visual video guides and shorts.
