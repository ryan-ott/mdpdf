import sys
import argparse
from pathlib import Path

from mdpdf.converter import convert
from mdpdf.template import render_template
from mdpdf.printer import render_pdf
from mdpdf import style as style_mod


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="mdpdf",
        description="Convert a Markdown file to PDF.",
    )
    parser.add_argument("file", help="Path to the Markdown file")
    parser.add_argument(
        "-o", "--output",
        help="Output PDF path (default: same directory as input file)",
        metavar="PATH",
    )
    parser.add_argument(
        "--style",
        help="Path to a TOML style config (default: auto-discover mdpdf.toml)",
        metavar="PATH",
    )
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

    output = Path(args.output) if args.output else source.with_suffix(".pdf")
    style_path = Path(args.style) if args.style else None
    style = style_mod.load(style_path, search_dirs=[source.parent, Path.cwd()])

    try:
        md_text = source.read_text(encoding="utf-8")
        body = convert(md_text)
        html = render_template(body, style)
        render_pdf(html, output, base_dir=source.parent, style=style)
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
