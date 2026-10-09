# AMP Blogger Post Guidelines for IDE Guide

This document outlines the formatting and compliance guidelines for blog post content generated for **IDE Guide** ([ideguide.blogspot.com](https://ideguide.blogspot.com/)).

## 1. Accelerated Mobile Pages (AMP) Standards

Blogger AMP posts must adhere strictly to Accelerated Mobile Pages HTML rules:

1. **Images (`<amp-img>`)**:
   - Standard HTML `<img>` tags are strictly prohibited.
   - All images must use `<amp-img>` with explicit `width`, `height`, and `layout` attributes (e.g., `layout="responsive"`).
   - Example:
     ```html
     <amp-img src="https://example.com/screenshot.png" width="800" height="450" layout="responsive" alt="IDE Interface"></amp-img>
     ```

2. **Styling Restrictions**:
   - Inline `style="..."` attributes on individual HTML tags are invalid in AMP HTML and must not be used.
   - Allowed CSS must be included inside `<style amp-custom>` blocks if full document AMP, or clean semantic tags for Blogger body content.

3. **Scripts & Disallowed Tags**:
   - Custom `<script>` tags are forbidden unless loading valid AMP components (e.g., `<script async custom-element="amp-img" src="https://cdn.ampproject.org/v0/amp-img-0.1.js"></script>`).
   - Disallowed elements like `<iframe>`, `<embed>`, `<object>`, or event handlers (e.g., `onclick`, `onload`) are prohibited in the post body.

4. **Semantic HTML Structure**:
   - Posts must use clean semantic tags: `<h1>`, `<h2>`, `<h3>`, `<p>`, `<ul>`, `<ol>`, `<li>`, `<table>`, `<blockquote>`, `<code>`, `<pre>`.

## 2. Article Structure & Content Rules

Each IDE guide blog post must cover:
1. **Title & Summary**: Clear, engaging title comparing or reviewing the target IDE or code editor.
2. **Overview**: Introduction to the IDE, primary programming language support, target audience, and key highlights.
3. **Good & Bad (Pros & Cons)**:
   - **Pros (The Good)**: Strengths, performance features, extension ecosystem, AI capabilities, UI/UX advantages.
   - **Cons (The Bad)**: Resource consumption, memory usage, learning curve, missing features, pricing hurdles.
4. **Pricing Model**: Explicit breakdown of whether the tool is Free, Open Source, Paid, Freemium, or Subscription-based.
5. **Verdict & Recommendations**: Guidance on who should use this IDE (e.g., beginners, enterprise teams, web developers, systems programmers).
6. **Mandatory Non-Sponsorship Disclaimer**: Every blog post must conclude with the exact disclaimer.

## 3. Mandatory Non-Sponsorship Disclaimer

All generated blog posts must contain the following exact disclaimer text:

> **Disclaimer**: IDE Guide is an independent technical publication. This content is not sponsored, endorsed, or affiliated with any software vendor or editor developer mentioned above. All reviews and assessments are based strictly on objective developer evaluation.
