import ast
from pathlib import Path


COMPARATOR_PACKAGE = Path("src/jga/comparator")


def test_comparator_has_no_runtime_loader_analysis_or_metrics_dependencies():
    forbidden_fragments = (
        ".loaders",
        "jga.runtime",
        "jga.pipeline",
        "jga.analysis",
        "metric",
    )
    imported_modules: set[str] = set()

    for source_path in COMPARATOR_PACKAGE.rglob("*.py"):
        tree = ast.parse(source_path.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imported_modules.update(alias.name for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module is not None:
                imported_modules.add(node.module)

    assert not any(
        fragment in module
        for module in imported_modules
        for fragment in forbidden_fragments
    )


def test_comparator_contains_no_accuracy_tolerance_or_conclusion_components():
    forbidden_names = ("accuracy", "tolerance", "conclusion", "regression")
    python_files = tuple(COMPARATOR_PACKAGE.rglob("*.py"))

    assert all(
        not any(name in path.name.lower() for name in forbidden_names)
        for path in python_files
    )
