# AMP HTML & Blogger Publishing Guidelines for IDE Guide

This document specifies the mandatory requirements and rules for generating AMP (Accelerated Mobile Pages) compliant HTML content for publishing on [IDE Guide Blogger](https://ideguide.blogspot.com/).

## 1. AMP HTML Boilerplate Requirements

All generated blog posts must follow the standard AMP HTML format:

```html
<!doctype html>
<html ⚡ lang="en">
<head>
  <meta charset="utf-8">
  <script async src="https://cdn.ampproject.org/v0.js"></script>
  <title>Title Here</title>
  <link rel="canonical" href="https://ideguide.blogspot.com/permalink.html">
  <meta name="viewport" content="width=device-width,minimum-scale=1,initial-scale=1">
  <style amp-boilerplate>body{-webkit-animation:-amp-start 8s steps(1,end) 0s 1 normal both;-moz-animation:-amp-start 8s steps(1,end) 0s 1 normal both;-ms-animation:-amp-start 8s steps(1,end) 0s 1 normal both;animation:-amp-start 8s steps(1,end) 0s 1 normal both}@-webkit-keyframes -amp-start{from{visibility:hidden}to{visibility:visible}}@-moz-keyframes -amp-start{from{visibility:hidden}to{visibility:visible}}@-ms-keyframes -amp-start{from{visibility:hidden}to{visibility:visible}}@-o-keyframes -amp-start{from{visibility:hidden}to{visibility:visible}}@keyframes -amp-start{from{visibility:hidden}to{visibility:visible}}</style><noscript><style amp-boilerplate>body{-webkit-animation:none;-moz-animation:none;-ms-animation:none;animation:none}</style></noscript>
  <style amp-custom>
    /* Custom CSS rules (max 75KB) */
    body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; line-height: 1.6; color: #1e293b; padding: 16px; margin: 0 auto; max-width: 800px; }
    .header { text-align: center; margin-bottom: 24px; }
    .badge-free { background: #10b981; color: white; padding: 4px 8px; border-radius: 4px; font-weight: bold; }
    .badge-paid { background: #f59e0b; color: white; padding: 4px 8px; border-radius: 4px; font-weight: bold; }
    .pros-cons { display: flex; gap: 16px; margin: 20px 0; }
    .pros, .cons { flex: 1; padding: 16px; border-radius: 8px; }
    .pros { background: #f0fdf4; border: 1px solid #bbf7d0; }
    .cons { background: #fef2f2; border: 1px solid #fecaca; }
    .disclaimer { background: #f8fafc; border-left: 4px solid #64748b; padding: 12px; margin-top: 32px; font-size: 0.9em; color: #475569; }
  </style>
</head>
<body>
  ...
</body>
</html>
```

## 2. Mandatory Restrictions & Elements

- **No custom JavaScript**: No `<script>` tags allowed except AMP runtime component scripts.
- **Image handling**: Standard `<img>` tags are forbidden. Use `<amp-img src="..." width="..." height="..." layout="responsive" alt="..."></amp-img>`.
- **Inline CSS**: Inline `style="..."` attributes are forbidden. All CSS must reside in `<style amp-custom>`.
- **Styling Limit**: CSS size in `<style amp-custom>` must not exceed 75KB.

## 3. Blog Post Structure for IDE Reviews

Every review blog post must contain the following sections:
1. **Header & Quick Summary**: Title, Pricing Model (`[FREE]` or `[PAID]`), Primary Target Language / Framework.
2. **Key Features & Capabilities**: What makes the IDE unique.
3. **Pros & Cons Breakdown**: Clear side-by-side comparison.
4. **Pricing & Licensing Details**: Explicitly states free tier vs paid enterprise options.
5. **Final Verdict & Recommendations**: Who should use this editor (beginners, team leads, performance-critical developers).
6. **Non-Sponsorship Disclaimer**: Must end with the exact disclaimer string below.

## 4. Non-Sponsorship Disclaimer Requirement

All AMP posts must conclude with the exact text:

> **Disclaimer**: IDE Guide is an independent technical publication. This content is not sponsored, endorsed, or affiliated with any software vendor or editor developer mentioned above. All reviews and assessments are based strictly on objective developer evaluation.
