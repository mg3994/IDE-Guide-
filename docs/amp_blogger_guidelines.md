# AMP Blogger Guidelines for IDE Guide

These guidelines define the specifications for generating Accelerated Mobile Pages (AMP) compliant blog post content tailored specifically for Blogger (`https://ideguide.blogspot.com/`).

---

## 1. Context: AMP in Blogger Post Editor

When publishing content to Blogger via the HTML post editor or automated API:
- Blogger renders posts within its template system. For full AMP compliance or AMP post body compliance, strict HTML restrictions apply.
- Interactive scripts (`<script>`), forbidden HTML tags (`<img>`, `<video>`, `<audio>`, `<iframe>`, `<frame>`), and inline event handlers (`onclick`, `onload`) are prohibited.
- Instead, use AMP components or AMP-safe HTML elements:
  - Use `<amp-img>` instead of `<img>` with explicit `width`, `height`, and `layout="responsive"`.
  - Use `<amp-youtube>` or `<amp-iframe>` for embedded media when needed.
  - No disallowed attributes: `style="..."` is allowed only in modern AMP if kept strictly minimal (or replaced with class styling embedded in `<style amp-custom>`).

---

## 2. Mandatory Rules for Blog Post Bodies

### Allowed HTML Tags
- Headings: `<h1>`, `<h2>`, `<h3>`, `<h4>`
- Structural: `<article>`, `<section>`, `<div>`, `<p>`, `<span>`, `<hr>`
- Lists: `<ul>`, `<ol>`, `<li>`, `<dl>`, `<dt>`, `<dd>`
- Tables: `<table>`, `<thead>`, `<tbody>`, `tr`, `th`, `td`
- Formatting: `<strong>`, `<em>`, `<code>`, `<pre>`, `<blockquote>`, `<mark>`
- AMP media: `<amp-img>` with explicit dimensions

### Disallowed HTML Tags
- `<img>` (Must always be converted to `<amp-img>`)
- `<script>` (No custom JavaScript)
- `<iframe>`, `<embed>`, `<object>` (Use `<amp-iframe>` or `<amp-youtube>` if necessary)
- `<font>`, `<center>`, `<basefont>`

### Required Attributes on Media
Whenever visual elements are included:
```html
<amp-img src="https://example.com/screenshot.webp"
         width="800"
         height="450"
         layout="responsive"
         alt="Code editor interface preview">
</amp-img>
```

---

## 3. Post Content Structure & Template

Every IDE Guide post must adhere to the following semantic structure:

1. **Title & Summary Header**:
   - Clear value proposition (e.g., *Is Cursor Worth It in 2026? Full IDE Breakdown*).
   - Quick specifications badge (Pricing model, supported OS, core engine).

2. **The Good (Strengths & Standout Features)**:
   - Detailed breakdown of developer experience, speed, key extensions, and AI tooling.

3. **The Bad (Drawbacks & Pain Points)**:
   - Objective criticism: memory overhead, telemetry, licensing hurdles, missing features.

4. **Pricing Breakdown (Free vs. Paid)**:
   - Explicit distinction: Completely free, open-source (FOSS), freemium tier, or commercial enterprise subscription.

5. **Who Is It Best For?**:
   - Persona-based recommendations (e.g., frontend developers, systems programmers, data scientists, enterprise teams).

6. **Quick Comparison Table**:
   - Comparing against 1-2 major rivals (e.g., VS Code, Neovim, IntelliJ).

7. **Mandatory Non-Sponsorship Disclaimer**:
   Every post must include the exact disclaimer at the end of the article:
   > "Disclaimer: IDE Guide is an independent technical publication. This content is not sponsored, endorsed, or affiliated with any software vendor or editor developer mentioned above. All reviews and assessments are based strictly on objective developer evaluation."

---

## 4. AMP Validation Checklist
- [ ] No `<img>` tags present (all images use `<amp-img>`).
- [ ] No `<script>` tags embedded in post body.
- [ ] All links (`<a href="...">`) include secure target attributes (`target="_blank" rel="noopener noreferrer"`).
- [ ] Non-sponsorship disclaimer is explicitly included.
- [ ] Semantic headings hierarchy (`h1` -> `h2` -> `h3`).
