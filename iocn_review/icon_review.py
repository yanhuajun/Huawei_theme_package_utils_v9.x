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
system_color=''



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

# def combineImg(img1Path ,img2Path ,outFileName ,inputBox ):
# 	# print "ready to combine img  : " + img1Path +" , and :" + img2Path

# 	base_img = img2Path # Image.open(img2Path)
# 	#新建透明底图，大小和手机图一样，mode使用RGBA，保留Alpha透明度，颜色为透明
# 	#Image.new(mode, size, color=0)，color可以用tuple表示，分别表示RGBA的值
# 	target = Image.new('RGBA', base_img.size, (0, 0, 0, 0))
# 	if inputBox == '':
# 		box = (0, 0, base_img.size[0], base_img.size[1]) #区域
# 	else:
# 		box = inputBox
# 	region = img1Path # Image.open(img1Path)
# 	# region = region.rotate(180) #旋转180度
# 	#确保图片是RGBA格式，大小和box区域一样
# 	region = region.convert("RGBA")
# 	region = region.resize((box[2] - box[0], box[3] - box[1]))
# 	#先将狐狸像合成到底图上
# 	target.paste(region,box)
# 	#将手机图覆盖上去，中间透明区域将狐狸像显示出来。
# 	target.paste(base_img,(0,0),base_img) #第一个参数表示需要粘贴的图像，中间的是坐标，最后是一个是mask图片，用于指定透明区域，将底图显示出来。
# 	# target.show()
# 	# target.save(os.path.join(default_output_file ,outFileName ))  # 保存图片

# 	targetObj = {}
# 	targetObj['img'] = target
# 	targetObj['name'] = os.path.join(default_output_file ,outFileName )
# 	return targetObj 

def combineImg_New(baseImg , frontImg , outFileName  , frontImgCenterPoint,frontImgResize):
	target = Image.new('RGBA' , baseImg.size , (0,0,0,0))
	baseImg = baseImg.convert("RGBA")
	frontImg = frontImg.convert("RGBA")
	target.paste(baseImg , (0,0) )
	# 处理粘贴坐标
	if frontImgCenterPoint == '':
		frontImgCenterPoint = (0,0)
	else:
		frontImgCenterPoint = (frontImgCenterPoint[0]-frontImg.size[0]/2  , frontImgCenterPoint[1]-frontImg.size[1] / 2)

	if frontImgResize != '':
		frontImg = frontImg.resize(frontImgResize)
	target.paste(frontImg , frontImgCenterPoint ,frontImg)

	targetObj = {}
	targetObj['img'] = target
	# targetObj['name'] = os.path.join(default_output_file ,outFileName )
	return targetObj 



def iconPaste1440_3168(targetObj,outputFileName ,isFirst):
	# print "icon:" + icons_list[0]		# icon.show()
	# targetObj = combineImg_New( targetObj["img"].convert("RGBA")  ,Image.open(icons_list[0]).convert("RGBA"), item ,(200,2900) ,(180,180) )
	# # targetObj = combineImg(Image.open(bgPath) ,  icon, item ,'')
	# targetObj = combineImg_New( targetObj["img"].convert("RGBA")  ,Image.open(icons_list[1]).convert("RGBA"), item ,(200+330*1,2900) ,(180,180) )
	# targetObj = combineImg_New( targetObj["img"].convert("RGBA")  ,Image.open(icons_list[3]).convert("RGBA"), item ,(200+330*2,2900) ,(180,180) )
	# targetObj = combineImg_New( targetObj["img"].convert("RGBA")  ,Image.open(icons_list[4]).convert("RGBA"), item ,(200+330*4,2900) ,(180,180) )

	start_width = 210
	margin_left = 330


	# 首页
	for i in range(0,4):
		targetObj = combineImg_New( targetObj["img"].convert("RGBA")  ,Image.open(icons_list[i]).convert("RGBA"), outputFileName ,(start_width+margin_left*i,2873) ,(180,180) )

	if isFirst:
		for i in range(4,8):
			targetObj = combineImg_New( targetObj["img"].convert("RGBA")  ,Image.open(icons_list[i]).convert("RGBA"), outputFileName ,(start_width+margin_left*(i-4),1490) ,(180,180) )

	if isFirst:
		for i in range(8,12):
			targetObj = combineImg_New( targetObj["img"].convert("RGBA")  ,Image.open(icons_list[i]).convert("RGBA"), outputFileName ,(start_width+margin_left*(i-8),1896) ,(180,180) )
	if isFirst:
		for i in range(12,16):
			targetObj = combineImg_New( targetObj["img"].convert("RGBA")  ,Image.open(icons_list[i]).convert("RGBA"), outputFileName ,(start_width+margin_left*(i-12),2303) ,(180,180) )


	# 第二页
	if not isFirst:
		for i in range(16,20):
			targetObj = combineImg_New( targetObj["img"].convert("RGBA")  ,Image.open(icons_list[i]).convert("RGBA"), outputFileName ,(start_width+margin_left*(i-16),271) ,(180,180) )
	if not isFirst:
		for i in range(20,24):
			targetObj = combineImg_New( targetObj["img"].convert("RGBA")  ,Image.open(icons_list[i]).convert("RGBA"), outputFileName ,(start_width+margin_left*(i-20),677) ,(180,180) )
	if not isFirst:
		for i in range(24,28):
			targetObj = combineImg_New( targetObj["img"].convert("RGBA")  ,Image.open(icons_list[i]).convert("RGBA"), outputFileName ,(start_width+margin_left*(i-24),1083) ,(180,180) )
	if not isFirst:
		for i in range(28,32):
			targetObj = combineImg_New( targetObj["img"].convert("RGBA")  ,Image.open(icons_list[i]).convert("RGBA"), outputFileName ,(start_width+margin_left*(i-28),1489) ,(180,180) )




	return targetObj;

def workWithSingleSize(bgPath ,resFilePath  ,width , height ):

	path = os.path.join(resFilePath , "%dx%d" %(height ,width ) , system_color.get() )

	resList = getFileFromPath(path , ['.png'])
	# if not os.path.exists(default_output_file):
	# 	os.makedirs(default_output_file)
	for i in range(0,len(resList)):
		item = resList[i]
		# 背景和前置文字组合
		targetObj = combineImg_New(Image.open(bgPath) , Image.open(os.path.join(path ,item )) , item ,'','')

		# icon和 以上组合
		if height == 3168:
			print "item:" + item 
			if item.find('preview_menu') >= 0 :
				isFirst = True
			else:
				isFirst = False
			targetObj = iconPaste1440_3168(targetObj,item ,isFirst)
		elif height == 1080:
			pass

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



def startWork():
	print 'start Work...'
	for item in bg_list:
		bgPath = os.path.join(default_bg_file , item )
		size = getImageSize(bgPath)
		# 查看res中是否存在此分辨率的资源文件
		resFileName = "%dx%d" %(size[1] , size[0])
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

var = Tkinter.StringVar()
var.set('white')
system_color=var
# l = Tkinter.Label(top, bg='yellow', width=20, text='empty')
l = Tkinter.Label(top,  text='请选择文字颜色（A、白色 B、黑色）默认白色')
l.pack()
def print_selection():
	global system_color
	system_color = var
	# l.config(text='you have selected ' + var.get())
Tkinter.Radiobutton(top, text='白色',variable=var, value='white',command=print_selection).pack()
Tkinter.Radiobutton(top, text='黑色',variable=var, value='black',command=print_selection).pack()


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


