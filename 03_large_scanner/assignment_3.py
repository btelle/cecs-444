#!/usr/bin/python

"""
# assignment_3.py
# Brandon Telle
# CECS 444 Project 3
# Scanner Client
# I alone wrote and modified what is turned in here
# Usage: assignment_3.py [nogui] [verbose] input.src
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

	print "\nDiscovered Identifier: Times Used"
	ids = scanner.identifiers()
	for v in ids.keys():
		print v+": "+str(ids[v])

# End Large Scanner Client
