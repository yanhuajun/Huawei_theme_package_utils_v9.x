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
	global error_icon_file_list
	print "changing list :"
	for item in fileNameList:
		pass
		#print "orginName:%s ===>tansName:%s" % (item  ,fileNameList[item])
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
			error_icon_file_list += "转换失败\t原始文件：" + item.encode("utf-8") + "\t\t\t,转换后文件:" + fileNameList[item].encode('utf-8') + "\n"
			continue;
	# 输出错误列表
	filePath = os.path.join(os.getcwd(),"orgin_icon_file","error_list.txt")
	file = open(filePath,'w')
	if error_icon_file_list == '':
		error_icon_file_list = '没有错误 ，请查看 trans_name_file 文件夹并使用图标 '
	file.write(error_icon_file_list)
	file.close()

	print "转换成功 ，可能有部分图片转换失败 ，请查看orgin_icon_file 是否有 error_list.txt 文件 ，转换错误的信息将写在此文件中 ，"

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
		result += "can't find :"+d+"\nmatched en name:"+ x +"\n\n"
	
	print result
	resultPath = os.path.join(checkFilePath , "check_icon_name_error.txt")
	resultFile = codecs.open(resultPath,"w",encoding='utf-8')
	resultFile.write(result)
	resultFile.close()
	print "结果文件成功写入至" + resultPath

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

# 更换下列文件
# tranName(fileNameList)



