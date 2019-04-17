#!/user/local/bin/python
# -*- coding:utf-8 -*-
import os
import sys
import zipfile
import time
import fileinput 


def getFileNameList():
	fileNameList = {}
	filePath = os.path.join(os.getcwd(),"orgin_icon_file","icon_rename_file.conf")
	for line in fileinput.input(filePath):
		# print line
		if not line:
			continue
		if line == '':
			continue
		if line.startswith("#"):
			continue
		line = line.strip()
		# print line
		array = line.split("=")
		# print array
		fileNameList[array[0]] = array[1]
	return fileNameList

def tranName(fileNameList):
	print "修改文件列表如下："
	for item in fileNameList:
		print "orginName:%s ===>tansName:%s" % (item  ,fileNameList[item])
	for item in fileNameList:
		if(os.sep == '/'):
			print("cp ./orgin_icon_file/%s ./trans_name_file/%s"  %(item  ,fileNameList[item]));
			os.system("cp ./orgin_icon_file/%s ./trans_name_file/%s"  %(item  ,fileNameList[item]));
		else:
			print("copy .\\orgin_icon_file\\%s .\\trans_name_file\\%s"  %(item  ,fileNameList[item]));
			os.system("copy .\\orgin_icon_file\\%s .\\trans_name_file\\%s"  %(item  ,fileNameList[item]));
#start

fileNameList = getFileNameList()

# 更换下列文件
tranName(fileNameList)
