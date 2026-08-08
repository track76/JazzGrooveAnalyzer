import ast
from pathlib import Path


CATALOGUE_PACKAGE = Path("src/jga/validation_catalog")


def test_catalogue_has_no_forbidden_dependencies():
    forbidden_prefixes = (
        "jga.runtime",
        "jga.pipeline",
        "jga.analysis",
        "jga.ground_truth",
        "jga.validation",
        "jga.interfaces.validation",
    )

    imported_modules: set[str] = set()
    for source_path in CATALOGUE_PACKAGE.rglob("*.py"):
        tree = ast.parse(source_path.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imported_modules.update(alias.name for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module is not None:
                imported_modules.add(node.module)

    assert not any(
        module == forbidden
        or module.startswith(f"{forbidden}.")
        for module in imported_modules
        for forbidden in forbidden_prefixes
    )


def test_catalogue_contains_no_comparator_metrics_or_analysis_components():
    forbidden_names = ("comparator", "metric", "analysis")
    python_files = tuple(CATALOGUE_PACKAGE.rglob("*.py"))

    assert all(
        not any(name in path.name.lower() for name in forbidden_names)
        for path in python_files
    )
