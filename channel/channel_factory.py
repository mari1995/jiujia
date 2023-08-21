#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@author: mario
@contact:mariogoogla@gmail.com
@version: 1.0.0
@file: channel_factory.py
@time: 2023/7/12 11:05
"""
from common import const


def create_channel(channel_type):
    """
    create a channel instance
    :param channel_type: channel type code
    :return: channel instance
    """
    if channel_type == const.TERMINAL:
        from channel.terminal.terminal_channel import TerminalChannel
        return TerminalChannel()

    if channel_type == const.WECHAT:
        from channel.wechat.wechat_channel import WechatChannel
        return WechatChannel()

    else:
        raise RuntimeError("unknown channel_type in config.json: " + channel_type)
