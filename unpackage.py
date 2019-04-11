#!/user/local/bin/python
# -*- coding:utf-8 -*-
import os
import sys
import zipfile
import time


def getTheme_packaged():
		fileList = [];
		for item in os.listdir(os.path.join(os.getcwd() , 'theme_package')):
			if item.endswith('.hwt') :
				fileList.append(item.split('.')[0])
		return fileList

def deleteFile( item, fileName  ):
	if os.sep == '/':
		print( "rm -rf ./theme_nopackage/%s/%s "% ( item , fileName ) )
		os.system( "rm -rf ./theme_nopackage/%s/%s "% ( item , fileName ) )
	else:
		print  "del .\\theme_nopackage\\%s\\%s "% ( item , fileName )
		os.system( "del .\\theme_nopackage\\%s\\%s "% ( item , fileName ) )

def move(item ,fileName ):
	if os.sep =='/':
		os.system("mv ./theme_nopackage/%s/%s ./theme_nopackage/%s/%s.zip" %(item ,fileName,item , fileName))
	else:
		os.system("move .\\theme_nopackage\\%s\\%s .\\theme_nopackage\\%s\\%s.zip" %(item ,fileName,item , fileName))


def move_out(item  ):
	if os.sep =='/':
		pass
	else:
		print("move .\\theme_package\\%s.zip .\\theme_package\\%s.hwt" % (item , item ))
		os.system("move .\\theme_package\\%s.zip .\\theme_package\\%s.hwt" % (item , item ))



def InnerZip( item ,fileName):

	if os.sep == '/':
		print("cd theme_package%s%s%s%s  \n zip -r %s.zip .%s* \n mv %s.zip ../ \n cd ../ \n rm -rf .%s%s \n mv %s.zip %s " % ( os.sep,item ,os.sep , fileName,fileName,os.sep,fileName,os.sep,fileName,fileName,fileName ) )
		os.system("cd theme_package%s%s%s%s  \n zip -r %s.zip .%s* \n mv %s.zip ../ \n cd ../ \n rm -rf .%s%s \n mv %s.zip %s " % ( os.sep,item ,os.sep , fileName,fileName,os.sep,fileName,os.sep,fileName,fileName,fileName ) )
	else :
		print("7z a -r -tZip .\\theme_package\\%s\\%s.zip .\\theme_package\\%s\\%s\\*.* \n move .\\theme_package\\%s\\%s.zip .\\theme_package\\%s\\%s" % ( item , fileName ,item ,fileName ,item, fileName,item , fileName ))
		os.system("7z a -r -tZip .\\theme_package\\%s\\%s.zip .\\theme_package\\%s\\%s\\*.* " % ( item , fileName ,item ,fileName  ))

def OutterZip( item ):
	if os.sep == '/':
		print("cd theme_package%s%s%s%s  \n zip -r %s.zip .%s* \n mv %s.zip ../ \n cd ../ \n rm -rf .%s%s \n mv %s.zip %s " % ( os.sep,item ,os.sep , fileName,fileName,os.sep,fileName,os.sep,fileName,fileName,fileName ) )
		os.system("cd theme_package%s%s%s%s  \n zip -r %s.zip .%s* \n mv %s.zip ../ \n cd ../ \n rm -rf .%s%s \n mv %s.zip %s " % ( os.sep,item ,os.sep , fileName,fileName,os.sep,fileName,os.sep,fileName,fileName,fileName ) )
	else :
		print("7z a -r -tZip .\\theme_package\\%s.hwt .\\theme_package\\%s\\*"% (item , item ))
		os.system("7z a -r -tZip .\\theme_package\\%s.hwt .\\theme_package\\%s\\*"% (item , item ))
		
def cpTemp( item ):
	print 'clean:%s' % item 
	fileName = os.path.join(os.getcwd() , 'theme_package',item )
	print 'clean path:%s' % fileName 
	if os.path.exists(fileName):
		print 'path found , clean countinue'
		if os.sep == '/' :
			os.remove(fileName)
		else:
			print "rmdir %s /s /q" % (fileName)
			os.system("rmdir %s /s /q" % (fileName))
	else:
		print 'path not found ,do not clean ' 
		
	if os.sep == '/':
		cp = 'cp'
		print "%s -R ./theme_nopackage/%s ./theme_package/" % ( cp,item )
		os.system("%s -R ./theme_nopackage/%s ./theme_package/" % ( cp,item ))
	else : 
		print "xcopy .\\theme_nopackage\\%s .\\theme_package\\%s /S /I" % ( item , item )
		os.system("xcopy .\\theme_nopackage\\%s .\\theme_package\\%s /S /I" % ( item , item ))

def unzipfile_outter(item):
	if os.sep == '/':
		os.system("unzip -o ./theme_package/%s.hwt -d ./theme_nopackage/%s" % (item ,item ));
	else:
		os.system("7z x -tZip -y ./theme_package/%s.hwt -o./theme_nopackage/%s" % (item ,item ) )

def unzipfile_inner(item,fileName):
	if os.sep == '/':
		os.system("unzip -o ./theme_nopackage/%s/%s.zip -d ./theme_nopackage/%s/%s" % (item ,fileName,item ,fileName ) )
	else:
		os.system("7z x -tZip -y ./theme_nopackage/%s/%s.zip -o./theme_nopackage/%s/%s" % (item ,fileName,item ,fileName ) )

# start
themeList = getTheme_packaged()
for item in themeList:
	print('success scan :%s' % item );
	unzipfile_outter(item)
	
	move( item ,'icons')
	move( item ,'com.android.contacts')
	move( item ,'com.android.mms')
	move( item ,'com.android.phone')
	move( item ,'com.android.phone.recorder')
	move( item ,'com.android.server.telecom')
	move( item ,'com.android.systemui')
	move( item ,'com.huawei.android.launcher')
	
	unzipfile_inner( item ,'icons')
	unzipfile_inner( item ,'com.android.contacts')
	unzipfile_inner( item ,'com.android.mms')
	unzipfile_inner( item ,'com.android.phone')
	unzipfile_inner( item ,'com.android.phone.recorder')
	unzipfile_inner( item ,'com.android.server.telecom')
	unzipfile_inner( item ,'com.android.systemui')
	unzipfile_inner( item ,'com.huawei.android.launcher')
	
	deleteFile( item ,'icons.zip')
	deleteFile( item ,'com.android.contacts.zip')
	deleteFile( item ,'com.android.mms.zip')
	deleteFile( item ,'com.android.phone.zip')
	deleteFile( item ,'com.android.phone.recorder.zip')
	deleteFile( item ,'com.android.server.telecom.zip')
	deleteFile( item ,'com.android.systemui.zip')
	deleteFile( item ,'com.huawei.android.launcher.zip')
	