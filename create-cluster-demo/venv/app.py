##!/usr/bin/python3
# -*- coding: utf-8 -*-
from _log import app_log
from flask import Flask, request, make_response
import tools
from steamapi import searchmod
# from steamapi import Dst
from hashlib import md5
import json
from time import sleep, time
from threading import Timer
from gc import collect

# 实例化一下，启动检查 dst 版本进程
# dst = Dst()

app = Flask(__name__)


@app.route('/tools/')
def test():
    return '<h1>你好</h1>'


@app.route('/tools/searchmod')
def search_mod():
    text = request.args.get('text', '')
    data = searchmod(text, num=25)
    if data is None:
        return 'Search Failed', 503
    data = json.dumps(data.get('mod'), ensure_ascii=False)
    result = make_response(data)
    # result.headers['Access-Control-Allow-Origin'] = '*'
    result.headers['Content-Type'] = 'application/json'
    result.headers['charset'] = 'utf-8'
    result.status = '200 OK'
    return result


@app.route('/tools/cluster', methods=['POST'])
def create_cluster():
    name = md5(request.data).hexdigest()
    data = request.json
    status = tools.createcluster(data, name)
    if not status:
        return '创建存档失败', 500
    result = make_response(name)
    # result.headers['Access-Control-Allow-Origin'] = '*'
    result.headers['charset'] = 'utf-8'
    result.status = '200 OK'
    return result


@app.route('/tools/mod/<int:modid>')
def get_modinfo(modid):
    try:
        code, modinfo = tools.query_modinfo(modid)
        modinfo = json.loads(modinfo)
    except json.JSONDecodeError as e:
        app_log.warning(e)
        code, modinfo = 10, '解析错误'
    except Exception as e:
        app_log.warning(e)
        code, modinfo = 0, '未知错误'
    result = {
        'status': code,
    }
    if code in [1, 2]:
        result['modinfo'] = modinfo
    else:
        result['error'] = modinfo
    result = json.dumps(result, ensure_ascii=False)
    result = make_response(result)
    # result.headers['Access-Control-Allow-Origin'] = '*'
    result.headers['Content-Type'] = 'application/json'
    result.headers['charset'] = 'utf-8'
    result.status = '200 OK'
    return result


# @app.route('/tools/version')
# def check_dst_version():
#     # 为什么服务器部署之后，只有在这里实例化才能真的修改实例属性，其他地方创建修改完访问还是初始值
#     # 导入实例化的对象和函数外创建实例都不可以。主动调用这个函数也不可以，只能等请求来了，才可以
#     # 啊 uwsgi 的问题，真可恶啊浪费好多时间排查，坑啊
#     # https://stackoverflow.com/questions/34252892/using-flask-sqlalchemy-in-multiple-uwsgi-processes
#     if not dst.version:
#         stop_time = time() + 1
#         while True:
#             sleep(0.25)
#             if dst.version:
#                 break
#             if time() > stop_time:
#                 app_log.warning('返回版本号为空')
#                 break
#     return dst.version


def gc_coll():
    collect()
    Timer(21600, gc_coll, ()).start()


gc_coll()

# import objgraph
# def show():
#     objgraph.show_growth()
#     Timer(60, show, ()).start()
#
# show()

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)
    # app.run(debug=True, host='127.0.0.1', port=5000, use_reloader=False)
