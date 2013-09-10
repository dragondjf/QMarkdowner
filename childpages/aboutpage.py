#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
from PyQt4 import QtGui
from PyQt4 import QtCore
from PyQt4 import QtNetwork
from PyQt4 import QtWebKit
from Cheetah.Template import Template
import json
import logging
from webkitbasepage import WebkitBasePage

logger = logging.getLogger(__name__)

templateDef_absolute = '''
#encoding utf-8
#set baseweb = $os.sep.join([$os.getcwd(), 'webjscss'])
#set $csspath = $os.sep.join([$os.getcwd(), 'webjscss', 'Bootstrap Metro UI CSS'])
#set $jspath = $os.sep.join([$os.getcwd(), 'webjscss', 'Bootstrap Metro UI CSS', 'js'])
#set $imagepath = $os.sep.join([$os.getcwd(), 'skin', 'images'])
#set $helpimagepath = $os.sep.join([$os.getcwd(), 'skin', 'images', 'help'])

#set $modern_css=$os.sep.join([$csspath, 'modern.css'])
#set $modern_responsive_css=$os.sep.join([$csspath, 'modern-responsive.css'])
#set $site_css=$os.sep.join([$csspath, 'site.css'])
#set $prettify_css=$os.sep.join([$csspath, 'prettify.css'])

#set $accordion_js=$os.sep.join([$jspath, 'accordion.js'])
#set $buttonset_js=$os.sep.join([$jspath, 'buttonset.js'])
#set $calendar_js=$os.sep.join([$jspath, 'calendar.js'])
#set $carousel_js=$os.sep.join([$jspath, 'carousel.js'])
#set $dropdown_js=$os.sep.join([$jspath, 'dropdown.js'])
#set $input_control_js=$os.sep.join([$jspath, 'input-control.js'])
#set $jquery_190_min_js=$os.sep.join([$jspath, 'jquery-1.9.0.min.js'])
#set $jquery_mousewheel_min_js=$os.sep.join([$jspath, 'jquery.mousewheel.min.js'])
#set $jquery_sharrre_134_min_js=$os.sep.join([$jspath, 'jquery.sharrre-1.3.4.min.js'])
#set $moment_js=$os.sep.join([$jspath, 'moment.js'])
#set $moment_langs_js=$os.sep.join([$jspath, 'moment_langs.js'])
#set $prettify_js=$os.sep.join([$jspath, 'prettify.js'])
#set $pagecontrol_js=$os.sep.join([$jspath, 'pagecontrol.js'])
#set $rating_js=$os.sep.join([$jspath, 'rating.js'])
#set $slider_js=$os.sep.join([$jspath, 'slider.js'])
#set $tile_drag_js=$os.sep.join([$jspath, 'tile-drag.js'])
#set $tile_slider_js=$os.sep.join([$jspath, 'tile-slider.js'])

#set $pdfobject_js=$os.sep.join([$baseweb, 'pdfobject','pdfobject.js'])

#set $company_image = $os.sep.join([$imagepath, 'compayimage.jpg'])
#set $onevo_image = $os.sep.join([$imagepath, 'onevo.jpg'])
#set $onevo1_image = $os.sep.join([$imagepath, 'onevo1.jpg'])
#set $onevo2_image = $os.sep.join([$imagepath, 'onevo2.jpg'])
#set $onevo3_image = $os.sep.join([$imagepath, 'onevo3.jpg'])

<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/html"><head><meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
    <meta charset="utf-8">
    <meta name="viewport" content="target-densitydpi=device-dpi, width=device-width, initial-scale=1.0, maximum-scale=1">
    <meta name="description" content="Metro UI CSS Alarm List">
    <meta name="author" content="dragondjf@gamil.com">
    <meta name="keywords" content="windows 8, modern style, Bootstrap,Metro UI, style, modern, css, framework">

    <link href="file:///$modern_css" rel="stylesheet" type="text/css">
    <link href="file:///$modern_responsive_css" rel="stylesheet" type="text/css">
    <link href="file:///$site_css" rel="stylesheet" type="text/css">
    <link href="file:///$prettify_css" rel="stylesheet" type="text/css">
    <script type="text/javascript" src="file:///$jquery_190_min_js"></script>
    <script type="text/javascript" src="file:///$jquery_mousewheel_min_js"></script>
    <script type="text/javascript" src="file:///$jquery_sharrre_134_min_js"></script>
    <script type="text/javascript" src="file:///$accordion_js"></script>
    <script type="text/javascript" src="file:///$buttonset_js"></script>
    <script type="text/javascript" src="file:///$calendar_js"></script>
    <script type="text/javascript" src="file:///$carousel_js"></script>
    <script type="text/javascript" src="file:///$dropdown_js"></script>
    <script type="text/javascript" src="file:///$moment_js"></script>
    <script type="text/javascript" src="file:///$moment_langs_js"></script>
    <script type="text/javascript" src="file:///$pagecontrol_js"></script>
    <script type="text/javascript" src="file:///$prettify_js"></script>
    <script type="text/javascript" src="file:///$rating_js"></script>
    <script type="text/javascript" src="file:///$slider_js"></script>
    <script type="text/javascript" src="file:///$tile_drag_js"></script>
    <script type="text/javascript" src="file:///$tile_slider_js"></script>
    <script type="text/javascript" src="file:///$pdfobject_js"></script>

    <script type="text/javascript">
        window.onload = function (){
            var success = new PDFObject({ url: "MarkDown.pdf" }).embed("pdf");
        };
    </script>
    <title>$title</title>
    <body class="modern-ui" onload="prettyPrint()">
        <div class="page secondary" style="width: 100%">
            <div class="page-region">
                    <div class="page-region-content">
                        <div class="page-control span10" data-role="page-control" style="width: 92%">
                            <ul style="display: block; overflow: visible;">
                                <li class="active"><a href="#page1">$help_info</a></li>
                                <li class=><a href="#page2">$soft_info</a></li>
                                <li class=""><a href="#page3">$company_info</a></li>
                            </ul>
                            <div class="frames">
                                <div class="frame" id="page1" style="display: none;">
                                    <object data="file:///MarkDown.pdf" type="application/x-pdf" width="100%" height="100%">
                                        <param name="showTableOfContents" value="true" />
                                        <param name="hideThumbnails" value="false" />
                                    </object>
                                </div>
                                <div class="frame" id="page2" style="display: none;">
                                    <h2>$soft_info</h2>
                                    <p>软件版本号：$sw_info</p>
                                    <p>版权所有：dragondjf</p>
                                </div>
                                <div class="frame" id="page3" style="display: none;">
                                    <h2>$company_info</h2>
                                    <p>联系邮箱：dragondjf@gmail.com, ding465398889@163.com</p>
                                    <p>联系QQ：465398889</p>
                                    <p>GitHub地址：https://github.com/dragondjf/</p>
                                    <p>感谢：Chrome插件MaDe作者Lyric Wai，ulipad和uliweb作者limodou, Good朋友jack_zh, PyQt and PySide群里的樱桃大丸子等大神.</p>
                                    <p>致敬：感谢开源精神，分享成就自我！</p>
                                </div>
                            </div>
                        </div>
                    </div>
                <iframe id="tmp_downloadhelper_iframe" style="display: none;"></iframe>
            </div>
        </div>
    </body>
</html>'''


