import json
from json import loads
from time import localtime, strftime, time
from urllib.parse import urlencode
from urllib.request import Request, urlopen


def getmodinfo(id_):
    url = 'https://api.steampowered.com/ISteamRemoteStorage/GetPublishedFileDetails/v1/'
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/89.0.4389.90 Safari/537.36 ',
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {
        # 'itemcount': '1',           # 单次查询的mod数量
        # 'publishedfileids[0]': ''   # mod id
    }
    if isinstance(id_, (str, int, bytes)):
        data['itemcount'] = '1'
        data['publishedfileids[0]'] = str(id_) if not isinstance(id_, bytes) else id_.decode('utf-8')
    elif isinstance(id_, (list, tuple, set, dict)):
        data['itemcount'] = str(len(id_))
        num = 0
        for modid_ in id_:
            data['publishedfileids[' + str(num) + ']'] = str(modid_)
            num += 1
    else:
        print('输入数据格式错误')
        return
    data = urlencode(data).encode('utf-8')
    req = Request(url=url, data=data, headers=headers)
    response = urlopen(req, timeout=20)
    result = response.read().decode('utf-8')
    response.close()

    # print(result)
    # 格式化数据，输出id对应的标题和版本
    # print(result)
    data = loads(result).get('response').get('publishedfiledetails')
    print('-' * 50)

    mod_info = {}
    for item in data:
        print(item.get('result'))
        workshopid = item.get('publishedfileid')
        title, version = '', ''
        if item.get('result') == 1:
            title = item.get('title')
            version = ''
            for tags in item.get('tags'):
                tag_version = tags.get('tag')
                if 'version' in tag_version:
                    version = tag_version
        mod_info[workshopid] = [title, version]

    print(mod_info)
    return mod_info


def getmodinfo2(id_, key_=None):
    if key_ is None:
        key_ = apikey
    url = 'https://api.steampowered.com/IPublishedFileService/GetDetails/v1/'
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/89.0.4389.90 Safari/537.36 ',
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {
        'steamapikey.txt': key_,                       # steam apikey  https://steamcommunity.com/dev/apikey
        'publishedfileids[0]': id_,        # 要查询的发布文件的ID
        'language': '6',                   # 0英文，6简中，7繁中
        # 'includevotes': 1,                 # 返回投票数据。  应该就是评分数据，那5个星星
        # 'includechildren': 1,            # 返回引用指定项目的项目。  测试了0和1，返回结果一致
        # 'includetags': 1,                # 返回mod详情中的标签。  测试了0和1，返回结果一致
        # 'includekvtags': 1,              # 返回mod详情中的键值标签，对饥荒和tags一样。  测试了0和1，返回结果一致
        # 'includeadditionalpreviews': 1,  # 返回mod的预览图片和视频详情。  测试了0和1，返回结果一致
        # 'short_description': 1,          # 返回简短描述而不是完整描述。 要看mod有没有设置简短描述，不然还是一样的描述
        # 'includeforsaledata': 1,         # 返回定价数据（如果适用）
        # 'includemetadata': 0,            # 填充元数据字段。  测试了0和1，返回结果一致
        # 'return_playtime_stats': 0,      # 返回今天之前指定天数的游戏时间统计信息
        # 'appid': 343050,                 # 游戏id。  不能带这个，不然不返回什么有用的信息
        # 'strip_description_bbcode': 1,   # 从描述中去除换行符
        # 'desired_revision': 0,           # 返回指定修订版的数据。  测试了几个数值，返回的结果都一样
        # 'includereactions': 0            # 返回对项目的反应。  测试了0和1，返回结果一致
    }
    if isinstance(id_, (str, int, bytes)):
        data['publishedfileids[0]'] = str(id_) if not isinstance(id_, bytes) else id_.decode('utf-8')
    elif isinstance(id_, (list, tuple, set, dict)):
        num = 0
        for modid_ in id_:
            data['publishedfileids[' + str(num) + ']'] = str(modid_)
            num += 1
    else:
        print('输入数据格式错误')
        return

    data = urlencode(data)
    url = url + '?' + data

    print('开始发送请求')
    req = Request(url=url, headers=headers)
    response = urlopen(req, timeout=20)
    result = response.read().decode('utf-8')
    response.close()
    print('解析回应')

    # 格式化数据，输出id对应的标题和版本
    print(result)
    data = loads(result).get('response').get('publishedfiledetails')
    print('-' * 50)

    mod_info = {}
    for item in data:
        print(item.get('result'))
        workshopid = item.get('publishedfileid')
        title, version = '', ''
        if item.get('result') == 1:
            title = item.get('title')
            version = ''
            if 'tags' in item:
                for tags in item.get('tags'):
                    tag_version = tags.get('tag')
                    if 'version:' in tag_version:
                        version = tag_version
        mod_info[workshopid] = [title, version]

    print(mod_info)
    return mod_info


