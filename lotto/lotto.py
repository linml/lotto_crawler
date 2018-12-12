# coding: utf8
from datetime import datetime, timedelta
from functools import partial

from tornado.gen import coroutine
from tornado import gen
from tornado.ioloop import IOLoop
from traceback import format_exc

from dao import db_get_last_issue_info, db_draw_result, db_get_next_issue_info, db_find_code_lotto, \
    db_find_lotto_parser_url, db_find_result
from push import notice_lotto_result
from parser import ParserBase, get_parser_handler
from util.log import info
from util.utils import gen_random_string, get_html, get_time_string, get_host, get_int, get_string, get_datetime


def check_lotto(lotto_id):
    return get_int(lotto_id) in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40]


def filter_lotto_data(lotto_id, data_list):
    """
    1   重庆时时彩
    2   新疆时时彩
    3   天津时时彩
    4   分分彩
    5   两分彩
    6   三分彩
    7   五分彩
    8   山东11选5
    9   江西11选5
    10  广东11选5
    11  江苏11选5
    12  安徽11选5
    13  山西11选5
    14  上海11选5
    15  分分11选5
    16  江苏快3
    17  安徽快3
    18  湖北快3
    19  河南快3
    20  江苏骰宝
    21  分分快3
    22  北京PK10
    23  幸运飞艇
    24  分分PK10
    25  福彩3D
    26  排列3
    27  排列5
    28  广东快乐十分
    29  重庆快乐十分
    30  天津快乐十分
    31  北京快乐8
    32  加拿大基诺
    33  分分快乐彩
    34  台湾宾果
    35  北京幸运28
    36  加拿大幸运28
    37  台湾幸运28
    38  香港六合彩
    39  五分六合彩
    40  十分六合彩
    :param data_list:
    :return:
    """
    ret_list = []
    for data in data_list:
        number_list = data[1].split(",")

        if lotto_id in (1, 2, 3, 4, 5, 6, 7,):  # 0-9
            if len(number_list) != 5:
                continue
            f = 1
            for num in number_list:
                n = int(num)
                if not (0 <= n <= 9):
                    f = 0
                    break
            if not f:
                continue

        elif lotto_id in (8,  9, 10, 11, 12, 13, 14, 15,):  # 1-11
            if len(number_list) != 5:
                continue
            f = 1
            for num in number_list:
                n = int(num)
                if not (1 <= n <= 11):
                    f = 0
                    break
            if not f:
                continue

        elif lotto_id in (16, 17, 18, 19, 20, 21, ):  # 1-6
            if len(number_list) != 3:
                continue
            f = 1
            for num in number_list:
                n = int(num)
                if not (1 <= n <= 6):
                    f = 0
                    break
            if not f:
                continue

        elif lotto_id in (22, 23, 24, ):  # 1-10
            if len(number_list) != 10:
                continue
            f = 1
            for num in number_list:
                n = int(num)
                if not (1 <= n <= 10):
                    f = 0
                    break
            if not f:
                continue

        elif lotto_id in (25, 26,):  # 0-9
            if len(number_list) != 3:
                continue
            f = 1
            for num in number_list:
                n = int(num)
                if not (0 <= n <= 9):
                    f = 0
                    break
            if not f:
                continue

        elif lotto_id in (27,):  # 0-9
            if len(number_list) != 5:
                continue
            f = 1
            for num in number_list:
                n = int(num)
                if not (0 <= n <= 9):
                    f = 0
                    break
            if not f:
                continue

        elif lotto_id in (28, 29, 30, ):  # 1-20
            if len(number_list) != 8:
                continue
            f = 1
            for num in number_list:
                n = int(num)
                if not (1 <= n <= 20):
                    f = 0
                    break
            if not f:
                continue

        elif lotto_id in (31, 32, 33, 34, ):  # 1-80
            if len(number_list) != 20:
                continue
            f = 1
            for num in number_list:
                n = int(num)
                if not (1 <= n <= 80):
                    f = 0
                    break
            if not f:
                continue

        elif lotto_id in (38, 39, 40):  # 1-49
            if len(number_list) != 7:
                continue
            f = 1
            for num in number_list:
                n = int(num)
                if not (1 <= n <= 49):
                    f = 0
                    break
            if not f:
                continue
        ret_list.append(data)
    return ret_list


class IssueInfo(object):
    def __init__(self):
        self.issue = ""
        self.start_time = datetime.now()
        self.stop_time = datetime.now()
        self.result_time = datetime.now()

    def set_issue(self, issue):
        self.issue = issue

    def set_start_time(self, t):
        self.start_time = get_datetime(t)

    def set_stop_time(self, t):
        self.stop_time = get_datetime(t)

    def set_result_time(self, t):
        self.result_time = get_datetime(t)

    def get_left_second(self, t):
        return (self.result_time - t).total_seconds()


