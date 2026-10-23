# AMP HTML Guidelines for Blogger Posts (IDE Guide)

This document outlines the strict AMP (Accelerated Mobile Pages) HTML requirements and standard structure for blog posts published on [IDE Guide](https://ideguide.blogspot.com/).

## 1. AMP HTML Boilerplate Requirements

All generated blog post content targeting Blogger AMP pages must adhere to the following standards:

1. **AMP Boilerplate Script**: Standard AMP boilerplate `<script async src="https://cdn.ampproject.org/v0.js"></script>` included or assumed by the Blogger AMP template.
2. **Standard HTML Tag Replacement**:
   - `<img>` must be rendered as `<amp-img width="..." height="..." layout="responsive" alt="...">` with explicit width and height attributes.
   - Videos must be embedded using `<amp-youtube>` or `<amp-video>` with valid width, height, and responsive layout parameters.
3. **Allowed Inline Styling**:
   - Use only `<style amp-custom>` for custom CSS rules.
   - Avoid inline `style="..."` attributes on individual tags as forbidden by AMP specifications.
4. **Required Non-Sponsorship Disclaimer**:
   - Every post MUST end with the following exact non-sponsorship disclaimer:
     > **Disclaimer:** IDE Guide is an independent technical publication. This content is not sponsored, endorsed, or affiliated with any software vendor or editor developer mentioned above. All reviews and assessments are based strictly on objective developer evaluation.

## 2. Blog Post Structure

Each AMP blog post generated for an IDE / Code Editor must include:

1. **Title**: Catchy headline focusing on IDE comparison/review (e.g., `VS Code vs Cursor: Is AI Pair Programming Worth the Hype?`).
2. **Overview**: Executive summary of the tool, its primary target audience, and primary use cases.
3. **Key Features & Breakdown**:
   - Technical capabilities & performance benchmarks.
   - Code intelligence / AI integration details.
4. **Pros and Cons**: Balanced evaluation highlighting strengths and limitations.
5. **Pricing & Licensing Model**: Explicit identification of whether the IDE is **Free**, **Paid**, **Freemium**, or **Open Source**.
6. **Verdict & Developer Recommendation**: Clear guidance on who should use it and when to choose alternatives.
7. **Disclaimer**: Non-sponsorship disclaimer block.
