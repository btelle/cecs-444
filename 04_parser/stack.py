#!/usr/bin/python

"""
# stack.py
# Brandon Telle
# CECS 444 Project 4
# Stack implementation for Python
# http://en.literateprograms.org/Stack_%28Python%29
"""

"""
Empty Stack Exception
"""
class EmptyStackException(Exception):
	pass

"""
Generic element class, used in Stack
"""
class Element:
	def __init__(self, value, next):
		self.value = value
		self.next = next
"""
Simple stack class
"""
class Stack:
	def __init__(self):
		self.head = None

	"""
	Push an element onto the stack
	"""
	def push(self, element):
		self.head = Element(element, self.head)

	"""
	Pop the head off the stack
	@return element the value of the element popped off
	"""
	def pop(self):
		if self.empty(): raise EmptyStackException
		result = self.head.value
		self.head = self.head.next
		return result
	
	"""
	Checks whether the stack is empty
	@return boolean true if stack is empty, false if not
	"""	
	def empty(self):
		return self.head == None
	
	"""
	Count the number of elements in the stack
	@return int number of elements in the stack
	"""	
	def count(self):
		eol = False
		count = 0
		pointer = self.head
		while not eol:
			count += 1
			if pointer.next != None:
				pointer = pointer.next
			else:
				eol = True
		return count

	"""
	Gets a list of all elements on the stack
	@return string representation of the stack
	"""
	def toString(self):
		eol = False
		out = ""
		pointer = self.head
		while not eol:
			out += str(pointer.value)+" "
			if pointer.next != None:
				pointer = pointer.next
			else:
				eol = True
		return out

# End Stack Class
