import subprocess


def update_docs():

    subprocess.run(
        ["python", "tools/update_project_state.py"],
        check=True,
    )

    subprocess.run(
        ["python", "tools/update_session_context.py"],
        check=True,
    )

    subprocess.run(
        ["python", "tools/update_decisions.py"],
        check=True,
    )
