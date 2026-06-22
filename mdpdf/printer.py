import base64
import re
import tempfile
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

from playwright.sync_api import sync_playwright


_EXT_IMG_RE = re.compile(r'(<img\b[^>]*\s)src="(https?://[^"]+)"')
_GF_CSS_RE = re.compile(r'<link\b[^>]*\bhref="(https://fonts\.googleapis\.com/css2[^"]+)"[^>]*/?\s*>')
_GF_URL_RE = re.compile(r'url\((https://fonts\.gstatic\.com[^)]+)\)')
_GF_UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"


def _embed_external_images(html: str) -> str:
    """Replace HTTP/HTTPS img src with base64 data URIs so they render from file://."""
    def _fetch(match: re.Match) -> str:
        prefix, url = match.group(1), match.group(2)
        try:
            with urllib.request.urlopen(url, timeout=10) as resp:
                content_type = resp.headers.get("Content-Type", "image/png").split(";")[0]
                data = base64.b64encode(resp.read()).decode()
                return f'{prefix}src="data:{content_type};base64,{data}"'
        except Exception:
            return match.group(0)

    return _EXT_IMG_RE.sub(_fetch, html)


def _embed_google_fonts(html: str) -> str:
    """Fetch Google Fonts CSS and inline font files as base64 so they render from file://."""
    def _fetch_font(url: str) -> tuple[str, str]:
        with urllib.request.urlopen(url, timeout=15) as r:
            return url, base64.b64encode(r.read()).decode()

    def replace_link(match: re.Match) -> str:
        css_url = match.group(1)
        try:
            req = urllib.request.Request(css_url, headers={"User-Agent": _GF_UA})
            with urllib.request.urlopen(req, timeout=15) as resp:
                css = resp.read().decode("utf-8")

            font_urls = _GF_URL_RE.findall(css)
            url_to_b64: dict[str, str] = {}
            with ThreadPoolExecutor(max_workers=8) as pool:
                futures = {pool.submit(_fetch_font, u): u for u in font_urls}
                for future in as_completed(futures):
                    try:
                        url, data = future.result()
                        url_to_b64[url] = data
                    except Exception:
                        pass

            def embed_url(m: re.Match) -> str:
                data = url_to_b64.get(m.group(1))
                return f"url(data:font/woff2;base64,{data})" if data else m.group(0)

            css = _GF_URL_RE.sub(embed_url, css)
            return f"<style>\n{css}\n</style>"
        except Exception:
            return match.group(0)

    return _GF_CSS_RE.sub(replace_link, html)


def render_pdf(html: str, output_path: Path, base_dir: Path | None = None, style: dict | None = None) -> None:
    """Render HTML to PDF using headless Chromium. Waits for Mermaid if present."""
    has_mermaid = 'class="mermaid"' in html

    if style and style["fonts"]["google_fonts"]:
        html = _embed_google_fonts(html)
    html = _embed_external_images(html)

    if style:
        fonts = style["fonts"]
        footer_font = fonts["mono"] if style["footer"].get("font") == "mono" else fonts["body"]
        footer_color = style["colors"].get("muted", "#6e7781")
    else:
        footer_font = "-apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif"
        footer_color = "#6e7781"

    footer_template = (
        '<div style="width:100%;text-align:center;font-size:10px;'
        f"color:{footer_color};font-family:{footer_font};padding-bottom:4mm;\">"
        '<span class="pageNumber"></span></div>'
    )

    tmp_dir = (base_dir or output_path.parent).resolve()
    tmp = tempfile.NamedTemporaryFile(
        suffix=".html", dir=tmp_dir, delete=False, mode="w", encoding="utf-8"
    )
    try:
        tmp.write(html)
        tmp.close()
        tmp_path = Path(tmp.name)

        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()
            page.goto(tmp_path.as_uri(), wait_until="networkidle")

            if has_mermaid:
                try:
                    page.wait_for_selector(".mermaid svg", timeout=10_000)
                except Exception:
                    pass

            page.pdf(
                path=str(output_path),
                format="A4",
                print_background=True,
                display_header_footer=True,
                header_template="<div></div>",
                footer_template=footer_template,
                margin={
                    "top": "20mm",
                    "bottom": "20mm",
                    "left": "18mm",
                    "right": "18mm",
                },
            )
            browser.close()
    finally:
        tmp_path.unlink(missing_ok=True)
