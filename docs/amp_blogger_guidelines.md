# AMP HTML Guidelines for Blogger (ideguide.blogspot.com)

This document outlines the strict guidelines and formatting rules for generating Accelerated Mobile Pages (AMP) compliant blog post content for **IDE Guide** on Blogger.

## Why AMP for Blogger?
Blogger supports AMP templates, but the content inside blog post bodies must strictly adhere to AMP HTML specification to ensure instant loading, zero layout shift, and SEO benefits on mobile devices.

## Key Rules for Blogger Post Content

1. **Clean Content-Only HTML Snippet**
   - Blog posts are inserted directly into the Blogger post HTML editor.
   - Do NOT include outer `<!doctype html>`, `<html>`, `<head>`, or `<body>` wrappers inside individual post body content files unless generating standalone AMP preview pages. For Blogger post body snippets, output valid, clean semantic HTML conforming to AMP markup.
   - Include inline `<style amp-custom>` at the top of the post snippet with custom, responsive, lightweight CSS (under 75KB AMP limit).

2. **No Disallowed HTML Elements**
   - **No `<script>` tags** (Blogger template or AMP runtime handles scripts; custom JavaScript inside post body is forbidden by AMP).
   - **No `<form>` or `<input>` tags** without proper AMP components (`amp-form`).
   - **No `<img>` tags**: Always use `<amp-img>` with explicit `width`, `height`, and `layout="responsive"`, along with descriptive `alt` text.
   - **No `<video>` or `<iframe>` tags**: Use `<amp-video>` or `<amp-youtube>` if video embeds are needed.
   - **No inline `style=""` attributes**: All styling must live in `<style amp-custom>`.

3. **Required Semantic Elements & Structure**
   - **Article Title (`<h1>` or `<h2>`)**: Clear, catchy, keyword-rich title highlighting the IDE review.
   - **Meta & Author Badge**: Stating publication by **IDE Guide** (`https://ideguide.blogspot.com/`).
   - **Tool Classification Badge**: Clear display of Pricing Tier (**100% Free / Open-Source**, **Freemium**, or **Paid / Commercial**).
   - **Executive Summary**: Fast 2-minute takeaway on whether the tool is worth adopting.
   - **The Good (Pros)**: Highlighting key features, performance, extension ecosystem, and AI integration.
   - **The Bad (Cons / Drawbacks)**: Objective critique of telemetry, memory usage, cost, learning curve, or bugs.
   - **Who It Is Best For**: Targeted developer persona (e.g., Beginners, Web Devs, Systems Engineers, AI Researchers).
   - **Comparison / Verdict**: Clear recommendation vs competing editors.
   - **Mandatory Non-Sponsorship Disclaimer**:
     > "Disclaimer: IDE Guide is an independent technical publication. This content is not sponsored, endorsed, or affiliated with any software vendor or editor developer mentioned above. All reviews and assessments are based strictly on objective developer evaluation."

4. **AMP Component Compatibility Table**
   | Standard HTML | AMP Equivalent | Requirements |
   | ------------- | -------------- | ------------ |
   | `<img>` | `<amp-img>` | Must define `width`, `height`, `layout="responsive"`, `alt` |
   | `<iframe>` (YouTube) | `<amp-youtube>` | Must specify `data-videoid`, `layout="responsive"`, `width`, `height` |
   | `<style>` | `<style amp-custom>` | Limit to max 75KB, no `!important`, no external CSS `@import` |

5. **Color & Typography Palette**
   - Dark/Modern tech theme: `#0f172a` (slate-900), `#1e293b` (slate-800), `#3b82f6` (blue-500), `#10b981` (emerald-500 for pros), `#ef4444` (red-500 for cons).
   - Clean readable fonts (`system-ui`, `-apple-system`, `sans-serif`).
