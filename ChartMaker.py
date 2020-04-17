#!/usr/bin/env python
import wx
from wx.html2 import WebView
import os
import codecs
import sys
import lxml.etree as ET

class WebPanel(wx.Panel):
	def __init__(self, parent):
		wx.Panel.__init__(self, parent)
		self.browser = WebView.New(self)
		bsizer = wx.BoxSizer()
		bsizer.Add(self.browser, 1, wx.EXPAND)
		self.SetSizerAndFit(bsizer)
		htmlText = "<p>Please open a file to convert from File Menu.</p>"
		self.browser.SetPage(htmlText, "")



class Window(wx.Frame):
	def __init__(self, parent, title):
		wx.Frame.__init__(self, parent, title=title, size=(1920,1080))
		self.dirname=""
		self.filename=""
		self.CreateStatusBar()
		fileMenu= wx.Menu()
		openMenu = fileMenu.Append(wx.ID_OPEN)
		self.Bind(wx.EVT_MENU, self.onOpen, openMenu)
		exitMenu = fileMenu.Append(wx.ID_EXIT)
		self.Bind(wx.EVT_MENU, self.OnExit, exitMenu)
		menuBar = wx.MenuBar()
		menuBar.Append(fileMenu,"&File")
		self.SetMenuBar(menuBar)
		self.WebPanel = WebPanel(self)
		self.Bind(wx.EVT_CLOSE, self.onClose, self)
		bsizer = wx.BoxSizer()
		bsizer.Add(self.WebPanel, 1, wx.EXPAND)
		self.SetSizerAndFit(bsizer)
		self.Show(True)
		self.Maximize(True)
		self.SetTitle("JamBRL")
		#self.focus()
		if len(sys.argv) > 1:
			self.dirname = os.path.dirname(sys.argv[1])
			self.filename = os.path.basename(sys.argv[1])
			self.open()
		self.focus()

	def open(self):
		self.file = os.path.join(self.dirname, self.filename)
		self.htmlText = self.convert()
		self.WebPanel.browser.SetPage(self.htmlText, "")
		self.SetTitle(self.filename+" | JamBRL")
		file = self.file.replace(".xml", ".html")
		output = open(file, "wb")
		output.write(self.htmlText)

	def onOpen(self,e):
		with wx.FileDialog(self, "Open", self.dirname, "", "*.xml", style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as dlg:
			if dlg.ShowModal() == wx.ID_CANCEL: return
			self.filename = dlg.GetFilename()
			self.dirname = dlg.GetDirectory()
			self.open()

	def OnExit(self,e):
		self.Close(True)

	def onClose(self, event):
		self.Destroy()
	
	def focus(self):
		focus = self.WebPanel.browser
		focus.SetFocus()
		robot = wx.UIActionSimulator()  
		position = focus.GetPosition() 
		position = focus.ClientToScreen(position) 
		robot.MouseMove(position) 
		robot.MouseClick()    

	def convert(self):
		dom = ET.parse(self.file)
		if getattr(sys, 'frozen', False):
			base = sys._MEIPASS
		else: base = os.path.dirname(os.path.abspath(__file__))
		xslt = ET.parse(os.path.join(base, "jambrl.xsl"))
		transform = ET.XSLT(xslt)
		newdom = transform(dom)
		return ET.tostring(newdom, pretty_print=True)

app = wx.App(False)
frame = Window(None, title="Markdown Editor")
app.MainLoop()
