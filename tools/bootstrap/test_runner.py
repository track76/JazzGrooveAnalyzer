import subprocess
import sys


def run_tests():

    result = subprocess.run(["pytest"])

    if result.returncode != 0:

        sys.exit(result.returncode)
