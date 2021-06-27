# -*- coding: utf-8 -*-
# Copyright (C) 2021 Héctor J. Benítez Corredera <xebolax@gmail.com>
# This file is covered by the GNU General Public License.

import addonHandler
import gui
import globalVars
from tones import beep
import ui
import api
import watchdog
import core
from keyboardHandler import KeyboardInputGesture
import time
import wx
import zipfile
import hashlib
from shutil import rmtree
from threading import Thread
import winsound
import os
import sys
import varGlobal
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import zn_ajustes as ajustes

# For translation
addonHandler.initTranslation()

class zNotas(wx.Dialog):
	def mensaje(self, mensaje, titulo, valor):
		if valor == 0:
			self.parametro = wx.OK | wx.ICON_INFORMATION
		elif valor == 1:
			self.parametro = wx.OK | wx.ICON_ERROR
		dlg = wx.MessageDialog(None, mensaje, titulo, self.parametro)
		dlg.SetOKLabel(_("&Aceptar"))
		dlg.ShowModal()
		dlg.Destroy()

	def __init__(self, parent):

		WIDTH = 1200
		HEIGHT = 850
		pos = varGlobal._calculatePosition(WIDTH, HEIGHT)

		super(zNotas,self).__init__(parent, -1, title=_("Notas rápidas"), pos = pos, size = (WIDTH, HEIGHT))

		self.archivoNotas = None
		self.dbNotas = None
		varGlobal.IS_WinON = True

		self.Panel = wx.Panel(self, 0)

		lbCategoria = wx.StaticText(self.Panel, wx.ID_ANY, label=_("&Categorías:"))
		self.lstCategorias = wx.ListBox(self.Panel, 1, style = wx.LB_NO_SB)
		self.lstCategorias.Bind(wx.EVT_LISTBOX,self.onRefrescar)
		self.lstCategorias.Bind(wx.EVT_CONTEXT_MENU,self.menuCategoria)
		self.lstCategorias.Bind(wx.EVT_KEY_UP, self.onTeclasCategoria)

		lbNotas = wx.StaticText(self.Panel, wx.ID_ANY, _("&Lista notas:"))
		self.lstNotas = wx.ListBox(self.Panel, 2, style = wx.LB_NO_SB)
		self.lstNotas.Bind(wx.EVT_CONTEXT_MENU,self.menuNotas)
		self.lstNotas.Bind(wx.EVT_KEY_UP, self.onTeclasNotas)
 
		self.menuBTN = wx.Button(self.Panel, 3, _("&Menú"))
		self.menuBTN.Bind(wx.EVT_BUTTON,self.menuBoton)

		self.Bind(wx.EVT_CHAR_HOOK, self.onkeyVentanaDialogo)
		self.Bind(wx.EVT_CLOSE, self.onSalir)

		szMain = wx.BoxSizer(wx.HORIZONTAL)
		szCategoria = wx.BoxSizer(wx.VERTICAL)
		szGeneral = wx.BoxSizer(wx.VERTICAL)

		szCategoria.Add(lbCategoria, 0)
		szCategoria.Add(self.lstCategorias, 1, wx.EXPAND)

		szGeneral.Add(lbNotas, 0, wx.EXPAND)
		szGeneral.Add(self.lstNotas, 1, wx.EXPAND)

		szGeneral.Add(self.menuBTN, 0, wx.EXPAND)

		szMain.Add(szCategoria, 0, wx.EXPAND)
		szMain.Add(szGeneral, 1, wx.EXPAND)

		self.Panel.SetSizer(szMain)

		self.onFocus()
		self.chkDatos()
		self.onRefrescar(None)
		ajustes.posicion = [0, 0]

		self.CenterOnScreen()

	def onFocus(self):
		""" Definimos los controles de todos los widgets"""
		self.Bind(wx.EVT_ACTIVATE, self.onSetFocus)
		self.Panel.Bind(wx.EVT_SET_FOCUS, self.onSetFocus)        
		# WidGets
		self.lstCategorias.Bind(wx.EVT_SET_FOCUS, self.onSetSelection)
		self.lstNotas.Bind(wx.EVT_SET_FOCUS, self.onSetSelection)
		# Botones
		self.menuBTN.Bind(wx.EVT_SET_FOCUS, self.onSetSelection)

	def onSetFocus(self, event):
		"""Devolvemos el foco al último widget que lo tubo"""
		if event.GetActive() == True:
			getattr(self, ajustes.focoActual).SetFocus()
			pass

	def onSetSelection(self, event):
		"""Guarda en la variable el widgetque tiene el foco"""
		id_widgets = {
# WidGets generales
			0:"Panel",
			1:"lstCategorias",
			2:"lstNotas",
			3:"menuBTN"
		}

		ajustes.focoActual = id_widgets.get(event.GetId())

	def chkDatos(self):
		tempDel = []
		for x in range(0, len(ajustes.nombreCategoria)):
			if os.path.isfile(os.path.join(ajustes.dbDir, ajustes.archivoCategoria[x])):
				pass
			else:
				ajustes.posicion = [0, 0]
				tempDel.append(x)

		for x in reversed(tempDel):
			del ajustes.nombreCategoria[x]
			del ajustes.archivoCategoria[x]

		ajustes.guardaCategorias()
		ajustes.refrescaCategorias()

		if len(ajustes.nombreCategoria) == 0:
			self.lstCategorias.Append(_("No hay categorías"))
			self.lstCategorias.SetSelection(0)
		else:
			self.lstCategorias.Append(ajustes.nombreCategoria)
			self.lstCategorias.SetSelection(ajustes.posicion[0])

		if self.lstCategorias.GetString(self.lstCategorias.GetSelection()) == _("No hay categorías"):
			self.lstNotas.Append(_("Sin notas"))
			self.lstNotas.SetSelection(0)
		else:
			self.onRefrescar(None)

	def onRefrescar(self, event):
		seleccion = self.lstCategorias.GetSelection()
		nombre =self.lstCategorias.GetString(self.lstCategorias.GetSelection())
		try:
			self.archivoNotas = os.path.join(ajustes.dbDir, ajustes.archivoCategoria[seleccion])
			self.dbNotas = ajustes.dbNotas(self.archivoNotas)
			self.dbNotas.CargaDatos()
			ajustes.notasLista = self.dbNotas.notas
			if len(ajustes.notasLista) == 0:
				self.lstNotas.Clear()
				self.lstNotas.Append(_("Sin notas"))
				self.lstNotas.SetSelection(0)
			else:
				self.lstNotas.Clear()
				for i in range(0, len(ajustes.notasLista)):
					self.lstNotas.Append(ajustes.notasLista[i][1])
				try:
					self.lstNotas.SetSelection(ajustes.posicion[1])
				except:
					self.lstNotas.SetSelection(0)
		except:
			self.lstNotas.Clear()
			self.lstNotas.Append(_("Sin notas"))
			self.lstNotas.SetSelection(0)

	def onPosicion(self):
		ajustes.posicion = [self.lstCategorias.GetSelection(), self.lstNotas.GetSelection()]

	def menuBoton(self, event):
		self.menu = wx.Menu()

		self.categoria = wx.Menu()
		itemAñadir = self.categoria.Append(1, _("&Añadir categoría"))
		self.Bind(wx.EVT_MENU, self.onMenuCategoria, itemAñadir)
		itemEditar = self.categoria.Append(2, _("&Editar categoría"))
		self.Bind(wx.EVT_MENU, self.onMenuCategoria, itemEditar)
		itemBorrar = self.categoria.Append(3, _("&Borrar categoría"))
		self.Bind(wx.EVT_MENU, self.onMenuCategoria, itemBorrar)
		self.menu.AppendSubMenu(self.categoria, _("&Categorías"))

		self.notas = wx.Menu()

		itemAñadirNota = self.notas.Append(4, _("&Añadir Nota"))
		self.Bind(wx.EVT_MENU, self.onMenuNotas, itemAñadirNota)
		itemEditar = self.notas.Append(10, _("&Editar Nota"))
		self.Bind(wx.EVT_MENU, self.onMenuNotas, itemEditar)
		itemBorrar = self.notas.Append(11, _("&Borrar Nota"))
		self.Bind(wx.EVT_MENU, self.onMenuNotas, itemBorrar)
		self.menu.AppendSubMenu(self.notas, _("&Notas"))

		self.copiaSeguridad = wx.Menu()
		itemHacer = self.copiaSeguridad.Append(20, _("&Hacer copia de seguridad"))
		self.Bind(wx.EVT_MENU, self.HacerBackup, itemHacer)
		itemRestaurar = self.copiaSeguridad.Append(21, _("&Restaurar copia de seguridad"))
		self.Bind(wx.EVT_MENU, self.RestaurarBackup, itemRestaurar)
		self.menu.AppendSubMenu(self.copiaSeguridad, _("&Hacer o restaurar copias de seguridad"))

		self.opciones = wx.Menu()
		itemdefecto = self.opciones.Append(wx.ID_ANY, _("&Volver a valores por defecto Notas rápidas"))
		self.Bind(wx.EVT_MENU, self.borrarValores, itemdefecto)
		self.menu.AppendSubMenu(self.opciones, _("&Opciones"))

		itemSalir = self.menu.Append(0, _("&Salir"))
		self.Bind(wx.EVT_MENU, self.onSalir, itemSalir)

		# Aqui lo que hace esto es llamar al constructor del menu para que se muestren los items centrados en la posición donde se encuentra el botón
		position = self.menuBTN.GetPosition()
		self.PopupMenu(self.menu,position)
		pass

	def menuCategoria(self, event):
		self.menu = wx.Menu()
		item1 = self.menu.Append(1, _("&Añadir categoría"))
		self.menu.Bind(wx.EVT_MENU, self.onMenuCategoria)
		item2 = self.menu.Append(2, _("&Editar categoría"))
		self.menu.Bind(wx.EVT_MENU, self.onMenuCategoria)
		item3 = self.menu.Append(3, _("&Borrar categoría"))
		self.menu.Bind(wx.EVT_MENU, self.onMenuCategoria)
		self.lstCategorias.PopupMenu(self.menu)

	def onMenuCategoria(self, event):
		id = event.GetId()
		nombreCategoria = self.lstCategorias.GetString(self.lstCategorias.GetSelection())
		if id == 1:
			dlg = AñadirCategoria(self)
			res = dlg.ShowModal()
			if res == 0:
				self.añadirCategoria(dlg.texto.GetValue())
			else:
				dlg.Destroy()
		elif id == 2:
			if nombreCategoria == _("No hay categorías"):
				msg = \
