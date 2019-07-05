import os
import random
import sys
import tempfile
import pytest


ROOT_DIR = os.path.dirname(os.path.abspath(__file__))


def get_secret_key():
    secret = "".join(
        [
            random.SystemRandom().choice(
                "abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)"
            )
            for i in range(50)
        ]
    )
    return secret


def main(argz):
    # expected to be run from the Jenkins WORKSPACE
    # Write a .env file for running unit tests.
    env_file = os.path.join(ROOT_DIR, "src/django_tdd_tutorial/.env")
    secret_key = get_secret_key
    db_file = os.path.join(tempfile.gettempdir(), "tdd-test.db")
    with open(env_file, "w") as f:
        f.write("DEBUG=False\n")
        f.write(f"SECRET_KEY={secret_key}\n")
        f.write(f"DATABASE_URL=sqlite:///{db_file}\n")
        f.write("INTERNAL_IPS=127.0.0.1,localhost\n")
        f.write("ALLOWED_HOSTS=127.0.0.1,localhost\n")
        f.write("STATIC_ROOT=\n")
        f.write("MEDIA_ROOT=\n")
    # Run pytest and generate the build reports in the build_reports dir
    # --disable-warnings --junit-xml=./build_reports/deploy/deploy.xml'
    pytest.main(
        [
            "src/lists",
            "--disable-warnings",
            "--junit-xml=./build_reports/django/tdd_tutorial.xml",
        ]
    )
    # delete the .env file
    os.remove(env_file)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
