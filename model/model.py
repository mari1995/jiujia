#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@author: mario
@contact:mariogoogla@gmail.com
@version: 1.0.0
@file: model.py
@time: 2023/7/12 11:08
"""
"""
Auto-replay chat robot abstract class
"""


class Model(object):
    def reply(self, query, context=None):
        """
        model auto-reply content
        :param req: received message
        :return: reply content
        """
        raise NotImplementedError

    def multiple_replies(self, query, context=None):
        """
        model auto-reply content
        :param req: received message
        :return: reply content
        """
        raise NotImplementedError
