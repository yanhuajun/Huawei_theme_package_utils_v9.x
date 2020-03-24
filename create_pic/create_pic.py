#!/usr/bin/python
# -*- coding: UTF-8 -*-
 
import Tkinter
import tkMessageBox
import os
import codecs
from PIL import Image ,ImageFont, ImageDraw
import platform
import xlrd
import re

shadow_size = 5
Grey = (190,190,190)
LightGray = (211,211,211)
alapblack = (211,211,211,100)
default_output_path = os.path.join(  os.getcwd()  , 'output' )


def createShadowImg(orginImg ):
	orginImg = orginImg.convert('RGBA')
	print 'createShadowImg'
	print (orginImg.format, orginImg.size, orginImg.mode)

	returnImg = Image.new('RGBA', orginImg.size,  (255,255,255,255) )
	if(orginImg.mode == 'RGB'):
		print 'orginImg is RGB'
		returnImg = Image.new('RGBA', orginImg.size, alapblack )
	else:
		print 'orginImg is RGBA'
		x = orginImg.size[0]
		y = orginImg.size[1]
		print 'orginImg size:(%d,%d)' %(x,y)
		for i in range(x):
			for k in range(y):
				color = orginImg.getpixel((i,k))
				# print 'color'
				# print color 
				color =  alapblack[:-1] + (color[3],)
				# print color 
				returnImg.putpixel((i,k)  , color )
					
	return  returnImg

def combineImg_New(baseImg , frontImg , outFileName  , frontImgCenterPoint,frontImgResize):
	target = Image.new('RGBA' , baseImg.size , (0,0,0,0))
	baseImg = baseImg.convert("RGBA")
	frontImg = frontImg.convert("RGBA")
	target.paste(baseImg , (0,0) )

	# 处理 font resize
	if frontImgResize != '':
		frontImg = frontImg.resize(frontImgResize)


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


def readConfFromFile( path):
	configList = []
	if not os.path.exists(path):
		print "config file not found"
	confFileContent = codecs.open(path ,'r','utf-8').read()
	# print confFileContent
	for line in confFileContent.split("\r"): 
		if line.startswith("#"):
			continue
		print line
		configList.append(line)
	return configList

def readConfFromExcel(excelFile):
	configList = []
	data = xlrd.open_workbook(excelFile)
	table = data.sheet_by_index(0)

	for rowNum in range(1,table.nrows):
		configItemList = []
		rowVale = table.row_values(rowNum)
		for colNum in range(table.ncols):
			# print(rowVale[colNum])
			configItemList.append(rowVale[colNum])
		# print("---------------")
		configList.append(configItemList)
	return configList


