#!/usr/bin/python
# -*- coding: UTF-8 -*-
 
import Tkinter
import tkMessageBox
import os
import codecs
from PIL import Image
import platform

default_icons_file = os.path.join(os.getcwd() , 'icons')
default_res_file = os.path.join(os.getcwd() , 'res')
default_output_file = os.path.join(os.getcwd() , 'output')
default_width = 180
default_height = 180

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
	arr = []
	if isWindows():
		arr = content.split('\r\n')
	else:
		arr = content.split('\n')
	for item in arr:
		if item != '' and not item.startswith('#') and  item.find("=") >= 0 :
			listArr.append(os.path.join(default_icons_file , item.split('=')[1] ))
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
		print "item:" + item 
		filePath = os.path.join(default_icons_file , item.split('=')[1] )
		print "filePath:" + filePath
		if os.path.exists(filePath):
			print 'exists'
			printArr.append(item)
			icons_list.append(filePath)
		else:
			print 'not exists'
		# printArr.append(item)
		# icons_list.append(filePath)

	return printArr 


def combineImg_New(baseImg , frontImg , outFileName  , frontImgCenterPoint,frontImgResize):
	target = Image.new('RGBA' , baseImg.size , (0,0,0,0))
	baseImg = baseImg.convert("RGBA")
	frontImg = frontImg.convert("RGBA")
	target.paste(baseImg , (0,0) )

	# 处理 font resize
	if frontImgResize != '':
		frontImg = frontImg.resize(frontImgResize,Image.ANTIALIAS)


	# 处理粘贴坐标
	if frontImgCenterPoint == '':
		frontImgCenterPoint = (0,0)
	else:
		frontImgCenterPoint = (frontImgCenterPoint[0]-frontImg.size[0]/2  , frontImgCenterPoint[1]-frontImg.size[1] / 2)

	target.paste(frontImg , frontImgCenterPoint ,frontImg)

	targetObj = {}
	targetObj['img'] = target
	# targetObj['name'] = os.path.join(default_output_file ,outFileName )
	return targetObj 

def loadIconPositionConf(size):
	width=size[0]
	height=size[1]
	print "pre to load %dx%d icon position config file..." %(height , width )
	content = codecs.open(os.path.join(default_res_file,"%dx%d"%(height,width),"icon_position.conf")).read()
	arr = []
	iconPositionConf = {}
	if isWindows():
		arr = content.split("\r\n")
	else:
		arr = content.split("\n")
	for item in arr:
		if item == '':
			continue;
		itemArr = item.split("=")
		print "itemArr[0]=%s , itemArr[1]=%s" %(itemArr[0] , itemArr[1])
		iconPositionConf[itemArr[0]] = int(itemArr[1])
	print iconPositionConf
	return iconPositionConf


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


