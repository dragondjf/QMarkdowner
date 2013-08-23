#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import os
from PyQt4 import QtGui
from PyQt4 import QtCore


'''
1：不要在顶层窗口（无父类的窗口）中使用setStyleSheet() ，否则其一父窗口的背景不会改变，
    其次其子窗口的背景设置方法变得局限唯一，不能再使用其它方法！
2：如果一个一般窗口（非顶层窗口）还有子窗口，那最好不要使用setStyleSheet()来设置其背景颜色，
    因为虽然此时该窗口的背景设置是生效的，但是其子窗口的背景设置也变得局限唯一，只能使用setStyleSheet，而不能使用其它方法！
    当然：你如果就是只想使用这种方法，那也完全可以！！


说白了就是：不要再MainWindow中使用setStyleSheet()！
    而上边之所以强调拓宽子窗口设置背景的方法范围，这是
    因为：如果只能用setStyleSheet样式表来设置背景图片的话，
    该图片是无法缩放的，如果其大小与widget窗口大小不相符，则我们无法用程序来实现图片的缩放，
    除非我们直接处理图片使其大小与widget窗口相符； 而如果不局限于用setStyleSheet样式表来设置的话，
    我们可以选择用QPalette调色版，其内部setBrush()之前，我们完全可以先对图片进行scale缩放再刷到窗口上，
    这样就避免直接去处理图片，灵活性强一点！
==========================================================================
'''


def set_bg(widget, bg=None):
    '''
        设置背景颜色或者图片
    '''
    if bg is None:
        bg = QtGui.QColor('#ABABAB')
    palette = QtGui.QPalette(widget)
    palette.setBrush(widget.backgroundRole(), QtGui.QBrush(bg))
    widget.setPalette(palette)
    setattr(widget, 'bg', bg)


def set_skin(QApplication, qssfile, style=''):
    qss = QtCore.QFile(qssfile)
    qss.open(QtCore.QIODevice.ReadOnly)
    if qss.isOpen():
        QApplication.setStyleSheet(QtCore.QVariant(qss.readAll()).toString() + style)
    qss.close()


def movecenter(w):
    qr = w.frameGeometry()
    cp = QtGui.QDesktopWidget().availableGeometry().center()
    qr.moveCenter(cp)
    w.move(qr.topLeft())


class QMessageBox(QtGui.QDialog):

    def __init__(self, parent=None):
        super(QMessageBox, self).__init__(parent)
        self.setObjectName('QMessageBox')
        self.setGeometry(300, 300, 400, 200)
        self.center()
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowSystemMenuHint | QtCore.Qt.WindowMinimizeButtonHint)  # 无边框， 带系统菜单， 可以最小化
        set_skin(self, os.sep.join(['skin', 'qss', 'MetroDialog.qss']))  # 设置弹出框样式
        self.setWindowIcon(QtGui.QIcon('icons/Write.png'))
        self.setModal(True)

    def center(self):
        qr = self.frameGeometry()
        cp = QtGui.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def information(self, info):
        infoButton = QtGui.QPushButton('info')
        infoButton.setObjectName('Info' + 'Button')
        info = QtGui.QTextEdit(info)
        info.setReadOnly(True)
        mainLayout = QtGui.QVBoxLayout()
        mainLayout.addWidget(infoButton)
        mainLayout.addWidget(info)
        # mainLayout.addStretch(4)
        infoButton.clicked.connect(self.clickReturn)
        self.setLayout(mainLayout)
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.exec_()

    def clickReturn(self):
        self.close()


