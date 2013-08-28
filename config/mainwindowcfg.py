#!/usr/bin/python
# -*- coding: utf-8 -*-

from PyQt4 import QtCore
from . import logo_ico

# 工具条toolbar停靠位置
dockAreas = {
    'left': QtCore.Qt.LeftToolBarArea,
    'right': QtCore.Qt.RightToolBarArea,
    'top': QtCore.Qt.TopToolBarArea,
    'bottom': QtCore.Qt.BottomToolBarArea
}


mainwindowsettings = {
    'title': u'',
    'postion': (300, 300),
    'minsize': (800, 600),
    'size': (800, 600),
    'windowicon': logo_ico,
    'fullscreenflag': True,
    'centralwindow': {
        'pagetags': [['Markdown', 'QChrome', 'About']],
        'pagetags_zh': {
            'Markdown': u'Markdown编辑(Edit)',
            'QChrome': u'QChrome(调试)',
            'About': u'关于(About)',
        }
    },
    'menusettings': {
        'visual': False,
        'menus': [
            {
                'name': u'File',
                'name_zh': u'',
                'actions': [
                    {
                        'name': u'Exit',
                        'name_zh': u'退出',
                        'icon': u'',
                        'shortcut': u'Ctrl+K',
                        'trigger': 'Exit',
                    },
                ]
            },
            {
                'name': u'Preference',
                'name_zh': u'',
                'actions': [
                    {
                        'name': u'Settings',
                        'name_zh': u'界面设定',
                        'icon': u'',
                        'shortcut': u'',
                        'trigger': 'Settings',
                    },
                    {
                        'name': u'Key Bindings',
                        'name_zh': u'快捷键',
                        'icon': u'',
                        'shortcut': u'',
                        'trigger': 'KeyBindings',
                    },
                ]
            },
            {
                'name': u'Help',
                'name_zh': u'',
                'actions': [
                    {
                        'name': u'Documentation',
                        'name_zh': u'文档',
                        'icon': u'',
                        'shortcut': u'',
                        'trigger': 'Documentation',
                    },
                    {
                        'name': u'Activity Logging',
                        'name_zh': u'活动日志',
                        'icon': u'',
                        'shortcut': u'',
                        'trigger': 'ActivityLogging',
                    },
                    {
                        'name': u'Enter License',
                        'name_zh': u'认证',
                        'icon': u'',
                        'shortcut': u'',
                        'trigger': 'EnterLicense',
                    },
                    {
                        'name': u'About',
                        'name_zh': u'关于',
                        'icon': u'',
                        'shortcut': u'',
                        'trigger': 'About',
                    },
                ]
            }
        ]
    },
    'toolbarsettings': {
        'visual': False,
        'dockArea': dockAreas['left'],
        'movable': False,
        'toolbars': [
            {
                'id': u'ImportButton',
                'icon': u'',
                'name': u'',
                'name_zh': u'',
                'shortcut': u'Ctrl+K',
                'trigger': u'',
                'tooltip': u'Import Markdown File'
            },
            {
                'id': u'ExportButton',
                'icon': u'',
                'name': u'',
                'name_zh': u'',
                'shortcut': u'Ctrl+M',
                'trigger': u'',
                'tooltip': u'Export Markdown File'
            },
            {
                'id': u'PreviewButton',
                'icon': u'',
                'name': u'',
                'name_zh': u'',
                'shortcut': u'Ctrl+P',
                'trigger': u'',
                'tooltip': u'Preview Markdown File in fullscreen'
            },
            {
                'id': u'ShareButton',
                'icon': u'',
                'name': u'',
                'name_zh': u'',
                'shortcut': u'Ctrl+L',
                'trigger': u'',
                'tooltip': u'Share Markdown File in Interent'
            },
            {
                'id': u'MinButton',
                'icon': u'',
                'name': u'',
                'name_zh': u'',
                'shortcut': u'',
                'trigger': u'',
                'tooltip': u'Min Window'
            },
            {
                'id': u'CloseButton',
                'icon': u'',
                'name': u'',
                'name_zh': u'',
                'shortcut': u'',
                'trigger': u'',
                'tooltip': u'Close Window'
            },
        ]
    },
    'statusbarsettings': {
        'initmessage': u'Ready',
        'minimumHeight': 30,
        'visual': True
    },
    'navigationvisual': True
}
