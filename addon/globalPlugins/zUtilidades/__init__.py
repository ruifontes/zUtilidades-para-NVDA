# -*- coding: utf-8 -*-
# Copyright (C) 2021 Héctor J. Benítez Corredera <xebolax@gmail.com>
# This file is covered by the GNU General Public License.

# import the necessary modules (NVDA)
import globalPluginHandler
import addonHandler
import gui
import globalVars
from scriptHandler import script
import wx
from threading import Thread
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from zLauncher import zl_modulo as zl

# For translation
addonHandler.initTranslation()

class GlobalPlugin(globalPluginHandler.GlobalPlugin):
	def __init__(self):
		super(GlobalPlugin, self).__init__()

		self._MainWindows = None
		if globalVars.appArgs.secure:
			return

		self.menu = wx.Menu()
		tools_menu = gui.mainFrame.sysTrayIcon.toolsMenu
		# Translators: Nombre del submenú para el lanzador de aplicaciones
		self.appLauncher = self.menu.Append(wx.ID_ANY, _("Lanzador de Aplicaciones"))
		gui.mainFrame.sysTrayIcon.Bind(wx.EVT_MENU, self.script_zLauncher, self.appLauncher)
		# Translators: Nombre del menú zUtilidades
		self.zUtilidadesMenu = tools_menu.AppendSubMenu(self.menu, _("&zUtilidades"))

	def terminate(self):
		try:
			if not self._MainWindows:
				self._MainWindows.Destroy()
		except (AttributeError, RuntimeError):
			pass

	@script(gesture=None, description= _("Muestra la ventana del lanzador de aplicaciones"), category= _("zUtilidades"))
	def script_zLauncher(self, event):
		if zl.ajustes.IS_WinON == False:
			self._MainWindows = HiloComplemento(1)
			self._MainWindows.start()

class HiloComplemento(Thread):
	def __init__(self, opcion):
		super(HiloComplemento, self).__init__()
		self.daemon = True
		self.opcion = opcion
	def run(self):
		def zl_app():
			self.windowsApp = zl.zLanzador(gui.mainFrame)
			gui.mainFrame.prePopup()
			self.windowsApp.Show()

		if self.opcion == 1:
			wx.CallAfter(zl_app)
