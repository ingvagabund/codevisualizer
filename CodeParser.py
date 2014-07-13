#!/bin/python

class CodeParser(object):

	def __init__(self, file):
		self.file = file
		self.parse()

	def parse(self):
		content = ""
		with open(self.file, "r") as file:
			content = file.read()

		# each line is counted
		self.lines = []
		#line_counter = 0
		for line in content.split("\n"):
			#line_counter = line_counter + 1
			#print "%d: %s" % (line_counter, line)
			self.lines.append(line)

	def getLines(self):
		return self.lines
