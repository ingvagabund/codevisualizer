#!/bin/python

import sys
from ply import lex

tokens = [
"IDENTIFIER",
"MACRO",
"WHITESPACE",
"COMMENT",
"INCLUDE",
"NUMBER",
#"LITERAL",
"LPARENTHESIS",
"RPARENTHESIS",
"SEMICOLON",
"COMMA",
"ASTERISK"
]

#C identifier
t_IDENTIFIER = (r"[a-zA-Z_]\w+")
#C macro
t_MACRO = (r"\#[a-zA-Z_]\w+")

#C whitespaces
t_WHITESPACE = (r"\s+")

# one line and multi-line comment
t_COMMENT = (
	r"//[^\n]*|"
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

# semicolon, comma, asterisk
t_SEMICOLON = (r";")
t_COMMA = (r",")
t_ASTERISK = (r"\*")

def t_error(t):
	raise TypeError("Unknown text '%s'" % (t.value,))

lex.lex()

with open(sys.argv[1], "r") as fd:
	#lex.input("hokus pokus\nnew line//one line comment\nnext line/* multi\nli**ne\co*m*m/ent*/")
	content = fd.read()
	#content = "/***//* */"
	#print content.replace('\n', "\\n")
	#content = "/*\n * This file is part of Taylor/core.\n\n    Taylor/core is free software: you can redistribute it and/or modify\n    it under the terms of the GNU General Public License as published by\n    the Free Software Foundation, either version 3 of the License, or\n    (at your option) any later version.\n\n    OpenGalaxySim is distributed in the hope that it will be useful,\n    but WITHOUT ANY WARRANTY; without even the implied warranty of\n    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the\n    GNU General Public License for more details.\n\n    You should have received a copy of the GNU General Public License\n    along with OpenGalaxySim.  If not, see <http://www.gnu.org/licenses/>.\n * \n * File:   error.h\n * Author: Vasek Vopenka\n *\n * Created on September 12, 2011, 11:57 AM\n */"
	lex.input(content)
	#lex.input("")

for tok in iter(lex.token, None):
    print repr(tok.type), repr(tok.value)
