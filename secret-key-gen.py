import random
import sys

SECRET_KEY = ''.join(
    [random.SystemRandom().choice('abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)') for i in range(50)])
sys.stdout.write(SECRET_KEY)

