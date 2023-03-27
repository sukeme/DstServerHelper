##!/usr/bin/python3
# -*- coding: utf-8 -*-
import re
from functools import reduce

import chardet
import lupa

from _log import modinfo_log

info_list_full = [
    'name',  # str mod名称
    'version',  # str 版本号
    'version_compatible',  # str 兼容版本号
    'author',  # str 作者
    'description',  # str 介绍
    'api_version',  # int ds mod api为6。ds只检查此项
    'api_version_dst',  # int dst mod api为10。dst首先检查此项， 此项没有会去检查'api_version'项
    'client_only_mod',  # bool 是否为仅客户端mod
    'server_only_mod',  # bool 是否为仅服务器mod
    'all_clients_require_mod',  # bool 服务器与客户端需要共同开启的mod
    'forumthread',  # str klei论坛的对应主题帖，应该是部分链接  旧的跳转方式貌似已经废弃了，手动拼接吧
    'server_filter_tags',  # lua_table > list 添加服务器标签 {"tag0", "tag1", "tag2", }
    # 'icon_atlas',  # str 图标的xml文件
    # 'icon',  # str 图标的tex文件
    'priority',  # int 加载优先级，数值越大优先级越高，可为负数
    'configuration_options',  # lua_table > list 首先注意，lua中值为nil等于该项不存在，""代表该项为字符串，内容为空
    # name：该项名称，缺省时该设置项将被忽略，label缺省时显示；label：功能名称位置显示的文字；hover：鼠标悬停按钮时最上方显示的文字
    # options缺省时该设置项将被忽略，只有一项时其中的data项不可为nil，否则设置时会崩溃。options中只有一项，且该项中data项为""时视为标题，字号加大，hover将被忽略
    # {{name = "", label = "", hover = "", options = {{ data = "", description = "", hover = ""},}, default = "", is_keylist = boolean, is_boolean = boolean}, }
    'dst_compatible',  # bool 是否兼容饥荒联机
    'forge_compatible',  # bool 是否兼容熔炉
    'gorge_compatible',  # bool 是否兼容暴食
    'dont_starve_compatible',  # bool 是否兼容饥荒单机
    'reign_of_giants_compatible',  # bool 是否兼容饥荒单机巨人国
    'hamlet_compatible',  # bool 是否兼容饥荒单机哈姆雷特
    'shipwrecked_compatible',  # bool 是否兼容饥荒单机海难
    'mod_dependencies',
    # lua_table > list 依赖mod，支持仅创意工坊、仅本地、两者共存，每项只能包含一或零项创意工坊mod，本地mod无限制 {{workshop = "workshop-1111111111", ["Test1"] = true, }, {["Test2_1"] = false, ["Test2_2"] = false, }}
    'StaticAssetsReg',  # 不清楚，应该是lua_table > list 静态资源注册，兼容动态加载mod
    'game_modes',  # 修改游戏模式
    'mim_assets',
]

escape = [34, 39, 48, 63, 92, 97, 98, 102, 110, 114, 116, 118]
# escape = ['"', "'", '0', '?', '\\', 'a', 'b', 'f', 'n', 'r', 't', 'v']

# bom 头 [大端字节序, 小端字节序]
bom = [b'\xef\xbb\xbf', b'\xef\xbf\xbe']

# lupa 全局变量
lupag = ['locale', 'folder_name', 'ChooseTranslationTable'] + ['print', 'rawlen', 'loadfile', 'rawequal', 'pairs', '_VERSION', 'select', 'pcall', 'debug', 'io', 'getmetatable', 'assert', 'package', 'os', 'warn', 'next', 'load', 'tostring', 'setmetatable', 'rawget', 'coroutine', 'tonumber', 'error', 'collectgarbage', 'python', 'utf8', 'math', 'ipairs', 'rawset', 'type', 'xpcall', '_G', 'table', 'dofile', 'require', 'string']


def table_dict(lua_table):
    if lupa.lua_type(lua_table) == 'table':
        keys = list(lua_table)
        # 假如lupa.table为空，或keys都是整数，且从数字 1 开始以 1 为单位递增，则认为是列表，否则为字典
        if reduce(lambda x, y: x and isinstance(y, int), keys, len(keys) == 0 or keys[0] == 1):  # 为空或首项为 1，全为整数
            if all(map(lambda x, y: x + 1 == y, keys[:-1], keys[1:])):  # 以 1 为单位递增
                return list(map(lambda x: table_dict(x), lua_table.values()))
        return dict(map(lambda x, y: (x, table_dict(y)), keys, lua_table.values()))
    # 由于需要用于解析 modinfo 为 json 格式，所以不支持函数，这里直接删掉
    if lupa.lua_type(lua_table) == 'function':
        return '这里原本是个函数，不过已经被我干掉了'
    return lua_table


