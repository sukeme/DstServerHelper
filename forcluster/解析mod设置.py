##!/usr/bin/python3
# -*- coding: utf-8 -*-
import json
import os
from functools import reduce
from os.path import basename, split as psplit, splitext
from re import findall

import lupa


def table_dict(lua_table, locale_list=None, lang=None):
    if lupa.lua_type(lua_table) == 'table':
        keys = list(lua_table)
        # 假如lupa.table为空，或keys都是整数，且从数字 1 开始以 1 为单位递增，则认为是列表，否则为字典
        if reduce(lambda x, y: x and isinstance(y, int), keys, len(keys) == 0 or keys[0] == 1):  # 为空或首项为 1，全为整数
            if all(map(lambda x, y: x + 1 == y, keys[:-1], keys[1:])):  # 以 1 为单位递增
                return list(map(lambda x: table_dict(x, locale_list, lang), lua_table.values()))
        new_dict = dict(map(lambda x, y: (x, table_dict(y, locale_list, lang)), keys, lua_table.values()))
        # 如果字典第一个键值为1，后续键值都在locale_list内，则认为是用了klei的多语言支持写法 {"An English Name", ["zh"] = "中文名",}
        # scripts/languages/loc.lua 查看locale所有值
        # 1、使用locale加逻辑判断来返回不同语言；2、通过ChooseTranslationTable函数支持，格式{"默认值", ["locale值"] = "locale语言中对应值",}
        if locale_list and list(new_dict)[0] == 1 and set(new_dict) < set(locale_list + [1]):
            new_dict = new_dict.get(lang) or new_dict.get(1)
        return new_dict
    return lua_table


def get_modinfo(path_modinfo, path_loc, lang='zh'):
    cwd_now = os.getcwd()
    with open(path_loc, 'r') as f:
        data_loc = f.read()
    locale_list = findall(r'(?<=code = ")\w+(?=")', data_loc)
    path_moddir, dirname = psplit(path_modinfo)[0], basename(psplit(path_modinfo)[0])

    os.chdir(path_moddir)
    lua = lupa.LuaRuntime()
    lua.execute('locale = python.eval("lang")')
    lua.execute('folder_name = python.eval("dirname")')
    lua.require(splitext(psplit(path_modinfo)[1])[0])
    os.chdir(cwd_now)

    info_list_full = [
        # 以下标注为解析后的类型，因为科雷的第二种多语言支持方式会导致返回lua_table，处理后才是标注值，举例如下：
        # lua_table > dict  {"An English Name", ["zh"] = "中文名",}，会被lupa解析为{1: 'An English Name', 'zh': '中文名'}
        'name',  # str mod名称
        'version',  # str 版本号
        'version_compatible',  # str 兼容版本号
        'author',  # str 作者
        'description',  # str 介绍
        'api_version',  # int ds mod api为6。ds只检查此项
        'api_version_dst',  # int dst mod api为10。dst首先检查此项， 此项没有会去检查'api_version'项
        'client_only_mod',  # bool 是否为仅客户端mod
        'folder_name',  # str mod所在文件夹
        'forumthread',  # str klei论坛的对应主题帖，应该是部分链接
        'server_filter_tags',  # lua_table > list 添加服务器标签 {"tag0", "tag1", "tag2", }
        'all_clients_require_mod',  # bool 服务器与客户端需要共同开启的mod
        'icon_atlas',  # str 图标的xml文件
        'icon',  # str 图标的tex文件
        'priority',  # int 加载优先级，数值越大优先级越高，可为负数
        # 'configuration_options',  # lua_table > list 首先注意，lua中值为nil等于该项不存在，""代表该项为字符串，内容为空
        # name：该项名称，缺省时该设置项将被忽略，label缺省时显示；label：功能名称位置显示的文字；hover：鼠标悬停按钮时最上方显示的文字
        # options缺省时该设置项将被忽略，只有一项时其中的data项不可为nil，否则设置时会崩溃。options中只有一项，且该项中data项为""时视为标题，字号加大，hover将被忽略
        # {{name = "", label = "", hover = "", options = {{ data = "", description = "", hover = ""},}, default = ""}, }
        'dst_compatible',  # bool 是否兼容饥荒联机
        'forge_compatible',  # bool 是否兼容熔炉
        'gorge_compatible',  # bool 是否兼容暴食
        'dont_starve_compatible',  # bool 是否兼容饥荒单机
        'reign_of_giants_compatible',  # bool 是否兼容饥荒单机巨人国
        'hamlet_compatible',  # bool 是否兼容饥荒单机哈姆雷特
        'shipwrecked_compatible',  # bool 是否兼容饥荒单机海难
        'mod_dependencies',  # lua_table > list 依赖mod，支持仅创意工坊、仅本地、两者共存，每项只能包含一或零项创意工坊mod，本地mod无限制 {{workshop = "workshop-1111111111", ["Test1"] = true, }, {["Test2_1"] = false, ["Test2_2"] = false, }}
        'StaticAssetsReg'  # 不清楚，应该是lua_table > list 静态资源注册，兼容动态加载mod
    ]
    g = lua.globals()
    info_dict = {i: table_dict(g[i], locale_list, lang) for i in info_list_full if i in g}
    # print('\n'.join(f'{i}: {j}' for i, j in info_dict.items()))
    print(info_dict)
    return info_dict


