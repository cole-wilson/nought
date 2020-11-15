"""
NOUGHT: a File Organizer
by Cole Wilson
colewilson.xyz
github.com/cole-wilson/nought

"""
import os, toml, re, datetime, time, requests

tab = 0

def shellquote(s):
	return s.replace('(',r"\(").replace(')',r"\)")#.replace(' ',r"\ ")
def e(string):
	return re.sub("\{.*?\}",ev,str(string))
def p(string):
	global config
	global tab
	if "verbose" in config['general']:
		if config['general']['verbose']:
			print("\t"*tab+str(string))
	else:
		return
def ensure(path):
	global rule
	# print(path.split('/')[:-1])
	sp = path.split('/')[:-1]
	d = os.sep.join(sp)
	if not os.path.isdir(d) and d!="":
		os.system('mkdir -p ' + d)
	# print(d)
def move(rule):
	global f
	if not "regex" in rule:#NORMAL MOVE
		newlocation = e(rule["move_to"])+os.sep+f
		ensure(newlocation)
		p("moving file to `"+newlocation+"`")
		os.rename(f,newlocation)

	else:#REGEX MOVE
		try:
			newlocation = re.sub(rule["regex"],e(rule['move_to']).replace('$name',f).replace('$','\\'),f)
			p("moving file to `"+newlocation+"`")
			ensure(newlocation)
			os.rename(f,newlocation)
		except:
			pass

def ev(match):
	t = match.group()
	return str(next(iter((eval(t.replace('$name','"'+f+'"'))))))
with open('nought.toml','r') as f:
	config = toml.loads(f.read())
for location in config["location"]:
	os.chdir(config["general"]["base_dir"])
	path = location["path"]
	p("Going to location " + path + ":")
	try:
		os.chdir(path)
	except FileNotFoundError:
		p("That didn't work! That folder doesn't exist.")
		continue
	tab += 1
	filedirs = []
	# get files and folders
	if "recursive" in location and location["recursive"]:
		for root, dirs, files in os.walk("."):
			path = root.split(os.sep)
			for file in files:
					filedirs.append(root.replace('./','')+os.sep+file.replace('./',''))
			for dir in dirs:
					filedirs.append(root.replace('./','')+os.sep+dir.replace('./',''))
	else:
		filedirs = os.listdir(".")
	files = []
	dirs = []
	for x in filedirs:
		if os.path.isfile(x):
			files.append(x.replace('./',''))
		elif os.path.isdir(x):
			dirs.append(x.replace('./',''))
	if ("include_dirs" in location and location["include_dirs"]):
		files = filedirs
	if ("only_dirs" in location and location["only_dirs"]):
		files = dirs
	# rules
	filesmatched = []
	for f in files:		
		if "debug" in config["general"] and config["general"]["debug"]:
			input('Press enter to continue...')
		f = f.replace('./','')
		pas = False
		if f.startswith('.'):
			if "include_hidden" in location:
				if location["include_hidden"]:
					pas = False
				else:
					pas = True
			else:
				pas = True
		else:
			pas = False
		if pas:
			continue
		if "include_dirs" in location and location["include_dirs"] and len(f.split(os.sep))>1:
			continue
		# f = f.replace(' ','_')
		# f = f.replace('(','_')
		# f = f.replace(')','_')
		newlocation = f
		p("- "+f)
		nomatch = True
		if "rule" not in location:
			location["rule"] = []
		for rule in location["rule"]:
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
				for include in e(rule["includes"]):
					if include in f:
						am += 1
						matches += " `"+include+"`"
			if "custom" in rule:
				if eval(rule["custom"].replace('$name','"'+f+'"')):
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
				if os.stat(f).st_ctime < int(e(rule["modified_before"])):
					matches += " modified_before `"+str(rule["modified_before"])+"`"
					am += 1
			if "modified_after" in rule:
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
					os.remove(f)
				# MOVE
				elif e(rule["action"]) == "move":
					move(rule)
				# SCRIPT
				elif "script" in rule:
					try:
						os.system(shellquote(rule["script"].replace('$name',newlocation)))
					except:
						pass
				# LINK
				if "link_in" in rule:
					if "regex" in rule:
						linkloc = re.sub(rule["regex"],e(rule['link_in']).replace('$name',f).replace('$','\\'),f)
					else:
						linkloc = e(rule['link_in'])
					p(f'linking to file from {linkloc}')
					ensure(linkloc)
					os.system(f'ln -s {newlocation} {linkloc}')
			tab -= 1
		if nomatch:
			tab += 1
			try:
				p(f"didn't match, doing action `{location['other']['action']}`")
			except KeyError:
				pass
			tab += 1
			try:
				rule = location['other']
			except:
				rule = {"action":"none"}
			if e(rule["action"]) == "delete":
				p("deleting item")
				try:
					os.remove(f)
				except IsADirectoryError:
					try:
						os.rmdir(f)
					except:
						pass
			# MOVE
			elif e(rule["action"]) == "move":
				move(rule)
			if "script" in rule:
				try:
					os.system(shellquote(rule["script"].replace('$name',newlocation)))
				except:
					pass
			if "link_in" in rule:
				if "regex" in rule:
					linkloc = re.sub(rule["regex"],e(rule['link_in']).replace('$name',f).replace('$','\\'),f)
				else:
					linkloc = e(rule['link_in'])
				p(f'linking to file from {linkloc}')
				ensure(linkloc)
				os.system(f'ln -s {newlocation} {linkloc}')
			tab -= 2
	tab -= 1