##!/usr/bin/python3
# -*- coding: utf-8 -*-
import os
import threading
import zipfile
from functools import wraps
from io import BytesIO
from json import loads
from shutil import rmtree
from time import sleep, time
from urllib.parse import urlencode
from urllib.request import Request, urlopen

import gevent
import steam.client
import steam.client.cdn
import steam.core.cm
import steam.webapi
from steam.exceptions import SteamError

from _log import steamapi_log
'''
webapi              https => http
cdn      348'          if => if self.offset <= chunk_start or end_offset >= chunk_end:
cm       101'     retry=0 => 3
         475'   cell_id=0 => 159
web       16'   session.headers['Connection'] = 'close'
'''
start = time()
# from gevent import monkey
# gevent.monkey.patch_all()


def searchmod(text_='', page=1, num=10):  # num <= 100  page0 == page1
    steamapi_log.info('通过 steamapi 根据关键词 %s 搜索 mod 的第 %s 页', text_, page)
    url_base = 'http://api.steampowered.com/IPublishedFileService/QueryFiles/v1/'
    # url_base = 'https://api.steampowered.com/IPublishedFileService/QueryFiles/v1/'
    data = {
        'page': page,
        'key': key,  # steam apikey  https://steamcommunity.com/dev/apikey
        'appid': 322330,  # 游戏id
        'language': 6,  # 0英文，6简中，7繁中
        'return_tags': True,  # 返回mod详情中的标签
        'numperpage': num,  # 每页结果
        'search_text': text_,  # 标题或描述中匹配的文字
        'return_vote_data': True,
        'return_children': True
    }

    url = url_base + '?' + urlencode(data)
    for _ in range(2):
        try:
            req = Request(url=url)
            response = urlopen(req, timeout=10)
            mod_data = response.read().decode('utf-8')
            # print(mod_data)
            response.close()
            break
        except Exception as e:
            steamapi_log.warning(e)
    else:
        return

    mod_data = loads(mod_data).get('response')

    mod_num = mod_data.get('total')
    mod_info_full = mod_data.get('publishedfiledetails')

    mod_list = []
    if mod_info_full:
        for mod_info_raw in mod_info_full:
            img = mod_info_raw.get('preview_url', '')
            vote_data = mod_info_raw.get('vote_data', {})
            mod_info = {
                'id': mod_info_raw.get('publishedfileid', ''),
                'name': mod_info_raw.get('title', ''),
                'auth': mod_info_raw.get("creator", 0),
                # 'auth': f'https://steamcommunity.com/profiles/{auth}/?xml=1' if auth else '',
                # 'desc': mod_info_raw.get('file_description'),
                'time': int(mod_info_raw.get('time_updated', 0)),
                'sub': int(mod_info_raw.get('subscriptions', '0')),
                'img': img if 'steamuserimages' in img else '',
                # 'v': [*[i.get('tag')[8:] for i in mod_info_raw.get('tags', '') if i.get('tag', '').startswith('version:')], ''][0],
                'vote': {'star': int(vote_data.get('score') * 5) + 1 if vote_data.get('votes_up') + vote_data.get('votes_down') >= 25 else 0,
                         'num': vote_data.get('votes_up') + vote_data.get('votes_down')}
            }
            if mod_info_raw.get("num_children"):
                mod_info['child'] = list(map(lambda x: x.get('publishedfileid'), mod_info_raw.get("children")))

            mod_list.append(mod_info)

    return {'num': mod_num, 'mod': mod_list}


