from pygments.formatters import HtmlFormatter


def _is_dark(hex_color: str) -> bool:
    c = hex_color.lstrip("#")
    r, g, b = int(c[0:2], 16), int(c[2:4], 16), int(c[4:6], 16)
    return (0.299 * r + 0.587 * g + 0.114 * b) < 128


def render_template(body: str, style: dict) -> str:
    fonts = style["fonts"]
    colors = style["colors"]
    headings = style["headings"]
    code_cfg = style["code"]
    footer_cfg = style["footer"]

    body_font = fonts["body"]
    mono_font = fonts["mono"]

    def resolve_font(name: str) -> str:
        return mono_font if name == "mono" else body_font

    heading_font = resolve_font(headings["font"])
    heading_color = headings.get("color") or colors["primary"]
    uppercase_levels = set(headings.get("uppercase_levels", []))
    color_levels = set(headings.get("color_levels", []))
    sizes = headings["sizes"]

    def hcolor(level: int) -> str:
        if not color_levels or level in color_levels:
            return heading_color
        return colors["muted"] if level == 6 else colors["text"]

    def htransform(level: int) -> str:
        return "uppercase" if level in uppercase_levels else "none"

    formatter = HtmlFormatter(style=code_cfg.get("theme", "github-dark"))
    code_bg = formatter.style.background_color or "#161b22"
    code_text = "#e6edf3" if _is_dark(code_bg) else "#24292f"
    code_border = "#30363d" if _is_dark(code_bg) else "#e1e4e8"
    pygments_css = formatter.get_style_defs(".codehilite")

    google_fonts_link = ""
    if fonts["google_fonts"]:
        families = "&family=".join(
            f.replace(" ", "+") + ":wght@300;400;600;700"
            for f in fonts["google_fonts"]
        )
        google_fonts_link = (
            '<link rel="preconnect" href="https://fonts.googleapis.com">'
            '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
            f'<link href="https://fonts.googleapis.com/css2?family={families}&display=swap" rel="stylesheet">'
        )

    return f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
{google_fonts_link}
<style>
  *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}

  body {{
    font-family: {body_font};
    font-size: 13.5px;
    line-height: 1.7;
    color: {colors["text"]};
    background: {colors["background"]};
    max-width: 860px;
    margin: 0 auto;
    padding: 48px 56px;
  }}

  h1 {{ font-size: {sizes["h1"]}; font-weight: 700; border-bottom: 2px solid #e1e4e8; padding-bottom: 0.3em; margin: 1.5em 0 0.75em; color: {hcolor(1)}; font-family: {heading_font}; text-transform: {htransform(1)}; }}
  h2 {{ font-size: {sizes["h2"]}; font-weight: 600; border-bottom: 1px solid #e1e4e8; padding-bottom: 0.25em; margin: 1.5em 0 0.6em; color: {hcolor(2)}; font-family: {heading_font}; text-transform: {htransform(2)}; }}
  h3 {{ font-size: {sizes["h3"]}; font-weight: 600; margin: 1.3em 0 0.5em; color: {hcolor(3)}; font-family: {heading_font}; text-transform: {htransform(3)}; }}
  h4 {{ font-size: {sizes["h4"]}; font-weight: 600; margin: 1.1em 0 0.4em; color: {hcolor(4)}; font-family: {heading_font}; text-transform: {htransform(4)}; }}
  h5 {{ font-size: {sizes["h5"]}; font-weight: 700; letter-spacing: 0.04em; margin: 1em 0 0.35em; color: {hcolor(5)}; font-family: {heading_font}; text-transform: {htransform(5)}; }}
  h6 {{ font-size: {sizes["h6"]}; font-weight: 600; letter-spacing: 0.04em; margin: 1em 0 0.3em; color: {hcolor(6)}; font-family: {heading_font}; text-transform: {htransform(6)}; }}

  p {{ margin: 0.6em 0; }}
  ul, ol {{ padding-left: 1.8em; margin: 0.5em 0; }}
  li {{ margin: 0.2em 0; }}

  code {{
    font-family: {mono_font};
    font-size: 0.87em;
    background: #f6f8fa;
    border: 1px solid #e1e4e8;
    border-radius: 4px;
    padding: 0.1em 0.35em;
    color: #cf222e;
  }}

  pre {{
    background: {code_bg};
    border-radius: 8px;
    padding: 16px 20px;
    overflow-x: hidden;
    white-space: pre-wrap;
    overflow-wrap: break-word;
    margin: 1em 0;
    border: 1px solid {code_border};
  }}
  pre code {{
    background: transparent;
    border: none;
    padding: 0;
    color: {code_text};
    font-size: 0.84em;
    line-height: 1.6;
    font-family: {mono_font};
  }}

  .codehilite {{ background: {code_bg}; border-radius: 8px; padding: 16px 20px; margin: 1em 0; border: 1px solid {code_border}; overflow-x: hidden; white-space: pre-wrap; overflow-wrap: break-word; }}
  .codehilite pre {{ background: transparent; border: none; padding: 0; margin: 0; }}
  .codehilite code {{ color: {code_text}; font-size: 0.84em; font-family: {mono_font}; }}
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
    color: {colors["text"]};
  }}
  td {{
    border: 1px solid #d0d7de;
    padding: 7px 12px;
    vertical-align: top;
  }}
  tr:nth-child(even) td {{ background: #f6f8fa; }}

  blockquote {{
    border-left: 4px solid {colors["primary"]};
    background: #f0f6ff;
    margin: 1em 0;
    padding: 10px 16px;
    border-radius: 0 6px 6px 0;
    color: {colors["text"]};
  }}
  blockquote p {{ margin: 0.3em 0; }}

  hr {{ border: none; border-top: 1px solid #e1e4e8; margin: 2em 0; }}
  strong {{ font-weight: 600; color: {colors["text"]}; }}

  img {{ max-width: 100%; max-height: 220mm; width: auto; height: auto; }}
  pre, table, blockquote, img, .mermaid {{ page-break-inside: avoid; }}
  h1, h2, h3, h4, h5, h6 {{ page-break-after: avoid; }}

  @page {{ margin: 20mm 18mm; }}
  @media print {{ body {{ padding: 0; max-width: 100%; }} }}
</style>
</head>
<body>
{body}
</body>
<script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
</html>"""
