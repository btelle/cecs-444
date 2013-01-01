#!/usr/bin/python

"""
# assignment_4.py
# Brandon Telle
# CECS 444 Project 4
# Parser Client
# I alone wrote and modified what is turned in here
"""

# Default options
verbose = False
nogui = False

# System utils
import sys

# GUI
try:
	import wx
	from graphical import wxParserApp, wxParserFrame 

except ImportError:
	nogui = True

# Scanner_Class
from scanner import Scanner_Class 
from parser_class import Parser_Class
from token import Token

# Command line args
for opt in sys.argv:
	if opt == "verbose":
		verbose = True
	if opt == "nogui":
		nogui = True
	
try:
	in_file = sys.argv[len(sys.argv)-1]	# input file is last argument

	if len(sys.argv) == 1 and nogui:
		sys.stderr.write('Error: Input file required')
		sys.exit(1)

except IndexError:
	if nogui:
		sys.stderr.write('Error: Input file required')
		sys.exit(1)

# GUI mode
if __name__ == "__main__" and not nogui:
	app = wxParserApp()
	app.MainLoop()
	
# Command line mode
else:
	parser = Parser_Class()

	try:
		parser.parse_file(in_file)

	except Exception as strerror:
		sys.stderr.write('Error: '+str(strerror))
		sys.exit(1)

	# Verbose
	if verbose:
		for line in parser.output():
			print line
	# Not Verbose	
	else:
		for line in parser.matches():
			print line

# End Large Parser Client
