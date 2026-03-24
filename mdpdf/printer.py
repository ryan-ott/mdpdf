from pathlib import Path
from playwright.sync_api import sync_playwright


def render_pdf(html: str, output_path: Path) -> None:
    """Render HTML to PDF using headless Chromium. Waits for Mermaid if present."""
    has_mermaid = 'class="mermaid"' in html

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.set_content(html, wait_until="networkidle")

        if has_mermaid:
            try:
                page.wait_for_selector(".mermaid svg", timeout=10_000)
            except Exception:
                # Mermaid failed to render (e.g. CDN unreachable) — continue anyway
                pass

        page.pdf(
            path=str(output_path),
            format="A4",
            print_background=True,
            display_header_footer=True,
            header_template="<div></div>",
            footer_template=(
                '<div style="width:100%;text-align:center;font-size:10px;'
                "color:#6e7781;font-family:-apple-system,BlinkMacSystemFont,"
                "'Segoe UI',Helvetica,Arial,sans-serif;padding-bottom:4mm;\">"
                '<span class="pageNumber"></span></div>'
            ),
            margin={
                "top": "20mm",
                "bottom": "20mm",
                "left": "18mm",
                "right": "18mm",
            },
        )
        browser.close()
