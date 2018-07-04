import re
import sys, os
import plistlib
import pprint

def SubDirPath (d):
    return list(filter(os.path.isdir, [os.path.join(d,f) for f in os.listdir(d)]))

pathDict = {}
def ListApps():
	
	print('')
	path = "/var/containers/Bundle/Application"
	c = SubDirPath(path)
	for x in c:
		z = SubDirPath(x)
		for y in z:
			filePath = "%s/Info.plist" % y
			with open(filePath, "r", encoding="latin-1") as f:
				infoFile = f.read()
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
	path = "/var/containers/Bundle/Application"
	c = SubDirPath(path)
	for x in c:
		z = SubDirPath(x)
		for y in z:
			filePath = "%s/Info.plist" % y
			with open(filePath, "r", encoding="latin-1") as f:
				infoFile = f.read()
			dirSerial = re.sub('\/var\/.*Application.', '', y)
			dirSerial = re.sub('.[^/]*\.app', '', dirSerial)
			dirNamePretty = re.findall('[^/]*\.app', y)
			dirNamePretty[0] = re.sub('\.app', "", dirNamePretty[0])
			appNameDir = dirNamePretty[0]
			pathDict[appNameDir] = dirSerial

			
def GetCopyBundle(path):
	fp = open(path, 'rb')
	pl = plistlib.readPlist(fp)
	print(" \'%s\' copied to clipboard." % pl["CFBundleIdentifier"])
	os.system("pbcopy %s" % pl["CFBundleIdentifier"])

	
def GetApp(appName): 
	if appName in pathDict:
		appNameApp = "%s.app" % appName
		appPath = "/var/containers/Bundle/Application/%s/%s/" % (pathDict[appName], appNameApp)
		infoPath = "/var/containers/Bundle/Application/%s/%s/Info.plist" % (pathDict[appName], appNameApp)
		with open(infoPath, "r", encoding='utf-8') as f:
			infoFile=f.read()
		
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
		appPath = "/var/containers/Bundle/Application/%s/%s/" % (pathDict[appName], appNameApp)
		infoPath = "/var/containers/Bundle/Application/%s/%s/Info.plist" % (pathDict[appName], appNameApp)
		with open(infoPath, "r", encoding='utf-8') as f:
			infoFile=f.read()
		
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
	path = "/var/containers/Bundle/Application"
	c = SubDirPath(path)
	
	for x in c:
		z = SubDirPath(x)
		for y in z:
			filePath = "%s/Info.plist" % y
			with open(filePath, "r", encoding="latin-1") as f:
				infoFile = f.read()
			
			appName = re.findall(r'bplist', infoFile)
			if not appName:
				PrintInfo(filePath)
			else:
				print(" *** Application Data Obfuscated (Apple Application) ***")
			print(" Directory: " + y)
			print("")

def GetKey(appName, pkey):
	if appName in pathDict:
		appNameApp = "%s.app" % appName
		appPath = "/var/containers/Bundle/Application/%s/%s/" % (pathDict[appName], appNameApp)
		infoPath = "/var/containers/Bundle/Application/%s/%s/Info.plist" % (pathDict[appName], appNameApp)
		with open(infoPath, "r", encoding='utf-8') as f:
			infoFile=f.read()
		
		appName = re.findall(r'bplist', infoFile)
		
		if not appName:
				pl = plistlib.readPlist(infoPath)
				try:
					print( ' \'%s\'' % pl[pkey])
				except KeyError:
					print(' Key does not exist.')
		else:
			print(" *** Application Data Obfuscated (Apple Application) ***")
		print("")
	else:
		print(" Application does not exist.")
		print("")
		
		
