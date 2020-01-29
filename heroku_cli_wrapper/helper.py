import subprocess
import logging


def call_cmd(cmd: str, capture_output=True):
    if capture_output:
        response = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                  universal_newlines=True)
    else:
        response = subprocess.run(cmd, shell=True, universal_newlines=True)
    if response.returncode != 0:
        logging.error(f'Command "{cmd}" returned non-zero exit status {response.returncode}.')
        logging.error(response.stderr)
        exit(response.returncode)
    return response
