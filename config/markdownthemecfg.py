#!/usr/bin/python
# -*- coding: utf-8 -*-

import os 


markdownthemes = {
    'themeblack': [os.sep.join([os.getcwd(), 'webjscss', 'themecss', 'black', css]) for css in ['preview.css', 'style.css']],
    'themewhite': [os.sep.join([os.getcwd(), 'webjscss', 'themecss', 'white', css]) for css in ['themewhite.css']],
    'themegray': [os.sep.join([os.getcwd(), 'webjscss', 'themecss', 'gray', css]) for css in ['themegray.css']],
    'themegithub': [os.sep.join([os.getcwd(), 'webjscss', 'themecss', 'github', css]) for css in ['themegithub.css']],
    'themeslate': [os.sep.join([os.getcwd(), 'webjscss', 'themecss', 'slate', css]) for css in ['themeslate.css']]
}
