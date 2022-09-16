import string
import random

default_chars: str = string.ascii_uppercase + string.ascii_lowercase + string.digits


def generate_str(size: int = 24, chars: str = default_chars) -> str:
    return "".join(random.choice(chars) for _ in range(size))
