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
def getCodeKeywordsOccurences(file):
	lex.lex()

	with open(file, "r") as fd:
		content = fd.read()
		lex.input(content)

	keywords = {}
	line_number = 1
	for tok in iter(lex.token, None):
		#print repr(tok.type), repr(tok.value), line_number

		if tok.type == 'COMMENT':
			line_number = line_number + 1
		elif tok.type == 'WHITESPACE' or tok.type == 'MCOMMENT':
			line_number = line_number + tok.value.count('\n')
		else:
			# save only identifiers
			if tok.type == 'IDENTIFIER':
				# filter out all language keywords

				# save into db keyword and its line number
				if repr(tok.value) not in keywords:
					keywords[repr(tok.value)] = [line_number]
				if line_number not in keywords[repr(tok.value)]:
					keywords[repr(tok.value)].append(line_number)

	for key in keywords:
		print "%s (%s)" % (key, str(keywords[key]))

if __name__ == "__main__":
	getCodeKeywordsOccurences(sys.argv[1])
