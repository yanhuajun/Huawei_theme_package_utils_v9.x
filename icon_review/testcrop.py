#!/usr/bin/python
# -*- coding: UTF-8 -*-
 
import Tkinter
import tkMessageBox
import os
import codecs
from PIL import Image
import platform


img = Image.open('/Users/mac/Documents/github_repository/Huawei_theme_package_utils_v9.x/icon_review/bg/bg_1440x3168.jpg')
print img.size
img.show()
img = img.crop((0,200,1080,1920+200))
img.show()
print img.size

