#!/usr/bin/python
# -*- coding: utf-8 -*-
from qframer.qt import QtGui
from qframer.qt import QtCore
from qframer.qt import QtWebKit
from qframer.qt import QtNetwork


class WebkitBasePage(QtGui.QWidget):
    def __init__(self, parent=None):
        super(WebkitBasePage, self).__init__(parent)
        self.parent = parent
        QtNetwork.QNetworkProxyFactory.setUseSystemConfiguration(True)
        QtWebKit.QWebSettings.globalSettings().setAttribute(\
            QtWebKit.QWebSettings.PluginsEnabled, True)

        self.view = QtWebKit.QWebView(self)
        self.view.setFocus()

        self.setupInspector()
        self.splitter = QtGui.QSplitter(self)
        self.splitter.setOrientation(QtCore.Qt.Vertical)

        self.splitter.addWidget(self.view)
        self.splitter.addWidget(self.webInspector)

        mainlayout = QtGui.QVBoxLayout(self)
        mainlayout.addWidget(self.splitter)
        self.setLayout(mainlayout)
        self.layout().setContentsMargins(0, 0, 0, 0)

    def setupInspector(self):
        page = self.view.page()
        page.settings().setAttribute(QtWebKit.QWebSettings.DeveloperExtrasEnabled, True)
        self.webInspector = QtWebKit.QWebInspector(self)
        self.webInspector.setPage(page)

        shortcut = QtGui.QShortcut(self)
        shortcut.setKey(QtCore.Qt.Key_F11)
        shortcut.activated.connect(self.toggleInspector)
        self.webInspector.setVisible(False)

    def toggleInspector(self):
        self.webInspector.setVisible(not self.webInspector.isVisible())
