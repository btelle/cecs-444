#!/usr/bin/python

"""
# Brandon Telle
# CECS 444 Assignment 2
# Baby Scanner GUI
# I alone wrote and modified what is turned in here
"""

import wx, sys
from scanner import Scanner_Class 

class wxScannerFrame(wx.Frame):
	
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
		self.file_label = wx.StaticText(self, label="File to scan:")
		self.options_label = wx.StaticText(self, label="Options:")
		self.source_label = wx.StaticText(self, label="Source text:")
		self.output_label = wx.StaticText(self, label="Scanner output:")
		self.h_rule = wx.StaticLine(self, -1, size=(350,2), style=wx.LI_HORIZONTAL)
		
		# Options
		self.opt_verbose = wx.CheckBox(self, label="Verbose output")
		
		# Input field
		self.edit = wx.TextCtrl(self, size=wx.Size(250, -1))
		
		# Buttons
		self.scan_button = wx.Button(self, label="Start scan")
		self.exit_button = wx.Button(self, label="Exit")
		self.browse_button = wx.Button(self, label="Browse...")
		
		#self.edit.Bind(wx.EVT_TEXT_ENTER, self.on_scan_pressed)
		self.scan_button.Bind(wx.EVT_BUTTON, self.on_scan_pressed)
		self.exit_button.Bind(wx.EVT_BUTTON, self.on_exit_pressed)
		self.browse_button.Bind(wx.EVT_BUTTON, self.on_file_browse)
		
		# Output fields
		self.source = wx.TextCtrl(self, -1, style=wx.TE_MULTILINE|wx.BORDER_SUNKEN|wx.TE_READONLY|
                                wx.TE_RICH2, size=(350,100))
		self.output = wx.TextCtrl(self, -1, style=wx.TE_MULTILINE|wx.BORDER_SUNKEN|wx.TE_READONLY|
                                wx.TE_RICH2, size=(350,200))

		
		# File label
		self.v_sizer.Add(self.file_label, 0, wx.LEFT | wx.BOTTOM | wx.TOP, 5)
		
		# File browser
		self.h_sizer.Add(self.edit, 1)
		self.h_sizer.AddSpacer((5,0))
		self.h_sizer.Add(self.browse_button, 0)
		self.v_sizer.Add(self.h_sizer, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 5)
		self.v_sizer.AddSpacer((0,10))
		
		# Options
		self.v_sizer.Add(self.options_label, 0, wx.LEFT | wx.BOTTOM, 5)
		self.v_sizer.Add(self.opt_verbose, 0, wx.LEFT, 10)
		self.v_sizer.AddSpacer((0,20))
		
		# Scan Button
		self.v_sizer.Add(self.scan_button, 0, wx.CENTER)
		self.v_sizer.AddSpacer((0,10))
		
		# Horizontal line
		self.v_sizer.Add(self.h_rule, 0, wx.CENTER)
		self.v_sizer.AddSpacer((0,20))
		
		# Source label
		self.v_sizer.Add(self.source_label, 0, wx.LEFT | wx.BOTTOM, 5)
		
		# Source box
		self.h_sizer = wx.BoxSizer(wx.HORIZONTAL)
		self.h_sizer.AddSpacer((5,0))
		self.h_sizer.Add(self.source, 1)
		
		self.v_sizer.Add(self.h_sizer, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 5)
		self.v_sizer.AddSpacer((0,20))
		
		# Output label
		self.v_sizer.Add(self.output_label, 0, wx.LEFT | wx.BOTTOM, 5)
		
		# Output box
		self.h_sizer = wx.BoxSizer(wx.HORIZONTAL)
		self.h_sizer.AddSpacer((5,0))
		self.h_sizer.Add(self.output, 1)
		
		self.v_sizer.Add(self.h_sizer, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 5)
		self.v_sizer.AddSpacer((0,10))
		
		# Exit button
		self.v_sizer.Add(self.exit_button, 0, wx.ALIGN_RIGHT | wx.BOTTOM | wx.RIGHT, 5)

		self.SetSizer(self.v_sizer)
		self.v_sizer.Fit(self)
		self.SetMinSize(self.v_sizer.GetMinSize())
		self.edit.SetFocus()
		
	"""
	Event handler for scan button and [return] key press
	Runs Scanner_Class.read_characters and outputs the 
	"""
	def on_scan_pressed(self, event):
		# Clear output areas
		self.output.Clear()
		self.source.Clear()
		
		scanner = Scanner_Class()
		try:
			scanner.read_characters(self.edit.GetValue())
			
			self.source.AppendText(scanner.source())
			
			if self.opt_verbose.GetValue():
				for line in scanner.output():
					self.output.AppendText(str(line+"\n"))
			else:
				for line in scanner.tokens():
					self.output.AppendText(str(line+"\n"))
			
			self.show_message("Scan completed successfully!")
		
		except Exception as strerror:
			self.source.AppendText(scanner.source())
			self.show_error('Error: '+str(strerror))
	
	"""
	Browse button event handler
	Displays file browser and sets the file input box to the file selected
	"""
	def on_file_browse(self, event):
		self.file_dialog = wx.FileDialog(self, message="Select a file", defaultDir=".", defaultFile="source.txt", style=wx.OPEN)
		if self.file_dialog.ShowModal() == wx.ID_OK:
			self.edit.SetValue(self.file_dialog.GetPath())
		else:
			print "what"
	
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
		
class wxScannerApp(wx.App):

	def OnInit(self):
		"""Main Program Loop (GUI)"""
		
		# Send print statements to error.log
		self.RedirectStdio('./error.log')
		
		# Create new frame
		frame = wxScannerFrame(None, title="Scanner")
		
		# Show the frame
		frame.Show()
		
		# Focus on the new frame
		self.SetTopWindow(frame)

		return True
