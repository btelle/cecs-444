#!/usr/bin/python

"""
# Brandon Telle
# CECS 444 Assignment 2
# Baby Scanner Class
# I alone wrote and modified what is turned in here
"""

import re #RegEx


### Constants ###
ERROR = 0
CONTINUE = 1
HALT = 2

IDENTIFIER = 1
INTEGER = 2
DOUBLE = 3
ASSIGN = 4
ADDOP = 5
SIMPLEOP = 6

# Psuedo-constants, for pretty tables
ER = ERROR
MA = CONTINUE
HR = HALT

ID = IDENTIFIER
INT = INTEGER
REAL = DOUBLE
EQ = ASSIGN
ADD = ADDOP
END = SIMPLEOP

class Scanner_Class:
	
	current_read = 0
	state = 0
	token_under_construction = ""

	# Logging levels
	L_DEBUG = 1
	L_ERROR = 2
	L_TOKEN = 3

	# Logging arrays
	mes_all = []
	mes_error = []
	mes_debug = []
	mes_token = []
	
	source_text = ""

	# State Table
	state_table = [  [ 1,  2,  3,  4,  5,  6, -1, -1],
			         [ 1, -1,  7, -1, -1, -1, -1, -1],
			         [ 2,  2, -1, -1, -1, -1,  8, -1],
			         [ 7, -1, -1, -1, -1, -1, -1, -1],
			         [-1, -1, -1, -1, -1, -1, -1, -1],
			         [-1, -1, -1, -1, -1, -1, -1, -1],
			         [-1, -1, -1, -1, -1, -1, -1, -1],
			         [ 7, -1, -1, -1, -1, -1, -1, -1],
			         [ 2,  2, -1, -1, -1, -1,  8, -1]  ]

	# Action Table
	action_table = [  [MA, MA, MA, MA, MA, MA, ER, ER],
			          [MA, HR, MA, HR, HR, HR, HR, HR],
			          [MA, MA, HR, HR, HR, HR, MA, HR],
			          [MA, ER, ER, ER, ER, ER, ER, ER],
			          [HR, HR, HR, HR, HR, HR, HR, HR],
			          [HR, HR, HR, HR, HR, HR, HR, HR],
			          [HR, HR, HR, HR, HR, HR, HR, HR],
			          [MA, HR, HR, HR, HR, HR, HR, HR],
			          [MA, MA, ER, ER, ER, ER, MA, ER]  ]

	# Look-up Table
	look_up_table = [  [  ER,   ER,   ER,   ER,   ER,   ER,   ER,   ER],
		    	       [  ER,  INT,   ER,  INT,  INT,  INT,  INT,  INT],
		               [  ER,   ER,   ID,   ID,   ID,   ID,   ID,   ID],
		               [  ER,   ER,   ER,   ER,   ER,   ER,   ER,   ER],
		               [  EQ,   EQ,   EQ,   EQ,   EQ,   EQ,   EQ,   EQ],
		               [ ADD,  ADD,  ADD,  ADD,  ADD,  ADD,  ADD,  ADD],
		               [ END,  END,  END,  END,  END,  END,  END,  END],
		               [  ER, REAL, REAL, REAL, REAL, REAL, REAL, REAL],
		               [  ER,   ER,   ER,   ER,   ER,   ER,   ER,   ER]  ]
	"""
	Scans the file at filename
	@throws IOError, SyntaxError
	"""
	def read_characters(self, filename):
		self.clear_messages()
		
		current_char = ''
		buffered = False

		try:
			file = open(filename, 'r')
			file_contents = file.read()
			file.close()
	
		except IOError:
			self.log('Input file not found', self.L_ERROR)
			raise IOError('Input file not found')
		
		self.source_text = file_contents
		i = 0
		
		while i < len(file_contents):
			if (not buffered) or (current_char == ' ') or (current_char == '\n'):
				current_char = file_contents[i]
				i += 1
			
			self.log("Current char: "+current_char+", EOF Status: "+str(i == len(file_contents)), self.L_DEBUG)
			
			# L=0, D=1, .=2, ==3, +=4, ;=5, _=6, [other]=7
			if self.is_alpha(current_char):
				self.current_read = 1
			elif self.is_digit(current_char):
				self.current_read = 0
			elif self.is_space(current_char):
				self.current_read = 7
			else:	# Special chars
			
				# Python doesn't do switches...
				if   current_char == '.': self.current_read = 2
				elif current_char == '=': self.current_read = 3
				elif current_char == '+': self.current_read = 4
				elif current_char == ';': self.current_read = 5
				elif current_char == '_': self.current_read = 6
				else: self.current_read = 7
				
			# Stats
			cur_stats =  "Current state: "+str(self.state)+", "
			cur_stats += "current_char: "+str(current_char)+", "
			cur_stats += "current_read: "+str(self.current_read)+", "
			cur_stats += "token status: "+str(self.token_under_construction)
			self.log(cur_stats, self.L_DEBUG)
			
			# Adding to token
			if ((self.next_state(self.state, self.current_read) != -1) and 
					(self.action(self.state, self.current_read) == CONTINUE)):
				
				buffered = False
				self.token_under_construction += current_char
				self.state = self.next_state(self.state, self.current_read)
				
			# Halting
			elif ((self.next_state(self.state, self.current_read) == -1) and
					(self.action(self.state, self.current_read) == HALT)):
					
				look_up = self.look_up(self.state, self.current_read)
				self.log("Inside switch with state "+str(self.state), self.L_DEBUG)
				self.log("The look-up value is "+str(look_up), self.L_DEBUG)
				self.log("We have a buffered char of '"+current_char+"'", self.L_DEBUG)
				buffered = True
				
				token_found = "TOKEN DISCOVERED IS "
	
				# Python still doesn't do switches :(
				if   look_up == IDENTIFIER:
					token_found += "AN IDENTIFIER -> "+self.token_under_construction
					
				elif look_up == INTEGER:
					token_found += "AN INTEGER -> "+self.token_under_construction
					
				elif look_up == DOUBLE:
					token_found += "A DOUBLE -> "+self.token_under_construction
					
				elif look_up == ASSIGN:
					token_found += "AN ASSIGNMENT OP -> "+self.token_under_construction
					
				elif look_up == ADDOP:
					token_found += "AN ADD OP -> "+self.token_under_construction
					
				elif look_up == SIMPLEOP:
					token_found += "A SIMPLE OP -> "+self.token_under_construction
					
				else:
					token_found += "AN ERROR!"
				
				self.log(token_found, self.L_TOKEN)
					
				# Return to S0
				self.state = 0
				
				# Reset token
				self.token_under_construction = ""

			# Syntax Error
			elif ((self.next_state(self.state, self.current_read) == -1) and
					(self.action(self.state, self.current_read) == ERROR)):
				self.log("Illegal character '"+current_char+"'", self.L_ERROR)
				raise SyntaxError("Illegal character '"+current_char+"'")

				
		# End while
		self.log("Done scanning!", self.L_DEBUG)
		
	# End read_characters
	
	"""
	State table look up
	@return next state number, or -1 on error
	"""
	def next_state(self, new_state, new_char):
		return self.state_table[new_state][new_char]
	
	"""
	Action table look up
	@return ERROR, CONTINUE, or HALT
	"""	
	def action(self, new_state, new_char):
		return self.action_table[new_state][new_char]
	
	"""
	Look-up table look up
	@return A token type, or ERROR
	"""
	def look_up(self, new_state, new_char):
		return self.look_up_table[new_state][new_char]
	
	"""
	Check if character is a-z
	@return true is alphabetical, false otherwise
	"""
	def is_alpha(self, char):
		search=re.compile(r'[^a-zA-Z]').search
		return not bool(search(char))
	
	"""
	Check if character is a digit
	@return true if numeric, false otherwise
	"""
	def is_digit(self, char):
		search=re.compile(r'[^0-9]').search
		return not bool(search(char))
		
	"""
	Check if a character is white space
	@return true if white space, false otherwise
	"""
	def is_space(self, char):
		return char == ' ' or char == '\n' or char == '\r' or char == '\t'

	"""
	Log a message to internal log arrays
	@param mes message to log
	@param level logging level to use
	"""
	def log(self, mes, level):
		self.mes_all.append(mes)

		if level == self.L_ERROR:
			self.mes_error.append(mes)

		if level == self.L_DEBUG:
			self.mes_debug.append(mes)

		if level == self.L_TOKEN:
			self.mes_token.append(mes)

	"""
	Get all logged messages
	@return array of logged messages
	"""
	def output(self):
		return self.mes_all

	"""
	Get all error messages
	@return array of error messages
	"""
	def error(self):
		return self.mes_error

	"""
	Get all token messages
	@return array of token messages
	"""
	def tokens(self):
		return self.mes_token

	"""
	Get the full text of the source scanned
	@return string of source text
	"""
	def source(self):
		return self.source_text
		
	def clear_messages(self):
		self.mes_all = []
		self.mes_error = []
		self.mes_debug = []
		self.mes_token = []
		