# AMP Blogger Guidelines for IDE Guide

This document specifies the format, rules, and guidelines for generating AMP (Accelerated Mobile Pages) HTML content tailored for [IDE Guide Blogger Website](https://ideguide.blogspot.com/).

## 1. AMP HTML Compliance Rules

AMP HTML posts published on Blogger must adhere to strict AMP HTML standards to ensure fast loading, mobile optimization, and search engine compatibility:

1. **Standard AMP Boilerplate**:
   - Every post fragment intended for Blogger AMP templates must use custom AMP tags where applicable (e.g., `<amp-img>` instead of `<img>`, `<amp-youtube>` for embedded videos).
   - In-line custom CSS must be scoped appropriately within `<style amp-custom>` blocks if full HTML is included, or use standard inline styling compatible with AMP HTML guidelines.

2. **Image Requirements (`<amp-img>`)**:
   - Standard `<img>` tags are strictly disallowed in AMP HTML.
   - Use `<amp-img src="..." width="..." height="..." layout="responsive" alt="...">` for all screenshots and graphics.
   - Always specify explicit `width` and `height` aspect ratios.

3. **Media Components**:
   - Videos must use `<amp-youtube data-videoid="..." layout="responsive" width="16" height="9"></amp-youtube>` or `<amp-video>`.

4. **Typography and Structured Headings**:
   - Use semantic hierarchy: `<h1>`, `<h2>`, `<h3>`, `<ul>`, `<ol>`, `<p>`.
   - Maintain clear sections for IDE Overview, Features, Pros & Cons, Pricing (Free vs. Paid), Target Audience, and Verdict.

5. **Non-Sponsorship Disclaimer**:
   - Every AMP blog post **MUST** include the following disclaimer block at the bottom:
   ```html
   <div class="disclaimer-box" style="margin-top: 20px; padding: 15px; border-left: 4px solid #f39c12; background-color: #fcf8e3; font-size: 0.9em;">
     <strong>Disclaimer:</strong> IDE Guide is an independent technical publication. This content is not sponsored, endorsed, or affiliated with any software vendor or editor developer mentioned above. All reviews and assessments are based strictly on objective developer evaluation.
   </div>
   ```

## 2. Post Structure Template

Each daily blog post generated for Blogger should follow this structure:

- **Title**: `[IDE Name] Review: Features, Pros & Cons, and Pricing Guide`
- **Header Badge**: Tagging pricing model (Free / Paid / Freemium)
- **Overview**: Elevator pitch and primary focus.
- **Key Features**: Bulleted breakdown of standout capabilities.
- **Pros & Cons Table or Comparison List**: Clear evaluation for developer decision-making.
- **Pricing & Licensing**: Explicit details on free tiers, trial versions, or commercial license costs.
- **Who Should Use It**: Ideal audience recommendations (e.g., frontend engineers, C++ developers, DevOps).
- **Disclaimer**: Mandatory non-sponsorship disclosure.
