# AMP HTML Blogger Guidelines for IDE Guide

This document defines the Accelerated Mobile Pages (AMP) standards and formatting rules for all blog posts published to [ideguide.blogspot.com](https://ideguide.blogspot.com/).

## 1. Core Formatting Rules

- **Valid AMP Markup**: Must use valid AMP tags. Standard `<img>` tags must be replaced with `<amp-img width="..." height="..." layout="responsive" src="...">`.
- **Inline Styling**: Inline styles must be minimal and contained in `<style amp-custom>...</style>` blocks if present. Unsafe inline `style="..."` attributes with prohibited expressions or external scripts `<script src="...">` are forbidden.
- **Allowed HTML Elements**: `<h2>`, `<h3>`, `<p>`, `<ul>`, `<li>`, `<strong>`, `<em>`, `<code>`, `<pre>`, `<table>`, `<tr>`, `<th>`, `<td>`, `<blockquote>`, `<amp-img>`.
- **Prohibited Elements**: Raw `<script>`, `<iframe>` (without `amp-iframe`), `<style>` outside `amp-custom`, `<form>`, `<input>`.

## 2. Blog Post Structure Requirements

Every generated blog post must follow this section structure:

1. **Title**: Catchy title including the IDE/Editor name, core verdict (e.g., *VS Code in 2026: Still the Best Free Code Editor?*).
2. **Introduction**: Brief summary of the IDE, developer, target audience, and primary ecosystem.
3. **Key Strengths (The Good)**: Detailed breakdown of top features, extension ecosystem, performance, and key workflows.
4. **Weaknesses & Drawbacks (The Bad)**: Honest review of memory usage, setup complexity, telemetry, or licensing concerns.
5. **Pricing & Licensing Model**: Explicit details on whether the IDE is Free, Open Source, Freemium, or Paid (Subscription/One-time).
6. **Verdict & Recommendations**: Guidance on who should use this editor (e.g. beginners, enterprise teams, web developers, systems programmers).
7. **Mandatory Non-Sponsorship Disclaimer**: Must appear at the bottom of every post.

## 3. Mandatory Non-Sponsorship Disclaimer

> **Disclaimer:** IDE Guide is an independent technical publication. This content is not sponsored, endorsed, or affiliated with any software vendor or editor developer mentioned above. All reviews and assessments are based strictly on objective developer evaluation.
