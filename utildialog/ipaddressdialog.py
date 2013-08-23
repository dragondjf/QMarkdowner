#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
from PyQt4 import QtGui
from PyQt4 import QtCore

from basedialog import BaseDialog


class IPaddressDialog(BaseDialog):
    def __init__(self, styleoptions, parent=None):
        super(IPaddressDialog, self).__init__(styleoptions, parent)

        # url内容输入
        self.urlwidget = QtGui.QWidget()
        ip_mainlayout = QtGui.QGridLayout()
        self.ipLabel = QtGui.QLabel(u'输入主机ip:')
        self.ipLineEdit = QtGui.QLineEdit(u'192.168.100.100')
        self.ipLineEdit.setInputMask('000.000.000.000')
        self.portLabel = QtGui.QLabel(u'输入主机port:')
        self.portLineEdit = QtGui.QLineEdit(u'8000')
        ip_mainlayout.addWidget(self.ipLabel, 0, 0)
        ip_mainlayout.addWidget(self.ipLineEdit, 0, 1)
        ip_mainlayout.addWidget(self.portLabel, 1, 0)
        ip_mainlayout.addWidget(self.portLineEdit, 1, 1)

        self.urlwidget.setLayout(ip_mainlayout)

        #确认按钮布局
        self.enterwidget = QtGui.QWidget()
        self.pbEnter = QtGui.QPushButton(u'确定', self)
        self.pbCancel = QtGui.QPushButton(u'取消', self)
        self.pbEnter.clicked.connect(self.enter)
        self.pbCancel.clicked.connect(self.reject)
        enterwidget_mainlayout = QtGui.QGridLayout()
        enterwidget_mainlayout.addWidget(self.pbEnter, 0, 0)
        enterwidget_mainlayout.addWidget(self.pbCancel, 0, 1)
        self.enterwidget.setLayout(enterwidget_mainlayout)

        self.layout().addWidget(self.urlwidget)
        self.layout().addWidget(self.enterwidget)
        self.resize(self.width(), self.height())

    def enter(self):
        self.accept()  # 关闭对话框并返回1


def ipaddressinput(options):
    dialog = IPaddressDialog(options)
    if dialog.exec_():
        return True, unicode(dialog.ipLineEdit.text()), int(dialog.portLineEdit.text())
    else:
        return False, unicode(dialog.ipLineEdit.text()), int(dialog.portLineEdit.text())


if __name__ == '__main__':
    import sys
    app = QtGui.QApplication(sys.argv)
    styleoptions = {
        'title': u'请输入相应的ip地址和端口号：',
        'windowicon': os.sep.join([os.path.dirname(__file__), 'utildialogskin', 'images', 'bg.jpg']),
        'minsize': (400, 300),
        'size': (400, 300),
        'logo_title': u'智能光纤云终端管理平台',
        'logo_img_url': os.sep.join([os.path.dirname(__file__), 'utildialogskin', 'images', 'bg.jpg'])
    }
    print ipaddressinput(styleoptions)
    sys.exit(app.exec_())
