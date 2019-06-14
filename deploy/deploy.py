import os
import sys
import json
from fabric import Connection
from get_secret import get_secret

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class Deployment:
    def __init__(self):
        self.app_secrets_name = os.environ.get('APP_SECRETS_NAME')
        self.region_name = os.environ.get('REGION_NAME')
        self.ssh_host = os.environ.get('SSH_HOST')
        self.ssh_username = os.environ.get('SSH_USERNAME')
        self.secrets = get_secret(self.app_secrets_name, self.region_name)
        self.app_secrets = json.loads(self.secrets[0])
        self.app_path = self.app_secrets['APP_PATH']
        self.django_src = os.path.join(ROOT_DIR, 'src')

    def copy_root_files(self, source_files, dest_dir=None):
        application_path = self.app_path if dest_dir is None else dest_dir
        with Connection(host=self.ssh_host, user=self.ssh_username, ) as c:
            self.clean(application_path, c)
            for f in source_files:
                c.put(os.path.join(self.django_src, f), f"{application_path}/")

    def clean(self, application_path, connection):
        print('Cleaning out files from application path')
        connection.run(f'find {application_path} -type f -exec rm {{}} \;')

    def copy_directories(self, ):
        pass


def main(argz):
    deployment = Deployment()

    # relative to the django_src path
    dirs_to_copy = ('django_tdd_tutorial', 'lists', 'templates')
    files_to_copy = ('manage.py',)

    deployment.copy_root_files(source_files=files_to_copy, )

    '''
    for d in dirs_to_copy:
        c.run(f'if [ -d "{app_path}/{d}" ]; then rm -Rf "{app_path}/{d}"; fi')
        c.run(f'mkdir -p {app_path}/{d}')
        source_path = os.path.join(django_src, d)
        remote_path = f"{app_path}/{d}"
        c.put(f"{source_path}", remote_path)
        '''


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
