# AMP HTML Blogger Guidelines for IDE Guide

These guidelines define the AMP HTML rules and formatting standards for blog posts targeted for [IDE Guide on Blogger](https://ideguide.blogspot.com/).

## Core Requirements

1. **AMP Boilerplate**:
   - Must begin with `<!doctype html>`.
   - The `<html>` tag must include `⚡` or `amp` attribute (e.g. `<html ⚡ lang="en">`).
   - Must contain `<meta charset="utf-8">`.
   - Must contain `<meta name="viewport" content="width=device-width,minimum-scale=1,initial-scale=1">`.
   - Must load the AMP runtime script: `<script async src="https://cdn.ampproject.org/v0.js"></script>`.
   - Must include `<style amp-boilerplate>` and `<noscript><style amp-boilerplate>` blocks.

2. **Custom Styling**:
   - Standard author CSS must be inlined within `<style amp-custom> ... </style>` inside `<head>`.
   - Total custom CSS must not exceed 75KB.
   - External stylesheets are disallowed except for approved web fonts.

3. **Media Elements**:
   - Images must use `<amp-img>` instead of standard `<img>` with explicit `width`, `height`, and `layout` attributes.
   - Videos must use `<amp-video>` or YouTube embeds `<amp-youtube>`.

4. **Non-Sponsorship Disclaimer**:
   - Every post must include the exact mandatory non-sponsorship disclaimer at the bottom:
   > "Disclaimer: IDE Guide is an independent technical publication. This content is not sponsored, endorsed, or affiliated with any software vendor or editor developer mentioned above. All reviews and assessments are based strictly on objective developer evaluation."

5. **Content Structure for IDE Guide Reviews**:
   - Overview & Target Use Cases.
   - Pricing Model (Free, Paid, Freemium, Open Source).
   - Key Features & Highlights (Good / Strengths).
   - Known Limitations & Drawbacks (Bad / Weaknesses).
   - Comparison & Verdict (Which developer persona should choose this IDE).
