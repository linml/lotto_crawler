# coding=utf-8

from contextlib import contextmanager
import DBUtils.PooledDB
import pymysql
import itertools

from decimal import Decimal
from traceback import format_exc

from settings import db_config as DB_KWARGS
from util.log import error, warn
from util.singleton import Singleton
from util.utils import get_int, get_string, sequence_to_string, get_decimal, load_json_util, \
    load_json_array_util

IntegrityError = pymysql.IntegrityError
OperationalError = pymysql.OperationalError
CONN_REMARK = 'Old version BY oys'


class Row(dict):
    """A dict that allows for object-like property access syntax."""

    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError:
            raise AttributeError(name)


class DBPool(object):
    __metaclass__ = Singleton
    used_conn = 0

    def __init__(self):
        super(DBPool, self).__init__()

        self.pool = None
        self.config = DB_KWARGS

        self.min_cached = 5
        self.max_connections = 100
        self.blocking = True

        self.init_pool()

    def init_pool(self):
        self.pool = DBUtils.PooledDB.PooledDB(
            pymysql, mincached=self.min_cached,
            maxconnections=self.max_connections,
            blocking=self.blocking, **self.config)

    def connection(self):
        conn = self.pool.connection()
        return conn


@contextmanager
def db_conn_guard(dict_cursor=False, server_cursor=False):
    conn = DBConn(dict_cursor, server_cursor)
    yield conn
    conn.close()


class DBConn(object):
    def __init__(self, dict_cursor=False, server_cursor=False):
        self.remark = CONN_REMARK
        self.cursor = None
        self.dict_cursor = None
        self.server_cursor = None
        pool = DBPool()
        self.conn = pool.connection()
        self.set_cursor(dict_cursor, server_cursor)

    def __del__(self):
        self.close()

    def close(self):
        try:
            if getattr(self, 'cursor', None) is not None:
                self.cursor.close()
                self.cursor = None
            if getattr(self, 'conn', None) is not None:
                self.conn.close()
                # DBPool().used_conn -= 1
                # print 'del: used conn: %s' % DBPool().used_conn
                self.conn = None
        except Exception as e:
            print format_exc()

    def get_message(self):
        for x in self.cursor.messages:
            yield x[1].args[1]

    def set_cursor(self, dict_cursor, server_cursor):
        if dict_cursor == self.dict_cursor and \
                        server_cursor == self.server_cursor:
            return
        self.dict_cursor = dict_cursor
        self.server_cursor = self.server_cursor

        if server_cursor:
            if dict_cursor:
                self.cursor = self.conn.cursor(pymysql.cursors.SSDictCursor)
            else:
                self.cursor = self.conn.cursor(pymysql.cursors.SSCursor)
        else:
            if dict_cursor:
                self.cursor = self.conn.cursor(pymysql.cursors.DictCursor)

            else:
                self.cursor = self.conn.cursor(pymysql.cursors.Cursor)

    def commit(self):
        try:
            self.conn.commit()
        except Exception as e:
            print format_exc()

    def rollback(self):
        try:
            self.conn.rollback()
        except Exception as e:
            print format_exc()

    def execute(self, query, args=None):
        self.cursor.execute(query, args)

    def executemany(self, query, args=None):
        self.cursor.executemany(query, args)

    def fetchone(self):
        return self.cursor.fetchone()

    def fetchall(self):
        return self.cursor.fetchall()

    def execute_fetchall(self, query, args=None):
        try:
            self.execute(query, args)
            return self.fetchall()
        except Exception as e:
            error('execute_fetchall$$sql:%s$$args:%s$$error:%s', query, sequence_to_string(args), get_string(e))
        return None

    def execute_fetchone(self, query, args=None):
        try:
            self.execute(query, args)
            return self.fetchone()
        except Exception as e:
            error('execute_fetchone$$sql:%s$$args:%s$$error:%s', query, sequence_to_string(args), get_string(e))
        return None

    def update_many(self, query, args=None):
        try:
            self.executemany(query, args)
            if self.cursor.rowcount > 0:
                return True
        except Exception as e:
            error('update_many:%s$$args:%s$$error:%s', query, sequence_to_string(args), get_string(e))
        return False

    def update(self, query, args=None):
        try:
            self.execute(query, args)
            if self.cursor.rowcount > 0:
                return True
        except Exception as e:
            error('update$$sql:%s$$args:%s$$error:%s', query, sequence_to_string(args), get_string(e))
        return False

    def insert_many(self, query, args=None):
        try:
            self.executemany(query, args)
            if self.cursor.rowcount > 0:
                return True
        except Exception as e:
            error('insert_many:%s$$args:%s$$error:%s', query, sequence_to_string(args), get_string(e))
        return False

    def insert(self, query, args=None):
        try:
            self.execute(query, args)
            if self.cursor.rowcount > 0:
                return True
        except Exception as e:
            error('insert$$sql:%s$$args:%s$$error:%s', query, sequence_to_string(args), get_string(e))
        return False

    def query_for_decimal(self, query, args=None, default=Decimal(0)):
        result = self.execute_fetchone(query, args)
        if not result:
            return default

        if self.dict_cursor:
            return get_decimal(result.popitem()[1], default)
        else:
            return get_decimal(result[0], default)

    def query_for_int(self, query, args=None, default=0):
        result = self.execute_fetchone(query, args)
        if not result:
            return default

        if self.dict_cursor:
            return get_int(result.popitem()[1], default)
        else:
            return get_int(result[0], default)

    def query_for_dict(self, query, args=None):
        result = self.execute_fetchone(query, args)
        if not result:
            return {}

        if self.dict_cursor:
            return result
        else:
            return {self.cursor.description[i][0]: result[i] for i in xrange(len(result))}

    def query_for_str(self, query, args=None):
        result = self.execute_fetchone(query, args)
        if not result:
            return ''

        if self.dict_cursor:
            return get_string(result.popitem()[1])
        else:
            return get_string(result[0])

    def query_for_list(self, query, args=None):
        try:
            self.execute(query, args)
            for row in self.cursor:
                yield row
        except Exception as e:
            error('query_for_list$$sql:%s$$args:%s$$error:%s', query, sequence_to_string(args), get_string(e))

    # =============新接口============
    def new_execute(self, query, args, kwargs):
        try:
            return self.cursor.execute(query, args or kwargs)
        except OperationalError:
            error("Error connecting to MySQL")
            warn('Error to execute sql:%s', query)
            self.close()
            raise

    def new_query(self, query, *args, **kwargs):
        # try:
        self.new_execute(query, args, kwargs)
        column_names = [d[0] for d in self.cursor.description]
        if self.dict_cursor:
            result = [row for row in self.cursor]
        else:
            result = [Row(itertools.izip(column_names, row)) for row in self.cursor]
        return result
        # finally:
        # cursor.close()

    def new_get(self, query, *args, **kwargs):
        rows = self.new_query(query, *args, **kwargs)
        if not rows:
            return None
        elif len(rows) > 1:
            raise Exception("Multiple rows returned for Database.get() query")
        else:
            return rows[0]

    def new_execute_lastrowid(self, query, *args, **kwargs):
        self.new_execute(query, args, kwargs)
        return self.cursor.lastrowid

    def new_execute_rowcount(self, query, *args, **kwargs):
        self.new_execute(query, args, kwargs)
        return self.cursor.rowcount

    def db_get_by_sql(self, sql, *args, **kwargs):
        result = self.new_get(sql, *args, **kwargs)
        return load_json_util(result) if result else {}

    def db_get_count_by_sql(self, sql, *args, **kwargs):
        result = self.db_get_by_sql(sql, *args, **kwargs)
        return get_int(result.get('count', 0)) if result else 0

    def db_find_list_by_sql(self, sql, *args, **kwargs):
        result = self.new_query(sql, *args, **kwargs)
        return load_json_array_util(result) if result else []

    def db_execute_sql_and_get_row_count(self, query, *args, **kwargs):
        row_count = 0
        try:
            row_count = self.new_execute_rowcount(query, *args, **kwargs)
            self.commit()
        except Exception, e:
            row_count = 0
            self.rollback()
            warn('execute sql exception>>>sql:%s\n%s', query, str(e))
        finally:
            return row_count

    def db_execute_sql_and_get_row_id(self, sql, *args, **kwargs):
        row_id = 0
        try:
            row_id = self.new_execute_lastrowid(sql, *args, **kwargs)
            self.commit()
        except Exception, e:
            row_id = 0
            self.rollback()
            warn('execute sql exception>>>sql:%s\n%s', sql, str(e))
        finally:
            return row_id


