#!/usr/bin/python
# -*- coding: UTF-8 -*-
 
import Tkinter
import tkMessageBox
import os
import codecs
from PIL import Image ,ImageFont, ImageDraw
import platform

default_bg_file = os.path.join(os.getcwd() , 'bg')
default_icons_file = os.path.join(os.getcwd() , 'icons')
default_res_file = os.path.join(os.getcwd() , 'res')
# default_icons_conf_file = os.path.join(os.getcwd() , 'iconsx3.conf')
default_output_file = os.path.join(os.getcwd() , 'output')

bg_list = []
icons_list = []
conf_list = []
system_color=''
all_size_arr = [(1080,1920),(1080,2160),(1080,2280),(1080,2340),(1080,2400),(1440,3168)]



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

	# 处理 font resize
	if frontImgResize != '':
		# 更新为按比例缩放   参照  width
		TW = float(frontImgResize[0])
		TH = TW / float(frontImg.size[0]) * float(frontImg.size[1])
		print 'TW:' 
		print TW
		print 'TH:' 
		print TH
		frontImg = frontImg.resize((int(TW),int(TH) ),Image.ANTIALIAS)


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
		targetObj = combineImg_New( targetObj["img"].convert("RGBA")  ,readAndCheckIcon(icons_list[i]).convert("RGBA"), outputFileName ,(start_width+margin_left*i,iconPositionConf["bottom_position_y"]) ,(iconPositionConf['icon_size'],iconPositionConf['icon_size']) )

	# 首页
	if isFirst:
		for i in range(4,8):
			targetObj = combineImg_New( targetObj["img"].convert("RGBA")  ,readAndCheckIcon(icons_list[i]).convert("RGBA"), outputFileName ,(start_width+margin_left*(i-4),iconPositionConf['p1_l1_y']) ,(iconPositionConf['icon_size'],iconPositionConf['icon_size']) )
	if isFirst:
		for i in range(8,12):
			targetObj = combineImg_New( targetObj["img"].convert("RGBA")  ,readAndCheckIcon(icons_list[i]).convert("RGBA"), outputFileName ,(start_width+margin_left*(i-8),iconPositionConf['p1_l2_y']) ,(iconPositionConf['icon_size'],iconPositionConf['icon_size']) )
	if isFirst:
		for i in range(12,16):
			targetObj = combineImg_New( targetObj["img"].convert("RGBA")  ,readAndCheckIcon(icons_list[i]).convert("RGBA"), outputFileName ,(start_width+margin_left*(i-12),iconPositionConf['p1_l3_y']) ,(iconPositionConf['icon_size'],iconPositionConf['icon_size']) )
	
	if size[1] == 3168:
		# 第二页
		if not isFirst:
			for i in range(16,20):
				targetObj = combineImg_New( targetObj["img"].convert("RGBA")  ,readAndCheckIcon(icons_list[i]).convert("RGBA"), outputFileName ,(start_width+margin_left*(i-16),iconPositionConf['p2_l1_y']) ,(iconPositionConf['icon_size'],iconPositionConf['icon_size']) )
		if not isFirst:
			for i in range(20,24):
				targetObj = combineImg_New( targetObj["img"].convert("RGBA")  ,readAndCheckIcon(icons_list[i]).convert("RGBA"), outputFileName ,(start_width+margin_left*(i-20),iconPositionConf['p2_l2_y']) ,(iconPositionConf['icon_size'],iconPositionConf['icon_size']) )
		if not isFirst:
			for i in range(24,28):
				targetObj = combineImg_New( targetObj["img"].convert("RGBA")  ,readAndCheckIcon(icons_list[i]).convert("RGBA"), outputFileName ,(start_width+margin_left*(i-24),iconPositionConf['p2_l3_y']) ,(iconPositionConf['icon_size'],iconPositionConf['icon_size']) )
		if not isFirst:
			for i in range(28,32):
				targetObj = combineImg_New( targetObj["img"].convert("RGBA")  ,readAndCheckIcon(icons_list[i]).convert("RGBA"), outputFileName ,(start_width+margin_left*(i-28),iconPositionConf['p2_l4_y']) ,(iconPositionConf['icon_size'],iconPositionConf['icon_size']) )


	else:
		if isFirst:
			for i in range(16,20):
				targetObj = combineImg_New( targetObj["img"].convert("RGBA")  ,readAndCheckIcon(icons_list[i]).convert("RGBA"), outputFileName ,(start_width+margin_left*(i-16),iconPositionConf['p1_l4_y']) ,(iconPositionConf['icon_size'],iconPositionConf['icon_size']) )
		

		# 第二页
		if not isFirst:
			for i in range(20,24):
				targetObj = combineImg_New( targetObj["img"].convert("RGBA")  ,readAndCheckIcon(icons_list[i]).convert("RGBA"), outputFileName ,(start_width+margin_left*(i-20),iconPositionConf['p2_l1_y']) ,(iconPositionConf['icon_size'],iconPositionConf['icon_size']) )
		if not isFirst:
			for i in range(24,28):
				targetObj = combineImg_New( targetObj["img"].convert("RGBA")  ,readAndCheckIcon(icons_list[i]).convert("RGBA"), outputFileName ,(start_width+margin_left*(i-24),iconPositionConf['p2_l2_y']) ,(iconPositionConf['icon_size'],iconPositionConf['icon_size']) )
		if not isFirst:
			for i in range(28,32):
				targetObj = combineImg_New( targetObj["img"].convert("RGBA")  ,readAndCheckIcon(icons_list[i]).convert("RGBA"), outputFileName ,(start_width+margin_left*(i-28),iconPositionConf['p2_l3_y']) ,(iconPositionConf['icon_size'],iconPositionConf['icon_size']) )
		if not isFirst:
			for i in range(32,36):
				targetObj = combineImg_New( targetObj["img"].convert("RGBA")  ,readAndCheckIcon(icons_list[i]).convert("RGBA"), outputFileName ,(start_width+margin_left*(i-32),iconPositionConf['p2_l4_y']) ,(iconPositionConf['icon_size'],iconPositionConf['icon_size']) )






	return targetObj;

