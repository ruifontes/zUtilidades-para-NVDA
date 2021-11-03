# -*- coding: utf-8 -*-
# Copyright (C) 2021 Héctor J. Benítez Corredera <xebolax@gmail.com>
# This file is covered by the GNU General Public License.

# import the necessary modules (NVDA)
import globalPluginHandler
import addonHandler
import gui
import globalVars
from scriptHandler import script, getLastScriptRepeatCount
from keyboardHandler import KeyboardInputGesture
import inputCore
from string import ascii_uppercase
from functools import wraps
import tones
import api
import watchdog
import core
import textInfos
import time
import wx
from threading import Thread
import re
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import varGlobal
from zLauncher import zl_modulo as zl
from zNotes import zn_modulo as zn
from comtypes.gen.ISimpleDOM import ISimpleDOMDocument
import controlTypes
# controlTypes module compatibility with old versions of NVDA
if not hasattr(controlTypes, "Role"):
	setattr(controlTypes, "Role", type('Enum', (), dict(
	[(x.split("ROLE_")[1], getattr(controlTypes, x)) for x in dir(controlTypes) if x.startswith("ROLE_")])))
	setattr(controlTypes, "State", type('Enum', (), dict(
	[(x.split("STATE_")[1], getattr(controlTypes, x)) for x in dir(controlTypes) if x.startswith("STATE_")])))
	setattr(controlTypes, "role", type("role", (), {"roleLabels": controlTypes.role._roleLabels}))
# End of compatibility fixes

# For translationn
addonHandler.initTranslation()

# Below toggle code came from Tyler Spivey's code, with enhancements by Joseph Lee.
def finally_(func, final):
	"""Calls final after func, even if it fails."""
	def wrap(f):
		@wraps(f)
		def new(*args, **kwargs):
			try:
				func(*args, **kwargs)
			finally:
				final()
		return new
	return wrap(final)

class GlobalPlugin(globalPluginHandler.GlobalPlugin):
	def __init__(self, *args, **kwargs):
		super(GlobalPlugin, self).__init__(*args, **kwargs)

		self._MainWindows = None
		if globalVars.appArgs.secure: return

		self.menu = wx.Menu()
		tools_menu = gui.mainFrame.sysTrayIcon.toolsMenu
		# Translators: Nombre del submenú para el lanzador de aplicaciones
		self.appLauncher = self.menu.Append(wx.ID_ANY, _("Lanzador de Aplicaciones"))
		gui.mainFrame.sysTrayIcon.Bind(wx.EVT_MENU, self.script_zLauncher, self.appLauncher)
		self.appNotes = self.menu.Append(wx.ID_ANY, _("Notas rápidas"))
		gui.mainFrame.sysTrayIcon.Bind(wx.EVT_MENU, self.script_zNotes, self.appNotes)
		# Translators: Nombre del menú zUtilidades
		self.zUtilidadesMenu = tools_menu.AppendSubMenu(self.menu, _("&zUtilidades"))

########## Inicio variables
##### Para el lanzador y notas
		self.categorias = []
		self.archivoCategorias = []
		self.temporal = []
		self.nombreAccion = []
##### Fin para el lanzador y notas
##### Inicio indices de categoría y item
		self.catIndexzl = 0
		self.catIndexzn = 0
		self.itemIndexzl = 0
		self.itemIndexzn = 0
		self.catTotalzl = 0
		self.catTotalzn = 0
		self.firstTimezl = True
		self.firstTimezn = True
##### Fin indices de categoría y item
##### Inicio banderas
		# Aqui guardaremos los enlaces a los gestos originales para restaurarlos despues
		self.oldGestureBindings = {}
		# Este flag nos indica si la capa de teclado esta activa o no
		self.toggling = False
# Para obtener la doble pulsación.
		self.doblePulsacion = False
# Para saber que modulo se activa.
		self.lanzador = ""
##### Fin banderas
########## Fin variables

	def terminate(self):
		try:
			if not self._MainWindows:
				self._MainWindows.Destroy()
		except (AttributeError, RuntimeError):
			pass

	@script(gesture=None, description= _("Con una pulsación Muestra la ventana del lanzador de aplicaciones, con doble pulsación el menú virtual del lanzador de aplicaciones"), category= _("zUtilidades"))
	def script_zLauncher(self, event):
		if getLastScriptRepeatCount() == 0:
			core.callLater(200, lambda: self.zlauncherClick(None))
		elif getLastScriptRepeatCount() == 1:
			self.doblePulsacion = True
			core.callLater(100, lambda: self.zlauncherDobleClick(None))

	def zlauncherClick(self, event):
		if self.doblePulsacion == False:
			if varGlobal.IS_WinON == False:
				self._MainWindows = HiloComplemento(1)
				self._MainWindows.start()
			else:
				msg = \
