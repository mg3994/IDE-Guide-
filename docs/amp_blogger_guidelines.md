# AMP HTML Guidelines for Blogger Posts

This document defines the AMP (Accelerated Mobile Pages) standards and guidelines for blog posts published on `ideguide.blogspot.com`.

## 1. Core AMP Rules for Blogger

- **No standard `<img>` tags**: Always use `<amp-img>` with explicit `width`, `height`, and `layout="responsive"`.
- **No inline `style` attributes**: All CSS must be placed inside `<style amp-custom>` in the head or contained within clean AMP layout classes.
- **Valid AMP boilerplate**: Ensure the document structure complies with standard AMP HTML specification.
- **Allowed Interactive Components**: `<amp-youtube>`, `<amp-carousel>`, and `<amp-accordion>` when media or expandable content is embedded.

## 2. Post Structure Requirements

Every generated blog post for `ideguide.blogspot.com` must follow this layout structure:

1. **Header & Badges**:
   - Title (e.g., *Cursor IDE Review: Features, Pros & Cons, and Pricing*)
   - Tier Badge: `Free`, `Paid`, or `Freemium (Free tier available)`
   - Category / Language Focus

2. **Overview & Key Features**:
   - Executive summary of the code editor / IDE.
   - Ideal developer audience (e.g., Python, Rust, AI-assisted coding, web dev).

3. **In-Depth Analysis**:
   - Pros (Strengths & Standout Capabilities)
   - Cons (Limitations & Performance/Cost Tradeoffs)
   - Pricing Model & Licensing Breakdown

4. **Verdict & Recommendations**:
   - Comparison with alternative editors.
   - Recommendation on who should use it.

5. **Mandatory Non-Sponsorship Disclaimer**:
   Every post MUST end with the exact disclaimer block:
   > Disclaimer: IDE Guide is an independent technical publication. This content is not sponsored, endorsed, or affiliated with any software vendor or editor developer mentioned above. All reviews and assessments are based strictly on objective developer evaluation.

## 3. AMP Image Example

```html
<amp-img src="https://images.unsplash.com/photo-1555066931-4365d14bab8c"
         width="800"
         height="450"
         layout="responsive"
         alt="Code Editor Visual Overview">
</amp-img>
```
