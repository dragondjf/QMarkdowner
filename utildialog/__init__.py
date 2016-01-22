#!/usr/bin/python
# -*- coding: utf-8 -*-
from qframer.qt import QtGui
from qframer.qt import QtCore
from logindialog import login
from exitdialog import exit
from msgdialog import MessageDialog
from msgdialog import msg
from ipaddressdialog import ipaddressinput
from urlinputdialog import urlinput
from numinputdialog import numinput
from confirmdialog import confirm
from confirmdialog import ConfirmDialog
from basedialog import DynamicTextWidget



__version__ = '0.1.0'

__all__ = ['DynamicTextWidget', 'ConfirmDialog', 'MessageDialog','login', 'exit', 'msg', 'ipaddressinput', 'urlinput', 'numinput', 'confirm']

__author__ = 'dragondjf(dragondjf@gmail.com)'
