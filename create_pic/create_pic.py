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
import random

import textwrap

shadow_size = 5
Grey = (190,190,190)
LightGray = (211,211,211)
alapblack = (211,211,211,100)
default_output_path = os.path.join(  os.getcwd()  , 'output' )
lineConfig = ''

backMode = {
	"text":[{
		"size":40,
		"ttf":os.path.join(os.getcwd() ,'font' ,  "msyh.ttc"),
		"color":"30,30,30",
		"position":(90,580),
		"frame":(900,40),
	},{
		"size":40,
		"ttf":os.path.join(os.getcwd() ,'font' ,  "msyh.ttc"),
		"color":"30,30,30",
		"position":(90,650),
		"frame":(900,40),
	},{
		"size":40,
		"ttf":os.path.join(os.getcwd() ,'font' ,  "msyh.ttc"),
		"color":"30,30,30",
		"position":(90,720),
		"frame":(900,40),
	},{
		"size":40,
		"ttf":os.path.join(os.getcwd() ,'font' ,  "msyh.ttc"),
		"color":"30,30,30",
		"position":(90,790),
		"frame":(900,40),
	}]
}


def getFileFromPath(path,prefix,suffix):
	print "getFileFrom:" + path
	fileList = []
	filenames = os.listdir(path)
	for filename in filenames:
		# print "suffix:" + filename[filename.rfind('.'):len(filename)]
		# if filename[filename.rfind('.'):len(filename)] in suffix :
		# 	fileList.append(filename)
		# else:
			# continue
		if len(suffix ) == 0 and len(prefix) == 0:
			# 没有前缀后缀匹配
			fileList.append(filename)
		else:
			for item in suffix:
				if filename.endswith(item):
					fileList.append(filename)
					continue
			for prefix_item in prefix:
				if filename.startswith(prefix_item):
					fileList.append(filename)
					continue
	print "fileList:"
	print fileList
	return fileList

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

def randomName(bgName,prefixArr):
	if bgName != '' :
		return bgName
	else:
		fileList = getFileFromPath( os.path.join(os.getcwd(),'res') , prefixArr , [] )
		return fileList[random.randint(0,len(fileList)-1)]


def circle_corner(img, radii):
    """
    圆角处理
    :param img: 源图象。
    :param radii: 半径，如：30。
    :return: 返回一个圆角处理后的图象。
    """

    # 画圆（用于分离4个角）
    circle = Image.new('L', (radii * 2, radii * 2), 0)  # 创建一个黑色背景的画布
    draw = ImageDraw.Draw(circle)
    draw.ellipse((0, 0, radii * 2, radii * 2), fill=255)  # 画白色圆形

    # 原图
    img = img.convert("RGBA")
    w, h = img.size

    # 画4个角（将整圆分离为4个部分）
    alpha = Image.new('L', img.size, 255)
    alpha.paste(circle.crop((0, 0, radii, radii)), (0, 0))  # 左上角
    alpha.paste(circle.crop((radii, 0, radii * 2, radii)), (w - radii, 0))  # 右上角
    alpha.paste(circle.crop((radii, radii, radii * 2, radii * 2)), (w - radii, h - radii))  # 右下角
    alpha.paste(circle.crop((0, radii, radii, radii * 2)), (0, h - radii))  # 左下角
    # alpha.show()

    img.putalpha(alpha)  # 白色区域透明可见，黑色区域不可见
    return img