# 采用多线程的方式规避不可控的网络问题。这样也许好一些？可惜写的差不多了不想再改了
def call_steam_arg(thr_num=3, timeout=30):
    def call_steam(func):
        @wraps(func)
        def wrap():
            def task_get(result_list_, stop_):
                anonymous = steam.client.SteamClient()
                try:
                    if stop_.is_set():
                        return
                    anonymous.anonymous_login()

                    if stop_.is_set():
                        return
                    steamcdn = steam.client.cdn.CDNClient(anonymous)

                    if stop_.is_set():
                        return
                    code, result_ = func(stop=stop_, steamcdn=steamcdn)

                    if stop_.is_set():
                        return
                    result_list_.append((code, result_))
                    if code == 1:
                        stop_.set()

                except gevent.timeout.Timeout:
                    steamapi_log.debug('请求等待超时')
                except Exception as e:
                    steamapi_log.debug(e, exc_info=True)
                finally:
                    anonymous.logout()
                    exit()

            stop_time = time() + timeout
            result = 0, ''
            result_list = []
            stop = threading.Event()

            # 在一秒内创建指定数量的子线程，执行传入的函数
            for i in range(thr_num):
                result_list.append([])
                # 部署时设为守护线程，测试时设为非守护线程
                # threading.Thread(target=task_get, args=(result_list[i], stop), daemon=True).start()
                threading.Thread(target=task_get, args=(result_list[i], stop)).start()
                sleep(1 / thr_num)

            # 每秒检查一次是否完成，如果有 成功完成的信号 或 任务都已完成 或 超时，退出
            while True:
                remain_time = stop_time - time()
                if remain_time <= 0:
                    break
                wait_time = 5 if remain_time > 5 else remain_time
                stop.wait(wait_time)
                if stop.is_set():
                    break
                if all(result_list):
                    stop.set()
                    break

            print(result_list)
            # 根据返回值的状态码，以从小到大的顺序赋值给结果，遇到正确状态码直接退出
            for result_valid in sorted(filter(lambda x: x, result_list), key=lambda x: x[0][0]):
                result = result_valid[0]
                if result[0] == 1:
                    break

            return result

        return wrap

    return call_steam


@call_steam_arg()
def get_dst_version2(stop: threading.Event = None, steamcdn=None):
    # 0:下载失败, 1:下载成功, 2:下载成功但内容为空, 3:其他线程已经完成了任务
    # steamapi_log.debug('开始检查饥荒游戏版本')
    for _ in range(3):
        try:
            if stop and stop.is_set():
                return 3, ''
            version = [*steamcdn.iter_files(343050, 'version.txt', filter_func=lambda x, y: x == 343052)]
            if not version:
                return 2, ''
            return 1, version[0].read().decode('utf-8').strip()
        except Exception as e:
            steamapi_log.warning(e, exc_info=True)
    return 0, ''


def login(func):
    """登录与退出"""

    # 0: 登陆失败, other: 登录成功
    @wraps(func)
    def warp(*args, **kwargs):
        for _ in range(2):
            try:
                anonymous = steam.client.SteamClient()
                anonymous.anonymous_login()
                # steamcdn = t.get_product_info([343050])
                steamcdn = steam.client.cdn.CDNClient(anonymous)
                break
            except gevent.timeout.Timeout:
                steamapi_log.warning('超时了')
            except Exception as e:
                steamapi_log.warning(e, exc_info=True)
                pass
        else:
            return 0, ''
        result = func(steamcdn=steamcdn, *args, **kwargs)

        anonymous.logout()
        return result

    return warp


@login
def get_dst_version(steamcdn=None):
    # 0 下载失败， 1 下载成功， 2 内容为空
    for _ in range(3):
        try:
            # b = next(steamcdn.get_manifests(343050, filter_func=lambda x, y: x == 343052))
            # version = next(b.iter_files('version.txt')).read().decode('utf-8').strip()
            version = [*steamcdn.iter_files(343050, 'version.txt', filter_func=lambda x, y: x == 343052)]
            if not version:
                return 2, ''
            version = version[0].read().decode('utf-8').strip()
            # print(version)
            return 1, version
        except SteamError as e:
            steamapi_log.warning(e, exc_info=True)
    return 0, ''


