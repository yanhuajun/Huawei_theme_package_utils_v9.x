#!/user/local/bin/python
# -*- coding:utf-8 -*-
import os
import sys
import zipfile
import time
import fileinput 
import chardet

def getFileNameList():
	fileNameList = {}
	filePath = os.path.join(os.getcwd(),"orgin_icon_file","icon_rename_file.conf")
	file = open(filePath,'r')
	text = file.read().decode("utf-8")
	#print text
	for line in text.split("\n"):
		#print "%s%s" %(line , "---")
		if not line:
			continue
		if line == '':
			continue
		if line.startswith("#"):
			continue
		line = line.strip()
		array = line.split("=")
		fileNameList[array[0]] = array[1]
	return fileNameList

def tranName(fileNameList):
	print "changing list :"
	for item in fileNameList:
		print "orginName:%s ===>tansName:%s" % (item  ,fileNameList[item])
	for item in fileNameList:
		if(os.sep == '/'):
			print("cp ./orgin_icon_file/%s ./trans_name_file/%s"  %(item  ,fileNameList[item]));
			os.system("cp ./orgin_icon_file/%s ./trans_name_file/%s"  %(item  ,fileNameList[item]));
		else:
			cmd = ("copy .\\orgin_icon_file\\%s .\\trans_name_file\\%s"  %(item ,fileNameList[item]))
			cmd = cmd.encode("gbk")
			print(cmd);
			os.system(cmd);
#start

fileNameList = getFileNameList()

# 更换下列文件
tranName(fileNameList)