def readAndCheckIcon( icon_path_str ):
	icon_path_dic = icon_path_str.split('=')
	if os.path.exists(os.path.join(default_icons_file,icon_path_dic[1])):
		# return Image.open(icon_path_dic[1])
		return addIconName(os.path.join(default_icons_file,icon_path_dic[1]),icon_path_dic[0])
	else:
		return Image.open(os.path.join(default_icons_file,'default_icon.png'))



def addIconName(icon_path,icon_name):
	print 'icon_Path:' + icon_path  +",icon_name:" + icon_name
	iconImg = Image.open(icon_path).convert('RGBA')
	bacImg = Image.new('RGBA', (iconImg.size[0] + 40, iconImg.size[1]+80), (255, 255, 255,1))
	bacImg.paste(iconImg,(20,0))
	# bacImg.show()
	draw = ImageDraw.Draw(bacImg) #修改图片
	#font = ImageFont.truetype(None, size = 40)#"C:\Users\Administrator\Desktop\每天小程序homework_day\0000\Helvetica Bold.ttf", 36) #更改文字字体
	# print 'positionx:'
	# print iconImg.size[0]/2
	# draw.text((getPositionFromCenterPointAndText('test',(bacImg.size[0], bacImg.size[1]),'./msyh.ttc',30 )[0],bacImg.size[1] - 100), 'test' , fill = (255, 255 ,255)) #利用ImageDraw的内置函数，在图片上写入文字
	# os.path.join(os.getcwd() ,'font' ,  "notosansscbold.ttf")
	font = ImageFont.truetype( os.path.join(os.getcwd() ,'font' ,  "msyh.ttc"), size = 40  ,encoding="unic" )
	position = getPositionFromCenterPointAndText(icon_name,(bacImg.size[0]/2 , bacImg.size[0] + 10 ),font )
	print 'system_color:' 
	print system_color.get()
	if system_color.get() == 'black':
		fillColor = (33,33,33)
	else:
		fillColor = (255,255,255)
	draw.text( (position[0] + 54 , iconImg.size[1] +20 ) , icon_name ,font= font , fill=fillColor)
	# bacImg.show()
	# exit()
	return bacImg

def getPositionFromCenterPointAndText(letters  , position ,font  ):
	print 'param position:'
	print position
	length = len(letters)
	# position = (1080,1920)
	im_50_blank = Image.new('RGB', position, (255, 0, 0))
	draw = ImageDraw.Draw(im_50_blank)
	# num = str(letters[random.randint(0, length - 1)])
	num = letters
	imwidth, imheight = im_50_blank.size
	font_width, font_height = draw.textsize(num, font)
	returnPosition = ((imwidth - font_width-font.getoffset(num)[0]) / 2, (imheight - font_height-font.getoffset(num)[1]) / 2)
	print 'returnPosition:'
	print returnPosition
	return returnPosition


def workWithSingleSize(bgPath ,resFilePath  ,width , height ,bg ):

	path = os.path.join(resFilePath , "%dx%d" %(height ,width ) , system_color.get() )

	resList = getFileFromPath(path , ['.png'])
	# if not os.path.exists(default_output_file):
	# 	os.makedirs(default_output_file)
	for i in range(0,len(resList)):
		item = resList[i]
		# 背景和前置文字组合
		if bg == '':
			bg = Image.open(bgPath)

		# 关闭前置文字
		# targetObj = combineImg_New(bg , Image.open(os.path.join(path ,item )) , item ,'','')
		targetObj = combineImg_New(bg , Image.new('RGBA',(bg.size[0],bg.size[1])  , (255,255,255,0)  ) , item ,'','')

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


top = Tkinter.Tk()
top.title("自动生成icons预览-oppo")

bgFilePathLabel = Tkinter.Label(top,text="背景图片文件夹路径（不填默认当前文件夹下bg文件夹）")
bgFilePathLabel.pack()

bgFilePathEntry = Tkinter.Entry(top  )
bgFilePathEntry.pack()

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
	global default_bg_file , default_icons_file , default_output_file , default_res_file  
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

		# listb2Label = Tkinter.Label(top,text="icons筛选配置文件内容")
		# listb2Label.pack()
		# if iconsConfigFilePathEntry.get() == '':
		# 	strr = default_icons_conf_file
		# else:
		# 	strr = iconsConfigFilePathEntry.get()
		# default_icons_conf_file = strr 
		# configLine = readContentFromFileByLine(default_icons_conf_file)
		# conf_list = configLine
		# listb2  = Tkinter.Listbox(top)  
		# for item in configLine:
		# 	# listb1.insert(0,os.path.join(iconsFilePathEntry.get() ,item))
		# 	listb2.insert(0,item)
		# listb2.pack()

		# listb1Label = Tkinter.Label(top,text="icons扫描结果")
		# listb1Label.pack()
		# if iconsFilePathEntry.get() == '':
		# 	strr = default_icons_file
		# else:
		# 	strr = iconsFilePathEntry.get()
		# default_icons_file = strr
		# icons_list = iconsList
		# listb1  = Tkinter.Listbox(top)  
		# for item in optByConf():
		# 	# listb1.insert(0,os.path.join(iconsFilePathEntry.get() ,item))
		# 	listb1.insert(0,item)
		# listb1.pack()

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


