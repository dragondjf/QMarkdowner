#!/usr/bin/python
# -*- coding: utf-8 -*-
from PyQt4 import QtGui
from PyQt4 import QtCore
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

        QtCore.QObject.connect(getattr(self, 'Navigation' + 'Button'), QtCore.SIGNAL('clicked()'), self.parent, QtCore.SLOT('backnavigationPage()'))
        QtCore.QObject.connect(getattr(self, 'Back' + 'Button'), QtCore.SIGNAL('clicked()'), self.parent, QtCore.SLOT('backPage()'))
        QtCore.QObject.connect(getattr(self, 'Forward' + 'Button'), QtCore.SIGNAL('clicked()'), self.parent, QtCore.SLOT('forwardnextPage()'))

        QtCore.QObject.connect(getattr(self, 'Min' + 'Button'), QtCore.SIGNAL('clicked()'), self.parent.parent(), QtCore.SLOT('showMinimized()'))
        QtCore.QObject.connect(getattr(self, 'Max' + 'Button'), QtCore.SIGNAL('clicked()'), self.parent.parent(), QtCore.SLOT('windowMaxNormal()'))
        QtCore.QObject.connect(getattr(self, 'Close' + 'Button'), QtCore.SIGNAL('clicked()'), self.parent.parent(), QtCore.SLOT('close()'))

        # getattr(self, 'MaxButton').setDisabled(True)


    def createNavigationByPage(self):
        navbutton = windowsoptions['mainwindow']['centralwindow']['pagetags'][0] + ['Min', 'Close']
        navbutton_zh = windowsoptions['mainwindow']['centralwindow']['pagetags_zh']
        self.navigation = QtGui.QWidget()
        navigationLayout = QtGui.QHBoxLayout()

        for item in navbutton:
            button = item + 'Button'
            if item not in ['Min', 'Close']:
                setattr(self, button, QtGui.QPushButton(navbutton_zh[item]))
                getattr(self,  button).clicked.connect(self.parent.childpageChange)
            else:
                setattr(self, button, QtGui.QPushButton())

            getattr(self, button).setObjectName(button)
            navigationLayout.addWidget(getattr(self, button))
        self.navigation.setLayout(navigationLayout)
        self.navigation.setMaximumHeight(60)
        self.navigation.setContentsMargins(0, 0, 0, 0)

        QtCore.QObject.connect(getattr(self, 'Min' + 'Button'), QtCore.SIGNAL('clicked()'), self.parent.parent(), QtCore.SLOT('showMinimized()'))
        QtCore.QObject.connect(getattr(self, 'Close' + 'Button'), QtCore.SIGNAL('clicked()'), self.parent.parent(), QtCore.SLOT('close()'))
