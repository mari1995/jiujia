#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@author: mario
@contact:mariogoogla@gmail.com
@version: 1.0.0
@file: channel.py
@time: 2023/7/12 11:07
"""
"""
Message sending channel abstract class
"""

from bridge.bridge import Bridge


class Channel(object):
    def startup(self):
        """
        init channel
        """
        raise NotImplementedError

    def handle(self, msg):
        """
        process received msg
        :param msg: message object
        """
        raise NotImplementedError

    def send(self, msg, receiver):
        """
        send message to user
        :param msg: message content
        :param receiver: receiver channel account
        :return:
        """
        raise NotImplementedError

    def build_reply_content(self, query, context=None):
        return Bridge().fetch_reply_content(query, context)

    # async def build_reply_stream(self, query, context=None):
    #     async for final,response in Bridge().fetch_reply_stream(query, context):
    #         yield final,response

    def wellcome(self, msg):
        raise NotImplementedError
