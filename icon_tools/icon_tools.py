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
import Tkinter
from Tkinter import *
import tkMessageBox
import platform




error_icon_file_list = '' 
default_output_file = os.path.join(os.getcwd() , 'output')
default_icons_file = os.path.join(os.getcwd() , 'icons')
default_res_file = os.path.join(os.getcwd() , 'res')
# default_config_name = ['hw_rd_100_p2.conf','hw_rd_100_p1.conf','hw_rd_47.conf']

#layoutview 
outputPathEntry = ''
iconsFilePathEntry=''
lb2 = ''
change_mode = 'ch'

def getFileNameList( text ):
	fileNameList = {}
	# filePath = os.path.join(os.getcwd(),"orgin_icon_file","icon_rename_file.conf")
	# file = codecs.open(filePath,'r','utf-8')
	# text = file.read()
	# file.close()
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
	global error_icon_file_list,outputPathEntry,iconsFilePathEntry
	error_icon_file_list = ''
	outputPath = ''
	if outputPathEntry.get() == '' :
		outputPath = default_output_file
	else :
		outputPath = outputPathEntry.get()
	if not os.path.exists(outputPath):
		os.makedirs(outputPath)
	iconsFilePath = ''
	if iconsFilePathEntry.get() == '':
		iconsFilePath = default_icons_file
	else:
		iconsFilePath = iconsFilePathEntry.get()

	# change_mode


	print "changing list :"

	for item in fileNameList:
		# pass
		try:
			# print item.decode('utf-8')
			# print fileNameList[item]
			
			if change_mode == 'ch':
				shutil.copyfile(os.path.join( iconsFilePath,  item ),os.path.join( outputPath,fileNameList[item] ) )
				# shutil.copyfile(os.path.join( iconsFilePath,  item.encode('gbk') ),os.path.join( outputPath,fileNameList[item] ) )
				# comamnd = " copy %s %s" %(  )
				# os.command()
			else:
				shutil.copyfile(os.path.join( iconsFilePath,  fileNameList[item] ),os.path.join( outputPath, item.encode('gbk') ) )

		except Exception , e : 
			print "error , " 
			print e 
			error_icon_file_list += u"转换失败,原始文件："
			if change_mode == 'ch':
				error_icon_file_list += item
			else:
				error_icon_file_list += fileNameList[item]
			error_icon_file_list += u" \t\t\t,转换后文件:"
			if change_mode == 'ch':
				error_icon_file_list += fileNameList[item]
			else:
				error_icon_file_list += item

			error_icon_file_list += u" \r\n\r\n" 
			continue

	# print error_icon_file_list

	# 输出错误列表
	filePath = os.path.join(outputPath,"error_list.txt")
	file = codecs.open(filePath,'w','utf-8')
	if error_icon_file_list == '':
		error_icon_file_list = u'没有错误 ，请查看 trans_name_file 文件夹并使用图标 '
	file.write(error_icon_file_list)
	file.close()


	tkMessageBox.showinfo( "确认信息", "转换成功 ，可能有部分图片转换失败 ，请查看输出文件夹下是否有 error_list.txt 文件 ，转换错误的信息将写在此文件中 ，" )

def tranName_new():
	print "changing list :"
	for item in fileNameList:
		
		orginFileName = ''
		targetFileName = ''

		if change_mode == 'ch':
			orginFileName = item.encode('gbk')
			targetFileName = fileNameList[item]
		else:
			orginFileName = fileNameList[item].encode('gbk')
			targetFileName = item
			
		try:
			shutil.copyfile(os.path.join( iconsFilePath,  orginFileName ),os.path.join( outputPath, targetFileName) )

		except Exception , e : 
			print "error , " 
			print e 
			error_icon_file_list += u"转换失败,原始文件："
			error_icon_file_list += orginFileName.decode('gbk')
			error_icon_file_list += u" \t\t\t,转换后文件:"
			error_icon_file_list += targetFileName
			error_icon_file_list += u" \r\n\r\n" 
			continue

	# print error_icon_file_list

	# 输出错误列表
	filePath = os.path.join(outputPath,"error_list.txt")
	file = codecs.open(filePath,'w','utf-8')
	if error_icon_file_list == '':
		error_icon_file_list = u'没有错误 ，请查看 trans_name_file 文件夹并使用图标 '
	file.write(error_icon_file_list)
	file.close()


	tkMessageBox.showinfo( "确认信息", "转换成功 ，可能有部分图片转换失败 ，请查看输出文件夹下是否有 error_list.txt 文件 ，转换错误的信息将写在此文件中 ，" )

	