class QInputDialog(QtGui.QDialog):

    def __init__(self, parent=None):
        super(QInputDialog, self).__init__(parent)
        self.setObjectName('QInputDialog')
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowSystemMenuHint | QtCore.Qt.WindowMinimizeButtonHint)  # 无边框， 带系统菜单， 可以最小化
        set_skin(self, os.sep.join(['skin', 'qss', 'MetroDialog.qss']))  # 设置弹出框样式
        self.setWindowIcon(QtGui.QIcon('icons/Write.png'))
        self.setModal(True)
        self.setGeometry(500, 600, 400, 100)
        self.createNavigation()

    def createNavigation(self):
        buttons = ['Ok', 'Cancel']
        self.navigation = QtGui.QWidget()
        navigationLayout = QtGui.QHBoxLayout()
        for item in buttons:
            button = item + 'Button'
            setattr(self, button, QtGui.QPushButton(item))
            getattr(self, button).setObjectName(button)
            navigationLayout.addWidget(getattr(self, button))
        self.navigation.setLayout(navigationLayout)
        # self.navigation.setMaximumHeight(10)
        self.navigation.setContentsMargins(0, 0, 0, 0)

        getattr(self, 'Cancel' + 'Button').clicked.connect(self.clickReturn)
        getattr(self, 'Ok' + 'Button').clicked.connect(self.clickReturn)

    def getInteger(self, title, intLabel, value, minvalue=-2147483647, maxvalue=2147483647, step=1):
        titleLabel = QtGui.QLabel(title)
        intLabel = QtGui.QLabel(intLabel)
        intValue = QtGui.QSpinBox()
        intValue.setMaximum(maxvalue)
        intValue.setValue(value)
        intValue.setMinimum(minvalue)
        intValue.setSingleStep(step)
        intValue.lineEdit().setReadOnly(False)

        intwidget = QtGui.QWidget()
        Layout = QtGui.QGridLayout()
        Layout.addWidget(titleLabel, 0, 0)
        Layout.addWidget(intLabel, 1, 0)
        Layout.addWidget(intValue, 1, 1)
        intwidget.setLayout(Layout)

        mainLayout = QtGui.QVBoxLayout()
        mainLayout.addWidget(intwidget)
        mainLayout.addWidget(self.navigation)
        self.setLayout(mainLayout)
        self.layout().setContentsMargins(0, 0, 0, 0)
        mainLayout.addStretch(1)

        self.intValue = intValue
        self.value = self.intValue.value()
        self.flag = False

        movecenter(self)
        self.exec_()
        return self.intValue.value(), self.flag

    def getDouble(self, title, doubleLabel, value, minvalue=-2147483647, maxvalue=2147483647, step=1.0, decimals=5):
        titleLabel = QtGui.QLabel(title)
        doubleLabel = QtGui.QLabel(doubleLabel)
        doubleValue = QtGui.QDoubleSpinBox()
        doubleValue.setMaximum(maxvalue)
        doubleValue.setValue(value)
        doubleValue.setMinimum(minvalue)
        doubleValue.setSingleStep(step)
        doubleValue.setDecimals(decimals)
        doubleValue.lineEdit().setReadOnly(False)

        doublewidget = QtGui.QWidget()
        Layout = QtGui.QGridLayout()
        Layout.addWidget(titleLabel, 0, 0)
        Layout.addWidget(doubleLabel, 1, 0)
        Layout.addWidget(doubleValue, 1, 1)
        doublewidget.setLayout(Layout)

        mainLayout = QtGui.QVBoxLayout()
        mainLayout.addWidget(doublewidget)
        mainLayout.addWidget(self.navigation)
        self.setLayout(mainLayout)
        self.layout().setContentsMargins(0, 0, 0, 0)
        mainLayout.addStretch(1)

        self.doubleValue = doubleValue
        self.exec_()
        return self.doubleValue.value(), self.flag

    def getText(self, title, textLabel, text, mode=QtGui.QLineEdit.Normal):
        titleLabel = QtGui.QLabel(title)
        textLabel = QtGui.QLabel(textLabel)
        textValue = QtGui.QLineEdit(text)
        textValue.setEchoMode(mode)

        textwidget = QtGui.QWidget()
        Layout = QtGui.QGridLayout()
        Layout.addWidget(titleLabel, 0, 0)
        Layout.addWidget(textLabel, 1, 0)
        Layout.addWidget(textValue, 1, 1)
        textwidget.setLayout(Layout)

        mainLayout = QtGui.QVBoxLayout()
        mainLayout.addWidget(textwidget)
        mainLayout.addWidget(self.navigation)
        self.setLayout(mainLayout)
        self.layout().setContentsMargins(0, 0, 0, 0)
        mainLayout.addStretch(1)

        self.textValue = textValue
        self.exec_()
        return unicode(self.textValue.text()), self.flag

    def getItem(self, title, itemLabel, items, index, editable=True):
        titleLabel = QtGui.QLabel(title)
        itemLabel = QtGui.QLabel(itemLabel)
        itemValue = QtGui.QComboBox()
        for item in items:
            itemValue.addItem(item)
        itemValue.setCurrentIndex(0)
        itemValue.setEditable(editable)

        itemwidget = QtGui.QWidget()
        Layout = QtGui.QGridLayout()
        Layout.addWidget(titleLabel, 0, 0)
        Layout.addWidget(itemLabel, 1, 0)
        Layout.addWidget(itemValue, 1, 1)
        itemwidget.setLayout(Layout)

        mainLayout = QtGui.QVBoxLayout()
        mainLayout.addWidget(itemwidget)
        mainLayout.addWidget(self.navigation)
        self.setLayout(mainLayout)
        self.layout().setContentsMargins(0, 0, 0, 0)
        mainLayout.addStretch(1)

        self.itemValue = itemValue
        self.exec_()
        return unicode(self.itemValue.currentText()), self.flag

    def clickReturn(self):
        self.close()
        if self.sender() is getattr(self, 'Ok' + 'Button'):
            self.flag = True
        elif self.sender() is getattr(self, 'Cancel' + 'Button'):
            self.flag = False