def startWork( config ):
	global lineConfig 
	lineConfig = config 
	im = Image.open(os.path.join(os.getcwd(),'res',randomName(config[0] , ['bg']) )) # 打开文件
	im = im.convert('RGBA')
	if config[1] != '' :
		size = config[1].split(',')
		im = im.resize( (int(size[0])  , int(size[1]) ) ,Image.ANTIALIAS )
	img2 = Image.open(os.path.join(os.getcwd(),'res',randomName(config[2] , ['front'])  )) 
	img2 = img2.convert('RGBA')
	size = []
	if config[3] != '' :
		size = config[3].split(',')
		img2 = img2.resize( ( int(size[2]) , int(size[3]) ) ,Image.ANTIALIAS)
	
	targetObj = {'img':im}


	# 切圆角
	if config[23] == 1.0:
		img2 = circle_corner(img2  , int(config[24]) );

	# shadow
	print 'is front img shadow?'
	print 'config[14]:'
	print config[14]
	if config[14] == 1.0 :
		print 'get shadow...' 
		img3 = createShadowImg(img2)
		targetObj = combineImg_New(im, img3 , '', ( int(size[0]) + 10 , int(size[1]) +10 ) , '' )
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
		if config[19] == '':
			font = ImageFont.truetype(os.path.join(os.getcwd() ,'font' ,  "msyh.ttc"), size = int(size[3])  )#更改文字字体
		else:
			font = ImageFont.truetype(os.path.join(os.getcwd() ,'font' ,  "./%s" % config[19] ), size = int(size[3])  )#更改文字字体

		colorArr = getColorFromHex(config[5])
		centerPoint = getPositionFromCenterPointAndText( config[4] , ( int(config[1].split(',')[0])  ,int(config[1].split(',')[1])  ) , os.path.join(os.getcwd() ,'font' ,  "notosansscbold.ttf" ),  int(size[3])  ) 
		draw.text( (centerPoint[0] , int(size[1]) ) , config[4],font= font ,  fill =  ( int(colorArr[0]) , int(colorArr[1]) , int(colorArr[2]) ) ) #利用ImageDraw的内置函数，在图片上写入文字
	if config[7]!= '' and config[8] != '' and config[9] != '' :
		size = config[9].split(',')
		if config[20] == '':
			font = ImageFont.truetype(os.path.join(os.getcwd(),'font' ,  "notosansscbold.ttf"), size = int(size[3])  )#更改文字字体
		else:
			font = ImageFont.truetype(os.path.join(os.getcwd() ,'font' ,  "./%s" % config[20] ), size = int(size[3])  )#更改文字字体
		colorArr = getColorFromHex(config[8])
		centerPoint = getPositionFromCenterPointAndText( config[7] , ( int(config[1].split(',')[0])  ,int(config[1].split(',')[1])  ) , os.path.join(os.getcwd() ,'font' ,  "notosansscbold.ttf" ),  int(size[3])  ) 
		draw.text( (centerPoint[0] , int(size[1]) )  , config[7],font= font ,  fill =  ( int(colorArr[0]) , int(colorArr[1]) , int(colorArr[2]) ) ) #利用ImageDraw的内置函数，在图片上写入文字
		# myfont = ImageFont.truetype(os.path.join(os.getcwd() , "notosansscbold.ttf", size = int(size[3]))
		# text = config[7];
		# tend = len(text)
		# while True:
		# 	text_size = draw.textsize(text[:tend], font=myfont) #文本图层的尺寸
		# 	#print(text_size)
		# 	if text_size[0] <= size[2]:
		# 		break
		# 	else:
		# 		tend -= 1 #文本太长，调整文本长度
		# draw.text(  (centerPoint[0] , int(size[1]) )   , text[:tend], font=myfont , fill =  ( int(colorArr[0]) , int(colorArr[1]) , int(colorArr[2]) )  )


	if config[10]!= '' and config[11] != '' and config[12] != '' :
		size = config[12].split(',')
		if config[21] == '':
			font = ImageFont.truetype(os.path.join(os.getcwd() ,'font' ,  "notosansscbold.ttf"), size = int(size[3])  )#更改文字字体
		else:
			font = ImageFont.truetype(os.path.join(os.getcwd() ,'font' ,  "./%s" % config[21] ), size = int(size[3])  )#更改文字字体

		colorArr = getColorFromHex(config[11])
		centerPoint = getPositionFromCenterPointAndText( config[10] , ( int(config[1].split(',')[0])  ,int(config[1].split(',')[1])  ) , os.path.join(os.getcwd() ,'font' ,  "notosansscbold.ttf") ,  int(size[3])  ) 
		draw.text( (centerPoint[0] , int(size[1]) )   , config[10],font= font ,  fill =  ( int(colorArr[0]) , int(colorArr[1]) , int(colorArr[2]) ) ) #利用ImageDraw的内置函数，在图片上写入文字
	if config[15]!= '' and config[16] != '' and config[17] != '' :
		size = config[17].split(',')
		if config[22] == '':
			font = ImageFont.truetype(os.path.join(os.getcwd() ,'font' ,  "notosansscbold.ttf" ), size = int(size[3])  )#更改文字字体
		else:
			font = ImageFont.truetype(os.path.join(os.getcwd() ,'font' ,  "%s" % config[22] ) , size = int(size[3])  )#更改文字字体
		colorArr = getColorFromHex(config[16])
		centerPoint = getPositionFromCenterPointAndText( config[15] , ( int(config[1].split(',')[0])  ,int(config[1].split(',')[1])  ) , os.path.join(os.getcwd() ,'font' , "notosansscbold.ttf" ),  int(size[3])  ) 
		draw.text( (centerPoint[0] , int(size[1]) )   , config[15],font= font ,  fill =  ( int(colorArr[0]) , int(colorArr[1]) , int(colorArr[2]) ) ) #利用ImageDraw的内置函数，在图片上写入文字
	print 'start write_line...'
	print 'backMode:' 
	print backMode
	print 'backMode["text"]'
	print backMode["text"]
	if config[18] != '':
		im = write_text(im  ,config[18], backMode["text"])
	

	# im.show()
	if not os.path.exists( default_output_path ) :
		os.makedirs(default_output_path)
	# im.show()
	im.save(os.path.join( default_output_path  ,config[13] )  )

