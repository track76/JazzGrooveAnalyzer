from bootstrap.git_tools import check_git_status
from bootstrap.test_runner import run_tests
from bootstrap.docs_updater import update_docs
from bootstrap.bootstrap_generator import generate_bootstrap
from bootstrap.repository_exporter import export_repository
from bootstrap.context_archive_exporter import export_context
from bootstrap.context_exporter import export_session_context
from bootstrap.architecture_exporter import (
    generate_architecture_map,
)

from bootstrap.scientific_state_exporter import (
    export_scientific_state,
)

from bootstrap.pipeline_state_exporter import (
    export_pipeline_state,
)

from bootstrap.runtime_state_exporter import (
    export_runtime_state,
)

from bootstrap.report import print_report


def main():

    print()
    print("=" * 60)
    print("Jazz Groove Analyzer Bootstrap")
    print("=" * 60)
    print()

    check_git_status()

    run_tests()

    update_docs()

    generate_bootstrap()

    export_repository()

    generate_architecture_map()

    export_session_context()

    export_context()

    export_scientific_state()

    export_pipeline_state()

    export_runtime_state()

    print_report()


if __name__ == "__main__":
    main()
