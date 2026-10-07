# AMP HTML Guidelines for Blogger Posts (`https://ideguide.blogspot.com/`)

This document outlines the strict Accelerated Mobile Pages (AMP) standards required for blog posts generated for the IDE Guide Blogger site.

## 1. Required AMP HTML Structure

AMP pages must adhere strictly to the boilerplate specification. For Blogger snippets or embeddable content:

- Must use `<html ⚡>` or `<html amp>`.
- High-level `<head>` must contain:
  - `<meta charset="utf-8">`
  - `<script async src="https://cdn.ampproject.org/v0.js"></script>`
  - `<link rel="canonical" href="...">`
  - `<meta name="viewport" content="width=device-width,minimum-scale=1,initial-scale=1">`
  - Required AMP boilerplate CSS inside `<style amp-boilerplate>` and `<noscript><style amp-boilerplate>`.

## 2. Disallowed HTML Tags

Standard HTML tags that perform external fetches or custom JS are prohibited in AMP:

- ❌ `<img>` -> Use `<amp-img>` with explicit `width`, `height`, and `layout="responsive"`.
- ❌ `<script>` (custom JS) -> Prohibited. Only official AMP extension scripts are allowed in `<head>`.
- ❌ `<iframe>` -> Use `<amp-iframe>` with valid HTTPS src and layout attributes.
- ❌ `<video>` / `<audio>` -> Use `<amp-video>` / `<amp-audio>`.
- ❌ Inline `style="..."` attributes -> Prohibited. All custom CSS must be placed in a single `<style amp-custom>` tag inside `<head>`.

## 3. Allowed Extensions for IDE Guide Posts

- `<script async custom-element="amp-youtube" src="https://cdn.ampproject.org/v0/amp-youtube-0.1.js"></script>`
- `<script async custom-element="amp-img" src="https://cdn.ampproject.org/v0/amp-img-0.1.js"></script>`

## 4. Mandatory Non-Sponsorship Disclaimer

Every AMP blog post must include the following non-sponsorship disclaimer banner at the top or bottom of the post body:

```html
<div class="disclaimer-box">
  <p><strong>Disclaimer:</strong> IDE Guide is an independent technical publication. This content is not sponsored, endorsed, or affiliated with any software vendor or editor developer mentioned above. All reviews and assessments are based strictly on objective developer evaluation.</p>
</div>
```

## 5. CSS Styling Guidelines (`<style amp-custom>`)

- Total custom CSS size must not exceed **50KB**.
- Avoid `!important` flags.
- Use modern responsive layouts with CSS grid/flexbox.
