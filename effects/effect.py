#!/usr/bin/python
# -*- coding: utf-8 -*-

from PyQt4 import QtGui
from PyQt4 import QtCore


class FaderWidget(QtGui.QWidget):
    '''
        淡入淡出效果控件
    '''
    def __init__(self, parent=None):
        super(FaderWidget, self).__init__(parent)

        if parent:
            self.startColor = parent.palette().window().color()
        else:
            self.startColor = QtCore.Qt.white

        self.currentAlpha = 0
        self.duration = 1000

        self.timer = QtCore.QTimer(self)
        self.connect(self.timer, QtCore.SIGNAL("timeout()"), self.update)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.resize(parent.size())

    def start(self):
        self.currentAlpha = 255
        self.timer.start(100)
        self.show()

    def paintEvent(self, event):
        semiTransparentColor = self.startColor
        semiTransparentColor.setAlpha(self.currentAlpha)
        painter = QtGui.QPainter(self)
        painter.fillRect(self.rect(), semiTransparentColor)
        self.currentAlpha -= (255 * self.timer.interval() / self.duration)

        if self.currentAlpha <= 0:
            self.timer.stop()
            self.close()
