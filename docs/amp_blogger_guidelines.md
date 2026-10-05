# AMP HTML Guidelines for Blogger (ideguide.blogspot.com)

This document provides technical guidelines and formatting standards for generating AMP (Accelerated Mobile Pages) compliant HTML content specifically tailored for Blogger posts published on [IDE Guide](https://ideguide.blogspot.com/).

---

## 1. AMP HTML Rules & Boilerplate Structure

All generated blog posts must strictly adhere to valid AMP HTML markup:

1. **Document Declaration**: Must start with `<!doctype html>`.
2. **AMP Tag**: The root element must be `<html ⚡>` or `<html amp>`.
3. **Encoding & Viewport**:
   - `<meta charset="utf-8">` as the first child of `<head>`.
   - `<meta name="viewport" content="width=device-width,initial-scale=1,minimum-scale=1">`.
4. **Canonical Tag**: Must include `<link rel="canonical" href="CANONICAL_URL">` pointing to the canonical post URL or self-referential link.
5. **AMP Script**: Must load the AMP runtime script `<script async src="https://cdn.ampproject.org/v0.js"></script>` in `<head>`.
6. **AMP Boilerplate Code**: Must include the standard AMP boilerplate style block in `<head>`:
   ```html
   <style amp-boilerplate>body{-webkit-animation:-amp-start 8s steps(1,end) 0s 1 normal both;-moz-animation:-amp-start 8s steps(1,end) 0s 1 normal both;-ms-animation:-amp-start 8s steps(1,end) 0s 1 normal both;animation:-amp-start 8s steps(1,end) 0s 1 normal both}@-webkit-keyframes -amp-start{from{visibility:hidden}to{visibility:visible}}@-moz-keyframes -amp-start{from{visibility:hidden}to{visibility:visible}}@-ms-keyframes -amp-start{from{visibility:hidden}to{visibility:visible}}@-o-keyframes -amp-start{from{visibility:hidden}to{visibility:visible}}@keyframes -amp-start{from{visibility:hidden}to{visibility:visible}}</style><noscript><style amp-boilerplate>body{-webkit-animation:none;-moz-animation:none;-ms-animation:none;animation:none}</style></noscript>
   ```

---

## 2. CSS & Layout Constraints

- **Custom Styles**: All CSS must be placed inside a single `<style amp-custom>` tag in `<head>`.
- **CSS Size Limit**: Maximum CSS size allowed is 50KB.
- **Prohibited CSS**:
  - No external stylesheets via `<link rel="stylesheet">` (except custom fonts).
  - No `!important` declarations in custom CSS.
  - No inline `style="..."` attributes on elements.
- **Responsive Layout**: Use flexbox or CSS grid with percentage-based or fluid sizing.

---

## 3. AMP Component Specifications

- **Images (`<amp-img>`)**:
  - Regular `<img>` tags are strictly forbidden. Use `<amp-img>`.
  - Always provide explicit `width`, `height`, `layout="responsive"`, and `alt` attributes.
  - Example: `<amp-img src="https://example.com/image.png" width="800" height="450" layout="responsive" alt="Editor UI"></amp-img>`
- **Videos & Embeds**:
  - YouTube embeds must use `<amp-youtube video-id="..." layout="responsive" width="480" height="270"></amp-youtube>` along with `<script async custom-element="amp-youtube" src="https://cdn.ampproject.org/v0.js/v1/amp-youtube-0.1.js"></script>`.
- **No Custom JavaScript**: Custom `<script>` tags are strictly forbidden except for approved AMP components.

---

## 4. Blog Post Content Structure

Each IDE Guide blog post must follow this consistent template:

1. **Header / Title**: Clear, engaging title including the IDE / Code Editor name.
2. **Metadata Header**: Publication date, target audience, pricing tier tag (Free / Paid / Freemium).
3. **Executive Summary**: Brief 2-3 sentence overview of the editor's primary positioning.
4. **Core Features Breakdown**: Highlighting 3-5 unique features (AI capabilities, speed, extension ecosystem, terminal integration, debugging, etc.).
5. **Pricing Analysis**: Honest evaluation of pricing plans, free tiers, trial constraints, or paid enterprise licenses.
6. **Pros & Cons Table or List**:
   - **Pros**: Key strengths and advantages.
   - **Cons**: Drawbacks, performance limitations, or missing functionality.
7. **Developer Verdict**: Guidance on who should use this IDE (e.g., beginner web developers, C++ systems engineers, AI power users).
8. **Mandatory Non-Sponsorship Disclaimer**: Every blog post MUST end with the explicit disclaimer:
   > *Disclaimer: IDE Guide is an independent technical publication. This content is not sponsored, endorsed, or affiliated with any software vendor or editor developer mentioned above. All reviews and assessments are based strictly on objective developer evaluation.*
