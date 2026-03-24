import pytest
from pathlib import Path
from mdpdf.printer import render_pdf


@pytest.mark.integration
def test_render_pdf_creates_file(tmp_path):
    html = """<!DOCTYPE html>
<html><head><meta charset="utf-8"></head>
<body><h1>Test</h1><p>Hello world</p></body>
</html>"""
    output = tmp_path / "test.pdf"
    render_pdf(html, output)
    assert output.exists()
    assert output.stat().st_size > 1000  # real PDF, not empty


@pytest.mark.integration
def test_render_pdf_a4_format(tmp_path):
    # A4 PDF should be a reasonable size for a simple document
    html = """<!DOCTYPE html>
<html><head><meta charset="utf-8"></head>
<body><h1>Test</h1></body>
</html>"""
    output = tmp_path / "test.pdf"
    render_pdf(html, output)
    size = output.stat().st_size
    assert 1_000 < size < 5_000_000
