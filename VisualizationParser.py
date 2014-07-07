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
			elif command.startswith('needinfo', 0, 8):
				if len(items) < 3:
					sys.stderr.write("line %s: '%s' not recognized, wrong format" % (line_counter, line))
                                        continue
				# does the command contains attribues?
				attrs = command.split('[')

				attrs_db = {}
				# comma separated values
				if len(attrs) > 1:
					attrs = attrs[1][0:-1].split(",")
					for attr in attrs:
						pair = attr.split("=")
						if len(pair) != 2:
							continue

						attrs_db[ pair[0] ] = pair[1]

				self.lines[ int(items[0]) ] = {'command': 'needinfo', 'keyword': items[2], 'value': items[3:][0], 'attrs': attrs_db }
			else:	
				self.lines[ int(items[0]) ] = {'command': items[1], 'value': "// " + ":".join(items[2:])}

	def getCommands(self):
		return self.lines

