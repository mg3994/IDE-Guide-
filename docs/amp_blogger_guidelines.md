# AMP HTML Guidelines for Blogger (IDE Guide)

This document specifies the AMP (Accelerated Mobile Pages) HTML structure and standards required for blog posts published on [IDE Guide Blogger](https://ideguide.blogspot.com/).

## Overview

All blog posts produced for IDE Guide must adhere strictly to AMP HTML standards to ensure lightning-fast mobile loading, optimal search indexing, and a clean reading experience across devices.

## Mandatory AMP HTML Elements

Every post HTML generated must include:

1. **AMP Metadata & Scripts**:
   ```html
   <!doctype html>
   <html ⚡ lang="en">
   <head>
     <meta charset="utf-8">
     <title>IDE Title</title>
     <link rel="canonical" href="https://ideguide.blogspot.com/">
     <meta name="viewport" content="width=device-width,minimum-scale=1,initial-scale=1">
     <script async src="https://cdn.ampproject.org/v0.js"></script>
     <style amp-boilerplate>body{-webkit-animation:-amp-start 8s steps(1,end) 0s 1 normal both;-moz-animation:-amp-start 8s steps(1,end) 0s 1 normal both;-ms-animation:-amp-start 8s steps(1,end) 0s 1 normal both;animation:-amp-start 8s steps(1,end) 0s 1 normal both}@-webkit-keyframes -amp-start{from{visibility:hidden}to{visibility:visible}}@-moz-keyframes -amp-start{from{visibility:hidden}to{visibility:visible}}@-ms-keyframes -amp-start{from{visibility:hidden}to{visibility:visible}}@-o-keyframes -amp-start{from{visibility:hidden}to{visibility:visible}}@keyframes -amp-start{from{visibility:hidden}to{visibility:visible}}</style><noscript><style amp-boilerplate>body{-webkit-animation:none;-moz-animation:none;-ms-animation:none;animation:none}</style></noscript>
     <style amp-custom>
       /* Custom responsive styles */
     </style>
   </head>
   ```

2. **AMP Component Tags**:
   - Images must use `<amp-img src="..." width="..." height="..." layout="responsive" alt="..."></amp-img>`. Standard `<img>` tags are strictly forbidden.
   - Video embeds must use `<amp-youtube>` or `<amp-video>`.
   - Inline `style="..."` attributes on elements are forbidden in strict AMP HTML; styling must reside within `<style amp-custom>`.

3. **Required Post Structure**:
   - **Title & Overview**: High-level introduction to the IDE/Code Editor.
   - **Key Features**: Highlights of developer tools, extensions, AI assistance, and performance.
   - **The Good (Pros)**: Standout benefits and strengths.
   - **The Bad (Cons)**: Drawbacks, performance overhead, or limitations.
   - **Pricing & Licensing**: Clear badge/section defining Free, Freemium, Open Source, or Commercial pricing model.
   - **Best For / Verdict**: Clear guide on which developer persona or use case benefits most.
   - **Mandatory Non-Sponsorship Disclaimer**:
     > Disclaimer: IDE Guide is an independent technical publication. This content is not sponsored, endorsed, or affiliated with any software vendor or editor developer mentioned above. All reviews and assessments are based strictly on objective developer evaluation.

## Blogger Compatibility

For embedding inside Blogger AMP templates:
- Clean semantic HTML structure (`<article>`, `<header>`, `<section>`, `<footer>`).
- Standard CSS custom properties and mobile-first responsive breakpoints.
