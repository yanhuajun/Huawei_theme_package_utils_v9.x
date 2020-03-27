#!/user/local/bin/python
# -*- coding:utf-8 -*-
import os
import sys
import zipfile
import time
import fileinput 
import chardet
import codecs
import shutil

def getFileNameList():
	fileNameList = {}
	filePath = os.path.join(os.getcwd(),"orgin_icon_file","icon_rename_file.conf")
	file = codecs.open(filePath,'r','utf-8')
	text = file.read()
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
		fileNameList[array[1]] = array[0]
	return fileNameList

def tranName(fileNameList):
	print "changing list :"
	for item in fileNameList:
		#print "orginName:%s ===>tansName:%s" % (item  ,fileNameList[item])
		# if(os.sep == '/'):
  #                       cmd = u"cp ./orgin_icon_file/%s ./trans_name_file/%s"  %(item  ,fileNameList[item])
		# 	#print(cmd);
		# 	os.system(cmd);
		# else:
		# 	cmd = (u"copy .\\orgin_icon_file\\%s .\\trans_name_file\\%s"  %(item ,fileNameList[item]))
  #                       cmd = cmd.encode('utf-8')
		# 	#print(cmd);
		# 	os.system(cmd);
		shutil.copyfile(os.path.join( os.getcwd(),"orgin_icon_file",  item.encode('gbk') ),os.path.join( os.getcwd(),"trans_name_file",fileNameList[item] ) )
#start

fileNameList = getFileNameList()

# 更换下列文件
tranName(fileNameList)
print u'出现此内容表示已成功， 列表内已存在文件已进行转换 ，忽略系统找不到指定文件等提示 ，请前往trans_name_file 文件查看图标'
