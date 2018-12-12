# coding=utf-8

import os

from os import getpid, path
from threading import Lock
from time import localtime, strftime
from traceback import format_exc
from util.utils import get_string
from util.singleton import Singleton


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def debug(msg, *args):
    Log().debug(msg, *args)


def info(msg, *args):
    Log().info(msg, *args)


def trace(msg, *args):
    Log().trace(msg, *args)


def warn(msg, *args):
    Log().warn(msg, *args)


def error(msg, *args):
    Log().error(msg, *args)


def critical(msg, *args):
    Log().critical(msg, *args)


def write_html(ip, port, *text):
    file_name = path.join(BASE_DIR, 'log', ''.join([
        'ip_', ip, '_', str(port), '.txt'
    ]))
    with open(file_name, 'w') as f:
        for x in text:
            f.write(str(x))
            f.write('\n')


class Log(object):
    __metaclass__ = Singleton

    def __init__(self):
        super(Log, self).__init__()
        self.thread_lock = Lock()
        self.print_require_level = 0
        self.file_require_level = 0

    def log(self, level, msg, args):
        try:
            self.thread_lock.acquire()

            if args and isinstance(args, tuple):
                msg = msg % tuple(
                    (arg.encode("utf8") if isinstance(arg, unicode)
                     else arg for arg in args))

            if level >= self.print_require_level:
                try:
                    print msg
                except:
                    pass

            if level >= self.file_require_level:
                file_name = path.join(BASE_DIR, 'log', ''.join([
                    'log_',
                    strftime('%Y-%m-%d', localtime()),
                    '_',
                    str(getpid()),
                    '.txt'
                ]))
                f = open(file_name, 'a')
                f.write(get_string(msg))
                f.write('\n')
                f.close()
        except Exception as e:
            print '(' * 6
            print msg
            print args
            print format_exc()
            print ')' * 6
        finally:
            self.thread_lock.release()

    def debug(self, msg, *args):
        self.log(1, ''.join([strftime('[%H:%M:%S]debug   :', localtime()) + msg]), args)

    def info(self, msg, *args):
        self.log(2, ''.join([strftime('[%H:%M:%S]info    :', localtime()) + msg]), args)

    def trace(self, msg, *args):
        self.log(3, ''.join([strftime('[%H:%M:%S]trace   :', localtime()) + msg]), args)

    def warn(self, msg, *args):
        self.log(4, ''.join([strftime('[%H:%M:%S]warn    :', localtime()) + msg]), args)

    def error(self, msg, *args):
        self.log(5, ''.join([strftime('[%H:%M:%S]error   :', localtime()) + msg]), args)

    def critical(self, msg, *args):
        self.log(6, ''.join([strftime('[%H:%M:%S]critical:', localtime()) + msg]), args)


if __name__ == "__main__":
    pass
