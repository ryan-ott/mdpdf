# Changelog

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
