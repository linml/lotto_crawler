# coding=utf-8
from decimal import Decimal, ROUND_DOWN
from inspect import stack
from urlparse import *
import sys
import json
import string
import time
import random
from datetime import datetime, date
from tornado.concurrent import Future
from tornado.curl_httpclient import CurlAsyncHTTPClient
from tornado.httpclient import HTTPRequest


def get_host(url):
    r = urlparse(url)
    if r.scheme == "" or r.netloc == "":
        return None
    return str(r.netloc)


def is_string(s):
    return isinstance(s, basestring)


def is_float_string(float_string):
    if not is_string(float_string):
        return False
    try:
        f = float(float_string)
        return True
    except:
        pass
    return False


def is_int_string(int_string):
    if not is_string(int_string):
        return False
    if int_string.startswith('-'):
        return int_string[1:].isdigit()
    return int_string.isdigit()


def is_time_string(time_string):
    if not is_int_string(time_string) or len(time_string) != 14:
        return False
    return True


def is_ip_string(ip_string):
    return is_string(ip_string) and ip_string.count('.') == 3


def is_date_string(date_string):
    if not is_int_string(date_string) or len(date_string) != 8:
        return False
    return True


def sequence_to_string(data):
    if isinstance(data, (list, tuple)):
        return [sequence_to_string(x) for x in data]
    elif isinstance(data, dict):
        return {sequence_to_string(k): sequence_to_string(v) for k, v in data.iteritems()}
    return get_string(data)


def sequence_to_unicode_string(data):
    if isinstance(data, (list, tuple)):
        return [sequence_to_unicode_string(x) for x in data]
    elif isinstance(data, dict):
        return {sequence_to_unicode_string(k): sequence_to_unicode_string(v) for k, v in data.iteritems()}
    return get_unicode_string(data)


def get_int(i, d=0):
    try:
        return int(i)
    except:
        pass
    return d


def get_float(f, d=0.0):
    try:
        return float(f)
    except:
        pass
    return d


def get_bool(b, d=False):
    try:
        return bool(b)
    except:
        pass
    return d


def get_string(s, d=''):
    try:
        if isinstance(s, str):
            return s
        elif isinstance(s, unicode):
            return s.encode('utf8')
        elif isinstance(s, Decimal):
            return str(s.quantize(Decimal('1.00'), rounding=ROUND_DOWN))
        elif isinstance(s, float):
            return '%.2f' % s
        elif isinstance(s, bool):
            return '0' if s else '1'
        elif s is None:
            return ''
        else:
            return str(s)
    except:
        pass
    return d


def get_unicode_string(s, d=u''):
    try:
        if isinstance(s, str):
            return s.decode('utf8')
        elif isinstance(s, unicode):
            return s
        elif isinstance(s, Decimal):
            return unicode(s.quantize(Decimal('1.00'), rounding=ROUND_DOWN))
        elif isinstance(s, float):
            return u'%.2f' % s
        elif isinstance(s, bool):
            return u'0' if s else u'1'
        elif s is None:
            return u''
        else:
            return unicode(s)
    except:
        pass
    return d


def get_decimal(dec, d=Decimal(0)):
    try:
        if isinstance(dec, Decimal):
            return dec
        return Decimal(str(dec))
    except:
        pass
    return d


def get_datetime(time_string=''):
    if not time_string or not is_time_string(time_string):
        return datetime.now()
    return datetime.strptime(time_string, '%Y%m%d%H%M%S')


def get_time_string(t='', d=None):
    if isinstance(t, (float,)):
        return time.strftime('%Y%m%d%H%M%S', time.localtime(t))
    elif isinstance(t, (datetime,)):
        return t.strftime('%Y%m%d%H%M%S')

    return time.strftime('%Y%m%d%H%M%S', time.localtime(d))


def format_time_string(t):
    return ''.join([
        t[:4], '-',
        t[4:6], '-',
        t[6:8], ' ',
        t[8:10], ':',
        t[10:12], ':',
        t[12:14]
    ])


def get_date_object(s=''):
    if isinstance(s, basestring):
        if len(s) >= 8 and s.isdigit():
            return date(year=int(s[:4]), month=int(s[4:6]), day=int(s[6:8]))
    return date.today()


def get_date_string(t='', d=None):
    if isinstance(t, (float,)):
        return time.strftime('%Y%m%d', time.localtime(t))
    elif isinstance(t, (datetime, date)):
        return t.strftime('%Y%m%d')
    return time.strftime('%Y%m%d', time.localtime(d))


