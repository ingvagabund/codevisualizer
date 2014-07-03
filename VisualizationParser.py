#!/bin/python

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

			command = items[1]

			if command == 'fold':
				if len(items) < 5:
					sys.stderr.write("line %s: '%s' not recognized, wrong format" % (line_counter, line))
	                                continue

				self.lines[ int(items[0]) ] = {'command': items[1], 'endline': int(items[2]), 'folded': int(items[3]), 'value': items[4:][0]}
			elif command == 'highlight':
				if len(items) < 3:
					sys.stderr.write("line %s: '%s' not recognized, wrong format" % (line_counter, line))
                                        continue
				self.lines[ int(items[0]) ] = {'command': items[1], 'keyword': items[2], 'value': items[3:][0]}
			elif command == 'needinfo':
				if len(items) < 3:
					sys.stderr.write("line %s: '%s' not recognized, wrong format" % (line_counter, line))
                                        continue
				self.lines[ int(items[0]) ] = {'command': items[1], 'keyword': items[2], 'value': items[3:][0]}
			else:	
				self.lines[ int(items[0]) ] = {'command': items[1], 'value': "// " + ":".join(items[2:])}

	def getCommands(self):
		return self.lines

