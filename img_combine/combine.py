#!/usr/bin/python
# -*- coding: UTF-8 -*-
 
import Tkinter
import tkMessageBox
import os
import codecs
from PIL import Image
import platform

default_bg_file = os.path.join(os.getcwd() , 'bg')
default_front_file = os.path.join(os.getcwd() , 'front')
default_output_file = os.path.join(os.getcwd() , 'output')


def getFileFromPath(path,prefix,suffix):
	print "getFileFrom:" + path
	fileList = []
	filenames = os.listdir(path)
	for filename in filenames:
		# print "suffix:" + filename[filename.rfind('.'):len(filename)]
		# if filename[filename.rfind('.'):len(filename)] in suffix :
		# 	fileList.append(filename)
		# else:
			# continue
		if len(suffix ) == 0 and len(prefix) == 0:
			# 没有前缀后缀匹配
			fileList.append(filename)
		else:
			for item in suffix:
				if filename.endswith(item):
					fileList.append(filename)
					continue
			for prefix_item in prefix:
				if filename.startswith(prefix_item):
					fileList.append(filename)
					continue
	print "fileList:"
	print fileList
	return fileList


def readContentFromFileByLine( path ):
	listArr = [] 
	content = codecs.open( path ,'r' , encoding ='utf-8').read()
	arr = []
	if isWindows():
		arr = content.split('\r\n')
	else:
		arr = content.split('\n')
	for item in arr:
		if item != '' and not item.startswith('#') and  item.find("=") >= 0 :
			listArr.append(os.path.join(default_icons_file , item.split('=')[1] ))
	return listArr

def combineImg_New(baseImg , frontImg , outFileName  , frontImgCenterPoint,frontImgResize):
	target = Image.new('RGBA' , baseImg.size , (0,0,0,0))
	baseImg = baseImg.convert("RGBA")
	frontImg = frontImg.convert("RGBA")
	target.paste(baseImg , (0,0) )

	# 处理 font resize
	if frontImgResize != '':
		frontImg = frontImg.resize(frontImgResize,Image.ANTIALIAS)


	# 处理粘贴坐标
	if frontImgCenterPoint == '':
		frontImgCenterPoint = (0,0)
	else:
		frontImgCenterPoint = (frontImgCenterPoint[0]-frontImg.size[0]/2  , frontImgCenterPoint[1]-frontImg.size[1] / 2)

	target.paste(frontImg , frontImgCenterPoint ,frontImg)

	targetObj = {}
	targetObj['img'] = target
	# targetObj['name'] = os.path.join(default_output_file ,outFileName )
	return targetObj 


def isWindows():
	return False
	platformStr = platform.platform()
	print platformStr
	if platformStr.find("windows")>=0 or platformStr.find("Windows") >=0 :
		print "platform is windows"
		return True
	else:
		print "platform is not windows"
		return False

# start 
bgFileList = getFileFromPath( default_bg_file ,[],[])
frontFileList = getFileFromPath( default_front_file ,[],[])

for bg in bgFileList:
	for front in frontFileList:
		bgImage = Image.open(os.path.join(default_bg_file,bg))
		targetObj = combineImg_New( bgImage ,Image.open(os.path.join(default_front_file,front))  , front , '' , bgImage.size )
		img = targetObj['img']
		img.show()
		if not os.path.exists(default_output_file):
			os.makedirs(default_output_file)
		img.save(os.path.join(default_output_file , front) )