def calc_list_page(count, row_count, page):
    row_count = get_int(row_count, 9)
    if row_count <= 0:
        row_count = 9

    max_page = (count + row_count - 1) / row_count
    page = get_int(page, 1)
    if page <= 0:
        page = 1
    elif page > max_page:
        page = max_page
    return page, max_page, row_count


def get_current_function_name():
    try:
        raise Exception
    except:
        f = sys.exc_info()[2].tb_frame.f_back
    return f.f_code.co_name


def get_permutation_count(a, r):
    count = 1
    for x in xrange(a, a - r, -1):
        count *= x
    return count


def get_combination_count(c, r):
    if 0 > r:
        return 0
    elif 0 == r:
        return 1
    elif 1 == r:
        return c
    elif 2 == r:
        return c * (c - 1) / 2
    return get_permutation_count(c, r) / get_permutation_count(r, r)


def get_combination_list_count(lc, lr):
    if not (len(lc) == len(lr) == 2):
        return 0

    repeat_count = 0
    for x in lc[0]:
        if x in lc[1]:
            repeat_count += 1

    return get_combination_count(len(lc[0]), lr[0]) * get_combination_count(len(lc[1]), lr[1]) - get_combination_count(
        len(lc[0]) - 1, lr[0] - 1) * get_combination_count(len(lc[1]) - 1, lr[1] - 1) * repeat_count


def div_list(l, n):
    return [l[i:i + n] for i in xrange(0, len(l), n)]


def chain_for(array, index=0):
    if index < len(array):
        for v in array[index]:
            for item in chain_for(array, index + 1):
                yield (v,) + item
    else:
        yield ()


def continuations(iterable, r):
    pool = tuple(iterable)
    n = len(pool)
    if r > n:
        return
    for i in xrange(n):
        if i + r > n:
            break
        yield pool[i: i + r]


def lstrip0(s):
    s = s.lstrip('0')
    if not s:
        s = '0'
    return s


class TimeLogger(object):
    def __init__(self):
        self.t = datetime.now()

    def __del__(self):
        t = datetime.now()
        print stack()[1][2:4], t - self.t
        self.t = datetime.now()

    def print_time_delta(self):
        t = datetime.now()
        print stack()[1][2:4], t - self.t
        self.t = datetime.now()


def get_html(url, params=None):
    if params is None:
        params = {}
    future = Future()

    def handle_response(response):
        if response.error:
            # future.set_exception(response.error)
            future.set_result('')
        else:
            future.set_result(response.body)

    curl_client = CurlAsyncHTTPClient()

    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 "
                      "(KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36",
        "Accept-Language": "zh-CN,zh;q=0.8,en;q=0.6",
        "Cache-Control": "max-age=0",
    }
    if params.get('headers'):
        headers = params.get('headers')
    request = HTTPRequest(url=url, headers=headers)
    if params.get("host") and params.get("port"):
        request.proxy_host = params.get("host")
        request.proxy_port = get_int(params.get("port"))
    curl_client.fetch(request, handle_response)

    return future

def json_loads_utf8_util(data):
    """
    json.loads解码后没有str,只有unicode
    此函数将unicode全部转化为utf8 str
    """
    data = json.loads(get_string(data))
    return {get_string(k): get_utf8_str(v) for k, v in data.iteritems()}


def get_utf8_str(s):
    if isinstance(s, unicode):
        s = s.encode('utf8')
    return s


class HttpJsonEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, (Decimal, )):
            return '%s' % o
        return super(HttpJsonEncoder, self).default(o)


def json_dumps_util(data):
    return json.dumps(data, cls=HttpJsonEncoder)


def load_json_util(data):
    return json_loads_utf8_util(json_dumps_util(data))


def load_json_array_util(data):
    return [json_loads_utf8_util(json_dumps_util(v)) for v in data]


def gen_random_string(n):
    random_seq = string.ascii_lowercase + string.digits
    u_num = ''.join([random.choice(random_seq) for _ in xrange(n)])
    return u_num


def format_date_str(str_s, str_before, str_after):
    try:
        str_s = datetime.strptime(str_s, str_before).strftime(str_after)
    except Exception, e:
        print e
    return str_s


def format_strip(str_c):
    s = str_c.strip(' \t\n\r').replace(' ', '')
    return s


if __name__ == '__main__':
    print gen_random_string(5)
