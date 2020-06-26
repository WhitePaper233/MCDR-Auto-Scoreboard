# MCDR-Auto-Scoreboard自动换榜插件

------

## 1.工作原理

​	使用time模块定时向控制台输出/scoreboard指令来实现定时换榜

## 2.工作步骤

​	1.加载时调用check_config_file()函数检查所有配置文件是否存在。若存在，向控制台输出“[AutoScoreboard插件] [通知]配置文件检查完成”；若不存在，则显示丢失的文件名并终止插件加载进程。

​	2.检查无问题后，调用load_settings()和load_scoreboards()函数对设置和计分板配置文件进行加载。

​	3.待服务端完全启动后，调用add_scoreboards(server)函数依次创建计分板，每0.1s创建一个。

​	4.计分板创建完成后，调用display(server)函数滚动显示计分板。

## 3.安装插件

​	1.使用“pip install”安装以下几个模块（均为Python安装时自带或安装MCDR时需要安装的模块，一般无需单独安装）

```
json
time
os
colorama
sys
```

​	2.安装插件本体

​		将plugins文件夹中的AutoScoreboard.py放在:“MCDR根目录/plugins”文件夹下

​	3.安装插件配置文件

​		将config文件夹中的AutoScoreboard文件夹放在“MCDR根目录/config”文件夹下

## 4.配置设置文件

​	插件的设置保存在“MCDR根目录/config/AutoScoreboard/Settings.json”中

| 属性                           | 含义                                                   | 默认值        |
| ------------------------------ | ------------------------------------------------------ | ------------- |
| time_per_scoreboard(second)    | 每个榜单停留时间（单位：秒）                           | 3             |
| start_command                  | 开启滚动榜单指令                                       | “!!asb start” |
| start_command_permission_level | 使用开启滚动榜单指令所需最低权限                       | 1             |
| stop_command                   | 停止滚动榜单指令                                       | "!!asb stop"  |
| stop_command_permission_level  | 使用停止滚动榜单指令所需最低权限                       | 1             |
| help_command                   | 显示插件帮助信息指令                                   | "!!asb help"  |
| Prevent_list_confusion         | 防止榜单混淆（开启后创建榜单时会在榜单名前加上“asb.”） | false         |

## 5.配置榜单文件

​	榜单列表保存在“MCDR根目录/config/AutoScoreboard/ScoreBoards.json”中，其中对象名作为便于修改时找到对应榜单的标识，而不作为插件创建榜单的内容，但请避免使用中文。

​	scoreboard_name作为创建榜单时的名称，若Settings.json中Prevent_list_confusion属性的值为true，则创建时榜单的名称会为“asb.”+scoreboard_name。

​	stats_category属性：

| 属性         | 对应Minecraft中的准则          |
| ------------ | ------------------------------ |
| air          | air                            |
| armor        | armor                          |
| deathCount   | deathCount                     |
| dummy        | dummy                          |
| food         | food                           |
| health       | health                         |
| level        | level                          |
| xp           | xp                             |
| killedByTeam | killedByTeam.                  |
| teamkill     | teamkill.                      |
| broken       | minecraft.broken:minecraft.    |
| crafted      | minecraft.crafted:minecraft.   |
| custom       | minecraft.custom:minecraft.    |
| dropped      | minecraft.dropped:minecraft.   |
| killed       | minecraft.killed:minecraft.    |
| killed_by    | minecraft.killed_by:minecraft. |
| mined        | minecraft.mined:minecraft.     |
| picked_up    | minecraft.picked_up:minecraft. |
| used         | minecraft.used:minecraft.      |

​	stats_content属性：

​		1.对于stats_category属性为'air', 'armor', 'deathCount', 'dummy', 'food', 'health', 'level', 'xp'的计分板，该属性可不填或直接删除，插件不会尝试读取。

例子：

```
    "xp": {
        "scoreboard_name":"xpboard",
        "stats_category": "xp",
        "display_name": "经验榜"
    }
```

​		2.对于stats_category属性为'killedByTeam', 'teamkill'的计分板，该项必填。填写内容为指令时指令stats_category属性对应准则后游戏提示补齐的内容。

例子：

```
    "TK": {
        "scoreboard_name":"tk",
        "stats_category": "teamkill",
        "stats_content": "blue",
        "display_name": "TK榜"
    }
```

​		3.对于stats_category属性为'broken', 'crafted', 'custom', 'dropped', 'killed', 'killed_by', 'mined', 'picked_up', 'used'的计分板，该项必填。填写内容为使用指令时指令stats_category属性对应准则后游戏提示补齐的内容。

例子：

```
"used.diamond_pickaxe": {
        "scoreboard_name":"pickaxe",
        "stats_category": "used",
        "stats_content": "diamond_pickaxe",
        "display_name": "挖掘榜"
    }
```

