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
#	[  ] - add keywords coloring
#	[  ] - add block folding
#	[  ] - add multilevel block folding
#	[  ] - add autofold from *.vis file

import sys
import os
from CodeParser import CodeParser
from VisualizationParser import VisualizationParser
from HTMLVisualizer import HTMLVisualizer

version = "0.0"
debug_level = 0

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
vis_file = os.path.basename(src_file) + ".vis"

# read visualization file
debug("Opening visualization file: %s " % vis_file)
#vis_content = ""
#with open(vis_file, "r") as file:
#	vis_content = file.read()


visParser = VisualizationParser(vis_file)
vis_lines = visParser.getCommands()

codeParser = CodeParser(src_file)
code_lines = codeParser.getLines()

htmlVis = HTMLVisualizer(code_lines, vis_lines)
htmlVis.printPage()

