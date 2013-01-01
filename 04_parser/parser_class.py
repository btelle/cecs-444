#!/usr/bin/python/

"""
# parser.py
# Brandon Telle
# CECstack.444 Project 4
# Large Parser Class
# I alone wrote and modified what is turned in here.
"""

from stack import Stack
from token import Token
from scanner import Scanner_Class

class Parser_Class:	
	reserved_list = {}
	token_list = {}

	# Logging levels
	L_DEBUG = 1
	L_ERROR = 2
	L_MATCH = 3

	# Logging arrays
	mes_all = []
	mes_error = []
	mes_debug = []
	mes_match = []

	"""
	Constructor
	Initializes external tables
	"""
	def __init__(self):
		self.stack_pushes = self.read_csv('./tables/stack_pushes.csv')
		self.parse_table = self.read_csv('./tables/parse_table.csv')
		self.init_reserved_list()
		self.init_token_list()

	"""
	Parse a given file. Uses Scanner_Class to scan file for tokens.
	"""
	def parse_file(self, filename):
		scanner = Scanner_Class(filename)
		self.source_text = scanner.source()
		self.clear_messages()
		ret = 1
			
		stack = Stack()
		stack.push(1)
		current_token = scanner.next_token()
		
		while not stack.empty():
			# Skip comments
			if current_token.type == 8:
				current_token = scanner.next_token()
				continue		
			
			# Map all terminals to an integer
			token_number = self.translate(current_token)
			
			# Get head of the stack
			stacktop = stack.head.value;
			
			# Stats
			self.log("current_token: "+str(current_token.toString()), self.L_DEBUG)
			self.log("token_number: "+str(token_number), self.L_DEBUG)
			#self.log("stacktop: "+str(stacktop), self.L_DEBUG)
			#self.log("stack count: "+str(stack.count()), self.L_DEBUG)
			self.log("current stack: "+str(stack.toString()), self.L_DEBUG)

			# Non-terminal symbols
			if stacktop > 0:
				table_entry = self.next_table_entry(stacktop, abs(token_number))
				
				if table_entry == 98:
					self.log("Scan error: dropping "+current_token.value, self.L_ERROR)
					current_token = scanner.next_token()

				elif table_entry == 99:
					self.log("Pop Error: popping "+str(stack.head.value), self.L_ERROR)
					stack.pop()
				
				elif table_entry <= len(self.stack_pushes):
					self.log("Fire "+str(table_entry), 
						self.L_MATCH)
					stack.pop()
					
					for i in self.pushes(table_entry-1):
						if i != 0:
							stack.push(i)
				else:
					self.log("Error!", self.L_ERROR)
			
			# Terminals - Match and pop
			elif stacktop == token_number:
				self.log("Match and pop "+
					str(current_token.value), self.L_MATCH)
				stack.pop()
				current_token = scanner.next_token()
			
			# Terminals - No Match :(
			else:
				self.log("Error -- Not Accepted", self.L_MATCH)
				break;

			# Success message
			if stack.empty():
				self.log("Accept", self.L_MATCH)
				ret = 0
		
		# End While

		return ret
	# End parse_file

	###################################################
	# Look Ups

	"""
	Look up a value in the parse table
	@return next level to fire
	"""
	def next_table_entry(self, non_terminal, token):
		return self.parse_table[non_terminal][token]
		
	"""
	Look up a table entry in the stack_pushes list
	@return list of values to push to the stack
	"""
	def pushes(self, level):
		row = self.stack_pushes[level]
		ret = []
		for i in row:
			if i != 0:
				ret.append(i)
		ret.reverse()
		return ret
		
	"""
	Translates a scanner token number into its appropriate parser
	token number.
	@return parser token number 
	"""
	def translate(self, token):
		ret = 0
		
		if token.type == 1:	# identifiers - reserved word check
			try:
				ret = self.reserved_list[token.value]
			except KeyError:
				ret = -3
		else:			# others - use token_list table
			try:
				ret = self.token_list[token.type]
			except IndexError:
				ret = 0
		
		return ret

	###################################################
	# Table Reads
		
	"""
	Read a comma-separated values (CSV) file
	@return table of values in a 2-dimensional array
	"""
	def read_csv(self, filename):
		file = open(filename, 'r')
		contents = file.read()
		file.close()

		ret = []

		rows = contents.split("\n")
		for row in rows:
			tmp = row.split(',')
			if len(tmp) > 1:
				for i in range(0, len(tmp)):
					tmp[i] = int(tmp[i])
				ret.append(tmp)
		
		return ret
	
	"""
	Initializes the reserved words list
	"""
	def init_reserved_list(self):
		file = open('./tables/parser_reserved.txt')
		contents = file.read()
		file.close()
		
		for row in contents.split('\n'):
			if row != '':
				cols = row.split(':')
				self.reserved_list[str(cols[0])] = int(cols[1])
	
	"""
	Initializes the token list 
	"""		
	def init_token_list(self):
		file = open('./tables/parser_tokens.txt')
		contents = file.read()
		file.close()
		
		for row in contents.split('\n'):
			if row != '':
				cols = row.split(':')
				self.token_list[int(cols[0])] = int(cols[1])

	"""
	Returns the source text being parsed.
	@return source string
	"""
	def source(self):
		return self.source_text

	###################################################
	# Logging

	"""
	Log a message to internal log arrays
	@param mes message to log
	@param level logging level to use
	"""
	def log(self, mes, level):
		#print mes
		mes = mes.replace("\n", "")
		self.mes_all.append(mes)

		if level == self.L_ERROR:
			self.mes_error.append(mes)
			self.mes_match.append(mes)

		if level == self.L_DEBUG:
			self.mes_debug.append(mes)

		if level == self.L_MATCH:
			self.mes_match.append(mes)

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
	def matches(self):
		return self.mes_match

	"""
	Clear message arrays, for multiple runs in one run
	"""
	def clear_messages(self):
		self.mes_all = []
		self.mes_error = []
		self.mes_debug = []
		self.mes_match = []


# End Parser_Class
