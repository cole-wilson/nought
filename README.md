# nought
`nought` is a super customizable file cleaner/organizer/automator that can help keep you organized.
It lets you have complete control over all of it's options (there are many)
## Installation
> **Note:** Please ensure that you have Python 3.6+ and `pip` installed on your computer before completing the following steps:

User only install: `sudo pip install nought --user`
System wide install: `sudo pip3 install nought`
## Usage
To start, the best way is to run the setup wizard (`nought -w`)
```text
usage: nought [options] [identifiers ...]
    Runs `nought`, the super customizable file cleaner/organizer/automator
    
    Options:
			-w, -s, --wizard, --witch, --squib		display the setup witch/wizard/squib
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
```
For example, to run the `r1` routine in config file `/etc/nought/conf.toml` after backing up all directories you would run:
`nought -bc /etc/nought/conf.toml r1`
The default config file location is stored in the `NOUGHT_CONFIG` environment variable.
## Configuration
The configuration file is a [toml](https://github.com/toml-lang/toml) file where you set routines and rules.
Here is an example one with comments:
```toml
[general]
base_dir = "~/" # (optional, default="./") The starting directory 

[[group]] # This entire section can be repeatable
path = "~/Desktop" # A string OR list of the location(s) the group applies to. (required)
id = "test" # (optional, default="./") A string OR list of identifiers (used in command line). If none is supplied, it is applied for all ids. If it is "default", then it is applied when no id is specified in command. 
recursive = true # (optional, default="./") Whether or not edit files recursively.
include_dirs = true # (optional, default="./") Whether to treat directories as files. WARNING: DIRECTORIES INCLUDE ALL FILES IN THEM!

	[[group.rule]] # Repeatable per group, matches file

	# Below are all the conditions that can be used to match files. ALL conditions must be met to perform action:
	# All values in curly braces are evaluated as python expressions, like this: "./home/{2*90}/test.txt" turns to "./home/180/test.txt"
	includes = [".jpg",".png"] # A list of non regex strings to search for IN FILENAME
	regex = '[Ss]creenshot(.*?)' # A regex string to match filename against. Capturing groups can be reused later. Use single quotes.
	size_less_than = 12 # Number of bytes (use less than 0 for empty files)
	size_more_than = 2 # Number of bytes
	content_includes = "text" # A non regex string to search for in file CONTENT
	custom = "len(open('$name').read().split()) > 2" # A python expression that returns True or False. `$name` is substituted with filename.
	modified_before = 8736423423 # A Unix timestamp in seconds. Negative values are subtracted from current time.
	modified_after = -1978263 # A Unix timestamp in seconds. Negative values are subtracted from current time.
	user = "root" # Matches Unix user name
	group = "www-data" # Matches Unix group name
	
	# `action` can be one of the following:
	action = "move" # Moves or renames file
	action = "delete" # Deletes file
	action = "script" # Runs a script
	
	move_to = "folder" # moves into folder
	move_to = "screenshots/$1/$name" # moves using regex backreferences and `$name` replacement.

	script = "nano $name" # $name is replaced with file

	# optional: symlink to new file in another directory:
	link_in = ".//path/to/symlink/location/" 
```
All values in curly braces are evaluated as python expressions, like this: `./home/{2*90}/test.txt` turns to `./home/180/test.txt`

## Upcoming
I will be adding NOT conditions soon.
## Contact
If you need any help with anything, even how to write your config file, contact:
[`cole@colewilson.xyz`](mailto:cole@colewilson.xyz)