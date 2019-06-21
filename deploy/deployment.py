import json
import os
import re

from fabric import Connection
from invoke import UnexpectedExit

from deploy.aws.get_secrets import get_secrets

EXCLUDED_FILE_PATTERNS = (
    r"^\..+$",
    r"[/|\\]\..+$",
    r".*\.log$",
    r".*\.db$",
    r"\.ipynb$",
)
EXCLUDED_DIRECTORY_PATTERNS = (
    r"__pycache__$",
    r"functional_tests$",
    r"\\\..+$",
    r"/\..+$",
    r"^\..+$",
)

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class SecretKeys:
    """ Using these to match keys in Secrets Manager to access their values. """

    def __init__(self):
        self.SECRET_KEY = "SECRET_KEY"
        self.DATABASE_URL = "DATABASE_URL"
        self.APPLICATION_PATH = "APP_PATH"
        self.VIRTUALENV_PATH = "VENV_PATH"
        self.STATIC_ROOT = "STATIC_ROOT"
        self.MEDIA_ROOT = "MEDIA_ROOT"
        self.DEBUG = "DEBUG"
        self.INTERNAL_IPS = "INTERNAL_IPS"
        self.ALLOWED_HOSTS = "ALLOWED_HOSTS"
        self.DJANGO_SETTINGS_DIR = "DJANGO_SETTINGS_DIR"


class DotEnvKeys:
    """ Keys that need to be included in the .env settings file. """

    def __init__(self):
        self.keys_ = (
            "DEBUG",
            "SECRET_KEY",
            "DATABASE_URL",
            "INTERNAL_IPS",
            "ALLOWED_HOSTS",
            "STATIC_ROOT",
            "MEDIA_ROOT",
        )


class Deployment:
    def __init__(self, django_src=None):
        self.secret_keys = SecretKeys()
        self.app_secrets_name = os.environ.get("APP_SECRETS_NAME")
        self.region_name = os.environ.get("REGION_NAME")
        self.ssh_host = os.environ.get("SSH_HOST")
        self.ssh_username = os.environ.get("SSH_USERNAME")
        self.secrets = get_secrets(self.app_secrets_name, self.region_name)
        self.app_secrets = json.loads(self.secrets[0])
        self.app_path = self.app_secrets[self.secret_keys.APPLICATION_PATH]
        self.django_src = (
            os.path.join(ROOT_DIR, "src") if django_src is None else django_src
        )

    def env_file_filter_values(self):
        env_keys = DotEnvKeys().keys_
        env_values = {}
        for k in env_keys:
            env_values[k] = self.app_secrets[k]
        return env_values

    def env_file_content(self):
        filtered_values = self.env_file_filter_values()
        content = ""
        for attr, value in filtered_values.items():
            content = content + f"{attr.lstrip().rstrip()}={value.lstrip().rstrip()}\r"
        return content

    def write_env_file(self, path):
        contents = self.env_file_content()
        with open(path, "w") as writer:
            writer.writelines(contents)

    def copy_contents_recursive(
            self, container, original_container, new_container, connection
    ):
        contents = [os.path.join(container, p) for p in os.listdir(container)]
        for item in contents:
            if os.path.isfile(item):
                if self.excluded(name=item, patterns=EXCLUDED_FILE_PATTERNS):
                    continue
                else:
                    destination_path = os.path.join(
                        new_container, os.path.relpath(item, original_container)
                    )
                    destination_path = destination_path.replace("\\", "/")
                    print(f"copying file to {destination_path}")
                    connection.put(item, destination_path)
                    continue
            if os.path.isdir(item):
                if self.excluded(name=item, patterns=EXCLUDED_DIRECTORY_PATTERNS):
                    continue
                else:
                    destination_path = os.path.join(
                        new_container, os.path.relpath(item, original_container)
                    )
                    destination_path = destination_path.replace("\\", "/")
                    print(f"creating directory {destination_path}")
                    connection.run(f"mkdir -p {destination_path}")
                    self.copy_contents_recursive(
                        item, original_container, new_container, connection
                    )

    def copy_app_contents(self, source=None, destination=None):
        django_source = self.django_src if source is None else source
        application_path = self.app_path if destination is None else destination
        with Connection(host=self.ssh_host, user=self.ssh_username) as conn:
            try:
                print(f"creating directory {application_path}")
                conn.run(f"mkdir -p {application_path}")
                print(f"removing all files below {application_path}")
                conn.run(
                    f"find {application_path} -mindepth 1 -type f -exec rm {{}} \\;"
                )
                print(f"removing all directories below {application_path}")
                try:
                    conn.run(
                        f"find {application_path} -mindepth 1 -type d -exec rm -rf {{}} \\;"
                    )
                except UnexpectedExit as e:
                    print("ignoring UnexpectedExit exception when removing directories")
                    print(f"{e.result}")
                self.copy_contents_recursive(
                    django_source, django_source, application_path, conn
                )
            except Exception as e:
                raise e

    @staticmethod
    def excluded(name, patterns):
        excluded = False
        for pattern in patterns:
            if re.search(pattern, name):
                excluded = True
                break
        return excluded

    def copy_env_file(self, env_file):
        env_file_destination = (
                self.app_path
                + "/"
                + self.app_secrets[self.secret_keys.DJANGO_SETTINGS_DIR]
                + "/"
                + ".env"
        )
        with Connection(host=self.ssh_host, user=self.ssh_username) as conn:
            try:
                result = conn.put(env_file, env_file_destination)
                print(f'{result.local} copied to {result.remote}')
                os.remove(env_file)
            except Exception as e:
                raise e

    def refresh_venv(self):
        """ Refresh virtualenv in VIRTUALENV_PATH. """
        pass

    def gather_static_files(self):
        """ Run collectstatic on remote. """
        # /var/www/apps/Envs/tdd/bin/python /var/www/apps/tdd/manage.py collectstatic --clear --noinput

        pass

    def django_migrations(self):
        """ run django migrations. """
        pass

    def django_check(self):
        """ run manage.py check """
        pass

    def restart_apache(self):
        pass