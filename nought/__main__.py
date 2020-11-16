import os, sys, getopt

def help():
	helptext = open(os.path.dirname(os.path.abspath(__file__))+"/help.txt").read()
	print(helptext)

def main():
	options = {}
	try:
		arguments, ids = getopt.getopt(sys.argv[1:], "hdbvatc:", ["help","default","config =",'backup =','about','test','easteregg'])
	except getopt.GetoptError as e:
		print(e)
		print('\n')
		help()
		sys.exit(0)
	if len(ids) == 0:
		ids = ["default"]
	for key,value in arguments:
		if key in ("--easteregg"):
			print("Don't be silly, there isn't any easter egg hidden in the program...")
			sys.exit()
		if key in ("--help", "-h"):
			help()
			sys.exit()
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
		elif "NOUGHT_CONFIG" in os.environ:
			options['config'] = os.environ["NOUGHT_CONFIG"]
		elif os.path.isfile('nought.toml'):
			options['config'] = 'nought.toml'
		else:
			print('nought: no config file found!\n')
			help()
			sys.exit(0)

		if key in ("--default", "-d"):
			os.environ['NOUGHT_CONFIG'] = options["config"]

	import nought.runner as runner
	runner.main(options,ids)

if __name__=="__main__":
	main()