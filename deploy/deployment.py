import json
import os
import sys
import re
from copy import copy
from os.path import join

from fabric import Connection
from deploy.aws.get_secrets import get_secrets

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXCLUDED_FILE_PATTERNS = (r'\..+$', '.*\.log$', '.*\.db$', )
EXCLUDED_DIRECTORY_PATTERNS = (r'__pycache__$', '\\\..+$', '/\..+$', )


class Deployment:
    def __init__(self):
        self.app_secrets_name = os.environ.get('APP_SECRETS_NAME')
        self.region_name = os.environ.get('REGION_NAME')
        self.ssh_host = os.environ.get('SSH_HOST')
        self.ssh_username = os.environ.get('SSH_USERNAME')
        self.secrets = get_secrets(self.app_secrets_name, self.region_name)
        self.app_secrets = json.loads(self.secrets[0])
        self.app_path = self.app_secrets['APP_PATH']
        self.django_src = os.path.join(ROOT_DIR, 'src')

    def copy_contents_recursive(self, container, original_container, new_container, connection):
        contents = [os.path.join(container, p) for p in os.listdir(container)]
        for item in contents:
            if os.path.isfile(item):
                if self.excluded(name=item, patterns=EXCLUDED_FILE_PATTERNS):
                    continue
                else:
                    destination_path = os.path.join(new_container, os.path.relpath(item, original_container))
                    connection.put(item, destination_path, )
            if os.path.isdir(item):
                if self.excluded(name=item, patterns=EXCLUDED_DIRECTORY_PATTERNS):
                    continue
                else:
                    destination_path = os.path.join(new_container, os.path.relpath(item, original_container))
                    connection.run(f'mkdir -p {destination_path}')
                    self.copy_contents_recursive(item, original_container, new_container, connection)

    def copy_app_contents(self, source, destination=None):
        application_path = self.app_path if destination is None else destination
        with Connection(host=self.ssh_host, user=self.ssh_username, ) as conn:
            try:
                conn.run(f'mkdir -p {application_path}')
                # clean out the root of the application path
                conn.run(f'find {application_path} -mindepth 1 -type f -exec rm {{}} \\;')
                conn.run(f'find {application_path} -mindepth 1 -type d -exec rm -rf {{}} \\;')
                self.copy_contents_recursive(source, source, application_path, conn)
            except Exception as e:
                raise e

    @staticmethod
    def excluded(name, patterns):
        excluded = False
        for pattern in patterns:
            p = re.compile(pattern)
            if p.match(name):
                excluded = True
                break
        return excluded


def main(argz):
    deployment = Deployment()

    # relative to the django_src path
    deployment.copy_app_contents(source=os.path.join(ROOT_DIR, 'src'), )


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
