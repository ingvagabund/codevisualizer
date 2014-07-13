#!/bin/python

import sys
from ply import lex

tokens = [
"IDENTIFIER",
"MACRO",
"WHITESPACE",
"COMMENT",
"MCOMMENT",
"INCLUDE",
"NUMBER",
#"LITERAL",
"LPARENTHESIS",
"RPARENTHESIS",
"LBRACKET",
"RBRACKET",
"LBRACE",
"RBRACE",
"SEMICOLON",
"COMMA",
"ASTERISK",
"EQUAL",
"ASSIGN",
"DIVIDE",
"NOT",
"MINUSLESS",
"STRING",
"CHARACTER",
"LESS",
"LEQ",
"GREATER",
"GEQ",
"NEQ",
"OR",
"AND",
"PLUS",
"MINUS",
"QUESTION",
"COLON",
"BAND",
"BOR",
"BACKSLASH",
"DOT"
]

t_BACKSLASH = (r"[\\]")

t_STRING = (r"\".*?\"")
t_CHARACTER = (r"'.*?'")

t_MINUSLESS = ("->")
t_QUESTION = (r"\?")
t_COLON = (":")
t_DOT = (".")

# unary operators

# binary operators
t_DIVIDE = ("/")
t_MINUS = ("-")
t_PLUS = (r"\+")

# bit operatos
t_BOR = (r"\|")
t_BAND = ("&")

# logical operatos
t_AND = ("&&")
t_OR = ("\|\|")
t_NOT = ("!")

# relational operators
t_GEQ = (">=")
t_LEQ = ("<=")
t_GREATER = (">")
t_LESS = ("<")
t_EQUAL = ("==")

# assigment
t_ASSIGN = ("=")

#C identifier
t_IDENTIFIER = (r"[a-zA-Z_]\w*")
#C macro
t_MACRO = (r"\#[a-zA-Z_]\w+")

#C whitespaces
t_WHITESPACE = (r"\s+")

# one line and multi-line comment
t_COMMENT = (
	r"//[^\n]*"
)

t_MCOMMENT = (
	r"/\*(\n|.)*?\*/"
)

# include <|"file.h"|>
t_INCLUDE = (
	r"\#include\s+<.+?>|"
	r"\#include\s+\".+?\""
)

# number
t_NUMBER = (r"(\+|-)?\d+(\.\d+)?(e|E((\+|-)?\d+))?")

# literal

# left,right parenthesis
t_LPARENTHESIS = (r"\(")
t_RPARENTHESIS = (r"\)")

# left, right bracket
t_LBRACKET = (r"\[")
t_RBRACKET = (r"\]")

# left, right brace
t_LBRACE = (r"\{")
t_RBRACE = (r"\}")

# semicolon, comma, asterisk
t_SEMICOLON = (r";")
t_COMMA = (r",")
t_ASTERISK = (r"\*")

def t_error(t):
	raise TypeError("Unknown text '%s'" % (t.value[0:20],))

################################################
source_code_keywords = {}
source_code_comments = []
def getCodeKeywordsOccurences(file):
	lex.lex()

	with open(file, "r") as fd:
		content = fd.read()
		lex.input(content)

	line_number = 1
	column_number = 1
	for tok in iter(lex.token, None):
		#print tok
		#print repr(tok.type), repr(tok.value), line_number, column_number
		# for each token compute next column_number (not for actual token but for the next)
		if tok.type == 'COMMENT':
			#print line_number, tok.value
			mcomment = []
			mcomment.append( (line_number, column_number) )
			#print (line_number, column_number)
			#print repr(tok.value)[1:-1]
			#print (line_number, column_number + len(repr(tok.value)[1:-1]) - 1)
			mcomment.append( (line_number, column_number + len(repr(tok.value)[1:-1]) - 1) )
			#print mcomment
			source_code_comments.append( mcomment )
			column_number = 1
		elif tok.type == 'WHITESPACE' or tok.type == 'MCOMMENT':
			#if tok.type == 'MCOMMENT':
			#	print line_number
			mcomment = []
			if tok.type == 'MCOMMENT':
				#print "cs: (%d, %d)" % (line_number, column_number)
				mcomment.append( (line_number, column_number) )

			line_number = line_number + tok.value.count('\n')
			# find the last \n character
			lnl = tok.value.rfind('\n')
			ll = len(tok.value)
			#print(ll, lnl + 1)

			if ll == (lnl + 1):
				column_number = 1
			else:
				if lnl != -1:
					column_number = ll - (lnl + 1) + 1
				else:
					column_number = column_number + ll
			if tok.type == 'MCOMMENT':
				#print "ce: (%d, %d)" % (line_number, column_number)
				mcomment.append( (line_number, column_number) )
				source_code_comments.append(mcomment)
				#print mcomment
		else:
			#print (line_number, tok.value)
			# save only identifiers
			if tok.type == 'IDENTIFIER':
				# filter out all language keywords

				# save into db keyword and its line number
				key = repr(tok.value)
				key = key[1:-1] # get rid of ' char at the beggining and end
				#print (key, line_number, column_number)
				if key not in source_code_keywords:
					source_code_keywords[key] = {line_number: [column_number]}
				if line_number not in source_code_keywords[key]:
					source_code_keywords[key][line_number] = [column_number]
				elif column_number not in source_code_keywords[key][line_number]:
					source_code_keywords[key][line_number].append(column_number)

			column_number = column_number + len(tok.value)

	#for key in source_code_keywords:
	#	print "%s (%s)" % (key, str(source_code_keywords[key]))
	return (source_code_keywords, source_code_comments)

if __name__ == "__main__":
	print getCodeKeywordsOccurences(sys.argv[1])
