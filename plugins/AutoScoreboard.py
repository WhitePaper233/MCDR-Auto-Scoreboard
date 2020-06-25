# coding: utf8

import json
import time
import os
import colorama
import sys


# 目录
Config_Path = os.getcwd().split('\plugins')[0] + '\config\AutoScoreboard'


# 查找文件
def search(path, name):
    for root, dirs, files in os.walk(path):
        if name in dirs or name in files:
            flag = 1
            root = str(root)
            dirs = str(dirs)
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
    settingsfile = open(Config_Path + '\Settings.json', encoding="utf-8")
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
    tps = settings['time_per_scoreboard(second)']
    start_command = settings['start_command']
    stop_command = settings['stop_command']
    start_command_pl = settings['start_command_permission_level']
    stop_command_pl = settings['stop_command_permission_level']


# 读取榜单列表
def load_scoreboards():
    # 读取json文件
    boards_file = open(Config_Path + '\ScoreBoards.json', encoding="utf-8")
    global boards
    boards = json.load(boards_file)


# 创建计分板
def add_scoreboards(server):
    global as_command
    for scoreboard in boards:
        scoreboard_name = 'asb.' + boards[scoreboard]['scoreboard_name']
        criterion_1 = boards[scoreboard]['stats_category']
        display_name = '"' + boards[scoreboard]['display_name'] + '"'
        if criterion_1 == 'air' or criterion_1 == 'armor' or criterion_1 == 'deathCount' or criterion_1 == 'dummy' or criterion_1 == 'food' or criterion_1 == 'health' or criterion_1 == 'level':
            as_command = '/scoreboard objectives add {} {} {}'.format(scoreboard_name, criterion_1, display_name)
        elif criterion_1 == 'killedByTeam' or criterion_1 == 'teamkill':
            criterion_2 = boards[scoreboard]['stats_content']
            as_command = '/scoreboard objectives add {} {} {} {}'.format(scoreboard_name, criterion_1, criterion_2, display_name)
        elif criterion_1 == 'broken' or criterion_1 == 'crafted' or criterion_1 == 'custom' or criterion_1 == 'dropped' or criterion_1 == 'killed' or criterion_1 == 'killed_by' or criterion_1 == 'mined' or criterion_1 == 'picked_up' or criterion_1 == 'used':
            criterion_2 = boards[scoreboard]['stats_content']
            as_command = '/scoreboard objectives add {} minecraft.{}:minecraft.{} {}'.format(scoreboard_name, criterion_1, criterion_2, display_name)
        else:
            pass
        server.execute(as_command)
    else:
        pass


# 循环榜单
def display(server):
    while state == 1:
        for scoreboard in boards:
            command = '/scoreboard objectives setdisplay sidebar ' + 'asb.' + boards[scoreboard]['scoreboard_name']
            server.execute(command)
            server.say(state)
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
            server.say(state)
            display(server)
        else:
            server.reply(info, '§4你没有使用这个命令的权限！', encoding="utf-8")
    if info.content.startswith(stop_command) and info.is_player:
        if server.get_permission_level(info) >= stop_command_pl:
            state = 0
        else:
            server.reply(info, '§4你没有使用这个命令的权限！', encoding="utf-8")
    if info.content.startswith('!!ASB help') and info.is_player:
        server.reply(info, start_command + '启动滚动计分板', encoding="utf-8")
        server.reply(info, stop_command + '暂停滚动计分板', encoding="utf-8")