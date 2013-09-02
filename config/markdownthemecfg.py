#!/usr/bin/python
# -*- coding: utf-8 -*-

import os 


markdownthemes = {
	'themes': ['themeblack', 'themewhite', 'themegithub', 'themeslate'],
    'themeblack': [os.sep.join([os.getcwd(), 'webjscss', 'themecss', 'black', css]) for css in ['themeblack.css']],
    'themewhite': [os.sep.join([os.getcwd(), 'webjscss', 'themecss', 'white', css]) for css in ['themewhite.css']],
    'themegithub': [os.sep.join([os.getcwd(), 'webjscss', 'themecss', 'github', css]) for css in ['themegithub.css']],
    'themeslate': [os.sep.join([os.getcwd(), 'webjscss', 'themecss', 'slate', css]) for css in ['themeslate.css']]
}
