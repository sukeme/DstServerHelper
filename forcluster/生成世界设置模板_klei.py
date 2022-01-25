##!/usr/bin/python3
# -*- coding: utf-8 -*-
# 调用 kle 的工具获取 worldgenoverride 模板，并不好用因为环境限制加没有翻译。
# 引用顺序不要修改
import os
import lupa
t = lupa.LuaRuntime()
path = r"C:\Program Files (x86)\Steam\steamapps\common\Don't Starve Together\data\databundles\scripts"
os.chdir(path)

t.execute('function math.pow(x, y) return x ^ y end')  # for tuning
t.execute('function IsNotConsole() return true end')  # IsNotConsole() 不是 PS4 或 XBONE 就返回 True  # for customize
t.execute('function IsConsole() return false end')  # IsConsole() 是 PS4 或 XBONE 就返回 True  # for forest
t.execute('function IsPS4() return false end')  # IsPS4() 不是 PS4 就返回False  # for customize
t.execute('POT_GENERATION = true')  # for strings
t.execute('ModManager = {}')  # for startlocations

t.require('class')  # for util
t.require('util')  # for startlocations
t.require('constants')  # 新年活动相关
t.require("strict")  # for levels
t.require("strings")  # for forest
t.require('tuning')  # for worldsettings_overrides
t.require("custompresets")  # for levels
t.execute('CustomPresetManager = CustomPresets()')  # for levels

t.require("tools/generate_worldgenoverride")
