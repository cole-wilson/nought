#!/usr/bin/env python3

import os,shutil,sys

if shutil.which('nought') is not None or True:
	import nought.__main__
	nought.__main__.main()
else:
	homedir = os.path.expanduser("~")
	os.system("osascript -e 'display alert \"This script will install nought on this system. Please quit to stop.\"'")
	try:
		shutil.copyfile(__file__,homedir+"/bin/nought")
	except:
		os.mkdir(homedir+"/bin")
		shutil.copyfile(__file__,""+homedir+"/bin/nought")
	os.system("chmod +x "+homedir+"/bin/nought")
	if homedir+"/bin" not in sys.path:
		print(f"Adding {homedir}/bin to $PATH...")
		sys.path.insert(0,homedir+"/bin")
	else:
		print(homedir+"/bin is already in $PATH.")
	os.system('hash -r')
	os.system("osascript -e 'display alert \"Done!\"'")