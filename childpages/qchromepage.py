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
from config import windowsoptions

logger = logging.getLogger(__name__)


class QChromePage(WebkitBasePage):
    def __init__(self, parent=None):
        super(QChromePage, self).__init__(parent)
        self.parent = parent

        self.createcontrolbar()
        self.layout().insertWidget(0, self.controlbar)
        self.view.page().mainFrame().setScrollBarPolicy(QtCore.Qt.Horizontal,QtCore.Qt.ScrollBarAlwaysOff)
        self.view.loadFinished.connect(self.finishLoading)

    def refreshcontent(self):
        markdownpageinstance = getattr(self.parent, 'MarkdownPage')
        frame = markdownpageinstance.view.page().mainFrame()
        mdhtml = unicode(frame.evaluateJavaScript("$('#preview').html()").toString())
        if not os.path.exists(os.sep.join([os.getcwd(), 'doc'])):
            os.mkdir(os.sep.join([os.getcwd(), 'doc']))
        htmlfile = os.sep.join([os.getcwd(), 'doc', 'preview.html'])
        self.theme = "evernote"
        self.html = mdhtmlcomplete(mdhtml, windowsoptions['markdownthemes']['theme%s' % self.theme], htmlfile, 'templateDef_evernote')
        url = QtCore.QUrl('file:///' + htmlfile)
        self.view.load(url)

    def finishLoading(self):
        pass

    def createcontrolbar(self):
        self.controlbar = QtGui.QWidget()
        controlbar_layout = QtGui.QGridLayout()

        self.pageLabel = QtGui.QLabel()
        exportmarkdownButton = QtGui.QPushButton(u'导出md')
        exportmarkdownButton.setObjectName('ExpmarkdownButton')
        exportmarkdownButton.setToolTip(u'导出md')
        self.exportmarkdownButton = exportmarkdownButton

        exporthtmlButton = QtGui.QPushButton(u'导出HTML')
        exporthtmlButton.setObjectName('ExphtmlButton')
        exporthtmlButton.setToolTip(u'导出')
        self.exporthtmlButton = exporthtmlButton

        exportpdfButton = QtGui.QPushButton(u'导出PDF')
        exportpdfButton.setObjectName('ExppdfButton')
        exportpdfButton.setToolTip(u'导出PDF')
        self.exportpdfButton = exportpdfButton

        n = 15
        blank1 = 3
        blank2 = 3
        for i in xrange(blank1):
            controlbar_layout.addWidget(QtGui.QLabel(), 0, i)

        themes = [ item[5:] for item in windowsoptions['markdownthemes']['themes']]
        for item in themes:
            button = 'Theme%sButton' % item
            setattr(self, button, QtGui.QPushButton(item))
            getattr(self, button).setObjectName(button)
            controlbar_layout.addWidget(getattr(self, button), 0, themes.index(item) + blank1)
            getattr(self, button).clicked.connect(self.settheme)

        for i in xrange(len(themes) + blank1, len(themes) + blank1 + blank2):
            controlbar_layout.addWidget(QtGui.QLabel(), 0, i)
        controlbar_layout.addWidget(exportmarkdownButton, 0, n-4)
        controlbar_layout.addWidget(exporthtmlButton, 0, n-3)
        controlbar_layout.addWidget(exportpdfButton, 0, n-2)
        controlbar_layout.addWidget(QtGui.QLabel(), 0, n)
        self.controlbar.setLayout(controlbar_layout)
        controlbar_layout.setContentsMargins(0, 0, 0, 0)
        self.controlbar.setMaximumHeight(50)

        exportmarkdownButton.clicked.connect(self.exportmarkdown)
        exporthtmlButton.clicked.connect(self.exporthtml)
        exportpdfButton.clicked.connect(self.exportpdf)


    def settheme(self):
        theme = self.sender().objectName()[5:-6]
        self.theme = theme 
        markdownpageinstance = getattr(self.parent, 'MarkdownPage')
        frame = markdownpageinstance.view.page().mainFrame()
        mdhtml = unicode(frame.evaluateJavaScript("$('#preview').html()").toString())
        if theme == "evernote":
            self.html = mdhtmlcomplete(mdhtml, windowsoptions['markdownthemes']['themeevernote'], template='templateDef_evernote')
        elif theme == "jeklyy":
            self.html = mdhtmlcomplete(mdhtml, windowsoptions['markdownthemes']['themejeklyy'], template='templateDef_jeklyy')
        else:
            self.html = mdhtmlcomplete(mdhtml, windowsoptions['markdownthemes']['theme%s'%theme])
        self.view.setHtml(self.html, QtCore.QUrl(os.getcwd()))

    def exportmarkdown(self):
        filename = QtGui.QFileDialog.getSaveFileName(self, u"另存为html文件", u'preview', "file(*.md)")
        import sys
        reload(sys)
        sys.setdefaultencoding('utf-8')
        if filename:
            markdownpageinstance = getattr(self.parent, 'MarkdownPage')
            frame = markdownpageinstance.view.page().mainFrame()
            md = unicode(frame.evaluateJavaScript("editor.getSession().getValue()").toString())
            with open(str(filename), 'wb') as f:
                f.write(str(md))

    def exporthtml(self):
        filename = QtGui.QFileDialog.getSaveFileName(self, u"另存为html文件", u'preview', "file(*.html)")
        import sys
        reload(sys)
        sys.setdefaultencoding('utf-8')
        if filename:
            with open(str(filename), 'wb') as f:
                f.write(str(self.html))

    def exportpdf(self):
        filename = QtGui.QFileDialog.getSaveFileName(self, u"另存为PDF文件", u'preview', "file(*.pdf)")
        import sys
        reload(sys)
        sys.setdefaultencoding('utf-8')
        pdfengine = os.sep.join([os.getcwd(), "dependtool", "wkhtmltopdf", "wkhtmltopdf.exe"])
        htmlfile = os.sep.join([os.getcwd(), 'doc', 'preview.html'])
        if filename:
            if self.theme == "evernote":
                pdfhtml = self.html
                pdfhtml = pdfhtml.replace('''<body class="wrapper" style="background: rgb(222,222,222)">
        <br>''','''<body class="wrapper" style="background: rgb(222,222,222)">''')
                pdfhtml = pdfhtml.replace('''<div id="container" class="wrapper">''',
                    '''<div id="container" class="wrapper" style="width: 100%;margin-left:0px">''')
                with open(str(htmlfile), 'wb') as f:
                    f.write(str(pdfhtml))
            elif self.theme == "jeklyy":
                markdownpageinstance = getattr(self.parent, 'MarkdownPage')
                frame = markdownpageinstance.view.page().mainFrame()
                mdhtml = unicode(frame.evaluateJavaScript("$('#preview').html()").toString())
                pdfcss = os.sep.join([os.getcwd(), 'webjscss', 'themecss', 'jeklyy', 'themejeklyypdf.css'])
                pdfhtml = mdhtmlcomplete(mdhtml, [pdfcss], template='templateDef_jeklyy')
                with open(str(htmlfile), 'wb') as f:
                    f.write(str(pdfhtml))
            else:
                pdfhtml = self.html
                with open(str(htmlfile), 'wb') as f:
                    f.write(str(pdfhtml))
            os.system("%s %s %s" %(pdfengine, htmlfile, filename))

if __name__ == '__main__':
    import sys
    app = QtGui.QApplication(sys.argv)
    w = ChromePage()
    w.show()
    sys.exit(app.exec_())
