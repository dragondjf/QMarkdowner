#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
from qframer.qt import QtGui
from qframer.qt import QtCore
import logging

logger = logging.getLogger(__name__)

style = 'QPushButton\
{\
    color: rgb(255, 255, 255);\
    background-color: rgb(167, 205, 255);\
    background: green;\
    border:none;\
    font-family: "Verdana";\
    font-size: 15px;\
    text-align: center;\
    width: 60px; \
}\
QPushButton:hover, QPushButton:pressed , QPushButton:checked\
{\
    background-color: rgb(85, 170, 255);\
    text-align: center;\
}\
QPushButton:hover\
{\
    background-repeat:no-repeat;\
    background-position: center left;\
}\
QPushButton:pressed, QPushButton:checked\
{\
    background-repeat:no-repeat;\
    background-position: center left;\
}\
\
QPushButton:disabled{\
    color: gray;\
    background-color: rgb(167, 205, 255);\
}\
\
QLineEdit {\
    padding: 1px;\
    border-style: solid;\
    border: 2px solid gray;\
    border-radius: 8px;\
    width:40px;\
}'


class BaseDialog(QtGui.QDialog):

    def __init__(self, styleoptions, parent=None):
        super(BaseDialog, self).__init__(parent)
        title = styleoptions['title']
        windowicon = styleoptions['windowicon']
        minsize = styleoptions['minsize']
        size = styleoptions['size']
        logo_title = styleoptions['logo_title']
        logo_img_url = styleoptions['logo_img_url']

        self.setWindowTitle(title)
        self.setWindowIcon(QtGui.QIcon(windowicon))  # 设置程序图标
        self.setMinimumSize(minsize[0], minsize[1])
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)  # 无边框， 带系统菜单， 可以最小化

        self.logowidget = DynamicTextWidget(logo_title, logo_img_url)

        # 主布局
        mainlayout = QtGui.QVBoxLayout()
        mainlayout.addWidget(self.logowidget)
        self.setLayout(mainlayout)
        # logger.info(os.sep.join([os.getcwd(), 'utildialogskin', 'qss', 'dialog.qss']))
        if os.path.isdir(os.sep.join([os.getcwd(), 'utildialogskin'])):
            setskin(self, os.sep.join([os.getcwd(), 'utildialogskin', 'qss', 'dialog.qss']))  # 设置主窗口样式
        elif  os.path.isdir(os.sep.join([os.getcwd(), 'utildialog', 'utildialogskin'])):
            setskin(self, os.sep.join([os.getcwd(), 'utildialog', 'utildialogskin', 'qss', 'dialog.qss']))  # 设置主窗口样式

        # self.setStyleSheet(style) # 设置主窗口样式
        self.resize(size[0], size[1])


class DynamicTextWidget(QtGui.QWidget):
    def __init__(self, text, bg, parent=None):


        super(DynamicTextWidget, self).__init__(parent)

        self.bg = bg
        self.text = text

        newFont = self.font()
        newFont.setPointSize(newFont.pointSize() + 10)
        self.setFont(newFont)

        self.painter = QtGui.QPainter()

        self.timer = QtCore.QBasicTimer()

        self.step = 0
        self.timer.start(60, self)

    def paintEvent(self, event):
        self.painter.begin(self)
        self.drawBackground(self.painter)
        self.drawDynamicText(self.painter)
        self.painter.end()

    def set_painterpencolor(self, painter):
        color = QtGui.QColor()
        import random
        i = random.randint(1, 15)
        color.setHsv((15 - i) * 16, 255, 191)
        painter.setPen(color)

    def drawBackground(self, painter):
        painter.drawPixmap(0, 0, self.width(), self.height(), QtGui.QPixmap(self.bg))

    def drawDynamicText(self, painter):
        sineTable = (0, 38, 71, 92, 100, 92, 71, 38, 0, -38, -71, -92, -100, -92, -71, -38)
        metrics = QtGui.QFontMetrics(self.font())
        x = (self.width() - metrics.width(self.text)) / 2
        y = (self.height() + metrics.ascent() - metrics.descent()) / 2
        color = QtGui.QColor()

        for i, ch in enumerate(self.text):
            index = (self.step + i) % 16
            color.setHsv((15 - index) * 16, 255, 191)
            painter.setPen(color)
            painter.drawText(x, y - ((sineTable[index] * metrics.height()) / 400), ch)
            x += metrics.width(ch)

    def setText(self, newText):
        self.text = newText

    def setspreed(self, spreed):
        self.spreed = spreed
        self.timer.stop()
        self.timer.start(self.spreed, self)

    def timerEvent(self, event):
        if self.text:
            if event.timerId() == self.timer.timerId():
                self.step += 1
                self.update()
            else:
                super(DynamicTextWidget, self).timerEvent(event)
        else:
            self.timer.stop()


class BaseDialog2(QtGui.QDialog):

    def __init__(self, styleoptions, parent=None):
        super(BaseDialog2, self).__init__(parent)
        title = styleoptions['title']
        windowicon = styleoptions['windowicon']
        minsize = styleoptions['minsize']
        size = styleoptions['size']
        logo_title = styleoptions['logo_title']
        logo_img_url = styleoptions['logo_img_url']

        self.setWindowTitle(title)
        self.setWindowIcon(QtGui.QIcon(windowicon))  # 设置程序图标
        self.setMinimumSize(minsize[0], minsize[1])
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowSystemMenuHint | QtCore.Qt.WindowMinimizeButtonHint)  # 无边框， 带系统菜单， 可以最小化

        # logo显示
        self.logowidget = QtGui.QWidget()
        logo_mainlayout = QtGui.QGridLayout()
        bg = QtGui.QLabel(logo_title)
        bg.setAlignment(QtCore.Qt.AlignCenter)
        logo_mainlayout.addWidget(bg)
        self.logowidget.setLayout(logo_mainlayout)
        self.bg = logo_img_url
        setbg(self.logowidget, self.bg)

        # 主布局
        mainlayout = QtGui.QVBoxLayout()
        mainlayout.addWidget(self.logowidget)
        self.setLayout(mainlayout)
        # setskin(self, os.sep.join([__file__.split('utildialog')[0], 'utildialogskin', 'qss', 'dialog.qss']))  # 设置主窗口样式
        setskin(self, 'D:\GitHub\QSoftKeyer\utildialogskin\qss\dialog.qss')
        self.resize(size[0], size[1])

    def resizeEvent(self, event):
        if hasattr(self, 'bg'):
            setbg(self.logowidget, self.bg)


def setbg(widget, filename):
    widget.setAutoFillBackground(True)
    palette = QtGui.QPalette()
    pixmap = QtGui.QPixmap(filename)
    pixmap = pixmap.scaled(widget.size())
    palette.setBrush(QtGui.QPalette.Background, QtGui.QBrush(pixmap))
    widget.setPalette(palette)


def setskin(app, qssfile, style=''):
    with open(qssfile, 'r') as f:
        app.setStyleSheet(f.read() + style)

if __name__ == '__main__':
    import sys
    app = QtGui.QApplication(sys.argv)
    styleoptions = {
        'title': u'退出设置',
        'windowicon': os.sep.join([os.path.dirname(__file__), 'utildialogskin', 'images', 'bg.jpg']),
        'minsize': (400, 300),
        'size': (400, 300),
        'logo_title': u'dssssssss',
        'logo_img_url': os.sep.join([os.path.dirname(__file__), 'utildialogskin', 'images', 'bg.jpg'])
    }
    dialog = BaseDialog(styleoptions)
    dialog.show()
    sys.exit(app.exec_())
