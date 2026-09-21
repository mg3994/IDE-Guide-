"""AMP HTML Generator for IDE Guide Blogger Posts (ideguide.blogspot.com).

Produces fully compliant AMP (Accelerated Mobile Pages) HTML documents for blog posts,
including feature breakdowns, pricing details, pros/cons, and the required non-sponsorship disclaimer.
"""

from typing import Dict, Any, List

DISCLAIMER_TEXT = (
    "Disclaimer: IDE Guide is an independent technical publication. "
    "This content is not sponsored, endorsed, or affiliated with any software vendor "
    "or editor developer mentioned above. All reviews and assessments are based strictly "
    "on objective developer evaluation."
)


def generate_amp_html(ide_info: Dict[str, Any]) -> str:
    """Generates valid AMP HTML string for an IDE review post."""
    name = ide_info.get("name", "Unknown IDE")
    tagline = ide_info.get("tagline", "A powerful code editor for modern developers.")
    description = ide_info.get("description", "A deep dive into features, performance, pricing, and overall developer experience.")
    category = ide_info.get("category", "Code Editor & IDE")
    pricing_type = ide_info.get("pricing_type", "Freemium")  # Free, Paid, Freemium
    pricing_details = ide_info.get("pricing_details", "Free open-source tier available; paid tier for advanced features.")
    features: List[str] = ide_info.get("features", [
        "Intelligent code completion and syntax highlighting",
        "Extensible plugin ecosystem",
        "Integrated terminal and debugging controls",
        "Git and version control integration"
    ])
    pros: List[str] = ide_info.get("pros", ["High performance", "Rich ecosystem", "Active community"])
    cons: List[str] = ide_info.get("cons", ["Resource intensive", "Learning curve for advanced workflows"])
    best_for = ide_info.get("best_for", "Developers looking for a modern and customizable coding environment.")
    canonical_url = ide_info.get("canonical_url", f"https://ideguide.blogspot.com/p/{name.lower().replace(' ', '-')}.html")

    features_li = "".join(f"<li><strong>{f.split(':')[0] if ':' in f else f}</strong>{':' + f.split(':', 1)[1] if ':' in f else ''}</li>" for f in features)
    pros_li = "".join(f"<li class=\"pro-item\">✅ {p}</li>" for p in pros)
    cons_li = "".join(f"<li class=\"con-item\">❌ {c}</li>" for c in cons)

    amp_html = f"""<!doctype html>
<html ⚡ lang="en">
<head>
  <meta charset="utf-8">
  <title>{name} Review & Guide - IDE Guide</title>
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
      max-width: 720px;
      margin: 0 auto;
      padding: 20px 16px;
    }}
    header {{
      background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
      color: #ffffff;
      padding: 32px 20px;
      border-radius: 12px;
      margin-bottom: 24px;
    }}
    .badge {{
      display: inline-block;
      background-color: #0284c7;
      color: #ffffff;
      font-size: 12px;
      font-weight: bold;
      text-transform: uppercase;
      padding: 4px 10px;
      border-radius: 9999px;
      margin-bottom: 12px;
    }}
    h1 {{
      font-size: 28px;
      margin: 0 0 8px 0;
      line-height: 1.2;
    }}
    .tagline {{
      font-size: 16px;
      color: #94a3b8;
      margin: 0;
    }}
    .card {{
      background: #ffffff;
      border-radius: 8px;
      padding: 20px;
      margin-bottom: 20px;
      box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }}
    h2 {{
      font-size: 20px;
      color: #0f172a;
      border-bottom: 2px solid #e2e8f0;
      padding-bottom: 8px;
      margin-top: 0;
    }}
    ul {{
      padding-left: 20px;
      margin: 12px 0;
    }}
    .list-unstyled {{
      padding-left: 0;
    }}
    li {{
      margin-bottom: 8px;
    }}
    .grid {{
      display: flex;
      flex-wrap: wrap;
      gap: 16px;
    }}
    .grid-col {{
      flex: 1 1 280px;
      background: #f1f5f9;
      padding: 16px;
      border-radius: 8px;
    }}
    .pro-item {{
      color: #15803d;
      list-style: none;
    }}
    .con-item {{
      color: #b91c1c;
      list-style: none;
    }}
    .pro-heading {{
      margin-top: 0;
      color: #15803d;
    }}
    .con-heading {{
      margin-top: 0;
      color: #b91c1c;
    }}
    .pricing-badge {{
      display: inline-block;
      font-weight: bold;
      padding: 6px 12px;
      border-radius: 6px;
      background: #e0f2fe;
      color: #0369a1;
      margin-top: 8px;
    }}
    .pricing-text {{
      margin-top: 12px;
    }}
    .disclaimer {{
      background-color: #fef2f2;
      border-left: 4px solid #ef4444;
      padding: 12px 16px;
      font-size: 13px;
      color: #7f1d1d;
      margin-top: 32px;
      border-radius: 4px;
    }}
    footer {{
      text-align: center;
      font-size: 13px;
      color: #64748b;
      margin-top: 24px;
    }}
    .footer-link {{
      color: #0284c7;
    }}
  </style>
</head>
<body>
  <div class="container">
    <header>
      <span class="badge">{category}</span>
      <h1>{name} Complete Review & Guide</h1>
      <p class="tagline">{tagline}</p>
    </header>

    <div class="card">
      <h2>Overview</h2>
      <p>{description}</p>
    </div>

    <div class="card">
      <h2>Key Features</h2>
      <ul>
        {features_li}
      </ul>
    </div>

    <div class="card">
      <h2>Pricing & Accessibility</h2>
      <div class="pricing-badge">Pricing Model: {pricing_type}</div>
      <p class="pricing-text">{pricing_details}</p>
    </div>

    <div class="card">
      <h2>Pros & Cons Breakdown</h2>
      <div class="grid">
        <div class="grid-col">
          <h3 class="pro-heading">Strengths</h3>
          <ul class="list-unstyled">
            {pros_li}
          </ul>
        </div>
        <div class="grid-col">
          <h3 class="con-heading">Drawbacks</h3>
          <ul class="list-unstyled">
            {cons_li}
          </ul>
        </div>
      </div>
    </div>

    <div class="card">
      <h2>Who Should Use {name}?</h2>
      <p>{best_for}</p>
    </div>

    <div class="disclaimer">
      {DISCLAIMER_TEXT}
    </div>

    <footer>
      <p>© IDE Guide - Independent Technical Evaluation & Reviews | <a href="https://ideguide.blogspot.com/" class="footer-link">ideguide.blogspot.com</a></p>
    </footer>
  </div>
</body>
</html>
"""
    return amp_html.strip()
