#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@author: mario
@contact:mariogoogla@gmail.com
@version: 1.0.0
@file: common_timer.py
@time: 2023/7/13 15:24
"""

from apscheduler.schedulers.background import BackgroundScheduler

from app.jiujia import jiujia
from channel.wechat.wechat_channel import WechatChannel
from common.log import logger

# 创建调度器：BlockingScheduler
# 配置执行器，并设置线程数
scheduler = BackgroundScheduler()


def start_up():
    logger.info("scheduler start up success")
    scheduler.add_job(sync, 'cron', hour=7, minute=30)  # 每天早上7点30分执行
    scheduler.add_job(sync, 'cron', hour=17, minute=33)  # 每天下午5点30分执行
    scheduler.add_job(sync, 'cron', hour=8, minute=8)  # 每天下午5点30分执行
    scheduler.add_job(notice, 'cron', hour=8, minute=30)
    # scheduler.add_job(notice, 'cron', hour=8)
    scheduler.add_job(notice_remain, 'cron', minute='*/1')

    scheduler.start()
    logger.info("scheduler start up success")


def notice_remain():
    reservation_times = jiujia.get_time()

    current_time = datetime.now()

    for reservation_time, value in reservation_times.items():
        target_time = datetime.strptime(reservation_time, "%Y-%m-%d %H:%M:%S")

        # 计算与当前时间的时间差
        time_difference = target_time - current_time

        # 将时间差转换为分钟
        minutes_difference = int(time_difference.total_seconds() / 60)
        logger.info(
            f"reservation_time:{reservation_time},minutes_difference:{minutes_difference},current_time:{current_time}")
        if minutes_difference == 10 or minutes_difference == 5 or minutes_difference == 1 or minutes_difference == 60 * 2 or minutes_difference == 30:
            WechatChannel().send_keyword_group(f" @所有人 抢号倒计时：{minutes_difference}分钟")
            for item in value:
                area_result, show = jiujia.convert_area_data(item, "", True)
                logger.info(f"reservation_time:{reservation_time},area_result:{area_result}")
                WechatChannel().send_keyword_group(area_result)
                break


from datetime import datetime


def notice():
    WechatChannel().send_keyword_group(" @所有人 今日可预约医院：")
    area_results = jiujia.gen_time_info(None)
    for area_result in area_results:
        WechatChannel().send_keyword_group(area_result)


def sync():
    if not jiujia.sync_db():
        jiujia.login(jiujia.account, jiujia.password, jiujia.get_code(jiujia.account))
        jiujia.sync_db()
