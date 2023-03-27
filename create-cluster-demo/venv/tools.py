##!/usr/bin/python3
# -*- coding: utf-8 -*-
import json
import os
import tarfile
import zipfile
from time import sleep
from _log import tools_log

from parse_modinfo import parse_modinfo
from sql_task import QueryMondInfo
from steamapi import download_modinfo, get_mod_detail

"""
mod 自带的版本格式不规范，甚至部分在 steam 没有 version 标签，v1 v2 都是，就不能把 mod 工具做好一点么。用上次更新时间判断有无更新
关于 mod 版本的部分规则，可以看 “获取 mod 设置” 文件

v1：老版本mod，2021.3.12 以前  数量 8885 + 84  -22.02.05-  可以用 steamwebapi 直接获取文件地址  说不定诈尸更新，所以还是要检测更新
v2：新版本mod，2021.3.12 以后  数量 3566 + 226 -22.02.05-  可以用 steam 库获取清单及所需文件，或直接用 steamcmd 下载 mod
最后更新日期在 1615490000 以前的都是 v1，以后的都是 v2
"""


class QueryResult:
    UNKNOWN = 0
    OK = 1
    EMPTY = 2
    NOTEXIST = 3
    PRIVACY = 4
    BUSY = 5
    WRONGID = 6
    DATABASE = 7
    NOTDST = 8
    DOWNERR = 9


def createcluster(data, name):
    def save_data(file_data_, file_name_):
        with open(file_name_, 'w+', encoding='utf-8') as f:
            f.write(file_data_)

    cwd_init = os.getcwd()
    os.chdir('../')
    if not os.path.exists('clusters'):
        os.mkdir('clusters')
    try:
        os.chdir('clusters')
        if not os.path.exists(name):
            os.mkdir(name)
        os.chdir(name)
        cwd_dirname = os.getcwd()
        if not os.path.exists('MyDediServer'):
            os.mkdir('MyDediServer')
        os.chdir('MyDediServer')

        data_tmp_list = {'admin': 'adminlist.txt', 'black': 'blocklist.txt', 'white': 'whitelist.txt',
                         'token': 'cluster_token.txt', 'cluster': 'cluster.ini'}
        data_tmp = {j: data.pop(i) for i, j in data_tmp_list.items() if i in data}
        for file_name, file_data in data_tmp.items():
            save_data(file_data, file_name)

        cwd_cluster_name = os.getcwd()
        world_tmp_list = {'world': 'worldgenoverride.lua', 'server': 'server.ini', 'mod': 'modoverrides.lua'}
        for dir_name, world_data in data.items():
            if not os.path.exists(dir_name):
                os.mkdir(dir_name)
            os.chdir(dir_name)
            for item_name, file_data in world_data.items():
                save_data(file_data, world_tmp_list[item_name])
            os.chdir(cwd_cluster_name)

        os.chdir(cwd_dirname)
        with tarfile.open('MyDediServer.tar', 'w|gz') as tar:
            tar.add('MyDediServer')
        with zipfile.ZipFile('MyDediServer.zip', 'w') as myzip:
            myzip.write('MyDediServer')
            for rt, dirs, files in os.walk('MyDediServer'):
                for i in dirs:
                    myzip.write(os.path.join(rt, i))
                for i in files:
                    myzip.write(os.path.join(rt, i))
        return True
    except Exception as e:
        tools_log.error(e, exc_info=True)
        return False
    finally:
        os.chdir(cwd_init)


