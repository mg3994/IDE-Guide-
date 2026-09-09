"""
AMP HTML Blog Post Generator for Blogger (ideguide.blogspot.com)
Generates Accelerated Mobile Pages (AMP) compliant HTML posts for IDE Guide.
"""

from typing import Dict, Any

DISCLAIMER_TEXT = (
    "Disclaimer: IDE Guide is an independent technical publication. "
    "This content is not sponsored, endorsed, or affiliated with any software vendor "
    "or editor developer mentioned above. All reviews and assessments are based strictly "
    "on objective developer evaluation."
)

def generate_amp_blog_post(ide_data: Dict[str, Any], canonical_url: str = "") -> str:
    """Generate a complete, valid AMP HTML blog post for an IDE review."""
    name = ide_data.get("name", "IDE Review")
    slug = ide_data.get("slug", "ide-review")
    developer = ide_data.get("developer", "Independent Developer")
    license_type = ide_data.get("license_type", "Free / Open Source")
    pricing = ide_data.get("pricing", "Free")
    website = ide_data.get("website", "")
    github_repo = ide_data.get("github_repo", "")
    description = ide_data.get("description", "")
    key_features = ide_data.get("key_features", [])
    pros = ide_data.get("pros", [])
    cons = ide_data.get("cons", [])
    target_audience = ide_data.get("target_audience", "Developers & Engineers")
    verdict_rating = ide_data.get("verdict_rating", "9.0/10")
    verdict_summary = ide_data.get("verdict_summary", "A solid code editor for modern software development.")

    if not canonical_url:
        canonical_url = f"https://ideguide.blogspot.com/p/{slug}.html"

    features_list_html = "".join([f"<li><strong>{feat}</strong></li>" for feat in key_features])
    pros_list_html = "".join([f"<li>✅ {pro}</li>" for pro in pros])
    cons_list_html = "".join([f"<li>⚠️ {con}</li>" for con in cons])

    repo_html = ""
    if github_repo:
        repo_html = f'<p><strong>GitHub Repository:</strong> <a href="{github_repo}" target="_blank" rel="noopener">{github_repo}</a></p>'

    website_html = ""
    if website:
        website_html = f'<p><strong>Official Website:</strong> <a href="{website}" target="_blank" rel="noopener">{website}</a></p>'

    amp_html = f"""<!DOCTYPE html>
<html ⚡ lang="en">
<head>
  <meta charset="utf-8">
  <title>{name} Review & Guide - Best Code Editors | IDE Guide</title>
  <link rel="canonical" href="{canonical_url}">
  <meta name="viewport" content="width=device-width,minimum-scale=1,initial-scale=1">
  <script async src="https://cdn.ampproject.org/v0.js"></script>
  <style amp-boilerplate>body{{-webkit-animation:-amp-start 8s steps(1,end) 0s 1 normal both;-moz-animation:-amp-start 8s steps(1,end) 0s 1 normal both;-ms-animation:-amp-start 8s steps(1,end) 0s 1 normal both;animation:-amp-start 8s steps(1,end) 0s 1 normal both}}@-webkit-keyframes -amp-start{{from{{visibility:hidden}}to{{visibility:visible}}}}@-moz-keyframes -amp-start{{from{{visibility:hidden}}to{{visibility:visible}}}}@-ms-keyframes -amp-start{{from{{visibility:hidden}}to{{visibility:visible}}}}@-o-keyframes -amp-start{{from{{visibility:hidden}}to{{visibility:visible}}}}@keyframes -amp-start{{from{{visibility:hidden}}to{{visibility:visible}}}}</style><noscript><style amp-boilerplate>body{{-webkit-animation:none;-moz-animation:none;-ms-animation:none;animation:none}}</style></noscript>
  <style amp-custom>
    body {{
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
      line-height: 1.6;
      color: #1e293b;
      background-color: #f8fafc;
      margin: 0;
      padding: 0;
    }}
    .container {{
      max-width: 800px;
      margin: 0 auto;
      padding: 20px;
      background-color: #ffffff;
      box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
      border-radius: 8px;
    }}
    header {{
      border-bottom: 3px solid #3b82f6;
      padding-bottom: 15px;
      margin-bottom: 25px;
    }}
    h1 {{
      color: #0f172a;
      font-size: 2rem;
      margin: 0 0 10px 0;
    }}
    .meta-badge {{
      display: inline-block;
      background-color: #e0f2fe;
      color: #0369a1;
      padding: 4px 10px;
      border-radius: 12px;
      font-size: 0.875rem;
      font-weight: 600;
      margin-right: 8px;
    }}
    .hero-img {{
      margin: 20px 0;
      border-radius: 8px;
      overflow: hidden;
    }}
    .section-title {{
      color: #1e3a8a;
      border-left: 4px solid #3b82f6;
      padding-left: 10px;
      font-size: 1.4rem;
      margin-top: 30px;
      margin-bottom: 15px;
    }}
    .good-box {{
      background-color: #f0fdf4;
      border-left: 4px solid #22c55e;
      padding: 15px;
      border-radius: 4px;
      margin-bottom: 20px;
    }}
    .bad-box {{
      background-color: #fff1f2;
      border-left: 4px solid #f43f5e;
      padding: 15px;
      border-radius: 4px;
      margin-bottom: 20px;
    }}
    ul {{
      padding-left: 20px;
    }}
    li {{
      margin-bottom: 8px;
    }}
    .verdict-card {{
      background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
      color: #ffffff;
      padding: 20px;
      border-radius: 8px;
      margin-top: 30px;
      text-align: center;
    }}
    .verdict-score {{
      font-size: 2.5rem;
      font-weight: bold;
      color: #38bdf8;
    }}
    .disclaimer-box {{
      margin-top: 40px;
      padding: 15px;
      background-color: #f1f5f9;
      border: 1px solid #cbd5e1;
      border-radius: 6px;
      font-size: 0.85rem;
      color: #475569;
      font-style: italic;
    }}
    a {{
      color: #2563eb;
      text-decoration: none;
    }}
    a:hover {{
      text-decoration: underline;
    }}
  </style>
</head>
<body>
  <div class="container">
    <header>
      <h1>{name}: Comprehensive Developer Review & Features Guide</h1>
      <div>
        <span class="meta-badge">Developer: {developer}</span>
        <span class="meta-badge">License: {license_type}</span>
        <span class="meta-badge">Price: {pricing}</span>
      </div>
    </header>

    <div class="hero-img">
      <amp-img src="https://images.unsplash.com/photo-1555066931-4365d14bab8c?w=800&auto=format&fit=crop&q=80"
               width="800"
               height="400"
               layout="responsive"
               alt="{name} IDE Review Visual"></amp-img>
    </div>

    <section>
      <h2 class="section-title">Overview</h2>
      <p>{description}</p>
      {website_html}
      {repo_html}
    </section>

    <section>
      <h2 class="section-title">Key Capabilities & Features</h2>
      <ul>
        {features_list_html}
      </ul>
    </section>

    <section>
      <h2 class="section-title">The Good (Pros)</h2>
      <div class="good-box">
        <ul>
          {pros_list_html}
        </ul>
      </div>
    </section>

    <section>
      <h2 class="section-title">The Bad (Cons)</h2>
      <div class="bad-box">
        <ul>
          {cons_list_html}
        </ul>
      </div>
    </section>

    <section>
      <h2 class="section-title">Who Is {name} Best For?</h2>
      <p>{target_audience}</p>
    </section>

    <div class="verdict-card">
      <h3>IDE Guide Rating & Verdict</h3>
      <div class="verdict-score">{verdict_rating}</div>
      <p>{verdict_summary}</p>
    </div>

    <div class="disclaimer-box">
      {DISCLAIMER_TEXT}
    </div>
  </div>
</body>
</html>"""
    return amp_html
