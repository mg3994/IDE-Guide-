import os
from scripts.ide_guide_agent_skill import build_custom_ide_data
from scripts.generate_daily_content import generate_amp_blog_post, generate_google_flow_spec
from scripts.amp_validator import validate_amp_html

def test_agent_skill_data():
    custom = build_custom_ide_data("Lapce Editor", repo_url="https://github.com/lapce/lapce", pricing="Open Source")
    assert custom["id"] == "lapce_editor"
    assert custom["name"] == "Lapce Editor"
    assert custom["pricing_type"] == "Open Source"
    assert "https://github.com/lapce/lapce" in custom["price_detail"]

    blog_html = generate_amp_blog_post(custom)
    is_valid, errors = validate_amp_html(blog_html)
    assert is_valid, f"Custom blog post failed AMP validation: {errors}"

    flow_spec = generate_google_flow_spec(custom)
    assert flow_spec["ide_metadata"]["id"] == "lapce_editor"
