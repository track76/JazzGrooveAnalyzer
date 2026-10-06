"""Generate the single current recovery entry from canonical repository records."""
from pathlib import Path
import json
import os
import re

ROOT = Path(__file__).resolve().parents[2]
SOURCE_INDEX = "docs/project/BOOTSTRAP_SOURCES.json"


def _root_links(text: str, source: Path, root: Path) -> str:
    def replace(match):
        target = match.group(1)
        if target.startswith(("https://", "http://", "#", "mailto:")):
            return match.group(0)
        path, separator, fragment = target.partition("#")
        absolute = (source.parent / path).resolve()
        if not absolute.is_relative_to(root.resolve()) or not absolute.exists():
            raise ValueError(f"Invalid recovery link in {source}: {target}")
        return "](" + os.path.relpath(absolute, root) + separator + fragment + ")"
    return re.sub(r"\]\(([^)]+)\)", replace, text)


def current_section(text, section):
    marker=section.get('current_section_end')
    if marker:
        if text.count(marker)!=1:raise ValueError('Current-section boundary must occur exactly once')
        return text.split(marker,1)[0]
    # Compatibility for older source configurations; semantic historical heading
    # takes precedence over decorative horizontal rules.
    match=re.search(r'^## (?:Historical|Archived|Preserved historical)\b',text,re.M)
    if match:return text[:match.start()]
    return text.split("\n---\n",1)[0]


def render_bootstrap(root: Path = ROOT) -> str:
    """Pure rendering; unchanged canonical inputs produce identical bytes."""
    root = Path(root)
    config = json.loads((root / SOURCE_INDEX).read_text(encoding="utf-8"))
    parts = ["""# Jazz Groove Analyzer — single current bootstrap

This ROOT file is the sole current session recovery entry point.
Canonical repository scientific/project records remain the source of truth.
If this bootstrap conflicts with them, canonical records prevail: report the
conflict and stop dependent work. Historical bootstrap snapshots are provenance
records, not competing current authorities.

Generated from [canonical recovery sources](docs/project/BOOTSTRAP_SOURCES.json).
Do not edit or prepend state here. Update canonical sources, then run
`python tools/bootstrap.py --recovery-only` when generation is authorized.
Startup requires reading this file, not running generators or experiments.
The next scientific action requires separate PI authorization; recovery grants none.
Consult Git for current branch/commit; no commit identity is embedded here.
"""]
    for section in config["sections"]:
        source = root / section["path"]
        text = source.read_text(encoding="utf-8")
        if section["current_section_only"]:
            text = current_section(text, section)
        parts.append(_root_links(text.strip(), source, root))
    links = []
    for name in config["recovery_links"]:
        if not (root / name).is_file():
            raise ValueError(f"Missing canonical recovery document: {name}")
        links.append(f"- [{name}]({name})")
    parts.append("## Recovery references\n\n" + "\n".join(links))
    return "\n\n".join(parts).rstrip() + "\n"


def generate_bootstrap(root: Path = ROOT) -> Path:
    """Write root only; never recreate a second mutable artifacts bootstrap."""
    root = Path(root)
    config=json.loads((root / SOURCE_INDEX).read_text())
    if config.get('production_generation_status','').startswith('DEFERRED'):
        raise ValueError('Production bootstrap generation deferred by PI; use isolated fixtures')
    text = render_bootstrap(root)  # Validate before replacing the existing output.
    output = root / "JGA_BOOTSTRAP.md"
    output.write_text(text, encoding="utf-8")
    return output