_("""Ya hay una instancia de zUtilidades abierta.

No es posible tener dos instancias a la vez.""")
				varGlobal.mensaje(msg)
		else:
			pass

	def zlauncherDobleClick(self, event):
		if self.doblePulsacion == True:
			if varGlobal.IS_WinON == False:
				self.lanzador = "zl"
				self.script_activarMenu(event)
				self.doblePulsacion = False
			else:
				msg = \
_("""Ya hay una instancia de zUtilidades abierta.

No es posible tener dos instancias a la vez.""")
				varGlobal.mensaje(msg)
				self.doblePulsacion = False
		else:
			self.doblePulsacion = False
			pass

	@script(gesture=None, description= _("Con una pulsación muestra la ventana de notas rápidas, con doble pulsación el menú virtual de notas rápidas"), category= _("zUtilidades"))
	def script_zNotes(self, event):
		if getLastScriptRepeatCount() == 0:
			core.callLater(200, lambda: self.znotaClick(None))
		elif getLastScriptRepeatCount() == 1:
			self.doblePulsacion = True
			core.callLater(100, lambda: self.znotaDobleClick(None))

	def znotaClick(self, event):
		if self.doblePulsacion == False:
			if varGlobal.IS_WinON == False:
				self._MainWindows = HiloComplemento(2)
				self._MainWindows.start()
			else:
				msg = \
_("""Ya hay una instancia de zUtilidades abierta.

No es posible tener dos instancias a la vez.""")
				varGlobal.mensaje(msg)
		else:
			pass

	def znotaDobleClick(self, event):
		if self.doblePulsacion == True:
			if varGlobal.IS_WinON == False:
				self.lanzador = "zn"
				self.script_activarMenu(event)
				self.doblePulsacion = False
			else:
				msg = \
_("""Ya hay una instancia de zUtilidades abierta.

No es posible tener dos instancias a la vez.""")
				varGlobal.mensaje(msg)
				self.doblePulsacion = False
		else:
			self.doblePulsacion = False
			pass

	@script(gesture=None, description= _("Con una pulsación agrega una nota rápida del texto seleccionado, con doble pulsación agrega una nueva nota rápida"), category= _("zUtilidades"))
	def script_zNotesCopy(self, gesture):
		if getLastScriptRepeatCount() == 0:
			core.callLater(200, lambda: self.selectNewNote(None))
		elif getLastScriptRepeatCount() == 1:
			self.doblePulsacion = True
			core.callLater(100, lambda: self.newNote(None))

	def selectNewNote(self, event):
		if self.doblePulsacion == False:
			if varGlobal.IS_WinON == False:
				# Inicio código obtenido de Buscador de definiciones de la RAE (DLEChecker) de Antonio Cascales
				obj = api.getFocusObject()
				selectedText = ""
				if hasattr(obj.treeInterceptor, 'TextInfo') and not obj.treeInterceptor.passThrough:
					try:
						info = obj.treeInterceptor.makeTextInfo(textInfos.POSITION_SELECTION)
					except (RuntimeError, NotImplementedError):
						info = None

					if not info or info.isCollapsed:
						varGlobal.mensaje(_("Seleccione un texto para poder agregar a una nota rápida"))
						return
					else:
						selectedText = info.text
				else:
					try:
						selectedText = obj.selection.text
					except (RuntimeError, NotImplementedError):
						varGlobal.mensaje(_("Seleccione un texto para poder agregar a una nota rápida"))
						return
					if obj.selection.text == "":
						varGlobal.mensaje(_("Seleccione un texto para poder agregar a una nota rápida"))
						return
				# Fin código obtenido de Buscador de definiciones de la RAE (DLEChecker) de Antonio Cascales
				if varGlobal.urlCaptura:
					url = self.getURL()
					selectedText = "\n\n".join([selectedText, url]) if url else selectedText
				self.lanzador = "zn"
				indiceNotes = varGlobal.dbDatos(os.path.join(zn.ajustes.dbDir, "index.dat")).CargaDatosIndex()
				self.NewCategorias =  varGlobal.AnalizaDatos(indiceNotes).GetCategoria()
				self.newArchivoCategorias = varGlobal.AnalizaDatos(indiceNotes).GetArchivosCat()
				if len(self.NewCategorias) == 0:
					msg = \
_("""No hay categorías para añadir una nota rápida.

Agregue una categoría antes para poder copiar un texto a una nota rápida.""")
					varGlobal.mensaje(msg)
					return

				self.windowsApp = AñadirNotaCopia(gui.mainFrame, self.NewCategorias, self.newArchivoCategorias, selectedText, 0)
				gui.mainFrame.prePopup()
				self.windowsApp.Show()
			else:
				msg = \
