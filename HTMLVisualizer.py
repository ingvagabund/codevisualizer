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

	def printPage(self):
		print "<!DOCTYPE html PUBLIC \"-//W3C//DTD XHTML 1.0 Strict//EN\" \"http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd\">"
		print "<html>"
		print "<head>"
		print "<link rel=\"stylesheet\" type=\"text/css\" href=\"vis.css\" />"
		print "<script type=\"text/javascript\" src=\"jquery-1.9.1.js\"></script>"
		print "<script type=\"text/javascript\" src=\"vis.js\"></script>"
		print "<script type=\"text/javascript\">\n<!--"
		print "$(document).ready(function() { $('span.fold_off').hide(); })"
		print "// -->\n</script>"
		print "</head>"
		print "<body>"
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
			if (index + 1) in self.vis_lines:
				command = self.vis_lines[index + 1]
				if command['command'] == 'comment':
					if len(line) > 0:
						line = line + 3*"&nbsp;"
					line = line + "<span class='comment'>%s</span>" % (command['value'])
				elif command['command'] == 'fold':
					fold = True
					fold_start = index + 1
					fold_end = command['endline']
					fold_text = command['value']
					folded = command['folded']
				elif command['command'] == 'highlight':
					line = self.highlightKeyword(line, command['keyword'], command['value'])
			else:
				line = self.colorLiterals(line)
				line = self.colorKeywords(line)

			line = self.tokenize(line)

			prefix = ""
			sufix = "<br />"
			if fold and fold_start == (index + 1):
				prefix = "<span class='fold_button fold_off fold_off_id_%d' onclick='toggleFold(%d)'>Unfold</span>" % (fold_id, fold_id)
				prefix = prefix + "<span class='fold_button fold_on fold_on_id_%d' onclick='toggleFold(%d)'>Fold</span>" % (fold_id, fold_id)
				prefix = prefix + "<span class='fold_text'>%s</span><br />" % fold_text
				prefix = prefix + "<div class='fold' id='fold_%d'>" % fold_id

				if folded:
					print "<script type='text/javascript'>"
					print "$(document).ready(function() { toggleFold(%d) })" % fold_id
					print "</script>"

				fold_id = fold_id + 1

			if fold and fold_end == (index + 1):
				sufix = "</div>"
				fold = False

                        print "%s%s %s%s" % (prefix, ln, line, sufix)

		print "</body>"
		print "</html>"
