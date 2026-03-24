from mdpdf.template import render_template


def test_render_template_returns_html_document():
    html = render_template("<p>hello</p>")
    assert "<!DOCTYPE html>" in html
    assert "<html>" in html
    assert "<body>" in html
    assert "</body>" in html


def test_render_template_injects_body():
    html = render_template("<p>test content</p>")
    assert "<p>test content</p>" in html


def test_render_template_includes_mermaid_cdn():
    html = render_template("")
    assert "cdn.jsdelivr.net/npm/mermaid@10" in html


def test_render_template_includes_pagination_css():
    html = render_template("")
    assert "page-break-inside: avoid" in html
    assert "page-break-after: avoid" in html


def test_render_template_includes_dark_code_theme():
    html = render_template("")
    assert "#161b22" in html


def test_render_template_includes_table_styles():
    html = render_template("")
    assert "border-collapse: collapse" in html


def test_render_template_includes_blockquote_styles():
    html = render_template("")
    assert "border-left" in html