@login
def download_dst_scripts(steamcdn=None):
    steamapi_log.info('开始下载世界设置所需饥荒文件')
    # 0:失败, 1:下载成功, 2:没有全部下载成功
    if not os.path.exists('data'):
        os.mkdir('data')
    if not os.path.exists('data/databundles'):
        os.mkdir('data/databundles')
    if not os.path.exists('data/images'):
        os.mkdir('data/images')
    code = 0
    status = {'scripts': False, 'set_tex': False, 'set_xml': False, 'gen_tex': False, 'gen_xml': False, 'ver': False}
    for i in range(5):
        try:
            # b = next(steamcdn.get_manifests(343050, filter_func=lambda x, y: x == 343052))
            # version = next(b.iter_files('version.txt')).read().decode('utf-8').strip()
            for file in steamcdn.iter_files(343050, filter_func=lambda x, y: x == 343052):
                if 'scripts.zip' in file.filename and not status['scripts']:
                    scripts_con = file.read()
                    with open('data/databundles/scripts.zip', 'wb') as f:
                        f.write(scripts_con)
                    with zipfile.ZipFile('data/databundles/scripts.zip') as file_zip:
                        if os.path.exists('data/databundles/scripts'):
                            rmtree('data/databundles/scripts')
                        file_zip.extractall('data/databundles')
                    steamapi_log.debug('获取 scripts.zip 成功')
                    status['scripts'] = True
                elif 'worldsettings_customization.tex' in file.filename and not status['set_tex']:
                    with open('data/images/worldsettings_customization.tex', 'wb') as f:
                        f.write(file.read())
                    steamapi_log.debug('获取 worldsettings_customization.tex 成功')
                    status['set_tex'] = True
                elif 'worldsettings_customization.xml' in file.filename and not status['set_xml']:
                    with open('data/images/worldsettings_customization.xml', 'wb') as f:
                        f.write(file.read())
                    steamapi_log.debug('获取 worldsettings_customization.xml 成功')
                    status['set_xml'] = True
                elif 'worldgen_customization.tex' in file.filename and not status['gen_tex']:
                    with open('data/images/worldgen_customization.tex', 'wb') as f:
                        f.write(file.read())
                    steamapi_log.debug('获取 worldgen_customization.tex 成功')
                    status['gen_tex'] = True
                elif 'worldgen_customization.xml' in file.filename and not status['gen_xml']:
                    with open('data/images/worldgen_customization.xml', 'wb') as f:
                        f.write(file.read())
                    steamapi_log.debug('获取 worldgen_customization.xml 成功')
                    status['gen_xml'] = True
                elif 'version.txt' in file.filename and not status['ver']:
                    with open('data/version.txt', 'wb') as f:
                        f.write(file.read())
                    steamapi_log.debug('获取 version.txt 成功')
                    status['ver'] = True

                code = 1 if all(status.values()) else 2
            if code == 1:
                break
        except SteamError as e:
            steamapi_log.warning(e, exc_info=True)
        except gevent.timeout.Timeout:
            steamapi_log.warning('超时了')
    return code, status


@login
def download_v2_modinfo(modid: int, steamcdn=None):
    """ 下载 v2 modinfo """
    steamapi_log.info('开始下载 v2 mod %s 的 modinfo.lua 文件', modid)
    # 0: 失败, 1: 正常, 2: 没有指定文件, 3: v1 mod 或 大小为 0, 4: mod 不存在或权限限制, 5: 未知错误
    status, modinfo = 0, {'modinfo': b'', 'modinfo_chs': b''}
    for _ in range(3):
        try:
            mod_item = steamcdn.get_manifest_for_workshop_item(modid)
            # for i in mod_item.payload.mappings:
            #     print(steam.client.cdn.CDNDepotFile(mod_item, i))
            modinfo_names = ['modinfo.lua', 'modinfo_chs.lua']
            # ['modinfo.lua', 'modinfo_chs.lua', 'modinfo_cht.lua']
            modinfo_list = list(filter(lambda x: x.filename in modinfo_names, mod_item.iter_files()))

            if not modinfo:
                steamapi_log.warning('%s 未在文件中找到 modinfo', modid)
                status = 2
                break

            steamapi_log.debug('%s 成功获取 modinfo', modid)
            for info in modinfo_list:
                modinfo[info.filename[:-4]] = info.read()
            status = 1
            break
        except SteamError as e:
            if '404' in e.__str__():
                steamapi_log.warning('%s mod 为 v1 mod 或 大小为 0', modid)
                status = 3
                break
            elif 'Failed getting workshop file info' in e.__str__():
                steamapi_log.warning('%s mod 不存在或没有查看权限', modid)
                status = 4
                break
            else:
                status = 5
                steamapi_log.warning('%s 未知错误', modid)
                steamapi_log.warning(e, exc_info=True)
        except Exception as e:
            steamapi_log.warning(e, exc_info=True)
            status = 5
    return status, modinfo


