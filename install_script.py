"""
This is the install script of the UH3D Server.
"""

import subprocess
import os
import sys

def check_status(status):
    """
    Check the status of a subprocess command and
    exit the script if it returns a non-zero status code.

    :param status: the return value of a subprocess command
    """
    if status != 0:
        sys.exit("Error detected while installing dependencies")

def install():
    """
    Install
    """
    os.system('echo "deb https://packages.cloud.google.com/apt coral-edgetpu-stable main" \
              | sudo tee /etc/apt/sources.list.d/coral-edgetpu.list')
    os.system('curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add -')

    args = ["sudo"] + ["apt"] + ["update"]
    check_status(subprocess.run(args, check=True).returncode)
    args = ["sudo"] + ["apt"] + ["-y"] + ["upgrade"]
    check_status(subprocess.run(args, check=True).returncode)
    args = ["sudo"] + ["apt"] + ["-y"] + ["install"] + ["hugin-tools"] + ["enblend"]\
          + ["imagemagick"] + ["libopencv-dev"] + ["build-essential"] + ["python3-opencv"] \
            + ["python3-tflite-runtime"]
    check_status(subprocess.run(args, check=True).returncode)
    args = ["pip3"] + ["install"] + ["xystitch"] + ["picamerax"] + ["Flask"] + ["flask-restful"]
    check_status(subprocess.run(args, check=True).returncode)

    args = ["sudo"] + ["cp"] + ["config.txt"] + ["/boot/config.txt"]
    check_status(subprocess.run(args, check=True).returncode)

    os.mkdir('./tmp')
    os.mkdir('./tmp/stitch')
    os.mkdir('./tmp/fs')

    args = ["git"] + ["clone"] + ["https://github.com/PetteriAimonen/focus-stack.git"]
    check_status(subprocess.run(args, check=True).returncode)
    args = ["make"]
    check_status(subprocess.run(args, cwd='./focus-stack/', check=True).returncode)
    args = ["sudo"] + ["make"] + ["install"]
    check_status(subprocess.run(args, cwd='./focus-stack/', check=True).returncode)

if __name__ == "__main__":
    install()
