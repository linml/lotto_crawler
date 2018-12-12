# coding: utf8

from base.db_popl import query_for_list, update, insert_many, query_for_dict
from util.utils import get_time_string


def db_gen_issue_table(lotto_id):
    call_sql = "CALL CreateLottoIssueTable(%s)"
    update(call_sql, lotto_id)


def db_find_code_lotto(params=None):
    if params is None:
        params = {}
    query_sql = "SELECT * FROM code_lotto WHERE 1=1 "

    if params.get("lotto_id"):
        query_sql += " AND lotto_id=%(lotto_id)s "
    if params.get("status"):
        query_sql += " AND status=%(status)s "

    return query_for_list(query_sql, params)


def db_find_lotto_factory(params=None):
    if params is None:
        params = {}
    query_sql = "SELECT * FROM issue_factory WHERE 1=1"

    if params.get("lotto_id"):
        query_sql += " AND lotto_id=%(lotto_id)s "
    if params.get("status"):
        query_sql += " AND status=%(status)s "

    return query_for_list(query_sql, params)


def db_set_code_lotto(lotto_id, filed, val):
    """

    :param lotto_id: int
    :param filed: str status, name
    :param val:
    :return:
    """
    params = {
        "lotto_id": lotto_id,
        filed: val
    }
    update_sql = "UPDATE code_lotto SET {0}=%({0})s WHERE lotto_id=%(lotto_id)s".format(filed)
    return update(update_sql, params)


def db_draw_result(lotto_id, issue, number,crawler_from):
    update_sql = "UPDATE lotto_result_{0} SET draw_number=%s,status=1,update_time=%s, crawler_from=%s WHERE issue=%s AND status=0".format(lotto_id)
    update(update_sql, [number, get_time_string(),crawler_from, issue])


def db_insert_issue_many(lotto_id, vals):
    insert_sql = "INSERT IGNORE INTO lotto_result_{0} (lotto_id,issue,start_time,stop_time,result_time,issue_date) VALUES(%s,%s,%s,%s,%s,%s)".format(lotto_id)
    return insert_many(insert_sql, vals)


def db_get_last_issue_info(lotto_id):
    query_sql = "SELECT * FROM lotto_result_{0} WHERE status = 1 AND result_time<={1} ORDER BY issue DESC LIMIT 1".format(lotto_id, get_time_string())
    return query_for_dict(query_sql)


def db_get_next_issue_info(lotto_id, last_issue):
    query_sql = "SELECT * FROM lotto_result_{0} WHERE status=0 AND issue>%s ORDER BY issue ASC LIMIT 1".format(lotto_id)
    return query_for_dict(query_sql, last_issue)


def db_find_lotto_parser_url(params=None):
    if params is None:
        params = {}
    query_sql = "SELECT * FROM lotto_parser_url WHERE 1=1 "

    if params.get("id"):
        query_sql += " AND id=%(id)s "
    if params.get("lotto_id"):
        query_sql += " AND lotto_id=%(lotto_id)s "
    if params.get("status"):
        query_sql += " AND status=%(status)s "

    return query_for_list(query_sql, params)


if __name__ == '__main__':
    print db_gen_issue_table(1)