def ModKey(appName, pkey, newValue):
	if appName in pathDict:
		appNameApp = "%s.app" % appName
		appPath = "/var/containers/Bundle/Application/%s/%s/" % (pathDict[appName], appNameApp)
		infoPath = "/var/containers/Bundle/Application/%s/%s/Info.plist" % (pathDict[appName], appNameApp)
		with open(infoPath, "r", encoding='utf-8') as f:
			infoFile=f.read()
		
		appName = re.findall(r'bplist', infoFile)
		
		if not appName:
			pl = plistlib.readPlist(infoPath)
			if pkey in pl:
					pl[pkey] = newValue
					plistlib.writePlist(pl, infoPath)
					print(" %s set to %s." % (pkey, newValue))
			else:
				print(' Key does not exist.')
		else:
			print(" *** Application Data Obfuscated (Apple Application) ***")
		print("")
	else:
		print(" Application does not exist.")
		print("")	

		
def AllKeys(appName):
	if appName in pathDict:
		appNameApp = "%s.app" % appName
		appPath = "/var/containers/Bundle/Application/%s/%s/" % (pathDict[appName], appNameApp)
		infoPath = "/var/containers/Bundle/Application/%s/%s/Info.plist" % (pathDict[appName], appNameApp)
		with open(infoPath, "r", encoding='utf-8') as f:
			infoFile=f.read()
		
		appName = re.findall(r'bplist', infoFile)
		
		if not appName:
				pl = plistlib.readPlist(infoPath)
				for key, value in list(pl.items()) :
					print('# %s' % key) 
		else:
			print(" *** Application Data Obfuscated (Apple Application) ***")
		print("")
	else:
		print(" Application does not exist.")
		print("")
	
		


	
def Help():
	print("")
	print(" Usage: python AppInfo.py [-h]")
	print("")
	print(" -l, --list    List all installed applications.")
	print(" -a, --all    Print information of all installed applications.")
	print(" -i, --info    Print information of specified application.")
	print(" -g, --get-key    Print the value of specified key from specified application's Info.plist.")
	print(" -ga, --get-all    List all keys in specified application's Info.plist.")	
	print(" -m, --modify-key    Change the value of specified key from specified application's Info.plist.")
	print(" -b, --bundle-id    Copy the specified application's Bundle Identifier to your clipboard. (pbcopy required)")
	print(" -h, --help    Print this message.")
	print("")
	
def Error():
	print("")
	print(" Unrecognized argument: " +  sys.argv[1])
	Help()

def InfoHelp():
	print("")
	print(" Please specify application name.")
	print(" E.g. python AppInfo.py --info Skype")
	print("")

def BundleHelp():
	print("")
	print(" Please specify application name.")
	print(" E.g. python AppInfo.py --bundle-id Skype")
	print("")
		

def KeyHelp():
	print("")
	print(" Please specify application name and the key to be extracted.")
	print(" E.g. python AppInfo.py --get-key Skype CFBundleExecutable")
	print("")
		
def AllKeysHelp():
	print("")
	print(" Please specify application name.")
	print(" E.g. python AppInfo.py --get-all Skype")
	print("")
	
def ModHelp():
	print("")
	print(" Please specify application name, the key to be changed and the value to set it to.")
	print(" E.g. python AppInfo.py --modify-key Skype CFBundleDisplayName NewValue")
	print("")
		
		
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
			InfoHelp()
	elif sys.argv[1] == "-h" or sys.argv[1] == "--help":
		Help()
	elif sys.argv[1] == "-b" or sys.argv[1] == "--bundle-id":
		if len(sys.argv) > 2:
			GetAllAppInfo()
			CopyBundleId(sys.argv[2])
		elif len(sys.argv) > 1:
			BundleHelp()
	elif sys.argv[1] == "-g" or sys.argv[1] == "--get-key":
		if len(sys.argv) > 3:
			GetAllAppInfo()
			GetKey(sys.argv[2], sys.argv[3])
		else:
			KeyHelp()
	elif sys.argv[1] == "-ga" or sys.argv[1] == "--get-all":
		if len(sys.argv) > 2:
			GetAllAppInfo()
			AllKeys(sys.argv[2])
		else:
			AllKeysHelp()
	elif sys.argv[1] == "-m" or sys.argv[1] == "--modify-key":
		if len(sys.argv) > 4:
			GetAllAppInfo()
			ModKey(sys.argv[2], sys.argv[3], sys.argv[4])
		else:
			ModHelp()
	else:
		Error()
else:
	Help()
