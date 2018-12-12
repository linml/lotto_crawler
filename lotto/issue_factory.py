# coding:utf8
from datetime import datetime, timedelta, date, time

from dao import db_find_lotto_factory, db_find_code_lotto, db_gen_issue_table, db_insert_issue_many
from util.time_utils import CP
from util.utils import get_date_string, get_datetime, get_time_string, get_int, get_string


class IssueFactory(object):
    IssueType1 = 1  # 每天期号在同一天, 时间间隔相同
    IssueType2 = 2  # 期号夸天生成, 时间间隔相同
    IssueType3 = 3  # 期号夸天生成, 时间间隔不相同
    IssueType4 = 4  # 每天期号在同一天, 时间间隔相同, 期号永久累计自增
    IssueType5 = 5  # 每天一期, 春节不开奖
    IssueType6 = 6  # 每天期号在同一天, 时间间隔不相同 重庆彩

    def __init__(self):
        self.lotto_id = 0
        self.status = 0
        self.count = 0
        self.issue_interval = 0
        self.iss_bit = 0
        self.block_sec = 0
        self.start_time = ""
        self.end_time = ""
        self.issue_type = 0
        self.offset = ""
        self.extra_info = ""

    def init(self, params):
        self.lotto_id = get_int(params.get('lotto_id', ''))
        self.status = get_int(params.get('status', ''))
        self.count = get_int(params.get('count', ''))
        self.issue_interval = get_int(params.get('issue_interval', ''))
        self.iss_bit = get_int(params.get('iss_bit', ''))
        self.block_sec = get_int(params.get('block_sec', ''))
        self.start_time = get_string(params.get('start_time', ''))
        self.end_time = get_string(params.get('end_time', ''))
        self.issue_type = get_int(params.get('issue_type', ''))
        self.offset = get_int(params.get('offset', ''))
        self.extra_info = get_string(params.get('extra_info', ''))

    def gen_issue(self, day_date):
        """

        :param day_date: date datetime
        :return: list
        """
        data = []
        if self.issue_type == self.IssueType1:
            head_issue = get_date_string(day_date)
            index = get_datetime(head_issue+self.start_time)
            start_time = get_datetime(head_issue+self.end_time) - timedelta(days=1)

            for i in range(1, self.count+1):
                issue_interval = timedelta(seconds=self.issue_interval)
                index += issue_interval
                end_time = index

                block_sec = timedelta(seconds=self.block_sec)
                lock_time = index - block_sec

                issue_format = "%s%0{0}d".format(self.iss_bit)

                issue = issue_format % (head_issue, i)

                data.append([
                    self.lotto_id,
                    issue,
                    get_time_string(start_time),
                    get_time_string(lock_time),
                    get_time_string(end_time),
                    get_time_string(end_time)[:8],
                ])
                start_time = end_time

            return data
        elif self.issue_type == self.IssueType2:
            head_issue = get_date_string(day_date)
            index = get_datetime(head_issue + self.start_time)
            start_time = get_datetime(head_issue + self.end_time)

            for i in range(1, self.count + 1):
                issue_interval = timedelta(seconds=self.issue_interval)
                index += issue_interval
                end_time = index

                block_sec = timedelta(seconds=self.block_sec)
                lock_time = index - block_sec

                issue_format = "%s%0{0}d".format(self.iss_bit)

                issue = issue_format % (head_issue, i)

                data.append([
                    self.lotto_id,
                    issue,
                    get_time_string(start_time),
                    get_time_string(lock_time),
                    get_time_string(end_time),
                    get_time_string(end_time)[:8],
                ])
                start_time = end_time

            return data
        elif self.issue_type == self.IssueType3:
            return data
        elif self.issue_type == self.IssueType4:

            extra_info = self.extra_info.split("|")
            if len(extra_info) != 2:
                return data
            point_issue = get_int(extra_info[0])
            point_issue_time = extra_info[1]

            pre_time = get_datetime(point_issue_time)
            pre_issue = point_issue

            diff_day = (datetime.strptime(str(day_date), '%Y-%m-%d') - pre_time).days + 1

            head_issue = get_date_string(day_date)
            index = get_datetime(head_issue + self.start_time)
            start_time = get_datetime(head_issue + self.end_time) - timedelta(days=1)

            for i in range(1, self.count + 1):
                issue_interval = timedelta(seconds=self.issue_interval)
                index += issue_interval
                end_time = index

                block_sec = timedelta(seconds=self.block_sec)
                lock_time = index - block_sec

                issue_format = "%d"

                issue = issue_format % (pre_issue + self.count*(diff_day - 1) + i)

                data.append([
                    self.lotto_id,
                    issue,
                    get_time_string(start_time),
                    get_time_string(lock_time),
                    get_time_string(end_time),
                    get_time_string(end_time)[:8],
                ])
                start_time = end_time

            return data
        elif self.issue_type == self.IssueType5:

            if CP.spring_first <= day_date < CP.spring_last:
                return data

            head_issue = get_date_string(day_date)
            start_time = None
            if CP.spring_last == day_date:
                t = get_date_string(CP.spring_first - timedelta(days=1))
                start_time = get_datetime(t + self.end_time)
            else:
                t = get_date_string(day_date - timedelta(days=1))
                start_time = get_datetime(t + self.end_time)

            lock_time = get_datetime(head_issue + self.end_time) - timedelta(minutes=10)
            end_time = get_datetime(head_issue + self.end_time)

            if CP.spring_last > day_date:
                issue = '%04d%03d' % (day_date.year, (day_date - date(day_date.year, 1, 1)).days + 1)
            else:
                issue = '%04d%03d' % (day_date.year,
                                      (day_date - date(day_date.year, 1, 1)).days - (
                                              CP.spring_last - CP.spring_first).days + 1)

            data.append([
                self.lotto_id,
                issue,
                get_time_string(start_time),
                get_time_string(lock_time),
                get_time_string(end_time),
                get_time_string(end_time)[:8],
            ])
            return data
        elif self.issue_type == self.IssueType6:

            if CP.spring_first <= day_date < CP.spring_last:
                return data

            d = datetime.combine(day_date, time(0, 0))

            start_time = get_time_string(d)
            for index in range(1, 121):
                if index < 24:
                    d += timedelta(minutes=5)
                elif 24 == index:
                    d = datetime.combine(day_date, time(10, 0))
                elif index < 97:
                    d += timedelta(minutes=10)
                else:
                    d += timedelta(minutes=5)

                end_time = get_time_string(d)
                if index < 24 or index >= 97:
                    lock_time = get_time_string(d - timedelta(seconds=20))
                else:
                    lock_time = get_time_string(d - timedelta(seconds=25))

                issue = get_date_string(day_date) + '%03d' % index
                data.append([self.lotto_id, issue, start_time, lock_time, end_time, end_time[:8]])
                start_time = end_time
            return data


def gen_lotto_issue():
    lotto_list = db_find_code_lotto({})
    for lotto_info in lotto_list:
        db_gen_issue_table(lotto_info.get("lotto_id"))

    factory_list = db_find_lotto_factory({})

    for params in factory_list:
        lotto_info = db_find_code_lotto({"lotto_id": params.get("lotto_id")})
        if lotto_info:
            lotto_info = lotto_info[0]
            if get_int(lotto_info.get("status")) != 1:
                continue
        else:
            continue
        issue_obj = IssueFactory()
        issue_obj.init(params)

        d = date.today()
        for x in xrange(3):
            issue_list = issue_obj.gen_issue(d)
            if not issue_list:
                break
            d += timedelta(days=1)

            db_insert_issue_many(lotto_info.get("lotto_id"), issue_list)


if __name__ == '__main__':
    gen_lotto_issue()
