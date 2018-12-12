# coding: utf8
import urllib
from json import loads

from tornado.curl_httpclient import CurlAsyncHTTPClient
from tornado.httpclient import HTTPRequest

from dao import lru_db_find_lotto_push
from util.log import info, warn
from util.utils import get_string, get_int


def notice_lotto_result(lotto_id, issue, numbers):
    post_data = {
        "lotto_id": lotto_id,
        "issue": issue,
        "numbers": numbers,
    }
    address_info_list = lru_db_find_lotto_push({"status": 1})

    def handle_response(response):
        if response.error:
            # print response.code
            warn(get_string(response.error))
            pass
        else:
            try:
                result = loads(response.body)
                code = get_int(result.get("code"), -1)
                msg = get_string(result.get("msg"))
                if code == 0:
                    info("==>%s", msg)
                else:
                    warn("=>%s",msg)
            except Exception as e:
                import traceback
                print traceback.format_exc()
                print e

    for address_info in address_info_list:
        curl_client = CurlAsyncHTTPClient()
        url = address_info.get("address")
        request = HTTPRequest(url=url, method='POST', body=urllib.urlencode(post_data))
        curl_client.fetch(request, handle_response)



