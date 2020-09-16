"""Main module."""
import sys
import os
import platform
import subprocess
PLATFORM = platform.uname().system
PREFIX = ''
if PLATFORM != 'Windows':
    PREFIX = './'
    shell = False

MODULE_PATH = os.path.dirname(os.path.abspath(__file__))
RCLONE_DIR_PATH = os.path.join(MODULE_PATH, 'rclone\\rclone')
RCLONE = [PREFIX + f'{RCLONE_DIR_PATH}']
RCLONE2 = [PREFIX + f'{RCLONE_DIR_PATH}']


def main():
    pass
    # cmd = RCLONE2 + sys.argv[1:]
    # print(cmd)
    # subprocess.run(cmd)
    # pipe = subprocess.Popen(" ".join(cmd), shell=True,
    #                         stdout=subprocess.PIPE)
    # while pipe.poll() is None:
    #     l = pipe.stdout.readline(
    #     print(l)


if __name__ == '__main__':
    main()


def cmd():
    cmd = RCLONE + sys.argv[1:]
    subprocess.run(cmd)


def execute(cmd):
    pipe = subprocess.run(cmd, capture_output=True, text=True, check=True)
    print(pipe.stdout)


def create(drive_type, drive_name, drive_user, drive_pass):
    cmd = RCLONE + ['config', 'create', drive_name,
                    drive_type, 'user', drive_user, 'pass', drive_pass]
    execute(cmd)


def copy(src, dest):
    cmd = RCLONE + ['copy', src, dest]
    execute(cmd)


def ls(drive, dir=''):
    cmd = RCLONE + ['ls', drive + '/' + dir]
    execute(cmd)


def get_size(drive):
    cmd = RCLONE + ['rclone', drive]
    pipe = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT)
    pipe_seg = list(iter(pipe.stdout.readline, b''))
    return float(pipe_seg[1].strip().split()[-2].lstrip(b'('))


create('mega', 'mega', 'shoveeshovee@gmail.com', 'snakhaus')
get_size('mega')
