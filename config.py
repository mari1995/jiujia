#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@author: mario
@contact:mariogoogla@gmail.com
@version: 1.0.0
@file: config.py
@time: 2023/7/12 11:02
"""
import json
import os

config = {}


def read_file(path):
    with open(path, mode='r', encoding='utf-8') as f:
        return f.read()


def load_config(config_path="./config.json"):
    global config
    if not os.path.exists(config_path):
        raise Exception('配置文件不存在，请根据config-template.json模板创建config.json文件')

    config_str = read_file(config_path)
    # 将json字符串反序列化为dict类型
    config = json.loads(config_str)
    print("Load config success")
    return config


def conf():
    return config


def channel_conf_val(channel_type, key, default=None):
    val = config.get('channel').get(channel_type).get(key)
    if not val:
        # common default config
        return config.get('channel').get(key, default)
    return val