_("""No tiene ninguna categoría para Editar.

Agregue antes una para llevar a cabo esta acción.""")
				self.mensaje(msg, _("Información"), 0)
			else:
				dlg = EditarCategoria(self)
				res = dlg.ShowModal()
				if res == 0:
					self.editarCategoria(dlg.texto.GetValue())
				else:
					dlg.Destroy()
		elif id == 3:
			if nombreCategoria == _("No hay categorías"):
				msg = \
_("""No tiene ninguna categoría para Borrar.

Agregue antes una para llevar a cabo esta acción.""")
				self.mensaje(msg, _("Información"), 0)
			else:
				msg = \
_("""ADVERTENCIA:

Esta acción no es reversible.

Va a borrar la categoría:

{}

Tenga en cuenta que al borrar la categoría se eliminaran las notas que estuvieran en dicha categoría.

¿Esta seguro que desea continuar?""").format(nombreCategoria)
				MsgBox = wx.MessageDialog(None, msg, _("Pregunta"), wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION)
				ret = MsgBox.ShowModal()
				if ret == wx.ID_YES:
					MsgBox.Destroy
					idel = ajustes.nombreCategoria.index(nombreCategoria)
					ifile = ajustes.archivoCategoria[idel]
					del ajustes.nombreCategoria[idel]
					del ajustes.archivoCategoria[idel]
					ajustes.notasLista = []
					try:
						os.remove(os.path.join(ajustes.dbDir, ifile))
					except:
						pass
					ajustes.guardaCategorias()
					self.lstCategorias.Clear()
					if len(ajustes.nombreCategoria) == 0:
						self.lstCategorias.Append(_("No hay categorías"))
					else:
						self.lstCategorias.Append(ajustes.nombreCategoria)
					self.lstCategorias.SetSelection(0)
					self.onRefrescar(None)
				else:
					MsgBox.Destroy

	def añadirCategoria(self, valor):
		ajustes.nombreCategoria.append(valor)
		nombre_archivo_db = False
		while nombre_archivo_db == False:
			nombre_archivo_db =  varGlobal.comprobar_archivo_db(15, ajustes.archivoCategoria)
			pass
		archivo = os.path.join(ajustes.dbDir, nombre_archivo_db)
		ajustes.dbNotas(archivo).GuardaDatos()
		ajustes.archivoCategoria.append(nombre_archivo_db)
		ajustes.guardaCategorias()
		self.lstCategorias.Clear()
		if len(ajustes.nombreCategoria) == 0:
			self.lstCategorias.Append(_("No hay categorías"))
		else:
			self.lstCategorias.Append(ajustes.nombreCategoria)
		self.lstCategorias.SetSelection(ajustes.nombreCategoria.index(valor))
		self.onRefrescar(None)

	def editarCategoria(self, valor):
		indice = self.lstCategorias.GetSelection()
		del ajustes.nombreCategoria[indice]
		ajustes.nombreCategoria.insert(indice, valor)
		ajustes.guardaCategorias()
		self.lstCategorias.Clear()
		if len(ajustes.nombreCategoria) == 0:
			self.lstCategorias.Append(_("No hay categorías"))
		else:
			self.lstCategorias.Append(ajustes.nombreCategoria)
		self.lstCategorias.SetSelection(indice)
		self.onRefrescar(None)

	def onTeclasCategoria(self, event):
		if self.lstCategorias.GetSelection() == -1:
			pass
		else:
			if self.lstCategorias.GetString(self.lstCategorias.GetSelection()) == _("No hay categorías"):
				pass
			else:
				if (event.AltDown(), event.GetKeyCode()) == (True, 315):
					self.mueveCategoria("arriba")
					event.Skip()
				elif (event.AltDown(), event.GetKeyCode()) == (True, 317):
					self.mueveCategoria("abajo")
					event.Skip()

	def mueveCategoria(self, valor):
		indice = self.lstCategorias.GetSelection()
		if valor == "arriba":
			totalLista = len(ajustes.nombreCategoria) - 1
			if totalLista == -1:
				pass
			else:
				if indice == 0:
					beep(100,150)
				else:
					ajustes.nombreCategoria.insert(indice - 1, ajustes.nombreCategoria.pop(indice))
					ajustes.archivoCategoria.insert(indice - 1, ajustes.archivoCategoria.pop(indice))
					ajustes.guardaCategorias()
					self.lstCategorias.Clear()
					if len(ajustes.nombreCategoria) == 0:
						self.lstCategorias.Append(_("No hay categorías"))
					else:
						self.lstCategorias.Append(ajustes.nombreCategoria)
					self.lstCategorias.SetSelection(indice - 1)
				self.onRefrescar(None)
		elif valor == "abajo":
			totalLista = len(ajustes.nombreCategoria) - 1
			if totalLista == -1:
				pass
			else:
				if indice == totalLista:
					beep(200,150)
				else:
					ajustes.nombreCategoria.insert(indice + 1, ajustes.nombreCategoria.pop(indice))
					ajustes.archivoCategoria.insert(indice + 1, ajustes.archivoCategoria.pop(indice))
					ajustes.guardaCategorias()
					self.lstCategorias.Clear()
					if len(ajustes.nombreCategoria) == 0:
						self.lstCategorias.Append(_("No hay categorías"))
					else:
						self.lstCategorias.Append(ajustes.nombreCategoria)
					self.lstCategorias.SetSelection(indice + 1)
				self.onRefrescar(None)

	def menuNotas(self, event):
		self.menu = wx.Menu()

		itemAñadirNota = self.menu.Append(4, _("&Añadir Nota"))
		self.Bind(wx.EVT_MENU, self.onMenuNotas, itemAñadirNota)
		itemEditar = self.menu.Append(10, _("&Editar Nota"))
		self.Bind(wx.EVT_MENU, self.onMenuNotas, itemEditar)
		itemBorrar = self.menu.Append(11, _("&Borrar Nota"))
		self.Bind(wx.EVT_MENU, self.onMenuNotas, itemBorrar)
		self.lstNotas.PopupMenu(self.menu)

	def onMenuNotas(self, event):
		id = event.GetId()
		nombreCategoria = self.lstCategorias.GetString(self.lstCategorias.GetSelection())
		nombreItem = self.lstNotas.GetString(self.lstNotas.GetSelection())
		indice = self.lstNotas.GetSelection()
		if id == 4:
			if nombreCategoria == _("No hay categorías"):
				msg = \
