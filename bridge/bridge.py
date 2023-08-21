#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@author: mario
@contact:mariogoogla@gmail.com
@version: 1.0.0
@file: bridge.py
@time: 2023/7/12 11:07
"""
from model import model_factory
import config
# from plugins.event import Event, EventContext
# from plugins.plugin_manager import PluginManager


class Bridge(object):
    def __init__(self):
        pass

    def fetch_reply_content(self, query, context):
        type = config.conf().get("model").get("type")
        return model_factory.create_bot(type).multiple_replies(query, context)

    # def fetch_reply_content(self, query, context):
    #     # econtext = PluginManager().emit_event(EventContext(
    #     #     Event.ON_BRIDGE_HANDLE_CONTEXT, {'context': query, 'args': context}))
    #     type = config.conf().get("model").get("type")
    #     # query = econtext.econtext.get("context", None)
    #     # reply = econtext.econtext.get("reply", "无回复")
    #     # if not econtext.is_pass() and query:
    #     return model_factory.create_bot(type).reply(query, context)
        # else:
        #     return reply

    # async def fetch_reply_stream(self, query, context):
    #     econtext = PluginManager().emit_event(EventContext(
    #         Event.ON_BRIDGE_HANDLE_CONTEXT, {'context': query, 'args': context}))
    #     type = econtext['args'].get('model') or config.conf().get("model").get("type")
    #     query = econtext.econtext.get("context", None)
    #     reply = econtext.econtext.get("reply", "无回复")
    #     bot = model_factory.create_bot(type)
    #     if not econtext.is_pass() and query:
    #         async for final, response in bot.reply_text_stream(query, context):
    #             yield final, response
    #     else:
    #         yield True, reply
