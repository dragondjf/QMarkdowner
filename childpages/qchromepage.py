#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
from PyQt4 import QtGui
from PyQt4 import QtCore
from PyQt4 import QtWebKit
from Cheetah.Template import Template
import json
import logging
from webkitbasepage import WebkitBasePage
from md2html import md2html

logger = logging.getLogger(__name__)


class QChromePage(WebkitBasePage):
    def __init__(self, parent=None):
        super(QChromePage, self).__init__(parent)
        self.parent = parent

        markdownpageinstance = getattr(self.parent, 'MarkdownPage') 
        print markdownpageinstance.view.page().mainFrame().documentElement().findAll('div').count()
        self.loadfromlocal()

    # def auto_html(self, template):
    #     nameSpace = {
    #     }
    #     t = Template(template, searchList=[nameSpace])
    #     with open(os.sep.join([os.getcwd(), 'md2html', 'MaDeEditor', 'MaDeEditor.html']), 'wb') as f:
    #         f.write(str(t))
    #     return unicode(t)

    def loadfromlocal(self):
        pass
        # md2html(mdfile, htmlfile, theme)
        # html = self.auto_html(templateDef_absolute)
        # url = QtCore.QUrl('file:///' + os.sep.join([os.getcwd(), 'md2html', 'MaDeEditor', 'MaDeEditor.html']))
        # self.view.load(url)
        # self.view.setFocus()



if __name__ == '__main__':
    import sys
    app = QtGui.QApplication(sys.argv)
    w = ChromePage()
    w.show()
    sys.exit(app.exec_())
