from pygments.formatters import HtmlFormatter


def render_template(body: str) -> str:
    pygments_css = HtmlFormatter(style="github-dark").get_style_defs(".codehilite")

    return f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}

  body {{
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
    font-size: 13.5px;
    line-height: 1.7;
    color: #24292f;
    max-width: 860px;
    margin: 0 auto;
    padding: 48px 56px;
  }}

  h1 {{ font-size: 2em; font-weight: 700; border-bottom: 2px solid #e1e4e8; padding-bottom: 0.3em; margin: 1.5em 0 0.75em; color: #0d1117; }}
  h2 {{ font-size: 1.45em; font-weight: 600; border-bottom: 1px solid #e1e4e8; padding-bottom: 0.25em; margin: 1.5em 0 0.6em; color: #0d1117; }}
  h3 {{ font-size: 1.15em; font-weight: 600; margin: 1.3em 0 0.5em; color: #0d1117; }}
  h4 {{ font-size: 1em; font-weight: 600; margin: 1.1em 0 0.4em; color: #0d1117; }}

  p {{ margin: 0.6em 0; }}
  ul, ol {{ padding-left: 1.8em; margin: 0.5em 0; }}
  li {{ margin: 0.2em 0; }}

  code {{
    font-family: "SFMono-Regular", Consolas, "Liberation Mono", Menlo, monospace;
    font-size: 0.87em;
    background: #f6f8fa;
    border: 1px solid #e1e4e8;
    border-radius: 4px;
    padding: 0.1em 0.35em;
    color: #cf222e;
  }}

  pre {{
    background: #161b22;
    border-radius: 8px;
    padding: 16px 20px;
    overflow-x: auto;
    margin: 1em 0;
    border: 1px solid #30363d;
  }}
  pre code {{
    background: transparent;
    border: none;
    padding: 0;
    color: #e6edf3;
    font-size: 0.84em;
    line-height: 1.6;
  }}

  .codehilite {{ background: #161b22; border-radius: 8px; padding: 16px 20px; margin: 1em 0; border: 1px solid #30363d; overflow-x: auto; }}
  .codehilite pre {{ background: transparent; border: none; padding: 0; margin: 0; }}
  .codehilite code {{ color: #e6edf3; font-size: 0.84em; }}
  {pygments_css}

  table {{
    border-collapse: collapse;
    width: 100%;
    margin: 1em 0;
    font-size: 0.9em;
  }}
  th {{
    background: #f6f8fa;
    border: 1px solid #d0d7de;
    padding: 8px 12px;
    text-align: left;
    font-weight: 600;
    color: #0d1117;
  }}
  td {{
    border: 1px solid #d0d7de;
    padding: 7px 12px;
    vertical-align: top;
  }}
  tr:nth-child(even) td {{ background: #f6f8fa; }}

  blockquote {{
    border-left: 4px solid #0969da;
    background: #f0f6ff;
    margin: 1em 0;
    padding: 10px 16px;
    border-radius: 0 6px 6px 0;
    color: #24292f;
  }}
  blockquote p {{ margin: 0.3em 0; }}

  hr {{ border: none; border-top: 1px solid #e1e4e8; margin: 2em 0; }}
  strong {{ font-weight: 600; color: #0d1117; }}

  pre, table, blockquote, img, .mermaid {{ page-break-inside: avoid; }}
  h1, h2, h3, h4 {{ page-break-after: avoid; }}

  @page {{ margin: 20mm 18mm; }}
  @media print {{ body {{ padding: 0; max-width: 100%; }} }}
</style>
</head>
<body>
{body}
</body>
<script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
</html>"""
