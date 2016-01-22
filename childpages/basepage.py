#!/usr/bin/python
# -*- coding: utf-8 -*-
from qframer.qt import QtGui
from qframer.qt import QtCore


class BasePage(QtGui.QWidget):
    def __init__(self, parent=None):
        super(BasePage, self).__init__(parent)
        self.parent = parent
