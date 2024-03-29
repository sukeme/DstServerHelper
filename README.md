在线创建存档: http://42.193.112.82:9999/

为方便管理自己的饥荒联机版服务器，写了这个脚本。

目前所有功能都在foralive.py文件中，其它项是为轻松配置世界所做的准备工作。

# 现有功能

1. 闲置超时重置
    * 默认 24 小时。
2. 满天数转无尽
    * 默认 40 天。
3. 检测游戏更新
    * 默认 15 分钟.
4. 备份聊天记录
    * 默认 2 分钟。
5. 检测模组更新
    * 默认 15 分钟。
    * 默认状态不能检测未公开 mod，需要填写 [Steam apikey](https://steamcommunity.com/dev/apikey) 以通过更高权限的 api 检测。
6. 游戏崩溃自启
    * 默认 2 分钟。
7. 网络错误重连
    * 默认 10 分钟
8. 多层世界支持

#### 可能添加

* 细分无人重置间隔，或添加在线时间检测。
    * 不太必要。
* 监测 cpu 负载，高负载过久重启饥荒服务器。
    * 条件很难判定，且高负载时一般玩家也较多，重启非常影响体验。

# 如何使用

## 注意

该脚本作用是自动维护已经开启的饥荒服务器，避免因更新或崩溃等导致服务器不可用，而不是开关或管理服务器。

该方式的优缺点：

* 优点
    * 不需要更换当前使用的开服工具，基本没有迁移成本。
* 缺点
    * 仍然需要一个开服工具，或手动开启服务器。

## 使用限制

1. 只支持Linux平台。
2. 该脚本与游戏进程交互是通过 [screen](https://www.gnu.org/software/screen/) 完成的，确保你开启世界也是同样的方式。
    * 目前开服工具大多采用此方式。

## 开始

### 准备工作

1. 打开文件，修改自定义参数中 screen_dir 项为适合你的设置。
    * 在世界开启的情况下，输入指令 `screen -ls` 可查看相关信息。
2. 打开文件，在文件内开启或关闭各项功能，对自定义参数进行设置。
3. 该脚本会自行检测所需路径，不用填写。如果需要，也可自行指定，脚本会优先使用指定的路径。请使用绝对路径。
4. 如果确定修改了 ugc_mod 目录，则需要填写自定义参数中 ugc_dir 项。

### 开启指令

确保在开启之前，已经关闭之前开启的该脚本，如果不确定，首先执行[**关闭指令**](#关闭指令)。

在 foralive.py 所在路径下执行：

```bash
screen -dmS foralive python3 foralive.py
```

执行指令后会在当前路径下生成 foralive.log 文件，打开该文件即可查看输出信息。

### 关闭指令

任意路径下执行：

```bash
screen -X -S foralive quit
```

# 其它内容

准备搭建一个网站，便于在线创建初始存档。

### 当前进度

已完成饥荒相关的准备工作。

* 通过饥荒服务器 lua 文件自动解析**世界可设置项与其选项**。
* 通过 mod 的 modinfo 文件自动解析**mod设置**。
* 黑/白/管理 名单、cluster.ini、server.ini 等文件的设置项。
* 饥荒表情的提取。

### 完成

功能部分基本写好了，欢迎测试。 地址：https://dst.suke.asia/
