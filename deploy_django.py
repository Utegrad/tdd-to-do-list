import os
import sys

from deploy.deployment import Deployment

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))


def main(argz):
    deployment = Deployment(django_src=os.path.join(ROOT_DIR, 'src'))

    # relative to the django_src path
    deployment.copy_app_contents()


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
