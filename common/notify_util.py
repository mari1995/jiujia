import logging

import requests
import json

import config
from common.log import logger


def logout_notify(content):
    title = f"账号登出，请重新登陆"

    url = 'http://www.pushplus.plus/send'
    data = {
        "token": config.conf().get("pushplus_token"),
        "title": title,
        "content": content
    }
    body = json.dumps(data).encode(encoding='utf-8')
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, data=body, headers=headers)
    logging.info(f"监控告警：title:{title} 通知:{response.json()}")


def login_notify(content):
    title = f"账号登陆"

    url = 'http://www.pushplus.plus/send'
    data = {
        "token": config.conf().get("pushplus_token"),
        "title": title,
        "content": content
    }
    body = json.dumps(data).encode(encoding='utf-8')
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, data=body, headers=headers)
    logger.info(f"监控告警：title:{title} 通知:{response.json()}")
