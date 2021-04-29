import os
import sys
import subprocess

import utils

def do_process(id):
    dirId = utils.storage_dir_for_id(id)
    fileName = os.path.join(dirId, id + ".pdf")

    proc = subprocess.Popen(["pdftoppm", "-png", id + ".pdf", id], cwd=dirId, stdout=subprocess.PIPE)

    while True:
        if (proc.poll() is not None):
            break

def process(id):
    try:
        do_process(id)
        status = "success"
    except Exception as e:
        import traceback
        traceback.print_exc(file=sys.stderr)
        status = "failure"
        return "error"

    return id
