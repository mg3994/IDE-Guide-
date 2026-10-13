# AMP (Accelerated Mobile Pages) Blogger Guidelines

This document specifies the formatting rules and structural requirements for generating valid AMP HTML blog posts tailored for Blogger publishing on `https://ideguide.blogspot.com/`.

---

## 1. AMP HTML Structure Requirements

Every generated blog post must strictly adhere to the official AMP standard (`⚡` or `amp` attribute):

```html
<!doctype html>
<html ⚡ lang="en">
<head>
  <meta charset="utf-8">
  <title>Title of Blog Post</title>
  <link rel="canonical" href="https://ideguide.blogspot.com/p/canonical-url.html">
  <meta name="viewport" content="width=device-width,minimum-scale=1,initial-scale=1">
  <style amp-boilerplate>body{-webkit-animation:-amp-start 8s steps(1,end) 0s 1 normal both;-moz-animation:-amp-start 8s steps(1,end) 0s 1 normal both;-ms-animation:-amp-start 8s steps(1,end) 0s 1 normal both;animation:-amp-start 8s steps(1,end) 0s 1 normal both}@-webkit-keyframes -amp-start{from{visibility:hidden}to{visibility:visible}}@-moz-keyframes -amp-start{from{visibility:hidden}to{visibility:visible}}@-ms-keyframes -amp-start{from{visibility:hidden}to{visibility:visible}}@-o-keyframes -amp-start{from{visibility:hidden}to{visibility:visible}}@keyframes -amp-start{from{visibility:hidden}to{visibility:visible}}</style><noscript><style amp-boilerplate>body{-webkit-animation:none;-moz-animation:none;-ms-animation:none;animation:none}</style></noscript>
  <script async src="https://cdn.ampproject.org/v0.js"></script>
  <style amp-custom>
    /* Custom CSS styles go here (under 75KB) */
    body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; line-height: 1.6; color: #1a202c; background: #f7fafc; padding: 20px; }
    .container { max-width: 800px; margin: 0 auto; background: #ffffff; padding: 30px; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); }
    .header-badge { display: inline-block; background: #2b6cb0; color: #fff; font-weight: bold; padding: 4px 12px; border-radius: 4px; font-size: 14px; margin-bottom: 12px; }
    h1 { font-size: 28px; color: #2d3748; margin-top: 0; }
    .meta-box { background: #edf2f7; padding: 16px; border-left: 4px solid #3182ce; border-radius: 4px; margin: 20px 0; }
    .pros-cons { display: flex; gap: 20px; margin: 20px 0; }
    .pro-card { flex: 1; background: #f0fff4; border: 1px solid #c6f6d5; padding: 16px; border-radius: 6px; }
    .con-card { flex: 1; background: #fff5f5; border: 1px solid #fed7d7; padding: 16px; border-radius: 6px; }
    .disclaimer-box { background: #fffaf0; border: 1px solid #feebc8; padding: 16px; border-radius: 6px; font-size: 13px; color: #744210; margin-top: 30px; }
  </style>
</head>
<body>
  <div class="container">
    <!-- AMP Content -->
  </div>
</body>
</html>
```

---

## 2. Mandatory Rules & Constraints

1. **AMP Boilerplate**: Include the exact `<style amp-boilerplate>` and `<script async src="https://cdn.ampproject.org/v0.js"></script>` runtime script.
2. **Prohibited Tags**: Never use `<script>` tags (other than allowed AMP custom elements), `<iframe>`, `<embed>`, `<object>`, or inline `style="..."` attributes on elements.
3. **Images**: Use `<amp-img src="..." width="..." height="..." layout="responsive"></amp-img>` instead of HTML `<img>`.
4. **Styles**: Place custom CSS strictly inside `<style amp-custom>` in the `<head>`. Total CSS size must be under 75KB.
5. **Non-Sponsorship Disclaimer**: Every blog post must prominently display the exact standard disclaimer text:

> **Disclaimer:** IDE Guide is an independent technical publication. This content is not sponsored, endorsed, or affiliated with any software vendor or editor developer mentioned above. All reviews and assessments are based strictly on objective developer evaluation.

---

## 3. Post Content Structure

Each post published on `https://ideguide.blogspot.com/` should contain:

1. **Header & Category Badge**: Target IDE Name and Category.
2. **Executive Overview**: What the IDE is, key features, and vendor details.
3. **Pricing Model**: Free vs Paid breakdown, license details.
4. **Pros & Cons Comparison**: Bullet points covering performance, extension ecosystem, memory usage, and language support.
5. **Ideal Developer Audience**: Who should use this IDE (e.g. frontend, backend, data science, mobile).
6. **Final Verdict**: Recommendation score and overall assessment.
7. **Non-Sponsorship Disclaimer**: Rendered in a dedicated disclaimer box.
