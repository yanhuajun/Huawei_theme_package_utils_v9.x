#!/user/local/bin/python
# -*- coding:utf-8 -*-
import os
import sys
import zipfile
import time
import fileinput 
import chardet
import re
import platform
from PIL import Image
# from lxml import etree
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET


isWindows = False


currentProjectFilePath = ''
toolPath = ''

def listConfigFileArray():
	frameworkResHwextConfigFilePathList = []
	normalConfigFilePathList = []
	retObj = {}
	for index in range(len(fileList)):
		fileItem = fileList[index]
		frameworkResHwextConfigFilePath = os.path.join(currentProjectFilePath,fileItem , "framework-res-hwext" , "theme.xml")
		# print("frameworkResHwextConfigFilePath:%s(%d)" %(frameworkResHwextConfigFilePath ,index) )
		frameworkResHwextConfigFilePathList.append(frameworkResHwextConfigFilePath)
		normalConfigFilePath = os.path.join(currentProjectFilePath,fileItem , "theme.xml")
		# print("normalConfigFilePath:%s(%d)" % (normalConfigFilePath ,index) )
		normalConfigFilePathList.append(normalConfigFilePath)
	retObj['frameworkResHwextConfigFilePathList'] = frameworkResHwextConfigFilePathList
	retObj['normalConfigFilePathList']  = normalConfigFilePathList
	# print retObj;
	return retObj;



def get_filelist(dir, Filelist,suffix):
	newDir = dir
	if os.path.isfile(dir):
		if dir.endswith(suffix):
			Filelist.append(dir)
		# # 若只是要返回文件文，使用这个
		# Filelist.append(os.path.basename(dir))
	elif os.path.isdir(dir):
		for s in os.listdir(dir):
			# 如果需要忽略某些文件夹，使用以下代码
			#if s == "xxx":
				#continue
			newDir=os.path.join(dir,s)
			get_filelist(newDir, Filelist,suffix)
	return Filelist

def check(arr):
	for item in arr:
		print "----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------"

		print "check filePath:" + item + "\n"
		data = open(item).read()
		print data
		root = ET.fromstring(data)
		if root == '' :
			print "有误"
		else:
			print root 
		print "----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------"
	

# start
print '输入参数列表:'
print sys.argv
if len(sys.argv) > 1:
	for index in range(len(sys.argv)):
		if index == 0:
			toolPath = sys.argv[index]
			toolPath = toolPath[0:toolPath.rfind('/')]
		if index == 1:
			currentProjectFilePath = sys.argv[index]
else:
	currentProjectFilePath = os.getcwd()
	toolPath = os.getcwd()
print 'currentProjectFilePath :' + currentProjectFilePath +",\ntoolPath:" + toolPath
print '\n'
# 判断是否windows
print  'now system version:' + platform.system()
if platform.system() == 'Windows' or platform.system() == 'windows':
	isWindows = True

if isWindows:
	print 'windows env'
else:
	print 'not windows env'

fileList = []
fileList = get_filelist(currentProjectFilePath,fileList,".xml")
print "fileList Number: %d" % (len(fileList) )
print "file list is :\n"
check(fileList)


