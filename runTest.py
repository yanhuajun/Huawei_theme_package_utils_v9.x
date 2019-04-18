#!/user/local/bin/python
# -*- coding:utf-8 -*-
import os
import sys
import zipfile
from flask import Flask
from bs4 import BeautifulSoup



def getTheme_nopackage():
		return os.listdir(os.path.join(os.getcwd() , 'theme_nopackage'))


def cpTemp( item ):
	print 'copy %s nopackage --> package dir :clean:%s' % (item , item ) 
	fileName = os.path.join(os.getcwd() , 'theme_package',item )
	print 'clean path:%s' % fileName 
	if os.path.exists(fileName):
		print 'path found , clean countinue'
		os.remove(fileName)
	else:
		print 'path not found ,do not clean ' 
		
	if os.sep == '/':
		cp = 'cp'
		print "%s -R ./theme_nopackage/'%s' ./theme_package/" % ( cp,item )
		os.system("%s -R ./theme_nopackage/'%s' ./theme_package/" % ( cp,item ))
	else : 
		print "xcopy .\\theme_nopackage\\'%s' .\\theme_package\\'%s' /T /I" % ( item , item )
		print "xcopy .\\theme_nopackage\\'%s' .\\theme_package\\'%s'" % ( item , item )
		os.system("xcopy .\\theme_nopackage\\'%s' .\\theme_package\\'%s' /T /I" % ( item , item ))
		os.system("xcopy .\\theme_nopackage\\'%s' .\\theme_package\\'%s'" % ( item , item ))
	

def parse_main(projectName , typeName):
	print '[parse_main]:projectName->%s, type->%s' % (projectName, typeName )
	themeList = getTheme_nopackage()
	for item in themeList : 
		if(item == projectName):
			print "[parse_main] found project :%s" % item
			cpTemp(projectName)
			if typeName == 'lockscreen':
				return parse_lockscreen(item)
			else:
				return "[parse_main]option is not allow,option:%s" % typeName
	return "null"

def parse_lockscreen(projectName):
	print "[parse_lockscreen] projectName:%s" % projectName
	lockFilePath = os.path.join(os.getcwd() ,"theme_package%s%s%sunlock" %(os.sep,projectName,os.sep))
	themeXmlPath = os.path.join(lockFilePath , "theme.xml")
	print "[parse_lockscreen] lockFilePath:%s,themeXmlPath:%s"%(lockFilePath,themeXmlPath)
	lockscreenFilePath = '';
	if not os.path.exists(themeXmlPath):
		return "[parse_lockscreen]:theme.xml not found ,path: %s" % themeXmlPath
	themeXmlFile = open(themeXmlPath);
	themeXmlContent = ''
	try:
		themeXmlContent = themeXmlFile.read()
	finally:
		themeXmlFile.close()
	print "[parse_lockscreen]:xmlContent:%s\n" % themeXmlContent
	soup = BeautifulSoup(themeXmlContent)
	print soup.prettify()
#TODO: xml校验， xml解析 获得dynamicpath
	return themeXmlContent

# start
# themeList = getTheme_nopackage()
# for item in themeList:
# 	print('success scan :%s' % item );
# 	if item == '.DS_Store':
# 		continue  
# 	cpTemp( item )

app = Flask(__name__)

@app.route("/")
def hello():
	return "<h1>Hello World</h1>"

@app.route("/lockscreen/<projectName>")
def testLocalScreen(projectName):
	print "projectName : %s" % projectName
	returnContent = parse_main(projectName, "lockscreen")
	if returnContent == 'null':
		return "<h1>projectName--><span style='color:red'>%s</span> </br>not found</h1>" % projectName
	else:
		return returnContent




if __name__ == "__main__":
	app.run()