# AMP HTML Blogger Guidelines for IDE Guide

This document outlines the standard specifications and guidelines for generating AMP (Accelerated Mobile Pages) compliant HTML content for the **IDE Guide** Blogger website ([ideguide.blogspot.com](https://ideguide.blogspot.com/)).

---

## 1. AMP HTML Rules & Requirements

To be valid AMP HTML and render cleanly on mobile devices and Blogger, every post or template must adhere to the following rules:

1. **AMP Root Attribute**: The document root MUST start with `<html ⚡>` or `<html amp>`.
2. **Standard AMP Boilerplate**:
   ```html
   <script async src="https://cdn.ampproject.org/v0.js"></script>
   <style amp-boilerplate>body{-webkit-animation:-amp-start 8s steps(1,end) 0s 1 normal both;-moz-animation:-amp-start 8s steps(1,end) 0s 1 normal both;-ms-animation:-amp-start 8s steps(1,end) 0s 1 normal both;animation:-amp-start 8s steps(1,end) 0s 1 normal both}@-webkit-keyframes -amp-start{from{visibility:hidden}to{visibility:visible}}@-moz-keyframes -amp-start{from{visibility:hidden}to{visibility:visible}}@-ms-keyframes -amp-start{from{visibility:hidden}to{visibility:visible}}@-o-keyframes -amp-start{from{visibility:hidden}to{visibility:visible}}@keyframes -amp-start{from{visibility:hidden}to{visibility:visible}}</style><noscript><style amp-boilerplate>body{-webkit-animation:none;-moz-animation:none;-ms-animation:none;-animation:none}</style></noscript>
   ```
3. **Canonical Link**: Always include a `<link rel="canonical" href="...">` pointing to the main post URL or canonical Blogger URL.
4. **Viewport Meta Tag**: Must contain `<meta name="viewport" content="width=device-width,minimum-scale=1,initial-scale=1">`.
5. **Image Tags**:
   - **DO NOT** use standard HTML `<img>` tags.
   - **ALWAYS** use `<amp-img>` with explicit `width`, `height`, and `layout="responsive"` attributes.
   - Example: `<amp-img src="https://example.com/image.jpg" width="800" height="450" layout="responsive" alt="IDE Interface"></amp-img>`
6. **Custom CSS**:
   - Custom CSS MUST be placed inside a single `<style amp-custom>` tag inside the `<head>`.
   - Max CSS size allowed by AMP spec is 75KB.
   - Avoid disallowed CSS properties like `!important` or filter functions where restricted.

---

## 2. Content Structure for IDE Reviews

Each Blogger post generated for IDE Guide must follow a structured, developer-focused format:

1. **Title & Headline**: Clear overview of the IDE or Editor (e.g., *Cursor IDE Review: Features, Pricing, Pros & Cons*).
2. **Metadata Header**:
   - **Category**: Code Editor / Cloud IDE / AI Editor / Terminal IDE.
   - **Pricing Model**: Free / Paid / Freemium (with exact tier details).
3. **Key Highlights & Core Features**: Highlighting top developer workflows.
4. **Pros & Cons Matrix**: Objective evaluation table.
5. **Verdict & Recommendation**: Who should use this editor and when.
6. **Non-Sponsorship Disclaimer**:
   - Every post MUST end with the explicit disclaimer:
     > **Disclaimer:** IDE Guide is an independent technical publication. This content is not sponsored, endorsed, or affiliated with any software vendor or editor developer mentioned above. All reviews and assessments are based strictly on objective developer evaluation.

---

## 3. Copy-Pasting into Blogger

When publishing generated AMP posts to Blogger:
1. Open Blogger post editor.
2. Switch to **HTML View** (click the pencil icon in top left and select `HTML View`).
3. Paste the entire AMP HTML document output.
4. Publish or save draft.
