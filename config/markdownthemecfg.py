#!/usr/bin/python
# -*- coding: utf-8 -*-

import os

markdownthemes = {
    'themes': ['themeblack', 'themewhite', 'themegithub', 'themeevernote', 'themejeklyy'],
    'themeblack': [os.sep.join([os.getcwd(), 'webjscss', 'themecss', 'black', css]) for css in ['themeblack.css']],
    'themewhite': [os.sep.join([os.getcwd(), 'webjscss', 'themecss', 'white', css]) for css in ['themewhite.css']],
    'themegithub': [os.sep.join([os.getcwd(), 'webjscss', 'themecss', 'github', css]) for css in ['themegithub.css']],
    'themeevernote': [os.sep.join([os.getcwd(), 'webjscss', 'themecss', 'evernote', css]) for css in ['themeevernote.css']],
    'themejeklyy': [os.sep.join([os.getcwd(), 'webjscss', 'themecss', 'jeklyy', css]) for css in ['themejeklyy.css']]
}
