# -*- coding:utf-8 -*-

from PIL import Image
import os
import xlrd

'''
   @author:yanhuajun
	根据conf.xlsx 中的中心点 ，切割图片成圆形png

'''

default_res = os.path.join(os.getcwd(),'bg')
default_output_path = os.path.join(os.getcwd(),'output')

default_orgin_size = (1080,1920)
default_center_point = (540,960)
default_output_size = (180,180)


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

def startWork(configList):
	for config in configList:
		if not os.path.exists(config[0]):
			print "%s not found...continue..." % config[0]
		image = Image.open(os.path.join(default_res,config[0]))
		# image.show()
		# 原图大小缩放
		if config[1] == '':
			image = image.resize(default_orgin_size,Image.ANTIALIAS)
		else:
			size = config[1].split(',')
			image = image.resize( (int(size[0]),int(size[1])) ,Image.ANTIALIAS)
		image = image.convert('RGBA')
		# image.show()

		# 原图合成中心点寻找
		position = ''
		if config[2] == '':
			position = default_center_point
		else:
			tmparr = config[2].split(',')
			position = ( int(tmparr[0]) , int(tmparr[1]) )

		print 'center point:'
		print position
		#准备依照中心点  裁切
		marginX = min( position[0] , image.size[0]- position[0] )
		marginY = min( position[1] , image.size[1]- position[1] )
		# 计算最大半径
		r = min(marginY, marginX)
		print 'max r:'
		print r

		print 'pre crop param:'
		print (position[0]-r,position[1]-r,position[0] + r  ,position[1] + r) 
		image = image.crop( (position[0]-r,position[1]-r,position[0] + r  ,position[1] + r)  )
		# image.show()	

		image = circle(image , r)
		# image.show()
		outputSize = ''
		if config[3] == '' :
			outputSize = default_output_size
		else:
			tmparr = config[3].split(',')
			outputSize = ( int(tmparr[0]) , int(tmparr[1]) )
		image = image.resize(outputSize , Image.ANTIALIAS)

		if not os.path.exists(default_output_path):
			os.makedirs(default_output_path)
		image.save(os.path.join(default_output_path  , config[0]))



def circle(ima,r):
	# ima = Image.open("b2.png").convert("RGBA")
	# ima = ima.resize((600, 600), Image.ANTIALIAS)
	size = ima.size
	print(size)
	# 因为是要圆形，所以需要正方形的图片
	r2 = min(size[0], size[1])
	if size[0] != size[1]:
		ima = ima.resize((r2, r2), Image.ANTIALIAS)
	# 最后生成圆的半径
	r3 = r
	imb = Image.new('RGBA', (r3*2, r3*2),(255,255,255,0))
	pima = ima.load()  # 像素的访问对象
	pimb = imb.load()
	r = float(r2/2) #圆心横坐标
	for i in range(r2):
		for j in range(r2):
			lx = abs(i-r) #到圆心距离的横坐标
			ly = abs(j-r)#到圆心距离的纵坐标
			l  = (pow(lx,2) + pow(ly,2))** 0.5  # 三角函数 半径
			if l < r3:
				pimb[i-(r-r3),j-(r-r3)] = pima[i,j]
	# imb.save("test_circle.png")
	# imb.show()
	return imb



#start
configList = readConfFromExcel(os.path.join(os.getcwd(),'conf.xlsx'))
startWork(configList)


