# coding: utf8

import json
import time
import os
import colorama
import sys

# 目录
Config_Path = os.path.join(os.path.dirname('plugins'),'config','AutoScoreboard')

# 查找文件
def search(path, name):
    if os.path.exists(Config_Path + os.sep + name):
        return True
    else:
        return False


# 检查配置文件
def check_config_file():
    check_config_1 = 0
    check_config_2 = 0

    if search(Config_Path, 'Settings.json'):
        check_config_1 = 1
    else:
        print(colorama.Fore.RED, '[AutoScoreboard插件][警告]AutoScoreboard配置文件“Settings.json”丢失', colorama.Fore.WHITE)

    if search(Config_Path, 'ScoreBoards.json'):
        check_config_2 = 1
    else:
        print(colorama.Fore.RED, '[AutoScoreboard插件][警告]AutoScoreboard配置文件“ScoreBoards.json”丢失', colorama.Fore.WHITE)

    if check_config_1 == 1 and check_config_2 == 1:
        print(colorama.Fore.GREEN, '[AutoScoreboard插件][通知]配置文件检查完成', colorama.Fore.WHITE)
    else:
        print(colorama.Fore.RED, '[AutoScoreboard插件][警告]终止AutoScoreboard进程...', colorama.Fore.WHITE)
        sys.exit()


# 读取设置文件
def load_settings():
    # 读取json文件
    settingsfile = open(Config_Path + os.sep + 'Settings.json', encoding="utf-8")
    settings = json.load(settingsfile)
    # 榜单间隔
    global tps
    # 开始指令
    global start_command
    # 结束指令
    global stop_command
    # 开始指令权限
    global start_command_pl
    # 结束指令权限
    global stop_command_pl
    # 帮助指令
    global help_command
    tps = settings['time_per_scoreboard(second)']
    start_command = settings['start_command']
    stop_command = settings['stop_command']
    help_command = settings['help_command']
    start_command_pl = settings['start_command_permission_level']
    stop_command_pl = settings['stop_command_permission_level']
    # 防止榜单混淆
    global command_prefix
    if settings['Prevent_list_confusion'] == True:
        command_prefix = 'asb.'
    elif settings['Prevent_list_confusion'] == False:
        command_prefix = ''
    else:
        pass


# 读取榜单列表
def load_scoreboards():
    # 读取json文件
    boards_file = open(Config_Path + os.sep + 'ScoreBoards.json', encoding="utf-8")
    global boards
    boards = json.load(boards_file)


# 创建计分板
def add_scoreboards(server):
    type_1 = ['air', 'armor', 'deathCount', 'dummy', 'food', 'health', 'level', 'xp']
    type_2 = ['killedByTeam', 'teamkill']
    type_3 = ['broken', 'crafted', 'custom', 'dropped', 'killed', 'killed_by', 'mined', 'picked_up', 'used']
    global formed_command
    for scoreboard in boards:
        scoreboard_name = command_prefix + boards[scoreboard]['scoreboard_name']
        criterion_1 = boards[scoreboard]['stats_category']
        display_name = '"' + boards[scoreboard]['display_name'] + '"'
        if criterion_1 in type_1:
            formed_command = '/scoreboard objectives add {} {} {}'.format(scoreboard_name, criterion_1, display_name)
        elif criterion_1 in type_2:
            criterion_2 = boards[scoreboard]['stats_content']
            formed_command = '/scoreboard objectives add {} {}.{} {}'.format(scoreboard_name, criterion_1, criterion_2, display_name)
        elif criterion_1 in type_3:
            criterion_2 = boards[scoreboard]['stats_content']
            formed_command = '/scoreboard objectives add {} minecraft.{}:minecraft.{} {}'.format(scoreboard_name, criterion_1, criterion_2, display_name)
        else:
            pass
        time.sleep(0.1)
        server.execute(formed_command)
    else:
        pass


# 循环榜单
def display(server):
    while state == 1:
        for scoreboard in boards:
            command = '/scoreboard objectives setdisplay sidebar {}{}'.format(command_prefix, boards[scoreboard]['scoreboard_name'])
            server.execute(command)
            time.sleep(tps)
    else:
        pass


check_config_file()


def on_load(server, old_module):
    # 插件默认状态
    global state
    state = 1
    load_settings()
    load_scoreboards()
    server.add_help_message(help_command, '显示AutoScoreBoard帮助信息')
    server.add_help_message(start_command, '启动滚动计分板')
    server.add_help_message(stop_command, '暂停滚动计分板')


def on_server_startup(server):
    add_scoreboards(server)
    display(server)


def on_info(server, info):
    if info.content.startswith(start_command) and info.is_player:
        global state
        if server.get_permission_level(info) >= start_command_pl:
            state = 1
            display(server)
        else:
            server.reply(info, '§4你没有使用这个命令的权限！', encoding="utf-8")
    if info.content.startswith(stop_command) and info.is_player:
        if server.get_permission_level(info) >= stop_command_pl:
            state = 0
        else:
            server.reply(info, '§4你没有使用这个命令的权限！', encoding="utf-8")
    if info.content == help_command and info.is_player:
        help_info = ['========MCDR AutoScoreBoard 插件========', start_command + '启动滚动计分板', stop_command + '暂停滚动计分板', '======================================']
        for line in help_info:
            server.reply(info, line, encoding='utf-8')