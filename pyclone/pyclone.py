"""Main module."""

import re
import subprocess
from .locations import RCLONE_DIR_PATH, RCLONE_PATH, CONFIG, SHELL, flatten


def main():
    return 0


if __name__ == '__main__':
    print(RCLONE_DIR_PATH)


class Pyclone():
    '''
        Pyclone object that will be used to interact with the pyclone shell

    '''

    def __init__(self, dir=RCLONE_DIR_PATH, executable=RCLONE_PATH):
        self.dir = dir
        self.executable = executable

    def __execute(self, cmd):
        pipe = subprocess.run(RCLONE_PATH + cmd, capture_output=True,
                              text=True, cwd=RCLONE_DIR_PATH, shell=SHELL)
        output = pipe.stdout if pipe.stdout else pipe.stderr
        return output

    def create(self, drive_type, drive_name, drive_user, drive_pass):
        cmd = ['config', 'create', drive_name,
               drive_type, 'user', drive_user, 'pass', drive_pass]
        return self.__execute(cmd)

    def copy(self, src, dest):
        cmd = ['copy', src, dest]
        self.__execute(cmd)

    def ls(self, drive, dir=''):
        cmd = ['ls', drive + ':/' + dir]
        return self.__execute(cmd)

    def remove(self, drive):
        cmd = ['config delete' + drive]
        return self.__execute(cmd)

    def get_size(self, drive):
        cmd = [drive + '']
        return self.__execute(cmd)


class DriveManager():
    '''
        Manages all the drive available from the config by name only
    '''

    def __init__(self, config=CONFIG):
        self.drives = self.__get_config(config)
        self.pyclone = Pyclone()

    # ensure that no other linux command is
    def __get_config(self, config):
        with open(config) as f:
            config_data = f.readlines()
        return self.__parse_config(config_data)

    def __parse_config(self, config_data):
        pattern = r'\[\S+\]'
        config_data = ''.join(config_data)
        return flatten(re.findall(pattern, config_data))

    def get_drive(self, drive):
        '''
            Returns the drive object from the pyclone config
        '''
        try:
            return Drive(drive)
        except Exception:
            print("Drive does not exist")

    def add_drive(self, drive_type, drive_name, drive_user, drive_pass):
        out = self.pyclone.create(
            drive_type, drive_name, drive_user, drive_pass)
        self.drives.append(drive_name)
        return out

    def remove_drive(self, drive):
        try:
            self.drives.pop(self.drives.index(drive))
            out = self.pyclone.remove(drive)
        except ValueError:
            print("Drive does not exist")

    def show_drives(self):
        return self.drives


class Drive(Pyclone):
    def __init__(self, drive):
        super().__init__()
        self.drive = drive


DRIVES = DriveManager()