_("""Ya hay una instancia de zUtilidades abierta.

No es posible tener dos instancias a la vez.""")
				varGlobal.mensaje(msg)
		else:
			pass


	def getURL(self):
		""" Se obtiene la URL del documento para anexarla a la nota. """
		try:
			if api.getFocusObject().treeInterceptor.passThrough == False:
				from comtypes.gen.ISimpleDOM import ISimpleDOMDocument
				for obj in globalVars.focusAncestors:
					try:
						if obj.role == controlTypes.Role.DOCUMENT:
							# Thanks to Alberto Buffolino, who discovered this method. https://nvda-addons.groups.io/g/nvda-addons/message/12943
							doc = obj.IAccessibleObject.QueryInterface(ISimpleDOMDocument)
							return doc.url
					except:
						pass
			# Si el flujo llega hasta aquí es que no se ha encontrado el objeto documento. Lo buscamos de otra forma: desde el objeto enfocado hacia arriba en el árbol.
			obj = api.getFocusObject()
			while obj:
				try:
					if obj.role == controlTypes.Role.DOCUMENT:
						doc = obj.IAccessibleObject.QueryInterface(ISimpleDOMDocument)
						return doc.url
				except:
					pass
				obj = obj.parent
			return None
		except AttributeError:
			return None

	def newNote(self, event):
		if self.doblePulsacion == True:
			if varGlobal.IS_WinON == False:
				self.lanzador = "zn"
				indiceNotes = varGlobal.dbDatos(os.path.join(zn.ajustes.dbDir, "index.dat")).CargaDatosIndex()
				self.NewCategorias =  varGlobal.AnalizaDatos(indiceNotes).GetCategoria()
				self.newArchivoCategorias = varGlobal.AnalizaDatos(indiceNotes).GetArchivosCat()
				if len(self.NewCategorias) == 0:
					msg = \
_("""No hay categorías para añadir una nota rápida.

Agregue una categoría antes para poder crear una nota rápida.""")
					varGlobal.mensaje(msg)
					self.doblePulsacion = False
					return
				self.windowsApp = AñadirNotaCopia(gui.mainFrame, self.NewCategorias, self.newArchivoCategorias, None, 1)
				url = self.getURL()
				if url: self.windowsApp.textoNota.SetValue(url)
				gui.mainFrame.prePopup()
				self.windowsApp.Show()
				self.doblePulsacion = False
			else:
				msg = \
_("""Ya hay una instancia de zUtilidades abierta.

No es posible tener dos instancias a la vez.""")
				varGlobal.mensaje(msg)
				self.doblePulsacion = False
		else:
			self.doblePulsacion = False
			pass

########## Inicio menú virtual
	def leerCategoriaDAT(self):
		indiceLauncher = varGlobal.dbDatos(os.path.join(zl.ajustes.dbDir, "index.dat")).CargaDatosIndex()
		indiceNotes = varGlobal.dbDatos(os.path.join(zn.ajustes.dbDir, "index.dat")).CargaDatosIndex()

		self.categorias = []
		self.archivoCategorias = []
		if self.lanzador == "zl":
			self.categorias =  varGlobal.AnalizaDatos(indiceLauncher).GetCategoria()
			self.archivoCategorias = varGlobal.AnalizaDatos(indiceLauncher).GetArchivosCat()
			self.catTotalzl = len(self.categorias)
		elif self.lanzador == "zn":
			self.categorias =  varGlobal.AnalizaDatos(indiceNotes).GetCategoria()
			self.archivoCategorias = varGlobal.AnalizaDatos(indiceNotes).GetArchivosCat()
			self.catTotalzn = len(self.categorias)

		if self.lanzador == "zl":
			firstTimeTemporal = self.firstTimezl
		if self.lanzador == "zn":
			firstTimeTemporal = self.firstTimezn
		if firstTimeTemporal:
			if len(self.categorias) == 0:
				pass
			else:
				self.leerArchivosDAT(0)
		else:
			if len(self.categorias) == 0:
				pass
			else:
				if self.lanzador == "zl":
					self.leerArchivosDAT(self.catIndexzl)
				elif self.lanzador == "zn":
					self.leerArchivosDAT(self.catIndexzn)

	def leerArchivosDAT(self, valor):
		if self.lanzador == "zl":
			if self.catIndexzl > len(self.categorias)-1:
				valor = 0
		elif self.lanzador == "zn":
			if self.catIndexzn > len(self.categorias)-1:
				valor = 0

		if self.lanzador == "zl":
			del self.temporal[:]
			del self.nombreAccion[:]
			self.temporal = varGlobal.dbDatos(os.path.join(zl.ajustes.dbDir, self.archivoCategorias[valor])).CargaDatosDB()
			self.nombreAccion = varGlobal.AnalizaDatos(self.temporal).GetNombreDB()
		elif self.lanzador == "zn":
			del self.temporal[:]
			del self.nombreAccion[:]
			self.temporal = varGlobal.dbDatos(os.path.join(zn.ajustes.dbDir, self.archivoCategorias[valor])).CargaDatosDB()
			self.nombreAccion = varGlobal.AnalizaDatos(self.temporal).GetNombreDB()

	def getScript(self, gesture):
		if not self.toggling:
			return globalPluginHandler.GlobalPlugin.getScript(self, gesture)

		if not self.toggling or re.match("br(\(.+\))?", gesture.normalizedIdentifiers[0]):
			return globalPluginHandler.GlobalPlugin.getScript(self, gesture)

		script = globalPluginHandler.GlobalPlugin.getScript(self, gesture)

		if not script:
			if "kb:"+str("escape") in gesture.identifiers:
				script = finally_(self.script_exit, self.finish)
			else:
				script = finally_(self.script_speechHelp, lambda: None) 
		return script

	@script(gesture=None, description= None, category= None)
	def script_activarMenu(self, gesture):
		# Prevents the helper was launched when the keyboard is locked by the InputLock addon
		if inputCore.manager._captureFunc and not inputCore.manager._captureFunc(gesture): return

		if varGlobal.IS_WinON == True:
			msg = \
