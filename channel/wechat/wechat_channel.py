#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@author: mario
@contact:mariogoogla@gmail.com
@version: 1.0.0
@file: wechat_channel.py
@time: 2023/7/12 11:14
"""
# encoding:utf-8

"""
wechat channel
"""

import time
import itchat
import json
from itchat.content import *
from channel.channel import Channel
from concurrent.futures import ThreadPoolExecutor
from common.log import logger
from common import const, notify_util
from config import channel_conf_val
import requests
# from plugins.plugin_manager import *

import io

thread_pool = ThreadPoolExecutor(max_workers=8)

notice = """禁止发广告、邀请链接等敏感信息\n提前在小程序上注册和填写疫苗接种人信息\n有什么问题或者想要交流的地方尽量在群里提出来解决，或者直接微信私聊问我也都可以。"""


@itchat.msg_register(TEXT)
def handler_single_msg(msg):
    logger.debug("[WX]receive msg: " + json.dumps(msg, ensure_ascii=False))
    WechatChannel().handle(msg)
    return None


@itchat.msg_register(TEXT, isGroupChat=True)
def handler_group_msg(msg):
    logger.debug("[WX]receive msg: " + json.dumps(msg, ensure_ascii=False))
    WechatChannel().handle_group(msg)
    return None


@itchat.msg_register(NOTE, isGroupChat=True)
def group_join_note(msg):
    logger.debug("[WX]receive msg: " + json.dumps(msg, ensure_ascii=False))
    WechatChannel().wellcome(msg)
    return None


class WechatChannel(Channel):
    def __init__(self):
        pass

    def startup(self):
        # login by scan QRCode
        hot_reload = channel_conf_val(const.WECHAT, 'hot_reload', True)
        if channel_conf_val(const.WECHAT, 'receive_qrcode_api'):
            itchat.auto_login(enableCmdQR=2, hotReload=hot_reload, qrCallback=self.login, exitCallback=self.ec)
        else:
            itchat.auto_login(enableCmdQR=2, hotReload=hot_reload, exitCallback=self.ec)

        # start message listener
        itchat.run()

    def ec(self):
        notify_util.logout_notify("")

    def login(self, uuid=None, status='0', qrcode=None):
        logger.info(f'uuid:{uuid}')
        logger.info(f'status:{status}')
        # 请将链接转发到外部接口，并在外部自行通过二维码生成库将链接转换为二维码后展示，例如：将下方的 qrcode_link 通过草料二维码进行处理后，再通过手机端扫码登录微信小号
        logger.info(f'qrcode_link: https://login.weixin.qq.com/l/{uuid}')
        # notify_util.login_notify(f'登陆链接：https://login.weixin.qq.com/l/{uuid}')

    def handle(self, msg):
        from_user_id = msg['FromUserName']
        to_user_id = msg['ToUserName']  # 接收人id
        other_user_id = msg['User']['UserName']  # 对手方id
        create_time = msg['CreateTime']  # 消息时间
        content = msg['Text']

        hot_reload = channel_conf_val(const.WECHAT, 'hot_reload', True)
        if hot_reload == True and int(create_time) < int(time.time()) - 60:  # 跳过1分钟前的历史消息
            logger.debug("[WX]history message skipped")
            return

        # 调用敏感词检测函数
        # if sw.process_text(content):
        #     self.send('请检查您的输入是否有违规内容', from_user_id)
        #     return

        match_prefix = self.check_prefix(content, channel_conf_val(const.WECHAT, 'single_chat_prefix'))
        if from_user_id == other_user_id and match_prefix is not None:
            # 好友向自己发送消息
            if match_prefix != '':
                str_list = content.split(match_prefix, 1)
                if len(str_list) == 2:
                    content = str_list[1].strip()
            thread_pool.submit(self._do_send, content, from_user_id)

        elif to_user_id == other_user_id and match_prefix:
            # 自己给好友发送消息
            str_list = content.split(match_prefix, 1)
            if len(str_list) == 2:
                content = str_list[1].strip()
            thread_pool.submit(self._do_send, content, to_user_id)

    def handle_group(self, msg):
        group_name = msg['User'].get('NickName', None)
        group_id = msg['User'].get('UserName', None)
        create_time = msg['CreateTime']  # 消息时间

        hot_reload = channel_conf_val(const.WECHAT, 'hot_reload', True)
        if hot_reload == True and int(create_time) < int(time.time()) - 60:  # 跳过1分钟前的历史消息
            logger.debug("[WX]history message skipped")
            return

        if not group_name:
            return None
        origin_content = msg['Content']
        content = msg['Content']
        content_list = content.split(' ', 1)
        context_special_list = content.split('\u2005', 1)
        if len(context_special_list) == 2:
            content = context_special_list[1]
        elif len(content_list) == 2:
            content = content_list[1]

        match_prefix = (msg['IsAt'] and not channel_conf_val(const.WECHAT, "group_at_off", False)) or self.check_prefix(
            origin_content, channel_conf_val(const.WECHAT, 'group_chat_prefix')) or self.check_contain(origin_content,
                                                                                                       channel_conf_val(
                                                                                                           const.WECHAT,
                                                                                                           'group_chat_keyword'))

        # 如果在群里被at了 或 触发机器人关键字，则调用敏感词检测函数
        # if match_prefix is True:
        #     if sw.process_text(content):
        #         self.send('请检查您的输入是否有违规内容', group_id)
        #         return

        group_white_list = channel_conf_val(const.WECHAT, 'group_name_white_list')

        if ('ALL_GROUP' in group_white_list or
            group_name in group_white_list or
            self.check_contain(group_name,
                               channel_conf_val(const.WECHAT, 'group_name_keyword_white_list'))) and match_prefix:
            thread_pool.submit(self._do_send_group, content, msg)
        return None

    def send(self, msg, receiver):
        logger.info('[WX] sendMsg={}, receiver={}'.format(msg, receiver))
        itchat.send(msg, toUserName=receiver)

    def _do_send(self, query, reply_user_id):
        try:
            if not query:
                return
            context = dict()
            context['from_user_id'] = reply_user_id

            reply = super().build_reply_content(query)

            if reply:
                self.send(channel_conf_val(const.WECHAT, "single_chat_reply_prefix") + query, reply_user_id)
        except Exception as e:
            logger.exception(e)

    def _do_send_img(self, query, context):
        try:
            if not query:
                return
            reply_user_id = context['from_user_id']
            img_urls = super().build_reply_content(query, context)
            if not img_urls:
                return
            if not isinstance(img_urls, list):
                self.send(channel_conf_val(const.WECHAT, "single_chat_reply_prefix") + img_urls, reply_user_id)
                return
            for url in img_urls:
                # 图片下载
                pic_res = requests.get(url, stream=True)
                image_storage = io.BytesIO()
                for block in pic_res.iter_content(1024):
                    image_storage.write(block)
                image_storage.seek(0)

                # 图片发送
                logger.info('[WX] sendImage, receiver={}'.format(reply_user_id))
                itchat.send_image(image_storage, reply_user_id)
        except Exception as e:
            logger.exception(e)

    def _do_send_group(self, query, msg):
        if not query:
            return
        context = dict()
        context['from_user_id'] = msg['User']['UserName']

        replies = super().build_reply_content(query)
        if isinstance(replies, list):
            for reply in replies:
                reply = '@' + msg['ActualNickName'] + ' \n' + reply.strip()
                self.send(channel_conf_val(const.WECHAT, "group_chat_reply_prefix", "") + reply,
                          msg['User']['UserName'])
        else:
            reply = '@' + msg['ActualNickName'] + ' \n' + replies.strip()
            self.send(channel_conf_val(const.WECHAT, "group_chat_reply_prefix", "") + reply,
                      msg['User']['UserName'])

    def check_prefix(self, content, prefix_list):
        for prefix in prefix_list:
            if content.startswith(prefix):
                return prefix
        return None

    def check_contain(self, content, keyword_list):
        if not keyword_list:
            return None
        for ky in keyword_list:
            if content.find(ky) != -1:
                return True
        return None

    def wellcome(self, msg):
        if u'加入' in msg['Content'] or u'invited' in msg['Content'] or u'join' in msg['Content']:
            str = msg['Content']
            rpos_start = str.rfind('"')
            rpos_end = str.rfind('"', 0, rpos_start)
            invitee = str[(rpos_end + 1): rpos_start]
            itchat.send_msg(
                f"@{invitee} 欢迎来到本群[Rose]，让大家可以顺顺利利打上九价。 \n\n @我 可以获取今日疫苗情况 \n\n{notice}",
                msg['FromUserName'])

    def send_keyword_group(self, content):
        itchat.get_chatrooms(update=True)
        rooms = itchat.search_chatrooms(name=channel_conf_val(const.WECHAT, 'group_name_keyword_white_list')[0])
        for room in rooms:
            try:
                if self.check_contain(room['NickName'],
                                      channel_conf_val(const.WECHAT, 'group_name_keyword_white_list')):
                    user_name = room['UserName']
                    self.send(content, user_name)
            except Exception as e:
                logger.error(f'warning: no this chatroom : {e}')
