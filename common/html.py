#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@author: mario
@contact:mariogoogla@gmail.com
@version: 1.0.0
@file: html.py
@time: 2023/7/12 16:02
"""
import re


def remove_html(html):
    pattern = re.compile(r'<[^>]+>', re.S)
    result = pattern.sub('', html)
    return result


def format(text):
    formatted_text = re.sub(r"(\d+\.)", r"\n\t\1", text)
    formatted_text = formatted_text.strip()
    return formatted_text