_("""Ya hay una instancia de zUtilidades abierta.

No es posible tener dos instancias a la vez.""")
			varGlobal.mensaje(msg)
			return

		self.leerCategoriaDAT()
		if len(self.categorias) == 0:
			varGlobal.mensaje(_("No hay categorías"))
			return

		varGlobal.IS_WinON = True
		if self.lanzador == "zl":
			catTotalTemporal = self.catTotalzl
		elif self.lanzador == "zn":
			catTotalTemporal = self.catTotalzn
		if catTotalTemporal == len(self.categorias):
			pass
		else:
			if self.lanzador == "zl":
				self.catIndexzl = 0
				self.itemIndexzl = -1
			elif self.lanzador == "zn":
				self.catIndexzn = 0
				self.itemIndexzn = -1
			if len(self.categorias) == 0:
				varGlobal.mensaje(_("No hay categorías"))
				varGlobal.IS_WinON = False
				return

		if self.toggling:
			self.script_exit(gesture)
			self.finish()
			return
		for k in ("upArrow", "downArrow", "leftArrow", "rightArrow", "enter", "shift+enter", "control+enter", "numpadEnter", "shift+numpadEnter", "control+numpadEnter", "escape", "backspace", "F1", "F12", "numpad2", "numpad4", "numpad5", "numpad6", "numpad8", "numpadPlus", "numpadMinus", "numpadDelete"):
			try:
				script = KeyboardInputGesture.fromName(k).script
			except KeyError:
				script = None
			if script and self != script.__self__:
				try:
					script.__self__.removeGestureBinding("kb:"+k)
				except KeyError:
					pass
				else:
					self.oldGestureBindings["kb:"+k] = script

		if self.lanzador == "zl":
			self.bindGestures(self.__zlmenuGestures)
		elif self.lanzador == "zn":
			self.bindGestures(self.__znmenuGestures)

		for c in ascii_uppercase:
			self.bindGesture("kb:"+c, "skipToCategory")

		if self.lanzador == "zn":
			self.bindGesture("kb:F1", "viewNote")
			self.bindGesture("kb:F2", "copyPP")
			self.bindGesture("kb:F3", "pastePP")

		self.toggling = True
		varGlobal.mensaje(_("Menú activado"))

		if self.lanzador == "zl":
			firstTimeTemporal = self.firstTimezl
		if self.lanzador == "zn":
			firstTimeTemporal = self.firstTimezn
		if firstTimeTemporal:
			self.script_speechHelp(None)
			if self.lanzador == "zl":
				self.firstTimezl = False
			elif self.lanzador == "zn":
				self.firstTimezn = False
			self.leerArchivosDAT(0)
			varGlobal.mensaje(self.categorias[0])
			if self.lanzador == "zl":
				self.catTotalzl = len(self.categorias)
			elif self.lanzador == "zn":
				self.catTotalzn = len(self.categorias)
		else:
			if self.lanzador == "zl":
				try:
					varGlobal.mensaje(self.categorias[self.catIndexzl])
				except:
					varGlobal.mensaje(self.categorias[0])
			elif self.lanzador == "zn":
				try:
					varGlobal.mensaje(self.categorias[self.catIndexzn])
				except:
					varGlobal.mensaje(self.categorias[0])

	def script_nextCategory(self, gesture):
		if self.lanzador == "zl":
			self.catIndexzl = self.catIndexzl+1 if self.catIndexzl < len(self.categorias)-1 else 0
			self.leerArchivosDAT(self.catIndexzl)
			varGlobal.mensaje(self.categorias[self.catIndexzl])
			self.itemIndexzl = -1
		elif self.lanzador == "zn":
			self.catIndexzn = self.catIndexzn+1 if self.catIndexzn < len(self.categorias)-1 else 0

			self.leerArchivosDAT(self.catIndexzn)
			varGlobal.mensaje(self.categorias[self.catIndexzn])
			self.itemIndexzn = -1

	def script_previousCategory(self, gesture):
		if self.lanzador == "zl":
			self.catIndexzl = self.catIndexzl -1 if self.catIndexzl > 0 else len(self.categorias)-1
			self.leerArchivosDAT(self.catIndexzl)
			varGlobal.mensaje(self.categorias[self.catIndexzl])
			self.itemIndexzl = -1
		elif self.lanzador == "zn":
			self.catIndexzn = self.catIndexzn -1 if self.catIndexzn > 0 else len(self.categorias)-1
			self.leerArchivosDAT(self.catIndexzn)
			varGlobal.mensaje(self.categorias[self.catIndexzn])
			self.itemIndexzn = -1

	def script_skipToCategory(self, gesture):
		if self.lanzador == "zl":
			categories = (self.categorias[self.catIndexzl+1:] if self.catIndexzl+1 < len(self.categorias) else []) + (self.categorias[:self.catIndexzl])
			try:
				self.catIndexzl = self.categorias.index(filter(lambda i: i[0].lower() == gesture.mainKeyName, categories).__next__())-1
			except AttributeError:
				try:
					self.catIndexzl = self.categorias.index(filter(lambda i: i[0].lower() == gesture.mainKeyName, categories)[0])-1
					self.script_nextCategory(None)
				except IndexError:
					if self.categorias[self.catIndexzl][0].lower() == gesture.mainKeyName:
						varGlobal.mensaje(self.categorias[self.catIndexzl])
					else:
						tones.beep(200, 30)
			except StopIteration:
				if self.categorias[self.catIndexzl][0].lower() == gesture.mainKeyName:
					varGlobal.mensaje(self.categorias[self.catIndexzl])
				else:
					tones.beep(200, 30)
			else:
				self.script_nextCategory(None)
		elif self.lanzador == "zn":
			categories = (self.categorias[self.catIndexzn+1:] if self.catIndexzn+1 < len(self.categorias) else []) + (self.categorias[:self.catIndexzn])
			try:
				self.catIndexzn = self.categorias.index(filter(lambda i: i[0].lower() == gesture.mainKeyName, categories).__next__())-1
			except AttributeError:
				try:
					self.catIndexzn = self.categorias.index(filter(lambda i: i[0].lower() == gesture.mainKeyName, categories)[0])-1
					self.script_nextCategory(None)
				except IndexError:
					if self.categorias[self.catIndexzn][0].lower() == gesture.mainKeyName:
						varGlobal.mensaje(self.categorias[self.catIndexzn])
					else:
						tones.beep(200, 30)
			except StopIteration:
				if self.categorias[self.catIndexzn][0].lower() == gesture.mainKeyName:
					varGlobal.mensaje(self.categorias[self.catIndexzn])
				else:
					tones.beep(200, 30)
			else:
				self.script_nextCategory(None)

	def script_nextItem(self, gesture):
		try:
			if self.lanzador == "zl":
				self.itemIndexzl = self.itemIndexzl + 1 if self.itemIndexzl < len(self.nombreAccion)-1 else 0
				varGlobal.mensaje(self.nombreAccion[self.itemIndexzl])
			elif self.lanzador == "zn":
				self.itemIndexzn = self.itemIndexzn + 1 if self.itemIndexzn < len(self.nombreAccion)-1 else 0
				varGlobal.mensaje(self.nombreAccion[self.itemIndexzn])
		except:
			if self.lanzador == "zl":
				varGlobal.mensaje(_("Sin acción"))
			if self.lanzador == "zn":
				varGlobal.mensaje(_("Sin notas"))

	def script_previousItem(self, gesture):
		try:
			if self.lanzador == "zl":
				self.itemIndexzl = self.itemIndexzl-1 if self.itemIndexzl > 0 else len(self.nombreAccion)-1
				varGlobal.mensaje(self.nombreAccion[self.itemIndexzl])
			elif self.lanzador == "zn":
				self.itemIndexzn = self.itemIndexzn-1 if self.itemIndexzn > 0 else len(self.nombreAccion)-1
				varGlobal.mensaje(self.nombreAccion[self.itemIndexzn])
		except:
			if self.lanzador == "zl":
				varGlobal.mensaje(_("Sin acción"))
			if self.lanzador == "zn":
				varGlobal.mensaje(_("Sin notas"))

	def script_executeCommand(self, gesture):
		if self.itemIndexzl < 0:
			varGlobal.mensaje(_("Use flechas derecha e izquierda para moverse por las categorías, flechas arriba y abajo para seleccionar item, enter para activarlo o escape para salir"))
			return

		if len(self.temporal) == 0:
			varGlobal.mensaje(_("Esta categoría no tiene acciones"))
			return
		else:
			varGlobal.mensaje(_("Ejecutando acción"))
			self.script_exit(None)
			valor = self.itemIndexzl
			if self.temporal[valor][0] == "app":
				if os.path.isfile(self.temporal[valor][2]):
					self.finish()
					if self.temporal[valor][5] == False:
						if self.temporal[valor][3] == False:
							varGlobal.ejecutar(None, "open", self.temporal[valor][2], None, os.path.dirname(self.temporal[valor][2]), 10)
						else:
							varGlobal.ejecutar(None, "open", self.temporal[valor][2], self.temporal[valor][4], os.path.dirname(self.temporal[valor][2]), 10)
					else:
						if self.temporal[valor][3] == False:
							varGlobal.ejecutar(None, "runas", self.temporal[valor][2], None, os.path.dirname(self.temporal[valor][2]), 10)
						else:
							varGlobal.ejecutar(None, "runas", self.temporal[valor][2], self.temporal[valor][4], os.path.dirname(self.temporal[valor][2]), 10)
				else:
					msg = \
