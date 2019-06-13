import os
import sys
import json
from fabric import Connection
from get_secret import get_secret

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def main(argz):
    app_secrets_name = os.environ.get('APP_SECRETS_NAME')
    region_name = os.environ.get('REGION_NAME')
    ssh_host = os.environ.get('SSH_HOST')
    ssh_username = os.environ.get('SSH_USERNAME')
    secrets = get_secret(app_secrets_name, region_name)
    app_secrets = json.loads(secrets[0])
    app_path = app_secrets['APP_PATH']

    django_src = os.path.join(ROOT_DIR, 'src')
    # relative to the django_src path
    dirs_to_copy = ('django_tdd_tutorial', 'lists', 'templates')
    files_to_copy = ('manage.py', )

    with Connection(host=ssh_host, user=ssh_username, ) as c:
        print('Cleaning out files from application path')
        c.run(f'find {app_path} -type f -exec rm {{}} \;')
        for f in files_to_copy:
            c.put(os.path.join(django_src, f), f"{app_path}/")

        for d in dirs_to_copy:
            c.run(f'if [ -d "{app_path}/{d}" ]; then rm -Rf "{app_path}/{d}"; fi')
            c.run(f'mkdir -p {app_path}/{d}')
            source_path = os.path.join(django_src, d)
            remote_path = f"{app_path}/{d}"
            c.put(f"{source_path}", remote_path)


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
