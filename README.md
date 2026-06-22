# mdpdf

Convert a Markdown file to a polished PDF, saved alongside the source file.

Built for technical docs: code blocks with syntax highlighting, tables, Mermaid diagrams, blockquotes, and clean pagination (no orphaned headings, no split tables). Images (relative paths, absolute paths, and HTTP/HTTPS URLs) are embedded automatically.

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

mdpdf path/to/document.md -o path/to/output.pdf
```

## Styling

Drop an `mdpdf.toml` in the same directory as your Markdown file and it is picked up automatically — no flag needed.

```toml
[fonts]
body        = "Space Grotesk"
mono        = "Space Mono"
google_fonts = ["Space Grotesk", "Space Mono"]  # fetched and embedded at build time

[colors]
primary    = "#FF4800"   # headings, blockquote borders
text       = "#000000"
background = "#F6F6F6"
muted      = "#888888"   # footer, h6

[headings]
uppercase = true
font      = "mono"       # "body" or "mono"
color     = "#FF4800"

[headings.sizes]
h1 = "2em"
h2 = "1.5em"
h3 = "1.25em"
h4 = "1.05em"
h5 = "0.95em"
h6 = "0.88em"

[code]
theme = "friendly"       # any Pygments style name

[footer]
font = "mono"            # "body" or "mono"
```

To use a config from a different location:

```bash
mdpdf document.md --style path/to/custom.toml
```

See [`examples/ml6.toml`](examples/ml6.toml) for a complete branded example.

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