_("""La ruta a la aplicación {}, no se encontró.

Ejecute el lanzador de aplicaciones en modo grafico para editar la acción.""").format(self.temporal[valor][1])
					varGlobal.mensaje(msg)
					self.finish()

			elif self.temporal[valor][0] == "cmd":
				self.finish()
				if self.temporal[valor][4] == False:
					if self.temporal[valor][3] == False:
						varGlobal.ejecutar(None, "open", "cmd.exe", "/c" + self.temporal[valor][2], None, 10)
					else:
						varGlobal.ejecutar(None, "open", "cmd.exe", "/c" + self.temporal[valor][2] + "&pause", None, 10)
				else:
					if self.temporal[valor][3] == False:
						varGlobal.ejecutar(None, "runas", "cmd.exe", "/c" + self.temporal[valor][2], None, 10)
					else:
						varGlobal.ejecutar(None, "runas", "cmd.exe", "/c" + self.temporal[valor][2] + "&pause", None, 10)

			elif self.temporal[valor][0] == "fol":
				if os.path.isdir(self.temporal[valor][2]):
					self.finish()
					varGlobal.ejecutar(None, "explore", self.temporal[valor][2], None, None, 10)
				else:
					msg = \
_("""La ruta a la carpeta no se encontró.

{}

Ejecute el lanzador de aplicaciones en modo grafico para editar la acción.""").format(self.temporal[valor][2])
					varGlobal.mensaje(msg)
					self.finish()

			elif self.temporal[valor][0] == "adr":
				if os.path.isfile(self.temporal[valor][2]):
					self.finish()
					if self.temporal[valor][3] == False:
						varGlobal.ejecutar(None, "open", self.temporal[valor][2], None, None, 10)
					else:
						varGlobal.ejecutar(None, "runas", self.temporal[valor][2], None, None, 10)
				else:
					msg = \