def getColorFromHex(tmp):
	tmp = tmp[1:]
	opt = re.findall(r'(.{2})',tmp) #将字符串两两分割
	strs = ""						#用以存放最后结果
	for i in range (0, len(opt)):	#for循环，遍历分割后的字符串列表
		strs += str(int(opt[i], 16)) + ","	#将结果拼接成12，12，12格式
	print(u"转换后的RGB数值为：")
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

def write_text(img , text, tmodeList):
	#写文本
	print 'tmodeList : '
	print tmodeList
	tlist = text.split("\n")
	mnum = 0
	draw = ImageDraw.Draw(img)
	for t in tlist:
		tbegin = 0
		tend = len(t)
		while True:
			img, tend = write_line(img, t[tbegin:tend], tmodeList[mnum])
			mnum += 1
			if tbegin + tend == len(t) or mnum == len(tmodeList):
				break
			else:
				tbegin = tbegin + tend
				tend = len(t)
		if mnum == len(tmodeList):
			break
	return img

def write_line(backimg ,text, tmode):
#给单个文本框填充数据
	myfont = ImageFont.truetype(os.path.join(os.getcwd() ,'font' ,  './%s' % lineConfig[26] ) ,size=int(lineConfig[25]))
	draw = ImageDraw.Draw(backimg)
	tend = len(text)
	while True:
		text_size = draw.textsize(text[:tend], font=myfont)
#文本图层的尺寸
		
#print(text_size)
		if text_size[0] <= tmode["frame"][0]:
			break
		else:
			tend -= 1
#文本太长，调整文本长度
	if tmode['color'] == '':
		color = (0,0,0)
	else:
		color = ( int(tmode['color'].split(',')[0]) , int(tmode['color'].split(',')[1]) , int(tmode['color'].split(',')[2]) ) 
	draw.text((tmode["position"][0], tmode["position"][1]), text[:tend], font=myfont , fill= color )

	return backimg, tend



# start
print 'start...'
# configList = readConfFromFile(os.path.join(os.getcwd() ,'config.conf'))
configList = readConfFromExcel( os.path.join( os.getcwd() ,'conf.xlsx' ) )
for item in configList:
	# print item 
	startWork(item )







