#!/bin/python

# Author: Jan Chaloupka, jchaloup@redhat.com
# 
# Date: 2 July 2014
#
# Aim: create a tool to visualize semantic parts of the code
# or comment the code without changing the source file itself
# 
# Output: html for now

# TODO:
#	[OK] - add keywords coloring
#	[OK] - add block folding
#	[  ] - add multilevel block folding
#	[OK] - add autofold from *.vis file
#	[OK] - add database of keywords description
#	[  ] - make a search in db more efficient
#	[  ] - support for multiple commands for single line (nonconflicting commands)
#	[  ] - support for multiline comments on a single line (flowing div)
#	[  ] - make a call graph for every module (use existing tools)
#	[  ] - ignore comments (+color them)

import sys
import os
import optparse
from CodeParser import CodeParser
from VisualizationParser import VisualizationParser
from HTMLVisualizer import HTMLVisualizer

version = "0.0"
debug_level = 0

# argument parsing
parser = optparse.OptionParser(usage="usage: %prog [--debug] [--dest=DEST] file")
parser.add_option(
    "", "--debug", dest = "debug", action = "store_true", default = False,
    help = "debug mode"
)

parser.add_option(
    "", "--dest", dest = "dest", action = "store", default = "examples",
    help = "destination folder for generated files"
)

options, args = parser.parse_args()

if options.debug:
	debug_level = 1

if len(args) != 1:
	print "Input source code missing!!!"
	exit(0)

if len(options.dest) == 0:
	print "Destination directory name must be at least of length 1"
	exit(0)

src_file = args[0]
destination = options.dest

def debug(msg):
	if debug_level > 0:
		print msg

def mkdir_p(path):
    if not os.access(path, os.F_OK):
        os.makedirs(path)

#####################################################################

debug("Code Visualizer, version %s" % version)
debug("Opening file: %s" % src_file)

# read source code
src_content = ""
with open(src_file, "r") as file:
	src_content = file.read()

# create visualization file
# is the destination relative?
if destination[0] != "/":
	destination = "%s/%s" % (os.getcwd(), destination)

# canonize the path
destination = os.path.realpath(destination)

# destination folder exists?
if not os.path.exists(destination):
	mkdir_p(destination)

# extract basename
vis_file = destination + "/" + os.path.basename(src_file) + ".vis"

# read visualization file
debug("Opening visualization file: %s " % vis_file)
# does the vis file exist?
if not os.path.exists(vis_file):
	debug("file not found, creating empty file")
	open(vis_file, 'a').close()

debug("Opening html file for write: %s " % vis_file)
html_file = destination + "/" + os.path.basename(src_file) + ".html"
# does the html file exist?
if not os.path.exists(html_file):
	debug("file not found, creating empty file")
	open(html_file, 'a').close()

debug("Parsing visualization file...")
visParser = VisualizationParser(vis_file)
vis_lines = visParser.getCommands()
debug("Visualization file parsed")

debug("Parsing source code file...")
codeParser = CodeParser(src_file)
code_lines = codeParser.getLines()
debug("Source file parser")

debug("Initializing html output...")
htmlVis = HTMLVisualizer(code_lines, vis_lines)
debug("Html output generated")
htmlVis.printPage(html_file)

