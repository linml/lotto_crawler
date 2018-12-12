# coding: utf8

import tornado.ioloop
import tornado.web

from lotto.dao import db_find_result
from lotto.lotto import check_lotto
from util.utils import get_int


class ResultHandler(tornado.web.RequestHandler):
    def get(self):
        lotto_id = ''
        count = 10
        ret = {
            "code": 0,
            "msg": "",
            "data": []
        }

        if self.request.arguments.has_key('lotto_id'):
            lotto_id = get_int(self.get_argument('lotto_id', ''))
        if self.request.arguments.has_key('count'):
            count = get_int(self.get_argument('count', ''))

        if not check_lotto(lotto_id):
            ret["code"] = 100
            ret["msg"] = "找不到该彩票"
        else:
            ret["data"] = db_find_result(lotto_id, count)

        self.write(ret)


def make_app():
    return tornado.web.Application([
        (r"/results", ResultHandler),
    ])


if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
