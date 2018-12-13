# coding: utf8
import json

import requests
from bs4 import BeautifulSoup

from util.utils import get_string


class ParserBase(object):
    def analyze(self, html):
        issue = ""
        number = ""
        return [[issue, number]]

    def headers(self):
        return {}


class ParserHtml_ssc_wangyi(ParserBase):
    """
    时时彩
    网易
    http://caipiao.163.com/award/cqssc/
    """
    def __init__(self):
        self.name = ""

    def analyze(self, html):
        find_string1 = r'<table width="100%" border="0" cellspacing="0" class="awardList">'
        find_string2 = r'</table>'
        pos1 = html.find(find_string1)
        pos2 = html.find(find_string2, pos1)
        if not (pos2 > pos1 > 0):
            return []
        pos1 += len(find_string1)
        data = html[pos1:pos2]

        handler_data = []
        soup = BeautifulSoup(data)
        for tr in soup.find_all('tr'):
            tds = tr.find_all('td', class_="start")
            if len(tds) < 3:
                continue
            for td in tds:
                try:
                    issue = "20" + td["data-period"]
                    number = get_string(td["data-win-number"]).replace(" ", ",")
                    if len(issue) != 11:
                        continue
                    if len(number) != 9:
                        continue
                    handler_data.append([issue, number])
                except:
                    pass
        handler_data.sort(key=lambda x: x[0])
        return handler_data


class ParserHtml_ssc_500(ParserBase):
    """
    时时彩
    500
    https://m.500.com/info/kaijiang/ssc/
    """
    def __init__(self):
        self.name = ""

    def analyze(self, html):
        find_string1 = r'<ul class="info-table">'
        find_string2 = r'</section>'
        pos1 = html.find(find_string1)
        pos2 = html.find(find_string2, pos1)
        if not (pos2 > pos1 > 0):
            return []
        pos1 += len(find_string1)
        data = html[pos1:pos2]

        handler_data = []
        soup = BeautifulSoup(data)
        for ul in soup.find_all('ul'):
            lis = ul.find_all('li')
            if len(lis) < 3:
                continue
            issue = lis[0].contents[0]
            number = get_string(lis[2].contents[0]).replace('\t', '').replace('\r', '').replace('\n', '')
            if len(issue) != 11:
                continue
            if len(number) != 9:
                continue
            handler_data.append([issue, number])

        handler_data.sort(key=lambda x: x[0])
        return handler_data


class ParserHtml_opencai_normal(ParserBase):
    """
    通用
    开奖通
    http://r.apiplus.net/newly.do?token=a6f237da9e631cff84e062a8be7d36a8&code=cqssc&rows=20&format=json
    """
    def __init__(self):
        self.name = ""

    def analyze(self, html):
        handler_data = []
        try:
            html_json = json.loads(html)
            result_list = html_json["data"]
            for result in result_list:
                issue = result["expect"]
                number = result["opencode"]
                handler_data.append([issue, number])
        except Exception, e:
            print e

        handler_data.sort(key=lambda x: x[0])
        return handler_data


class ParserHtml_fc3d_gov(ParserBase):
    """
    福彩3D
    中国福利彩票
    http://www.cwl.gov.cn/cwl_admin/kjxx/findDrawNotice?name=3d&issueCount=30
    """
    def __init__(self):
        self.name = ""

    def headers(self):
        return {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36",
            "Accept-Language": "zh-CN,zh;q=0.8,en;q=0.6",
            "Cache-Control": "max-age=0",
            "Referer": "http://www.cwl.gov.cn/"
    }

    def analyze(self, html):
        handler_data = []
        try:
            html_json = json.loads(html)
            result_list = html_json["result"]
            for result in result_list:
                issue = result["code"]
                number = result["red"]
                handler_data.append([issue, number])
        except Exception, e:
            print e

        handler_data.sort(key=lambda x: x[0])
        return handler_data


def get_parser_handler(name):
    obj_name = "ParserHtml_" + name
    obj = None
    if obj_name in globals():
        obj = globals()[obj_name]()
    return obj


def test_parser(name, url):
    r = requests.get(url)
    obj = get_parser_handler(name)
    obj.analyze(r.content)


if __name__ == '__main__':
    # test_parser("ssc_wangyi", "http://caipiao.163.com/award/cqssc/")
    # test_parser("fc3d_gov", "http://www.cwl.gov.cn/cwl_admin/kjxx/findDrawNotice?name=3d&issueCount=30")
    test_parser("ssc_500", "https://m.500.com/info/kaijiang/ssc/")