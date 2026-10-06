# AMP HTML Guidelines for Blogger Posts

This document outlines the strict AMP (Accelerated Mobile Pages) formatting and compliance standards required for all blog post content published to [IDE Guide on Blogger](https://ideguide.blogspot.com/).

## Core AMP Requirements

1. **AMP Root Tag**: Must begin with `<html ⚡>` or `<html amp>` and contain `<head>` and `<body>` sections.
2. **Charset**: Must contain `<meta charset="utf-8">` as the first child of `<head>`.
3. **AMP Runtime Script**: Must include `<script async src="https://cdn.ampproject.org/v0.js"></script>` in `<head>`.
4. **Canonical Link**: Must include `<link rel="canonical" href="...">` pointing to the canonical URL or self-referencing.
5. **Viewport**: Must include `<meta name="viewport" content="width=device-width,minimum-scale=1,initial-scale=1">`.
6. **AMP Boilerplate**: Must include the exact `<style amp-boilerplate>` and `<noscript><style amp-boilerplate>` styles in `<head>`.

## HTML Restrictions & Guidelines

- **No Custom Scripts**: Native `<script>` tags are forbidden, except for AMP extension scripts (e.g., `<script async custom-element="amp-img" src="https://cdn.ampproject.org/v0/amp-img-0.1.js"></script>`).
- **No External Stylesheets**: Style links (`<link rel="stylesheet">`) are prohibited except for authorized custom fonts.
- **Custom Styling**: All custom CSS must be placed in a single `<style amp-custom>` tag inside `<head>` and must not exceed 75KB.
- **Images**: Standard `<img>` tags must be replaced with `<amp-img>` tags specifying `width`, `height`, and appropriate `layout` (e.g., `responsive`).
- **Media**: Use `<amp-video>`, `<amp-iframe>`, or `<amp-youtube>` for embedded media content.

## Mandatory Non-Sponsorship Disclaimer

Every blog post must include the exact disclaimer text in the footer or designated disclaimer section:

> **Disclaimer:** IDE Guide is an independent technical publication. This content is not sponsored, endorsed, or affiliated with any software vendor or editor developer mentioned above. All reviews and assessments are based strictly on objective developer evaluation.
