# AMP HTML Guidelines for Blogger Posts (IDE Guide)

This document outlines the strict HTML and AMP (Accelerated Mobile Pages) standards required for blog post generation targeting `https://ideguide.blogspot.com/`.

## 1. AMP HTML Core Requirements
- **AMP HTML Root**: The document HTML tag must start with `<html ⚡>` or `<html amp>`.
- **Charset & Viewport**:
  - `<meta charset="utf-8">`
  - `<meta name="viewport" content="width=device-width,initial-scale=1,minimum-scale=1,maximum-scale=1,user-scalable=no,minimal-ui">`
- **AMP JS Library**: Must include `<script async src="https://cdn.ampproject.org/v0.js"></script>` in the `<head>`.
- **Canonical Link**: Must contain `<link rel="canonical" href="...">`.
- **AMP Boilerplate CSS**: Mandatory AMP CSS boilerplate script in the `<head>`:
  ```html
  <style amp-boilerplate>body{-webkit-animation:-amp-start 8s steps(1,end) 0s 1 normal both;-moz-animation:-amp-start 8s steps(1,end) 0s 1 normal both;-ms-animation:-amp-start 8s steps(1,end) 0s 1 normal both;animation:-amp-start 8s steps(1,end) 0s 1 normal both}@-webkit-keyframes -amp-start{from{visibility:hidden}to{visibility:visible}}@-moz-keyframes -amp-start{from{visibility:hidden}to{visibility:visible}}@-ms-keyframes -amp-start{from{visibility:hidden}to{visibility:visible}}@-o-keyframes -amp-start{from{visibility:hidden}to{visibility:visible}}@keyframes -amp-start{from{visibility:hidden}to{visibility:visible}}</style><noscript><style amp-boilerplate>body{-webkit-animation:none;-moz-animation:none;-ms-animation:none;animation:none}</style></noscript>
  ```

## 2. Media Tag Rules
- **No standard `<img>` tags**: Standard `<img>` tags are disallowed in AMP. All images must use `<amp-img>` with explicit `width`, `height`, and `layout` attributes (e.g., `layout="responsive"`).
- **Custom Components**: Any extended AMP components (e.g., `<amp-youtube>`, `<amp-carousel>`) must include their respective script loaders in `<head>`.

## 3. Style Rules
- Custom CSS must reside within `<style amp-custom>...</style>` inside `<head>`.
- Total CSS size in `<style amp-custom>` must not exceed **75KB**.
- No `style="..."` inline attributes allowed on HTML elements.
- No external stylesheets via `<link rel="stylesheet">` except for Google Fonts.

## 4. Mandatory Content Sections
Every blog post generated for IDE Guide must contain:
1. **Title & Summary Header**: Concise overview of the IDE or code editor.
2. **Pros (The Good)**: Detailed bullet points highlighting advantages, performance, extensions, and unique features.
3. **Cons (The Bad)**: Objective breakdown of limitations, memory footprint, learning curve, or cost considerations.
4. **Target Audience & Best Use Cases**: Guidance on who should use the tool (e.g., frontend engineers, C++ developers, beginners vs veterans).
5. **Pricing Breakdown**: Clear information on Free tier, Paid subscriptions, Open Source, or Commercial licensing.
6. **Mandatory Non-Sponsorship Disclaimer**:
   ```
   Disclaimer: IDE Guide is an independent technical publication. This content is not sponsored, endorsed, or affiliated with any software vendor or editor developer mentioned above. All reviews and assessments are based strictly on objective developer evaluation.
   ```
