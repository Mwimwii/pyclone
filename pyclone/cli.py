"""Console script for pyclone."""
import re
import subprocess
import sys
from .locations import RCLONE_DIR_PATH, RCLONE_PATH, SHELL

pattern = r'(Rclone.+?\n.+?\n\n.+?\n.+walkthroughs.)'
sub_pattern = '''Pyclone is wrapper for Rclone (https://rclone.org) that syncs files to and from cloud storage providers as well as\nmounting them, listing them in lots of different ways.\n\nSee the home page (https://github.com/Mwimwii/pyclone) for installation, usage, documentation,\nchangelog and configuration walkthroughs.'''


def main(args=None):
    return 0

def execute_from_commandline():
    cmd = RCLONE_PATH + sys.argv[1:]
    if ('config' in cmd) and (len(cmd) == 2):
        pipe = subprocess.run(cmd, cwd=RCLONE_DIR_PATH, shell=SHELL)
    else:
        pipe = subprocess.run(cmd, capture_output=True,
                              text=True, cwd=RCLONE_DIR_PATH, shell=SHELL)
        output = pipe.stdout if pipe.stdout else pipe.stderr
        print(rcloneToPyCli(output))


def rcloneToPyCli(output):
    ''' Changes the RClone to PyClone'''
    output = (re.sub('rclone ', 'pyclone ', output))
    return (re.sub(pattern, sub_pattern, output))


if __name__ == '__main__':
    sys.exit(main())
