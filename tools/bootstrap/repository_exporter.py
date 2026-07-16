import subprocess


def export_repository():

    subprocess.run(
        [
            "git",
            "archive",
            "--format=zip",
            "--output=JGA_REPOSITORY.zip",
            "HEAD",
        ],
        check=True,
    )
