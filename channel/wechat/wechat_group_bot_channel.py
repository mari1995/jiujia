#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@author: mario
@contact:mariogoogla@gmail.com
@version: 1.0.0
@file: wechat_group_bot_channel.py
@time: 2023/7/12 14:52
"""
import json

import requests

from channel.channel import Channel


class WechatGroupBotChannel(Channel):

    def startup(self):
        pass

    def send(self, msg, receiver):
        url = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=37c1a9a0-3e8c-4180-812e-c156480fab1f"

        payload = json.dumps({
            "msgtype": "text",
            "text": {
                "content": msg
            }
        })
        headers = {
            'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        print(response.text)
