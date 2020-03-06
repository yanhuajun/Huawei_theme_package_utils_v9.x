#!/user/local/bin/python
# -*- coding:utf-8 -*-
import os
import sys
import zipfile
import time
import fileinput 
import chardet
import codecs

error_icon_file_list = '' 

def getFileNameList(filePath):
	fileNameList = {}
	file = codecs.open(filePath,'r','utf-8')
	text = file.read()
	file.close()
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

def check_icon_name(configFileList, checkFilePath):
	fileList = getFileFromPath(checkFilePath)
	# print fileList 
	# 对比中文名 ，则选择configFileList 中的kek  ，对比英文名则选择 value
	for item in fileList:
		if configFileList.has_key(item ):
			configFileList.pop(item)
	# 剩下的configFileList 都是未找到对应的，需要输出到文件
	if len(configFileList) == 0:
		print "已检查" + checkFilePath +"下所有png文件，文件名正确"
		return
	result = ''
	for (d,x) in configFileList.items():
		result += "can't find :"+d+"\r\nmatched en name:"+ x +"\r\n\r\n"
	
	# print result
	resultPath = os.path.join(checkFilePath , "check_icon_name_error.txt")
	resultFile = codecs.open(resultPath,"w",encoding='utf-8')
	#resultFile = codecs.open(resultPath,"w",encoding='gbk')
	resultFile.write(result)
	resultFile.close()
	print u"结果文件成功写入至" + resultPath

def getFileFromPath(path):
	print "getFileFrom:" + path
	fileList = []
	filenames = os.listdir(path)
	for filename in filenames:
		if filename.endswith(".png"):
			fileList.append(filename)
		else:
			continue
	return fileList


#start

configFileList = getFileNameList(os.path.join(os.getcwd(),"orgin_icon_file","icon_rename_file.conf"))
print "get configFileList success"
# print configFileList

check_icon_name(configFileList , os.path.join(os.getcwd(),"orgin_icon_file"))

