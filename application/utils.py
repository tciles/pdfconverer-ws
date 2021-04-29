import os
import string
import tempfile
import uuid

from random import SystemRandom
choice = lambda seq: SystemRandom().choice(seq)
letter_set = set(string.ascii_letters)

STORAGE_DIR = os.environ.get("OUTPUT_DIR", tempfile.gettempdir())

def generate_id():
    return str(uuid.uuid4())
    # return "".join(choice(string.ascii_letters) for i in range(32))


def storage_dir_for_id(id):
    return os.path.join(STORAGE_DIR, id[0:1], id[0:2], id[0:3], id)


def storage_file_for_id(id, ext):
    return os.path.join(storage_dir_for_id(id), id + "." + ext)


def validate_id(id):
    return len(set(id) - set(string.ascii_letters)) == 0