_("""No tiene ninguna categoría.

Agregue una categoría antes para poder añadir una Nota.""")
				self.mensaje(msg, _("Información"), 0)
			else:
				dlg = AñadirNota(self)
				res = dlg.ShowModal()
				if res == 0:
					dlg.Destroy()
					ajustes.notasLista.append(dlg.lista)
					ajustes.guardaNotas(self.dbNotas)
					self.onRefrescar(None)
				else:
					dlg.Destroy()

		elif id == 10:
			if nombreCategoria == _("No hay categorías"):
				msg = \
_("""No tiene ninguna categoría.

Agregue una categoría antes para poder añadir una Nota.""")
				self.mensaje(msg, _("Información"), 0)
			else:
				if nombreItem == _("Sin notas"):
					msg = \
_("""No tiene ninguna Nota.

Agregue una antes para poder editar.""")
					self.mensaje(msg, _("Información"), 0)
				else:
					dlg = EditarNota(self)
					res = dlg.ShowModal()
					if res == 0:
						dlg.Destroy()
						del ajustes.notasLista[indice]
						ajustes.notasLista.insert(indice, dlg.lista)
						ajustes.guardaNotas(self.dbNotas)
						self.onRefrescar(None)
					else:
						dlg.Destroy()

		elif id == 11:
			if nombreCategoria == _("No hay categorías"):
				msg = \
_("""No tiene ninguna categoría.

Agregue una categoría antes para poder añadir una Nota.""")
				self.mensaje(msg, _("Información"), 0)
			else:
				if nombreItem == _("Sin notas"):
					msg = \
_("""No tiene ninguna Nota.

Agregue una antes para poder borrar.""")
					self.mensaje(msg, _("Información"), 0)
				else:
					msg = \
