#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import markdown
import codecs
from Cheetah.Template import Template


templateDef = '''
#encoding utf-8
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en-US" lang="en-US">
    <head>
        <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
        <title>$title</title>
        #for $cssfile in $css
            <link href="file:///$cssfile" rel="stylesheet" type="text/css">
        #end for
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


def md2html(mdfile, theme, htmlfile=None):
    '''
        mdfile: 需要转换的markdown的完整路径
        htmlfile: 需要生成html文件的完整路径
        theme: themes中任选其中一个
    '''
    # Open input file in read, utf-8 mode
    input_file = codecs.open(mdfile, mode="r", encoding="utf8")
    text = input_file.read()
    content = markdown.markdown(text)
    nameSpace = {
        'title': u'',
        'content': content,
        'css': theme
    }
    currentmodule = __import__('md2html')
    template = getattr(currentmodule, 'templateDef')
    html = Template(template, searchList=[nameSpace])
    # Write string html to disk
    if htmlfile:
        with open(htmlfile, 'wb') as f:
            f.write(str(html))
    return unicode(html), content


def mdhtmlcomplete(mdhtml, theme, htmlfile=None):
    '''
        mdfile: 需要转换的markdown的完整路径
        htmlfile: 需要生成html文件的完整路径
        theme: themes中任选其中一个
    '''
    # Open input file in read, utf-8 mode
    nameSpace = {
        'title': u'',
        'content': mdhtml,
        'css': theme
    }
    currentmodule = __import__('md2html')
    template = getattr(currentmodule, 'templateDef')
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