def iconPaste(targetObj,outputFileName ,isFirst,size):
	# 根据分辨率读取iconconfig
	global icons_list
	if size[1] == 3168:
		icons_list = readContentFromFileByLine(os.path.join(os.getcwd(),'iconsx3.conf'))
	else:
		icons_list = readContentFromFileByLine(os.path.join(os.getcwd(),'iconsx4.conf'))
	iconPositionConf = loadIconPositionConf(size)

	start_width = iconPositionConf['start_width']
	margin_left = iconPositionConf['margin_left']


	# 底部通用
	for i in range(0,4):
		targetObj = combineImg_New( targetObj["img"].convert("RGBA")  ,Image.open(icons_list[i]).convert("RGBA"), outputFileName ,(start_width+margin_left*i,iconPositionConf["bottom_position_y"]) ,(iconPositionConf['icon_size'],iconPositionConf['icon_size']) )

	# 首页
	if isFirst:
		for i in range(4,8):
			targetObj = combineImg_New( targetObj["img"].convert("RGBA")  ,Image.open(icons_list[i]).convert("RGBA"), outputFileName ,(start_width+margin_left*(i-4),iconPositionConf['p1_l1_y']) ,(iconPositionConf['icon_size'],iconPositionConf['icon_size']) )
	if isFirst:
		for i in range(8,12):
			targetObj = combineImg_New( targetObj["img"].convert("RGBA")  ,Image.open(icons_list[i]).convert("RGBA"), outputFileName ,(start_width+margin_left*(i-8),iconPositionConf['p1_l2_y']) ,(iconPositionConf['icon_size'],iconPositionConf['icon_size']) )
	if isFirst:
		for i in range(12,16):
			targetObj = combineImg_New( targetObj["img"].convert("RGBA")  ,Image.open(icons_list[i]).convert("RGBA"), outputFileName ,(start_width+margin_left*(i-12),iconPositionConf['p1_l3_y']) ,(iconPositionConf['icon_size'],iconPositionConf['icon_size']) )
	
	if size[1] == 3168:
		# 第二页
		if not isFirst:
			for i in range(16,20):
				targetObj = combineImg_New( targetObj["img"].convert("RGBA")  ,Image.open(icons_list[i]).convert("RGBA"), outputFileName ,(start_width+margin_left*(i-16),iconPositionConf['p2_l1_y']) ,(iconPositionConf['icon_size'],iconPositionConf['icon_size']) )
		if not isFirst:
			for i in range(20,24):
				targetObj = combineImg_New( targetObj["img"].convert("RGBA")  ,Image.open(icons_list[i]).convert("RGBA"), outputFileName ,(start_width+margin_left*(i-20),iconPositionConf['p2_l2_y']) ,(iconPositionConf['icon_size'],iconPositionConf['icon_size']) )
		if not isFirst:
			for i in range(24,28):
				targetObj = combineImg_New( targetObj["img"].convert("RGBA")  ,Image.open(icons_list[i]).convert("RGBA"), outputFileName ,(start_width+margin_left*(i-24),iconPositionConf['p2_l3_y']) ,(iconPositionConf['icon_size'],iconPositionConf['icon_size']) )
		if not isFirst:
			for i in range(28,32):
				targetObj = combineImg_New( targetObj["img"].convert("RGBA")  ,Image.open(icons_list[i]).convert("RGBA"), outputFileName ,(start_width+margin_left*(i-28),iconPositionConf['p2_l4_y']) ,(iconPositionConf['icon_size'],iconPositionConf['icon_size']) )


	else:
		if isFirst:
			for i in range(16,20):
				targetObj = combineImg_New( targetObj["img"].convert("RGBA")  ,Image.open(icons_list[i]).convert("RGBA"), outputFileName ,(start_width+margin_left*(i-16),iconPositionConf['p1_l4_y']) ,(iconPositionConf['icon_size'],iconPositionConf['icon_size']) )
		

		# 第二页
		if not isFirst:
			for i in range(20,24):
				targetObj = combineImg_New( targetObj["img"].convert("RGBA")  ,Image.open(icons_list[i]).convert("RGBA"), outputFileName ,(start_width+margin_left*(i-20),iconPositionConf['p2_l1_y']) ,(iconPositionConf['icon_size'],iconPositionConf['icon_size']) )
		if not isFirst:
			for i in range(24,28):
				targetObj = combineImg_New( targetObj["img"].convert("RGBA")  ,Image.open(icons_list[i]).convert("RGBA"), outputFileName ,(start_width+margin_left*(i-24),iconPositionConf['p2_l2_y']) ,(iconPositionConf['icon_size'],iconPositionConf['icon_size']) )
		if not isFirst:
			for i in range(28,32):
				targetObj = combineImg_New( targetObj["img"].convert("RGBA")  ,Image.open(icons_list[i]).convert("RGBA"), outputFileName ,(start_width+margin_left*(i-28),iconPositionConf['p2_l3_y']) ,(iconPositionConf['icon_size'],iconPositionConf['icon_size']) )
		if not isFirst:
			for i in range(32,36):
				targetObj = combineImg_New( targetObj["img"].convert("RGBA")  ,Image.open(icons_list[i]).convert("RGBA"), outputFileName ,(start_width+margin_left*(i-32),iconPositionConf['p2_l4_y']) ,(iconPositionConf['icon_size'],iconPositionConf['icon_size']) )

	return targetObj;