_("""ADVERTENCIA:

Esta acción no es reversible.

Va a borrar la Nota:

{}

¿Esta seguro que desea continuar?""").format(nombreItem)
					MsgBox = wx.MessageDialog(None, msg, _("Pregunta"), wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION)
					ret = MsgBox.ShowModal()
					if ret == wx.ID_YES:
						MsgBox.Destroy
						del ajustes.notasLista[indice]
						ajustes.guardaNotas(self.dbNotas)
						self.onRefrescar(None)
					else:
						MsgBox.Destroy

	def onTeclasNotas(self, event):
		if self.lstNotas.GetSelection() == -1:
			pass
		else:
			if self.lstNotas.GetString(self.lstNotas.GetSelection()) == _("Sin notas"):
				pass
			else:
				if event.GetKeyCode() == 32: # 13 Intro 32 Espacio
					self.visualiza(self.lstNotas.GetSelection())
				elif event.GetKeyCode() == 340: # F1 verbaliza nota
					self.onVerbaliza(self.lstNotas.GetSelection())
				elif event.GetKeyCode() == 341: # F2 copia al portapapeles
					self.onPortapapeles(self.lstNotas.GetSelection())
				elif event.GetKeyCode() == 342: # Shift+v pega en la app
					self.onPegar(event, self.lstNotas.GetSelection())

				elif (event.AltDown(), event.GetKeyCode()) == (True, 315):
					self.mueveAplicacion("arriba")
				elif (event.AltDown(), event.GetKeyCode()) == (True, 317):
					self.mueveAplicacion("abajo")
				event.Skip()

	def mueveAplicacion(self, valor):
		indice = self.lstNotas.GetSelection()
		if valor == "arriba":
			totalLista = len(ajustes.notasLista) - 1
			if totalLista == -1:
				pass
			else:
				if indice == 0:
					beep(100,150)
				else:
					ajustes.notasLista.insert(indice - 1, ajustes.notasLista.pop(indice))
					ajustes.guardaNotas(self.dbNotas)
					ajustes.posicion = [self.lstCategorias.GetSelection(), self.lstNotas.GetSelection() - 1]
					self.onRefrescar(None)
		elif valor == "abajo":
			totalLista = len(ajustes.notasLista) - 1
			if totalLista == -1:
				pass
			else:
				if indice == totalLista:
					beep(200,150)
				else:
					ajustes.notasLista.insert(indice + 1, ajustes.notasLista.pop(indice))
					ajustes.guardaNotas(self.dbNotas)
					ajustes.posicion = [self.lstCategorias.GetSelection(), self.lstNotas.GetSelection() + 1]
					self.onRefrescar(None)

	def visualiza(self, valor):
		dlg = VisualizarNota(self, self.lstNotas.GetString(valor), ajustes.notasLista[valor][2])
		res = dlg.ShowModal()
		if res == 0:
			dlg.Destroy()
		else:
			dlg.Destroy()

	def onVerbaliza(self, valor):
		ui.message(ajustes.notasLista[valor][2])

	def onPortapapeles(self, valor):
		self.dataObj = wx.TextDataObject()
		self.dataObj.SetText(ajustes.notasLista[valor][2])
		if wx.TheClipboard.Open():
			wx.TheClipboard.SetData(self.dataObj)
			wx.TheClipboard.Flush()
			ui.message(_("Se a copiado la nota {} al portapapeles.").format(self.lstNotas.GetString(self.lstNotas.GetSelection())))
		else:
			ui.message(_("No se a podido copiar la nota {} al portapapeles.").format(self.lstNotas.GetString(self.lstNotas.GetSelection())))

	def onPegar(self, event, valor):
		if ajustes.notasLista[valor][0] == "txt":
			self.Hide()
			event.Skip()
			paste = ajustes.notasLista[valor][2]
			# Source code taken from: frequentText add-on for NVDA. Written by Rui Fontes and Ângelo Abrantes
			clipboardBackup = api.getClipData()
			api.copyToClip(paste)
			time.sleep(0.1)
			api.processPendingEvents(False)
			focus = api.getFocusObject()
			if focus.windowClassName == "ConsoleWindowClass":
				# Windows console window - Control+V doesn't work here, so using an alternative method here
				WM_COMMAND = 0x0111
				watchdog.cancellableSendMessage(focus.windowHandle, WM_COMMAND, 0xfff1, 0)
			else:
				KeyboardInputGesture.fromName("Control+v").send()
			ui.message("Nota pegada en el foco.")
			core.callLater(300, lambda: api.copyToClip(clipboardBackup))
			self.onSalir(None)

	def HacerBackup(self, event):
		wildcard = _("Archivo copia de seguridad zUtilidades (*.zut-zn)|*.zut-zn")
		dlg = wx.FileDialog(self, message=_("Guardar en..."), defaultDir=os.getcwd(), defaultFile=varGlobal.fecha(), wildcard=wildcard, style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)
		if dlg.ShowModal() == wx.ID_OK:
			pathbackup = dlg.GetPath()
			fichero_final = os.path.basename(pathbackup)
			dlg.Destroy()
			dlg = BackupDialogo(_("Haciendo copia de seguridad..."), pathbackup)
			result = dlg.ShowModal()
			if result == 0:
				pass
			else:
				pass
			dlg.Destroy()
		else:
			dlg.Destroy()
			pass

	def RestaurarBackup(self, event):
		xguiMsg = \
_("""*** ADVERTENCIA ***

Esto borrara toda la base de datos de Notas rápidas

Toda la base de datos será sustituida por la copia de seguridad.

El complemento restaurara la copia de seguridad y se cerrara.

Esta acción no es reversible.

¿Desea continuar con el proceso?""")
		msg = wx.MessageDialog(None, xguiMsg, _("Pregunta"), wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION)
		ret = msg.ShowModal()
		if ret == wx.ID_YES:
			msg.Destroy
			wildcard = _("Archivo copia de seguridad zUtilidades (*.zut-zn)|*.zut-zn")
			dlgF = wx.FileDialog(None, message=_("Seleccione un archivo de copia de seguridad"), defaultDir=os.getcwd(), defaultFile="", wildcard=wildcard, style=wx.FD_OPEN | wx.FD_CHANGE_DIR | wx.FD_FILE_MUST_EXIST | wx.FD_PREVIEW)
			if dlgF.ShowModal() == wx.ID_OK:
				pathbackup = dlgF.GetPath()
				dlgF.Destroy()
				dlg = BackupDialogo(_("Restaurando copia de seguridad..."), pathbackup, True)
				result = dlg.ShowModal()
				if result == 0:
					dlg.Destroy()
					ajustes.refrescaCategoriasBackup()
					ajustes.posicion = [0, 0]
					varGlobal.IS_WinON = False
					ajustes.focoActual = "lstCategorias"
					self.Destroy()
					gui.mainFrame.postPopup()
				else:
					dlg.Destroy()
			else:
				dlgF.Destroy()
				getattr(self, ajustes.focoActual).SetFocus()
		else:
			msg.Destroy

	def borrarValores(self, event):
		xguiMsg = \
