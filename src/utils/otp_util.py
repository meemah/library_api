
from random import randint


def generate_otp(length=4):
    return f"{randint(10**(length - 1), 10**length - 1)}"