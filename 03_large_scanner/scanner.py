#!/usr/bin/python

"""
# scanner.py
# Brandon Telle
# CECS 444 Project 3
# Large Scanner Class
# I alone wrote and modified what is turned in here
"""

import re 	# RegEx


### Constants ###
ERROR = 0
CONTINUE = 1
HALT = 2

class Scanner_Class:
	
	current_read = 0
	state = 0
	token_under_construction = ""
	source_text = ""
	reserved_words = []
	used_identifiers = {}

	# Logging levels
	L_DEBUG = 1
	L_ERROR = 2
	L_TOKEN = 3

	# Logging arrays
	mes_all = []
	mes_error = []
	mes_debug = []
	mes_token = []

	token_table = {}
	symbol_table = {}
	state_table = []
	action_table = []
	look_up_table = []
	
	"""
	Initialize scanner, scan external resources
	"""
	def __init__(self):
		self.init_reserved_words()
		self.init_token_table()
		self.init_symbol_table()
		self.state_table = self.read_csv('./tables/state_table.csv')
		self.action_table = self.read_csv('./tables/action_table.csv')
		self.look_up_table = self.read_csv('./tables/look_up_table.csv')
	
	"""
	Scans the file at filename
	@throws IOError, SyntaxError
	"""
	def read_characters(self, filename):
		self.clear_messages()
		self.used_identifiers = {}
		
		current_char = ''
		buffered = False

		try:
			file = open(filename, 'r')
			file_contents = file.read()
			file.close()
			file_contents = file_contents.replace('\t', '    ')
	
		except IOError:
			self.log('Input file not found', self.L_ERROR)
			raise IOError('Input file not found')
		
		self.source_text = file_contents
		i = 0
		
		while i < len(file_contents):
			if (not buffered) or (current_char == ' ') or (current_char == '\n'):
				current_char = file_contents[i]
				i += 1
			
			self.log("Current char: "+current_char+", EOF Status: "
				+str(i == len(file_contents)), self.L_DEBUG)
			
			self.current_read = self.character_look_up(current_char)
				
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
					
				self.log_token(self.token_look_up(look_up))
					
				# Return to S0
				self.state = 0
				
				# Reset token
				self.token_under_construction = ""

			# Syntax Error
			elif ((self.next_state(self.state, self.current_read) == -1) and
					(self.action(self.state, self.current_read) == ERROR) and 
					(self.current_read != 30) and (self.current_read != 31)):
				self.log("Illegal character '"+current_char+"'", self.L_ERROR)
				raise SyntaxError("Illegal character '"+current_char+"'")

				
		# End while
		self.log("Done scanning!", self.L_DEBUG)
		
	# End read_characters
	
	"""
	Push a found identifier onto the used_identifiers hash
	@return 0 if new identifier, 1 if already in table
	"""
	def push_identifier(self, id):
		ret = 1
		try:
			self.used_identifiers[id] = self.used_identifiers[id]+1
		except Exception:
			self.used_identifiers[id] = 1
			ret = 0
		return  ret

	###################################################
	# Look up functions
	
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
	Look up a character in symbol_table
	@return character code of char
	"""
	def character_look_up(self, char):
		ret = 32
		
		if self.is_alpha(char):
			ret = 0
		elif self.is_digit(char):
			ret = 1
		else:	# Special chars
			try:
				ret = self.symbol_table[char]
			except Exception:
				ret = 32
		
		if char == '\t':	# Tabs count as spaces for whitespace ignoring
			ret = 31
			
		return ret
		
	"""
	Look up a token in the token table
	Does some size checking to make sure tokens are valid
	@return plain text representation of token
	"""
	def token_look_up(self, token):
		try:
			look_up = self.token_table[token]
		except IndexError:
			look_up = "error"
		
		# Context checking
		# Identifiers
		if token == 1:
			if self.is_reserved(self.token_under_construction):
				look_up = "identifier and reserved word"
			else:
				tmp = self.push_identifier(self.token_under_construction)
				if tmp == 0:
					look_up = "identifier inserted into table"
				else:
					look_up = "identifier EXISTS in table"
		
		# Integers
		if token == 2:
			tmp = abs(int(str(self.token_under_construction).replace(',', '')))
			if tmp > 8589934592:
				look_up = "invalid integer"
				
		# Currency
		if token == 9:
			tmp = float(str(self.token_under_construction).replace(',', '').replace('$', ''))
			if tmp > 9999999999:
				look_up = "invalid currency"
				
		# Real lit
		if token == 3:
			length = len(str(self.token_under_construction).replace('-', ''))
			if length > 17:
				look_up = "invalid real literal"
		
		return look_up

 	###################################################
	# Is-a functions

	"""
	Check if character is a-z
	@return true if alphabetical, false otherwise
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
		return char == ' ' or char == '\t'
	
	"""
	Check if word is in the reserved words list
	@return true if word is reserved, false otherwise
	"""
	def is_reserved(self, word):
		try:
			return self.reserved_words.index(word) >= 0
		except ValueError:
			return False

	###################################################
	# Logging

	"""
	Log a message to internal log arrays
	@param mes message to log
	@param level logging level to use
	"""
	def log(self, mes, level):
		mes = mes.replace("\n", "")
		self.mes_all.append(mes)

		if level == self.L_ERROR:
			self.mes_error.append(mes)

		if level == self.L_DEBUG:
			self.mes_debug.append(mes)

		if level == self.L_TOKEN:
			self.mes_token.append(mes)

	"""
	Log a found token
	"""
	def log_token(self, type):		
		token_found = self.token_under_construction+"\t"+type
		self.log(token_found, self.L_TOKEN)
	
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
		
	"""
	Get all the identifiers scanned with the frequency they were found
	@return dictionary of used identifiers
	"""
	def identifiers(self):
		return self.used_identifiers

	"""
	Clear message arrays, for multiple runs in one run
	"""
	def clear_messages(self):
		self.mes_all = []
		self.mes_error = []
		self.mes_debug = []
		self.mes_token = []
	
	###################################################
	# External file reads
	
	"""
	Initialize the reserved words list
	"""
	def init_reserved_words(self):
		fname = "./tables/reserved_words.txt"
		
		file = open(fname, 'r')
		contents = file.read()
		file.close()
		
		self.reserved_words = contents.split()
	
	"""	
	Read the token table from text file
	"""
	def init_token_table(self):
		file = open('./tables/token_list.txt')
		contents = file.read()
		file.close()
		
		for row in contents.split('\n'):
			if row != '':
				cols = row.split(':')
				self.token_table[int(cols[0])] = str(cols[1])
	
	"""
	Read the symbol table from a text file
	"""
	def init_symbol_table(self):
		file = open('./tables/symbol_list.txt')
		contents = file.read()
		file.close()
		
		for row in contents.split('\n'):
			cols = row.split(':')
			if cols[0] == 'E':		# Special case: EOL
				cols[0] = '\n'
				
			if cols[0] == 'C':		# Special case: Colon
				cols[0] = ':'
				
			self.symbol_table[str(cols[0])] = int(cols[1])

	"""
	Read a comma-separated values (CSV) file
	@return table of values in a 2-dimensional array
	"""
	def read_csv(self, filename):
		file = open(filename, 'r')
		contents = file.read()
		file.close()

		ret = []

		contents = contents.replace("MA", str(CONTINUE))
		contents = contents.replace("ER", str(ERROR))
		contents = contents.replace("HR", str(HALT))
		rows = contents.split("\n")
		for row in rows:
			tmp = row.split(',')
			if len(tmp) > 1:
				for i in range(0, len(tmp)):
					tmp[i] = int(tmp[i])
				ret.append(tmp)
		
		return ret
	

# End Scanner_Class
