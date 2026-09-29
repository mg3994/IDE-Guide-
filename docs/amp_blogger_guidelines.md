# AMP Blogger Guidelines for IDE Guide

This document outlines the standard specification for generating AMP (Accelerated Mobile Pages) compliant HTML content for the **IDE Guide** Blogger publication (`https://ideguide.blogspot.com/`).

## 1. AMP HTML Rules & Requirements

All blog post outputs targeting Blogger must adhere strictly to AMP HTML standards:

- **Root Tag:** Must start with `<html ⚡>` or `<html amp>` and include `lang="en"`.
- **Head Requirements:**
  - `<meta charset="utf-8">` as the first child of `<head>`.
  - `<script async src="https://cdn.ampproject.org/v0.js"></script>` included in the head.
  - `<link rel="canonical" href="...">` pointing to the canonical URL or target blog post URL.
  - `<meta name="viewport" content="width=device-width,minimum-scale=1,initial-scale=1">`.
  - `<style amp-boilerplate>` and `<noscript><style amp-boilerplate>...</style></noscript>` styles included.
- **Image Tags:**
  - Must use `<amp-img>` instead of standard `<img>` tags.
  - Required attributes: `src`, `width`, `height`, `layout="responsive"`, `alt`.
- **CSS Rules:**
  - Custom CSS must be enclosed within a single `<style amp-custom>` block in the head.
  - Inline `style="..."` attributes are strictly prohibited.
  - Maximum CSS size must not exceed 75KB.
- **External Scripts:** No unauthorized external JavaScript files or inline `<script>` tags allowed.

## 2. Article Content Structure

Every daily IDE review blog post on IDE Guide follows a structured layout:

1. **Header & Metadata:** Title, Target Audience, Last Updated Date, Category (Paid / Free / Freemium).
2. **Overview:** Introduction to the IDE/Code Editor, primary programming languages supported, and key audience.
3. **Key Features:** Deep dive into top 3-5 core capabilities (e.g., AI autocomplete, debugging, extensions, performance).
4. **Pros and Cons:** Balanced objective analysis table or bullet points.
5. **Pricing & Licensing:** Detailed breakdown of Free tier, Commercial pricing, or Subscription models.
6. **Verdict & Recommendations:** Guidance on who should use the IDE (e.g., Beginners, Enterprise, Backend Engineers).
7. **Mandatory Non-Sponsorship Disclaimer:** Positioned prominently at the end of the post.

## 3. Mandatory Non-Sponsorship Disclaimer

Every AMP blog post generated for IDE Guide MUST conclude with the following exact disclaimer text:

> **Disclaimer:** IDE Guide is an independent technical publication. This content is not sponsored, endorsed, or affiliated with any software vendor or editor developer mentioned above. All reviews and assessments are based strictly on objective developer evaluation.
