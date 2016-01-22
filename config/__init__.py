#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import json
# import logging

# logger = logging.getLogger(__name__)

__softwarename__ = 'QMarkdowner'
__author__ = "dragondjf"
__url__ = "dragondjf.github.com"
__description__ = '''
    This is a SoftwareFrame based on qframer.qt with Metro Style.
'''
__logoico__ = os.sep.join([os.getcwd(), 'skin', 'images', 'MarkdownLife.ico'])
__version__ = '1.0.0'


logo_ico = __logoico__
logo_img_url = os.sep.join([os.getcwd(), 'skin', 'images', 'qmarkdowner.png'])
logo_title = u''

from mainwindowcfg import mainwindowsettings
from utildialogcfg import utidialogsettings
from shortcutcfg import shortcutsettings
from markdownthemecfg import markdownthemes

try:
    with open(os.sep.join([os.getcwd(), 'options', 'windowsoptions.json']), 'r') as f:
        windowsoptions = json.load(f)
        # logger.info('Load windowsoptions from file')
except Exception, e:
    # logger.exception(e)
    # logger.info('Load windowsoptions from local')
    windowsoptions = {
        'mainwindow': mainwindowsettings,
        'shortcutsettings': shortcutsettings,
        'splashimg': os.sep.join([os.getcwd(), 'skin', 'images', 'splash.png']),
        'markdownthemes': markdownthemes
    }
    windowsoptions.update(utidialogsettings)
