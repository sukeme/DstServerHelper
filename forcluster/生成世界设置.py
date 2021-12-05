r"""https://forums.kleientertainment.com/forums/topic/53014-worldgenoverridelua-with-the-new-post-caves-settings/page/5/"""

r"""
C:\Program Files (x86)\Steam\steamapps\common\Don't Starve Together\data\databundles\scripts\map\customize.lua
世界设置
C:\Program Files (x86)\Steam\steamapps\common\Don't Starve Together\data\databundles\scripts\strings.lua
世界设置的选项名
C:\Program Files (x86)\Steam\steamapps\common\Don't Starve Together\data\databundles\scripts\languages\chinese_s.po
选项名的翻译

通过 WORLDGEN_GROUP 系列变量，获取世界设置选项
有通用 desc 的向上搜索对应描述， desc 为除默认外的可选选项，text 为对应选项的名称代号，可用此寻找对应翻译
无通用 desc 的，对应设置项后会附带 desc ，再前往对应位置搜索
world 表明该选项是否包含在某个世界中
某些选项比较危险，不会出现在游戏内的设置项中，建议同样选择隐藏
"""

"""
worldgenoverride.lua
    如果您使用任何给定的选项代替"SURVIVAL_GET"整体预设该服务器的世界看起来会有所不同。
        -- "SURVIVAL_TOGETHER"(默认地上), "MOD_MISSING"(与会添加设置选项的mod有关，用不到), "SURVIVAL_TOGETHER_CLASSIC"(经典地上，无ROG内容), "SURVIVAL_DEFAULT_PLUS"(较困难的地上), "COMPLETE_DARKNESS"(永夜), "TERRARIA" (泰拉)
        -- "DST_CAVE"(默认洞穴), "DST_CAVE_PLUS"(较困难的洞穴), "TERRARIA_CAVE"(泰拉洞穴)
    有关部分预设之间差异的详细信息：
    "SURVIVAL_TOGETHER" - 是默认的 DST 主世界森林世界，其中添加了巨人王朝 DLC 元素，例如更多的巨人、桦木树等。
    "SURVIVAL_TOGETHER_CLASSIC" - 是一个没有巨人王朝 DLC 元素的 DST 主世界森林世界，看起来更接近饥荒原版。
    "SURVIVAL_DEFAULT_PLUS" - 是一个 DST 主世界森林世界，但与上述两个相比难度略有增加。有了这个，主世界将有一个独特的产卵区，更多的恩惠，更少的浆果灌木，更少的胡萝卜，更少的兔子洞，但有更多的蜘蛛。
    "TERRARIA" - 是一个 DST 主世界森林世界，无影怪多雨植物生长快等
    "DST_CAVE" - 是默认的 DST 洞穴世界。
    "DST_CAVE_PLUS" - 是一个 DST 洞穴世界，与默认设置相比难度略有增加。有了这个，洞穴会有更多的恩惠，更少的浅色花朵，发光的浆果和浆果灌木以及更多的蜘蛛。
    "TERRARIA_CAVE" - 蜘蛛蠕虫蝙蝠等变多，荧光果蘑菇树变多

下方内容为 worldgenoverride.lua 文件模板，只需添加override项并根据世界类型修改preset项（"SURVIVAL_TOGETHER"、"DST_CAVE"）即可
preset项 指使用的预设，不同预设中，各选项的默认值会不同。只有默认值不同，所以不同预设其实没有什么区别，选默认然后选项全自定义就好
overrides指玩家自己定义的会覆盖掉预设默认值的选项，没有指定的选项就会用预设中默认值。
"""
r"""
KLEI     1 return {
	override_enabled = true,
	settings_preset = "SURVIVAL_TOGETHER",
	worldgen_preset = "SURVIVAL_TOGETHER",
	overrides = {
		flint = "never",
		grass = "never",
		sapling = "never",
	},
}


"""
import json
import os
import time
from functools import reduce
from os.path import join as pjoin
from re import compile, sub

import lupa

start = time.time()
path_dir = r"C:\Program Files (x86)\Steam\steamapps\common\Don't Starve Together\data\databundles\scripts"
po_chs = r'languages/chinese_s.po'
lua_customize = r'map/customize'  # 务必用正斜杠避免问题。lua 内部 require 会用正斜杠，两个不一样的话操作对应模块时会有坑


