# mdpdf

Convert a Markdown file to a polished PDF, saved alongside the source file.

Built for technical docs: code blocks with syntax highlighting, tables, Mermaid diagrams, blockquotes, and clean pagination (no orphaned headings, no split tables).

## Install

```bash
uv tool install git+https://github.com/ryan-ott/mdpdf
uv tool run --from mdpdf playwright install chromium
```

## Update

```bash
uv tool upgrade mdpdf
```

## Usage

```bash
mdpdf path/to/document.md
# → path/to/document.pdf
```

## Cursor / VS Code

Add to your user tasks (`Cmd+Shift+P → Preferences: Open User Tasks`):

```json
{
  "version": "2.0.0",
  "tasks": [
    {
      "label": "Convert to PDF",
      "type": "shell",
      "command": "${env:HOME}/.local/bin/mdpdf",
      "args": ["${file}"],
      "presentation": {
        "reveal": "silent",
        "panel": "shared"
      },
      "problemMatcher": []
    }
  ]
}
```

Then `Cmd+Shift+P → Tasks: Run Task → Convert to PDF`.

> **Note:** Cursor runs tasks in a non-login shell, so the full path to `mdpdf` is required. `${env:HOME}/.local/bin/mdpdf` assumes a standard `uv` install location — adjust if your path differs (`which mdpdf`).
