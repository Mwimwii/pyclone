"""Main module."""

import subprocess
from .locations import RCLONE_DIR_PATH, RCLONE_PATH, SHELL

def main():
    return 0


if __name__ == '__main__':
    print(RCLONE_DIR_PATH)


class DriveManager():
    # def __init__(self, config=locations.CONFIG):
    #     pass
    # ensure that no other linux command is

    def cmd(self):
        pass
    # returns value of cmd

    def __execute(self, cmd):
        pipe = subprocess.run(RCLONE_PATH + cmd, capture_output=True,
                              text=True, cwd=RCLONE_DIR_PATH, shell=SHELL)
        output = pipe.stdout if pipe.stdout else pipe.stderr
        return output

    def create(self, drive_type, drive_name, drive_user, drive_pass):
        cmd = ['config', 'create', drive_name,
               drive_type, 'user', drive_user, 'pass', drive_pass]
        self.__execute(cmd)

    def copy(self, src, dest):
        cmd = ['copy', src, dest]
        self.__execute(cmd)

    def ls(self, drive, dir=''):
        cmd = ['ls', drive + ':/' + dir]
        self.__execute(cmd)

    def get_size(self, drive):
        cmd = [drive + '']
        self.__execute(cmd)


payload = {}