def table_dict(lua_table):
    if lupa.lua_type(lua_table) == 'table':
        keys = list(lua_table)
        # 假如lupa.table为空，或keys都是整数，且从数字 1 开始以 1 为单位递增，则认为是列表，否则为字典
        if reduce(lambda x, y: x and isinstance(y, int), keys, len(keys) == 0 or keys[0] == 1):  # 为空或首项为 1，全为整数
            if all(map(lambda x, y: x + 1 == y, keys[:-1], keys[1:])):  # 以 1 为单位递增
                return list(map(lambda x: table_dict(x), lua_table.values()))
        new_dict = dict(map(lambda x, y: (x, table_dict(y)), keys, lua_table.values()))
        if 'desc' in new_dict:  # task_set 和 start_location 的 desc 是个函数，需要调用一下返回实际值
            for i, j in new_dict.items():
                if lupa.lua_type(j) == 'function':
                    new_dict[i] = {world: table_dict(j(world)) for world in new_dict.get('world', [])}
        return new_dict
    return lua_table


def dict_table(py_dict):  # dict 转 table。列表之类类型的转过去会有索引，table_from 的问题，自己写一个太麻烦了又不是不能用
    if isinstance(py_dict, dict):
        return lua.table_from(
            {i: (dict_table(j) if isinstance(j, (dict, list, tuple, set)) else j) for i, j in py_dict.items()})
    return lua.table_from([(dict_table(i) if isinstance(i, (dict, list, tuple, set)) else i) for i in py_dict])


def scan(dict_scan, num, key_set):  # 返回指定深度的 keys 集合, key_set初始传入空set
    if num != 0:
        for value in dict_scan.values():
            if isinstance(value, dict):
                key_set = key_set | scan(value, num - 1, key_set)
        return key_set
    return key_set | set(dict_scan)


def parse_po(path_po):  # 把 po 文件按照 msgctxt: msgstr 的格式转为字典，再以 . 的深度分割 keys。这里为了效率主要转了 UI 部分的
    with open(path_po, 'rb') as f:
        f.seek(-50000, 2)
        data = f.read()
        while b'"STRINGS.T' not in data:
            f.seek(-100000, 1)
            data = f.read(50000) + data
    data = data.decode('utf-8').replace('\r\n', '\n')
    pattern = compile(r'\nmsgctxt\s*"(.*)"\nmsgid\s*"(.*)"\nmsgstr\s*"(.*)"')

    dict_zh_split, dict_en_split = {}, {}
    dict_zh = {i[0]: i[2] for i in pattern.findall(data)}  # 因为 costomize 中有连接字符串的，所以这里不能构建成一个字典，会出错
    for i, j in dict_zh.items():
        split_key(dict_zh_split, i.split("."), j)
    dict_en = {i[0]: i[1] for i in pattern.findall(data)}  # 因为 costomize 中有连接字符串的，所以这里不能构建成一个字典，会出错
    for i, j in dict_en.items():
        split_key(dict_en_split, i.split("."), j)

    dict_split = {'zh': dict_zh_split, 'en': dict_en_split}
    # dict_split = {'zh': dict_zh_split}
    return dict_split


def split_key(dict_split, list_split, value):  # 以列表值为 keys 补全字典深度。用于分割 dict 的 keys，所以叫 split
    if not list_split:
        return
    if list_split[0] not in dict_split:
        dict_split[list_split[0]] = value if len(list_split) == 1 else {}
    split_key(dict_split.get(list_split.pop(0)), list_split, value)


def del_data(path_cus):  # 删去local、不必要的require 和不需要的内容
    with open(path_cus + '.lua', 'r+') as f:
        data = f.read()
        if 'local MOD_WORLDSETTINGS_GROUP' in data:
            data = data[:data.find('local MOD_WORLDSETTINGS_GROUP')]
        f.seek(0)
        f.truncate()
        data = sub(r'local [^=]+?\n', '', data).replace('local ', '')
        data = sub(r'require(?![^\n]+?(?=tasksets"|startlocations"))', '', data)
        f.write(data)


