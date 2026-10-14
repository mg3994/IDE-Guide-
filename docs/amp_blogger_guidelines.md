# AMP Blogger Guidelines for IDE Guide

This document specifies the AMP (Accelerated Mobile Pages) HTML formatting rules and standards required for blog posts published to Blogger at [https://ideguide.blogspot.com/](https://ideguide.blogspot.com/).

## Core Requirements

1. **AMP Boilerplate & Markup**:
   - Posts must adhere to AMP HTML specifications.
   - Standard HTML `<img>` tags are strictly forbidden; use `<amp-img>` with explicit `width`, `height`, and `layout="responsive"`.
   - External JavaScript `<script>` tags are disallowed unless loading official AMP component scripts in `<head>`.
   - Inline style attributes (`style="..."`) on individual HTML elements are strictly prohibited. Custom CSS must be placed in a single `<style amp-custom>` block.

2. **Required Structure for Blogger Posts**:
   - Every post must include:
     - Clear title (`<h1>`)
     - Key Highlights / Summary box
     - Features and Architecture breakdown
     - Pros (Good) and Cons (Bad) sections
     - Pricing model details (Free vs Paid / Freemium / Open Source)
     - Target Audience / Ideal Use Case recommendation
     - Interactive / Visual `<amp-img>` illustration placeholders with fallback text
     - Mandatory Non-Sponsorship Disclaimer

3. **Mandatory Non-Sponsorship Disclaimer**:
   Every post generated MUST conclude with the following exact disclaimer text:

   > Disclaimer: IDE Guide is an independent technical publication. This content is not sponsored, endorsed, or affiliated with any software vendor or editor developer mentioned above. All reviews and assessments are based strictly on objective developer evaluation.

4. **AMP Component Reference**:
   - `<amp-img src="..." width="800" height="450" layout="responsive" alt="..."></amp-img>`
   - `<style amp-custom>` for styling content layout, pros/cons cards, badges, and code blocks.
