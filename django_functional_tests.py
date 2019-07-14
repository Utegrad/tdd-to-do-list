import os
import sys

import pytest

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))


def main(argz):
    # expected to be run from the Jenkins WORKSPACE
    # Run pytest and generate the build reports in the build_reports dir
    # --disable-warnings --junit-xml=./build_reports/deploy/deploy.xml'
    pytest.main(
        [
            "src/functional_tests/test_list_app.py",
            "--disable-warnings",
            "--junit-xml=./build_reports/django/tdd_tutorial.xml",
        ]
    )


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
