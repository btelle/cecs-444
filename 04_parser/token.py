#!/usr/bin/python

"""
# token.py
# Brandon Telle
# CECS 444 Project 4
# Simple Token Class
# I alone wrote and modified what is turned in here
"""

class Token:
	type = 0
	value = ""
	
	"""
	Return a stringified representation of the token
	@return string representation of the token
	"""
	def toString(self):
		return "Token of type "+str(self.type)+": "+str(self.value.replace("\n", "<EOL>"))
