import ast
from pathlib import Path


SOURCE_DIRECTORY = Path("src/jga/analysis_representation")
FORBIDDEN_PREFIXES = (
    "jga.comparator",
    "jga.ground_truth",
    "jga.validation_catalog",
)


def test_materialization_boundary_has_no_validation_side_dependencies():
    imports = set()
    for path in SOURCE_DIRECTORY.glob("*.py"):
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imports.update(alias.name for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                imports.add(node.module)

    assert not {
        name
        for name in imports
        if name.startswith(FORBIDDEN_PREFIXES)
    }