_("""*** ADVERTENCIA ***

Esto borrara toda la base de datos de Notas rápidas

El complemento borrara la base de datos y se cerrara.

Esta acción no es reversible.

¿Desea continuar con el proceso?""")
		msg = wx.MessageDialog(None, xguiMsg, _("Pregunta"), wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION)
		ret = msg.ShowModal()
		if ret == wx.ID_YES:
			msg.Destroy
			rmtree(ajustes.dbDir)
			if os.path.exists(ajustes.dbDir) == False:
				try:
					os.mkdir(os.path.join(globalVars.appArgs.configPath, "zUtilidades"))
				except:
					pass
				os.mkdir(ajustes.dbDir)
			del ajustes.nombreCategoria[:]
			del ajustes.archivoCategoria[:]
			ajustes.refrescaCategoriasBackup()
			ajustes.posicion = [0, 0]
			varGlobal.IS_WinON = False
			ajustes.focoActual = "lstCategorias"
			self.Destroy()
			gui.mainFrame.postPopup()
		else:
			msg.Destroy

	def onkeyVentanaDialogo(self, event):
		if event.GetKeyCode() == 27: # Pulsamos ESC y cerramos la ventana
			self.onPosicion()
			varGlobal.IS_WinON = False
			self.Destroy()
			gui.mainFrame.postPopup()
		else:
			event.Skip()

	def onSalir(self, event):
		self.onPosicion()
		varGlobal.IS_WinON = False
		self.Destroy()
		gui.mainFrame.postPopup()

class AñadirCategoria(wx.Dialog):
	def __init__(self, frame):

		super(AñadirCategoria, self).__init__(None, -1, title=_("Añadir categoría"))

		self.frame = frame
		self.Panel = wx.Panel(self)

		label1 = wx.StaticText(self.Panel, wx.ID_ANY, label=_("&Introduzca el nombre de la categoría:"))
		self.texto = wx.TextCtrl(self.Panel, wx.ID_ANY, style = wx.TE_PROCESS_ENTER)
		self.texto.Bind(wx.EVT_TEXT_ENTER, self.onPass)

		self.AceptarBTN = wx.Button(self.Panel, 0, label=_("&Aceptar"))
		self.Bind(wx.EVT_BUTTON, self.onAceptar, id=self.AceptarBTN.GetId())

		self.CancelarBTN = wx.Button(self.Panel, 1, label=_("&Cancelar"))
		self.Bind(wx.EVT_BUTTON, self.onCancelar, id=self.CancelarBTN.GetId())

		self.Bind(wx.EVT_CHAR_HOOK, self.onkeyVentanaDialogo)

		sizeV = wx.BoxSizer(wx.VERTICAL)
		sizeH = wx.BoxSizer(wx.HORIZONTAL)

		sizeV.Add(label1, 0, wx.EXPAND)
		sizeV.Add(self.texto, 0, wx.EXPAND)

		sizeH.Add(self.AceptarBTN, 2, wx.EXPAND)
		sizeH.Add(self.CancelarBTN, 2, wx.EXPAND)

		sizeV.Add(sizeH, 0, wx.EXPAND)

		self.Panel.SetSizer(sizeV)

		self.CenterOnScreen()

	def onPass(self, event):
		pass

	def onAceptar(self, event):
		if self.texto.GetValue() == "":
			msg = \
_("""El campo no puede quedar en blanco.

Introduzca un nombre para añadir una categoría.""")
			self.frame.mensaje(msg, _("Información"), 0)
			self.texto.SetFocus()
		else:
			p = varGlobal.estaenlistado(ajustes.nombreCategoria, self.texto.GetValue())
			if p == True:
				msg = \
_("""No puede duplicar el nombre de una categoría.

Modifique el nombre para poder continuar.""")
				self.frame.mensaje(msg, _("Información"), 0)
				self.texto.SetFocus()
			else:
				if self.IsModal():
					self.EndModal(event.EventObject.Id)
				else:
					self.Close()

	def onkeyVentanaDialogo(self, event):
		if event.GetKeyCode() == 27: # Pulsamos ESC y cerramos la ventana
			if self.IsModal():
				self.EndModal(1)
			else:
				self.Close()
		else:
			event.Skip()

	def onCancelar(self, event):
		if self.IsModal():
			self.EndModal(event.EventObject.Id)
		else:
			self.Close()

class EditarCategoria(wx.Dialog):
	def __init__(self, frame):

		super(EditarCategoria, self).__init__(None, -1, title=_("Editar categoría"))

		self.frame = frame
		self.Panel = wx.Panel(self)

		label1 = wx.StaticText(self.Panel, wx.ID_ANY, label=_("&Introduzca el nombre de la categoría:"))
		self.texto = wx.TextCtrl(self.Panel, wx.ID_ANY, style = wx.TE_PROCESS_ENTER)
		self.texto.Bind(wx.EVT_TEXT_ENTER, self.onPass)
		self.texto.SetValue(self.frame.lstCategorias.GetString(self.frame.lstCategorias.GetSelection()))

		self.AceptarBTN = wx.Button(self.Panel, 0, label=_("&Aceptar"))
		self.Bind(wx.EVT_BUTTON, self.onAceptar, id=self.AceptarBTN.GetId())

		self.CancelarBTN = wx.Button(self.Panel, 1, label=_("&Cancelar"))
		self.Bind(wx.EVT_BUTTON, self.onCancelar, id=self.CancelarBTN.GetId())

		self.Bind(wx.EVT_CHAR_HOOK, self.onkeyVentanaDialogo)

		sizeV = wx.BoxSizer(wx.VERTICAL)
		sizeH = wx.BoxSizer(wx.HORIZONTAL)

		sizeV.Add(label1, 0, wx.EXPAND)
		sizeV.Add(self.texto, 0, wx.EXPAND)

		sizeH.Add(self.AceptarBTN, 2, wx.EXPAND)
		sizeH.Add(self.CancelarBTN, 2, wx.EXPAND)

		sizeV.Add(sizeH, 0, wx.EXPAND)

		self.Panel.SetSizer(sizeV)

		self.CenterOnScreen()

	def onPass(self, event):
		pass

	def onAceptar(self, event):
		if self.texto.GetValue() == "":
			msg = \
