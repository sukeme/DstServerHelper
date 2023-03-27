##!/usr/bin/python3
# -*- coding: utf-8 -*-
from functools import wraps
from time import time

import mysql.connector

from _log import sql_log

config = {
    # 'host': '42.193.112.82',
    'host': 'localhost',
    'port': 33306,
    'user': 'dst',
    'passwd': 'Tem5Gk77RfzF2A6n',
    'db': 'dst',
    'charset': 'utf8mb4'
}


class QueryMondInfo:

    def __init__(self, modid: int, **new_config):
        config.update(new_config)
        self.db = mysql.connector.connect(**config)
        # self.db = MySQLdb.connect(**config)
        self.modid = modid
        self.max_run = 32
        self.modinfo = None  # ('update_time', 'check_time',  'mod_type')
        self.timeout = {1: 6000, 2: 600}

    def disconnect(self):
        self.db.close()

    @property
    def now(self):
        return int(time())

    # 发送 sql 语句
    while True:
        # noinspection PyMethodParameters
        def send_cmd(func):
            # noinspection PyTypeChecker
            @wraps(func)
            def wrap(self, *args, **kwargs):
                cur = self.db.cursor()
                try:
                    # noinspection PyCallingNonCallable
                    cmd = func(self, *args, **kwargs)
                    if isinstance(cmd, str):
                        cur.execute(cmd)
                    elif isinstance(cmd[1], tuple):
                        cur.execute(*cmd)
                    else:
                        cur.executemany(*cmd)
                    result = 1, cur.fetchall()
                    cur.close()
                    self.db.commit()
                except Exception as e:
                    result = 0, e.__str__()
                    self.db.rollback()
                    sql_log.error(e, exc_info=True)
                return result

            return wrap

        # noinspection PyArgumentList
        @send_cmd
        def add_data(self, table_name: str, data: dict, *other):
            """
            modinfo: mod_id, update_time, check_time, mod_type, mod_info
            running: mod_id, start_time, end_time*, waitting*, mod_info*
            """
            sql_log.debug('在表 %s 中插入 mod_id 为 %s 的数据', table_name, data.get('mod_id'))
            cmd = f'INSERT INTO {table_name} ({", ".join(data.keys())}) VALUES ({"%s, " * (len(data) - 1)}%s)'
            args = tuple(data.values())
            if other:
                args = [args, *(tuple(oth.values()) for oth in other)]
                return cmd, args
            return cmd, args

        # noinspection PyArgumentList
        @send_cmd
        def update_data(self, table_name: str, data: dict):
            """
            modinfo: mod_id, update_time, check_time, mod_type, mod_info
            running: mod_id, start_time, end_time*, waitting*, mod_info*
            """
            modid = data.pop('mod_id')
            sql_log.debug('更新表 %s 中 mod_id 为 %s 的数据', table_name, modid)
            cmd = f'UPDATE {table_name} SET {", ".join([f"{i} = %s" for i in data])} WHERE mod_id = {modid}'
            args = tuple(data.values())
            return cmd, args

        # noinspection PyArgumentList
        @send_cmd
        def del_data(self, table_name: str, mod_id: str or int):
            sql_log.debug('删除表 %s 中 mod_id 为 %s 的数据', table_name, mod_id)
            return f'DELETE FROM {table_name} WHERE mod_id = %s', (mod_id,)

        # noinspection PyArgumentList
        @send_cmd
        def query_data(self, table_name: str, condition: dict, data: tuple = ()):
            """ 表名 筛选条件 返回的列 """
            sql_log.debug('查询表 %s 中符合查询条件 %s 的数据：%s', table_name, ", ".join(data), ', '.join(data))
            cmd = f'SELECT {"*" if not data else ", ".join(data)} FROM {table_name} WHERE' + \
                  ' AND'.join([f' {i} = %s' for i in condition])
            args = tuple(condition.values())
            return cmd, args

        # noinspection PyArgumentList
        @send_cmd
        def row_count(self, table_name):
            sql_log.debug('查询表 %s 的行数', table_name)
            return f'SELECT COUNT(*) FROM {table_name}', ()

        break

    # 维护正在运行的表
    while True:
        @property
        def is_run(self):
            """mod 是否正在处理"""
            code, data = self.query_data('running', {'mod_id': self.modid}, ('mod_id',))
            return True if code and data else False

        @property
        def run_num(self):
            """当前正在处理的任务数量"""
            code, data = self.row_count('running')
            return data[0][0] if code else 0

        @property
        def run_end(self):
            """mod 是否处理完成"""
            code, data = self.query_data('running', {'mod_id': self.modid}, ('end_time',))
            return True if data[0][0] else False

        @property
        def run_filled(self):
            """任务队列是否满了"""
            return False if self.run_num < self.max_run else True

        @property
        def wait_num(self):
            """当前正在等待任务结果的数量"""
            code, data = self.query_data('running', {'mod_id': self.modid}, ('waitting',))
            return data[0][0] if code else 0

        def del_run(self):
            """正在处理的列表中删除 mod"""
            code, data = self.del_data('running', self.modid)
            return True if code else False

        def add_run(self):
            """将 mod 添加到正在处理"""
            code, data = self.add_data('running', {'mod_id': self.modid, 'start_time': self.now, 'mod_info': '""'})
            return True if code else False

        def _ad_de(self, intent):
            cur = self.db.cursor()
            try:
                sql_log.debug('mod_id 为 %s 的数据中，waitting 值 %s 1', self.modid, intent)
                cur.execute(f'UPDATE running SET waitting = waitting {intent} 1 WHERE mod_id = {self.modid};')
                cur.close()
                self.db.commit()
                return True
            except Exception as e:
                self.db.rollback()
                sql_log.error(e, exc_info=True)
                return False

        def wait(self):
            """开始等待"""
            return self._ad_de('+')

        def leave(self):
            """不再等待"""
            return self._ad_de('-')

        def end_run(self, data):
            """更新处理结果"""
            sql_log.debug('更新 mod_id %s 的处理结果', self.modid)
            cur = self.db.cursor()
            try:
                cur.execute(f'SELECT waitting FROM running WHERE mod_id = {self.modid} FOR UPDATE;')
                wait_num = cur.fetchall()[0][0]
                if wait_num == 0:
                    sql_log.debug('mod_id %s 无任务等待，删除数据', self.modid)
                    cur.execute(f'DELETE FROM running WHERE mod_id = {self.modid};')
                else:
                    sql_log.debug('mod_id %s 有任务等待，更新数据', self.modid)
                    cur.execute(f'UPDATE running SET mod_info = %s, end_time = %s WHERE mod_id = %s;',
                                (data, self.now, self.modid))
                cur.close()
                self.db.commit()
                return True
            except Exception as e:
                sql_log.error(e, exc_info=True)
                self.db.rollback()
                return False

        def result_run(self, get_info=True):
            """(获取 mod 的处理结果)* say byebye"""
            sql_log.debug('尝试获取 mod_id %s 的处理结果', self.modid)
            cur = self.db.cursor()
            try:
                modinfo = ''
                if get_info:
                    cur.execute(f'SELECT end_time FROM running WHERE mod_id = {self.modid} FOR UPDATE;')
                    end_time = cur.fetchall()[0][0]
                    if end_time == 0:
                        sql_log.debug('mod_id %s 未处理完毕', self.modid)
                        cur.close()
                        self.db.commit()
                        return False, ''
                    sql_log.debug('mod_id %s 已处理完毕，开始获取 modinfo', self.modid)
                    cur.execute(f'SELECT mod_info FROM running WHERE mod_id = {self.modid};')
                    modinfo = cur.fetchall()[0][0]
                sql_log.debug('检查 mod_id %s 是否有任务等待', self.modid)
                cur.execute(f'SELECT waitting FROM running WHERE mod_id = {self.modid};')
                wait_num = cur.fetchall()[0][0]
                if wait_num == 1:
                    sql_log.debug('mod_id %s 无任务等待，删除', self.modid)
                    cur.execute(f'DELETE FROM running WHERE mod_id = {self.modid};')
                else:
                    sql_log.debug('mod_id %s 有任务等待，waitting 减一，退出', self.modid)
                    cur.execute(f'UPDATE running SET waitting = waitting - 1 WHERE mod_id = {self.modid};')
                cur.close()
                self.db.commit()
                return True if get_info else False, modinfo
            except Exception as e:
                self.db.rollback()
                sql_log.error(e, exc_info=True)
                return False, ''

        break

    # 维护modinfo表
    while True:
        def add_info(self, **kwargs):
            """update_time, mod_type, mod_info"""
            kwargs['mod_id'] = self.modid
            kwargs['check_time'] = self.now
            code, data = self.add_data('modinfo', kwargs)
            return True if code else False

        def del_info(self):
            code, data = self.del_data('modinfo', self.modid)
            return True if code else False

        def up_info(self, **kwargs):
            """更新 mod_info。参数：update_time, mod_type, mod_info"""
            kwargs['mod_id'] = self.modid
            kwargs['check_time'] = self.now
            code, data = self.update_data('modinfo', kwargs)
            return True if code else False

        def query_info(self):
            """获取 mod 对应信息 update_time, check_time,  mod_type"""
            code, data = self.query_data('modinfo', {'mod_id': self.modid}, ('update_time', 'check_time', 'mod_type'))
            return data[0] if code and data else ()

        def result_info(self):
            """获取 mod 的 mod_info"""
            code, data = self.query_data('modinfo', {'mod_id': self.modid}, ('mod_info',))
            if not code:
                return code, data
            return code, data[0][0]

        @property
        def recorded(self):
            """检查 mod 是否在数据库中，并更新实例中的 mod_info"""
            data = self.query_info()
            if not data:
                self.modinfo = ()
                return False
            self.modinfo = data
            return True

        @property
        def need_check(self):
            """mod 是否需要检查更新"""
            if self.modinfo is None:
                raise RuntimeError('未通过 record 初始化数据')
            if not self.modinfo:
                raise RuntimeError('数据库中没有对应信息')
            return True if self.modinfo[1] + self.timeout.get(self.modinfo[2], 86400) < time() else False

        @property
        def update_time(self):
            """mod 的上次更新时间，用于判断 mod 是否有更新"""
            if self.modinfo is None:
                raise RuntimeError('未通过 record 初始化数据')
            if not self.modinfo:
                raise RuntimeError('数据库中没有对应信息')
            return self.modinfo[0]

        break


if __name__ == '__main__':
    # 改为 json 格式，可以对键进行操作。json格式效率很低。现在数据量小，默认使用json格式
    # ALTER TABLE modinfo CHANGE mod_info mod_info MEDIUMTEXT NOT NULL;
    # ALTER TABLE modinfo CHANGE mod_info mod_info JSON NOT NULL;
    # SELECT mod_info -> '$.name' FROM modinfo WHERE 1;
    # 删除第二个字典中键为空的字段
    # """UPDATE running SET mod_info = JSON_MERGE_PATCH(mod_info, '{"icon": null, "icon_atlas": null}') WHERE 1"""
    eg = QueryMondInfo(2263870666)
    eg.modid = 0



