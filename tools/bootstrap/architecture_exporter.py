from pathlib import Path
import ast


ROOT = Path(__file__).resolve().parents[2]

SOURCE_ROOT = ROOT / "src" / "jga"


def extract_python_info(path: Path):

    try:
        tree = ast.parse(
            path.read_text(encoding="utf-8")
        )
    except Exception:
        return None

    imports = []
    classes = []
    context_reads = []
    context_writes = []

    for node in ast.walk(tree):

        if isinstance(node, ast.Import):
            for item in node.names:
                imports.append(item.name)

        elif isinstance(node, ast.ImportFrom):
            module = node.module or ""
            imports.append(module)

        elif isinstance(node, ast.ClassDef):

            methods = []

            for item in node.body:
                if isinstance(item, ast.FunctionDef):
                    methods.append(
                        item.name
                    )

            classes.append(
                {
                    "name": node.name,
                    "methods": methods,
                }
            )

        elif isinstance(node, ast.Attribute):

            if (
                isinstance(node.value, ast.Name)
                and node.value.id == "context"
            ):

                if isinstance(node.ctx, ast.Load):
                    context_reads.append(node.attr)

                elif isinstance(node.ctx, ast.Store):
                    context_writes.append(node.attr)

    return {
        "imports": sorted(set(imports)),
        "classes": classes,
        "context_reads": sorted(set(context_reads)),
        "context_writes": sorted(set(context_writes)),
    }


def generate_architecture_map():

    output = ROOT / "artifacts" / "JGA_ARCHITECTURE_MAP.md"

    lines = []

    lines.append(
        "# Jazz Groove Analyzer - Architecture Map\n"
    )

    lines.append(
        "\nGenerated automatically by bootstrap.\n"
    )

    lines.append(
        "\n## Source Tree\n"
    )

    for path in sorted(SOURCE_ROOT.rglob("*.py")):

        relative = path.relative_to(ROOT)

        lines.append(
            f"\n### {relative}\n"
        )

        info = extract_python_info(path)

        if info is None:
            continue

        if info["imports"]:

            lines.append(
                "\nImports:\n"
            )

            for item in info["imports"]:

                lines.append(
                    f"- {item}\n"
                )

        if info["classes"]:

            lines.append(
                "\nClasses:\n"
            )

            for cls in info["classes"]:

                lines.append(
                    f"- {cls['name']}\n"
                )

                for method in cls["methods"]:

                    lines.append(
                        f"  - {method}\n"
                    )

        if info["context_reads"]:

            lines.append(
                "\nAnalysisContext reads:\n"
            )

            for item in info["context_reads"]:

                lines.append(
                    f"- context.{item}\n"
                )

        if info["context_writes"]:

            lines.append(
                "\nAnalysisContext writes:\n"
            )

            for item in info["context_writes"]:

                lines.append(
                    f"- context.{item}\n"
                )

    output.write_text(
        "".join(lines),
        encoding="utf-8",
    )
