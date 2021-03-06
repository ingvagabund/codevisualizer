import re
import os
import shutil

class HTMLVisualizer(object):

	def __init__(self, src_lines, src_keywords, src_comments, vis_lines, keywords_file, script_dir):
		self.src_lines = src_lines
		self.src_keywords = src_keywords
		self.src_comments = src_comments
		self.vis_lines = vis_lines
		self.keywords_file = keywords_file
		self.layout_dir = "%s/layout" % script_dir
		self.keywords = self.getKeywords()

	def copyLayout(self, layout_dir, destination):
		# copy css
		#shutil.copyfile("%s/vis.css" % layout_dir, "%s/vis.css" % destination)
		#shutil.copyfile("%s/vis.js" % layout_dir, "%s/js.css" % destination)
		#shutil.copyfile("%s/jquery-1.9.1.js" % layout_dir, "%s/jquery-1.9.1.js" % destination)	
		if os.path.exists("%s/layout" % destination):
			shutil.rmtree("%s/layout" % destination)

		shutil.copytree(layout_dir, "%s/layout" % destination)

	def getKeywords(self):
		content = ""
		with open(self.keywords_file, 'r') as file:
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

	def parseKeywordDB(self, file):
		content = ""
		keyworddb = {}

		# keyworddb exists?
		if not os.path.exists(file):
			open(file, 'a').close()
			return {}

		with open(file, 'r') as fd:
                        content = fd.read()

		for line in content.split("\n"):
			if len(line) == 0:
				continue

			if line[0] == '#':
				continue

			items = line.split(":")
			if len(items) < 2:
				continue

			keyworddb[items[0]] = ":".join(items[1:])

		return keyworddb

	def pretokenize(self, line):
		line = line.replace('&', "&amp;")
		line = line.replace('<', "&lt;")
		line = line.replace('>', "&gt;")
		return line

	def tokenize(self, line):
		return line.replace('\t', 6*"&nbsp;")

	def postTokenize(self, line):
		in_tag = 0
		oline = ""
		for char in line:
			if char == ' ' and in_tag == 0:
					oline = oline + "&nbsp;"
			else:
				oline = oline + char

			if char == '<':
				in_tag = in_tag + 1
			elif char == '>':
				in_tag = in_tag - 1
		
		return oline

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

	def commentBox(self, comment):
		return "<span class='comment'>%s</span>" % comment

	def highlightKeyword(self, line, keyword, value):
		line = line.replace(keyword, "<span class='highlight'>%s</span>" % keyword)
		return line + "<span class='highlight_text'>%s</span>" % value

	def needinfoKeyword(self, line, keyword, value, attrs):
		lkeyword = keyword
		if 'link' in attrs:
			lkeyword = "<a href='#%s'>%s</a>" % (attrs['link'], keyword)

		line = line.replace(keyword, "<span class='needinfo'>%s</span>" % lkeyword)
		return line + "<span class='needinfo_text'><b>NEEDINFO:</b> %s</span>" % value

	def highlightBox(self, keyword):
		return "<span class='highlight'>%s</span>" % keyword

	def needinfoBox(self, keyword, attrs):
		lkeyword = keyword
                if 'link' in attrs:
                        lkeyword = "<a href='#%s'>%s</a>" % (attrs['link'], keyword)

		return "<span class='needinfo'>%s</span>" % lkeyword

	def highlightLabel(self, value):
		return "<span class='highlight_text'>%s</span>" % value
		
	def needinfoLabel(self, value):
		return "<span class='needinfo_text'><b>NEEDINFO:</b> %s</span>" % value

	def add2lnSubs(self, clm, size, value):
		#print "clm: %d" % clm
		if clm not in self.ln_subs:
			self.ln_subs[clm] = [(size, value)]
		else:
			self.ln_subs[clm].append( (size, value) )

	def decomposeLineForSubs(self, line, points):
		#print line
		# get all intersection points
		i_points = {}
		i_substs = {}
		for point in points:
			sz = 0
			i_substs[point] = []

			for (size, subs) in points[point]:
				sz = max(sz, size)
				if point in i_substs:
					i_substs[point].append(subs)
				else:
					i_substs[point] = [subs]

			i_points[point] = sz

		if i_points:
			#print i_points
			ks = sorted(i_points.keys())
			#print ks

			d_lines = []
			pks = 0
			for p in ks:
				#print p
				d_lines.append( (line[pks:p-1], line[pks:p-1]) )
				#print line[pks:p-1]
				# primarly for more comments at the end of a line
				# but having more highlighted keywords (needinfo+highligh)
				jp = "".join(i_substs[p])
				#print jp
				# THIS IS HACK, HAS TO BE REWRITTEN!!!
				if len(i_substs[p]) == 2:
					if "<span class='highlight'>" in jp and "<span class='needinfo'>" in jp:
						keyword = re.sub(r"<[^>]*>", "", jp)
						# now the keyword is 2 times duplicated
						size = len(keyword)
						keyword = keyword[:size/2]
						jp = "<span class='highlight'><span class='needinfo'>%s</span></span>" % (keyword)

				d_lines.append( (line[(p-1):p - 1 + i_points[p]], jp ) )
				#print d_lines
				pks = i_points[p] + p - 1
			# append the last bit of the line
			d_lines.append( (line[pks:], line[pks:]) )
			#exit(0)
			return d_lines

		return [(line,line)]

	def addToCommentsDB(self, line, column, start):
		if line not in self.comments_db:
			self.comments_db[line] = [(column, start)]
		else:
			self.comments_db[line].append( (column, start) )

	def processComments(self):
		self.comments_db = {}
		for [(ls,cs),(le,ce)] in self.src_comments:
			self.addToCommentsDB(ls, cs, True)
			self.addToCommentsDB(le, ce, False)

	def printPage(self, file, destination):

		with open("%s/%s.html" % (destination, file), 'w') as fd:
			fd.write("<!DOCTYPE html PUBLIC \"-//W3C//DTD XHTML 1.0 Strict//EN\" \"http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd\">\n")
			fd.write("<html>\n")
			fd.write("<head>\n")
			fd.write("<link rel=\"stylesheet\" type=\"text/css\" href=\"layout/vis.css\" />\n")
			fd.write("<script type=\"text/javascript\" src=\"layout/jquery-1.9.1.js\"></script>\n")
			fd.write("<script type=\"text/javascript\" src=\"layout/vis.js\"></script>\n")
			fd.write("<script type=\"text/javascript\">\n<!--\n")
			fd.write("$(document).ready(function() { $('span.fold_off').hide(); })\n")
			fd.write("// -->\n</script>\n")
			fd.write("</head>\n")
			fd.write("<body>\n")

			self.copyLayout(self.layout_dir, destination)
			self.keyworddb = self.parseKeywordDB("%s/keyworddb" % destination)
			filekeyworddb = self.parseKeywordDB("%s/%s.keyworddb" % (destination, file))

			# source code file specific keywords has higher priority (later maybe display both)
			for key in filekeyworddb:
				self.keyworddb[key] = filekeyworddb[key]

			#self.src_keywords
			

			count = len(self.src_lines)
			fold_id = 1
			fold = False
			fold_start = -1
			fold_end = -1
			fold_text = ""
			folded = 0
			fold_stack = []

			self.processComments()

	                for index in range(0, count):
				ln = "%4s" % (index + 1)
				ln = "<a name='%s'>%s</a>" % (index + 1, ln.replace(' ', "&nbsp;"))
				oline = line = self.src_lines[index]

				self.ln_subs = {}

				if (index + 1) in self.vis_lines:
					commands = self.vis_lines[index + 1]
					for command in commands:
						if command['command'] == 'comment':
							#print index + 1
							prefix = ""
							if len(line) > 0:
								prefix = 3*"&nbsp;"
							# put comment at the end of the current line
							clm = len(oline) + 1
							self.add2lnSubs(clm, len(command['value']), prefix + self.commentBox( command['value'] ))

						elif command['command'] == 'fold':
							fold = True
							fold_start = index + 1
							fold_end = command['endline']
							fold_text = self.pretokenize(command['value'])
							folded = command['folded']

							fold_stack.append( {'id': fold_id, 'start': index + 1, 'end': command['endline'], 'folded': command['folded'], 'label': self.pretokenize(command['value']) } )
							fold_id = fold_id + 1

						elif command['command'] == 'highlight':
							v_keyword = command['keyword']
							if v_keyword in self.src_keywords and (index + 1) in self.src_keywords[ v_keyword ]:
								clm = self.src_keywords[ v_keyword ][ index + 1 ]
								for clm_item in clm:
									self.add2lnSubs(clm_item, len(v_keyword), self.highlightBox(v_keyword))
									comment = self.highlightLabel( self.pretokenize(command['value']) )
									self.add2lnSubs(len(oline)+1, len(comment), comment)
						elif command['command'] == 'needinfo':
							v_keyword = command['keyword']
							if v_keyword in self.src_keywords and (index + 1) in self.src_keywords[ v_keyword ]:
	                                                        clm = self.src_keywords[ v_keyword ][ index + 1 ]
	                                                        for clm_item in clm:
									self.add2lnSubs(clm_item, len(v_keyword), self.needinfoBox(v_keyword, command['attrs']))
									comment = self.needinfoLabel( self.pretokenize(command['value']) )
									self.add2lnSubs(len(oline)+1, len(comment), comment)
						
				for keyword in self.keyworddb:
					if keyword not in self.src_keywords:
						continue

					if (index + 1) not in self.src_keywords[ keyword ]:
						continue

					clm = self.src_keywords[ keyword ][ index + 1 ]
					for clm_item in clm:
						self.add2lnSubs(clm_item, len(keyword), self.highlightBox(keyword))
						comment = self.highlightLabel( self.pretokenize( self.keyworddb[keyword]) )
						self.add2lnSubs(len(oline)+1, len(comment), comment)
							

				# color comments
				if index + 1 in self.comments_db:
					for (column, start) in self.comments_db[index + 1]:
						#print (column, start)
						if start:
							self.add2lnSubs(column, 0, "<span class='codecomment'>")
						else:
							self.add2lnSubs(column, 0, "</span>")
						#print self.ln_subs[column]

				out_line = []
				# split the line into pairs of substrings (to replace, replace with
				d_lines = self.decomposeLineForSubs(oline, self.ln_subs)
				for (orig, new) in d_lines:
					if orig == new:
						new = self.pretokenize(new)
						new = self.colorLiterals(new)
						new = self.colorKeywords(new)
						new = self.tokenize(new)
						new = self.postTokenize(new)

					out_line.append(new)
				
				out_line = "".join(out_line)

				prefix = ""
				sufix = "<br />"
				# get the current fold
				cfold = []
				if fold_stack:
					fold = True
					cfold = fold_stack[-1]
				else:
					fold = False

				if fold and cfold['start'] == (index + 1):
					prefix = "<span class='fold_button fold_off fold_off_id_%d' onclick='toggleFold(%d)'>Unfold</span>" % (cfold['id'], cfold['id'])
					prefix = prefix + "<span class='fold_button fold_on fold_on_id_%d' onclick='toggleFold(%d)'>Fold</span>" % (cfold['id'], cfold['id'])
					prefix = prefix + "<span class='fold_text'>%s</span><br />" % cfold['label']
					prefix = prefix + "<div class='fold' id='fold_%d'>" % cfold['id']

					if cfold['folded']:
						fd.write("<script type='text/javascript'>\n")
						fd.write("$(document).ready(function() { toggleFold(%d) })\n" % cfold['id'])
						fd.write("</script>\n")

				if fold and cfold['end'] == (index + 1):
					sufix = "</div>"
					while True:
						# remove fold from stack
						del(fold_stack[-1])
						if fold_stack and fold_stack[-1]['end'] == (index + 1):
							sufix = sufix + "</div>"
							cfold = fold_stack[-1]
							continue
						else:
							break

				fd.write("%s%s %s%s\n" % (prefix, ln, out_line, sufix))

			fd.write("</body>\n")
			fd.write("</html>\n")
