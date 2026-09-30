# AMP (Accelerated Mobile Pages) Guidelines for Blogger Posts

## Website Context
- **Blogger URL**: [https://ideguide.blogspot.com/](https://ideguide.blogspot.com/)
- **Daily Frequency**: 3 AMP Blog Posts per day.
- **Focus**: In-depth IDE/Code Editor reviews, comparisons, pros/cons, pricing models (Free vs Paid), and setup guides.

## Strict AMP HTML Rules for Blogger Body Content

When publishing content to Blogger in AMP format, the body markup must strictly adhere to Google AMP HTML standards:

### 1. Tag Restrictions
- **Images**: Use `<amp-img src="..." width="..." height="..." layout="responsive" alt="..."></amp-img>`. Standard `<img>` tags are forbidden.
- **Videos**: Use `<amp-video>` or `<amp-youtube>` components if video embeds are included.
- **Scripts**: Custom inline JavaScript (`<script>` tags) is strictly prohibited except for AMP boilerplate/component scripts.
- **Styles**: Inline `style="..."` attributes are forbidden in AMP. All custom CSS must be scoped within `<style amp-custom>` in the head or contained within clean semantic CSS classes.

### 2. Mandatory Structural Components
Every blog post HTML document or snippet generated must include:
- Clean semantic HTML structure (`<article>`, `<h1>`, `<h2>`, `<section>`, `<ul>`, `<table>`).
- Schema.org Structured Data (`TechArticle` or `BlogPosting` JSON-LD) for SEO enrichment.
- Standard responsive layout attributes on all media elements.

### 3. Content Requirements
Each blog post must contain:
- **Title**: SEO-optimized title containing the IDE name and review focus.
- **Pricing Breakdown**: Explicit section detailing Free tier, Commercial licenses, and Open Source status.
- **Pros & Cons Matrix**: Clean comparative table or list highlighting strengths and weaknesses.
- **Ideal Use Cases**: Guidance on language ecosystem, project scale, and developer experience level.
- **Mandatory Non-Sponsorship Disclaimer**: Explicit disclaimer at the bottom of the article.

## Mandatory Non-Sponsorship Disclaimer

Every AMP blog post MUST include the following exact disclaimer snippet:

```html
<footer class="disclaimer-box">
  <p><strong>Disclaimer:</strong> IDE Guide is an independent technical publication. This content is not sponsored, endorsed, or affiliated with any software vendor or editor developer mentioned above. All reviews and assessments are based strictly on objective developer evaluation.</p>
</footer>
```
