#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
from PyQt4 import QtGui
from PyQt4 import QtCore

from basedialog import BaseDialog


class UrlinputDialog(BaseDialog):
    def __init__(self, styleoptions, parent=None):
        super(UrlinputDialog, self).__init__(styleoptions, parent)

        # url内容输入
        self.urlwidget = QtGui.QWidget()
        url_mainlayout = QtGui.QGridLayout()
        self.urlLabel = QtGui.QLabel(u'请输入需要访问的url:')
        self.urlLineEdit = QtGui.QLineEdit(u'http://192.168.10.135:8000/webs/protection_areas/list')
        url_mainlayout.addWidget(self.urlLabel, 0, 0)
        url_mainlayout.addWidget(self.urlLineEdit, 1, 0)
        self.urlwidget.setLayout(url_mainlayout)

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


def urlinput(options):
    dialog = UrlinputDialog(options)
    if dialog.exec_():
        return True, unicode(dialog.urlLineEdit.text())
    else:
        return False, unicode(dialog.urlLineEdit.text())


if __name__ == '__main__':
    import sys
    app = QtGui.QApplication(sys.argv)
    styleoptions = {
        'title': u'退出设置',
        'windowicon': os.sep.join([os.path.dirname(__file__), 'utildialogskin', 'images', 'bg.jpg']),
        'minsize': (400, 300),
        'size': (400, 300),
        'logo_title': u'智能光纤云终端管理平台',
        'logo_img_url': os.sep.join([os.path.dirname(__file__), 'utildialogskin', 'images', 'bg.jpg'])
    }
    print urlinput(styleoptions)
    sys.exit(app.exec_())