_("""La ruta al acceso directo no se encontró.

{}

Ejecute el lanzador de aplicaciones en modo grafico para editar la acción.""").format(self.temporal[valor][2])
					varGlobal.mensaje(msg)
					self.finish()

			elif self.temporal[valor][0] == "sap":
				self.finish()
				if self.temporal[valor][3] == False:
					varGlobal.ejecutar(None, "open", "explorer.exe", "shell:appsfolder\{}".format(self.temporal[valor][2]), None, 10)
				else:
					varGlobal.ejecutar(None, "runas", "explorer.exe", "shell:appsfolder\{}".format(self.temporal[valor][2]), None, 10)

	def script_viewNote(self, gesture):
		if self.itemIndexzn < 0:
			varGlobal.mensaje(_("Use flechas derecha e izquierda para moverse por las categorías, flechas arriba y abajo para seleccionar item, F1 para escuchar el contenido de la nota, F2 para copiar al portapapeles, F3 para pegar en el foco o escape para salir"))
			return

		if len(self.temporal) == 0:
			varGlobal.mensaje(_("Esta categoría no tiene notas"))
			return
		else:
			valor = self.itemIndexzn
			if self.temporal[valor][0] == "txt":
				varGlobal.mensaje(self.temporal[valor][2])

	def script_copyPP(self, gesture):
		if self.itemIndexzn < 0:
			varGlobal.mensaje(_("Use flechas derecha e izquierda para moverse por las categorías, flechas arriba y abajo para seleccionar item, F1 para escuchar el contenido de la nota, F2 para copiar al portapapeles, F3 para pegar en el foco o escape para salir"))
			return

		if len(self.temporal) == 0:
			varGlobal.mensaje(_("Esta categoría no tiene notas"))
			return
		else:
			valor = self.itemIndexzn
			self.dataObj = wx.TextDataObject()
			self.dataObj.SetText(self.temporal[valor][2])
			if wx.TheClipboard.Open():
				wx.TheClipboard.SetData(self.dataObj)
				wx.TheClipboard.Flush()
				varGlobal.mensaje(_("Se ha copiado la nota {} al portapapeles").format(self.temporal[valor][1]))
			else:
				varGlobal.mensaje(_("No se pudo copiar la nota {} al portapapeles").format(self.temporal[valor][1]))
			self.script_exit(None)
			self.finish()

	def script_pastePP(self, gesture):
		if self.itemIndexzn < 0:
			varGlobal.mensaje(_("Use flechas derecha e izquierda para moverse por las categorías, flechas arriba y abajo para seleccionar item, F1 para escuchar el contenido de la nota, F2 para copiar al portapapeles, F3 para pegar en el foco o escape para salir"))
			return

		if len(self.temporal) == 0:
			varGlobal.mensaje(_("Esta categoría no tiene notas"))
			return
		else:
			valor = self.itemIndexzn
			if self.temporal[valor][0] == "txt":
				self.script_exit(None)
				self.finish()
				paste = self.temporal[valor][2]
				# Source code taken from: frequentText add-on for NVDA. Written by Rui Fontes and Ângelo Abrantes
				try:
					clipboardBackup = api.getClipData()
				except:
					pass

				api.copyToClip(paste)
				time.sleep(0.1)
				api.processPendingEvents(False)
				focus = api.getFocusObject()
				if focus.windowClassName == "ConsoleWindowClass":
					# Windows console window - Control+V doesn't work here, so using an alternative method here
					WM_COMMAND = 0x0111
					watchdog.cancellableSendMessage(focus.windowHandle, WM_COMMAND, 0xfff1, 0)
				else:
					time.sleep(0.1)
					KeyboardInputGesture.fromName("Control+v").send()
				varGlobal.mensaje(_("Nota pegada en el foco"))
				try:
					core.callLater(300, lambda: api.copyToClip(clipboardBackup))
				except:
					pass

	def script_speechHelp(self, gesture):
		if self.lanzador == "zl":
			varGlobal.mensaje(_("Use flechas derecha e izquierda para moverse por las categorías, flechas arriba y abajo para seleccionar item, enter para activarlo o escape para salir"))
		elif self.lanzador == "zn":
			varGlobal.mensaje(_("Use flechas derecha e izquierda para moverse por las categorías, flechas arriba y abajo para seleccionar item, F1 para escuchar el contenido de la nota, F2 para copiar al portapapeles, F3 para pegar en el foco o escape para salir"))

	def script_exit(self, gesture):
		varGlobal.mensaje(_("Saliendo del menú"))

	def finish(self):
		varGlobal.IS_WinON = False
		if self.lanzador == "zl":
			self.catTotalzl = len(self.categorias)
		elif self.lanzador == "zn":
			self.catTotalzn = len(self.categorias)
		self.toggling = False
		self.clearGestureBindings()
