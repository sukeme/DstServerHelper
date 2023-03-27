##!/usr/bin/python3
# -*- coding: utf-8 -*-
# https://docs.python.org/zh-cn/3/library/logging.config.html#logging-config-dictschema
import logging
import logging.config

LOGGING_CONF = {
    'version': 1,
    'incremental': False,
    'disable_existing_loggers': False,
    'formatters': {
        'simple': {
            'format': '%(asctime)s | %(levelname)-8s | - %(message)s',
            'datefmt': '%y-%m-%d %H:%M:%S',
            'style': '%',  # 指定的格式化类型 % { $，默认 %
            'validate': True,  # 格式错误就报错
            # 'class': '',  # 指定 formatter 类的名称，用于实例化自定义的类
        },
        'complex': {
            'format': '%(asctime)s | %(levelname)-8s | %(name)-8s:%(lineno)4d | %(funcName)-20s | - %(message)s',
            'datefmt': '%y-%m-%d %H:%M:%S',
            'style': '%',  # 指定的格式化符号，默认 %
            'validate': True,  # 格式错误就报错
            # 'class': '',  # 指定 formatter 类的名称，用于实例化自定义的类
        }
    },
    'filters': {},
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'INFO',
            'formatter': 'simple',
            # 'filter': []

            # 下面的将会作为实例化的参数
            # 'stream': 'ext://sys.stdout',
        },
        'file': {
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'level': 'DEBUG',
            'formatter': 'complex',
            # 'filter': []

            'filename': './log/app.log',
            'when': 'midnight',
            'encoding': 'utf-8',
        }
    },
    'loggers': {
        'app': {
            'level': 'DEBUG',
            'propagate': False,
            # 'filters': [],
            'handlers': ['console', 'file'],
        },
        'steamapi': {
            'level': 'DEBUG',
            'propagate': False,
            # 'filters': [],
            'handlers': ['console', 'file'],
        },
        'tools': {
            'level': 'DEBUG',
            'propagate': False,
            # 'filters': [],
            'handlers': ['console', 'file'],
        },
        'modinfo': {
            'level': 'DEBUG',
            'propagate': False,
            # 'filters': [],
            'handlers': ['console', 'file'],
        },
        'world': {
            'level': 'DEBUG',
            'propagate': False,
            # 'filters': [],
            'handlers': ['console', 'file'],
        },
        'sql': {
            'level': 'DEBUG',
            'propagate': False,
            # 'filters': [],
            'handlers': ['console', 'file'],
        },
    },
    'root': {
        'level': 'INFO',
        'handlers': ['console', 'file']
    }
}

logging.config.dictConfig(LOGGING_CONF)

app_log      = logging.getLogger('app')
modinfo_log  = logging.getLogger('modinfo')
sql_log      = logging.getLogger('sql')
steamapi_log = logging.getLogger('steamapi')
tools_log    = logging.getLogger('tools')
world_log    = logging.getLogger('world')

# print(logging.Logger.manager.loggerDict)