def parse_cus(path, lua_cus, po):
    cwd_now = os.getcwd()
    os.chdir(path)
    del_data(pjoin(path, lua_cus))  # 删去多余的不需要的数据

    lua.execute('function IsNotConsole() return Ture end')  # IsNotConsole() 不是 PS4 或 XBONE 就返回 True  # for customize
    lua.execute('function IsPS4() return False end')  # IsPS4() 不是 PS4 就返回False  # for customize
    lua.execute('ModManager = {}')  # for startlocations
    lua.require('class')  # for util
    lua.require('util')  # for startlocations

    dict_po = parse_po(pjoin(path, po))
    options_list = ['WORLDGEN_GROUP', 'WORLDSETTINGS_GROUP']  # 所需数据列表
    misc_list = ['WORLDGEN_MISC', 'WORLDSETTINGS_MISC']  # 所需数据列表
    options = {}
    for lang, tran in dict_po.items():
        strings = dict_table(tran.get('STRINGS'))
        if strings:
            pass
        lua.execute('STRINGS=python.eval("strings")')  # 为了翻译，也免去要先给 STRINGS 加引号之类的麻烦事
        lua.execute('SPECIAL_EVENTS=STRINGS.UI.SANDBOXMENU')  # 懒猪klei，这里为什么不用全的

        lua.require(lua_customize)  # 终于开始干正事了。导入的 tasksets 会自动打印一些东西出来
        options[lang] = {'setting': {i: table_dict(lua.globals()[i]) for i in options_list if i in lua.globals()},
                         'translate': tran}
        for package in list(lua.globals().package.loaded):  # 清除加载的 customize 模块，避免下次 require 时不加载
            if 'map/' in package:
                lua.execute(f'package.loaded["{package}"]=nil')  # table.remove 不能用，显示 package.loaded 长度为0
    os.chdir(cwd_now)
    miscs = {i: table_dict(lua.globals()[i]) for i in misc_list if i in lua.globals()}
    return options, miscs


def parse_option(group_dict):
    result = {}
    for lang, opt in group_dict.items():
        setting, translate = opt.values()
        forest, cave = {}, {}
        result[lang] = {'forest': forest, 'cave': cave}
        for group, group_value in setting.items():
            forest[group] = {}
            cave[group] = {}
            for com, com_value in group_value.items():
                desc_val = com_value.get('desc')
                for world, world_value in result.get(lang).items():
                    world_value.get(group)[com] = {
                        'order': int(com_value.get('order')), 'text': com_value.get('text'), 'desc': desc_val,
                        'items': {}}
                for item, item_value in com_value.get('items').items():
                    tmp = []
                    if 'forest' in item_value.get('world', '') or not item_value.get('world', ''):
                        tmp.append(('forest', result.get(lang).get('forest')))
                    if 'cave' in item_value.get('world', ''):
                        tmp.append(('cave', result.get(lang).get('cave')))
                    print('这个有问题{}\n'.format(item_value) if not tmp else '', end='')
                    for world, world_value in tmp:
                        world_value.get(group).get(com).get('items')[item] = {
                            'value': item_value.get('value'),
                            'image': item_value.get('image'),
                            'text': translate.get('STRINGS').get('UI').get('CUSTOMIZATIONSCREEN').get(item.upper())}
                        if item_value.get('desc'):
                            world_value.get(group).get(com).get('items').get(item)['desc'] = item_value.get('desc')
                forest.get(group).pop(com) if not forest.get(group).get(com).get('items') else 0  # 删去空的不包含item项的组
                cave.get(group).pop(com) if not cave.get(group).get(com).get('items') else 0  # 删去空的不包含item项的组
    return result


lua = lupa.LuaRuntime()
options_raw, misc = parse_cus(path_dir, lua_customize, po_chs)
# print(options_raw)
settings = parse_option(options_raw)
print(time.time() - start)
# print(settings)

if settings == 1:
    open('dst_world_setting.json', 'w').write(json.dumps(settings))

eg = {
    'zh': {
        'forest': {
            'worldgen_group': {
                'monsters': {
                    'order': 5,
                    'text': '敌对生物以及刷新点',
                    'desc': {  # 优先使用 item 自有的 desc
                        'never': '无',
                        'rare': '很少'
                    },
                    'items': {
                        'spiders': {
                            'value': 'default',
                            'desc': {  # 可能有可能无，优先使用 item 自带的 desc
                                'never': '无',
                                'rare': '很少'
                            },
                            'image': 'spiderden.tex',
                            'chs': '蜘蛛巢'

                        },
                        'houndmound': {}
                    },
                },
                'animals': {}
            },
            'worldsettings_group': {}
        },
        'cave': {}
    }
}
