#!/user/local/bin/python
# -*- coding:utf-8 -*-
import os
import sys
import zipfile
import time
import fileinput 
import chardet

error_icon_file_list = '' 

def getFileNameList():
	fileNameList = {}
	filePath = os.path.join(os.getcwd(),"orgin_icon_file","icon_rename_file.conf")
	file = open(filePath,'r')
	text = file.read().decode("utf-8")
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
	print "changing list :"
	for item in fileNameList:

		#print "orginName:%s ===>tansName:%s" % (item  ,fileNameList[item])
	for item in fileNameList:
		try:
			if(os.sep == '/'):
				print("cp ./orgin_icon_file/%s ./trans_name_file/%s"  %(item  ,fileNameList[item]));
				os.system("cp ./orgin_icon_file/%s ./trans_name_file/%s"  %(item  ,fileNameList[item]));
			else:
				cmd = ("copy .\\orgin_icon_file\\%s .\\trans_name_file\\%s"  %(item ,fileNameList[item]))
				cmd = cmd.encode("gbk")
				print(cmd);
				os.system(cmd)
		except Exception , e : 
			print "error , " + e.message 
			error_icon_file_list += "转换失败\t原始文件：" + item + ",转换后文件:" + fileNameList[item] + "\n"
			continue;
	# 输出错误列表
	filePath = os.path.join(os.getcwd(),"orgin_icon_file","error_list.txt")
	file = open(filePath,'w')
	if error_icon_file_list == '':
		error_icon_file_list = '没有错误 ，请查看 trans_name_file 文件夹并使用图标 '
	file.write(error_icon_file_list)
	file.close()

	print "看到 success 字样说明转换成功 ，请查看orgin_icon_file 是否有 error_list.txt 文件 ，转换错误的信息将写在此文件中 ，"
#start

fileNameList = getFileNameList()

# 更换下列文件
tranName(fileNameList)