_("""El campo no puede quedar en blanco.

Introduzca un nombre para añadir una categoría.""")
			self.frame.mensaje(msg, _("Información"), 0)
			self.texto.SetFocus()
		else:
			if self.frame.lstCategorias.GetString(self.frame.lstCategorias.GetSelection()) == self.texto.GetValue():
				if self.IsModal():
					self.EndModal(event.EventObject.Id)
				else:
					self.Close()
			else:
				p = varGlobal.estaenlistado(ajustes.nombreCategoria, self.texto.GetValue())
				if p == True:
					msg = \
_("""No puede duplicar el nombre de una categoría.

Modifique el nombre para poder continuar.""")
					self.frame.mensaje(msg, _("Información"), 0)
					self.texto.SetFocus()
				else:
					if self.IsModal():
						self.EndModal(event.EventObject.Id)
					else:
						self.Close()

	def onkeyVentanaDialogo(self, event):
		if event.GetKeyCode() == 27: # Pulsamos ESC y cerramos la ventana
			if self.IsModal():
				self.EndModal(1)
			else:
				self.Close()
		else:
			event.Skip()

	def onCancelar(self, event):
		if self.IsModal():
			self.EndModal(event.EventObject.Id)
		else:
			self.Close()

class AñadirNota(wx.Dialog):
	def __init__(self, frame):

		WIDTH = 1200
		HEIGHT = 850
		pos = varGlobal._calculatePosition(WIDTH, HEIGHT)

		super(AñadirNota, self).__init__(None, -1, title=_("Añadir Nota"), pos = pos, size = (WIDTH, HEIGHT))

		self.frame = frame
		self.lista = []

		self.Panel = wx.Panel(self)

		label1 = wx.StaticText(self.Panel, wx.ID_ANY, label=_("Introduzca el nombre de la Nota:"))
		self.textoNombre = wx.TextCtrl(self.Panel, wx.ID_ANY)

		label2 = wx.StaticText(self.Panel, wx.ID_ANY, label=_("Contenido de la Nota:"))
		self.textoNota = wx.TextCtrl(self.Panel, wx.ID_ANY, style=wx.TE_MULTILINE)

		self.AceptarBTN = wx.Button(self.Panel, 0, label=_("&Aceptar"))
		self.Bind(wx.EVT_BUTTON, self.onAceptar, id=self.AceptarBTN.GetId())

		self.CancelarBTN = wx.Button(self.Panel, 1, label=_("&Cancelar"))
		self.Bind(wx.EVT_BUTTON, self.onCancelar, id=self.CancelarBTN.GetId())

		self.Bind(wx.EVT_CHAR_HOOK, self.onkeyVentanaDialogo)

		sizeV = wx.BoxSizer(wx.VERTICAL)
		sizeH = wx.BoxSizer(wx.HORIZONTAL)

		sizeV.Add(label1, 0, wx.EXPAND)
		sizeV.Add(self.textoNombre, 0, wx.EXPAND)

		sizeV.Add(label2, 0, wx.EXPAND)
		sizeV.Add(self.textoNota, 1, wx.EXPAND)

		sizeH.Add(self.AceptarBTN, 2, wx.EXPAND)
		sizeH.Add(self.CancelarBTN, 2, wx.EXPAND)

		sizeV.Add(sizeH, 0, wx.EXPAND)

		self.Panel.SetSizer(sizeV)

		self.CenterOnScreen()

	def onAceptar(self, event):
		if self.textoNombre.GetValue() == "":
			msg = \
_("""El campo no puede quedar en blanco.

Introduzca un nombre para añadir una Nota.""")
			self.frame.mensaje(msg, _("Información"), 0)
			self.textoNombre.SetFocus()
		else:
			if self.textoNota.GetValue() == "":
				msg = \
_("""El campo no puede quedar en blanco.

Introduzca un texto para guardar la nota.""")
				self.frame.mensaje(msg, _("Información"), 0)
				self.textoNota.SetFocus()
			else:
				listaTemporal = []
				for i in range(0, len(ajustes.notasLista)):
					listaTemporal.append(ajustes.notasLista[i][1])
				p = varGlobal.estaenlistado(listaTemporal, self.textoNombre.GetValue())
				if p == True:
					msg = \
_("""No puede duplicar el nombre de una Nota.

Modifique el nombre para poder continuar.""")
					self.frame.mensaje(msg, _("Información"), 0)
					self.textoNombre.SetFocus()
				else:
					self.lista = ["txt", self.textoNombre.GetValue(), self.textoNota.GetValue()]
					if self.IsModal():
						self.EndModal(event.EventObject.Id)
					else:
						self.Close()

	def onkeyVentanaDialogo(self, event):
		if event.GetKeyCode() == 27: # Pulsamos ESC y cerramos la ventana
			if self.IsModal():
				self.EndModal(1)
			else:
				self.Close()
		else:
			event.Skip()

	def onCancelar(self, event):
		if self.IsModal():
			self.EndModal(event.EventObject.Id)
		else:
			self.Close()

