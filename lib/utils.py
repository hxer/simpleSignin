#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""

"""
import random


def pad_randomstr(text, size=6):
    chars = '0123456789'
    randstr = ''.join(random.choice(chars) for _ in range(size))
    if isinstance(text, bytes):
        text = str(text, 'utf-8')
    return '{0}{1}'.format(text, randstr)

