# AMP HTML Guidelines for Blogger (IDE Guide)

Target Blog: [IDE Guide Blogspot](https://ideguide.blogspot.com/)

## 1. Overview
All blog posts generated for `ideguide.blogspot.com` must strictly comply with the Accelerated Mobile Pages (AMP) HTML specification. AMP HTML ensures lightning-fast page loads on mobile devices and optimal SEO indexing.

## 2. Mandatory AMP HTML Structural Rules
Every AMP post HTML document must include:
1. `<html ⚡>` or `<html amp>` as the root tag.
2. `<head>` and `<body>` tags.
3. `<meta charset="utf-8">` as the first child of `<head>`.
4. `<script async src="https://cdn.ampproject.org/v0.js"></script>` inside `<head>`.
5. `<link rel="canonical" href="...">` pointing to the canonical URL or original post link.
6. `<meta name="viewport" content="width=device-width,minimum-scale=1,initial-scale=1">` inside `<head>`.
7. AMP Boilerplate CSS in `<head>`:
```html
<style amp-boilerplate>body{-webkit-animation:-amp-start 8s steps(1,end) 0s 1 normal both;-moz-animation:-amp-start 8s steps(1,end) 0s 1 normal both;-ms-animation:-amp-start 8s steps(1,end) 0s 1 normal both;animation:-amp-start 8s steps(1,end) 0s 1 normal both}@-webkit-keyframes -amp-start{from{visibility:hidden}to{visibility:visible}}@-moz-keyframes -amp-start{from{visibility:hidden}to{visibility:visible}}@-ms-keyframes -amp-start{from{visibility:hidden}to{visibility:visible}}@-o-keyframes -amp-start{from{visibility:hidden}to{visibility:visible}}@keyframes -amp-start{from{visibility:hidden}to{visibility:visible}}</style><noscript><style amp-boilerplate>body{-webkit-animation:none;-moz-animation:none;-ms-animation:none;animation:none}</style></noscript>
```

## 3. Disallowed Elements & Prohibited Constructs
- **NO standard `<img>` tags**: Use `<amp-img src="..." width="..." height="..." layout="responsive" alt="..."></amp-img>`.
- **NO custom `<script>` tags**: Only official AMP scripts (`cdn.ampproject.org`) are allowed.
- **NO external stylesheets**: Inline CSS only inside `<style amp-custom>`.
- **NO `style="..."` inline attributes** on HTML tags.
- **NO `!important` qualifiers** in custom CSS.

## 4. Blog Post Structure Requirements
Each daily IDE post must contain:
1. **Title & Subtitle**: Clear naming of the IDE / Code Editor.
2. **At-a-Glance Summary Table**:
   - License (Open Source / Proprietary / Freemium)
   - Pricing (Free tier vs Paid subscription details)
   - Supported Platforms (Windows, macOS, Linux, Web)
   - Key Ecosystem Strengths
3. **In-Depth Analysis**:
   - Standout Features & Performance Breakdown
   - Pros vs. Cons
4. **Who Should Use It**: Tailored developer persona recommendations.
5. **Mandatory Non-Sponsorship Disclaimer**:
   > **Disclaimer**: IDE Guide is an independent technical publication. This content is not sponsored, endorsed, or affiliated with any software vendor or editor developer mentioned above. All reviews and assessments are based strictly on objective developer evaluation.