def workWithSingleSize(bgPath ,resFilePath  ,width , height ,bg ):

	path = os.path.join(resFilePath , "%dx%d" %(height ,width ) , resize_mode.get() )

	resList = getFileFromPath(path , ['.png','.PNG'])
	# if not os.path.exists(default_output_file):
	# 	os.makedirs(default_output_file)
	for i in range(0,len(resList)):
		item = resList[i]
		# 背景和前置文字组合
		if bg == '':
			bg = Image.open(bgPath)
		targetObj = combineImg_New(bg , Image.open(os.path.join(path ,item )) , item ,'','')

		# icon和 以上组合
		print "item:" + item 
		if item.find('preview_menu') >= 0 :
			isFirst = True
		else:
			isFirst = False
		targetObj = iconPaste(targetObj,item ,isFirst,(width,height))

		# 准备存储
		print targetObj
		# if isWindows:
		# 	dirs = targetObj['name'][0:targetObj['name'].rfind("\\")]
		# else:
		# 	dirs = targetObj['name'][0:targetObj['name'].rfind("/")]
		dirs = os.path.join( default_output_file ,"drawable-xxhdpi-%dx%d" %(height , width )  )
		if dirs.find('drawable-xxhdpi-1920x1080') >= 0:
			dirs = dirs.replace('drawable-xxhdpi-1920x1080' ,'drawable-xxhdpi')
		if not os.path.exists(dirs):
			os.makedirs(dirs)
		outputFilePath = os.path.join(dirs , item)
		# targetObj['img'].show()
		targetObj['img'].save(   outputFilePath   )


def findMostRelatedSize(existsSizeArr  ,size):
	size = size[0]*size[1]
	tmparr = {}
	minSize = {};
	for item in existsSizeArr:
		tmparr['%dx%d' %(item[0],item[1])] = item[0]*item[1]
	for (key,value) in tmparr.items():
		cha = abs(value - size)
		if len(minSize) ==0:
			minSize['name'] = key
			minSize['cha'] = cha
		else:
			if cha < minSize['cha']:
				minSize['name'] = key
				minSize['cha'] = cha
	print 'minSize[name]:' + minSize['name'] + (',minSize[cha]:%d' % minSize['cha'])
	return ( int(minSize['name'].split('x')[0])  ,int(minSize['name'].split('x')[1]) )

def startWork():
	size_arr = []
	print 'start Work...'
	for item in bg_list:
		bgPath = os.path.join(default_bg_file , item )
		size = getImageSize(bgPath)
		size_arr.append(size)
		# 查看res中是否存在此分辨率的资源文件
		resFileName = "%dx%d" %(size[1] , size[0])
		# print resFileName
		if os.path.exists(os.path.join(default_res_file ,resFileName)):
			workWithSingleSize( bgPath ,default_res_file , size[0] , size[1] , '' )
		else:
			print resFileName + " not exists ..."
			continue

	print 'start match bg img  , and cut ...'
	print 'start clean all_size_arr'
	print all_size_arr
	for item in size_arr:
		print item 
		print 'workfinish and remove'
		all_size_arr.remove(item )
	for item in all_size_arr:
		size = findMostRelatedSize(size_arr , item)
		print size 
		bgFilePath = getBgFromSize(size);
		if bgFilePath == 'fail':
			print 'can not find matched bg file ... continue'
			continue
		cuttedImg = cutPic( Image.open( bgFilePath ) ,item)
		workWithSingleSize( '' ,default_res_file , cuttedImg.size[0] , cuttedImg.size[1]  ,  cuttedImg )

	tkMessageBox.showinfo( "结果提示", "成功" )

def getBgFromSize( size ):
	print 'getBgFromSize,size:'
	print size 
	for item in bg_list:
		path = os.path.join(default_bg_file  , item )
		print 'path:' + path 
		img = Image.open(path)
		print img.size 
		if img.size == size :
			print 'find matched bg ,bgpath' + path 
			return path
	return 'fail'

