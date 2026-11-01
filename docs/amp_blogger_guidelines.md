# Accelerated Mobile Pages (AMP) Blogger Post Guidelines

This document specifies the engineering requirements for generating **AMP HTML** blog posts compatible with Google Blogger (`https://ideguide.blogspot.com/`).

---

## 1. Core AMP Rules for Blogger

Blogger posts are rendered within Blogger's layout engine. When outputting AMP-compliant blog content:

1. **No External or Inline JavaScript**:
   - Never inject custom `<script>` tags, event handlers (`onclick`, `onload`), or interactive JS.
   - Only validated AMP component scripts are allowed (if included in post template). For blogger post content, rely on clean, valid AMP markup.
2. **AMP Image Elements (`<amp-img>`)**:
   - Replace standard `<img>` tags with `<amp-img>` specifying explicit `width`, `height`, and `layout="responsive"`.
   - Always supply descriptive `alt` text for accessibility.
   - Example:
     ```html
     <amp-img src="https://images.unsplash.com/photo-..."
              width="1200"
              height="675"
              layout="responsive"
              alt="Visual Studio Code Interface Review">
     </amp-img>
     ```
3. **No Forbidden Tags**:
   - Strictly avoid: `<iframe class="...">` (must use `<amp-iframe>` with dimensions if needed), `<frame>`, `<object>`, `<embed>`, `<applet>`.
4. **Style Restrictions**:
   - In standard AMP pages, styling belongs in `<style amp-custom>`.
   - In Blogger post HTML snippets, scoped clean inline CSS rules within standard elements or semantic tags (`<div class="...">`, `<section>`, `<header>`, `<footer>`) must be used without `!important` or disallowed CSS pseudo-elements.
5. **Semantic Hierarchy**:
   - Every post must include an `<h1>` post title, structured `<h2>` and `<h3>` section headers, semantic lists (`<ul>`, `<ol>`), and `<p>` blocks.
6. **Mandatory Non-Sponsorship Disclaimer**:
   - Every post must visibly present the independent disclaimer:
   > *"Disclaimer: IDE Guide is an independent technical publication. This content is not sponsored, endorsed, or affiliated with any software vendor or editor developer mentioned above. All reviews and assessments are based strictly on objective developer evaluation."*

---

## 2. Recommended Article Blueprint

Every generated Blogger AMP post follows this structure:

1. **Header Block**: Title, publication metadata, badges (Pricing, Platform, Rating).
2. **Hero Section**: Responsive `<amp-img>` with high-contrast badge overlays.
3. **Executive Summary**: 2-3 sentence overview of what the tool is and why developers should care.
4. **Pricing Breakdown Table / Card**:
   - Clear distinction between **Free**, **Paid**, **Freemium**, or **Open Source**.
   - Hidden costs, subscription fees, or cloud credit caps explained.
5. **Pros & Cons Matrix**: Balanced analysis of engineering advantages and current limitations.
6. **Core Technical Highlights**: In-depth inspection of standout features.
7. **Who Should Use It**: Concrete target audience scenarios.
8. **Verdict & Score**: Transparent numerical score and definitive editorial verdict.
9. **Official Channel Links & Disclaimer**:
   - YouTube: `https://www.youtube.com/@IDEguide`
   - Independent non-sponsorship disclosure.