def combineConf(list):
	content = ''
	for item in list:
		content += codecs.open(item,'r','utf-8').read()
	return content



def nextStepButtonAction():
	# print lb2.get()
	selectedConfList = []
	for index in lb2.curselection():
		selectedConfList.append( os.path.join( default_res_file , lb2.get(index) ) ) 
	configContent = combineConf(selectedConfList)
	fileNameList = getFileNameList(configContent)
	# print fileNameList
	tranName(fileNameList)


def getFileFromPath(path,suffix):
	print "getFileFrom:" + path
	fileList = []
	filenames = os.listdir(path)
	for filename in filenames:
		# print "suffix:" + filename[filename.rfind('.'):len(filename)]
		# if filename[filename.rfind('.'):len(filename)] in suffix :
		# 	fileList.append(filename)
		# else:
			# continue
		if len(suffix ) == 0:
			fileList.append(filename)
		else:
			for item in suffix:
				if filename.endswith(item):
					fileList.append(filename)
	print "fileList:"
	print fileList
	return fileList

def clearOutputPathButtonAction():
	outputPath = ''
	if outputPathEntry.get() == '' :
		outputPath = default_output_file
	else :
		outputPath = outputPathEntry.get()
	if not os.path.exists(outputPath):
		os.makedirs(outputPath)
		return 
	else:
		fileNameList = getFileFromPath(outputPath , [])
		#删除
		for fileName in fileNameList:
			os.remove(os.path.join( outputPath , fileName ) )
		tkMessageBox.showinfo( "确认信息", "已清空:"  + outputPath +"文件夹内容..." )


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

def ch2EnButtonAction():
	global change_mode
	change_mode = 'ch'
	nextStepButtonAction()

def en2ChButtonAction():
	global change_mode
	change_mode = 'en'
	nextStepButtonAction()


def chCheckButtonAction():
	selectedConfList = []
	for index in lb2.curselection():
		selectedConfList.append( os.path.join( default_res_file , lb2.get(index) ) ) 
	configContent = combineConf(selectedConfList)
	fileNameList = getFileNameList(configContent)
	#print fileNameList
	iconsPath  = '' 
	if iconsFilePathEntry.get() == '':
		iconsPath = default_icons_file
	else:
		iconsPath = iconsConfigFilePathEntry.get()
		
	print iconsPath
	errorFileContent = u""
	for item in fileNameList:
		if not os.path.exists( os.path.join(iconsPath , item) ):
			#print u"未找到文件: " 
			#print item
			errorFileContent += u"未找到文件: " +item +u"\n"
			#print item
	if errorFileContent == u'':
		errorFileContent = u'没有错误，检测通过'
	print errorFileContent
	#print type(errorFileContent)
	outFilePath = os.path.join( iconsPath  , 'result.txt' )
	errorFile = codecs.open( outFilePath , 'w' ,'utf-8')
	errorFile.write(errorFileContent)
	errorFile.flush()
	errorFile.close()
	tkMessageBox.showinfo( "确认信息", "检测完毕 ，结果已输出至 %s" % outFilePath )

	
def enCheckButtonAction():
	selectedConfList = []
	for index in lb2.curselection():
		selectedConfList.append( os.path.join( default_res_file , lb2.get(index) ) ) 
	configContent = combineConf(selectedConfList)
	fileNameList = getFileNameList(configContent)
	#print fileNameList
	iconsPath  = '' 
	if iconsFilePathEntry.get() == '':
		iconsPath = default_icons_file
	else:
		iconsPath = iconsConfigFilePathEntry.get()
		
	print iconsPath
	errorFileContent = u""
	for item in fileNameList:
		if not os.path.exists( os.path.join(iconsPath , fileNameList[item]) ):
			#print u"未找到文件: " 
			#print item
			errorFileContent += u"未找到文件: " +fileNameList[item] +u"\n"
			#print item
	if errorFileContent == u'':
		errorFileContent = u'没有错误，检测通过'
	print errorFileContent
	#print type(errorFileContent)
	outFilePath = os.path.join( iconsPath  , 'result.txt' )
	errorFile = codecs.open( outFilePath, 'w' ,'utf-8')
	errorFile.write(errorFileContent)
	errorFile.flush()
	errorFile.close()
	tkMessageBox.showinfo( "确认信息", "检测完毕 ，结果已输出至 %s" % outFilePath )