#		self.bindGestures(self.__gestures)
		for key in self.oldGestureBindings:
			script = self.oldGestureBindings[key]
			if hasattr(script.__self__, script.__name__):
				script.__self__.bindGesture(key, script.__name__[7:])

	__zlmenuGestures = {
	"kb:rightArrow": "nextCategory",
	"kb:leftArrow": "previousCategory",
	"kb:downArrow": "nextItem",
	"kb:upArrow": "previousItem",
	"kb:enter": "executeCommand",
	"kb:numpadEnter": "executeCommand",
	}

	__znmenuGestures = {
	"kb:rightArrow": "nextCategory",
	"kb:leftArrow": "previousCategory",
	"kb:downArrow": "nextItem",
	"kb:upArrow": "previousItem",
	}
##########Fin menú virtual

class AñadirNotaCopia(wx.Dialog):
	def mensaje(self, mensaje, titulo, valor):
		if valor == 0:
			self.parametro = wx.OK | wx.ICON_INFORMATION
		elif valor == 1:
			self.parametro = wx.OK | wx.ICON_ERROR
		dlg = wx.MessageDialog(None, mensaje, titulo, self.parametro)
		dlg.SetOKLabel(_("&Aceptar"))
		dlg.ShowModal()
		dlg.Destroy()

	def leerArchivosDAT(self, valor):
		self.archivoNotas = os.path.join(zn.ajustes.dbDir, self.archivos[valor])
		self.dbNotas = zn.ajustes.dbNotas(self.archivoNotas)
		self.dbNotas.CargaDatos()
		temporal = self.dbNotas.notas
		nombresNotas = []
		for x in temporal:
			nombresNotas.append(x[1])
		return nombresNotas, temporal, self.dbNotas

	def guardaNotas(self, notasLista, obj):
		obj.notas = notasLista
		obj.GuardaDatos()

	def __init__(self, parent, categorias, archivos, texto, opcion):

		WIDTH = 1200
		HEIGHT = 850
		pos = varGlobal._calculatePosition(WIDTH, HEIGHT)

		if opcion == 0:
			super(AñadirNotaCopia, self).__init__(parent, -1, title=_("Agregar nota rápida del texto seleccionado"),pos = pos, size = (WIDTH, HEIGHT))
		if opcion == 1:
			super(AñadirNotaCopia, self).__init__(parent, -1, title=_("Añadir una nueva nota rápida"),pos = pos, size = (WIDTH, HEIGHT))

		self.categorias = categorias
		self.archivos = archivos
		self.texto = texto
		self.indice = 0
		self.listaNombres, self.temporal, self.guardar = self.leerArchivosDAT(self.indice)

