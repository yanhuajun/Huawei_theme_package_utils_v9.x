#!/user/local/bin/python
# -*- coding:utf-8 -*-
import os
import sys
import zipfile
import time
import fileinput 
import chardet
import re
import platform
from PIL import Image

isWindows = False


def mkdir(path):
    if not os.path.isdir(path):
        mkdir(os.path.split(path)[0])
    else:
        return
    os.mkdir(path)

def checkdot9pic():
	for item in dot9picList:
		inputFilePath = os.path.join(os.getcwd(),item['input'])
		outFilePath = os.path.join(currentProjectFilePath , item['output'] )
		if not os.path.exists(inputFilePath):
			print '模板点9文件出现问题 ， path:%s' % inputFilePath
			continue
		if os.path.exists(outFilePath):
			print '点9文件已存在 ， path:%s , 已跳过处理...' %(  outFilePath )
			continue

		arr = outFilePath.split('/')
		tmpPath = ''
		if isWindows:
			tmpPath = '\\' + arr[len(arr)-1]
		else:
			tmpPath = '/' + arr[len(arr)-1]
		tmpPath = outFilePath.replace(tmpPath  ,'');
		if not os.path.exists(tmpPath) :
			mkdir(tmpPath)
		if isWindows:
			inputFilePath = inputFilePath.replace('/','\\',99)
			outFilePath = outFilePath.replace('/','\\',99)
		color = getOrginColorFromConfig(os.path.join(currentProjectFilePath , item['output'].split('/')[0], item['target'] ,'theme.xml')  ,'', item['color'] , item['defaultcolor'])
		changeDot9PngColor(inputFilePath  ,outFilePath , Hex_to_RGB(color))


def getOrginColorFromConfig( filePath ,fileContent,  colorPatten  , defaultcolor):
	color = defaultcolor
	if color == '':
		color = '#ffffff'
	if filePath == '' and fileContent == '' :
		return color
	if filePath != '' and fileContent == '' and not os.path.exists(filePath):
		return color
	if filePath == '' and fileContent == '':
		return color 
	if colorPatten == '' :
		return color
	content = ''
	if filePath != '':
		content = open(filePath).read()
	if fileContent != '':
		content = fileContent
	if content == '' :
		return color
	print 'colorPatten:' + colorPatten
	matchObj = re.search(r''+colorPatten , content )
	if matchObj == None:
		return color
	color = matchObj.group(1)
	print 'color:' + color
	return color 



 
# RGB格式颜色转换为16进制颜色格式
def RGB_to_Hex(rgb):
	RGB = rgb.split(',')            # 将RGB格式划分开来
	color = '#'
	for i in RGB:
		num = int(i)
		# 将R、G、B分别转化为16进制拼接转换并大写  hex() 函数用于将10进制整数转换成16进制，以字符串形式表示
		color += str(hex(num))[-2:].replace('x', '0').upper()
	print(color)
	return color
 
 
# 16进制颜色格式颜色转换为RGB格式
def Hex_to_RGB(hex):
	r = int(hex[1:3],16)
	g = int(hex[3:5],16)
	b = int(hex[5:7],16)
	rgb = str(r)+','+str(g)+','+str(b)
	print(rgb)
	return rgb


def changeDot9PngColor(inputPic , outputPic ,afterColor):
	img = Image.open(inputPic) 
	imageWidth = img.width 
	imageHeight = img.height
	print 'imgwidth:%s , imgheight:%s' %(imageWidth, imageHeight);
	
	# 改色
	# for i in xrange(imageWidth):
	# 	for j in xrange(imageHeight):
	# 		r,g,b,a= img.getpixel((i,j))
	# 		if a == 0:
	# 			continue
	# 		b=int(afterColor.split(',')[2])
	# 		g=int(afterColor.split(',')[1])
	# 		r=int(afterColor.split(',')[0])
	# 		img.putpixel((i,j), (r,g,b,a)) 

	# 获取 需要取得 图像x,y 最大值 
	minX = ''
	minY = ''
	maxX = ''
	maxY = ''
	for i in xrange(imageWidth):
		for j in xrange(imageHeight):
			r,g,b,a= img.getpixel((i,j))
			if a == 0:
				continue
			# print 'i:%d , j:%d' %( i , j )
			if minX == '':
				minX = i
			if minY == '':
				minY = j

			if maxX == '' or i >= maxX:
				maxX = i
			if maxY == '' or j >= maxY:
				maxY = j

			if minX == '' or i <= minX:
				minX = i 
			if minY == '' or j <= minY:
				minY = j
	if isWindows:
		print 'image real size : minX:%d , maxX:%d , minY:%d , maxY:%d' %( minX , maxX , minY , maxY)
	else:
		print '图片实际大小：minX:%d , maxX:%d , minY:%d , maxY:%d' %( minX , maxX , minY , maxY)

	if imageWidth <=20 and imageHeight <=20:
		img.save(outputPic)
		# img.show()
		return 

	img2 = Image.new('RGBA',(imageWidth + 1,imageHeight +1)  ,(0,0,0))
	box1 = (0,0,imageWidth,imageHeight)
	region = img.crop(box1)
	img2.paste(region,(1,1))

	for i in xrange(imageWidth + 1):
		for j in xrange( imageHeight + 1):
			# print 'i:%d , j:%d' % (i,j)
			if i == 0 or i == imageWidth or j ==0 or j == imageHeight:
				# 画黑线  ，需要取得 图像x,y 最大值 
				if imageWidth > 20 and imageHeight > 20 :
					ysize = maxY - minY 
					xsize = maxX - minX
					yratio = 0.42
					xratio = 0.30
					#             上中点										左中点					下中线																		右中线
					if (i == minX + xsize/2 and j == 0) or (i == 0 and j == minY + ysize/2) or ( ( i >= minX + xsize/2 - xsize*xratio and i<= minX + xsize/2 + xsize*xratio ) and j == imageHeight ) or ( i == imageWidth and j >= minY + ysize/2 -ysize*yratio and j <= minY + ysize/2 +ysize*yratio):
						b = 0
						g = 0
						r = 0
						a = 255
					else:
						b = 0
						g = 0
						r = 0
						a = 0
				else:
					b = 0
					g = 0
					r = 0
					a = 0
				img2.putpixel((i,j), (r,g,b,a)) 

	img2.save(outputPic)
	# img2.show()

def scandot9( filePath ):
	fileList = [];
	for item in os.listdir(filePath):
		if item.endswith('.png'):
			fileList.append(os.path.join( filePath , item ))#[0:len(item) - 4]
	return fileList

#start

# 判断是否windows
print  '当前系统为：' + platform.system()
if platform.system() == 'Windows' or platform.system() == 'windows':
	isWindows = True

if isWindows:
	print 'windows env...'
else:
	print '非windows环境'

fileList = scandot9(os.path.join(os.getcwd(),'input'))
print fileList
for item in fileList:
	changeDot9PngColor( item , item.replace('input','output')  ,'')
