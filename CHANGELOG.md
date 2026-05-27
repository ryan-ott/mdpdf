# Changelog

## [0.3.0] - 2026-05-27

### Added
- `-o`/`--output` flag to specify the PDF output path; defaults to same directory as the source file

## [0.2.4] - 2026-05-27

### Fixed
- Long lines in code blocks no longer clip at the page edge; they now wrap within the block

## [0.2.3] - 2026-04-16

### Changed
- Widened visual hierarchy between h3 and h4 headings
- Added distinct styles for h5 (uppercase, bold) and h6 (uppercase, muted)
- Page-break-avoid rule now covers h5 and h6

## [0.2.2] - 2026-04-07

### Fixed
- List nesting now recognizes 2-space indentation to match markdown linter

## [0.2.1] - 2026-03-24

### Changed
- Add git version tags so `uv tool upgrade mdpdf` works without `--force`

## [0.2.0] - 2026-03-24

### Added
- Page numbers at bottom center of each PDF page

## [0.1.0] - 2026-03-24

### Added
- Initial release: Markdown to PDF conversion with GitHub-dark theme
- Syntax highlighting via Pygments (github-dark)
- Mermaid diagram support
- Table, blockquote, and code block rendering
- Pagination rules: no orphaned headings, no split tables/code/diagrams
- Cursor / VS Code task integration
