import tomllib
from pathlib import Path

DEFAULTS: dict = {
    "fonts": {
        "body": "-apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif",
        "mono": "'SFMono-Regular', Consolas, 'Liberation Mono', Menlo, monospace",
        "google_fonts": [],
    },
    "colors": {
        "primary": "#0969da",
        "text": "#24292f",
        "background": "#ffffff",
        "muted": "#6e7781",
    },
    "headings": {
        "uppercase": False,
        "font": "body",
        "color": "",
        "sizes": {
            "h1": "2em",
            "h2": "1.5em",
            "h3": "1.25em",
            "h4": "1.05em",
            "h5": "0.95em",
            "h6": "0.88em",
        },
    },
    "code": {
        "theme": "github-dark",
    },
    "footer": {
        "font": "body",
    },
}


def load(path: Path | None = None, search_dirs: list[Path] | None = None) -> dict:
    user: dict = {}
    if path:
        with open(path, "rb") as f:
            user = tomllib.load(f)
    elif search_dirs:
        for d in search_dirs:
            candidate = d / "mdpdf.toml"
            if candidate.exists():
                with open(candidate, "rb") as f:
                    user = tomllib.load(f)
                break
    return _merge(DEFAULTS, user)


def _merge(base: dict, override: dict) -> dict:
    result = dict(base)
    for k, v in override.items():
        if isinstance(v, dict) and isinstance(result.get(k), dict):
            result[k] = _merge(result[k], v)
        else:
            result[k] = v
    return result