def query_modinfo(modid: int):
    # 逻辑看思维导图
    def return_info(modinfo_tmp):
        if modinfo_tmp == '{}':
            tools_log.info('%s modinfo 数据为空', modid)
            return QueryResult.EMPTY, modinfo_tmp
        tools_log.info('%s modinfo 状态正常', modid)
        return QueryResult.OK, modinfo_tmp

    def update_data(type_, data_, update_time_=None, mod_type_=None):
        # 1: 处理run, 2: 1 + 更新检查时间, 3: 2 + 更新 modinfo, 4: 1 + 新增 modinfo
        nonlocal mod
        if type_ == 4:
            tools_log.debug('%s 将该 mod 的 modinfo 等相关信息添加到数据库', modid)
            mod.add_info(update_time=update_time_, mod_type=mod_type_, mod_info=data_)
        if type_ == 3:
            tools_log.debug('%s 更新数据库中该 mod 的 modinfo 等相关信息', modid)
            mod.up_info(update_time=update_time_, mod_type=mod_type_, mod_info=data_)
        if type_ == 2:
            tools_log.debug('%s 更新数据库中该 mod 的检查时间', modid)
            mod.up_info()
        if not mod.end_run(data_):
            tools_log.debug('%s 准备在任务队列中移除该任务', modid)
            mod.end_run(data_)

    tools_log.info('开始获取 mod %s 的 modinfo', modid)
    if not isinstance(modid, int):
        modid = int(modid)
    if not 99999999 < modid <= 9999999999:
        tools_log.info('%s modid 错误', modid)
        return QueryResult.WRONGID, '"modid 错误"'

    mod = QueryMondInfo(modid)
    tools_log.debug('%s 创建数据库连接', modid)

    if mod.is_run:
        tools_log.debug('%s 正在被其他任务查询，等待处理结果', modid)
        mod.wait()
        tools_log.debug('%s 每秒尝试获取结果，持续 60s', modid)
        for countdown in range(60, -1, -1):
            code, modinfo = mod.result_run(countdown)
            if not code:
                if countdown:
                    sleep(1)
                continue
            if modinfo == '9':
                tools_log.info('%s mod 不存在', modid)
                return QueryResult.NOTEXIST, '"mod 不存在"'
            elif modinfo == '15':
                tools_log.info('%s 没有查看该 mod 的权限', modid)
                return QueryResult.PRIVACY, '"没有查看该 mod 的权限"'
            elif modinfo == '99':
                tools_log.info('%s 不是饥荒联机版 mod', modid)
                return QueryResult.NOTDST, '"不是饥荒联机版 mod"'
            elif modinfo == '0':
                tools_log.info('%s 未知错误', modid)
                return QueryResult.UNKNOWN, '"未知错误"'
            tools_log.debug('%s 获取结果成功', modid)
            return return_info(modinfo)
        else:
            tools_log.info('%s 60s 都没有获取成功，不再重试', modid)
            return QueryResult.UNKNOWN, '"未知错误"'

    try:
        if mod.run_filled:
            tools_log.debug('%s 任务队列已满', modid)
            if mod.recorded and not mod.need_check:
                code, modinfo = mod.result_info()
                if code:
                    tools_log.debug('%s 数据库中有该 mod 信息，且不需要检测更新，返回 modinfo', modid)
                    return return_info(modinfo)
                tools_log.info('%s 任务队列已满，拒绝处理任务，返回服务器繁忙', modid)
                return QueryResult.BUSY, '"服务器繁忙"'

        tools_log.debug('%s 将 mod 添加到任务队列', modid)
        mod.add_run()

        recorded = mod.recorded
        if recorded:
            tools_log.debug('%s mod 在数据库中有记录', modid)
            if not mod.need_check:
                tools_log.debug('%s mod 刚刚更新过信息，不需要再次查询', modid)
                code, modinfo = mod.result_info()
                if not code:
                    tools_log.info('%s 从数据库获取 modinfo 失败', modid)
                    update_data(1, '0')
                    return QueryResult.DATABASE, '"请求 modinfo 失败了"'
                tools_log.debug('%s 从数据库获取 modinfo 成功', modid)
                update_data(1, modinfo)
                return return_info(modinfo)

        tools_log.debug('%s mod 在数据库中没有记录', modid)
        tools_log.debug('%s 查询 mod 的详情，根据详情获取 mod 最后更新时间等', modid)
        code, detail = get_mod_detail(modid)
        if code != 1:
            tools_log.info('%s 详情状态码不对：%s', modid, code)
            if code == 9:
                if recorded:
                    mod.del_info()
                update_data(1, '9')
                return QueryResult.NOTEXIST, '"mod 不存在"'
            elif code == 15:
                # if recorded:
                #     mod.del_info()
                update_data(1, '15')
                return QueryResult.PRIVACY, '"没有查看该 mod 的权限"'
            elif code == 0:
                update_data(1, '0')
                return QueryResult.DOWNERR, '"获取 mod 信息失败"'
            else:
                tools_log.warning('%s 来自 webapi 的未知类型：%s', modid, code)
                update_data(1, '0')
                return QueryResult.UNKNOWN, '"未知错误"'

        if recorded and detail.get('last_time') == mod.update_time:
            tools_log.debug('%s 最后更新与数据库记录的相同，mod 没有更新，从数据库获取 modinfo', modid)
            code_, modinfo_ = mod.result_info()
            if not code_:
                tools_log.info('%s 从数据库获取 modinfo 失败', modid)
                update_data(1, '0')
                return QueryResult.DATABASE, '"请求 modinfo 失败了"'
            tools_log.debug('%s 从数据库获取 modinfo 成功', modid)
            update_data(2, modinfo_)
            return return_info(modinfo_)

        # creator_appid == 245850
        # consumer_appid == 322330      dst
        # consumer_appid == 245850      ds
        # creator_appid == 766
        # consumer_appid == 322330      dst mod collect
        # consumer_appid == 245850      ds mod collect
        creator_appid, consumer_appid = detail.get('creator_appid'), detail.get('consumer_appid')
        if not (creator_appid == 245850 and consumer_appid == 322330):
            tools_log.info('%s 不是饥荒联机版 mod', modid)
            if recorded:
                mod.del_info()
            update_data(1, '99')
            return QueryResult.NOTDST, '"不是饥荒联机版 mod"'

        tools_log.debug('%s 判断 mod 类型，下载 mod 的 modinfo 文件', modid)
        if detail.get('file_url'):
            modtype = 1  # v1
            code_, modinfo_raw_ = download_modinfo(detail.get('file_url'))
        else:
            modtype = 2  # v2
            code_, modinfo_raw_ = download_modinfo(mod.modid)

        if code_ == 0:
            tools_log.info('%s 下载 modinfo 文件失败', modid)
            update_data(1, '0')
            return QueryResult.DOWNERR, '"获取 mod 设置失败"'
        elif code == 2:
            tools_log.debug('%s modinfo 文件内容为空', modid)
            modinfo_ = '{}'
            if recorded:
                update_data(3, modinfo_, detail.get('last_time'), modtype)
            else:
                update_data(4, modinfo_, detail.get('last_time'), modtype)
            return return_info(modinfo_)

        tools_log.debug('%s 解析 modinfo 文件', modid)
        code2_, modinfo_dict = parse_modinfo(modinfo_raw_)
        # code2_ 1 代表成功，0 代表失败，会返回{}，一般来说是 mod 作者的问题。
        # 区分的意义在于有的 modinfo 是空的，也会返回{}，这里应该没必要区分。
        modinfo_ = json.dumps(modinfo_dict, ensure_ascii=False)
        if recorded:
            update_data(3, modinfo_, detail.get('last_time'), modtype)
        else:
            update_data(4, modinfo_, detail.get('last_time'), modtype)

        tools_log.debug('%s 解析处理完成，返回结果', modid)
        return return_info(modinfo_)
    except Exception as e:
        update_data(1, '0')
        tools_log.warning(e, exc_info=True)
    finally:
        mod.disconnect()


if __name__ == '__main__':
    # ddd = {
    #     'cluster': 'cluster_description',
    #     'admin': 'test1test2',
    #     'black': 'test1test2',
    #     'white': 'test1test2',
    #     'token': 'test1test2',
    #     'Master': {'world': '1234', 'server': '4321', 'mod': '1423'},
    #     'Caves': {'world': '1234', 'server': '4321', 'mod': '1423'},
    # }
    # createcluster(ddd, '2wqesd3253tre')

    print([query_modinfo(2263870666)[1]])
