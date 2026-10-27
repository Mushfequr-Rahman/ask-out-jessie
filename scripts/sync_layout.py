"""Refresh shared header/footer in checked-in HTML; no runtime build is required."""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
PAGES = {"index.html": "chapters", "chapters.html": "chapters",
         "prologue.html": "chapters", "glossary.html": "glossary",
         "magneton.html": "glossary"}
header = (ROOT / "partials/header.html").read_text().strip()
footer = (ROOT / "partials/footer.html").read_text().strip()
for filename, active in PAGES.items():
    path = ROOT / filename
    text = path.read_text()
    rendered = header.replace("{{CHAPTERS_CURRENT}}", ' aria-current="page"' if active == "chapters" else "")
    rendered = rendered.replace("{{GLOSSARY_CURRENT}}", ' aria-current="page"' if active == "glossary" else "")
    for part, contents in [("header", rendered), ("footer", footer)]:
        pattern = rf"<!-- site-{part} -->.*?<!-- /site-{part} -->"
        replacement = f"<!-- site-{part} -->\n{contents}\n<!-- /site-{part} -->"
        text, count = re.subn(pattern, lambda _: replacement, text, flags=re.S)
        if count != 1:
            raise ValueError(f"Expected one shared {part} marker in {filename}")
    path.write_text(text)
