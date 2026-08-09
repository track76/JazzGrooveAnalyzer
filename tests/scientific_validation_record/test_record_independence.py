import ast
from pathlib import Path


SOURCE_DIRECTORY = Path("src/jga/scientific_validation_record")
FORBIDDEN_PREFIXES = (
    "jga.ground_truth",
    "jga.pipeline",
    "jga.runtime",
    "jga.validation_catalog",
)


def test_record_boundary_has_no_execution_or_ground_truth_dependencies():
    imports = set()
    for path in SOURCE_DIRECTORY.glob("*.py"):
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imports.update(alias.name for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                imports.add(node.module)

    assert not {
        name for name in imports if name.startswith(FORBIDDEN_PREFIXES)
    }
