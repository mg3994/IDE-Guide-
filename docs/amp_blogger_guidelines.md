# AMP Blogger Guidelines for IDE Guide

These guidelines define the AMP (Accelerated Mobile Pages) HTML post requirements for content published on [ideguide.blogspot.com](https://ideguide.blogspot.com/).

## 1. AMP HTML Compliance Rules
- **DOCTYPE & Standard AMP boilerplate:** All blog post outputs must use valid AMP markup structure or AMP snippet wrappers compatible with Google Blogger post injection.
- **Forbidden HTML elements:** No raw `<img>`, `<video>`, `<script>` (except AMP components), or external custom JavaScript tags.
- **AMP Image Tag:** Use `<amp-img src="..." width="..." height="..." layout="responsive" alt="..."></amp-img>`.
- **AMP YouTube Component:** Use `<amp-youtube data-videoid="..." layout="responsive" width="480" height="270"></amp-youtube>`.
- **Styling:** CSS must be contained inside `<style amp-custom> ... </style>` tags or inline style attributes compliant with AMP limits (max 75KB total CSS).

## 2. Blog Post Structure & Required Sections
Every blog post generated for IDE Guide must include:
1. **Title:** Engaging, SEO-optimized title comparing or reviewing the IDE / Code Editor.
2. **Overview:** Introduction, target audience, and primary developer use-cases.
3. **Key Features & Strengths (The Good):** Highlighting performance, extension ecosystem, AI capabilities, and debugging tools.
4. **Weaknesses & Drawbacks (The Bad):** Memory usage, learning curve, price barriers, or lack of language support.
5. **Pricing Breakdown:** Detailed list of Free tiers, Pro plans, Enterprise options, and open-source availability.
6. **Verdict & Recommendations:** Who should use this IDE (Beginners, Enterprise, Data Scientists, Web Developers).
7. **Mandatory Non-Sponsorship Disclaimer:**
   > *Disclaimer: IDE Guide is an independent technical publication. This content is not sponsored, endorsed, or affiliated with any software vendor or editor developer mentioned above. All reviews and assessments are based strictly on objective developer evaluation.*

## 3. Validation
All generated blog post snippets must be validated against `scripts/amp_validator.py` to ensure zero validation errors before posting.
