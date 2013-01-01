#!/usr/bin/python

"""
# graphical.py
# Brandon Telle
# CECS 444 Project 4
# Large Parser GUI
# I alone wrote and modified what is turned in here
"""

import wx, sys
from parser_class import Parser_Class 

class wxParserFrame(wx.Frame):
	
	"""
	Constructor
	"""
	def __init__(self, *args, **kwargs):
		wx.Frame.__init__(self, *args, **kwargs)
		self.create_controls()
	
	"""
	Creates the wigits within the new frame
	"""
	def create_controls(self):
		# Sizers
		self.h_sizer = wx.BoxSizer(wx.HORIZONTAL)
		self.v_sizer = wx.BoxSizer(wx.VERTICAL)

		# Labels
		self.file_label = wx.StaticText(self, label="File to parse:")
		self.out_file_label = wx.StaticText(self, label="Output file:")
		self.options_label = wx.StaticText(self, label="Options:")
		self.source_label = wx.StaticText(self, label="Source text:")
		self.output_label = wx.StaticText(self, label="Parser output:")
		
		# Rules
		self.h_rule = wx.StaticLine(self, -1, size=(350,2), style=wx.LI_HORIZONTAL)
		self.v_rule = wx.StaticLine(self, -1, size=(2,350), style=wx.LI_VERTICAL)
		
		# Options
		self.opt_verbose = wx.CheckBox(self, label="Verbose output")
		
		# Input field
		self.edit = wx.TextCtrl(self, size=wx.Size(250, -1))
		self.out_file = wx.TextCtrl(self, size=wx.Size(250, -1))
		
		# Buttons
		self.scan_button = wx.Button(self, label="Start Parse")
		self.browse_button = wx.Button(self, label="Browse...")
		self.out_browse_button = wx.Button(self, label="Browse...")
		
		# Button Binds
		self.edit.Bind(wx.EVT_TEXT_ENTER, self.on_scan_pressed)
		self.scan_button.Bind(wx.EVT_BUTTON, self.on_scan_pressed)
		self.browse_button.Bind(wx.EVT_BUTTON, self.on_file_browse)
		self.out_browse_button.Bind(wx.EVT_BUTTON, self.on_out_file_browse)
		
		# Output fields
		self.source = wx.TextCtrl(self, -1, style=wx.TE_MULTILINE|wx.BORDER_SUNKEN|
				wx.TE_READONLY|wx.TE_RICH2, size=(350,168))
		self.output = wx.TextCtrl(self, -1, style=wx.TE_MULTILINE|wx.BORDER_SUNKEN|
				wx.TE_READONLY|wx.TE_RICH2, size=(350,395))
		
		# File label
		self.v_sizer.Add(self.file_label, 0, wx.LEFT | wx.BOTTOM | wx.TOP, 5)
		
		# File browser
		self.h_sizer.Add(self.edit, 1)
		self.h_sizer.AddSpacer((5,0))
		self.h_sizer.Add(self.browse_button, 0)
		self.v_sizer.Add(self.h_sizer, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 5)
		self.v_sizer.AddSpacer((0,5))
		
		# Output file label
		self.v_sizer.Add(self.out_file_label, 0, wx.LEFT | wx.BOTTOM | wx.TOP, 5)
		
		# Output file browser
		self.h_sizer = wx.BoxSizer(wx.HORIZONTAL)
		self.h_sizer.Add(self.out_file, 1)
		self.h_sizer.AddSpacer((5,0))
		self.h_sizer.Add(self.out_browse_button, 0)
		self.v_sizer.Add(self.h_sizer, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 5)
		self.v_sizer.AddSpacer((0,10))
		
		# Options
		self.v_sizer.Add(self.options_label, 0, wx.LEFT | wx.BOTTOM, 5)
		self.v_sizer.Add(self.opt_verbose, 0, wx.LEFT, 10)
		self.v_sizer.AddSpacer((0,10))
		
		# Scan Button
		self.v_sizer.Add(self.scan_button, 0, wx.CENTER)
		self.v_sizer.AddSpacer((0,10))
		
		# Horizontal line
		self.v_sizer.Add(self.h_rule, 0, wx.CENTER)
		self.v_sizer.AddSpacer((0,10))
		
		# Source label
		self.v_sizer.Add(self.source_label, 0, wx.LEFT | wx.BOTTOM, 5)
		
		# Source box
		self.v_sizer.AddSpacer((5,0))
		self.v_sizer.Add(self.source, 0, wx.EXPAND | wx.BOTTOM, 5)
		
		# Add first column 
		self.h_sizer = wx.BoxSizer(wx.HORIZONTAL)
		self.h_sizer.Add(self.v_sizer, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 5)
		
		# Vertical Rule
		self.h_sizer.Add(self.v_rule, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 5)
		self.v_sizer = wx.BoxSizer(wx.VERTICAL)
		
		# Output label
		self.v_sizer.AddSpacer((0,5))
		self.v_sizer.Add(self.output_label, 0, wx.LEFT | wx.BOTTOM, 5)
		
		# Output box
		self.v_sizer.Add(self.output, 1, wx.EXPAND | wx.LEFT | wx.BOTTOM | wx.RIGHT, 5 )
		
		# Add second column
		self.h_sizer.Add(self.v_sizer, 1)

		self.SetSizer(self.h_sizer)
		self.h_sizer.Fit(self)
		self.SetMinSize(self.h_sizer.GetMinSize())
		self.edit.SetFocus()
		
	"""
	Event handler for scan button
	Runs Parser_Class.parse_file and puts output to 
	output fields
	"""
	def on_scan_pressed(self, event):
		# Clear output areas
		self.output.Clear()
		self.source.Clear()
		
		parser = Parser_Class()
		try:
			ret_code = parser.parse_file(self.edit.GetValue())
			
			self.source.AppendText(parser.source())
			
			# Output file
			if self.out_file.GetValue() != '':
				try:
					file = open(self.out_file.GetValue(), 'w')
					
					if self.opt_verbose.GetValue():
						for line in parser.output():
							file.write(str(line)+"\n")
					else:
						for line in parser.matches():
							file.write(str(line)+"\n")
					
					file.close()
				except Exception as strerror:
					self.show_error('Error: '+str(strerror))
			
			# Verbose output
			if self.opt_verbose.GetValue():
				for line in parser.output():
					self.output.AppendText(str(line+"\n"))
			# Match-only output
			else:
				for line in parser.matches():
					self.output.AppendText(str(line+"\n"))

			# Show errors
			if len(parser.error()) > 0:
				err_str = "There are errors in this source!\n\n"
				for error in parser.error():
					err_str += error+"\n"
				self.show_error(err_str)

			# Show status of parse
			if ret_code == 0 and len(parser.error()) == 0:
				self.show_message("Parse completed successfully!")

			elif ret_code == 0 and len(parser.error()) > 0:
				self.show_message("Parse completed with errors!")

			else:
				self.show_error("Parse failed!")
		
		except Exception as strerror:
			self.source.AppendText(scanner.source())
			for line in scanner.output():
					self.output.AppendText(str(line+"\n"))
			self.show_error('Error: '+str(strerror))
	
	"""
	Browse button event handler
	Displays file browser and sets the file input box to the file selected
	"""
	def on_file_browse(self, event):
		self.file_dialog = wx.FileDialog(self, message="Select a file", 
			defaultDir=".", defaultFile="source.txt", style=wx.OPEN)
		
		if self.file_dialog.ShowModal() == wx.ID_OK:
			self.edit.SetValue(self.file_dialog.GetPath())
			
	"""
	Browse button event handler
	Displays file browser and sets the file input box to the file selected
	"""
	def on_out_file_browse(self, event):
		self.file_dialog = wx.FileDialog(self, message="Select a file", 
			defaultDir=".", defaultFile="script.log", style=wx.OPEN)
		
		if self.file_dialog.ShowModal() == wx.ID_OK:
			self.out_file.SetValue(self.file_dialog.GetPath())
	
	"""
	Display an error message
	"""
	def show_error(self, msg):
		msg_box = wx.MessageDialog(self
			, msg
			, "Error"
			, wx.OK | wx.CENTRE | wx.ICON_EXCLAMATION)
			
		msg_box.ShowModal()
		
	"""
	Display an informational message
	"""
	def show_message(self, msg):
		msg_box = wx.MessageDialog(self
			, msg
			, "Info"
			, wx.OK | wx.CENTRE | wx.ICON_INFORMATION)

		msg_box.ShowModal()
		
	"""
	Exit button handler
	Closes the frame
	"""
	def on_exit_pressed(self, event):
		self.Close()
		
class wxParserApp(wx.App):

	"""
	Main Program Loop (GUI)
	"""
	def OnInit(self):
		# Send print statements to error.log
		self.RedirectStdio('./error.log')
		
		# Create new frame
		frame = wxParserFrame(None, title="Large Parser")
		
		# Show the frame
		frame.Show()
		
		# Focus on the new frame
		self.SetTopWindow(frame)

		return True

# End Parser GUI
