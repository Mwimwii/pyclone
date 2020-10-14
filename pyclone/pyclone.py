"""Main module."""
import os
import re
import subprocess
from .locations import RCLONE_DIR_PATH, RCLONE_PATH, CONFIG, SHELL


def set_path(path, config):
    global RCLONE_DIR_PATH, CONFIG
    RCLONE_DIR_PATH = path
    CONFIG = config
    dict(RcloneDirectorty=RCLONE_DIR_PATH, ConfigPath=CONFIG)
    return


def main():
    return 0


if __name__ == '__main__':
    main()


class Response(object):
    def __init__(self, text, responsecode, args, stdout, stderr):
        if (responsecode == 0) and (text == ''):
            self.text = 'Process run successfully'
        else:
            self.text = text
        self.responsecode = responsecode
        self.args = args
        self.stdout = stdout
        self.stderr = stderr


class Pyclone(object):
    '''
        Pyclone object that will be used to interact with the pyclone shell
    '''

    def __init__(self, dir=RCLONE_DIR_PATH, executable=RCLONE_PATH):
        self.dir = dir
        self.executable = executable

    def execute(cmd, dir=RCLONE_DIR_PATH, executable=RCLONE_PATH):
        '''
            Returns a response object similar to the requests package with:

            text         - stdout or stderr output message
            responsecode - reponse code of the process. ie 1, 2, ...
            args         - initial arguments passed to the subprocess
            stdout       - stdout output message
            stderr       - stderr output message
        '''
        pipe = subprocess.run(executable + cmd, capture_output=True,
                              text=True, cwd=dir, shell=SHELL)

        text = pipe.stdout if pipe.stdout else pipe.stderr
        response = Response(text, pipe.returncode,
                            pipe.args, pipe.stdout, pipe.stderr)
        return response

    def execute(self, cmd):
        '''
            Returns a response object similar to the requests package with:

            text         - stdout or stderr output message
            responsecode - reponse code of the process. ie 1, 2, ...
            args         - initial arguments passed to the subprocess
            stdout       - stdout output message
            stderr       - stderr output message
        '''
        pipe = subprocess.run(self.executable + cmd, capture_output=True,
                              text=True, cwd=self.dir, shell=SHELL)

        text = pipe.stdout if pipe.stdout else pipe.stderr
        response = Response(text, pipe.returncode,
                            pipe.args, pipe.stdout, pipe.stderr)
        return response

    # Pyclone core functions
    def config_create(self, remote_type, remote_name, remote_user, remote_pass):
        cmd = ['config', 'create', remote_name,
               remote_type, 'user', remote_user, 'pass', remote_pass]
        return self.execute(cmd)

    def config_delete(self, remote):
        cmd = ['config', 'delete', remote]
        return self.execute(cmd)

    def copy(self, src, dest):
        cmd = ['copy', src, dest]
        return self.execute(cmd)

    def move(self, src, dest, rmdir=True):
        flags = []
        if rmdir:
            flags = ["--delete-empty-src-dirs"]
        cmd = ['move', src, dest] + flags
        return self.execute(cmd)

    def delete(self, remote_path):
        cmd = ['delete', remote_path]
        return self.execute(cmd)

    def ls(self, remote):
        cmd = ['lsf', remote]
        return self.execute(cmd)

    # def copyurl(self, url, remote, dir='', options=[]):
    #     cmd = ['copyurl', url, remote + ':', dir, ] + options.split()
    #     self.execute(cmd)

    # def get_size(self, remote):
    #     cmd = [remote + ':']
    #     return self.execute(cmd)


class RemoteManager():
    '''
        Manages all the remote available from the config by name only
    '''

    def __init__(self, config=CONFIG):
        self.config = config
        self.pyclone = Pyclone()

    def set_config(self, config):
        self.config = config

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

    def create(self, remote_type, remote_name, remote_user, remote_pass):
        response = self.pyclone.config_create(
            remote_type, remote_name, remote_user, remote_pass)
        return response

    def delete(self, remote):
        response = self.pyclone.config_delete(remote)
        return response

    def show(self):
        return self.__get_config(self.config)

    # Extra features

    # def dump(self):
    #     dump_file = self.pyclone.execute(['config', 'dump'])
    #     return json.loads(dump_file)


class Remote(Pyclone):
    def __init__(self, remote):
        super().__init__()
        self.remote = remote

    def copy(self, src, dest=None, dl=False):
        src, dest = self.__get_src_dest(src, dest, dl)
        cmd = ['copy', src, dest]
        return self.execute(cmd)

    def move(self, src, dest=None, dl=False, rmdir=True):
        flags = []
        src, dest = self.__get_src_dest(src, dest, dl)
        if rmdir:
            flags = ["--delete-empty-src-dirs"]
        cmd = ['move', src, dest] + flags
        return self.execute(cmd)

    def delete(self, path):
        remote_dir = f'{self.remote}:{path}'
        cmd = ['delete', remote_dir]
        return self.execute(cmd)

    def __get_src_dest(self, src, dest, dl):
        if dl:
            src = f'{self.remote}:{src}'
            if dest is None:
                dest = os.getcwd()
        else:
            if dest is None:
                dest = ''
            dest = f'{self.remote}:{dest}'
        return src, dest

    # def download(self, src, dest=os.getcwd()):
    #     if dest != os.getcwd():
    #         dest = os.getcwd() + '/' + dest
    #     remote_dir = f'{self.remote}:{src}'
    #     cmd = ['copy', remote_dir, dest]
    #     return self.execute(cmd)

    def ls(self, dir=''):
        remote_dir = f'{self.remote}:{dir}'
        cmd = ['lsf', remote_dir]
        return self.execute(cmd)

    def size(self, dir=''):
        remote_dir = f'{self.remote}:{dir}'
        cmd = ['size', remote_dir]
        return self.execute(cmd)
