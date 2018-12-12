# coding: utf8
from tornado.ioloop import IOLoop

from lotto.issue_factory import gen_lotto_issue
from lotto.lotto import run_crawler


def main():
    IOLoop.instance().add_callback(gen_lotto_issue)
    IOLoop.instance().add_callback(run_crawler)
    IOLoop.instance().start()


if __name__ == '__main__':
    main()
