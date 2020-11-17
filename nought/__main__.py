import os, sys, getopt

def help():
	helptext = open(os.path.dirname(os.path.abspath(__file__))+"/help.txt").read()
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
	# print(os.abspath(__file__))
	elif os.path.isfile('nought.toml'):
		options['config'] = './nought.toml'
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