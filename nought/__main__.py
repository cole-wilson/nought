import os, sys, getopt
hel = """
usage: nought [options] [identifiers ...]
    Runs `nought`, the super customizable file cleaner/organizer/automator
    
    Options:
			-c [location], --config [location]  	specify configuration file. Default: "./nought.toml" (see -d and "Environment Variables")
			-b [location], --backup [location]		backup files to specified location. Default: false
			-d, --default		set the config file as default
			-a, --about			display version and exit
			-h, --help			display this help message
			-t, --test			test configuration without actually doing anything (enables verbose mode)
    
    Arguments:
			IDENTIFIERS:		a repeatable identifier for which groups to run
    
    Environment Variables:
			NOUGHT_CONFIG:  the path to the default configuration file
"""
def help():
	global hel
	try:
		helptext = open(os.path.dirname(os.path.abspath(__file__))+os.sep+"help.txt").read()
	except:
		helptext = hel
	print(helptext)

def main():
	options = {}
	try:
		arguments, ids = getopt.getopt(sys.argv[1:], "hdbsvmwatc:", ["help","wizard","witch","squib","muggle","default","config=",'backup =','about','test','easteregg'])
	except getopt.GetoptError as e:
		print(e)
		print('\n')
		help()
		sys.exit(0)
	if len(ids) == 0:
		ids = ["default"]
	options["verbose"] = False
	options["test"] = False
	for key,value in arguments:
		if key in ("--easteregg"):
			print("Don't be silly, there aren't any easter eggs hidden in the program... i think...")
			sys.exit()
		if key in ("--help", "-h"):
			help()
			sys.exit()
		if key in ("--muggle", "-m"):
			print("There aren't any wizards here, what are you talking about?\n**OBLIVIATE!!**")
			sys.exit()
		
		if key in ("--wizard", "-w","--witch","--squib",'-s'):
			import nought.wizard as wizard
			wizard.main()
		
		if key in ("--about", "-a"):
			try:
				print('v.0.0.1\nConfig file at: {}'.format(os.environ["NOUGHT_CONFIG"]))
			except KeyError:
				print('v.0.0.1\nConfig file at: NOT DEFINED YET')
			sys.exit()

		if key in ("--verbose", "-v"):
			options['verbose'] = True

		if key in ("--backup", "-b"):
			options['backup'] = True

		if key in ("--test", "-t"):
			options['test'] = True

		if key in ("--config", "-c"):
			options['config'] = value

		if key in ("--default", "-d"):
			options['def'] = True
		if key in ("--config", "-c"):
			options['config'] = value
		
	if "config" in options:
		pass
	elif "NOUGHT_CONFIG" in os.environ:
		options['config'] = os.environ["NOUGHT_CONFIG"]
	elif os.path.isfile(os.path.abspath(__file__).replace(__file__,"")+"conf.toml"):
		options['config'] = os.path.abspath(__file__).replace(__file__,"")+"conf.toml"
	elif os.name == 'nt':
		print('You are using Windows, so you have to manually set a config location with -c or --config')
		sys.exit(1)
	# print(os.abspath(__file__))
	elif os.path.isfile('nought.toml'):
		options['config'] = 'nought.toml'
	else:
		print('nought: no config file found!\n')
		help()
		sys.exit(0)
	if "def" in options and options['def']:
		print('To set a default path to config, please change the NOUGHT_CONFIG env variable like so:')
		print('\n\texport NOUGHT_CONFIG={}'.format(options['config']))
		sys.exit(0)
	if "verbose" in options and options["verbose"]:
		print("using configuration file: "+options['config'])
	import nought.runner as runner
	runner.main(options,ids)

if __name__=="__main__":
	main()