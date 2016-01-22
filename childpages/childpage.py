#!/usr/bin/python
# -*- coding: utf-8 -*-
from qframer.qt import QtGui
from qframer.qt import QtCore
from config import windowsoptions
from qchromepage import QChromePage


class ChildPage(QtGui.QWidget):
    """docstring for childPage"""
    def __init__(self, parent=None, child=None):
        super(ChildPage, self).__init__(parent)
        self.parent = parent
        self.child = child
        self.createNavigationByPage()

        mainLayout = QtGui.QVBoxLayout()
        mainLayout.addWidget(self.navigation)
        mainLayout.addWidget(self.child)
        self.setLayout(mainLayout)
        self.layout().setContentsMargins(0, 0, 0, 0)

    def createNavigation(self):
        navbutton = ['Navigation', 'Back', 'Forward', 'Min', 'Max', 'Close']
        navbutton_zh = {
            'Navigation': u'导航主页(Navigation)',
            'Back': u'后退(Back）',
            'Forward': u'前进(Forward)',
            'Min': u'',
            'Max': u'',
            'Close': u''
        }
        self.navigation = QtGui.QWidget()
        navigationLayout = QtGui.QHBoxLayout()

        for item in navbutton:
            button = item + 'Button'
            if item not in ['Min', 'Max', 'Close']:
                setattr(self, button, QtGui.QPushButton(navbutton_zh[item]))
            else:
                setattr(self, button, QtGui.QPushButton())
                getattr(self, button).setMaximumWidth(50)

            getattr(self, button).setObjectName(button)
            navigationLayout.addWidget(getattr(self, button))
        self.navigation.setLayout(navigationLayout)
        self.navigation.setMaximumHeight(60)
        self.navigation.setContentsMargins(0, 0, 0, 0)

       

        getattr(self, 'Navigation' + 'Button').clicked.connect(self.parent.backnavigationPage)
        getattr(self, 'Back' + 'Button').clicked.connect(self.parent.backPage)
        getattr(self, 'Forward' + 'Button').clicked.connect(self.parent.forwardnextPage)
        getattr(self, 'Min' + 'Button').clicked.connect(self.parent.parent().showMinimized)
        getattr(self, 'Max' + 'Button').clicked.connect(self.parent.parent().windowMaxNormal)
        getattr(self, 'Close' + 'Button').clicked.connect(self.parent.parent().close)



    def createNavigationByPage(self):
        systembuttons = ['Min', 'Max', 'Close']
        navbutton = windowsoptions['mainwindow']['centralwindow']['pagetags'][0] + systembuttons
        navbutton_zh = windowsoptions['mainwindow']['centralwindow']['pagetags_zh']
        self.navigation = QtGui.QWidget()
        navigationLayout = QtGui.QHBoxLayout()

        for item in navbutton:
            button = item + 'Button'
            if item not in systembuttons:
                setattr(self, button, QtGui.QPushButton(navbutton_zh[item]))
                getattr(self,  button).clicked.connect(self.parent.childpageChange)
            else:
                setattr(self, button, QtGui.QPushButton())

            getattr(self, button).setObjectName(button)
            navigationLayout.addWidget(getattr(self, button))
        self.navigation.setLayout(navigationLayout)
        self.navigation.setMaximumHeight(60)
        self.navigation.setContentsMargins(0, 0, 0, 0)

        getattr(self, 'Min' + 'Button').clicked.connect(self.parent.parent().showMinimized)
        getattr(self, 'Max' + 'Button').clicked.connect(self.parent.parent().windowMaxNormal)
        getattr(self, 'Close' + 'Button').clicked.connect(self.parent.parent().close)
