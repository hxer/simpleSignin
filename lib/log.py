#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import logging

logger = logging.getLogger('AutoSignin')

log_format = '%(asctime)s %(name)s %(levelname)s: %(message)s'
logger.propagate = False
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter(log_format)
handler.setFormatter(formatter)
logger.addHandler(handler)