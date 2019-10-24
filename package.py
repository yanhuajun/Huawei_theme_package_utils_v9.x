#!/user/local/bin/python
# -*- coding:utf-8 -*-
import os
import sys
import zipfile
import time


DEBUGMODE = True

currentProjectFilePath = ""
outputPath = ""

def getTheme_nopackage():
		return os.listdir(os.path.join(os.getcwd() , 'theme_nopackage'))

def delete( item, fileName  ):
	if os.sep == '/':
		pass
	else:
		os.system( "rd .\\theme_package\\%s\\%s /q /s "% ( item , fileName ) )

def move(item ,fileName ):
	if os.sep =='/':
		pass
	else:
		os.system("move .\\theme_package\\%s\\%s.zip .\\theme_package\\%s\\%s" %(item ,fileName,item , fileName))


def move_out(item  ):
	if os.sep =='/':
		pass
	else:
		print("move .\\theme_package\\%s.zip .\\theme_package\\%s.hwt" % (item , item ))
		os.system("move .\\theme_package\\%s.zip .\\theme_package\\%s.hwt" % (item , item ))



def InnerZip( item ):
	command = ""
	command += "cd '%s_temp/%s' \n" %(outputPath + projectName , item )  + "pwd \n" + "zip -r '%s.zip' ./* \n" % item 
	command += "mv '%s.zip' ../ \n" % item 
	command += "cd ../ \n"
	command += "rm -rf '%s' \n" % item 
	command += "mv '%s.zip' '%s' \n" %(item , item )
	print "innerZip,command:" +command
	os.system(command)

	# if os.sep == '/':
	# 	print("cd %s%stheme_package%s%s%s%s  \n pwd \n zip -r %s.zip .%s* \n mv %s.zip ../ \n cd ../ \n rm -rf .%s%s \n mv %s.zip %s " 
	# 	% ( os.getcwd() ,os.sep , os.sep,item ,os.sep , fileName,fileName,os.sep,fileName,os.sep,fileName,fileName,fileName ) )
	# 	os.system("cd %s%stheme_package%s%s%s%s  \n pwd \n zip -r %s.zip .%s* \n mv %s.zip ../ \n cd ../ \n rm -rf .%s%s \n mv %s.zip %s " 
	# 	% ( os.getcwd() ,os.sep , os.sep,item ,os.sep , fileName,fileName,os.sep,fileName,os.sep,fileName,fileName,fileName ) )
	# else:
	# 	print("cd .\\theme_package\\%s\\%s &&  zip -r %s.zip .\\* && mv %s.zip ../ && cd ../ " 
	# 	%  (item,fileName,fileName,fileName) )
	# 	os.system("cd .\\theme_package\\%s\\%s &&  zip -r %s.zip .\\* && mv %s.zip ../ && cd ../ " 
	# 	%  (item,fileName,fileName,fileName) )

def OutterZip( ):
	command = ""
	command += "cd '%s_temp' \n" % (outputPath + projectName)  
	command += "zip -r '%s.zip' ./* \n" % projectName 
	command += "mv '%s.zip' ../ \n" % projectName
	command += "cd ../ \n"
	command += "rm -rf '%s_temp' \n" % (outputPath + projectName)
	command += "mv '%s.zip' '%s.hwt' \n" % (projectName , projectName )
	print "OutterZip,command:" + command
	os.system(command)
	# print("cd theme_package%s%s  && zip -r %s.zip .%s* && mv %s.zip ../ && cd ../ && mv %s.zip %s.hwt " 
	# 	% ( os.sep,item ,item ,os.sep,item,item,item) )
	# os.system("cd theme_package%s%s  && zip -r %s.zip .%s* && mv %s.zip ../ && cd ../ && mv %s.zip %s.hwt " 
	# 	% ( os.sep,item ,item ,os.sep,item,item,item) )


def cpTemp( ):
	command = "cp -R '%s' '%s_temp'" % ( currentProjectFilePath  , outputPath + projectName )
	print "command:" + command
	os.system(command)


def log(logStr):
	if DEBUGMODE:
		print logStr

# start

print '输入参数列表:'
print sys.argv 
if len(sys.argv) == 2:
	print "get outputPath from currentProjectFilePath..."
	for index in range(len(sys.argv)):
		if index == 1:
			currentProjectFilePath = sys.argv[index]
			outputPath = currentProjectFilePath[0:currentProjectFilePath.rindex('/')+1]
if len(sys.argv) == 3:
	print "get outputPath from argv..."
	for index in range(len(sys.argv)):
		if index == 1:
			currentProjectFilePath = sys.argv[index]
		if index == 2:
			outputPath = sys.argv[index]
if len(sys.argv) < 2 :
	currentProjectFilePath = os.getcwd()
	outputPath = os.getcwd()

print 'currentProjectFilePath :' + currentProjectFilePath
print 'outputPath:' + outputPath

projectName = currentProjectFilePath[currentProjectFilePath.rindex('/') +1: len(currentProjectFilePath)].replace(".hwt","")
print "projectName:" + projectName

cpTemp( )
InnerZip( 'icons')
InnerZip( 'com.android.contacts')
InnerZip( 'com.android.mms')
InnerZip( 'com.android.phone')
InnerZip( 'com.android.phone.recorder')
InnerZip( 'com.android.server.telecom')
InnerZip( 'com.android.systemui')
InnerZip( 'com.huawei.android.launcher')
InnerZip( 'com.huawei.hwvoipservice')

OutterZip()




####################################################    之前的版本    ######################################################################################################
# themeList = getTheme_nopackage()
# for item in themeList:
# 	print('success scan :%s' % item );
# for item in themeList:
# 	if item == '.DS_Store':
# 		continue  
# 	cpTemp( item )
# 	InnerZip( item ,'icons')
# 	InnerZip( item ,'com.android.contacts')
# 	InnerZip( item ,'com.android.mms')
# 	InnerZip( item ,'com.android.phone')
# 	InnerZip( item ,'com.android.phone.recorder')
# 	InnerZip( item ,'com.android.server.telecom')
# 	InnerZip( item ,'com.android.systemui')
# 	InnerZip( item ,'com.huawei.android.launcher')
# 	InnerZip( item ,'com.huawei.hwvoipservice')

	
# 	delete( item ,'icons')
# 	delete( item ,'com.android.contacts')
# 	delete( item ,'com.android.mms')
# 	delete( item ,'com.android.phone')
# 	delete( item ,'com.android.phone.recorder')
# 	delete( item ,'com.android.server.telecom')
# 	delete( item ,'com.android.systemui')
# 	delete( item ,'com.huawei.android.launcher')
# 	delete( item ,'com.huawei.hwvoipservice')

# 	move( item ,'icons')
# 	move( item ,'com.android.contacts')
# 	move( item ,'com.android.mms')
# 	move( item ,'com.android.phone')
# 	move( item ,'com.android.phone.recorder')
# 	move( item ,'com.android.server.telecom')
# 	move( item ,'com.android.systemui')
# 	move( item ,'com.huawei.android.launcher')	
# 	move( item ,'com.huawei.hwvoipservice')
	
# 	OutterZip(item )
