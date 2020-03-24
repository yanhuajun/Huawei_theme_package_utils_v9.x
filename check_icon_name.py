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
		# array = line.split("=")
		# fileNameList[array[0]] = array[1]
		fileNameList[line] = line
	return fileNameList

def check_icon_name(configFileList, checkFilePath):
	fileList = getFileFromPath(checkFilePath)
	# print fileList 
	# 对比中文名 ，则选择configFileList 中的kek  ，对比英文名则选择 value
	for item in fileList:
		if configFileList.has_key(item.decode('gbk') ):
			configFileList.pop(item.decode('gbk'))
	# 剩下的configFileList 都是未找到对应的，需要输出到文件
	result = u'以下为命名错误图标，请检查 \r\n\r\n'
	if len(configFileList) == 0:
		# print u"已检查" + checkFilePath +u"下所有png文件，文件名正确"
		print "success  ,finish check all file in path:" + checkFilePath + ",with conf file:" + os.path.join(os.getcwd(),"orgin_icon_file","icon_check_list.conf") +", and all file name is right!!" 
		result = u'全部验证， 无错误... \r\n\r\n'
	for (d,x) in configFileList.items():
		# result += u"未找到 （中文名）:"+d + u"\r\n匹配的英文名:"+ x +"\r\n\r\n"
		result += u"未找到 （中文名）:"+d + "\r\n\r\n"
	# print result
	resultPath = os.path.join(checkFilePath , "check_icon_name_error.txt")
	resultFile = codecs.open(resultPath,"w",encoding='utf-8')
	#resultFile = codecs.open(resultPath,"w",encoding='gbk')
	resultFile.write(result)
	resultFile.close()

	# print u"结果文件成功写入至" + resultPath
	print "success , output file path:" + resultPath

def getFileFromPath(path):
	print "getFileFrom:" + path
	fileList = []
	filenames = os.listdir(path)
	for filename in filenames:
		if filename.endswith(".png"):
			fileList.append(filename)
		else:
			continue
	print "fileList:"
	print fileList
	return fileList


#start

configFileList = getFileNameList(os.path.join(os.getcwd(),"orgin_icon_file","icon_check_list.conf"))
print "get configFileList success"
print configFileList

check_icon_name(configFileList , os.path.join(os.getcwd(),"orgin_icon_file"))