class EditarNota(wx.Dialog):
	def __init__(self, frame):

		WIDTH = 1200
		HEIGHT = 850
		pos = varGlobal._calculatePosition(WIDTH, HEIGHT)

		super(EditarNota, self).__init__(None, -1, title=_("Editar Nota"), pos = pos, size = (WIDTH, HEIGHT))

		self.frame = frame
		self.indice = self.frame.lstNotas.GetSelection()
		self.lista = []

		self.Panel = wx.Panel(self)

		label1 = wx.StaticText(self.Panel, wx.ID_ANY, label=_("Introduzca el nombre de la Nota:"))
		self.textoNombre = wx.TextCtrl(self.Panel, wx.ID_ANY)
		self.textoNombre.SetValue(ajustes.notasLista[self.indice][1])

		label2 = wx.StaticText(self.Panel, wx.ID_ANY, label=_("Contenido de la nota:"))
		self.textoNota = wx.TextCtrl(self.Panel, wx.ID_ANY, style=wx.TE_MULTILINE)
		self.textoNota.SetValue(ajustes.notasLista[self.indice][2])

		self.AceptarBTN = wx.Button(self.Panel, 0, label=_("&Aceptar"))
		self.Bind(wx.EVT_BUTTON, self.onAceptar, id=self.AceptarBTN.GetId())

		self.CancelarBTN = wx.Button(self.Panel, 1, label=_("&Cancelar"))
		self.Bind(wx.EVT_BUTTON, self.onCancelar, id=self.CancelarBTN.GetId())

		self.Bind(wx.EVT_CHAR_HOOK, self.onkeyVentanaDialogo)

		sizeV = wx.BoxSizer(wx.VERTICAL)
		sizeH = wx.BoxSizer(wx.HORIZONTAL)

		sizeV.Add(label1, 0, wx.EXPAND)
		sizeV.Add(self.textoNombre, 0, wx.EXPAND)

		sizeV.Add(label2, 0, wx.EXPAND)
		sizeV.Add(self.textoNota, 1, wx.EXPAND)

		sizeH.Add(self.AceptarBTN, 2, wx.EXPAND)
		sizeH.Add(self.CancelarBTN, 2, wx.EXPAND)

		sizeV.Add(sizeH, 0, wx.EXPAND)

		self.Panel.SetSizer(sizeV)

		self.CenterOnScreen()

	def onAceptar(self, event):
		if self.textoNombre.GetValue() == "":
			msg = \
_("""El campo no puede quedar en blanco.

Introduzca un nombre para añadir una Nota.""")
			self.frame.mensaje(msg, _("Información"), 0)
			self.textoNombre.SetFocus()
		else:
			if self.textoNota.GetValue() == "":
				msg = \
_("""El campo no puede quedar en blanco.

Introduzca un texto para guardar la nota.""")
				self.frame.mensaje(msg, _("Información"), 0)
				self.textoNota.SetFocus()
			else:
				if self.textoNombre.GetValue() == ajustes.notasLista[self.indice][1]:
					self.lista = ["txt", self.textoNombre.GetValue(), self.textoNota.GetValue()]
					if self.IsModal():
						self.EndModal(event.EventObject.Id)
					else:
						self.Close()
				else:
					listaTemporal = []
					for i in range(0, len(ajustes.notasLista)):
						listaTemporal.append(ajustes.notasLista[i][1])
					p = varGlobal.estaenlistado(listaTemporal, self.textoNombre.GetValue())
					if p == True:
						msg = \
_("""No puede duplicar el nombre de una Nota.

Modifique el nombre para poder continuar.""")
						self.frame.mensaje(msg, "Información", 0)
						self.textoNombre.SetFocus()
					else:
						self.lista = ["txt", self.textoNombre.GetValue(), self.textoNota.GetValue()]
						if self.IsModal():
							self.EndModal(event.EventObject.Id)
						else:
							self.Close()

	def onkeyVentanaDialogo(self, event):
		if event.GetKeyCode() == 27: # Pulsamos ESC y cerramos la ventana
			if self.IsModal():
				self.EndModal(1)
			else:
				self.Close()
		else:
			event.Skip()

	def onCancelar(self, event):
		if self.IsModal():
			self.EndModal(event.EventObject.Id)
		else:
			self.Close()

class VisualizarNota(wx.Dialog):
	def __init__(self, frame, titulo, texto):

		WIDTH = 1200
		HEIGHT = 850
		pos = varGlobal._calculatePosition(WIDTH, HEIGHT)

		super(VisualizarNota, self).__init__(None, -1, title=titulo, pos = pos, size = (WIDTH, HEIGHT))

		self.texto = texto

		self.Panel = wx.Panel(self)

		label1 = wx.StaticText(self.Panel, wx.ID_ANY, label=_("Contenido de la Nota:"))
		self.textoNota = wx.TextCtrl(self.Panel, wx.ID_ANY, style=wx.TE_MULTILINE | wx.TE_READONLY)
		self.textoNota.AppendText(self.texto)
		self.textoNota.SetInsertionPoint(0)
		self.textoNota.Bind(wx.EVT_CONTEXT_MENU, self.CancelaFunciones)

		self.CerrarBTN = wx.Button(self.Panel, 1, label=_("&Cerrar"))
		self.Bind(wx.EVT_BUTTON, self.onCancelar, id=self.CerrarBTN.GetId())

		self.Bind(wx.EVT_CHAR_HOOK, self.onkeyVentanaDialogo)

		sizeV = wx.BoxSizer(wx.VERTICAL)

		sizeV.Add(label1, 0, wx.EXPAND)
		sizeV.Add(self.textoNota, 1, wx.EXPAND)
		sizeV.Add(self.CerrarBTN, 0, wx.EXPAND)

		self.Panel.SetSizer(sizeV)

		self.CenterOnScreen()

	def CancelaFunciones(self, event):
		pass

	def onkeyVentanaDialogo(self, event):
		if event.GetKeyCode() == 27: # Pulsamos ESC y cerramos la ventana
			if self.IsModal():
				self.EndModal(1)
			else:
				self.Close()
		else:
			event.Skip()

	def onCancelar(self, event):
		if self.IsModal():
			self.EndModal(event.EventObject.Id)
		else:
			self.Close()