def download_v1_modinfo(file_url: str):
    """ 下载 v1 modinfo """
    steamapi_log.info('开始下载 v1 mod，并提取 modinfo.lua 文件')
    # 0: 下载失败, 1: 下载成功, 2: mod 中没有 modinfo.lua 文件
    status, modinfo = 0, {'modinfo': b'', 'modinfo_chs': b''}
    tmp = BytesIO()
    for i in range(3):
        try:
            req = Request(url=file_url)
            res = urlopen(req, timeout=10)
            tmp.write(res.read())
            res.close()
            break
        except Exception as e:
            steamapi_log.warning('%s 下载失败', file_url)
            steamapi_log.warning(e, exc_info=True)
            tmp.close()
    else:
        steamapi_log.warning('%s 下载失败 3 次，不再尝试', file_url)
        return status, modinfo
    steamapi_log.debug('%s 下载成功，开始解压', file_url)
    with zipfile.ZipFile(tmp) as file_zip:
        namelist = file_zip.namelist()
        if 'modinfo.lua' in namelist:
            steamapi_log.debug('%s 开始解压 modinfo.lua', file_url)
            modinfo['modinfo'] = file_zip.read('modinfo.lua')
        if 'modinfo_chs.lua' in namelist:
            steamapi_log.debug('%s 开始解压 modinfo_chs.lua', file_url)
            modinfo['modinfo_chs'] = file_zip.read('modinfo_chs.lua')
        # if 'modinfo_cht.lua' in namelist:
        #     modinfo['modinfo_cht'] = file_zip.read('modinfo_cht.lua')
    tmp.close()
    status = 1 if modinfo.get('modinfo.lua') else 2
    return status, modinfo


def download_modinfo(modid_or_fileurl: str or int):
    # 0: 请求失败, 1: 下载成功, 2: 请求成功但是 mod 没有 modinfo 文件, 3: 请求成功但是未找到 mod
    steamapi_log.info('开始下载 %s', modid_or_fileurl)
    if isinstance(modid_or_fileurl, str) and not modid_or_fileurl.isdecimal():
        steamapi_log.debug('v1 mod')
        return download_v1_modinfo(modid_or_fileurl)

    steamapi_log.debug('v2 mod')
    status, modinfo = download_v2_modinfo(int(modid_or_fileurl))

    if status in [0, 5]:
        return 0, modinfo
    elif status in [1]:
        return 1, modinfo
    elif status in [2, 3]:
        return 2, modinfo
    else:
        return 3, modinfo


def get_mod_detail(modid):
    """获取绝大多数 mod 的详情"""
    steamapi_log.info('获取 mod %s 的详情', modid)

    # 失败次数过多就换 http
    url = 'http://api.steampowered.com/IPublishedFileService/GetDetails/v1/'
    # url = 'https://api.steampowered.com/IPublishedFileService/GetDetails/v1/'
    data = {
        'key': key,  # steam apikey  https://steamcommunity.com/dev/apikey
        'language': 6,  # 0英文，6简中，7繁中
        'publishedfileids[0]': str(modid),  # 要查询的发布文件的ID
    }

    url = url + '?' + urlencode(data)
    for i in range(3):
        try:
            req = Request(url=url)
            res = urlopen(req, timeout=10)
            response = res.read().decode('utf-8')
            res.close()
            break
        except Exception as e:
            steamapi_log.warning('%s 获取失败', modid)
            steamapi_log.warning(e, exc_info=True)
    else:
        steamapi_log.warning('%s 获取失败 3 次，不再尝试', modid)
        return 0, {}

    steamapi_log.debug('%s 详情获取成功', modid)
    data = loads(response).get('response').get('publishedfiledetails')[0]
    if data.get('result') != 1:
        steamapi_log.debug('%s 状态码有误：%s', modid, data.get('result'))
        return data.get('result'), {}

    img = data.get('preview_url', '')
    auth = data.get("creator")
    mod_info = {
        'id': data.get('publishedfileid'),
        'name': data.get('title'),
        'last_time': data.get('time_updated'),
        'auth': f'https://steamcommunity.com/profiles/{auth}/?xml=1' if auth else '',
        'file_url': data.get('file_url'),
        'img': f'{img}?imw=64&imh=64&ima=fit&impolicy=Letterbox&imcolor=%23000000&letterbox=true'
        if 'steamuserimages' in img else '',
        'v': [*[i.get('tag')[8:] for i in data.get('tags', '') if i.get('tag', '').startswith('version:')], ''][0],
        'creator_appid': data.get('creator_appid'),
        'consumer_appid': data.get('consumer_appid'),
    }
    # print(mod_info)
    return data.get('result'), mod_info


