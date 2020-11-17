"""
NOUGHT: a File Organizer
by Cole Wilson
colewilson.xyz
github.com/cole-wilson/nought

"""
import os, toml, re, datetime, time, requests, sys, getopt

verb = False
tab = 0
f = ""
def shellquote(s):
	return s.replace('(',r"\(").replace(')',r"\)")#.replace(' ',r"\ ")
def e(string):
	return re.sub("_\{.*?\}",ev,str(string))
def p(string):
	global verb
	global tab
	if verb:
		print("\t"*tab+str(string))
	else:
		return
def ensure(path):
	global rule
	# print(path.split(os.sep)[:-1])
	sp = path.split(os.sep)[:-1]
	d = os.sep.join(sp)
	if not os.path.isdir(d) and d!="":
		os.system('mkdir -p ' + d)
	# print(d)
def move(rule,options):
	global f
	if not "regex" in rule:#NORMAL MOVE
		newgroup = e(rule["move_to"].replace('$bp',basepath))+os.sep+f
		ensure(newgroup)
		if not options['test']:
			p("moving file to `"+newgroup+"`")
			os.rename(f,newgroup)

	else:#REGEX MOVE
		# try:
		newgroup = e(re.sub(".*?"+rule["regex"]+".*",rule['move_to'].replace('$bp',basepath).replace('$name',f.split(os.sep)[-1]).replace('$','\\'),f))
		p("moving file to `"+newgroup+"`")
		if not options['test']:
			ensure(newgroup)
			os.rename(f,newgroup)
		# except:
			# pass
def ev(match):
	t = match.group().replace('_','')
	return str(next(iter((eval(t.replace('$bp',basepath).replace('$name','"'+f.split(os.sep)[-1]+'"'))))))