def cutPic(orginPic  , size ):
	orginSize = orginPic.size
	width = orginSize[0] - size[0] 
	height = orginSize[1] - size[1]
	x = (orginSize[0] - size[0]) / 2
	y = (orginSize[1] - size[1]) / 2
	cutSize =(x,y,size[0] + x,size[1] + y )
	print 'cutSize:'
	print cutSize 
	orginPic = orginPic.crop(cutSize)
	# orginPic.show()
	print 'cutted pic size:'
	print orginPic.size
	return orginPic


def startWork(iconsPath ,outputPath ,width ,height ,resizeMode):
	print 'iconsFilePath:' + iconsPath
	print 'outputFilePath:' + outputPath
	print 'width:%d'  %width
	print 'height:%d'  %height
	print 'resize_mode:%s'  %  resizeMode

	iconsList = getFileFromPath(iconsPath,[])
	if len(iconsList) == 0:
		return 
	if not os.path.exists(outputPath):
		os.makedirs(outputPath)
	for icon in iconsList:
		image = Image.open(os.path.join( iconsPath , icon ) )
		image = image.convert('RGBA')
		if resizeMode == 'A':
			image = image.resize( (int(width)  ,int(height)) ,Image.ANTIALIAS)
			image.save( os.path.join( outputPath , icon ) )
		else:
			bgImage = Image.open( os.path.join( default_res_file, 'bg.png' ) )
			bgImage = bgImage.convert('RGBA')
			bgImage = bgImage.resize( (int(width)  ,int(height)) ,Image.ANTIALIAS )
			targetObj = combineImg_New(bgImage , image ,icon  ,'' , '')
			targetObj['img'].save( os.path.join( outputPath , icon ) )


# start 
top = Tkinter.Tk()
top.title("icons大小批量修改-oppo")

iconsFilePathLabel = Tkinter.Label(top,text="icons文件夹路径（不填默认当前文件夹下icons文件夹）")
iconsFilePathLabel.pack()

iconsFilePathEntry = Tkinter.Entry(top  )
iconsFilePathEntry.pack()



outputPathLabel = Tkinter.Label(top,text="输出文件夹目录（不填则默认当前文件夹下output文件夹）")
outputPathLabel.pack()
outputPathEntry = Tkinter.Entry(top  )
outputPathEntry.pack()

widthLabel = Tkinter.Label(top,text="width（默认180）")
widthLabel.pack()

widthEntry = Tkinter.Entry(top  )
widthEntry.pack()

heightLabel = Tkinter.Label(top,text="height（默认180）")
heightLabel.pack()

heightEntry = Tkinter.Entry(top  )
heightEntry.pack()




var = Tkinter.StringVar()
var.set('A')
resize_mode=var
# l = Tkinter.Label(top, bg='yellow', width=20, text='empty')
l = Tkinter.Label(top,  text='请选择文字颜色（A、等比例放大 B、周围留白）默认等比')
l.pack()


def print_selection():
	global resize_mode
	resize_mode = var
	# l.config(text='you have selected ' + var.get())
Tkinter.Radiobutton(top, text='A.等比例放大',variable=var, value='A',command=print_selection).pack()
# Tkinter.Radiobutton(top, text='B.周围留白',variable=var, value='B',command=print_selection).pack()


strvar = Tkinter.StringVar()
strvar.set("确认") #初始的按钮文本
def nextStepButtonAction():
	iconsFilePath  ='' 
	outputFilePath ='' 
	width ='' 
	height = '' 
	if iconsFilePathEntry.get() == '':
		iconsFilePath = default_icons_file 
	else:
		iconsFilePath = iconsFilePathEntry.get()
	if outputPathEntry.get() == '':
		outputFilePath = default_output_file
	else:
		outputFilePath = outputPathEntry.get()
	if widthEntry.get() == '':
		width = default_width
	else:
		width = widthEntry.get()
	if heightEntry.get() == '':
		height = default_height
	else:
		height = heightEntry.get()
	startWork(iconsFilePath , outputFilePath , int(width)  ,int(height)  ,resize_mode.get())
	tkMessageBox.showinfo( "成功信息", "已输出至："  + outputFilePath.decode('gbk').encode('utf-8') +"文件夹下..." )




nextStepButton = Tkinter.Button(top, textvariable=strvar, command = nextStepButtonAction)
nextStepButton.pack()



top.mainloop()