class LottoBase(object):

    def __init__(self):

        self.lotto_id = ''
        self.lotto_name = ''
        self.lotto_status = ''

        self.url = ''
        self.parser_name = ''
        self.parser_obj = ParserBase()
        self.url_status = ''

        self.work_id = ''

        self.last_issue = IssueInfo()
        self.next_issue = IssueInfo()
        self.left_second = 0
        
    def init(self, params):
        self.set_lotto_id(params.get('lotto_id'))
        self.set_lotto_name(params.get('lotto_name'))
        self.set_lotto_status(params.get('lotto_status'))
        
        self.set_url(params.get('url'))
        self.set_parser_name(params.get('parser_name'))
        self.set_url_status(params.get('url_status'))

        self.parser_obj = get_parser_handler(self.parser_name)
        self.work_id = self.gen_work_id()

        self.last_issue = IssueInfo()
        self.next_issue = IssueInfo()

    @staticmethod
    def gen_work_id():
        return gen_random_string(6)

    def get_work_id(self):
        return self.work_id

    def update_work_id(self):
        self.work_id = self.gen_work_id()

    def get_url(self):
        return self.url

    def set_url(self, url):
        self.url = url

    def set_parser_name(self, name):
        self.parser_name = name

    def get_lotto_status(self):
        return self.lotto_status

    def set_lotto_status(self, status):
        self.lotto_status = get_int(status)

    def get_url_status(self):
        return self.url_status

    def set_url_status(self, status):
        self.url_status = status

    def get_lotto_id(self):
        return self.url_status

    def set_lotto_id(self, lotto_id):
        self.lotto_id = get_int(lotto_id)

    def get_lotto_name(self):
        return self.lotto_name

    def set_lotto_name(self, lotto_name):
        self.lotto_name = lotto_name

    @coroutine
    def get_html(self):
        _params = {}
        headers = self.parser_obj.headers()
        if headers:
            _params["headers"] = headers
        html = yield get_html(self.url, params=_params)
        raise gen.Return(html)

    def parser_data(self, html):
        data = self.parser_obj.analyze(html)
        return data

    def refresh_last_issue(self):
        info = db_get_last_issue_info(self.lotto_id)
        if not info:
            info = {}
        self.last_issue.set_issue(info.get('issue'))
        self.last_issue.set_start_time(info.get('start_time'))
        self.last_issue.set_stop_time(info.get('stop_time'))
        self.last_issue.set_result_time(info.get('result_time'))

    def refresh_next_issue(self):
        info = db_get_next_issue_info(self.lotto_id, self.last_issue.issue)
        if not info:
            info = {}
        self.next_issue.set_issue(info.get('issue'))
        self.next_issue.set_start_time(info.get('start_time'))
        self.next_issue.set_stop_time(info.get('stop_time'))
        self.next_issue.set_result_time(info.get('result_time'))

    def save_data(self, data_list):
        for data in data_list:
            issue = data[0]
            numbers = data[1]
            if not db_find_result(self.lotto_id, {"issue": issue, "status": 1}) and db_find_result(self.lotto_id, {"issue": issue}):
                notice_lotto_result(self.lotto_id, issue, numbers)
            db_draw_result(self.lotto_id, issue, numbers, self.url)

    @coroutine
    def run(self):
        interval = 5
        if self.lotto_status != 1 or self.url_status != 1:
            return

        try:
            html = yield self.get_html()
            data_list = self.parser_data(html)
            data_list = filter_lotto_data(self.lotto_id, data_list)

            msg = "{0}=>".format(get_string(self.lotto_name))
            if data_list:
                self.refresh_last_issue()
                self.save_data(data_list)
                crawler_last_issue = max(data_list, key=lambda x: x[0])[0]
                if self.last_issue.issue >= crawler_last_issue:
                    msg += "已有最新期号:{}".format(self.last_issue.issue)
                else:
                    msg += "更新最新:{}".format(crawler_last_issue)
            else:
                msg += "无数据,最后{}期".format(self.last_issue.issue)

            now = datetime.now()
            self.refresh_last_issue()
            if self.last_issue.issue:
                self.refresh_next_issue()
                left_second = get_int(self.next_issue.get_left_second(now))
                if left_second > 0:
                    interval = left_second

                msg += ";下一期{}期将在{}开奖".format(self.next_issue.issue, self.next_issue.result_time)
            msg += ";系统%s秒后采集" % interval
            info(msg)
        except Exception as e:
            print format_exc()
            print e

        finally:
            IOLoop.instance().add_timeout(
                timedelta(
                    milliseconds=interval * 1000),
                partial(
                    self.run))


def run_crawler():
    lotto_info_list = db_find_code_lotto({"status": 1})
    for lotto_info in lotto_info_list:
        crawler_url_list = db_find_lotto_parser_url({"lotto_id": lotto_info.get("lotto_id"), "status": 1})
        for crawler_url in crawler_url_list:
            params = {
                "lotto_id": lotto_info.get("lotto_id"),
                "lotto_name": lotto_info.get("name"),
                "lotto_status": lotto_info.get("status"),

                "url": crawler_url.get("url"),
                "parser_name": crawler_url.get("parser_obj"),
                "url_status": crawler_url.get("status"),
            }

            lotto_obj = LottoBase()
            lotto_obj.init(params)
            print "开始采集:", crawler_url.get("url"), lotto_info.get("name"), "\t"
            IOLoop.instance().add_callback(partial(lotto_obj.run))


if __name__ == '__main__':
    IOLoop.instance().add_callback(run_crawler)
    IOLoop.instance().start()
