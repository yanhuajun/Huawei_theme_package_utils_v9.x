#!/user/local/bin/python
# -*- coding:utf-8 -*-
import os
import sys
import zipfile
import time


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



def InnerZip( item ,fileName):
	if os.sep == '/':
		print("cd %s%stheme_package%s%s%s%s  \n pwd \n zip -r %s.zip .%s* \n mv %s.zip ../ \n cd ../ \n rm -rf .%s%s \n mv %s.zip %s " 
		% ( os.getcwd() ,os.sep , os.sep,item ,os.sep , fileName,fileName,os.sep,fileName,os.sep,fileName,fileName,fileName ) )
		os.system("cd %s%stheme_package%s%s%s%s  \n pwd \n zip -r %s.zip .%s* \n mv %s.zip ../ \n cd ../ \n rm -rf .%s%s \n mv %s.zip %s " 
		% ( os.getcwd() ,os.sep , os.sep,item ,os.sep , fileName,fileName,os.sep,fileName,os.sep,fileName,fileName,fileName ) )
	else:
		print("cd .\\theme_package\\%s\\%s &&  zip -r %s.zip .\\* && mv %s.zip ../ && cd ../ " 
		%  (item,fileName,fileName,fileName) )
		os.system("cd .\\theme_package\\%s\\%s &&  zip -r %s.zip .\\* && mv %s.zip ../ && cd ../ " 
		%  (item,fileName,fileName,fileName) )

def OutterZip( item ):
	print("cd theme_package%s%s  && zip -r %s.zip .%s* && mv %s.zip ../ && cd ../ && mv %s.zip %s.hwt " 
		% ( os.sep,item ,item ,os.sep,item,item,item) )
	os.system("cd theme_package%s%s  && zip -r %s.zip .%s* && mv %s.zip ../ && cd ../ && mv %s.zip %s.hwt " 
		% ( os.sep,item ,item ,os.sep,item,item,item) )


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

# start

themeList = getTheme_nopackage()
for item in themeList:
	print('success scan :%s' % item );
for item in themeList:
	if item == '.DS_Store':
		continue  
	cpTemp( item )
	InnerZip( item ,'icons')
	InnerZip( item ,'com.android.contacts')
	InnerZip( item ,'com.android.mms')
	InnerZip( item ,'com.android.phone')
	InnerZip( item ,'com.android.phone.recorder')
	InnerZip( item ,'com.android.server.telecom')
	InnerZip( item ,'com.android.systemui')
	InnerZip( item ,'com.huawei.android.launcher')
	
	delete( item ,'icons')
	delete( item ,'com.android.contacts')
	delete( item ,'com.android.mms')
	delete( item ,'com.android.phone')
	delete( item ,'com.android.phone.recorder')
	delete( item ,'com.android.server.telecom')
	delete( item ,'com.android.systemui')
	delete( item ,'com.huawei.android.launcher')
    
	move( item ,'icons')
	move( item ,'com.android.contacts')
	move( item ,'com.android.mms')
	move( item ,'com.android.phone')
	move( item ,'com.android.phone.recorder')
	move( item ,'com.android.server.telecom')
	move( item ,'com.android.systemui')
	move( item ,'com.huawei.android.launcher')	
	
	OutterZip(item )
