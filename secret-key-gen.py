import random
import sys


def get_secret_key():
    secret = ''.join(
        [random.SystemRandom().
             choice('abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)')
                for i in range(50)]
    )
    return secret


def main():
    secret = get_secret_key()
    sys.stdout.write(secret)


if __name__ == '__main__':
    main()