def startLayoutView():
	global outputPathEntry,lb2,change_mode,iconsFilePathEntry

	top = Tkinter.Tk()
	top.title("图标中英文转换工具")

	# bgFilePathLabel = Tkinter.Label(top,text="背景图片文件夹路径（不填默认当前文件夹下bg文件夹）")
	# bgFilePathLabel.pack()

	# bgFilePathEntry = Tkinter.Entry(top  )
	# bgFilePathEntry.pack()

	iconsFilePathLabel = Tkinter.Label(top,text="icons文件夹路径（不填默认当前文件夹下icons文件夹）")
	iconsFilePathLabel.pack()

	iconsFilePathEntry = Tkinter.Entry(top  )
	iconsFilePathEntry.pack()


	# iconsConfigFilePathLabel = Tkinter.Label(top,text="icons筛选配置文件路径（不填默认当前文件夹下icons.conf）")
	# iconsConfigFilePathLabel.pack()

	# iconsConfigFilePathEntry = Tkinter.Entry(top  )
	# iconsConfigFilePathEntry.pack()

	outputPathLabel = Tkinter.Label(top,text="输出文件夹目录（不填则默认当前文件夹下output文件夹）")
	outputPathLabel.pack()
	outputPathEntry = Tkinter.Entry(top  )
	outputPathEntry.pack()

	#var = Tkinter.StringVar()
	#var.set('ch')
	#change_mode=var.get()
	## l = Tkinter.Label(top, bg='yellow', width=20, text='empty')
	#l = Tkinter.Label(top,  text='请选择转换方式（A.中转英 B.英转中）默认中转')
	#l.pack()
	#def print_selection():
	#	global change_mode
	#	change_mode = var.get()
	#	# l.config(text='you have selected ' + var.get())
	#Tkinter.Radiobutton(top, text='A.中转英',variable=var, value='ch',command=print_selection).pack()
	#Tkinter.Radiobutton(top, text='B.英转中',variable=var, value='en',command=print_selection).pack()



	configSelectedListLabel = Tkinter.Label(top,text="可选配置列表")
	configSelectedListLabel.pack()

	#.创建一个可以多选的Listbox,使用属性selectmaod'
	lb2=Tkinter.Listbox(top,selectmode=MULTIPLE)

	for item in getFileFromPath(default_res_file,['.conf']):
		if(isWindows()):
			lb2.insert(END,str(item.decode('gbk').encode('utf-8')))
		else:
			lb2.insert(END,str(item))

	#  有两个特殊的值ACTIVE和END，ACTIVE是向当前选中的item前插入一个
	# （即使用当前选中的索引作为插入位置）；END是向
	#  Listbox的最后一项添加插入一项
	# lb2.delete(1,3)
	#删除全部内容,使用delete指定第一个索引值0和最后一个参数END，即可
	lb2.pack()

	clearOutputPathButton = Tkinter.Button(top, text="清空输出文件夹", command = clearOutputPathButtonAction)
	clearOutputPathButton.pack()
	
	ch2EnButton = Tkinter.Button(top, text="中转英", command = ch2EnButtonAction)
	ch2EnButton.pack()
	
	en2ChButton = Tkinter.Button(top, text="英转中", command = en2ChButtonAction)
	en2ChButton.pack()
	
	chCheckButton = Tkinter.Button(top, text="检测中文", command = chCheckButtonAction)
	chCheckButton.pack()
	
	enCheckButton = Tkinter.Button(top, text="检测英文", command = enCheckButtonAction)
	enCheckButton.pack()

	#strvar = Tkinter.StringVar()
	#strvar.set("中英转换") #初始的按钮文本
	#nextStepButton = Tkinter.Button(top, textvariable=strvar, command = nextStepButtonAction)
	#nextStepButton.pack()

	





	top.mainloop()


#start
startLayoutView()
