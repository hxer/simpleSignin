#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from .bean import Bean
from .bean_app import BeanApp
from .bean_jr import SignJR
from .daka_app import DakaApp
from .data_station import DataStation
from .double_jr import DoubleSign_JR
from .jdstock_sign import JDStock_Sign
from .shopsign import ShopSign

__all__ = ['jobs_all']

jobs_all = [ShopSign, DakaApp, Bean, SignJR, BeanApp, DataStation]
