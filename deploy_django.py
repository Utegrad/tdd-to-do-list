import os
import sys

from deploy.deployment import Deployment

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))


def main(argz):
    env_file = os.path.join(ROOT_DIR, '.env')
    deployment = Deployment(django_src=os.path.join(ROOT_DIR, 'src'))

    # relative to the django_src path
    deployment.copy_app_contents()
    deployment.write_env_file(env_file)
    deployment.copy_env_file(env_file)


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
