#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@author: mario
@contact:mariogoogla@gmail.com
@version: 1.0.0
@file: redis_client.py
@time: 2023/7/13 11:08
"""
import redis

from config import config


class RedisClientSingleton:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        if not hasattr(self, 'redis_client'):
            self.redis_client = redis.Redis(
                host=config.get('common').get('redis_db').get('host'),
                port=config.get('common').get('redis_db').get('port'),
                password=config.get('common').get('redis_db').get('password'),
                decode_responses=True
            )


# 创建Redis客户端实例
redis_client = RedisClientSingleton().redis_client


class RedisKeys:
    REDIS_KEY_PREFIX = "jiujia:"

    TOKEN = REDIS_KEY_PREFIX + "token"
    SYSTEM_CONFIG = REDIS_KEY_PREFIX + "GetSystemConfig"
    SPECIAL_RESERVATION_INSTITUTIONS = REDIS_KEY_PREFIX + "GetSpecialReservationInstitutions"
