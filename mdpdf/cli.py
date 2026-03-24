import sys
import argparse
from pathlib import Path

from mdpdf.converter import convert
from mdpdf.template import render_template
from mdpdf.printer import render_pdf


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="mdpdf",
        description="Convert a Markdown file to PDF.",
    )
    parser.add_argument("file", help="Path to the Markdown file")
    args = parser.parse_args()

    source = Path(args.file)

    if not source.exists():
        print(f"Error: file not found: {source}", file=sys.stderr)
        sys.exit(1)

    if not source.is_file():
        print(f"Error: not a file: {source}", file=sys.stderr)
        sys.exit(1)

    if source.suffix.lower() != ".md":
        print(f"Warning: {source.name} does not have a .md extension — proceeding anyway", file=sys.stderr)

    output = source.with_suffix(".pdf")

    try:
        md_text = source.read_text(encoding="utf-8")
        body = convert(md_text)
        html = render_template(body)
        render_pdf(html, output)
    except PermissionError:
        print(f"Error: cannot write to {output} (permission denied)", file=sys.stderr)
        sys.exit(1)
    except Exception as exc:
        if "Executable doesn't exist" in str(exc) or "chromium" in str(exc).lower():
            print(
                "Error: Playwright Chromium not found.\n"
                "Run: uv tool run --from mdpdf playwright install chromium",
                file=sys.stderr,
            )
        else:
            print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)

    print(f"PDF saved: {output}")
