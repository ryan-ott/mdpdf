import re
import markdown
from markdown.extensions.codehilite import CodeHiliteExtension
from markdown.extensions.fenced_code import FencedCodeExtension
from markdown.extensions.tables import TableExtension
from markdown.extensions.toc import TocExtension


_MERMAID_FENCE_RE = re.compile(
    r"```mermaid\n(.*?)```",
    re.DOTALL,
)
_PLACEHOLDER_PREFIX = "MDPDF_MERMAID_"


def _extract_mermaid(md_text: str) -> tuple[str, list[str]]:
    """Replace mermaid fences with placeholders. Returns modified text and extracted blocks."""
    blocks: list[str] = []

    def replacer(match: re.Match) -> str:
        idx = len(blocks)
        blocks.append(match.group(1).strip())
        return f"\n\n{_PLACEHOLDER_PREFIX}{idx}\n\n"

    return _MERMAID_FENCE_RE.sub(replacer, md_text), blocks


def _restore_mermaid(html: str, blocks: list[str]) -> str:
    """Replace placeholders with <div class="mermaid"> elements."""
    for idx, content in enumerate(blocks):
        # python-markdown wraps the placeholder in a <p> tag
        html = html.replace(
            f"<p>{_PLACEHOLDER_PREFIX}{idx}</p>",
            f'<div class="mermaid">{content}</div>',
        )
        # fallback: replace bare placeholder if not wrapped
        html = html.replace(
            f"{_PLACEHOLDER_PREFIX}{idx}",
            f'<div class="mermaid">{content}</div>',
        )
    return html


def convert(md_text: str) -> str:
    """Convert Markdown text to an HTML body fragment."""
    preprocessed, mermaid_blocks = _extract_mermaid(md_text)

    md = markdown.Markdown(
        tab_length=2,
        extensions=[
            FencedCodeExtension(),
            CodeHiliteExtension(
                pygments_style="github-dark",
                linenums=False,
                guess_lang=True,
            ),
            TableExtension(),
            TocExtension(toc_depth=6),
            "markdown.extensions.nl2br",
            "markdown.extensions.smarty",
            "markdown.extensions.attr_list",
        ]
    )
    body = md.convert(preprocessed)
    return _restore_mermaid(body, mermaid_blocks)