class HiloBackup(Thread):
	def __init__(self, frame, nombreFichero, restore=False):
		super(HiloBackup, self).__init__()

		self.frame = frame
		self.nombreFichero = nombreFichero
		self.restore = restore
		self.daemon = True
		self.start()

	def comprimir_directorio(self, nombrezip, directorio):
		total = 0
		for root, dirs, files in os.walk(directorio):
			for fname in files:
				path = os.path.join(root, fname)
				total += os.path.getsize(path)
		basename = os.path.basename(directorio)
		z = zipfile.ZipFile(nombrezip, 'w', zipfile.ZIP_DEFLATED)
		current = 0
		for root, dirs, files in os.walk(directorio):
			for fname in files:
				path = os.path.join(root, fname)
				arcname = os.path.join(basename, fname)
				progress = (lambda x, y: (int(x), int(x*y) % y/y))(100 * current / total, 1e0)
				filename = os.path.basename(arcname)
				wx.CallAfter(self.frame.TextoRefresco, _("Comprimiendo el archivo: %s") % filename)
				wx.CallAfter(self.frame.next, progress[0])
				z.write(path, arcname)
				current += os.path.getsize(path)
		z.close()

	def descomprimir_zip(self, archivo, directorio_destino):
		zf = zipfile.ZipFile(archivo)
		uncompress_size = sum((file.file_size for file in zf.infolist()))
		extracted_size = 0
		for file in zf.infolist():
			extracted_size += file.file_size
			progress = (lambda x, y: (int(x), int(x*y) % y/y))((extracted_size * 100/uncompress_size), 1e0)
			filename = os.path.basename(file.filename)
			wx.CallAfter(self.frame.TextoRefresco, _("Descomprimiendo el archivo: %s") % filename)
			wx.CallAfter(self.frame.next, progress[0])
			zf.extract(file, directorio_destino)

	def ponerComentario(self, archivo, comentario):
		with zipfile.ZipFile(archivo, 'a') as zip:
			zip.comment = comentario.encode("utf-8")

	def leerComentario(self, archivo):
		archive = zipfile.ZipFile(archivo, 'r')
		return archive.comment.decode("utf-8")

	def generar_md5(self, text):
		return hashlib.md5(text).hexdigest()

	def generar_listaZIP(self, archivo):
		with zipfile.ZipFile(archivo, "r") as zip_ref:
			lista_ficheros = zip_ref.namelist()
		lista_unida = "-".join(lista_ficheros)
		return lista_unida.encode("utf-8")

	def chk_validez(self, archivo):
		p = self.leerComentario(archivo)
		if self.generar_md5(self.generar_listaZIP(archivo)) == p:
			return True
		else:
			return False

	def run(self):
		if self.restore == False:
			try:
# Creamos el archivo zip
				self.comprimir_directorio(self.nombreFichero, ajustes.dbDir)
# Creamos el md5 a partir de la lista de archivos del zip
				self.ponerComentario(self.nombreFichero, self.generar_md5(self.generar_listaZIP(self.nombreFichero)))
#Comprobamos el md5 del archivo con el md5 del comentario y si es correcto terminamos
				t = self.chk_validez(self.nombreFichero)
				if t == False:
					try:
						os.remove(self.nombreFichero)
					except:
						pass
					wx.CallAfter(self.frame.error, _("Algo salió mal.\n") + _("Inténtelo de nuevo.\n") + _("Ya puede cerrar esta ventana."))
				else:
					wx.CallAfter(self.frame.next, 100)
					wx.CallAfter(self.frame.done, _("La copia de seguridad fue un éxito.\n") + _("Ya puede cerrar esta ventana."))
			except:
				try:
					os.remove(self.nombreFichero)
				except:
					pass
				wx.CallAfter(self.frame.error, _("Algo salió mal.\n") + _("Inténtelo de nuevo.\n") + _("Ya puede cerrar esta ventana."))
		elif self.restore == True:
			try:
				t = self.chk_validez(self.nombreFichero)
				if t == False:
					wx.CallAfter(self.frame.error, _("Algo salió mal.\n") + _("Inténtelo de nuevo.\n") + _("Ya puede cerrar esta ventana."))
				else:
					rmtree(ajustes.dbDir)
					self.descomprimir_zip(self.nombreFichero, ajustes.dirRestaura)
				wx.CallAfter(self.frame.next, 100)
				wx.CallAfter(self.frame.done, _("Se completo la restauración correctamente.\n") + _("Ya puede cerrar esta ventana."))
			except:
				wx.CallAfter(self.frame.error, _("Algo salió mal.\n") + _("Inténtelo de nuevo.\n") + _("Ya puede cerrar esta ventana."))

class BackupDialogo(wx.Dialog):
	def __init__(self, titulo, nombreFichero, restore=False):

		super(BackupDialogo, self).__init__(None, -1, title=titulo)

		self.CenterOnScreen()

		self.nombreFichero = nombreFichero
		self.restore = restore

		self.Panel = wx.Panel(self)

		self.progressBar=wx.Gauge(self.Panel, wx.ID_ANY, range=100, style = wx.GA_HORIZONTAL)
		self.textorefresco = wx.TextCtrl(self.Panel, wx.ID_ANY, style =wx.TE_MULTILINE|wx.TE_READONLY)
		self.textorefresco.Bind(wx.EVT_CONTEXT_MENU, self.skip)

		self.AceptarTRUE = wx.Button(self.Panel, 0, _("&Aceptar"))
		self.Bind(wx.EVT_BUTTON, self.onAceptarTRUE, id=self.AceptarTRUE.GetId())
		self.AceptarTRUE.Disable()

		self.AceptarFALSE = wx.Button(self.Panel, 1, _("&Cerrar"))
		self.Bind(wx.EVT_BUTTON, self.onAceptarFALSE, id=self.AceptarFALSE.GetId())
		self.AceptarFALSE.Disable()

		self.Bind(wx.EVT_CLOSE, self.onNull)

		sizer = wx.BoxSizer(wx.VERTICAL)
		sizer_botones = wx.BoxSizer(wx.HORIZONTAL)

		sizer.Add(self.progressBar, 0, wx.EXPAND)
		sizer.Add(self.textorefresco, 1, wx.EXPAND)

		sizer_botones.Add(self.AceptarTRUE, 2, wx.CENTER)
		sizer_botones.Add(self.AceptarFALSE, 2, wx.CENTER)

		sizer.Add(sizer_botones, 0, wx.EXPAND)

		self.Panel.SetSizer(sizer)

		if self.restore == False:
			HiloBackup(self, self.nombreFichero)
		else:
			HiloBackup(self, self.nombreFichero, self.restore)

		self.textorefresco.SetFocus()

	def skip(self, event):
		return

	def onNull(self, event):
		pass

	def next(self, event):
		self.progressBar.SetValue(event)

	def TextoRefresco(self, event):
		self.textorefresco.Clear()
		self.textorefresco.AppendText(event)

	def done(self, event):
		winsound.MessageBeep(0)
		self.AceptarTRUE.Enable()
		self.textorefresco.Clear()
		self.textorefresco.AppendText(event)
		self.textorefresco.SetInsertionPoint(0) 

	def error(self, event):
		winsound.MessageBeep(16)
		self.AceptarFALSE.Enable()
		self.textorefresco.Clear()
		self.textorefresco.AppendText(event)
		self.textorefresco.SetInsertionPoint(0) 

	def onAceptarTRUE(self, event):
		if self.IsModal():
			self.EndModal(0)
		else:
			self.Close()

	def onAceptarFALSE(self, event):
		if self.IsModal():
			self.EndModal(1)
		else:
			self.Close()