class AboutPage(WebkitBasePage):
    def __init__(self, parent=None):
        super(AboutPage, self).__init__(parent)
        self.parent = parent
        self.view.page().settings().setAttribute(QtWebKit.QWebSettings.PluginsEnabled, True)
        self.loadfromlocal()

    def auto_html(self, template):
        verfilepath = os.sep.join([os.getcwd(), 'options', 'ver.json'])
        try:
            with open(verfilepath, 'r') as f:
                info = json.load(f)
                sw_info = '-'.join([info['sw_name'], info['sw_version'], info['svn_version'], info['buildtime']])
        except Exception, e:
            logger.error(e)
            info = {
               "sw_name": "QDConfiger", 
               "sw_version": "v1.0", 
               "svn_version": "r100",
               "buildtime": "b20130725"
            }
            sw_info = '-'.join([info['sw_name'], info['sw_version'], info['svn_version'], info['buildtime']])
        nameSpace = {
            'title': "关于",
            'funtion_info': "软件基本功能",
            'soft_info': '软件版本说明',
            'company_info': '关于我们',
            'help_info': 'MarkDown语法简介',
            'sw_info': sw_info,
            'imagewidth': QtGui.QDesktopWidget().availableGeometry().width()* 3 / 5,
            'imageheight': QtGui.QDesktopWidget().availableGeometry().width() * 27 / 80,
        }
        t = Template(template, searchList=[nameSpace])
        html = unicode(t)
        return html

    def loadfromlocal(self):
        html = self.auto_html(templateDef_absolute)
        self.view.setHtml(html, QtCore.QUrl(os.getcwd()))

if __name__ == '__main__':
    import sys
    app = QtGui.QApplication(sys.argv)
    w = AboutPage()
    w.show()
    sys.exit(app.exec_())
