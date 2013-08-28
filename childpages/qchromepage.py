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
from md2html import mdhtmlcomplete

logger = logging.getLogger(__name__)


class QChromePage(WebkitBasePage):
    def __init__(self, parent=None):
        super(QChromePage, self).__init__(parent)
        self.parent = parent

    def refreshcontent(self):
        markdownpageinstance = getattr(self.parent, 'MarkdownPage')
        frame = markdownpageinstance.view.page().mainFrame()
        mdhtml = unicode(frame.evaluateJavaScript("$('#preview').html()").toString())
        htmlfile = os.sep.join([os.getcwd(), 'doc', 'preview.html'])
        mdhtmlcomplete(mdhtml, 'themeblack', htmlfile)
        url = QtCore.QUrl('file:///' + htmlfile)
        self.view.load(url)


if __name__ == '__main__':
    import sys
    app = QtGui.QApplication(sys.argv)
    w = ChromePage()
    w.show()
    sys.exit(app.exec_())
