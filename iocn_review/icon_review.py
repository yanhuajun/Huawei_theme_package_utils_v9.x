#!/usr/bin/python
# -*- coding: UTF-8 -*-
 
import Tkinter
import tkMessageBox
import os
import codecs
from PIL import Image
import platform

default_bg_file = os.path.join(os.getcwd() , 'bg')
default_icons_file = os.path.join(os.getcwd() , 'icons')
default_res_file = os.path.join(os.getcwd() , 'res')
default_icons_conf_file = os.path.join(os.getcwd() , 'icons.conf')
default_output_file = os.path.join(os.getcwd() , 'output')

bg_list = []
icons_list = []
conf_list = []

isWindows = True

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

def readContentFromFileByLine( path ):
	listArr = [] 
	content = codecs.open( path ,'r' , encoding ='utf-8').read()
	for item in content.split('\n'):
		if item.find("=") >= 0 :
			listArr.append(item)
	return listArr

def getImageSize(path):
	img = Image.open(path)
	# print img.size
	return img.size

def optByConf( ):
	global conf_list
	print 'optByConf '
	printArr = []

	for item in conf_list:
		# print "item:" + item 
		filePath = os.path.join(default_icons_file , item.split('=')[1] )
		print "filePath:" + filePath
		if os.path.exists(filePath):
			print 'exists'
			printArr.append(item)
			icons_list.append(filePath)
	return printArr 

def combineImg(img1Path ,img2Path ,outFileName ,inputBox ):
	# print "ready to combine img  : " + img1Path +" , and :" + img2Path

	base_img = img2Path # Image.open(img2Path)
	#新建透明底图，大小和手机图一样，mode使用RGBA，保留Alpha透明度，颜色为透明
	#Image.new(mode, size, color=0)，color可以用tuple表示，分别表示RGBA的值
	target = Image.new('RGBA', base_img.size, (0, 0, 0, 0))
	if inputBox == '':
		box = (0, 0, base_img.size[0], base_img.size[1]) #区域
	else:
		box = inputBox
	# 加载需要狐狸像
	region = img1Path # Image.open(img1Path)
	# region = region.rotate(180) #旋转180度
	#确保图片是RGBA格式，大小和box区域一样
	region = region.convert("RGBA")
	region = region.resize((box[2] - box[0], box[3] - box[1]))
	#先将狐狸像合成到底图上
	target.paste(region,box)
	#将手机图覆盖上去，中间透明区域将狐狸像显示出来。
	target.paste(base_img,(0,0),base_img) #第一个参数表示需要粘贴的图像，中间的是坐标，最后是一个是mask图片，用于指定透明区域，将底图显示出来。
	# target.show()
	# target.save(os.path.join(default_output_file ,outFileName ))  # 保存图片

	targetObj = {}
	targetObj['img'] = target
	targetObj['name'] = os.path.join(default_output_file ,outFileName )
	return targetObj 

def isWindows():
	platformStr = platform.platform()
	print platformStr
	if platformStr.find("windows")>=0 or platformStr.find("Windows") >=0 :
		print "platform is windows"
		return True
	else:
		print "platform is not windows"
		return False


def workWithSingleSize(bgPath ,resFilePath  ,width , height ):
	path = os.path.join(resFilePath , "%d*%d" %(width ,height ) )
	resList = getFileFromPath(path , ['.png'])
	# if not os.path.exists(default_output_file):
	# 	os.makedirs(default_output_file)
	for item in resList:
		# 背景和前置文字组合
		targetObj = combineImg(Image.open(bgPath) , Image.open(os.path.join(path ,item )) , item ,'')
		# icon和 以上组合
		print "icon:" + icons_list[0]
		icon = Image.open(icons_list[0])
		targetObj = combineImg(targetObj["img"] ,  icon, item ,'')



		# 准备存储
		print targetObj
		if isWindows:
			dirs = targetObj['name'][0:targetObj['name'].rfind("\\")]
		else:
			dirs = targetObj['name'][0:targetObj['name'].rfind("/")]
		if not os.path.exists(dirs):
			os.makedirs(dirs)
		targetObj['img'].show()
		# targetObj['img'].save(os.path.join(default_output_file ,targetObj['name'] ))



