# AMP HTML Blogger Guidelines for IDE Guide

This document outlines the standard guidelines and rules for generating AMP (Accelerated Mobile Pages) compliant HTML content specifically tailored for Blogger (`https://ideguide.blogspot.com/`).

## Core AMP Rules & Boilerplate

1. **Document Declaration**:
   - Start with `<!doctype html>`
   - Top-level tag must be `<html ⚡>` or `<html amp>` with `lang="en"` (or applicable language).

2. **Head Tag Requirements**:
   - `<meta charset="utf-8">`
   - `<script async src="https://cdn.ampproject.org/v0.js"></script>`
   - `<link rel="canonical" href="CANONICAL_URL">`
   - `<meta name="viewport" content="width=device-width,minimum-scale=1,initial-scale=1">`
   - AMP Boilerplate code:
     ```html
     <style amp-boilerplate>body{-webkit-animation:-amp-start 8s steps(1,end) 0s 1 normal both;-moz-animation:-amp-start 8s steps(1,end) 0s 1 normal both;-ms-animation:-amp-start 8s steps(1,end) 0s 1 normal both;animation:-amp-start 8s steps(1,end) 0s 1 normal both}@-webkit-keyframes -amp-start{from{visibility:hidden}to{visibility:visible}}@-moz-keyframes -amp-start{from{visibility:hidden}to{visibility:visible}}@-ms-keyframes -amp-start{from{visibility:hidden}to{visibility:visible}}@-o-keyframes -amp-start{from{visibility:hidden}to{visibility:visible}}@keyframes -amp-start{from{visibility:hidden}to{visibility:visible}}</style><noscript><style amp-boilerplate>body{-webkit-animation:none;-moz-animation:none;-ms-animation:none;animation:none}</style></noscript>
     ```

3. **Styling Rules (`<style amp-custom>`)**:
   - All custom styles must reside inside a single `<style amp-custom>` tag inside `<head>`.
   - Max size: 75KB.
   - Do not use `!important` flags or disallowed CSS properties (`behavior`, `-ms-behavior`, etc.).

4. **Media Tags**:
   - Standard HTML `<img>` tags are forbidden. Use `<amp-img>` with explicit `width`, `height`, and `layout` attributes (e.g., `layout="responsive"`).

5. **Disallowed Tags & Scripts**:
   - No custom `<script>` tags allowed.
   - No inline `style="..."` attributes on body elements.

## Mandatory Non-Sponsorship Disclaimer

Every AMP blog post generated for IDE Guide **MUST** include the following exact disclaimer text in the footer or designated disclaimer section:

> **Disclaimer:** IDE Guide is an independent technical publication. This content is not sponsored, endorsed, or affiliated with any software vendor or editor developer mentioned above. All reviews and assessments are based strictly on objective developer evaluation.

## Blogger Post Structure Template

Each article generated for an IDE or Code Editor should follow this schema:

1. **Header & Badges**:
   - IDE Name, Version/Category, Pricing Tag (`[FREE]`, `[PAID]`, or `[FREEMIUM]`).
2. **Executive Overview**:
   - What the tool is, core focus, ecosystem support.
3. **Key Features & Strengths (The Good)**:
   - Performance, extensions, AI assistance, multi-language support.
4. **Limitations & Drawbacks (The Bad)**:
   - Memory consumption, learning curve, plugin quality, platform lock-in.
5. **Pricing Breakdown**:
   - Detailed free vs. paid tier comparison table.
6. **Verdict & Recommendations**:
   - Which developers or project types should choose this tool.
7. **Non-sponsorship Disclaimer Notice**.
