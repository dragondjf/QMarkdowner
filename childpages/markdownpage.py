#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
from qframer.qt import QtGui
from qframer.qt import QtCore
from qframer.qt import QtNetwork
from qframer.qt import QtWebKit
from Cheetah.Template import Template
import json
import logging
from webkitbasepage import WebkitBasePage

logger = logging.getLogger(__name__)

templateDef_absolute = '''
#encoding utf-8
#set $csspath = $os.sep.join([$os.getcwd(), 'webjscss', 'MaDeEditor', 'css'])
#set $jspath = $os.sep.join([$os.getcwd(), 'webjscss', 'MaDeEditor', 'js'])

#set $preview_css=$os.sep.join([$csspath, 'preview.css'])
#set $style_css=$os.sep.join([$csspath, 'style.css'])


#set $ace_js=$os.sep.join([$jspath, 'ace.js'])
#set $jquery_js=$os.sep.join([$jspath, 'jquery.js'])
#set $made_js=$os.sep.join([$jspath, 'made.js'])
#set $mode_markdown_js=$os.sep.join([$jspath, 'mode-markdown.js'])
#set $Markdown_Converter_js=$os.sep.join([$jspath, 'Markdown.Converter.js'])
#set $theme_textmate_js=$os.sep.join([$jspath, 'theme-textmate.js'])
#set $theme_twilight_js=$os.sep.join([$jspath, 'theme-twilight.js'])

<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en-US" lang="en-US">
    <head>
        <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
        <title>MaDe Editor</title>
        <link href="file:///$preview_css" rel="stylesheet" type="text/css">
        <link href="file:///$style_css" rel="stylesheet" type="text/css">
    </head>
        <body>
        <div id="bar">
            <h1 id="title">Markdown  Tool     <span class="desc">An Editor for markdown</span></h1>
            <div id="control">
                <a href="#" class="button" id="import_button">
                    <span class="label">Import</span>
                </a>
                <input type="file" id="import_file_button">
            </div>
            <div id="color_scheme"><label>Color Scheme</label>
                <a href="dark" id="color_scheme_dark" class="selected"><span></span></a>
                <a href="light" id="color_scheme_light"><span></span></a>
            </div>
        </div>
        <div id="container" style="height: 131px;">
            <div class="pane ace_editor dark ace-twilight" id="input" placeholder="type some markdown code or drag &amp; drop a .md file here" style="font-size: 14px; width: 810px;">
                <div class="ace_gutter">
                    <div class="ace_layer ace_gutter-layer" style="margin-top: -16px; height: 169px;">
                        <div class="ace_gutter-cell " title="" style="height:24px;">128</div>
                        <div class="ace_gutter-cell " title="" style="height:24px;">129</div>
                        <div class="ace_gutter-cell " title="" style="height:24px;">130</div>
                        <div class="ace_gutter-cell " title="" style="height:24px;">131</div>
                        <div class="ace_gutter-cell " title="" style="height:24px;">132</div>
                        <div class="ace_gutter-cell " title="" style="height:24px;">133</div>
                        <div class="ace_gutter-cell " title="" style="height:24px;">134</div>
                    </div>
                </div>
                <div class="ace_scroller dark" style="left: 50px; width: 750px; height: 131px;">
                    <div class="ace_content" style="margin-top: 0px; width: 750px; height: 291px;">
                        <div class="ace_layer ace_marker-layer">
                            <div class="ace_active_line" style="height:24px;width:750px;top:0px;left:0px;"></div>
                        </div>
                        <div class="ace_print_margin_layer">
                            <div class="ace_print_margin" style="left: 648px; visibility: visible;"></div>
                        </div>
                        <div class="ace_layer ace_text-layer" style="width: auto; padding: 0px 4px;">
                            <div class="ace_line_group">
                                <div class="ace_line" style="height:24px">the&nbsp;new&nbsp;text&nbsp;here</div>
                            </div>
                        </div>
                        <div class="ace_layer ace_marker-layer"></div>
                        <div class="ace_layer ace_cursor-layer">
                            <div class="ace_cursor ace_hidden" style="left: 140px; top: 0px; width: 8px; height: 24px; visibility: visible;"></div>
                        </div>
                    </div>
                </div>
                <div class="ace_sb dark" style="width: 15px; height: 121px;">
                    <div style="height: 8040px;"></div>
                </div>
                <textarea style="left: 82px; top: 161px;"></textarea>
            </div>
            <div id="preview_pane" class="pane" style="width: 780px;">
                <div id="preview">
            </div>
            </div>
    </body>
        <script type="text/javascript" src="file:///$jquery_js"></script>
        <script type="text/javascript" src="file:///$made_js"></script>
        <script type="text/javascript" src="file:///$ace_js"></script>
        <script type="text/javascript" src="file:///$mode_markdown_js"></script>
        <script type="text/javascript" src="file:///$theme_textmate_js"></script>
        <script type="text/javascript" src="file:///$theme_twilight_js"></script>
        <script type="text/javascript" src="file:///$Markdown_Converter_js"></script>
</html>
'''

def getfiles(path):
    '''
        获取指定path下的所有文件列表
    '''
    files = []
    for dirpath, dirnames, filenames in os.walk(path):
        for filename in filenames:
            files.append(os.sep.join([dirpath, filename]))
    return files


class MarkdownPage(WebkitBasePage):
    def __init__(self, parent=None):
        super(MarkdownPage, self).__init__(parent)
        self.parent = parent

        jspath = os.sep.join([os.getcwd(), 'webjscss', 'MaDeEditor','js'])
        jsfiles = [
            'jquery.js', 'made.js', 'ace.js', 'mode-markdown.js', 
            'theme-textmate.js', 'theme-twilight.js', 'Markdown.Converter.js']
        self.jsfiles = [os.sep.join([jspath, js]) for js in jsfiles]
        self.jsbuffers = []
        for jsfile in self.jsfiles:
            jsname = '.'.join(os.path.basename(jsfile).split('.')[:-1])
            if os.path.exists(jsfile):
                with open(jsfile, 'rb') as fd:
                    jscontent = fd.read()
                    setattr(self, jsname, jscontent)
                    self.jsbuffers.append(getattr(self, jsname))
                setattr(self, jsname, jscontent)
            else:
                setattr(self, jsname, '')

        # self.view.loadFinished.connect(self.finishLoading)

        self.loadfromlocal()

    # def finishLoading(self):
    #     # for js in self.jsbuffers:
    #     #     self.view.page().mainFrame().evaluateJavaScript(js)
    #     print '14111'

    def auto_html(self, template):
        nameSpace = {
        }
        t = Template(template, searchList=[nameSpace])
        with open(os.sep.join([os.getcwd(), 'webjscss', 'MaDeEditor', 'MaDeEditor.html']), 'wb') as f:
            f.write(str(t))
        return unicode(t)

    def loadfromlocal(self):
        html = self.auto_html(templateDef_absolute)
        url = QtCore.QUrl('file:///' + os.sep.join([os.getcwd(), 'webjscss', 'MaDeEditor', 'MaDeEditor.html']))
        self.view.load(url)
        self.view.setFocus()

if __name__ == '__main__':
    import sys
    app = QtGui.QApplication(sys.argv)
    w = MarkdownPage()
    w.show()
    sys.exit(app.exec_())
