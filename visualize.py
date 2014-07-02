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
#
#

import sys
import os

version = "0.0"

src_file = sys.argv[1]

print "Code Visualizer, version %s" % version
print "Opening file: %s" % src_file

# read source code
src_content = ""
with open(src_file, "r") as file:
	src_content = file.read()

# create visualization file
# extract basename
vis_file = os.path.basename(src_file) + ".vis"

# read visualization file
print "Opening visualization file: %s " % vis_file
#vis_content = ""
#with open(vis_file, "r") as file:
#	vis_content = file.read()

class VisualizationParser(object):

	def __init__(self, file):
		self.file = file
		self.parse()

	def parse(self):
		vis_content = ""
		with open(self.file, "r") as file:
        		vis_content = file.read()

		self.lines = {}
		line_counter = 0
		for line in vis_content.split("\n"):
			line_counter = line_counter + 1
			#skip empty lines
			if len(line) == 0:
				continue

			#skip comments
			if line[0] == "#":
				continue

			#<linenumber>:<command>:<value>
			items = line.split(":")
			if len(items) < 3:
				sys.stderr.write("line %s: '%s' not recognized, wrong format" % (line_counter, line))
				continue

			self.lines[ int(items[0]) ] = {'command': items[1], 'value': items[2:]}

	def getCommands(self):
		return self.lines

class CodeParser(object):

	def __init__(self, file):
		self.file = file
		self.parse()

	def parse(self):
		content = ""
		with open(self.file, "r") as file:
			content = file.read()

		# each line is counted
		line_counter = 0
		for line in content.split("\n"):
			line_counter = line_counter + 1
			print "%d: %s" % (line_counter, line)

codeParser = CodeParser(src_file)

visParser = VisualizationParser(vis_file)
#print visParser.getCommands()

print ""
#print vis_content

