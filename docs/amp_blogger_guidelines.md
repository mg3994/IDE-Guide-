# AMP HTML Blogger Guidelines for IDE Guide

These guidelines define the Accelerated Mobile Pages (AMP) compliance requirements for blog posts published on [IDE Guide Blogger](https://ideguide.blogspot.com/).

## 1. Core AMP Rules for Blogger Content Body
When creating AMP HTML post content for Blogger:
- Use semantic HTML tags (`<h2>`, `<h3>`, `<p>`, `<ul>`, `<li>`, `<table>`, `<blockquote>`).
- **Do not** use raw HTML `<img>` tags. Use `<amp-img>` with explicit `width`, `height`, and `layout="responsive"`.
- **Do not** use raw `<iframe>` or `<video>` tags. Use `<amp-youtube>` or `<amp-video>` when embedding media.
- **Do not** use inline `style="..."` attributes on elements, as custom inline styling is restricted in strict AMP HTML.
- **Do not** insert custom inline `<script>` tags in post bodies.

## 2. Standard Responsive Media Pattern
```html
<amp-img
  src="https://images.unsplash.com/photo-1555066931-4365d14bab8c"
  width="1200"
  height="675"
  layout="responsive"
  alt="IDE Comparison Screenshot">
</amp-img>
```

## 3. Mandatory Non-Sponsorship Disclaimer
Every post MUST end with the exact non-sponsorship disclaimer text:

> **Disclaimer:** IDE Guide is an independent technical publication. This content is not sponsored, endorsed, or affiliated with any software vendor or editor developer mentioned above. All reviews and assessments are based strictly on objective developer evaluation.