path_lo = r"C:\Program Files (x86)\Steam\steamapps\common\Don't Starve Together\data\databundles\scripts\languages\loc.lua"
path = r'C:\Users\suke\Desktop\modinfo.lua'  # 先检测有没有中文版
language = 'zh'

info = get_modinfo(path, path_lo)
if path == 1:
    open('modinfo.json', 'w').write(json.dumps(info))
# print(info)
"""
    "\243\176\128\128", -- 1 F3B08080 红色骷髅
    "\243\176\128\129", -- 2 F3B08081 牛
    "\243\176\128\130", -- 3 F3B08082 箱子
    "\243\176\128\131", -- 4 F3B08083 切斯特
    "\243\176\128\132", -- 5 F3B08084 crockpot
    "\243\176\128\133", -- 6 F3B08085 眼球
    "\243\176\128\134", -- 7 F3B08086 齿
    "\243\176\128\135", -- 8 F3B08087 农场
    "\243\176\128\136", -- 9 F3B08088 火焰
    "\243\176\128\137", -- 10 F3B08089 鬼
    "\243\176\128\138", -- 11 F3B0808A墓碑
    "\243\176\128\139", -- 12 F3B0808B 火腿棒
    "\243\176\128\140", -- 13 F3B0808C 锤子
    "\243\176\128\141", -- 14 F3B0808D 心
    "\243\176\128\142", -- 15 F3B0808E 饥饿
    "\243\176\128\143", -- 16 F3B0808F灯泡
    "\243\176\128\144", -- 17 F3B08090 猪人
    "\243\176\128\145", -- 18 F3B08091 粪便
    "\243\176\128\146", -- 19 F3B08092 红宝石
    "\243\176\128\147", -- 20 F3B08093 理智
    "\243\176\128\148", -- 21 F3B08094 科学机
    "\243\176\128\149", -- 22 F3B08095 头骨
    "\243\176\128\150", -- 23 F3B08096 礼帽
    "\243\176\128\151", -- 24 F3B08097 网页
    "\243\176\128\152", -- 25 F3B08098 剑
    "\243\176\128\153", -- 26 F3B08099 强力臂
    "\243\176\128\154", -- 27 F3B0809A 金块
    "\243\176\128\155", -- 28 F3B0809B 割炬
    "\243\176\128\156", -- 29 F3B0809C 阿比盖尔花
    "\243\176\128\157", -- 30 F3B0809D炼金机
    "\243\176\128\158", -- 31 F3B0809E背包
    "\243\176\128\159", -- 32 F3B0809F 蜂箱
    "\243\176\128\160", -- 33 F3B080A0 浆果丛
    "\243\176\128\161", -- 34 F3B080A1 胡萝卜
    "\243\176\128\162", -- 35 F3B080A2 鸡蛋
    "\243\176\128\163", -- 36 F3B080A3 眼花
    "\243\176\128\164", -- 37 F3B080A4 火坑
    "\243\176\128\165", -- 38 F3B080A5 牛角
    "\243\176\128\166", -- 39 F3B080A6 大肉
    "\243\176\128\167", -- 40 F3B080A7 钻石
    "\243\176\128\168", -- 41 F3B080A8 盐
    "\243\176\128\169", -- 42 F3B080A9 影子操纵器
    "\243\176\128\170", -- 43 F3B080AA 铲
    "\243\176\128\171", -- 44 F3B080AB 竖起大拇指
    "\243\176\128\172", -- 45 F3B080AC 捕兔器
    "\243\176\128\173", -- 46 F3B080AD 奖杯
    "\243\176\128\174", -- 47 F3B080AE 挥手
    "\243\176\128\175", -- 48 F3B080AF 虫洞
"""