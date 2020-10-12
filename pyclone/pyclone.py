"""Main module."""

import json
import os
import re
import subprocess
from .locations import RCLONE_DIR_PATH, RCLONE_PATH, CONFIG, SHELL


def main():
    return 0


if __name__ == '__main__':
    print(RCLONE_DIR_PATH)


class Pyclone(object):
    '''
        Pyclone object that will be used to interact with the pyclone shell

    '''

    def __init__(self, dir=RCLONE_DIR_PATH, executable=RCLONE_PATH):
        self.dir = dir
        self.executable = executable

    def execute(self, cmd):
        pipe = subprocess.run(RCLONE_PATH + cmd, capture_output=True,
                              text=True, cwd=RCLONE_DIR_PATH, shell=SHELL)
        output = pipe.stdout if pipe.stdout else pipe.stderr
        return output

    def create(self, remote_type, remote_name, remote_user, remote_pass):
        cmd = ['config', 'create', remote_name,
               remote_type, 'user', remote_user, 'pass', remote_pass]
        return self.execute(cmd)

    def copy(self, src, dest):
        cmd = ['copy', src, dest]
        self.execute(cmd)

    def copyurl(self, url, remote, dir='', options=[]):
        cmd = ['copyurl', url, remote + ':', dir, ] + options.split()
        self.execute(cmd)

    def ls(self, remote, dir=''):
        cmd = ['ls', remote + ':/' + dir]
        return self.execute(cmd)

    def delete(self, remote):
        cmd = ['config delete' + remote]
        return self.execute(cmd)

    def get_size(self, remote):
        cmd = [remote + ':']
        return self.execute(cmd)


class RemoteManager():
    '''
        Manages all the remote available from the config by name only
    '''

    def __init__(self, config=CONFIG):
        self.config = config
        self.pyclone = Pyclone()

    # ensure that no other linux command is
    def __get_config(self, config):
        with open(config) as f:
            config_data = f.readlines()
        return self.__parse_config(config_data)

    def __parse_config(self, config_data):
        pattern = r'\[\S+\]'
        config_data = ''.join(config_data)
        parsed_config_data = re.findall(pattern, config_data)
        return [remote[1:-1] for remote in parsed_config_data]

    def get_remote(self, remote):
        '''
            Returns the remote object from the pyclone config
        '''
        try:
            return Remote(remote)
        except Exception:
            print("remote does not exist")

    def add(self, remote_type, remote_name, remote_user, remote_pass):
        out = self.pyclone.create(
            remote_type, remote_name, remote_user, remote_pass)
        return out

    def delete(self, remote):
        try:
            out = self.pyclone.delete(remote)
        except ValueError:
            out = "remote does not exist"
        return out

    def show(self):
        return self.__get_config(self.config)

    def dump(self):
        dump_file = self.pyclone.execute(['config', 'dump'])
        return json.loads(dump_file)


class Remote(Pyclone):
    def __init__(self, remote):
        super().__init__()
        self.remote = remote

    def upload(self, src):
        cmd = ['copy', src, self.remote + ':']
        self.execute(cmd)

    def download(self, src, dest=os.getcwd()):
        if dest != os.getcwd():
            dest = os.path.join(os.getcwd(), dest)
        cmd = ['copy',  self.remote + ':' + src, dest]
        self.execute(cmd)

    def ls(self, dir=''):
        cmd = ['ls', self.remote + ':/' + dir]
        return self.execute(cmd)

    def delete(self):
        cmd = ['config delete' + self.remote]
        return self.execute(cmd)

    def get_size(self):
        cmd = [self.remote + '']
        return self.execute(cmd)

# remotes = RemoteManager()
