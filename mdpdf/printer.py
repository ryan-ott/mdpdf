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
            margin={
                "top": "20mm",
                "bottom": "20mm",
                "left": "18mm",
                "right": "18mm",
            },
        )
        browser.close()
