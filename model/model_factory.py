#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@author: mario
@contact:mariogoogla@gmail.com
@version: 1.0.0
@file: model_factory.py
@time: 2023/7/12 11:09
"""

from common import const


def create_bot(model_type):
    """
    create a channel instance
    :param channel_type: channel type code
    :return: channel instance
    """

    if model_type == const.JIU_JIA:
        from model.jiujia.jiujia_model import JiuJiaModel
        return JiuJiaModel()

    raise RuntimeError