def searchmod(text_='1', key=None, page=1, num=10):
    url_base = 'https://api.steampowered.com/IPublishedFileService/QueryFiles/v1/'
    data = {
        # 'return_kv_tags': True,          # 返回mod详情中的键值标签，对饥荒和tags一样
        # 'return_previews': True,         # 在tags的基础上增加mod的预览图片和视频详情
        # 'child_publishedfileid=0': '0',  # 查找所有引用指定项目的项目。
        # 'cursor': cur,  # 返回下一页参数，利用返回的参数访问下一页。第一页为'*'。 # steam 说这个好，实际上一言难尽，漏结果、重复项、凭空多页
        'page': page,
        'steamapikey.txt': key,  # steam apikey  https://steamcommunity.com/dev/apikey
        'appid': 322330,  # 游戏id
        'language': 6,  # 0英文，6简中，7繁中
        'return_tags': True,  # 返回mod详情中的标签
        'numperpage': num,  # 每页结果
        'search_text': text_  # 标题或描述中匹配的文字
    }

    url = url_base + '?' + urlencode(data)
    req = Request(url=url)
    response = urlopen(req, timeout=20)
    mod_data = response.read().decode('utf-8')
    # print(mod_data)
    response.close()

    mod_data = loads(mod_data).get('response')

    mod_num = mod_data.get('total')
    mod_info_full = mod_data.get('publishedfiledetails')

    mod_list = []
    if mod_info_full:
        for mod_info_raw in mod_info_full:
            img = mod_info_raw.get('preview_url', '')
            auth = mod_info_raw.get("creator")

            mod_info = {
                'id': mod_info_raw.get('publishedfileid', ''),
                'name': mod_info_raw.get('title', ''),
                'file': mod_info_raw.get('file_url', ''),
                # 'auth': f'https://steamcommunity.com/profiles/{auth}/?xml=1' if auth else '',
                # 'desc': mod_info_raw.get('file_description'),
                'time': mod_info_raw.get('time_updated', ''),
                # 'sub': mod_info_raw.get('subscriptions', ''),
                # 'img': f'{img}?imw=64&imh=64&ima=fit&impolicy=Letterbox&imcolor=%23000000&letterbox=true' if 'steamuserimages' in img else '',
                'v': [*[i.get('tag')[8:] for i in mod_info_raw.get('tags', '') if i.get('tag', '').startswith('version:')], ''][0],
            }
            mod_list.append(mod_info)
        print('done')
        start2 = time()
        global start
        print(start2 - start)
        start = start2
    return {'num': mod_num, 'mod': mod_list}



if __name__ == '__main__':
    # https://partner.steamgames.com/doc/webapi/ISteamRemoteStorage
    # https://api.steampowered.com/ISteamRemoteStorage/GetUGCFileDetails/v1/
    print('执行时间：{}'.format(strftime("%Y.%m.%d %H:%M:%S", localtime(time()))))

    with open('steamapikey.txt', 'r', encoding='utf-8') as f:
        apikey = f.read().strip()
    # path = r'C:\Users\suke\Desktop'
    # import os
    # with open(os.path.join(path, 'lack.json'), 'r', encoding='utf-8') as f:
    #     modidlist = json.loads(f.read())
    # for i in range(12):
    #     print(i)
    #     modid = modidlist[i * 100:(i+1)*100]
    #     xxx = getmodinfo2(modid, apikey)  # 和上个几乎一样，而且支持mod的多语言适配，但是需要apikey。部分mod信息上个函数获取不到，这个可以
    #     with open(os.path.join(path, str(i) + '123'), 'w', encoding='utf-8') as f:
    #         f.write(json.dumps(xxx))

    modid = '2392968885'
    # modid = '1755586017'
    # getmodinfo(modid)             # 返回mod的详细信息，这里只打印了版本号。只能返回mod原语言，不支持mod的多语言适配 获取不到非公开的mod
    getmodinfo2(modid, apikey)  # 和上个几乎一样，而且支持mod的多语言适配，但是需要apikey。部分mod信息上个函数获取不到，这个可以

    # search_text = input('输入搜索项\n') or ' '
    # start = time()
    # for ii in range(130):
    #     print(ii + 1)
    #     searchmod(search_text, apikey, ii+1)
    # print(searchmod('', apikey, 1).get('num'))