def startWork():
	global isWindows
	print 'start Work...'
	isWindows = isWindows()
	for item in bg_list:
		bgPath = os.path.join(default_bg_file , item )
		size = getImageSize(bgPath)
		# 查看res中是否存在此分辨率的资源文件
		resFileName = "%d*%d" %(size[0] , size[1])
		# print resFileName
		if os.path.exists(os.path.join(default_res_file ,resFileName)):
			workWithSingleSize( bgPath ,default_res_file , size[0] , size[1]   )
		else:
			print resFileName + " not exists ..."
			continue


	tkMessageBox.showinfo( "结果提示", "成功" )




top = Tkinter.Tk()
top.title="自动生成icons预览-oppo"

bgFilePathLabel = Tkinter.Label(top,text="背景图片文件夹路径（不填默认当前文件夹下bg文件夹）")
bgFilePathLabel.pack()

bgFilePathEntry = Tkinter.Entry(top  )
bgFilePathEntry.pack()

iconsFilePathLabel = Tkinter.Label(top,text="icons文件夹路径（不填默认当前文件夹下icons文件夹）")
iconsFilePathLabel.pack()

iconsFilePathEntry = Tkinter.Entry(top  )
iconsFilePathEntry.pack()


iconsConfigFilePathLabel = Tkinter.Label(top,text="icons筛选配置文件路径（不填默认当前文件夹下icons.conf）")
iconsConfigFilePathLabel.pack()

iconsConfigFilePathEntry = Tkinter.Entry(top  )
iconsConfigFilePathEntry.pack()

outputPathLabel = Tkinter.Label(top,text="输出文件夹目录（不填则默认当前文件夹下output文件夹）")
outputPathLabel.pack()

outputPathEntry = Tkinter.Entry(top  )
outputPathEntry.pack()

strvar = Tkinter.StringVar()
strvar.set("下一步") #初始的按钮文本

def nextStepButtonAction():
	global default_bg_file , default_icons_file , default_output_file , default_res_file , default_icons_conf_file 
	global bg_list , icons_list ,conf_list

	global strvar
	print strvar.get()
	if strvar.get() == u'下一步' :
		# tkMessageBox.showinfo( "确认信息", bgFilePathEntry.get() )
		listbLabel = Tkinter.Label(top,text="背景扫描结果")
		listbLabel.pack()
		print default_bg_file
		if bgFilePathEntry.get() == '':
			strr = default_bg_file
		else:
			strr = bgFilePathEntry.get()
		# bgList = getFileFromPath( strr , '.png')
		default_bg_file = strr 
		bgList = getFileFromPath( strr , ['.png','.jpg','.jpeg'])
		bg_list = bgList
		listb  = Tkinter.Listbox(top)  
		for item in bgList:
			# listb.insert(0,os.path.join(bgFilePathEntry.get() ,item))
			listb.insert(0,item)
		listb.pack()

		listb2Label = Tkinter.Label(top,text="icons筛选配置文件内容")
		listb2Label.pack()
		if iconsConfigFilePathEntry.get() == '':
			strr = default_icons_conf_file
		else:
			strr = iconsConfigFilePathEntry.get()
		default_icons_conf_file = strr 
		configLine = readContentFromFileByLine(strr)
		conf_list = configLine
		listb2  = Tkinter.Listbox(top)  
		for item in configLine:
			# listb1.insert(0,os.path.join(iconsFilePathEntry.get() ,item))
			listb2.insert(0,item)
		listb2.pack()

		listb1Label = Tkinter.Label(top,text="icons扫描结果")
		listb1Label.pack()
		if iconsFilePathEntry.get() == '':
			strr = default_icons_file
		else:
			strr = iconsFilePathEntry.get()
		default_icons_file = strr
		# icons_list = iconsList
		listb1  = Tkinter.Listbox(top)  
		for item in optByConf():
			# listb1.insert(0,os.path.join(iconsFilePathEntry.get() ,item))
			listb1.insert(0,item)
		listb1.pack()

		strvar.set("确认输出")
	else:
		if outputPathEntry.get() == '':
			outputfilePath = default_output_file;
		else:
			outputfilePath = outputPathEntry.get()
		default_output_file = outputfilePath
		tkMessageBox.showinfo( "确认信息", "将输出至:"  + outputfilePath +"文件夹下，请稍后..." )
		startWork()
nextStepButton = Tkinter.Button(top, textvariable=strvar, command = nextStepButtonAction)
nextStepButton.pack()



top.mainloop()


