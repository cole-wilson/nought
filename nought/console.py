import os, sys, getopt

def main():
	options = {}
	try:
		arguments, ids = getopt.getopt(sys.argv[1:], "hdbvatc:", ["help"])
	except getopt.GetoptError as e:
		print(e)
		sys.exit(0)
	for key,value in arguments:
		if key in ("--help", "-h"):
			print('here is some help nno leave')
			sys.exit()
		if key in ("--about", "-a"):
			try:
				print('v.0.0.1\nConfig file at: {}'.format(os.environ["NOUGHT_CONFIG"]))
			except KeyError:
				print('v.0.0.1\nConfig file at: NOT DEFINED YET')
			sys.exit()
			
		if key in ("--verbose", "-v"):
			options['verbose'] = True

		if key in ("--default", "-d"):
			options['default'] = True

		if key in ("--backup", "-b"):
			options['backup'] = True

		if key in ("--test", "-t"):
			options['test'] = True

		if key in ("--config", "-c"):
			options['config'] = value
		print(options)

if __name__=="__main__":
	main()