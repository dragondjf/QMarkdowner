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
#set $csspath = $os.sep.join([$os.getcwd(), 'Bootstrap Metro UI CSS'])
#set $jspath = $os.sep.join([$os.getcwd(), 'Bootstrap Metro UI CSS', 'js'])
#set $imagepath = $os.sep.join([$os.getcwd(), 'skin', 'images'])
#set $helpimagepath = $os.sep.join([$os.getcwd(), 'skin', 'images', 'help'])

#set $modern_css=$os.sep.join([$csspath, 'modern.css'])
#set $modern_responsive_css=$os.sep.join([$csspath, 'modern-responsive.css'])
#set $site_css=$os.sep.join([$csspath, 'site.css'])
#set $prettify_css=$os.sep.join([$csspath, 'prettify.css'])

#set $accordion_js=$os.sep.join([$jspath, 'accordion_js'])
#set $button_js=$os.sep.join([$jspath, 'button.js'])
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
    <script type="text/javascript" src="file:///$accordion_js"></script>
    <script type="text/javascript" src="file:///$button_js"></script>
    <script type="text/javascript" src="file:///$calendar_js"></script>
    <script type="text/javascript" src="file:///$carousel_js"></script>
    <script type="text/javascript" src="file:///$dropdown_js"></script>
    <script type="text/javascript" src="file:///$jquery_190_min_js"></script>
    <script type="text/javascript" src="file:///$jquery_mousewheel_min_js"></script>
    <script type="text/javascript" src="file:///$jquery_sharrre_134_min_js"></script>
    <script type="text/javascript" src="file:///$moment_js"></script>
    <script type="text/javascript" src="file:///$moment_langs_js"></script>
    <script type="text/javascript" src="file:///$pagecontrol_js"></script>
    <script type="text/javascript" src="file:///$prettify_js"></script>
    <script type="text/javascript" src="file:///$rating_js"></script>
    <script type="text/javascript" src="file:///$slider_js"></script>
    <script type="text/javascript" src="file:///$tile_drag_js"></script>
    <script type="text/javascript" src="file:///$tile_slider_js"></script>
    <title>$title</title>
    <body class="modern-ui" onload="prettyPrint()">
        <div class="page secondary" style="width: 100%">
            <div class="page-region">
                    <div class="page-region-content">
                        <div class="page-control span10" data-role="page-control" style="width: 92%">
                            <ul style="display: block; overflow: visible;">
                                <li class="active"><a href="#page1">$soft_info</a></li>
                                <li class=""><a href="#page2">$company_info</a></li>
                            </ul>
                            <div class="frames">
                                <div class="frame" id="page1" style="display: none;">
                                    <h2>$soft_info</h2>
                                    <p>软件版本号：$sw_info</p>
                                    <p>版权所有：武汉光谷奥源科技股份有限公司</p>
                                </div>
                                <div class="frame" id="page2" style="display: none;">
                                    <h2>$company_info</h2>
                                    <div class="about">
                                        <div align="center"><img src="file:///$company_image" onload="javascript:DrawImage(this);" style="border:none" width="586" height="229" alt="1024×401"></div><p style="text-indent:2em;">
                                        &nbsp;
                                        </p><p style="text-indent:2em;">
                                            武汉光谷奥源科技股份有限公司（简称“光谷奥源”），位于中国光谷，拥有光纤传感、光纤接入系统和测试核心技术及业界领军人物，荣获国家技术发明奖和日内瓦国际发明金奖，致力于成为下一代<img style="width:50px;height:17px;" height="21" alt="" src="file:///$onevo_image" width="64">解决方案领先厂商。目前涵盖物联网、三网融合和下一代互联网接入领域系列高科技产品系统及软件，广泛应用于电信宽带、专网通讯、智能电网、智能交通、安防监控、煤炭石化等众多行业领域。公司拥有专家级的技术队伍和资深的管理团队，在研发、营销、生产服务和供应链方面积累了多年的运营经验，具备实力雄厚的技术开发、产品实现和解决方案提供能力。
                                        </p>
                                        <p style="text-indent:2em;">
                                            光谷奥源依托华中科技大学的科研技术优势和奥信集团的金融资本优势，实施资源整合和战略合作，是国家级技术创新平台—“下一代互联网接入系统国家工程实验室”的战略联盟单位，并斥资千万在华中科技大学设立“光谷奥源联合实验室”，本着“高科技、高起点、高标准”的定位原则，致力于发展物联网、三网融合和下一代互联网领域的创新技术产品并实施产业化。
                                        </p>
                                        <p style="text-indent:2em;">
                                            光谷奥源目前主要的战略产品和解决方案服务包括：
                                        </p>
                                        <p style="text-indent:2em;">
                                            &nbsp;
                                        </p>
                                        <p style="text-indent:2em;">
                                            <strong><img height="15" alt="" src="file:///$onevo1_image" width="53">&nbsp;光传感产品</strong>——智能光纤振动传感周界产品及解决方案、安防系统集成及服务；
                                        </p>
                                        <p style="text-indent:2em;">
                                            <strong><img height="15" alt="" src="file:///$onevo2_image" width="53">&nbsp;光测试产品</strong>——光通信网络测试和监控产品及解决方案、测试系统集成及服务；
                                        </p>
                                        <p style="text-indent:2em;">
                                            <strong><img height="15" alt="" src="file:///$onevo3_image" width="53">&nbsp;光接入产品</strong>——专网工业无源光网络接入产品、网络系统集成及服务；
                                        </p>
                                        <p style="text-indent:2em;">
                                            &nbsp;
                                        </p>
                                        <p style="text-indent:2em;">
                                            创新是光谷奥源不断推出业界领先产品和服务的核心保障，唯有坚持不停息的技术创新，并和客户分享成功的产品和解决方案，成就客户价值，才能实现公司的价值回报。通过和华中科技大学的战略合作及不断引进先进管理经验、加大科技投入，建立高素质的技术团队，实施自主创新，光谷奥源拥有一系列的发明专利和软件著作权，相关成果已获得包括国家技术发明奖在内的多项奖励。
                                        </p>
                                        <p style="text-indent:2em;">
                                            光谷奥源的使命就是打造成为国内下一代<img style="width:50px;height:17px;" height="21" alt="" src="file:///$onevo_image" width="64">技术领域重要的创新和产业化平台。公司推行与国内外一流企业展开技术与市场方面的合作战略，通过优势互补的技术和产品，整合形成高性价比的整体解决方案进入国内外市场，共同服务于客户，实现双赢。奥源人秉承“创新、分享、尊重、执着”的企业理念，欢迎多种形式的交流合作，竭诚期盼与广大合作伙伴和客户携手合作，为国家的物联网、三网融合和下一代互联网产业发展做出有力的贡献，共同谱写辉煌篇章！
                                        </p>
                                    </div>
                                    <p></p>
                                    <p style="line-height:24px;">
                                        <span style="line-height:2;"></span>&nbsp;
                                    </p>
                                    <div class="about">
                                        <h2>联系我们</h2>
                                        <p style="line-height:24px;">
                                            总部地址：武汉关东科技园留学生创业园C座1层
                                        </p>
                                        <p style="line-height:24px;">
                                            全国热线：400-886-7707
                                        </p>
                                        <p style="line-height:24px;">
                                            营销专线：027-87204017
                                        </p>
                                        <p style="line-height:24px;">
                                            行政总机：027-87204290
                                        </p>
                                        <p style="line-height:24px;">
                                            传真号码：027-87204277
                                        </p>
                                        <p style="line-height:24px;">
                                            电子邮箱：<a href="mailto:onevo@ov-orange.com">onevo@ov-orange.com</a> 
                                        </p>
                                        <p style="line-height:24px;">
                                            </p><p style="line-height:24px;">
                                                公司网址：<a href="http://www.ov-orange.com">www.ov-orange.com</a> 
                                            </p>
                                            <p style="line-height:24px;">
                                                百度百科：光谷奥源
                                            </p>
                                        <span style="line-height:2;"></span>
                                        <p></p>
                                        <p style="line-height:24px;">
                                            <span style="line-height:2;"></span>&nbsp;
                                        </p>
                                        <p style="line-height:24px;">
                                            <span style="line-height:2;">山东</span><span style="line-height:2;">地址：</span><span style="line-height:2;">山东</span><span style="line-height:2;">济宁市高新区东外环北路奥信大院</span>
                                        </p>
                                        <p style="line-height:24px;">
                                            <span style="line-height:2;">营销专线：0537-5175970</span>
                                        </p>
                                        <p style="line-height:24px;">
                                            电子邮箱：<a href="mailto:wyy@ov-orange.com">wyy@ov-orange.com</a>
                                        </p>      
                                    </div>
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