def update(query, args=None):
    with db_conn_guard() as conn:
        result = conn.update(query, args)
        if result:
            conn.commit()
    return result


def update_many(query, args=None):
    with db_conn_guard() as conn:
        result = conn.update_many(query, args)
        if result:
            conn.commit()
    return result


def insert_many(query, args=None):
    with db_conn_guard() as conn:
        result = conn.insert_many(query, args)
        if result:
            conn.commit()
    return result


def query_for_one(sql, args=None):
    with db_conn_guard() as conn:
        result = conn.execute_fetchone(sql, args)
    return result


def query_for_all(sql, args=None):
    with db_conn_guard() as conn:
        result = conn.execute_fetchall(sql, args)
    return result


def query_for_int(sql, args=None, default=0):
    with db_conn_guard() as conn:
        result = conn.execute_fetchone(sql, args)
        if not (result and isinstance(result, tuple) and len(result)):
            result = [default]
    return get_int(result[0], default)


def query_for_str(sql, args=None, default=''):
    with db_conn_guard() as conn:
        result = conn.execute_fetchone(sql, args)
        if not (result and isinstance(result, tuple) and len(result)):
            result = [default]
    return get_string(result[0], default)


def query_for_decimal(sql, args=None, default=Decimal(0)):
    with db_conn_guard() as conn:
        result = conn.execute_fetchone(sql, args)
        if not (result and isinstance(result, tuple) and len(result)):
            result = [default]
    return get_decimal(result[0])


def query_for_dict(sql, args=None):
    with db_conn_guard(dict_cursor=True) as conn:
        result = conn.execute_fetchone(sql, args)
    return result


def query_for_list(sql, args=None):
    with db_conn_guard(dict_cursor=True) as conn:
        result = conn.execute_fetchall(sql, args)
    return result


def get_data_base_time(conn=None):
    sql = 'SELECT DATE_FORMAT(NOW(),"%Y%m%d%H%i%s");'
    ret = conn.query_for_str(sql) if conn else query_for_str(sql)
    return ret


if __name__ == '__main__':
    pass
