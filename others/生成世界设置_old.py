r"""https://forums.kleientertainment.com/forums/topic/53014-worldgenoverridelua-with-the-new-post-caves-settings/page/5/"""

r"""
C:\Program Files (x86)\Steam\steamapps\common\Don't Starve Together\data\databundles\scripts\map\customize.lua
世界设置
C:\Program Files (x86)\Steam\steamapps\common\Don't Starve Together\data\databundles\scripts\strings.lua
世界设置的选项名
C:\Program Files (x86)\Steam\steamapps\common\Don't Starve Together\data\databundles\scripts\languages\chinese_s.po
选项名的翻译

通过 WORLDGEN_GROUP 系列函数，获取世界设置选项
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
from re import findall, search, sub
from json import dumps, loads
from time import time

misc_default = {
    'worldgen_misc': {
        'forest': {
            'has_ocean': True,  # 控制陆地之外是海洋还是以前的空洞  有海上物品的不能关，卡生成
            'keep_disconnected_tiles': True,  # 不知道
            'layout_mode': "LinkNodesByKeys",  # 不知道，生成地面是1，生成其它世界是2 "LinkNodesByKeys", "RestrictNodesByKey"
            'no_joining_islands': True,  # 不知道
            'no_wormholes_to_disconnected_tiles': True,  # 不知道
            'roads': "default",  # 控制刷不刷自然生成的小路 "never", "default"
            'wormhole_prefab': "wormhole"  # 控制虫洞位置刷虫洞还是大触手，也可以强行其它物品，就是不能跳。"wormhole", "tentacle_pillar", nil

        },
        'cave': {
            'layout_mode': "RestrictNodesByKey",  # 不知道，生成地面是1，生成其它世界都是2 "LinkNodesByKeys", "RestrictNodesByKey"
            'roads': "never",  # 控制刷不刷自然生成的小路 "never", "default"
            'wormhole_prefab': "tentacle_pillar"  # 控制虫洞位置刷什么东西。"wormhole", "tentacle_pillar", nil

        }
    },
    'worldsettings_misc': {
        'forest': {},
        'cave': {}
    }
}  # 正常存档的默认选项，建议不要改动

desc_list = [
    'frequency_descriptions', 'worldgen_frequency_descriptions', 'ocean_worldgen_frequency_descriptions',
    'starting_swaps_descriptions', 'petrification_descriptions', 'speed_descriptions', 'disease_descriptions',
    'day_descriptions', 'season_length_descriptions', 'season_start_descriptions', 'size_descriptions',
    'branching_descriptions', 'loop_descriptions', 'complexity_descriptions', 'specialevent_descriptions',
    'yesno_descriptions', 'extrastartingitems_descriptions', 'autodetect',
    'dropeverythingondespawn_descriptions',
    'atrium_descriptions'
]

desc_fix = {
    'frequency_descriptions': '{\n        { text = STRINGS.UI.SANDBOXMENU.SLIDENEVER, data = "never" },\n        { text = STRINGS.UI.SANDBOXMENU.SLIDERARE, data = "rare" },\n        { text = STRINGS.UI.SANDBOXMENU.SLIDEDEFAULT, data = "default" },\n        { text = STRINGS.UI.SANDBOXMENU.SLIDEOFTEN, data = "often" },\n        { text = STRINGS.UI.SANDBOXMENU.SLIDEALWAYS, data = "always" },\n    }',
    'worldgen_frequency_descriptions': '{\n        { text = STRINGS.UI.SANDBOXMENU.SLIDENEVER, data = "never" },\n        { text = STRINGS.UI.SANDBOXMENU.SLIDERARE, data = "rare" },\n        { text = STRINGS.UI.SANDBOXMENU.SLIDEUNCOMMON, data = "uncommon" },\n        { text = STRINGS.UI.SANDBOXMENU.SLIDEDEFAULT, data = "default" },\n        { text = STRINGS.UI.SANDBOXMENU.SLIDEOFTEN, data = "often" },\n        { text = STRINGS.UI.SANDBOXMENU.SLIDEMOSTLY, data = "mostly" },\n        { text = STRINGS.UI.SANDBOXMENU.SLIDEALWAYS, data = "always" },\n        { text = STRINGS.UI.SANDBOXMENU.SLIDEINSANE, data = "insane" },\n    }',
    'ocean_worldgen_frequency_descriptions': '{\n        { text = STRINGS.UI.SANDBOXMENU.SLIDENEVER, data = "ocean_never" },\n        { text = STRINGS.UI.SANDBOXMENU.SLIDERARE, data = "ocean_rare" },\n        { text = STRINGS.UI.SANDBOXMENU.SLIDEUNCOMMON, data = "ocean_uncommon" },\n        { text = STRINGS.UI.SANDBOXMENU.SLIDEDEFAULT, data = "ocean_default" },\n        { text = STRINGS.UI.SANDBOXMENU.SLIDEOFTEN, data = "ocean_often" },\n        { text = STRINGS.UI.SANDBOXMENU.SLIDEMOSTLY, data = "ocean_mostly" },\n        { text = STRINGS.UI.SANDBOXMENU.SLIDEALWAYS, data = "ocean_always" },\n        { text = STRINGS.UI.SANDBOXMENU.SLIDEINSANE, data = "ocean_insane" },\n    }',
    'size_descriptions': '{\n        \n        { text = STRINGS.UI.SANDBOXMENU.SLIDESMALL, data = "small"},\n        { text = STRINGS.UI.SANDBOXMENU.SLIDESMEDIUM, data = "medium"},\n        { text = STRINGS.UI.SANDBOXMENU.SLIDESLARGE, data = "default"},\n        { text = STRINGS.UI.SANDBOXMENU.SLIDESHUGE, data = "huge"},\n        \n    }'
}  # 该部分会因为平台不同，有不同的选项，涉及到if、for等语句，比较麻烦，直接替换吧反正应该不太可能有改动

desc_spe = {
    'tasksets.GetGenTaskLists': {'forest': {'default': '联机版', 'classic': '经典'}, 'cave': {'cave_default': '地下'}},
    'startlocations.GetGenStartLocations': {'forest': {'default': '默认', 'plus': '额外资源', 'darkness': '黑暗'},
                                            'cave': {'caves': '洞穴'}}
}  # 调用了其它函数的，有点复杂，生物群落和出生点，不太可能会改，直接指定吧

group_list = ['WORLDGEN_GROUP', 'WORLDSETTINGS_GROUP']

misc_list = ['WORLDGEN_MISC', 'WORLDSETTINGS_MISC']


def translate_text(data_chs):
    global path_cus
    with open(path_cus, 'r', encoding='utf-8') as f:
        data = f.read()
    data = sub(r'(?<=[^-])--\[\[[\S\s]*?]]', '', data)  # 删除多行注释
    data = sub(r'--[\S\s]*?(?=\n)', '', data)  # 删除单行注释
    data_chs = data_chs[data_chs.find('STRINGS.UI.SAND'):]
    data_chs = sub(r'#\.[\d\D]*?\n', '', data_chs)
    code = findall(r'STRINGS\.UI\.SANDBOXMENU(?:[.]?[0-9A-Z_]+)*', data)
    r = r'"[\d\D]*?msgid\s*"(?P<en>[\d\D]*?)"[\d\D]*?msgstr\s*"(?P<ch>[\d\D]*?)"'
    # r = r'"\nmsgid "(?P<en>[\d\D]*?)"\nmsgstr "(?P<ch>[\d\D]*?)"'
    chs = {i: {'chs': ch, 'en': en} for i in code for ch, en in [search(i[21:] + r, data_chs).group('ch', 'en')]}
    # chs = {i: search(i[21:] + r'"[\d\D]*?msgstr\s*"(?P<chs>[\d\D]*?)"', data_chs).group('chs') for i in code}
    # print(chs)
    return chs


def translate_items(group_dict_, data_chs):
    data = group_dict_
    code = [iii for i in data for ii in data.get(i) for iii in data.get(i).get(ii).get('items')]
    data_chs = data_chs[:data_chs.rfind('STRINGS.UI.C') + 1000]
    data_chs = sub(r'#\.[\d\D]*?\n', '', data_chs)
    # chs = {i: search(r'\.{}"[\d\D]*?msgstr\s*"(?P<ch>[\d\D]*?)"'.format(i.upper()), data_chs).group('ch') for i in code}
    r = r'\.{}"[\d\D]*?msgid\s*"(?P<e>[\d\D]*?)"[\d\D]*?msgstr\s*"(?P<c>[\d\D]*?)"'
    chs = {i: {'chs': c, 'en': e} for i in code for c, e in [search(r.format(i.upper()), data_chs).group('c', 'e')]}
    # print(chs)
    return chs


def to_dict(data_raw):  # 传入数据为'{...}'或'[...]'
    sign = (('[', ']'), ('{', '}'))[data_raw.startswith('{')]
    data_raw = data_raw[data_raw.find(sign[0]):data_raw.rfind(sign[1]) + 1]
    data_raw = data_raw.replace('=', ' : ').replace('  ', ' ').replace(' :', ':').replace(' ,', ',').replace(
        '["', '"').replace('"]', '"').replace('\t', '    ')
    data_raw = sub(r'(?P<item>[\w.]+)(?=\s*:)', r'"\g<item>"', data_raw)  # 键加 ""
    data_raw = sub(r'(:\s*)(?P<item>[\w.]+)', r'\1"\g<item>"', data_raw)  # 值加 ""
    data_raw = sub(r',(?=\s*?[}|\]])', r'', data_raw)  # 删去与结束符"}]"之间无数据的逗号
    data_raw = sub(r'({[^:]*?})', lambda x: '[' + x.group()[1:-1] + ']', data_raw)  # 内部不包含":"的"{}"转为"[]"
    data_raw = data_raw.replace('"nil"', 'false')
    data = loads(data_raw)
    return data


def parse_brace(data_raw):
    times, times_tmp, result = 0, 0, []
    if '{' not in data_raw or '}' not in data_raw:
        return
    for i in range(len(data_raw)):
        times += 1 if data_raw[i] == '{' else 0
        times -= 1 if data_raw[i] == '}' and times else 0
        result.append([i, i]) if times_tmp == 0 and times == 1 else 0
        if times_tmp == 1 and times == 0:
            result[-1][1] = i
        times_tmp = times
    # for i in range(len(result)):  # 递归查询子串中的大括号范围
    #     find = parse_brace(data_raw[result[i][0] + 1:result[i][1]])
    #     result[i] = result[i] + [find] if find else result[i]
    #  输出切割一次后的数据
    # data = [data_raw[0:result[i][1] + 1] if i == 0 else data_raw[result[i - 1][1] + 1:result[i][1] + 1] for i in range(len(result))]
    return result


def parse_var(data_raw):
    result = []
    result.append(0) if data_raw[0:6] == 'local ' else 0
    for i in range(len(data_raw) - 7):
        if data_raw[i] == '\n':
            if data_raw[i + 1:i + 7] == 'local ':
                result.append(i + 1)
    data = [data_raw[result[i]:result[i + 1]] for i in range(len(result) - 1)]
    return data


def to_group(data_raw, chs):
    global group_list
    group_dict = {i: ii[ii.find('{'):] for i in group_list for ii in data_raw if ' ' + i + ' = {' in ii}
    for i, value in group_dict.items():
        find = parse_brace(value)
        find = find[0] if find else [0, len(value)]
        group_dict[i] = to_dict(value[find[0]:find[1] + 1])
        group_value = group_dict.get(i)
        for ii, class_value in group_value.items():
            text_value = class_value.get('text', '')
            class_value['text'] = chs.get(text_value) if 'STRINGS.UI' in text_value else text_value
    group_dict['worldgen_group'] = group_dict.pop('WORLDGEN_GROUP')
    group_dict['worldsettings_group'] = group_dict.pop('WORLDSETTINGS_GROUP')
    # print(group_dict)
    return group_dict


def to_misc(data_raw):
    global misc_list
    misc_dict = {i: ii[ii.find('{'):] for i in misc_list for ii in data_raw if ' ' + i + ' = {' in ii}
    for i in misc_dict:
        value = misc_dict.get(i)
        find = parse_brace(value)
        find = find[0] if find else [0, len(value)]
        misc_dict[i] = to_dict(value[find[0]:find[1] + 1])
    misc_dict['worldgen_misc'] = misc_dict.pop('WORLDGEN_MISC')
    misc_dict['worldsettings_misc'] = misc_dict.pop('WORLDSETTINGS_MISC')
    for i, misc_items in misc_dict.items():
        for misc_item in misc_items:
            if misc_item not in misc_default.get(i).get('forest'):
                print('游戏添加了新的未解析的选项：{}'.format(misc_item))
    misc_dict = misc_default
    return misc_dict


def to_desc(data_raw, chs):
    desc_dict = {i: ii[ii.find('{'):] for i in desc_list for ii in data_raw if ' ' + i + ' = {' in ii}
    for desc in desc_dict:
        if desc in desc_fix:
            desc_dict[desc] = desc_fix.get(desc)
        value = desc_dict.get(desc)
        find = parse_brace(value)
        find = find[0] if find else [0, len(value)]
        desc_dict[desc] = {ii.get('data'): chs.get(ii.get('text')) or {
            lang: '{} {}'.format(ch.get(lang), en.get(lang))
            for ch, en in [(chs.get(i) for i in ii.get('text').split('andand'))] for lang in en}
                           for ii in to_dict('[' + value[find[0] + 1:find[1]] + ']')}
        # ii.get('data'): chs.get(ii.get('text')) or ' '.join([chs.get(i) for i in ii.get('text').split('andand')]) for ii in to_dict('[' + value[find[0] + 1:find[1]] + ']')}
    return desc_dict


def process():
    global desc_list, desc_fix, misc_default, path_cus, path_chs
    with open(path_cus, 'r', encoding='utf-8') as f:
        data = f.read()
    with open(path_chs, 'r', encoding='utf-8') as f:
        data_chs = f.read()
    data_chs = data_chs[data_chs.find('"STRINGS.UI.CUS'):data_chs.rfind('"STRINGS.UI.SAND') + 500]
    data = data.replace('    ', '\t').replace('   ', '\t').replace('  ', ' ').replace(
        '\t', '    ').replace('.." "..', 'andand')
    data = sub(r'(?<=[^-])--\[\[[\S\s]*?]]', '', data)  # 删除多行注释
    data = sub(r'--[\S\s]*?(?=\n)', '', data)  # 删除单行注释
    data_var_raw = parse_var(data)  # 以'local '分割的字符串组成的列表
    chs_text = translate_text(data_chs)
    group_dict = to_group(data_var_raw, chs_text)
    chs_item = translate_items(group_dict, data_chs)
    misc_dict = to_misc(data_var_raw)  # 基本用不到这些，游戏内也没有这些设置项，有用的可定义项就一个 'roads'
    desc_dict = to_desc(data_var_raw, chs_text)
    # print(group_dict)
    # print(misc_dict)
    # print(desc_dict)
    # print(chs_text)
    # print(chs_item)
    return group_dict, misc_dict, desc_dict, chs_item


def main():
    group_dict, misc_dict, desc_dict, chs_item = process()
    forest, cave = {}, {}
    result = {'forest': forest, 'cave': cave}
    for group, group_value in group_dict.items():
        forest[group] = {}
        cave[group] = {}
        for com, com_value in group_value.items():
            desc_val = com_value.get('desc')
            desc_v = desc_dict.get(com_value.get('desc')) or desc_spe.get(desc_val, {}).get('forest')
            for world, world_value in result.items():
                world_value.get(group)[com] = {
                    'order': int(com_value.get('order')), 'text': com_value.get('text'), 'desc': desc_v, 'items': {}}
            for item, item_value in com_value.get('items').items():
                tmp = []
                if 'forest' in item_value.get('world', '') or not item_value.get('world', ''):
                    tmp.append(('forest', result.get('forest')))
                if 'cave' in item_value.get('world', ''):
                    tmp.append(('cave', result.get('cave')))
                print('这个有问题{}\n'.format(item_value) if not tmp else '', end='')
                for world, world_value in tmp:
                    world_value.get(group).get(com).get('items')[item] = {
                        'value': item_value.get('value'),
                        'image': item_value.get('image'),
                        'chs': chs_item.get(item)}
                    if item_value.get('desc'):
                        world_value.get(group).get(com).get('items').get(item)['desc'] = desc_dict.get(
                            item_value.get('desc')) or desc_spe.get(
                            item_value.get('desc')).get(world) or item_value.get('desc')
            forest.get(group).pop(com) if not forest.get(group).get(com).get('items') else 0  # 删去空的不包含item项的组
            cave.get(group).pop(com) if not cave.get(group).get(com).get('items') else 0  # 删去空的不包含item项的组
    return result, misc_dict


if __name__ == "__main__":
    path = r"C:\Program Files (x86)\Steam\steamapps\common\Don't Starve Together\data\databundles"
    path_cus = path + r"\scripts\map\customize.lua"
    path_chs = path + r"\scripts\languages\chinese_s.po"  # 出于效率，应该在游戏更新后重新解包scripts时，修改该文件内容为 data_chs
    sss = time()
    options, options_misc = main()
    print('用时', time() - sss)
    open('dst_worldo_setting.json', 'w+', encoding='utf-8').write(dumps(options))
    # print(options)
    # print(options_misc)  # 都是游戏内就不支持自定义的，除了 roads 没有有用的设置项，可忽略
    forest_item = [iiii for i in options if i == 'forest' for ii in options.get(i) for iii in options.get(i).get(ii)
                   for iiii in options.get(i).get(ii).get(iii).get('items')]
    cave_item = [iiii for i in options if i == 'cave' for ii in options.get(i) for iii in options.get(i).get(ii)
                 for iiii in options.get(i).get(ii).get(iii).get('items')]
    print('地上世界选项共{}个'.format(len(forest_item)))
    print('洞穴世界选项共{}个'.format(len(cave_item)))

options = {
    'forest': {
        'worldgen_group': {
            'monsters': {
                'order': 5,
                'text': '敌对生物以及刷新点',
                'desc': {
                    'never': '无',
                    'rare': '很少'
                },  # 优先使用item自有的 desc
                'items': {
                    'spiders': {
                        'value': 'default',
                        'desc': {  # 可能有可能无，优先使用item自带的desc
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
