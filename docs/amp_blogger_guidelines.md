# AMP HTML Guidelines for Blogger Posts

This document specifies the mandatory structure and formatting rules for all AMP (Accelerated Mobile Pages) HTML blog posts generated for [IDE Guide](https://ideguide.blogspot.com/).

## 1. AMP HTML Required Boilerplate

Every generated blog post must be a standalone, valid AMP HTML document containing:

1. `<!doctype html>` declaring HTML5 format.
2. `<html ⚡ lang="en">` or `<html amp lang="en">` root tag.
3. `<head>` and `<body>` tags.
4. `<meta charset="utf-8">` as the first child of `<head>`.
5. `<script async src="https://cdn.ampproject.org/v0.js"></script>` to load the AMP JS library.
6. `<link rel="canonical" href="...">` pointing to the canonical post URL.
7. `<meta name="viewport" content="width=device-width,initial-scale=1,minimum-scale=1,maximum-scale=1,user-scalable=no,minimal-ui">`.
8. AMP Boilerplate code in `<head>`:
   ```html
   <style amp-boilerplate>body{-webkit-animation:-amp-start 8s steps(1,end) 0s 1 normal both;-moz-animation:-amp-start 8s steps(1,end) 0s 1 normal both;-ms-animation:-amp-start 8s steps(1,end) 0s 1 normal both;animation:-amp-start 8s steps(1,end) 0s 1 normal both}@-webkit-keyframes -amp-start{from{visibility:hidden}to{visibility:visible}}@-moz-keyframes -amp-start{from{visibility:hidden}to{visibility:visible}}@-ms-keyframes -amp-start{from{visibility:hidden}to{visibility:visible}}@-o-keyframes -amp-start{from{visibility:hidden}to{visibility:visible}}@keyframes -amp-start{from{visibility:hidden}to{visibility:visible}}</style><noscript><style amp-boilerplate>body{-webkit-animation:none;-moz-animation:none;-ms-animation:none;animation:none}</style></noscript>
   ```
9. Custom CSS inside `<style amp-custom>...</style>`. Maximum size is 75KB.

## 2. AMP Rules & Best Practices

- **No Custom JavaScript**: Custom `<script>` tags are strictly forbidden in AMP.
- **Images**: Plain `<img>` tags are NOT allowed. Always use `<amp-img>` with explicit `width`, `height`, and `layout="responsive"` or `layout="fixed"`.
- **Styling**: Inline `style="..."` attributes are disallowed in AMP. All styles must be defined inside `<style amp-custom>`.

## 3. Required Content Sections

Every IDE review blog post must include:
1. **Header / Introduction**: Name, overview, and targeted developer workflow.
2. **Key Features & Strengths (Pros)**: Highlighting key productivity drivers.
3. **Limitations & Drawbacks (Cons)**: Objective evaluation of pain points.
4. **Pricing Model**: Clear designation of Free, Freemium, Paid, or Open Source licensing.
5. **Verdict & Best For**: Clear target persona recommendations (e.g., Python backend engineers, Flutter developers).
6. **Mandatory Non-Sponsorship Disclaimer**:
   ```
   Disclaimer: IDE Guide is an independent technical publication. This content is not sponsored, endorsed, or affiliated with any software vendor or editor developer mentioned above. All reviews and assessments are based strictly on objective developer evaluation.
   ```
