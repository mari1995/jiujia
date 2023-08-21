#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@author: mario
@contact:mariogoogla@gmail.com
@version: 1.0.0
@file: jiujia_model.py
@time: 2023/7/12 11:10
"""
from app.jiujia import jiujia
from common.log import logger
from model.model import Model


class JiuJiaModel(Model):

    def reply(self, query, context=None):
        return ""

    def multiple_replies(self, query, context=None):
        try:
            if query.isdigit():
                infos = jiujia.gen_time_info(query)
                if infos.__len__() == 0:
                    return "没有可预约的九价疫苗"
            else:
                infos = jiujia.gen_info(query)
            return infos

        except Exception as e:
            logger.error(e)
            return "网络出现异常，联系客服"
