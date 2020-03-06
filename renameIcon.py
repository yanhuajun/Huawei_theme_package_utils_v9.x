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

def getFileNameList():
	fileNameList = {}
	filePath = os.path.join(os.getcwd(),"orgin_icon_file","icon_rename_file.conf")
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

def tranName(fileNameList):
	global error_icon_file_list
	print "changing list :"
	for item in fileNameList:
		pass
		#print u"orginName:%s ===>tansName:%s" % (item ,fileNameList[item])
	for item in fileNameList:
		try:
			if(os.sep == '/'):
				cmd = "cp ./orgin_icon_file/'%s' ./trans_name_file/'%s'"  %(item  ,fileNameList[item])
				print(cmd);
				os.system(cmd);
			else:
				cmd = ("copy .\\orgin_icon_file\\'%s' .\\trans_name_file\\'%s'"  %(item ,fileNameList[item]))
				cmd = cmd.encode("gbk")
				print(cmd);
				os.system(cmd)
		except Exception , e : 
			print "error , " + e.message 
			error_icon_file_list += u"转换失败,原始文件：" + item+ u"\t\t\t,转换后文件:" + fileNameList[item]+ "\r\n\r\n"
			continue;
	# 输出错误列表
	filePath = os.path.join(os.getcwd(),"orgin_icon_file","error_list.txt")
	file = codecs.open(filePath,'w','utf-8')
	if error_icon_file_list == '':
		error_icon_file_list = u'没有错误 ，请查看 trans_name_file 文件夹并使用图标 '
	file.write(error_icon_file_list)
	file.close()

	print u"转换成功 ，可能有部分图片转换失败 ，请查看orgin_icon_file 是否有 error_list.txt 文件 ，转换错误的信息将写在此文件中 ，"
#start

configFileList = getFileNameList()
# print configFileList

# 更换下列文件
tranName(configFileList)
