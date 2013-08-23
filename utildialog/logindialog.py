#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
from PyQt4 import QtGui
from PyQt4 import QtCore

from basedialog import BaseDialog


class LoginDialog(BaseDialog):
    def __init__(self, styleoptions, parent=None):
        super(LoginDialog, self).__init__(styleoptions, parent)

        self.login_np = QtGui.QWidget()
        login_np_mainlayout = QtGui.QGridLayout()
        login_nameLabel = QtGui.QLabel(u'用户名')
        self.login_name = QtGui.QLineEdit(self)
        self.login_name.setPlaceholderText(u'用户名')

        login_passwordLabel = QtGui.QLabel(u'密码')
        self.login_password = QtGui.QLineEdit(self)
        self.login_password.setEchoMode(QtGui.QLineEdit.Password)
        self.login_password.setPlaceholderText(u'密码')

        login_np_mainlayout.addWidget(login_nameLabel, 0, 0)
        login_np_mainlayout.addWidget(self.login_name, 0, 1)
        login_np_mainlayout.addWidget(login_passwordLabel, 1, 0)
        login_np_mainlayout.addWidget(self.login_password, 1, 1)
        self.login_np.setLayout(login_np_mainlayout)

        #确认按钮布局
        self.enterwidget = QtGui.QWidget()
        self.pbLogin = QtGui.QPushButton(u'登录', self)
        self.pbCancel = QtGui.QPushButton(u'取消', self)
        self.pbLogin.clicked.connect(self.login)
        self.pbCancel.clicked.connect(self.reject)

        enterwidget_mainlayout = QtGui.QGridLayout()
        enterwidget_mainlayout.addWidget(self.pbLogin, 0, 0)
        enterwidget_mainlayout.addWidget(self.pbCancel, 0, 1)
        self.enterwidget.setLayout(enterwidget_mainlayout)

        self.layout().addWidget(self.login_np)
        self.layout().addWidget(self.enterwidget)
        self.resize(self.width(), self.height())

    def login(self):
        self.accept()  # 关闭对话框并返回1


def login(loginoptions):
    """返回True或False"""
    dialog = LoginDialog(loginoptions)
    if dialog.exec_():
        return True, (unicode(dialog.login_name.text()), unicode(dialog.login_password.text()))
    else:
        return False, (u'', u'')


if __name__ == '__main__':
    import sys
    app = QtGui.QApplication(sys.argv)
    styleoptions = {
        'title': u'登录',
        'windowicon': os.sep.join([os.path.dirname(__file__), 'utildialogskin', 'images', 'bg.jpg']),
        'minsize': (400, 300),
        'size': (400, 300),
        'logo_title': u'智能光纤云终端管理平台',
        'logo_img_url': os.sep.join([os.path.dirname(__file__), 'utildialogskin', 'images', 'bg.jpg'])
    }
    print login(styleoptions)
    sys.exit(app.exec_())