def startWork( config ):
	im = Image.open(os.path.join(os.getcwd(),'res',config[0])) # 打开文件
	im = im.convert('RGBA')
	if config[1] != '' :
		size = config[1].split(',')
		im = im.resize( (int(size[0])  , int(size[1]) ) )
	img2 = Image.open(os.path.join(os.getcwd(),'res',config[2])) 
	img2 = img2.convert('RGBA')
	size = []
	if config[3] != '' :
		size = config[3].split(',')
		img2 = img2.resize( ( int(size[2]) , int(size[3]) ) )
	img3 = createShadowImg(img2)
	targetObj = {'img':im}

	# shadow
	# targetObj = combineImg_New(im, img3 , '', ( int(size[0]) + 5 , int(size[1]) +5 ) , '' )
	targetObj = combineImg_New(targetObj['img'], img2 , '',( int(size[0]) , int(size[1])  ) ,'' )
	
	# img4 = Image.open('箭头@2x.png')
	# img5 = createShadowImg(img4)
	# targetObj = combineImg_New(targetObj['img'], img5 , '',(255,255) , '' )
	# targetObj = combineImg_New(targetObj['img'], img4 , '',(250,250) , '' )

	# img6 = Image.open('book.png')
	# img6 = img6.resize( (img6.size[0]/3,img6.size[1]/3) )
	# img7 = createShadowImg(img6)
	# targetObj = combineImg_New(targetObj['img'], img7 , '',(105,305) , '' )
	# targetObj = combineImg_New(targetObj['img'], img6 , '',(100,300) , '' )


	# img8 = Image.open('icon.png')
	# img8 = img8.resize( (img8.size[0],img8.size[1]) )
	# img9 = createShadowImg(img8)
	# targetObj = combineImg_New(targetObj['img'], img9 , '',(105,305) , '' )
	# targetObj = combineImg_New(targetObj['img'], img8 , '',(100,300) , '' )

	im = targetObj['img']
	
	# 写字
	draw = ImageDraw.Draw(im) #修改图片

	if config[4]!= '' and config[5] != '' and config[6] != '' :
		size = config[6].split(',')
		font = ImageFont.truetype("./NotoSansSC-Bold.ttf", size = int(size[3])  )#更改文字字体
		colorArr = getColorFromHex(config[5])
		centerPoint = getPositionFromCenterPointAndText( config[4] , ( int(config[1].split(',')[0])  ,int(config[1].split(',')[1])  ) , "./NotoSansSC-Bold.ttf" ,  int(size[3])  ) 
		draw.text( (centerPoint[0] , int(size[1]) ) , config[4],font= font ,  fill =  ( int(colorArr[0]) , int(colorArr[1]) , int(colorArr[2]) ) ) #利用ImageDraw的内置函数，在图片上写入文字
	if config[7]!= '' and config[8] != '' and config[9] != '' :
		size = config[9].split(',')
		font = ImageFont.truetype("./NotoSansSC-Bold.ttf", size = int(size[3])  )#更改文字字体
		colorArr = getColorFromHex(config[8])
		centerPoint = getPositionFromCenterPointAndText( config[7] , ( int(config[1].split(',')[0])  ,int(config[1].split(',')[1])  ) , "./NotoSansSC-Bold.ttf" ,  int(size[3])  ) 
		draw.text( (centerPoint[0] , int(size[1]) )  , config[7],font= font ,  fill =  ( int(colorArr[0]) , int(colorArr[1]) , int(colorArr[2]) ) ) #利用ImageDraw的内置函数，在图片上写入文字
	if config[10]!= '' and config[11] != '' and config[12] != '' :
		size = config[12].split(',')
		font = ImageFont.truetype("./NotoSansSC-Bold.ttf", size = int(size[3])  )#更改文字字体
		colorArr = getColorFromHex(config[11])
		centerPoint = getPositionFromCenterPointAndText( config[10] , ( int(config[1].split(',')[0])  ,int(config[1].split(',')[1])  ) , "./NotoSansSC-Bold.ttf" ,  int(size[3])  ) 
		draw.text( (centerPoint[0] , int(size[1]) )   , config[10],font= font ,  fill =  ( int(colorArr[0]) , int(colorArr[1]) , int(colorArr[2]) ) ) #利用ImageDraw的内置函数，在图片上写入文字
	
	# im.show()
	if not os.path.exists( default_output_path ) :
		os.makedirs(default_output_path)
	im.save(os.path.join( default_output_path  ,config[13] )  )

def getColorFromHex(tmp):
	tmp = tmp[1:]
	opt = re.findall(r'(.{2})',tmp) #将字符串两两分割
	strs = ""						#用以存放最后结果
	for i in range (0, len(opt)):	#for循环，遍历分割后的字符串列表
		strs += str(int(opt[i], 16)) + ","	#将结果拼接成12，12，12格式
	print("转换后的RGB数值为：")
	strs = strs[0:-1]
	print(strs)				#输出最后结果，末尾的","不打印
	return strs.split(',')
def getPositionFromCenterPointAndText(letters  , position ,font ,fontSize ):
	length = len(letters)
	# position = (1080,1920)
	im_50_blank = Image.new('RGB', position, (255, 0, 0))
	draw = ImageDraw.Draw(im_50_blank)
	# num = str(letters[random.randint(0, length - 1)])
	num = letters
	font = ImageFont.truetype(font, fontSize)
	imwidth, imheight = im_50_blank.size
	font_width, font_height = draw.textsize(num, font)
	returnPosition = ((imwidth - font_width-font.getoffset(num)[0]) / 2, (imheight - font_height-font.getoffset(num)[1]) / 2)
	print 'returnPosition:'
	print returnPosition
	return returnPosition


# start
print 'start...'
# configList = readConfFromFile(os.path.join(os.getcwd() ,'config.conf'))
configList = readConfFromExcel( os.path.join( os.getcwd() ,'conf.xlsx' ) )
for item in configList:
	# print item 
	startWork(item )







