# AMP Blogger Guidelines for IDE Guide

These guidelines define the Accelerated Mobile Pages (AMP) HTML standards and structural requirements for blog posts generated for [ideguide.blogspot.com](https://ideguide.blogspot.com/).

## 1. AMP HTML Constraints & Standard Formatting

To comply with Blogger AMP post requirements:
- **Disallowed Tags**: Standard `<img>`, `<video>`, `<audio>`, or `<script>` tags are disallowed inside the post body content except for valid inline style blocks or specified AMP components (e.g., `<amp-img>`).
- **Inline Styling**: Avoid external stylesheets. CSS must be clean inline styles or scoped via permitted `<style amp-custom>` components.
- **Images**: Any inline image must use `<amp-img src="..." width="..." height="..." layout="responsive" alt="..."></amp-img>`.
- **Layout Structure**:
  - Semantic section headings (`<h2>`, `<h3>`).
  - Bulleted pros and cons (`<ul>`, `<li>`).
  - Clear pricing and feature breakdown table or bullet list (Free vs Paid vs Freemium).
  - Verdict recommendation section ("Who should use this IDE?").

## 2. Non-Sponsorship & Independence Disclaimer

Every blog post **MUST** include the exact non-sponsorship disclosure in a highlighted callout block (`<div class="disclaimer">...</div>` or `<p><em>...</em></p>`):

> **Disclaimer**: IDE Guide is an independent technical publication. This content is not sponsored, endorsed, or affiliated with any software vendor or editor developer mentioned above. All reviews and assessments are based strictly on objective developer evaluation.

## 3. Post Structure Template

```html
<article class="ide-review-post">
  <header>
    <h1>[IDE Name] Review: Features, Pros & Cons, and Best Use Cases</h1>
    <p class="meta">Published by IDE Guide | Target Audience: Developers & Software Engineers</p>
  </header>

  <section class="overview">
    <h2>Overview</h2>
    <p>[Detailed objective intro covering history, target platform, ecosystem]</p>
  </section>

  <section class="key-features">
    <h2>Key Features & Capabilities</h2>
    <ul>
      <li><strong>[Feature 1]:</strong> [Details]</li>
      <li><strong>[Feature 2]:</strong> [Details]</li>
    </ul>
  </section>

  <section class="pros-cons">
    <h2>Pros & Cons</h2>
    <h3>Pros</h3>
    <ul>
      <li>[Pro 1]</li>
      <li>[Pro 2]</li>
    </ul>
    <h3>Cons</h3>
    <ul>
      <li>[Con 1]</li>
      <li>[Con 2]</li>
    </ul>
  </section>

  <section class="pricing">
    <h2>Pricing Model: Free vs Paid</h2>
    <p><strong>License Type:</strong> [Free / Open Source / Paid / Freemium]</p>
    <p>[Pricing details and tiers if applicable]</p>
  </section>

  <section class="verdict">
    <h2>Verdict: Is [IDE Name] Right For You?</h2>
    <p>[Final recommendation and developer persona fit]</p>
  </section>

  <footer class="disclaimer-block">
    <p><em>Disclaimer: IDE Guide is an independent technical publication. This content is not sponsored, endorsed, or affiliated with any software vendor or editor developer mentioned above. All reviews and assessments are based strictly on objective developer evaluation.</em></p>
  </footer>
</article>
```
