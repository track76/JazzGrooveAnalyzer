from bootstrap.git_tools import check_git_status
from bootstrap.test_runner import run_tests
from bootstrap.docs_updater import update_docs
from bootstrap.bootstrap_generator import generate_bootstrap
from bootstrap.repository_exporter import export_repository
from bootstrap.report import print_report


def main():

    check_git_status()

    run_tests()

    update_docs()

    generate_bootstrap()

    export_repository()

    print_report()


if __name__ == "__main__":
    main()
