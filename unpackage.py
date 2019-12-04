#!/user/local/bin/python
# -*- coding:utf-8 -*-
import os
import sys
import zipfile
import time
import platform

DEBUGMODE = True

currentProjectFilePath = ''
outputPath = ''
projectName = ''

isWindows = False;

def getTheme_packaged():
		fileList = [];
		for item in os.listdir(os.path.join(os.getcwd() , 'theme_package')):
			if item.endswith('.hwt') :
				fileList.append(item[0:len(item) - 4])
		return fileList

def deleteFile( item  ):
	if not isWindows:
		command  = "rm -rf '%s/%s' "% ( outputPath + projectName , item  )
		print( command)
		os.system( command )
	else:
		str = "del '%s\\%s' " % ( outputPath + projectName , item  )
		log(str)
		os.system( str )

def move(item  ):
	command = ""
	if not isWindows:
		print "move"
		command ="mv '%s/%s' '%s/%s.zip' " % ( outputPath+projectName ,  item  ,outputPath + projectName  ,item )
		print "command:"  + command
		os.system(command)
	else:
		command ="mv '%s/%s' '%s/%s.zip' " % ( outputPath+projectName ,  item  ,outputPath + projectName  ,item )
		print "command:" + command
		os.system(command)
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
	if not isWindows:
		str = "unzip -o '%s' -d '%s' " % (currentProjectFilePath , outputPath + projectName  )
		log(str)
		os.system(str);
	else:
		str = "7z x -tZip -y '%s' -o'%s'" % (currentProjectFilePath , outputPath + projectName  )
		log(str)
		os.system(str)

def unzipfile_inner(item):
	if not isWindows:
		print "unzipfile_inner"
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
# 判断是否windows
print  'now system version:' + platform.system()
if platform.system() == 'Windows' or platform.system() == 'windows':
	isWindows = True

if isWindows:
	print 'windows env'
else:
	print 'not windows env'



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

print "=================unzipfile_outter================================="
unzipfile_outter()

print "test"
print os.path.exists(os.path.join(outputPath , projectName  , 'icons' ) )
print "dir:"
print os.path.join(outputPath , projectName  , 'icons' )

print "=================move================================="
if os.path.exists(os.path.join(outputPath , projectName  , 'icons' ) )  :
	move( 'icons')
if os.path.exists(os.path.join(outputPath , projectName  , 'com.android.contacts' ) )  :
	move( 'com.android.contacts')
if os.path.exists(os.path.join(outputPath , projectName  , 'com.android.mms' ) )  :
	move( 'com.android.mms')
if os.path.exists(os.path.join(outputPath , projectName  , 'com.android.phone' ) )  :
	move( 'com.android.phone')
if os.path.exists(os.path.join(outputPath , projectName  , 'com.android.phone.recorder' ) )  :
	move( 'com.android.phone.recorder')
if os.path.exists(os.path.join(outputPath , projectName  , 'com.android.server.telecom' ) )  :
	move( 'com.android.server.telecom')
if os.path.exists(os.path.join(outputPath , projectName  , 'com.android.systemui' ) )  :
	move( 'com.android.systemui')
if os.path.exists(os.path.join(outputPath , projectName  , 'com.huawei.android.launcher' ) )  :
	move( 'com.huawei.android.launcher')
if os.path.exists(os.path.join(outputPath , projectName  , 'com.huawei.hwvoipservice' ) )  :
	move( 'com.huawei.hwvoipservice')


print "=================unzipfile_inner================================="
if os.path.exists(os.path.join(outputPath , projectName  , 'icons.zip' ) )  :
	unzipfile_inner( 'icons')
if os.path.exists(os.path.join(outputPath , projectName  , 'com.android.contacts.zip' ) )  :
	unzipfile_inner( 'com.android.contacts')
if os.path.exists(os.path.join(outputPath , projectName  , 'com.android.mms.zip' ) )  :
	unzipfile_inner( 'com.android.mms')
if os.path.exists(os.path.join(outputPath , projectName  , 'com.android.phone.zip' ) )  :
	unzipfile_inner( 'com.android.phone')
if os.path.exists(os.path.join(outputPath , projectName  , 'com.android.phone.recorder.zip' ) )  :
	unzipfile_inner( 'com.android.phone.recorder')
if os.path.exists(os.path.join(outputPath , projectName  , 'com.android.server.telecom.zip' ) )  :
	unzipfile_inner( 'com.android.server.telecom')
if os.path.exists(os.path.join(outputPath , projectName  , 'com.android.systemui.zip' ) )  :
	unzipfile_inner( 'com.android.systemui')
if os.path.exists(os.path.join(outputPath , projectName  , 'com.huawei.android.launcher.zip' ) )  :
	unzipfile_inner( 'com.huawei.android.launcher')
if os.path.exists(os.path.join(outputPath , projectName  , 'com.huawei.hwvoipservice.zip' ) )  :
	unzipfile_inner( 'com.huawei.hwvoipservice')

print "=================deleteFile================================="
if os.path.exists(os.path.join(outputPath , projectName  , 'icons.zip' ) )  :
	deleteFile( 'icons.zip')
if os.path.exists(os.path.join(outputPath , projectName  , 'com.android.contacts.zip' ) )  :
	deleteFile( 'com.android.contacts.zip')
if os.path.exists(os.path.join(outputPath , projectName  , 'com.android.mms.zip' ) )  :
	deleteFile( 'com.android.mms.zip')
if os.path.exists(os.path.join(outputPath , projectName  , 'com.android.phone.zip' ) )  :
	deleteFile( 'com.android.phone.zip')
if os.path.exists(os.path.join(outputPath , projectName  , 'com.android.phone.recorder.zip' ) )  :
	deleteFile( 'com.android.phone.recorder.zip')
if os.path.exists(os.path.join(outputPath , projectName  , 'com.android.server.telecom.zip' ) )  :
	deleteFile( 'com.android.server.telecom.zip')
if os.path.exists(os.path.join(outputPath , projectName  , 'com.android.systemui.zip' ) )  :
	deleteFile( 'com.android.systemui.zip')
if os.path.exists(os.path.join(outputPath , projectName  , 'com.huawei.android.launcher.zip' ) )  :
	deleteFile( 'com.huawei.android.launcher.zip')
if os.path.exists(os.path.join(outputPath ,projectName , 'com.huawei.hwvoipservice.zip' ) )  :
	deleteFile( 'com.huawei.hwvoipservice.zip')





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