def parse_modinfo_single(data_raw, modid=0, lang='zh'):
    """

    :param data_raw: modinfo 的内容
    :type data_raw: bytes
    :param modid: mod 在创意工坊对应的 id
    :type modid: int or str
    :param lang: 语言，用于有多语言支持时返回对应语言版本
    :type lang: str
    :return: dict
    """

    def invalid_escape():
        nonlocal data_raw, data
        maybe_err = re.findall(rb'(?:\\\\)*\\(.)', data_raw)
        err_char = filter(lambda x: ord(x) not in escape, maybe_err)
        for char in err_char:
            data_raw = data_raw.replace(b'\\' + char, char)
        data = data_raw.decode(encoding)

    def fix_arg():
        nonlocal data
        data = re.sub(r'\(\.\.\.\)', '(...) local arg = {...} arg.n = #arg', data)

    status, info_dict = 0, {}

    # 去除可能存在的 bom 头，保险起见两个都处理
    if data_raw[:3] in bom:
        modinfo_log.debug('modinfo 中含 BOM 头')
        data_raw = data_raw[3:]

    # 选取合适的编码格式
    try:
        encoding = 'utf-8'
        data = data_raw.decode(encoding)
    except UnicodeDecodeError:
        encoding = chardet.detect(data_raw).get('encoding') or 'latin-1'
        data = data_raw.decode(encoding, errors='replace')

    modinfo_log.debug('modinfo 编码格式为 %s', encoding)

    # 多次尝试解析数据
    for times in range(5):
        try:
            lua = lupa.LuaRuntime()

            # 模拟运行环境
            lua.execute(f'locale = "{lang}"')
            lua.execute(f'folder_name = "workshop-{modid}"')
            lua.execute(f'ChooseTranslationTable = function(tbl) return tbl["{lang}"] or tbl[1] end')

            # 开始处理数据
            lua.execute(data)

            # 选取需要的值并转为 python 对象
            g = lua.globals()
            # 选择白名单或黑名单模式
            info_dict = {key: table_dict(g[key]) for key in filter(lambda x: x not in lupag, g)}
            # info_dict = {key: table_dict(g[key]) for key in filter(lambda x: x in info_list_full, g)}

            # 去除空值
            info_dict = {i: j for i, j in info_dict.items() if j or j is False or j == 0}
            status = 1
            break
        except Exception as e:
            # import logging
            # logging.exception(e)

            # 错误的转义字符
            if 'invalid escape sequence near' in e.__str__():
                modinfo_log.debug('modinfo %s 含有错误的转义序列，准备处理', modid)
                invalid_escape()

            # lupa 的 lua5.4 不支持 5.1 的 arg 语法了，手动处理一下
            elif "a nil value (global 'arg')" in e.__str__():
                modinfo_log.debug('modinfo %s 含有 lua5.4 不支持的 arg 语法，准备处理', modid)
                fix_arg()

            # 一般来说是编译后的 lua5.2 文件，就不处理了吧，饥荒是 5.1 本来也识别不出来的
            elif 'bad binary format' in e.__str__():
                modinfo_log.warn('modinfo %s 预编译了，lua 版本还不对，作者大大滴坏，准备退出', modid)
                break
            else:
                # 这作者写的有问题吧
                modinfo_log.error('modinfo %s 出现了未知的错误，准备退出', modid)
                modinfo_log.error(e, exc_info=True)
                break

    modinfo_log.debug('modinfo %s 解析完成，status: %s', modid, status)
    return status, info_dict


def parse_modinfo(modinfo_raw, modid=0, lang='zh'):
    """

    :param modinfo_raw: 传入字节串或该形式的字典 {'modinfo': b'', 'modinfo_chs': b''}
    :type modinfo_raw: dict or bytes
    :param modid: modid
    :type modid: int str
    :param lang: 语言
    :type lang: str
    :return:
    """

    modinfo_log.info('mod %s 数据传入', modid)

    if isinstance(modinfo_raw, bytes):
        modinfo_log.debug('传入数据为字节类型')
        modinfo_bytes = modinfo_raw
        modinfo_chs_bytes = None

    elif isinstance(modinfo_raw, dict):
        modinfo_log.debug('传入数据为字典类型')
        modinfo_bytes = modinfo_raw.get('modinfo')
        modinfo_chs_bytes = modinfo_raw.get('modinfo_chs')

    else:
        modinfo_log.warn('传入数据类型错误，是 %s', type(modinfo_raw))
        raise ValueError("传入数据类型应为 dict 或 bytes")

    modinfo_log.debug('开始解析 modinfo')
    status, modinfo = parse_modinfo_single(modinfo_bytes, modid, lang)
    if not status:
        modinfo_log.debug('解析 modinfo 失败')
        return status, modinfo

    modinfo_log.debug('解析 modinfo 成功')

    # 有这个翻译支持吗，我是不是被坑了  # 这还真有人用，还是得解析  # 是由汉化 mod 支持的第三方协议，如 1418746242
    if modinfo_chs_bytes:
        modinfo_log.debug('开始解析 modinfo_chs')
        chs_stat, modinfo_chs = parse_modinfo_single(modinfo_chs_bytes, modid, lang)
        if chs_stat:
            modinfo.update(modinfo_chs)
        else:
            modinfo_log.warn('解析 modinfo_chs 失败')
    # if not modinfo_raw.get('modinfo_cht'):
    #     ...

    modinfo_log.info('mod %s modinfo 解析完成，status: %s', modid, status)
    return status, modinfo


if __name__ == '__main__':
    # loc_list = ["fr", "es", "de", "it", "pt", "pl", "ru", "ko", "zh", "zht", "zhr"]
    # 先检测有没有中文版
    with open(r'C:\Users\suke\Desktop\modinfo.lua', 'rb') as f:
        mod_info = parse_modinfo_single(f.read())
    print(list(mod_info[1]))
    # _test()
    # tt = b'name = 0\n version = {} \n author = "" \n priority = false'
    print(parse_modinfo(b''))
