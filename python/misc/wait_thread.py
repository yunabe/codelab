# Python script that shows we can use waitpid with thread.
# I think this does not work in Linux before 2.4.
# (Read 'Linux Notes' in man wait)

import os
import threading
import time

class WaitThread(threading.Thread):
    def __init__(self, pid):
        threading.Thread.__init__(self)
        self.__pid = pid

    def run(self):
        print 'waiting', self.__pid
        os.waitpid(self.__pid, 0)


def main():
    pid = os.fork()
    if pid != 0:
        th = WaitThread(pid)
        th.start()
        th.join()
    else:
        time.sleep(1)


if __name__ == '__main__':
    main()
