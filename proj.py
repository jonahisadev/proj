#!/usr/local/bin/python

#
#	Project Manager (c) 2017 Jonah Alligood
#

import sys
import os
from datetime import date
	
#
#	ACTUAL CODE
#

def help():
	print "Invalid command!"
	sys.exit(1)

def createProject():
	name = raw_input("Enter project name: ")
	desc = raw_input("Enter a project description: ")
	auth = raw_input("Enter an author name: ")
	git_in  = raw_input("Setup for Git? (Y/N): ")
	git = False
	repo = ""
	
	if git_in.upper() == "Y":
		git = True
		repo = raw_input("Enter a remote git server: ")
	
	# Create directories
	os.system("mkdir src")
	os.system("mkdir include")
	os.system("mkdir include/%s" % (name))
	os.system("mkdir .proj")
	
	# Create files
	os.system("touch README.MD")
	os.system("touch LICENSE.MD")
	os.system("touch Makefile")
	os.system("touch .proj/config.txt")
		
	# Write to config
	cfg = open(".proj/config.txt", "w")
	cfg.write("%s\n" % (name))
	if git == True:
		cfg.write("1")
	else:
		cfg.write("0")
	cfg.close();
		
	# Write to Makefile
	make = open("Makefile", "w")
	make.write(MAKEFILE_TEXT % (name, name.lower()))
	make.close()
	
	# Write to README
	read = open("README.MD", "w")
	read.write(README_TEXT % (name, desc))
	read.close()
	
	# Write to LICENSE
	lic = open("LICENSE.MD", "w")
	lic.write(LICENSE_TEXT % (name, date.today().year, auth))
	lic.close()
	
	if git == True:
		os.system("git init")
		os.system("git remote add origin %s" % (repo))
		os.system("touch .gitignore")
	
def deleteProject():
	really = raw_input("Are you sure? (Y/N): ")
	
	cfg = open(".proj/config.txt").read()
	cfg = cfg.split("\n")
	
	if cfg[1] == "1":
		os.system("rm -rf .git")
	
	if really.upper() == "Y":
		os.system("rm -rf include")
		os.system("rm -rf src")
		os.system("rm -rf .proj")
		os.system("rm -rf .git")
		os.system("rm Makefile")
		os.system("rm LICENSE.MD")
		os.system("rm README.MD")
		
		
def deleteClass():
	if not os.path.exists(".proj"):
		print "Please create a project first"
		return
		
	name = raw_input("Enter class name to delete: ")
	
	# Get configuration
	cfg = open(".proj/config.txt", "r").read()
	cfg = cfg.split("\n")
	
	# Delete files
	os.system("rm src/%s.cpp" % (name))
	os.system("rm include/%s/%s.h" % (cfg[0], name))
	
def addClass():
	if not os.path.exists(".proj"):
		print "Please create a project first"
		return
	
	name = raw_input("Enter class name: ")
	
	# Get configuration
	cfg = open(".proj/config.txt", "r").read()
	cfg = cfg.split("\n")
	
	# Create files
	os.system("touch src/%s.cpp" % (name))
	os.system("touch include/%s/%s.h" % (cfg[0], name))
	
	# Edit source
	src = open("src/%s.cpp" % (name), "w")
	src.write(CLASS_SOURCE_TEXT % (cfg[0], name, cfg[0]))
	src.close()
	
	# Set up header huard
	guard = HEADER_GUARD % (cfg[0].upper(), name.upper())
	
	# Edit header
	head = open("include/%s/%s.h" % (cfg[0], name), "w")
	head.write(CLASS_HEADER_TEXT % (guard, guard, cfg[0], name, guard))
	head.close()
	
def pushCode():
	if not os.path.exists(".proj"):
		print "Please create a project first"
		return
		
	# Get configuration
	cfg = open(".proj/config.txt", "r").read()
	cfg = cfg.split("\n")
	
	if not cfg[1] == "1":
		print "Git was not enabled for this project"
		return
	
	# Get description
	branch = raw_input("Enter branch [master]: ")
	desc = raw_input("Enter commit description: ")
	
	if branch == "":
		branch = "master"
	
	# Run git commands
	os.system("git add *")
	os.system("git commit -m \"%s\"" % (desc))
	os.system("git push origin %s" % (branch))
	
def setConfig():
	if os.path.exists(".proj"):
		print "Project configuration already exists"
		return
		
	# Get info
	name = raw_input("Enter project name: ")
	git = raw_input("Has git been set up? (Y/N): ")
	
	git_w = "0"
	if git == "Y":
		git_w = "1"
		
	# Create coniguration
	os.system("mkdir .proj")
	os.system("touch .proj/config.txt")
	
	# Write config
	cfg = open(".proj/config.txt", "w")
	cfg.write("%s\n" % (name))
	cfg.write(git_w)
	cfg.close()
	
def main():
	if len(sys.argv) < 2:
		help()
		
	if sys.argv[1] == "create":
		createProject()
		
	elif sys.argv[1] == "delete":
		deleteProject()
		
	elif sys.argv[1] == "rm":
		deleteClass()
		
	elif sys.argv[1] == "class":
		addClass()
		
	elif sys.argv[1] == "push":
		pushCode()
	
	elif sys.argv[1] == "exists":
		setConfig()
		
	else:
		help()

#
#	ANNOYING CONSTANTS
#

MAKEFILE_TEXT = """CC = g++
LDFLAGS =
CFLAGS = -I include -g -c -std=c++11
SRC = $(wildcard *.cpp src/*.cpp)
HEAD = $(wildcard include/%s/*.h)
OBJ = $(SRC:.cpp=.o)
EXEC = %s

all: $(OBJ) $(EXEC) $(HEAD)

$(EXEC): $(OBJ)
	$(CC) $(LDFLAGS) $^ -o $@

%%.o: %%.cpp
	$(CC) $(CFLAGS) $^ -o $@

clean:
	rm -rf *.o src/*.o $(EXEC)"""
	
README_TEXT = """# %s

%s"""

LICENSE_TEXT = "%s Copyright (c) %s %s"

CLASS_HEADER_TEXT = """#ifndef %s
#define %s

namespace %s {

	class %s {
	
	};

}

#endif // %s"""

CLASS_SOURCE_TEXT = """#include <%s/%s.h>

namespace %s {



}"""

HEADER_GUARD = "%s_%s_H"

#
#	MAIN CALL
#

if __name__ == "__main__":
	main()