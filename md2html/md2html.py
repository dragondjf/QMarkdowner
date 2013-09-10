#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import markdown
import codecs
from Cheetah.Template import Template
import time


templateDef_default = '''
#encoding utf-8
#set $highlight_js = $os.sep.join([$os.getcwd(), 'webjscss', 'highlight', 'highlight.pack.js'])
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en-US" lang="en-US">
    <head>
        <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
        <title>$title</title>
        <style>
            $themecss
        </style>
        <script>
            $highlightjs
        </script>
        <script>hljs.initHighlightingOnLoad();</script>
    </head>
        <body style="background: transparent;">
            <div id="main_content_wrap" class="outer" style="margin:0px auto">
                <section id="main_content" class="inner">
                    <div id="preview_pane" class="pane" style="width: 780px; margin:0px auto">
                        <div id="preview">$content</div>
                    </div>
                </section>
            </div>
        </body>
</html>
'''

templateDef_evernote = '''
#encoding utf-8
#set $csspath = $os.sep.join([$os.getcwd(), 'webjscss', 'themecss', 'evernote'])
#set $themeevernote_css=$os.sep.join([$csspath, 'themeevernote.css'])
#set $createtime = $time.ctime()
#set $highlight_js = $os.sep.join([$os.getcwd(), 'webjscss', 'highlight', 'highlight.pack.js'])
<!DOCTYPE html>
<html>
    <head>
        <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
        <meta name="en:locale" content="zh_CN_evernoteChina">
        <meta charset="utf-8">
        <title>$title</title>
        <style>
            $themecss
        </style>
        <script>
            $highlightjs
        </script>
        <script>hljs.initHighlightingOnLoad();</script>
    </head>
    <body class="wrapper" style="background: rgb(222,222,222)">
        <br>
        <div class="SharedNoteView"><div id="container-boundingbox" class="wrapper">
            <div id="container" class="wrapper">
                <div class="shared-by shared-by-desktop">
                    <div class="shared-by-corner"></div>
                    $title
                </div>
                <br>
                <br>
                <div class="vtop">
                    <div class="note-updated">
                      <span>作者: dragondjf</span>
                    </div>
                    <div class="note-updated">
                      <span>时间：$createtime</span>
                    </div>
                </div>
                <div class="divider"></div>
                <div class="note-content">
                    <div style="word-wrap: break-word; -webkit-nbsp-mode: space;
                            -webkit-line-break: after-white-space;" class="ennote">
                        $content
                    </div>
                </div>
            </div>
        </div>
    </body>
</html>
'''

templateDef_jeklyy = '''
#encoding utf-8
#set $highlight_js = $os.sep.join([$os.getcwd(), 'webjscss', 'highlight', 'highlight.pack.js'])
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en-US" lang="en-US">
    <head>
        <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
        <title>$title</title>
        <style>
            $themecss
        </style>
        <script>
            $highlightjs
        </script>
        <script>hljs.initHighlightingOnLoad();</script>
    </head>
        <body>
        <div>
            </div>
            <div class="mainwindow">
                <div class="note">
                    <h5>$title</h5>
                </div>
                <div class="centerwindow">
                    $content
                </div>
            </div>
        </div>
        <div class="footer">
            <h5>Designed by dragondjf 20130908</h5>
            <h5>Inspired by jekyll</h5>
        </div>
    </body>
</html>
'''


jsfile = os.sep.join([os.getcwd(), 'webjscss', 'highlight', 'highlight.pack.js'])
js = codecs.open(jsfile, mode="r", encoding="utf8")
highlightjs = js.read()
js.close()


def md2html(mdfile, theme, htmlfile=None, template="templateDef_default"):
    '''
        mdfile: 需要转换的markdown的完整路径
        htmlfile: 需要生成html文件的完整路径
        theme: themes中任选其中一个
    '''
    # Open input file in read, utf-8 mode
    input_file = codecs.open(mdfile, mode="r", encoding="utf8")
    text = input_file.read()
    input_file.close()
    themecss = ''
    for css in theme:
        if not os.path.exists(css):
            themecss = ""
        else:
            theme_file = codecs.open(css, mode="r", encoding="utf8")
            themecss += theme_file.read()
            theme_file.close()
    content = markdown.markdown(text)
    nameSpace = {
        'title': mdhtml.split("\n")[0][4:-5],
        'content': content,
        'themecss': themecss,
        'highlightjs': highlightjs
    }
    currentmodule = __import__('md2html')
    template = getattr(currentmodule, template)
    html = Template(template, searchList=[nameSpace])
    # Write string html to disk
    if htmlfile:
        with open(htmlfile, 'wb') as f:
            f.write(str(html))
    return unicode(html), content


def mdhtmlcomplete(mdhtml, theme, htmlfile=None, template="templateDef_default"):
    '''
        mdfile: 需要转换的markdown的完整路径
        htmlfile: 需要生成html文件的完整路径
        theme: themes中任选其中一个
    '''
    # Open input file in read, utf-8 mode
    themecss = ''
    for css in theme:
        theme_file = codecs.open(css, mode="r", encoding="utf8")
        themecss += theme_file.read()
        theme_file.close()
    nameSpace = {
        'title': mdhtml.split("\n")[0][4:-5],
        'content': mdhtml,
        'themecss': themecss,
        'highlightjs': highlightjs
    }
    currentmodule = __import__('md2html')
    template = getattr(currentmodule, template)
    completehtml = Template(template, searchList=[nameSpace])
    # Write string completehtml to disk
    if htmlfile:
        with open(htmlfile, 'wb') as f:
            f.write(str(completehtml))
    return unicode(completehtml)


def main():
    mdfile = os.sep.join([os.path.dirname(__file__), 'demo.md'])
    htmlfile = os.sep.join([os.path.dirname(__file__), 'demo.html'])
    md2html(mdfile, htmlfile, 'themewhite')
    # md2html(mdfile, htmlfile, 'themeblack')

if __name__ == '__main__':
    main()
