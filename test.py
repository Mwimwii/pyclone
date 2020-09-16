#!/usr/bin/python
from subprocess import Popen, PIPE, STDOUT
import io


def __main__():
    try:
        p = Popen(["ping", "-n", "3", "127.0.0.1"],
                  stdin=PIPE, stdout=PIPE, stderr=STDOUT)
    except:
        print("Popen failed")
        quit()
    sout = io.open(p.stdout.fileno(), 'rb', closefd=False)
    while True:
        buf = sout.read1(1024)
        if len(buf) == 0:
            break
        print(buf),


if __name__ == '__main__':
    __main__()
