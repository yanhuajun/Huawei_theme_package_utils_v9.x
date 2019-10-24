#!/user/local/bin/python
# -*- coding:utf-8 -*-
import os
import sys
import zipfile
import time

DEBUGMODE = True

currentProjectFilePath = ''
outputPath = ''
projectName = ''

def getTheme_packaged():
		fileList = [];
		for item in os.listdir(os.path.join(os.getcwd() , 'theme_package')):
			if item.endswith('.hwt') :
				fileList.append(item[0:len(item) - 4])
		return fileList

def deleteFile( item  ):
	if os.sep == '/':
		command  = "rm -rf '%s/%s' "% ( outputPath + projectName , item  ) 
		print( command)
		os.system( command )
	else:
		str = "del '%s\\%s' " % ( outputPath + projectName , item  ) 
		log(str)
		os.system( str )

def move(item  ):
	if os.sep =='/':
		os.system("mv '%s/%s' '%s/%s.zip' " % ( outputPath+projectName ,  item  ,outputPath + projectName  ,item )  )
	else:
		os.system("mv '%s/%s' '%s/%s.zip' " % ( outputPath+projectName ,  item  ,outputPath + projectName  ,item )  )
		log(str)
		os.system(str)


def move_out(item  ):
	if os.sep =='/':
		pass
	else:
		print("move .\\theme_package\\'%s.zip' .\\theme_package\\'%s.hwt'" % (item , item ))
		os.system("move .\\theme_package\\'%s.zip' .\\theme_package\\'%s.hwt'" % (item , item ))

def cpTemp( item ):
	print 'clean:%s' % item 
	fileName = os.path.join(os.getcwd() , 'theme_package',item )
	print 'clean path:%s' % fileName 
	if os.path.exists(fileName):
		print 'path found , clean countinue'
		if os.sep == '/' :
			os.remove(fileName)
		else:
			print "rmdir '%s' /s /q" % (fileName)
			os.system("rmdir '%s' /s /q" % (fileName))
	else:
		print 'path not found ,do not clean ' 
		
	if os.sep == '/':
		cp = 'cp'
		print "%s -R ./theme_nopackage/'%s' ./theme_package/" % ( cp,item )
		os.system("%s -R ./theme_nopackage/'%s' ./theme_package/" % ( cp,item ))
	else : 
		print "xcopy .\\theme_nopackage\\'%s' .\\theme_package\\'%s' /S /I" % ( item , item )
		os.system("xcopy .\\theme_nopackage\\'%s' .\\theme_package\\'%s' /S /I" % ( item , item ))

def unzipfile_outter():
	if os.sep == '/':
		str = "unzip -o '%s' -d '%s' " % (currentProjectFilePath , outputPath + projectName  )
		log(str)
		os.system(str);
	else:
		str = "7z x -tZip -y '%s' -o'%s'" % (currentProjectFilePath , outputPath + projectName  ) 
		log(str)
		os.system(str)

def unzipfile_inner(item):
	if os.sep == '/':
		str = "unzip -o '%s/%s.zip' -d '%s/%s' " % (outputPath + projectName ,item ,outputPath + projectName , item   ) 
		log(str)
		os.system(str)
	else:
		os.system("7z x -tZip -y '%s/%s.zip' -o'%s/%s' " % ( outputPath + projectName ,item ,outputPath + projectName , item ) )

def log(logString):
	if DEBUGMODE:
		print logString
	else:
		return

#########################################################      start    #####################################################################################

# print '输入参数列表:' 
if len(sys.argv) > 1:
	for index in range(len(sys.argv)):
		if index == 1:
			currentProjectFilePath = sys.argv[index]
else:
	currentProjectFilePath = os.getcwd()
print 'currentProjectFilePath :' + currentProjectFilePath

outputPath = currentProjectFilePath[0:currentProjectFilePath.rindex('/')+1]
print "outputPath:" + outputPath

projectName = currentProjectFilePath[currentProjectFilePath.rindex('/') +1: len(currentProjectFilePath)].replace(".hwt","")
print "projectName:" + projectName

unzipfile_outter()

move( 'icons')
move( 'com.android.contacts')
move( 'com.android.mms')
move( 'com.android.phone')
move( 'com.android.phone.recorder')
move( 'com.android.server.telecom')
move( 'com.android.systemui')
move( 'com.huawei.android.launcher')
move( 'com.huawei.hwvoipservice') # com.huawei.hwvoipservice


unzipfile_inner( 'icons')
unzipfile_inner( 'com.android.contacts')
unzipfile_inner( 'com.android.mms')
unzipfile_inner( 'com.android.phone')
unzipfile_inner( 'com.android.phone.recorder')
unzipfile_inner( 'com.android.server.telecom')
unzipfile_inner( 'com.android.systemui')
unzipfile_inner( 'com.huawei.android.launcher')
unzipfile_inner( 'com.huawei.hwvoipservice')

deleteFile('icons.zip')
deleteFile('com.android.contacts.zip')
deleteFile('com.android.mms.zip')
deleteFile('com.android.phone.zip')
deleteFile('com.android.phone.recorder.zip')
deleteFile('com.android.server.telecom.zip')
deleteFile('com.android.systemui.zip')
deleteFile('com.huawei.android.launcher.zip')
deleteFile('com.huawei.hwvoipservice.zip')






#########################################################      之前的版本    #####################################################################################


# 扫描 package文件夹并输出至unpackage文件夹
# themeList = getTheme_packaged()
# for item in themeList:
# 	print('success scan :%s' % item );
# 	unzipfile_outter(item)
	
# 	move( item ,'icons')
# 	move( item ,'com.android.contacts')
# 	move( item ,'com.android.mms')
# 	move( item ,'com.android.phone')
# 	move( item ,'com.android.phone.recorder')
# 	move( item ,'com.android.server.telecom')
# 	move( item ,'com.android.systemui')
# 	move( item ,'com.huawei.android.launcher')
# 	move( item ,'com.huawei.hwvoipservice') # com.huawei.hwvoipservice

	
# 	unzipfile_inner( item ,'icons')
# 	unzipfile_inner( item ,'com.android.contacts')
# 	unzipfile_inner( item ,'com.android.mms')
# 	unzipfile_inner( item ,'com.android.phone')
# 	unzipfile_inner( item ,'com.android.phone.recorder')
# 	unzipfile_inner( item ,'com.android.server.telecom')
# 	unzipfile_inner( item ,'com.android.systemui')
# 	unzipfile_inner( item ,'com.huawei.android.launcher')
# 	unzipfile_inner( item ,'com.huawei.hwvoipservice')

# 	deleteFile( item ,'icons.zip')
# 	deleteFile( item ,'com.android.contacts.zip')
# 	deleteFile( item ,'com.android.mms.zip')
# 	deleteFile( item ,'com.android.phone.zip')
# 	deleteFile( item ,'com.android.phone.recorder.zip')
# 	deleteFile( item ,'com.android.server.telecom.zip')
# 	deleteFile( item ,'com.android.systemui.zip')
# 	deleteFile( item ,'com.huawei.android.launcher.zip')
# 	deleteFile( item ,'com.huawei.hwvoipservice.zip')
	