def main(options,ids):
	global f
	try:
		with open(options['config'],'r') as f:
			config = toml.loads(f.read())
	except FileNotFoundError:
		print("nought: error reading config: `"+options['config']+"` not found")
		sys.exit(0)
	except toml.decoder.TomlDecodeError as error:
		print("nought: error in reading config file `"+options['config']+"`:\n\t"+str(error))
		sys.exit(0)		
	if options["verbose"] or options["test"]:
		global verb
		verb = True
	global tab
	global basepath
	for group in config["group"]:
		if "id" not in group:
			group["id"] = ids
		if isinstance(group["id"],str):
			group["id"] = [group["id"]]
		pa = True
		print('IDs: '+str(ids))
		for x in group["id"]:
			if x in ids:
				pa = False
		if pa:
			continue
		if "base_dir" in config["general"]:
			p("Going to base directory "+config["general"]["base_dir"])
			os.chdir(config["general"]["base_dir"])
		path = group["path"]
		if isinstance(path,str):
			path = [path]
		p("Going to group with locations " + str(path) + ":")
		for path in path:
			basepath = os.path.abspath(path)
			if "backup" in options:
				ensure(options["backup"])
				os.system('cd -r {} {}'.format(path,options["backup"]))
			try:
				os.chdir(path)
			except FileNotFoundError:
				p("That didn't work! That folder doesn't exist.")
				continue
			tab += 1
			filedirs = []
			# get files and folders
			if "recursive" in group and group["recursive"]:
				for root, dirs, files in os.walk("."):
					path = root.split(os.sep)
					for file in files:
							filedirs.append(root.replace('.'+os.sep,'')+os.sep+file.replace('.'+os.sep,''))
					for dir in dirs:
							filedirs.append(root.replace('.'+os.sep,'')+os.sep+dir.replace('.'+os.sep,''))
			else:
				filedirs = os.listdir(".")
			files = []
			dirs = []
			for x in filedirs:
				if os.path.isfile(x):
					files.append(x.replace('.'+os.sep,''))
				elif os.path.isdir(x):
					dirs.append(x.replace('.'+os.sep,''))
			if ("include_dirs" in group and group["include_dirs"]):
				files = filedirs
			if ("only_dirs" in group and group["only_dirs"]):
				files = dirs
			# rules
			filesmatched = []
			for f in files:		
				if "debug" in config["general"] and config["general"]["debug"]:
					input('Press enter to continue...')
				f = f.replace('.'+os.sep,'')
				pas = False
				if f.startswith('.'):
					if "include_hidden" in group:
						if group["include_hidden"]:
							pas = False
						else:
							pas = True
					else:
						pas = True
				else:
					pas = False
				if pas:
					continue
				if "include_dirs" in group and group["include_dirs"] and len(f.split(os.sep))>1:
					continue
				# f = f.replace(' ','_')
				# f = f.replace('(','_')
				# f = f.replace(')','_')
				newgroup = f
				p("- "+f)
				nomatch = True
				if "rule" not in group:
					group["rule"] = []
				for rule in group["rule"]:
					if f in filesmatched:
						break
					match = False
					tab += 1
					a = 0
					am = 0
					matches = "matches: "
					for x in ["includes","regex","size_less_than","size_more_than","content_includes","custom","modified_before","modified_after","user","group"]:
						if x in rule:
							a += 1
					if "includes" in rule:
						for include in rule["includes"]:
							if include in f:
								am += 1
								matches += " `"+include+"`"
					if "custom" in rule:
						if eval(rule["custom"].replace('$bp',basepath).replace('$name','"'+f.split(os.sep)[-1]+'"')):
							am += 1
							matches += " `"+rule['custom']+"`"
					if "regex" in rule:
						if re.search(rule["regex"],f):
							matches += " `"+rule["regex"]+"`"
							am += 1
					if "size_less_than" in rule:
						if os.stat(f).st_size < int(e(rule["size_less_than"])):
							matches += " size<`"+str(rule["size_less_than"])+"`"
							am += 1
					if "size_more_than" in rule:
						if os.stat(f).st_size < int(e(rule["size_more_than"])):
							matches += " size>`"+str(rule["size_more_than"])+"`"
							am += 1
					if "modified_before" in rule:
						if rule["modified_before"] < 0:
							rule["modified_before"] - time.time()
						if os.stat(f).st_ctime < int(e(rule["modified_before"])):
							matches += " modified_before `"+str(rule["modified_before"])+"`"
							am += 1
					if "modified_after" in rule:
						if rule["modified_after"] < 0:
							rule["modified_after"] - time.time()
						if os.stat(f).st_ctime > int(e(rule["modified_after"])):
							matches += " modified_after `"+str(rule["modified_after"])+"`"
							am += 1
					if "user" in rule:
						if os.popen('getent passwd '+str(os.stat(f).st_uid)+' | cut -d: -f1').read().replace('\n','') == e(rule["user"]):
							matches += " owned_by_user `"+str(rule["user"])+"`"
							am += 1
					if "group" in rule:
						if os.popen('getent passwd '+str(os.stat(f).st_gid)+' | cut -d: -f1').read().replace('\n','') == e(rule["group"]):
							matches += " owned_by_group `"+str(rule["group"])+"`"
							am += 1
					if "content_includes" in rule:
						if e(rule["content_includes"]) in open(f).read():
							matches += " content_includes:`"+str(rule["content_includes"])+"`"
							am += 1
					if am == a:
						match = True
						nomatch = False
						p(matches)
					if match:
						# DELETE
						filesmatched.append(f)
						if e(rule["action"]) == "delete":
							p("deleting item")
							if not options['test']:
								os.remove(f)
						# MOVE
						elif e(rule["action"]) == "move":
							move(rule,options)
						# SCRIPT
						elif "script" in rule:
							try:
								p("ruinning script: {}".format(shellquote(rule["script"].replace('$bp',basepath).replace('$name',newgroup.split(os.sep)[-1]))))
								if not options['test']:
									os.system(shellquote(rule["script"].replace('$bp',basepath).replace('$name',newgroup.split(os.sep)[-1])))
							except:
								pass
						# LINK
						if "link_in" in rule:
							if "regex" in rule:
								linkloc = re.sub(rule["regex"],e(rule['link_in']).replace('$bp',basepath).replace('$name',f.split(os.sep)[-1]).replace('$','\\'),f)
							else:
								linkloc = e(rule['link_in'])
							p(f'linking to file from {linkloc}')
							if not options['test']:
								ensure(linkloc)
								os.system(f'ln -s {newgroup} {linkloc}')
					tab -= 1
				if nomatch:
					tab += 1
					try:
						p(f"didn't match, doing action `{group['other']['action']}`")
					except KeyError:
						pass
					tab += 1
					try:
						rule = group['other']
					except:
						rule = {"action":"none"}
					if e(rule["action"]) == "delete":
						p("deleting item")
						try:
							if not options['test']:
								os.remove(f)
						except IsADirectoryError:
							try:
								os.rmdir(f)
							except:
								pass
					# MOVE
					elif e(rule["action"]) == "move":
						move(rule,options)
					if "script" in rule:
						try:
							os.system(shellquote(rule["script"].replace('$bp',basepath).replace('$name',newgroup.split(os.sep)[-1])))
						except:
							pass
					if "link_in" in rule:
						if "regex" in rule:
							linkloc = re.sub(rule["regex"],e(rule['link_in']).replace('$bp',basepath).replace('$name',f.split(os.sep)[-1]).replace('$','\\'),f)
						else:
							linkloc = e(rule['link_in'])
						p(f'linking to file from {linkloc}')
						ensure(linkloc)
						os.system(f'ln -s {newgroup} {linkloc}')
					tab -= 2
			tab -= 1