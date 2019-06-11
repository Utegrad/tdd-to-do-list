import os
import sys
from fabric import Connection
from get_secret import get_secret

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def main(argz):
    print(ROOT_DIR)
    app_secrets_name = os.environ.get('APP_SECRETS_NAME')
    region_name = os.environ.get('REGION_NAME')
    ssh_host = os.environ.get('SSH_HOST')
    ssh_username = os.environ.get('SSH_USERNAME')
    ssh_password = os.environ.get('SSH_PASSWORD')
    kwargs = {'password': ssh_password}

    with Connection(host=ssh_host, user=ssh_username, connect_kwargs=kwargs) as c:
        c.run('uname -r')

    secrets = get_secret(app_secrets_name, region_name)
    print(secrets)


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))