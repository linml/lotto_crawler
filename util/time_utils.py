# coding=utf-8

from lunardate import LunarDate
from datetime import datetime, timedelta
from datetime import date
from platform import system
import os


def set_system_time(datetime_obejct):
    system_string = system()
    if system_string.startswith('Linux'):
        os.system(datetime_obejct.strftime('date -s "%Y-%m-%d %H:%M:%S"'))
    elif system_string.startswith('Darwin'):
        os.system(datetime_obejct.strftime('date %m%d%H%M%Y.%S'))
    elif system_string.startswith('Windows'):
        os.system(datetime_obejct.strftime('date %Y-%m-%d'))
        os.system(datetime_obejct.strftime('time %H:%M:%S.') +
                  datetime_obejct.strftime('%f')[:2])


def get_beginning_spring(year):
    '''
    立春准确时间的计算方法
    计算公式：[Y*D+C]-L
    公式解读：年数的后2位乘0.2422加3.87取整数减闰年数。21世纪C值=3.87，22世纪C值=4.15。
    举例说明：2058年立春日期的计算步骤[58×.0.2422+3.87]-[(58-1)/4]=17-14=3，则2月3日立春。
    '''
    return date(year=year, month=2,
                day=(int(year % 100 * 0.2422 + 3.87) - int((year % 100 - 1) / 4)))


def get_chinese_zodiac(d=None):
    '''
    子鼠、丑牛、寅虎、卯兔、辰龙、巳蛇、午马、未羊、申猴、酉鸡、戌狗、亥猪。
    '''
    if not isinstance(d, date):
        d = date.today()

    zodiac = d.year - 2008
    if d < get_beginning_spring(d.year):
        zodiac -= 1
    return zodiac % 12


class CP(object):
    regular_year = None
    regular_year_month = None
    regular_abb_year_month = None
    spring_first = None
    spring_last = None  # 这里是[)
    chinese_zodiac = -1
    zodiac_number_table = [_ for _ in xrange(1, 13, 1)]
    current_year = -1
    need_odds = False

    def __init__(self):
        super(CP, self).__init__()

    @staticmethod
    def change_year(year):
        if not (CP.spring_first and CP.spring_last and
                        CP.spring_first.year == year and CP.spring_last.year == year):
            CP.spring_first = (LunarDate(year, 1, 1) - timedelta(days=1)).toSolarDate()
            CP.spring_last = CP.spring_first + timedelta(days=7)

        if CP.current_year != year:
            d = datetime.now()
            year = d.year
            # month = d.month

            CP.regular_year_month = '^201\d((0\d)|(1[0-2]))(([0-2]\d)|(3[01]))'
            CP.regular_abb_year_month = '^1\d((0\d)|(1[0-2]))(([0-2]\d)|(3[01]))'
            CP.regular_year = '^201\d'
            CP.current_year = year

            CP.chinese_zodiac = get_chinese_zodiac()
            CP.zodiac_number_table = CP.zodiac_number_table[CP.chinese_zodiac::-1] + \
                                     CP.zodiac_number_table[:CP.chinese_zodiac:-1]


def init_cp():
    CP.change_year(datetime.now().year)


def spring_count(date_object):
    count = CP.spring_first.year - 2016
    return count + 1 if date_object > CP.spring_last else count


if __name__ != '__main__':
    init_cp()
