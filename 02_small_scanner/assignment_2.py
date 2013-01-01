#!/usr/bin/python

"""
# Brandon Telle
# CECS 444 Assignment 2
# Scanner Client
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
	from graphical import wxScannerApp, wxScannerFrame 

except ImportError:
	nogui = True

# Scanner_Class
from scanner import Scanner_Class 

# Command line args
for opt in sys.argv:
	if opt == "verbose":
		verbose = True
	if opt == "nogui":
		nogui = True
	
try:
	in_file = sys.argv[len(sys.argv)-1]
	if len(sys.argv) == 1:
		in_file = "./source.txt"
except IndexError:
	in_file = "./source.txt"

# GUI mode
if __name__ == "__main__" and not nogui:
	app = wxScannerApp()
	app.MainLoop()
	
# Command line mode
else:
	scanner = Scanner_Class()

	try:
		scanner.read_characters(in_file)

	except Exception as strerror:
		sys.stderr.write('Error: '+str(strerror))
		sys.exit(1)

	if verbose:
		for line in scanner.output():
			print line
	else:
		for line in scanner.tokens():
			print line
