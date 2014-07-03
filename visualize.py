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
from CodeParser import CodeParser
from VisualizationParser import VisualizationParser
from HTMLVisualizer import HTMLVisualizer

version = "0.0"
debug_level = 1

src_file = sys.argv[1]

def debug(msg):
	if debug_level > 0:
		print msg

debug("Code Visualizer, version %s" % version)
debug("Opening file: %s" % src_file)

# read source code
src_content = ""
with open(src_file, "r") as file:
	src_content = file.read()

# create visualization file
# extract basename
vis_file = "examples/" + os.path.basename(src_file) + ".vis"

# read visualization file
debug("Opening visualization file: %s " % vis_file)
# does the vis file exist?
if not os.path.exists(vis_file):
	debug("file not found, creating empty file")
	open(vis_file, 'a').close()

debug("Opening html file for write: %s " % vis_file)
html_file = "examples/" + os.path.basename(src_file) + ".html"
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

