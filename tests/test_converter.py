from mdpdf.converter import convert


def test_convert_heading():
    html = convert("# Hello World")
    assert "<h1" in html
    assert "Hello World" in html


def test_convert_h2():
    html = convert("## Section")
    assert "<h2" in html


def test_convert_paragraph():
    html = convert("Just some text here.")
    assert "<p>" in html
    assert "Just some text here." in html


def test_convert_bold():
    html = convert("**bold text**")
    assert "<strong>" in html
    assert "bold text" in html


def test_convert_table():
    md = "| Name | Value |\n|------|-------|\n| foo  | bar   |"
    html = convert(md)
    assert "<table>" in html
    assert "<th>" in html or 'scope="col"' in html
    assert "<td>" in html


def test_convert_blockquote():
    html = convert("> This is a note")
    assert "<blockquote>" in html
    assert "This is a note" in html


def test_convert_code_block_highlighted():
    html = convert("```python\nprint('hello')\n```")
    # codehilite wraps in a div with class codehilite
    assert "codehilite" in html
    # The code content appears somewhere in the output
    assert "print" in html


def test_convert_inline_code():
    html = convert("Use `foo()` to do it")
    assert "<code>" in html
    assert "foo()" in html


def test_convert_unordered_list():
    html = convert("- item one\n- item two")
    assert "<ul>" in html
    assert "<li>" in html
    assert "item one" in html


def test_convert_horizontal_rule():
    html = convert("---")
    assert "<hr" in html


def test_convert_mermaid_fence_becomes_div():
    md = "```mermaid\ngraph TD\n  A --> B\n```"
    html = convert(md)
    assert '<div class="mermaid">' in html
    assert "graph TD" in html
    assert "A --> B" in html


def test_convert_mermaid_no_pre_wrapper():
    md = "```mermaid\ngraph TD\n  A --> B\n```"
    html = convert(md)
    # mermaid block should not be inside a <pre> tag
    assert "<pre>" not in html


def test_convert_mermaid_does_not_get_syntax_highlighted():
    md = "```mermaid\ngraph TD\n  A --> B\n```"
    html = convert(md)
    # codehilite wrapper class must not appear around mermaid content
    assert "codehilite" not in html


def test_convert_multiple_mermaid_blocks():
    md = "```mermaid\ngraph TD\n  A --> B\n```\n\nSome text\n\n```mermaid\nsequenceDiagram\n  A->>B: Hello\n```"
    html = convert(md)
    assert html.count('<div class="mermaid">') == 2
    assert "graph TD" in html
    assert "sequenceDiagram" in html


def test_convert_mermaid_mixed_with_code():
    md = "```python\nprint('hi')\n```\n\n```mermaid\ngraph TD\n  A --> B\n```"
    html = convert(md)
    assert "codehilite" in html          # python block is highlighted
    assert '<div class="mermaid">' in html  # mermaid block is a div
