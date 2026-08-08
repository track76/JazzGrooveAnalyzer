import ast
from pathlib import Path


GROUND_TRUTH_PACKAGE = Path("src/jga/ground_truth")


def test_ground_truth_has_no_forbidden_jga_dependencies():
    forbidden_prefixes = (
        "jga.runtime",
        "jga.domain",
        "jga.validation",
        "jga.interfaces.validation",
    )

    imported_modules: set[str] = set()
    for source_path in GROUND_TRUTH_PACKAGE.rglob("*.py"):
        tree = ast.parse(source_path.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imported_modules.update(alias.name for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module is not None:
                imported_modules.add(node.module)

    assert not any(
        module.startswith(forbidden_prefixes) for module in imported_modules
    )


def test_ground_truth_layer_contains_no_comparator():
    python_files = tuple(GROUND_TRUTH_PACKAGE.rglob("*.py"))

    assert all("comparator" not in path.name.lower() for path in python_files)