# import gc
# import objgraph
# class Dst(object):
#     _instance_lock = threading.Lock()
#
#     def __new__(cls, *args, **kwargs):
#         if not hasattr(Dst, "_instance"):
#             with Dst._instance_lock:
#                 if not hasattr(Dst, "_instance"):
#                     Dst._instance = object.__new__(cls)
#         return Dst._instance
#
#     def __init__(self):
#         if not hasattr(Dst, "_inited"):
#             with Dst._instance_lock:
#                 if not hasattr(Dst, "_inited"):
#                     steamapi_log.debug('Dst 开始初始化')
#                     Dst._inited = True
#                     self.old_version = ''
#                     self.version = ''
#                     self.read_saved()
#                     # 如果不设为守护线程，需要 sleep 一下，防止主线程直接结束，子线程报错
#                     # threading.Thread(target=self.check_version, daemon=True).start()
#                     threading.Thread(target=self.check_version).start()
#                     sleep(0.1)
#
#     def read_saved(self):
#         steamapi_log.debug('从文件初始化 old_version')
#         if os.path.exists('dst_version.txt'):
#             with open('dst_version.txt', 'r', encoding='utf-8') as f:
#                 self.old_version = f.read()
#
#     def save(self):
#         steamapi_log.debug('将新的 version 保存到文件中')
#         with open('dst_version.txt', 'w', encoding='utf-8') as f:
#             f.write(self.version)
#
#     def check_version(self):
#         # steamapi_log.debug('开始任务 获取饥荒 version')
#
#         # gc.collect()
#         # objgraph.show_growth()
#         # print('-------------------------------------------------------------')
#         # interval = 60
#         interval = 600
#         try:
#             code, version = get_dst_version2()
#             if code != 1:
#                 interval = 60
#                 steamapi_log.warning('获取 dst 版本出错，状态码：%s，%ss 后再来一次', code, interval)
#                 return
#             self.version = version
#             if self.version != self.old_version:
#                 # TODO 需要更新饥荒文件了
#                 self.old_version = self.version
#                 self.save()
#             steamapi_log.info('获取 dst 版本成功：%s，%ss 后再来一次', version, interval)
#         except Exception as e:
#             interval = 60
#             steamapi_log.warning('获取 dst 版本出错，%ss 后再来一次', interval)
#             steamapi_log.warning(e, exc_info=True)
#         finally:
#             threading.Timer(interval, self.check_version, ()).start()


with open('steamapikey.txt', 'r', encoding='utf-8') as key_value:
    key = key_value.read()
    steamapi_log.debug('从文件读取 steamapikey 成功')

if __name__ == '__main__':
    # print(get_dst_version())
    # print(download_dst_scripts())

    # url = 'https://steamusercontent-a.akamaihd.net/ugc/' \
    #       '1466437966115152320/8A3E11F0B32FCBFBF308DEB0B5C98A702215374B/'
    # download_v1_modinfo(url)
    # download_v2_modinfo(2720074492)
    # print(download_modinfo(2720074492))
    # get_mod_detail(360122003)

    # print(searchmod('神话', num=5))
    # print(get_dst_version2())

    # print(time() - start)

    # print(s)
    # print(type(dst.version))
    # print(get_mod_detail(2753581100))
    Dst()
