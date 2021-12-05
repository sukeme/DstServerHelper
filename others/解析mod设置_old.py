"""
简单获取 name 和 version 在 foralive 中有
设置 name 有3种方式：1.直接写在后面；2.定义一个函数，等于这个函数名，用于多语言适配；3.换行后用 [[]] 包含；4、andor的返回值，可能有嵌套
version 有 version和 api_version 等，同时描述中也可能有 version 字段，引号可能单双。
不换行也可以，比如T键，注意避坑

foralive中有转义部分

创意工厂返回的版本标签相对于文件内
1 字母变小写
2 前后空格去除，中间不影响
3 可识别转义
4 有中文或其他不支持的字符时会导致不显示版本。普通英文字符中 , 不可以，这些可以 .:_<>/?'"-+=|()`~*&^%#$#@!\
5 超过58长度之后不显示版本号
./dontstarve_dedicated_server_nullrenderer -cluster 213423 -shard Master -only_update_server_mods

"""

from re import findall, sub
from os import listdir, mkdir, remove, rename, sep, stat, walk
from os.path import abspath, dirname, exists, expanduser, isdir, join as pathjoin


path = r'C:\Users\suke\Desktop\2548785501_\modinfo.lua'
with open(path, 'rb') as f:
    data = f.read()
data = sub(rb'\\(\d{1,3})', lambda x: bytes(chr(int(x.group(1))), 'utf-8', 'ignore'), data).decode(
    'utf-8', 'ignore').encode('latin1', 'ignore')  # 将ascii码转为正常字符
data = sub(rb'[ ]+', b' ', data)  # 将所有空格减少到一位
data = data.replace(b'\n', b'').replace(b'\r', b'').replace(b'\'', b'"')  # 清除换行符，单引号转为双引号
data = sub(rb'version[ ]*=', b'version=', data)
data = sub(rb'=[ ]*"', b'="', data)
version = str(findall(rb'(?<=version=")[\W\w]*?(?=")', data)[0], encoding='utf-8')
print(version)


def get_mod_version(mode=''):
    global path_cluster, path_dst
    path_dst_bin_dir = dirname(path_dst)
    try:

        dir_path1 = pathjoin(path_dst_bin_dir, 'mods')
        dir_path2 = pathjoin(path_dst_bin_dir, 'ugc_mods/MyDediServer/Master/content/322330')
        dir_path3 = pathjoin(path_dst_bin_dir, 'ugc_mods/MyDediServer/Caves/content/322330')

        mod_list, mod_path_list, mod_lack_list, modoverride_paths, mod_version = [], [], [], [], {}

        for i in listdir(path_cluster):
            path_temp = pathjoin(path_cluster, i)
            if isdir(path_temp):
                modoverride_paths.append(path_temp)
        for i in modoverride_paths:
            modo_path = pathjoin(i, 'modoverrides.lua')
            if exists(modo_path):
                with open(modo_path, 'r', encoding='utf-8') as f:
                    data = f.read()
                ignore_data = findall(r'(?<=--\[\[)[\S\s]*?(?=]]--)', data.replace('--[[]]--', ''))
                for ii in ignore_data:
                    data = data.replace(ii, '')
                ignore_data2 = findall(r'(?<=--)[\S\s]*?(?=\n)', data)
                for ii in ignore_data2:
                    data = data.replace(ii, '')
                mod_ids = findall(r'(?<=[\'"]workshop-)\d+(?=[\'"])', data)
                mod_list.extend(mod_ids)
        mod_list = list(set(mod_list))

        for mod_id in mod_list:
            path_tmp1 = pathjoin(pathjoin(dir_path1, 'workshop-' + mod_id), 'modinfo.lua')
            path_tmp2 = pathjoin(pathjoin(dir_path2, mod_id), 'modinfo.lua')
            path_tmp3 = pathjoin(pathjoin(dir_path3, mod_id), 'modinfo.lua')
            if exists(path_tmp2):
                mod_path_list.append(path_tmp2)
            elif exists(path_tmp3):
                mod_path_list.append(path_tmp3)
            elif exists(path_tmp1):
                mod_path_list.append(path_tmp1)
            else:
                mod_lack_list.append(mod_id)
                if mode:
                    print(' ' * 20 + 'mod {} 尚未下载，待更新时下载'.format(mod_id))

        for mod_path in mod_path_list:
            mod_id = mod_path.split(sep)[-2].replace('workshop-', '')
            with open(mod_path, 'rb') as f:
                data = f.read()
            data = sub(rb'\\(\d{1,3})', lambda x: bytes(chr(int(x.group(1))), 'utf-8', 'ignore'), data).decode('utf-8', 'ignore').encode('latin1', 'ignore')
            data = data.replace(b'\n', b'').replace(b'\r', b'').replace(b'\'', b'"')

            too_many_blank = findall(b'version[ ]*=', data)
            for blank in too_many_blank:
                data = data.replace(blank, b'version=')
            too_many_blank2 = findall(b'=[ ]*"', data)
            for blank in too_many_blank2:
                data = data.replace(blank, b'="')
            version = str(findall(rb'(?<=version=")[\W\w]*?(?=")', data)[0], encoding='utf-8')

            mod_version[mod_id] = version

        return mod_version if not mode else mod_lack_list + [i for i in mod_version]
    except Exception as e:
        print('get_mod_version函数出错，未能找到开启的mod')
        print(e)
        return {}
