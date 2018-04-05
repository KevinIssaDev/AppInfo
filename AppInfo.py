import re
import sys, os
import plistlib

def SubDirPath (d):
    return filter(os.path.isdir, [os.path.join(d,f) for f in os.listdir(d)])


pathDict = {}
def ListApps():
	
	print('')
	path = "/var/mobile/Containers/Bundle/Application"
	c = SubDirPath(path)
	for x in c:
		z = SubDirPath(x)
		for y in z:
			filePath = "%s/Info.plist" % y
			infoFile = open(filePath, 'r').read()
			dirNamePretty = re.findall('[^/]*\.app', y)
			dirNamePretty[0] = re.sub('\.app', "", dirNamePretty[0])
			print("# " + dirNamePretty[0])
	print('')

	
def PrintInfo(path):
	fp = open(path, 'rb')
	pl = plistlib.readPlist(fp)
	print(" ### %s ###" % pl["CFBundleName"])
	print(" Version: " + pl["CFBundleShortVersionString"])
	print(" Minimum iOS: " + pl["MinimumOSVersion"])
	print(" Binary name: " + pl["CFBundleExecutable"])
	print(" Bundle Identifier: " + pl["CFBundleIdentifier"])

	
def GetAllAppInfo():
	print('')
	path = "/var/mobile/Containers/Bundle/Application"
	c = SubDirPath(path)
	for x in c:
		z = SubDirPath(x)
		for y in z:
			filePath = "%s/Info.plist" % y
			infoFile = open(filePath, 'r').read()
			dirSerial = re.sub('\/var\/.*Application.', '', y)
			dirSerial = re.sub('.[^/]*\.app', '', dirSerial)
			dirNamePretty = re.findall('[^/]*\.app', y)
			dirNamePretty[0] = re.sub('\.app', "", dirNamePretty[0])
			appNameDir = dirNamePretty[0]
			pathDict[appNameDir] = dirSerial

			
def GetCopyBundle(path):
	fp = open(path, 'rb')
	pl = plistlib.readPlist(fp)
	print(" \"%s\" copied to clipboard." % pl["CFBundleIdentifier"])
	os.system("pbcopy %s" % pl["CFBundleIdentifier"])

	
def GetApp(appName): 
	if appName in pathDict:
		appNameApp = "%s.app" % appName
		appPath = "/var/mobile/Containers/Bundle/Application/%s/%s/" % (pathDict[appName], appNameApp)
		infoPath = "/var/mobile/Containers/Bundle/Application/%s/%s/Info.plist" % (pathDict[appName], appNameApp)
		infoFile = open(infoPath, 'r').read()
		
		appName = re.findall(r'bplist', infoFile)
		
		if not appName:
			PrintInfo(infoPath)
		else:
			print(" *** Application Data Obfuscated (Apple Application) ***")
		print(" Directory: " + appPath)
		print("")
	else:
		print(" Application does not exist.")
		print("")
	
def CopyBundleId(appName):
	if appName in pathDict:
		appNameApp = "%s.app" % appName
		appPath = "/var/mobile/Containers/Bundle/Application/%s/%s/" % (pathDict[appName], appNameApp)
		infoPath = "/var/mobile/Containers/Bundle/Application/%s/%s/Info.plist" % (pathDict[appName], appNameApp)
		infoFile = open(infoPath, 'r').read()
		
		appName = re.findall(r'bplist', infoFile)
		
		if not appName:
			GetCopyBundle(infoPath)
		else:
			print(" *** Application Data Obfuscated (Apple Application) ***")
		print("")
	else:
		print(" Application does not exist.")
		print("")
	
def GetAllApps():
	path = "/var/mobile/Containers/Bundle/Application"
	c = SubDirPath(path)
	
	for x in c:
		z = SubDirPath(x)
		for y in z:
			filePath = "%s/Info.plist" % y
			infoFile = open(filePath, 'r').read()
			
			appName = re.findall(r'bplist', infoFile)
			if not appName:
				PrintInfo(filePath)
			else:
				print(" *** Application Data Obfuscated (Apple Application) ***")
			print(" Directory: " + y)
			print("")

		
	
def Help():
	print("")
	print(" Usage: python AppInfo.py [-h]")
	print("")
	print(" -l, --list	List all installed applications.")
	print(" -a, --all	Print information of all installed applications.")
	print(" -i, --info 	Print information of specified application.")
	print(" -b, --bundle-id 	Copy bundle identifier of specified application to clipboard.")
	print(" -h, --help 	Print this message.")
	print("")
	
def Error():
	print("")
	print(" Unrecognized argument: " +  sys.argv[1])
	Help()

def MissingArg():
	print("")
	print(" Missing argument: application name")
	Help()
		
	
if len(sys.argv) > 1:
	if sys.argv[1] == "-l" or sys.argv[1] == "--list":
		ListApps()
	elif sys.argv[1] == "-a" or sys.argv[1] == "--all":
		GetAllApps()
	elif sys.argv[1] == "-i" or sys.argv[1] == "--info":
		if len(sys.argv) > 2:
			GetAllAppInfo()
			GetApp(sys.argv[2])
		elif len(sys.argv) > 1:
			MissingArg()
	elif sys.argv[1] == "-h" or sys.argv[1] == "--help":
		Help()
	elif sys.argv[1] == "-b" or sys.argv[1] == "--bundle-id":
		if len(sys.argv) > 2:
			GetAllAppInfo()
			CopyBundleId(sys.argv[2])
		elif len(sys.argv) > 1:
			MissingArg()
	else:
		Error()
else:
	Help()
