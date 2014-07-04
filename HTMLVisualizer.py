import re

class HTMLVisualizer(object):

	def __init__(self, src_lines, vis_lines):
		self.src_lines = src_lines
		self.vis_lines = vis_lines
		self.keywords = self.getKeywords()

	def getKeywords(self):
		content = ""
		with open('keywords', 'r') as file:
			content = file.read()

		keywords = {}
		for keyword in content.split('\n'):
			if len(keyword) == 0:
				continue

			# has keyword specific css name?
			parts = keyword.split(":")
			if len(parts) == 1:
				keywords[keyword] = ""
			else:
				keywords[parts[0].strip()] = parts[1:][0].strip()

		return keywords

	def parseKeywordDB(self):
		content = ""
		self.keyworddb = {}
		with open('examples/keyworddb', 'r') as file:
                        content = file.read()

		for line in content.split("\n"):
			if len(line) == 0:
				continue

			if line[0] == '#':
				continue

			items = line.split(":")
			if len(items) < 2:
				continue

			self.keyworddb[items[0]] = ":".join(items[1:])

	def pretokenize(self, line):
		line = line.replace('&', "&amp;")
		line = line.replace('<', "&lt;")
		line = line.replace('>', "&gt;")
		return line

	def tokenize(self, line):
		return line.replace('\t', 6*"&nbsp;")

	def colorKeywords(self, line):
		for keyword in self.keywords:
			line = re.sub(r"(\s)(%s)(\s)" % keyword, r"\1<span class='%s'>\2</span>\3" % (keyword.replace('#', '')), line)
			line = re.sub(r"^%s(\s)" % keyword, r"<span class='%s'>%s</span>\1" % (keyword.replace('#', ''), keyword), line)
			line = re.sub(r"(\s)%s$" % keyword, "\1<span class='%s'>%s</span>" % (keyword.replace('#', ''), keyword), line)
		return line

	def colorLiterals(self, line):
		line = re.sub(r"('[^']*')", r"<span class='str_literal'>\1</span>", line)
		line = re.sub(r'("[^"]*")', r"<span class='str_literal'>\1</span>", line)
		return line

	def highlightKeyword(self, line, keyword, value):
		line = line.replace(keyword, "<span class='highlight'>%s</span>" % keyword)
		return line + "<span class='highlight_text'>%s</span>" % value

	def needinfoKeyword(self, line, keyword, value):
		line = line.replace(keyword, "<span class='needinfo'>%s</span>" % keyword)
		return line + "<span class='needinfo_text'><b>NEEDINFO:</b> %s</span>" % value

	def printPage(self, file):
		with open(file, 'w') as file:
			file.write("<!DOCTYPE html PUBLIC \"-//W3C//DTD XHTML 1.0 Strict//EN\" \"http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd\">\n")
			file.write("<html>\n")
			file.write("<head>\n")
			file.write("<link rel=\"stylesheet\" type=\"text/css\" href=\"../layout/vis.css\" />\n")
			file.write("<script type=\"text/javascript\" src=\"../layout/jquery-1.9.1.js\"></script>\n")
			file.write("<script type=\"text/javascript\" src=\"../layout/vis.js\"></script>\n")
			file.write("<script type=\"text/javascript\">\n<!--\n")
			file.write("$(document).ready(function() { $('span.fold_off').hide(); })\n")
			file.write("// -->\n</script>\n")
			file.write("</head>\n")
			file.write("<body>\n")

			self.parseKeywordDB()

			count = len(self.src_lines)
			fold_id = 1
			fold = False
			fold_start = -1
			fold_end = -1
			fold_text = ""
			folded = 0
	                for index in range(0, count):
				ln = "%4s" % (index + 1)
				ln = ln.replace(' ', "&nbsp;")
				line = self.src_lines[index]
				line = self.pretokenize(line)

				if (index + 1) in self.vis_lines:
					command = self.vis_lines[index + 1]
					if command['command'] == 'comment':
						if len(line) > 0:
							line = line + 3*"&nbsp;"
						line = line + "<span class='comment'>%s</span>" % (self.pretokenize(command['value']))
					elif command['command'] == 'fold':
						fold = True
						fold_start = index + 1
						fold_end = command['endline']
						fold_text = self.pretokenize(command['value'])
						folded = command['folded']
					elif command['command'] == 'highlight':
						line = self.highlightKeyword(line, command['keyword'], self.pretokenize(command['value']))
					elif command['command'] == 'needinfo':
	                                        line = self.needinfoKeyword(line, command['keyword'], self.pretokenize(command['value']))
				else:
					line = self.colorLiterals(line)
					line = self.colorKeywords(line)

					for keyword in self.keyworddb:
						if keyword in line:
							line = self.highlightKeyword(line, keyword, self.keyworddb[keyword])

				line = self.tokenize(line)

				prefix = ""
				sufix = "<br />"
				if fold and fold_start == (index + 1):
					prefix = "<span class='fold_button fold_off fold_off_id_%d' onclick='toggleFold(%d)'>Unfold</span>" % (fold_id, fold_id)
					prefix = prefix + "<span class='fold_button fold_on fold_on_id_%d' onclick='toggleFold(%d)'>Fold</span>" % (fold_id, fold_id)
					prefix = prefix + "<span class='fold_text'>%s</span><br />" % fold_text
					prefix = prefix + "<div class='fold' id='fold_%d'>" % fold_id

					if folded:
						file.write("<script type='text/javascript'>\n")
						file.write("$(document).ready(function() { toggleFold(%d) })\n" % fold_id)
						file.write("</script>\n")

					fold_id = fold_id + 1

				if fold and fold_end == (index + 1):
					sufix = "</div>"
					fold = False

	                        file.write("%s%s %s%s\n" % (prefix, ln, line, sufix))

			file.write("</body>\n")
			file.write("</html>\n")