#		if opcion == 0:
		varGlobal.IS_WinON = True

		self.Panel = wx.Panel(self)

		label1 = wx.StaticText(self.Panel, wx.ID_ANY, label=_("Seleccione una categoría donde guardar la nota rápida:"))
		self.choice = wx.Choice(self.Panel, wx.ID_ANY, choices = self.categorias) 
		self.choice.SetSelection(0)
		self.choice.Bind(wx.EVT_CHOICE, self.OnChoice)

		label2 = wx.StaticText(self.Panel, wx.ID_ANY, label=_("Introduzca el nombre de la Nota:"))
		self.textoNombre = wx.TextCtrl(self.Panel, wx.ID_ANY)
		if varGlobal.tituloCaptura:
			try:
				self.textoNombre.SetValue(api.getForegroundObject().name)
			except:
				self.textoNombre.SetValue(_("No se pudo capturar el título"))

		label3 = wx.StaticText(self.Panel, wx.ID_ANY, label=_("Contenido de la Nota:"))
		self.textoNota = wx.TextCtrl(self.Panel, wx.ID_ANY, style=wx.TE_MULTILINE)
		if opcion == 0:
			self.textoNota.SetValue(self.texto)

		self.AceptarBTN = wx.Button(self.Panel, 0, label=_("&Aceptar"))
		self.Bind(wx.EVT_BUTTON, self.onAceptar, id=self.AceptarBTN.GetId())

		self.CancelarBTN = wx.Button(self.Panel, wx.ID_CANCEL, label=_("&Cancelar"))
		self.Bind(wx.EVT_BUTTON, self.onCancelar, id=wx.ID_CANCEL)

		self.Bind(wx.EVT_CLOSE, self.onCancelar)

		sizeV = wx.BoxSizer(wx.VERTICAL)
		sizeH = wx.BoxSizer(wx.HORIZONTAL)

		sizeV.Add(label1, 0, wx.EXPAND)
		sizeV.Add(self.choice, 0, wx.EXPAND)

		sizeV.Add(label2, 0, wx.EXPAND)
		sizeV.Add(self.textoNombre, 0, wx.EXPAND)

		sizeV.Add(label3, 0, wx.EXPAND)
		sizeV.Add(self.textoNota, 1, wx.EXPAND)

		sizeH.Add(self.AceptarBTN, 2, wx.EXPAND)
		sizeH.Add(self.CancelarBTN, 2, wx.EXPAND)

		sizeV.Add(sizeH, 0, wx.EXPAND)

		self.Panel.SetSizer(sizeV)

		self.CenterOnScreen()

	def OnChoice(self, event):
		self.indice = event.GetSelection()
		self.listaNombres, self.temporal, self.guardar = self.leerArchivosDAT(self.indice)

	def onAceptar(self, event):
		if self.textoNombre.GetValue() == "":
			msg = \
_("""El campo no puede quedar en blanco.

Introduzca un nombre para añadir una Nota.""")
			self.mensaje(msg, _("Información"), 0)
			self.textoNombre.SetFocus()
		else:
			if self.textoNota.GetValue() == "":
				msg = \
_("""El campo no puede quedar en blanco.

Introduzca un texto para guardar la nota.""")
				self.mensaje(msg, _("Información"), 0)
				self.textoNota.SetFocus()
			else:
				listaTemporal = []
				for i in range(0, len(self.listaNombres)):
					listaTemporal.append(self.listaNombres[i])
				p = varGlobal.estaenlistado(listaTemporal, self.textoNombre.GetValue())
				if p == True:
					msg = \
_("""No puede duplicar el nombre de una Nota.

Modifique el nombre para poder continuar.""")
					self.mensaje(msg, _("Información"), 0)
					self.textoNombre.SetFocus()
				else:
					lista = ["txt", self.textoNombre.GetValue(), self.textoNota.GetValue()]
					self.temporal.append(lista)
					self.guardaNotas(self.temporal, self.guardar)
					varGlobal.IS_WinON = False
					self.Destroy()
					gui.mainFrame.postPopup()

	def onCancelar(self, event):
		varGlobal.IS_WinON = False
		self.Destroy()
		gui.mainFrame.postPopup()

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

		def zn_app():
			self.windowsApp = zn.zNotas(gui.mainFrame)
			gui.mainFrame.prePopup()
			self.windowsApp.Show()

		if self.opcion == 1:
			wx.CallAfter(zl_app)
		elif self.opcion == 2:
			wx.CallAfter(zn_app)
