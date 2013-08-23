#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import json
import logging

logger = logging.getLogger(__name__)

logo_ico = os.sep.join([os.getcwd(), 'skin', 'images', 'config8.png'])
logo_img_url = os.sep.join([os.getcwd(), 'skin', 'images', 'ov-orange-green.png'])
logo_title = u''

try:
    with open(os.sep.join([os.getcwd(), 'options', 'windowsoptions.json']), 'r') as f:
        windowsoptions = json.load(f)
        logger.info('Load windowsoptions from file')
except Exception, e:
    logger.exception(e)
    logger.info('Load windowsoptions from local')
    windowsoptions = {
        'login_window': {
                'title': u'登陆',
                'windowicon': logo_ico,
                'minsize': (400, 300),
                'size': (400, 300),
                'logo_title': logo_title,
                'logo_img_url': logo_img_url
            },
        'webseverlogin_window': {
                'title': u'WebService登陆',
                'windowicon': logo_ico,
                'minsize': (400, 300),
                'size': (400, 300),
                'logo_title': u'加载来自WebService的防区',
                'logo_img_url': logo_img_url
            },
        'mainwindow': {
                'title': logo_title,
                'postion': (300, 300),
                'minsize': (800, 600),
                'size': (800, 600),
                'windowicon': logo_ico,
                'fullscreenflag': True,
                'centralwindow': {
                    'page_tag': [['Markdown', 'About']],
                    'page_tag_zh': {
                        'Markdown': u'Markdown编辑(Edit)',
                        'About': u'关于(About)',
                    }
                },
                'MenuSettings':{
                    'visual' : False,
                    'menus':[
                        {
                            'MenuName': u'File',
                            'MenuName_zh': u'',
                            'MenuActions': [
                                {
                                    'Name': u'Exit',
                                    'Name_zh': u'退出',
                                    'Icon': u'',
                                    'Shortcut': u'',
                                    'TriggerName': 'Exit'
                                },
                            ]
                        },
                        {
                            'MenuName': u'Preference',
                            'MenuName_zh': u'',
                            'MenuActions': [
                                {
                                    'Name': u'Settings',
                                    'Name_zh': u'界面设定',
                                    'Icon': u'',
                                    'Shortcut': u'',
                                    'TriggerName': 'Settings'
                                },
                                {
                                    'Name': u'Key Bindings',
                                    'Name_zh': u'快捷键',
                                    'Icon': u'',
                                    'Shortcut': u'',
                                    'TriggerName': 'KeyBindings'
                                },
                            ]
                        },
                        {
                            'MenuName': u'Help',
                            'MenuName_zh': u'',
                            'MenuActions': [
                                {
                                    'Name': u'Documentation',
                                    'Name_zh': u'文档',
                                    'Icon': u'',
                                    'Shortcut': u'',
                                    'TriggerName': 'Documentation'
                                },
                                {
                                    'Name': u'Activity Logging',
                                    'Name_zh': u'活动日志',
                                    'Icon': u'',
                                    'Shortcut': u'',
                                    'TriggerName': 'ActivityLogging'
                                },
                                {
                                    'Name': u'Enter License',
                                    'Name_zh': u'认证',
                                    'Icon': u'',
                                    'Shortcut': u'',
                                    'TriggerName': 'EnterLicense'
                                },
                                {
                                    'Name': u'About',
                                    'Name_zh': u'关于',
                                    'Icon': u'',
                                    'Shortcut': u'',
                                    'TriggerName': 'About'
                                },
                            ]
                        }
                    ]    
                },
                'statusbar': {
                    'initmessage': u'Ready',
                    'minimumHeight': 30,
                    'visual': True
                },
                'navigation_show': True
            },
        'logo_widget': {
            'title': u'Logo 控件',
            'windowicon': logo_ico,
            'minsize': (400, 300),
            'size': (400, 300),
            'logo_title': u'基于PyQt4的C/S客户端框架',
            'logo_img_url': u''
        },
        'exitdialog': {
            'title': u'登陆',
            'windowicon': logo_ico,
            'minsize': (400, 300),
            'size': (400, 300),
            'logo_title': logo_title,
            'logo_img_url': logo_img_url
        },
        'adddcdialog': {
            'title': u'增加采集器',
            'windowicon': logo_ico,
            'minsize': (400, 300),
            'size': (400, 300),
            'logo_title': logo_title,
            'logo_img_url': logo_img_url
        },
        'msgdialog': {
            'title': u'消息提示',
            'windowicon': logo_ico,
            'minsize': (400, 300),
            'size': (400, 300),
            'logo_title': logo_title,
            'logo_img_url': logo_img_url
        },
        'confirmdialog': {
            'title': u'消息提示',
            'windowicon': logo_ico,
            'minsize': (400, 300),
            'size': (400, 300),
            'logo_title': logo_title,
            'logo_img_url': logo_img_url
        },
        'urldialog': {
            'title': u'输入访问的url',
            'windowicon': logo_ico,
            'minsize': (400, 300),
            'size': (400, 300),
            'logo_title': logo_title,
            'logo_img_url': logo_img_url
        },
        'ipaddressdialog': {
            'title': u'输入访问的url',
            'windowicon': logo_ico,
            'minsize': (400, 300),
            'size': (400, 300),
            'logo_title': logo_title,
            'logo_img_url': logo_img_url
        },
        'numinputdialog': {
            'title': u'输入整数',
            'windowicon': logo_ico,
            'minsize': (400, 300),
            'size': (400, 300),
            'logo_title': logo_title,
            'logo_img_url': logo_img_url
        },
        'splashimg': os.sep.join([os.getcwd(), 'skin', 'images', 'splash.png']),
        'monitorpage': {
            'backgroundimg': logo_img_url
        },
        'maxpanum': 128,
        'panum': 6,
        'status_islog': False
    }
