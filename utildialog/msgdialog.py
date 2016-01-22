#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
from qframer.qt import QtGui
from qframer.qt import QtCore

from basedialog import BaseDialog


class MessageDialog(BaseDialog):
    def __init__(self, text, styleoptions, parent=None):
        super(MessageDialog, self).__init__(styleoptions, parent)
        # message内容提示
        self.msglabel = QtGui.QLabel(text)
        self.msglabel.setAlignment(QtCore.Qt.AlignCenter)
        #确认按钮布局
        self.enterwidget = QtGui.QWidget()
        self.pbEnter = QtGui.QPushButton(u'确定', self)
        self.pbEnter.clicked.connect(self.enter)
        self.enter_mainlayout = QtGui.QGridLayout()
        self.enter_mainlayout.addWidget(self.pbEnter, 0, 0)
        self.enterwidget.setLayout(self.enter_mainlayout)

        self.layout().addWidget(self.msglabel)
        self.layout().addWidget(self.enterwidget)
        self.resize(self.width(), self.height())

    def enter(self):
        self.accept()  # 关闭对话框并返回1


def msg(text, styleoptions):
    """返回True或False"""
    dialog = MessageDialog(text, styleoptions)
    if dialog.exec_():
        return True
    else:
        return False


if __name__ == '__main__':
    import sys
    app = QtGui.QApplication(sys.argv)
    styleoptions = {
        'title': u'消息提示',
        'windowicon': os.sep.join([os.path.dirname(__file__), 'utildialogskin', 'images', 'bg.jpg']),
        'minsize': (400, 300),
        'size': (400, 300),
        'logo_title': u'智能光纤云终端管理平台',
        'logo_img_url': os.sep.join([os.path.dirname(__file__), 'utildialogskin', 'images', 'bg.jpg'])
    }
    msg('sddsdsdsdssddsds', styleoptions)
    sys.exit(app.exec_())
